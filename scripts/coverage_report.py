from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from workbook.module_registry import WORKBOOK_MODULES
from workbook.dispositions import disposition_for_case
from workbook.parser import load_case_index


CASE_MARK_RE = re.compile(r"case_id\(\s*['\"]([A-Z]+-\d{4})['\"]\s*\)")


def find_implemented_case_ids(tests_dir: Path) -> set[str]:
    case_ids: set[str] = set()
    for path in tests_dir.rglob("test_*.py"):
        case_ids.update(CASE_MARK_RE.findall(path.read_text(encoding="utf-8")))
    return case_ids


def find_case_locations(tests_dir: Path) -> dict[str, list[str]]:
    locations: dict[str, list[str]] = defaultdict(list)
    for path in tests_dir.rglob("test_*.py"):
        text = path.read_text(encoding="utf-8")
        for case_id in CASE_MARK_RE.findall(text):
            locations[case_id].append(path.as_posix())
    return dict(locations)


def _is_candidate(value: str) -> bool:
    return value.strip().lower() in {"yes", "candidate"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Report SauceDemo workbook automation coverage.")
    parser.add_argument("--workbook", required=True, help="Path to the ground-truth workbook.")
    parser.add_argument("--tests-dir", default="tests", help="Directory containing pytest tests.")
    args = parser.parse_args()

    workbook_cases = load_case_index(args.workbook)
    locations = find_case_locations(Path(args.tests_dir))
    implemented = set(locations)
    auto_planned = {case_id for case_id in workbook_cases if disposition_for_case(case_id) == "AUTO"}
    hybrid_planned = {case_id for case_id in workbook_cases if disposition_for_case(case_id) == "HYBRID"}
    manual_planned = {case_id for case_id in workbook_cases if disposition_for_case(case_id) == "MANUAL"}
    candidates = {case.case_id for case in workbook_cases.values() if _is_candidate(case.automation_candidate)}
    stale = implemented - set(workbook_cases)
    missing_auto = auto_planned - implemented
    duplicate_mappings = {case_id: paths for case_id, paths in locations.items() if len(paths) > 1}

    implemented_by_module = Counter(workbook_cases[case_id].module for case_id in implemented if case_id in workbook_cases)
    rows = []
    for case_id, case in sorted(workbook_cases.items()):
        rows.append(
            {
                "Case ID": case_id,
                "Module": case.module,
                "Scenario": case.scenario,
                "Category": case.category,
                "Applicable User": case.applicable_user,
                "Browser Coverage": case.browser_coverage,
                "Automation Candidate": case.automation_candidate,
                "Disposition": disposition_for_case(case_id),
                "Implementation Path": ";".join(locations.get(case_id, [])),
                "Implementation Status": "implemented" if case_id in implemented else "missing",
            }
        )

    print(f"Workbook total: {len(workbook_cases)}")
    print(f"Workbook Automation Candidate Yes/Candidate: {len(candidates)}")
    print(f"AUTO planned: {len(auto_planned)}")
    print(f"HYBRID planned: {len(hybrid_planned)}")
    print(f"MANUAL planned: {len(manual_planned)}")
    print(f"Implemented automated: {len(implemented - stale)}")
    print(f"Missing AUTO implementations: {len(missing_auto)}")
    print(f"Stale automation mappings: {len(stale)}")
    print(f"Duplicate code mappings: {len(duplicate_mappings)}")
    print("")
    print("Workbook modules:")
    for workbook_module in WORKBOOK_MODULES:
        workbook_count = sum(1 for case in workbook_cases.values() if case.sheet_name == workbook_module.sheet_name)
        implemented_count = implemented_by_module.get(workbook_module.module, 0)
        status = "implemented" if implemented_count == workbook_count else ("partial" if implemented_count else "unimplemented")
        print(
            f"  {workbook_module.code} {workbook_module.module}: "
            f"{implemented_count} implemented / {workbook_count} workbook cases ({status})"
        )

    if missing_auto:
        print("")
        print("Missing AUTO Case IDs:")
        print(", ".join(sorted(missing_auto)))

    output_base = Path("results") / "coverage_report"
    output_base.parent.mkdir(exist_ok=True)
    (output_base.with_suffix(".json")).write_text(
        json.dumps(
            {
                "workbook_total": len(workbook_cases),
                "auto_planned": sorted(auto_planned),
                "hybrid_planned": sorted(hybrid_planned),
                "manual_planned": sorted(manual_planned),
                "implemented": sorted(implemented - stale),
                "missing_auto": sorted(missing_auto),
                "stale": sorted(stale),
                "duplicate_mappings": duplicate_mappings,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    with output_base.with_suffix(".csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    return 1 if stale or duplicate_mappings else 0


if __name__ == "__main__":
    raise SystemExit(main())
