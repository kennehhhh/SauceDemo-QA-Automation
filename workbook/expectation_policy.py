from __future__ import annotations

from enum import StrEnum


class ExpectationMode(StrEnum):
    PRESENCE_PROBE = "PRESENCE_PROBE"
    DEPENDENT_BEHAVIOR = "DEPENDENT_BEHAVIOR"
    BOUNDED_BEHAVIORAL_PROBE = "BOUNDED_BEHAVIORAL_PROBE"
    MANUAL_EXPECTATION_REVIEW = "MANUAL_EXPECTATION_REVIEW"


class ExpectationBlocked(AssertionError):
    """Raised when an expectation behavior cannot run because a prerequisite is absent."""

    def __init__(self, case_id: str, prerequisite_case_id: str, message: str) -> None:
        super().__init__(message)
        self.case_id = case_id
        self.prerequisite_case_id = prerequisite_case_id
