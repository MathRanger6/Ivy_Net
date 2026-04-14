"""
Single entry point for ``530_sports_pipeline.ipynb``: panel → perf/LOO → diagnostics → EDA.

All stage toggles live on ``PipelineConfig`` (CELL 2). Call ``run_conductor(CFG)`` once, or
``prepare_panel`` + ``run_conductor_from_panel`` in a loop to sweep ``perf_metric`` without
rebuilding the panel each time.
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from sports_pipeline import bpm_merge, data_integrity, dataset_coverage, draft_match, ingest_box
from sports_pipeline import panel_build, panel_rebuild, paths, sr_bpm
from sports_pipeline.perf_metric import perf_metric_active, resolve_perf_metric


def _prepare_panel(cfg: Any) -> pd.DataFrame:
    """Load or rebuild from box; optional SR refresh; return panel before ``perf`` / LOO."""
    use_csv = bool(getattr(cfg, "use_prebuilt_panel_csv", False))
    if use_csv:
        panel = panel_build.load_panel(cfg)
    else:
        panel = panel_rebuild.build_from_box(cfg)

    if bool(getattr(cfg, "run_sr_refresh", False)):
        bpm_merge.run_sr_refresh_stage(
            cfg,
            panel,
            do_crosswalk=bool(getattr(cfg, "sr_refresh_do_crosswalk", True)),
            do_scrape_jobs=bool(getattr(cfg, "sr_refresh_do_scrape_jobs", True)),
            do_scrape=bool(getattr(cfg, "sr_refresh_do_scrape", False)),
            do_match=bool(getattr(cfg, "sr_refresh_do_match", True)),
        )
        if use_csv:
            panel = panel_rebuild.merge_sr_matched_into_panel(panel)
        else:
            panel = panel_rebuild.build_from_box(cfg)
    return panel


def prepare_panel(cfg: Any) -> pd.DataFrame:
    """
    Load or rebuild the panel (+ optional SR refresh), **before** ``perf`` / LOO.

    Use with ``run_conductor_from_panel`` when looping ``perf_metric`` so the heavy
    ingest/merge steps run only once.
    """
    panel = _prepare_panel(cfg)
    if bool(getattr(cfg, "print_unmatched_school_lists", False)):
        data_integrity.print_unmatched_school_reports(cfg)
    return panel


def run_conductor_from_panel(cfg: Any, panel: pd.DataFrame) -> dict[str, Any]:
    """
    Run perf → integrity → coverage → ventiles → export on ``panel`` without reloading it.

    ``panel`` must be the pre-perf frame (same as ``prepare_panel`` returns). Pass
    ``panel.copy(deep=True)`` per metric when looping so each run starts from a clean base.
    """
    out: dict[str, Any] = {"stage": "530_conductor"}
    out["panel_shape_before_perf"] = tuple(panel.shape)

    panel_work = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=getattr(cfg, "poolq_winsor_quantiles", None),
        zscore_perf_within_season=bool(getattr(cfg, "perf_zscore_within_season", False)),
    )
    out["PANEL"] = panel_work

    if bool(getattr(cfg, "run_data_integrity_report", True)):
        print("--- Data integrity ---")
        data_integrity.print_data_integrity(panel_work, cfg)
        print()

    if bool(getattr(cfg, "run_yearly_coverage_chart", True)):
        tab, png = dataset_coverage.export_yearly_coverage_chart(cfg, show=True)
        out["coverage_table"] = tab
        out["coverage_png"] = png

    if bool(getattr(cfg, "run_ventile_eda", True)):
        bin_tab, png = panel_build.run_ventile_eda(panel_work, cfg)
        out["ventile_table"] = bin_tab
        out["ventile_png"] = png

    if bool(getattr(cfg, "run_dirty_lpm", True)):
        lpm = panel_build.run_dirty_lpm(panel_work, cfg)
        out["lpm"] = lpm
        if hasattr(lpm, "summary"):
            print("--- LPM (statsmodels) ---")
            print(lpm.summary())
        else:
            print("--- LPM coefficients (numpy OLS) ---")
            print(lpm)

    if bool(getattr(cfg, "export_panel_after_run", False)):
        dest = getattr(cfg, "export_panel_dest", None)
        ep = panel_build.export_panel(panel_work, cfg, dest=dest)
        out["exported_panel_path"] = str(ep)
        print(f"--- Wrote panel CSV: {ep} ---")

    print(
        f"--- Conductor done — perf_metric={getattr(cfg, 'perf_metric', ['minutes'])!r} — panel "
        f"{out['panel_shape_before_perf']} → {panel_work.shape[0]:,} rows after perf/LOO; "
        f"exports_dir={getattr(cfg, 'exports_dir', paths.mbb_dir() / 'exports_inverted_u_v0')} ---"
    )
    return out


def run_conductor(cfg: Any) -> dict[str, Any]:
    """
    Run the 530 pipeline according to boolean flags on ``cfg``.

    Returns a dict including ``"PANEL"`` (post perf/LOO) and optional stage outputs.
    """
    if bool(getattr(cfg, "run_stage3_status", False)):
        print("--- Stage 3 status (stubs / optional scrape) ---")
        print(ingest_box.run(cfg))
        print(draft_match.run(cfg))
        print(sr_bpm.run(cfg))
        print()

    panel = prepare_panel(cfg)
    return run_conductor_from_panel(cfg, panel)


def panel_has_metric_column(panel: pd.DataFrame, metric: str) -> bool:
    """True if ``panel`` has the source column needed for ``metric`` (see ``perf_metric``)."""
    _label, col = resolve_perf_metric(metric)
    return col in panel.columns
