#!/usr/bin/env python3
"""PD20 thin diagnostic — cold Gibbs (rule D) vs top-K (rule C) overlay.

At λ in the breakpoint band and very small t, rule D should ≈ rule C (hard cut).
Same ASSIGN seeds for both arms; only SELECT differs.

Run (repo root):
  python sports/scripts/grandchild_temperature_cold_limit_diagnostic.py
  python sports/scripts/grandchild_temperature_cold_limit_diagnostic.py --quick

Outputs (HEROs_and_PASSes/pd20_temperature/):
  GRANDCHILD_temperature_cold_limit_2011_2021.png
  GRANDCHILD_temperature_cold_limit_2011_2021_meta.json
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
DEFAULT_LAMBDA = 2.0
DEFAULT_LOG10_T = -3.0
DEFAULT_T = float(10.0 ** DEFAULT_LOG10_T)
EMP_COLOR = glc.EMP_COLOR
C_COLOR = "crimson"
D_COLOR = "mediumpurple"


def _plot_rule_arm(
    ax,
    summ: pd.DataFrame,
    xcol: str,
    *,
    color: str,
    label: str,
    linestyle: str,
    marker: str,
    fillstyle: str,
    zorder: int,
) -> None:
    x = summ[xcol].to_numpy(dtype=float)
    y = summ["selection_rate"].to_numpy(dtype=float)
    curv = gsel._curvature_label(summ)
    ax.plot(
        x,
        y,
        marker=marker,
        linestyle=linestyle,
        lw=2.4 if linestyle == "-" else 2.0,
        ms=6,
        mfc=color if fillstyle == "full" else "none",
        mew=1.8,
        color=color,
        fillstyle=fillstyle,
        label=f"{label} ({curv['shape'].replace('_', ' ')})",
        zorder=zorder,
    )


def _plot_cold_limit(
    emp_loo: pd.DataFrame,
    emp_mean: pd.DataFrame,
    summ_c_loo: pd.DataFrame,
    summ_c_mean: pd.DataFrame,
    summ_d_loo: pd.DataFrame,
    summ_d_mean: pd.DataFrame,
    *,
    seasons: str,
    rho: float,
    lam: float,
    temperature: float,
    out_path: Path,
    curves_coincide: bool,
) -> None:
    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8))
    panels = [
        (emp_loo, summ_c_loo, summ_d_loo, r"LOO pool quality (poolq_loo)", "mean_loo_q"),
        (emp_mean, summ_c_mean, summ_d_mean, r"Pool mean (team_mean)", "mean_team_mean"),
    ]
    for ax, (emp, summ_c, summ_d, xlab, xcol) in zip(axes, panels, strict=True):
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
        _plot_rule_arm(
            ax,
            summ_c,
            xcol,
            color=C_COLOR,
            label=r"Rule C (top-$K$)",
            linestyle="-",
            marker="o",
            fillstyle="full",
            zorder=2,
        )
        _plot_rule_arm(
            ax,
            summ_d,
            xcol,
            color=D_COLOR,
            label=rf"Rule D ($t={temperature:g}$)",
            linestyle="--",
            marker="o",
            fillstyle="none",
            zorder=3,
        )
        ax.set_xlabel(xlab, fontsize=10)
        ax.set_ylabel("Selection / draft rate", fontsize=10)
        ax.legend(fontsize=8, loc="upper left")
        ax.grid(alpha=0.25)
        ymax = 0.01
        if len(emp):
            ymax = max(ymax, float(emp["selection_rate"].max()))
        for summ in (summ_c, summ_d):
            ymax = max(ymax, float(summ["selection_rate"].max()))
        ax.set_ylim(0, min(1.0, ymax * 1.15))

    if curves_coincide:
        fig.text(
            0.99,
            0.01,
            r"C $\equiv$ D (bin-for-bin at cold $t$)",
            ha="right",
            va="bottom",
            fontsize=9,
            color="0.35",
        )

    fig.suptitle(
        rf"Cold Gibbs check — rule C vs D ($\lambda={lam:g}$, $t={temperature:g}$, "
        rf"MBB {seasons}, $\rho={rho:g}$)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _max_bin_gap(a: pd.DataFrame, b: pd.DataFrame) -> float:
    merged = a.merge(b, on="bin", suffixes=("_a", "_b"))
    if not len(merged):
        return float("nan")
    return float(
        np.max(
            np.abs(
                merged["selection_rate_a"].to_numpy(dtype=float)
                - merged["selection_rate_b"].to_numpy(dtype=float)
            )
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--lambda", dest="lam", type=float, default=DEFAULT_LAMBDA)
    parser.add_argument("--log10-t", type=float, default=DEFAULT_LOG10_T)
    parser.add_argument("--season-min", type=int, default=None)
    parser.add_argument("--season-max", type=int, default=None)
    parser.add_argument(
        "--quick",
        action="store_true",
        help=f"Smoke: season {SEASON_MIN} only",
    )
    args = parser.parse_args()

    temperature = float(10.0 ** float(args.log10_t))
    if args.quick:
        season_min = int(args.season_min if args.season_min is not None else SEASON_MIN)
        season_max = int(args.season_max if args.season_max is not None else season_min)
    else:
        season_min = int(args.season_min if args.season_min is not None else SEASON_MIN)
        season_max = int(args.season_max if args.season_max is not None else SEASON_MAX)

    ensure_hero_dirs()
    seasons = seasons_label(season_min, season_max)
    tag = f"{season_min}_{season_max}"
    out_png = OUT / f"GRANDCHILD_temperature_cold_limit_{tag}.png"
    out_meta = OUT / f"GRANDCHILD_temperature_cold_limit_{tag}_meta.json"

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
        loo_gap_weight=float(args.lam),
        score_mode="loo_gap_plus_ability",
    )

    sel_c = replace(sel_base, winner_selection="C")
    sel_d = replace(
        sel_base,
        winner_selection="D",
        selection_temperature=temperature,
    )

    print("Running rule C (top-K) ...")
    _, summ_c_loo, summ_c_mean, runs_c = gcaps._run_panel_select(
        season_min=season_min,
        season_max=season_max,
        rho=float(args.rho),
        seed=int(args.seed),
        gc=gc,
        cfg=cfg,
        sel_template=sel_c,
        hero_work=hero_work,
        tge=tge,
        tpa=tpa,
        assign_poolq_bin_labels=assign_poolq_bin_labels,
    )

    print("Running rule D (cold Gibbs) ...")
    _, summ_d_loo, summ_d_mean, runs_d = gcaps._run_panel_select(
        season_min=season_min,
        season_max=season_max,
        rho=float(args.rho),
        seed=int(args.seed),
        gc=gc,
        cfg=cfg,
        sel_template=sel_d,
        hero_work=hero_work,
        tge=tge,
        tpa=tpa,
        assign_poolq_bin_labels=assign_poolq_bin_labels,
    )

    gap_loo = _max_bin_gap(summ_c_loo, summ_d_loo)
    gap_mean = _max_bin_gap(summ_c_mean, summ_d_mean)
    curv_c_loo = gsel._curvature_label(summ_c_loo)
    curv_d_loo = gsel._curvature_label(summ_d_loo)

    print(
        f"  max |C−D| bin gap: LOO={gap_loo:.6f}  pool mean={gap_mean:.6f}"
    )
    print(f"  LOO curvature: C={curv_c_loo['shape']}  D={curv_d_loo['shape']}")

    _plot_cold_limit(
        emp_loo,
        emp_mean,
        summ_c_loo,
        summ_c_mean,
        summ_d_loo,
        summ_d_mean,
        seasons=seasons,
        rho=float(args.rho),
        lam=float(args.lam),
        temperature=temperature,
        out_path=out_png,
        curves_coincide=gap_loo < 1e-9 and gap_mean < 1e-9,
    )
    print(f"Wrote {out_png}")

    meta = {
        "diagnostic": "grandchild_temperature_cold_limit",
        "date": date.today().isoformat(),
        "seasons": seasons,
        "season_min": season_min,
        "season_max": season_max,
        "rho": float(args.rho),
        "seed": int(args.seed),
        "lambda": float(args.lam),
        "log10_t": float(args.log10_t),
        "temperature": temperature,
        "winner_c": "C",
        "winner_d": "D",
        "max_bin_gap_loo": gap_loo,
        "max_bin_gap_pool_mean": gap_mean,
        "curvature_loo_c": curv_c_loo,
        "curvature_loo_d": curv_d_loo,
        "curvature_pool_mean_c": gsel._curvature_label(summ_c_mean),
        "curvature_pool_mean_d": gsel._curvature_label(summ_d_mean),
        "cold_limit_match": gap_loo < 1e-9 and gap_mean < 1e-9,
        "outputs": {"png": out_png.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_meta}")
    print("Done.")


if __name__ == "__main__":
    main()
