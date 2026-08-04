#!/usr/bin/env python3
"""Educational figure: hard viability step vs smooth σ(γ(A−θ)).

Explains why L_C is ≈0 / ≈1 / interior — not literally binary — in code.

Run (repo root):
  python sports/scripts/build_viability_hard_vs_smooth_figure.py

Output:
  HEROs_and_PASSes/sort_chop_lambda/VIABILITY_hard_vs_smooth.png
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
PNG = OUT / "VIABILITY_hard_vs_smooth.png"

from gallery_mathtext import configure_matplotlib_mathtext

THETA = 0.72
GAMMA_DEFAULT = 10.0
GAMMA_COLORS = {5.0: "#2ca02c", 10.0: "#1f77b4", 20.0: "#d62728"}


def _sigma(a: np.ndarray, *, theta: float, gamma: float) -> np.ndarray:
    z = np.clip(gamma * (a - theta), -500.0, 500.0)
    return 1.0 / (1.0 + np.exp(-z))


def _hard(a: np.ndarray, *, theta: float) -> np.ndarray:
    return (a > theta).astype(float)


def build_figure() -> None:
    configure_matplotlib_mathtext()
    fig = plt.figure(figsize=(11, 8.0))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.35, 0.85, 0.45], hspace=0.42, wspace=0.28)

    a = np.linspace(0.0, 1.0, 500)

    # --- Top left: hard step --------------------------------------------------
    ax_hard = fig.add_subplot(gs[0, 0])
    y_hard = _hard(a, theta=THETA)
    ax_hard.plot(a, y_hard, color="0.15", lw=3, label=r"Hard: $\mathbb{1}[A>\theta]$")
    ax_hard.axvline(THETA, color="0.45", ls=":", lw=1.2)
    ax_hard.axhline(0, color="0.75", lw=0.8)
    ax_hard.axhline(1, color="0.75", lw=0.8)
    ax_hard.text(
        THETA + 0.015,
        0.08,
        rf"$\theta={THETA:g}$",
        fontsize=10,
        color="0.35",
    )
    ax_hard.annotate(
        "below θ → exactly 0",
        xy=(THETA - 0.18, 0.0),
        xytext=(0.12, 0.22),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="0.35", lw=1.0),
        color="0.25",
    )
    ax_hard.annotate(
        "above θ → exactly 1",
        xy=(THETA + 0.18, 1.0),
        xytext=(0.78, 0.78),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", color="0.35", lw=1.0),
        color="0.25",
    )
    ax_hard.set_xlim(0, 1)
    ax_hard.set_ylim(-0.08, 1.12)
    ax_hard.set_xlabel(r"Teammate ability $A_j$")
    ax_hard.set_ylabel(r"Viability weight")
    ax_hard.set_title(
        r"Hard rule (storybook)"
        "\n"
        r"peer counts only if $A_j > \theta$",
        fontsize=11,
    )
    ax_hard.legend(loc="center right", fontsize=9)

    # --- Top right: smooth σ at three γ ---------------------------------------
    ax_soft = fig.add_subplot(gs[0, 1])
    for gamma in (5.0, 10.0, 20.0):
        ax_soft.plot(
            a,
            _sigma(a, theta=THETA, gamma=gamma),
            lw=2.6 if gamma == GAMMA_DEFAULT else 2.0,
            color=GAMMA_COLORS[gamma],
            label=rf"$\gamma={gamma:g}$",
        )
    ax_soft.axvline(THETA, color="0.45", ls=":", lw=1.2)
    ax_soft.axhline(0.5, color="0.8", ls=":", lw=0.9)
    ax_soft.plot([THETA], [0.5], "ko", ms=5, zorder=5)
    ax_soft.text(
        THETA + 0.014,
        0.42,
        rf"$\theta={THETA:g}$",
        fontsize=10,
        color="0.35",
        va="top",
        ha="left",
    )

    # Zoom inset near θ
    inset = ax_soft.inset_axes([0.08, 0.48, 0.42, 0.46])
    a_zoom = np.linspace(THETA - 0.12, THETA + 0.12, 200)
    for gamma in (5.0, 10.0, 20.0):
        inset.plot(
            a_zoom,
            _sigma(a_zoom, theta=THETA, gamma=gamma),
            color=GAMMA_COLORS[gamma],
            lw=1.8,
        )
    inset.axvline(THETA, color="0.45", ls=":", lw=1.0)
    inset.axhline(0.5, color="0.8", ls=":", lw=0.8)
    inset.set_xlim(THETA - 0.11, THETA + 0.11)
    inset.set_ylim(0.05, 0.95)
    inset.set_title("zoom at θ", fontsize=8)
    inset.tick_params(labelsize=7)

    ax_soft.annotate(
        "never exactly 0 or 1\nat finite A",
        xy=(THETA - 0.05, 0.42),
        xytext=(0.08, 0.12),
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", color=GAMMA_COLORS[10.0], lw=1.0),
        color="0.25",
    )
    ax_soft.annotate(
        r"$\gamma\uparrow$ → sharper knee",
        xy=(THETA + 0.06, 0.88),
        xytext=(0.55, 0.92),
        fontsize=8.5,
        arrowprops=dict(arrowstyle="->", color=GAMMA_COLORS[20.0], lw=1.0),
        color="0.25",
    )
    ax_soft.set_xlim(0, 1)
    ax_soft.set_ylim(-0.02, 1.05)
    ax_soft.set_xlabel(r"Teammate ability $A_j$")
    ax_soft.set_ylabel(r"Soft viability $\sigma(\gamma(A_j-\theta))$")
    ax_soft.set_title(
        r"Smooth rule (code: crowding\_smooth)"
        "\n"
        r"$L_C$ = mean of these weights over LOO teammates",
        fontsize=11,
    )
    ax_soft.legend(
        loc="lower right",
        fontsize=8.5,
        framealpha=0.92,
        ncol=3,
        columnspacing=1.0,
        handletextpad=0.4,
    )

    # --- Middle: roster schematic (dots only — no caption overlay) ------------
    ax_roster = fig.add_subplot(gs[1, :])
    ax_roster.set_xlim(0, 1)
    ax_roster.set_ylim(0, 1)
    ax_roster.set_xlabel(r"Teammate ability $A_j$ on one $\theta$-straddle roster (14 LOO peers, NCAA)")
    ax_roster.set_yticks([])
    for spine in ("top", "right", "left"):
        ax_roster.spines[spine].set_visible(False)

    peer_a = np.array(
        [0.66, 0.68, 0.69, 0.70, 0.705, 0.715, 0.725, 0.735, 0.745, 0.755, 0.765, 0.78, 0.79, 0.82]
    )
    gamma = GAMMA_DEFAULT
    w_soft = _sigma(peer_a, theta=THETA, gamma=gamma)
    w_hard = _hard(peer_a, theta=THETA)
    lc_soft = float(w_soft.mean())
    lc_hard = float(w_hard.mean())

    y_dots = 0.55
    y_soft = 0.22
    y_hard = 0.08
    for aj, ws, wh in zip(peer_a, w_soft, w_hard):
        ax_roster.plot(aj, y_dots, "o", ms=9, color=GAMMA_COLORS[gamma], zorder=3)
        ax_roster.plot([aj, aj], [y_hard, y_dots - 0.08], color="0.85", lw=0.8, zorder=1)
        ax_roster.text(aj, y_soft, f"{ws:.2f}", ha="center", va="top", fontsize=6.5, color=GAMMA_COLORS[gamma])
        ax_roster.text(aj, y_hard, f"h:{wh:g}", ha="center", va="top", fontsize=6, color="0.45")

    ax_roster.axvline(THETA, color="0.45", ls="--", lw=1.4, zorder=2)
    ax_roster.text(
        THETA + 0.012,
        0.78,
        rf"$\theta={THETA:g}$",
        fontsize=10,
        color="0.35",
        ha="left",
    )
    ax_roster.text(
        0.99,
        y_dots,
        "each dot = one teammate",
        ha="right",
        va="center",
        fontsize=8,
        color="0.35",
    )

    # --- Bottom: caption strip (plain text — not drawn on top of dots) --------
    ax_cap = fig.add_subplot(gs[2, :])
    ax_cap.axis("off")
    cap_lines = [
        "Example: mean peer weight → L_C for one player on a straddle roster.",
        rf"Blue numbers = soft $\sigma(\gamma(A_j-\theta))$ at $\gamma={gamma:g}$; "
        rf"gray h: = hard $\mathbb{{1}}[A_j>\theta]$ (0 or 1 only).",
        rf"Average over 14 LOO peers: soft $\Rightarrow$ $L_C \approx {lc_soft:.2f}$ (interior); "
        rf"hard $\Rightarrow$ $L_C = {lc_hard:.2f}$ (still interior when roster mixes above/below $\theta$).",
    ]
    for i, line in enumerate(cap_lines):
        ax_cap.text(
            0.5,
            0.82 - i * 0.32,
            line,
            transform=ax_cap.transAxes,
            ha="center",
            va="top",
            fontsize=9.5 if i == 0 else 9,
            fontweight="bold" if i == 0 else "normal",
            color="0.12" if i == 0 else "0.25",
        )

    fig.suptitle(
        r"Hard vs smooth peer viability — why $L_C \approx 0$, interior, or $\approx 1$ (not exact)",
        fontsize=12,
        y=0.98,
    )
    ensure_hero_dirs()
    fig.savefig(PNG, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {PNG}")


if __name__ == "__main__":
    build_figure()
