from __future__ import annotations

import hashlib
import json
import os
import platform
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest

from results.models import ExecutionResult


VALID_STATUSES = {"Not Executed", "Passed", "Failed", "Blocked", "Not Applicable"}


@dataclass(frozen=True)
class CaseMetadata:
    case_id: str
    module: str
    test_user: str


def make_run_id(started_at: datetime | None = None, seed: str | None = None) -> str:
    started_at = started_at or datetime.now(timezone.utc)
    seed = seed or f"{started_at.isoformat()}-{os.getpid()}-{platform.node()}"
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
    stamp = started_at.strftime("%Y%m%dT%H%M%S")
    return f"RUN-{stamp}-{digest}"


def get_marker_value(item: pytest.Item, name: str, default: str = "") -> str:
    marker = item.get_closest_marker(name)
    if not marker:
        return default
    if marker.args:
        return str(marker.args[0])
    return str(marker.kwargs.get("value", default))


def get_case_metadata(item: pytest.Item) -> CaseMetadata | None:
    case_id = get_marker_value(item, "case_id")
    if not case_id:
        return None
    return CaseMetadata(
        case_id=case_id,
        module=get_marker_value(item, "module", "Unmapped"),
        test_user=get_marker_value(item, "test_user", "N/A"),
    )


def get_user_property(item: pytest.Item, name: str, default: str = "") -> str:
    for prop_name, prop_value in item.user_properties:
        if prop_name == name:
            return str(prop_value)
    return default


def set_user_property(item: pytest.Item, name: str, value: str) -> None:
    item.user_properties = [(n, v) for n, v in item.user_properties if n != name]
    item.user_properties.append((name, value))


def classify_report(report: pytest.TestReport) -> str:
    if report.passed:
        return "Passed"
    if report.when == "setup" and report.failed:
        return "Blocked"
    if report.failed:
        return "Failed"
    if report.skipped:
        return "Not Applicable"
    return "Blocked"


def concise_failure(report: pytest.TestReport, max_chars: int = 1400) -> str:
    text = str(report.longrepr)
    return text.replace("\n", " ")[:max_chars]


def build_actual_result(item: pytest.Item, report: pytest.TestReport) -> str:
    if report.passed:
        return get_user_property(
            item,
            "actual_result",
            get_marker_value(item, "actual_result", "Automated assertion completed as expected."),
        )
    if report.when == "setup":
        return f"Automation setup did not complete, so the case could not be meaningfully executed: {concise_failure(report)}"
    return f"Expected workbook behavior was not observed. {concise_failure(report)}"


def build_execution_result(
    item: pytest.Item,
    report: pytest.TestReport,
    *,
    run_id: str,
    browser: str,
    artifacts_dir: Path,
) -> ExecutionResult | None:
    metadata = get_case_metadata(item)
    if metadata is None:
        return None

    status = classify_report(report)
    if status not in VALID_STATUSES:
        raise ValueError(f"Unsupported execution status: {status}")

    evidence_path = get_user_property(item, "evidence_path")
    remarks = f"Automated by Selenium + pytest; run_id={run_id}"
    if evidence_path:
        remarks += f"; evidence: {evidence_path}"

    return ExecutionResult(
        case_id=metadata.case_id,
        module=metadata.module,
        test_user=metadata.test_user,
        browser=browser,
        actual_result=build_actual_result(item, report)[:2000],
        status=status,
        related_defect_id="",
        tester=os.getenv("TESTER_NAME", platform.node()),
        execution_date=datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %z"),
        remarks=remarks,
        run_id=run_id,
    )


def save_result_manifest(path: Path, run_id: str, results: list[ExecutionResult]) -> None:
    payload: dict[str, Any] = {
        "run_id": run_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "results": [result.to_dict() for result in results],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
