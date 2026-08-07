#!/usr/bin/env python3
"""PD17 — Empirical vs sim interval overlap (coverage) by \\rho.

Default layout: 1×3 side by side —
  (1) empirical NCAA rosters
  (2) sim four \\rho arms (538 Plot A — rho_low … rho_very_high)
  (3) sim eight-arm \\rho sweep 1→32 with hue ramp

Also writes sim-only sweep PNG for HAND swaps.

Run (repo root):
  python sports/scripts/empirical_rho_coverage_overlay.py
  python sports/scripts/empirical_rho_coverage_overlay.py --cmap Greens
  python sports/scripts/empirical_rho_coverage_overlay.py --two-panel

Outputs (HEROs_and_PASSes/empirical_pd17/):
  EMPIRICAL_rho_coverage_overlay.png              — 1×3 default (emp | 4-arm | sweep)
  EMPIRICAL_rho_coverage_sim_rho_1_32_sweep.png  — sim sweep only
  EMPIRICAL_rho_coverage_overlay_meta.json
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))

from gallery_knobs import (
    HERO_SEED,
    PRESET,
    RHO_HIGH,
    RHO_LOW,
    RHO_MODERATE,
    RHO_VERY_HIGH,
)
from hero_gallery_paths import EMPIRICAL_PD17, ensure_hero_dirs

OUT = EMPIRICAL_PD17
PNG = OUT / "EMPIRICAL_rho_coverage_overlay.png"
PNG_SIM_SWEEP = OUT / "EMPIRICAL_rho_coverage_sim_rho_1_32_sweep.png"
META_JSON = OUT / "EMPIRICAL_rho_coverage_overlay_meta.json"

SIM_RHO_SWEEP_1_32 = [float(x) for x in np.geomspace(1.0, 32.0, 8)]

LEGACY_RHO_ARMS: list[tuple[str, float]] = [
    ("rho_low", RHO_LOW),
    ("rho_moderate", RHO_MODERATE),
    ("rho_high", RHO_HIGH),
    ("rho_very_high", RHO_VERY_HIGH),
]
LEGACY_COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"]

SIM_GRID_POINTS = 81
EMP_GRID_POINTS = 400


def _load_tier1():
    for mod_name in list(sys.modules):
        if mod_name.startswith("tier1_"):
            del sys.modules[mod_name]
    sys.path.insert(0, str(SPORTS))
    sys.path.insert(0, str(REPO))
    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa

    return tge, tpa


def _coverage_curve(lo: np.ndarray, hi: np.ndarray, grid: np.ndarray) -> np.ndarray:
    cover = np.zeros(grid.size, dtype=int)
    for a, b in zip(lo, hi):
        cover += (grid >= a) & (grid <= b)
    return cover


def _empirical_coverage() -> tuple[np.ndarray, np.ndarray, np.ndarray, dict]:
    from empirical_team_interval_overlap import (
        _disjoint_benchmark,
        _prepare_panel,
        _team_intervals,
    )

    panel = _prepare_panel()
    iv, work = _team_intervals(panel)
    grid = np.linspace(iv["A_hat_min"].min(), iv["A_hat_max"].max(), EMP_GRID_POINTS)
    lo = iv["A_hat_min"].to_numpy(dtype=float)
    hi = iv["A_hat_max"].to_numpy(dtype=float)
    cover = _coverage_curve(lo, hi, grid)
    cover_disjoint, _, _ = _disjoint_benchmark(work, len(iv), grid)
    stats = {
        "coverage_max": int(cover.max()),
        "coverage_disjoint_max": int(cover_disjoint.max()),
        "coverage_frac_gt_1": float((cover > 1).mean()),
        "n_team_seasons": int(len(iv)),
    }
    return grid, cover, cover_disjoint, stats


def _539_state(mod, *, theta: float) -> dict:
    return {
        "ability_draw": str(getattr(mod, "SELECTION_539_ABILITY_DRAW", "beta_2_2")),
        "target_dist": "uniform",
        "t_low": float(getattr(mod, "SELECTION_539_TARGET_MEAN_LOW", 0.0)),
        "t_high": float(getattr(mod, "SELECTION_539_TARGET_MEAN_HIGH", 1.0)),
        "viability_theta": float(theta),
        "viability_sharpness": float(
            getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0)
        ),
        "n_bins": 16,
    }


def _sim_coverage_arm(
    tpa,
    *,
    params,
    ability: np.ndarray,
    team_targets: np.ndarray,
    rho: float,
    grid: np.ndarray,
) -> tuple[np.ndarray, int]:
    arm_params = replace(params, assignment_rho=float(rho))
    rng = np.random.default_rng(HERO_SEED + int(rho * 1000))
    players, _, _ = tpa.simulate_generative_rosters(
        arm_params,
        rng=rng,
        method="soft",
        ability=ability,
        team_targets=team_targets,
    )
    teams = tpa.roster_team_stats(players)
    lo = teams["min"].to_numpy(dtype=float)
    hi = teams["max"].to_numpy(dtype=float)
    cover = _coverage_curve(lo, hi, grid)
    return cover, int(cover.max())


def _sim_sort_chop_coverage(
    tpa,
    *,
    params,
    ability: np.ndarray,
    grid: np.ndarray,
) -> tuple[np.ndarray, int]:
    rng = np.random.default_rng(HERO_SEED + 999)
    pool_chop = tpa.assign_sort_chop_benchmark(
        rng,
        ability,
        params.n_teams,
        sorting_noise_sd=params.sorting_noise_sd,
    )
    team_targets = np.linspace(params.target_mean_low, params.target_mean_high, params.n_teams)
    players = tpa.build_roster_dataframe(ability, pool_chop, team_targets)
    teams = tpa.roster_team_stats(players)
    lo = teams["min"].to_numpy(dtype=float)
    hi = teams["max"].to_numpy(dtype=float)
    cover = _coverage_curve(lo, hi, grid)
    return cover, int(cover.max())


def _rho_sweep_colors(rhos: list[float], *, cmap_name: str) -> list:
    """Light → saturated hues as rho increases (1 → 32)."""
    cmap = colormaps[cmap_name]
    norm = Normalize(vmin=min(rhos), vmax=max(rhos))
    return [cmap(0.22 + 0.73 * norm(rho)) for rho in rhos]


def _plot_empirical_panel(ax, emp_grid, emp_cover, emp_disjoint) -> None:
    ax.fill_between(
        emp_grid, emp_cover, step="mid", alpha=0.35, color="steelblue", label="Actual rosters"
    )
    ax.plot(
        emp_grid,
        emp_disjoint,
        color="crimson",
        lw=1.5,
        ls="--",
        label="Sort-and-chop benchmark",
    )
    ax.axhline(1, color="gray", ls=":", lw=1)
    ax.set_xlabel(r"Player $\hat{A}_i$ (PPM $z$ within season)", fontsize=10)
    ax.set_ylabel("Team-seasons covering level", fontsize=10)
    ax.set_title("Empirical MBB (2011–2021)", fontsize=11, pad=8)
    ax.legend(fontsize=7, loc="upper right")
    ax.text(
        0.02,
        0.98,
        rf"max coverage = {emp_cover.max():,}",
        transform=ax.transAxes,
        va="top",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )


def _plot_sim_panel(
    ax,
    sim_grid: np.ndarray,
    curves: list[tuple[float, np.ndarray, int]],
    chop_cov: np.ndarray,
    chop_peak: int,
    *,
    cmap_name: str,
    title_suffix: str,
) -> None:
    rhos = [c[0] for c in curves]
    colors = _rho_sweep_colors(rhos, cmap_name=cmap_name)

    for (rho, cov, peak), color in zip(curves, colors):
        ax.plot(sim_grid, cov, lw=1.7, color=color, alpha=0.92)

    ax.plot(
        sim_grid,
        chop_cov,
        color="crimson",
        lw=1.5,
        ls="--",
        label=f"Sort-and-chop (peak={chop_peak})",
        zorder=1,
    )
    ax.axhline(1, color="gray", ls=":", lw=1, zorder=0)
    ax.set_xlabel(r"Player $A_i$ (539 ability on [0,1])", fontsize=10)
    ax.set_ylabel("Teams covering level", fontsize=10)
    ax.set_title(rf"Sim — $\rho$ sweep 1$\to$32 ({PRESET})", fontsize=10, pad=8)

    norm = Normalize(vmin=min(rhos), vmax=max(rhos))
    sm = ScalarMappable(cmap=colormaps[cmap_name], norm=norm)
    sm.set_array([])
    cbar = ax.figure.colorbar(sm, ax=ax, shrink=0.82, pad=0.02)
    cbar.set_label(r"$\rho$", fontsize=9)
    cbar.ax.tick_params(labelsize=7)

    rho_lo, peak_lo = curves[0][0], curves[0][2]
    rho_hi, peak_hi = curves[-1][0], curves[-1][2]
    ax.text(
        0.98,
        0.98,
        rf"$\rho={rho_lo:.2g}$: peak {peak_lo}" + "\n" + rf"$\rho={rho_hi:.2g}$: peak {peak_hi}",
        transform=ax.transAxes,
        va="top",
        ha="right",
        fontsize=7,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )


def _plot_sim_panel_legacy(
    ax,
    sim_grid: np.ndarray,
    sim_curves: list[tuple[str, float, np.ndarray, int]],
    chop_cov: np.ndarray,
    chop_peak: int,
) -> None:
    for i, (_label, rho, cov, peak) in enumerate(sim_curves):
        rho_lbl = rf"$\rho={rho:g}$" if rho >= 0.01 else r"$\rho \approx 0$"
        ax.plot(
            sim_grid,
            cov,
            lw=1.8,
            color=LEGACY_COLORS[i % len(LEGACY_COLORS)],
            label=f"{rho_lbl} (peak={peak})",
        )
    ax.plot(
        sim_grid,
        chop_cov,
        color="crimson",
        lw=1.5,
        ls="--",
        label=f"Sort-and-chop (peak={chop_peak})",
    )
    ax.axhline(1, color="gray", ls=":", lw=1)
    ax.set_xlabel(r"Player $A_i$ (539 ability on [0,1])", fontsize=10)
    ax.set_ylabel("Teams covering level", fontsize=10)
    ax.set_title(rf"Sim — four $\rho$ arms (538 Plot A)", fontsize=10, pad=8)
    ax.legend(fontsize=5.5, loc="upper right")


def main() -> None:
    parser = argparse.ArgumentParser(description="Empirical vs sim rho coverage overlay")
    parser.add_argument(
        "--cmap",
        default="Oranges",
        choices=("Oranges", "Greens", "YlOrRd", "YlGn"),
        help="Hue ramp for rho=1→32 sweep (default: Oranges)",
    )
    parser.add_argument(
        "--two-panel",
        action="store_true",
        help="Old 1×2 layout: empirical | rho sweep only (no middle four-arm panel)",
    )
    args = parser.parse_args()

    ensure_hero_dirs()

    emp_grid, emp_cover, emp_disjoint, emp_stats = _empirical_coverage()

    mod_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    tge, tpa = _load_tier1()
    theta = float(getattr(mod, "SELECTION_539_VIABILITY_THETA", 0.72))
    state = _539_state(mod, theta=theta)
    params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)

    rng = np.random.default_rng(HERO_SEED)
    ability = tpa.draw_abilities(
        rng,
        params.n_individuals,
        ability_draw=params.ability_draw,
        ability_mean=params.ability_mean,
        ability_sd=params.ability_sd,
        ability_clip_low=params.ability_clip_low,
        ability_clip_high=params.ability_clip_high,
        ability_student_t_df=params.ability_student_t_df,
        ability_student_t_scale=params.ability_student_t_scale,
    )
    team_targets = tpa.draw_target_means(
        rng,
        params.n_teams,
        target_mean_dist=params.target_mean_dist,
        target_mean_low=params.target_mean_low,
        target_mean_high=params.target_mean_high,
        target_mean_mu=params.target_mean_mu,
        target_mean_sigma=params.target_mean_sigma,
    )

    sim_grid = np.linspace(0.0, 1.0, SIM_GRID_POINTS)
    chop_cov, chop_peak = _sim_sort_chop_coverage(
        tpa, params=params, ability=ability, grid=sim_grid
    )

    legacy_meta: list[dict] = []
    sweep_meta: list[dict] = []
    legacy_curves: list[tuple[str, float, np.ndarray, int]] = []
    sweep_curves: list[tuple[float, np.ndarray, int]] = []

    for label, rho in LEGACY_RHO_ARMS:
        cov, peak = _sim_coverage_arm(
            tpa,
            params=params,
            ability=ability,
            team_targets=team_targets,
            rho=rho,
            grid=sim_grid,
        )
        legacy_curves.append((label, rho, cov, peak))
        legacy_meta.append({"arm": label, "rho": rho, "coverage_peak": peak})
        print(f"Sim {label} rho={rho:g} coverage_peak={peak}")

    for rho in SIM_RHO_SWEEP_1_32:
        cov, peak = _sim_coverage_arm(
            tpa,
            params=params,
            ability=ability,
            team_targets=team_targets,
            rho=rho,
            grid=sim_grid,
        )
        sweep_curves.append((rho, cov, peak))
        sweep_meta.append({"rho": rho, "coverage_peak": peak})
        print(f"Sim sweep rho={rho:.4g} coverage_peak={peak}")

    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()

    # --- Sim-only sweep PNG ---
    fig_sim, ax_sim = plt.subplots(figsize=(6.2, 4.9))
    _plot_sim_panel(
        ax_sim,
        sim_grid,
        sweep_curves,
        chop_cov,
        chop_peak,
        cmap_name=args.cmap,
        title_suffix="",
    )
    fig_sim.tight_layout()
    fig_sim.savefig(PNG_SIM_SWEEP, dpi=150, bbox_inches="tight")
    plt.close(fig_sim)
    print(f"Wrote {PNG_SIM_SWEEP}")

    # --- Full overlay ---
    if args.two_panel:
        fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.0))
        _plot_empirical_panel(axes[0], emp_grid, emp_cover, emp_disjoint)
        _plot_sim_panel(
            axes[1],
            sim_grid,
            sweep_curves,
            chop_cov,
            chop_peak,
            cmap_name=args.cmap,
            title_suffix="",
        )
        suptitle = (
            r"Interval overlap: empirical target vs sim $\rho$ sweep "
            r"($\rho=1\to32$, hue ramp)"
        )
        fig.subplots_adjust(left=0.07, right=0.96, top=0.86, bottom=0.14, wspace=0.28)
    else:
        fig, axes = plt.subplots(1, 3, figsize=(17.5, 5.0))
        _plot_empirical_panel(axes[0], emp_grid, emp_cover, emp_disjoint)
        _plot_sim_panel_legacy(axes[1], sim_grid, legacy_curves, chop_cov, chop_peak)
        _plot_sim_panel(
            axes[2],
            sim_grid,
            sweep_curves,
            chop_cov,
            chop_peak,
            cmap_name=args.cmap,
            title_suffix="",
        )
        axes[1].sharey(axes[2])
        axes[2].set_ylabel("")
        suptitle = (
            r"Interval overlap: empirical target vs sim $\rho$ "
            r"(four arms + 1$\to$32 sweep)"
        )
        fig.subplots_adjust(left=0.06, right=0.98, top=0.86, bottom=0.14, wspace=0.32)

    fig.suptitle(suptitle, fontsize=12, y=1.02)
    fig.text(
        0.5,
        0.01,
        "Axes not overlaid — PPM z (empirical) vs [0,1] ability (sim). Compare coverage peak and shape.",
        ha="center",
        fontsize=8,
        color="0.35",
    )
    fig.savefig(PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG}")

    meta = {
        "diagnostic": "empirical_rho_coverage_overlay",
        "date": date.today().isoformat(),
        "preset": PRESET,
        "seed": HERO_SEED,
        "empirical": emp_stats,
        "sim_sort_chop_peak": chop_peak,
        "sim_panel_mode": "two_panel" if args.two_panel else "three_panel",
        "sim_legacy_arms": legacy_meta,
        "sim_sweep_arms": sweep_meta,
        "sim_rho_sweep": SIM_RHO_SWEEP_1_32,
        "sim_cmap": args.cmap,
        "outputs": {
            "png": PNG.name,
            "png_sim_sweep": PNG_SIM_SWEEP.name,
        },
    }
    META_JSON.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {META_JSON}")
    print("Done.")


if __name__ == "__main__":
    main()
