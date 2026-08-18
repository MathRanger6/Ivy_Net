"""Shared PD22 AUTO slide copy (box QC policy, Aug 2026).

HAND deck convention: wrap numbers and operators in one $...$ block when possible
(e.g. $\\leq 10$ not $\\leq$ 10; $4{,}135\\rightarrow4{,}248$ not $4{,}135$ $\\rightarrow$ $4{,}248$)
so Charles can paste into PowerPoint formulas.
"""

from __future__ import annotations

# Canonical match for PipelineConfig.min_team_season_games default (keep >= MIN+1 games).
MIN_TEAM_SEASON_GAMES = 10
KEEP_MIN_TEAM_SEASON_GAMES = MIN_TEAM_SEASON_GAMES + 1

BOX_QC_POLICY_REF = r"Policy: \texttt{pd22\_minutes/BOX\_QC\_panel\_build\_policy.md}."


def m(n: int | float, *, decimals: int | None = None) -> str:
    """Numeric literal in math mode."""
    if decimals is not None:
        return rf"${n:.{decimals}f}$"
    if isinstance(n, float) and n == int(n):
        n = int(n)
    if isinstance(n, int):
        return rf"${n:,}$"
    return rf"${n:g}$"


def mleq(n: int | float) -> str:
    return rf"$\leq {n:g}$"


def mgeq(n: int | float) -> str:
    return rf"$\geq {n:g}$"


def mgt(n: int | float) -> str:
    return rf"$> {n:g}$"


def mlt(n: int | float) -> str:
    return rf"$< {n:g}$"


def mpct(x: float, decimals: int = 1) -> str:
    return rf"${x:.{decimals}f}\%$"


def mapprox(x: int | float) -> str:
    return rf"$\approx {x:g}$"


def msim(x: int | float) -> str:
    return rf"$\sim {x:g}$"


def _fmt_num(n: int | float, *, decimals: int | None = None) -> str:
    """Numeric literal inside math mode (no $ delimiters)."""
    if decimals is not None:
        return f"{n:.{decimals}f}"
    if isinstance(n, float) and n == int(n):
        n = int(n)
    if isinstance(n, int):
        return f"{n:,}"
    return f"{n:g}"


def marrow(a: int | float, b: int | float, *, decimals: int | None = None) -> str:
    """Single math block for a → b (HAND formula paste)."""
    return rf"${_fmt_num(a, decimals=decimals)}\rightarrow{_fmt_num(b, decimals=decimals)}$"


BOX_QC_PANEL_NOTE = (
    r"Box QC at panel build: drop dash-name placeholders; keep team-seasons with "
    rf"{mgeq(KEEP_MIN_TEAM_SEASON_GAMES)} distinct games in box (frozen CSV untouched)."
)
