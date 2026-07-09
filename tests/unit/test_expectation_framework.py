from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from openpyxl import Workbook

from results.collector import build_execution_result, set_user_property
from workbook.expectation_policy import ExpectationBlocked, ExpectationMode
from workbook.expectations import load_expectation_cases, safe_preflight_case_ids, validate_expectation_dependencies


HEADERS = [
    "Case ID",
    "Test Category",
    "Module",
    "Test Case / Scenario",
    "Preconditions",
    "Test Data",
    "Test Steps",
    "Expected Result",
    "Applicable User",
    "Browser Coverage",
    "Remarks",
    "Automation Candidate",
]


def make_expectation_workbook(path: Path) -> Path:
    wb = Workbook()
    ws = wb.active
    ws.title = "Login & Session - TC"
    ws.append(["Login & Session Test Cases"])
    ws.append(["Module Code: LG"])
    ws.append(HEADERS)
    ws.append(["LG-0028", "System", "Login & Session", "Remember Me option is available", "", "", "", "", "standard_user", "Primary Browser", "Standard feature expectation", "Yes"])
    ws.append(["LG-0029", "System", "Login & Session", "Remember Me persists intended login convenience", "", "", "", "", "standard_user", "Primary Browser", "Standard feature expectation", "Yes"])
    ws.append(["LG-0034", "System", "Login & Session", "Repeated failed logins are rate-limited", "", "", "", "", "N/A", "Primary Browser", "Standard login/security expectation", "Yes"])
    pl = wb.create_sheet("Product Listing - TC")
    pl.append(["Product Listing Test Cases"])
    pl.append(["Module Code: PL"])
    pl.append(HEADERS)
    pl.append(["PL-0021", "System", "Product Listing", "Product search control is available", "", "", "", "", "standard_user", "Primary Browser", "Standard feature expectation", "Yes"])
    pl.append(["PL-0022", "System", "Product Listing", "Search returns matching products", "", "", "", "", "standard_user", "Primary Browser", "Standard feature expectation", "Yes"])
    pl.append(["PL-0023", "System", "Product Listing", "No-result search state is clear", "", "", "", "", "standard_user", "Primary Browser", "Standard feature expectation", "Yes"])
    wb.save(path)
    wb.close()
    return path


class DummyItem:
    name = "test_expectation"

    def __init__(self):
        self.user_properties = []
        self._markers = {
            "case_id": "LG-0029",
            "module": "Login & Session",
            "test_user": "standard_user",
        }

    def get_closest_marker(self, name):
        value = self._markers.get(name)
        if value is None:
            return None
        return SimpleNamespace(args=(value,), kwargs={})


def test_expectation_classification_from_workbook_remarks(tmp_path):
    workbook = make_expectation_workbook(tmp_path / "expectations.xlsx")

    expectations = load_expectation_cases(workbook)

    assert set(expectations) == {"LG-0028", "LG-0029", "LG-0034", "PL-0021", "PL-0022", "PL-0023"}
    assert expectations["LG-0028"].mode == ExpectationMode.PRESENCE_PROBE
    assert expectations["LG-0029"].mode == ExpectationMode.DEPENDENT_BEHAVIOR
    assert expectations["LG-0034"].mode == ExpectationMode.BOUNDED_BEHAVIORAL_PROBE


def test_expectation_dependencies_validate_against_workbook(tmp_path):
    workbook = make_expectation_workbook(tmp_path / "expectations.xlsx")

    assert validate_expectation_dependencies(workbook) == []


def test_preflight_includes_only_presence_and_bounded_probes(tmp_path):
    workbook = make_expectation_workbook(tmp_path / "expectations.xlsx")

    assert safe_preflight_case_ids(workbook) == {"LG-0028", "LG-0034", "PL-0021"}


def test_dependent_absent_prerequisite_becomes_blocked_result():
    item = DummyItem()
    blocked = ExpectationBlocked(
        "LG-0029",
        "LG-0028",
        "Remember Me persistence behavior could not be executed because the required Remember Me control was absent.",
    )
    set_user_property(item, "forced_status", "Blocked")
    set_user_property(item, "actual_result", str(blocked))
    set_user_property(item, "additional_remarks", "Blocked by failed prerequisite LG-0028; Standard Expectation; no defect auto-created")
    report = SimpleNamespace(when="call", passed=False, failed=True, skipped=False, longrepr=str(blocked))

    result = build_execution_result(
        item,
        report,
        run_id="RUN-20260709T103000-12345678",
        browser="Chrome",
        artifacts_dir=Path("artifacts"),
    )

    assert result is not None
    assert result.status == "Blocked"
    assert "Remember Me persistence behavior could not be executed" in result.actual_result
    assert "no defect auto-created" in result.remarks
