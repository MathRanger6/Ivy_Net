#!/usr/bin/env python3
"""CCT Act II — conditional draft-rate plots (fixed Â_i, vary pond / rank).

Priority 1: matched Â band × poolq_loo ventiles (Squid vs Jackal test).
Priority 3: roster percentile × T̂_j quartile (within-team big-fish axis).

Run (repo root):
  python sports/scripts/pass_a_congestion_conditional.py --plot matched_pond
  python sports/scripts/pass_a_congestion_conditional.py --plot roster_rank_tj
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SPORTS))

from gallery_knobs import HERO_BINS
from hero_gallery_paths import BASIC_DATA_PLOTS, ensure_hero_dirs
from interval_overlap_paths import seasons_label
from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    current_window,
)

DEFAULT_MIN_MINUTES = 20.0
DEFAULT_WINSOR_LO = 0.01
DEFAULT_WINSOR_HI = 0.99
DEFAULT_N_BINS = HERO_BINS
DEFAULT_AI_LO = 1.5
DEFAULT_AI_HI = 2.0
# Charles sensitivity presets (2026-08-21)
WIDER_AI_LO = 1.0
WIDER_AI_HI = 2.0
ELITE_AI_LO = 2.0
ELITE_AI_HI = 3.0
P1_GRID_METRICS = ("ppm", "bpm", "obpm")
P1_GRID_BANDS = ((1.0, 2.0), (1.5, 2.0), (2.0, 3.0))

_panel_cache: dict[tuple, pd.DataFrame] = {}
MIN_CELL_N_WARN = 30
MIN_CELL_N_CLAIM = 10
TJ_QUARTILE_LABELS = ("Q1 (lowest T̂_j)", "Q2", "Q3", "Q4 (highest T̂_j)")

# Priority 1 — 0-indexed poolq_loo ventiles within matched Â band
SQUID_VENT = (5, 6, 7)
JACKAL_VENT = (13, 14, 15)

SQUID_COLOR = "#2ecc71"
JACKAL_COLOR = "#e67e22"
OTHER_COLOR = "steelblue"
THIN_COLOR = "#c0392b"


@dataclass(frozen=True)
class CctSpec:
    season_min: int
    season_max: int
    min_minutes: float
    min_team_season_games: int
    winsor_lo: float
    winsor_hi: float
    n_bins: int
    ai_lo: float | None
    ai_hi: float | None
    perf_metric: str = "ppm"
    poolq_binning: str = "quantile"
    dft: bool = False

    @property
    def winsor_quantiles(self) -> tuple[float, float]:
        return (self.winsor_lo, self.winsor_hi)

    @property
    def ai_band_label(self) -> str:
        if self.ai_lo is None or self.ai_hi is None:
            return "full panel"
        return f"[{self.ai_lo:g}, {self.ai_hi:g}]"

    @property
    def population_label(self) -> str:
        return "+DFT" if self.dft else "full panel"

    def apply_ai_band(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.ai_lo is None or self.ai_hi is None:
            return df
        return df.loc[(df["perf"] >= self.ai_lo) & (df["perf"] <= self.ai_hi)]


def _drafted_team_ids(panel: pd.DataFrame) -> set:
    y = pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).astype(int)
    return set(panel.loc[y == 1, "team_id"].dropna().unique())


def _apply_dft(panel: pd.DataFrame, drafted_teams: set) -> pd.DataFrame:
    """+DFT — keep player-seasons on teams with ≥1 draftee in the panel window."""
    return panel.loc[panel["team_id"].isin(drafted_teams)].copy()


def _z_slug(z: float) -> str:
    s = f"{z:g}".replace(".", "p").replace("-", "m")
    return s


def _matched_pond_basename(spec: CctSpec) -> str:
    """Uniform: CCT_draft_rate_ai_band_poolq_loo_min{10|20}_{ppm|bpm|obpm}_z{lo}_{hi}_{allt|dft}."""
    parts = [
        "CCT_draft_rate_ai_band_poolq_loo",
        f"min{int(spec.min_minutes)}",
        str(spec.perf_metric).strip().lower(),
    ]
    if spec.ai_lo is not None and spec.ai_hi is not None:
        parts.append(f"z{_z_slug(spec.ai_lo)}_{_z_slug(spec.ai_hi)}")
    parts.append("dft" if spec.dft else "allt")
    return "_".join(parts)


def _wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return float("nan"), float("nan")
    p = successes / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    margin = z * math.sqrt((p * (1.0 - p) / n + z2 / (4.0 * n * n))) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def _prepare_panel(spec: CctSpec) -> pd.DataFrame:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.config import PipelineConfig
    from sports_pipeline.perf_metric import perf_metric_active

    drafted_teams: set | None = None
    if spec.dft:
        cfg0 = PipelineConfig(
            perf_metric=[spec.perf_metric],
            perf_zscore_within_season=True,
            ventiles=int(spec.n_bins),
            poolq_binning=str(spec.poolq_binning),
            poolq_winsor_quantiles=spec.winsor_quantiles,
            min_minutes=0.0,
            min_team_season_games=int(spec.min_team_season_games),
            drop_dash_placeholder_names=True,
            restrict_teams_by_draftees=False,
            use_prebuilt_panel_csv=False,
            panel_season_min=int(spec.season_min),
            panel_season_max=int(spec.season_max),
            analysis_season_min=int(spec.season_min),
            analysis_season_max=int(spec.season_max),
        )
        raw = conductor.prepare_panel(cfg0)
        drafted_teams = _drafted_team_ids(raw.dropna(subset=["team_id", "season"]))

    cfg = PipelineConfig(
        perf_metric=[spec.perf_metric],
        perf_zscore_within_season=True,
        ventiles=int(spec.n_bins),
        poolq_binning=str(spec.poolq_binning),
        poolq_winsor_quantiles=spec.winsor_quantiles,
        min_minutes=float(spec.min_minutes),
        min_team_season_games=int(spec.min_team_season_games),
        drop_dash_placeholder_names=True,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=int(spec.season_min),
        panel_season_max=int(spec.season_max),
        analysis_season_min=int(spec.season_min),
        analysis_season_max=int(spec.season_max),
    )
    panel = conductor.prepare_panel(cfg)
    if spec.dft and drafted_teams is not None:
        panel = _apply_dft(panel, drafted_teams)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    return panel_build.filter_panel(panel, cfg)


def _panel_cache_key(spec: CctSpec) -> tuple:
    return (
        spec.season_min,
        spec.season_max,
        float(spec.min_minutes),
        int(spec.min_team_season_games),
        float(spec.winsor_lo),
        float(spec.winsor_hi),
        str(spec.perf_metric),
        bool(spec.dft),
    )


def _get_panel(spec: CctSpec) -> pd.DataFrame:
    key = _panel_cache_key(spec)
    if key not in _panel_cache:
        _panel_cache[key] = _prepare_panel(spec)
    return _panel_cache[key]


def _matched_pond_table(use: pd.DataFrame, spec: CctSpec) -> tuple[pd.DataFrame, pd.DataFrame]:
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    band = use.dropna(subset=["perf", "poolq_loo", "Y_draft"]).copy()
    band = spec.apply_ai_band(band)
    band["vent"] = assign_poolq_bin_labels(
        band["poolq_loo"], spec.n_bins, spec.poolq_binning
    )
    rows = []
    for vent, grp in band.dropna(subset=["vent"]).groupby("vent", observed=True):
        n = int(len(grp))
        drafts = int(pd.to_numeric(grp["Y_draft"], errors="coerce").fillna(0).sum())
        rate = drafts / n if n else float("nan")
        lo, hi = _wilson_ci(drafts, n)
        rows.append(
            {
                "vent": int(vent),
                "bin_display": int(vent) + 1,
                "n": n,
                "drafts": drafts,
                "draft_rate": rate,
                "ci_lo": lo,
                "ci_hi": hi,
                "poolq_loo_mean": float(grp["poolq_loo"].mean()),
                "poolq_loo_median": float(grp["poolq_loo"].median()),
                "perf_mean": float(grp["perf"].mean()),
                "thin_cell": n < MIN_CELL_N_WARN,
                "no_claim": n < MIN_CELL_N_CLAIM,
            }
        )
    tbl = pd.DataFrame(rows).sort_values("vent").reset_index(drop=True)
    return band, tbl


def _pool_summary(tbl: pd.DataFrame, vents: tuple[int, ...], label: str) -> dict:
    sub = tbl.loc[tbl["vent"].isin(vents)]
    n = int(sub["n"].sum())
    drafts = int(sub["drafts"].sum())
    rate = drafts / n if n else float("nan")
    lo, hi = _wilson_ci(drafts, n)
    return {
        "label": label,
        "ventiles_0idx": list(vents),
        "bins_1idx": [v + 1 for v in vents],
        "n": n,
        "drafts": drafts,
        "draft_rate": rate,
        "ci_lo": lo,
        "ci_hi": hi,
    }


def _bar_color_for_vent(vent: int, thin: bool) -> str:
    if thin:
        return THIN_COLOR
    if vent in SQUID_VENT:
        return SQUID_COLOR
    if vent in JACKAL_VENT:
        return JACKAL_COLOR
    return OTHER_COLOR


def plot_matched_pond(
    spec: CctSpec,
    tbl: pd.DataFrame,
    band: pd.DataFrame,
    out_png: Path,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    seasons = seasons_label(spec.season_min, spec.season_max)
    perf_label = str(spec.perf_metric).strip().upper()
    pop_suffix = " · +DFT subsample" if spec.dft else ""
    squid = _pool_summary(tbl, SQUID_VENT, "Squid proxy (mid pond)")
    jackal = _pool_summary(tbl, JACKAL_VENT, "Jackal proxy (top pond)")

    fig, ax = plt.subplots(figsize=(10.5, 5.0))
    x = tbl["bin_display"].to_numpy(dtype=float)
    y = tbl["draft_rate"].to_numpy(dtype=float)
    yerr_lo = y - tbl["ci_lo"].to_numpy(dtype=float)
    yerr_hi = tbl["ci_hi"].to_numpy(dtype=float) - y
    colors = [
        _bar_color_for_vent(int(v), bool(thin))
        for v, thin in zip(tbl["vent"], tbl["thin_cell"], strict=True)
    ]
    ax.bar(x, y, color=colors, edgecolor="white", alpha=0.92, width=0.85)
    ax.errorbar(
        x,
        y,
        yerr=[yerr_lo, yerr_hi],
        fmt="none",
        ecolor="0.25",
        capsize=2,
        linewidth=0.8,
    )

    ax.set_xlabel(r"$\mathrm{poolq\_loo}$ ventile within matched $\hat{A}_i$ band (1 = lowest pond)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(
        rf"CCT Priority 1 — draft rate at fixed $\hat{{A}}_i$ · MBB {seasons}\n"
        rf"mg{spec.min_team_season_games} min{spec.min_minutes:g} · {perf_label} $z$ band "
        rf"{spec.ai_band_label} · winsor {spec.winsor_lo:g}–{spec.winsor_hi:g}{pop_suffix}",
        fontsize=10,
    )
    ax.set_xticks(x)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)

    cct_holds = squid["draft_rate"] > jackal["draft_rate"]
    compare = (
        f"Squid: {100*squid['draft_rate']:.2f}% (n={squid['n']:,})\n"
        f"Jackal: {100*jackal['draft_rate']:.2f}% (n={jackal['n']:,})\n"
        f"CCT signature (Squid > Jackal): {'YES' if cct_holds else 'NO'}"
    )
    ax.text(0.02, 0.98, compare, transform=ax.transAxes, fontsize=8, va="top", family="monospace")

    legend_handles = [
        mpatches.Patch(facecolor=SQUID_COLOR, edgecolor="white", label="Squid proxy (mid pond)"),
        mpatches.Patch(facecolor=JACKAL_COLOR, edgecolor="white", label="Jackal proxy (top pond)"),
        mpatches.Patch(facecolor=OTHER_COLOR, edgecolor="white", label="Other ventiles"),
        mpatches.Patch(facecolor=THIN_COLOR, edgecolor="white", label=f"Thin cell (n < {MIN_CELL_N_WARN})"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", fontsize=8, framealpha=0.92)

    note = (
        rf"Band n={len(band):,} PS · total drafts={int(band['Y_draft'].sum()):,}"
    )
    fig.text(0.5, 0.01, note, ha="center", fontsize=8, color="0.35")

    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")


def run_matched_pond(spec: CctSpec, out_dir: Path, *, write_readme: bool = True) -> Path:
    ensure_hero_dirs()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = _matched_pond_basename(spec)
    out_png = out_dir / f"{stem}.png"
    out_json = out_dir / f"{stem}.json"

    use = _get_panel(spec)
    band, tbl = _matched_pond_table(use, spec)
    if tbl.empty:
        raise SystemExit("No rows in matched Â band — check --ai-lo / --ai-hi")

    plot_matched_pond(spec, tbl, band, out_png)

    squid = _pool_summary(tbl, SQUID_VENT, "Squid proxy (mid pond)")
    jackal = _pool_summary(tbl, JACKAL_VENT, "Jackal proxy (top pond)")
    meta = {
        "diagnostic": "cct_matched_pond",
        "date": date.today().isoformat(),
        "plot": "matched_pond",
        "axis": "poolq_loo",
        "bdp_spec": f"mg{spec.min_team_season_games} min{spec.min_minutes:g} "
        f"{seasons_label(spec.season_min, spec.season_max)}",
        "population": spec.population_label,
        "dft": spec.dft,
        "seasons": seasons_label(spec.season_min, spec.season_max),
        "panel_n": int(len(use)),
        "band_n": int(len(band)),
        "band_drafts": int(pd.to_numeric(band["Y_draft"], errors="coerce").fillna(0).sum()),
        "ai_lo": spec.ai_lo,
        "ai_hi": spec.ai_hi,
        "n_bins": spec.n_bins,
        "winsor": list(spec.winsor_quantiles),
        "min_minutes": spec.min_minutes,
        "min_team_season_games": spec.min_team_season_games,
        "perf_metric": spec.perf_metric,
        "bins": tbl.to_dict(orient="records"),
        "squid_proxy": squid,
        "jackal_proxy": jackal,
        "cct_signature_squid_gt_jackal": bool(squid["draft_rate"] > jackal["draft_rate"]),
        "png": out_png.name,
    }
    out_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    print(
        f"  Band n={meta['band_n']:,} drafts={meta['band_drafts']:,} · "
        f"Squid {100*squid['draft_rate']:.2f}% vs Jackal {100*jackal['draft_rate']:.2f}% · "
        f"CCT={'YES' if meta['cct_signature_squid_gt_jackal'] else 'NO'}"
    )
    if write_readme:
        _write_readme(out_dir, meta, plot_key="matched_pond")
    return out_png


def run_p1_grid(base: CctSpec, out_dir: Path) -> Path:
    """Full P1 matrix: 3 metrics × 3 Â bands × {full, +DFT} (18 plots)."""
    ensure_hero_dirs()
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    total = len(P1_GRID_METRICS) * len(P1_GRID_BANDS) * 2
    n_done = 0
    for metric in P1_GRID_METRICS:
        for ai_lo, ai_hi in P1_GRID_BANDS:
            for dft in (False, True):
                n_done += 1
                spec = replace(
                    base,
                    perf_metric=metric,
                    ai_lo=float(ai_lo),
                    ai_hi=float(ai_hi),
                    dft=dft,
                )
                print(
                    f"[{n_done}/{total}] {metric.upper()} z∈[{ai_lo},{ai_hi}] "
                    f"{'+DFT' if dft else 'full panel'}",
                    flush=True,
                )
                out_png = run_matched_pond(spec, out_dir, write_readme=False)
                meta = json.loads((out_dir / f"{_matched_pond_basename(spec)}.json").read_text())
                squid = meta["squid_proxy"]
                jackal = meta["jackal_proxy"]
                rows.append(
                    {
                        "metric": metric,
                        "ai_lo": ai_lo,
                        "ai_hi": ai_hi,
                        "dft": dft,
                        "population": meta["population"],
                        "band_n": meta["band_n"],
                        "band_drafts": meta["band_drafts"],
                        "squid_rate": squid["draft_rate"],
                        "jackal_rate": jackal["draft_rate"],
                        "squid_n": squid["n"],
                        "jackal_n": jackal["n"],
                        "cct_squid_gt_jackal": meta["cct_signature_squid_gt_jackal"],
                        "png": meta["png"],
                        "json": f"{_matched_pond_basename(spec)}.json",
                    }
                )
    manifest = {
        "diagnostic": "cct_p1_grid",
        "date": date.today().isoformat(),
        "panel": f"mg{base.min_team_season_games} min{base.min_minutes:g} "
        f"{seasons_label(base.season_min, base.season_max)}",
        "bands": [list(b) for b in P1_GRID_BANDS],
        "metrics": list(P1_GRID_METRICS),
        "cells": rows,
    }
    manifest_path = out_dir / f"CCT_p1_grid_manifest_min{int(base.min_minutes)}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {manifest_path.relative_to(REPO)} ({len(rows)} cells)")
    _write_readme_all_grids(out_dir)
    return manifest_path


def _add_roster_rank_and_tj(df: pd.DataFrame) -> pd.DataFrame:
    work = df.dropna(subset=["perf", "team_id", "season", "Y_draft"]).copy()
    grp = work.groupby(["team_id", "season"], observed=True)["perf"]
    work["roster_pct"] = grp.rank(method="average", pct=True)
    work["T_j_hat"] = grp.transform("mean")
    team_tj = (
        work.groupby(["team_id", "season"], observed=True)
        .agg(T_j_hat=("T_j_hat", "first"))
        .reset_index()
    )
    team_tj["tj_quartile"] = pd.qcut(
        team_tj["T_j_hat"],
        4,
        labels=list(range(4)),
        duplicates="drop",
    ).astype("Int64")
    return work.merge(
        team_tj[["team_id", "season", "tj_quartile"]],
        on=["team_id", "season"],
        how="left",
    )


def _roster_rank_table(use: pd.DataFrame, spec: CctSpec) -> tuple[pd.DataFrame, pd.DataFrame]:
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    work = _add_roster_rank_and_tj(use)
    work = spec.apply_ai_band(work)
    work = work.dropna(subset=["roster_pct", "tj_quartile"])
    rows = []
    for tj_q, sub in work.groupby("tj_quartile", observed=True):
        sub = sub.copy()
        sub["vent"] = assign_poolq_bin_labels(
            sub["roster_pct"], spec.n_bins, spec.poolq_binning
        )
        for vent, grp in sub.dropna(subset=["vent"]).groupby("vent", observed=True):
            n = int(len(grp))
            drafts = int(pd.to_numeric(grp["Y_draft"], errors="coerce").fillna(0).sum())
            rate = drafts / n if n else float("nan")
            lo, hi = _wilson_ci(drafts, n)
            rows.append(
                {
                    "tj_quartile": int(tj_q),
                    "tj_label": TJ_QUARTILE_LABELS[int(tj_q)],
                    "vent": int(vent),
                    "bin_display": int(vent) + 1,
                    "n": n,
                    "drafts": drafts,
                    "draft_rate": rate,
                    "ci_lo": lo,
                    "ci_hi": hi,
                    "roster_pct_mean": float(grp["roster_pct"].mean()),
                    "T_j_hat_mean": float(grp["T_j_hat"].mean()),
                    "thin_cell": n < MIN_CELL_N_WARN,
                    "no_claim": n < MIN_CELL_N_CLAIM,
                }
            )
    tbl = pd.DataFrame(rows).sort_values(["tj_quartile", "vent"]).reset_index(drop=True)
    return work, tbl


def _quartile_rank_summary(tbl: pd.DataFrame, tj_q: int) -> dict:
    sub = tbl.loc[tbl["tj_quartile"] == tj_q]
    top = sub.loc[sub["vent"].isin((12, 13, 14, 15))]
    mid = sub.loc[sub["vent"].isin((5, 6, 7, 8))]
    top_n = int(top["n"].sum())
    top_d = int(top["drafts"].sum())
    mid_n = int(mid["n"].sum())
    mid_d = int(mid["drafts"].sum())
    top_rate = top_d / top_n if top_n else float("nan")
    mid_rate = mid_d / mid_n if mid_n else float("nan")
    top_lo, top_hi = _wilson_ci(top_d, top_n)
    mid_lo, mid_hi = _wilson_ci(mid_d, mid_n)
    return {
        "tj_quartile": tj_q,
        "tj_label": TJ_QUARTILE_LABELS[tj_q],
        "top_rank_ventiles_0idx": [12, 13, 14, 15],
        "top_rank_bins_1idx": [13, 14, 15, 16],
        "top_rank_n": top_n,
        "top_rank_drafts": top_d,
        "top_rank_rate": top_rate,
        "top_rank_ci_lo": top_lo,
        "top_rank_ci_hi": top_hi,
        "mid_rank_ventiles_0idx": [5, 6, 7, 8],
        "mid_rank_bins_1idx": [6, 7, 8, 9],
        "mid_rank_n": mid_n,
        "mid_rank_drafts": mid_d,
        "mid_rank_rate": mid_rate,
        "mid_rank_ci_lo": mid_lo,
        "mid_rank_ci_hi": mid_hi,
        "top_gt_mid": bool(top_rate > mid_rate) if top_n and mid_n else None,
    }


def plot_roster_rank_tj(
    spec: CctSpec,
    tbl: pd.DataFrame,
    work: pd.DataFrame,
    out_png: Path,
) -> None:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    seasons = seasons_label(spec.season_min, spec.season_max)
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharey=True)
    axes_flat = axes.ravel()

    for tj_q, ax in enumerate(axes_flat):
        sub = tbl.loc[tbl["tj_quartile"] == tj_q]
        if sub.empty:
            ax.set_visible(False)
            continue
        x = sub["bin_display"].to_numpy(dtype=float)
        y = sub["draft_rate"].to_numpy(dtype=float)
        yerr_lo = y - sub["ci_lo"].to_numpy(dtype=float)
        yerr_hi = sub["ci_hi"].to_numpy(dtype=float) - y
        colors = [THIN_COLOR if thin else OTHER_COLOR for thin in sub["thin_cell"]]
        ax.bar(x, y, color=colors, edgecolor="white", alpha=0.92, width=0.85)
        ax.errorbar(
            x,
            y,
            yerr=[yerr_lo, yerr_hi],
            fmt="none",
            ecolor="0.25",
            capsize=2,
            linewidth=0.8,
        )
        summ = _quartile_rank_summary(tbl, tj_q)
        ax.set_title(
            f"{TJ_QUARTILE_LABELS[tj_q]}\n"
            f"top rank {100*summ['top_rank_rate']:.1f}% vs mid {100*summ['mid_rank_rate']:.1f}%",
            fontsize=9,
        )
        ax.set_xlabel(r"Roster percentile ventile (1 = bottom on team)")
        ax.set_xticks(x[::2])
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        if tj_q in (0, 2):
            ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")

    q4 = _quartile_rank_summary(tbl, 3)
    q2 = _quartile_rank_summary(tbl, 1)
    fig.suptitle(
        rf"CCT Priority 3 — draft rate vs within-team rank · MBB {seasons}\n"
        rf"mg10 min20 · PPM $z$ {spec.ai_band_label} · faceted by $\hat{{T}}_j$ quartile",
        fontsize=11,
    )
    note = (
        f"Panel n={len(work):,} PS · drafts={int(work['Y_draft'].sum()):,} · "
        f"Q4 top>mid rank: {'YES' if q4['top_gt_mid'] else 'NO'}"
    )
    fig.text(0.5, 0.01, note, ha="center", fontsize=8, color="0.35")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")


def run_roster_rank_tj(spec: CctSpec, out_dir: Path) -> Path:
    ensure_hero_dirs()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / "CCT_draft_rate_roster_pct_by_tj_quartile.png"
    out_json = out_dir / "CCT_draft_rate_roster_pct_by_tj_quartile.json"

    use = _prepare_panel(spec)
    work, tbl = _roster_rank_table(use, spec)
    if tbl.empty:
        raise SystemExit("No rows for roster-rank table — check panel filters")

    plot_roster_rank_tj(spec, tbl, work, out_png)

    quartile_summaries = [_quartile_rank_summary(tbl, q) for q in range(4)]
    q4 = quartile_summaries[3]
    meta = {
        "diagnostic": "cct_roster_rank_tj",
        "date": date.today().isoformat(),
        "plot": "roster_rank_tj",
        "bdp_spec": "mg10 min20 11_21",
        "seasons": seasons_label(spec.season_min, spec.season_max),
        "panel_n": int(len(use)),
        "analysis_n": int(len(work)),
        "analysis_drafts": int(pd.to_numeric(work["Y_draft"], errors="coerce").fillna(0).sum()),
        "ai_lo": spec.ai_lo,
        "ai_hi": spec.ai_hi,
        "n_bins": spec.n_bins,
        "winsor": list(spec.winsor_quantiles),
        "min_minutes": spec.min_minutes,
        "min_team_season_games": spec.min_team_season_games,
        "perf_metric": spec.perf_metric,
        "cells": tbl.to_dict(orient="records"),
        "quartile_summaries": quartile_summaries,
        "cct_q4_top_rank_gt_mid_rank": q4["top_gt_mid"],
        "png": out_png.name,
    }
    out_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {out_json.relative_to(REPO)}")
    print(
        f"  Analysis n={meta['analysis_n']:,} drafts={meta['analysis_drafts']:,} · "
        f"Q4 top rank {100*q4['top_rank_rate']:.2f}% vs mid {100*q4['mid_rank_rate']:.2f}%"
    )
    _write_readme(out_dir, meta, plot_key="roster_rank_tj")
    return out_png


def _write_readme(out_dir: Path, meta: dict, *, plot_key: str) -> None:
    readme = out_dir / "CCT_README.md"
    lines = [
        "# CCT Act II outputs",
        "",
        f"**Updated:** {date.today().isoformat()}",
        "",
    ]
    p1_files = sorted(out_dir.glob("CCT_draft_rate_ai_band_poolq_loo*.json"))
    p3_json = out_dir / "CCT_draft_rate_roster_pct_by_tj_quartile.json"
    for p1_json in p1_files:
        p1 = json.loads(p1_json.read_text(encoding="utf-8"))
        squid = p1["squid_proxy"]
        jackal = p1["jackal_proxy"]
        pop = p1.get("population", "full panel")
        perf = str(p1.get("perf_metric", "ppm")).upper()
        lines.extend(
            [
                f"## Priority 1 — matched Â × poolq_loo ({perf} · {pop})",
                "",
                f"- Panel: mg10 min20 {p1['seasons']}",
                f"- Fixed {perf} z band: [{p1['ai_lo']}, {p1['ai_hi']}]",
                f"- Band n: {p1['band_n']:,} PS; {p1['band_drafts']:,} drafted",
                f"- **Squid** (mid pond): {100*squid['draft_rate']:.2f}% (n={squid['n']:,})",
                f"- **Jackal** (top pond): {100*jackal['draft_rate']:.2f}% (n={jackal['n']:,})",
                f"- **CCT signature (Squid > Jackal):** "
                f"{'**YES**' if p1['cct_signature_squid_gt_jackal'] else '**NO**'}",
                f"- Files: `{p1['png']}`, `{p1_json.name}`",
                "",
            ]
        )
    if p3_json.exists():
        p3 = json.loads(p3_json.read_text(encoding="utf-8"))
        q4 = p3["quartile_summaries"][3]
        band_note = (
            "full panel"
            if p3.get("ai_lo") is None
            else f"z ∈ [{p3['ai_lo']}, {p3['ai_hi']}]"
        )
        lines.extend(
            [
                "## Priority 3 — roster percentile × T̂_j quartile",
                "",
                f"- Panel: mg10 min20 {p3['seasons']} · {band_note}",
                f"- Analysis n: {p3['analysis_n']:,} PS; {p3['analysis_drafts']:,} drafted",
                f"- Q4 top roster rank: {100*q4['top_rank_rate']:.2f}% vs mid: {100*q4['mid_rank_rate']:.2f}%",
                f"- Top > mid at Q4: {'**YES**' if p3['cct_q4_top_rank_gt_mid_rank'] else '**NO**'}",
                "- Files: `CCT_draft_rate_roster_pct_by_tj_quartile.png`, `.json`",
                "",
            ]
        )
    lines.append("Legend on P1: green = Squid, orange = Jackal. Red bars: n < 30.")
    lines.append("")
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {readme.relative_to(REPO)}")


def _write_readme_all_grids(out_dir: Path) -> None:
    manifests = sorted(out_dir.glob("CCT_p1_grid_manifest_min*.json"))
    legacy = out_dir / "CCT_p1_grid_manifest.json"
    if legacy.exists() and not any("min20" in p.name for p in manifests):
        manifests = [legacy] + list(manifests)
    if not manifests:
        return
    readme = out_dir / "CCT_README.md"
    lines = [
        "# CCT Act II outputs",
        "",
        f"**Updated:** {date.today().isoformat()}",
        "",
    ]
    for manifest_path in manifests:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        lines.extend(
            [
                f"## Priority 1 grid — {manifest['panel']}",
                "",
                "3 metrics × 3 Â bands × {full panel, +DFT} = **18 plots**.",
                "",
                f"Manifest: `{manifest_path.name}`",
                "",
                "| Metric | Band | Pop | Band n | Squid | Jackal | CCT? | File |",
                "|--------|------|-----|--------|-------|--------|------|------|",
            ]
        )
        for row in manifest["cells"]:
            pop = "+DFT" if row["dft"] else "full"
            cct = "**YES**" if row["cct_squid_gt_jackal"] else "NO"
            lines.append(
                f"| {row['metric'].upper()} | [{row['ai_lo']}, {row['ai_hi']}] | {pop} | "
                f"{row['band_n']:,} | {100*row['squid_rate']:.1f}% | {100*row['jackal_rate']:.1f}% | "
                f"{cct} | `{row['png']}` |"
            )
        lines.append("")
    lines.extend(["## Priority 3", ""])
    p3_json = out_dir / "CCT_draft_rate_roster_pct_by_tj_quartile.json"
    if p3_json.exists():
        p3 = json.loads(p3_json.read_text(encoding="utf-8"))
        q4 = p3["quartile_summaries"][3]
        lines.append(
            f"- Q4 top rank {100*q4['top_rank_rate']:.1f}% vs mid {100*q4['mid_rank_rate']:.1f}% — "
            f"`CCT_draft_rate_roster_pct_by_tj_quartile.png`"
        )
    lines.extend(
        [
            "",
            "Filename pattern: `CCT_draft_rate_ai_band_poolq_loo_min{10|20}_{ppm|bpm|obpm}_z{lo}_{hi}_{allt|dft}.png`",
            "",
            "Legend: green = Squid (mid pond), orange = Jackal (top pond).",
            "",
        ]
    )
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {readme.relative_to(REPO)}")


def _resolve_ai_band(args: argparse.Namespace, plot: str) -> tuple[float | None, float | None]:
    has_lo = args.ai_lo is not None
    has_hi = args.ai_hi is not None
    if has_lo != has_hi:
        raise SystemExit("Pass both --ai-lo and --ai-hi, or neither.")
    if has_lo and has_hi:
        return float(args.ai_lo), float(args.ai_hi)
    if plot in ("matched_pond", "p1_grid") and plot == "matched_pond":
        return DEFAULT_AI_LO, DEFAULT_AI_HI
    return None, None


def _spec_from_args(args: argparse.Namespace) -> CctSpec:
    w = current_window()
    ai_lo, ai_hi = _resolve_ai_band(args, args.plot)
    return CctSpec(
        season_min=int(w.season_min),
        season_max=int(w.season_max),
        min_minutes=float(args.min_minutes),
        min_team_season_games=int(args.min_team_season_games),
        winsor_lo=float(args.winsor_lo),
        winsor_hi=float(args.winsor_hi),
        n_bins=int(args.n_bins),
        ai_lo=ai_lo,
        ai_hi=ai_hi,
        perf_metric=str(args.perf_metric).strip().lower(),
        dft=bool(args.dft),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="CCT conditional draft-rate plots (Act II).")
    add_window_args(parser)
    parser.add_argument(
        "--plot",
        choices=("matched_pond", "roster_rank_tj", "p1_grid"),
        default="matched_pond",
        help="Figure family (P1, P3, or full P1 grid).",
    )
    parser.add_argument("--min-minutes", type=float, default=DEFAULT_MIN_MINUTES)
    parser.add_argument("--min-team-season-games", type=int, default=10)
    parser.add_argument("--winsor-lo", type=float, default=DEFAULT_WINSOR_LO)
    parser.add_argument("--winsor-hi", type=float, default=DEFAULT_WINSOR_HI)
    parser.add_argument("--n-bins", type=int, default=DEFAULT_N_BINS)
    parser.add_argument("--ai-lo", type=float, default=None, help="Lower perf z band (P1 default 1.5).")
    parser.add_argument("--ai-hi", type=float, default=None, help="Upper perf z band (P1 default 2.0).")
    parser.add_argument("--perf-metric", type=str, default="ppm", choices=("ppm", "obpm", "bpm"))
    parser.add_argument(
        "--dft",
        action="store_true",
        help="+DFT subsample: teams with ≥1 draftee in window (all roster PS, not drafted-only).",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=BASIC_DATA_PLOTS,
        help="Output directory (default basic_data_plots/).",
    )
    args = parser.parse_args()
    activate_from_args(args)
    spec = _spec_from_args(args)
    out_dir = args.out_dir if args.out_dir.is_absolute() else REPO / args.out_dir

    print(
        f"CCT {args.plot} · {seasons_label(spec.season_min, spec.season_max)} · "
        f"{spec.perf_metric.upper()} · {spec.population_label} · "
        f"Â z {spec.ai_band_label} · mg{spec.min_team_season_games} min{spec.min_minutes:g}",
        flush=True,
    )
    if args.plot == "matched_pond":
        run_matched_pond(spec, out_dir)
    elif args.plot == "roster_rank_tj":
        run_roster_rank_tj(spec, out_dir)
    elif args.plot == "p1_grid":
        _panel_cache.clear()
        base = replace(spec, ai_lo=None, ai_hi=None)
        run_p1_grid(base, out_dir)


if __name__ == "__main__":
    main()
