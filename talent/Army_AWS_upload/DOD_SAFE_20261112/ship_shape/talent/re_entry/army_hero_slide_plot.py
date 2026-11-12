#!/usr/bin/env python3
"""Army HERO panel (panel 9) — binned promotion rate vs B1/B2/B3 peer axes.

Defaults (legacy B3): z_pool_minus_mean_snr_fwd · EW8 · min pool 3 · full sample.

B1–B3 campaign stems: ``ARMY_HERO_b2_fwd_z_ew12_full_run1.png``

Run (520 workspace root):
  python talent/re_entry/army_hero_slide_plot.py
  python talent/re_entry/army_hero_slide_plot.py --axis b2 --direction fwd --scale z --band boe
  python talent/re_entry/army_hero_grid_runner.py --quick
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import army_gallery_paths  # noqa: F401 — bootstraps sys.path

from army_basic_plots import (  # noqa: E402
    COL_AI,
    COL_EVENT,
    COL_LOO,
    COL_POOL_SIZE,
    COL_TJ,
    GRAIN_LABEL,
    load_officer_last_snapshot,
)
from army_gallery_paths import HERO_DIR, PREFIX, REPO, TAG_RUN1, ensure_army_output_dirs, resolve_feather
from army_hero_axes import (  # noqa: E402
    Band,
    Direction,
    Scale,
    Axis,
    hero_output_stem,
    resolve_hero_column,
)
from hero_plot_style import (  # noqa: E402
    PLOT_DPI,
    annotate_bar_n,
    count_weighted_bar_colors,
    finalize_bar_figure,
    set_wrapped_ax_title,
)

# --- Legacy default (B3 · fwd · z) ---
plot_var = "z_pool_minus_mean_snr_fwd"
n_bins_default = 8
min_pool_size = 3
min_group_size = 3
filter_zero_oer = True
filter_nan_variable = True
outcome_mode = "last_event"

OER_CHECK_COLS = (
    COL_AI,
    COL_LOO,
    COL_TJ,
    "tb_ratio_fwd_snr",
    "tb_ratio_bwd_snr",
    "pool_mean_snr_fwd",
    "pool_loo_snr_fwd",
    "pool_minus_loo_snr_fwd",
    "pool_minus_mean_snr_fwd",
    "pool_tb_ratio_mean_snr_fwd",
    "z_tb_ratio_fwd_snr",
    "z_pool_minus_mean_snr_fwd",
    "z_pool_minus_loo_snr_fwd",
    "z_pool_loo_snr_fwd",
    "z_pool_mean_snr_fwd",
)


def load_feather_officers(feather: Path) -> pd.DataFrame:
    officers, _ = load_officer_last_snapshot(feather)
    return officers


def _hero_xlabel(var: str, *, n_bins: int, bin_method: str = "equal_width") -> str:
    if bin_method == "quantile":
        tag = f"Q{n_bins}"
    else:
        tag = f"EW{n_bins}"
    return f"{var} ({tag})"


def _hero_title_var_label(var: str) -> str:
    if var.startswith("z_"):
        return f"z-scored {var[2:]}"
    return var


def _apply_band_of_excellence(
    officers: pd.DataFrame,
    *,
    band: Band,
    direction: Direction,
) -> tuple[pd.DataFrame, int]:
    """Drop ratees with own TB ratio == 0 (Band of Excellence cohort)."""
    if band != "boe":
        return officers, 0
    tb_col = f"tb_ratio_{direction}_snr"
    if tb_col not in officers.columns:
        raise SystemExit(f"Band of Excellence needs {tb_col} on feather.")
    tb = pd.to_numeric(officers[tb_col], errors="coerce")
    drop = tb == 0.0
    n_drop = int(drop.sum())
    return officers.loc[~drop].copy(), n_drop


def _filter_hero_cohort(
    officers: pd.DataFrame,
    *,
    x_column: str,
    min_pool: int,
    drop_nan_x: bool,
    drop_zero_oer: bool,
) -> tuple[pd.DataFrame, dict[str, int]]:
    work = officers.copy()
    counts: dict[str, int] = {"n_start": len(work)}

    if drop_zero_oer:
        oer_cols = [c for c in OER_CHECK_COLS if c in work.columns]
        if oer_cols:
            work = work[work[oer_cols].notna().any(axis=1)].copy()
    counts["n_after_zero_oer"] = len(work)

    if min_pool > 0 and COL_POOL_SIZE in work.columns:
        ps = pd.to_numeric(work[COL_POOL_SIZE], errors="coerce")
        work = work[ps >= min_pool].copy()
    counts["n_after_min_pool"] = len(work)

    if drop_nan_x and x_column in work.columns:
        x = pd.to_numeric(work[x_column], errors="coerce")
        work = work[x.notna()].copy()
    counts["n_after_nan_x"] = len(work)

    return work, counts


def _promoted_indicator(officers: pd.DataFrame, *, mode: str) -> np.ndarray:
    if mode == "last_event":
        return (pd.to_numeric(officers[COL_EVENT], errors="coerce") == 1).to_numpy(dtype=float)
    if mode == "ever_promoted":
        return (officers["outcome"] == "promoted").to_numpy(dtype=float)
    raise ValueError(f"Unknown outcome_mode: {mode}")


def _summarize_bins(
    x: np.ndarray,
    y: np.ndarray,
    *,
    bin_idx: np.ndarray,
    n_bins: int,
    edges: np.ndarray | None,
    min_group_size: int,
) -> pd.DataFrame:
    rows = []
    for b in range(n_bins):
        m = bin_idx == b
        n = int(m.sum())
        if n < min_group_size:
            continue
        if edges is not None and b < len(edges) - 1:
            x_lo, x_hi = float(edges[b]), float(edges[b + 1])
            x_mid = 0.5 * (x_lo + x_hi)
        else:
            x_lo = x_hi = x_mid = float(np.nanmean(x[m]))
        rows.append(
            {
                "bin": b + 1,
                "x_mid": x_mid,
                "x_lo": x_lo,
                "x_hi": x_hi,
                "promotion_rate": float(y[m].mean()),
                "n": n,
                "n_promoted": int(y[m].sum()),
            }
        )
    return pd.DataFrame(rows)


def _bin_equal_width(
    x: np.ndarray,
    y: np.ndarray,
    *,
    n_bins: int,
    min_group_size: int = 1,
) -> pd.DataFrame:
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if x.size == 0:
        return pd.DataFrame()
    edges = np.linspace(float(x.min()), float(x.max()), n_bins + 1)
    bin_idx = np.clip(np.digitize(x, edges, right=False) - 1, 0, n_bins - 1)
    return _summarize_bins(x, y, bin_idx=bin_idx, n_bins=n_bins, edges=edges, min_group_size=min_group_size)


def _bin_quantile(
    x: np.ndarray,
    y: np.ndarray,
    *,
    n_bins: int,
    min_group_size: int = 1,
) -> pd.DataFrame:
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if x.size < min_group_size:
        return pd.DataFrame()
    ranks = pd.Series(x).rank(method="first")
    try:
        cats = pd.qcut(ranks, q=n_bins, labels=False, duplicates="drop")
    except ValueError:
        return pd.DataFrame()
    bin_idx = cats.to_numpy(dtype=int)
    n_effective = int(bin_idx.max()) + 1 if bin_idx.size else 0
    if n_effective == 0:
        return pd.DataFrame()
    return _summarize_bins(
        x,
        y,
        bin_idx=bin_idx,
        n_bins=n_effective,
        edges=None,
        min_group_size=min_group_size,
    )


def build_hero_panel(
    officers: pd.DataFrame,
    *,
    n_bins: int = n_bins_default,
    tag: str = TAG_RUN1,
    x_column: str | None = None,
    axis: Axis | None = None,
    direction: Direction = "fwd",
    scale: Scale = "z",
    band: Band = "full",
    bin_method: str = "equal_width",
    min_pool: int = min_pool_size,
    min_group: int = min_group_size,
    drop_nan_x: bool = filter_nan_variable,
    drop_zero_oer: bool = filter_zero_oer,
    outcome: str = outcome_mode,
) -> tuple[Path, Path]:
    col_set = frozenset(officers.columns)
    if x_column is None:
        if axis is None:
            axis = "b3"
        x_column = resolve_hero_column(
            axis=axis, direction=direction, scale=scale, available=col_set
        )
    elif axis is None:
        axis = "b3"

    if x_column not in officers.columns:
        raise SystemExit(f"Column not in feather: {x_column}")

    work, band_dropped = _apply_band_of_excellence(officers, band=band, direction=direction)
    work, filter_counts = _filter_hero_cohort(
        work,
        x_column=x_column,
        min_pool=min_pool,
        drop_nan_x=drop_nan_x,
        drop_zero_oer=drop_zero_oer,
    )
    filter_counts["n_dropped_boe_own_tb_zero"] = band_dropped
    if work.empty:
        raise SystemExit("No officers left after HERO filters.")

    x = pd.to_numeric(work[x_column], errors="coerce").to_numpy(dtype=float)
    y = _promoted_indicator(work, mode=outcome)
    if bin_method == "quantile":
        binned = _bin_quantile(x, y, n_bins=n_bins, min_group_size=min_group)
    else:
        binned = _bin_equal_width(x, y, n_bins=n_bins, min_group_size=min_group)
    if binned.empty:
        raise SystemExit(f"No bins for HERO panel — check {x_column}.")

    var_label = _hero_title_var_label(x_column)
    y_label = (
        r"Promotion rate (event=1 · last snapshot)"
        if outcome == "last_event"
        else r"Promotion rate (ever promoted)"
    )
    band_note = "BoE (Â>0)" if band == "boe" else "full sample"

    fig, ax = plt.subplots(figsize=(8.0, 4.75))
    xs = binned["bin"].to_numpy(dtype=float)
    rates = binned["promotion_rate"].to_numpy(dtype=float)
    counts = binned["n"].to_numpy(dtype=int)
    colors = count_weighted_bar_colors(counts, cmap_name="Blues")
    ax.bar(xs, rates, color=colors, edgecolor="white", alpha=0.95, width=0.82, linewidth=0.6)
    annotate_bar_n(ax, xs, rates, counts, colors)

    ax.set_xlabel(_hero_xlabel(x_column, n_bins=n_bins, bin_method=bin_method))
    ax.set_ylabel(y_label)
    set_wrapped_ax_title(
        ax,
        [
            f"{PREFIX} HERO · {axis.upper()} · {band_note} · {var_label}",
            GRAIN_LABEL,
        ],
        fontsize=10,
        pad=10,
        fontweight="bold",
    )
    ax.set_ylim(0, min(1.05, float(rates.max()) * 1.15 + 0.05))

    footer = [
        f"Army Run 1 · {x_column} · n={len(work):,} (filtered) · {date.today().isoformat()}",
        f"min_pool={min_pool} · min_group={min_group} · outcome={outcome} · band={band}",
    ]
    finalize_bar_figure(fig, footer, top=0.86)

    stem = hero_output_stem(
        axis=axis,
        direction=direction,
        scale=scale,
        bin_method=bin_method,
        n_bins=n_bins,
        band=band,
        tag=tag,
        prefix=PREFIX,
    )

    out_png = HERO_DIR / f"{stem}.png"
    out_csv = HERO_DIR / f"{stem}.csv"
    out_meta = HERO_DIR / f"{stem}.json"

    fig.savefig(out_png, dpi=PLOT_DPI)
    plt.close(fig)
    binned.to_csv(out_csv, index=False)
    out_meta.write_text(
        json.dumps(
            {
                "date": date.today().isoformat(),
                "panel": 9,
                "axis": axis,
                "direction": direction,
                "scale": scale,
                "band": band,
                "n_bins": n_bins,
                "bin_method": bin_method,
                "x_column": x_column,
                "n_officers_raw": len(officers),
                "n_officers_filtered": len(work),
                "filter_counts": filter_counts,
                "min_pool_size": min_pool,
                "min_group_size": min_group,
                "filter_zero_oer": drop_zero_oer,
                "filter_nan_variable": drop_nan_x,
                "outcome_mode": outcome,
                "csv": out_csv.name,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png, out_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Army HERO slide panel")
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--n-bins", type=int, default=n_bins_default)
    parser.add_argument("--axis", choices=("b1", "b2", "b3"), default=None)
    parser.add_argument("--direction", choices=("fwd", "bwd"), default="fwd")
    parser.add_argument("--scale", choices=("z", "raw"), default="z")
    parser.add_argument("--band", choices=("full", "boe"), default="full")
    parser.add_argument(
        "--bin-method",
        choices=("equal_width", "quantile"),
        default="equal_width",
    )
    parser.add_argument(
        "--plot-var",
        default=None,
        help=f"Explicit feather column (overrides --axis); legacy default {plot_var}",
    )
    parser.add_argument("--min-pool-size", type=int, default=min_pool_size)
    parser.add_argument("--min-group-size", type=int, default=min_group_size)
    parser.add_argument(
        "--outcome",
        choices=("last_event", "ever_promoted"),
        default=outcome_mode,
    )
    parser.add_argument("--no-filter-zero-oer", action="store_true")
    parser.add_argument("--no-filter-nan-x", action="store_true")
    parser.add_argument("--tag", default=TAG_RUN1)
    args = parser.parse_args()

    ensure_army_output_dirs()
    feather = resolve_feather(args.input)
    officers = load_feather_officers(feather)
    print(f"HERO raw cohort: {len(officers):,} officers")
    build_hero_panel(
        officers,
        n_bins=args.n_bins,
        x_column=args.plot_var,
        axis=args.axis,
        direction=args.direction,
        scale=args.scale,
        band=args.band,
        bin_method=args.bin_method,
        tag=args.tag,
        min_pool=args.min_pool_size,
        min_group=args.min_group_size,
        drop_zero_oer=filter_zero_oer and not args.no_filter_zero_oer,
        drop_nan_x=filter_nan_variable and not args.no_filter_nan_x,
        outcome=args.outcome,
    )
    print("Done.")


if __name__ == "__main__":
    main()
