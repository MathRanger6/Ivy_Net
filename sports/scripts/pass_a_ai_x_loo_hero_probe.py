#!/usr/bin/env python3
"""Disposable probe — HERO bins on Â × poolq_loo (product of z-scores).

Does not touch canonical pass_a/ or sports_sandbox/hero/ outputs.

Spec (reigning lock):
  2009–2021 · last-ps · ever-Y · mg10 · min20 · ppm z within season · LOO winsor

X-axis: ai_x_loo = perf_z * poolq_loo_z  (both from locked panel; quantile bins)

Run (repo root):
  export PYTHONPATH="sports"
  python3 sports/scripts/pass_a_ai_x_loo_hero_probe.py --n-bins 8 10 16
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
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SPORTS))

OUT_DIR = (
    REPO
    / "3-Master_Plan"
    / "re_entry"
    / "HEROs_and_PASSes"
    / "sports_sandbox"
    / "_DISPOSABLE_ai_x_loo_last_ps"
)

SEASON_MIN = 2009
SEASON_MAX = 2021
MIN_MINUTES = 20.0
MIN_TEAM_SEASON_GAMES = 10
WINSOR = (0.01, 0.99)
DEFAULT_BINS = (8, 10, 16)


def _prepare_panel() -> pd.DataFrame:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.config import PipelineConfig
    from sports_pipeline.y_draft_mode import restrict_to_last_season_rows

    cfg = PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=16,
        poolq_binning="quantile",
        poolq_winsor_quantiles=WINSOR,
        min_minutes=float(MIN_MINUTES),
        min_team_season_games=int(MIN_TEAM_SEASON_GAMES),
        drop_dash_placeholder_names=True,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=int(SEASON_MIN),
        panel_season_max=int(SEASON_MAX),
        analysis_season_min=int(SEASON_MIN),
        analysis_season_max=int(SEASON_MAX),
    )
    panel = conductor.prepare_panel(cfg)
    from sports_pipeline.perf_metric import perf_metric_active

    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    use = panel_build.filter_panel(panel, cfg)
    use, audit = restrict_to_last_season_rows(use)
    work = use.dropna(subset=["perf", "poolq_loo"]).copy()
    work["ai_x_loo"] = (
        pd.to_numeric(work["perf"], errors="coerce")
        * pd.to_numeric(work["poolq_loo"], errors="coerce")
    )
    print(
        f"PPM z × LOO · last-ps: {audit['n_rows_before']:,} → "
        f"{audit['n_rows_after']:,} rows · plot n={len(work):,}",
        flush=True,
    )
    return work


def _roster_table(df: pd.DataFrame, n_bins: int) -> pd.DataFrame:
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    work = df.dropna(subset=["ai_x_loo", "Y_draft"]).copy()
    work["vent"] = assign_poolq_bin_labels(work["ai_x_loo"], n_bins, "quantile")
    return (
        work.dropna(subset=["vent"])
        .groupby("vent", observed=True)
        .agg(
            n=("Y_draft", "size"),
            draft_rate=("Y_draft", "mean"),
            ai_x_loo_mean=("ai_x_loo", "mean"),
            ai_x_loo_median=("ai_x_loo", "median"),
            perf_mean=("perf", "mean"),
            poolq_loo_mean=("poolq_loo", "mean"),
        )
        .reset_index()
        .sort_values("vent")
    )


def _quadratic_beta2(df: pd.DataFrame, x_col: str) -> float:
    work = df.dropna(subset=[x_col, "Y_draft"]).copy()
    x = pd.to_numeric(work[x_col], errors="coerce").to_numpy(dtype=float)
    y = pd.to_numeric(work["Y_draft"], errors="coerce").to_numpy(dtype=float)
    mask = np.isfinite(x) & np.isfinite(y)
    if mask.sum() < 10:
        return float("nan")
    x = x[mask]
    y = y[mask]
    x_mat = np.column_stack([np.ones(len(x)), x, x**2])
    beta, *_ = np.linalg.lstsq(x_mat, y, rcond=None)
    return float(beta[2])


def _plot_hero(roster: pd.DataFrame, *, n_bins: int, n_rows: int, beta2: float) -> Path:
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="#2E7D32", edgecolor="white", alpha=0.9)
    ax.set_xlabel(r"Quantile bin ($1$ = lowest $\hat{A}_i \times \mathrm{poolq}_{\mathrm{LOO}}$)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(
        rf"HERO probe — $\hat{{A}}_i \times \mathrm{{poolq}}_{{\mathrm{{LOO}}}}$ · last-PS · "
        rf"MBB {SEASON_MIN}–{SEASON_MAX}\n"
        rf"Q{n_bins} quantile · mg{MIN_TEAM_SEASON_GAMES} · min {MIN_MINUTES:g} min · N={n_rows:,}",
        fontsize=10,
    )
    ax.set_xticks(x)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    if np.isfinite(beta2):
        sign = "<0, concave" if beta2 < 0 else "not concave"
        ax.text(
            0.02,
            0.96,
            rf"LPM $\beta_2={beta2:+.4g}$ on product axis ({sign})",
            transform=ax.transAxes,
            fontsize=8,
            va="top",
        )
    footer = (
        f"DISPOSABLE Â×LOO probe · {date.today().isoformat()} · "
        f"ppm z within season × winsorized poolq_loo"
    )
    fig.text(0.01, 0.01, footer, fontsize=7, color="0.45")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    png = OUT_DIR / f"HERO_q{n_bins}_ai_x_loo_lastps_{SEASON_MIN}_{SEASON_MAX}.png"
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return png


def main() -> None:
    parser = argparse.ArgumentParser(description="Â × LOO product HERO probe (disposable)")
    parser.add_argument(
        "--n-bins",
        type=int,
        nargs="+",
        default=list(DEFAULT_BINS),
        help="Quantile bin counts (default: 8 10 16)",
    )
    args = parser.parse_args()

    panel = _prepare_panel()
    plot_panel = panel.dropna(subset=["ai_x_loo", "Y_draft"]).copy()
    n_rows = len(plot_panel)
    n_drafts = int(pd.to_numeric(plot_panel["Y_draft"], errors="coerce").fillna(0).sum())
    neg_product = int((plot_panel["ai_x_loo"] < 0).sum())
    print(
        f"HERO panel: N={n_rows:,} · drafts={n_drafts:,} · "
        f"negative product rows={neg_product:,} ({100 * neg_product / max(n_rows, 1):.1f}%)",
        flush=True,
    )

    # Reference: LOO-only β₂ on same rows
    beta2_loo = _quadratic_beta2(plot_panel, "poolq_loo")
    beta2_ai = _quadratic_beta2(plot_panel, "perf")
    print(f"Same-panel LPM β₂ (poolq_loo only): {beta2_loo:+.5f}", flush=True)
    print(f"Same-panel LPM β₂ (perf only):     {beta2_ai:+.5f}", flush=True)

    meta = {
        "diagnostic": "ai_x_loo_hero_probe",
        "date": date.today().isoformat(),
        "seasons": f"{SEASON_MIN}-{SEASON_MAX}",
        "panel_rows": "last-ps",
        "min_minutes": MIN_MINUTES,
        "mg": MIN_TEAM_SEASON_GAMES,
        "n_rows": n_rows,
        "n_drafts": n_drafts,
        "negative_product_rows": neg_product,
        "beta2_poolq_loo_only": beta2_loo,
        "beta2_perf_only": beta2_ai,
        "runs": [],
    }

    for n_bins in args.n_bins:
        roster = _roster_table(plot_panel, int(n_bins))
        beta2 = _quadratic_beta2(plot_panel, "ai_x_loo")
        png = _plot_hero(roster, n_bins=int(n_bins), n_rows=n_rows, beta2=beta2)
        csv = OUT_DIR / f"HERO_q{n_bins}_ai_x_loo_lastps_{SEASON_MIN}_{SEASON_MAX}.csv"
        roster.to_csv(csv, index=False)
        meta["runs"].append(
            {
                "n_bins": int(n_bins),
                "beta2_product": beta2,
                "png": png.name,
                "csv": csv.name,
            }
        )
        print(f"Wrote {png.relative_to(REPO)} · bins={len(roster)} · β₂={beta2:+.5f}")

    meta_path = OUT_DIR / f"HERO_ai_x_loo_meta_{SEASON_MIN}_{SEASON_MAX}.json"
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {meta_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
