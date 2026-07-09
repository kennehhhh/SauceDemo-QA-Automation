from __future__ import annotations

from dataclasses import dataclass


MODULE_SHEET_SUFFIX = " - TC"
EXECUTION_LOG_SHEET = "Test Execution Log"


@dataclass(frozen=True)
class WorkbookCase:
    case_id: str
    category: str
    module: str
    scenario: str
    preconditions: str
    test_data: str
    steps: str
    expected_result: str
    applicable_user: str
    browser_coverage: str
    remarks: str
    automation_candidate: str
    sheet_name: str
