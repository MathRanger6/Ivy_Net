#!/usr/bin/env python3
"""Pass A — Empirical MBB: talent-only read (left) vs roster-pressure hero (right).

==============================================================================
FOR LATER CHARLES — read this block first
==============================================================================
What this file is
  One-shot script that builds the empirical pair for Alex:
    Left  — mean draft rate by quantile bins of player ability (perf / ppm z)
    Right — mean draft rate by poolq_loo bins (locked hero spec by default)

What this file is NOT
  - Not generative sim (Pass B) — see pass_b_generative_knockout_bundle.py
  - Not ρ ablation (Pass C) — see pass_c_rho_ablation_bundle.py
  - Not the full 530 pipeline UI — this reuses panel_build on the locked estimand

Pass A claim
  Empirical contrast: talent alone tends monotone; peer/roster context (poolq_loo)
  shows inverted-U. No λ language on the empirical side.

Pipeline (real data — no sim ASSIGN/SCORE/SELECT)
  VISUALIZE only: bin MBB panel → plot mean Y_draft (ability ventiles | poolq_loo).

Run (repo root)
  python sports/scripts/pass_a_empirical_bundle.py
  python sports/scripts/pass_a_empirical_bundle.py --season-min 2013 --season-max 2021

  # Sensitivity / exploration (parallel filenames — does not clobber locked PNGs)
  python sports/scripts/pass_a_empirical_bundle.py --season-min 2013 --season-max 2021 \\
    --n-bins 20 --poolq-binning equal_width --output-tag ew20

Outputs (pass_a/)
  Full panel + locked defaults: legacy names without season tag.
  Other windows / non-default spec: tagged PNG/CSV/txt (parallel to PD20–22 campaign).

Spec
  sports/540_READ_ME_SIM.md
==============================================================================
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SPORTS))

from gallery_knobs import HERO_BINS
from hero_gallery_paths import PASS_A, ensure_hero_dirs
from interval_overlap_paths import seasons_label
from plot_provenance import (
    HeroProvenance,
    hero_bin_label,
    hero_bin_slug,
    normalize_roster_x,
    population_slug,
    roster_x_label,
    roster_x_mathtext,
    roster_x_slug,
    season_slug,
    stamp_figure_footer,
    write_provenance_json,
)
from pd20_22_campaign_window import (
    activate_from_args,
    add_window_args,
    current_window,
)

DEFAULT_MIN_MINUTES = 20.0
DEFAULT_WINSOR_LO = 0.01
DEFAULT_WINSOR_HI = 0.99
DEFAULT_N_BINS = HERO_BINS
DEFAULT_POOLQ_BINNING = "quantile"

OUT = PASS_A

_spec: PassAHeroSpec | None = None


@dataclass(frozen=True)
class PassAHeroSpec:
    """Tunable Pass A hero / side-by-side figure spec."""

    n_bins: int = DEFAULT_N_BINS
    poolq_binning: str = DEFAULT_POOLQ_BINNING
    min_minutes: float = DEFAULT_MIN_MINUTES
    winsor_lo: float = DEFAULT_WINSOR_LO
    winsor_hi: float = DEFAULT_WINSOR_HI
    output_tag: str | None = None
    perf_metric: str = "ppm"
    y_draft_mode: str = "ever"
    min_team_season_games: int = 10
    dft: bool = False
    panel_rows: str = "all-ps"
    roster_x: str = "poolq_loo"

    @property
    def last_season_only(self) -> bool:
        from sports_pipeline.y_draft_mode import panel_rows_is_last_only

        return panel_rows_is_last_only(self.panel_rows)

    @property
    def population_label(self) -> str:
        return "+DFT" if self.dft else "full panel"

    @property
    def plot_spec_line(self) -> str:
        mode_label = "quantile" if self.poolq_binning == "quantile" else "equal width"
        pop = rf" · {self.population_label}" if self.dft else ""
        ls = r" · final-season PS only" if self.last_season_only else r" · all PS rows"
        return (
            rf"${self.n_bins}$ {mode_label} | min$={self.min_minutes:g}$ | "
            rf"mg$={int(self.min_team_season_games)}$ | "
            rf"winsor ${self.winsor_lo:g}$–${self.winsor_hi:g}${pop}{ls}"
        )

    def is_locked_default(self) -> bool:
        return (
            int(self.n_bins) == DEFAULT_N_BINS
            and self.poolq_binning == DEFAULT_POOLQ_BINNING
            and float(self.min_minutes) == DEFAULT_MIN_MINUTES
            and float(self.winsor_lo) == DEFAULT_WINSOR_LO
            and float(self.winsor_hi) == DEFAULT_WINSOR_HI
            and not self.output_tag
            and str(self.perf_metric).strip().lower() == "ppm"
            and str(self.y_draft_mode).strip().lower() == "ever"
            and not self.dft
        )

    @property
    def winsor_quantiles(self) -> tuple[float, float]:
        return (float(self.winsor_lo), float(self.winsor_hi))

    @property
    def bin_mode_slug(self) -> str:
        return hero_bin_slug(poolq_binning=self.poolq_binning, n_bins=self.n_bins)

    @property
    def bin_mode_label(self) -> str:
        return hero_bin_label(poolq_binning=self.poolq_binning, n_bins=self.n_bins)

    @property
    def winsor_slug(self) -> str:
        lo = int(round(self.winsor_lo * 100))
        hi = int(round(self.winsor_hi * 100))
        return f"winsor{lo:02d}{hi:02d}"


def _hero_spec() -> PassAHeroSpec:
    if _spec is None:
        raise RuntimeError("PassAHeroSpec not initialized — call activate_hero_spec() first")
    return _spec


def activate_hero_spec(spec: PassAHeroSpec) -> None:
    global _spec
    _spec = spec


def _w():
    return current_window()


def _filename_core() -> str:
    """Compact slug: always includes bin, population, min, mg, seasons."""
    spec = _hero_spec()
    w = _w()
    parts: list[str] = [
        spec.bin_mode_slug,
        population_slug(dft=spec.dft),
        f"min{int(spec.min_minutes)}",
        f"mg{int(spec.min_team_season_games)}",
        season_slug(w.season_min, w.season_max),
    ]
    perf = str(spec.perf_metric).strip().lower()
    if perf != "ppm":
        parts.insert(0, perf)
    if str(spec.y_draft_mode).strip().lower() == "season":
        parts.append("season_y")
    if spec.last_season_only:
        parts.append("last_ps")
    if normalize_roster_x(spec.roster_x) == "poolq":
        parts.insert(0, "poolq")
    if spec.output_tag:
        parts.append(spec.output_tag)
    return "_".join(parts)


def _hero_provenance(*, n_rows: int | None = None, n_drafts: int | None = None) -> HeroProvenance:
    spec = _hero_spec()
    w = _w()
    return HeroProvenance(
        bin_slug=spec.bin_mode_slug,
        bin_label=spec.bin_mode_label,
        perf_metric=str(spec.perf_metric).strip().lower(),
        season_min=int(w.season_min),
        season_max=int(w.season_max),
        min_minutes=float(spec.min_minutes),
        min_team_season_games=int(spec.min_team_season_games),
        population=population_slug(dft=spec.dft),
        y_draft_mode=str(spec.y_draft_mode).strip().lower(),
        winsor_lo=float(spec.winsor_lo),
        winsor_hi=float(spec.winsor_hi),
        panel_rows=str(spec.panel_rows),
        n_rows=n_rows,
        n_drafts=n_drafts,
        axis=roster_x_label(spec.roster_x),
    )


def _uses_legacy_names() -> bool:
    """Legacy side-by-side name retired — filenames always carry bin/pop/min/mg/seasons."""
    return False


def _name_parts() -> list[str]:
    return _filename_core().split("_")


def _tag_suffix() -> str:
    core = _filename_core()
    return f"_{core}" if core else ""


def _hero_slug() -> str:
    return _filename_core()


def _pass_a_png_name() -> str:
    return f"PASS_A_side_by_side_{_filename_core()}.png"


def _hero_png_name() -> str:
    return f"HERO_{_filename_core()}.png"


def _roster_csv_name() -> str:
    xslug = roster_x_slug(_hero_spec().roster_x)
    return f"PASS_A_binned_draft_rate_{xslug}_{_filename_core()}.csv"


def _ability_csv_name() -> str:
    return f"PASS_A_binned_draft_rate_ability_{_filename_core()}.csv"


def _lpm_txt_name() -> str:
    return f"PASS_A_lpm_hero_coefficients_{_filename_core()}.txt"


def _caption_txt_name() -> str:
    return f"PASS_A_side_by_side_caption_{_filename_core()}.txt"


def _provenance_json_name() -> str:
    return f"HERO_{_filename_core()}_provenance.json"


def _attach_roster_pressure_x(df: pd.DataFrame, spec: PassAHeroSpec) -> pd.DataFrame:
    """Add ``roster_x`` / ``roster_x_sq`` for hero binning and LPM."""
    import numpy as np

    work = df.copy()
    x = normalize_roster_x(spec.roster_x)
    if x == "poolq_loo":
        work["roster_x"] = pd.to_numeric(work["poolq_loo"], errors="coerce")
    else:
        work["roster_x"] = work.groupby(["team_id", "season"], observed=True)["perf"].transform("mean")
        lo_q, hi_q = float(spec.winsor_lo), float(spec.winsor_hi)
        s = work["roster_x"].dropna()
        if len(s):
            lo = float(s.quantile(lo_q))
            hi = float(s.quantile(hi_q))
            work["roster_x"] = work["roster_x"].clip(lower=lo, upper=hi)
    work["roster_x_sq"] = np.square(pd.to_numeric(work["roster_x"], errors="coerce"))
    return work


def roster_ventile_table(df: pd.DataFrame, spec: PassAHeroSpec) -> pd.DataFrame:
    """Bin ``roster_x``; within each bin, mean ``Y_draft``."""
    import numpy as np

    from sports_pipeline.panel_build import assign_poolq_bin_labels

    work = df.dropna(subset=["roster_x", "Y_draft"]).copy()
    x = pd.to_numeric(work["roster_x"], errors="coerce")
    work["vent"] = assign_poolq_bin_labels(x, spec.n_bins, spec.poolq_binning)
    tbl = (
        work.dropna(subset=["vent"])
        .groupby("vent", observed=True)
        .agg(
            n=("Y_draft", "size"),
            draft_rate=("Y_draft", "mean"),
            poolq_mean=("roster_x", "mean"),
            poolq_median=("roster_x", "median"),
            x_min=("roster_x", "min"),
            x_max=("roster_x", "max"),
        )
        .reset_index()
        .sort_values("vent")
    )
    if str(spec.poolq_binning).strip().lower() == "equal_width":
        from bdp_reigning_loo_plots import _equal_width_edges

        edges = _equal_width_edges(x.dropna().to_numpy(dtype=float), spec.n_bins)
        tbl["edge_lo"] = tbl["vent"].astype(int).map(lambda v: float(edges[int(v)]))
        tbl["edge_hi"] = tbl["vent"].astype(int).map(lambda v: float(edges[int(v) + 1]))
        tbl["x_center"] = (tbl["edge_lo"] + tbl["edge_hi"]) / 2.0
    else:
        tbl["edge_lo"] = tbl["x_min"]
        tbl["edge_hi"] = tbl["x_max"]
        tbl["x_center"] = tbl["poolq_mean"]
    return tbl


def _roster_quadratic_lpm(use: pd.DataFrame) -> pd.Series:
    """OLS Y_draft ~ 1 + roster_x + roster_x_sq."""
    import numpy as np

    y = pd.to_numeric(use["Y_draft"], errors="coerce").astype(float).to_numpy()
    p = pd.to_numeric(use["roster_x"], errors="coerce").astype(float).to_numpy()
    q = pd.to_numeric(use["roster_x_sq"], errors="coerce").astype(float).to_numpy()
    mask = np.isfinite(y) & np.isfinite(p) & np.isfinite(q)
    x_mat = np.column_stack([np.ones(mask.sum()), p[mask], q[mask]])
    beta, *_ = np.linalg.lstsq(x_mat, y[mask], rcond=None)
    spec = _hero_spec()
    xname = normalize_roster_x(spec.roster_x)
    return pd.Series(beta, index=["const", xname, f"{xname}_sq"])


def _drafted_team_ids(panel: pd.DataFrame) -> set:
    y = pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).astype(int)
    return set(panel.loc[y == 1, "team_id"].dropna().unique())


def _apply_dft(panel: pd.DataFrame, drafted_teams: set) -> pd.DataFrame:
    """+DFT — all player-seasons on teams with ≥1 Y=1 row in the reference panel."""
    return panel.loc[panel["team_id"].isin(drafted_teams)].copy()


def _y_label_note() -> str:
    spec = _hero_spec()
    parts: list[str] = []
    if str(spec.y_draft_mode).strip().lower() == "season":
        parts.append("season-Y label (Y=1 last PS only)")
    if spec.last_season_only:
        parts.append("final-season cross-section")
    return (" · " + " · ".join(parts)) if parts else ""


def _prepare_hero_panel():
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active
    from sports_pipeline.y_draft_mode import (
        apply_y_draft_last_season,
        audit_y1_survival,
        emit_survival_summary,
        filter_team_seasons_min_games,
        normalize_y_draft_mode,
        restrict_to_last_season_rows,
        set_last_survival_audit,
    )

    spec = _hero_spec()
    y_mode = normalize_y_draft_mode(spec.y_draft_mode)

    def _maybe_last_season(panel: pd.DataFrame, audits: list[dict] | None) -> pd.DataFrame:
        if not spec.last_season_only:
            return panel
        before = panel
        panel, ls_audit = restrict_to_last_season_rows(panel)
        if audits is not None:
            audits.append(ls_audit)
            audits.append(audit_y1_survival(before, panel, "last_season_only"))
        print(
            f"Last-season cross-section · {ls_audit['n_rows_before']:,} → "
            f"{ls_audit['n_rows_after']:,} rows · {ls_audit['n_athletes']:,} athletes",
            flush=True,
        )
        return panel

    def _build_cfg(*, min_minutes: float, min_team_season_games: int):
        from sports_pipeline.config import PipelineConfig

        w = _w()
        perf = str(spec.perf_metric).strip().lower()
        return PipelineConfig(
            perf_metric=[perf],
            perf_zscore_within_season=True,
            ventiles=int(spec.n_bins),
            poolq_binning=str(spec.poolq_binning),
            poolq_winsor_quantiles=spec.winsor_quantiles,
            min_minutes=float(min_minutes),
            min_team_season_games=int(min_team_season_games),
            drop_dash_placeholder_names=True,
            restrict_teams_by_draftees=False,
            use_prebuilt_panel_csv=False,
            panel_season_min=int(w.season_min),
            panel_season_max=int(w.season_max),
            analysis_season_min=int(w.season_min),
            analysis_season_max=int(w.season_max),
        )

    if y_mode == "season":
        cfg_pre = _build_cfg(min_minutes=0.0, min_team_season_games=0)
        panel = conductor.prepare_panel(cfg_pre)
        panel = panel_build.apply_perf_metric_for_analysis(
            panel,
            perf_metric_active(cfg_pre),
            poolq_winsor_quantiles=cfg_pre.poolq_winsor_quantiles,
            zscore_perf_within_season=True,
        )
        panel, label_audit = apply_y_draft_last_season(panel)
        audits: list[dict] = [label_audit]

        drafted_teams: set | None = None
        if spec.dft:
            drafted_teams = _drafted_team_ids(panel.dropna(subset=["team_id", "season"]))

        if int(spec.min_team_season_games) > 0:
            before = panel
            panel = filter_team_seasons_min_games(panel, int(spec.min_team_season_games))
            audits.append(
                audit_y1_survival(
                    before,
                    panel,
                    f"min_team_season_games<={spec.min_team_season_games}",
                )
            )

        cfg_filt = _build_cfg(min_minutes=float(spec.min_minutes), min_team_season_games=0)
        before = panel
        panel = panel_build.filter_panel(panel, cfg_filt)
        if float(spec.min_minutes) > 0:
            audits.append(
                audit_y1_survival(before, panel, f"min_minutes>={spec.min_minutes:g}")
            )

        if spec.dft and drafted_teams is not None:
            before = panel
            panel = _apply_dft(panel, drafted_teams)
            audits.append(audit_y1_survival(before, panel, "+DFT team filter"))

        panel = _maybe_last_season(panel, audits)

        set_last_survival_audit(audits)
        emit_survival_summary(audits)
        return cfg_filt, panel

    drafted_teams: set | None = None
    if spec.dft:
        cfg0 = _build_cfg(min_minutes=0.0, min_team_season_games=int(spec.min_team_season_games))
        raw = conductor.prepare_panel(cfg0)
        drafted_teams = _drafted_team_ids(raw.dropna(subset=["team_id", "season"]))

    cfg = _build_cfg(
        min_minutes=float(spec.min_minutes),
        min_team_season_games=int(spec.min_team_season_games),
    )
    panel = conductor.prepare_panel(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    set_last_survival_audit(None)
    use = panel_build.filter_panel(panel, cfg)
    if spec.dft and drafted_teams is not None:
        use = _apply_dft(use, drafted_teams)
    use = _maybe_last_season(use, None)
    return cfg, use


def ability_ventile_table(df: pd.DataFrame, n_bins: int) -> pd.DataFrame:
    """Bin ``perf`` (ability); within each bin, mean ``Y_draft`` (always quantile)."""
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    work = df.dropna(subset=["perf", "Y_draft"]).copy()
    work["vent"] = assign_poolq_bin_labels(work["perf"], n_bins, "quantile")
    return (
        work.dropna(subset=["vent"])
        .groupby("vent", observed=True)
        .agg(
            n=("Y_draft", "size"),
            draft_rate=("Y_draft", "mean"),
            perf_mean=("perf", "mean"),
            perf_median=("perf", "median"),
        )
        .reset_index()
        .sort_values("vent")
    )


def run_layer_a_lpm(out_dir: Path, use: pd.DataFrame) -> pd.Series:
    """Layer A: OLS Y_draft ~ roster_x + roster_x_sq on hero-filtered panel."""
    spec = _hero_spec()
    coef = _roster_quadratic_lpm(use)
    seasons = seasons_label(_w().season_min, _w().season_max)
    xname = normalize_roster_x(spec.roster_x)
    sq_name = f"{xname}_sq"
    lines = [
        f"# Hero Layer A — quadratic LPM ({date.today().isoformat()})",
        f"seasons={seasons} ({_w().season_min}–{_w().season_max})",
        f"n={len(use):,} player-seasons after hero filters",
        f"Y_draft=1 count: {int(use['Y_draft'].sum()):,}",
        f"roster_x={xname}",
        f"n_bins={spec.n_bins} poolq_binning={spec.poolq_binning} perf_metric={spec.perf_metric}",
        f"min_minutes={spec.min_minutes} winsor={spec.winsor_lo}–{spec.winsor_hi}",
        f"mg={spec.min_team_season_games} y_draft_mode={spec.y_draft_mode} "
        f"panel_rows={spec.panel_rows} dft={spec.dft}",
        *( [f"output_tag={spec.output_tag}"] if spec.output_tag else [] ),
        "",
        f"Model: Y_draft ~ const + {xname} + {sq_name}",
        "",
        coef.to_string(),
        "",
        f"Interpretation: beta_{sq_name} = {coef[sq_name]:.6g} "
        f"({'concave / inverted-U consistent' if coef[sq_name] < 0 else 'not concave — flat elite tail on POST-QC panel'})",
    ]
    txt = out_dir / _lpm_txt_name()
    txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return coef


def build_empirical_tables(out_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, HeroProvenance]:
    """Ability ventiles (left) + roster-pressure ventiles (right) on the same filtered panel."""
    spec = _hero_spec()
    _cfg, use = _prepare_hero_panel()
    use = _attach_roster_pressure_x(use, spec)
    n_rows = int(len(use))
    n_drafts = int(pd.to_numeric(use["Y_draft"], errors="coerce").fillna(0).sum())
    prov = _hero_provenance(n_rows=n_rows, n_drafts=n_drafts)
    ability = ability_ventile_table(use, spec.n_bins)
    roster = roster_ventile_table(use, spec)
    ability_path = out_dir / _ability_csv_name()
    roster_path = out_dir / _roster_csv_name()
    ability.to_csv(ability_path, index=False)
    roster.to_csv(roster_path, index=False)
    print(f"Wrote {ability_path.name} and {roster_path.name}")
    coef = run_layer_a_lpm(out_dir, use)
    write_provenance_json(
        out_dir / _provenance_json_name(),
        {
            **prov.to_dict(),
            "footer": prov.footer_text(),
            "roster_x": normalize_roster_x(spec.roster_x),
            "poolq_binning": spec.poolq_binning,
            "output_files": {
                "hero_png": _hero_png_name(),
                "side_by_side_png": _pass_a_png_name(),
                "roster_csv": _roster_csv_name(),
                "ability_csv": _ability_csv_name(),
            },
        },
    )
    print(f"Wrote {_provenance_json_name()}")
    return ability, roster, coef, prov


def _hero_shape_readout(coef: pd.Series) -> str:
    sq_keys = [k for k in coef.index if str(k).endswith("_sq")]
    b2 = float(coef[sq_keys[0]]) if sq_keys else float("nan")
    if b2 < 0:
        return "concave / inverted-U consistent (check mg — may be pre-QC artifact)"
    return "not concave — flat elite tail on POST-QC panel"


def _hero_panel_note(spec: PassAHeroSpec, coef: pd.Series) -> str:
    mg = int(spec.min_team_season_games)
    sq_keys = [k for k in coef.index if str(k).endswith("_sq")]
    b2 = float(coef[sq_keys[0]]) if sq_keys else float("nan")
    if mg <= 0 and b2 < 0:
        return "pre-QC replay (mg=0) — inverted-U tail likely fragment/cameo artifact"
    if mg > 0 and b2 < 0:
        return "unexpected concavity at mg>0 — investigate"
    if mg > 0:
        return "middle rise; flat elite tail"
    return "mg=0 — not canonical POST-QC hero"


def _caption_panel_lines(spec: PassAHeroSpec, coef: pd.Series, seasons: str) -> list[str]:
    mg = int(spec.min_team_season_games)
    shape = _hero_shape_readout(coef)
    xdesc = roster_x_label(spec.roster_x)
    lines = [
        "Right: Mean NBA draft rate by ventile of roster pressure",
        f"({xdesc}), MBB {seasons}, mg={mg}, min_minutes={spec.min_minutes:g}.",
        f"LPM readout: {shape}.",
    ]
    if mg <= 0:
        lines.append(
            "mg=0 includes fragmentary team-seasons — sensitivity only; canonical hero uses mg=10."
        )
    else:
        lines.append("Canonical POST-QC hero: mg=10. July pre-QC inverted-U: pass_a/sensitivity/.")
    return lines


def _lpm_annotation(coef: pd.Series) -> str | None:
    """On-figure LPM readout for roster-pressure panel."""
    sq_keys = [k for k in coef.index if str(k).endswith("_sq")]
    if not sq_keys:
        return None
    b2 = float(coef[sq_keys[0]])
    if b2 < 0:
        return rf"LPM: $\beta_2={b2:.4g}$ ($<0$, concave)"
    return rf"LPM: $\beta_2={b2:+.4g}$ (flat / not concave on this panel)"


def build_hero_single_panel(
    out_dir: Path,
    roster: pd.DataFrame,
    coef: pd.Series,
    *,
    prov: HeroProvenance,
) -> None:
    """Standalone hero PNG (poolq_loo ventiles only)."""
    from gallery_mathtext import configure_matplotlib_mathtext
    from hero_plot_style import (
        PLOT_DPI,
        annotate_bar_n,
        count_weighted_bar_colors,
        format_poolq_tick,
        finalize_bar_figure,
        layout_bar_figure,
        set_wrapped_ax_title,
        stamp_wrapped_footer,
    )

    configure_matplotlib_mathtext()
    spec = _hero_spec()
    seasons = seasons_label(_w().season_min, _w().season_max)
    xtex = roster_x_mathtext(spec.roster_x)
    bin_badge = spec.bin_mode_label
    fig, ax = plt.subplots(figsize=(10.5, 5.8))
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float)
    counts = roster["n"].to_numpy(dtype=int)
    is_ew = str(spec.poolq_binning).strip().lower() == "equal_width"
    if is_ew:
        bar_colors = count_weighted_bar_colors(counts, cmap_name="Blues")
    else:
        bar_colors = ["steelblue"] * len(x)
    ax.bar(x, y, color=bar_colors, edgecolor="white", alpha=0.92, width=0.85)
    annotate_bar_n(ax, x, y, counts, bar_colors)
    ax.set_xticks(x)
    if is_ew:
        ax.set_xticklabels([format_poolq_tick(v) for v in roster["x_center"]], fontsize=7, rotation=45, ha="right")
        ax.set_xlabel(rf"poolq$_{{\mathrm{{LOO}}}}$ bin midpoint · {bin_badge}", labelpad=2)
    else:
        ax.set_xlabel(rf"Bin ($1$ = lowest {xtex}) · {bin_badge}")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    set_wrapped_ax_title(
        ax,
        [
            rf"Empirical hero — roster context · MBB {seasons}",
            rf"{bin_badge} · {spec.plot_spec_line} · POST-QC panel{_y_label_note()}",
        ],
        fontsize=10,
    )
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    note = _lpm_annotation(coef)
    if note:
        ax.text(0.02, 0.96, note, transform=ax.transAxes, fontsize=8, va="top")
    seasons_short = seasons_label(_w().season_min, _w().season_max)
    pop = spec.population_label
    y_mode = str(spec.y_draft_mode).strip().lower()
    finalize_bar_figure(
        fig,
        [
            (
                f"HERO · poolq_LOO · {seasons_short} · {bin_badge} · "
                f"n={prov.n_rows:,} · drafts={prov.n_drafts:,}"
            ),
            (
                f"min{spec.min_minutes:g} mg{spec.min_team_season_games} · {pop} · "
                f"Y={y_mode} · winsor {spec.winsor_lo:g}–{spec.winsor_hi:g}"
            ),
        ],
        rotated_x=is_ew,
    )
    png = out_dir / _hero_png_name()
    fig.savefig(png, dpi=PLOT_DPI, facecolor="white")
    plt.close(fig)
    print(f"Wrote {png}")


def build_side_by_side(
    out_dir: Path,
    ability: pd.DataFrame,
    roster: pd.DataFrame,
    coef: pd.Series,
    *,
    prov: HeroProvenance,
) -> None:
    """Left = talent (ability ventiles); right = roster pressure (poolq_loo hero)."""
    from gallery_mathtext import configure_matplotlib_mathtext
    from hero_plot_style import PLOT_DPI

    configure_matplotlib_mathtext()
    spec = _hero_spec()
    perf = str(spec.perf_metric).strip().upper()
    seasons = seasons_label(_w().season_min, _w().season_max)
    xtex = roster_x_mathtext(spec.roster_x)
    left_spec = (
        rf"${spec.n_bins}$ quantile | min$={spec.min_minutes:g}$ | "
        rf"winsor ${spec.winsor_lo:g}$–${spec.winsor_hi:g}$ | perf={perf}"
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    ax = axes[0]
    x = ability["vent"].to_numpy(dtype=float) + 1
    y = ability["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="seagreen", edgecolor="white", alpha=0.9)
    ax.set_xlabel(rf"Ability ventile ($1$ = lowest perf, {perf} $z$ within season)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(f"Empirical — talent alone\n{left_spec}")
    ax.set_xticks(x)

    ax = axes[1]
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="steelblue", edgecolor="white", alpha=0.9)
    ax.set_xlabel(rf"Ventile bin ($1$ = lowest {xtex})")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(
        f"Empirical — roster context (hero)\n"
        f"{spec.plot_spec_line} · {_hero_panel_note(spec, coef)}"
    )
    ax.set_xticks(x)
    note = _lpm_annotation(coef)
    if note:
        ax.text(0.02, 0.96, note, transform=ax.transAxes, fontsize=8, va="top")

    fig.suptitle(
        f"Pass A — Empirical MBB: talent vs roster context · {seasons} · POST-QC panel\n"
        r"Qualitative shapes only; generative inverted-U is Pass B/C (not bin-for-bin match)",
        fontsize=11,
        y=1.02,
    )
    stamp_figure_footer(fig, prov.footer_text())
    fig.tight_layout(rect=(0, 0.05, 1, 0.98))
    png = out_dir / _pass_a_png_name()
    fig.savefig(png, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")

    caption = out_dir / _caption_txt_name()
    caption.write_text(
        "\n".join(
            [
                "Pass A caption — empirical pair",
                "",
                f"Spec: n_bins={spec.n_bins} poolq_binning={spec.poolq_binning} "
                f"min_minutes={spec.min_minutes} mg={spec.min_team_season_games} "
                f"winsor={spec.winsor_lo}–{spec.winsor_hi} perf_metric={spec.perf_metric}",
                *( [f"output_tag={spec.output_tag}"] if spec.output_tag else [] ),
                "",
                "Left: Mean NBA draft rate by ventile of player ability (perf z-scored",
                "within season). Monotone-up is the talent-only stylized read.",
                "",
                *_caption_panel_lines(spec, coef, seasons),
                "",
                "We do not use λ language on the empirical side; λ is a generative score knob (Pass B).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _sanitize_output_tag(raw: str | None) -> str | None:
    if raw is None or raw == "":
        return None
    tag = re.sub(r"[^A-Za-z0-9_-]+", "_", raw.strip()).strip("_")
    if not tag:
        raise ValueError(f"Invalid --output-tag {raw!r} (empty after sanitization)")
    return tag


def add_hero_spec_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--n-bins",
        type=int,
        default=None,
        help=f"Poolq_loo + ability bin count (default: GALLERY_HERO_BINS or {DEFAULT_N_BINS}).",
    )
    parser.add_argument(
        "--poolq-binning",
        choices=("quantile", "equal_width"),
        default=DEFAULT_POOLQ_BINNING,
        help="Right-panel roster-pressure binning (left ability panel always quantile).",
    )
    parser.add_argument(
        "--roster-x",
        choices=("poolq_loo", "poolq"),
        default="poolq_loo",
        help=(
            "Right-panel x-axis: poolq_loo (LOO teammate mean; default) or "
            "poolq (team-season mean perf z, includes self). Not F-HERO T̂_j band plot."
        ),
    )
    parser.add_argument(
        "--min-minutes",
        type=float,
        default=DEFAULT_MIN_MINUTES,
        help=f"Playing-time floor (default: {DEFAULT_MIN_MINUTES:g}).",
    )
    parser.add_argument(
        "--winsor-lo",
        type=float,
        default=DEFAULT_WINSOR_LO,
        help=f"Lower poolq winsor quantile (default: {DEFAULT_WINSOR_LO}).",
    )
    parser.add_argument(
        "--winsor-hi",
        type=float,
        default=DEFAULT_WINSOR_HI,
        help=f"Upper poolq winsor quantile (default: {DEFAULT_WINSOR_HI}).",
    )
    parser.add_argument(
        "--min-team-season-games",
        type=int,
        default=10,
        help="Drop team-seasons with <= this many games after season-Y labeling (default 10).",
    )
    parser.add_argument(
        "--y-draft-mode",
        choices=("ever", "season"),
        default="ever",
        help=(
            "Y_draft labeling: ever-draft (default) or season-Y "
            "(Y=1 on draftee's last college PS only; earlier PS rows kept with Y=0)."
        ),
    )
    parser.add_argument(
        "--panel-rows",
        choices=("all-ps", "last-ps"),
        default="all-ps",
        help=(
            "Panel rows for plots. all-ps (default): every PS passing filters. "
            "last-ps: one row per athlete at max(season) — cross-section."
        ),
    )
    parser.add_argument(
        "--last-season-only",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--all-seasons",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--dft",
        action="store_true",
        help="+DFT: keep player-seasons on teams with ≥1 draftee (all roster PS).",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=None,
        help=(
            "Override output directory (e.g. sports_sandbox/hero). "
            "Default: pass_a/ or pass_a/season_y_experiment/ or pass_a/sensitivity/."
        ),
    )
    parser.add_argument(
        "--output-tag",
        type=str,
        default=None,
        help=(
            "Extra filename tag for exploration runs (e.g. ew20). "
            "Non-default spec also embeds bin mode in filenames."
        ),
    )
    parser.add_argument(
        "--side-by-side",
        action="store_true",
        help="Also write talent|roster pair PNG + caption (default: HERO single panel only).",
    )
    parser.add_argument(
        "--perf-metric",
        type=str,
        default="ppm",
        choices=("ppm", "obpm", "opm", "bpm", "dbpm", "dpm"),
        help="Own-ability + LOO teammate perf source (default ppm). SR merge required for obpm/bpm.",
    )


def hero_spec_from_args(args: argparse.Namespace) -> PassAHeroSpec:
    n_bins = DEFAULT_N_BINS if args.n_bins is None else int(args.n_bins)
    if n_bins < 2:
        raise SystemExit("--n-bins must be >= 2")
    winsor_lo = float(args.winsor_lo)
    winsor_hi = float(args.winsor_hi)
    if not (0.0 <= winsor_lo < winsor_hi <= 1.0):
        raise SystemExit("--winsor-lo and --winsor-hi must satisfy 0 <= lo < hi <= 1")
    from sports_pipeline.y_draft_mode import resolve_panel_rows_from_args

    panel_rows = resolve_panel_rows_from_args(args)
    return PassAHeroSpec(
        n_bins=n_bins,
        poolq_binning=str(args.poolq_binning),
        min_minutes=float(args.min_minutes),
        winsor_lo=winsor_lo,
        winsor_hi=winsor_hi,
        output_tag=_sanitize_output_tag(args.output_tag),
        perf_metric=str(args.perf_metric).strip().lower(),
        y_draft_mode=str(args.y_draft_mode).strip().lower(),
        min_team_season_games=int(args.min_team_season_games),
        dft=bool(args.dft),
        panel_rows=panel_rows,
        roster_x=normalize_roster_x(str(args.roster_x)),
    )


def _resolve_out_dir(output_root: Path | None) -> Path:
    """Non-PPM robustness runs go under pass_a/sensitivity/ (Track C)."""
    if output_root is not None:
        out = output_root if output_root.is_absolute() else REPO / output_root
        out.mkdir(parents=True, exist_ok=True)
        return out
    spec = _hero_spec()
    if str(spec.y_draft_mode).strip().lower() == "season":
        out = OUT / "season_y_experiment"
        out.mkdir(parents=True, exist_ok=True)
        return out
    if str(spec.perf_metric).strip().lower() == "ppm" and spec.is_locked_default():
        return OUT
    sens = OUT / "sensitivity"
    sens.mkdir(parents=True, exist_ok=True)
    return sens


def main() -> None:
    parser = argparse.ArgumentParser(description="Pass A empirical HERO (+ optional talent|roster side-by-side).")
    add_window_args(parser)
    add_hero_spec_args(parser)
    args = parser.parse_args()
    activate_from_args(args)
    spec = hero_spec_from_args(args)
    activate_hero_spec(spec)

    out_dir = _resolve_out_dir(args.output_root)
    ensure_hero_dirs()
    out_dir.mkdir(parents=True, exist_ok=True)
    seasons = seasons_label(_w().season_min, _w().season_max)
    print(
        f"Pass A · seasons {seasons} ({_w().season_min}–{_w().season_max}) · "
        f"perf={spec.perf_metric} · "
        f"{spec.bin_mode_slug} min={spec.min_minutes:g} mg={spec.min_team_season_games} "
        f"winsor={spec.winsor_lo}–{spec.winsor_hi} "
        f"pop={population_slug(dft=spec.dft)} panel={spec.panel_rows} "
        f"roster_x={normalize_roster_x(spec.roster_x)} Y={spec.y_draft_mode}"
        + (f" tag={spec.output_tag}" if spec.output_tag else "")
        + (f" · out={out_dir.relative_to(REPO)}" if out_dir != OUT else ""),
        flush=True,
    )
    ability, roster, coef, prov = build_empirical_tables(out_dir)
    build_hero_single_panel(out_dir, roster, coef, prov=prov)
    if args.side_by_side:
        build_side_by_side(out_dir, ability, roster, coef, prov=prov)
        print(f"\nDone. HERO: {out_dir / _hero_png_name()} · side-by-side: {out_dir / _pass_a_png_name()}")
    else:
        print(f"\nDone. HERO: {out_dir / _hero_png_name()}")


if __name__ == "__main__":
    main()
