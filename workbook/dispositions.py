from __future__ import annotations


MANUAL_CASE_IDS = {
    "LG-0040",
    "PL-0024",
    "PS-0014",
    "PD-0016",
    "CT-0021",
    "CT-0022",
    "CI-0027",
    "CO-0016",
    "CO-0017",
    "OC-0009",
    "MN-0012",
    "RS-0008",
    "UX-0016",
    "CW-0014",
    "CW-0015",
}

HYBRID_CASE_IDS = {
    "UX-0001",
    "UX-0002",
    "UX-0005",
    "UX-0006",
    "UX-0007",
    "UX-0010",
    "UX-0011",
    "UX-0012",
    "UX-0013",
    "UX-0014",
    "UX-0015",
}


def disposition_for_case(case_id: str) -> str:
    if case_id in MANUAL_CASE_IDS:
        return "MANUAL"
    if case_id in HYBRID_CASE_IDS:
        return "HYBRID"
    return "AUTO"
