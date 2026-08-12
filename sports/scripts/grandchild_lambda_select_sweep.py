#!/usr/bin/env python3
"""LG λ sweep on SELECT — empirical roster caps (Alex input fix held fixed).

ASSIGN: LG with exact NCAA roster-size multiset, fixed ρ (default 0.5).
SCORE: S = A − λ·L_C (loo_gap_plus_ability); sweep λ = loo_gap_weight.
SELECT: top-K per season (empirical K/N), bin vs Hero LOO + pool mean.

Run (repo root):
  python sports/scripts/grandchild_lambda_select_sweep.py
  python sports/scripts/grandchild_lambda_select_sweep.py --lambda 0 0.55 1.0
  python sports/scripts/grandchild_lambda_select_sweep.py --quick

Outputs (HEROs_and_PASSes/grandchild_assign/):
  GRANDCHILD_lambda_select_sweep_2011_2021.png
  GRANDCHILD_lambda_select_sweep_2011_2021_meta.json
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

from gallery_knobs import LAMBDA_HIGH, LAMBDA_LOW, LAMBDA_MODERATE
from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs
from interval_overlap_paths import seasons_label

import grandchild_empirical_lc_compare as glc
import grandchild_empirical_roster_caps_diagnostic as gcaps
import grandchild_selection_inverted_u_diagnostic as gsel

OUT = GRANDCHILD_ASSIGN
SEASON_MIN = glc.FULL_PANEL_SEASON_MIN
SEASON_MAX = glc.FULL_PANEL_SEASON_MAX
DEFAULT_RHO = glc.DEFAULT_RHO
DEFAULT_SEED = glc.DEFAULT_SEED
DEFAULT_GAMMA = glc.DEFAULT_GAMMA
EMP_COLOR = glc.EMP_COLOR

DEFAULT_LAMBDAS = (0.0, LAMBDA_LOW, LAMBDA_MODERATE, LAMBDA_HIGH, 2.0)
QUICK_LAMBDAS = (0.0, LAMBDA_MODERATE, 1.0)

LAM_COLORS = {
    0.0: "gray",
    0.25: "teal",
    0.55: "darkorange",
    1.0: "mediumpurple",
    2.0: "crimson",
}


def _lambda_color(lam: float) -> str:
    if lam in LAM_COLORS:
        return LAM_COLORS[lam]
    return plt.cm.plasma(min(0.95, max(0.05, lam / 2.0)))


def _plot_selection_sweep(
    emp_loo: pd.DataFrame,
    emp_mean: pd.DataFrame,
    frames_loo: dict[float, pd.DataFrame],
    frames_mean: dict[float, pd.DataFrame],
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
        for lam in sorted(frames):
            summ = frames[lam]
            x = summ[xcol].to_numpy(dtype=float)
            y = summ["selection_rate"].to_numpy(dtype=float)
            curv = gsel._curvature_label(summ)
            color = _lambda_color(float(lam))
            ax.plot(
                x,
                y,
                "o-",
                lw=1.8,
                ms=4,
                color=color,
                label=rf"LG $\lambda={lam:g}$ ({curv['shape'].replace('_', ' ')})",
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
        rf"LG SELECT — $\lambda$ sweep vs empirical (MBB {seasons}, "
        rf"empirical caps, $\rho={rho:g}$, $S=A-\lambda L_C$)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO)
    parser.add_argument("--gamma", type=float, default=DEFAULT_GAMMA)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--lambda",
        dest="lambdas",
        type=float,
        nargs="+",
        default=None,
        help=f"SCORE weights (default: {list(DEFAULT_LAMBDAS)})",
    )
    parser.add_argument(
        "--season-min",
        type=int,
        default=None,
        help=f"Panel start (default {SEASON_MIN}; --quick uses {SEASON_MIN})",
    )
    parser.add_argument(
        "--season-max",
        type=int,
        default=None,
        help=f"Panel end (default {SEASON_MAX})",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help=f"Smoke: seasons {SEASON_MIN} only, λ arms {list(QUICK_LAMBDAS)}",
    )
    args = parser.parse_args()

    if args.quick:
        lambdas = sorted(set(float(x) for x in (args.lambdas or QUICK_LAMBDAS)))
        season_min = int(args.season_min if args.season_min is not None else SEASON_MIN)
        season_max = int(args.season_max if args.season_max is not None else season_min)
    else:
        lambdas = sorted(set(float(x) for x in (args.lambdas or DEFAULT_LAMBDAS)))
        season_min = int(args.season_min if args.season_min is not None else SEASON_MIN)
        season_max = int(args.season_max if args.season_max is not None else SEASON_MAX)

    ensure_hero_dirs()
    seasons = seasons_label(season_min, season_max)
    tag = f"{season_min}_{season_max}"
    out_png = OUT / f"GRANDCHILD_lambda_select_sweep_{tag}.png"
    out_meta = OUT / f"GRANDCHILD_lambda_select_sweep_{tag}_meta.json"

    gc = importlib.import_module("541_grandchild_homophily_assign")
    cfg = gsel._load_cfg()
    tge, tpa, assign_poolq_bin_labels = gsel._load_modules()

    print(f"Loading empirical panel {seasons} ...")
    hero_work = gsel._prepare_hero_panel(season_min, season_max)
    emp_loo, emp_mean = gsel._empirical_reference_tables(hero_work, assign_poolq_bin_labels)
    k_ref, _, _ = gsel._season_k_theta(hero_work, season_min)
    sel_base = gsel._selection_config(tge, cfg, n_selected=max(1, k_ref))

    frames_loo: dict[float, pd.DataFrame] = {}
    frames_mean: dict[float, pd.DataFrame] = {}
    run_meta: list[dict] = []

    from diagnostic_progress import StepProgress

    sweep = StepProgress("λ SELECT sweep", lambdas)
    sweep.header()
    for i, lam in enumerate(lambdas):
        sweep.begin(rf"λ={lam:g}")
        sel = replace(
            sel_base,
            loo_gap_weight=float(lam),
            score_mode="loo_gap_plus_ability",
        )
        pooled, summ_loo, summ_mean, season_runs = gcaps._run_panel_select(
            season_min=season_min,
            season_max=season_max,
            rho=float(args.rho),
            seed=int(args.seed) + 31 * i,
            gc=gc,
            cfg=cfg,
            sel_template=sel,
            hero_work=hero_work,
            tge=tge,
            tpa=tpa,
            assign_poolq_bin_labels=assign_poolq_bin_labels,
        )
        frames_loo[lam] = summ_loo
        frames_mean[lam] = summ_mean
        curv_loo = gsel._curvature_label(summ_loo)
        curv_mean = gsel._curvature_label(summ_mean)
        print(
            f"  SELECT LOO: {curv_loo['shape']}  pool mean: {curv_mean['shape']}  "
            f"(n={len(pooled):,})"
        )
        run_meta.append(
            {
                "lambda": float(lam),
                "score_mode": sel.score_mode,
                "loo_gap_weight": float(lam),
                "n_players_pooled": int(len(pooled)),
                "curvature_loo": curv_loo,
                "curvature_pool_mean": curv_mean,
                "season_runs_select": season_runs,
            }
        )

    sweep.finish()
    print("\nWriting figure ...", flush=True)
    _plot_selection_sweep(
        emp_loo,
        emp_mean,
        frames_loo,
        frames_mean,
        seasons=seasons,
        rho=float(args.rho),
        out_path=out_png,
    )
    print(f"Wrote {out_png}")

    meta = {
        "diagnostic": "grandchild_lambda_select_sweep",
        "date": date.today().isoformat(),
        "seasons": seasons,
        "season_min": season_min,
        "season_max": season_max,
        "rho": float(args.rho),
        "gamma": float(args.gamma),
        "seed": int(args.seed),
        "roster_mode": "empirical_caps_multiset",
        "score": "loo_gap_plus_ability",
        "lambda_values": [float(x) for x in lambdas],
        "empirical": {
            "curvature_loo": gsel._curvature_label(emp_loo),
            "curvature_pool_mean": gsel._curvature_label(emp_mean),
        },
        "runs": run_meta,
        "outputs": {"selection_png": out_png.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_meta}")
    print("Done.")


if __name__ == "__main__":
    main()
