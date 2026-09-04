#!/usr/bin/env python3
"""Tenure porch basic data plots — inference panel (HIGH/MEDIUM, LOO computable).

Mirrors reigning-hero / MBB BDP porch: distributions + uni-year pool interval overlap.

Run (repo root):
  python tenure/scripts/tenure_basic_plots.py
  python tenure/scripts/tenure_basic_plots.py --only overlap poolq_loo
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

REPO = Path(__file__).resolve().parents[2]
TENURE_PIPELINE = REPO / "tenure" / "tenure_pipeline"
sys.path.insert(0, str(TENURE_PIPELINE))
from decision_hero_prep import (  # noqa: E402
    build_dept_year_rosters,
    prepare_decision_hero_persons,
)
from decision_year_cohort import (  # noqa: E402
    REFERENCE_ASST_TIME_MAX,
    REFERENCE_ASST_TIME_MIN,
    build_decision_cohort_records,
    iter_resolved_exit_records,
    load_career_lookup,
)
SPORTS_SCRIPTS = REPO / "sports" / "scripts"
SCRIPTS_DIR = REPO / "tenure" / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from tenure_grain_labels import (  # noqa: E402
    ASST_PS,
    DECISION,
    stamp_window_badge,
    window_badge,
    window_display_label,
)
DEFAULT_IN = TENURE_PIPELINE / "faculty_panel_with_pools.jsonl"
OUT_DIR = (
    REPO
    / "3-Master_Plan"
    / "re_entry"
    / "HEROs_and_PASSes"
    / "tenure_sandbox"
    / "basic_data_plots"
)
TAG = "infHM"
TAG_PD29 = "pd29"
PREFIX = "TENURE"
CAREER_MASTER = TENURE_PIPELINE / "author_year_career_master.jsonl"
GRAIN_PD29_DECISION = "Decision cohort · all resolved · Alex Â (pubs_per_career_year)"
GRAIN_PD29_DEPT_LOO = "Decision cohort · dept pond LOO · whole dept · pubs_per_career_year"
PRIMARY_TIERS = frozenset({"HIGH", "MEDIUM"})
POOL_MIN = 2

GRAIN_ASST_PS_MEAN = window_display_label(ASST_PS, stat="mean")
GRAIN_ASST_PERSON_YEARS = "ASST-PS · asst person-years"


def _stamp_grain_badge(ax, window: str = ASST_PS, *, corner: str = "upper_left", y: float = 0.98) -> None:
    stamp_window_badge(ax, window, corner=corner, y=y)


TENURE_OVERLAP_LABELS = {
    "coverage_ylabel": "Uni-year pools covering this level",
    "span_ylabel": "Uni-year pools",
    "sample_ylabel": "Sample of {n} uni-year pools (sorted by $\\hat{{T}}_j$)",
    "all_ylabel": "All uni-year pools (sorted by $\\hat{{T}}_j$)",
    "coverage_grid_note": "{frac:.1%} of grid with $>$1 pool",
    "legend_actual": "Actual peer pools",
    "overlap_title": "Interval overlap along performance spectrum",
    "span_xlabel": r"Pool span ($\max \hat{A}_i - \min \hat{A}_i$)",
    "span_title": "Width of each pool's performance window",
    "sample_title": r"Pool $[\min, \max]$ intervals (sample)",
}

PD29_OVERLAP_LABELS = {
    **TENURE_OVERLAP_LABELS,
    "coverage_ylabel": "Dept-year pools covering this level",
    "span_ylabel": "Dept-year pools",
    "sample_ylabel": "Sample of {n} dept-year pools (sorted by $\\hat{{T}}_j$)",
    "all_ylabel": "All dept-year pools (sorted by $\\hat{{T}}_j$)",
}

PLOT_DPI = 150
TENURE_MASS_STEP = 10.0
PANEL_TOP_CUTS_PD29 = (7.0, 15.0, 25.0, 40.0)
PANEL_CUT_COLOR = "#7030a0"
TENURE_MASS_COLOR = "#c00000"
# ECDF palettes — keep mass-ECDF (blue vs orange) separate from outcome ECDF (blue vs red)
ECDF_COHORT_COLOR = "#2e75b6"
ECDF_MASS_TENURED_COLOR = "#ed7d31"
ECDF_OUTCOME_TENURED_COLOR = "#2166ac"
ECDF_OUTCOME_ATTRITION_COLOR = "#b2182b"
ECDF_ALL_BASELINE_COLOR = "#757575"
ECDF_DEPT_LOO_HIST_COLOR = "#4daf4a"


def load_inference_assistant_panel(in_path: Path) -> pd.DataFrame:
    """Assistant person-years: HIGH/MEDIUM + non-null poolq_loo_mean."""
    rows: list[dict] = []
    with in_path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("match_confidence") not in PRIMARY_TIERS:
                continue
            if r.get("rank") != "assistant":
                continue
            if r.get("poolq_loo_mean") is None:
                continue
            if r.get("transferred") or r.get("exclude_from_metrics"):
                continue
            rows.append(r)
    if not rows:
        raise SystemExit(f"No inference assistant rows in {in_path}")
    return pd.DataFrame(rows)


def person_level_loo(panel: pd.DataFrame) -> pd.DataFrame:
    """One row per faculty_id — mean poolq_loo_mean + mean pubs_year (HERO grain)."""
    work = panel.copy()
    work["poolq_loo_mean"] = pd.to_numeric(work["poolq_loo_mean"], errors="coerce")
    work["pubs_year"] = pd.to_numeric(work["pubs_year"], errors="coerce")
    agg = (
        work.groupby("faculty_id", observed=True)
        .agg(
            loo_mean=("poolq_loo_mean", "mean"),
            pubs_mean=("pubs_year", "mean"),
            n_asst_years=("poolq_loo_mean", "count"),
            tenure=("tenure_event", "max"),
            attrition=("attrition", "max"),
            censored=("censored", "max"),
        )
        .reset_index()
    )
    return agg


def _outcome_group(persons: pd.DataFrame) -> pd.Series:
    """Mutually exclusive outcome label at person grain (HERO panel)."""
    def _one(row: pd.Series) -> str:
        if bool(row["tenure"]):
            return "tenured"
        if bool(row["attrition"]):
            return "attrition"
        if bool(row["censored"]):
            return "censored"
        return "other"

    return persons.apply(_one, axis=1)


OUTCOME_COLORS = {
    "tenured": ECDF_OUTCOME_TENURED_COLOR,
    "attrition": ECDF_OUTCOME_ATTRITION_COLOR,
    "censored": ECDF_ALL_BASELINE_COLOR,
}
OUTCOME_LABELS = {
    "tenured": "Tenured (promoted)",
    "attrition": "Attrition (left as asst)",
    "censored": "Censored (outcome unknown)",
}


def _summary(name: str, values: np.ndarray) -> dict:
    v = np.asarray(values, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return {"label": name, "n": 0}
    return {
        "label": name,
        "n": int(v.size),
        "mean": float(v.mean()),
        "std": float(v.std()),
        "min": float(v.min()),
        "max": float(v.max()),
        "median": float(np.median(v)),
    }


def _write_meta(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path.relative_to(REPO)}")


def _plot_ecdf(
    ax,
    values: np.ndarray,
    *,
    color: str = "steelblue",
    label: str | None = None,
    lw: float = 1.8,
    ls: str = "-",
    alpha: float = 1.0,
) -> None:
    v = np.sort(values[np.isfinite(values)])
    if v.size == 0:
        return
    ys = np.arange(1, v.size + 1) / v.size
    ax.step(v, ys, where="post", color=color, lw=lw, label=label, ls=ls, alpha=alpha)


def _career_rate_lookup(
    career: dict[tuple[str, int], dict],
    faculty_id: str,
    year: int,
) -> float | None:
    row = career.get((str(faculty_id), int(year)))
    if not row:
        return None
    raw = row.get("pubs_per_career_year")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _hero_persons_with_dept_mean(panel_path: Path) -> tuple[pd.DataFrame, dict]:
    """Decision HERO persons + dept mean career rate (T̂_j, includes focal)."""
    career = load_career_lookup(CAREER_MASTER)
    rosters = build_dept_year_rosters(panel_path)
    df, prep_stats = _hero_persons_df(panel_path)
    dept_means: list[float] = []
    for _, row in df.iterrows():
        roster = rosters.get((str(row["uni_slug"]), int(row["decision_year"])), set())
        rates = [
            r
            for pfid in roster
            if (r := _career_rate_lookup(career, pfid, int(row["decision_year"]))) is not None
        ]
        dept_means.append(float(np.mean(rates)) if rates else float("nan"))
    df["dept_mean_career_rate"] = dept_means
    return df, prep_stats


def _prepare_pd29_dept_overlap(panel_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Dept × calendar-year pools on Alex career pubs rate (z within year)."""
    career = load_career_lookup(CAREER_MASTER)
    rosters = build_dept_year_rosters(panel_path)
    rows: list[dict] = []
    for (uni, year), roster in rosters.items():
        for fid in roster:
            rate = _career_rate_lookup(career, fid, int(year))
            if rate is None:
                continue
            rows.append(
                {
                    "faculty_id": str(fid),
                    "uni_slug": str(uni),
                    "year": int(year),
                    "career_rate": rate,
                }
            )
    work = pd.DataFrame(rows)
    if work.empty:
        raise SystemExit("No career-rate rows for PD29 dept overlap.")

    def _z(s: pd.Series) -> pd.Series:
        mu = float(s.mean())
        sd = float(s.std())
        if sd <= 0:
            return pd.Series(0.0, index=s.index)
        return (s - mu) / sd

    work["perf"] = work.groupby("year", observed=True)["career_rate"].transform(_z)
    iv = (
        work.groupby(["uni_slug", "year"], observed=True)["perf"]
        .agg(
            A_hat_min="min",
            A_hat_max="max",
            T_j_hat="mean",
            roster_n="count",
        )
        .reset_index()
    )
    iv = iv.loc[iv["roster_n"] >= POOL_MIN].copy()
    iv["perf_span"] = iv["A_hat_max"] - iv["A_hat_min"]
    iv["team_id"] = iv["uni_slug"]
    iv["season"] = iv["year"]
    work["team_id"] = work["uni_slug"]
    work["season"] = work["year"]
    return iv, work


def run_poolq_loo_distribution(persons: pd.DataFrame) -> Path:
    vals = persons["loo_mean"].to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vals, bins=40, color="steelblue", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Person-level mean poolq_LOO (pubs/yr)", fontsize=10)
    ax.set_ylabel("Persons", fontsize=10)
    ax.set_title(
        f"Tenure inference panel — poolq_LOO distribution (N={len(persons):,} persons)",
        fontsize=11,
        fontweight="bold",
    )
    stats = _summary("loo_mean", vals)
    ax.text(
        0.98,
        0.98,
        f"median={stats['median']:.2f} · mean={stats['mean']:.2f} · sd={stats['std']:.2f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    _stamp_grain_badge(ax, ASST_PS, corner="upper_left")
    stem = f"{PREFIX}_poolq_loo_distribution_{TAG}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_poolq_loo_distribution",
            "date": date.today().isoformat(),
            "filter": "HIGH/MEDIUM inference · assistant rows · LOO computable",
            "grain": GRAIN_ASST_PS_MEAN,
            "loo_mean": stats,
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_pubs_year_distribution(panel: pd.DataFrame) -> Path:
    vals = pd.to_numeric(panel["pubs_year"], errors="coerce").dropna().to_numpy(dtype=float)
    pos = vals[vals > 0]
    n_zero = int((vals == 0).sum())
    p99 = float(np.percentile(vals, 99)) if vals.size else 50.0
    x_cap = max(p99 * 1.05, 10.0)

    fig, ax = plt.subplots(figsize=(8.5, 5.25))
    ax.hist(vals, bins=40, range=(0, x_cap), color="steelblue", edgecolor="white", alpha=0.85)
    ax.set_xlim(0, x_cap)
    ax.set_xlabel("Own pubs_year (assistant person-years)", fontsize=10)
    ax.set_ylabel("Assistant-years", fontsize=10)
    ax.set_title(
        f"Tenure inference panel — own publication rate (N={len(vals):,} asst-years)",
        fontsize=11,
        fontweight="bold",
    )
    stats_all = _summary("pubs_year", vals)
    stats_pos = _summary("pubs_year_gt0", pos)
    n_above_cap = int((vals > x_cap).sum())
    ax.text(
        0.98,
        0.98,
        f"all: median={stats_all['median']:.1f} · mean={stats_all['mean']:.1f} · "
        f"zero={n_zero:,} ({100 * n_zero / len(vals):.0f}%)\n"
        f"x capped at {x_cap:.0f} ({n_above_cap} above; max={stats_all['max']:.0f})",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8.5,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )

    # Inset: intensive margin (pubs > 0 only)
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    axins = inset_axes(ax, width="44%", height="44%", loc="center right", borderpad=2.2)
    pos_cap = max(float(np.percentile(pos, 99)) * 1.05, 10.0) if pos.size else x_cap
    axins.hist(pos, bins=28, range=(0.5, pos_cap), color="#d6604d", edgecolor="white", alpha=0.9)
    axins.set_xlim(0.5, pos_cap)
    axins.set_title(f"Inset: pubs > 0 (N={len(pos):,})", fontsize=8, fontweight="bold")
    axins.set_xlabel("pubs_year", fontsize=7)
    axins.set_ylabel("Count", fontsize=7)
    axins.tick_params(labelsize=6.5)
    axins.text(
        0.97,
        0.97,
        f"med={stats_pos['median']:.1f}\nmean={stats_pos['mean']:.1f}",
        transform=axins.transAxes,
        ha="right",
        va="top",
        fontsize=6.5,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    _stamp_grain_badge(ax, ASST_PS, corner="upper_left")
    stem = f"{PREFIX}_pubs_year_distribution_{TAG}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_pubs_year_distribution",
            "date": date.today().isoformat(),
            "filter": "HIGH/MEDIUM inference · assistant rows · LOO computable",
            "grain": GRAIN_ASST_PERSON_YEARS,
            "pubs_year": stats_all,
            "pubs_year_gt0": stats_pos,
            "n_zero": n_zero,
            "pct_zero": round(100 * n_zero / len(vals), 2),
            "display_x_cap": x_cap,
            "inset_x_cap": pos_cap,
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_pool_size_distribution(panel: pd.DataFrame) -> Path:
    vals = pd.to_numeric(panel["pool_size_oa_loo"], errors="coerce").dropna().to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vals, bins=30, color="steelblue", edgecolor="white", alpha=0.85)
    ax.set_xlabel("pool_size_oa_loo (OA peers after leave-one-out)", fontsize=10)
    ax.set_ylabel("Assistant-years", fontsize=10)
    ax.set_title(
        f"Tenure inference panel — LOO peer pool size (N={len(vals):,} asst-years)",
        fontsize=11,
        fontweight="bold",
    )
    stats = _summary("pool_size_oa_loo", vals)
    ax.text(
        0.98,
        0.98,
        f"median={stats['median']:.0f} · mean={stats['mean']:.1f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    _stamp_grain_badge(ax, ASST_PS, corner="upper_left")
    stem = f"{PREFIX}_pool_size_loo_distribution_{TAG}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_pool_size_loo_distribution",
            "date": date.today().isoformat(),
            "filter": "HIGH/MEDIUM inference · assistant rows · LOO computable",
            "grain": GRAIN_ASST_PERSON_YEARS,
            "pool_size_oa_loo": stats,
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def _prepare_overlap_panel(
    panel: pd.DataFrame, *, pubs_gt0: bool = False
) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = panel.copy()
    work["pubs_year"] = pd.to_numeric(work["pubs_year"], errors="coerce")
    work = work.dropna(subset=["pubs_year", "uni_slug", "year"])
    work = work.loc[work["openalex_id"].astype(str).str.len() > 0].copy()
    if pubs_gt0:
        work = work.loc[work["pubs_year"] > 0].copy()

    def _z(s: pd.Series) -> pd.Series:
        mu = float(s.mean())
        sd = float(s.std())
        if sd <= 0:
            return pd.Series(0.0, index=s.index)
        return (s - mu) / sd

    work["perf"] = work.groupby("year", observed=True)["pubs_year"].transform(_z)

    iv = (
        work.groupby(["uni_slug", "year"], observed=True)["perf"]
        .agg(
            A_hat_min="min",
            A_hat_max="max",
            T_j_hat="mean",
            roster_n="count",
        )
        .reset_index()
    )
    iv = iv.loc[iv["roster_n"] >= POOL_MIN].copy()
    iv["perf_span"] = iv["A_hat_max"] - iv["A_hat_min"]
    iv["team_id"] = iv["uni_slug"]
    iv["season"] = iv["year"]
    work["team_id"] = work["uni_slug"]
    work["season"] = work["year"]
    return iv, work


def _compute_h_sort(work: pd.DataFrame) -> float | None:
    sys.path.insert(0, str(REPO / "sports"))
    try:
        import importlib

        gc = importlib.import_module("541_grandchild_homophily_assign")
        use = work.dropna(subset=["perf"]).copy()
        use["pool_id"] = use.groupby(["team_id", "season"], observed=True).ngroup()
        return float(
            gc.realized_sorting_index_H_sort(
                use["perf"].to_numpy(dtype=float),
                use["pool_id"].to_numpy(dtype=np.int64),
            )
        )
    except Exception as exc:
        print(f"  ⚠  H_sort skipped: {exc}")
        return None


def run_interval_overlap(panel: pd.DataFrame, *, pubs_gt0: bool = False) -> Path:
    sys.path.insert(0, str(SPORTS_SCRIPTS))
    from empirical_team_interval_overlap import build_figure

    iv, work = _prepare_overlap_panel(panel, pubs_gt0=pubs_gt0)
    y0, y1 = int(work["year"].min()), int(work["year"].max())
    seasons = f"{y0}-{y1}"

    suffix = "_pubs_gt0" if pubs_gt0 else ""
    stem = f"{PREFIX}_pool_interval_overlap_{TAG}{suffix}"
    out_png = OUT_DIR / f"{stem}.png"
    out_csv = OUT_DIR / f"{stem}_uni_year.csv"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    iv.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv.relative_to(REPO)}")

    h_sort = _compute_h_sort(work)
    h_line = f"\nRealized sorting $H_{{sort}}={h_sort:.3f}$" if h_sort is not None else ""
    gt0_line = " · pubs > 0 only" if pubs_gt0 else ""
    stats = build_figure(
        iv,
        work,
        png_path=out_png,
        seasons=seasons,
        h_sort=h_sort,
        suptitle=(
            f"Tenure inference — uni-year peer pool interval overlap ({seasons})"
            + gt0_line
            + h_line
        ),
        xlab=r"Assistant own pubs/year ($z$ within calendar year; pubs $>$ 0)"
        if pubs_gt0
        else r"Assistant own pubs/year ($z$ within calendar year)",
        labels=TENURE_OVERLAP_LABELS,
        grain_badge=window_badge(ASST_PS),
    )

    base_filter = "HIGH/MEDIUM inference · OA-matched assistant-years · LOO computable"
    meta = {
        "diagnostic": "tenure_pool_interval_overlap_pubs_gt0"
        if pubs_gt0
        else "tenure_pool_interval_overlap",
        "date": date.today().isoformat(),
        "filter": base_filter + (" · pubs_year > 0" if pubs_gt0 else ""),
        "pool_unit": "uni_slug × year (OpenAlex assistant peer pool)",
        "grain": GRAIN_ASST_PERSON_YEARS,
        "perf": "pubs_year z-scored within calendar year"
        + (" · among pubs > 0 rows only" if pubs_gt0 else ""),
        "pool_min_assistants": POOL_MIN,
        "seasons": seasons,
        **stats,
        "n_uni_year_pools": stats.get("n_team_seasons"),
        "n_assistant_years": stats.get("n_player_seasons"),
        "outputs": {"png": out_png.name, "uni_year_csv": out_csv.name},
    }
    _write_meta(out_meta, meta)
    return out_png


def run_pubs_by_outcome(persons: pd.DataFrame) -> Path:
    """Person-level mean pubs_year by tenure / attrition / censored."""
    work = persons.copy()
    work["outcome"] = _outcome_group(work)
    x_cap = max(float(work["pubs_mean"].quantile(0.99)) * 1.05, 10.0)

    fig, ax = plt.subplots(figsize=(8.5, 5.25))
    meta_groups: dict[str, dict] = {}
    bins = np.linspace(0, x_cap, 28)

    for key in ("tenured", "attrition", "censored"):
        vals = work.loc[work["outcome"] == key, "pubs_mean"].to_numpy(dtype=float)
        meta_groups[key] = _summary(key, vals)
        if vals.size == 0:
            continue
        ax.hist(
            vals,
            bins=bins,
            alpha=0.55,
            color=OUTCOME_COLORS[key],
            edgecolor="white",
            label=f"{OUTCOME_LABELS[key]} (N={len(vals):,})",
        )

    ax.set_xlim(0, x_cap)
    ax.set_xlabel("Person-level mean own pubs/year (assistant years)", fontsize=10)
    ax.set_ylabel("Persons", fontsize=10)
    ax.set_title(
        f"Inference panel — own pubs by outcome (HERO N={len(work):,} persons)",
        fontsize=11,
        fontweight="bold",
    )
    ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.0, 0.68))
    ax.text(
        0.02,
        0.98,
        "\n".join(
            f"{OUTCOME_LABELS[k].split('(')[0].strip()}: med={meta_groups[k].get('median', 0):.1f} · "
            f"mean={meta_groups[k].get('mean', 0):.1f}"
            for k in ("tenured", "attrition", "censored")
            if meta_groups[k].get("n", 0) > 0
        ),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    _stamp_grain_badge(ax, ASST_PS, corner="upper_right")

    stem = f"{PREFIX}_pubs_mean_by_outcome_{TAG}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_pubs_mean_by_outcome",
            "date": date.today().isoformat(),
            "grain": GRAIN_ASST_PS_MEAN,
            "filter": "HIGH/MEDIUM inference · LOO computable",
            **{k: meta_groups[k] for k in meta_groups},
            "display_x_cap": x_cap,
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_pubs_tenured(persons: pd.DataFrame) -> Path:
    """Promoted instructors only — person-level mean pubs_year (+ inset pubs_mean > 0)."""
    tenured = persons.loc[persons["tenure"] == True].copy()  # noqa: E712
    vals = tenured["pubs_mean"].to_numpy(dtype=float)
    pos = vals[vals > 0]
    p99 = float(np.percentile(vals, 99)) if vals.size else 10.0
    x_cap = max(p99 * 1.05, 10.0)

    fig, ax = plt.subplots(figsize=(8.5, 5.25))
    ax.hist(vals, bins=28, range=(0, x_cap), color=OUTCOME_COLORS["tenured"], edgecolor="white", alpha=0.88)
    ax.set_xlim(0, x_cap)
    ax.set_xlabel("Person-level mean own pubs/year (assistant years)", fontsize=10)
    ax.set_ylabel("Tenured persons", fontsize=10)
    ax.set_title(
        f"Promoted instructors — own pubs distribution (N={len(tenured):,} tenured)",
        fontsize=11,
        fontweight="bold",
    )
    stats_all = _summary("tenured_pubs_mean", vals)
    stats_pos = _summary("tenured_pubs_mean_gt0", pos)
    n_zero = int((vals == 0).sum())
    ax.text(
        0.98,
        0.98,
        f"med={stats_all['median']:.1f} · mean={stats_all['mean']:.1f} · "
        f"zero mean={n_zero} ({100 * n_zero / len(vals):.0f}%)\n"
        f"x capped at {x_cap:.0f} (max={stats_all['max']:.0f})",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=8.5,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    _stamp_grain_badge(ax, ASST_PS, corner="upper_left")

    if pos.size:
        from mpl_toolkits.axes_grid1.inset_locator import inset_axes

        axins = inset_axes(ax, width="42%", height="42%", loc="center right", borderpad=2.2)
        pos_cap = max(float(np.percentile(pos, 99)) * 1.05, 5.0)
        axins.hist(pos, bins=22, range=(0.01, pos_cap), color="#4393C3", edgecolor="white", alpha=0.9)
        axins.set_xlim(0.01, pos_cap)
        axins.set_title(f"Inset: mean > 0 (N={len(pos):,})", fontsize=8, fontweight="bold")
        axins.set_xlabel("pubs/year", fontsize=7)
        axins.set_ylabel("Count", fontsize=7)
        axins.tick_params(labelsize=6.5)
        axins.text(
            0.97,
            0.97,
            f"med={stats_pos['median']:.1f}\nmean={stats_pos['mean']:.1f}",
            transform=axins.transAxes,
            ha="right",
            va="top",
            fontsize=6.5,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
        )

    stem = f"{PREFIX}_pubs_mean_tenured_{TAG}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_pubs_mean_tenured",
            "date": date.today().isoformat(),
            "grain": GRAIN_ASST_PS_MEAN + " · tenure_event only",
            "tenured_pubs_mean": stats_all,
            "tenured_pubs_mean_gt0": stats_pos,
            "n_zero_mean": n_zero,
            "display_x_cap": x_cap,
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_loo_by_outcome(persons: pd.DataFrame) -> Path:
    """Person-level mean poolq_LOO by outcome — mirrors pubs split for HERO context."""
    work = persons.copy()
    work["outcome"] = _outcome_group(work)
    x_cap = max(float(work["loo_mean"].quantile(0.99)) * 1.05, 5.0)

    fig, ax = plt.subplots(figsize=(8.5, 5.25))
    meta_groups: dict[str, dict] = {}
    bins = np.linspace(0, x_cap, 28)

    for key in ("tenured", "attrition", "censored"):
        vals = work.loc[work["outcome"] == key, "loo_mean"].to_numpy(dtype=float)
        meta_groups[key] = _summary(key, vals)
        if vals.size == 0:
            continue
        ax.hist(
            vals,
            bins=bins,
            alpha=0.55,
            color=OUTCOME_COLORS[key],
            edgecolor="white",
            label=f"{OUTCOME_LABELS[key]} (N={len(vals):,})",
        )

    ax.set_xlim(0, x_cap)
    ax.set_xlabel("Person-level mean poolq_LOO (pubs/yr)", fontsize=10)
    ax.set_ylabel("Persons", fontsize=10)
    ax.set_title(
        f"Inference panel — peer LOO by outcome (HERO N={len(work):,} persons)",
        fontsize=11,
        fontweight="bold",
    )
    ax.legend(fontsize=8, loc="upper right", bbox_to_anchor=(1.0, 0.68))
    _stamp_grain_badge(ax, ASST_PS, corner="upper_right")

    stem = f"{PREFIX}_poolq_loo_by_outcome_{TAG}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_poolq_loo_by_outcome",
            "date": date.today().isoformat(),
            "grain": GRAIN_ASST_PS_MEAN,
            **{k: meta_groups[k] for k in meta_groups},
            "display_x_cap": x_cap,
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def _load_pd29_cohort(
    panel_path: Path,
    *,
    asst_time_min: int | None = None,
    asst_time_max: int | None = None,
) -> tuple[pd.DataFrame, dict]:
    records, stats = build_decision_cohort_records(
        panel_path,
        CAREER_MASTER,
        asst_time_min=asst_time_min,
        asst_time_max=asst_time_max,
    )
    if not records:
        raise SystemExit(
            "No decision cohort rows. Check panel + author_year_career_master.jsonl."
        )
    df = pd.DataFrame(records)
    df["outcome"] = df.apply(
        lambda r: "tenured"
        if r["tenure_event"]
        else ("attrition" if r["attrition"] else "other"),
        axis=1,
    )
    return df, stats


def run_decision_asst_time_histogram(panel_path: Path, *, tag: str = TAG_PD29) -> Path:
    """Resolved exits — assistant time at last assistant year (reference band shaded)."""
    times: list[int] = []
    for rec in iter_resolved_exit_records(panel_path):
        t = rec.get("asst_time")
        if t is not None:
            times.append(int(t))
    vals = np.asarray(times, dtype=int)
    fig, ax = plt.subplots(figsize=(8, 5))
    bins = np.arange(0.5, max(vals.max() + 1.5, 10.5), 1.0)
    ax.hist(vals, bins=bins, color="steelblue", edgecolor="white", alpha=0.88)
    ax.axvspan(
        REFERENCE_ASST_TIME_MIN - 0.5,
        REFERENCE_ASST_TIME_MAX + 0.5,
        color="#FFF3CD",
        alpha=0.45,
        zorder=0,
    )
    ax.set_xlabel("asst_time at exit (last assistant year)", fontsize=10)
    ax.set_ylabel("Resolved persons", fontsize=10)
    ax.set_title(
        f"Assistant time at exit — all resolved (N={len(vals):,})",
        fontsize=11,
        fontweight="bold",
    )
    n_ref = int(
        ((vals >= REFERENCE_ASST_TIME_MIN) & (vals <= REFERENCE_ASST_TIME_MAX)).sum()
    )
    ax.text(
        0.98,
        0.98,
        f"reference band {REFERENCE_ASST_TIME_MIN}–{REFERENCE_ASST_TIME_MAX}: "
        f"{n_ref:,} ({100 * n_ref / len(vals):.1f}%)\n"
        f"median asst_time={int(np.median(vals))}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    stem = f"{PREFIX}_decision_asst_time_exit_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_decision_asst_time_at_exit",
            "date": date.today().isoformat(),
            "filter": "HIGH/MEDIUM · resolved (tenure or attrition) · excl. transferred",
            "grain": "exit cross-section",
            "reference_asst_time_band": [REFERENCE_ASST_TIME_MIN, REFERENCE_ASST_TIME_MAX],
            "n_resolved": len(vals),
            "n_in_reference_band": n_ref,
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_career_rate_distribution(cohort: pd.DataFrame, *, tag: str = TAG_PD29) -> Path:
    vals = pd.to_numeric(cohort["pubs_per_career_year"], errors="coerce").dropna().to_numpy(float)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vals, bins=32, color="#2166AC", edgecolor="white", alpha=0.88)
    ax.set_xlabel(r"Alex $\hat{A}$ — cum pubs $\div$ career age at decision year", fontsize=10)
    ax.set_ylabel("Persons", fontsize=10)
    ax.set_title(
        f"Decision cohort — career pubs rate (N={len(vals):,} with rate)",
        fontsize=11,
        fontweight="bold",
    )
    stats = _summary("pubs_per_career_year", vals)
    ax.text(
        0.98,
        0.98,
        f"med={stats['median']:.2f} · mean={stats['mean']:.2f} · sd={stats['std']:.2f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    stem = f"{PREFIX}_pubs_career_rate_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_pubs_per_career_year_pd29",
            "date": date.today().isoformat(),
            "grain": GRAIN_PD29_DECISION,
            "pubs_per_career_year": stats,
            "n_cohort": len(cohort),
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_career_rate_by_outcome(cohort: pd.DataFrame, *, tag: str = TAG_PD29) -> Path:
    work = cohort.dropna(subset=["pubs_per_career_year"]).copy()
    x_cap = max(float(work["pubs_per_career_year"].quantile(0.99)) * 1.05, 5.0)
    fig, ax = plt.subplots(figsize=(8.5, 5.25))
    meta_groups: dict[str, dict] = {}
    bins = np.linspace(0, x_cap, 26)
    for key in ("tenured", "attrition"):
        vals = work.loc[work["outcome"] == key, "pubs_per_career_year"].to_numpy(dtype=float)
        meta_groups[key] = _summary(key, vals)
        if vals.size == 0:
            continue
        ax.hist(
            vals,
            bins=bins,
            alpha=0.58,
            color=OUTCOME_COLORS[key],
            edgecolor="white",
            label=f"{OUTCOME_LABELS[key]} (N={len(vals):,})",
        )
    ax.set_xlim(0, x_cap)
    ax.set_xlabel(r"Career pubs rate at decision ($\mathrm{cum}/(\mathrm{yr}-\mathrm{first\ pub})$)", fontsize=10)
    ax.set_ylabel("Persons", fontsize=10)
    ax.set_title(
        rf"Decision cohort — career pubs rate by outcome (N={len(work):,})",
        fontsize=11,
        fontweight="bold",
    )
    ax.legend(fontsize=8, loc="upper right")
    stem = f"{PREFIX}_pubs_career_rate_by_outcome_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_career_rate_by_outcome_pd29",
            "date": date.today().isoformat(),
            "grain": GRAIN_PD29_DECISION,
            **{k: meta_groups[k] for k in meta_groups},
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_annual_zero_tenured(cohort: pd.DataFrame, *, tag: str = TAG_PD29) -> Path:
    """Alex porch: promoted with pubs_year=0 at decision but positive career rate."""
    tenured = cohort.loc[cohort["tenure_event"] == True].copy()  # noqa: E712
    py = pd.to_numeric(tenured["pubs_year"], errors="coerce")
    rate = pd.to_numeric(tenured["pubs_per_career_year"], errors="coerce")
    zero_annual = (py.fillna(0) == 0) & rate.notna() & (rate > 0)
    n_zero = int(zero_annual.sum())
    n_t = len(tenured)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    labels = ["annual=0\n career rate>0", "other tenured"]
    sizes = [n_zero, max(n_t - n_zero, 0)]
    colors = ["#D6604D", "#2166AC"]
    ax.bar(labels, sizes, color=colors, edgecolor="white", alpha=0.9)
    ax.set_ylabel("Tenured (resolved cohort)", fontsize=10)
    ax.set_title(
        "Tenured with zero decision-year pubs but positive career rate",
        fontsize=11,
        fontweight="bold",
    )
    pct = 100 * n_zero / n_t if n_t else 0
    ax.text(
        0.5,
        0.95,
        f"N={n_t} tenured · zero annual / positive career: {n_zero} ({pct:.0f}%)",
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="#FFF3CD", alpha=0.9),
    )
    stem = f"{PREFIX}_annual_zero_tenured_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_annual_zero_positive_career_pd29",
            "date": date.today().isoformat(),
            "grain": GRAIN_PD29_DECISION,
            "n_tenured": n_t,
            "n_zero_annual_positive_career": n_zero,
            "pct": round(pct, 2),
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def _hero_persons_df(panel_path: Path) -> tuple[pd.DataFrame, dict]:
    persons, stats = prepare_decision_hero_persons(panel_path, CAREER_MASTER)
    if not persons:
        raise SystemExit("No decision HERO persons with computable dept LOO.")
    df = pd.DataFrame(persons)
    df["outcome"] = df.apply(
        lambda r: "tenured" if r["tenure"] else "attrition",
        axis=1,
    )
    return df, stats


def run_dept_loo_distribution(panel_path: Path, *, tag: str = TAG_PD29) -> Path:
    """Dept pond LOO career rate — MBB-style hist | ECDF with outcome overlay."""
    df, prep_stats = _hero_persons_df(panel_path)
    work = df.dropna(subset=["dept_loo_career_rate"]).copy()
    loo = work["dept_loo_career_rate"].to_numpy(dtype=float)
    stats = _summary("dept_loo_career_rate", loo)
    med_pool = float(np.median(work["pool_size_rate_loo"]))

    lo = float(np.min(loo)) if loo.size else 0.0
    hi = float(np.max(loo)) if loo.size else 1.0
    bins = np.linspace(lo, hi, 36)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    fig.subplots_adjust(wspace=0.28, top=0.84, bottom=0.16)

    ax = axes[0]
    ax.hist(
        loo,
        bins=bins,
        color=ECDF_DEPT_LOO_HIST_COLOR,
        alpha=0.85,
        edgecolor="white",
        linewidth=0.35,
    )
    ax.axvline(stats["median"], color="0.35", linestyle=":", linewidth=1.4, label=rf"Median = {stats['median']:.2f}")
    ax.set_xlabel("Dept pond LOO — mean peers' career pubs rate at decision year", fontsize=10)
    ax.set_ylabel("Persons", fontsize=10)
    ax.set_title(r"Peer talent environment (dept pond LOO)", fontsize=10)
    ax.legend(fontsize=6, loc="upper right", framealpha=0.95)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    _stamp_grain_badge(ax, DECISION, corner="upper_left", y=0.98)

    ax = axes[1]
    _plot_ecdf(
        ax,
        loo,
        color=ECDF_ALL_BASELINE_COLOR,
        label=rf"All resolved ($n={len(loo):,}$)",
        lw=1.4,
        ls=":",
        alpha=0.85,
    )
    meta_groups: dict[str, dict] = {"all": stats}
    for key in ("tenured", "attrition"):
        vals = work.loc[work["outcome"] == key, "dept_loo_career_rate"].to_numpy(dtype=float)
        meta_groups[key] = _summary(key, vals)
        if vals.size:
            _plot_ecdf(
                ax,
                vals,
                color=OUTCOME_COLORS[key],
                label=f"{OUTCOME_LABELS[key]} ($n={len(vals):,}$)",
                lw=2.6,
                ls="-" if key == "tenured" else "--",
            )
    ax.axhline(0.5, color="0.82", linestyle=":", linewidth=0.9)
    ax.axvline(stats["median"], color="0.35", linestyle=":", linewidth=1.4, label=rf"Median = {stats['median']:.2f}")
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Dept pond LOO — career pubs rate")
    ax.set_ylabel(r"ECDF  $F(x)$")
    ax.set_title("ECDF by outcome", fontsize=10)
    ax.legend(fontsize=6, loc="lower right", framealpha=0.95)
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.text(
        0.03,
        0.97,
        f"med={stats['median']:.2f} · μ={stats['mean']:.2f} · σ={stats['std']:.2f}\n"
        f"median LOO peer count={med_pool:.0f}",
        transform=ax.transAxes,
        va="top",
        ha="left",
        fontsize=8,
        bbox=dict(boxstyle="round,pad=0.35", facecolor="white", alpha=0.92, edgecolor="0.8"),
    )

    fig.suptitle(
        f"Decision cohort — dept pond LOO on Alex career rate (N={len(loo):,})",
        fontsize=11,
        fontweight="bold",
    )
    fig.text(
        0.5,
        0.02,
        GRAIN_PD29_DEPT_LOO,
        ha="center",
        va="bottom",
        fontsize=8,
        color="0.35",
    )

    stem = f"{PREFIX}_dept_loo_career_rate_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_dept_loo_career_rate_pd29",
            "date": date.today().isoformat(),
            "grain": GRAIN_PD29_DEPT_LOO,
            "format": "hist_ecdf_outcome_overlay",
            "dept_loo_career_rate": stats,
            **{k: meta_groups[k] for k in meta_groups if k != "all"},
            "n_cohort_resolved": prep_stats.get("n_cohort"),
            "n_with_dept_loo": len(loo),
            "peer_pool": "whole department at decision year · LOO excludes focal person",
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_dept_loo_by_outcome(panel_path: Path, *, tag: str = TAG_PD29) -> Path:
    """ECDF-only dept pond LOO by outcome (porch companion — main plot folds this in)."""
    df, prep_stats = _hero_persons_df(panel_path)
    work = df.dropna(subset=["dept_loo_career_rate"]).copy()
    lo = float(work["dept_loo_career_rate"].min())
    hi = float(work["dept_loo_career_rate"].max())

    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    _stamp_grain_badge(ax, DECISION, corner="upper_left", y=0.98)
    meta_groups: dict[str, dict] = {}
    for key in ("tenured", "attrition"):
        vals = work.loc[work["outcome"] == key, "dept_loo_career_rate"].to_numpy(dtype=float)
        meta_groups[key] = _summary(key, vals)
        if vals.size:
            _plot_ecdf(
                ax,
                vals,
                color=OUTCOME_COLORS[key],
                label=f"{OUTCOME_LABELS[key]} (N={len(vals):,})",
                lw=2.6,
                ls="-" if key == "tenured" else "--",
            )
    ax.axhline(0.5, color="0.82", linestyle=":", linewidth=0.9)
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(
        "Dept pond LOO — peers' career pubs rate at decision year",
        fontsize=10,
    )
    ax.set_ylabel(r"ECDF  $F(x)$", fontsize=10)
    ax.set_title(
        f"Decision cohort — dept pond LOO ECDF by outcome (N={len(work):,})",
        fontsize=11,
        fontweight="bold",
    )
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.25, linewidth=0.5)

    stem = f"{PREFIX}_dept_loo_career_rate_by_outcome_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_dept_loo_by_outcome_pd29",
            "date": date.today().isoformat(),
            "grain": GRAIN_PD29_DEPT_LOO,
            "format": "ecdf_only",
            "note": "Overlapping histogram retired; see dept_loo hist|ECDF panel",
            **{k: meta_groups[k] for k in meta_groups},
            "n_with_dept_loo": len(work),
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_ai_tj_pd29(panel_path: Path, *, tag: str = TAG_PD29) -> Path:
    """Dual histogram: own Â and dept T̂_j at decision year (Alex career rate)."""
    df, prep_stats = _hero_persons_with_dept_mean(panel_path)
    ai = pd.to_numeric(df["own_career_rate"], errors="coerce").dropna().to_numpy(dtype=float)
    tj = pd.to_numeric(df["dept_mean_career_rate"], errors="coerce").dropna().to_numpy(dtype=float)
    stats_ai = _summary("own_career_rate", ai)
    stats_tj = _summary("dept_mean_career_rate", tj)

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    fig.subplots_adjust(wspace=0.22, top=0.82, bottom=0.14)

    for ax, vals, stats, xlabel, title, color in (
        (
            axes[0],
            ai,
            stats_ai,
            r"Alex $\hat{A}$ — cum pubs $\div$ career age at decision",
            rf"Own ability ($n={stats_ai['n']:,}$)",
            ECDF_COHORT_COLOR,
        ),
        (
            axes[1],
            tj,
            stats_tj,
            r"Dept $\hat{T}_j$ — mean career pubs rate (whole dept)",
            rf"Dept talent ($n={stats_tj['n']:,}$)",
            ECDF_DEPT_LOO_HIST_COLOR,
        ),
    ):
        hi = max(float(np.percentile(vals, 99)) * 1.05, 5.0) if vals.size else 5.0
        ax.hist(vals, bins=32, range=(0, hi), color=color, edgecolor="white", alpha=0.88)
        ax.set_xlim(0, hi)
        ax.set_xlabel(xlabel, fontsize=9)
        ax.set_ylabel("Persons", fontsize=9)
        ax.set_title(title, fontsize=10)
        ax.grid(axis="y", alpha=0.25, linewidth=0.5)
        ax.text(
            0.97,
            0.98,
            f"mean={stats['mean']:.2f}  sd={stats['std']:.2f}",
            transform=ax.transAxes,
            va="top",
            ha="right",
            fontsize=7,
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white", alpha=0.92, edgecolor="0.8"),
        )

    fig.suptitle(
        "Decision cohort — own Â vs dept T̂_j (pubs_per_career_year at decision year)",
        fontsize=11,
        fontweight="bold",
    )
    fig.text(0.5, 0.02, GRAIN_PD29_DECISION, ha="center", va="bottom", fontsize=8, color="0.35")

    stem = f"{PREFIX}_BDP_Ai_Tj_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_ai_tj_pd29",
            "date": date.today().isoformat(),
            "grain": GRAIN_PD29_DECISION,
            "own_career_rate": stats_ai,
            "dept_mean_career_rate": stats_tj,
            "n_cohort": prep_stats.get("n_cohort"),
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_tenure_mass_ecdf_pd29(cohort: pd.DataFrame, *, tag: str = TAG_PD29) -> Path:
    """Tenure-mass ECDF on Alex Â — cohort vs tenured overlay (MBB panel 4 analog)."""
    work = cohort.dropna(subset=["pubs_per_career_year"]).copy()
    all_rates = work["pubs_per_career_year"].to_numpy(dtype=float)
    tenured_rates = work.loc[work["tenure_event"] == True, "pubs_per_career_year"].to_numpy(dtype=float)  # noqa: E712
    n_t = int(tenured_rates.size)
    n_all = int(all_rates.size)

    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    _plot_ecdf(
        ax,
        all_rates,
        color=ECDF_COHORT_COLOR,
        lw=2.2,
        label=rf"Resolved cohort ($n={n_all:,}$)",
    )
    _plot_ecdf(
        ax,
        tenured_rates,
        color=ECDF_MASS_TENURED_COLOR,
        lw=2.4,
        label=rf"Tenured ($n={n_t:,}$)",
    )

    masses = np.arange(TENURE_MASS_STEP, 100.0, TENURE_MASS_STEP)
    for m in masses:
        q = float(np.quantile(tenured_rates, m / 100.0)) if n_t else float("nan")
        if not np.isfinite(q):
            continue
        ax.axhline(m / 100.0, color=TENURE_MASS_COLOR, ls=":", lw=0.9, alpha=0.55)
        ax.plot(q, m / 100.0, "o", color=TENURE_MASS_COLOR, ms=4.0, zorder=5)
        if int(m) % 20 == 0:
            ax.annotate(
                f"{int(m)}%",
                xy=(q, m / 100.0),
                xytext=(4, 2),
                textcoords="offset points",
                fontsize=7,
                color=TENURE_MASS_COLOR,
            )

    for top in PANEL_TOP_CUTS_PD29:
        z = float(np.quantile(all_rates, 1.0 - top / 100.0))
        ax.axvline(z, color=PANEL_CUT_COLOR, ls="--", lw=1.4, alpha=0.85)
        ax.annotate(
            f"top {top:g}%",
            xy=(z, 0.02),
            xytext=(3, 8),
            textcoords="offset points",
            fontsize=7.5,
            color=PANEL_CUT_COLOR,
            rotation=90,
            va="bottom",
        )

    x_lo = float(min(all_rates.min(), tenured_rates.min())) if n_all and n_t else 0.0
    x_hi = float(max(all_rates.max(), tenured_rates.max())) if n_all else 5.0
    pad = 0.06 * (x_hi - x_lo) if x_hi > x_lo else 0.5
    ax.set_xlim(max(0, x_lo - pad), x_hi + pad)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"Alex $\hat{A}$ — cum pubs $\div$ career age at decision year", fontsize=10)
    ax.set_ylabel("Cumulative fraction", fontsize=10)
    ax.set_title(
        rf"Tenure-mass ECDF · grid {TENURE_MASS_STEP:g}% · panel top cuts",
        fontsize=11,
        fontweight="bold",
    )
    ax.grid(alpha=0.25, linewidth=0.5)
    ax.legend(loc="lower right", fontsize=9, framealpha=0.95)
    fig.text(0.5, 0.02, GRAIN_PD29_DECISION, ha="center", va="bottom", fontsize=8, color="0.35")

    stem = f"{PREFIX}_tenure_mass_ecdf_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_mass_ecdf_pd29",
            "date": date.today().isoformat(),
            "grain": GRAIN_PD29_DECISION,
            "n_cohort_with_rate": n_all,
            "n_tenured_with_rate": n_t,
            "tenure_mass_step_pct": TENURE_MASS_STEP,
            "panel_top_cuts_pct": list(PANEL_TOP_CUTS_PD29),
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


def run_overlap_pd29(panel_path: Path, *, tag: str = TAG_PD29) -> Path:
    """Dept-year interval overlap on career pubs rate (PD29 peer environment)."""
    sys.path.insert(0, str(SPORTS_SCRIPTS))
    from empirical_team_interval_overlap import build_figure

    iv, work = _prepare_pd29_dept_overlap(panel_path)
    y0, y1 = int(work["year"].min()), int(work["year"].max())
    seasons = f"{y0}-{y1}"

    stem = f"{PREFIX}_dept_interval_overlap_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_csv = OUT_DIR / f"{stem}_dept_year.csv"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    iv.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv.relative_to(REPO)}")

    h_sort = _compute_h_sort(work)
    h_line = f"\nRealized sorting $H_{{sort}}={h_sort:.3f}$" if h_sort is not None else ""
    stats = build_figure(
        iv,
        work,
        png_path=out_png,
        seasons=seasons,
        h_sort=h_sort,
        suptitle=(
            f"Tenure PD29 — dept-year interval overlap ({seasons})"
            + h_line
        ),
        xlab=r"Career pubs rate ($z$ within calendar year; cum/(yr$-$first pub))",
        labels=PD29_OVERLAP_LABELS,
        grain_badge=window_badge(DECISION),
    )

    meta = {
        "diagnostic": "tenure_dept_interval_overlap_pd29",
        "date": date.today().isoformat(),
        "grain": GRAIN_PD29_DEPT_LOO,
        "perf": "pubs_per_career_year z-scored within calendar year",
        "pool_unit": "uni_slug × decision calendar year (whole dept roster)",
        "pool_min_faculty": POOL_MIN,
        "seasons": seasons,
        **stats,
        "n_dept_year_pools": stats.get("n_team_seasons"),
        "n_faculty_year_rows": stats.get("n_player_seasons"),
        "outputs": {"png": out_png.name, "dept_year_csv": out_csv.name},
    }
    _write_meta(out_meta, meta)
    return out_png


def run_pool_size_decision_pd29(panel_path: Path, *, tag: str = TAG_PD29) -> Path:
    """Whole-dept roster size at decision year (|T_j| analog)."""
    df, prep_stats = _hero_persons_df(panel_path)
    vals = pd.to_numeric(df["pool_size_dept"], errors="coerce").dropna().to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vals, bins=30, color="steelblue", edgecolor="white", alpha=0.85)
    _stamp_grain_badge(ax, DECISION, corner="upper_left", y=0.98)
    ax.set_xlabel("Dept roster size at decision year (all faculty observed)", fontsize=10)
    ax.set_ylabel("Persons", fontsize=10)
    ax.set_title(
        f"Decision cohort — dept pool size |T_j| (N={len(vals):,})",
        fontsize=11,
        fontweight="bold",
    )
    stats = _summary("pool_size_dept", vals)
    ax.text(
        0.98,
        0.98,
        f"median={stats['median']:.0f} · mean={stats['mean']:.1f}",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.85),
    )
    stem = f"{PREFIX}_pool_size_decision_{tag}"
    out_png = OUT_DIR / f"{stem}.png"
    out_meta = OUT_DIR / f"{stem}_meta.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_png.relative_to(REPO)}")
    _write_meta(
        out_meta,
        {
            "diagnostic": "tenure_pool_size_decision_pd29",
            "date": date.today().isoformat(),
            "grain": GRAIN_PD29_DEPT_LOO,
            "pool_size_dept": stats,
            "n_cohort": prep_stats.get("n_cohort"),
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


PD29_PLOT_RUNNERS = {
    "decision_asst_time": lambda panel, cohort: run_decision_asst_time_histogram(panel),
    "career_rate": lambda panel, cohort: run_career_rate_distribution(cohort),
    "career_rate_by_outcome": lambda panel, cohort: run_career_rate_by_outcome(cohort),
    "annual_zero_tenured": lambda panel, cohort: run_annual_zero_tenured(cohort),
    "ai_tj": lambda panel, cohort: run_ai_tj_pd29(panel),
    "dept_loo": lambda panel, cohort: run_dept_loo_distribution(panel),
    "dept_loo_by_outcome": lambda panel, cohort: run_dept_loo_by_outcome(panel),
    "tenure_mass_ecdf": lambda panel, cohort: run_tenure_mass_ecdf_pd29(cohort),
    "overlap_pd29": lambda panel, cohort: run_overlap_pd29(panel),
    "pool_size_pd29": lambda panel, cohort: run_pool_size_decision_pd29(panel),
}


PLOT_RUNNERS = {
    "overlap": lambda panel, persons: run_interval_overlap(panel),
    "overlap_gt0": lambda panel, persons: run_interval_overlap(panel, pubs_gt0=True),
    "poolq_loo": lambda panel, persons: run_poolq_loo_distribution(persons),
    "pubs_year": lambda panel, persons: run_pubs_year_distribution(panel),
    "pool_size": lambda panel, persons: run_pool_size_distribution(panel),
    "pubs_by_outcome": lambda panel, persons: run_pubs_by_outcome(persons),
    "pubs_tenured": lambda panel, persons: run_pubs_tenured(persons),
    "loo_by_outcome": lambda panel, persons: run_loo_by_outcome(persons),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Tenure porch basic data plots (inference panel)")
    parser.add_argument("--input", type=Path, default=DEFAULT_IN)
    parser.add_argument(
        "--mode",
        choices=("v0", "pd29", "all"),
        default="v0",
        help="v0 = infHM porch (default); pd29 = decision cohort BDPs; all = both",
    )
    parser.add_argument(
        "--asst-time-min",
        type=int,
        default=None,
        help="Optional diagnostic filter on decision cohort (default: all resolved)",
    )
    parser.add_argument(
        "--asst-time-max",
        type=int,
        default=None,
        help="Optional diagnostic filter on decision cohort (default: all resolved)",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        default=None,
        help="Subset of plots (keys depend on --mode)",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")

    manifest: list[dict] = []

    if args.mode in ("v0", "all"):
        only_v0 = args.only if args.only and args.mode == "v0" else sorted(PLOT_RUNNERS)
        if args.mode == "all" and args.only:
            only_v0 = [k for k in args.only if k in PLOT_RUNNERS]
        panel = load_inference_assistant_panel(args.input)
        persons = person_level_loo(panel)
        print(f"[v0] assistant-years: {len(panel):,} · persons: {len(persons):,}")
        for key in only_v0:
            if key not in PLOT_RUNNERS:
                continue
            png = PLOT_RUNNERS[key](panel, persons)
            manifest.append({"mode": "v0", "key": key, "png": png.name})

    if args.mode in ("pd29", "all"):
        only_pd29 = args.only if args.only and args.mode == "pd29" else sorted(PD29_PLOT_RUNNERS)
        if args.mode == "all" and args.only:
            only_pd29 = [k for k in args.only if k in PD29_PLOT_RUNNERS]
        cohort, pd29_stats = _load_pd29_cohort(
            args.input,
            asst_time_min=args.asst_time_min,
            asst_time_max=args.asst_time_max,
        )
        filt = (
            f"asst_time {args.asst_time_min}–{args.asst_time_max}"
            if args.asst_time_min is not None or args.asst_time_max is not None
            else "all resolved"
        )
        print(
            f"[pd29] cohort ({filt}): {len(cohort):,} rows · "
            f"career rate: {pd29_stats.get('n_with_career_rate')} · "
            f"tenure/attrition: {pd29_stats.get('n_tenure')}/{pd29_stats.get('n_attrition')} · "
            f"OTT: {pd29_stats.get('n_off_tenure_track')}"
        )
        panel_stub = pd.DataFrame()
        needs_panel = frozenset(
            {
                "decision_asst_time",
                "ai_tj",
                "dept_loo",
                "dept_loo_by_outcome",
                "overlap_pd29",
                "pool_size_pd29",
            },
        )
        for key in only_pd29:
            if key not in PD29_PLOT_RUNNERS:
                continue
            png = PD29_PLOT_RUNNERS[key](
                args.input if key in needs_panel else panel_stub,
                cohort,
            )
            manifest.append({"mode": "pd29", "key": key, "png": png.name})

    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "date": date.today().isoformat(),
                "mode": args.mode,
                "filter_v0": "infHM",
                "filter_pd29": (
                    f"asst_time_{args.asst_time_min}_{args.asst_time_max}"
                    if args.asst_time_min is not None or args.asst_time_max is not None
                    else "all_resolved"
                ),
                "plots": manifest,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {manifest_path.relative_to(REPO)}")
    print("Done.")


if __name__ == "__main__":
    main()
