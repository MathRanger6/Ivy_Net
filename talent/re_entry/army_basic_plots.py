#!/usr/bin/env python3
"""Army porch basic data plots — uniform 3×3 deck (panels 2–4, 6).

Mirrors tenure/scripts/tenure_basic_plots.py panel semantics for cross-domain comparison.

Run (repo root or AWS with cwd = talent/talent_pipeline):
  python talent/re_entry/army_basic_plots.py
  python talent/re_entry/army_basic_plots.py --input ./running_vars/df_pipeline_11_cox_analysis.feather
  python talent/re_entry/army_basic_plots.py --only ai_tj pool_loo promotion_mass pool_size

Prerequisite: 520 through Cell 11 → df_pipeline_11_cox_analysis.feather
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

_RE_ENTRY = Path(__file__).resolve().parent
REPO = _RE_ENTRY.parents[2]
sys.path.insert(0, str(_RE_ENTRY))
sys.path.insert(0, str(REPO / "sports" / "scripts"))

from army_gallery_paths import (  # noqa: E402
    BASIC_DATA_PLOTS,
    PREFIX,
    TAG_RUN1,
    ensure_army_output_dirs,
    resolve_feather,
)
from hero_plot_style import PLOT_DPI  # noqa: E402

# Run 1 · forward senior-rater columns (match pipeline_config_17_1)
COL_PID = "pid_pde"
COL_STOP = "stop_time"
COL_EVENT = "event"
COL_AI = "tb_ratio_fwd_snr"
COL_TJ = "pool_tb_ratio_mean_snr_fwd"
COL_LOO = "pool_minus_mean_snr_fwd"
COL_POOL_SIZE = "pool_size_snr_fwd"

ECDF_PROMOTED = "#2166AC"
ECDF_ATTRITION = "#B2182B"
ECDF_CENSORED = "#757575"
ECDF_LOO_HIST = "#4daf4a"

GRAIN_LABEL = "Last snapshot per officer (Cell 11 grain)"


def _summary(name: str, values: np.ndarray) -> dict[str, float | int]:
    v = values[np.isfinite(values)]
    if v.size == 0:
        return {"name": name, "n": 0}
    return {
        "name": name,
        "n": int(v.size),
        "mean": float(np.mean(v)),
        "median": float(np.median(v)),
        "std": float(np.std(v)),
        "p05": float(np.percentile(v, 5)),
        "p95": float(np.percentile(v, 95)),
    }


def _write_meta(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _plot_ecdf(
    ax,
    values: np.ndarray,
    *,
    color: str,
    label: str,
    lw: float = 2.0,
    ls: str = "-",
    alpha: float = 1.0,
) -> None:
    v = np.sort(values[np.isfinite(values)])
    if v.size == 0:
        return
    ys = np.arange(1, v.size + 1) / v.size
    ax.step(v, ys, where="post", color=color, lw=lw, label=label, ls=ls, alpha=alpha)


def load_officer_last_snapshot(feather_path: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    """One row per officer — last interval by stop_time (Cell 11 collapse rule)."""
    raw = pd.read_feather(feather_path)
    need = [COL_PID, COL_STOP, COL_EVENT, COL_AI, COL_LOO, COL_TJ]
    missing = [c for c in need if c not in raw.columns]
    if missing:
        raise SystemExit(f"Missing columns in feather: {missing}")

    work = raw.copy()
    work[COL_STOP] = pd.to_numeric(work[COL_STOP], errors="coerce")
    work = work.sort_values([COL_PID, COL_STOP])
    last = work.groupby(COL_PID, as_index=False).tail(1).copy()

    # Ever-promoted / ever-attrited flags from full panel
    ever = work.groupby(COL_PID)[COL_EVENT].agg(
        ever_promoted=lambda s: bool((s == 1).any()),
        ever_attrition=lambda s: bool((s == 2).any()),
    )
    last = last.merge(ever, on=COL_PID, how="left")
    last["outcome"] = np.where(
        last["ever_promoted"],
        "promoted",
        np.where(last["ever_attrition"], "attrition", "censored"),
    )

    stats = {
        "n_officers": int(last[COL_PID].nunique()),
        "n_rows_raw": int(len(raw)),
        "n_promoted": int((last["outcome"] == "promoted").sum()),
        "n_attrition": int((last["outcome"] == "attrition").sum()),
        "n_censored": int((last["outcome"] == "censored").sum()),
        "feather": str(feather_path),
        "grain": GRAIN_LABEL,
    }
    if COL_POOL_SIZE in last.columns:
        ps = pd.to_numeric(last[COL_POOL_SIZE], errors="coerce")
        stats["median_pool_size"] = float(np.nanmedian(ps))
    return last, stats


def run_ai_tj(officers: pd.DataFrame, *, tag: str = TAG_RUN1) -> Path:
    """Panel 2 — own TB ratio vs pool mean (T̂_j includes self)."""
    ai = pd.to_numeric(officers[COL_AI], errors="coerce").to_numpy(dtype=float)
    tj = pd.to_numeric(officers[COL_TJ], errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(ai) & np.isfinite(tj)
    ai, tj = ai[mask], tj[mask]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    fig.subplots_adjust(wspace=0.28, top=0.84)

    ax = axes[0]
    ax.hist(ai, bins=48, color="steelblue", alpha=0.85, edgecolor="white", linewidth=0.35)
    s_ai = _summary(COL_AI, ai)
    ax.set_title(r"Own performance ($\hat{A}_i$ · TB ratio SNR fwd)", fontsize=10)
    ax.set_xlabel("tb_ratio_fwd_snr")
    ax.set_ylabel("Officers")
    ax.text(
        0.98, 0.98,
        f"n={s_ai['n']:,}\nmed={s_ai['median']:.3f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )

    ax = axes[1]
    ax.hist(tj, bins=48, color="#E8B923", alpha=0.85, edgecolor="white", linewidth=0.35)
    s_tj = _summary(COL_TJ, tj)
    ax.set_title(r"Pool mean talent ($\hat{T}_j$ · incl. self)", fontsize=10)
    ax.set_xlabel("pool_tb_ratio_mean_snr_fwd")
    ax.set_ylabel("Officers")
    ax.text(
        0.98, 0.98,
        f"n={s_tj['n']:,}\nmed={s_tj['median']:.3f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=8,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )

    fig.suptitle(f"{PREFIX} BDP · Â_i and T̂_j · {GRAIN_LABEL}", fontsize=11, fontweight="bold", y=0.98)
    stem = f"{PREFIX}_BDP_Ai_Tj_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(out_meta, {"date": date.today().isoformat(), "panel": 2, "stats_ai": s_ai, "stats_tj": s_tj})
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


def run_pool_loo_distribution(officers: pd.DataFrame, *, tag: str = TAG_RUN1) -> Path:
    """Panel 3 — LOO pool minus mean (peer context support)."""
    loo = pd.to_numeric(officers[COL_LOO], errors="coerce").to_numpy(dtype=float)
    stats = _summary(COL_LOO, loo)
    lo, hi = float(np.min(loo)), float(np.max(loo))
    bins = np.linspace(lo, hi, 36)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    fig.subplots_adjust(wspace=0.28, top=0.84)

    ax = axes[0]
    ax.hist(loo, bins=bins, color=ECDF_LOO_HIST, alpha=0.85, edgecolor="white", linewidth=0.35)
    ax.axvline(stats["median"], color="0.35", linestyle=":", linewidth=1.4)
    ax.set_xlabel("pool_minus_mean_snr_fwd (LOO peer context)")
    ax.set_ylabel("Officers")
    ax.set_title("Peer pool quality (LOO minus mean)", fontsize=10)

    ax = axes[1]
    _plot_ecdf(ax, loo, color=ECDF_LOO_HIST, label=f"All ($n={stats['n']:,}$)", lw=1.8, ls="-")
    for key, color, ls in (
        ("promoted", ECDF_PROMOTED, "-"),
        ("attrition", ECDF_ATTRITION, "--"),
    ):
        sub = officers.loc[officers["outcome"] == key, COL_LOO].to_numpy(dtype=float)
        if sub.size:
            _plot_ecdf(ax, sub, color=color, label=f"{key} ($n={sub.size:,}$)", lw=2.2, ls=ls)
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("pool_minus_mean_snr_fwd")
    ax.set_ylabel(r"ECDF  $F(x)$")
    ax.set_title("ECDF by eventual outcome", fontsize=10)
    ax.legend(fontsize=7, loc="lower right", framealpha=0.95)
    ax.grid(alpha=0.2)

    fig.suptitle(f"{PREFIX} BDP · pool LOO distribution · {GRAIN_LABEL}", fontsize=11, fontweight="bold", y=0.98)
    stem = f"{PREFIX}_BDP_pool_minus_mean_loo_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(out_meta, {"date": date.today().isoformat(), "panel": 3, "stats": stats})
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


def run_promotion_mass_ecdf(officers: pd.DataFrame, *, tag: str = TAG_RUN1) -> Path:
    """Panel 4 — cumulative share of promotions by own-TB (Â) tiers."""
    ai = pd.to_numeric(officers[COL_AI], errors="coerce")
    promoted = officers["outcome"] == "promoted"
    work = pd.DataFrame({"ai": ai, "promoted": promoted}).dropna()
    work = work.sort_values("ai")
    n_prom = int(work["promoted"].sum())
    if n_prom == 0:
        raise SystemExit("No promoted officers in panel — check event coding.")

    work["cum_prom_share"] = work["promoted"].cumsum() / n_prom

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.step(work["ai"], work["cum_prom_share"], where="post", color=ECDF_PROMOTED, lw=2.2)
    ax.set_xlabel(r"Own TB ratio SNR fwd ($\hat{A}_i$)")
    ax.set_ylabel("Cumulative share of promotions")
    ax.set_title(
        f"{PREFIX} — promotion mass vs own performance\n{GRAIN_LABEL} · n_prom={n_prom:,}",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.25)

    stem = f"{PREFIX}_BDP_promotion_mass_ecdf_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(
        out_meta,
        {
            "date": date.today().isoformat(),
            "panel": 4,
            "n_promoted": n_prom,
            "n_officers": len(work),
        },
    )
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


def run_pool_size_distribution(officers: pd.DataFrame, *, tag: str = TAG_RUN1) -> Path:
    """Panel 6 — senior-rater pool size at last snapshot."""
    if COL_POOL_SIZE not in officers.columns:
        raise SystemExit(f"Column {COL_POOL_SIZE} not in feather — re-run 520 pool cells.")
    ps = pd.to_numeric(officers[COL_POOL_SIZE], errors="coerce").to_numpy(dtype=float)
    stats = _summary(COL_POOL_SIZE, ps)

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.hist(ps, bins=40, color="steelblue", alpha=0.85, edgecolor="white")
    ax.set_xlabel("pool_size_snr_fwd (senior-rater pool count)")
    ax.set_ylabel("Officers")
    ax.set_title(f"{PREFIX} — pool size |T_j| · {GRAIN_LABEL}", fontsize=11, fontweight="bold")
    ax.text(
        0.98, 0.98,
        f"n={stats['n']:,}\nmed={stats['median']:.0f}",
        transform=ax.transAxes, ha="right", va="top", fontsize=9,
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.9),
    )
    stem = f"{PREFIX}_BDP_pool_size_{tag}"
    out_png = BASIC_DATA_PLOTS / f"{stem}.png"
    out_meta = BASIC_DATA_PLOTS / f"{stem}.json"
    fig.tight_layout()
    fig.savefig(out_png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(out_meta, {"date": date.today().isoformat(), "panel": 6, "stats": stats})
    print(f"Wrote {out_png.relative_to(REPO)}")
    return out_png


PLOT_RUNNERS = {
    "ai_tj": lambda df, _s: run_ai_tj(df),
    "pool_loo": lambda df, _s: run_pool_loo_distribution(df),
    "promotion_mass": lambda df, _s: run_promotion_mass_ecdf(df),
    "pool_size": lambda df, _s: run_pool_size_distribution(df),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Army porch basic data plots (BDP)")
    parser.add_argument("--input", type=Path, default=None, help="df_pipeline_11 feather path")
    parser.add_argument(
        "--only",
        nargs="+",
        default=None,
        choices=sorted(PLOT_RUNNERS),
        help="Subset of panels to build",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Build all implemented BDP panels (default if --only omitted)",
    )
    args = parser.parse_args()

    ensure_army_output_dirs()
    feather = resolve_feather(args.input)
    officers, cohort_stats = load_officer_last_snapshot(feather)
    print(
        f"Loaded {cohort_stats['n_officers']:,} officers from {feather.name} "
        f"(promoted={cohort_stats['n_promoted']:,}, "
        f"attrition={cohort_stats['n_attrition']:,}, "
        f"censored={cohort_stats['n_censored']:,})"
    )

    keys = args.only if args.only else sorted(PLOT_RUNNERS)
    manifest: list[dict[str, str]] = []
    for key in keys:
        png = PLOT_RUNNERS[key](officers, cohort_stats)
        manifest.append({"key": key, "png": png.name})

    manifest_path = BASIC_DATA_PLOTS / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "date": date.today().isoformat(),
                "cohort": cohort_stats,
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
