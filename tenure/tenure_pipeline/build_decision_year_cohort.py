#!/usr/bin/env python3
"""
build_decision_year_cohort.py — decision-year cohort (Mac)

Join faculty_panel_with_pools.jsonl exit row + author_year_career_master.jsonl
(Alex own-performance = pubs_per_career_year at decision calendar year).

Default: all resolved (tenure + attrition), excluding transferred.
Optional --asst-time-min/max for diagnostic slices only.

Usage (repo root):
  python tenure/tenure_pipeline/build_decision_year_cohort.py
  python tenure/tenure_pipeline/build_decision_year_cohort.py --asst-time-min 5 --asst-time-max 6
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from decision_year_cohort import (  # noqa: E402
    REFERENCE_ASST_TIME_MAX,
    REFERENCE_ASST_TIME_MIN,
    build_decision_cohort_records,
)

DEFAULT_PANEL = _HERE / "faculty_panel_with_pools.jsonl"
DEFAULT_CAREER = _HERE / "author_year_career_master.jsonl"
DEFAULT_OUT = _HERE / "decision_year_cohort.jsonl"
DEFAULT_META = _HERE / "decision_year_cohort_meta.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build decision-year cohort JSONL")
    parser.add_argument("--panel", type=Path, default=DEFAULT_PANEL)
    parser.add_argument("--career", type=Path, default=DEFAULT_CAREER)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--meta", type=Path, default=DEFAULT_META)
    parser.add_argument(
        "--asst-time-min",
        type=int,
        default=None,
        help="Optional diagnostic filter (default: include all resolved)",
    )
    parser.add_argument(
        "--asst-time-max",
        type=int,
        default=None,
        help="Optional diagnostic filter (default: include all resolved)",
    )
    args = parser.parse_args()

    if not args.panel.is_file():
        raise SystemExit(f"Panel not found: {args.panel}")
    if not args.career.is_file():
        raise SystemExit(
            f"Career master not found: {args.career}\nRun build_author_year_career_master.py first"
        )

    records, stats = build_decision_cohort_records(
        args.panel,
        args.career,
        asst_time_min=args.asst_time_min,
        asst_time_max=args.asst_time_max,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    meta = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "script": "build_decision_year_cohort.py",
        "policy": {
            "resolved": "tenure or attrition (incl. OTT)",
            "excluded": "censored, transferred, exclude_from_metrics",
            "inclusion": "all asst_time unless --asst-time-min/max set",
            "reference_band": f"asst_time {REFERENCE_ASST_TIME_MIN}–{REFERENCE_ASST_TIME_MAX} (stats only)",
        },
        "inputs": {
            "panel": str(args.panel.name),
            "career_master": str(args.career.name),
        },
        **stats,
        "output": str(args.out.name),
    }
    args.meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(meta, indent=2))
    print(f"\n✅ Wrote {args.out} ({len(records):,} rows)")
    print(f"✅ Meta → {args.meta}")


if __name__ == "__main__":
    main()
