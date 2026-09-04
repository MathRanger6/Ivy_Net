#!/usr/bin/env python3
"""Tenure Pass A — empirical HERO (tenure rate vs LOO peer quality).

v0 lock: inference panel (HIGH/MEDIUM), ASST-PS mean peer LOO (annum), Q16 bins,
tenure rate among resolved (censored excluded from denominator).

Outputs → 3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/

Run (repo root):
  python tenure/scripts/tenure_pass_a_hero.py
  python tenure/scripts/tenure_pass_a_hero.py --bin-method equal_width --x-metric poolq --output-tag ew16_poolq_infHM
  python tenure/scripts/tenure_pass_a_hero.py --window last_ps --stat cum --output-tag q16_lastps_loo_cum_infHM
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
import warnings
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

sys.path.insert(0, str(TENURE_PIPELINE))
from hero_panel_prep import prepare_hero_panel, write_jsonl  # noqa: E402
from stage9_analysis import build_inverted_u, _load_person_level  # noqa: E402

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))
from tenure_grain_labels import (  # noqa: E402
    ASST_PS,
    ANNUM,
    LAST_PS,
    normalize_stat,
    normalize_window,
    provenance_spec_label,
    warn_if_legacy_cli,
)
from tenure_hero_slide_plot import (  # noqa: E402
    build_hero_slide_panel,
    write_lpm_txt,
)


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


def _resolve_window_stat(args: argparse.Namespace) -> tuple[str, str]:
    """CLI window/stat with legacy --grain / --pool-perf fallback."""
    if getattr(args, "grain", None) is not None or getattr(args, "pool_perf", None) is not None:
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            window, stat = warn_if_legacy_cli(
                grain=getattr(args, "grain", None) or args.window,
                pool_perf=getattr(args, "pool_perf", None) or args.stat,
            )
        return window, stat
    return normalize_window(args.window), normalize_stat(args.stat)


def write_provenance(
    path: Path,
    *,
    args: argparse.Namespace,
    window: str,
    stat: str,
    filter_stats: dict,
    result: dict,
    png_name: str,
    csv_name: str,
    slide_png_name: str | None = None,
    lpm_name: str | None = None,
    shape: dict | None = None,
) -> None:
    outputs = {"png": png_name, "csv": csv_name}
    if slide_png_name:
        outputs["slide_png"] = slide_png_name
    if lpm_name:
        outputs["lpm_txt"] = lpm_name
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
            "window": window,
            "stat": stat,
            "spec_label": provenance_spec_label(
                window=window, stat=stat, x_metric=args.x_metric
            ),
            "x_metric": args.x_metric,
            "n_bins": args.n_bins,
            "bin_method": args.bin_method,
            "exclude_censored": args.exclude_censored,
            "y_primary": "tenure_event / n_resolved",
            "y_companion": "attrition / n_resolved",
        },
        "outputs": outputs,
        "stage9_summary": result,
    }
    if shape:
        prov["shape"] = shape
    path.write_text(json.dumps(prov, indent=2) + "\n", encoding="utf-8")


def _uses_custom_prep(window: str, stat: str, x_metric: str) -> bool:
    return window != ASST_PS or stat != ANNUM or x_metric == "own_cum"


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
        choices=("loo", "poolq", "own_cum"),
        default="loo",
        help="loo = LOO pool mean; poolq = full OA pool mean; own_cum = own pubs_cumulative (last_ps)",
    )
    parser.add_argument(
        "--window",
        choices=("asst_ps", "last_ps", "all_ps"),
        default="asst_ps",
        help="asst_ps = mean over assistant years (v0); last_ps = final assistant row (MBB last-ps)",
    )
    parser.add_argument(
        "--stat",
        choices=("annum", "cum", "mean"),
        default="annum",
        help="annum = pubs_year LOO; cum = pubs_cumulative LOO at that row",
    )
    parser.add_argument(
        "--grain",
        choices=("spell_mean", "last_asst"),
        default=None,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--pool-perf",
        choices=("annual", "cumulative"),
        default=None,
        help=argparse.SUPPRESS,
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
        "--no-slide-panel",
        action="store_true",
        help="skip MBB-format single-panel slide PNG",
    )
    parser.add_argument(
        "--include-all-in-denominator",
        action="store_true",
        help="future: Option B (censored in denominator); default is Option A",
    )
    parser.add_argument(
        "--slides-only",
        action="store_true",
        help="skip Stage 9; re-render *_slide.png from existing binned CSV + provenance summary",
    )
    args = parser.parse_args()

    if args.include_all_in_denominator:
        args.exclude_censored = False

    window, stat = _resolve_window_stat(args)

    if args.x_metric == "own_cum" and window != LAST_PS:
        raise SystemExit("--x-metric own_cum requires --window last_ps")

    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}\nRun: ./scripts/rsync_pull_recent_hpc.sh tenure")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    base = f"HERO_tenure_{args.output_tag}"
    csv_dest = args.out_dir / f"{base}_binned.csv"
    slide_dest = args.out_dir / f"{base}_slide.png"
    lpm_dest = args.out_dir / f"{base}_lpm.txt"
    prov_dest = args.out_dir / f"{base}_provenance.json"

    if args.slides_only:
        if not csv_dest.is_file():
            raise SystemExit(f"--slides-only requires {csv_dest.relative_to(REPO)}")
        prov = json.loads(prov_dest.read_text(encoding="utf-8")) if prov_dest.is_file() else {}
        result = prov.get("stage9_summary") or {}
        spec = prov.get("spec") or {}
        if "window" in spec:
            window = normalize_window(spec["window"])
            stat = normalize_stat(spec["stat"])
        elif "grain" in spec:
            window = normalize_window(spec["grain"])
            stat = normalize_stat(spec.get("pool_perf", "annual"))

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", delete=False, prefix="tenure_inf_", encoding="utf-8"
        ) as tmp:
            filtered_path = Path(tmp.name)
        try:
            if _uses_custom_prep(window, stat, args.x_metric):
                rows, prep_stats = prepare_hero_panel(
                    args.input,
                    tiers=PRIMARY_TIERS,
                    window=window,
                    stat=stat,
                    x_metric=args.x_metric,
                )
                write_jsonl(rows, filtered_path)
            else:
                filter_inference_jsonl(args.input, filtered_path)
            persons = _load_person_level(
                filtered_path,
                x_metric=args.x_metric,
                window=window,
                stat=stat,
            )
            coef, shape = build_hero_slide_panel(
                csv_dest,
                slide_dest,
                persons=persons,
                n_bins=args.n_bins,
                bin_method=args.bin_method,
                x_metric=args.x_metric,
                window=window,
                stat=stat,
                exclude_censored=args.exclude_censored,
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
        finally:
            filtered_path.unlink(missing_ok=True)
        return

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".jsonl", delete=False, prefix="tenure_inf_", encoding="utf-8"
    ) as tmp:
        filtered_path = Path(tmp.name)

    try:
        print(f"Preparing HERO panel → {filtered_path.name}")
        if _uses_custom_prep(window, stat, args.x_metric):
            rows, prep_stats = prepare_hero_panel(
                args.input,
                tiers=PRIMARY_TIERS,
                window=window,
                stat=stat,
                x_metric=args.x_metric,
            )
            write_jsonl(rows, filtered_path)
            filter_stats = {
                "rows_in": prep_stats.get("n_inference_asst_rows", 0),
                "rows_out": prep_stats.get("n_with_x", prep_stats.get("n_with_loo", 0)),
                "prep": prep_stats,
            }
        else:
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
            window=window,
            stat=stat,
        )

        png_dest = args.out_dir / f"{base}.png"

        shutil.copy2(work_dir / "stage9_inverted_u.png", png_dest)
        shutil.copy2(work_dir / "stage9_binned_table.csv", csv_dest)

        shape: dict | None = None
        if not args.no_slide_panel:
            persons = _load_person_level(
                filtered_path,
                x_metric=args.x_metric,
                window=window,
                stat=stat,
            )
            coef, shape = build_hero_slide_panel(
                csv_dest,
                slide_dest,
                persons=persons,
                n_bins=args.n_bins,
                bin_method=args.bin_method,
                x_metric=args.x_metric,
                window=window,
                stat=stat,
                exclude_censored=args.exclude_censored,
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
            print(f"✅ LPM txt → {lpm_dest.relative_to(REPO)}")

        write_provenance(
            prov_dest,
            args=args,
            window=window,
            stat=stat,
            filter_stats=filter_stats,
            result=result,
            png_name=png_dest.name,
            csv_name=csv_dest.name,
            slide_png_name=slide_dest.name if not args.no_slide_panel else None,
            lpm_name=lpm_dest.name if not args.no_slide_panel else None,
            shape=shape,
        )

        print(f"\n✅ HERO PNG → {png_dest.relative_to(REPO)}")
        print(f"✅ Binned CSV → {csv_dest.relative_to(REPO)}")
        print(f"✅ Provenance → {prov_dest.relative_to(REPO)}")
    finally:
        filtered_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
