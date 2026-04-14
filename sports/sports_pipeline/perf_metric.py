"""
Performance measure (`perf`) — options when *building* or *interpreting* the 530 panel.

The exported modeling table (`player_season_panel_530.csv`) carries a single column
`perf`: whatever measure you chose for leave-one-out teammate pool quality (`poolq_loo`
is the mean of teammates’ `perf` excluding self; `poolq_sq` is its square).

**Legacy conductor strings** (see `obsolete_files/sports_gameplan_old/530_sports_pipeline_bkup.ipynb`,
Cells 3 & 7) map PERF_METRIC → a source column copied into `perf`:

| User setting   | Panel column filled into `perf` | Requires SR merge file? |
|----------------|----------------------------------|-------------------------|
| `"ppm"`        | `ppm` (points / minutes, ESPN box) | No — ESPN box only   |
| `"minutes"`    | `minutes` (player-season total)      | No                   |
| `"bpm"`        | `BPM` (Box Plus/Minus)             | Yes — `bpm_player_season_matched.csv` |
| `"opm"`        | `OBPM` (offensive BPM)             | Yes (same merge)     |
| `"dpm"`        | `DBPM` (defensive BPM)             | Yes (same merge)     |
| `"per"`        | `PER` (player efficiency rating)   | Yes                  |
| `"ws40"`       | `WS/40` (win shares per 40 min)   | Yes                  |
| `"ws"`         | `WS` (win shares, season total)    | Yes                  |
| `"tspct"` / `"ts_pct"` | `ts_pct_sr` (true shooting %, SR) | Yes           |

**Two-pass workflow** (when switching to SR): export once with `ppm` or `minutes`,
complete SR scrape + merge under `DO_NOT_ERASE/`, then rebuild panel with `bpm` /
`opm` / `dpm` and recompute LOO so `poolq_loo` reflects the new `perf`.

**Switching the analysis measure in-memory:** after `panel_build.load_panel`, set
`PipelineConfig.perf_metric` (a **list** of user keys, e.g. ``[\"obpm\"]`` or ``[\"obpm\", \"ws40\"]``)
and call `panel_build.apply_perf_metric_for_analysis(df, perf_metric_active(cfg))`.
A single string is normalized to a one-element list. ``run_conductor`` uses the **first** list entry per run;
sweep multiple metrics via the notebook loop or ``RUN_ALL_PERF_METRICS``.
Plot captions use `plot_label_for_metric` / `PipelineConfig.perf_measure_label` (active = first metric).
For legacy winsorization or a full CSV rebuild, re-export from `530_sports_pipeline_bkup.ipynb`.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd

# Canonical keys accepted by legacy `_resolve_perf_metric` in 530 backup.
PERF_METRIC_BOX_ONLY: tuple[str, ...] = ("ppm", "minutes")
PERF_METRIC_SR: tuple[str, ...] = (
    "bpm",
    "opm",
    "dpm",
    "per",
    "ws40",
    "ws",
    "tspct",
    "ts_pct",
)

# Panel columns that come from the SR matched merge (not ESPN box alone).
_SR_MERGE_PANEL_COLS: frozenset[str] = frozenset(
    {"BPM", "OBPM", "DBPM", "PER", "WS", "WS/40", "ts_pct_sr"}
)

# Normalized user input → (short token for logging, panel column name).
_PERF_MAP: dict[str, tuple[str, str]] = {
    "ppm": ("ppm", "ppm"),
    "minutes": ("minutes", "minutes"),
    "bpm": ("bpm", "BPM"),
    "opm": ("obpm", "OBPM"),
    "obpm": ("obpm", "OBPM"),
    "dpm": ("dbpm", "DBPM"),
    "dbpm": ("dbpm", "DBPM"),
    "per": ("per", "PER"),
    "ws40": ("ws40", "WS/40"),
    "ws": ("ws", "WS"),
    "tspct": ("tspct", "ts_pct_sr"),
    "ts_pct": ("tspct", "ts_pct_sr"),
}

# Human-readable plot / report captions (one row per accepted user key in `_PERF_MAP`).
_PERF_PLOT_LABELS: dict[str, str] = {
    "ppm": "PPM — points per minute (ESPN box); LOO teammate mean on perf",
    "minutes": "Minutes — player-season total; LOO teammate mean on perf",
    "bpm": "BPM — Box Plus/Minus (Sports-Reference merge); LOO teammate mean on perf",
    "opm": "OBPM — offensive BPM (Sports-Reference merge); LOO teammate mean on perf",
    "obpm": "OBPM — offensive BPM (Sports-Reference merge); LOO teammate mean on perf",
    "dpm": "DBPM — defensive BPM (Sports-Reference merge); LOO teammate mean on perf",
    "dbpm": "DBPM — defensive BPM (Sports-Reference merge); LOO teammate mean on perf",
    "per": "PER — player efficiency rating (SR); LOO teammate mean on perf",
    "ws40": "WS/40 — win shares per 40 minutes (SR); LOO teammate mean on perf",
    "ws": "WS — win shares, season total (SR); LOO teammate mean on perf",
    "tspct": "TS% — true shooting percentage (SR, stored as ts_pct_sr); LOO teammate mean on perf",
    "ts_pct": "TS% — true shooting percentage (SR, stored as ts_pct_sr); LOO teammate mean on perf",
}


def resolve_perf_metric(metric: str) -> tuple[str, str]:
    """
    Return (short_label, panel_column) for a user-facing PERF_METRIC string.

    Raises ValueError if unknown. SR-backed metrics still need the merge columns
    present on the panel when you copy them into `perf`.
    """
    key = metric.strip().lower()
    if key not in _PERF_MAP:
        allowed = ", ".join(sorted(set(_PERF_MAP.keys())))
        raise ValueError(
            f"Unknown PERF_METRIC {metric!r}. "
            f"Expected one of: {allowed}. "
            f"See module docstring in sports_pipeline.perf_metric."
        )
    return _PERF_MAP[key]


def normalize_perf_metric_list(value: Any) -> list[str]:
    """
    Coerce ``cfg.perf_metric`` (str or iterable) to a non-empty list of user keys.

    Each entry is stripped; duplicates are removed preserving order. Unknown keys are
    still passed through here — ``PipelineConfig.__post_init__`` validates with
    ``resolve_perf_metric``.
    """
    if value is None:
        return ["minutes"]
    if isinstance(value, str):
        s = value.strip()
        return [s] if s else ["minutes"]
    if isinstance(value, (list, tuple)):
        out: list[str] = []
        seen: set[str] = set()
        for x in value:
            xs = str(x).strip()
            if not xs:
                continue
            lk = xs.lower()
            if lk in seen:
                continue
            seen.add(lk)
            out.append(xs)
        return out if out else ["minutes"]
    s = str(value).strip()
    return [s] if s else ["minutes"]


def perf_metric_active(cfg: Any) -> str:
    """
    The single perf key used for one conductor pass: **first** element of ``cfg.perf_metric``.

    When looping metrics, pass ``replace(cfg, perf_metric=[m])`` so the active key is ``m``.
    """
    return normalize_perf_metric_list(getattr(cfg, "perf_metric", None))[0]


def plot_label_for_metric(metric: str) -> str:
    """Caption for figures and tables; keyed like `resolve_perf_metric` (e.g. ``\"opm\"``, ``\"obpm\"``)."""
    key = metric.strip().lower()
    if key not in _PERF_MAP:
        allowed = ", ".join(sorted(set(_PERF_MAP.keys())))
        raise ValueError(f"Unknown perf metric {metric!r}. Expected one of: {allowed}.")
    return _PERF_PLOT_LABELS[key]


def export_plot_slug(cfg: Any) -> str:
    """
    Filesystem-safe token for export filenames.

    Suffixes may include: ``_poolqeqwidth``, ``_zwithinseason``, ``_tdalltime`` / ``_tdseason``
    (team draftee restriction when ``restrict_teams_by_draftees`` is True).
    """
    m = perf_metric_active(cfg).strip().lower()
    if m not in _PERF_MAP:
        m = re.sub(r"[^a-z0-9]+", "_", m)
    safe = m.replace("/", "_").replace("%", "pct")
    if str(getattr(cfg, "poolq_binning", "quantile")).strip().lower() == "equal_width":
        safe = f"{safe}_poolqeqwidth"
    if bool(getattr(cfg, "perf_zscore_within_season", False)):
        safe = f"{safe}_zwithinseason"
    if bool(getattr(cfg, "restrict_teams_by_draftees", True)):
        dr = str(getattr(cfg, "draftee_restriction", "all_time")).strip().lower()
        safe = f"{safe}_tdseason" if dr == "season" else f"{safe}_tdalltime"
    if str(getattr(cfg, "ventile_eda_plot_style", "poolq_line")).strip().lower() == "bins_bars_520":
        safe = f"{safe}_ventilebars520"
    return safe


def perf_options_df() -> pd.DataFrame:
    """
    One row per accepted analysis metric: user key, panel column, SR merge flag, plot label.

    Use in the conductor next to ``PipelineConfig.perf_metric`` to see allowed values.
    """
    import pandas as pd

    rows: list[dict[str, object]] = []
    for k in sorted(set(_PERF_MAP.keys())):
        _, col = _PERF_MAP[k]
        rows.append(
            {
                "metric": k,
                "panel_column": col,
                "needs_sr_merge": col in _SR_MERGE_PANEL_COLS,
                "plot_label": _PERF_PLOT_LABELS[k],
            }
        )
    return pd.DataFrame(rows).sort_values(["needs_sr_merge", "panel_column", "metric"]).reset_index(drop=True)


def perf_metric_needs_sr_merge(metric: str) -> bool:
    """True if this choice requires Sports-Reference columns on the panel."""
    key = metric.strip().lower()
    if key not in _PERF_MAP:
        return False
    _, col = _PERF_MAP[key]
    return col in _SR_MERGE_PANEL_COLS


def describe_perf_options() -> str:
    """Module docstring plus hint to use `perf_options_df()` for the options table."""
    base = (__doc__ or "").strip()
    return f"{base}\n\nFor a compact table: perf_metric.perf_options_df()  (or .to_string())."
