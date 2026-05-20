#!/usr/bin/env python3
"""Rivanna staged runner for faithful_538_sweep.py (mirror of 537 worker).

  python faithful_538_sweep_rivanna_worker.py stage1-shard --shard-id 0 --n-shards 32
  python faithful_538_sweep_rivanna_worker.py merge-stage1 --n-shards 32
  python faithful_538_sweep_rivanna_worker.py stage2-shard --shard-id 0 --n-shards 32
  python faithful_538_sweep_rivanna_worker.py merge --n-shards 32
  python faithful_538_sweep_rivanna_worker.py plot-candidates
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import pandas as pd

import faithful_538_sweep as sweep

BASE = Path(__file__).resolve().parent
RIVANNA_DIR = BASE / "rivanna_faithful_538"
STAGE1_SHARD_DIR = RIVANNA_DIR / "stage1_shards"
STAGE2_SHARD_DIR = RIVANNA_DIR / "stage2_shards"
STAGE1_CSV = RIVANNA_DIR / "stage1_results.csv"
STAGE2_CSV = RIVANNA_DIR / "stage2_results_merged.csv"
GROUPED_CSV = RIVANNA_DIR / "grouped_candidates.csv"
README = RIVANNA_DIR / "README.md"
PLOT_DIR = RIVANNA_DIR / "candidate_plots"


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
        f.flush()


def read_rows(path: Path) -> list[dict]:
    df = pd.read_csv(path)
    rows = df.to_dict("records")
    for row in rows:
        for key in (
            "target_mean_low",
            "target_mean_high",
            "assignment_temperature",
            "preferential_alpha",
            "loo_gap_weight",
            "tail_drop_frac",
            "left_lift_frac",
            "tail_slope_last3",
            "peak_y",
            "first_bin_y",
            "final_y",
            "coverage_peak",
            "median_pool_sd",
        ):
            if key in row:
                row[key] = float(row[key])
        for key in (
            "n_teams",
            "roster_size",
            "n_selected",
            "n_bins",
            "n_runs",
            "seed",
            "peak_bin",
            "tail_bins_declining",
        ):
            if key in row and not pd.isna(row[key]):
                row[key] = int(row[key])
        for key in ("interior_peak", "moderate_downturn", "moderate_downturn_strict"):
            if key in row:
                val = row[key]
                if pd.isna(val):
                    row[key] = False
                elif isinstance(val, str):
                    row[key] = val.strip().lower() in ("true", "1", "yes")
                else:
                    row[key] = bool(val)
    return rows


def run_stage1_shard(shard_id: int, n_shards: int, *, pilot: bool, reset: bool) -> None:
    RIVANNA_DIR.mkdir(parents=True, exist_ok=True)
    STAGE1_SHARD_DIR.mkdir(parents=True, exist_ok=True)
    shard_csv = STAGE1_SHARD_DIR / f"stage1_shard_{shard_id:04d}_of_{n_shards:04d}.csv"
    shard_jsonl = STAGE1_SHARD_DIR / f"stage1_shard_{shard_id:04d}_of_{n_shards:04d}.jsonl"
    if reset:
        shard_csv.unlink(missing_ok=True)
        shard_jsonl.unlink(missing_ok=True)
    all_scenarios = list(sweep.iter_stage1(pilot=pilot))
    scenarios = [sc for i, sc in enumerate(all_scenarios) if i % n_shards == shard_id]
    print(
        f"538 stage1 shard {shard_id}/{n_shards}: {len(scenarios):,} of {len(all_scenarios):,}",
        flush=True,
    )
    rows: list[dict] = []
    for idx, sc in enumerate(scenarios, start=1):
        row = sweep.run_scenario(sc)
        rows.append(row)
        append_jsonl(shard_jsonl, row)
        if idx % 25 == 0 or idx == len(scenarios):
            best = max(
                (float(r["tail_drop_frac"]) for r in rows if math.isfinite(float(r["tail_drop_frac"]))),
                default=float("nan"),
            )
            print(f"shard {shard_id}: {idx:,}/{len(scenarios):,}; best tail drop={best:.3f}", flush=True)
    write_csv(shard_csv, rows)


def merge_stage1(n_shards: int, *, pilot: bool) -> None:
    shard_paths = sorted(STAGE1_SHARD_DIR.glob(f"stage1_shard_*_of_{n_shards:04d}.csv"))
    if len(shard_paths) != n_shards:
        raise FileNotFoundError(f"expected {n_shards} stage1 shards, found {len(shard_paths)}")
    expected = len(list(sweep.iter_stage1(pilot=pilot)))
    merged = pd.concat([pd.read_csv(p) for p in shard_paths], ignore_index=True)
    if len(merged) != expected:
        raise ValueError(f"merge-stage1: expected {expected} rows, got {len(merged)}")
    merged.to_csv(STAGE1_CSV, index=False)
    print(f"Wrote {STAGE1_CSV} ({len(merged):,} rows)", flush=True)


def run_stage2_shard(shard_id: int, n_shards: int, *, pilot: bool, reset: bool) -> None:
    if not STAGE1_CSV.exists():
        raise FileNotFoundError(f"Missing {STAGE1_CSV}")
    STAGE2_SHARD_DIR.mkdir(parents=True, exist_ok=True)
    shard_csv = STAGE2_SHARD_DIR / f"stage2_shard_{shard_id:04d}_of_{n_shards:04d}.csv"
    shard_jsonl = STAGE2_SHARD_DIR / f"stage2_shard_{shard_id:04d}_of_{n_shards:04d}.jsonl"
    if reset:
        shard_csv.unlink(missing_ok=True)
        shard_jsonl.unlink(missing_ok=True)
    stage1_rows = read_rows(STAGE1_CSV)
    all_scenarios = list(sweep.iter_stage2(stage1_rows, pilot=pilot))
    scenarios = [sc for i, sc in enumerate(all_scenarios) if i % n_shards == shard_id]
    print(
        f"538 stage2 shard {shard_id}/{n_shards}: {len(scenarios):,} of {len(all_scenarios):,}",
        flush=True,
    )
    rows: list[dict] = []
    for idx, sc in enumerate(scenarios, start=1):
        row = sweep.run_scenario(sc)
        rows.append(row)
        append_jsonl(shard_jsonl, row)
        if idx % 5 == 0 or idx == len(scenarios):
            print(f"shard {shard_id}: {idx:,}/{len(scenarios):,}", flush=True)
    write_csv(shard_csv, rows)


def merge_stage2(n_shards: int) -> None:
    shard_paths = sorted(STAGE2_SHARD_DIR.glob(f"stage2_shard_*_of_{n_shards:04d}.csv"))
    if not shard_paths:
        raise FileNotFoundError(f"No stage2 shards in {STAGE2_SHARD_DIR}")
    stage2 = pd.concat([pd.read_csv(p) for p in shard_paths], ignore_index=True)
    stage2.to_csv(STAGE2_CSV, index=False)
    rows = stage2.to_dict("records")
    grouped = sweep.grouped_candidates(rows)
    grouped.to_csv(GROUPED_CSV, index=False)
    old_plot = sweep.PLOT_DIR
    sweep.PLOT_DIR = PLOT_DIR
    try:
        sweep.plot_top(rows, grouped, n_plots=20)
    finally:
        sweep.PLOT_DIR = old_plot
    README.write_text(
        f"# Rivanna 538 sweep\n\nStage2 rows: {len(stage2):,}\n"
        f"Stable moderate: {int(grouped['moderate_stable'].sum()) if not grouped.empty else 0:,}\n",
        encoding="utf-8",
    )
    print(f"Wrote {STAGE2_CSV}, {GROUPED_CSV}", flush=True)


def plot_candidates(
    *,
    stage2_csv: Path | None = None,
    plot_dir: Path | None = None,
    grouped_csv: Path | None = None,
    n_plots: int = 20,
) -> None:
    """Rebuild ``rivanna_faithful_538/candidate_plots/`` from merged Stage 2 CSV."""
    s2 = stage2_csv if stage2_csv is not None else STAGE2_CSV
    if not s2.is_file():
        raise FileNotFoundError(
            f"plot-candidates: missing Stage 2 CSV: {s2}\n"
            "  Sync `rivanna_faithful_538/stage2_results_merged.csv` from the cluster, "
            "or pass --stage2-csv."
        )
    rows = read_rows(s2)
    grouped = sweep.grouped_candidates(rows)

    g_out = grouped_csv if grouped_csv is not None else (s2.parent / "grouped_candidates.csv")
    g_out.parent.mkdir(parents=True, exist_ok=True)
    grouped.to_csv(g_out, index=False)
    print(f"Wrote {g_out}", flush=True)

    p_out = plot_dir if plot_dir is not None else (s2.parent / "candidate_plots")
    old_plot_dir = sweep.PLOT_DIR
    sweep.PLOT_DIR = p_out
    try:
        sweep.plot_top(rows, grouped, n_plots=n_plots)
        if sweep.plt is not None and p_out.is_dir():
            n_png = len(list(p_out.glob("candidate_*.png")))
            print(f"==> candidate_plots: {n_png} PNG(s) -> {p_out.resolve()}", flush=True)
    finally:
        sweep.PLOT_DIR = old_plot_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["stage1-shard", "merge-stage1", "stage2-shard", "merge", "plot-candidates"],
    )
    parser.add_argument("--shard-id", type=int, default=0)
    parser.add_argument("--n-shards", type=int, default=32)
    parser.add_argument("--pilot", action="store_true")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument(
        "--stage2-csv",
        type=Path,
        default=None,
        help="For plot-candidates: merged Stage 2 CSV (default: rivanna_faithful_538/stage2_results_merged.csv).",
    )
    parser.add_argument(
        "--plot-dir",
        type=Path,
        default=None,
        help="For plot-candidates: PNG output dir (default: rivanna_faithful_538/candidate_plots).",
    )
    parser.add_argument(
        "--grouped-csv",
        type=Path,
        default=None,
        help="For plot-candidates: grouped_candidates.csv path (default: next to stage2 CSV).",
    )
    parser.add_argument(
        "--n-plots",
        type=int,
        default=20,
        help="For plot-candidates: number of top grouped rows to plot (default: 20).",
    )
    args = parser.parse_args()

    if args.command == "stage1-shard":
        run_stage1_shard(args.shard_id, args.n_shards, pilot=args.pilot, reset=args.reset)
    elif args.command == "merge-stage1":
        merge_stage1(args.n_shards, pilot=args.pilot)
    elif args.command == "stage2-shard":
        run_stage2_shard(args.shard_id, args.n_shards, pilot=args.pilot, reset=args.reset)
    elif args.command == "merge":
        merge_stage2(args.n_shards)
    elif args.command == "plot-candidates":
        plot_candidates(
            stage2_csv=args.stage2_csv,
            plot_dir=args.plot_dir,
            grouped_csv=args.grouped_csv,
            n_plots=args.n_plots,
        )


if __name__ == "__main__":
    main()
