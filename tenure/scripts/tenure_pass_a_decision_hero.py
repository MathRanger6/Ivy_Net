#!/usr/bin/env python3
"""Tenure Pass A — decision cohort HERO (PD29 dept pond).

One row per resolved decision event; peer context = LOO dept pond career rate
at decision calendar year (all ranks in department, pubs_per_career_year).

Run (repo root):
  python tenure/scripts/tenure_pass_a_decision_hero.py
  python tenure/scripts/tenure_pass_a_decision_hero.py --x-metric own_career \\
    --output-tag q16_decision_own_career_infHM
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TENURE_PIPELINE = REPO / "tenure" / "tenure_pipeline"
DEFAULT_IN = TENURE_PIPELINE / "faculty_panel_with_pools.jsonl"
DEFAULT_CAREER = TENURE_PIPELINE / "author_year_career_master.jsonl"
DEFAULT_OUT_DIR = (
    REPO
    / "3-Master_Plan"
    / "re_entry"
    / "HEROs_and_PASSes"
    / "tenure_sandbox"
    / "hero"
)

sys.path.insert(0, str(TENURE_PIPELINE))
from decision_hero_prep import prepare_decision_hero_persons  # noqa: E402
from stage9_analysis import build_inverted_u  # noqa: E402

SCRIPTS_DIR = REPO / "tenure" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from tenure_grain_labels import DECISION, MEAN  # noqa: E402
from tenure_hero_slide_plot import build_hero_slide_panel, write_lpm_txt  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Tenure decision cohort HERO (dept pond)")
    parser.add_argument("--input", type=Path, default=DEFAULT_IN)
    parser.add_argument("--career", type=Path, default=DEFAULT_CAREER)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--n-bins", type=int, default=16)
    parser.add_argument(
        "--bin-method",
        choices=("quantile", "equal_width"),
        default="quantile",
    )
    parser.add_argument(
        "--x-metric",
        choices=("decision_loo", "own_career"),
        default="decision_loo",
        help="decision_loo = dept pond LOO career rate; own_career = ability slice",
    )
    parser.add_argument(
        "--output-tag",
        default=None,
        help="filename token after HERO_tenure_ (default from x-metric)",
    )
    parser.add_argument(
        "--no-slide-panel",
        action="store_true",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")
    if not args.career.is_file():
        raise SystemExit(f"Career master not found: {args.career}")

    tag = args.output_tag or (
        "q16_decision_dept_loo_infHM"
        if args.x_metric == "decision_loo"
        else "q16_decision_own_career_infHM"
    )

    persons, prep_stats = prepare_decision_hero_persons(
        args.input,
        args.career,
        x_metric=args.x_metric,
    )
    print(json.dumps(prep_stats, indent=2))
    if not persons:
        raise SystemExit("No decision HERO persons with computable X.")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = args.out_dir / "_stage9_scratch_decision"
    work_dir.mkdir(parents=True, exist_ok=True)

    result = build_inverted_u(
        args.input,
        work_dir,
        n_bins=args.n_bins,
        exclude_censored=True,
        bin_method=args.bin_method,
        x_metric=args.x_metric,
        window=DECISION,
        stat=MEAN,
        persons=persons,
    )

    base = f"HERO_tenure_{tag}"
    png_dest = args.out_dir / f"{base}.png"
    csv_dest = args.out_dir / f"{base}_binned.csv"
    slide_dest = args.out_dir / f"{base}_slide.png"
    lpm_dest = args.out_dir / f"{base}_lpm.txt"
    prov_dest = args.out_dir / f"{base}_provenance.json"

    shutil.copy2(work_dir / "stage9_inverted_u.png", png_dest)
    shutil.copy2(work_dir / "stage9_binned_table.csv", csv_dest)

    shape = None
    if not args.no_slide_panel:
        coef, shape = build_hero_slide_panel(
            csv_dest,
            slide_dest,
            persons=persons,
            n_bins=args.n_bins,
            bin_method=args.bin_method,
            x_metric=args.x_metric,
            window=DECISION,
            stat=MEAN,
            exclude_censored=True,
            stage9_summary=result,
        )
        write_lpm_txt(
            lpm_dest,
            coef,
            meta={
                "n_resolved": result.get("n_resolved"),
                "n_tenure": result.get("n_tenure"),
                "x_metric": args.x_metric,
                "n_bins": args.n_bins,
                "bin_method": args.bin_method,
            },
        )
        print(f"✅ HERO slide PNG → {slide_dest.relative_to(REPO)}")

    prov = {
        "artifact": "tenure_pass_a_decision_hero",
        "date": date.today().isoformat(),
        "input": str(args.input.relative_to(REPO)),
        "career_master": str(args.career.relative_to(REPO)),
        "prep": prep_stats,
        "spec": {
            "window": DECISION,
            "stat": MEAN,
            "x_metric": args.x_metric,
            "n_bins": args.n_bins,
            "bin_method": args.bin_method,
            "peer_pool": "whole department at decision year · pubs_per_career_year LOO",
            "cohort": "all resolved infHM · excl transferred",
        },
        "outputs": {
            "png": png_dest.name,
            "csv": csv_dest.name,
            "slide_png": slide_dest.name if not args.no_slide_panel else None,
            "lpm_txt": lpm_dest.name if not args.no_slide_panel else None,
        },
        "stage9_summary": result,
        "shape": shape,
    }
    prov_dest.write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")

    print(f"\n✅ HERO PNG → {png_dest.relative_to(REPO)}")
    print(f"✅ Binned CSV → {csv_dest.relative_to(REPO)}")
    print(f"✅ Provenance → {prov_dest.relative_to(REPO)}")


if __name__ == "__main__":
    main()
