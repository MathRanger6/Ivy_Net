#!/usr/bin/env python3
"""Grandchild LG — empirical roster-size multiset (Alex Aug 2026).

Instead of fixed C=15 (or C sweep), each synthetic team gets a stub capacity
drawn from the **exact** NCAA filtered roster-size multiset for that season:
one capacity per real team-season, summing to N players. Same homophily ASSIGN;
then L_C and SELECT readouts vs empirical NCAA.

Run (repo root):
  python sports/scripts/grandchild_empirical_roster_caps_diagnostic.py
  python sports/scripts/grandchild_empirical_roster_caps_diagnostic.py --rho 0.5

Outputs (HEROs_and_PASSes/grandchild_assign/):
  GRANDCHILD_empirical_roster_caps_lc_2011_2021.png
  GRANDCHILD_empirical_roster_caps_selection_2011_2021.png
  GRANDCHILD_empirical_roster_caps_roster_compare_2011_2021.png
  GRANDCHILD_empirical_roster_caps_2011_2021_meta.json
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from dataclasses import replace
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

from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs
from interval_overlap_paths import seasons_label

import grandchild_empirical_lc_compare as glc
import grandchild_selection_inverted_u_diagnostic as gsel

OUT = GRANDCHILD_ASSIGN
SEASON_MIN = glc.FULL_PANEL_SEASON_MIN
SEASON_MAX = glc.FULL_PANEL_SEASON_MAX
DEFAULT_RHO = glc.DEFAULT_RHO
DEFAULT_SEED = glc.DEFAULT_SEED
DEFAULT_GAMMA = glc.DEFAULT_GAMMA
N_LC_BINS = glc.N_LC_BINS
EMP_COLOR = glc.EMP_COLOR
SIM_COLOR = glc.SIM_COLOR
POOL_ID_SEASON_OFFSET = gsel.POOL_ID_SEASON_OFFSET


def _lc_density(lc: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    edges = np.linspace(0.0, 1.0, N_LC_BINS + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    density, _ = np.histogram(lc, bins=edges, density=True)
    return centers, density


def _empirical_roster_sizes(panel: pd.DataFrame) -> np.ndarray:
    use = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    roster = (
        use.groupby(["team_id", "season"], observed=True)
        .agg(roster_n=("perf", "size"))
        .reset_index()
    )
    return roster["roster_n"].to_numpy(dtype=int)


def _sim_roster_sizes(sim_team: pd.DataFrame) -> np.ndarray:
    return sim_team["roster_n"].to_numpy(dtype=int)


def _sim_team_lc_panel_empirical_caps(
    *,
    season_min: int,
    season_max: int,
    rho: float,
    seed: int,
    theta: float,
    gamma: float,
    gc,
) -> tuple[pd.DataFrame, list[dict]]:
    seasons = list(range(int(season_min), int(season_max) + 1))
    parts: list[pd.DataFrame] = []
    season_runs: list[dict] = []
    from diagnostic_progress import SeasonProgress

    prog = SeasonProgress("L_C empirical caps", season_min, season_max)
    prog.header()
    for season in seasons:
        ability, caps, emp_meta = gc.load_empirical_roster_caps_season(int(season))
        rng = np.random.default_rng(int(seed) + int(season))
        res = gc.run_one_realization(
            ability, None, float(rho), roster_caps=caps, rng=rng
        )
        team_df = glc._teams_from_grandchild(
            res.ability,
            res.pool_id,
            season=season,
            theta=theta,
            gamma=gamma,
        )
        parts.append(team_df)
        season_runs.append(
            {
                "season": int(season),
                "n_teams": int(len(team_df)),
                "n_players": int(len(ability)),
                "H_sort": float(res.sorting_index_h),
                "within_team_mse": float(res.within_team_mse),
                "roster_caps_mean": float(caps.mean()),
                **{k: emp_meta.get(k) for k in ("n_teams_empirical", "roster_mode")},
            }
        )
        prog.tick(
            season,
            f"J={len(team_df)} mean cap={caps.mean():.1f} H_sort={res.sorting_index_h:.3f}",
        )
    prog.finish()
    return pd.concat(parts, ignore_index=True), season_runs


def _run_one_season_select(
    *,
    season: int,
    rho: float,
    seed: int,
    gc,
    cfg,
    sel_template,
    hero_work: pd.DataFrame,
    tpa,
) -> tuple[pd.DataFrame, dict]:
    ability, caps, emp_meta = gc.load_empirical_roster_caps_season(int(season))
    k, theta, season_meta = gsel._season_k_theta(hero_work, season)
    sel = replace(sel_template, n_selected=int(k))
    rng = np.random.default_rng(int(seed) + int(season))
    pool_id, mu_final = gc.grandchild_assign(
        rng, ability, roster_caps=caps, rho=float(rho)
    )
    players = tpa.build_roster_dataframe(ability, pool_id, mu_final)
    players = tpa.assign_selection(
        players,
        rng,
        n_selected=sel.n_selected,
        score_mode=sel.score_mode,
        loo_gap_weight=sel.loo_gap_weight,
        winner_selection=sel.winner_selection,
        pool_l_mode=sel.loo_pool_l_mode,
        viability_theta=float(theta),
        viability_sharpness=float(getattr(cfg, "SELECTION_539_VIABILITY_SHARPNESS", 10.0)),
    )
    players["season"] = int(season)
    players["pool_id"] = players["pool_id"].astype(np.int64) + int(season) * POOL_ID_SEASON_OFFSET
    season_meta = {
        **season_meta,
        **emp_meta,
        "n_players_sim": int(len(players)),
        "n_teams_sim": int(players["pool_id"].nunique()),
    }
    return players, season_meta


def _run_panel_select(
    *,
    season_min: int,
    season_max: int,
    rho: float,
    seed: int,
    gc,
    cfg,
    sel_template,
    hero_work: pd.DataFrame,
    tge,
    tpa,
    assign_poolq_bin_labels,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict]]:
    seasons = list(range(int(season_min), int(season_max) + 1))
    parts: list[pd.DataFrame] = []
    season_runs: list[dict] = []
    from diagnostic_progress import SeasonProgress

    prog = SeasonProgress("SELECT empirical caps", season_min, season_max)
    prog.header()
    for season in seasons:
        players, info = _run_one_season_select(
            season=season,
            rho=float(rho),
            seed=int(seed),
            gc=gc,
            cfg=cfg,
            sel_template=sel_template,
            hero_work=hero_work,
            tpa=tpa,
        )
        parts.append(players)
        season_runs.append(info)
        prog.tick(
            season,
            f"N={info['n_players_sim']:,} K={info['K']} selected={int(players['Y_selected'].sum())}",
        )
    prog.finish()
    pooled = pd.concat(parts, ignore_index=True)
    summ_loo = tge.inverted_u_bin_table(
        pooled, sel_template, assign_poolq_bin_labels=assign_poolq_bin_labels, tpa=tpa
    )
    summ_mean = tge.inverted_u_bin_table_team_mean(
        pooled, sel_template, assign_poolq_bin_labels=assign_poolq_bin_labels
    )
    return pooled, summ_loo, summ_mean, season_runs


def _plot_lc_compare(
    emp_lc: np.ndarray,
    sim_lc: np.ndarray,
    *,
    seasons: str,
    rho: float,
    gamma: float,
    out_path: Path,
) -> None:
    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.5), sharey=True)
    panels = [
        (emp_lc, EMP_COLOR, "NCAA empirical"),
        (sim_lc, SIM_COLOR, r"LG empirical caps"),
    ]
    ymax = 0.0
    for ax, (lc, color, label) in zip(axes, panels, strict=True):
        xs, ys = _lc_density(lc)
        ymax = max(ymax, float(ys.max()) if len(ys) else ymax)
        stats = glc._summary("L_C", lc)
        ax.bar(xs, ys, width=1.0 / N_LC_BINS * 0.95, color=color, alpha=0.75, label=label)
        ax.set_xlim(0, 1)
        ax.set_xticks(glc.LC_TICKS)
        ax.set_xlabel(r"$L_C$")
        ax.set_title(
            rf"{label} ($n={stats['n']:,}$, mean={stats['mean']:.3f}, sd={stats['std']:.3f})",
            fontsize=9,
        )
        ax.legend(fontsize=8, loc="upper right")
        ax.grid(axis="y", alpha=0.25)
    axes[0].set_ylabel("Density")
    fig.suptitle(
        rf"Team $L_C$ — LG with empirical roster caps vs NCAA (MBB {seasons}, "
        rf"$\rho={rho:g}$, $\gamma={gamma:g}$)",
        fontsize=11,
        y=0.98,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.90))
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _plot_selection(
    emp_loo: pd.DataFrame,
    emp_mean: pd.DataFrame,
    summ_loo: pd.DataFrame,
    summ_mean: pd.DataFrame,
    *,
    seasons: str,
    rho: float,
    out_path: Path,
) -> None:
    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8))
    curv = gsel._curvature_label(summ_loo)
    panels = [
        (summ_loo, emp_loo, r"LOO pool quality (poolq_loo)", "mean_loo_q"),
        (summ_mean, emp_mean, r"Pool mean (team_mean)", "mean_team_mean"),
    ]
    for ax, (summ, emp, xlab, xcol) in zip(axes, panels, strict=True):
        if len(emp):
            ax.plot(
                emp[xcol],
                emp["selection_rate"],
                "s--",
                color=EMP_COLOR,
                lw=2.0,
                ms=5,
                alpha=0.9,
                label="Empirical NCAA",
                zorder=1,
            )
        ax.plot(
            summ[xcol],
            summ["selection_rate"],
            "o-",
            color=SIM_COLOR,
            lw=2.0,
            ms=5,
            label=rf"LG empirical caps ({curv['shape'].replace('_', ' ')})",
            zorder=2,
        )
        ax.set_xlabel(xlab, fontsize=10)
        ax.set_ylabel("Selection / draft rate", fontsize=10)
        ax.legend(fontsize=8, loc="upper left")
        ax.grid(alpha=0.25)
        ymax = 0.01
        if len(emp):
            ymax = max(ymax, float(emp["selection_rate"].max()))
        ymax = max(ymax, float(summ["selection_rate"].max()))
        ax.set_ylim(0, min(1.0, ymax * 1.15))
    fig.suptitle(
        rf"LG SELECT — empirical roster caps vs NCAA (MBB {seasons}, $\rho={rho:g}$)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _plot_roster_compare(
    emp_sizes: np.ndarray,
    sim_sizes: np.ndarray,
    *,
    seasons: str,
    out_path: Path,
) -> None:
    configure_matplotlib_mathtext()
    lo = min(int(emp_sizes.min()), int(sim_sizes.min()))
    hi = max(int(emp_sizes.max()), int(sim_sizes.max()))
    bins = np.arange(lo - 0.5, hi + 1.5, 1.0)
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.hist(
        emp_sizes,
        bins=bins,
        density=True,
        alpha=0.55,
        color=EMP_COLOR,
        label=f"NCAA empirical (n={emp_sizes.size:,})",
    )
    ax.hist(
        sim_sizes,
        bins=bins,
        density=True,
        histtype="step",
        lw=2.2,
        color=SIM_COLOR,
        label=f"LG empirical caps (n={sim_sizes.size:,})",
    )
    ax.axvline(float(emp_sizes.mean()), color=EMP_COLOR, ls=":", lw=1.8, alpha=0.8)
    ax.axvline(float(sim_sizes.mean()), color=SIM_COLOR, ls=":", lw=1.8, alpha=0.8)
    ax.set_xlabel("Qualifying players per team-season")
    ax.set_ylabel("Density")
    ax.set_title(rf"Roster-size input — exact NCAA multiset per season (MBB {seasons})")
    ax.legend(fontsize=9)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO)
    parser.add_argument("--gamma", type=float, default=DEFAULT_GAMMA)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    ensure_hero_dirs()
    seasons = seasons_label(SEASON_MIN, SEASON_MAX)
    tag = f"{SEASON_MIN}_{SEASON_MAX}"
    out_lc = OUT / f"GRANDCHILD_empirical_roster_caps_lc_{tag}.png"
    out_sel = OUT / f"GRANDCHILD_empirical_roster_caps_selection_{tag}.png"
    out_roster = OUT / f"GRANDCHILD_empirical_roster_caps_roster_compare_{tag}.png"
    out_meta = OUT / f"GRANDCHILD_empirical_roster_caps_{tag}_meta.json"

    gc = importlib.import_module("541_grandchild_homophily_assign")
    cfg = gsel._load_cfg()
    tge, tpa, assign_poolq_bin_labels = gsel._load_modules()

    print(f"Loading empirical panel {seasons} ...")
    panel = glc._hero_panel(SEASON_MIN, SEASON_MAX)
    panel = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    ability = panel["perf"].to_numpy(dtype=float)
    n_drafted = int(panel["Y_draft"].sum())
    n_total = int(len(panel))
    k_over_n = n_drafted / n_total if n_total else float("nan")
    theta = float(np.quantile(ability, 1.0 - k_over_n))
    gamma = float(args.gamma)

    emp_team = glc._empirical_team_lc(panel, theta=theta, gamma=gamma)
    emp_lc = emp_team["L_C"].dropna().to_numpy(dtype=float)
    emp_roster_sizes = _empirical_roster_sizes(panel)
    print(f"Empirical: {emp_lc.size:,} team-seasons  L_C mean={emp_lc.mean():.3f}")

    print("\n=== L_C panel (empirical roster caps) ===")
    sim_team, season_runs_lc = _sim_team_lc_panel_empirical_caps(
        season_min=SEASON_MIN,
        season_max=SEASON_MAX,
        rho=float(args.rho),
        seed=int(args.seed),
        theta=theta,
        gamma=gamma,
        gc=gc,
    )
    sim_lc = sim_team["L_C"].dropna().to_numpy(dtype=float)
    sim_roster_sizes = _sim_roster_sizes(sim_team)
    lc_stats = glc._summary("L_C", sim_lc)
    print(f"  L_C: n={lc_stats['n']:,} mean={lc_stats['mean']:.3f} sd={lc_stats['std']:.3f}")

    hero_work = gsel._prepare_hero_panel(SEASON_MIN, SEASON_MAX)
    emp_loo, emp_mean = gsel._empirical_reference_tables(hero_work, assign_poolq_bin_labels)
    k_ref, _, _ = gsel._season_k_theta(hero_work, SEASON_MIN)
    sel_template = gsel._selection_config(tge, cfg, n_selected=max(1, k_ref))

    print("\n=== SELECT panel (empirical roster caps) ===")
    pooled, summ_loo, summ_mean, season_runs_sel = _run_panel_select(
        season_min=SEASON_MIN,
        season_max=SEASON_MAX,
        rho=float(args.rho),
        seed=int(args.seed),
        gc=gc,
        cfg=cfg,
        sel_template=sel_template,
        hero_work=hero_work,
        tge=tge,
        tpa=tpa,
        assign_poolq_bin_labels=assign_poolq_bin_labels,
    )
    curv_loo = gsel._curvature_label(summ_loo)
    curv_mean = gsel._curvature_label(summ_mean)
    print(f"  SELECT LOO: {curv_loo['shape']}  pool mean: {curv_mean['shape']}")

    print("\nWriting figures ...", flush=True)
    _plot_lc_compare(
        emp_lc,
        sim_lc,
        seasons=seasons,
        rho=float(args.rho),
        gamma=gamma,
        out_path=out_lc,
    )
    print(f"Wrote {out_lc}")

    _plot_selection(
        emp_loo,
        emp_mean,
        summ_loo,
        summ_mean,
        seasons=seasons,
        rho=float(args.rho),
        out_path=out_sel,
    )
    print(f"Wrote {out_sel}")

    _plot_roster_compare(
        emp_roster_sizes,
        sim_roster_sizes,
        seasons=seasons,
        out_path=out_roster,
    )
    print(f"Wrote {out_roster}")

    meta = {
        "diagnostic": "grandchild_empirical_roster_caps",
        "date": date.today().isoformat(),
        "seasons": seasons,
        "rho": float(args.rho),
        "gamma": gamma,
        "seed": int(args.seed),
        "roster_mode": "empirical_caps_multiset",
        "empirical": {
            "n_player_seasons": n_total,
            "n_drafted": n_drafted,
            "n_team_seasons_lc": int(emp_lc.size),
            "L_C": glc._summary("L_C", emp_lc),
            "roster_sizes": glc._summary("roster_n", emp_roster_sizes.astype(float)),
            "curvature_loo": gsel._curvature_label(emp_loo),
            "curvature_pool_mean": gsel._curvature_label(emp_mean),
        },
        "sim": {
            "n_player_seasons": int(len(pooled)),
            "n_team_seasons_lc": int(lc_stats["n"]),
            "L_C": lc_stats,
            "roster_sizes": glc._summary("roster_n", sim_roster_sizes.astype(float)),
            "curvature_loo": curv_loo,
            "curvature_pool_mean": curv_mean,
            "season_runs_lc": season_runs_lc,
            "season_runs_select": season_runs_sel,
        },
        "outputs": {
            "lc_png": out_lc.name,
            "selection_png": out_sel.name,
            "roster_compare_png": out_roster.name,
        },
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_meta}")
    print("Done.")


if __name__ == "__main__":
    main()
