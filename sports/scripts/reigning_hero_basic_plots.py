#!/usr/bin/env python3
"""Reigning hero (slide 12) — porch basic data plots.

Lock: mg10 · min20 · 09_21 · ALLT · winsor 0.01–0.99 on poolq_loo where relevant.

Run (repo root):
  python sports/scripts/reigning_hero_basic_plots.py
  python sports/scripts/reigning_hero_basic_plots.py --only overlap ai_tj

Outputs:
  ``3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/basic_data_plots/``
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from bdp_ai_tj_distributions import BdpSpec, parse_bdp_spec, run_spec
from bdp_draft_rate_apgms_argms import run_metric as run_draft_rate_metric
from bdp_team_size_distributions import run_spec as run_team_size
from bdp_reigning_exposure_plots import run_minutes_dual, run_team_games
from bdp_reigning_loo_plots import (
    run_draft_rate_loo_vs_tj,
    run_draft_rate_vs_loo,
    run_poolq_loo_distribution,
)
from bdp_reigning_hsort_distribution import (
    run_ability_loo_residual_distribution,
    run_ability_residual_distributions,
    run_ability_team_vs_loo_residual_compare,
    run_hsort_distribution,
    run_tj_minus_loo_distribution,
)
from hero_gallery_paths import REIGNING_HERO_BASIC_PLOTS, ensure_hero_dirs

REIGNING_SPEC = "mg10 min20 09_21"
WINSOR = (0.01, 0.99)
PREFIX = "REIGNING"


def _out(name: str) -> Path:
    return REIGNING_HERO_BASIC_PLOTS / name


def run_interval_overlap(spec: BdpSpec) -> Path:
    import numpy as np
    import pandas as pd

    from bdp_ai_tj_distributions import _pipeline_config
    from empirical_team_interval_overlap import (
        _compute_H_sort,
        _team_intervals,
        build_figure,
    )

    sys.path.insert(0, str(REPO / "sports"))
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _pipeline_config(spec, "ppm")
    panel = conductor.prepare_panel(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=None,
        zscore_perf_within_season=True,
    )
    use = panel.dropna(subset=["perf", "team_id", "season"]).copy()
    mm = float(spec.min_minutes)
    if mm > 0 and "minutes" in use.columns:
        use = use.loc[pd.to_numeric(use["minutes"], errors="coerce") >= mm]

    iv, work = _team_intervals(use)
    seasons = f"{spec.season_min}-{spec.season_max}"
    stem = f"{PREFIX}_team_interval_overlap_{spec.slug}"
    out_png = _out(f"{stem}.png")
    out_csv = _out(f"{stem}_team_season.csv")
    out_meta = _out(f"{stem}_meta.json")

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    iv.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv.relative_to(REPO)}")

    h_sort = _compute_H_sort(work)
    stats = build_figure(
        iv,
        work,
        png_path=out_png,
        seasons=seasons,
        h_sort=h_sort,
    )
    meta = {
        "diagnostic": "reigning_hero_team_interval_overlap",
        "date": date.today().isoformat(),
        "reigning_spec": spec.label,
        "panel_rows": "all-ps",
        "seasons": seasons,
        "perf": "PPM z within season",
        **stats,
        "outputs": {"png": out_png.name, "team_csv": out_csv.name},
    }
    out_meta.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out_meta.relative_to(REPO)}")
    return out_png


def run_ai_tj(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_Ai_Tj_{spec.slug}_ppm_lastps"
    return run_spec(
        spec,
        "ppm",
        overlay_dft=True,
        panel_rows="last-ps",
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        figsize=(10.5, 7.0),
    )


def run_ai_loo(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_Ai_poolq_loo_{spec.slug}_ppm_lastps"
    return run_spec(
        spec,
        "ppm",
        overlay_dft=True,
        panel_rows="last-ps",
        right_is_loo=True,
        poolq_winsor_quantiles=WINSOR,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        figsize=(10.5, 7.0),
    )


def run_tj_loo_compare_plot(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_Tj_vs_poolq_loo_{spec.slug}_ppm_lastps"
    return run_tj_loo_compare(
        spec,
        "ppm",
        panel_rows="last-ps",
        poolq_winsor_quantiles=WINSOR,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        figsize=(8.5, 4.8),
    )


def run_tj_loo_compare_nowinsor_plot(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_Tj_vs_poolq_loo_{spec.slug}_ppm_lastps_NOWINSOR"
    return run_tj_loo_compare(
        spec,
        "ppm",
        panel_rows="last-ps",
        poolq_winsor_quantiles=None,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        figsize=(8.5, 4.8),
    )


def run_draft_rates(spec: BdpSpec) -> list[Path]:
    out: list[Path] = []
    for metric in ("apgms", "argms"):
        stem = f"{PREFIX}_BDP_draft_rate_{metric.upper()}_{spec.slug}"
        out.append(
            run_draft_rate_metric(
                spec.label,
                metric,
                dft_only=False,
                overlay_dft=True,
                out_dir=REIGNING_HERO_BASIC_PLOTS,
                out_stem=stem,
            )
        )
    return out


def run_roster_size(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_team_size_{spec.slug}"
    return run_team_size(
        spec,
        overlay_dft=True,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
    )


def run_team_games_plot(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_team_games_{spec.slug}"
    return run_team_games(
        spec,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        prefix=PREFIX,
        raw_box=False,
    )


def run_minutes_plot(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_minutes_player_team_{spec.slug}"
    return run_minutes_dual(
        spec,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        prefix=PREFIX,
    )


def run_hsort_dist_plot(spec: BdpSpec) -> Path:
    return run_hsort_distribution(spec, out_meta_dir=REIGNING_HERO_BASIC_PLOTS, prefix=PREFIX)


def run_ability_residuals_plot(spec: BdpSpec) -> Path:
    return run_ability_residual_distributions(spec, out_meta_dir=REIGNING_HERO_BASIC_PLOTS, prefix=PREFIX)


def run_ability_loo_residuals_plot(spec: BdpSpec) -> Path:
    return run_ability_loo_residual_distribution(spec, out_meta_dir=REIGNING_HERO_BASIC_PLOTS, prefix=PREFIX)


def run_ability_tj_vs_loo_residuals_plot(spec: BdpSpec) -> Path:
    return run_ability_team_vs_loo_residual_compare(
        spec, out_meta_dir=REIGNING_HERO_BASIC_PLOTS, prefix=PREFIX
    )


def run_tj_minus_loo_plot(spec: BdpSpec) -> Path:
    return run_tj_minus_loo_distribution(spec, out_meta_dir=REIGNING_HERO_BASIC_PLOTS, prefix=PREFIX)


def run_loo_dist_plot(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_poolq_loo_dist_{spec.slug}_ppm_lastps"
    return run_poolq_loo_distribution(
        spec,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        prefix=PREFIX,
    )


def run_loo_dist_nowinsor_plot(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_poolq_loo_dist_{spec.slug}_ppm_lastps_nowinsor"
    return run_poolq_loo_distribution(
        spec,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        prefix=PREFIX,
        poolq_winsor_quantiles=None,
    )


def run_draft_rate_loo_plot(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_draft_rate_poolq_loo_{spec.slug}_ew16_ppm_lastps"
    return run_draft_rate_vs_loo(
        spec,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        prefix=PREFIX,
    )


def run_draft_rate_loo_tj_plot(spec: BdpSpec) -> Path:
    stem = f"{PREFIX}_BDP_draft_rate_poolq_loo_vs_Tj_{spec.slug}_ew16_ppm_lastps"
    return run_draft_rate_loo_vs_tj(
        spec,
        out_png=_out(f"{stem}.png"),
        out_meta_dir=REIGNING_HERO_BASIC_PLOTS,
        prefix=PREFIX,
    )


PLOT_FNS = {
    "overlap": run_interval_overlap,
    "ai_tj": run_ai_tj,
    "ai_loo": run_ai_loo,
    "tj_loo": run_tj_loo_compare_plot,
    "tj_loo_nowinsor": run_tj_loo_compare_nowinsor_plot,
    "loo_dist": run_loo_dist_plot,
    "loo_dist_nowinsor": run_loo_dist_nowinsor_plot,
    "hsort_dist": run_hsort_dist_plot,
    "ability_residuals": run_ability_residuals_plot,
    "ability_loo_residuals": run_ability_loo_residuals_plot,
    "ability_tj_vs_loo_residuals": run_ability_tj_vs_loo_residuals_plot,
    "tj_minus_loo": run_tj_minus_loo_plot,
    "draft_rate_loo": run_draft_rate_loo_plot,
    "draft_rate_loo_tj": run_draft_rate_loo_tj_plot,
    "draft_rate": run_draft_rates,
    "team_games": run_team_games_plot,
    "minutes": run_minutes_plot,
    "team_size": run_roster_size,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Reigning hero basic data plots (slide 12).")
    parser.add_argument(
        "--only",
        nargs="+",
        choices=tuple(PLOT_FNS.keys()),
        help="Run subset only (default: all).",
    )
    args = parser.parse_args()

    ensure_hero_dirs()
    REIGNING_HERO_BASIC_PLOTS.mkdir(parents=True, exist_ok=True)
    spec = parse_bdp_spec(REIGNING_SPEC)
    keys = args.only or list(PLOT_FNS.keys())

    print(f"Reigning hero basic plots · {spec.label} · out={REIGNING_HERO_BASIC_PLOTS.relative_to(REPO)}")
    for key in keys:
        print(f"\n=== {key} ===")
        fn = PLOT_FNS[key]
        result = fn(spec)
        if isinstance(result, list):
            for p in result:
                print(f"  → {p.name}")
        else:
            print(f"  → {result.name}")
    print("\nDone.")


if __name__ == "__main__":
    main()
