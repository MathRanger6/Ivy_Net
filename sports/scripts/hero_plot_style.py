"""Shared bar-chart layout for HERO / CCT / elite-pond figures."""

from __future__ import annotations

import textwrap
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np

PLOT_DPI = 300
# Wrap only when line would exceed typical axes width (~10.5 in figure).
TITLE_WRAP_CHARS = 78
FOOTER_WRAP_CHARS = 96


def wrap_lines(text: str, width: int) -> list[str]:
    t = str(text).strip()
    if not t:
        return []
    return textwrap.wrap(t, width=width)


def set_wrapped_ax_title(ax, lines: Iterable[str], *, fontsize: float = 10, pad: float = 8) -> None:
    parts: list[str] = []
    for line in lines:
        parts.extend(wrap_lines(line, TITLE_WRAP_CHARS) or [""])
    ax.set_title("\n".join(parts), fontsize=fontsize, pad=pad)


def stamp_wrapped_footer(
    fig,
    lines: Iterable[str],
    *,
    margin_floor: float = 0.003,
    fontsize: float = 7.5,
    line_spacing: float = 0.013,
    text_height: float = 0.014,
) -> float:
    """Stamp footer lines at figure bottom; return top of footer block (figure coords)."""
    wrapped: list[str] = []
    for line in lines:
        wrapped.extend(wrap_lines(line, FOOTER_WRAP_CHARS) or [""])
    wrapped = [w for w in wrapped if w.strip()]
    for i, line in enumerate(wrapped):
        fig.text(
            0.5,
            margin_floor + i * line_spacing,
            line,
            ha="center",
            va="bottom",
            fontsize=fontsize,
            color="0.35",
        )
    if not wrapped:
        return margin_floor
    return margin_floor + (len(wrapped) - 1) * line_spacing + text_height


def layout_bar_figure(
    fig,
    *,
    top: float = 0.90,
    bottom: float = 0.11,
    left: float = 0.10,
    right: float = 0.96,
    footer_lines: int = 0,
    rotated_x: bool = False,
) -> None:
    """Legacy helper — prefer ``finalize_bar_figure`` for footer + margin together."""
    if rotated_x:
        bottom = 0.19 if footer_lines >= 2 else 0.17
    elif footer_lines >= 3:
        bottom = 0.13
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right)


def finalize_bar_figure(
    fig,
    footer_lines: Iterable[str],
    *,
    rotated_x: bool = False,
    top: float = 0.90,
    left: float = 0.10,
    right: float = 0.96,
) -> None:
    """Footer pinned to figure bottom; axes bottom margin fits x-label (+ rotated ticks)."""
    wrapped: list[str] = []
    for line in footer_lines:
        wrapped.extend(wrap_lines(line, FOOTER_WRAP_CHARS) or [""])
    wrapped = [w for w in wrapped if w.strip()]
    n = len(wrapped)
    if rotated_x:
        bottom = 0.19 if n >= 2 else 0.17
    elif n >= 3:
        bottom = 0.13
    else:
        bottom = 0.11
    fig.subplots_adjust(top=top, bottom=bottom, left=left, right=right)
    if wrapped:
        stamp_wrapped_footer(fig, wrapped)


def format_poolq_tick(val: float) -> str:
    v = float(val)
    if not np.isfinite(v):
        return ""
    if abs(v) < 1.5:
        return f"{v:.2f}"
    return f"{v:.2g}"


def count_weighted_bar_colors(counts: np.ndarray, *, cmap_name: str = "Blues") -> list:
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


def label_color_for_bar(facecolor) -> str:
    from matplotlib.colors import to_rgba

    rgba = to_rgba(facecolor)
    lum = 0.299 * float(rgba[0]) + 0.587 * float(rgba[1]) + 0.114 * float(rgba[2])
    return "0.15" if lum > 0.62 else "white"


def annotate_bar_n(
    ax,
    x: np.ndarray,
    y: np.ndarray,
    counts: np.ndarray,
    bar_colors: list,
) -> None:
    ymin, ymax = ax.get_ylim()
    span = ymax - ymin if ymax > ymin else 1.0
    for i, (xi, yi, n) in enumerate(zip(x, y, counts, strict=True)):
        ni = int(n)
        if ni <= 0:
            continue
        yi_f = float(yi)
        if yi_f < span * 0.12:
            y_pos = yi_f + span * 0.015
            rotation = 0
            fontsize = 7
            va = "bottom"
            color = "0.25"
        else:
            y_pos = ymin + span * 0.22
            rotation = 90
            fontsize = 7.5
            va = "bottom"
            color = label_color_for_bar(bar_colors[i])
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
