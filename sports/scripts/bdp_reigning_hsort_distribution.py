#!/usr/bin/env python3
"""BDP — empirical H_sort distribution (reigning hero · all-ps).

H_sort = realized sorting index (variance explained by team assignment).
Distinct from interval-overlap geometry (team windows vs perf axis).

Run (repo root):
  python sports/scripts/bdp_reigning_hsort_distribution.py
"""

from __future__ import annotations

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

from bdp_ai_tj_distributions import BdpSpec, parse_bdp_spec, subtitle_lines
from gallery_mathtext import configure_matplotlib_mathtext
from hero_gallery_paths import REIGNING_HERO_BASIC_PLOTS, REIGNING_HERO_CALIBRATION_RHO, ensure_hero_dirs
from pd21_rho_hsort_calibrate import PanelPrepConfig, empirical_h_sort, prepare_calibration_panel

PREFIX = "REIGNING"
SIM_COLOR = "#d95f02"
# New BDP standard (Aug 2026): DFT overlay lines purple; individual=blue, team=orange elsewhere.
DFT_OVERLAY_COLOR = "#7b3299"
LOO_RESIDUAL_COLOR = "steelblue"
TEAM_RESIDUAL_COLOR = SIM_COLOR


def _season_hsort_table(panel: pd.DataFrame, season_min: int, season_max: int) -> pd.DataFrame:
    rows = []
    for season in range(int(season_min), int(season_max) + 1):
        sub = panel.loc[panel["season"] == season]
        rows.append(
            {
                "season": int(season),
                "h_sort_empirical": float(empirical_h_sort(sub)),
                "n_players": int(sub["perf"].notna().sum()),
            }
        )
    return pd.DataFrame(rows)


def _pooled_hsort(panel: pd.DataFrame) -> float:
    from empirical_team_interval_overlap import _compute_H_sort

    return float(_compute_H_sort(panel))


def _drafted_teams_in_panel(panel: pd.DataFrame) -> set:
    if "Y_draft" not in panel.columns:
        return set()
    y = pd.to_numeric(panel["Y_draft"], errors="coerce")
    return set(panel.loc[y == 1, "team_id"].dropna().unique())


def _ability_residual_vectors(
    panel: pd.DataFrame,
    *,
    team_ids: set | None = None,
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    """Pooled H_sort decomposition: team-mean vs grand-mean centered perf."""
    work = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    work["perf"] = pd.to_numeric(work["perf"], errors="coerce")
    work = work.dropna(subset=["perf"])
    if team_ids is not None:
        work = work.loc[work["team_id"].isin(team_ids)]
    if work.empty:
        return np.array([]), np.array([]), {"n": 0}
    mu_team = work.groupby(["team_id", "season"], observed=True)["perf"].transform("mean")
    a_bar = float(work["perf"].mean())
    r_team = (work["perf"] - mu_team).to_numpy(dtype=float)
    r_grand = (work["perf"] - a_bar).to_numpy(dtype=float)
    ss_team = float(np.sum(r_team**2))
    ss_grand = float(np.sum(r_grand**2))
    h_sort = 1.0 - ss_team / ss_grand if ss_grand > 0 else float("nan")
    return r_team, r_grand, {
        "n": int(len(work)),
        "A_bar": a_bar,
        "ss_team": ss_team,
        "ss_grand": ss_grand,
        "H_sort_pooled": h_sort,
        "std_team_residual": float(np.std(r_team, ddof=0)),
        "std_grand_residual": float(np.std(r_grand, ddof=0)),
    }


def _ability_loo_residual_vector(
    panel: pd.DataFrame,
    *,
    team_ids: set | None = None,
) -> tuple[np.ndarray, dict[str, float]]:
    """Ability minus player LOO pool quality: A_i - poolq_LOO,i."""
    work = panel.dropna(subset=["perf", "poolq_loo", "team_id", "season"]).copy()
    work["perf"] = pd.to_numeric(work["perf"], errors="coerce")
    work["poolq_loo"] = pd.to_numeric(work["poolq_loo"], errors="coerce")
    work = work.dropna(subset=["perf", "poolq_loo"])
    if team_ids is not None:
        work = work.loc[work["team_id"].isin(team_ids)]
    if work.empty:
        return np.array([]), {"n": 0}
    r_loo = (work["perf"] - work["poolq_loo"]).to_numpy(dtype=float)
    ss_loo = float(np.sum(r_loo**2))
    ss_grand = float(np.sum((work["perf"] - work["perf"].mean()) ** 2))
    return r_loo, {
        "n": int(len(work)),
        "ss_loo": ss_loo,
        "ss_grand": ss_grand,
        "frac_var_loo_residual": ss_loo / ss_grand if ss_grand > 0 else float("nan"),
        "std_loo_residual": float(np.std(r_loo, ddof=0)),
    }


def _ability_team_loo_residual_pair(
    panel: pd.DataFrame,
    *,
    team_ids: set | None = None,
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    """Same player-rows: A_i - T̂_j (team mean) and A_i - poolq_LOO,i."""
    work = panel.dropna(subset=["perf", "poolq_loo", "team_id", "season"]).copy()
    work["perf"] = pd.to_numeric(work["perf"], errors="coerce")
    work["poolq_loo"] = pd.to_numeric(work["poolq_loo"], errors="coerce")
    work = work.dropna(subset=["perf", "poolq_loo"])
    if team_ids is not None:
        work = work.loc[work["team_id"].isin(team_ids)]
    if work.empty:
        return np.array([]), np.array([]), {"n": 0}
    mu_team = work.groupby(["team_id", "season"], observed=True)["perf"].transform("mean")
    r_team = (work["perf"] - mu_team).to_numpy(dtype=float)
    r_loo = (work["perf"] - work["poolq_loo"]).to_numpy(dtype=float)
    corr = float(np.corrcoef(r_team, r_loo)[0, 1]) if len(r_team) > 1 else float("nan")
    return r_team, r_loo, {
        "n": int(len(work)),
        "std_team_residual": float(np.std(r_team, ddof=0)),
        "std_loo_residual": float(np.std(r_loo, ddof=0)),
        "corr_team_loo_residual": corr,
    }


def _tj_minus_loo_vector(
    panel: pd.DataFrame,
    *,
    team_ids: set | None = None,
) -> tuple[np.ndarray, dict[str, float]]:
    """Team mean minus player LOO: T̂_j - poolq_LOO,i (self-inclusion gap)."""
    work = panel.dropna(subset=["perf", "poolq_loo", "team_id", "season"]).copy()
    work["perf"] = pd.to_numeric(work["perf"], errors="coerce")
    work["poolq_loo"] = pd.to_numeric(work["poolq_loo"], errors="coerce")
    work = work.dropna(subset=["perf", "poolq_loo"])
    if team_ids is not None:
        work = work.loc[work["team_id"].isin(team_ids)]
    if work.empty:
        return np.array([]), {"n": 0}
    mu_team = work.groupby(["team_id", "season"], observed=True)["perf"].transform("mean")
    delta = (mu_team - work["poolq_loo"]).to_numpy(dtype=float)
    r_team = (work["perf"] - mu_team).to_numpy(dtype=float)
    r_loo = (work["perf"] - work["poolq_loo"]).to_numpy(dtype=float)
    a_bar = float(work["perf"].mean())
    ss_team = float(np.sum(r_team**2))
    ss_loo = float(np.sum(r_loo**2))
    ss_grand = float(np.sum((work["perf"] - a_bar) ** 2))
    corr = float(np.corrcoef(delta, r_team)[0, 1]) if len(delta) > 1 else float("nan")
    return delta, {
        "n": int(len(work)),
        "mean_tj_minus_loo": float(np.mean(delta)),
        "std_tj_minus_loo": float(np.std(delta, ddof=0)),
        "H_sort_team": 1.0 - ss_team / ss_grand if ss_grand > 0 else float("nan"),
        "H_sort_loo": 1.0 - ss_loo / ss_grand if ss_grand > 0 else float("nan"),
        "corr_tj_minus_loo_vs_ai_minus_tj": corr,
    }


def _plot_tj_minus_loo_distribution(
    delta: np.ndarray,
    stats: dict[str, float],
    *,
    spec: BdpSpec,
    png_path: Path,
    delta_dft: np.ndarray | None = None,
    stats_dft: dict[str, float] | None = None,
) -> None:
    from matplotlib.ticker import MultipleLocator
    from scipy.stats import gaussian_kde

    configure_matplotlib_mathtext()
    has_dft = stats_dft is not None and stats_dft.get("n", 0) > 0
    line1, line2 = subtitle_lines(spec, has_overlay=False)
    line2 += " · all-ps · min20 · mg10 · PPM z"
    if has_dft:
        line2 += " · purple line = +DFT"

    fig, ax = plt.subplots(1, 1, figsize=(7.2, 4.6))
    fig.subplots_adjust(top=0.70, bottom=0.16, left=0.11, right=0.96)

    pools = [delta]
    if delta_dft is not None and delta_dft.size:
        pools.append(delta_dft)
    lo = float(min(v.min() for v in pools if v.size))
    hi = float(max(v.max() for v in pools if v.size))
    pad = 0.05 * (hi - lo) if hi > lo else 0.5
    x_grid = np.linspace(lo - pad, hi + pad, 400)
    y_headroom = 1.12
    color = TEAM_RESIDUAL_COLOR

    density = gaussian_kde(delta)(x_grid)
    ymax = float(density.max())
    ax.fill_between(x_grid, 0.0, density, color=color, alpha=0.35, linewidth=0.0)
    ax.plot(
        x_grid,
        density,
        color=color,
        lw=2.0,
        label=rf"w/o DFT ($n={stats['n']:,}$, $\sigma={stats['std_tj_minus_loo']:.3f}$)",
    )
    if delta_dft is not None and delta_dft.size > 1 and stats_dft is not None:
        density_dft = gaussian_kde(delta_dft)(x_grid)
        ymax = max(ymax, float(density_dft.max()))
        ax.plot(
            x_grid,
            density_dft,
            color=DFT_OVERLAY_COLOR,
            lw=2.0,
            label=rf"+ DFT ($n={stats_dft['n']:,}$, $\sigma={stats_dft['std_tj_minus_loo']:.3f}$)",
        )
    ax.axvline(0.0, color="0.35", linestyle=":", linewidth=1.0)
    ax.set_xlim(x_grid[0], x_grid[-1])
    ax.set_xlabel(r"$\hat{T}_j - \mathrm{poolq}^{\mathrm{LOO}}_i$  (PPM $z$)")
    ax.set_ylabel("Density")
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=6.5, loc="upper right", framealpha=0.95)

    tick_step = 0.5 if ymax * y_headroom > 1.0 else (0.1 if ymax * y_headroom > 0.5 else 0.05)
    y_top = float(np.ceil(ymax * y_headroom / tick_step) * tick_step)
    ax.set_ylim(0.0, y_top)
    ax.yaxis.set_major_locator(MultipleLocator(tick_step))

    h_team = stats["H_sort_team"]
    h_loo = stats["H_sort_loo"]
    corr = stats.get("corr_tj_minus_loo_vs_ai_minus_tj", float("nan"))
    fig.text(
        0.5,
        0.985,
        rf"Self-inclusion gap · $H_{{\mathrm{{sort}}}}^{{\mathrm{{team}}}}={h_team:.3f}$ · "
        rf"$H_{{\mathrm{{sort}}}}^{{\mathrm{{LOO}}}}={h_loo:.3f}$ · "
        rf"$\mathrm{{corr}}(\hat{{T}}_j-\mathrm{{LOO}},\,A_i-\hat{{T}}_j)={corr:.3f}$",
        ha="center",
        va="top",
        fontsize=10,
    )
    fig.text(0.5, 0.915, line1, ha="center", va="top", fontsize=9)
    fig.text(
        0.5,
        0.885,
        r"Links $A_i-\hat{T}_j$ and $A_i-\mathrm{poolq}^{\mathrm{LOO}}_i$; "
        r"$H_{\mathrm{sort}}^{\mathrm{LOO}}$ uses LOO residuals in the $H_{\mathrm{sort}}$ ratio",
        ha="center",
        va="top",
        fontsize=8.5,
        color="0.25",
    )
    fig.text(0.5, 0.855, line2, ha="center", va="top", fontsize=8, color="0.35")
    fig.savefig(png_path, dpi=160)
    plt.close(fig)


def _plot_team_vs_loo_residual_overlay(
    r_team: np.ndarray,
    r_loo: np.ndarray,
    stats: dict[str, float],
    *,
    spec: BdpSpec,
    png_path: Path,
) -> None:
    from matplotlib.ticker import MultipleLocator
    from scipy.stats import gaussian_kde

    configure_matplotlib_mathtext()
    line1, line2 = subtitle_lines(spec, has_overlay=False)
    line2 += " · all-ps · min20 · mg10 · PPM z · blue = LOO · orange = team"

    fig, ax = plt.subplots(1, 1, figsize=(7.2, 4.6))
    fig.subplots_adjust(top=0.70, bottom=0.16, left=0.11, right=0.96)

    lo = float(min(r_team.min(), r_loo.min()))
    hi = float(max(r_team.max(), r_loo.max()))
    pad = 0.05 * (hi - lo) if hi > lo else 0.5
    x_grid = np.linspace(lo - pad, hi + pad, 400)
    y_headroom = 1.12

    series = [
        (
            r_team,
            TEAM_RESIDUAL_COLOR,
            rf"$A_i - \hat{{T}}_j$  ($\sigma={stats['std_team_residual']:.3f}$)",
        ),
        (
            r_loo,
            LOO_RESIDUAL_COLOR,
            rf"$A_i - \mathrm{{poolq}}^{{\mathrm{{LOO}}}}_i$  ($\sigma={stats['std_loo_residual']:.3f}$)",
        ),
    ]
    ymax = 0.0
    for vals, color, label in series:
        density = gaussian_kde(vals)(x_grid)
        ymax = max(ymax, float(density.max()))
        ax.fill_between(x_grid, 0.0, density, color=color, alpha=0.30, linewidth=0.0)
        ax.plot(x_grid, density, color=color, lw=2.0, label=label)

    ax.axvline(0.0, color="0.35", linestyle=":", linewidth=1.0)
    ax.set_xlim(x_grid[0], x_grid[-1])
    ax.set_xlabel(r"Residual (PPM $z$)")
    ax.set_ylabel("Density")
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=7, loc="upper right", framealpha=0.95)

    tick_step = 0.05
    y_top = float(np.ceil(ymax * y_headroom / tick_step) * tick_step)
    ax.set_ylim(0.0, y_top)
    ax.yaxis.set_major_locator(MultipleLocator(tick_step))

    corr = stats.get("corr_team_loo_residual", float("nan"))
    fig.text(
        0.5,
        0.985,
        rf"Team vs LOO ability residuals · $n={stats['n']:,}$ · $\mathrm{{corr}}={corr:.3f}$",
        ha="center",
        va="top",
        fontsize=11,
    )
    fig.text(0.5, 0.915, line1, ha="center", va="top", fontsize=9)
    fig.text(
        0.5,
        0.885,
        r"$\hat{T}_j$ = team-season mean perf (includes $i$); poolq$^{\mathrm{LOO}}_i$ = teammate mean excl.\ self",
        ha="center",
        va="top",
        fontsize=8.5,
        color="0.25",
    )
    fig.text(0.5, 0.855, line2, ha="center", va="top", fontsize=8, color="0.35")
    fig.savefig(png_path, dpi=160)
    plt.close(fig)


def _plot_single_residual_density(
    vals: np.ndarray,
    stats: dict[str, float],
    *,
    spec: BdpSpec,
    png_path: Path,
    xlab: str,
    title: str,
    vals_dft: np.ndarray | None = None,
    stats_dft: dict[str, float] | None = None,
    header_line: str | None = None,
) -> None:
    from matplotlib.ticker import MultipleLocator
    from scipy.stats import gaussian_kde

    configure_matplotlib_mathtext()
    has_dft = stats_dft is not None and stats_dft.get("n", 0) > 0
    line1, line2 = subtitle_lines(spec, has_overlay=False)
    line2 += " · all-ps · min20 · mg10 · PPM z"
    if has_dft:
        line2 += " · purple line = +DFT"

    fig, ax = plt.subplots(1, 1, figsize=(6.2, 4.6))
    fig.subplots_adjust(top=0.70, bottom=0.16, left=0.12, right=0.96)

    pools = [vals]
    if vals_dft is not None and vals_dft.size:
        pools.append(vals_dft)
    lo = float(min(v.min() for v in pools if v.size))
    hi = float(max(v.max() for v in pools if v.size))
    pad = 0.05 * (hi - lo) if hi > lo else 0.5
    x_grid = np.linspace(lo - pad, hi + pad, 400)
    y_headroom = 1.12
    color = "steelblue"

    density = gaussian_kde(vals)(x_grid)
    ymax = float(density.max())
    ax.fill_between(x_grid, 0.0, density, color=color, alpha=0.82, linewidth=0.0)
    line_main, = ax.plot(x_grid, density, color=color, lw=1.4, label=rf"w/o DFT ($n={stats['n']:,}$)")
    if vals_dft is not None and vals_dft.size > 1 and stats_dft is not None:
        density_dft = gaussian_kde(vals_dft)(x_grid)
        ymax = max(ymax, float(density_dft.max()))
        ax.plot(
            x_grid,
            density_dft,
            color=DFT_OVERLAY_COLOR,
            lw=2.0,
            label=rf"+ DFT ($n={stats_dft['n']:,}$)",
        )
    ax.axvline(0.0, color="0.35", linestyle=":", linewidth=1.0)
    ax.set_xlim(x_grid[0], x_grid[-1])
    ax.set_xlabel(xlab)
    ax.set_ylabel("Density")
    std_key = "std_loo_residual" if "std_loo_residual" in stats else "std_team_residual"
    ax.set_title(rf"$\sigma = {stats[std_key]:.3f}$", fontsize=10)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.legend(fontsize=6.5, loc="upper right", framealpha=0.95)

    tick_step = 0.05
    y_top = float(np.ceil(ymax * y_headroom / tick_step) * tick_step)
    ax.set_ylim(0.0, y_top)
    ax.yaxis.set_major_locator(MultipleLocator(tick_step))

    if header_line:
        fig.text(0.5, 0.985, header_line, ha="center", va="top", fontsize=11)
    fig.text(0.5, 0.915, line1, ha="center", va="top", fontsize=9)
    fig.text(0.5, 0.885, title, ha="center", va="top", fontsize=9)
    fig.text(0.5, 0.855, line2, ha="center", va="top", fontsize=8, color="0.35")
    fig.savefig(png_path, dpi=160)
    plt.close(fig)


def _plot_ability_residual_distributions(
    r_team: np.ndarray,
    r_grand: np.ndarray,
    stats: dict[str, float],
    *,
    spec: BdpSpec,
    png_path: Path,
    r_team_dft: np.ndarray | None = None,
    r_grand_dft: np.ndarray | None = None,
    stats_dft: dict[str, float] | None = None,
) -> None:
    from matplotlib.ticker import MultipleLocator
    from scipy.stats import gaussian_kde

    configure_matplotlib_mathtext()
    has_dft = stats_dft is not None and stats_dft.get("n", 0) > 0
    line1, line2 = subtitle_lines(spec, has_overlay=False)
    line2 += " · all-ps · min20 · mg10 · PPM z"
    if has_dft:
        line2 += " · purple line = +DFT"

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6))
    fig.subplots_adjust(wspace=0.22, top=0.70, bottom=0.16)

    pools = [r_team, r_grand]
    if r_team_dft is not None and r_team_dft.size:
        pools.append(r_team_dft)
    if r_grand_dft is not None and r_grand_dft.size:
        pools.append(r_grand_dft)
    lo = float(min(v.min() for v in pools if v.size))
    hi = float(max(v.max() for v in pools if v.size))
    pad = 0.05 * (hi - lo) if hi > lo else 0.5
    x_grid = np.linspace(lo - pad, hi + pad, 400)
    y_headroom = 1.12
    color = "steelblue"

    ymax = 0.0
    panels = [
        (axes[0], r_team, r_team_dft, r"$A_i - \mu_{\mathrm{team}(i)}$", stats["std_team_residual"]),
        (axes[1], r_grand, r_grand_dft, r"$A_i - \bar{A}$", stats["std_grand_residual"]),
    ]
    legend_handles: list = []
    legend_labels: list[str] = []
    for ax, vals, vals_dft, xlab, std in panels:
        density = gaussian_kde(vals)(x_grid)
        ymax = max(ymax, float(density.max()))
        ax.fill_between(x_grid, 0.0, density, color=color, alpha=0.82, linewidth=0.0)
        line_main, = ax.plot(x_grid, density, color=color, lw=1.4, label=rf"w/o DFT ($n={stats['n']:,}$)")
        ax.axvline(0.0, color="0.35", linestyle=":", linewidth=1.0)
        ax.set_xlim(x_grid[0], x_grid[-1])
        ax.set_xlabel(xlab)
        ax.set_title(rf"$\sigma = {std:.3f}$", fontsize=10)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        if not legend_handles:
            legend_handles.append(line_main)
            legend_labels.append(line_main.get_label())
        if vals_dft is not None and vals_dft.size > 1 and stats_dft is not None:
            density_dft = gaussian_kde(vals_dft)(x_grid)
            ymax = max(ymax, float(density_dft.max()))
            line_dft, = ax.plot(
                x_grid,
                density_dft,
                color=DFT_OVERLAY_COLOR,
                lw=2.0,
                label=rf"+ DFT ($n={stats_dft['n']:,}$)",
            )
            if len(legend_handles) < 2:
                legend_handles.append(line_dft)
                legend_labels.append(line_dft.get_label())

    y_top = ymax * y_headroom
    tick_step = 0.05
    y_top = float(np.ceil(y_top / tick_step) * tick_step)
    for ax in axes:
        ax.set_ylim(0.0, y_top)
        ax.yaxis.set_major_locator(MultipleLocator(tick_step))

    axes[0].set_ylabel("Density")
    if legend_handles:
        axes[1].legend(handles=legend_handles, labels=legend_labels, fontsize=6.5, loc="upper right", framealpha=0.95)
    h_sort = stats["H_sort_pooled"]
    fig.text(
        0.5,
        0.985,
        rf"$H_{{\mathrm{{sort}}}} = 1 - \sum_i (A_i - \mu_{{\mathrm{{team}}(i)}})^2 / \sum_i (A_i - \bar{{A}})^2 = {h_sort:.3f}$",
        ha="center",
        va="top",
        fontsize=11,
    )
    fig.text(0.5, 0.915, line1, ha="center", va="top", fontsize=9)
    fig.text(0.5, 0.885, line2, ha="center", va="top", fontsize=8, color="0.35")
    fig.savefig(png_path, dpi=160)
    plt.close(fig)


def _load_sim_rho_zero(detail_jsonl: Path) -> pd.DataFrame:
    if not detail_jsonl.is_file():
        return pd.DataFrame()
    rows = []
    with detail_jsonl.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if float(rec.get("rho", -1)) != 0.0:
                continue
            rows.append(
                {
                    "season": int(rec["season"]),
                    "rho": float(rec["rho"]),
                    "seed": int(rec["seed"]),
                    "h_sort_sim": float(rec["h_sort_sim"]),
                }
            )
    return pd.DataFrame(rows)


def _plot_hsort_distribution(
    season_tbl: pd.DataFrame,
    pooled_emp: float,
    sim_zero: pd.DataFrame,
    *,
    spec: BdpSpec,
    png_path: Path,
) -> None:
    configure_matplotlib_mathtext()
    line1, line2 = subtitle_lines(spec, has_overlay=False)
    line2 += " · all-ps · min20 · mg10 · PPM z"

    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.6))
    fig.subplots_adjust(wspace=0.28, top=0.86, bottom=0.16)

    # --- Left: per-season empirical ---
    ax = axes[0]
    x = season_tbl["season"].to_numpy(dtype=int)
    y = season_tbl["h_sort_empirical"].to_numpy(dtype=float)
    ax.bar(x, y, color="steelblue", alpha=0.88, edgecolor="white", linewidth=0.5, label="empirical")
    if not sim_zero.empty:
        sim_by_season = (
            sim_zero.groupby("season", observed=True)["h_sort_sim"]
            .agg(["mean", "std"])
            .reindex(x)
        )
        ax.errorbar(
            x,
            sim_by_season["mean"],
            yerr=sim_by_season["std"],
            fmt="o",
            color=SIM_COLOR,
            ecolor=SIM_COLOR,
            capsize=3,
            markersize=5,
            linewidth=1.1,
            label=rf"LG sim $\rho=0$ (mean $\pm$ sd)",
        )
    ax.axhline(pooled_emp, color="0.35", linestyle=":", linewidth=1.2, label=rf"pooled emp = {pooled_emp:.3f}")
    ax.set_xlabel("Season")
    ax.set_ylabel(r"$H_{\mathrm{sort}}$")
    ax.set_title("Per-season empirical $H_{\\mathrm{sort}}$", fontsize=10)
    ax.legend(fontsize=6.5, loc="upper right", framealpha=0.95)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    # --- Right: sim rho=0 distribution vs empirical ---
    ax = axes[1]
    if not sim_zero.empty:
        sim_vals = sim_zero["h_sort_sim"].to_numpy(dtype=float)
        bins = np.linspace(max(0.0, sim_vals.min() - 0.01), sim_vals.max() + 0.01, 28)
        ax.hist(
            sim_vals,
            bins=bins,
            color=SIM_COLOR,
            alpha=0.55,
            edgecolor="white",
            linewidth=0.35,
            label=rf"LG $\rho=0$ sim ($n={len(sim_vals):,}$)",
        )
    ax.axvline(pooled_emp, color="steelblue", linewidth=2.0, label=rf"pooled empirical = {pooled_emp:.3f}")
    for val in y:
        ax.axvline(val, color="steelblue", alpha=0.25, linewidth=0.8)
    ax.set_xlabel(r"$H_{\mathrm{sort}}$")
    ax.set_ylabel("Count")
    ax.set_title(r"Sim $\rho=0$ distribution vs empirical", fontsize=10)
    ax.legend(fontsize=6.5, loc="upper right", framealpha=0.95)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    fig.suptitle(
        rf"Empirical sorting index $H_{{\mathrm{{sort}}}}$ · MBB {spec.season_min}–{spec.season_max} · all-ps",
        fontsize=11,
    )
    fig.text(0.5, 0.02, f"{line1} · {line2}", ha="center", va="bottom", fontsize=8, color="0.35")
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run_hsort_distribution(
    spec: BdpSpec,
    *,
    out_png: Path | None = None,
    out_meta_dir: Path | None = None,
    prefix: str = PREFIX,
    detail_jsonl: Path | None = None,
) -> Path:
    ensure_hero_dirs()
    out_dir = out_meta_dir or REIGNING_HERO_BASIC_PLOTS
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = PanelPrepConfig.from_args(
        min_minutes=20.0,
        ppm_zero_below_minutes=None,
        season_min=spec.season_min,
        season_max=spec.season_max,
    )
    panel = prepare_calibration_panel(cfg)
    season_tbl = _season_hsort_table(panel, spec.season_min, spec.season_max)
    pooled_emp = _pooled_hsort(panel)

    stem = f"{prefix}_BDP_Hsort_dist_{spec.slug}_ppm_allps"
    out_png = out_png or out_dir / f"{stem}.png"
    out_csv = out_dir / f"{stem}_by_season.csv"
    out_meta = out_dir / f"{stem}.json"

    if detail_jsonl is None:
        detail_jsonl = (
            REIGNING_HERO_CALIBRATION_RHO
            / "REIGNING_PD21_rho_hsort_calibrate_2009_2021_mg10_min20_09_21_detail_bracket.jsonl"
        )
    sim_zero = _load_sim_rho_zero(detail_jsonl)

    season_tbl.to_csv(out_csv, index=False)
    _plot_hsort_distribution(season_tbl, pooled_emp, sim_zero, spec=spec, png_path=out_png)

    meta = {
        "diagnostic": "bdp_hsort_distribution",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "panel_rows": "all-ps",
        "H_sort_pooled_empirical": pooled_emp,
        "H_sort_empirical_by_season": season_tbl.to_dict(orient="records"),
        "H_sort_sim_rho0_n": int(len(sim_zero)),
        "H_sort_sim_rho0_mean": float(sim_zero["h_sort_sim"].mean()) if len(sim_zero) else None,
        "note": (
            "H_sort measures variance explained by team assignment (low ≈ weak homophily). "
            "Interval overlap tracks team windows on the perf axis — a different geometry."
        ),
        "outputs": {"png": out_png.name, "csv": out_csv.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_csv.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def run_ability_residual_distributions(
    spec: BdpSpec,
    *,
    out_png: Path | None = None,
    out_meta_dir: Path | None = None,
    prefix: str = PREFIX,
) -> Path:
    """Side-by-side density of team-mean vs grand-mean ability residuals."""
    ensure_hero_dirs()
    out_dir = out_meta_dir or REIGNING_HERO_BASIC_PLOTS
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = PanelPrepConfig.from_args(
        min_minutes=20.0,
        ppm_zero_below_minutes=None,
        season_min=spec.season_min,
        season_max=spec.season_max,
    )
    panel = prepare_calibration_panel(cfg)
    r_team, r_grand, stats = _ability_residual_vectors(panel)
    dft_teams = _drafted_teams_in_panel(panel)
    r_team_dft: np.ndarray | None = None
    r_grand_dft: np.ndarray | None = None
    stats_dft: dict[str, float] | None = None
    if dft_teams:
        r_team_dft, r_grand_dft, stats_dft = _ability_residual_vectors(panel, team_ids=dft_teams)

    stem = f"{prefix}_BDP_ability_residuals_{spec.slug}_ppm_allps"
    out_png = out_png or out_dir / f"{stem}.png"
    out_meta = out_dir / f"{stem}.json"

    _plot_ability_residual_distributions(
        r_team,
        r_grand,
        stats,
        spec=spec,
        png_path=out_png,
        r_team_dft=r_team_dft,
        r_grand_dft=r_grand_dft,
        stats_dft=stats_dft,
    )

    meta = {
        "diagnostic": "bdp_ability_residual_distributions",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "panel_rows": "all-ps",
        "overlay_dft": bool(dft_teams),
        **stats,
        "dft": stats_dft,
        "note": (
            "Left: within-team demeaned perf (numerator of H_sort ratio). "
            "Right: grand-mean demeaned perf (denominator). Pooled over 09–21 all-ps panel. "
            "+ DFT = draft-ever teams (all-time in window)."
        ),
        "outputs": {"png": out_png.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def run_ability_loo_residual_distribution(
    spec: BdpSpec,
    *,
    out_png: Path | None = None,
    out_meta_dir: Path | None = None,
    prefix: str = PREFIX,
) -> Path:
    """Density of A_i - poolq_LOO,i (LOO teammate pool quality instead of team mean)."""
    ensure_hero_dirs()
    out_dir = out_meta_dir or REIGNING_HERO_BASIC_PLOTS
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = PanelPrepConfig.from_args(
        min_minutes=20.0,
        ppm_zero_below_minutes=None,
        season_min=spec.season_min,
        season_max=spec.season_max,
    )
    panel = prepare_calibration_panel(cfg)
    r_loo, stats = _ability_loo_residual_vector(panel)
    dft_teams = _drafted_teams_in_panel(panel)
    r_loo_dft: np.ndarray | None = None
    stats_dft: dict[str, float] | None = None
    if dft_teams:
        r_loo_dft, stats_dft = _ability_loo_residual_vector(panel, team_ids=dft_teams)

    stem = f"{prefix}_BDP_ability_loo_residuals_{spec.slug}_ppm_allps"
    out_png = out_png or out_dir / f"{stem}.png"
    out_meta = out_dir / f"{stem}.json"

    _plot_single_residual_density(
        r_loo,
        stats,
        spec=spec,
        png_path=out_png,
        xlab=r"$A_i - \mathrm{poolq}^{\mathrm{LOO}}_i$",
        title=r"Ability minus player LOO ($A_i - \mathrm{poolq}^{\mathrm{LOO}}_i$)",
        vals_dft=r_loo_dft,
        stats_dft=stats_dft,
    )

    meta = {
        "diagnostic": "bdp_ability_loo_residual_distribution",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "panel_rows": "all-ps",
        "overlay_dft": bool(dft_teams),
        **stats,
        "dft": stats_dft,
        "note": (
            "LOO residual = perf minus leave-one-out teammate mean pool quality (poolq_LOO). "
            "Analogous to left panel of ability_residuals but μ_team(i) replaced by poolq_LOO,i. "
            "+ DFT = draft-ever teams (all-time in window)."
        ),
        "outputs": {"png": out_png.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def run_ability_team_vs_loo_residual_compare(
    spec: BdpSpec,
    *,
    out_png: Path | None = None,
    out_meta_dir: Path | None = None,
    prefix: str = PREFIX,
) -> Path:
    """Overlay A_i - T̂_j (orange) vs A_i - poolq_LOO,i (blue) on the same axes."""
    ensure_hero_dirs()
    out_dir = out_meta_dir or REIGNING_HERO_BASIC_PLOTS
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = PanelPrepConfig.from_args(
        min_minutes=20.0,
        ppm_zero_below_minutes=None,
        season_min=spec.season_min,
        season_max=spec.season_max,
    )
    panel = prepare_calibration_panel(cfg)
    r_team, r_loo, stats = _ability_team_loo_residual_pair(panel)

    stem = f"{prefix}_BDP_ability_Tj_vs_loo_residuals_{spec.slug}_ppm_allps"
    out_png = out_png or out_dir / f"{stem}.png"
    out_meta = out_dir / f"{stem}.json"

    _plot_team_vs_loo_residual_overlay(r_team, r_loo, stats, spec=spec, png_path=out_png)

    meta = {
        "diagnostic": "bdp_ability_team_vs_loo_residual_compare",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "panel_rows": "all-ps",
        **stats,
        "note": (
            "Superposed KDEs on identical player-rows. Orange = A_i - T̂_j (team mean incl. i); "
            "blue = A_i - poolq_LOO,i (teammate mean excl. i)."
        ),
        "outputs": {"png": out_png.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def run_tj_minus_loo_distribution(
    spec: BdpSpec,
    *,
    out_png: Path | None = None,
    out_meta_dir: Path | None = None,
    prefix: str = PREFIX,
) -> Path:
    """Distribution of T̂_j - poolq_LOO,i with team vs LOO H_sort comparison."""
    ensure_hero_dirs()
    out_dir = out_meta_dir or REIGNING_HERO_BASIC_PLOTS
    out_dir.mkdir(parents=True, exist_ok=True)

    cfg = PanelPrepConfig.from_args(
        min_minutes=20.0,
        ppm_zero_below_minutes=None,
        season_min=spec.season_min,
        season_max=spec.season_max,
    )
    panel = prepare_calibration_panel(cfg)
    delta, stats = _tj_minus_loo_vector(panel)
    dft_teams = _drafted_teams_in_panel(panel)
    delta_dft: np.ndarray | None = None
    stats_dft: dict[str, float] | None = None
    if dft_teams:
        delta_dft, stats_dft = _tj_minus_loo_vector(panel, team_ids=dft_teams)

    stem = f"{prefix}_BDP_Tj_minus_loo_{spec.slug}_ppm_allps"
    out_png = out_png or out_dir / f"{stem}.png"
    out_meta = out_dir / f"{stem}.json"

    _plot_tj_minus_loo_distribution(
        delta,
        stats,
        spec=spec,
        png_path=out_png,
        delta_dft=delta_dft,
        stats_dft=stats_dft,
    )

    meta = {
        "diagnostic": "bdp_tj_minus_loo_distribution",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "panel_rows": "all-ps",
        "overlay_dft": bool(dft_teams),
        **stats,
        "dft": stats_dft,
        "note": (
            "T̂_j - poolq_LOO,i = self-inclusion gap (team mean minus LOO teammate mean). "
            "H_sort^team = 1 - sum(A_i - T̂_j)² / sum(A_i - Ā)² (standard). "
            "H_sort^LOO replaces team mean with poolq_LOO in the numerator; can be negative "
            "because LOO is not a partition of variance across teams."
        ),
        "outputs": {"png": out_png.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def main() -> None:
    spec = parse_bdp_spec("mg10 min20 09_21")
    run_hsort_distribution(spec)
    run_ability_residual_distributions(spec)
    run_ability_loo_residual_distribution(spec)
    run_ability_team_vs_loo_residual_compare(spec)
    run_tj_minus_loo_distribution(spec)


if __name__ == "__main__":
    main()
