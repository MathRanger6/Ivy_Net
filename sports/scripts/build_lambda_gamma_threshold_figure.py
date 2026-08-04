#!/usr/bin/env python3
"""Educational figure: soft viability σ(γ(A−θ)) and λ_crit ≈ 4/γ.

Sort-and-chop threshold story — γ shapes L_C; λ must exceed 4/γ before
congestion reorders selection at the θ knee.

Run (repo root):
  python sports/scripts/build_lambda_gamma_threshold_figure.py

Output:
  3-Master_Plan/re_entry/HEROs_and_PASSes/sort_chop_lambda/LAMBDA_threshold_gamma_viability.png
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from hero_gallery_paths import SORT_CHOP_LAMBDA, ensure_hero_dirs

OUT = SORT_CHOP_LAMBDA
PNG = OUT / "LAMBDA_threshold_gamma_viability.png"

from gallery_mathtext import configure_matplotlib_mathtext

# 539 selection preset (sort-and-chop λ diagnostic uses these)
THETA = 0.72
GAMMA_DEFAULT = 10.0
GAMMA_COMPARE = (5.0, 10.0, 20.0)
GAMMA_COLORS = {5.0: "#2ca02c", 10.0: "#1f77b4", 20.0: "#d62728"}


def _sigma(a: np.ndarray, *, theta: float, gamma: float) -> np.ndarray:
    z = np.clip(gamma * (a - theta), -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(-z))


def build_figure() -> None:
    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6))

    # --- Left: viability curves -----------------------------------------------
    ax0 = axes[0]
    a = np.linspace(0.0, 1.0, 400)
    for gamma in GAMMA_COMPARE:
        y = _sigma(a, theta=THETA, gamma=gamma)
        ax0.plot(
            a,
            y,
            lw=2.4 if gamma == GAMMA_DEFAULT else 2.0,
            color=GAMMA_COLORS[gamma],
            label=rf"$\gamma={gamma:g}$  ($\lambda_{{\mathrm{{crit}}}}\approx{4/gamma:.2f}$)",
        )
        slope = gamma / 4.0
        ax0.plot(
            THETA,
            0.5,
            "o",
            ms=7,
            color=GAMMA_COLORS[gamma],
            zorder=5,
        )
        # Tangent at θ: steepest slope γ/4 — extend across full A axis (clipped by axes)
        x_tan = np.array([0.0, 1.0])
        y_tan = 0.5 + slope * (x_tan - THETA)
        ax0.plot(
            x_tan,
            y_tan,
            "--",
            lw=1.2,
            alpha=0.55,
            color=GAMMA_COLORS[gamma],
            clip_on=True,
        )

    ax0.axvline(THETA, color="0.45", ls=":", lw=1.2)
    ax0.text(
        THETA + 0.012,
        0.04,
        rf"$\theta={THETA:g}$",
        fontsize=10,
        color="0.35",
    )
    ax0.set_xlim(0, 1)
    ax0.set_ylim(-0.02, 1.05)
    ax0.set_xlabel(r"Ability $A$ (539 unit interval)")
    ax0.set_ylabel(r"Soft viability $\sigma(\gamma(A-\theta))$")
    ax0.set_title(
        r"Peer viability (smooth $L_C$ kernel)"
        "\n"
        r"dashed: tangent slope $=\gamma/4$ at $\theta$",
        fontsize=11,
    )
    ax0.legend(loc="upper left", fontsize=8.5, framealpha=0.92)

    # --- Right: λ_crit vs γ ---------------------------------------------------
    ax1 = axes[1]
    gamma_grid = np.linspace(2.0, 25.0, 200)
    lam_crit = 4.0 / gamma_grid
    ax1.plot(gamma_grid, lam_crit, color="0.25", lw=2.2)
    for gamma in GAMMA_COMPARE:
        lc = 4.0 / gamma
        ax1.scatter(
            [gamma],
            [lc],
            s=90,
            color=GAMMA_COLORS[gamma],
            zorder=5,
            edgecolors="white",
            linewidths=0.8,
        )
        ax1.annotate(
            rf"$\gamma={gamma:g}$" + "\n" + rf"$\lambda_{{\mathrm{{crit}}}}={lc:.2f}$",
            xy=(gamma, lc),
            xytext=(12, 10 if gamma != 20 else -28),
            textcoords="offset points",
            fontsize=9,
            color=GAMMA_COLORS[gamma],
            arrowprops=dict(arrowstyle="->", color=GAMMA_COLORS[gamma], lw=1.0),
        )

    ax1.axhline(4.0 / GAMMA_DEFAULT, color=GAMMA_COLORS[GAMMA_DEFAULT], ls=":", lw=1.1, alpha=0.7)
    ax1.scatter(
        [GAMMA_DEFAULT],
        [4.0 / GAMMA_DEFAULT],
        s=120,
        facecolors="none",
        edgecolors=GAMMA_COLORS[GAMMA_DEFAULT],
        linewidths=2.0,
        zorder=6,
        label=rf"539 default ($\gamma={GAMMA_DEFAULT:g}$)",
    )
    ax1.set_xlabel(r"Sharpness $\gamma$")
    ax1.set_ylabel(r"Critical $\lambda_{\mathrm{crit}} \approx 4/\gamma$")
    ax1.set_title(
        r"Sort-and-chop: first reorder when $\lambda > \min(\Delta A/\Delta L)$"
        "\n"
        r"bottleneck at $\theta$ $\Rightarrow$ $\lambda_{\mathrm{crit}}\approx 4/\gamma$",
        fontsize=11,
    )
    ax1.set_xlim(0, 26)
    ax1.set_ylim(0, 2.05)
    ax1.legend(loc="upper right", fontsize=8.5, framealpha=0.92)

    fig.suptitle(
        r"Why $\lambda\approx 0.41$ on sort-and-chop (not $A_i$, not $T_j$)"
        "\n"
        rf"$S_i=A_i-\lambda L_C$; $\gamma$ only matters when $\lambda>0$ (crowding in score)",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout()
    ensure_hero_dirs()
    fig.savefig(PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG}")


if __name__ == "__main__":
    build_figure()
