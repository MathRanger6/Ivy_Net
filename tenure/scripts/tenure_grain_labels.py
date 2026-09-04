"""Tenure HERO/BDP window + stat labels (MBB-aligned grain naming).

Windows (person-years):
  all_ps   — all ranks in panel
  asst_ps  — assistant person-years only
  last_ps  — final assistant person-year (exit cross-section)

Stats:
  mean   — average over the window (person collapse for ASST-PS)
  cum    — stock through end of window
  annum  — single person-year value (replaces legacy "annual")
"""

from __future__ import annotations

import warnings

# Canonical tokens
ALL_PS = "all_ps"
ASST_PS = "asst_ps"
LAST_PS = "last_ps"
DECISION = "decision"

MEAN = "mean"
CUM = "cum"
ANNUM = "annum"

WINDOWS = frozenset({ALL_PS, ASST_PS, LAST_PS, DECISION})
STATS = frozenset({MEAN, CUM, ANNUM})

_LEGACY_WINDOW = {
    "spell_mean": ASST_PS,
    "last_asst": LAST_PS,
    "all_ps": ALL_PS,
    "asst_ps": ASST_PS,
    "last_ps": LAST_PS,
    "decision": DECISION,
}

_LEGACY_STAT = {
    "annual": ANNUM,
    "cumulative": CUM,
    "annum": ANNUM,
    "cum": CUM,
    "mean": MEAN,
}


def normalize_window(value: str) -> str:
    key = str(value).strip().lower()
    if key not in _LEGACY_WINDOW:
        raise ValueError(
            f"window must be one of {sorted(WINDOWS)}, got {value!r}"
        )
    return _LEGACY_WINDOW[key]


def normalize_stat(value: str) -> str:
    key = str(value).strip().lower()
    if key not in _LEGACY_STAT:
        raise ValueError(
            f"stat must be one of {sorted(STATS)}, got {value!r}"
        )
    return _LEGACY_STAT[key]


def warn_if_legacy_cli(*, grain: str | None, pool_perf: str | None) -> tuple[str, str]:
    """Map deprecated --grain / --pool-perf to window / stat with a warning."""
    if grain is None and pool_perf is None:
        raise ValueError("warn_if_legacy_cli requires grain or pool_perf")
    window = normalize_window(grain or ASST_PS)
    stat = normalize_stat(pool_perf or ANNUM)
    if grain is not None and grain not in WINDOWS:
        warnings.warn(
            f"--grain {grain!r} is deprecated; use --window {window!r}",
            DeprecationWarning,
            stacklevel=3,
        )
    if pool_perf is not None and pool_perf not in STATS:
        warnings.warn(
            f"--pool-perf {pool_perf!r} is deprecated; use --stat {stat!r}",
            DeprecationWarning,
            stacklevel=3,
        )
    return window, stat


def window_badge(window: str) -> str:
    w = normalize_window(window)
    return {"all_ps": "ALL-PS", "asst_ps": "ASST-PS", "last_ps": "LAST-PS", "decision": "DECISION"}[w]


def window_display_label(window: str, *, stat: str | None = None) -> str:
    w = normalize_window(window)
    if w == LAST_PS:
        return "LAST-PS (final assistant year)"
    if w == DECISION:
        return "DECISION (resolved exit · dept pond)"
    if w == ALL_PS:
        base = "ALL-PS (all person-years)"
    else:
        base = "ASST-PS (assistant person-years)"
    if stat is not None:
        s = normalize_stat(stat)
        if w == ASST_PS and s == MEAN:
            return f"{base} · mean"
    return base


def stamp_window_badge(
    ax,
    window: str,
    *,
    corner: str = "upper_right",
    y: float = 0.98,
) -> None:
    """Compact yellow badge — short window label only."""
    x, ha = (0.98, "right") if corner == "upper_right" else (0.02, "left")
    ax.text(
        x,
        y,
        window_badge(window),
        transform=ax.transAxes,
        ha=ha,
        va="top",
        fontsize=8,
        fontweight="bold",
        color="0.15",
        bbox={
            "boxstyle": "round,pad=0.2",
            "facecolor": "#FFF3CD",
            "edgecolor": "0.65",
            "alpha": 0.92,
        },
        zorder=10,
    )


def perf_display_label(*, x_metric: str, stat: str = ANNUM) -> str:
    s = normalize_stat(stat)
    if x_metric == "own_cum":
        return "own cumulative pubs"
    if x_metric == "own_career":
        return "own career pubs rate"
    if x_metric == "decision_loo":
        return "dept LOO career rate"
    if s == CUM:
        return "peer cumulative LOO"
    return "peer LOO (annum)"


def provenance_spec_label(*, window: str, stat: str, x_metric: str) -> str:
    w = normalize_window(window)
    s = normalize_stat(stat)
    badge = window_badge(w)
    if x_metric == "own_cum":
        return f"{badge} · own cum pubs (ability slice)"
    if w == DECISION and x_metric == "decision_loo":
        return f"{badge} · dept pond LOO · career rate"
    if w == DECISION and x_metric == "own_career":
        return f"{badge} · own career rate (ability slice)"
    if w == LAST_PS and s == CUM and x_metric == "loo":
        return f"{badge} · cum · peer LOO"
    if w == LAST_PS and s == ANNUM:
        return f"{badge} · annum · peer LOO"
    if w == ASST_PS and s == MEAN:
        return f"{badge} · mean · peer LOO (annum)"
    if w == ASST_PS and s == ANNUM:
        return f"{badge} · mean · peer LOO (annum) · v0 default"
    return f"{badge} · {s} · {x_metric}"


def hero_title_line(*, window: str, stat: str, x_metric: str) -> str:
    w = normalize_window(window)
    s = normalize_stat(stat)
    if x_metric == "own_cum":
        return "Empirical hero — own cumulative pubs (ability slice)"
    if w == DECISION and x_metric == "own_career":
        return "Empirical hero — own career pubs rate at decision"
    if w == DECISION:
        return "Empirical hero — dept pond LOO (career rate at decision year)"
    if w == LAST_PS and s == CUM:
        return "Empirical hero — peer cumulative stock at exit"
    if w == ASST_PS:
        return "Empirical hero — peer pool context (ASST-PS mean)"
    return "Empirical hero — peer pool context · tenure inference panel"


# Thin legacy aliases (read old provenance / gradual import migration)
def grain_badge_short(grain: str) -> str:
    return window_badge(grain)


def grain_display_label(grain: str) -> str:
    return window_display_label(grain)


def stamp_grain_badge(ax, grain: str, **kwargs) -> None:
    stamp_window_badge(ax, grain, **kwargs)
