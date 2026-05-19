#!/usr/bin/env python3
"""Parameter sweep for 538 generative Tier 1 (soft assign + selection).

Faithful to `tier1_pool_assignment.py` + `tier1_generative_eda.py` (CELL 10–12):
- draw T_j, draw A_i, soft assign
- LOO poolq_loo, selection score, winner draw A/B/C
- bin on **player LOO Q** (not 537 pool-mean bins)

Stage 1: broad screen. Stage 2: verify promising specs across seeds.
Outputs append incrementally (JSONL + CSV) for resume and HPC shards.

Local:
  python faithful_538_sweep.py --pilot
  python faithful_538_sweep.py --stage1-only
  python faithful_538_sweep.py --reset
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

_SPORTS = Path(__file__).resolve().parents[2]
_REPO = _SPORTS.parent
for _p in (_SPORTS, _REPO):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import tier1_pool_assignment as tpa  # noqa: E402
from sports_pipeline.panel_build import assign_poolq_bin_labels  # noqa: E402
from tier1_generative_eda import SelectionConfig  # noqa: E402

OUT_DIR = Path(__file__).resolve().parent
RESULTS_JSONL = OUT_DIR / "faithful_538_sweep_results.jsonl"
STAGE1_CSV = OUT_DIR / "faithful_538_sweep_stage1_results.csv"
STAGE2_CSV = OUT_DIR / "faithful_538_sweep_stage2_results.csv"
GROUPED_CSV = OUT_DIR / "faithful_538_sweep_grouped_candidates.csv"
README = OUT_DIR / "faithful_538_sweep_README.md"
PLOT_DIR = OUT_DIR / "faithful_538_candidate_plots"

_BASE_PARAMS = tpa.AssignmentParams.from_tier1_sim_config(_SPORTS / "tier1_sim_config.py")
_spec_cfg = importlib.util.spec_from_file_location(
    "tier1_sim_config", _SPORTS / "tier1_sim_config.py"
)
_cfg_mod = importlib.util.module_from_spec(_spec_cfg)
assert _spec_cfg is not None and _spec_cfg.loader is not None
_spec_cfg.loader.exec_module(_cfg_mod)


@dataclass(frozen=True)
class Scenario:
    stage: str
    n_teams: int
    roster_size: int
    target_mean_dist: str
    target_mean_low: float
    target_mean_high: float
    assignment_kernel: str
    assignment_temperature: float
    preferential_alpha: float
    ability_draw: str
    n_selected: int
    score_mode: str
    loo_gap_weight: float
    winner_selection: str
    n_bins: int
    bin_mode: str
    n_runs: int
    seed: int


def _assignment_params(sc: Scenario) -> tpa.AssignmentParams:
    return tpa.AssignmentParams(
        n_teams=sc.n_teams,
        roster_size=sc.roster_size,
        target_mean_dist=sc.target_mean_dist,
        target_mean_low=sc.target_mean_low,
        target_mean_high=sc.target_mean_high,
        target_mean_mu=_BASE_PARAMS.target_mean_mu,
        target_mean_sigma=_BASE_PARAMS.target_mean_sigma,
        assignment_kernel=sc.assignment_kernel,
        assignment_temperature=sc.assignment_temperature,
        preferential_alpha=sc.preferential_alpha,
        preferential_k=_BASE_PARAMS.preferential_k,
        ability_draw=sc.ability_draw,
        ability_mean=_BASE_PARAMS.ability_mean,
        ability_sd=_BASE_PARAMS.ability_sd,
        ability_clip_low=_BASE_PARAMS.ability_clip_low,
        ability_clip_high=_BASE_PARAMS.ability_clip_high,
        ability_student_t_df=_BASE_PARAMS.ability_student_t_df,
        ability_student_t_scale=_BASE_PARAMS.ability_student_t_scale,
        sorting_noise_sd=_BASE_PARAMS.sorting_noise_sd,
    )


def _coverage_peak(teams: pd.DataFrame) -> float:
    grid = np.linspace(-2.0, 2.0, 81)
    lo = teams["min"].to_numpy(dtype=float)
    hi = teams["max"].to_numpy(dtype=float)
    cov = np.zeros(len(grid), dtype=float)
    for a, b in zip(lo, hi):
        cov += (grid >= a) & (grid <= b)
    return float(cov.max())


def _curve_metrics(y_valid: np.ndarray) -> dict:
    if y_valid.size == 0:
        return {
            "peak_bin": -1,
            "peak_y": float("nan"),
            "first_bin_y": float("nan"),
            "final_y": float("nan"),
            "tail_drop_frac": float("nan"),
            "left_lift_frac": float("nan"),
            "tail_slope_last3": float("nan"),
            "interior_peak": False,
            "moderate_downturn": False,
        }
    peak_idx = int(np.argmax(y_valid))
    peak_y = float(y_valid[peak_idx])
    first_y = float(y_valid[0])
    final_y = float(y_valid[-1])
    tail_drop_frac = (peak_y - final_y) / peak_y if peak_y > 0 else 0.0
    left_lift_frac = (peak_y - first_y) / peak_y if peak_y > 0 else 0.0
    if y_valid.size >= 3:
        tail_slope = float(y_valid[-1] - y_valid[-3])
    elif y_valid.size >= 2:
        tail_slope = float(y_valid[-1] - y_valid[-2])
    else:
        tail_slope = float("nan")
    interior_peak = bool(y_valid.size >= 3 and 1 <= peak_idx <= y_valid.size - 2)
    both_ends_below = bool(first_y < peak_y and final_y < peak_y)
    moderate_downturn = bool(
        interior_peak
        and both_ends_below
        and peak_y > 0
        and left_lift_frac >= 0.05
        and tail_drop_frac >= 0.05
    )
    return {
        "peak_bin": peak_idx,
        "peak_y": peak_y,
        "first_bin_y": first_y,
        "final_y": final_y,
        "tail_drop_frac": tail_drop_frac,
        "left_lift_frac": left_lift_frac,
        "tail_slope_last3": tail_slope,
        "interior_peak": interior_peak,
        "moderate_downturn": moderate_downturn,
    }


def run_scenario(sc: Scenario) -> dict:
    """One grid point: aggregate selection-rate curve over n_runs."""
    params = _assignment_params(sc)
    rng = np.random.default_rng(sc.seed)
    n_bins = int(sc.n_bins)
    sum_rate = np.zeros(n_bins, dtype=float)
    sum_x = np.zeros(n_bins, dtype=float)
    sum_n = np.zeros(n_bins, dtype=float)
    seen = np.zeros(n_bins, dtype=float)
    coverage_peak = float("nan")
    median_pool_sd = float("nan")

    for run_i in range(sc.n_runs):
        run_rng = np.random.default_rng(int(rng.integers(0, 2**31 - 1)))
        players, teams, _ = tpa.simulate_generative_rosters(
            params, rng=run_rng, method="soft"
        )
        if run_i == sc.n_runs - 1:
            coverage_peak = _coverage_peak(teams)
            median_pool_sd = float(teams["pool_sd"].median())
        players = tpa.assign_selection(
            players,
            run_rng,
            n_selected=sc.n_selected,
            score_mode=sc.score_mode,
            loo_gap_weight=sc.loo_gap_weight,
            winner_selection=sc.winner_selection,
        )
        use = players.dropna(subset=["poolq_loo", "Y_selected"]).copy()
        if use.empty:
            continue
        use["bin"] = assign_poolq_bin_labels(
            use["poolq_loo"], n_bins, sc.bin_mode
        )
        for b in range(n_bins):
            mask = use["bin"] == b
            if not np.any(mask):
                continue
            sum_rate[b] += float(use.loc[mask, "Y_selected"].mean())
            sum_x[b] += float(use.loc[mask, "poolq_loo"].mean())
            sum_n[b] += float(mask.sum())
            seen[b] += 1.0

    with np.errstate(invalid="ignore", divide="ignore"):
        y = sum_rate / seen
        x = sum_x / seen
    valid = np.isfinite(y) & (seen > 0)
    y_valid = y[valid]
    x_valid = x[valid]
    metrics = _curve_metrics(y_valid)

    out = asdict(sc)
    out.update(metrics)
    out.update(
        {
            "n_individuals": params.n_individuals,
            "coverage_peak": coverage_peak,
            "median_pool_sd": median_pool_sd,
            "curve_x": json.dumps(
                [
                    None if not np.isfinite(v) else round(float(v), 8)
                    for v in x
                ]
            ),
            "curve_y": json.dumps(
                [
                    None if not np.isfinite(v) else round(float(v), 8)
                    for v in y
                ]
            ),
            "curve_n": json.dumps([round(float(v), 3) for v in sum_n]),
        }
    )
    return out


def scenario_key(row: dict) -> tuple:
    fields = [
        "n_teams",
        "roster_size",
        "target_mean_dist",
        "target_mean_low",
        "target_mean_high",
        "assignment_kernel",
        "assignment_temperature",
        "preferential_alpha",
        "ability_draw",
        "n_selected",
        "score_mode",
        "loo_gap_weight",
        "winner_selection",
        "n_bins",
        "bin_mode",
    ]
    return tuple(row[f] for f in fields)


def _yield_scenarios(
    *,
    stage: str,
    n_runs: int,
    seed: int,
    pilot: bool,
) -> Iterable[Scenario]:
    roster = int(_BASE_PARAMS.roster_size)
    t_low = float(_BASE_PARAMS.target_mean_low)
    t_high = float(_BASE_PARAMS.target_mean_high)
    bin_mode = str(getattr(_cfg_mod, "GENERATIVE_POOLQ_BINNING", "quantile"))
    n_bins = int(getattr(_cfg_mod, "GENERATIVE_N_BINS", 12))

    if pilot:
        taus = [0.35, 0.55, 0.75]
        n_teams_vals = [50, 100]
        kernels = ["gaussian"]
        abilities = ["normal_clipped"]
        pref_alphas = [0.0]
        ks = [80, 160]
        loo_ws = [0.5, 0.75, 1.0]
        scores = ["loo_gap_plus_ability", "ability"]
        winners = ["C", "A"]
        targets = ["uniform"]
    else:
        taus = [0.25, 0.45, 0.65, 0.9]
        n_teams_vals = [50, 100, 150]
        kernels = ["gaussian", "cauchy"]
        abilities = ["normal_clipped", "normal_plus_student_t"]
        pref_alphas = [0.0, 0.5]
        ks = [60, 120, 200]
        loo_ws = [0.0, 0.25, 0.5, 0.75, 1.0]
        scores = ["loo_gap_plus_ability", "ability"]
        winners = ["A", "B", "C"]
        targets = ["uniform", "normal_clipped"]

    for (
        tau,
        n_teams,
        kernel,
        ability,
        pref_a,
        k_sel,
        loo_w,
        score,
        winner,
        target_dist,
    ) in itertools.product(
        taus,
        n_teams_vals,
        kernels,
        abilities,
        pref_alphas,
        ks,
        loo_ws,
        scores,
        winners,
        targets,
    ):
        if score == "ability" and loo_w != 0.0:
            continue
        if score == "loo_gap_plus_ability" and loo_w == 0.0:
            continue
        yield Scenario(
            stage=stage,
            n_teams=int(n_teams),
            roster_size=roster,
            target_mean_dist=target_dist,
            target_mean_low=t_low,
            target_mean_high=t_high,
            assignment_kernel=kernel,
            assignment_temperature=float(tau),
            preferential_alpha=float(pref_a),
            ability_draw=ability,
            n_selected=int(k_sel),
            score_mode=score,
            loo_gap_weight=float(loo_w),
            winner_selection=winner,
            n_bins=n_bins,
            bin_mode=bin_mode,
            n_runs=n_runs,
            seed=seed,
        )


def iter_stage1(*, pilot: bool = False) -> Iterable[Scenario]:
    n_runs = 40 if pilot else 60
    yield from _yield_scenarios(stage="stage1", n_runs=n_runs, seed=538001, pilot=pilot)


def iter_stage2(stage1_rows: list[dict], *, pilot: bool = False) -> Iterable[Scenario]:
    ranked = sorted(
        stage1_rows,
        key=lambda r: (
            not bool(r["moderate_downturn"]),
            not bool(r["interior_peak"]),
            -float(r["tail_drop_frac"]) if math.isfinite(float(r["tail_drop_frac"])) else 0.0,
            -float(r.get("coverage_peak", 0) or 0),
        ),
    )
    candidates: list[dict] = []
    seen_keys: set[tuple] = set()
    cap = 80 if pilot else 200
    for row in ranked:
        if bool(row["moderate_downturn"]) or (
            bool(row["interior_peak"]) and float(row["tail_drop_frac"]) > 0.02
        ):
            key = scenario_key(row)
            if key not in seen_keys:
                candidates.append(row)
                seen_keys.add(key)
        if len(candidates) >= cap:
            break

    seeds = [538001, 538002, 538003] if pilot else [538001, 538002, 538003, 538004, 538005]
    n_runs = 120 if pilot else 200
    for row in candidates:
        for seed in seeds:
            yield Scenario(
                stage="stage2",
                n_teams=int(row["n_teams"]),
                roster_size=int(row["roster_size"]),
                target_mean_dist=str(row["target_mean_dist"]),
                target_mean_low=float(row["target_mean_low"]),
                target_mean_high=float(row["target_mean_high"]),
                assignment_kernel=str(row["assignment_kernel"]),
                assignment_temperature=float(row["assignment_temperature"]),
                preferential_alpha=float(row["preferential_alpha"]),
                ability_draw=str(row["ability_draw"]),
                n_selected=int(row["n_selected"]),
                score_mode=str(row["score_mode"]),
                loo_gap_weight=float(row["loo_gap_weight"]),
                winner_selection=str(row["winner_selection"]),
                n_bins=int(row["n_bins"]),
                bin_mode=str(row["bin_mode"]),
                n_runs=n_runs,
                seed=seed,
            )


def append_jsonl(row: dict) -> None:
    with RESULTS_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
        f.flush()


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def grouped_candidates(stage2_rows: list[dict]) -> pd.DataFrame:
    if not stage2_rows:
        return pd.DataFrame()
    df = pd.DataFrame(stage2_rows)
    group_cols = [
        "n_teams",
        "roster_size",
        "target_mean_dist",
        "target_mean_low",
        "target_mean_high",
        "assignment_kernel",
        "assignment_temperature",
        "preferential_alpha",
        "ability_draw",
        "n_selected",
        "score_mode",
        "loo_gap_weight",
        "winner_selection",
        "n_bins",
        "bin_mode",
        "n_runs",
    ]
    grouped = (
        df.groupby(group_cols, dropna=False, observed=True)
        .agg(
            seeds=("seed", "nunique"),
            moderate_seed_count=("moderate_downturn", "sum"),
            interior_seed_count=("interior_peak", "sum"),
            mean_left_lift_frac=("left_lift_frac", "mean"),
            mean_tail_drop_frac=("tail_drop_frac", "mean"),
            min_tail_drop_frac=("tail_drop_frac", "min"),
            mean_tail_slope_last3=("tail_slope_last3", "mean"),
            mean_peak_y=("peak_y", "mean"),
            mean_final_y=("final_y", "mean"),
            mean_coverage_peak=("coverage_peak", "mean"),
            mean_median_pool_sd=("median_pool_sd", "mean"),
        )
        .reset_index()
    )
    grouped["moderate_stable"] = (
        (grouped["seeds"] >= 3)
        & (grouped["moderate_seed_count"] >= np.ceil(grouped["seeds"] * 0.6))
        & (grouped["mean_tail_drop_frac"] >= 0.05)
        & (grouped["mean_left_lift_frac"] >= 0.05)
    )
    grouped = grouped.sort_values(
        ["moderate_stable", "mean_tail_drop_frac", "mean_left_lift_frac", "interior_seed_count"],
        ascending=[False, False, False, False],
        kind="mergesort",
    )
    return grouped


def _format_plot_title(rank: int, row: pd.Series) -> str:
    return (
        f"538 sweep #{rank}: τ={row['assignment_temperature']:.2f} "
        f"J={int(row['n_teams'])} K={int(row['n_selected'])} "
        f"w={row['loo_gap_weight']:.2f} winner={row['winner_selection']}"
    )


def plot_top(stage2_rows: list[dict], grouped: pd.DataFrame, n_plots: int = 12) -> None:
    if plt is None or grouped.empty:
        return
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(stage2_rows)
    group_cols = [
        "n_teams",
        "roster_size",
        "target_mean_dist",
        "target_mean_low",
        "target_mean_high",
        "assignment_kernel",
        "assignment_temperature",
        "preferential_alpha",
        "ability_draw",
        "n_selected",
        "score_mode",
        "loo_gap_weight",
        "winner_selection",
        "n_bins",
        "bin_mode",
        "n_runs",
    ]
    for idx, grow in grouped.head(n_plots).reset_index(drop=True).iterrows():
        mask = np.ones(len(df), dtype=bool)
        for col in group_cols:
            mask &= df[col].to_numpy() == grow[col]
        sub = df.loc[mask]
        if sub.empty:
            continue
        curves_y = np.array([json.loads(v) for v in sub["curve_y"]], dtype=float)
        curves_x_list = [json.loads(v) for v in sub["curve_x"]]
        curves_x = np.array(
            [
                [
                    np.nan if v is None else float(v)
                    for v in row
                ]
                for row in curves_x_list
            ],
            dtype=float,
        )
        x = np.nanmean(curves_x, axis=0)
        y_mean = np.nanmean(curves_y, axis=0)
        y_min = np.nanmin(curves_y, axis=0)
        y_max = np.nanmax(curves_y, axis=0)
        if not np.any(np.isfinite(x)):
            x = np.arange(len(y_mean), dtype=float)
            xlabel = "LOO Q bin index"
        else:
            xlabel = "Bin mean LOO pool quality (poolq_loo)"

        fig, ax = plt.subplots(figsize=(8.2, 5.0))
        ax.fill_between(x, y_min, y_max, color="C0", alpha=0.18, label="seed range")
        ax.plot(x, y_mean, "o-", color="C0", label="mean across seeds")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Mean selection rate")
        ax.set_title(_format_plot_title(idx + 1, grow), fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=8)
        fig.tight_layout()
        fig.savefig(PLOT_DIR / f"candidate_{idx + 1:02d}.png", dpi=160)
        plt.close(fig)


def write_readme(stage1_rows: list[dict], stage2_rows: list[dict], grouped: pd.DataFrame) -> None:
    stable = int(grouped["moderate_stable"].sum()) if not grouped.empty else 0
    text = f"""# Faithful 538 generative sweep

Generated by `faithful_538_sweep.py`.

## Design

- **538 Thread A:** soft assign to fixed T_j attractors (`tier1_pool_assignment.py`).
- **Selection:** LOO gap + ability score, winner A/B/C (`assign_selection`).
- **Curve:** mean `Y_selected` by **player LOO poolq_loo** quantile bins (CELL 12 logic).
- **Not** the 537 faithful sweep (sort-and-chop, pool-mean bins, local rank).

## Moderate downturn rule

Same as 537 sweep: interior peak, both ends ≥5% below peak (`moderate_downturn`).
Grouped `moderate_stable` when ≥60% of seeds pass across Stage 2.

## Pool diagnostics (last run per scenario)

- `coverage_peak`: Plot A-style overlap (want ≫1 vs 530).
- `median_pool_sd`: within-roster ability SD (target ~0.8 z-scale).

## Outputs

- `{RESULTS_JSONL.name}`
- `{STAGE1_CSV.name}`, `{STAGE2_CSV.name}`, `{GROUPED_CSV.name}`
- `faithful_538_candidate_plots/`

## Counts

- Stage 1: {len(stage1_rows):,}
- Stage 2: {len(stage2_rows):,}
- Stable moderate downturn settings: {stable:,}

## Local commands

```bash
cd sports/outputs/simulation_sweeps
python faithful_538_sweep.py --pilot --reset
python faithful_538_sweep.py --stage1-only --reset
python faithful_538_sweep.py --reset
```

## Rivanna

Use `faithful_538_sweep_rivanna_worker.py` (mirror of 537 worker). Push with `./scripts/rsync_push_to_hpc.sh sweep`.
"""
    README.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="538 generative inverted-U sweep")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--pilot", action="store_true", help="small grid for Mac/local")
    parser.add_argument("--stage1-only", action="store_true")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if args.reset:
        for path in (RESULTS_JSONL, STAGE1_CSV, STAGE2_CSV, GROUPED_CSV, README):
            path.unlink(missing_ok=True)
        if PLOT_DIR.is_dir():
            for p in PLOT_DIR.glob("candidate_*.png"):
                p.unlink()

    stage1 = list(iter_stage1(pilot=args.pilot))
    print(f"Stage 1 scenarios: {len(stage1):,} (pilot={args.pilot})", flush=True)
    stage1_rows: list[dict] = []
    for idx, sc in enumerate(stage1, start=1):
        row = run_scenario(sc)
        stage1_rows.append(row)
        append_jsonl(row)
        if idx % 50 == 0 or idx == len(stage1):
            best = max(
                (
                    float(r["tail_drop_frac"])
                    for r in stage1_rows
                    if math.isfinite(float(r["tail_drop_frac"]))
                ),
                default=float("nan"),
            )
            n_mod = sum(1 for r in stage1_rows if r["moderate_downturn"])
            print(
                f"Stage 1 {idx:,}/{len(stage1):,}; moderate={n_mod}; best tail drop={best:.3f}",
                flush=True,
            )
    write_csv(STAGE1_CSV, stage1_rows)
    print(f"Wrote {STAGE1_CSV}", flush=True)

    if args.stage1_only:
        write_readme(stage1_rows, [], pd.DataFrame())
        return

    stage2 = list(iter_stage2(stage1_rows, pilot=args.pilot))
    print(f"Stage 2 scenarios: {len(stage2):,}", flush=True)
    stage2_rows: list[dict] = []
    for idx, sc in enumerate(stage2, start=1):
        row = run_scenario(sc)
        stage2_rows.append(row)
        append_jsonl(row)
        if idx % 20 == 0 or idx == len(stage2):
            grouped = grouped_candidates(stage2_rows)
            stable = int(grouped["moderate_stable"].sum()) if not grouped.empty else 0
            print(f"Stage 2 {idx:,}/{len(stage2):,}; stable={stable:,}", flush=True)
    write_csv(STAGE2_CSV, stage2_rows)
    grouped = grouped_candidates(stage2_rows)
    grouped.to_csv(GROUPED_CSV, index=False)
    plot_top(stage2_rows, grouped)
    write_readme(stage1_rows, stage2_rows, grouped)
    print("Done.")
    print(f"Grouped: {GROUPED_CSV}")
    print(f"Plots: {PLOT_DIR}")


if __name__ == "__main__":
    main()
