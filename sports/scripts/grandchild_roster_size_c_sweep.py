#!/usr/bin/env python3
"""Grandchild LG — roster capacity C sweep (10, 11, 15) vs fixed empirical panel.

Side-by-side sim readouts at fixed rho (default 0.5):
  - Team L_C density (normalized) vs same NCAA empirical
  - Selection rate vs LOO pool quality (+ empirical overlay)
  - Selection rate vs pool mean (+ empirical overlay)

Run (repo root):
  python sports/scripts/grandchild_roster_size_c_sweep.py
  python sports/scripts/grandchild_roster_size_c_sweep.py --rho 0.5 -C 10 11 15

Outputs (HEROs_and_PASSes/grandchild_assign/):
  GRANDCHILD_roster_size_c_sweep_lc_2011_2021.png
  GRANDCHILD_roster_size_c_sweep_selection_2011_2021.png
  GRANDCHILD_roster_size_c_sweep_2011_2021_meta.json
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

from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs
from interval_overlap_paths import seasons_label

import grandchild_empirical_lc_compare as glc
import grandchild_selection_inverted_u_diagnostic as gsel

OUT = GRANDCHILD_ASSIGN
SEASON_MIN = glc.FULL_PANEL_SEASON_MIN
SEASON_MAX = glc.FULL_PANEL_SEASON_MAX
DEFAULT_C = (10, 11, 15)
DEFAULT_RHO = glc.DEFAULT_RHO
DEFAULT_SEED = glc.DEFAULT_SEED
DEFAULT_GAMMA = glc.DEFAULT_GAMMA
N_LC_BINS = glc.N_LC_BINS
EMP_COLOR = glc.EMP_COLOR

C_COLORS = {10: "teal", 11: "mediumpurple", 15: "darkorange"}


def _lc_density(lc: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    edges = np.linspace(0.0, 1.0, N_LC_BINS + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    density, _ = np.histogram(lc, bins=edges, density=True)
    return centers, density


def _plot_lc_sweep(
    emp_lc: np.ndarray,
    by_c: dict[int, np.ndarray],
    *,
    seasons: str,
    rho: float,
    gamma: float,
    out_path: Path,
) -> None:
    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, len(by_c), figsize=(4.2 * len(by_c), 4.5), sharey=True)
    if len(by_c) == 1:
        axes = [axes]

    xe, ye = _lc_density(emp_lc)
    ymax = float(ye.max()) if len(ye) else 1.0

    for ax, c in zip(axes, sorted(by_c), strict=True):
        sim_lc = by_c[c]
        xs, ys = _lc_density(sim_lc)
        ymax = max(ymax, float(ys.max()) if len(ys) else ymax)
        color = C_COLORS.get(c, "darkorange")
        ax.bar(xs, ys, width=1.0 / N_LC_BINS * 0.95, color=color, alpha=0.75, label=rf"LG $C={c}$")
        ax.plot(xe, ye, color=EMP_COLOR, lw=2, ls="--", label="NCAA empirical")
        stats = glc._summary("L_C", sim_lc)
        ax.set_xlim(0, 1)
        ax.set_xticks(glc.LC_TICKS)
        ax.set_xlabel(r"$L_C$")
        ax.set_title(
            rf"$C={c}$ · $n={stats['n']:,}$ teams\n"
            rf"mean={stats['mean']:.3f}, sd={stats['std']:.3f}",
            fontsize=9,
        )
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(axis="y", alpha=0.25)

    axes[0].set_ylabel("Density")
    fig.suptitle(
        rf"Team $L_C$ — LG capacity sweep vs NCAA (MBB {seasons}, "
        rf"$\rho={rho:g}$, $\gamma={gamma:g}$)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _plot_selection_sweep(
    emp_loo: pd.DataFrame,
    emp_mean: pd.DataFrame,
    frames_loo: dict[int, pd.DataFrame],
    frames_mean: dict[int, pd.DataFrame],
    *,
    seasons: str,
    rho: float,
    out_path: Path,
) -> None:
    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8))

    panels = [
        (frames_loo, emp_loo, r"LOO pool quality (poolq_loo)", "mean_loo_q"),
        (frames_mean, emp_mean, r"Pool mean (team_mean)", "mean_team_mean"),
    ]
    for ax, (frames, emp, xlab, xcol) in zip(axes, panels, strict=True):
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
        for c in sorted(frames):
            summ = frames[c]
            x = summ[xcol].to_numpy(dtype=float)
            y = summ["selection_rate"].to_numpy(dtype=float)
            color = C_COLORS.get(c, "darkorange")
            curv = gsel._curvature_label(summ)
            ax.plot(
                x,
                y,
                "o-",
                lw=1.8,
                ms=4,
                color=color,
                label=rf"LG $C={c}$ ({curv['shape'].replace('_', ' ')})",
                zorder=2,
            )
        ax.set_xlabel(xlab, fontsize=10)
        ax.set_ylabel("Selection / draft rate", fontsize=10)
        ax.legend(fontsize=6, loc="upper left")
        ax.grid(alpha=0.25)
        ymax = 0.01
        if len(emp):
            ymax = max(ymax, float(emp["selection_rate"].max()))
        for summ in frames.values():
            ymax = max(ymax, float(summ["selection_rate"].max()))
        ax.set_ylim(0, min(1.0, ymax * 1.15))

    fig.suptitle(
        rf"Grandchild SELECT — capacity $C$ sweep vs empirical (MBB {seasons}, $\rho={rho:g}$)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO)
    parser.add_argument("--gamma", type=float, default=DEFAULT_GAMMA)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "-C",
        "--roster-size",
        type=int,
        nargs="+",
        default=list(DEFAULT_C),
        dest="roster_sizes",
    )
    args = parser.parse_args()
    roster_sizes = sorted(set(int(c) for c in args.roster_sizes))

    ensure_hero_dirs()
    seasons = seasons_label(SEASON_MIN, SEASON_MAX)
    tag = f"{SEASON_MIN}_{SEASON_MAX}"
    out_lc = OUT / f"GRANDCHILD_roster_size_c_sweep_lc_{tag}.png"
    out_sel = OUT / f"GRANDCHILD_roster_size_c_sweep_selection_{tag}.png"
    out_meta = OUT / f"GRANDCHILD_roster_size_c_sweep_{tag}_meta.json"

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
    print(f"Empirical: {emp_lc.size:,} team-seasons  L_C mean={emp_lc.mean():.3f}")

    hero_work = gsel._prepare_hero_panel(SEASON_MIN, SEASON_MAX)
    emp_loo, emp_mean = gsel._empirical_reference_tables(hero_work, assign_poolq_bin_labels)
    k_ref, _, _ = gsel._season_k_theta(hero_work, SEASON_MIN)
    sel_template = gsel._selection_config(tge, cfg, n_selected=max(1, k_ref))

    lc_by_c: dict[int, np.ndarray] = {}
    frames_loo: dict[int, pd.DataFrame] = {}
    frames_mean: dict[int, pd.DataFrame] = {}
    run_meta: list[dict] = []

    for i, c in enumerate(roster_sizes):
        print(f"\n=== C={c} ===")
        sim_team, season_runs = glc._sim_team_lc_panel(
            season_min=SEASON_MIN,
            season_max=SEASON_MAX,
            rho=float(args.rho),
            seed=int(args.seed),
            theta=theta,
            gamma=gamma,
            gc=gc,
            roster_size=c,
        )
        sim_lc = sim_team["L_C"].dropna().to_numpy(dtype=float)
        lc_by_c[c] = sim_lc
        lc_stats = glc._summary("L_C", sim_lc)
        print(f"  L_C: n={lc_stats['n']:,} mean={lc_stats['mean']:.3f} sd={lc_stats['std']:.3f}")

        pooled, summ_loo, summ_mean, sel_runs = gsel._run_panel(
            season_min=SEASON_MIN,
            season_max=SEASON_MAX,
            rho=float(args.rho),
            seed=int(args.seed) + 17 * i,
            gc=gc,
            cfg=cfg,
            sel_template=sel_template,
            c=c,
            hero_work=hero_work,
            tge=tge,
            tpa=tpa,
            assign_poolq_bin_labels=assign_poolq_bin_labels,
        )
        frames_loo[c] = summ_loo
        frames_mean[c] = summ_mean
        curv_loo = gsel._curvature_label(summ_loo)
        curv_mean = gsel._curvature_label(summ_mean)
        print(f"  SELECT LOO: {curv_loo['shape']}  pool mean: {curv_mean['shape']}")

        n_teams_total = int(sum(r.get("n_teams_sim", 0) for r in sel_runs))
        run_meta.append(
            {
                "roster_size": c,
                "n_players_pooled": int(len(pooled)),
                "n_teams_lc": int(lc_stats["n"]),
                "n_teams_select": n_teams_total,
                "L_C": lc_stats,
                "curvature_loo": curv_loo,
                "curvature_pool_mean": curv_mean,
                "season_runs_lc": season_runs,
            }
        )

    _plot_lc_sweep(
        emp_lc,
        lc_by_c,
        seasons=seasons,
        rho=float(args.rho),
        gamma=gamma,
        out_path=out_lc,
    )
    print(f"Wrote {out_lc}")

    _plot_selection_sweep(
        emp_loo,
        emp_mean,
        frames_loo,
        frames_mean,
        seasons=seasons,
        rho=float(args.rho),
        out_path=out_sel,
    )
    print(f"Wrote {out_sel}")

    meta = {
        "diagnostic": "grandchild_roster_size_c_sweep",
        "date": date.today().isoformat(),
        "seasons": seasons,
        "rho": float(args.rho),
        "gamma": gamma,
        "seed": int(args.seed),
        "roster_sizes": roster_sizes,
        "empirical": {
            "n_player_seasons": n_total,
            "n_drafted": n_drafted,
            "n_team_seasons_lc": int(emp_lc.size),
            "L_C": glc._summary("L_C", emp_lc),
            "curvature_loo": gsel._curvature_label(emp_loo),
            "curvature_pool_mean": gsel._curvature_label(emp_mean),
        },
        "runs": run_meta,
        "outputs": {
            "lc_png": out_lc.name,
            "selection_png": out_sel.name,
        },
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_meta}")
    print("Done.")


if __name__ == "__main__":
    main()
