#!/usr/bin/env python3
"""Rivanna-friendly staged/array runner for the faithful 537 sweep.

Usage:
  python faithful_537_sweep_rivanna_worker.py stage1
  python faithful_537_sweep_rivanna_worker.py stage1-shard --shard-id 0 --n-shards 64
  python faithful_537_sweep_rivanna_worker.py merge-stage1 --n-shards 64
  python faithful_537_sweep_rivanna_worker.py stage2-shard --shard-id 0 --n-shards 64
  python faithful_537_sweep_rivanna_worker.py merge --n-shards 64
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

import faithful_537_sweep as sweep


BASE = Path(__file__).resolve().parent
RIVANNA_DIR = BASE / "rivanna_faithful_537"
STAGE1_SHARD_DIR = RIVANNA_DIR / "stage1_shards"
SHARD_DIR = RIVANNA_DIR / "stage2_shards"
PLOT_DIR = RIVANNA_DIR / "candidate_plots"
STAGE1_CSV = RIVANNA_DIR / "stage1_results.csv"
STAGE2_CSV = RIVANNA_DIR / "stage2_results_merged.csv"
GROUPED_CSV = RIVANNA_DIR / "grouped_candidates.csv"
README = RIVANNA_DIR / "README.md"


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
    # Keep types close enough for sweep.iter_stage2 and grouping.
    for row in rows:
        for key in [
            "local_rank_weight",
            "sorting_noise_sd",
            "min_ability_for_promotion",
            "tail_drop_frac",
            "tail_slope_last3",
            "peak_y",
            "final_y",
        ]:
            if key in row:
                row[key] = float(row[key])
        for key in ["n", "k", "n_pools", "n_runs", "n_pool_bins", "seed", "peak_bin"]:
            if key in row and not pd.isna(row[key]):
                row[key] = int(row[key])
        for key in ["interior_peak", "moderate_downturn"]:
            if key in row:
                val = row[key]
                row[key] = bool(val) if isinstance(val, (bool, np.bool_)) else str(val).lower() == "true"
    return rows


def run_stage1(reset: bool) -> None:
    RIVANNA_DIR.mkdir(parents=True, exist_ok=True)
    if reset:
        STAGE1_CSV.unlink(missing_ok=True)
        (RIVANNA_DIR / "stage1_results.jsonl").unlink(missing_ok=True)
    scenarios = list(sweep.iter_stage1())
    print(f"Rivanna stage1 scenarios: {len(scenarios):,}", flush=True)
    rows: list[dict] = []
    jsonl = RIVANNA_DIR / "stage1_results.jsonl"
    for idx, sc in enumerate(scenarios, start=1):
        row = sweep.run_scenario(sc)
        rows.append(row)
        append_jsonl(jsonl, row)
        if idx % 500 == 0 or idx == len(scenarios):
            best = max(
                (float(r["tail_drop_frac"]) for r in rows if math.isfinite(float(r["tail_drop_frac"]))),
                default=float("nan"),
            )
            print(f"stage1 {idx:,}/{len(scenarios):,}; best tail drop={best:.3f}", flush=True)
    write_csv(STAGE1_CSV, rows)
    print(f"Wrote {STAGE1_CSV}", flush=True)


def run_stage1_shard(shard_id: int, n_shards: int, reset: bool) -> None:
    RIVANNA_DIR.mkdir(parents=True, exist_ok=True)
    STAGE1_SHARD_DIR.mkdir(parents=True, exist_ok=True)
    shard_csv = STAGE1_SHARD_DIR / f"stage1_shard_{shard_id:04d}_of_{n_shards:04d}.csv"
    shard_jsonl = STAGE1_SHARD_DIR / f"stage1_shard_{shard_id:04d}_of_{n_shards:04d}.jsonl"
    if reset:
        shard_csv.unlink(missing_ok=True)
        shard_jsonl.unlink(missing_ok=True)
    all_scenarios = list(sweep.iter_stage1())
    scenarios = [sc for i, sc in enumerate(all_scenarios) if i % n_shards == shard_id]
    print(
        f"Rivanna stage1 shard {shard_id}/{n_shards}: {len(scenarios):,} of {len(all_scenarios):,}",
        flush=True,
    )
    rows: list[dict] = []
    for idx, sc in enumerate(scenarios, start=1):
        row = sweep.run_scenario(sc)
        rows.append(row)
        append_jsonl(shard_jsonl, row)
        if idx % 100 == 0 or idx == len(scenarios):
            best = max(
                (float(r["tail_drop_frac"]) for r in rows if math.isfinite(float(r["tail_drop_frac"]))),
                default=float("nan"),
            )
            print(f"stage1 shard {shard_id}: {idx:,}/{len(scenarios):,}; best tail drop={best:.3f}", flush=True)
    write_csv(shard_csv, rows)
    print(f"Wrote {shard_csv}", flush=True)


def merge_stage1(n_shards: int) -> None:
    shard_paths = sorted(STAGE1_SHARD_DIR.glob(f"stage1_shard_*_of_{n_shards:04d}.csv"))
    if len(shard_paths) != n_shards:
        raise FileNotFoundError(
            f"merge-stage1: expected {n_shards} shard CSVs matching "
            f"stage1_shard_*_of_{n_shards:04d}.csv in {STAGE1_SHARD_DIR}, "
            f"found {len(shard_paths)}"
        )
    expected = len(list(sweep.iter_stage1()))
    frames = [pd.read_csv(path) for path in shard_paths]
    merged = pd.concat(frames, ignore_index=True)
    if len(merged) != expected:
        raise ValueError(
            f"merge-stage1: expected {expected} rows (full Stage 1 grid), got {len(merged)} "
            f"from {len(shard_paths)} shards — check shard tasks completed successfully."
        )
    merged.to_csv(STAGE1_CSV, index=False)
    print(f"Wrote {STAGE1_CSV} ({len(merged):,} rows)", flush=True)


def run_stage2_shard(shard_id: int, n_shards: int, reset: bool) -> None:
    if not STAGE1_CSV.exists():
        raise FileNotFoundError(f"Missing {STAGE1_CSV}; run stage1 first.")
    SHARD_DIR.mkdir(parents=True, exist_ok=True)
    shard_csv = SHARD_DIR / f"stage2_shard_{shard_id:04d}_of_{n_shards:04d}.csv"
    shard_jsonl = SHARD_DIR / f"stage2_shard_{shard_id:04d}_of_{n_shards:04d}.jsonl"
    if reset:
        shard_csv.unlink(missing_ok=True)
        shard_jsonl.unlink(missing_ok=True)
    stage1_rows = read_rows(STAGE1_CSV)
    all_scenarios = list(sweep.iter_stage2(stage1_rows))
    scenarios = [sc for i, sc in enumerate(all_scenarios) if i % n_shards == shard_id]
    print(
        f"Rivanna stage2 shard {shard_id}/{n_shards}: {len(scenarios):,} of {len(all_scenarios):,}",
        flush=True,
    )
    rows: list[dict] = []
    for idx, sc in enumerate(scenarios, start=1):
        row = sweep.run_scenario(sc)
        rows.append(row)
        append_jsonl(shard_jsonl, row)
        if idx % 5 == 0 or idx == len(scenarios):
            best = max(
                (float(r["tail_drop_frac"]) for r in rows if math.isfinite(float(r["tail_drop_frac"]))),
                default=float("nan"),
            )
            print(f"shard {shard_id}: {idx:,}/{len(scenarios):,}; best tail drop={best:.3f}", flush=True)
    write_csv(shard_csv, rows)
    print(f"Wrote {shard_csv}", flush=True)


def merge(n_shards: int) -> None:
    shard_paths = sorted(SHARD_DIR.glob(f"stage2_shard_*_of_{n_shards:04d}.csv"))
    if not shard_paths:
        raise FileNotFoundError(f"No shard CSVs found in {SHARD_DIR}")
    frames = [pd.read_csv(path) for path in shard_paths]
    stage2 = pd.concat(frames, ignore_index=True)
    stage2.to_csv(STAGE2_CSV, index=False)
    rows = stage2.to_dict("records")
    grouped = sweep.grouped_candidates(rows)
    grouped.to_csv(GROUPED_CSV, index=False)

    # Reuse plotting helper, temporarily pointing it at Rivanna output.
    old_plot_dir = sweep.PLOT_DIR
    sweep.PLOT_DIR = PLOT_DIR
    try:
        sweep.plot_top(rows, grouped, n_plots=20)
    finally:
        sweep.PLOT_DIR = old_plot_dir

    stable = int(grouped["moderate_stable"].sum()) if not grouped.empty else 0
    README.write_text(
        "\n".join(
            [
                "# Rivanna Faithful 537 Sweep",
                "",
                f"Stage 1 rows: {len(read_rows(STAGE1_CSV)):,}",
                f"Stage 2 rows: {len(stage2):,}",
                f"Stage 2 shard CSVs merged: {len(shard_paths):,}",
                f"Stable moderate downturn settings: {stable:,}",
                "",
                "Moderate stable rule: at least 60% of seeds have an interior peak with final bin",
                "at least 5% below that peak, and mean tail drop is at least 5%.",
                "",
                f"Grouped candidates: `{GROUPED_CSV.name}`",
                f"Candidate plots: `{PLOT_DIR.name}/`",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {STAGE2_CSV}", flush=True)
    print(f"Wrote {GROUPED_CSV}", flush=True)
    print(f"Wrote {README}", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=["stage1", "stage1-shard", "merge-stage1", "stage2-shard", "merge"],
    )
    parser.add_argument("--shard-id", type=int, default=0)
    parser.add_argument("--n-shards", type=int, default=64)
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    if args.command == "stage1":
        run_stage1(reset=args.reset)
    elif args.command == "stage1-shard":
        if not (0 <= args.shard_id < args.n_shards):
            raise ValueError("--shard-id must be in [0, n_shards)")
        run_stage1_shard(args.shard_id, args.n_shards, reset=args.reset)
    elif args.command == "merge-stage1":
        merge_stage1(args.n_shards)
    elif args.command == "stage2-shard":
        if not (0 <= args.shard_id < args.n_shards):
            raise ValueError("--shard-id must be in [0, n_shards)")
        run_stage2_shard(args.shard_id, args.n_shards, reset=args.reset)
    elif args.command == "merge":
        merge(args.n_shards)


if __name__ == "__main__":
    main()
