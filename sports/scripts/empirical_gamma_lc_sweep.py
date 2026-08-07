#!/usr/bin/env python3
"""PD17 — Empirical γ sweep: team L_C distribution on real rosters.

Same panel and θ (K/N quantile on PPM z); only γ in σ(γ(Â−θ)) varies.
Mirrors Phase B L_C strip layout (HAND slide ~15) on empirical data.

Run (repo root):
  python sports/scripts/empirical_gamma_lc_sweep.py

Outputs (HEROs_and_PASSes/empirical_pd17/):
  EMPIRICAL_L_C_gamma_sweep_strip.png
  EMPIRICAL_L_C_gamma_sweep_summary.csv
  EMPIRICAL_L_C_gamma_sweep_meta.json
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

import empirical_lc_distributions as elc
from hero_gallery_paths import EMPIRICAL_PD17, ensure_hero_dirs

OUT = EMPIRICAL_PD17
PNG_STRIP = OUT / "EMPIRICAL_L_C_gamma_sweep_strip.png"
CSV_SUMMARY = OUT / "EMPIRICAL_L_C_gamma_sweep_summary.csv"
META_JSON = OUT / "EMPIRICAL_L_C_gamma_sweep_meta.json"

GAMMA_ARMS: list[float] = [10.0, 5.0, 1.0, 0.5, 0.001]

SINGLE_PANEL_W = 2.15
SINGLE_PANEL_H = 5.5
X_LABEL = r"$L_C$"
X_TICKS = [0.0, 0.5, 1.0]


def _gamma_label(gamma: float) -> str:
    if gamma < 0.01:
        return "gamma_approx_0"
    g = float(gamma)
    return f"gamma_{g:g}".replace(".", "p")


def _gamma_panel_title(gamma: float) -> str:
    line = rf"$\gamma={gamma:g}$" if gamma >= 0.01 else r"$\gamma \approx 0$"
    return line + "\n" + rf"{elc.N_LC_BINS} bins"


def _style_gamma_axes(ax, *, show_ylabel: bool = True) -> None:
    ax.set_xlim(0.0, 1.0)
    ax.set_xticks(X_TICKS)
    ax.tick_params(axis="x", labelbottom=True, labelsize=7)
    ax.tick_params(axis="y", labelsize=7)
    ax.set_xlabel(X_LABEL, fontsize=9)
    if show_ylabel:
        ax.set_ylabel("Teams", fontsize=8)


def _histogram_curve(lc: np.ndarray, *, bins: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    counts, edges = np.histogram(lc, bins=bins)
    centers = 0.5 * (edges[:-1] + edges[1:])
    return centers, counts.astype(float)


def _global_ymax(lc_by_gamma: dict[float, np.ndarray], lc_edges: np.ndarray) -> float:
    ymax = 0.0
    for lc in lc_by_gamma.values():
        _, counts = _histogram_curve(lc, bins=lc_edges)
        if counts.size:
            ymax = max(ymax, float(counts.max()))
    return ymax * 1.06 if ymax > 0 else 1.0


def _arm_summary(gamma: float, lc: np.ndarray) -> dict:
    lc = lc[np.isfinite(lc)]
    return {
        "gamma": float(gamma),
        "label": _gamma_label(gamma),
        "n_team_seasons": int(lc.size),
        "L_C_mean": float(lc.mean()) if lc.size else float("nan"),
        "L_C_std": float(lc.std()) if lc.size else float("nan"),
        "L_C_min": float(lc.min()) if lc.size else float("nan"),
        "L_C_max": float(lc.max()) if lc.size else float("nan"),
        "frac_L_C_below_0.05": float((lc < 0.05).mean()) if lc.size else float("nan"),
        "frac_L_C_above_0.5": float((lc > 0.5).mean()) if lc.size else float("nan"),
    }


def build_strip(
    lc_by_gamma: dict[float, np.ndarray],
    *,
    theta: float,
    k_over_n: float,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    lc_edges = np.linspace(0.0, 1.0, elc.N_LC_BINS + 1)
    bin_width = lc_edges[1] - lc_edges[0]
    y_top = _global_ymax(lc_by_gamma, lc_edges)

    items = [(g, lc_by_gamma[g]) for g in GAMMA_ARMS if g in lc_by_gamma]
    n = len(items)
    fig_w = SINGLE_PANEL_W * n
    fig, axes = plt.subplots(
        1, n, figsize=(fig_w, SINGLE_PANEL_H), sharey=True, squeeze=False
    )
    axes = axes.ravel()

    for i, (ax, (gamma, lc)) in enumerate(zip(axes, items)):
        centers, counts = _histogram_curve(lc, bins=lc_edges)
        ax.bar(
            centers,
            counts,
            width=bin_width * 0.98,
            align="center",
            color=elc.BAR_COLOR,
            alpha=elc.BAR_ALPHA,
            edgecolor=elc.BAR_COLOR,
            linewidth=0.3,
        )
        _style_gamma_axes(ax, show_ylabel=(i == 0))
        ax.set_ylim(0.0, y_top)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        stats = elc._summary("", lc)
        ax.text(
            0.03,
            0.97,
            rf"mean={stats['mean']:.3f}",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=7,
            bbox=dict(
                boxstyle="round,pad=0.2",
                facecolor="white",
                alpha=0.85,
                edgecolor="0.8",
            ),
        )
        ax.set_title(_gamma_panel_title(gamma), fontsize=10, linespacing=1.15, pad=10)

    fig.suptitle(
        rf"Empirical MBB — team $L_C$ vs $\gamma$ "
        rf"($\theta={theta:.3f}$ z-units, $K/N={k_over_n:.4f}$)",
        fontsize=12,
        y=0.97,
    )
    fig.subplots_adjust(left=0.06, right=0.99, top=0.78, bottom=0.12, wspace=0.14)
    fig.savefig(PNG_STRIP, dpi=150, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(f"Wrote {PNG_STRIP}")


def main() -> None:
    ensure_hero_dirs()

    panel = elc._prepare_panel()
    panel = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    ability = panel["perf"].to_numpy(dtype=float)
    n_drafted = int(panel["Y_draft"].sum())
    n_total = int(len(panel))
    k_over_n = n_drafted / n_total if n_total else float("nan")
    theta = float(np.quantile(ability, 1.0 - k_over_n))

    lc_by_gamma: dict[float, np.ndarray] = {}
    summary_rows: list[dict] = []

    for gamma in GAMMA_ARMS:
        print(f"Computing team L_C at gamma={gamma:g} ...")
        team_df = elc._attach_team_lc(panel, theta=theta, gamma=gamma)
        lc = team_df["L_C"].dropna().to_numpy(dtype=float)
        lc_by_gamma[gamma] = lc
        summary_rows.append(_arm_summary(gamma, lc))

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(CSV_SUMMARY, index=False)
    print(f"Wrote {CSV_SUMMARY}")
    print(summary_df.to_string(index=False))

    build_strip(lc_by_gamma, theta=theta, k_over_n=k_over_n)

    meta = {
        "diagnostic": "empirical_gamma_lc_sweep",
        "date": date.today().isoformat(),
        "source": "MBB player-season panel (530 pipeline / hero filters)",
        "seasons": "2011-2021",
        "perf": "PPM z within season",
        "lc_mode": "crowding_smooth_team",
        "theta_mode": "empirical_k_over_n_quantile",
        "theta": theta,
        "theta_K_over_N": {
            "n_accepted": n_drafted,
            "n_total": n_total,
            "K_over_N": k_over_n,
            "theta_quantile": 1.0 - k_over_n,
        },
        "gamma_arms": GAMMA_ARMS,
        "lc_bins": elc.N_LC_BINS,
        "summary": summary_rows,
        "outputs": {
            "png_strip": PNG_STRIP.name,
            "csv": CSV_SUMMARY.name,
        },
    }
    META_JSON.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {META_JSON}")
    print("Done.")


if __name__ == "__main__":
    main()
