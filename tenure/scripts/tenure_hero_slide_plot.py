#!/usr/bin/env python3
"""MBB-style HERO slide panel for tenure (single bar chart + LPM readout).

Mirrors pass_a_empirical_bundle.build_hero_single_panel layout for deck parity.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _bin_label(bin_method: str, n_bins: int) -> str:
    kind = "QTL" if bin_method == "quantile" else "EW"
    return f"{kind}{n_bins}"


def _x_mathtext(x_metric: str, *, pool_perf: str = "annual") -> str:
    if x_metric == "own_cum":
        return r"$\mathrm{cum\ pubs}$"
    if pool_perf == "cumulative" and x_metric == "loo":
        return r"$\mathrm{LOO}_{\mathrm{cum}}$"
    return r"$\mathrm{poolq\_LOO}$" if x_metric == "loo" else r"$\mathrm{poolq}$"


def _spec_subtitle(
    n_bins: int,
    bin_method: str,
    x_metric: str,
    *,
    grain: str = "spell_mean",
    pool_perf: str = "annual",
) -> str:
    bin_lbl = _bin_label(bin_method, n_bins)
    xtex = _x_mathtext(x_metric, pool_perf=pool_perf)
    if grain == "last_asst" and pool_perf == "cumulative":
        return rf"{bin_lbl} · last-ps · {xtex} cum pubs · Option A"
    if grain == "last_asst" and x_metric == "own_cum":
        return rf"{bin_lbl} · last-ps · own {xtex} · Option A"
    if grain == "last_asst":
        return rf"{bin_lbl} · last-ps · {xtex} · Option A"
    return rf"{bin_lbl} · {xtex} · person-level mean · Option A"


def quadratic_lpm_tenure(
    persons: list[dict[str, Any]], *, exclude_censored: bool = True
) -> pd.Series:
    """OLS tenure ~ 1 + loo_mean + loo_mean_sq on resolved persons."""
    if exclude_censored:
        use = [p for p in persons if not p.get("censored")]
    else:
        use = list(persons)
    y = np.array([float(p["tenure"]) for p in use], dtype=float)
    p = np.array([float(p["loo_mean"]) for p in use], dtype=float)
    q = p**2
    mask = np.isfinite(y) & np.isfinite(p) & np.isfinite(q)
    x_mat = np.column_stack([np.ones(mask.sum()), p[mask], q[mask]])
    beta, *_ = np.linalg.lstsq(x_mat, y[mask], rcond=None)
    return pd.Series(beta, index=["const", "loo_mean", "loo_mean_sq"])


def shape_summary_from_binned_csv(csv_path: Path, *, coef: pd.Series | None = None) -> dict:
    if not csv_path.is_file():
        return {}
    df = pd.read_csv(csv_path)
    if df.empty or "tenure_rate" not in df.columns:
        return {}
    plot = df.loc[df["tenure_rate"].notna()].copy()
    if plot.empty:
        return {}
    peak_idx = int(plot["tenure_rate"].idxmax())
    peak = plot.loc[peak_idx]
    bin0 = plot.loc[plot["bin"].idxmin()] if "bin" in plot.columns else plot.iloc[0]
    last = plot.iloc[-1]
    beta_sq = None
    if coef is not None and "loo_mean_sq" in coef.index:
        beta_sq = float(coef["loo_mean_sq"])
    peak_bin = int(peak.get("bin", peak_idx + 1)) - 1
    bin0_bin = int(bin0.get("bin", 1)) - 1
    return {
        "peak_vent": peak_bin,
        "peak_rate_pct": round(100 * float(peak["tenure_rate"]), 3),
        "bin0_rate_pct": round(100 * float(bin0["tenure_rate"]), 3),
        "last_bin_rate_pct": round(100 * float(last["tenure_rate"]), 3),
        "bin0_is_peak": bool(peak_bin == bin0_bin),
        "beta_sq": beta_sq,
    }


def _count_weighted_bar_colors(counts: np.ndarray, *, cmap_name: str = "Blues") -> list:
    """Map bin row counts to bar face colors (light = sparse, dark = dense)."""
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
    r, g, b = float(rgba[0]), float(rgba[1]), float(rgba[2])
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return "0.15" if lum > 0.62 else "white"


def _annotate_bin_n_on_bar(
    ax,
    x: np.ndarray,
    y: np.ndarray,
    counts: np.ndarray,
    bar_colors: list | None = None,
    *,
    rotation: float = 90.0,
    y_frac: float = 0.10,
) -> None:
    """Label each bar with bin population on the bar face (MBB BDP equal-width style)."""
    for i, (xi, yi, n) in enumerate(zip(x, y, counts, strict=True)):
        ni = int(n)
        if ni <= 0 or float(yi) <= 0:
            continue
        y_pos = max(float(yi) * y_frac, 0.0015)
        txt_color = "white"
        if bar_colors is not None and i < len(bar_colors):
            txt_color = _label_color_for_bar(bar_colors[i])
        ax.text(
            xi,
            y_pos,
            f"{ni:,}",
            ha="center",
            va="bottom",
            fontsize=7,
            rotation=rotation,
            color=txt_color,
            fontweight="bold",
            clip_on=True,
        )


def _x_axis_label(
    bin_method: str,
    x_metric: str,
    *,
    pool_perf: str = "annual",
) -> str:
    xtex = _x_mathtext(x_metric, pool_perf=pool_perf)
    kind = "Quantile" if bin_method == "quantile" else "Equal-width"
    if pool_perf == "cumulative" and x_metric == "loo":
        return rf"{kind} bin ($1$ = lowest peer cum pubs LOO)"
    if x_metric == "own_cum":
        return rf"{kind} bin ($1$ = lowest own cumulative pubs)"
    return rf"{kind} bin ($1$ = lowest {xtex})"


def _lpm_annotation(coef: pd.Series) -> str | None:
    if "loo_mean_sq" not in coef.index:
        return None
    b2 = float(coef["loo_mean_sq"])
    if b2 < 0:
        return rf"LPM: $\beta_2={b2:.4g}$ ($<0$, concave)"
    return rf"LPM: $\beta_2={b2:+.4g}$ (flat / not concave on this panel)"


def _tenure_footer(
    *,
    n_bins: int,
    bin_method: str,
    x_metric: str,
    n_persons: int,
    n_tenure: int,
    n_resolved: int,
    grain: str = "spell_mean",
    pool_perf: str = "annual",
) -> str:
    grain_bit = "last-ps" if grain == "last_asst" else "spell-mean"
    if x_metric == "own_cum":
        perf_bit = "own cum pubs"
    else:
        perf_bit = "cum-pubs LOO" if pool_perf == "cumulative" else "annual LOO"
    return (
        f"HERO · {_x_mathtext(x_metric, pool_perf=pool_perf).strip('$')} · {_bin_label(bin_method, n_bins)} · "
        f"{grain_bit} · {perf_bit} · infHM · resolved-only · "
        f"n={n_persons:,} · tenure={n_tenure:,} · resolved={n_resolved:,} · "
        f"{date.today().isoformat()}"
    )


def build_hero_slide_panel(
    csv_path: Path,
    out_png: Path,
    *,
    persons: list[dict[str, Any]],
    n_bins: int,
    bin_method: str = "quantile",
    x_metric: str = "loo",
    grain: str = "spell_mean",
    pool_perf: str = "annual",
    exclude_censored: bool = True,
    stage9_summary: dict[str, Any] | None = None,
) -> tuple[pd.Series, dict]:
    """Write MBB-format single-panel tenure HERO PNG."""
    sys_path = Path(__file__).resolve().parents[2] / "sports" / "scripts"
    import sys

    sys.path.insert(0, str(sys_path))
    from gallery_mathtext import configure_matplotlib_mathtext
    from plot_provenance import stamp_figure_footer

    configure_matplotlib_mathtext()

    df = pd.read_csv(csv_path)
    plot = df.loc[df["tenure_rate"].notna()].copy()
    if plot.empty:
        raise ValueError(f"No resolved bins in {csv_path}")

    coef = quadratic_lpm_tenure(persons, exclude_censored=exclude_censored)
    shape = shape_summary_from_binned_csv(csv_path, coef=coef)

    x = plot["bin"].to_numpy(dtype=float)
    y = plot["tenure_rate"].to_numpy(dtype=float)
    n_res = plot["n_resolved"].to_numpy(dtype=int)
    n_all = plot["n_all"].to_numpy(dtype=int)

    summ = stage9_summary or {}
    n_persons = int(summ.get("n_persons_with_loo", len(persons)))
    n_tenure = int(summ.get("n_tenure", sum(p["tenure"] for p in persons)))
    n_resolved = int(summ.get("n_resolved", sum(1 for p in persons if not p["censored"])))

    xlab = _x_axis_label(bin_method, x_metric, pool_perf=pool_perf)
    equal_width = bin_method == "equal_width"

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    if equal_width:
        bar_colors = _count_weighted_bar_colors(n_res, cmap_name="Blues")
        ax.bar(x, y, color=bar_colors, edgecolor="white", alpha=0.95, width=0.82, linewidth=0.6)
    else:
        bar_colors = None
        ax.bar(x, y, color="steelblue", edgecolor="white", alpha=0.9, width=0.82)
    ax.set_xlabel(xlab)
    ax.set_ylabel(r"Mean $Y_{\mathrm{tenure}}$ (resolved only)")
    if x_metric == "own_cum":
        title_line = "Empirical hero — own cumulative pubs (last-ps · ability)"
    elif grain == "last_asst" and pool_perf == "cumulative":
        title_line = "Empirical hero — last-ps peer cumulative stock"
    else:
        title_line = "Empirical hero — peer pool context · tenure inference panel"
    ax.set_title(
        rf"{title_line}\n" + _spec_subtitle(
            n_bins, bin_method, x_metric, grain=grain, pool_perf=pool_perf
        ),
        fontsize=10,
    )
    ax.set_xticks(x)
    ax.set_ylim(0, min(1.0, max(y) * 1.18 + 0.02))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    if equal_width:
        _annotate_bin_n_on_bar(ax, x, y, n_res, bar_colors)
    else:
        # Quantile: equal n_all per bin; n_resolved varies (censored uneven by LOO).
        for xi, yi, ni_res, ni_all in zip(x, y, n_res, n_all, strict=True):
            ax.text(
                xi,
                yi + 0.015,
                f"{ni_res}/{ni_all}",
                ha="center",
                va="bottom",
                fontsize=7,
                color="0.35",
            )
        ax.text(
            0.98,
            0.02,
            "bar label = resolved / all (quantile ≈ equal all)",
            transform=ax.transAxes,
            fontsize=7,
            ha="right",
            va="bottom",
            color="0.45",
        )

    note = _lpm_annotation(coef)
    if note:
        ax.text(0.02, 0.96, note, transform=ax.transAxes, fontsize=8, va="top")
    if equal_width:
        ax.text(
            0.98,
            0.02,
            "bar shade ∝ bin n (dark = more resolved) · n on bar face",
            transform=ax.transAxes,
            fontsize=7,
            ha="right",
            va="bottom",
            color="0.45",
        )

    footer = _tenure_footer(
        n_bins=n_bins,
        bin_method=bin_method,
        x_metric=x_metric,
        n_persons=n_persons,
        n_tenure=n_tenure,
        n_resolved=n_resolved,
        grain=grain,
        pool_perf=pool_perf,
    )
    stamp_figure_footer(fig, footer)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return coef, shape


def write_lpm_txt(path: Path, coef: pd.Series, *, meta: dict[str, Any]) -> None:
    b2 = float(coef["loo_mean_sq"])
    lines = [
        f"# Tenure hero Layer A — quadratic LPM ({date.today().isoformat()})",
        f"n={meta.get('n_resolved', '?')} resolved persons",
        f"tenure events: {meta.get('n_tenure', '?')}",
        f"x_metric={meta.get('x_metric', 'loo')}",
        f"n_bins={meta.get('n_bins')} bin_method={meta.get('bin_method')}",
        "",
        "Model: tenure ~ const + loo_mean + loo_mean_sq (resolved only)",
        "",
        coef.to_string(),
        "",
        f"Interpretation: beta_loo_mean_sq = {b2:.6g} "
        f"({'concave / inverted-U consistent' if b2 < 0 else 'not concave on this panel'})",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
