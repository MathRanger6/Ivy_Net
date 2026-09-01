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
SPORTS_SCRIPTS = REPO / "sports" / "scripts"
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
PREFIX = "TENURE"
PRIMARY_TIERS = frozenset({"HIGH", "MEDIUM"})
POOL_MIN = 2

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
    "tenured": "#2166AC",
    "attrition": "#D6604D",
    "censored": "#888888",
}
OUTCOME_LABELS = {
    "tenured": "Tenured (promoted)",
    "attrition": "Attrition (left as asst)",
    "censored": "Censored (still asst ≈ 2024)",
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
            "grain": "person-level mean poolq_loo_mean (matches Q16 HERO)",
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
            "grain": "assistant person-year",
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
    )

    base_filter = "HIGH/MEDIUM inference · OA-matched assistant-years · LOO computable"
    meta = {
        "diagnostic": "tenure_pool_interval_overlap_pubs_gt0"
        if pubs_gt0
        else "tenure_pool_interval_overlap",
        "date": date.today().isoformat(),
        "filter": base_filter + (" · pubs_year > 0" if pubs_gt0 else ""),
        "pool_unit": "uni_slug × year (OpenAlex assistant peer pool)",
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
    ax.legend(fontsize=8.5, loc="upper right")
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
            "grain": "person-level mean pubs_year over assistant years",
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
            "grain": "person-level mean pubs_year · tenure_event only",
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
    ax.legend(fontsize=8.5, loc="upper right")

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
            "grain": "person-level mean poolq_loo_mean",
            **{k: meta_groups[k] for k in meta_groups},
            "display_x_cap": x_cap,
            "outputs": {"png": out_png.name},
        },
    )
    return out_png


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
        "--only",
        nargs="+",
        choices=sorted(PLOT_RUNNERS),
        default=sorted(PLOT_RUNNERS),
        help="Subset of plots to run",
    )
    args = parser.parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")

    panel = load_inference_assistant_panel(args.input)
    persons = person_level_loo(panel)
    print(f"Inference assistant-years: {len(panel):,} · persons (HERO N): {len(persons):,}")

    manifest: list[dict] = []
    for key in args.only:
        png = PLOT_RUNNERS[key](panel, persons)
        manifest.append({"key": key, "png": png.name})

    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "date": date.today().isoformat(),
                "filter": "infHM",
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
