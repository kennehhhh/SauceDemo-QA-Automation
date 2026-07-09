from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import json

from results.collector import build_execution_result, classify_report, make_run_id, save_result_manifest, set_user_property


class DummyItem:
    name = "test_CW_0001_old_style_name"

    def __init__(self, markers):
        self._markers = markers
        self.user_properties = []

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


def test_assertion_failure_is_classified_as_failed():
    report = SimpleNamespace(when="call", passed=False, failed=True, skipped=False)

    assert classify_report(report) == "Failed"


def test_failure_actual_result_includes_recorded_observation_and_url():
    item = DummyItem({"case_id": "LG-0010", "module": "Login & Session", "test_user": "N/A"})
    set_user_property(item, "actual_result", "Username-required message was not displayed.")
    set_user_property(item, "current_url", "https://www.saucedemo.com/")
    report = SimpleNamespace(when="call", passed=False, failed=True, skipped=False, longrepr="assert False")

    result = build_execution_result(
        item,
        report,
        run_id="RUN-20260709T103000-12345678",
        browser="Chrome",
        artifacts_dir=Path("artifacts"),
        browser_version="120",
        current_url="https://www.saucedemo.com/",
    )

    assert result is not None
    assert result.status == "Failed"
    assert "Username-required message" in result.actual_result
    assert "Current URL" in result.actual_result
    assert "browser_version=120" in result.remarks


def test_manifest_serialization(tmp_path):
    item = DummyItem(
        {
            "case_id": "LG-0001",
            "module": "Login & Session",
            "test_user": "N/A",
            "actual_result": "Username input was visible.",
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
    path = tmp_path / "manifest.json"

    save_result_manifest(path, "RUN-20260709T103000-12345678", [result])

    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["run_id"] == "RUN-20260709T103000-12345678"
    assert payload["results"][0]["case_id"] == "LG-0001"


def test_run_id_contains_timestamp_and_short_hash():
    run_id = make_run_id(seed="stable")

    assert run_id.startswith("RUN-")
    assert len(run_id.rsplit("-", 1)[-1]) == 8
