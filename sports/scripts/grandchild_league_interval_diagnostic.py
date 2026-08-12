#!/usr/bin/env python3
"""Grandchild sim league — team interval overlap (PD17 compare window).

Single season (legacy):
  python sports/scripts/grandchild_league_interval_diagnostic.py --season 2015

Multi-season apples-to-apples window (one ASSIGN run per season, stacked team-seasons):
  python sports/scripts/grandchild_league_interval_diagnostic.py --season-min 2015 --season-max 2019
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs
from interval_overlap_paths import empirical_overlap_paths, grandchild_overlap_paths, window_tag

N_INTERVAL_SAMPLE = 80
COVERAGE_GRID_POINTS = 400
SPAN_BINS = 40
BAR_COLOR = "darkorange"
DEFAULT_RHO = 0.5
DEFAULT_SEED = 5412015


def _summary(name: str, values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    return {
        "label": name,
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": float(v.min()),
        "max": float(v.max()),
        "median": float(np.median(v)),
    }


def _team_intervals(
    ability: np.ndarray,
    pool_id: np.ndarray,
    *,
    season: int | None = None,
    team_season_offset: int = 0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = pd.DataFrame({"perf": ability, "pool_id": pool_id.astype(np.int64)})
    if season is not None:
        work["season"] = int(season)
    iv = (
        work.groupby("pool_id", observed=True)["perf"]
        .agg(
            A_hat_min="min",
            A_hat_max="max",
            T_j_hat="mean",
            roster_n="count",
        )
        .reset_index()
        .rename(columns={"pool_id": "team_id"})
    )
    iv["perf_span"] = iv["A_hat_max"] - iv["A_hat_min"]
    if season is not None:
        iv["season"] = int(season)
    iv["team_season_id"] = np.arange(team_season_offset, team_season_offset + len(iv))
    pool_to_ts = dict(zip(iv["team_id"], iv["team_season_id"]))
    work["team_season_id"] = work["pool_id"].map(pool_to_ts).astype(np.int64)
    return iv, work


def _coverage_curve(lo: np.ndarray, hi: np.ndarray, grid: np.ndarray) -> np.ndarray:
    cover = np.zeros(grid.size, dtype=int)
    for a, b in zip(lo, hi):
        cover += (grid >= a) & (grid <= b)
    return cover


def _disjoint_benchmark(work: pd.DataFrame, n_slices: int, grid: np.ndarray) -> np.ndarray:
    perf_sorted = np.sort(work["perf"].to_numpy(dtype=float))
    cuts = np.array_split(perf_sorted, n_slices)
    disjoint_lo = np.array([c.min() for c in cuts if len(c)])
    disjoint_hi = np.array([c.max() for c in cuts if len(c)])
    return _coverage_curve(disjoint_lo, disjoint_hi, grid)


def _coverage_stats(cover: np.ndarray, n_units: int) -> dict:
    cov_max = int(cover.max())
    return {
        "coverage_max": cov_max,
        "coverage_max_normalized": float(cov_max / n_units) if n_units else None,
        "coverage_mean": float(cover.mean()),
        "coverage_frac_gt_1": float((cover > 1).mean()),
    }


def build_figure(
    iv: pd.DataFrame,
    work: pd.DataFrame,
    *,
    png_path: Path,
    seasons: str,
    rho: float,
    h_sort: float,
    multi_season: bool,
    roster_label: str = r"$C=15$",
    global_wss: float | None = None,
) -> dict:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()

    grid = np.linspace(iv["A_hat_min"].min(), iv["A_hat_max"].max(), COVERAGE_GRID_POINTS)
    lo = iv["A_hat_min"].to_numpy(dtype=float)
    hi = iv["A_hat_max"].to_numpy(dtype=float)
    cover = _coverage_curve(lo, hi, grid)
    cover_disjoint = _disjoint_benchmark(work, len(iv), grid)
    n_units = len(iv)
    cov_stats = _coverage_stats(cover, n_units)
    unit_label = "team-seasons" if multi_season else "teams"

    iv_plot = iv.sort_values("T_j_hat").reset_index(drop=True)
    step = max(1, len(iv_plot) // N_INTERVAL_SAMPLE)
    sample = iv_plot.iloc[::step].head(N_INTERVAL_SAMPLE).copy()

    xlab = r"Player $\hat{A}_i$ (PPM $z$ within season)"
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    ax.fill_between(
        grid,
        cover,
        step="mid",
        alpha=0.35,
        color=BAR_COLOR,
        label=rf"LG rosters ($\rho={rho:g}$)",
    )
    ax.plot(
        grid,
        cover_disjoint,
        color="crimson",
        lw=1.5,
        ls="--",
        label="Disjoint sort-and-chop (equal-$n$ slices)",
    )
    ax.axhline(1, color="gray", ls=":", lw=1, label="No overlap (coverage = 1)")
    ax.set_xlabel(xlab, fontsize=10)
    ax.set_ylabel(f"{unit_label.capitalize()} covering this level", fontsize=10)
    ax.set_title("Interval overlap along talent spectrum", fontsize=11, pad=8)
    ax.text(
        0.02,
        0.98,
        rf"max coverage = {cov_stats['coverage_max']:,}  |  "
        rf"{cov_stats['coverage_frac_gt_1']:.1%} of grid with $>$1 team",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    ax.legend(fontsize=7, loc="lower right")

    ax = axes[0, 1]
    ax.hist(iv["perf_span"], bins=SPAN_BINS, color=BAR_COLOR, edgecolor="white", alpha=0.85)
    ax.set_xlabel(r"Roster span ($\max \hat{A}_i - \min \hat{A}_i$)", fontsize=10)
    ax.set_ylabel(unit_label.capitalize(), fontsize=10)
    ax.set_title("Width of each team's talent window", fontsize=11, pad=8)
    span_stats = _summary("perf_span", iv["perf_span"].to_numpy(dtype=float))
    ax.text(
        0.98,
        0.98,
        rf"mean={span_stats['mean']:.2f}, median={span_stats['median']:.2f}",
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )

    ax = axes[1, 0]
    y0 = np.arange(len(sample))
    ax.hlines(y0, sample["A_hat_min"], sample["A_hat_max"], colors=BAR_COLOR, lw=2, alpha=0.85)
    ax.scatter(sample["T_j_hat"], y0, color="crimson", s=28, zorder=3, label=r"$\hat{T}_j$")
    ax.set_yticks(y0[:: max(1, len(y0) // 8)])
    ax.set_xlabel(xlab, fontsize=10)
    ax.set_ylabel(f"Sample of {len(sample)} {unit_label} (sorted by $\\hat{{T}}_j$)", fontsize=9)
    ax.set_title(r"Roster $[\min, \max]$ intervals (sample)", fontsize=11, pad=8)
    ax.legend(fontsize=8, loc="lower right")

    ax = axes[1, 1]
    y_all = np.arange(len(iv_plot))
    ax.hlines(
        y_all,
        iv_plot["A_hat_min"],
        iv_plot["A_hat_max"],
        colors=BAR_COLOR,
        alpha=0.15,
        linewidth=0.6,
    )
    ax.set_xlabel(xlab, fontsize=10)
    ax.set_ylabel(f"All {unit_label} (sorted by $\\hat{{T}}_j$)", fontsize=9)
    ax.set_title(
        f"All {len(iv_plot):,} intervals (faint) — overlap = vertical stacking",
        fontsize=11,
        pad=8,
    )

    fig.suptitle(
        rf"LG ASSIGN — team talent window overlap (MBB {seasons}, $\rho={rho:g}$, {roster_label})"
        + rf"\nRealized sorting $H_{{sort}}={h_sort:.3f}$"
        + (rf", global\_wss={global_wss:,.0f}" if global_wss is not None else "")
        + " on this partition",
        fontsize=12,
        y=0.98,
    )
    fig.subplots_adjust(left=0.08, right=0.96, top=0.90, bottom=0.08, hspace=0.38, wspace=0.28)
    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png_path}")

    return {
        **cov_stats,
        "coverage_disjoint_max": int(cover_disjoint.max()),
        "coverage_disjoint_mean": float(cover_disjoint.mean()),
        "n_team_seasons": int(len(iv)) if multi_season else None,
        "n_teams": int(len(iv)) if not multi_season else None,
        "n_players": int(len(work)),
        "H_sort": float(h_sort),
        "global_wss": float(global_wss) if global_wss is not None else None,
        "perf_span": span_stats,
        "T_j_hat": _summary(r"\hat{T}_j", iv["T_j_hat"].to_numpy(dtype=float)),
    }


def _run_one_season_empirical_caps(
    gc,
    *,
    season: int,
    rho: float,
    seed: int,
    team_season_offset: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    ability, caps, emp_meta = gc.load_empirical_roster_caps_season(int(season))
    rng = np.random.default_rng(int(seed) + int(season))
    res = gc.run_one_realization(
        ability, None, float(rho), roster_caps=caps, rng=rng
    )
    iv, work = _team_intervals(
        res.ability,
        res.pool_id,
        season=season,
        team_season_offset=team_season_offset,
    )
    season_info = {
        "season": int(season),
        "n_players": int(len(ability)),
        "n_teams": int(len(iv)),
        "H_sort": float(res.sorting_index_h),
        "global_wss": float(res.global_wss),
        "centroid_sd": float(res.centroid_sd),
        "roster_mode": "empirical_caps",
        "ability_source": emp_meta,
    }
    return iv, work, season_info


def _run_one_season(
    gc,
    *,
    season: int,
    rho: float,
    seed: int,
    c: int,
    team_season_offset: int,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    ability, emp_meta = gc.load_empirical_abilities_season(int(season), roster_size=c)
    if len(ability) % c != 0:
        raise ValueError(
            f"Season {season}: N={len(ability)} not divisible by C={c} after trim"
        )
    rng = np.random.default_rng(int(seed) + int(season))
    res = gc.run_one_realization(ability, c, float(rho), rng=rng, seed=int(seed) + int(season))
    iv, work = _team_intervals(
        res.ability,
        res.pool_id,
        season=season,
        team_season_offset=team_season_offset,
    )
    season_info = {
        "season": int(season),
        "n_players": int(len(ability)),
        "n_teams": int(len(iv)),
        "H_sort": float(res.sorting_index_h),
        "centroid_sd": float(res.centroid_sd),
        "ability_source": emp_meta,
    }
    return iv, work, season_info


def _compute_h_sort(work: pd.DataFrame, gc) -> float:
    return float(
        gc.realized_sorting_index_H_sort(
            work["perf"].to_numpy(dtype=float),
            work["team_season_id"].to_numpy(dtype=np.int64),
        )
    )


def _load_ncaa_window_ref(season_min: int, season_max: int) -> dict:
    ref_path = empirical_overlap_paths(season_min=season_min, season_max=season_max)["meta"]
    if ref_path.is_file():
        return json.loads(ref_path.read_text(encoding="utf-8"))
    return {}


def run_diagnostic(
    *,
    season_min: int,
    season_max: int,
    rho: float = DEFAULT_RHO,
    seed: int = DEFAULT_SEED,
    legacy_single: bool = False,
    empirical_roster_caps: bool = False,
) -> dict:
    paths = grandchild_overlap_paths(
        season_min=season_min,
        season_max=season_max,
        single_season_legacy=legacy_single and season_min == season_max,
    )
    if empirical_roster_caps:
        tag = window_tag(season_min, season_max) if season_max > season_min else str(season_min)
        paths = {
            **paths,
            "png": GRANDCHILD_ASSIGN / f"GRANDCHILD_league_interval_empirical_caps_{tag}.png",
            "csv": GRANDCHILD_ASSIGN / f"GRANDCHILD_league_interval_empirical_caps_{tag}_team_season.csv",
            "meta": GRANDCHILD_ASSIGN / f"GRANDCHILD_league_interval_empirical_caps_{tag}_meta.json",
        }
    multi_season = season_max > season_min or (not legacy_single and season_min != season_max)

    gc = importlib.import_module("541_grandchild_homophily_assign")
    c = int(gc.ROSTER_SIZE_DEFAULT)

    seasons = list(range(int(season_min), int(season_max) + 1))
    iv_parts: list[pd.DataFrame] = []
    work_parts: list[pd.DataFrame] = []
    season_runs: list[dict] = []
    offset = 0

    from diagnostic_progress import SeasonProgress

    mode = "empirical caps" if empirical_roster_caps else f"C={c}"
    prog = SeasonProgress(f"Interval overlap ({mode})", season_min, season_max)
    prog.header()

    for season in seasons:
        if empirical_roster_caps:
            iv, work, info = _run_one_season_empirical_caps(
                gc,
                season=season,
                rho=rho,
                seed=seed,
                team_season_offset=offset,
            )
        else:
            iv, work, info = _run_one_season(
                gc,
                season=season,
                rho=rho,
                seed=seed,
                c=c,
                team_season_offset=offset,
            )
        iv_parts.append(iv)
        work_parts.append(work)
        season_runs.append(info)
        offset += len(iv)
        prog.tick(
            season,
            f"J={len(iv)} N={info['n_players']} H_sort={info['H_sort']:.3f}",
        )

    prog.finish()
    print("Building figure ...", flush=True)
    iv_all = pd.concat(iv_parts, ignore_index=True)
    work_all = pd.concat(work_parts, ignore_index=True)
    h_sort = _compute_h_sort(work_all, gc) if multi_season else float(season_runs[0]["H_sort"])
    global_wss = float(
        gc.global_wss(
            work_all["perf"].to_numpy(dtype=float),
            work_all["team_season_id"].to_numpy(dtype=np.int64),
        )
    )
    roster_label = r"empirical caps" if empirical_roster_caps else r"$C=15$"

    paths["csv"].parent.mkdir(parents=True, exist_ok=True)
    iv_all.to_csv(paths["csv"], index=False)
    print(f"Wrote {paths['csv']}")

    stats = build_figure(
        iv_all,
        work_all,
        png_path=paths["png"],
        seasons=paths["seasons"],
        rho=float(rho),
        h_sort=float(h_sort),
        multi_season=multi_season or len(seasons) > 1,
        roster_label=roster_label,
        global_wss=global_wss,
    )

    ncaa_ref = _load_ncaa_window_ref(season_min, season_max) if len(seasons) > 1 or not legacy_single else {}

    assign_block = {
        "method": "grandchild",
        "rho": float(rho),
        "seed": int(seed),
        "roster_size": None if empirical_roster_caps else c,
        "roster_mode": "empirical_caps" if empirical_roster_caps else "fixed_c15",
        "n_team_seasons": int(len(iv_all)) if multi_season or len(seasons) > 1 else None,
        "n_teams": int(len(iv_all)) if len(seasons) == 1 else None,
        "n_players": int(len(work_all)),
        "sorting_index_h": float(h_sort),
        "H_sort": float(h_sort),
        "global_wss": global_wss,
        "seasons": paths["seasons"],
        "season_min": int(season_min),
        "season_max": int(season_max),
        "season_runs": season_runs,
    }
    if len(seasons) == 1:
        assign_block["centroid_sd"] = float(season_runs[0]["centroid_sd"])
        assign_block["n_teams"] = int(len(iv_all))

    meta = {
        "diagnostic": "grandchild_league_interval_overlap",
        "date": date.today().isoformat(),
        "assignment": assign_block,
        "ability_source": season_runs[0]["ability_source"] if len(seasons) == 1 else {"seasons": seasons},
        "ncaa_window_reference": ncaa_ref,
        "coverage_grid_points": COVERAGE_GRID_POINTS,
        "n_interval_sample": N_INTERVAL_SAMPLE,
        "compare_window": len(seasons) > 1 or not legacy_single,
        **stats,
        "outputs": {
            "png": paths["png"].name,
            "team_csv": paths["csv"].name,
        },
    }
    paths["meta"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {paths['meta']}")
    print(
        f"seasons={paths['seasons']}  rho={rho:g}  units={len(iv_all):,}  "
        f"max coverage={stats['coverage_max']:,}  "
        f"norm={stats.get('coverage_max_normalized', 0):.3f}  "
        f"H_sort={h_sort:.3f}"
    )
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Grandchild sim league interval overlap")
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--season", type=int, default=None, help="Legacy single-season run (2015 default)")
    parser.add_argument("--season-min", type=int, default=None)
    parser.add_argument("--season-max", type=int, default=None)
    parser.add_argument(
        "--empirical-roster-caps",
        action="store_true",
        help="Use exact NCAA filtered roster-size multiset per season (Alex Aug 2026)",
    )
    args = parser.parse_args()

    if args.season_min is not None or args.season_max is not None:
        if args.season_min is None or args.season_max is None:
            parser.error("--season-min and --season-max must be supplied together")
        season_min, season_max = int(args.season_min), int(args.season_max)
        legacy_single = False
    else:
        season_min = season_max = int(args.season if args.season is not None else 2015)
        legacy_single = args.season is None

    ensure_hero_dirs()
    run_diagnostic(
        season_min=season_min,
        season_max=season_max,
        rho=float(args.rho),
        seed=int(args.seed),
        legacy_single=legacy_single,
        empirical_roster_caps=bool(args.empirical_roster_caps),
    )
    print("Done.")


if __name__ == "__main__":
    main()
