from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from results.models import ExecutionResult
from workbook.updater import append_results_to_workbook


def load_manifest(path: Path) -> list[ExecutionResult]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [ExecutionResult(**item) for item in payload["results"]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Append automated execution results to a SauceDemo workbook copy.")
    parser.add_argument("--workbook", required=True, help="Path to the ground-truth workbook.")
    parser.add_argument("--manifest", required=True, help="Path to a results/execution_manifest_*.json file.")
    parser.add_argument("--output", default="", help="Output workbook copy path. Defaults to timestamped copy.")
    parser.add_argument("--in-place", action="store_true", help="Update the workbook in place after creating a backup.")
    args = parser.parse_args()

    updated_path = append_results_to_workbook(
        args.workbook,
        load_manifest(Path(args.manifest)),
        output_path=args.output or None,
        in_place=args.in_place,
    )
    print(updated_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
