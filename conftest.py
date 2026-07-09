from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
from selenium import webdriver

from config import DEFAULT_BROWSER, HEADLESS
from results.collector import (
    build_execution_result,
    get_marker_value,
    make_run_id,
    save_result_manifest,
    set_user_property,
)
from results.exporters import export_csv
from results.models import ExecutionResult
from workbook.module_registry import MODULES_BY_CODE
from workbook.parser import validate_workbook_contract
from workbook.updater import append_results_to_workbook

RESULTS_DIR = Path(__file__).parent / "results"
ARTIFACTS_DIR = Path(__file__).parent / "artifacts"

EXECUTION_RESULTS: list[ExecutionResult] = []


def _make_driver(browser_name: str):
    browser_name = browser_name.lower()

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        return webdriver.Chrome(options=options)

    if browser_name == "edge":
        options = webdriver.EdgeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        return webdriver.Edge(options=options)

    if browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if HEADLESS:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1440, 1000)
        return driver

    raise ValueError(
        f"Unsupported BROWSER={browser_name!r}. "
        "Use chrome, edge, or firefox for this automation project."
    )


def _actual_browser_name(driver) -> str:
    browser_name = driver.capabilities.get("browserName") if driver else None
    if browser_name:
        return str(browser_name).capitalize()
    return DEFAULT_BROWSER.capitalize()


def _actual_browser_version(driver) -> str:
    if not driver:
        return ""
    return str(driver.capabilities.get("browserVersion") or driver.capabilities.get("version") or "")


def _current_url(driver) -> str:
    if not driver:
        return ""
    try:
        return str(driver.current_url)
    except Exception:
        return ""


@pytest.fixture
def driver():
    driver = _make_driver(DEFAULT_BROWSER)
    driver.implicitly_wait(0)
    yield driver
    driver.quit()


@pytest.fixture
def record_actual_result(request):
    def _record(message: str) -> None:
        set_user_property(request.node, "actual_result", message)
        set_user_property(request.node, "observed_summary", message)

    return _record


def pytest_addoption(parser):
    parser.addoption(
        "--workbook-path",
        action="store",
        default="",
        help="Path to the ground-truth SauceDemo workbook. When provided, results append to a saved workbook copy.",
    )
    parser.addoption(
        "--workbook-output",
        action="store",
        default="",
        help="Optional output path for the updated workbook copy.",
    )
    parser.addoption(
        "--workbook-in-place",
        action="store_true",
        help="Deliberately update the workbook in place. A timestamped backup is created first.",
    )
    parser.addoption(
        "--no-csv",
        action="store_true",
        help="Disable CSV fallback export.",
    )
    parser.addoption(
        "--case-id",
        action="store",
        default="",
        help="Run only tests marked with the exact workbook Case ID.",
    )
    parser.addoption(
        "--module-code",
        action="store",
        default="",
        help="Run only tests whose Case ID starts with the workbook module code, e.g. LG.",
    )
    parser.addoption(
        "--run-only-automated",
        action="store_true",
        default=True,
        help="Run only executable automated pytest cases; manual workbook cases are never materialized as rows.",
    )


def pytest_configure(config):
    EXECUTION_RESULTS.clear()
    RESULTS_DIR.mkdir(exist_ok=True)
    ARTIFACTS_DIR.mkdir(exist_ok=True)
    workbook_path = config.getoption("--workbook-path")
    if workbook_path:
        path = Path(workbook_path)
        if not path.exists():
            raise pytest.UsageError(f"--workbook-path does not exist: {workbook_path}")
        errors = validate_workbook_contract(path)
        if errors:
            raise pytest.UsageError("Workbook contract validation failed:\n" + "\n".join(errors))

    started_at = datetime.now(timezone.utc)
    config._execution_started_at = started_at
    config._run_id = make_run_id(started_at)
    config.addinivalue_line("markers", "case_id(value): exact workbook Case ID for this automated test.")
    config.addinivalue_line("markers", "module(value): exact workbook Module value for this automated test.")
    config.addinivalue_line("markers", "test_user(value): workbook Test User value actually exercised.")
    config.addinivalue_line("markers", "actual_result(value): default passing Actual Result text.")


def pytest_collection_modifyitems(config, items):
    wanted_case_id = config.getoption("--case-id")
    wanted_module_code = config.getoption("--module-code").upper()
    if wanted_module_code and wanted_module_code not in MODULES_BY_CODE:
        raise pytest.UsageError(f"Unknown --module-code {wanted_module_code!r}. Use one of: {', '.join(MODULES_BY_CODE)}")

    collection_errors: list[str] = []
    for item in items:
        is_selenium_workbook_test = "driver" in getattr(item, "fixturenames", ())
        case_id = get_marker_value(item, "case_id")
        module = get_marker_value(item, "module")
        if is_selenium_workbook_test and (not case_id or not module):
            collection_errors.append(f"{item.nodeid} is a Selenium workbook test missing case_id/module marker.")
            continue

        if wanted_case_id and case_id != wanted_case_id:
            item.add_marker(pytest.mark.skip(reason=f"Only running workbook Case ID {wanted_case_id}"))
            continue
        if wanted_module_code and not case_id.startswith(f"{wanted_module_code}-"):
            item.add_marker(pytest.mark.skip(reason=f"Only running workbook module {wanted_module_code}"))

    if collection_errors:
        raise pytest.UsageError("Workbook metadata errors:\n" + "\n".join(collection_errors))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when not in {"setup", "call"}:
        return
    if report.skipped:
        return
    if report.when == "setup" and report.passed:
        return
    if getattr(item, "_execution_result_recorded", False):
        return

    driver = item.funcargs.get("driver")
    browser = _actual_browser_name(driver)
    browser_version = _actual_browser_version(driver)
    current_url = _current_url(driver)
    run_id = item.config._run_id

    if report.failed and driver is not None:
        evidence_dir = ARTIFACTS_DIR / run_id
        evidence_dir.mkdir(parents=True, exist_ok=True)
        case_id = item.get_closest_marker("case_id")
        case_label = str(case_id.args[0]) if case_id and case_id.args else item.name
        safe_case = case_label.replace("/", "_").replace("\\", "_")
        screenshot = evidence_dir / f"{safe_case}_{browser.lower()}_failure.png"
        html = evidence_dir / f"{safe_case}_{browser.lower()}_page.html"
        try:
            driver.save_screenshot(str(screenshot))
            html.write_text(driver.page_source, encoding="utf-8")
            set_user_property(item, "evidence_path", str(screenshot))
        except Exception as exc:  # pragma: no cover - best-effort evidence capture
            set_user_property(item, "evidence_path", f"evidence capture failed: {exc}")

    result = build_execution_result(
        item,
        report,
        run_id=run_id,
        browser=browser,
        artifacts_dir=ARTIFACTS_DIR,
        browser_version=browser_version,
        current_url=current_url,
    )
    if result is None:
        return

    EXECUTION_RESULTS.append(result)
    item._execution_result_recorded = True


def pytest_sessionfinish(session, exitstatus):
    if not EXECUTION_RESULTS:
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = session.config._run_id
    manifest_path = RESULTS_DIR / f"execution_manifest_{run_id}.json"
    save_result_manifest(manifest_path, run_id, EXECUTION_RESULTS)
    print(f"\nExecution manifest written to: {manifest_path}")

    if not session.config.getoption("--no-csv"):
        csv_path = RESULTS_DIR / f"test_execution_log_{stamp}.csv"
        export_csv(csv_path, EXECUTION_RESULTS)
        print(f"Workbook-compatible execution CSV written to: {csv_path}")

    workbook_path = session.config.getoption("--workbook-path")
    if workbook_path:
        output_path = session.config.getoption("--workbook-output") or None
        updated_path = append_results_to_workbook(
            workbook_path,
            EXECUTION_RESULTS,
            output_path=output_path,
            in_place=session.config.getoption("--workbook-in-place"),
        )
        print(f"Updated workbook written to: {updated_path}")
