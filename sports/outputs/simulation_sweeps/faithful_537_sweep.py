#!/usr/bin/env python3
"""Faithful parameter sweep for 537_Sports_Simulation mechanics.

This script mirrors the current notebook mechanics before adding any new
congestion/opportunity terms:

- ability laws A/B/C
- random / assortative / disassortative pool assignment
- sorting noise used only for pool assignment
- ability, global rank, local rank, and additive local-rank/ability scores
- winner draws A/B/C from the 537 manual
- pool-quality summaries using mean LOO peer A in pool-mean-A bins

Outputs are written incrementally so long sweeps can be inspected or resumed.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # keep the numerical sweep runnable in lean shells
    plt = None

_CELL10_CATALOG = Path(__file__).resolve().parents[2] / "cell10_knob_catalog.py"
_spec_cat = importlib.util.spec_from_file_location("cell10_knob_catalog", _CELL10_CATALOG)
_cell10_catalog = importlib.util.module_from_spec(_spec_cat)
assert _spec_cat.loader is not None
_spec_cat.loader.exec_module(_cell10_catalog)

OUT_DIR = Path(__file__).resolve().parent
RESULTS_JSONL = OUT_DIR / "faithful_537_sweep_results.jsonl"
STAGE1_CSV = OUT_DIR / "faithful_537_sweep_stage1_results.csv"
STAGE2_CSV = OUT_DIR / "faithful_537_sweep_stage2_results.csv"
GROUPED_CSV = OUT_DIR / "faithful_537_sweep_grouped_candidates.csv"
README = OUT_DIR / "faithful_537_sweep_README.md"
PLOT_DIR = OUT_DIR / "candidate_plots"


@dataclass(frozen=True)
class Scenario:
    stage: str
    ability_choice: str
    pool_assignment: str
    winner_choice: str
    score_mode: str
    local_rank_weight: float
    sorting_noise_sd: float
    min_ability_for_promotion: float
    n: int
    k: int
    n_pools: int
    n_runs: int
    n_pool_bins: int
    seed: int


def generate_ability(rng: np.random.Generator, n: int, choice: str) -> np.ndarray:
    if choice == "A":
        return rng.uniform(0.0, 1.0, size=n)
    if choice == "B":
        return np.clip(rng.normal(loc=0.5, scale=0.18, size=n), 0.0, 1.0)
    if choice == "C":
        vals = rng.beta(a=2.0, b=5.0, size=n)
        vmax = float(vals.max())
        return vals / vmax if vmax > 0 else vals
    raise ValueError(f"unknown ability choice {choice!r}")


def rank_score(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty_like(order, dtype=float)
    ranks[order] = np.arange(1, len(values) + 1, dtype=float)
    return ranks / float(len(values))


def normalized_weights(score: np.ndarray) -> np.ndarray:
    w = np.asarray(score, dtype=float)
    w = np.where(np.isfinite(w), w, 0.0)
    w = np.clip(w, 0.0, None)
    total = float(w.sum())
    if total <= 0:
        return np.full(len(w), 1.0 / len(w))
    return w / total


def choose_winners(
    rng: np.random.Generator,
    weights: np.ndarray,
    k: int,
    choice: str,
) -> np.ndarray:
    n = len(weights)
    w = np.asarray(weights, dtype=float)
    w = np.where(np.isfinite(w), w, 0.0)
    w = np.clip(w, 0.0, None)
    n_positive = int(np.count_nonzero(w > 0))
    if n_positive == 0:
        return np.zeros(n, dtype=bool)
    k_eff = min(int(k), n_positive)
    if choice == "A":
        p = normalized_weights(w)
        idx = rng.choice(n, size=k_eff, replace=False, p=p)
        winners = np.zeros(n, dtype=bool)
        winners[idx] = True
        return winners
    if choice == "B":
        p = np.minimum(normalized_weights(w) * k, 1.0)
        return rng.uniform(size=n) < p
    if choice == "C":
        idx = np.argsort(w, kind="mergesort")[-k_eff:]
        winners = np.zeros(n, dtype=bool)
        winners[idx] = True
        return winners
    raise ValueError(f"unknown winner choice {choice!r}")


def equal_pool_template(n: int, n_pools: int) -> np.ndarray:
    return np.repeat(np.arange(n_pools), int(np.ceil(n / n_pools)))[:n]


def assign_pool_ids(
    rng: np.random.Generator,
    ability: np.ndarray,
    n_pools: int,
    choice: str,
    sorting_noise_sd: float,
) -> tuple[np.ndarray, np.ndarray]:
    n = len(ability)
    base = equal_pool_template(n, n_pools)
    pool_id = np.empty(n, dtype=np.int64)
    noise_sd = max(float(sorting_noise_sd), 0.0)
    signal = ability if noise_sd == 0.0 else ability + rng.normal(0.0, noise_sd, size=n)
    if choice == "A":
        return rng.permutation(base), signal
    order = np.argsort(signal, kind="mergesort")
    if choice == "B":
        pool_id[order] = base
        return pool_id, signal
    if choice == "C":
        pool_id[order] = np.arange(n) % n_pools
        return pool_id, signal
    raise ValueError(f"unknown pool assignment {choice!r}")


def local_rank_and_pool_stats(
    ability: np.ndarray,
    pool_id: np.ndarray,
    n_pools: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    n = len(ability)
    pool_sum = np.bincount(pool_id, weights=ability, minlength=n_pools)
    pool_count = np.bincount(pool_id, minlength=n_pools).astype(float)
    pool_mean = pool_sum / pool_count
    poolq_loo = (pool_sum[pool_id] - ability) / np.maximum(pool_count[pool_id] - 1.0, np.nan)

    local_rank = np.empty(n, dtype=float)
    for pid in range(n_pools):
        idx = np.flatnonzero(pool_id == pid)
        order = idx[np.argsort(ability[idx], kind="mergesort")]
        ranks = np.arange(1, len(idx) + 1, dtype=float) / float(len(idx))
        local_rank[order] = ranks
    return local_rank, pool_mean, poolq_loo, pool_count


def pool_bin_codes(pool_mean: np.ndarray, n_pool_bins: int) -> np.ndarray:
    pool_order = np.argsort(pool_mean, kind="mergesort")
    chunks = np.array_split(pool_order, n_pool_bins)
    codes = np.empty(len(pool_mean), dtype=np.int64)
    for b, chunk in enumerate(chunks):
        codes[chunk] = b
    return codes


def run_scenario(sc: Scenario) -> dict:
    rng = np.random.default_rng(sc.seed)
    sum_rate = np.zeros(sc.n_pool_bins, dtype=float)
    sum_x = np.zeros(sc.n_pool_bins, dtype=float)
    sum_n = np.zeros(sc.n_pool_bins, dtype=float)
    seen = np.zeros(sc.n_pool_bins, dtype=float)

    for _run in range(sc.n_runs):
        ability = generate_ability(rng, sc.n, sc.ability_choice)
        global_rank = rank_score(ability)
        pool_id, _signal = assign_pool_ids(
            rng,
            ability,
            sc.n_pools,
            sc.pool_assignment,
            sc.sorting_noise_sd,
        )
        local_rank, pool_mean, poolq_loo, _pool_count = local_rank_and_pool_stats(
            ability,
            pool_id,
            sc.n_pools,
        )

        if sc.score_mode == "ability":
            weights = ability
        elif sc.score_mode == "global_rank":
            weights = global_rank
        elif sc.score_mode == "local_rank":
            weights = local_rank
        elif sc.score_mode == "local_rank_plus_ability":
            w = float(sc.local_rank_weight)
            weights = w * local_rank + (1.0 - w) * ability
        else:
            raise ValueError(f"unknown score mode {sc.score_mode!r}")

        if sc.min_ability_for_promotion > 0:
            weights = np.where(ability >= sc.min_ability_for_promotion, weights, 0.0)

        promoted = choose_winners(rng, weights, sc.k, sc.winner_choice)
        bin_codes = pool_bin_codes(pool_mean, sc.n_pool_bins)

        for b in range(sc.n_pool_bins):
            member_pools = np.flatnonzero(bin_codes == b)
            mask = np.isin(pool_id, member_pools)
            if not np.any(mask):
                continue
            sum_rate[b] += float(np.mean(promoted[mask]))
            sum_x[b] += float(np.nanmean(poolq_loo[mask]))
            sum_n[b] += float(np.sum(mask))
            seen[b] += 1.0

    with np.errstate(invalid="ignore", divide="ignore"):
        y = sum_rate / seen
        x = sum_x / seen

    valid = np.isfinite(y)
    y_valid = y[valid]
    x_valid = x[valid]
    if y_valid.size == 0:
        peak_idx = -1
        peak_y = float("nan")
        first_y = float("nan")
        final_y = float("nan")
        tail_drop_frac = float("nan")
        left_lift_frac = float("nan")
        tail_slope = float("nan")
        interior_peak = False
        moderate_downturn = False
    else:
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
        # Stricter inverted-U shape: peak is neither first nor last bin (>=3 bins),
        # both endpoints strictly below the peak, and each side is at least 5% below peak.
        interior_peak = bool(y_valid.size >= 3 and 1 <= peak_idx <= y_valid.size - 2)
        both_ends_below = bool(first_y < peak_y and final_y < peak_y)
        moderate_downturn = bool(
            interior_peak
            and both_ends_below
            and peak_y > 0
            and left_lift_frac >= 0.05
            and tail_drop_frac >= 0.05
        )

    out = asdict(sc)
    out.update(
        {
            "curve_x": json.dumps([None if not np.isfinite(v) else round(float(v), 8) for v in x]),
            "curve_y": json.dumps([None if not np.isfinite(v) else round(float(v), 8) for v in y]),
            "curve_n": json.dumps([round(float(v), 3) for v in sum_n]),
            "peak_bin": peak_idx,
            "peak_y": peak_y,
            "first_bin_y": first_y if y_valid.size > 0 else float("nan"),
            "final_y": final_y,
            "left_lift_frac": left_lift_frac,
            "tail_drop_frac": tail_drop_frac,
            "tail_slope_last3": tail_slope,
            "interior_peak": interior_peak,
            "moderate_downturn": moderate_downturn,
        }
    )
    return out


def scenario_key(row: dict) -> tuple:
    fields = [
        "ability_choice",
        "pool_assignment",
        "winner_choice",
        "score_mode",
        "local_rank_weight",
        "sorting_noise_sd",
        "min_ability_for_promotion",
        "n",
        "k",
        "n_pools",
        "n_runs",
        "n_pool_bins",
    ]
    return tuple(row[f] for f in fields)


def iter_stage1() -> Iterable[Scenario]:
    # Broad faithful screen. N/RUNS are intentionally smaller here; Stage 2 verifies.
    ability_choices = ["A", "B", "C"]
    pool_assignments = ["A", "B", "C"]
    winner_choices = ["A", "B", "C"]
    score_specs = [("ability", 0.0), ("global_rank", 0.0), ("local_rank", 1.0)] + [
        ("local_rank_plus_ability", w) for w in [0.0, 0.25, 0.5, 0.75, 1.0]
    ]
    sorting_noises = [0.0, 0.01, 0.05, 0.10, 0.25, 0.50]
    min_as = [0.0, 0.25, 0.50]
    ks = [10, 50, 100]
    n_pools_vals = [20, 50, 100]
    seed = 27876507

    for ability, pool, winner, (score, w), noise, min_a, k, n_pools in itertools.product(
        ability_choices,
        pool_assignments,
        winner_choices,
        score_specs,
        sorting_noises,
        min_as,
        ks,
        n_pools_vals,
    ):
        yield Scenario(
            stage="stage1",
            ability_choice=ability,
            pool_assignment=pool,
            winner_choice=winner,
            score_mode=score,
            local_rank_weight=float(w),
            sorting_noise_sd=float(noise),
            min_ability_for_promotion=float(min_a),
            n=500,
            k=int(k),
            n_pools=int(n_pools),
            n_runs=80,
            n_pool_bins=8,
            seed=seed,
        )


def iter_stage2(stage1_rows: list[dict]) -> Iterable[Scenario]:
    # Verify candidates and near-candidates at higher precision across seeds.
    ranked = sorted(
        stage1_rows,
        key=lambda r: (
            not bool(r["interior_peak"]),
            -float(r["tail_drop_frac"]),
            float(r["tail_slope_last3"]),
        ),
    )
    candidates = []
    seen_keys = set()
    for row in ranked:
        if bool(row["interior_peak"]) or float(row["tail_drop_frac"]) > 0.0:
            key = scenario_key(row)
            if key not in seen_keys:
                candidates.append(row)
                seen_keys.add(key)
        if len(candidates) >= 240:
            break

    # Always include exact/manual-relevant local-rank-heavy assortative settings.
    manual_rows = []
    for ability, winner, score, w, noise, min_a, k, n_pools in itertools.product(
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["local_rank", "local_rank_plus_ability"],
        [0.75, 1.0],
        [0.0, 0.01, 0.05, 0.10, 0.25, 0.50],
        [0.0, 0.25, 0.50],
        [10, 50, 100],
        [20, 50, 100],
    ):
        if score == "local_rank" and w != 1.0:
            continue
        manual_rows.append(
            {
                "ability_choice": ability,
                "pool_assignment": "B",
                "winner_choice": winner,
                "score_mode": score,
                "local_rank_weight": float(w),
                "sorting_noise_sd": float(noise),
                "min_ability_for_promotion": float(min_a),
                "k": int(k),
                "n_pools": int(n_pools),
            }
        )

    base_specs = []
    spec_keys = set()
    for row in candidates + manual_rows:
        spec = (
            row["ability_choice"],
            row["pool_assignment"],
            row["winner_choice"],
            row["score_mode"],
            float(row["local_rank_weight"]),
            float(row["sorting_noise_sd"]),
            float(row["min_ability_for_promotion"]),
            int(row["k"]),
            int(row["n_pools"]),
        )
        if spec not in spec_keys:
            base_specs.append(spec)
            spec_keys.add(spec)

    seeds = [27876507, 27876508, 27876509, 27876510, 27876511]
    for spec in base_specs[:650]:
        ability, pool, winner, score, w, noise, min_a, k, n_pools = spec
        for seed in seeds:
            yield Scenario(
                stage="stage2",
                ability_choice=ability,
                pool_assignment=pool,
                winner_choice=winner,
                score_mode=score,
                local_rank_weight=w,
                sorting_noise_sd=noise,
                min_ability_for_promotion=min_a,
                n=1000,
                k=k,
                n_pools=n_pools,
                n_runs=500,
                n_pool_bins=8,
                seed=seed,
            )


def append_jsonl(row: dict) -> None:
    with RESULTS_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
        f.flush()


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def grouped_candidates(stage2_rows: list[dict]) -> pd.DataFrame:
    if not stage2_rows:
        return pd.DataFrame()
    df = pd.DataFrame(stage2_rows)
    group_cols = [
        "ability_choice",
        "pool_assignment",
        "winner_choice",
        "score_mode",
        "local_rank_weight",
        "sorting_noise_sd",
        "min_ability_for_promotion",
        "n",
        "k",
        "n_pools",
        "n_runs",
        "n_pool_bins",
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


def plot_top(stage2_rows: list[dict], grouped: pd.DataFrame, n_plots: int = 12) -> None:
    if plt is None:
        print(
            "faithful_537_sweep: skipping candidate_plots/ — matplotlib is not installed "
            "(install in your conda env, e.g. pip install matplotlib)",
            flush=True,
        )
        return
    if grouped.empty:
        return
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(stage2_rows)
    group_cols = [
        "ability_choice",
        "pool_assignment",
        "winner_choice",
        "score_mode",
        "local_rank_weight",
        "sorting_noise_sd",
        "min_ability_for_promotion",
        "n",
        "k",
        "n_pools",
        "n_runs",
        "n_pool_bins",
    ]
    for idx, grow in grouped.head(n_plots).reset_index(drop=True).iterrows():
        mask = np.ones(len(df), dtype=bool)
        for col in group_cols:
            mask &= df[col].to_numpy() == grow[col]
        sub = df.loc[mask].copy()
        if sub.empty:
            continue
        curves_y = np.array([json.loads(v) for v in sub["curve_y"]], dtype=float)
        curves_x_list = [json.loads(v) for v in sub["curve_x"]]
        curves_x = np.array(
            [
                [np.nan if (v is None or (isinstance(v, float) and np.isnan(v))) else float(v) for v in row]
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
            xlabel = "Pool-quality bin index (0 = lowest-Q bin)"
        else:
            xlabel = "Mean leave-one-out peer A in pool-quality bin"

        fig, ax = plt.subplots(figsize=(8.2, 5.4))
        ax.fill_between(x, y_min, y_max, color="steelblue", alpha=0.20, label="seed range")
        ax.plot(x, y_mean, "o-", color="steelblue", label="mean across seeds")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Promotion probability")
        title = _cell10_catalog.format_faithful_sweep_plot_title(idx + 1, grow.to_dict())
        ax.set_title(title, fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="best", fontsize=8)
        fig.tight_layout()
        fig.savefig(PLOT_DIR / f"candidate_{idx+1:02d}.png", dpi=180)
        plt.close(fig)


def write_readme(stage1_rows: list[dict], stage2_rows: list[dict], grouped: pd.DataFrame) -> None:
    stable_count = int(grouped["moderate_stable"].sum()) if not grouped.empty else 0
    text = f"""# Faithful 537 Simulation Sweep

Generated by `faithful_537_sweep.py`.

## Design

- Faithful to current `537_Sports_Simulation.ipynb` mechanics.
- No new congestion, opportunity, visibility, or recognition penalty terms.
- Stage 1: broad screen at `N=500`, `runs=80`, one seed.
- Stage 2: higher-precision verification at `N=1000`, `runs=500`, five seeds.
- Pool summary: pools sorted by mean `A`, split into 8 equal-count pool bins; x-axis is mean leave-one-out peer `A`.

## Moderate downturn rule

A seed is marked `moderate_downturn=True` when the promotion curve looks like a **strict inverted-U** (not a single descending leg):

- at least three valid pool bins, and the **maximum** is neither the first nor the last bin;
- **both** the first and last bins are **strictly below** the peak (so the peak is not at a boundary);
- `peak_y > 0`, and each side is at least **5% below the peak** in relative terms: `left_lift_frac` (first to peak) and `tail_drop_frac` (peak to last) are both ≥ 0.05.

A grouped setting is marked `moderate_stable=True` when:

- at least three seeds were run and **≥ 60%** have `moderate_downturn`; and
- **mean** `tail_drop_frac` and **mean** `left_lift_frac` are each at least **0.05**.

## Outputs

- `{RESULTS_JSONL.name}`: incremental full result stream.
- `{STAGE1_CSV.name}`: broad screen results.
- `{STAGE2_CSV.name}`: verified results.
- `{GROUPED_CSV.name}`: grouped candidate ranking.
- `candidate_plots/`: plots for the top grouped settings (titles use the same knob phrases as Cell 10 via `cell10_knob_catalog.py`).

## Counts

- Stage 1 rows: {len(stage1_rows):,}
- Stage 2 rows: {len(stage2_rows):,}
- Stable moderate downturn settings: {stable_count:,}
"""
    README.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="remove old outputs first")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    if args.reset:
        for path in [RESULTS_JSONL, STAGE1_CSV, STAGE2_CSV, GROUPED_CSV, README]:
            path.unlink(missing_ok=True)
        for path in PLOT_DIR.glob("candidate_*.png"):
            path.unlink()

    stage1_rows: list[dict] = []
    stage1 = list(iter_stage1())
    print(f"Stage 1 scenarios: {len(stage1):,}", flush=True)
    for idx, sc in enumerate(stage1, start=1):
        row = run_scenario(sc)
        stage1_rows.append(row)
        append_jsonl(row)
        if idx % 250 == 0 or idx == len(stage1):
            best = max((r["tail_drop_frac"] for r in stage1_rows if math.isfinite(float(r["tail_drop_frac"]))), default=float("nan"))
            print(f"Stage 1 {idx:,}/{len(stage1):,}; best tail drop so far={best:.3f}", flush=True)
    write_csv(STAGE1_CSV, stage1_rows)

    stage2_rows: list[dict] = []
    stage2 = list(iter_stage2(stage1_rows))
    print(f"Stage 2 scenarios: {len(stage2):,}", flush=True)
    for idx, sc in enumerate(stage2, start=1):
        row = run_scenario(sc)
        stage2_rows.append(row)
        append_jsonl(row)
        if idx % 25 == 0 or idx == len(stage2):
            grouped = grouped_candidates(stage2_rows)
            stable = int(grouped["moderate_stable"].sum()) if not grouped.empty else 0
            best = float(grouped["mean_tail_drop_frac"].max()) if not grouped.empty else float("nan")
            print(
                f"Stage 2 {idx:,}/{len(stage2):,}; stable={stable:,}; best mean tail drop={best:.3f}",
                flush=True,
            )
    write_csv(STAGE2_CSV, stage2_rows)
    grouped = grouped_candidates(stage2_rows)
    grouped.to_csv(GROUPED_CSV, index=False)
    plot_top(stage2_rows, grouped)
    write_readme(stage1_rows, stage2_rows, grouped)
    print("Done.")
    print(f"Grouped candidates: {GROUPED_CSV}")
    print(f"Plots: {PLOT_DIR}")


if __name__ == "__main__":
    main()
