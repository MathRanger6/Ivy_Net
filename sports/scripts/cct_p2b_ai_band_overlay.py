#!/usr/bin/env python3
"""P2b Â-band overlay — draft rate vs T̂_j (line superposition).

Runs the same piecewise T̂_j binning as F-HERO (P2b) on **percentile slices** of Â
(pooled perf z on +DFT panel), then plots draft rate vs **T̂_j bin mean** so bands
are comparable on one axis.

Run (repo root):
  # Sweep default candidate bands → CSV + overlay PNG
  python sports/scripts/cct_p2b_ai_band_overlay.py

  # Custom bands (top 0–7% = F-HERO, then 7–15%, …) — comma-separated top_lo:top_hi
  python sports/scripts/cct_p2b_ai_band_overlay.py --bands "0:7,7:15,15:25,25:40"

  # Suggest equal-width top-% slices until bands get too thin
  python sports/scripts/cct_p2b_ai_band_overlay.py --suggest-width 10 --min-band-n 200

Outputs (``basic_data_plots/``):
  ``CCT_P2b_ai_band_overlay_lines.png``
  ``CCT_P2b_ai_band_overlay_sweep.csv``
  ``CCT_P2b_ai_band_overlay.json``
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs
from interval_overlap_paths import seasons_label
from pass_a_congestion_conditional import (
    DEFAULT_P2B_TAIL_SPLIT_Q,
    DEFAULT_P2B_TJ_BINNING,
    DEFAULT_P2B_TJ_N_HIGH,
    DEFAULT_P2B_TJ_N_LOW,
    MIN_CELL_N_CLAIM,
    MIN_CELL_N_WARN,
    T_JHAT_COL,
    CctSpec,
    _asymmetric_yerr,
    _attach_t_j_hat,
    _get_panel,
    _p2b_knee_summary,
    _tj_piecewise_tail_edges,
    _assign_tj_bin_labels,
    _wilson_ci,
)
from pd20_22_campaign_window import activate_from_args, add_window_args, current_window

# F-HERO defaults
DEFAULT_MIN_MINUTES = 20.0
DEFAULT_TOP_BANDS = ((0.0, 7.0), (7.0, 15.0), (15.0, 25.0), (25.0, 40.0), (40.0, 60.0))
DEFAULT_P2B_TJ_N_HIGH_FHERO = 7
FHERO_TOP_LO, FHERO_TOP_HI = 0.0, 7.0
MIN_BAND_N_SWEEP = 150
MIN_DRAFTS_SWEEP = 25
KNEE_PEAK_RATE_TOL = 0.02  # rightmost bin within this of max rate (plateau edge)
KNEE_MARKER_COLOR = "#c00000"

LINE_COLORS = [
    "#1f4e79",  # F-HERO emphasis
    "#2e75b6",
    "#5b9bd5",
    "#ed7d31",
    "#a5a5a5",
    "#7030a0",
    "#c00000",
]


@dataclass(frozen=True)
class AiTopPctBand:
    """Top-percent slice of pooled perf z on the analysis panel.

    ``top_lo=0, top_hi=7`` → top 7% (F-HERO). ``7:15`` → next 8% below that, etc.
    """

    top_lo: float
    top_hi: float

    def __post_init__(self) -> None:
        if self.top_lo < 0 or self.top_hi <= self.top_lo or self.top_hi > 100:
            raise ValueError(f"invalid top band {self.top_lo}:{self.top_hi}")

    @property
    def label(self) -> str:
        if self.top_lo <= 0:
            return f"top {self.top_hi:g}%"
        return f"top {self.top_lo:g}–{self.top_hi:g}%"

    @property
    def slide_label(self) -> str:
        pct_floor = 100.0 - self.top_hi
        if self.top_lo <= 0:
            return rf"$\hat{{A}}_i \in ({pct_floor:g}\%, \infty)$"
        pct_ceil = 100.0 - self.top_lo
        return rf"$\hat{{A}}_i \in ({pct_floor:g}\%, {pct_ceil:g}\%]$"

    @property
    def slug(self) -> str:
        lo = int(self.top_lo) if self.top_lo == int(self.top_lo) else str(self.top_lo).replace(".", "p")
        hi = int(self.top_hi) if self.top_hi == int(self.top_hi) else str(self.top_hi).replace(".", "p")
        if self.top_lo <= 0:
            return f"top{hi}"
        return f"top{lo}_{hi}"


def parse_bands(text: str) -> list[AiTopPctBand]:
    out: list[AiTopPctBand] = []
    for part in text.strip().split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise ValueError(f"band must be top_lo:top_hi, got {part!r}")
        lo_s, hi_s = part.split(":", 1)
        out.append(AiTopPctBand(float(lo_s), float(hi_s)))
    if not out:
        raise ValueError("empty --bands")
    return out


def _perf_cutoffs(panel: pd.DataFrame, tops: set[float]) -> dict[float, float]:
    perf = pd.to_numeric(panel["perf"], errors="coerce").dropna()
    if perf.empty:
        raise SystemExit("Empty perf on panel — check filters.")
    return {t: float(perf.quantile(1.0 - t / 100.0)) for t in sorted(tops)}


def apply_top_pct_band(panel: pd.DataFrame, band: AiTopPctBand, cuts: dict[float, float]) -> pd.DataFrame:
    """Slice pooled perf z by top-% ranks (``top_hi`` = outer edge, ``top_lo`` = inner edge)."""
    perf = pd.to_numeric(panel["perf"], errors="coerce")
    cut_outer = cuts[float(band.top_hi)]
    if band.top_lo <= 0:
        return panel.loc[perf >= cut_outer].copy()
    cut_inner = cuts[float(band.top_lo)]
    return panel.loc[(perf >= cut_outer) & (perf < cut_inner)].copy()


def _tj_table_from_band(
    band: pd.DataFrame,
    *,
    tj_n_low: int,
    tj_n_high: int,
    tail_split_q: float,
) -> tuple[pd.DataFrame, dict]:
    if band.empty:
        return pd.DataFrame(), {"mode": "piecewise_tail", "n_low_bins": tj_n_low, "n_high_bins": tj_n_high}

    edges, split_tj = _tj_piecewise_tail_edges(
        band[T_JHAT_COL],
        n_low=int(tj_n_low),
        n_high=int(tj_n_high),
        split_q=float(tail_split_q),
    )
    band = band.copy()
    band["vent"] = _assign_tj_bin_labels(band[T_JHAT_COL], edges)
    tj_lo, tj_hi = float(edges[0]), float(edges[-1])
    n_low_bins = int(tj_n_low)

    rows = []
    for vent, grp in band.dropna(subset=["vent"]).groupby("vent", observed=True):
        v = int(vent)
        n = int(len(grp))
        drafts = int(pd.to_numeric(grp["Y_draft"], errors="coerce").fillna(0).sum())
        rate = drafts / n if n else float("nan")
        lo, hi = _wilson_ci(drafts, n)
        elo, ehi = float(edges[v]), float(edges[v + 1])
        is_tail = v >= n_low_bins
        rows.append(
            {
                "vent": v,
                "bin_display": v + 1,
                "n": n,
                "drafts": drafts,
                "draft_rate": rate,
                "ci_lo": lo,
                "ci_hi": hi,
                "edge_lo": elo,
                "edge_hi": ehi,
                "T_j_mean": float(grp[T_JHAT_COL].mean()),
                "T_j_median": float(grp[T_JHAT_COL].median()),
                "bin_region": "fine_tail" if is_tail else "coarse",
                "high_tj_tail": is_tail,
                "thin_cell": n < MIN_CELL_N_WARN,
                "no_claim": n < MIN_CELL_N_CLAIM,
            }
        )
    tbl = pd.DataFrame(rows).sort_values("vent").reset_index(drop=True)
    meta = {
        "mode": "piecewise_tail",
        "n_low_bins": int(tj_n_low),
        "n_high_bins": int(tj_n_high),
        "tail_split_quantile": float(tail_split_q),
        "tail_split_tj": split_tj,
        "tj_range": {"lo": tj_lo, "hi": tj_hi},
        "n_edges": len(edges),
    }
    return tbl, meta


def _estimate_knee_tj(tbl: pd.DataFrame, knee: dict) -> float | None:
    """Descriptive knee: T̂_j at first post-plateau bin where rate drops below plateau mean."""
    if tbl.empty or not knee.get("alex_downturn_visible"):
        return None
    n_plateau = len(knee.get("plateau_bins_1idx") or [])
    if n_plateau <= 0:
        return None
    plateau_rate = float(knee["plateau_mean_draft_rate"])
    tail = tbl.iloc[n_plateau:].sort_values("T_j_mean")
    for _, row in tail.iterrows():
        if bool(row["thin_cell"]):
            continue
        if float(row["draft_rate"]) < plateau_rate:
            return float(row["T_j_mean"])
    return float(tbl.iloc[-1]["T_j_mean"])


def _visual_knee_peak(tbl: pd.DataFrame, *, rate_tol: float = KNEE_PEAK_RATE_TOL) -> dict | None:
    """Visual knee = rightmost peak on the plateau (max rate, then max T̂_j within tol of max).

    Picks F-HERO knee at ~0.33 (last strong bin before downturn), not the leftmost spike.
    """
    if tbl.empty:
        return None
    solid = tbl.loc[~tbl["thin_cell"].astype(bool)].copy()
    if solid.empty:
        solid = tbl.copy()
    max_rate = float(solid["draft_rate"].max())
    if not np.isfinite(max_rate):
        return None
    near_peak = solid.loc[solid["draft_rate"] >= max_rate - float(rate_tol)].sort_values("T_j_mean")
    if near_peak.empty:
        row = solid.loc[solid["draft_rate"].idxmax()]
    else:
        row = near_peak.iloc[-1]
    return {
        "knee_tj": float(row["T_j_mean"]),
        "knee_rate": float(row["draft_rate"]),
        "knee_bin": int(row["bin_display"]),
        "knee_n": int(row["n"]),
    }


def run_one_band(
    panel_pre: pd.DataFrame,
    cuts: dict[float, float],
    band: AiTopPctBand,
    *,
    tj_n_low: int,
    tj_n_high: int,
    tail_split_q: float,
) -> dict:
    sliced = apply_top_pct_band(panel_pre, band, cuts)
    tbl, binning_meta = _tj_table_from_band(
        sliced,
        tj_n_low=tj_n_low,
        tj_n_high=tj_n_high,
        tail_split_q=tail_split_q,
    )
    knee = _p2b_knee_summary(tbl, binning_meta=binning_meta)
    knee_tail = _estimate_knee_tj(tbl, knee)
    knee_peak = _visual_knee_peak(tbl)
    perf_lo = cuts[float(band.top_hi)]
    perf_hi = cuts[float(band.top_lo)] if band.top_lo > 0 else None
    min_bin_n = int(tbl["n"].min()) if not tbl.empty else 0
    return {
        "band": band,
        "band_n": int(len(sliced)),
        "total_drafts": int(pd.to_numeric(sliced["Y_draft"], errors="coerce").fillna(0).sum()),
        "perf_cut_outer": perf_lo,
        "perf_cut_inner": perf_hi,
        "tbl": tbl,
        "binning_meta": binning_meta,
        "knee": knee,
        "knee_tj_mean": knee_tail,
        "knee_peak": knee_peak,
        "min_bin_n": min_bin_n,
        "pct_floor": 100.0 - band.top_hi,
        "pct_ceil": 100.0 - band.top_lo if band.top_lo > 0 else 100.0,
    }


def suggest_bands(
    panel_pre: pd.DataFrame,
    cuts: dict[float, float],
    *,
    width: float,
    min_band_n: int,
    min_drafts: int,
    max_bands: int = 8,
) -> list[AiTopPctBand]:
    """Stack equal top-% slices from the apex until power gets thin."""
    bands: list[AiTopPctBand] = []
    top = 0.0
    while top < 100.0 and len(bands) < max_bands:
        hi = min(100.0, top + width)
        candidate = AiTopPctBand(top, hi)
        sliced = apply_top_pct_band(panel_pre, candidate, cuts)
        n = len(sliced)
        drafts = int(pd.to_numeric(sliced["Y_draft"], errors="coerce").fillna(0).sum())
        if n < min_band_n or drafts < min_drafts:
            break
        bands.append(candidate)
        top = hi
    if not bands:
        raise SystemExit(
            f"No bands passed min_band_n={min_band_n} / min_drafts={min_drafts} at width={width}."
        )
    return bands


def sweep_rows(results: list[dict]) -> pd.DataFrame:
    rows = []
    for r in results:
        b: AiTopPctBand = r["band"]
        k = r["knee"]
        kp = r.get("knee_peak") or {}
        rows.append(
            {
                "band": b.label,
                "slide_label": b.slide_label,
                "top_lo": b.top_lo,
                "top_hi": b.top_hi,
                "pct_floor": r["pct_floor"],
                "pct_ceil": r["pct_ceil"],
                "perf_z_cut_outer": r["perf_cut_outer"],
                "perf_z_cut_inner": r["perf_cut_inner"],
                "band_n": r["band_n"],
                "total_drafts": r["total_drafts"],
                "draft_rate_band": r["total_drafts"] / r["band_n"] if r["band_n"] else float("nan"),
                "min_bin_n": r["min_bin_n"],
                "plateau_rate": k.get("plateau_mean_draft_rate"),
                "tail_rate": k.get("tail_mean_draft_rate"),
                "downturn_visible": k.get("alex_downturn_visible"),
                "knee_tj_peak": kp.get("knee_tj"),
                "knee_rate_peak": kp.get("knee_rate"),
                "knee_bin_peak": kp.get("knee_bin"),
                "knee_tj_tail_rule": r["knee_tj_mean"],
                "ok_for_overlay": bool(
                    r["band_n"] >= MIN_BAND_N_SWEEP
                    and r["total_drafts"] >= MIN_DRAFTS_SWEEP
                    and not r["tbl"].empty
                ),
            }
        )
    return pd.DataFrame(rows)


def plot_overlay(
    results: list[dict],
    out_png: Path,
    *,
    base_spec: CctSpec,
    tj_n_low: int,
    tj_n_high: int,
    hero_top_lo: float,
    hero_top_hi: float,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    w = current_window()
    seasons = seasons_label(w.season_min, w.season_max)

    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    legend_handles = []

    for i, r in enumerate(results):
        b: AiTopPctBand = r["band"]
        tbl: pd.DataFrame = r["tbl"]
        if tbl.empty:
            continue
        is_hero = abs(b.top_lo - hero_top_lo) < 1e-9 and abs(b.top_hi - hero_top_hi) < 1e-9
        color = LINE_COLORS[i % len(LINE_COLORS)]
        lw = 2.8 if is_hero else 1.8
        alpha = 1.0 if is_hero else 0.88
        zorder = 10 if is_hero else 5 - i * 0.01

        plot_tbl = tbl.sort_values("T_j_mean")
        x = plot_tbl["T_j_mean"].to_numpy(dtype=float)
        y = plot_tbl["draft_rate"].to_numpy(dtype=float)
        yerr_lo, yerr_hi = _asymmetric_yerr(y, plot_tbl["ci_lo"], plot_tbl["ci_hi"])

        # Hollow markers on thin cells
        thin = plot_tbl["thin_cell"].to_numpy(dtype=bool)
        marker = "o"
        ms = 7 if is_hero else 5

        line, = ax.plot(
            x, y,
            color=color,
            lw=lw,
            alpha=alpha,
            zorder=zorder,
            marker=marker,
            ms=ms,
            markerfacecolor="white" if thin.any() else color,
            markeredgecolor=color,
            markeredgewidth=1.2,
        )
        ax.errorbar(
            x, y,
            yerr=[yerr_lo, yerr_hi],
            fmt="none",
            ecolor=color,
            elinewidth=1.0,
            capsize=2.5,
            alpha=0.65,
            zorder=zorder - 0.01,
        )

        kp = r.get("knee_peak")
        if kp and np.isfinite(kp.get("knee_tj", float("nan"))):
            ax.plot(
                kp["knee_tj"],
                kp["knee_rate"],
                "o",
                color=KNEE_MARKER_COLOR,
                ms=9 if is_hero else 7,
                markeredgecolor="white",
                markeredgewidth=1.0,
                zorder=20,
            )

        knee_tj = kp.get("knee_tj") if kp else r.get("knee_tj_mean")
        label = f"{b.slide_label} (n={r['band_n']:,}, drafts={r['total_drafts']:,}"
        if knee_tj is not None and np.isfinite(knee_tj):
            label += f", knee≈{knee_tj:.2f}"
        label += ")"
        if is_hero:
            label = rf"F-HERO · {label}"
        line.set_label(label)
        legend_handles.append(line)

    ax.set_xlabel(r"$\hat{T}_j$ (team mean PPM $z$; bin mean within Â slice)", fontsize=10)
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$", fontsize=10)
    ax.set_ylim(bottom=0)
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.legend(loc="upper right", fontsize=7, framealpha=0.95)
    ax.plot([], [], "o", color=KNEE_MARKER_COLOR, ms=7, label="Visual knee (plateau peak)")
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="upper right", fontsize=7, framealpha=0.95)

    pop = "+DFT" if base_spec.dft else "full panel"
    # Title block above axes — spaced so lines do not overlap (tight_layout fights fig.text).
    fig.subplots_adjust(top=0.72, bottom=0.11, left=0.08, right=0.97)
    fig.text(
        0.5,
        0.98,
        "P2b overlay — draft rate vs $\\hat{T}_j$ by fixed $\\hat{A}_i$ percentile band",
        ha="center",
        va="top",
        fontsize=12,
        fontweight="medium",
    )
    fig.text(
        0.5,
        0.945,
        (
            f"{base_spec.perf_metric.upper()} $z$ · MBB {seasons} · mg{base_spec.min_team_season_games} "
            f"min{base_spec.min_minutes:g} · {pop} · piecewise {tj_n_low}+{tj_n_high} bins"
        ),
        ha="center",
        va="top",
        fontsize=9,
        color="0.35",
    )
    fig.text(
        0.5,
        0.912,
        "X = $\\hat{T}_j$ at bin center (not bin index). Hollow markers = thin cell ($n<30$).",
        ha="center",
        va="top",
        fontsize=8,
        color="0.45",
    )
    fig.savefig(out_png, dpi=150, bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")


def _base_spec(args) -> CctSpec:
    w = current_window()
    return CctSpec(
        season_min=w.season_min,
        season_max=w.season_max,
        min_minutes=float(args.min_minutes),
        min_team_season_games=int(args.min_team_games),
        winsor_lo=0.01,
        winsor_hi=0.99,
        n_bins=16,
        ai_lo=None,
        ai_hi=None,
        ai_top_pct=None,
        perf_metric=str(args.perf_metric).strip().lower(),
        dft=bool(args.dft),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="P2b Â-band overlay (lines on T̂_j).")
    parser.add_argument("--bands", default=None, help='Top-% slices, e.g. "0:7,7:15,15:25".')
    parser.add_argument(
        "--suggest-width",
        type=float,
        default=None,
        help="Build bands 0:W, W:2W, … until min_band_n/min_drafts fail.",
    )
    parser.add_argument("--min-band-n", type=int, default=MIN_BAND_N_SWEEP)
    parser.add_argument("--min-drafts", type=int, default=MIN_DRAFTS_SWEEP)
    parser.add_argument("--min-minutes", type=float, default=DEFAULT_MIN_MINUTES)
    parser.add_argument("--min-team-games", type=int, default=10, dest="min_team_games")
    parser.add_argument("--perf-metric", default="ppm")
    parser.add_argument("--dft", action="store_true", default=True)
    parser.add_argument("--no-dft", action="store_false", dest="dft")
    parser.add_argument("--tj-n-low", type=int, default=DEFAULT_P2B_TJ_N_LOW)
    parser.add_argument("--tj-n-high", type=int, default=DEFAULT_P2B_TJ_N_HIGH_FHERO)
    parser.add_argument(
        "--tail-split-q",
        type=float,
        default=DEFAULT_P2B_TAIL_SPLIT_Q,
    )
    parser.add_argument("--hero-top", default="0:7", help="F-HERO band for emphasis (top_lo:top_hi).")
    parser.add_argument(
        "--sweep-only",
        action="store_true",
        help="Write sweep CSV only; skip overlay PNG.",
    )
    add_window_args(parser)
    args = parser.parse_args()
    activate_from_args(args)

    if args.bands:
        bands = parse_bands(args.bands)
    elif args.suggest_width:
        bands = None  # filled after panel load
    else:
        bands = [AiTopPctBand(lo, hi) for lo, hi in DEFAULT_TOP_BANDS]

    hero_band = parse_bands(args.hero_top)[0]
    hero_lo, hero_hi = hero_band.top_lo, hero_band.top_hi

    ensure_hero_dirs()
    base = _base_spec(args)
    print(f"Building panel · min{base.min_minutes:g} · {base.population_label} …", flush=True)
    use = _get_panel(base)
    panel_pre = _attach_t_j_hat(use).dropna(subset=["perf", T_JHAT_COL, "Y_draft"]).copy()

    tops = {0.0}
    if bands:
        for b in bands:
            tops.add(b.top_lo)
            tops.add(b.top_hi)
    else:
        tops.update(float(x) for x in np.arange(0.0, 100.0 + float(args.suggest_width), float(args.suggest_width)) if x <= 100.0)
    cuts = _perf_cutoffs(panel_pre, tops)

    if bands is None:
        bands = suggest_bands(
            panel_pre,
            cuts,
            width=float(args.suggest_width),
            min_band_n=int(args.min_band_n),
            min_drafts=int(args.min_drafts),
        )
        print(f"Suggested {len(bands)} bands (width={args.suggest_width:g}%): {[b.label for b in bands]}")

    results = [
        run_one_band(
            panel_pre,
            cuts,
            b,
            tj_n_low=int(args.tj_n_low),
            tj_n_high=int(args.tj_n_high),
            tail_split_q=float(args.tail_split_q),
        )
        for b in bands
    ]

    sweep = sweep_rows(results)
    out_csv = BASIC_DATA_PLOTS / "CCT_P2b_ai_band_overlay_sweep.csv"
    sweep.to_csv(out_csv, index=False, float_format="%.6g")
    print(f"Wrote {out_csv.relative_to(REPO)}")
    print(sweep[["band", "band_n", "total_drafts", "knee_tj_peak", "knee_rate_peak", "ok_for_overlay"]].to_string(index=False))

    ok_labels = set(sweep.loc[sweep["ok_for_overlay"], "band"])
    overlay_bands = [r for r in results if r["band"].label in ok_labels]
    if not overlay_bands:
        print("Warning: no band passed ok_for_overlay — plotting all bands anyway.", flush=True)
        overlay_bands = results

    out_png = BASIC_DATA_PLOTS / "CCT_P2b_ai_band_overlay_lines.png"
    if not args.sweep_only:
        plot_overlay(
            overlay_bands,
            out_png,
            base_spec=base,
            tj_n_low=int(args.tj_n_low),
            tj_n_high=int(args.tj_n_high),
            hero_top_lo=hero_lo,
            hero_top_hi=hero_hi,
        )

    meta = {
        "diagnostic": "cct_p2b_ai_band_overlay",
        "date": date.today().isoformat(),
        "min_minutes": base.min_minutes,
        "dft": base.dft,
        "perf_metric": base.perf_metric,
        "tj_n_low": int(args.tj_n_low),
        "tj_n_high": int(args.tj_n_high),
        "bands": [
            {
                "label": r["band"].label,
                "slide_label": r["band"].slide_label,
                "top_lo": r["band"].top_lo,
                "top_hi": r["band"].top_hi,
                "band_n": r["band_n"],
                "total_drafts": r["total_drafts"],
                "knee": r["knee"],
                "knee_peak": r["knee_peak"],
                "knee_tj_tail_rule": r["knee_tj_mean"],
                "bins": r["tbl"].to_dict(orient="records") if not r["tbl"].empty else [],
            }
            for r in results
        ],
        "sweep_csv": out_csv.name,
        "png": out_png.name if not args.sweep_only else None,
    }
    out_json = BASIC_DATA_PLOTS / "CCT_P2b_ai_band_overlay.json"
    out_json.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    print("Done.")


if __name__ == "__main__":
    main()
