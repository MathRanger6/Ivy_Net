#!/usr/bin/env python3
"""BDP — player poolq_LOO porch plots (reigning hero / Alex Aug 2026).

1. Distribution of player poolq_LOO (last-ps, winsor 1–99).
2. P(Y=1) vs poolq_LOO (EW16 equal-width bins — reigning lock).

Run (repo root):
  python sports/scripts/bdp_reigning_loo_plots.py
  python sports/scripts/bdp_reigning_loo_plots.py --only loo_dist draft_rate_loo
"""

from __future__ import annotations

import argparse
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
sys.path.insert(0, str(SCRIPTS))

from bdp_ai_tj_distributions import (  # noqa: E402
    DFT_OVERLAY_COLOR,
    BdpSpec,
    parse_bdp_spec,
    subtitle_lines,
)
from gallery_mathtext import configure_matplotlib_mathtext  # noqa: E402
from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs  # noqa: E402

WINSOR = (0.01, 0.99)
N_BINS_EW = 16


def _prepare_last_ps(
    spec: BdpSpec,
    perf_metric: str = "ppm",
    *,
    poolq_winsor_quantiles: tuple[float, float] | None = WINSOR,
) -> pd.DataFrame:
    from bdp_ai_tj_distributions import _prepare

    return _prepare(
        spec,
        perf_metric,
        panel_rows="last-ps",
        poolq_winsor_quantiles=poolq_winsor_quantiles,
    )


def _poolq_values(panel: pd.DataFrame) -> np.ndarray:
    return pd.to_numeric(panel["poolq_loo"], errors="coerce").dropna().to_numpy(dtype=float)


def _loo_summary(values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return {"n": 0}
    return {
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": float(v.min()),
        "max": float(v.max()),
        "median": float(np.median(v)),
        "p25": float(np.percentile(v, 25)),
        "p75": float(np.percentile(v, 75)),
    }


def _equal_width_edges(values: np.ndarray, n_bins: int) -> np.ndarray:
    s = np.asarray(values, dtype=float)
    s = s[np.isfinite(s)]
    if s.size == 0:
        return np.linspace(0.0, 1.0, int(n_bins) + 1)
    lo, hi = float(s.min()), float(s.max())
    if hi <= lo:
        hi = lo + 1.0
    return np.linspace(lo, hi, int(n_bins) + 1)


def _panel_with_t_j_hat(panel: pd.DataFrame) -> pd.DataFrame:
    """Team-season mean perf z (T̂_j, includes self) with winsor 1–99 — matches Pass A ``roster-x poolq``."""
    work = panel.copy()
    work["t_j_hat"] = work.groupby(["team_id", "season"], observed=True)["perf"].transform("mean")
    s = pd.to_numeric(work["t_j_hat"], errors="coerce").dropna()
    if len(s):
        lo = float(s.quantile(WINSOR[0]))
        hi = float(s.quantile(WINSOR[1]))
        work["t_j_hat"] = pd.to_numeric(work["t_j_hat"], errors="coerce").clip(lower=lo, upper=hi)
    return work


def _ventile_table(
    panel: pd.DataFrame,
    x_col: str,
    *,
    n_bins: int = N_BINS_EW,
    poolq_binning: str = "equal_width",
) -> pd.DataFrame:
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    work = panel.dropna(subset=[x_col, "Y_draft"]).copy()
    x = pd.to_numeric(work[x_col], errors="coerce")
    work["vent"] = assign_poolq_bin_labels(x, n_bins, poolq_binning)
    tbl = (
        work.dropna(subset=["vent"])
        .groupby("vent", observed=True)
        .agg(
            n=("Y_draft", "size"),
            drafts=("Y_draft", "sum"),
            draft_rate=("Y_draft", "mean"),
            x_mean=(x_col, "mean"),
            x_median=(x_col, "median"),
            x_min=(x_col, "min"),
            x_max=(x_col, "max"),
        )
        .reset_index()
        .sort_values("vent")
    )
    tbl["bin_display"] = tbl["vent"].astype(int) + 1
    if str(poolq_binning).strip().lower() == "equal_width":
        edges = _equal_width_edges(x.dropna().to_numpy(dtype=float), n_bins)
        tbl["edge_lo"] = tbl["vent"].astype(int).map(lambda v: float(edges[int(v)]))
        tbl["edge_hi"] = tbl["vent"].astype(int).map(lambda v: float(edges[int(v) + 1]))
        tbl["x_center"] = (tbl["edge_lo"] + tbl["edge_hi"]) / 2.0
    else:
        tbl["edge_lo"] = tbl["x_min"]
        tbl["edge_hi"] = tbl["x_max"]
        tbl["x_center"] = tbl["x_mean"]
    tbl["poolq_binning"] = poolq_binning
    return tbl


def _loo_ventile_table(
    panel: pd.DataFrame,
    *,
    n_bins: int = N_BINS_EW,
    poolq_binning: str = "equal_width",
) -> pd.DataFrame:
    tbl = _ventile_table(panel, "poolq_loo", n_bins=n_bins, poolq_binning=poolq_binning)
    return tbl.rename(
        columns={
            "x_mean": "poolq_mean",
            "x_median": "poolq_median",
            "x_min": "poolq_min",
            "x_max": "poolq_max",
        }
    )


def _t_j_ventile_table(
    panel: pd.DataFrame,
    *,
    n_bins: int = N_BINS_EW,
    poolq_binning: str = "equal_width",
) -> pd.DataFrame:
    work = _panel_with_t_j_hat(panel)
    tbl = _ventile_table(work, "t_j_hat", n_bins=n_bins, poolq_binning=poolq_binning)
    return tbl.rename(
        columns={
            "x_mean": "t_j_mean",
            "x_median": "t_j_median",
            "x_min": "t_j_min",
            "x_max": "t_j_max",
        }
    )


def _quadratic_lpm_coef_x(panel: pd.DataFrame, x_col: str, *, b1: str, b2: str) -> dict:
    work = panel.dropna(subset=[x_col, "Y_draft"]).copy()
    y = pd.to_numeric(work["Y_draft"], errors="coerce").astype(float).to_numpy()
    p = pd.to_numeric(work[x_col], errors="coerce").astype(float).to_numpy()
    q = np.square(p)
    mask = np.isfinite(y) & np.isfinite(p) & np.isfinite(q)
    x_mat = np.column_stack([np.ones(mask.sum()), p[mask], q[mask]])
    beta, *_ = np.linalg.lstsq(x_mat, y[mask], rcond=None)
    return {"const": float(beta[0]), b1: float(beta[1]), b2: float(beta[2])}


def _quadratic_lpm_coef(panel: pd.DataFrame) -> dict:
    return _quadratic_lpm_coef_x(
        panel,
        "poolq_loo",
        b1="beta_poolq_loo",
        b2="beta_poolq_loo_sq",
    )


def _quadratic_lpm_coef_t_j(panel: pd.DataFrame) -> dict:
    work = _panel_with_t_j_hat(panel)
    return _quadratic_lpm_coef_x(work, "t_j_hat", b1="beta_t_j", b2="beta_t_j_sq")


def _lpm_note(b2: float) -> str:
    if b2 < -1e-5:
        return rf"LPM: $\beta_2={b2:.4g}$ ($<0$, concave)"
    return rf"LPM: $\beta_2={b2:+.4g}$ (flat / not concave)"


def _plot_ecdf(ax, values: np.ndarray, *, color: str = "steelblue", label: str | None = None) -> None:
    v = np.sort(values[np.isfinite(values)])
    if v.size == 0:
        return
    ys = np.arange(1, v.size + 1) / v.size
    ax.step(v, ys, where="post", color=color, lw=1.8, label=label)


def _plot_dft_count_line(ax, values_dft: np.ndarray, bins: np.ndarray, *, label: str) -> None:
    counts_dft, _ = np.histogram(values_dft, bins=bins)
    centers = 0.5 * (bins[:-1] + bins[1:])
    ax.plot(
        centers,
        counts_dft,
        color=DFT_OVERLAY_COLOR,
        linewidth=2.0,
        marker="o",
        markersize=2.5,
        label=label,
    )


def _stats_column_lines(stats: dict, title: str, *, col_w: int = 11) -> list[str]:
    return [
        title.rjust(col_w),
        f"n={stats['n']:,}".rjust(col_w),
        f"med={stats['median']:.2f}".rjust(col_w),
        f"μ={stats['mean']:.2f}".rjust(col_w),
        f"σ={stats['std']:.2f}".rjust(col_w),
    ]


def _annotate_loo_stats(ax, stats: dict, *, stats_dft: dict | None = None, col_w: int = 11) -> None:
    if stats_dft is None:
        text = "\n".join(_stats_column_lines(stats, "", col_w=col_w))
    else:
        left = _stats_column_lines(stats, "w/o DFT", col_w=col_w)
        right = _stats_column_lines(stats_dft, "+ DFT", col_w=col_w)
        text = "\n".join(f"{l}   {r}" for l, r in zip(left, right))
    ax.text(
        0.03,
        0.97,
        text,
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        linespacing=1.15,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", alpha=0.92, edgecolor="0.8"),
    )


def _count_weighted_bar_colors(counts: np.ndarray, *, cmap_name: str = "Blues") -> list:
    n = np.asarray(counts, dtype=float)
    if n.size == 0:
        return []
    lo, hi = float(n.min()), float(n.max())
    cmap = plt.get_cmap(cmap_name)
    if hi <= lo:
        return [cmap(0.65) for _ in n]
    norm = plt.Normalize(vmin=lo, vmax=hi)
    levels = 0.28 + 0.67 * norm(n)
    return [cmap(float(v)) for v in levels]


def _label_color_for_bar(facecolor) -> str:
    rgba = facecolor if len(facecolor) >= 3 else (0.5, 0.5, 0.5, 1.0)
    lum = 0.299 * float(rgba[0]) + 0.587 * float(rgba[1]) + 0.114 * float(rgba[2])
    return "0.15" if lum > 0.62 else "white"


def _annotate_bin_n(ax, x: np.ndarray, y: np.ndarray, counts: np.ndarray, bar_colors: list) -> None:
    ymin, ymax = ax.get_ylim()
    span = ymax - ymin
    for i, (xi, yi, n) in enumerate(zip(x, y, counts)):
        ni = int(n)
        if ni <= 0:
            continue
        yi_f = float(yi)
        if yi_f < span * 0.12:
            y_pos = yi_f + span * 0.015
            rotation = 0
            fontsize = 6
            va = "bottom"
            color = "0.25"
        else:
            y_pos = ymin + span * 0.24
            rotation = 90
            fontsize = 6.5
            va = "bottom"
            color = _label_color_for_bar(bar_colors[i])
        ax.text(
            xi,
            y_pos,
            f"{ni:,}",
            ha="center",
            va=va,
            fontsize=fontsize,
            rotation=rotation,
            color=color,
            fontweight="bold",
            clip_on=True,
        )


def _format_loo_tick(val: float) -> str:
    v = float(val)
    if not np.isfinite(v):
        return ""
    if abs(v) < 1.5:
        return f"{v:.2f}"
    return f"{v:.2g}"


def _plot_poolq_loo_distribution(
    loo: np.ndarray,
    *,
    loo_dft: np.ndarray | None,
    stats: dict,
    stats_dft: dict | None,
    spec: BdpSpec,
    png_path: Path,
    poolq_winsor_quantiles: tuple[float, float] | None = WINSOR,
) -> None:
    configure_matplotlib_mathtext()
    has_overlay = loo_dft is not None and loo_dft.size > 0
    line1, line2 = subtitle_lines(spec, has_overlay=has_overlay)
    if poolq_winsor_quantiles is None:
        line2 += " · last-ps · no poolq_LOO winsor"
        title_suffix = r" (no winsor)"
    else:
        lo_pct = int(round(poolq_winsor_quantiles[0] * 100))
        hi_pct = int(round(poolq_winsor_quantiles[1] * 100))
        line2 += f" · last-ps · winsor {lo_pct}–{hi_pct} on poolq_LOO"
        title_suffix = ""

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    fig.subplots_adjust(wspace=0.28, top=0.86, bottom=0.14)

    lo = float(np.min(loo)) if loo.size else -1.0
    hi = float(np.max(loo)) if loo.size else 1.0
    if has_overlay and loo_dft is not None and loo_dft.size:
        lo = min(lo, float(np.min(loo_dft)))
        hi = max(hi, float(np.max(loo_dft)))
    bins = np.linspace(lo, hi, 36)

    ax = axes[0]
    ax.hist(
        loo,
        bins=bins,
        color="steelblue",
        alpha=0.85,
        edgecolor="white",
        linewidth=0.35,
        label=rf"without DFT ($n={stats['n']:,}$)" if has_overlay else None,
    )
    if has_overlay and loo_dft is not None and stats_dft is not None:
        _plot_dft_count_line(
            ax,
            loo_dft,
            bins,
            label=rf"+ DFT ($n={stats_dft['n']:,}$)",
        )
    ax.axvline(stats["median"], color="0.35", linestyle=":", linewidth=1.4, label=rf"Median = {stats['median']:.2f}")
    ax.set_xlabel(r"Player poolq$_{\mathrm{LOO}}$ (PPM $z$, teammate mean excl. self)")
    ax.set_ylabel("Player count")
    ax.set_title("Histogram", fontsize=10)
    ax.legend(fontsize=6, loc="upper right", framealpha=0.95)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    ax = axes[1]
    _plot_ecdf(ax, loo, label=rf"without DFT ($n={stats['n']:,}$)" if has_overlay else None)
    if has_overlay and loo_dft is not None and stats_dft is not None:
        _plot_ecdf(ax, loo_dft, color=DFT_OVERLAY_COLOR, label=rf"+ DFT ($n={stats_dft['n']:,}$)")
    ax.axhline(0.5, color="0.82", linestyle=":", linewidth=0.9)
    ax.axvline(stats["median"], color="0.35", linestyle=":", linewidth=1.4, label=rf"Median = {stats['median']:.2f}")
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"Player poolq$_{\mathrm{LOO}}$")
    ax.set_ylabel(r"ECDF  $F(x)$")
    ax.set_title("ECDF", fontsize=10)
    ax.legend(fontsize=6, loc="lower right", framealpha=0.95)
    ax.grid(alpha=0.25, linewidth=0.5)
    _annotate_loo_stats(ax, stats, stats_dft=stats_dft)

    fig.suptitle(
        rf"Player poolq$_{{\mathrm{{LOO}}}}$ distribution{title_suffix} · MBB {spec.season_min}–{spec.season_max} · last-ps",
        fontsize=11,
    )
    fig.text(0.5, 0.02, f"{line1} · {line2}", ha="center", va="bottom", fontsize=8, color="0.35")
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _paint_draft_rate_panel(
    ax,
    tbl: pd.DataFrame,
    *,
    title: str,
    xlabel: str,
    lpm_b2: float,
    show_ylabel: bool = True,
    poolq_binning: str = "equal_width",
) -> None:
    x = tbl["vent"].to_numpy(dtype=float) + 1
    y = tbl["draft_rate"].to_numpy(dtype=float)
    counts = tbl["n"].to_numpy(dtype=int)
    quantile_bins = str(poolq_binning).strip().lower() == "quantile"
    if quantile_bins:
        bar_colors = ["steelblue"] * len(counts)
    else:
        bar_colors = _count_weighted_bar_colors(counts)
    ax.bar(x, y, color=bar_colors, edgecolor="white", linewidth=0.6, alpha=0.95)
    ymax = float(np.max(y)) if len(y) else 0.05
    ax.set_ylim(0, max(0.05, ymax * 1.22))
    if not quantile_bins:
        _annotate_bin_n(ax, x, y, counts, bar_colors)
    ax.set_xticks(x)
    if str(poolq_binning).strip().lower() == "equal_width":
        labels = [_format_loo_tick(v) for v in tbl["x_center"]]
        ax.set_xticklabels(labels, fontsize=6.5, rotation=50, ha="right")
    else:
        ax.set_xticklabels([str(int(v)) for v in x], fontsize=7)
    ax.set_xlabel(xlabel, fontsize=9, labelpad=8)
    if show_ylabel:
        ax.set_ylabel(r"$\hat{P}(Y{=}1)$  (mean $Y_{\mathrm{draft}}$ per bin)", fontsize=9)
    ax.set_title(title, fontsize=9.5, pad=10)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    ax.text(
        0.98,
        0.97,
        _lpm_note(lpm_b2),
        transform=ax.transAxes,
        fontsize=7.5,
        va="top",
        ha="right",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9, edgecolor="0.85"),
    )


def _plot_draft_rate_vs_loo(
    tbl: pd.DataFrame,
    coef: dict,
    *,
    spec: BdpSpec,
    png_path: Path,
    perf_metric: str = "ppm",
) -> None:
    configure_matplotlib_mathtext()
    line1, line2 = subtitle_lines(spec, has_overlay=False)
    line2 += f" · last-ps · EW{N_BINS_EW} equal-width · winsor 1–99 · perf={perf_metric}"

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    _paint_draft_rate_panel(
        ax,
        tbl,
        title=(
            rf"Empirical draft rate vs player LOO · MBB {spec.season_min}–{spec.season_max}\n"
            rf"Reigning lock · ever-$Y$ · ALLT · min{spec.min_minutes:g} · mg{spec.min_team_season_games} · "
            rf"$\mathrm{{perf}}$={perf_metric}"
        ),
        xlabel=r"Player poolq$_{\mathrm{LOO}}$ (equal-width bins; ticks = bin midpoints)",
        lpm_b2=coef["beta_poolq_loo_sq"],
    )

    fig.text(0.5, 0.01, f"{line1} · {line2}", ha="center", va="bottom", fontsize=8, color="0.35")
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(png_path, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _plot_draft_rate_loo_vs_tj(
    tbl_loo_ew: pd.DataFrame,
    tbl_tj_ew: pd.DataFrame,
    tbl_loo_q: pd.DataFrame,
    tbl_tj_q: pd.DataFrame,
    coef_loo: dict,
    coef_tj: dict,
    *,
    spec: BdpSpec,
    png_path: Path,
    n_bins: int = N_BINS_EW,
) -> None:
    configure_matplotlib_mathtext()
    line1, line2 = subtitle_lines(spec, has_overlay=False)
    line2 += f" · last-ps · winsor 1–99 on each x-axis"

    fig, axes = plt.subplots(2, 2, figsize=(14.0, 10.0))
    fig.subplots_adjust(left=0.08, right=0.98, wspace=0.26, hspace=0.42, top=0.91, bottom=0.14)

    _paint_draft_rate_panel(
        axes[0, 0],
        tbl_loo_ew,
        title=rf"HERO poolq$_{{\mathrm{{LOO}}}}$ · equal-width (EW{n_bins})",
        xlabel=r"poolq$_{\mathrm{LOO}}$ bin midpoint",
        lpm_b2=coef_loo["beta_poolq_loo_sq"],
        show_ylabel=True,
        poolq_binning="equal_width",
    )
    _paint_draft_rate_panel(
        axes[0, 1],
        tbl_tj_ew,
        title=rf"Team $\hat{{T}}_j$ · equal-width (EW{n_bins})",
        xlabel=r"$\hat{T}_j$ bin midpoint",
        lpm_b2=coef_tj["beta_t_j_sq"],
        show_ylabel=False,
        poolq_binning="equal_width",
    )
    _paint_draft_rate_panel(
        axes[1, 0],
        tbl_loo_q,
        title=rf"HERO poolq$_{{\mathrm{{LOO}}}}$ · quantile (Q{n_bins})",
        xlabel=r"Ventile bin ($1$ = lowest poolq$_{\mathrm{LOO}}$)",
        lpm_b2=coef_loo["beta_poolq_loo_sq"],
        show_ylabel=True,
        poolq_binning="quantile",
    )
    _paint_draft_rate_panel(
        axes[1, 1],
        tbl_tj_q,
        title=rf"Team $\hat{{T}}_j$ · quantile (Q{n_bins})",
        xlabel=r"Ventile bin ($1$ = lowest $\hat{T}_j$)",
        lpm_b2=coef_tj["beta_t_j_sq"],
        show_ylabel=False,
        poolq_binning="quantile",
    )

    fig.suptitle(
        rf"Empirical $\hat{{P}}(Y{{=}}1)$ vs roster context · MBB {spec.season_min}–{spec.season_max} · last-ps",
        fontsize=11,
        y=0.98,
    )
    fig.text(
        0.5,
        0.03,
        f"{line1}\n{line2} · ever-$Y$ · ALLT · min{spec.min_minutes:g} · mg{spec.min_team_season_games}"
        f" · top row EW{n_bins} · bottom row quantile {n_bins}",
        ha="center",
        va="bottom",
        fontsize=7.5,
        color="0.35",
        linespacing=1.2,
    )
    fig.savefig(png_path, dpi=160)
    plt.close(fig)


def run_poolq_loo_distribution(
    spec: BdpSpec,
    *,
    out_png: Path,
    out_meta_dir: Path,
    prefix: str = "REIGNING",
    overlay_dft: bool = True,
    poolq_winsor_quantiles: tuple[float, float] | None = WINSOR,
) -> Path:
    panel = _prepare_last_ps(spec, poolq_winsor_quantiles=poolq_winsor_quantiles)
    loo = _poolq_values(panel)
    stats = _loo_summary(loo)

    loo_dft: np.ndarray | None = None
    stats_dft: dict | None = None
    if overlay_dft and not spec.dft:
        panel_dft = _prepare_last_ps(
            replace(spec, dft=True),
            poolq_winsor_quantiles=poolq_winsor_quantiles,
        )
        loo_dft = _poolq_values(panel_dft)
        stats_dft = _loo_summary(loo_dft)

    stem = f"{prefix}_BDP_poolq_loo_dist_{spec.slug}_ppm_lastps"
    if poolq_winsor_quantiles is None:
        stem += "_nowinsor"
    out_png = out_png.parent / f"{stem}.png"
    out_meta = out_meta_dir / f"{stem}.json"

    _plot_poolq_loo_distribution(
        loo,
        loo_dft=loo_dft,
        stats=stats,
        stats_dft=stats_dft,
        spec=spec,
        png_path=out_png,
        poolq_winsor_quantiles=poolq_winsor_quantiles,
    )

    meta = {
        "diagnostic": "bdp_poolq_loo_distribution",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "panel_rows": "last-ps",
        "poolq_winsor": list(poolq_winsor_quantiles) if poolq_winsor_quantiles else None,
        "overlay_dft": overlay_dft and not spec.dft,
        "poolq_loo": stats,
        "outputs": {"png": out_png.name},
    }
    if stats_dft is not None:
        meta["poolq_loo_dft"] = stats_dft
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def run_draft_rate_vs_loo(
    spec: BdpSpec,
    *,
    perf_metric: str = "ppm",
    out_png: Path,
    out_meta_dir: Path,
    out_meta_dir_csv: Path | None = None,
    prefix: str = "REIGNING",
    n_bins: int = N_BINS_EW,
) -> Path:
    panel = _prepare_last_ps(spec, perf_metric)
    tbl = _loo_ventile_table(panel, n_bins=n_bins)
    coef = _quadratic_lpm_coef(panel)

    stem = f"{prefix}_BDP_draft_rate_poolq_loo_{spec.slug}_ew{n_bins}_{perf_metric}_lastps"
    out_png = out_png.parent / f"{stem}.png"
    out_meta = out_meta_dir / f"{stem}.json"
    csv_dir = out_meta_dir_csv or out_meta_dir
    out_csv = csv_dir / f"{stem}.csv"

    _plot_draft_rate_vs_loo(tbl, coef, spec=spec, png_path=out_png, perf_metric=perf_metric)
    tbl.to_csv(out_csv, index=False)

    meta = {
        "diagnostic": "bdp_draft_rate_vs_poolq_loo",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "perf_metric": perf_metric,
        "panel_rows": "last-ps",
        "y_draft_mode": "ever",
        "poolq_binning": "equal_width",
        "n_bins": int(n_bins),
        "poolq_winsor": list(WINSOR),
        "lpm_quadratic": coef,
        "n_panel_rows": int(len(panel)),
        "n_binned_rows": int(tbl["n"].sum()),
        "outputs": {"png": out_png.name, "bins_csv": out_csv.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_csv.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def run_draft_rate_loo_vs_tj(
    spec: BdpSpec,
    *,
    out_png: Path,
    out_meta_dir: Path,
    prefix: str = "REIGNING",
    n_bins: int = N_BINS_EW,
) -> Path:
    """2×2 HERO: EW + quantile rows; poolq_LOO (left) vs T̂_j (right)."""
    panel = _prepare_last_ps(spec)
    tbl_loo_ew = _loo_ventile_table(panel, n_bins=n_bins, poolq_binning="equal_width")
    tbl_tj_ew = _t_j_ventile_table(panel, n_bins=n_bins, poolq_binning="equal_width")
    tbl_loo_q = _loo_ventile_table(panel, n_bins=n_bins, poolq_binning="quantile")
    tbl_tj_q = _t_j_ventile_table(panel, n_bins=n_bins, poolq_binning="quantile")
    coef_loo = _quadratic_lpm_coef(panel)
    coef_tj = _quadratic_lpm_coef_t_j(panel)

    stem = f"{prefix}_BDP_draft_rate_poolq_loo_vs_Tj_{spec.slug}_ew{n_bins}_ppm_lastps"
    out_png = out_png.parent / f"{stem}.png"
    out_meta = out_meta_dir / f"{stem}.json"
    out_csv_loo_ew = out_meta_dir / f"{stem}_poolq_loo_ew.csv"
    out_csv_tj_ew = out_meta_dir / f"{stem}_Tj_ew.csv"
    out_csv_loo_q = out_meta_dir / f"{stem}_poolq_loo_quantile.csv"
    out_csv_tj_q = out_meta_dir / f"{stem}_Tj_quantile.csv"

    _plot_draft_rate_loo_vs_tj(
        tbl_loo_ew,
        tbl_tj_ew,
        tbl_loo_q,
        tbl_tj_q,
        coef_loo,
        coef_tj,
        spec=spec,
        png_path=out_png,
        n_bins=n_bins,
    )
    tbl_loo_ew.to_csv(out_csv_loo_ew, index=False)
    tbl_tj_ew.to_csv(out_csv_tj_ew, index=False)
    tbl_loo_q.to_csv(out_csv_loo_q, index=False)
    tbl_tj_q.to_csv(out_csv_tj_q, index=False)

    meta = {
        "diagnostic": "bdp_draft_rate_poolq_loo_vs_Tj",
        "date": date.today().isoformat(),
        "bdp_spec": spec.label,
        "panel_rows": "last-ps",
        "y_draft_mode": "ever",
        "n_bins": int(n_bins),
        "poolq_binning_rows": {
            "top": "equal_width",
            "bottom": "quantile",
        },
        "poolq_winsor": list(WINSOR),
        "left_axis": "poolq_loo (player LOO teammate mean; self excluded)",
        "right_axis": "t_j_hat (team-season mean perf z; includes self; winsor on T_j)",
        "lpm_poolq_loo": coef_loo,
        "lpm_t_j": coef_tj,
        "n_panel_rows": int(len(panel)),
        "outputs": {
            "png": out_png.name,
            "poolq_loo_ew_csv": out_csv_loo_ew.name,
            "t_j_ew_csv": out_csv_tj_ew.name,
            "poolq_loo_quantile_csv": out_csv_loo_q.name,
            "t_j_quantile_csv": out_csv_tj_q.name,
        },
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_png.relative_to(REPO)}")
    print(f"Wrote {out_csv_loo_ew.relative_to(REPO)}")
    print(f"Wrote {out_csv_tj_ew.relative_to(REPO)}")
    print(f"Wrote {out_csv_loo_q.relative_to(REPO)}")
    print(f"Wrote {out_csv_tj_q.relative_to(REPO)}")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="Player poolq_LOO distribution + draft-rate porch plots.")
    parser.add_argument("--spec", default="mg10 min20 09_21")
    parser.add_argument("--prefix", default="REIGNING")
    parser.add_argument(
        "--only",
        nargs="+",
        choices=("loo_dist", "draft_rate_loo", "draft_rate_loo_tj"),
        help="Subset (default: both).",
    )
    parser.add_argument("--out-dir", type=Path, default=BASIC_DATA_PLOTS)
    args = parser.parse_args()

    ensure_hero_dirs()
    spec = parse_bdp_spec(args.spec)
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    keys = args.only or ["loo_dist", "draft_rate_loo", "draft_rate_loo_tj"]
    for key in keys:
        if key == "loo_dist":
            run_poolq_loo_distribution(
                spec,
                out_png=out_dir / "poolq_loo_dist.png",
                out_meta_dir=out_dir,
                prefix=args.prefix,
            )
        elif key == "draft_rate_loo":
            run_draft_rate_vs_loo(
                spec,
                out_png=out_dir / "draft_rate_loo.png",
                out_meta_dir=out_dir,
                prefix=args.prefix,
            )
        elif key == "draft_rate_loo_tj":
            run_draft_rate_loo_vs_tj(
                spec,
                out_png=out_dir / "draft_rate_loo_tj.png",
                out_meta_dir=out_dir,
                prefix=args.prefix,
            )


if __name__ == "__main__":
    main()
