#!/usr/bin/env python3
"""Empirical vs Grandchild sim — team L_C distribution (2011–2021).

Apples-to-apples:
  - Same panel filters as PD17 empirical L_C (Pass A hero spec)
  - Same formula: team smooth L_C = mean_j σ(γ(Â_j − θ))
  - Empirical: real NCAA rosters
  - Sim: one Grandchild assign per season, stacked team-seasons

Run (repo root):
  python sports/scripts/grandchild_empirical_lc_compare.py
  python sports/scripts/grandchild_empirical_lc_compare.py --rho 0.5 --gamma 0.5

Outputs (HEROs_and_PASSes/grandchild_assign/):
  GRANDCHILD_empirical_lc_compare_2011_2021.png              — side-by-side (counts)
  GRANDCHILD_empirical_lc_compare_normalized_2011_2021.png — side-by-side (density)
  GRANDCHILD_empirical_lc_overlay_2011_2021.png             — overlay (density)
  GRANDCHILD_empirical_lc_compare_2011_2021_meta.json
  GRANDCHILD_league_L_C_team_season_2011_2021.csv  — sim team table
"""

from __future__ import annotations

import argparse
import importlib
import importlib.util
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
from interval_overlap_paths import seasons_label, window_tag

FULL_PANEL_SEASON_MIN = 2011
FULL_PANEL_SEASON_MAX = 2021
OUT = GRANDCHILD_ASSIGN

N_LC_BINS = 48
LC_TICKS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
EMP_COLOR = "steelblue"
SIM_COLOR = "darkorange"
DEFAULT_RHO = 0.5
DEFAULT_GAMMA = 0.5
DEFAULT_SEED = 5412015


def _output_paths(season_min: int, season_max: int) -> dict:
    tag = window_tag(season_min, season_max) if season_min != season_max else str(season_min)
    stem = f"GRANDCHILD_empirical_lc_compare_{tag}"
    return {
        "png_side": OUT / f"{stem}.png",
        "png_side_normalized": OUT / f"{stem}_normalized.png",
        "png_overlay": OUT / f"GRANDCHILD_empirical_lc_overlay_{tag}.png",
        "meta": OUT / f"{stem}_meta.json",
        "sim_csv": OUT / f"GRANDCHILD_league_L_C_team_season_{tag}.csv",
        "seasons": seasons_label(season_min, season_max),
    }


def _load_gamma_default() -> float:
    mod_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return float(getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0))


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


def _hero_panel(season_min: int, season_max: int) -> pd.DataFrame:
    import empirical_lc_distributions as elc

    panel = elc._prepare_panel()
    return panel.loc[(panel["season"] >= season_min) & (panel["season"] <= season_max)].copy()


def _empirical_team_lc(panel: pd.DataFrame, *, theta: float, gamma: float) -> pd.DataFrame:
    import empirical_lc_distributions as elc

    return elc._attach_team_lc(panel, theta=theta, gamma=gamma)


def _teams_from_grandchild(
    ability: np.ndarray,
    pool_id: np.ndarray,
    *,
    season: int,
    theta: float,
    gamma: float,
) -> pd.DataFrame:
    import tier1_pool_assignment as tpa

    lc_col = tpa.POOL_L_CROWDING_SMOOTH_TEAM_COL
    players = pd.DataFrame({"ability": ability, "pool_id": pool_id.astype(np.int64)})
    players = tpa.add_team_pool_columns(
        players,
        viability_theta=float(theta),
        viability_sharpness=float(gamma),
    )
    team_df = (
        players.groupby("pool_id", observed=True)
        .agg(
            T_j_hat=("ability", "mean"),
            A_hat_min=("ability", "min"),
            A_hat_max=("ability", "max"),
            L_C=(lc_col, "first"),
            roster_n=("ability", "size"),
        )
        .reset_index()
        .rename(columns={"pool_id": "team_id"})
    )
    team_df["season"] = int(season)
    team_df["perf_span"] = team_df["A_hat_max"] - team_df["A_hat_min"]
    return team_df


def _sim_team_lc_panel(
    *,
    season_min: int,
    season_max: int,
    rho: float,
    seed: int,
    theta: float,
    gamma: float,
    gc,
) -> tuple[pd.DataFrame, list[dict]]:
    c = int(gc.ROSTER_SIZE_DEFAULT)
    seasons = list(range(int(season_min), int(season_max) + 1))
    parts: list[pd.DataFrame] = []
    season_runs: list[dict] = []
    for season in seasons:
        ability, emp_meta = gc.load_empirical_abilities_season(int(season), roster_size=c)
        rng = np.random.default_rng(int(seed) + int(season))
        res = gc.run_one_realization(ability, c, float(rho), rng=rng, seed=int(seed) + int(season))
        team_df = _teams_from_grandchild(
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
                **{k: emp_meta.get(k) for k in ("n_players_raw", "n_teams_grandchild")},
            }
        )
        print(f"  season {season}: J={len(team_df)} teams  H_sort={res.sorting_index_h:.3f}")
    return pd.concat(parts, ignore_index=True), season_runs


def _histogram(lc: np.ndarray, *, density: bool = False) -> tuple[np.ndarray, np.ndarray]:
    lc_edges = np.linspace(0.0, 1.0, N_LC_BINS + 1)
    centers = 0.5 * (lc_edges[:-1] + lc_edges[1:])
    counts, _ = np.histogram(lc, bins=lc_edges, density=density)
    return centers, counts


def _plot_side_by_side(
    emp_lc: np.ndarray,
    sim_lc: np.ndarray,
    *,
    paths: dict,
    rho: float,
    theta: float,
    gamma: float,
    k_over_n: float,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    lc_edges = np.linspace(0.0, 1.0, N_LC_BINS + 1)
    centers = 0.5 * (lc_edges[:-1] + lc_edges[1:])
    bin_width = lc_edges[1] - lc_edges[0]
    emp_counts, _ = np.histogram(emp_lc, bins=lc_edges)
    sim_counts, _ = np.histogram(sim_lc, bins=lc_edges)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.5), sharey=True)

    for ax, counts, lc, color, label, n_units in zip(
        axes,
        (emp_counts, sim_counts),
        (emp_lc, sim_lc),
        (EMP_COLOR, SIM_COLOR),
        ("Empirical NCAA (real rosters)", rf"Grandchild sim ($\rho={rho:g}$)"),
        (emp_lc.size, sim_lc.size),
        strict=True,
    ):
        ax.bar(
            centers,
            counts,
            width=bin_width * 0.98,
            align="center",
            color=color,
            alpha=0.85,
            edgecolor=color,
            linewidth=0.3,
            label=label,
        )
        ax.set_xlim(0.0, 1.0)
        ax.set_xticks(LC_TICKS)
        ax.set_xlabel(r"$L_C$", fontsize=11)
        ax.set_ylabel("Team-seasons", fontsize=10)
        stats = _summary("", lc)
        ax.set_title(
            rf"{label.split('(')[0].strip()} ($n={n_units:,}$)",
            fontsize=10,
        )
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        ax.text(
            0.97,
            0.97,
            rf"mean={stats['mean']:.3f}, sd={stats['std']:.3f}",
            transform=ax.transAxes,
            va="top",
            ha="right",
            fontsize=8,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
        )

    fig.suptitle(
        rf"Team smooth $L_C$ — empirical vs Grandchild (MBB {paths['seasons']}, "
        rf"$\gamma={gamma:g}$, $\theta={theta:.3f}$ z, $K/N={k_over_n:.4f}$)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(paths["png_side"], dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {paths['png_side']}")


def _plot_side_by_side_normalized(
    emp_lc: np.ndarray,
    sim_lc: np.ndarray,
    *,
    paths: dict,
    rho: float,
    theta: float,
    gamma: float,
    k_over_n: float,
) -> None:
    """Side-by-side density histograms — shape comparison without count-scale distortion."""
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    lc_edges = np.linspace(0.0, 1.0, N_LC_BINS + 1)
    centers = 0.5 * (lc_edges[:-1] + lc_edges[1:])
    bin_width = lc_edges[1] - lc_edges[0]
    emp_density, _ = np.histogram(emp_lc, bins=lc_edges, density=True)
    sim_density, _ = np.histogram(sim_lc, bins=lc_edges, density=True)

    fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.5), sharey=True)

    for ax, density, lc, color, label, n_units in zip(
        axes,
        (emp_density, sim_density),
        (emp_lc, sim_lc),
        (EMP_COLOR, SIM_COLOR),
        ("Empirical NCAA (real rosters)", rf"Grandchild sim ($\rho={rho:g}$)"),
        (emp_lc.size, sim_lc.size),
        strict=True,
    ):
        ax.bar(
            centers,
            density,
            width=bin_width * 0.98,
            align="center",
            color=color,
            alpha=0.85,
            edgecolor=color,
            linewidth=0.3,
            label=label,
        )
        ax.set_xlim(0.0, 1.0)
        ax.set_xticks(LC_TICKS)
        ax.set_xlabel(r"$L_C$", fontsize=11)
        ax.set_ylabel("Density", fontsize=10)
        stats = _summary("", lc)
        ax.set_title(
            rf"{label.split('(')[0].strip()} ($n={n_units:,}$)",
            fontsize=10,
        )
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        ax.text(
            0.97,
            0.97,
            rf"mean={stats['mean']:.3f}, sd={stats['std']:.3f}",
            transform=ax.transAxes,
            va="top",
            ha="right",
            fontsize=8,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
        )

    fig.suptitle(
        rf"Team smooth $L_C$ — normalized compare (MBB {paths['seasons']}, "
        rf"$\gamma={gamma:g}$, $\theta={theta:.3f}$ z, $K/N={k_over_n:.4f}$)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    fig.savefig(paths["png_side_normalized"], dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {paths['png_side_normalized']}")


def _plot_overlay(
    emp_lc: np.ndarray,
    sim_lc: np.ndarray,
    *,
    paths: dict,
    rho: float,
    theta: float,
    gamma: float,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    x_emp, y_emp = _histogram(emp_lc, density=True)
    x_sim, y_sim = _histogram(sim_lc, density=True)

    fig, ax = plt.subplots(figsize=(8.0, 4.5))
    ax.plot(x_emp, y_emp, color=EMP_COLOR, lw=2.0, label=f"Empirical (n={emp_lc.size:,})")
    ax.fill_between(x_emp, 0, y_emp, alpha=0.15, color=EMP_COLOR)
    ax.plot(
        x_sim,
        y_sim,
        color=SIM_COLOR,
        lw=2.0,
        label=rf"Grandchild sim $\rho={rho:g}$ (n={sim_lc.size:,})",
    )
    ax.fill_between(x_sim, 0, y_sim, alpha=0.12, color=SIM_COLOR)
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(LC_TICKS)
    ax.set_xlabel(r"$L_C$", fontsize=11)
    ax.set_ylabel("Density", fontsize=10)
    ax.set_title(
        rf"Team $L_C$ density overlay — MBB {paths['seasons']} ($\gamma={gamma:g}$)",
        fontsize=11,
    )
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    fig.tight_layout()
    fig.savefig(paths["png_overlay"], dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {paths['png_overlay']}")


def _resolve_season_window(args) -> tuple[int, int]:
    if args.season is not None:
        return int(args.season), int(args.season)
    if args.season_min is not None or args.season_max is not None:
        if args.season_min is None or args.season_max is None:
            raise SystemExit("--season-min and --season-max must be supplied together")
        return int(args.season_min), int(args.season_max)
    return FULL_PANEL_SEASON_MIN, FULL_PANEL_SEASON_MAX


def main() -> None:
    parser = argparse.ArgumentParser(description="Empirical vs Grandchild team L_C compare")
    parser.add_argument("--rho", type=float, default=DEFAULT_RHO)
    parser.add_argument("--gamma", type=float, default=None)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--season", type=int, default=None)
    parser.add_argument("--season-min", type=int, default=None)
    parser.add_argument("--season-max", type=int, default=None)
    args = parser.parse_args()

    season_min, season_max = _resolve_season_window(args)
    paths = _output_paths(season_min, season_max)
    ensure_hero_dirs()

    gamma_default = _load_gamma_default()
    gamma = float(args.gamma) if args.gamma is not None else DEFAULT_GAMMA
    gamma_source = (
        f"CLI --gamma {gamma:g}"
        if args.gamma is not None
        else f"HAND17 default ({DEFAULT_GAMMA:g}); tier1 default is {gamma_default:g}"
    )

    print(f"Loading empirical panel {paths['seasons']} ...")
    panel = _hero_panel(season_min, season_max)
    panel = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    ability = panel["perf"].to_numpy(dtype=float)
    n_drafted = int(panel["Y_draft"].sum())
    n_total = int(len(panel))
    k_over_n = n_drafted / n_total if n_total else float("nan")
    theta = float(np.quantile(ability, 1.0 - k_over_n))

    emp_team = _empirical_team_lc(panel, theta=theta, gamma=gamma)
    emp_lc = emp_team["L_C"].dropna().to_numpy(dtype=float)
    print(f"Empirical: {emp_lc.size:,} team-seasons  L_C mean={emp_lc.mean():.3f}")

    gc = importlib.import_module("541_grandchild_homophily_assign")
    print(f"Running Grandchild assign (ρ={args.rho:g}) ...")
    sim_team, season_runs = _sim_team_lc_panel(
        season_min=season_min,
        season_max=season_max,
        rho=float(args.rho),
        seed=int(args.seed),
        theta=theta,
        gamma=gamma,
        gc=gc,
    )
    sim_team.to_csv(paths["sim_csv"], index=False)
    print(f"Wrote {paths['sim_csv']}")
    sim_lc = sim_team["L_C"].dropna().to_numpy(dtype=float)
    print(f"Sim: {sim_lc.size:,} team-seasons  L_C mean={sim_lc.mean():.3f}")

    _plot_side_by_side(
        emp_lc,
        sim_lc,
        paths=paths,
        rho=float(args.rho),
        theta=theta,
        gamma=gamma,
        k_over_n=k_over_n,
    )
    _plot_side_by_side_normalized(
        emp_lc,
        sim_lc,
        paths=paths,
        rho=float(args.rho),
        theta=theta,
        gamma=gamma,
        k_over_n=k_over_n,
    )
    _plot_overlay(
        emp_lc,
        sim_lc,
        paths=paths,
        rho=float(args.rho),
        theta=theta,
        gamma=gamma,
    )

    meta = {
        "diagnostic": "grandchild_empirical_lc_compare",
        "date": date.today().isoformat(),
        "season_min": season_min,
        "season_max": season_max,
        "seasons": paths["seasons"],
        "lc_mode": "crowding_smooth_team",
        "theta": theta,
        "gamma": gamma,
        "gamma_source": gamma_source,
        "theta_K_over_N": {
            "n_accepted": n_drafted,
            "n_total": n_total,
            "K_over_N": k_over_n,
            "theta_quantile": 1.0 - k_over_n,
        },
        "empirical": {
            "n_team_seasons": int(emp_lc.size),
            "L_C": _summary("L_C", emp_lc),
            "T_j_hat": _summary(r"\hat{T}_j", emp_team["T_j_hat"].to_numpy(dtype=float)),
        },
        "sim": {
            "method": "grandchild",
            "rho": float(args.rho),
            "seed": int(args.seed),
            "n_team_seasons": int(sim_lc.size),
            "L_C": _summary("L_C", sim_lc),
            "T_j_hat": _summary(r"\hat{T}_j", sim_team["T_j_hat"].to_numpy(dtype=float)),
            "season_runs": season_runs,
        },
        "outputs": {
            "png_side_by_side": paths["png_side"].name,
            "png_side_by_side_normalized": paths["png_side_normalized"].name,
            "png_overlay": paths["png_overlay"].name,
            "sim_team_csv": paths["sim_csv"].name,
        },
    }
    paths["meta"].write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {paths['meta']}")
    print("Done.")


if __name__ == "__main__":
    main()
