from __future__ import annotations

import csv
from pathlib import Path

from results.models import ExecutionResult, WORKBOOK_EXECUTION_FIELDS


def export_csv(path: Path, results: list[ExecutionResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=WORKBOOK_EXECUTION_FIELDS)
        writer.writeheader()
        for idx, result in enumerate(results, start=1):
            writer.writerow(result.to_workbook_row(f"EXE-{idx:04d}"))
