#!/usr/bin/env python3
"""PD20 — log-spaced temperature sweep on Gibbs SELECT (rule D).

ASSIGN: LG with exact NCAA roster-size multiset, fixed ρ (default 0.5).
SCORE: S = A − λ·L_C (loo_gap_plus_ability); two λ panels per Alex PD20 plan.
SELECT: Gibbs weights exp(S/t), K draws without replacement (rule "D").

Run (repo root):
  python sports/scripts/grandchild_temperature_select_sweep.py
  python sports/scripts/grandchild_temperature_select_sweep.py --quick
  python sports/scripts/grandchild_temperature_select_sweep.py --log10-t -2 -1 0 1 2

Outputs (HEROs_and_PASSes/pd20_temperature/):
  GRANDCHILD_temperature_select_sweep_2011_2021.png
  GRANDCHILD_temperature_select_sweep_2011_2021_meta.json

PD17 baseline (top-K, rule C) stays in grandchild_assign/ — unchanged.
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
from hero_gallery_paths import PD20_TEMPERATURE, ensure_hero_dirs
from interval_overlap_paths import seasons_label

import grandchild_empirical_lc_compare as glc
import grandchild_empirical_roster_caps_diagnostic as gcaps
import grandchild_selection_inverted_u_diagnostic as gsel

OUT = PD20_TEMPERATURE
SEASON_MIN = glc.FULL_PANEL_SEASON_MIN
SEASON_MAX = glc.FULL_PANEL_SEASON_MAX
DEFAULT_RHO = glc.DEFAULT_RHO
DEFAULT_SEED = glc.DEFAULT_SEED
DEFAULT_GAMMA = glc.DEFAULT_GAMMA
EMP_COLOR = glc.EMP_COLOR

# Alex PD20 panels: λ at breakpoint band (PD17 λ sweep: U emerges ~1.5–2).
DEFAULT_LAMBDAS = (1.5, 2.0)
QUICK_LAMBDAS = (2.0,)

# log10(t) grid — Alex: sweep orders of magnitude in the exponent.
DEFAULT_LOG10_T = tuple(float(x) for x in np.linspace(-3.0, 3.0, 13))
QUICK_LOG10_T = (-2.0, -1.0, 0.0, 1.0, 2.0)


def _temperature_palette(log10_t_values: list[float]) -> dict[float, str]:
    sorted_t = sorted(set(float(x) for x in log10_t_values))
    n = len(sorted_t)
    cmap = plt.cm.plasma if n <= 12 else plt.cm.viridis
    return {t: cmap(i / max(n - 1, 1)) for i, t in enumerate(sorted_t)}


def _plot_temperature_sweep(
    emp_loo: pd.DataFrame,
    emp_mean: pd.DataFrame,
    panels: dict[float, tuple[dict[float, pd.DataFrame], dict[float, pd.DataFrame]]],
    *,
    seasons: str,
    rho: float,
    log10_t_values: list[float],
    out_path: Path,
) -> None:
    configure_matplotlib_mathtext()
    lambdas = sorted(panels)
    fig, axes = plt.subplots(len(lambdas), 2, figsize=(12.0, 4.8 * len(lambdas)))
    if len(lambdas) == 1:
        axes = np.array([axes])
    colors = _temperature_palette(log10_t_values)
    col_specs = [
        (0, "LOO pool quality (poolq_loo)", "mean_loo_q"),
        (1, "Pool mean (team_mean)", "mean_team_mean"),
    ]
    for row, lam in enumerate(lambdas):
        frames_loo, frames_mean = panels[lam]
        for col, xlab, xcol in col_specs:
            ax = axes[row, col]
            emp = emp_loo if col == 0 else emp_mean
            frames = frames_loo if col == 0 else frames_mean
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
            for log10_t in sorted(frames):
                summ = frames[log10_t]
                x = summ[xcol].to_numpy(dtype=float)
                y = summ["selection_rate"].to_numpy(dtype=float)
                curv = gsel._curvature_label(summ)
                t_val = 10.0 ** float(log10_t)
                ax.plot(
                    x,
                    y,
                    "o-",
                    lw=1.8,
                    ms=4,
                    color=colors[float(log10_t)],
                    label=rf"$t={t_val:g}$ ({curv['shape'].replace('_', ' ')})",
                    zorder=2,
                )
            ax.set_xlabel(xlab, fontsize=10)
            if col == 0:
                ax.set_ylabel("Selection / draft rate", fontsize=10)
            ax.legend(fontsize=5.5, loc="upper left")
            ax.grid(alpha=0.25)
            ymax = 0.01
            if len(emp):
                ymax = max(ymax, float(emp["selection_rate"].max()))
            for summ in frames.values():
                ymax = max(ymax, float(summ["selection_rate"].max()))
            ax.set_ylim(0, min(1.0, ymax * 1.15))
        axes[row, 0].set_title(rf"Panel $\lambda={lam:g}$", fontsize=10, loc="left")

    fig.suptitle(
        rf"PD20 Gibbs SELECT — $t$ sweep vs empirical (MBB {seasons}, "
        rf"empirical caps, $\rho={rho:g}$, rule D, $S=A-\lambda L_C$)",
        fontsize=11,
        y=1.01,
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
        help=f"SCORE λ panels (default: {list(DEFAULT_LAMBDAS)})",
    )
    parser.add_argument(
        "--log10-t",
        dest="log10_t",
        type=float,
        nargs="+",
        default=None,
        help=f"log10(temperature) grid (default: {len(DEFAULT_LOG10_T)} pts −3…3)",
    )
    parser.add_argument(
        "--season-min",
        type=int,
        default=None,
        help=f"Panel start (default {SEASON_MIN})",
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
        help=f"Smoke: season {SEASON_MIN} only, λ={list(QUICK_LAMBDAS)}, "
        f"log10 t={list(QUICK_LOG10_T)}",
    )
    args = parser.parse_args()

    if args.quick:
        lambdas = sorted(set(float(x) for x in (args.lambdas or QUICK_LAMBDAS)))
        log10_t_values = sorted(set(float(x) for x in (args.log10_t or QUICK_LOG10_T)))
        season_min = int(args.season_min if args.season_min is not None else SEASON_MIN)
        season_max = int(args.season_max if args.season_max is not None else season_min)
    else:
        lambdas = sorted(set(float(x) for x in (args.lambdas or DEFAULT_LAMBDAS)))
        log10_t_values = sorted(
            set(float(x) for x in (args.log10_t or DEFAULT_LOG10_T))
        )
        season_min = int(args.season_min if args.season_min is not None else SEASON_MIN)
        season_max = int(args.season_max if args.season_max is not None else SEASON_MAX)

    ensure_hero_dirs()
    seasons = seasons_label(season_min, season_max)
    tag = f"{season_min}_{season_max}"
    out_png = OUT / f"GRANDCHILD_temperature_select_sweep_{tag}.png"
    out_meta = OUT / f"GRANDCHILD_temperature_select_sweep_{tag}_meta.json"

    gc = importlib.import_module("541_grandchild_homophily_assign")
    cfg = gsel._load_cfg()
    tge, tpa, assign_poolq_bin_labels = gsel._load_modules()

    print(f"Loading empirical panel {seasons} ...")
    hero_work = gsel._prepare_hero_panel(season_min, season_max)
    emp_loo, emp_mean = gsel._empirical_reference_tables(hero_work, assign_poolq_bin_labels)
    k_ref, _, _ = gsel._season_k_theta(hero_work, season_min)
    sel_base = gsel._selection_config(tge, cfg, n_selected=max(1, k_ref))
    sel_base = replace(
        sel_base,
        winner_selection="D",
        score_mode="loo_gap_plus_ability",
    )

    panels: dict[float, tuple[dict[float, pd.DataFrame], dict[float, pd.DataFrame]]] = {}
    run_meta: list[dict] = []

    from diagnostic_progress import StepProgress

    for lam_idx, lam in enumerate(lambdas):
        frames_loo: dict[float, pd.DataFrame] = {}
        frames_mean: dict[float, pd.DataFrame] = {}
        sweep = StepProgress(
            rf"λ={lam:g} t sweep",
            [f"log10 t={x:g}" for x in log10_t_values],
        )
        sweep.header()
        for t_idx, log10_t in enumerate(log10_t_values):
            temperature = float(10.0 ** float(log10_t))
            sweep.begin(rf"log10 t={log10_t:g}  (t={temperature:g})")
            sel = replace(
                sel_base,
                loo_gap_weight=float(lam),
                selection_temperature=temperature,
            )
            pooled, summ_loo, summ_mean, season_runs = gcaps._run_panel_select(
                season_min=season_min,
                season_max=season_max,
                rho=float(args.rho),
                seed=int(args.seed) + 31 * lam_idx + 17 * t_idx,
                gc=gc,
                cfg=cfg,
                sel_template=sel,
                hero_work=hero_work,
                tge=tge,
                tpa=tpa,
                assign_poolq_bin_labels=assign_poolq_bin_labels,
            )
            frames_loo[log10_t] = summ_loo
            frames_mean[log10_t] = summ_mean
            curv_loo = gsel._curvature_label(summ_loo)
            curv_mean = gsel._curvature_label(summ_mean)
            print(
                f"  SELECT LOO: {curv_loo['shape']}  pool mean: {curv_mean['shape']}  "
                f"(n={len(pooled):,})"
            )
            run_meta.append(
                {
                    "lambda": float(lam),
                    "log10_t": float(log10_t),
                    "temperature": temperature,
                    "winner_selection": "D",
                    "n_players_pooled": int(len(pooled)),
                    "curvature_loo": curv_loo,
                    "curvature_pool_mean": curv_mean,
                    "season_runs_select": season_runs,
                }
            )
        sweep.finish()
        panels[float(lam)] = (frames_loo, frames_mean)

    print("\nWriting figure ...", flush=True)
    _plot_temperature_sweep(
        emp_loo,
        emp_mean,
        panels,
        seasons=seasons,
        rho=float(args.rho),
        log10_t_values=log10_t_values,
        out_path=out_png,
    )
    print(f"Wrote {out_png}")

    meta = {
        "diagnostic": "grandchild_temperature_select_sweep",
        "date": date.today().isoformat(),
        "seasons": seasons,
        "season_min": season_min,
        "season_max": season_max,
        "rho": float(args.rho),
        "gamma": float(args.gamma),
        "seed": int(args.seed),
        "roster_mode": "empirical_caps_multiset",
        "score": "loo_gap_plus_ability",
        "winner_selection": "D",
        "lambda_panels": [float(x) for x in lambdas],
        "log10_t_values": [float(x) for x in log10_t_values],
        "temperature_values": [float(10.0 ** x) for x in log10_t_values],
        "empirical": {
            "curvature_loo": gsel._curvature_label(emp_loo),
            "curvature_pool_mean": gsel._curvature_label(emp_mean),
        },
        "runs": run_meta,
        "outputs": {"selection_png": out_png.name},
        "pd17_baseline_note": "grandchild_lambda_select_sweep.py (rule C) in grandchild_assign/",
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_meta}")
    print("Done.")


if __name__ == "__main__":
    main()
