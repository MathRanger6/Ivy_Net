"""
Conductor configuration (`PipelineConfig`).

**Performance metric:** set `perf_metric` to a **list** of user keys (e.g. ``[\"minutes\"]``,
``[\"obpm\", \"ws40\"]``). A single string is normalized to a one-element list at init.
`run_conductor` uses the **first** entry per pass; sweep more keys in CELL 4 or
`RUN_ALL_PERF_METRICS`. Allowed values and plot text live in `sports_pipeline.perf_metric`.
`perf_measure_label` reflects the **active** (first) metric.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from sports_pipeline import paths
from sports_pipeline.perf_metric import (
    normalize_perf_metric_list,
    perf_metric_active,
    plot_label_for_metric,
    resolve_perf_metric,
)


@dataclass
class PipelineConfig:
    """
    Shared knobs for `530_sports_pipeline.ipynb` and `sports_pipeline.*` stages.

    Many fields are placeholders for future stage wiring (`run_spine_refresh`, etc.).
    """

    # --- Panel / EDA (ventile plot + LPM) ---------------------------------
    #: If True, read ``player_season_panel_530.csv`` instead of rebuilding from box.
    #: After SR refresh, matched stats are merged from disk onto that frame.
    use_prebuilt_panel_csv: bool = False
    #: When rebuilding from box (`panel_rebuild.build_from_box`): inclusive season bounds.
    #: ``None`` = use all seasons present in `mbb_df_player_box.csv`.
    panel_season_min: int | None = None
    panel_season_max: int | None = None
    #: Drop player-seasons below this many minutes before LOO / ventiles (0 = no filter).
    min_minutes: float = 0.0
    #: Number of bins for nonparametric draft-rate vs ``poolq_loo`` EDA (see ``poolq_binning``).
    ventiles: int = 20
    #: ``quantile`` — ``pd.qcut`` (~equal count per bin; 20 bins = traditional *ventiles*).
    #: ``equal_width`` — ``pd.cut`` on the min–max range of ``poolq_loo`` (same idea as 520 ``equal_width``).
    poolq_binning: str = "quantile"
    #: Where PNG/CSV exports from `panel_build.run_ventile_eda` are written.
    exports_dir: Path = field(default_factory=lambda: paths.mbb_dir() / "exports_inverted_u_v0")
    #: Which column(s) drive analysis after `apply_perf_metric_for_analysis`: `ppm`, `minutes`,
    #: `bpm`, `opm`/`obpm`, `dpm`/`dbpm`. One conductor pass uses the **first** list entry;
    #: use CELL 4 / `RUN_ALL_PERF_METRICS` to sweep. See `perf_metric.perf_options_df()`.
    perf_metric: list[str] = field(default_factory=lambda: ["minutes"])
    #: If True, overlay the quadratic LPM curve on the ventile figure (same Y ~ poolq + poolq² spec).
    show_quadratic_lpm_on_eda_plot: bool = True
    #: If True, draw the sample / draft / per-ventile-n caption block under the ventile plot PNG.
    #: Provenance is always written to ``ventile_eda_provenance_*.txt`` and printed when EDA runs.
    ventile_plot_show_metadata: bool = True
    #: ``poolq_line`` — single axes, draft rate vs mean ``poolq_loo`` per bin (current default).
    #: ``bins_bars_520`` — **bars only** vs bin index (1 = lowest poolq), ``steelblue`` / white edges
    #: (legacy Cell 11 left panel); optional metadata block below matches ``poolq_line`` layout.
    ventile_eda_plot_style: str = "poolq_line"
    #: Optional winsor on ``poolq_loo`` after LOO (e.g. ``(0.01, 0.99)``); ``None`` = off.
    poolq_winsor_quantiles: tuple[float, float] | None = None
    #: If True, replace ``perf`` with its z-score **within collegiate season** before LOO
    #: (``poolq_loo`` is then in cross-player SD units within each season).
    perf_zscore_within_season: bool = False
    #: After ``prepare_panel``, print draft-unmapped college names + SR-unmatched ESPN teams (reads QA CSVs).
    print_unmatched_school_lists: bool = False
    #: Cap printed lines per section (``None`` = print all). Full lists remain on disk in the cited CSVs.
    unmatched_school_report_max_lines: int | None = 400
    #: If True, drop rows whose team fails the draftee rule below (ventiles, LPM, integrity ``use``).
    restrict_teams_by_draftees: bool = True
    #: ``all_time`` — keep only ``team_id``s with ≥1 row with ``Y_draft==1`` anywhere in the filtered sample.
    #: ``season`` — keep only ``(team_id, season)`` with ≥1 roster member with ``Y_draft==1`` that season.
    draftee_restriction: str = "all_time"

    # --- SR refresh (``conductor.run_conductor`` — only if ``run_sr_refresh``) ----------
    #: If True, run crosswalk / jobs / optional scrape / match before final panel merge.
    run_sr_refresh: bool = False
    sr_refresh_do_crosswalk: bool = True
    sr_refresh_do_scrape_jobs: bool = True
    #: Network fetch to SR (needs ``pip install -e '.[scrape]'``).
    sr_refresh_do_scrape: bool = False
    sr_refresh_do_match: bool = True

    # --- Conductor steps (``conductor.run_conductor``) ---------------------------------
    #: Print ingest/draft/SR stub dicts (usually leave False).
    run_stage3_status: bool = False
    run_data_integrity_report: bool = True
    run_yearly_coverage_chart: bool = True
    run_ventile_eda: bool = True
    run_dirty_lpm: bool = True
    #: After a successful run, write ``PANEL`` to CSV (default path: canonical panel file).
    export_panel_after_run: bool = False
    export_panel_dest: Path | None = None

    # --- Data integrity report (`data_integrity.summarize_data_integrity`) ------------
    #: If both set, collegiate season window for the report; else min/max seasons from plot subset `use`.
    analysis_season_min: int | None = None
    analysis_season_max: int | None = None
    #: Draft-year band for match-rate denominators: [season_min - before, season_max + after].
    draft_year_before_season: int = 1
    draft_year_after_season: int = 5

    # --- Stage toggles (stubs until ingest/draft/SR code is ported) --------------------
    run_spine_refresh: bool = False
    run_draft_match: bool = False
    #: If True, `sr_bpm.run` calls `scrape_bpm.run_batch` (needs `pip install -e .[scrape]`).
    run_sr_scrape: bool = False
    #: Optional contact string embedded in the scraper User-Agent (email or URL).
    sr_scrape_contact: str | None = None
    #: Cap pages per conductor run (`None` = no cap; useful for testing throttles).
    sr_scrape_max_fetches: int | None = None

    def __post_init__(self) -> None:
        self.perf_metric = normalize_perf_metric_list(self.perf_metric)
        for m in self.perf_metric:
            resolve_perf_metric(m)
        pb = str(self.poolq_binning).strip().lower()
        if pb not in ("quantile", "equal_width"):
            raise ValueError(
                f"poolq_binning must be 'quantile' or 'equal_width', got {self.poolq_binning!r}"
            )
        self.poolq_binning = pb
        dr = str(self.draftee_restriction).strip().lower()
        if dr not in ("all_time", "season"):
            raise ValueError(
                f"draftee_restriction must be 'all_time' or 'season', got {self.draftee_restriction!r}"
            )
        self.draftee_restriction = dr
        ves = str(self.ventile_eda_plot_style).strip().lower()
        if ves not in ("poolq_line", "bins_bars_520"):
            raise ValueError(
                "ventile_eda_plot_style must be 'poolq_line' or 'bins_bars_520', "
                f"got {self.ventile_eda_plot_style!r}"
            )
        self.ventile_eda_plot_style = ves

    @property
    def perf_measure_label(self) -> str:
        """Plot caption from `perf_metric.plot_label_for_metric` (kept in sync automatically)."""
        return plot_label_for_metric(perf_metric_active(self))
