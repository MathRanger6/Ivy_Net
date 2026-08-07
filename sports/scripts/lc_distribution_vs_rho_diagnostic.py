#!/usr/bin/env python3
"""PD16 Sketch A — distribution of team L_C vs assignment assortativity ρ.

Alex whiteboard (Paper Directions 16, Aug 2026):
  ρ dials the *spread* of team-level congestion across the league — not only
  "the selection curve bends."

This script does NOT run score/select. It only:
  (1) ASSIGN rosters at fixed A_i / T_{j*} under different soft-ρ arms
  (2) Compute **team smooth L_C** = mean_j σ(γ(A_k − θ)) on each roster
  (3) Plot how that team-L_C distribution changes with ρ

Outputs (under pass_c_rho/):
  LC_distribution_vs_rho_1d_strip{SUFFIX}.png — four narrow panels (slide-ready)
  LC_distribution_vs_rho_2d{SUFFIX}.png         — heatmap: realized T_j vs L_C
  LC_distribution_vs_rho_teams{SUFFIX}.csv     — one row per team × ρ arm
  LC_distribution_vs_rho_meta{SUFFIX}.json      — summary stats

Run (repo root):
  python sports/scripts/lc_distribution_vs_rho_diagnostic.py

PD16 defaults (team L_C + naive-draft θ) — same as --pd16 slides:
  export GALLERY_LC_MODE=team_smooth
  export GALLERY_THETA_MODE=k_over_n
  export GALLERY_OUTPUT_SUFFIX=_pd16

See: re_entry/08_PD16_Alex_meeting_takeaways.md (Whiteboard A)
"""

from __future__ import annotations

import json
import os
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
sys.path.insert(0, str(SCRIPTS))

from gallery_knobs import (
    HERO_N_TEAMS,
    HERO_ROSTER_SIZE,
    HERO_SEED,
    OUTPUT_SUFFIX,
    PRESET,
    RHO_HIGH,
    RHO_LOW,
    RHO_MODERATE,
    RHO_VERY_HIGH,
    THETA_MODE,
    gallery_mode_subtitle,
    resolve_viability_theta,
)
from hero_gallery_paths import PASS_C_RHO, ensure_hero_dirs

OUT = PASS_C_RHO
SUFFIX = OUTPUT_SUFFIX
PNG_1D_STRIP = OUT / f"LC_distribution_vs_rho_1d_strip{SUFFIX}.png"
PNG_2D = OUT / f"LC_distribution_vs_rho_2d{SUFFIX}.png"
CSV_TEAMS = OUT / f"LC_distribution_vs_rho_teams{SUFFIX}.csv"
META_JSON = OUT / f"LC_distribution_vs_rho_meta{SUFFIX}.json"

SOFT_ARMS: list[tuple[str, float]] = [
    ("rho_low", RHO_LOW),
    ("rho_moderate", RHO_MODERATE),
    ("rho_high", RHO_HIGH),
    ("rho_very_high", RHO_VERY_HIGH),
]

LC_COL = "pool_c_smooth_team"
N_LC_BINS = int(os.environ.get("GALLERY_LC_BINS", "48"))
N_2D_LC_BINS = 20
N_2D_A_BINS = 20

X_LABEL = r"$L_C$"
X_TICKS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
Y_LABEL_2D = r"$T_j$ (realized team talent)"

SINGLE_RHO_PANEL_W = 2.35
SINGLE_RHO_PANEL_H = 7.0
BAR_COLOR = "steelblue"
BAR_ALPHA = 0.85
SINGLE_RHO_X_TICKS = [0.0, 0.5, 1.0]


def _style_single_rho_axes(ax, *, show_ylabel: bool = True) -> None:
    """Compact axes for narrow slide panels."""
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(SINGLE_RHO_X_TICKS)
    ax.tick_params(axis="x", labelbottom=True, labelsize=7)
    ax.tick_params(axis="y", labelsize=7)
    ax.set_xlabel(X_LABEL, fontsize=9)
    if show_ylabel:
        ax.set_ylabel("Teams", fontsize=8)


def _style_lc_x_axis(ax) -> None:
    """Tick numbers + explicit L_C x-axis label on every panel."""
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(X_TICKS)
    ax.tick_params(axis="x", labelbottom=True, labelsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_xlabel(X_LABEL, fontsize=13)


def _load_modules():
    for mod_name in list(sys.modules):
        if mod_name.startswith("tier1_"):
            del sys.modules[mod_name]
    sys.path.insert(0, str(SPORTS))
    sys.path.insert(0, str(REPO))
    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa

    return tge, tpa


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
        "n_teams": HERO_N_TEAMS,
        "roster_size": HERO_ROSTER_SIZE,
        "winner_selection": str(getattr(mod, "SELECTION_539_WINNER_SELECTION", "C")),
    }


def team_lc_table(players: pd.DataFrame, tpa) -> pd.DataFrame:
    """One row per team: L_C (team smooth), realized T_j, assignment target T_j_star."""
    teams = tpa.roster_team_stats(players)
    lc_by_pool = (
        players.groupby("pool_id", observed=True)[LC_COL]
        .first()
        .rename("team_L_C")
    )
    out = teams.merge(lc_by_pool, on="pool_id", how="left")
    out = out.rename(columns={"pool_mean": "T_j", "team_target": "T_j_star"})
    return out


def run_arm(
    label: str,
    rho: float,
    *,
    params,
    ability,
    team_targets,
    tpa,
    theta: float,
    gamma: float,
) -> pd.DataFrame:
    """Assign at fixed ρ; attach team L_C; return team-level table."""
    arm_params = replace(params, assignment_rho=float(rho))
    rng = np.random.default_rng(HERO_SEED + int(rho * 1000) + len(label))
    players, _, _ = tpa.simulate_generative_rosters(
        arm_params,
        rng=rng,
        method="soft",
        ability=ability,
        team_targets=team_targets,
    )
    players = tpa.add_team_pool_columns(
        players,
        viability_theta=theta,
        viability_sharpness=gamma,
    )
    tbl = team_lc_table(players, tpa)
    tbl["arm"] = label
    tbl["rho"] = float(rho)
    return tbl


def _rho_panel_title(rho: float) -> str:
    rho_line = rf"$\rho={rho:g}$" if rho >= 0.01 else rf"$\rho \approx 0$"
    return rf"{rho_line}" + "\n" + rf"{N_LC_BINS} bins"


def build_1d_rho_strip(frames: dict[str, pd.DataFrame], *, theta: float) -> None:
    """One wide PNG — four narrow bar panels side by side, shared y-scale."""
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    lc_edges = np.linspace(0.0, 1.0, N_LC_BINS + 1)
    bin_width = lc_edges[1] - lc_edges[0]
    y_top = _global_ymax(frames, lc_edges)

    items = sorted(frames.items(), key=lambda kv: float(kv[1]["rho"].iloc[0]))
    n = len(items)
    fig_w = SINGLE_RHO_PANEL_W * n
    fig, axes = plt.subplots(
        1, n, figsize=(fig_w, SINGLE_RHO_PANEL_H), sharey=True, squeeze=False
    )
    axes = axes.ravel()

    for i, (ax, (label, df)) in enumerate(zip(axes, items)):
        rho = float(df["rho"].iloc[0])
        lc = df["team_L_C"].dropna().to_numpy()
        centers, counts = _histogram_curve(lc, bins=lc_edges)
        ax.bar(
            centers,
            counts,
            width=bin_width * 0.98,
            align="center",
            color=BAR_COLOR,
            alpha=BAR_ALPHA,
            edgecolor=BAR_COLOR,
            linewidth=0.3,
        )
        _style_single_rho_axes(ax, show_ylabel=(i == 0))
        ax.set_ylim(0.0, y_top)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        ax.set_title(_rho_panel_title(rho), fontsize=10, linespacing=1.15, pad=4)
        if i > 0:
            ax.tick_params(axis="y", labelleft=True)

    fig.subplots_adjust(left=0.06, right=0.99, top=0.92, bottom=0.10, wspace=0.12)
    fig.savefig(PNG_1D_STRIP, dpi=150, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(f"Wrote {PNG_1D_STRIP}")


def _global_ymax(frames: dict[str, pd.DataFrame], lc_edges: np.ndarray) -> float:
    ymax = 0.0
    for df in frames.values():
        lc = df["team_L_C"].dropna().to_numpy()
        _, counts = _histogram_curve(lc, bins=lc_edges)
        if counts.size:
            ymax = max(ymax, float(counts.max()))
    return ymax * 1.06 if ymax > 0 else 1.0


def _histogram_curve(lc: np.ndarray, *, bins: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    counts, edges = np.histogram(lc, bins=bins)
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers, counts.astype(float)


def build_2d_panels(frames: dict[str, pd.DataFrame], *, theta: float) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    items = sorted(frames.items(), key=lambda kv: float(kv[1]["rho"].iloc[0]))
    n = len(items)
    ncols = 2 if n <= 4 else 3
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(4.5 * ncols, 3.8 * nrows))
    axes = np.atleast_1d(axes).ravel()
    lc_edges = np.linspace(0.0, 1.0, N_2D_LC_BINS + 1)
    a_edges = np.linspace(0.0, 1.0, N_2D_A_BINS + 1)

    for ax, (label, df) in zip(axes, items):
        lc = df["team_L_C"].to_numpy(dtype=float)
        a = df["T_j"].to_numpy(dtype=float)
        mask = np.isfinite(lc) & np.isfinite(a)
        h, _, _, im = ax.hist2d(
            lc[mask],
            a[mask],
            bins=[lc_edges, a_edges],
            cmap="viridis",
        )
        rho = float(df["rho"].iloc[0])
        ax.set_title(rf"$\rho={rho:g}$", fontsize=10)
        _style_lc_x_axis(ax)
        ax.set_ylabel(Y_LABEL_2D, fontsize=10)
        ax.set_ylim(0.0, 1.0)
        ax.set_yticks(X_TICKS)
        fig.colorbar(im, ax=ax, label="Teams in bin", shrink=0.85)

    for ax in axes[len(items) :]:
        ax.set_visible(False)

    fig.suptitle(
        rf"Do better teams face more congestion?  (heatmap of team counts; "
        rf"{PRESET}, {HERO_N_TEAMS} teams)"
        "\n"
        + gallery_mode_subtitle(theta_value=theta),
        fontsize=11,
        y=1.03,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(PNG_2D, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG_2D}")


def summary_stats(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict] = []
    for label, df in frames.items():
        lc = df["team_L_C"].dropna()
        rows.append(
            {
                "arm": label,
                "rho": float(df["rho"].iloc[0]),
                "n_teams": int(lc.shape[0]),
                "L_C_mean": float(lc.mean()),
                "L_C_std": float(lc.std()),
                "L_C_min": float(lc.min()),
                "L_C_max": float(lc.max()),
                "frac_L_C_below_0.05": float((lc < 0.05).mean()),
                "frac_L_C_above_0.5": float((lc > 0.5).mean()),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    ensure_hero_dirs()
    mod_path = SPORTS / "tier1_sim_config.py"
    import importlib.util

    spec = importlib.util.spec_from_file_location("tier1_sim_config", mod_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)

    tge, tpa = _load_modules()
    preset_theta = float(getattr(mod, "SELECTION_539_VIABILITY_THETA", 0.72))
    ability_draw = str(getattr(mod, "SELECTION_539_ABILITY_DRAW", "beta_2_2"))
    theta = resolve_viability_theta(preset=preset_theta, ability_draw=ability_draw)
    gamma = float(getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0))

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

    frames: dict[str, pd.DataFrame] = {}
    for label, rho in SOFT_ARMS:
        print(f"Running {label} (ρ={rho:g}) ...")
        frames[label] = run_arm(
            label,
            rho,
            params=params,
            ability=ability,
            team_targets=team_targets,
            tpa=tpa,
            theta=theta,
            gamma=gamma,
        )

    all_teams = pd.concat(frames.values(), ignore_index=True)
    all_teams.to_csv(CSV_TEAMS, index=False)
    print(f"Wrote {CSV_TEAMS}")

    stats = summary_stats(frames)
    print("\nTeam L_C spread summary:")
    print(stats.to_string(index=False))

    build_1d_rho_strip(frames, theta=theta)
    build_2d_panels(frames, theta=theta)

    meta = {
        "diagnostic": "lc_distribution_vs_rho",
        "date": date.today().isoformat(),
        "preset": PRESET,
        "seed": HERO_SEED,
        "theta": theta,
        "theta_mode": THETA_MODE,
        "gamma": gamma,
        "lc_bins": N_LC_BINS,
        "lc_column": LC_COL,
        "arms": [{"label": a, "rho": r} for a, r in SOFT_ARMS],
        "outputs": {
            "png_1d_strip": str(PNG_1D_STRIP.name),
            "png_2d": str(PNG_2D.name),
            "csv": str(CSV_TEAMS.name),
        },
        "summary": stats.to_dict(orient="records"),
    }
    META_JSON.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {META_JSON}")
    print("Done.")


if __name__ == "__main__":
    main()
