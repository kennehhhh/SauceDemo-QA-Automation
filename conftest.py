from __future__ import annotations

import csv
import os
import platform
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest
from selenium import webdriver

from config import DEFAULT_BROWSER, HEADLESS

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

EXECUTION_ROWS: list[dict[str, str]] = []


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


@pytest.fixture
def driver():
    driver = _make_driver(DEFAULT_BROWSER)
    driver.implicitly_wait(0)
    yield driver
    driver.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--test-user",
        action="store",
        default="standard_user",
        help="Workbook Test User value recorded in the execution export.",
    )


def pytest_configure(config):
    config._execution_started_at = time.time()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    match = re.search(r"(CW-\d{4})", item.name)
    case_id = match.group(1) if match else item.get_closest_marker("case_id")
    if not case_id:
        return

    status = "Passed" if report.passed else ("Failed" if report.failed else "Blocked")
    actual_result = "Automated workflow completed as expected." if report.passed else str(report.longrepr)

    EXECUTION_ROWS.append({
        "Execution ID": "",
        "Case ID": str(case_id),
        "Module": "Core Workflows",
        "Test User": item.config.getoption("--test-user"),
        "Browser": DEFAULT_BROWSER.capitalize(),
        "Actual Result": actual_result[:2000],
        "Status": status,
        "Related Defect ID": "",
        "Tester": os.getenv("TESTER_NAME", platform.node()),
        "Execution Date": datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z"),
        "Remarks": "Automated by Selenium + pytest",
    })


def pytest_sessionfinish(session, exitstatus):
    if not EXECUTION_ROWS:
        return

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = RESULTS_DIR / f"test_execution_log_{stamp}.csv"
    fields = [
        "Execution ID", "Case ID", "Module", "Test User", "Browser",
        "Actual Result", "Status", "Related Defect ID", "Tester",
        "Execution Date", "Remarks",
    ]

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for idx, row in enumerate(EXECUTION_ROWS, start=1):
            row = dict(row)
            row["Execution ID"] = f"EXE-{idx:04d}"
            writer.writerow(row)

    print(f"\nWorkbook-compatible execution CSV written to: {path}")
