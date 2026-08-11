#!/usr/bin/env python3
"""NCAA roster-size distribution for the PD17 / Grandchild analysis panel.

Uses the same filtered player-season panel as empirical_lc_distributions and
grandchild_empirical_lc_compare (PPM z, min 20 minutes, 2011–2021).

Run (repo root):
  python sports/scripts/grandchild_ncaa_roster_size_distribution.py

Outputs (HEROs_and_PASSes/grandchild_assign/):
  GRANDCHILD_ncaa_roster_size_distribution_2011_2021.png
  GRANDCHILD_ncaa_vs_lg_roster_size_compare_2011_2021.png  — normalized NCAA vs LG inputs
  GRANDCHILD_ncaa_roster_size_distribution_2011_2021_meta.json
  GRANDCHILD_ncaa_roster_size_by_team_season_2011_2021.csv
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs
from interval_overlap_paths import seasons_label, window_tag

FULL_PANEL_SEASON_MIN = 2011
FULL_PANEL_SEASON_MAX = 2021
LG_ROSTER_SIZE = 15
OUT = GRANDCHILD_ASSIGN
BAR_COLOR = "steelblue"
LG_COLOR = "darkorange"
NCAA_MEAN_COLOR = "crimson"


def _output_paths(season_min: int, season_max: int) -> dict:
    tag = window_tag(season_min, season_max) if season_min != season_max else str(season_min)
    stem = f"GRANDCHILD_ncaa_roster_size_distribution_{tag}"
    return {
        "png": OUT / f"{stem}.png",
        "png_compare": OUT / f"GRANDCHILD_ncaa_vs_lg_roster_size_compare_{tag}.png",
        "meta": OUT / f"{stem}_meta.json",
        "csv": OUT / f"GRANDCHILD_ncaa_roster_size_by_team_season_{tag}.csv",
        "seasons": seasons_label(season_min, season_max),
    }


def _roster_table(panel: pd.DataFrame) -> pd.DataFrame:
    use = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    roster = (
        use.groupby(["team_id", "season"], observed=True)
        .agg(roster_n=("perf", "size"))
        .reset_index()
        .sort_values(["season", "team_id"])
    )
    return roster


def _summary(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=int)
    return {
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": int(v.min()),
        "max": int(v.max()),
        "median": float(np.median(v)),
        "p10": float(np.quantile(v, 0.10)),
        "p25": float(np.quantile(v, 0.25)),
        "p75": float(np.quantile(v, 0.75)),
        "p90": float(np.quantile(v, 0.90)),
        "share_eq_15": float((v == LG_ROSTER_SIZE).mean()),
        "share_ge_15": float((v >= LG_ROSTER_SIZE).mean()),
    }


def _reference_lines(ax, *, ncaa_mean: float) -> None:
    ax.axvline(
        LG_ROSTER_SIZE,
        color=LG_COLOR,
        linestyle="--",
        linewidth=2,
        label=rf"LG fixed $C={LG_ROSTER_SIZE}$",
    )
    ax.axvline(
        ncaa_mean,
        color=NCAA_MEAN_COLOR,
        linestyle=":",
        linewidth=2,
        label=rf"NCAA mean = {ncaa_mean:.1f}",
    )


def _histogram_bins(*arrays: np.ndarray) -> np.ndarray:
    lo = min(int(a.min()) for a in arrays)
    hi = max(int(a.max()) for a in arrays)
    return np.arange(lo - 0.5, hi + 1.5, 1.0)


def _lg_roster_table(season_min: int, season_max: int) -> pd.DataFrame:
    """LG synthetic team-seasons — every roster has fixed capacity C."""
    sys.path.insert(0, str(REPO / "sports"))
    import importlib

    gc = importlib.import_module("541_grandchild_homophily_assign")
    c = int(gc.ROSTER_SIZE_DEFAULT)
    rows: list[dict] = []
    for season in range(int(season_min), int(season_max) + 1):
        ability, emp_meta = gc.load_empirical_abilities_season(int(season), roster_size=c)
        n_teams = int(emp_meta.get("n_teams_grandchild", len(ability) // c))
        rows.extend({"season": season, "team_idx": j, "roster_n": c} for j in range(n_teams))
    return pd.DataFrame(rows)


def _plot(roster: pd.DataFrame, *, paths: dict) -> None:
    sizes = roster["roster_n"].to_numpy(dtype=int)
    stats = _summary(sizes)
    ncaa_mean = stats["mean"]
    bins = _histogram_bins(sizes)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True)

    ax = axes[0]
    ax.hist(sizes, bins=bins, color=BAR_COLOR, alpha=0.85, edgecolor="white", linewidth=0.4)
    _reference_lines(ax, ncaa_mean=ncaa_mean)
    ax.set_xlabel("Players per team-season (≥20 min filter)")
    ax.set_ylabel("Team-season count")
    ax.set_title("NCAA roster sizes — team-season histogram")
    ax.legend(loc="upper right", fontsize=9)

    ax = axes[1]
    ax.hist(
        sizes,
        bins=bins,
        color=BAR_COLOR,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.4,
        weights=np.ones_like(sizes, dtype=float) / sizes.size,
    )
    _reference_lines(ax, ncaa_mean=ncaa_mean)
    ax.set_xlabel("Players per team-season")
    ax.set_ylabel("Share of team-seasons")
    ax.set_title("Same distribution (normalized)")
    ax.legend(loc="upper right", fontsize=9)

    fig.suptitle(
        rf"NCAA roster sizes fed to PD17 / LG analysis ({paths['seasons']}) — "
        rf"$n={stats['n']:,}$ team-seasons, mean={ncaa_mean:.1f}, "
        rf"median={stats['median']:.0f}, sd={stats['std']:.1f}",
        fontsize=11,
        y=1.02,
    )
    fig.savefig(paths["png"], dpi=160, bbox_inches="tight")
    plt.close(fig)


def _plot_ncaa_vs_lg(
    ncaa_roster: pd.DataFrame,
    lg_roster: pd.DataFrame,
    *,
    paths: dict,
) -> None:
    ncaa_sizes = ncaa_roster["roster_n"].to_numpy(dtype=int)
    lg_sizes = lg_roster["roster_n"].to_numpy(dtype=int)
    ncaa_stats = _summary(ncaa_sizes)
    lg_stats = _summary(lg_sizes)
    bins = _histogram_bins(ncaa_sizes, lg_sizes)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5), constrained_layout=True, sharey=True)

    for ax, sizes, color, title, label in (
        (
            axes[0],
            ncaa_sizes,
            BAR_COLOR,
            "NCAA empirical (real team-seasons)",
            "NCAA",
        ),
        (
            axes[1],
            lg_sizes,
            LG_COLOR,
            rf"LG sim (synthetic $C={LG_ROSTER_SIZE}$ leagues)",
            "LG",
        ),
    ):
        ax.hist(
            sizes,
            bins=bins,
            color=color,
            alpha=0.85,
            edgecolor="white",
            linewidth=0.4,
            weights=np.ones_like(sizes, dtype=float) / sizes.size,
        )
        if label == "NCAA":
            _reference_lines(ax, ncaa_mean=ncaa_stats["mean"])
        else:
            ax.axvline(
                LG_ROSTER_SIZE,
                color=LG_COLOR,
                linestyle="--",
                linewidth=2,
                label=rf"LG fixed $C={LG_ROSTER_SIZE}$",
            )
            ax.axvline(
                ncaa_stats["mean"],
                color=NCAA_MEAN_COLOR,
                linestyle=":",
                linewidth=2,
                label=rf"NCAA mean = {ncaa_stats['mean']:.1f}",
            )
        ax.set_xlabel("Players per team-season")
        ax.set_title(title)
        ax.legend(loc="upper right", fontsize=9)

    axes[0].set_ylabel("Share of team-seasons (normalized)")

    fig.suptitle(
        rf"Roster sizes fed into NCAA vs LG pipelines ({paths['seasons']}) — "
        rf"NCAA: $n={ncaa_stats['n']:,}$, mean={ncaa_stats['mean']:.1f}  |  "
        rf"LG: $n={lg_stats['n']:,}$, all rosters $C={LG_ROSTER_SIZE}$",
        fontsize=11,
        y=1.02,
    )
    fig.savefig(paths["png_compare"], dpi=160, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--season-min", type=int, default=FULL_PANEL_SEASON_MIN)
    parser.add_argument("--season-max", type=int, default=FULL_PANEL_SEASON_MAX)
    args = parser.parse_args()

    ensure_hero_dirs()
    paths = _output_paths(args.season_min, args.season_max)

    import empirical_lc_distributions as elc

    panel = elc._prepare_panel()
    panel = panel.loc[
        (panel["season"] >= args.season_min) & (panel["season"] <= args.season_max)
    ].copy()

    roster = _roster_table(panel)
    sizes = roster["roster_n"].to_numpy(dtype=int)
    lg_roster = _lg_roster_table(args.season_min, args.season_max)

    _plot(roster, paths=paths)
    _plot_ncaa_vs_lg(roster, lg_roster, paths=paths)
    roster.to_csv(paths["csv"], index=False)

    per_season = (
        roster.groupby("season", observed=True)
        .agg(
            n_teams=("team_id", "nunique"),
            mean_roster_n=("roster_n", "mean"),
            median_roster_n=("roster_n", "median"),
            min_roster_n=("roster_n", "min"),
            max_roster_n=("roster_n", "max"),
            n_players=("roster_n", "sum"),
        )
        .reset_index()
    )
    per_season["n_teams_lg_if_c15"] = (per_season["n_players"] // LG_ROSTER_SIZE).astype(int)
    per_season["n_players_trimmed_for_lg"] = (
        per_season["n_players"] - per_season["n_teams_lg_if_c15"] * LG_ROSTER_SIZE
    )

    meta = {
        "generated": date.today().isoformat(),
        "panel": "empirical_lc_distributions._prepare_panel (PPM z, min 20 min)",
        "season_min": args.season_min,
        "season_max": args.season_max,
        "seasons_label": paths["seasons"],
        "lg_roster_size_reference": LG_ROSTER_SIZE,
        "team_season_summary": _summary(sizes),
        "lg_team_season_summary": _summary(lg_roster["roster_n"].to_numpy(dtype=int)),
        "player_seasons": int(sizes.sum()),
        "per_season": per_season.to_dict(orient="records"),
        "outputs": {k: str(v) for k, v in paths.items() if k != "seasons"},
    }
    paths["meta"].write_text(json.dumps(meta, indent=2), encoding="utf-8")

    s = meta["team_season_summary"]
    lg_s = meta["lg_team_season_summary"]
    print(f"Wrote {paths['png']}")
    print(f"Wrote {paths['png_compare']}")
    print(
        f"NCAA team-seasons={s['n']:,}  mean={s['mean']:.2f}  median={s['median']:.0f}  "
        f"sd={s['std']:.2f}  share(C=15)={s['share_eq_15']:.1%}"
    )
    print(f"LG team-seasons={lg_s['n']:,}  (all roster_n={LG_ROSTER_SIZE})")


if __name__ == "__main__":
    main()
