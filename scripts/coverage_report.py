from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workbook.module_registry import WORKBOOK_MODULES
from workbook.parser import load_case_index


CASE_MARK_RE = re.compile(r"case_id\(\s*['\"]([A-Z]+-\d{4})['\"]\s*\)")


def find_implemented_case_ids(tests_dir: Path) -> set[str]:
    case_ids: set[str] = set()
    for path in tests_dir.rglob("test_*.py"):
        case_ids.update(CASE_MARK_RE.findall(path.read_text(encoding="utf-8")))
    return case_ids


def _is_candidate(value: str) -> bool:
    return value.strip().lower() in {"yes", "candidate"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Report SauceDemo workbook automation coverage.")
    parser.add_argument("--workbook", required=True, help="Path to the ground-truth workbook.")
    parser.add_argument("--tests-dir", default="tests", help="Directory containing pytest tests.")
    args = parser.parse_args()

    workbook_cases = load_case_index(args.workbook)
    implemented = find_implemented_case_ids(Path(args.tests_dir))
    candidates = {case.case_id for case in workbook_cases.values() if _is_candidate(case.automation_candidate)}
    stale = implemented - set(workbook_cases)
    missing_candidates = candidates - implemented
    manual_only = set(workbook_cases) - candidates

    implemented_by_module = Counter(workbook_cases[case_id].module for case_id in implemented if case_id in workbook_cases)

    print(f"Workbook total: {len(workbook_cases)}")
    print(f"Automatable candidates: {len(candidates)}")
    print(f"Implemented automated: {len(implemented - stale)}")
    print(f"Candidate but not implemented: {len(missing_candidates)}")
    print(f"Manual-only / not marked candidate: {len(manual_only)}")
    print(f"Stale automation mappings: {len(stale)}")
    print("")
    print("Workbook modules:")
    for workbook_module in WORKBOOK_MODULES:
        workbook_count = sum(1 for case in workbook_cases.values() if case.module == workbook_module.module)
        implemented_count = implemented_by_module.get(workbook_module.module, 0)
        print(
            f"  {workbook_module.code} {workbook_module.module}: "
            f"{implemented_count} implemented / {workbook_count} workbook cases "
            f"({workbook_module.status})"
        )
    return 1 if stale else 0


if __name__ == "__main__":
    raise SystemExit(main())
