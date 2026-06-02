"""Track A-1 — draft rate vs pool quality by own-ability slice (530 panel).

Two modes:

* ``three-way`` — bottom 50% / middle p50–p90 / top 10% (first-pass heterogeneity test).
* ``top-tail`` (default) — nested top perf slices (1%, 2.5%, 5%, 10%): draft is ~60
  NBA slots per year, so the empirical story lives in the **upper tail**, not the middle mass.

Usage (from ``sports/``)::

    python tier1_heterogeneity_ventiles.py
    python tier1_heterogeneity_ventiles.py --mode top-tail
    python tier1_heterogeneity_ventiles.py --mode three-way --out ../datasets/mbb/exports_inverted_u_v0/heterogeneity_three_way.png
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sports_pipeline.config import PipelineConfig
from sports_pipeline.panel_build import (
    apply_perf_metric_for_analysis,
    assign_poolq_bin_labels,
    filter_panel,
    load_panel,
)


@dataclass(frozen=True)
class AbilitySliceSpec:
    """Mutually exclusive perf bands (quantiles on the analysis sample)."""

    name: str
    label: str
    lo_q: float | None  # inclusive lower quantile; None = −inf side
    hi_q: float | None  # exclusive upper quantile; None = +inf side
    color: str
    marker: str

    def mask(self, perf: pd.Series) -> pd.Series:
        p = pd.to_numeric(perf, errors="coerce")
        lo = float(p.quantile(self.lo_q)) if self.lo_q is not None else None
        hi = float(p.quantile(self.hi_q)) if self.hi_q is not None else None
        m = p.notna()
        if lo is not None:
            m &= p >= lo
        if hi is not None:
            m &= p < hi
        return m


THREE_WAY_SLICES: tuple[AbilitySliceSpec, ...] = (
    AbilitySliceSpec(
        "bottom_half",
        "Bottom 50% own perf",
        lo_q=None,
        hi_q=0.50,
        color="#9aa0a6",
        marker="s",
    ),
    AbilitySliceSpec(
        "middle_high",
        "Middle-high (p50–p90 own perf)",
        lo_q=0.50,
        hi_q=0.90,
        color="#1a73e8",
        marker="o",
    ),
    AbilitySliceSpec(
        "top_decile",
        "Top 10% own perf",
        lo_q=0.90,
        hi_q=None,
        color="#ea4335",
        marker="^",
    ),
)

# Backward-compatible alias
DEFAULT_SLICES = THREE_WAY_SLICES

_TOP_TAIL_STYLE = (
    (0.01, "#b71c1c", "^"),
    (0.025, "#ea4335", "v"),
    (0.05, "#1a73e8", "o"),
    (0.10, "#9aa0a6", "s"),
)


def top_tail_slices(
    tail_fracs: tuple[float, ...] = (0.01, 0.025, 0.05, 0.10),
) -> tuple[AbilitySliceSpec, ...]:
    """Nested top-perf slices: each line is perf >= sample quantile(1 − frac)."""
    style = {f: (c, m) for f, c, m in _TOP_TAIL_STYLE}
    out: list[AbilitySliceSpec] = []
    for frac in tail_fracs:
        pct = frac * 100.0
        label_pct = f"{pct:g}%" if pct < 1 else f"{pct:.0f}%"
        color, marker = style.get(frac, ("#333333", "o"))
        out.append(
            AbilitySliceSpec(
                f"top_{label_pct.replace('.', 'p').replace('%', 'pct')}",
                f"Top {label_pct} own perf",
                lo_q=1.0 - float(frac),
                hi_q=None,
                color=color,
                marker=marker,
            )
        )
    return tuple(out)


def slice_set_for_mode(mode: str) -> tuple[AbilitySliceSpec, ...]:
    m = str(mode).strip().lower().replace("_", "-")
    if m in ("three-way", "three", "3way", "default-legacy"):
        return THREE_WAY_SLICES
    if m in ("top-tail", "top", "tail", "draft-tail"):
        return top_tail_slices()
    raise ValueError(f"unknown mode {mode!r}; use 'top-tail' or 'three-way'")


def default_footnote(mode: str) -> str:
    m = str(mode).strip().lower().replace("_", "-")
    if m in ("three-way", "three", "3way", "default-legacy"):
        return (
            "Three-way split (first pass): check whether curve *shape* differs by slice, "
            "not only level. June 2026: shapes often parallel — see top-tail mode."
        )
    return (
        "Draft-scale view (~60 NBA slots/yr): nested top-perf tails. "
        "Ask whether pool-quality curve steepens or drops in elite bins as the tail tightens."
    )


def cfg_like_538d() -> PipelineConfig:
    """538D CELL 1 defaults (restrict_teams_by_draftees=False → ~80k+ rows)."""
    return PipelineConfig(
        panel_season_min=2011,
        panel_season_max=2021,
        ventiles=20,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.05, 0.95),
        perf_zscore_within_season=True,
        restrict_teams_by_draftees=False,
        draftee_restriction="season",
        min_minutes=0.0,
    )


def load_analysis_frame(
    *,
    perf_metric: str = "ppm",
    cfg: PipelineConfig | None = None,
) -> pd.DataFrame:
    """Same sample contract as 538D CELL 1–2."""
    cfg = cfg or cfg_like_538d()
    df = load_panel(cfg)
    smin = getattr(cfg, "panel_season_min", None)
    smax = getattr(cfg, "panel_season_max", None)
    if smin is not None:
        df = df.loc[pd.to_numeric(df["season"], errors="coerce") >= smin]
    if smax is not None:
        df = df.loc[pd.to_numeric(df["season"], errors="coerce") <= smax]
    df = apply_perf_metric_for_analysis(
        df,
        perf_metric,
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=cfg.perf_zscore_within_season,
    )
    use = filter_panel(df, cfg)
    return use.dropna(subset=["poolq_loo", "perf", "Y_draft"]).copy()


def binned_draft_table(
    df: pd.DataFrame,
    *,
    q_col: str,
    n_bins: int,
    bin_mode: str,
) -> pd.DataFrame:
    work = df.copy()
    work["pool_bin"] = assign_poolq_bin_labels(work[q_col], n_bins, bin_mode)
    return (
        work.dropna(subset=["pool_bin"])
        .groupby("pool_bin", observed=True)
        .agg(
            n=("Y_draft", "size"),
            draft_rate=("Y_draft", "mean"),
            poolq_mean=(q_col, "mean"),
        )
        .reset_index()
        .sort_values("poolq_mean")
    )


def figure_heterogeneity_ventiles(
    df: pd.DataFrame,
    *,
    slices: tuple[AbilitySliceSpec, ...] | None = None,
    mode: str = "top-tail",
    q_col: str = "poolq_loo",
    n_bins: int = 20,
    bin_mode: str = "quantile",
    title: str | None = None,
    footnote: str | None = None,
) -> tuple[plt.Figure, pd.DataFrame]:
    if slices is None:
        slices = slice_set_for_mode(mode)
    """Multi-line ventile plot: mean Y_draft vs mean poolq_loo, one line per ability slice."""
    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    rows: list[dict[str, Any]] = []

    for spec in slices:
        sub = df.loc[spec.mask(df["perf"])].copy()
        if sub.empty:
            continue
        tab = binned_draft_table(sub, q_col=q_col, n_bins=n_bins, bin_mode=bin_mode)
        tab["slice"] = spec.name
        rows.extend(tab.to_dict(orient="records"))

        x = tab["poolq_mean"].to_numpy(dtype=float)
        y = tab["draft_rate"].to_numpy(dtype=float)
        ax.plot(
            x,
            y,
            marker=spec.marker,
            linestyle="-",
            color=spec.color,
            lw=2.0,
            ms=6,
            label=f"{spec.label} (n={len(sub):,})",
        )

    long = pd.DataFrame(rows)
    xlab = "Mean poolq_loo in bin (LOO teammate perf)"
    ax.set_xlabel(xlab)
    ax.set_ylabel("Mean draft rate (Y_draft)")
    ax.set_ylim(bottom=0.0)
    ax.grid(True, alpha=0.25, lw=0.6)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.92)

    if title is None:
        mode_label = "top perf tails" if "top" in str(mode).lower() else "three-way slices"
        title = (
            f"Track A-1 — draft rate vs pool quality ({mode_label})\n"
            f"{n_bins} bins ({bin_mode}); perf = within-season z-scored PPM"
        )
    ax.set_title(title, fontsize=11)

    fig.text(
        0.01,
        0.01,
        footnote if footnote is not None else default_footnote(mode),
        fontsize=8,
        color="#444",
        ha="left",
    )
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    return fig, long


def _default_out_path(mode: str = "top-tail") -> Path:
    from sports_pipeline import paths

    out_dir = paths.mbb_dir() / "exports_inverted_u_v0"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = "top_tail" if "top" in str(mode).lower() else "three_way"
    return out_dir / f"heterogeneity_ventiles_{slug}.png"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--perf-metric", default="ppm")
    parser.add_argument("--q-col", default="poolq_loo")
    parser.add_argument("--n-bins", type=int, default=20)
    parser.add_argument("--bin-mode", default="quantile", choices=("quantile", "equal_width"))
    parser.add_argument(
        "--mode",
        default="top-tail",
        choices=("top-tail", "three-way"),
        help="top-tail = nested top 1/2.5/5/10%% perf; three-way = bottom/middle/top decile",
    )
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--csv", type=Path, default=None, help="Optional long table export")
    args = parser.parse_args(argv)

    slices = slice_set_for_mode(args.mode)
    df = load_analysis_frame(perf_metric=args.perf_metric)
    fig, long = figure_heterogeneity_ventiles(
        df,
        slices=slices,
        mode=args.mode,
        q_col=args.q_col,
        n_bins=args.n_bins,
        bin_mode=args.bin_mode,
    )

    out = args.out or _default_out_path(args.mode)
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)

    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        long.to_csv(args.csv, index=False)

    print(f"Analysis sample n={len(df):,}  mode={args.mode}")
    for spec in slices:
        m = spec.mask(df["perf"])
        n_slice = int(m.sum())
        rate = float(df.loc[m, "Y_draft"].mean()) if n_slice else float("nan")
        drafted = int(df.loc[m, "Y_draft"].sum()) if n_slice else 0
        print(
            f"  {spec.name}: n={n_slice:,}  drafted={drafted}  "
            f"overall draft rate={rate:.4f}"
        )
    print(f"Wrote figure: {out}")
    if args.csv:
        print(f"Wrote table: {args.csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
