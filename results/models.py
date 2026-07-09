from __future__ import annotations

from dataclasses import asdict, dataclass


WORKBOOK_EXECUTION_FIELDS = [
    "Execution ID",
    "Case ID",
    "Module",
    "Test User",
    "Browser",
    "Actual Result",
    "Status",
    "Related Defect ID",
    "Tester",
    "Execution Date",
    "Remarks",
]


@dataclass(frozen=True)
class ExecutionResult:
    case_id: str
    module: str
    test_user: str
    browser: str
    actual_result: str
    status: str
    related_defect_id: str
    tester: str
    execution_date: str
    remarks: str
    run_id: str

    def to_workbook_row(self, execution_id: str = "") -> dict[str, str]:
        return {
            "Execution ID": execution_id,
            "Case ID": self.case_id,
            "Module": self.module,
            "Test User": self.test_user,
            "Browser": self.browser,
            "Actual Result": self.actual_result,
            "Status": self.status,
            "Related Defect ID": self.related_defect_id,
            "Tester": self.tester,
            "Execution Date": self.execution_date,
            "Remarks": self.remarks,
        }

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
