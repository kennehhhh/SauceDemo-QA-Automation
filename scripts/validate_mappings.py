from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workbook.parser import load_case_index


CASE_MARK_RE = re.compile(r"case_id\(\s*['\"]([A-Z]+-\d{4})['\"]\s*\)")


def find_implemented_case_ids(tests_dir: Path) -> set[str]:
    case_ids: set[str] = set()
    for path in tests_dir.rglob("test_*.py"):
        case_ids.update(CASE_MARK_RE.findall(path.read_text(encoding="utf-8")))
    return case_ids


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pytest Case ID markers against the workbook.")
    parser.add_argument("--workbook", required=True, help="Path to the ground-truth workbook.")
    parser.add_argument("--tests-dir", default="tests", help="Directory containing pytest tests.")
    args = parser.parse_args()

    workbook_cases = load_case_index(args.workbook)
    implemented = find_implemented_case_ids(Path(args.tests_dir))
    stale = sorted(case_id for case_id in implemented if case_id not in workbook_cases)

    print(f"Workbook cases: {len(workbook_cases)}")
    print(f"Implemented markers: {len(implemented)}")
    print(f"Stale automation mappings: {len(stale)}")
    for case_id in stale:
        print(f"STALE {case_id}")
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
