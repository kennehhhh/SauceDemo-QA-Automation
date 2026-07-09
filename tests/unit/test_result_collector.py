from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from results.collector import build_execution_result, classify_report, make_run_id


class DummyItem:
    name = "test_CW_0001_old_style_name"
    user_properties = []

    def __init__(self, markers):
        self._markers = markers

    def get_closest_marker(self, name):
        value = self._markers.get(name)
        if value is None:
            return None
        return SimpleNamespace(args=(value,), kwargs={})


def test_build_execution_result_uses_explicit_case_id_marker():
    item = DummyItem(
        {
            "case_id": "CW-0001",
            "module": "Core Workflows",
            "test_user": "standard_user",
            "actual_result": "Case-specific success.",
        }
    )
    report = SimpleNamespace(when="call", passed=True, failed=False, skipped=False, longrepr="")

    result = build_execution_result(
        item,
        report,
        run_id="RUN-20260709T103000-12345678",
        browser="Chrome",
        artifacts_dir=Path("artifacts"),
    )

    assert result is not None
    assert result.case_id == "CW-0001"
    assert result.module == "Core Workflows"
    assert result.test_user == "standard_user"
    assert result.actual_result == "Case-specific success."


def test_setup_failure_is_classified_as_blocked():
    report = SimpleNamespace(when="setup", passed=False, failed=True, skipped=False)

    assert classify_report(report) == "Blocked"


def test_run_id_contains_timestamp_and_short_hash():
    run_id = make_run_id(seed="stable")

    assert run_id.startswith("RUN-")
    assert len(run_id.rsplit("-", 1)[-1]) == 8
