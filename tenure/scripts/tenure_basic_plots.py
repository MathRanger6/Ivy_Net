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
    """One row per faculty_id — mean poolq_loo_mean (HERO grain)."""
    work = panel.copy()
    work["poolq_loo_mean"] = pd.to_numeric(work["poolq_loo_mean"], errors="coerce")
    agg = (
        work.groupby("faculty_id", observed=True)
        .agg(
            loo_mean=("poolq_loo_mean", "mean"),
            n_asst_years=("poolq_loo_mean", "count"),
            tenure=("tenure_event", "max"),
            attrition=("attrition", "max"),
            censored=("censored", "max"),
        )
        .reset_index()
    )
    return agg


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
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vals, bins=40, color="steelblue", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Own pubs_year (assistant person-years)", fontsize=10)
    ax.set_ylabel("Assistant-years", fontsize=10)
    ax.set_title(
        f"Tenure inference panel — own publication rate (N={len(vals):,} asst-years)",
        fontsize=11,
        fontweight="bold",
    )
    stats = _summary("pubs_year", vals)
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
            "pubs_year": stats,
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


def _prepare_overlap_panel(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    work = panel.copy()
    work["pubs_year"] = pd.to_numeric(work["pubs_year"], errors="coerce")
    work = work.dropna(subset=["pubs_year", "uni_slug", "year"])
    work = work.loc[work["openalex_id"].astype(str).str.len() > 0].copy()

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


def run_interval_overlap(panel: pd.DataFrame) -> Path:
    sys.path.insert(0, str(SPORTS_SCRIPTS))
    from empirical_team_interval_overlap import build_figure

    iv, work = _prepare_overlap_panel(panel)
    y0, y1 = int(work["year"].min()), int(work["year"].max())
    seasons = f"{y0}-{y1}"

    stem = f"{PREFIX}_pool_interval_overlap_{TAG}"
    out_png = OUT_DIR / f"{stem}.png"
    out_csv = OUT_DIR / f"{stem}_uni_year.csv"
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
            f"Tenure inference — uni-year peer pool interval overlap ({seasons})"
            + h_line
        ),
        xlab=r"Assistant own pubs/year ($z$ within calendar year)",
    )

    meta = {
        "diagnostic": "tenure_pool_interval_overlap",
        "date": date.today().isoformat(),
        "filter": "HIGH/MEDIUM inference · OA-matched assistant-years · LOO computable",
        "pool_unit": "uni_slug × year (OpenAlex assistant peer pool)",
        "perf": "pubs_year z-scored within calendar year",
        "pool_min_assistants": POOL_MIN,
        "seasons": seasons,
        **stats,
        "outputs": {"png": out_png.name, "uni_year_csv": out_csv.name},
    }
    _write_meta(out_meta, meta)
    return out_png


PLOT_RUNNERS = {
    "overlap": lambda panel, persons: run_interval_overlap(panel),
    "poolq_loo": lambda panel, persons: run_poolq_loo_distribution(persons),
    "pubs_year": lambda panel, persons: run_pubs_year_distribution(panel),
    "pool_size": lambda panel, persons: run_pool_size_distribution(panel),
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
