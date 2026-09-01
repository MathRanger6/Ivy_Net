#!/usr/bin/env python3
"""Tenure Pass A — empirical HERO (tenure rate vs LOO peer quality).

v0 lock: inference panel (HIGH/MEDIUM), person-level LOO mean, Q16 bins,
tenure rate among resolved (censored excluded from denominator).

Outputs → 3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/

Run (repo root):
  python tenure/scripts/tenure_pass_a_hero.py
  python tenure/scripts/tenure_pass_a_hero.py --bin-method equal_width --x-metric poolq --output-tag ew16_poolq_infHM
  python tenure/scripts/tenure_pass_a_hero.py --bin-method quantile --x-metric loo --output-tag q16_loo_infHM
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
TENURE_PIPELINE = REPO / "tenure" / "tenure_pipeline"
DEFAULT_IN = TENURE_PIPELINE / "faculty_panel_with_pools.jsonl"
DEFAULT_OUT_DIR = (
    REPO
    / "3-Master_Plan"
    / "re_entry"
    / "HEROs_and_PASSes"
    / "tenure_sandbox"
    / "hero"
)

PRIMARY_TIERS = frozenset({"HIGH", "MEDIUM"})

# Import stage9 from tenure_pipeline (notebook-adjacent module path)
sys.path.insert(0, str(TENURE_PIPELINE))
from stage9_analysis import build_inverted_u  # noqa: E402


def filter_inference_jsonl(in_path: Path, out_path: Path) -> dict:
    """Keep HIGH/MEDIUM rows with non-null poolq_loo_mean (inference v1 spirit)."""
    n_in = 0
    n_out = 0
    tier_in: dict[str, int] = {}
    with in_path.open(encoding="utf-8") as fin, out_path.open("w", encoding="utf-8") as fout:
        for line in fin:
            n_in += 1
            r = json.loads(line)
            tier = r.get("match_confidence")
            tier_in[str(tier)] = tier_in.get(str(tier), 0) + 1
            if tier not in PRIMARY_TIERS:
                continue
            if r.get("poolq_loo_mean") is None:
                continue
            fout.write(json.dumps(r) + "\n")
            n_out += 1
    return {"rows_in": n_in, "rows_out": n_out, "tier_counts_in": tier_in}


def write_provenance(
    path: Path,
    *,
    args: argparse.Namespace,
    filter_stats: dict,
    result: dict,
    png_name: str,
    csv_name: str,
) -> None:
    prov = {
        "artifact": "tenure_pass_a_hero_v0",
        "date": date.today().isoformat(),
        "input": str(args.input.relative_to(REPO) if args.input.is_relative_to(REPO) else args.input),
        "filter": {
            "match_confidence": sorted(PRIMARY_TIERS),
            "require_poolq_loo_mean": True,
            "rows_in": filter_stats["rows_in"],
            "rows_out": filter_stats["rows_out"],
        },
        "spec": {
            "grain": (
                "person-level mean poolq_loo_mean (assistant years)"
                if args.x_metric == "loo"
                else "person-level mean full OA pool pubs/yr (assistant years)"
            ),
            "x_metric": args.x_metric,
            "n_bins": args.n_bins,
            "bin_method": args.bin_method,
            "exclude_censored": args.exclude_censored,
            "y_primary": "tenure_event / n_resolved",
            "y_companion": "attrition / n_resolved",
        },
        "outputs": {"png": png_name, "csv": csv_name},
        "stage9_summary": result,
    }
    path.write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Tenure empirical HERO (v0 inference panel)")
    parser.add_argument("--input", type=Path, default=DEFAULT_IN, help="faculty_panel_with_pools.jsonl")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="hero output directory")
    parser.add_argument("--n-bins", type=int, default=16, help="number of bins (default 16)")
    parser.add_argument(
        "--bin-method",
        choices=("quantile", "equal_width"),
        default="quantile",
        help="quantile (equal N) or equal_width (equal x range)",
    )
    parser.add_argument(
        "--x-metric",
        choices=("loo", "poolq"),
        default="loo",
        help="loo = leave-one-out pool mean; poolq = full OA pool mean",
    )
    parser.add_argument(
        "--exclude-censored",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="rates among resolved only (default True)",
    )
    parser.add_argument(
        "--output-tag",
        default="q16_infHM_resolved_v0",
        help="filename token after HERO_tenure_",
    )
    parser.add_argument(
        "--include-all-in-denominator",
        action="store_true",
        help="future: Option B (censored in denominator); default is Option A",
    )
    args = parser.parse_args()

    if args.include_all_in_denominator:
        args.exclude_censored = False

    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}\nRun: ./scripts/rsync_pull_recent_hpc.sh tenure")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, prefix="tenure_inf_", encoding="utf-8"
    ) as tmp:
        filtered_path = Path(tmp.name)

    try:
        print(f"Filtering inference panel → {filtered_path.name}")
        filter_stats = filter_inference_jsonl(args.input, filtered_path)
        print(json.dumps(filter_stats, indent=2))

        work_dir = args.out_dir / "_stage9_scratch"
        work_dir.mkdir(parents=True, exist_ok=True)

        result = build_inverted_u(
            filtered_path,
            work_dir,
            n_bins=args.n_bins,
            exclude_censored=args.exclude_censored,
            bin_method=args.bin_method,
            x_metric=args.x_metric,
        )

        base = f"HERO_tenure_{args.output_tag}"
        png_dest = args.out_dir / f"{base}.png"
        csv_dest = args.out_dir / f"{base}_binned.csv"
        prov_dest = args.out_dir / f"{base}_provenance.json"

        shutil.copy2(work_dir / "stage9_inverted_u.png", png_dest)
        shutil.copy2(work_dir / "stage9_binned_table.csv", csv_dest)
        write_provenance(prov_dest, args=args, filter_stats=filter_stats, result=result, png_name=png_dest.name, csv_name=csv_dest.name)

        print(f"\n✅ HERO PNG → {png_dest.relative_to(REPO)}")
        print(f"✅ Binned CSV → {csv_dest.relative_to(REPO)}")
        print(f"✅ Provenance → {prov_dest.relative_to(REPO)}")
    finally:
        filtered_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
