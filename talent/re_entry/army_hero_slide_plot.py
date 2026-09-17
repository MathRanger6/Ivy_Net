#!/usr/bin/env python3
"""Army HERO panel (panel 9) — binned promotion rate vs pool minus mean LOO.

MBB/tenure-format bar chart with count-weighted blues (equal-width bins).

Run:
  python talent/re_entry/army_hero_slide_plot.py
  python talent/re_entry/army_hero_slide_plot.py --n-bins 8 --input ./running_vars/df_pipeline_11_cox_analysis.feather
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_RE_ENTRY = Path(__file__).resolve().parent
REPO = _RE_ENTRY.parents[2]
sys.path.insert(0, str(_RE_ENTRY))
sys.path.insert(0, str(REPO / "sports" / "scripts"))

from army_basic_plots import (  # noqa: E402
    COL_AI,
    COL_LOO,
    GRAIN_LABEL,
    load_officer_last_snapshot,
)
from army_gallery_paths import HERO_DIR, PREFIX, TAG_RUN1, ensure_army_output_dirs, resolve_feather
from hero_plot_style import (  # noqa: E402
    PLOT_DPI,
    annotate_bar_n,
    count_weighted_bar_colors,
    finalize_bar_figure,
)


def _bin_equal_width(x: np.ndarray, y: np.ndarray, *, n_bins: int) -> pd.DataFrame:
    """Bin x; y = promoted indicator (0/1)."""
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
        if n == 0:
            continue
        rows.append(
            {
                "bin": b + 1,
                "x_mid": 0.5 * (edges[b] + edges[b + 1]),
                "promotion_rate": float(y[m].mean()),
                "n": n,
                "n_promoted": int(y[m].sum()),
            }
        )
    return pd.DataFrame(rows)


def build_hero_panel(
    officers: pd.DataFrame,
    *,
    n_bins: int = 8,
    tag: str = TAG_RUN1,
) -> tuple[Path, Path]:
    x = pd.to_numeric(officers[COL_LOO], errors="coerce").to_numpy(dtype=float)
    y = (officers["outcome"] == "promoted").to_numpy(dtype=float)
    binned = _bin_equal_width(x, y, n_bins=n_bins)
    if binned.empty:
        raise SystemExit("No bins for HERO panel — check LOO column.")

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    xs = binned["bin"].to_numpy(dtype=float)
    rates = binned["promotion_rate"].to_numpy(dtype=float)
    counts = binned["n"].to_numpy(dtype=int)
    colors = count_weighted_bar_colors(counts, cmap_name="Blues")
    ax.bar(xs, rates, color=colors, edgecolor="white", alpha=0.95, width=0.82, linewidth=0.6)
    annotate_bar_n(ax, xs, rates, counts, fontsize=7)

    ax.set_xlabel("pool_minus_mean_snr_fwd (equal-width bins)")
    ax.set_ylabel(r"Promotion rate (ever promoted)")
    ax.set_title(
        f"{PREFIX} HERO · EW{n_bins} · pool LOO · {GRAIN_LABEL}",
        fontsize=10,
        fontweight="bold",
    )
    ax.set_ylim(0, min(1.05, float(rates.max()) * 1.15 + 0.05))

    footer = [
        f"Army Run 1 · n_officers={len(officers):,} · {date.today().isoformat()}",
        "Descriptive bin means — not Cox HR · compare to MBB/tenure HERO porch",
    ]
    finalize_bar_figure(fig, footer)

    stem = f"{PREFIX}_HERO_ew{n_bins}_pool_minus_mean_{tag}"
    out_png = HERO_DIR / f"{stem}.png"
    out_csv = HERO_DIR / f"{stem}.csv"
    out_meta = HERO_DIR / f"{stem}.json"

    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    binned.to_csv(out_csv, index=False)
    out_meta.write_text(
        json.dumps(
            {
                "date": date.today().isoformat(),
                "panel": 9,
                "n_bins": n_bins,
                "bin_method": "equal_width",
                "x_column": COL_LOO,
                "n_officers": len(officers),
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
    parser.add_argument("--n-bins", type=int, default=8)
    args = parser.parse_args()

    ensure_army_output_dirs()
    feather = resolve_feather(args.input)
    officers, stats = load_officer_last_snapshot(feather)
    print(f"HERO cohort: {stats['n_officers']:,} officers")
    build_hero_panel(officers, n_bins=args.n_bins)
    print("Done.")


if __name__ == "__main__":
    main()
