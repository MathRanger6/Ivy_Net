#!/usr/bin/env python3
"""Army HERO panel (panel 9) — binned promotion rate vs pool LOO (CR CIF-bar aligned).

Defaults mirror Cell 11 ``run1_cr_z_pool_minus_mean_snr_fwd``:
  z_pool_minus_mean_snr_fwd · EW8 · min pool 3 · filter NaN/zero-OER · last-event promotion.

Run (AWS 520 root — no PYTHONPATH needed):
  ./talent/re_entry/army_hero_slide_plot.py
  ./talent/re_entry/army_hero_slide_plot.py --outcome ever_promoted
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
from hero_plot_style import (  # noqa: E402
    PLOT_DPI,
    annotate_bar_n,
    count_weighted_bar_colors,
    finalize_bar_figure,
    set_wrapped_ax_title,
)

# --- HERO defaults (Cell 11 CR CIF-bar alignment) ---
plot_var = "z_pool_minus_mean_snr_fwd"
n_bins_default = 8
min_pool_size = 3
min_group_size = 3
filter_zero_oer = True
filter_nan_variable = True
outcome_mode = "last_event"  # "ever_promoted" for original porch-deck semantics

OER_CHECK_COLS = (
    COL_AI,
    COL_LOO,
    COL_TJ,
    "tb_ratio_fwd_snr",
    "pool_minus_mean_snr_fwd",
    "pool_tb_ratio_mean_snr_fwd",
    "z_tb_ratio_fwd_snr",
    "z_pool_minus_mean_snr_fwd",
)


def _hero_var_slug(var: str) -> str:
    """Filename-safe token derived from plot_var."""
    return var


def _hero_xlabel(var: str, *, n_bins: int, bin_method: str = "equal_width") -> str:
    bm = bin_method.replace("_", "-")
    return f"{var} ({bm} · EW{n_bins})"


def _hero_title_var_label(var: str) -> str:
    if var.startswith("z_"):
        return f"z-scored {var[2:]}"
    return var


def _filter_hero_cohort(
    officers: pd.DataFrame,
    *,
    x_column: str,
    min_pool: int,
    drop_nan_x: bool,
    drop_zero_oer: bool,
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Apply Cell-11-style filters before binning."""
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


def _bin_equal_width(
    x: np.ndarray,
    y: np.ndarray,
    *,
    n_bins: int,
    min_group_size: int = 1,
) -> pd.DataFrame:
    """Bin x; y = promoted indicator (0/1). Skip bins below min_group_size."""
    mask = np.isfinite(x) & np.isfinite(y)
    x, y = x[mask], y[mask]
    if x.size == 0:
        return pd.DataFrame()
    edges = np.linspace(float(x.min()), float(x.max()), n_bins + 1)
    bin_idx = np.clip(np.digitize(x, edges, right=False) - 1, 0, n_bins - 1)
    rows = []
    for b in range(n_bins):
        m = bin_idx == b
        n = int(m.sum())
        if n == 0 or n < min_group_size:
            continue
        rows.append(
            {
                "bin": b + 1,
                "x_mid": 0.5 * (edges[b] + edges[b + 1]),
                "x_lo": float(edges[b]),
                "x_hi": float(edges[b + 1]),
                "promotion_rate": float(y[m].mean()),
                "n": n,
                "n_promoted": int(y[m].sum()),
            }
        )
    return pd.DataFrame(rows)


def build_hero_panel(
    officers: pd.DataFrame,
    *,
    n_bins: int = n_bins_default,
    tag: str = TAG_RUN1,
    x_column: str = plot_var,
    min_pool: int = min_pool_size,
    min_group: int = min_group_size,
    drop_nan_x: bool = filter_nan_variable,
    drop_zero_oer: bool = filter_zero_oer,
    outcome: str = outcome_mode,
) -> tuple[Path, Path]:
    if x_column not in officers.columns:
        raise SystemExit(f"Column not in feather: {x_column}")

    work, filter_counts = _filter_hero_cohort(
        officers,
        x_column=x_column,
        min_pool=min_pool,
        drop_nan_x=drop_nan_x,
        drop_zero_oer=drop_zero_oer,
    )
    if work.empty:
        raise SystemExit("No officers left after HERO filters.")

    x = pd.to_numeric(work[x_column], errors="coerce").to_numpy(dtype=float)
    y = _promoted_indicator(work, mode=outcome)
    binned = _bin_equal_width(x, y, n_bins=n_bins, min_group_size=min_group)
    if binned.empty:
        raise SystemExit(f"No bins for HERO panel — check {x_column}.")

    var_slug = _hero_var_slug(x_column)
    var_label = _hero_title_var_label(x_column)
    y_label = (
        r"Promotion rate (event=1 · last snapshot)"
        if outcome == "last_event"
        else r"Promotion rate (ever promoted)"
    )

    fig, ax = plt.subplots(figsize=(8.0, 4.75))
    xs = binned["bin"].to_numpy(dtype=float)
    rates = binned["promotion_rate"].to_numpy(dtype=float)
    counts = binned["n"].to_numpy(dtype=int)
    colors = count_weighted_bar_colors(counts, cmap_name="Blues")
    ax.bar(xs, rates, color=colors, edgecolor="white", alpha=0.95, width=0.82, linewidth=0.6)
    annotate_bar_n(ax, xs, rates, counts, colors)

    ax.set_xlabel(_hero_xlabel(x_column, n_bins=n_bins))
    ax.set_ylabel(y_label)
    set_wrapped_ax_title(
        ax,
        [
            f"{PREFIX} HERO · EW{n_bins} · {var_label}",
            GRAIN_LABEL,
        ],
        fontsize=10,
        pad=10,
        fontweight="bold",
    )
    ax.set_ylim(0, min(1.05, float(rates.max()) * 1.15 + 0.05))

    footer = [
        f"Army Run 1 · {x_column} · n={len(work):,} (filtered) · {date.today().isoformat()}",
        f"CR-aligned · min_pool={min_pool} · min_group={min_group} · outcome={outcome}",
    ]
    finalize_bar_figure(fig, footer, top=0.86)

    stem = f"{PREFIX}_HERO_ew{n_bins}_{var_slug}_{tag}"
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
                "n_bins": n_bins,
                "bin_method": "equal_width",
                "x_column": x_column,
                "plot_var": x_column,
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
    parser.add_argument(
        "--plot-var",
        default=plot_var,
        help=f"Feather column for HERO x-axis (default: {plot_var})",
    )
    parser.add_argument("--min-pool-size", type=int, default=min_pool_size)
    parser.add_argument("--min-group-size", type=int, default=min_group_size)
    parser.add_argument(
        "--outcome",
        choices=("last_event", "ever_promoted"),
        default=outcome_mode,
        help="Promotion coding (default: last_event = Cell 11 CIF bars)",
    )
    parser.add_argument(
        "--no-filter-zero-oer",
        action="store_true",
        help="Disable zero-OER officer exclusion",
    )
    parser.add_argument(
        "--no-filter-nan-x",
        action="store_true",
        help="Disable NaN exclusion on plot_var",
    )
    args = parser.parse_args()

    ensure_army_output_dirs()
    feather = resolve_feather(args.input)
    officers, stats = load_officer_last_snapshot(feather)
    print(f"HERO raw cohort: {stats['n_officers']:,} officers · x={args.plot_var}")
    build_hero_panel(
        officers,
        n_bins=args.n_bins,
        x_column=args.plot_var,
        min_pool=args.min_pool_size,
        min_group=args.min_group_size,
        drop_zero_oer=filter_zero_oer and not args.no_filter_zero_oer,
        drop_nan_x=filter_nan_variable and not args.no_filter_nan_x,
        outcome=args.outcome,
    )
    print("Done.")


if __name__ == "__main__":
    main()
