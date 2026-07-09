from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from workbook.expectation_dependencies import EXPECTATION_DEPENDENCIES
from workbook.expectation_policy import ExpectationMode
from workbook.models import WorkbookCase
from workbook.parser import load_case_index


EXPECTATION_LABELS = (
    "standard feature expectation",
    "standard login/security expectation",
)

BOUNDED_EXPECTATION_CASE_IDS = {
    "LG-0032",
    "LG-0033",
    "LG-0034",
    "LG-0035",
    "CI-0023",
    "CI-0024",
    "AC-0011",
    "AC-0012",
}

PRESENCE_EXPECTATION_CASE_IDS = {
    "LG-0028",
    "LG-0030",
    "LG-0031",
    "PL-0021",
    "PD-0015",
    "CT-0020",
}

MANUAL_EXPECTATION_CASE_IDS: set[str] = set()


@dataclass(frozen=True)
class ExpectationCase:
    case_id: str
    module: str
    scenario: str
    remarks: str
    expectation_type: str
    mode: ExpectationMode
    prerequisite_case_id: str | None


def is_standard_expectation(case: WorkbookCase) -> bool:
    remarks = (case.remarks or "").casefold()
    return any(label in remarks for label in EXPECTATION_LABELS)


def expectation_type(case: WorkbookCase) -> str:
    remarks = (case.remarks or "").casefold()
    if "standard login/security expectation" in remarks:
        return "Standard login/security expectation"
    return "Standard feature expectation"


def mode_for_case_id(case_id: str) -> ExpectationMode:
    if case_id in EXPECTATION_DEPENDENCIES:
        return ExpectationMode.DEPENDENT_BEHAVIOR
    if case_id in BOUNDED_EXPECTATION_CASE_IDS:
        return ExpectationMode.BOUNDED_BEHAVIORAL_PROBE
    if case_id in MANUAL_EXPECTATION_CASE_IDS:
        return ExpectationMode.MANUAL_EXPECTATION_REVIEW
    return ExpectationMode.PRESENCE_PROBE


def load_expectation_cases(workbook_path: str | Path) -> dict[str, ExpectationCase]:
    cases = load_case_index(workbook_path)
    expectations: dict[str, ExpectationCase] = {}
    for case in cases.values():
        if not is_standard_expectation(case):
            continue
        expectations[case.case_id] = ExpectationCase(
            case_id=case.case_id,
            module=case.module,
            scenario=case.scenario,
            remarks=case.remarks,
            expectation_type=expectation_type(case),
            mode=mode_for_case_id(case.case_id),
            prerequisite_case_id=EXPECTATION_DEPENDENCIES.get(case.case_id),
        )
    return expectations


def safe_preflight_case_ids(workbook_path: str | Path) -> set[str]:
    expectations = load_expectation_cases(workbook_path)
    return {
        case_id
        for case_id, expectation in expectations.items()
        if expectation.mode in {ExpectationMode.PRESENCE_PROBE, ExpectationMode.BOUNDED_BEHAVIORAL_PROBE}
    }


def validate_expectation_dependencies(workbook_path: str | Path) -> list[str]:
    errors: list[str] = []
    expectations = load_expectation_cases(workbook_path)
    for dependent_id, prerequisite_id in EXPECTATION_DEPENDENCIES.items():
        dependent = expectations.get(dependent_id)
        prerequisite = expectations.get(prerequisite_id)
        if dependent is None:
            errors.append(f"Expectation dependency dependent case is not workbook-labeled expectation: {dependent_id}")
        if prerequisite is None:
            errors.append(f"Expectation dependency prerequisite case is not workbook-labeled expectation: {prerequisite_id}")
        if prerequisite and prerequisite.mode != ExpectationMode.PRESENCE_PROBE:
            errors.append(f"Prerequisite {prerequisite_id} must be PRESENCE_PROBE, found {prerequisite.mode}")
    return errors
