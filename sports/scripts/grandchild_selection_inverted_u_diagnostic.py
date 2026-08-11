#!/usr/bin/env python3
"""Grandchild ASSIGN → SCORE → SELECT — inverted-U vs empirical (smoothed panel).

Apples-to-apples default: MBB 2011–2021 (same full panel as PD17 slide 3 / Pass A hero).
One Grandchild assign + top-K select **per season**, then stack player-seasons and bin once.

Overlays empirical NCAA draft rate (real rosters) on the LOO pool-quality axis.

Run (repo root):
  python sports/scripts/grandchild_selection_inverted_u_diagnostic.py
  python sports/scripts/grandchild_selection_inverted_u_diagnostic.py --rho 0.5
  python sports/scripts/grandchild_selection_inverted_u_diagnostic.py --season 2015
  python sports/scripts/grandchild_selection_inverted_u_diagnostic.py --rho-sweep

Outputs (HEROs_and_PASSes/grandchild_assign/):
  GRANDCHILD_selection_inverted_u_2011_2021.png      — default full panel
  GRANDCHILD_selection_inverted_u_2011_2021_meta.json
  GRANDCHILD_selection_inverted_u_2011_2021_rho_sweep.png  (--rho-sweep)
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
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

from gallery_knobs import HERO_BINS, resolve_pool_l_mode
from hero_gallery_paths import GRANDCHILD_ASSIGN, ensure_hero_dirs
from interval_overlap_paths import seasons_label, window_tag

FULL_PANEL_SEASON_MIN = 2011
FULL_PANEL_SEASON_MAX = 2021
OUT = GRANDCHILD_ASSIGN

DEFAULT_RHO = 0.5
DEFAULT_SEED = 5412015
N_BINS = HERO_BINS
POOL_ID_SEASON_OFFSET = 100_000


def _output_paths(season_min: int, season_max: int) -> dict:
    tag = window_tag(season_min, season_max) if season_min != season_max else str(season_min)
    stem = f"GRANDCHILD_selection_inverted_u_{tag}"
    return {
        "png": OUT / f"{stem}.png",
        "png_sweep": OUT / f"{stem}_rho_sweep.png",
        "meta": OUT / f"{stem}_meta.json",
        "season_min": season_min,
        "season_max": season_max,
        "seasons": seasons_label(season_min, season_max),
    }


def _load_modules():
    for mod_name in list(sys.modules):
        if mod_name.startswith("tier1_"):
            del sys.modules[mod_name]
    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    return tge, tpa, assign_poolq_bin_labels


def _load_cfg():
    mod_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _hero_pipeline_config():
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=N_BINS,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=20,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=FULL_PANEL_SEASON_MIN,
        panel_season_max=FULL_PANEL_SEASON_MAX,
        analysis_season_min=FULL_PANEL_SEASON_MIN,
        analysis_season_max=FULL_PANEL_SEASON_MAX,
    )


def _prepare_hero_panel(season_min: int, season_max: int) -> pd.DataFrame:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _hero_pipeline_config()
    panel = conductor.prepare_panel(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    use = panel_build.filter_panel(panel, cfg)
    use = use.loc[(use["season"] >= season_min) & (use["season"] <= season_max)].copy()
    return use


def _selection_config(tge, mod, *, n_selected: int, n_bins: int = N_BINS):
    w = float(getattr(mod, "SELECTION_539_LOO_GAP_WEIGHT", 0.55))
    pool_l_mode = resolve_pool_l_mode()
    return tge.SelectionConfig(
        n_bins=int(n_bins),
        bin_mode=str(getattr(mod, "GENERATIVE_POOLQ_BINNING", "quantile")),
        n_selected=int(n_selected),
        score_mode=str(getattr(mod, "SELECTION_539_SCORE_MODE", "loo_gap_plus_ability")),
        loo_gap_weight=w,
        winner_selection=str(getattr(mod, "SELECTION_539_WINNER_SELECTION", "C")),
        loo_pool_l_mode=pool_l_mode,
    )


def _season_k_theta(work: pd.DataFrame, season: int) -> tuple[int, float, dict]:
    sub = work.loc[work["season"] == int(season)].dropna(subset=["perf"])
    ability = sub["perf"].to_numpy(dtype=float)
    n_total = int(len(sub))
    if "Y_draft" in sub.columns:
        n_drafted = int(sub["Y_draft"].sum())
    else:
        n_drafted = max(1, int(round(0.01 * n_total)))
    k = max(1, n_drafted)
    k_over_n = k / n_total if n_total else float("nan")
    theta = float(np.quantile(ability, 1.0 - k_over_n)) if n_total else float("nan")
    return k, theta, {
        "season": int(season),
        "n_total": n_total,
        "n_drafted_empirical": n_drafted,
        "K": k,
        "K_over_N": k_over_n,
        "theta_quantile": 1.0 - k_over_n if n_total else float("nan"),
        "viability_theta": theta,
    }


def _empirical_reference_tables(
    work: pd.DataFrame,
    assign_poolq_bin_labels,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Real NCAA rosters: draft rate vs LOO pool quality and vs team mean."""
    ycol = "Y_draft"
    loo = work.dropna(subset=["poolq_loo", ycol]).copy()
    loo["bin"] = assign_poolq_bin_labels(loo["poolq_loo"], N_BINS, "quantile")
    summ_loo = (
        loo.dropna(subset=["bin"])
        .groupby("bin", observed=True)
        .agg(
            n=(ycol, "size"),
            selection_rate=(ycol, "mean"),
            mean_loo_q=("poolq_loo", "mean"),
        )
        .reset_index()
        .sort_values("mean_loo_q")
    )

    mean = work.dropna(subset=["perf", ycol]).copy()
    mean["team_mean"] = mean.groupby(["team_id", "season"], observed=True)["perf"].transform(
        "mean"
    )
    mean["bin"] = assign_poolq_bin_labels(mean["team_mean"], N_BINS, "quantile")
    summ_mean = (
        mean.dropna(subset=["bin"])
        .groupby("bin", observed=True)
        .agg(
            n=(ycol, "size"),
            selection_rate=(ycol, "mean"),
            mean_team_mean=("team_mean", "mean"),
        )
        .reset_index()
        .sort_values("mean_team_mean")
    )
    return summ_loo, summ_mean


def _curvature_label(summ: pd.DataFrame, *, rate_col: str = "selection_rate") -> dict:
    y = summ[rate_col].to_numpy(dtype=float)
    if len(y) < 3:
        return {"shape": "insufficient_bins", "peak_bin": None}
    peak_idx = int(np.argmax(y))
    peak_interior = 0 < peak_idx < len(y) - 1
    left = float(y[0])
    right = float(y[-1])
    peak = float(y[peak_idx])
    endpoints_below_peak = peak > left and peak > right
    if peak_interior and endpoints_below_peak:
        shape = "inverted_u_like"
    elif peak_idx == len(y) - 1:
        shape = "monotone_increasing"
    elif peak_idx == 0:
        shape = "monotone_decreasing"
    else:
        shape = "other"
    return {
        "shape": shape,
        "peak_bin": peak_idx,
        "peak_rate": peak,
        "left_rate": left,
        "right_rate": right,
    }


def _run_one_season(
    *,
    season: int,
    rho: float,
    seed: int,
    gc,
    cfg,
    sel_template,
    c: int,
    hero_work: pd.DataFrame,
    tge,
    tpa,
) -> tuple[pd.DataFrame, dict]:
    ability, emp_meta = gc.load_empirical_abilities_season(int(season), roster_size=c)
    params = gc.assignment_params_for_abilities(ability, roster_size=c)
    k, theta, season_meta = _season_k_theta(hero_work, season)
    params = replace(
        params,
        viability_theta=float(theta),
        viability_sharpness=float(getattr(cfg, "SELECTION_539_VIABILITY_SHARPNESS", 10.0)),
        assignment_rho=float(rho),
    )
    sel = replace(sel_template, n_selected=int(k))
    rng = np.random.default_rng(int(seed) + int(season))
    players, _, _ = tpa.simulate_generative_rosters(
        params,
        rng=rng,
        method="grandchild",
        ability=ability,
        team_targets=None,
    )
    players = tpa.assign_selection(
        players,
        rng,
        n_selected=sel.n_selected,
        score_mode=sel.score_mode,
        loo_gap_weight=sel.loo_gap_weight,
        winner_selection=sel.winner_selection,
        pool_l_mode=sel.loo_pool_l_mode,
        viability_theta=params.viability_theta,
        viability_sharpness=params.viability_sharpness,
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


def _run_panel(
    *,
    season_min: int,
    season_max: int,
    rho: float,
    seed: int,
    gc,
    cfg,
    sel_template,
    c: int,
    hero_work: pd.DataFrame,
    tge,
    tpa,
    assign_poolq_bin_labels,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, list[dict]]:
    seasons = list(range(int(season_min), int(season_max) + 1))
    parts: list[pd.DataFrame] = []
    season_runs: list[dict] = []
    for season in seasons:
        players, info = _run_one_season(
            season=season,
            rho=float(rho),
            seed=int(seed),
            gc=gc,
            cfg=cfg,
            sel_template=sel_template,
            c=c,
            hero_work=hero_work,
            tge=tge,
            tpa=tpa,
        )
        parts.append(players)
        season_runs.append(info)
        print(
            f"  season {season}: N={info['n_players_sim']:,}  K={info['K']}  "
            f"theta={info['viability_theta']:.3f}  selected={int(players['Y_selected'].sum())}"
        )

    pooled = pd.concat(parts, ignore_index=True)
    summ_loo = tge.inverted_u_bin_table(
        pooled, sel_template, assign_poolq_bin_labels=assign_poolq_bin_labels, tpa=tpa
    )
    summ_mean = tge.inverted_u_bin_table_team_mean(
        pooled, sel_template, assign_poolq_bin_labels=assign_poolq_bin_labels
    )
    return pooled, summ_loo, summ_mean, season_runs


def _plot_dual(
    summ_loo: pd.DataFrame,
    summ_mean: pd.DataFrame,
    *,
    emp_loo: pd.DataFrame | None,
    emp_mean: pd.DataFrame | None,
    rho: float,
    title_suffix: str,
    out_path: Path,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8))

    panels = [
        (summ_loo, emp_loo, r"LOO pool quality ($L_Q$ / poolq_loo)", "mean_loo_q"),
        (summ_mean, emp_mean, r"Pool mean (team_mean)", "mean_team_mean"),
    ]
    for ax, (summ, emp, xlab, xcol) in zip(axes, panels, strict=True):
        if emp is not None and len(emp):
            xe = emp[xcol].to_numpy(dtype=float)
            ye = emp["selection_rate"].to_numpy(dtype=float)
            ax.plot(
                xe,
                ye,
                "s--",
                color="steelblue",
                lw=1.8,
                ms=5,
                alpha=0.9,
                label="Empirical NCAA (real rosters)",
                zorder=2,
            )
        x = summ[xcol].to_numpy(dtype=float)
        y = summ["selection_rate"].to_numpy(dtype=float)
        ax.plot(
            x,
            y,
            "o-",
            color="darkorange",
            lw=2.0,
            ms=6,
            label=rf"Grandchild sim ($\rho={rho:g}$)",
            zorder=3,
        )
        ax.fill_between(x, 0, y, alpha=0.10, color="darkorange")
        ax.set_xlabel(xlab, fontsize=10)
        ax.set_ylabel("Selection / draft rate", fontsize=10)
        ymax = max(
            float(y.max()) if len(y) else 0.0,
            float(ye.max()) if emp is not None and len(emp) else 0.0,
        )
        ax.set_ylim(0, min(1.0, max(ymax * 1.15, 0.01)))
        curv = _curvature_label(summ)
        ax.set_title(
            f"{xlab.split('(')[0].strip()} — sim: {curv['shape'].replace('_', ' ')}",
            fontsize=10,
        )
        ax.legend(fontsize=7, loc="upper left")

    fig.suptitle(
        rf"Grandchild ASSIGN ($\rho={rho:g}$) → congestion SCORE → top-$K$ SELECT"
        + title_suffix,
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


def _plot_rho_sweep(
    frames_loo: dict[float, pd.DataFrame],
    frames_mean: dict[float, pd.DataFrame],
    *,
    emp_loo: pd.DataFrame | None,
    emp_mean: pd.DataFrame | None,
    seasons: str,
    out_path: Path,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.8))
    colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(frames_loo)))

    panels = [
        (frames_loo, emp_loo, r"LOO pool quality", "mean_loo_q"),
        (frames_mean, emp_mean, r"Pool mean (team_mean)", "mean_team_mean"),
    ]
    for ax, (frames, emp, xlab, xcol) in zip(axes, panels, strict=True):
        if emp is not None and len(emp):
            ax.plot(
                emp[xcol],
                emp["selection_rate"],
                "s--",
                color="steelblue",
                lw=2.0,
                ms=4,
                alpha=0.85,
                label="Empirical NCAA",
                zorder=1,
            )
        for (rho, summ), color in zip(sorted(frames.items()), colors, strict=True):
            x = summ[xcol].to_numpy(dtype=float)
            y = summ["selection_rate"].to_numpy(dtype=float)
            ax.plot(x, y, "o-", lw=1.6, ms=3, color=color, label=rf"$\rho={rho:g}$", zorder=2)
        ax.set_xlabel(xlab, fontsize=10)
        ax.set_ylabel("Selection / draft rate", fontsize=10)
        ax.legend(fontsize=6, loc="best")
        ax.set_title(xlab, fontsize=10)

    fig.suptitle(
        rf"Grandchild $\rho$ sweep vs empirical — MBB {seasons} (stacked player-seasons)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


def _resolve_season_window(args) -> tuple[int, int]:
    if args.season is not None:
        return int(args.season), int(args.season)
    if args.season_min is not None or args.season_max is not None:
        if args.season_min is None or args.season_max is None:
            raise SystemExit("--season-min and --season-max must be supplied together")
        return int(args.season_min), int(args.season_max)
    return FULL_PANEL_SEASON_MIN, FULL_PANEL_SEASON_MAX


def main() -> None:
    parser = argparse.ArgumentParser(description="Grandchild inverted-U selection diagnostic")
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--season", type=int, default=None, help="Single-season run (legacy)")
    parser.add_argument("--season-min", type=int, default=None)
    parser.add_argument("--season-max", type=int, default=None)
    parser.add_argument(
        "--rho-sweep",
        action="store_true",
        help="Also plot ρ in {0, 0.25, 0.5, 0.75, 1} on same stacked panel",
    )
    args = parser.parse_args()

    season_min, season_max = _resolve_season_window(args)
    paths = _output_paths(season_min, season_max)

    ensure_hero_dirs()
    gc = importlib.import_module("541_grandchild_homophily_assign")
    cfg = _load_cfg()
    tge, tpa, assign_poolq_bin_labels = _load_modules()
    c = int(gc.ROSTER_SIZE_DEFAULT)

    print(f"Loading hero panel {season_min}–{season_max} ...")
    hero_work = _prepare_hero_panel(season_min, season_max)
    emp_loo, emp_mean = _empirical_reference_tables(hero_work, assign_poolq_bin_labels)
    print(
        f"Empirical reference: N={len(hero_work):,} player-seasons, "
        f"drafts={int(hero_work['Y_draft'].sum()):,}"
    )

    # Placeholder K for SelectionConfig template (actual K is per season).
    k_ref, _, _ = _season_k_theta(hero_work, season_min)
    sel_template = _selection_config(tge, cfg, n_selected=max(1, k_ref))

    print(f"Running Grandchild panel assign (ρ={args.rho:g}) ...")
    pooled, summ_loo, summ_mean, season_runs = _run_panel(
        season_min=season_min,
        season_max=season_max,
        rho=float(args.rho),
        seed=int(args.seed),
        gc=gc,
        cfg=cfg,
        sel_template=sel_template,
        c=c,
        hero_work=hero_work,
        tge=tge,
        tpa=tpa,
        assign_poolq_bin_labels=assign_poolq_bin_labels,
    )

    n_selected_total = int(pooled["Y_selected"].sum())
    title_suffix = (
        rf" (MBB {paths['seasons']}, stacked $N={len(pooled):,}$, "
        rf"$\Sigma K={n_selected_total:,}$)"
    )
    _plot_dual(
        summ_loo,
        summ_mean,
        emp_loo=emp_loo,
        emp_mean=emp_mean,
        rho=float(args.rho),
        title_suffix=title_suffix,
        out_path=paths["png"],
    )

    curv_loo = _curvature_label(summ_loo)
    curv_mean = _curvature_label(summ_mean)
    curv_emp_loo = _curvature_label(emp_loo)
    curv_emp_mean = _curvature_label(emp_mean)

    sweep_meta: list[dict] = []
    if args.rho_sweep:
        rhos = [0.0, 0.25, 0.5, 0.75, 1.0]
        frames_loo: dict[float, pd.DataFrame] = {}
        frames_mean: dict[float, pd.DataFrame] = {}
        for i, rho in enumerate(rhos):
            print(f"ρ sweep: {rho:g} ...")
            _, s_loo, s_mean, _ = _run_panel(
                season_min=season_min,
                season_max=season_max,
                rho=float(rho),
                seed=int(args.seed) + 100 * i,
                gc=gc,
                cfg=cfg,
                sel_template=sel_template,
                c=c,
                hero_work=hero_work,
                tge=tge,
                tpa=tpa,
                assign_poolq_bin_labels=assign_poolq_bin_labels,
            )
            frames_loo[rho] = s_loo
            frames_mean[rho] = s_mean
            sweep_meta.append(
                {
                    "rho": float(rho),
                    "loo_shape": _curvature_label(s_loo)["shape"],
                    "team_mean_shape": _curvature_label(s_mean)["shape"],
                }
            )
        _plot_rho_sweep(
            frames_loo,
            frames_mean,
            emp_loo=emp_loo,
            emp_mean=emp_mean,
            seasons=paths["seasons"],
            out_path=paths["png_sweep"],
        )

    meta = {
        "diagnostic": "grandchild_selection_inverted_u",
        "date": date.today().isoformat(),
        "season_min": season_min,
        "season_max": season_max,
        "seasons": paths["seasons"],
        "assignment": {
            "method": "grandchild",
            "rho": float(args.rho),
            "seed": int(args.seed),
            "roster_size": c,
            "one_run_per_season": True,
        },
        "empirical_reference": {
            "panel": "Pass A hero spec (ppm z, min 20 min, poolq winsor 0.01–0.99)",
            "n_player_seasons": int(len(hero_work)),
            "n_drafted": int(hero_work["Y_draft"].sum()),
            "curvature": {
                "loo_pool_quality": curv_emp_loo,
                "pool_mean": curv_emp_mean,
            },
        },
        "sim_pooled": {
            "n_player_seasons": int(len(pooled)),
            "n_selected_total": n_selected_total,
            "season_runs": season_runs,
        },
        "selection": {
            "score_mode": sel_template.score_mode,
            "loo_pool_l_mode": sel_template.loo_pool_l_mode,
            "loo_gap_weight": float(sel_template.loo_gap_weight),
            "K_per_season": "empirical draft count each season",
            "theta_per_season": "PPM z quantile at 1 − K/N each season",
        },
        "curvature_sim": {
            "loo_pool_quality": curv_loo,
            "pool_mean": curv_mean,
        },
        "rho_sweep": sweep_meta if args.rho_sweep else None,
        "outputs": {
            "png": paths["png"].name,
            "png_rho_sweep": paths["png_sweep"].name if args.rho_sweep else None,
        },
    }
    paths["meta"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {paths['meta']}")
    print(
        f"Empirical LOO: {curv_emp_loo['shape']}  |  "
        f"Sim LOO: {curv_loo['shape']}  |  "
        f"Sim pool mean: {curv_mean['shape']}"
    )


if __name__ == "__main__":
    main()
