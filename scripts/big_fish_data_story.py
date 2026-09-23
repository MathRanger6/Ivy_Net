#!/usr/bin/env python3
"""Big Fish domains — 3×3 data story panels (Legends + Football + Education).

Run (repo root):
  python scripts/big_fish_data_story.py --domain legends --mode all
  python scripts/big_fish_data_story.py --domain football --mode all
  python scripts/big_fish_data_story.py --domain nels88 --mode all
  python scripts/big_fish_data_story.py --domain hsb80_soph --mode all
  python scripts/big_fish_data_story.py --domain hsb80_senior --mode all
  python scripts/big_fish_data_story.py --domain legends --mode perf-story
  python scripts/big_fish_data_story.py --domain football --mode perf-story
  python scripts/big_fish_data_story.py --domain football --mode hero QB RB_FB
  python scripts/big_fish_data_story.py --domain football --positions QB WR_TE --mode perf-story
  python scripts/big_fish_data_story.py --domain football --mode all DB --team-mean
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
SPORTS_SCRIPTS = REPO / "sports" / "scripts"
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(SPORTS_SCRIPTS))

from empirical_team_interval_overlap import (  # noqa: E402
    _compute_H_sort,
    _team_intervals,
    build_figure,
)
from gallery_mathtext import configure_matplotlib_mathtext  # noqa: E402
from hero_plot_style import PLOT_DPI, annotate_bar_n, count_weighted_bar_colors, format_poolq_tick  # noqa: E402
from sports_pipeline.y_draft_mode import PANEL_ROWS_LAST, restrict_to_last_season_rows  # noqa: E402
from story_page_layout import MOSAIC_PAGE_SIZE_CHOICES, PERF_PAGE_SIZE_CHOICES  # noqa: E402
from build_perf_metric_mosaic import build_perf_metric_story_pages  # noqa: E402

SANDBOX_ROOT = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"

ECDF_COHORT = "#2e75b6"
ECDF_POS = "#ed7d31"
ECDF_NEG = "#b2182b"
ECDF_BASE = "#757575"
ECDF_LOO_HIST = "#4daf4a"

# (column, short name, axis label) — culminating composite last
LEGENDS_PERF_METRICS: tuple[tuple[str, str, str], ...] = (
    ("z_damage_per_min", "dmg/min", r"Own $z_{\mathrm{dmg/min}}$"),
    ("z_earned_gold_per_min", "gold/min", r"Own $z_{\mathrm{gold/min}}$"),
    ("z_kda_ratio", "KDA", r"Own $z_{\mathrm{KDA}}$"),
    ("z_kill_participation", "kill part.", r"Own $z_{\mathrm{kill\ part.}}$"),
    ("z_vision_score_per_min", "vision/min", r"Own $z_{\mathrm{vision/min}}$"),
    ("z_gold_diff_15", "gold @15", r"Own $z_{\mathrm{gold@15}}$"),
    ("z_xp_diff_15", "XP @15", r"Own $z_{\mathrm{XP@15}}$"),
    ("z_cs_diff_15", "CS @15", r"Own $z_{\mathrm{CS@15}}$"),
    ("own_performance_index", "Â composite", r"Own $\hat{A}$ composite"),
)

FOOTBALL_PERF_METRICS: tuple[tuple[str, str, str], ...] = (
    ("z_performance_volume", "volume z", r"Own $z_{\mathrm{volume}}$ (Alex)"),
    ("z_performance_efficiency", "efficiency z", r"Own $z_{\mathrm{efficiency}}$ (Alex)"),
    ("z_diy_recruit_rating", "recruit z · prior", r"Recruit rating $z$ (prior · DIY)"),
    ("z_diy_ppa_total_all", "PPA total z", r"PPA total $z$ (DIY · skill pos.)"),
    ("z_diy_usage_overall", "usage z", r"Usage $z$ (DIY · skill pos.)"),
    ("own_performance_index", "Â composite", r"Own $\hat{A}$ composite (Alex)"),
)

# Raw columns → DIY z column names (1% winsor · z within position_group × season)
FOOTBALL_DIY_Z_SOURCES: tuple[tuple[str, str], ...] = (
    ("recruit_rating", "z_diy_recruit_rating"),
    ("ppa_total_all", "z_diy_ppa_total_all"),
    ("usage_overall", "z_diy_usage_overall"),
)

DOMAIN_PERF_METRICS: dict[str, tuple[tuple[str, str, str], ...]] = {
    "legends": LEGENDS_PERF_METRICS,
    "football": FOOTBALL_PERF_METRICS,
}

# Legends has 9 metric rows — split across two letter/tabloid pages.
LEGENDS_PERF_ROWS_PER_PAGE = 5

PERF_STORY_TITLES: dict[str, str] = {
    "legends": "Legends (LoL) — HERO by metric · P(promoted) vs teammate LOO",
    "football": "Football (FBS) — HERO by metric · P(drafted) vs teammate LOO",
}

PERF_STORY_COPY: dict[str, dict[str, str | tuple[str, ...]]] = {
    "legends": {
        "title": "Legends (LoL) — HERO by metric · P(promoted) vs teammate LOO",
        "subtitle_tpl": (
            "Dev cohort · N={n:,} · promoted={y_rate:.1%} · "
            "each row = P(Y) vs LOO for that metric · left=Q16 · right=EW16"
        ),
        "head": "HERO porches — teammate LOO axis varies by row",
        "head_lines": (
            "Cohort: developmental · eligible · no prior top tier · full 2y follow-up",
            "Y: P(top-tier debut within 2y) · X: teammate LOO on same metric (excl. self)",
            "Each row: environment curve for a different peer-context definition",
            "Last row: composite Â LOO (Alex teammate_mean_performance_excl_self)",
            "Not own-ability bins · EW: count-weighted blues · Q16: equal-n ventiles",
        ),
    },
    "football": {
        "title": "Football (FBS) — HERO by metric · P(drafted) vs teammate LOO",
        "subtitle_tpl": (
            "Final-season cohort · N={n:,} · drafted={y_rate:.1%} · "
            "each row = P(Y) vs LOO for that metric · left=Q16 · right=EW16"
        ),
        "head": "HERO porches — teammate LOO axis varies by row",
        "head_lines": (
            "Cohort: eligible analysis · skill positions (OL excluded) · final-ps",
            "Panel rows: one row per player at max(season) in data (MBB last-ps rule)",
            "Y: P(drafted next NFL draft) · X: teammate LOO on same metric (excl. self)",
            "Rows 1–2: Alex z_vol / z_eff LOO · 3–5: DIY metric LOO (exploratory v0)",
            "Last row: composite Â LOO (Alex teammate_mean_performance_excl_self)",
            "Exit season: drafted or attrition (no later row) · LOO from full roster pond",
        ),
    },
}

# Subset for quick hero-mode component probes (full set → --mode perf-story)
LEGENDS_HERO_COMPONENTS: tuple[tuple[str, str, tuple[str, ...]], ...] = tuple(
    (col, label, ("quantile", "equal_width"))
    for col, _short, label in LEGENDS_PERF_METRICS
    if col in {"z_kda_ratio", "z_damage_per_min", "z_kill_participation"}
)


@dataclass(frozen=True)
class DomainSpec:
    key: str
    prefix: str
    csv: Path
    sandbox: str
    title: str
    subtitle: str
    reigning_tag: str
    ai_col: str
    loo_col: str
    y_col: str
    pool_col: str
    team_keys: tuple[str, ...]
    season_key: str
    grain: str
    y_pos_label: str
    y_neg_label: str
    overlap_xlab: str
    cohort_lines: tuple[str, ...]
    panel_rows: str = "all-ps"
    athlete_id_col: str | None = None
    tie_break_col: str | None = None


FOOTBALL_POSITION_GROUPS: tuple[str, ...] = (
    "DB",
    "WR_TE",
    "DL_EDGE",
    "LB",
    "RB_FB",
    "QB",
    "K",
    "P",
)

FOOTBALL_POSITION_ALIASES: dict[str, str] = {
    "WR": "WR_TE",
    "TE": "WR_TE",
    "DL": "DL_EDGE",
    "EDGE": "DL_EDGE",
    "RB": "RB_FB",
    "FB": "RB_FB",
}


@dataclass(frozen=True)
class PositionFilter:
    """Football-only subset on ``position_group``; LOO recomputed within the filter."""

    groups: tuple[str, ...]

    @classmethod
    def parse(cls, tokens: list[str] | None) -> PositionFilter | None:
        if not tokens:
            return None
        seen: set[str] = set()
        groups: list[str] = []
        for raw in tokens:
            token = raw.strip().upper()
            if not token:
                continue
            token = FOOTBALL_POSITION_ALIASES.get(token, token)
            if token not in FOOTBALL_POSITION_GROUPS:
                valid = ", ".join(FOOTBALL_POSITION_GROUPS)
                raise SystemExit(f"Unknown position_group {raw!r}. Valid: {valid}")
            if token not in seen:
                seen.add(token)
                groups.append(token)
        if not groups:
            return None
        return cls(groups=tuple(groups))

    @property
    def label(self) -> str:
        return " · ".join(self.groups)

    @property
    def slug(self) -> str:
        return "pos_" + "_".join(self.groups)

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        if "position_group" not in df.columns:
            raise ValueError("position filter requires position_group column")
        out = df.loc[df["position_group"].isin(self.groups)].copy()
        if out.empty:
            raise SystemExit(f"No rows after position filter ({self.label})")
        return out


@dataclass(frozen=True)
class PeerAxis:
    """Panels 7–9 peer context: teammate LOO (default) or team mean T̂_j (incl. self)."""

    use_team_mean: bool = False

    @classmethod
    def from_flag(cls, team_mean: bool) -> PeerAxis:
        return cls(use_team_mean=bool(team_mean))

    @property
    def key(self) -> str:
        return "team_mean" if self.use_team_mean else "loo"

    @property
    def path_suffix(self) -> str:
        return "peer_tj" if self.use_team_mean else ""

    def x_col(self, spec: DomainSpec) -> str:
        return "team_mean_ai" if self.use_team_mean else spec.loo_col

    def x_label(self, *, bin_tag: str = "Q16", short: str | None = None) -> str:
        if self.use_team_mean:
            return rf"Team $\hat{{T}}_j$ ({bin_tag})"
        if short:
            return f"Teammate LOO · {short} ({bin_tag})"
        return f"Teammate LOO ({bin_tag})"

    def slug_part(self) -> str:
        return "team_tj" if self.use_team_mean else "team_loo"


DOMAINS: dict[str, DomainSpec] = {
    "legends": DomainSpec(
        key="legends",
        prefix="LEGENDS",
        csv=REPO / "datasets/legends/lol_big_fish_player_split_panel.csv",
        sandbox="legends_sandbox",
        title="Legends (LoL) data story — dev cohort",
        subtitle="developmental · full 2y follow-up · own index · team LOO  |  Read top-left → bottom-right",
        reigning_tag="q16_dev_team_loo_promo2y",
        ai_col="own_performance_index",
        loo_col="teammate_mean_performance_excl_self",
        y_col="top_tier_debut_within_2y",
        pool_col="team_roster_players",
        team_keys=("teamid", "year", "split"),
        season_key="year",
        grain="player stint · developmental league · Alex performance index",
        y_pos_label="Promoted",
        y_neg_label="Not promoted",
        overlap_xlab=r"Own performance index ($z$ within split year)",
        cohort_lines=(
            "Domain: LoL esports (Oracle's Elixir)",
            "Grain: dev-league player stint",
            "Y: top-tier debut within 2y",
            "Peer X: teammate LOO index",
            "Filter: eligible dev · no prior top tier",
            "",
            "Reigning tag:",
            "q16_dev_team_loo_promo2y",
        ),
    ),
    "football": DomainSpec(
        key="football",
        prefix="FOOTBALL",
        csv=REPO
        / "datasets/football/football_big_fish_player_season_panel/football_big_fish_player_season_panel.csv",
        sandbox="football_sandbox",
        title="Football data story — FBS eligible · final season",
        subtitle="final-season PS · eligible analysis · team LOO  |  Read top-left → bottom-right",
        reigning_tag="q16_eligible_team_loo_draft_last_ps",
        ai_col="own_performance_index",
        loo_col="teammate_mean_performance_excl_self",
        y_col="drafted_next_draft",
        pool_col="team_roster_players",
        team_keys=("team", "season"),
        season_key="season",
        grain="player · final college season in data · FBS · CollegeFootballData",
        y_pos_label="Drafted",
        y_neg_label="Not drafted",
        overlap_xlab=r"Own performance index ($z$ within season)",
        cohort_lines=(
            "Domain: FBS college football",
            "Grain: final-season cross-section (last-ps)",
            "Y: drafted next NFL draft (season-Y on exit row)",
            "Peer X: teammate LOO index (full-roster pond)",
            "Panel: max(season) per player · transfer tie → role opportunities",
            "",
            "Reigning tag:",
            "q16_eligible_team_loo_draft_last_ps",
        ),
        panel_rows=PANEL_ROWS_LAST,
        athlete_id_col="player_id",
        tie_break_col="role_opportunities",
    ),
    "nels88": DomainSpec(
        key="nels88",
        prefix="NELS88",
        csv=REPO / "datasets/nels88/nels88_big_fish_panel.csv",
        sandbox="education_sandbox/nels88",
        title="NELS:88 data story — 10th-grade school pond",
        subtitle="analytic min-10 peers · baseline test z · school LOO  |  Read top-left → bottom-right",
        reigning_tag="q16_school_loo_ba2000",
        ai_col="own_performance_z",
        loo_col="peer_mean_z_loo",
        y_col="bachelors_or_higher_by_2000",
        pool_col="unit_n",
        team_keys=("school_id",),
        season_key="panel_wave",
        grain="student · 10th-grade school · sampled classmates (not full roster)",
        y_pos_label="BA or higher",
        y_neg_label="No BA",
        overlap_xlab=r"Baseline test composite ($z$)",
        cohort_lines=(
            "Domain: NELS:88 (NCES longitudinal)",
            "Grain: 10th-grade high-school snapshot",
            "Y: bachelor's or higher by 2000 (~age 26)",
            "Peer X: peer_mean_z_loo (Alex precomputed)",
            "Filter: analytic_sample_min10",
            "Note: attainment ≠ top-K selection (cf. draft/tenure)",
            "",
            "Reigning tag:",
            "q16_school_loo_ba2000",
        ),
    ),
    "hsb80_soph": DomainSpec(
        key="hsb80_soph",
        prefix="HSB80SOPH",
        csv=REPO / "datasets/hsb80/hsb80_big_fish_panel.csv",
        sandbox="education_sandbox/hsb80_soph",
        title="HS&B:80 data story — Sophomore school pond",
        subtitle="analytic min-5 peers · baseline test z · school LOO  |  Read top-left → bottom-right",
        reigning_tag="q16_soph_school_loo_ba1986",
        ai_col="own_performance_z",
        loo_col="peer_mean_z_loo",
        y_col="bachelors_or_higher_by_1986",
        pool_col="unit_n",
        team_keys=("school_id",),
        season_key="panel_wave",
        grain="student · 1980 Sophomore sample · school × cohort (not full roster)",
        y_pos_label="BA or higher",
        y_neg_label="No BA",
        overlap_xlab=r"Baseline test composite ($z$)",
        cohort_lines=(
            "Domain: HS&B:80 (NCES longitudinal)",
            "Grain: 1980 Sophomore high-school snapshot",
            "Y: bachelor's or higher by 1986 (~age 22; early for BA)",
            "Peer X: peer_mean_z_loo (Alex precomputed)",
            "Filter: analytic_sample_min5 · cohort=Sophomore",
            "Note: do not pool with Senior deck · attainment ≠ top-K selection",
            "",
            "Reigning tag:",
            "q16_soph_school_loo_ba1986",
        ),
    ),
    "hsb80_senior": DomainSpec(
        key="hsb80_senior",
        prefix="HSB80SEN",
        csv=REPO / "datasets/hsb80/hsb80_big_fish_panel.csv",
        sandbox="education_sandbox/hsb80_senior",
        title="HS&B:80 data story — Senior school pond",
        subtitle="analytic min-5 peers · baseline test z · school LOO  |  Read top-left → bottom-right",
        reigning_tag="q16_senior_school_loo_ba1986",
        ai_col="own_performance_z",
        loo_col="peer_mean_z_loo",
        y_col="bachelors_or_higher_by_1986",
        pool_col="unit_n",
        team_keys=("school_id",),
        season_key="panel_wave",
        grain="student · 1980 Senior sample · school × cohort (not full roster)",
        y_pos_label="BA or higher",
        y_neg_label="No BA",
        overlap_xlab=r"Baseline test composite ($z$)",
        cohort_lines=(
            "Domain: HS&B:80 (NCES longitudinal)",
            "Grain: 1980 Senior high-school snapshot",
            "Y: bachelor's or higher by 1986 (~age 22–24)",
            "Peer X: peer_mean_z_loo (Alex precomputed)",
            "Filter: analytic_sample_min5 · cohort=Senior",
            "Note: do not pool with Sophomore deck · attainment ≠ top-K selection",
            "",
            "Reigning tag:",
            "q16_senior_school_loo_ba1986",
        ),
    ),
}


def _with_positions(title: str, position_filter: PositionFilter | None) -> str:
    if position_filter is None:
        return title
    return f"{title} · {position_filter.label}"


def _paths(
    spec: DomainSpec,
    *,
    position_filter: PositionFilter | None = None,
    peer_axis: PeerAxis | None = None,
) -> dict[str, Path]:
    root = SANDBOX_ROOT / spec.sandbox
    if position_filter is not None:
        root = root / position_filter.slug
    if peer_axis is not None and peer_axis.path_suffix:
        root = root / peer_axis.path_suffix
    return {
        "root": root,
        "bdp": root / "basic_data_plots",
        "hero": root / "hero",
        "act2": root / "act2",
        "story": root / "data_story",
        "perf": root / "perf_story",
    }


def _summary(name: str, values: np.ndarray) -> dict[str, Any]:
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
    path.write_text(json.dumps(payload, indent=2) + "\n")


def _plot_ecdf(ax, values: np.ndarray, *, color: str, label: str, lw: float = 2.0, ls: str = "-") -> None:
    v = np.sort(np.asarray(values, dtype=float))
    v = v[np.isfinite(v)]
    if v.size == 0:
        return
    y = np.arange(1, v.size + 1) / v.size
    ax.plot(v, y, color=color, lw=lw, ls=ls, label=label)


def _winsorize_series(s: pd.Series, *, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    v = pd.to_numeric(s, errors="coerce")
    if v.notna().sum() < 10:
        return v
    return v.clip(v.quantile(lo), v.quantile(hi))


def _pg_season_z(series: pd.Series) -> pd.Series:
    """Alex-style: 1% winsorize then z within position_group × season group."""
    s = _winsorize_series(series)
    out = pd.Series(np.nan, index=s.index, dtype=float)
    mask = s.notna()
    if mask.sum() < 5:
        return out
    std = float(s[mask].std())
    if std <= 1e-9:
        return out
    out.loc[mask] = (s[mask] - s[mask].mean()) / std
    return out


def attach_football_diy_zscores(work: pd.DataFrame) -> pd.DataFrame:
    """Add DIY z columns for perf-metric story (exploratory v0)."""
    out = work.copy()
    if "position_group" not in out.columns or "season" not in out.columns:
        raise ValueError("football DIY z requires position_group and season")
    for raw, zcol in FOOTBALL_DIY_Z_SOURCES:
        if raw not in out.columns:
            continue
        out[zcol] = out.groupby(["position_group", "season"], observed=True)[raw].transform(_pg_season_z)
    return out


def _restrict_to_last_ps(work: pd.DataFrame, spec: DomainSpec) -> tuple[pd.DataFrame, dict[str, Any]]:
    """MBB-compatible final season: ``max(season)`` per athlete; transfer tie → tie-break col."""
    if spec.athlete_id_col is None:
        raise ValueError(f"{spec.key} last-ps requires athlete_id_col on DomainSpec")
    tmp = work.copy()
    tmp["athlete_id"] = pd.to_numeric(tmp[spec.athlete_id_col], errors="coerce")
    tie_col = spec.tie_break_col or "minutes"
    if tie_col not in tmp.columns:
        raise ValueError(f"{spec.key} last-ps tie-break column missing: {tie_col!r}")
    tmp["minutes"] = pd.to_numeric(tmp[tie_col], errors="coerce").fillna(-1.0)
    out, audit = restrict_to_last_season_rows(tmp)
    audit["panel_rows"] = spec.panel_rows
    audit["athlete_id_col"] = spec.athlete_id_col
    audit["tie_break_col"] = tie_col
    return out, audit


def _finalize_cohort(work: pd.DataFrame, spec: DomainSpec) -> pd.DataFrame:
    work = work.dropna(subset=[spec.ai_col, spec.loo_col]).copy()
    work["outcome"] = work[spec.y_col].astype(bool)
    work["outcome_label"] = np.where(work["outcome"], spec.y_pos_label, spec.y_neg_label)
    tj = (
        work.groupby(list(spec.team_keys), observed=True)[spec.ai_col]
        .transform("mean")
        .rename("team_mean_ai")
    )
    work["team_mean_ai"] = tj
    work["pool_id"] = work[list(spec.team_keys)].astype(str).agg("|".join, axis=1)
    return work


def _load_eligible_frame(spec: DomainSpec) -> pd.DataFrame:
    df = pd.read_csv(spec.csv, low_memory=False)
    if spec.key == "legends":
        m = (
            (df["league_tier"] == "developmental")
            & df["eligible_developmental_cohort"]
            & ~df["prior_top_tier_before_period"]
            & df["full_2y_followup"]
            & df["performance_components_available"]
        )
    elif spec.key == "nels88":
        m = df["analytic_sample_min10"] == 1
        out = df.loc[m].copy()
        out["panel_wave"] = 1988
        return out
    elif spec.key == "hsb80_soph":
        m = (df["analytic_sample_min5"] == 1) & (df["cohort"] == "Sophomore")
        out = df.loc[m].copy()
        out["panel_wave"] = 1980
        return out
    elif spec.key == "hsb80_senior":
        m = (df["analytic_sample_min5"] == 1) & (df["cohort"] == "Senior")
        out = df.loc[m].copy()
        out["panel_wave"] = 1980
        return out
    else:
        m = df["eligible_analysis_cohort"] == 1
    return df.loc[m].copy()


def _attach_position_loo(
    work: pd.DataFrame,
    spec: DomainSpec,
    position_filter: PositionFilter,
) -> pd.DataFrame:
    pool = position_filter.apply(_load_eligible_frame(spec))
    work = work.copy()
    work[spec.loo_col] = compute_team_loo(pool, spec.ai_col, spec.team_keys).reindex(work.index)
    return work


def load_cohort(
    spec: DomainSpec,
    *,
    for_loo_pool: bool = False,
    position_filter: PositionFilter | None = None,
) -> pd.DataFrame:
    work = _load_eligible_frame(spec)
    if position_filter is not None:
        work = position_filter.apply(work)
    if for_loo_pool:
        return work
    if spec.panel_rows == PANEL_ROWS_LAST:
        work, _audit = _restrict_to_last_ps(work, spec)
    if position_filter is not None:
        work = _attach_position_loo(work, spec, position_filter)
    return _finalize_cohort(work, spec)


def load_cohort_with_audit(
    spec: DomainSpec,
    *,
    position_filter: PositionFilter | None = None,
) -> tuple[pd.DataFrame, dict[str, Any] | None]:
    """Load analysis panel; return last-ps audit metadata when applicable."""
    work = _load_eligible_frame(spec)
    if position_filter is not None:
        work = position_filter.apply(work)
    audit: dict[str, Any] | None = None
    if spec.panel_rows == PANEL_ROWS_LAST:
        work, audit = _restrict_to_last_ps(work, spec)
        if audit is not None and position_filter is not None:
            audit = dict(audit)
            audit["position_groups"] = list(position_filter.groups)
    if position_filter is not None:
        work = _attach_position_loo(work, spec, position_filter)
    return _finalize_cohort(work, spec), audit


def run_ai_tj(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    position_filter: PositionFilter | None = None,
) -> Path:
    configure_matplotlib_mathtext()
    ai = work[spec.ai_col].to_numpy(dtype=float)
    tj = work["team_mean_ai"].to_numpy(dtype=float)
    sa, st = _summary("ai", ai), _summary("team_mean", tj)
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2))
    fig.subplots_adjust(wspace=0.22, top=0.82, bottom=0.14)
    for ax, vals, stats, xlab, title, color in (
        (axes[0], ai, sa, r"Own $\hat{A}$ — performance index", rf"Own ability ($n={sa['n']:,}$)", ECDF_COHORT),
        (axes[1], tj, st, r"Team $\hat{T}_j$ — mean index on stint", rf"Team talent ($n={st['n']:,}$)", ECDF_LOO_HIST),
    ):
        lo, hi = float(np.percentile(vals, 1)), float(np.percentile(vals, 99))
        pad = 0.05 * (hi - lo or 1.0)
        ax.hist(vals, bins=32, range=(lo - pad, hi + pad), color=color, edgecolor="white", alpha=0.88)
        ax.set_xlabel(xlab, fontsize=9)
        ax.set_ylabel("Rows", fontsize=9)
        ax.set_title(title, fontsize=10)
        ax.grid(axis="y", alpha=0.25)
    fig.suptitle(_with_positions(f"{spec.prefix} — own Â vs team T̂_j", position_filter), fontsize=11, fontweight="bold")
    fig.text(0.5, 0.02, spec.grain, ha="center", fontsize=8, color="0.35")
    out = paths["bdp"] / f"{spec.prefix}_BDP_Ai_Tj.png"
    fig.savefig(out, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    _write_meta(out.with_name(out.stem + "_meta.json"), {"diagnostic": "ai_tj", "date": date.today().isoformat(), "n": len(work)})
    print(f"Wrote {out.relative_to(REPO)}")
    return out


def run_loo_hist_ecdf(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    position_filter: PositionFilter | None = None,
) -> Path:
    configure_matplotlib_mathtext()
    loo = work[spec.loo_col].to_numpy(dtype=float)
    stats = _summary("loo", loo)
    lo, hi = float(loo.min()), float(loo.max())
    bins = np.linspace(lo, hi, 36)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    fig.subplots_adjust(wspace=0.28, top=0.84, bottom=0.16)
    axes[0].hist(loo, bins=bins, color=ECDF_LOO_HIST, alpha=0.85, edgecolor="white", linewidth=0.35)
    axes[0].axvline(stats["median"], color="0.35", linestyle=":", linewidth=1.4)
    axes[0].set_xlabel("Teammate LOO performance index (excl. self)", fontsize=10)
    axes[0].set_ylabel("Rows", fontsize=10)
    axes[0].set_title("Peer talent environment (team LOO)", fontsize=10)
    ax = axes[1]
    _plot_ecdf(ax, loo, color=ECDF_BASE, label=f"All ($n={len(loo):,}$)", lw=1.4, ls=":")
    for pos, color, ls in ((True, ECDF_POS, "-"), (False, ECDF_NEG, "--")):
        vals = work.loc[work["outcome"] == pos, spec.loo_col].to_numpy(dtype=float)
        lab = spec.y_pos_label if pos else spec.y_neg_label
        _plot_ecdf(ax, vals, color=color, label=f"{lab} ($n={len(vals):,}$)", lw=2.4, ls=ls)
    ax.axhline(0.5, color="0.82", linestyle=":", linewidth=0.9)
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel("Team LOO index")
    ax.set_ylabel(r"ECDF  $F(x)$")
    ax.set_title("ECDF by outcome", fontsize=10)
    ax.legend(fontsize=6, loc="lower right")
    fig.suptitle(
        _with_positions(f"{spec.prefix} — team LOO distribution (N={len(loo):,})", position_filter),
        fontsize=11,
        fontweight="bold",
    )
    out = paths["bdp"] / f"{spec.prefix}_team_loo_distribution.png"
    fig.savefig(out, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.relative_to(REPO)}")
    return out


def run_mass_ecdf(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    position_filter: PositionFilter | None = None,
) -> Path:
    configure_matplotlib_mathtext()
    ai = np.sort(work[spec.ai_col].to_numpy(dtype=float))
    pos = work.loc[work["outcome"], spec.ai_col].to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    _plot_ecdf(ax, ai, color=ECDF_COHORT, label=f"Cohort ($n={len(ai):,}$)", lw=2.4, ls="-")
    _plot_ecdf(ax, pos, color=ECDF_POS, label=f"{spec.y_pos_label} ($n={len(pos):,}$)", lw=2.4, ls="--")
    ax.axhline(0.5, color="0.82", linestyle=":", linewidth=0.9)
    ax.set_xlabel(r"Own $\hat{A}$ — performance index", fontsize=10)
    ax.set_ylabel(r"ECDF  $F(x)$")
    ax.set_title(
        _with_positions(f"{spec.prefix} — outcome mass vs own ability", position_filter),
        fontsize=11,
        fontweight="bold",
    )
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.25)
    out = paths["bdp"] / f"{spec.prefix}_outcome_mass_ecdf.png"
    fig.savefig(out, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.relative_to(REPO)}")
    return out


def _try_compute_h_sort(work: pd.DataFrame) -> float | None:
    try:
        return _compute_H_sort(work)
    except Exception as exc:
        print(f"  H_sort skipped: {exc}")
        return None


def run_overlap(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    position_filter: PositionFilter | None = None,
) -> Path:
    panel = work.copy()
    panel["team_id"] = panel["pool_id"]
    panel["season"] = panel[spec.season_key]
    z_keys = [spec.season_key]
    if position_filter is not None and "position_group" in panel.columns:
        z_keys = ["position_group", spec.season_key]
    panel["perf"] = panel.groupby(z_keys, observed=True)[spec.ai_col].transform(
        lambda s: (s - s.mean()) / (s.std() if s.std() > 1e-9 else 1.0)
    )
    iv, w = _team_intervals(panel)
    y0, y1 = int(panel[spec.season_key].min()), int(panel[spec.season_key].max())
    out = paths["bdp"] / f"{spec.prefix}_team_interval_overlap.png"
    out_csv = out.with_name(out.stem + "_team_season.csv")
    iv.to_csv(out_csv, index=False)

    h_sort = _try_compute_h_sort(w)
    base_title = _with_positions(f"{spec.prefix} — team interval overlap ({y0}-{y1})", position_filter)
    h_line = (
        f"\nRealized sorting $H_{{sort}}={h_sort:.3f}$ on this partition"
        if h_sort is not None and np.isfinite(h_sort)
        else ""
    )
    perf_note = (
        f"{spec.ai_col} z within position × season"
        if position_filter is not None
        else f"{spec.ai_col} z within season"
    )
    stats = build_figure(
        iv,
        w,
        png_path=out,
        seasons=f"{y0}-{y1}",
        h_sort=h_sort,
        suptitle=base_title + h_line,
        xlab=spec.overlap_xlab,
        labels={
            "coverage_ylabel": "Team stints covering this level",
            "span_ylabel": "Team stints",
            "span_xlabel": r"Roster span ($\max \hat{A} - \min \hat{A}$)",
        },
        grain_badge=spec.grain[:48],
    )
    _write_meta(
        out.with_name(out.stem + "_meta.json"),
        {
            "diagnostic": "team_interval_overlap",
            "date": date.today().isoformat(),
            "domain": spec.key,
            "perf": perf_note,
            "seasons": f"{y0}-{y1}",
            "position_groups": list(position_filter.groups) if position_filter else None,
            **stats,
            "outputs": {"png": out.name, "team_csv": out_csv.name},
        },
    )
    print(f"Wrote {out.relative_to(REPO)}")
    if h_sort is not None and np.isfinite(h_sort):
        print(f"  H_sort={h_sort:.3f}")
    return out


def run_pool_size(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    position_filter: PositionFilter | None = None,
) -> Path:
    configure_matplotlib_mathtext()
    vals = pd.to_numeric(work[spec.pool_col], errors="coerce").dropna().to_numpy(dtype=float)
    stats = _summary("pool", vals)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(vals, bins=30, color="steelblue", edgecolor="white", alpha=0.85)
    ax.set_xlabel("Team roster size on stint", fontsize=10)
    ax.set_ylabel("Rows", fontsize=10)
    ax.set_title(
        _with_positions(f"{spec.prefix} — pool size |T_j| (N={len(vals):,})", position_filter),
        fontsize=11,
        fontweight="bold",
    )
    ax.text(0.98, 0.98, f"median={stats['median']:.0f}", transform=ax.transAxes, ha="right", va="top", fontsize=9,
            bbox=dict(boxstyle="round", facecolor="white", alpha=0.85))
    out = paths["bdp"] / f"{spec.prefix}_pool_size.png"
    fig.savefig(out, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.relative_to(REPO)}")
    return out


def _equal_width_edges(values: np.ndarray, n_bins: int) -> np.ndarray:
    s = np.asarray(values, dtype=float)
    s = s[np.isfinite(s)]
    if s.size == 0:
        return np.linspace(0.0, 1.0, int(n_bins) + 1)
    lo, hi = float(s.min()), float(s.max())
    if hi <= lo:
        hi = lo + 1.0
    return np.linspace(lo, hi, int(n_bins) + 1)


def _bin_table_on(
    work: pd.DataFrame,
    spec: DomainSpec,
    x_col: str,
    *,
    n_bins: int = 16,
    binning: str = "quantile",
) -> pd.DataFrame:
    sub = work.dropna(subset=[x_col, spec.y_col]).copy()
    if str(binning).strip().lower() == "equal_width":
        edges = _equal_width_edges(sub[x_col].to_numpy(dtype=float), n_bins)
        sub["bin"] = pd.cut(sub[x_col], bins=edges, include_lowest=True)
    else:
        sub["bin"] = pd.qcut(sub[x_col], q=n_bins, duplicates="drop")
    rows = []
    for i, (_, g) in enumerate(sub.groupby("bin", observed=True), start=1):
        n = len(g)
        y = g[spec.y_col].astype(bool)
        rows.append({"bin": i, "x_mean": g[x_col].mean(), "n": n, "y_rate": y.mean() if n else np.nan})
    return pd.DataFrame(rows)


def compute_team_loo(work: pd.DataFrame, col: str, team_keys: tuple[str, ...]) -> pd.Series:
    """Teammate leave-one-out mean of ``col`` within pond keys."""
    v = pd.to_numeric(work[col], errors="coerce")
    keys = list(team_keys)
    gsum = v.groupby([work[k] for k in keys], observed=True).transform("sum")
    gcnt = v.notna().groupby([work[k] for k in keys], observed=True).transform("sum")
    loo = (gsum - v) / (gcnt - 1)
    loo[(gcnt <= 1) | ~v.notna()] = np.nan
    return loo


def metric_loo_column(
    work: pd.DataFrame,
    spec: DomainSpec,
    metric_col: str,
    *,
    loo_pool: pd.DataFrame | None = None,
    recompute_loo: bool = False,
) -> str:
    """Return temp column name with teammate LOO for ``metric_col``."""
    loo_col = f"_loo_{metric_col}"
    use_precomputed = (
        not recompute_loo
        and metric_col == spec.ai_col
        and spec.loo_col in work.columns
    )
    if use_precomputed:
        work[loo_col] = pd.to_numeric(work[spec.loo_col], errors="coerce")
    else:
        pool = loo_pool if loo_pool is not None else work
        loo_series = compute_team_loo(pool, metric_col, spec.team_keys)
        work[loo_col] = loo_series.reindex(work.index)
    return loo_col


def _bin_table(
    work: pd.DataFrame,
    spec: DomainSpec,
    *,
    n_bins: int = 16,
    peer_axis: PeerAxis | None = None,
    x_col: str | None = None,
) -> pd.DataFrame:
    axis = peer_axis or PeerAxis()
    col = x_col or axis.x_col(spec)
    return _bin_table_on(work, spec, col, n_bins=n_bins)


def run_hero_porch(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    n_bins: int = 16,
    binning: str = "quantile",
    x_col: str | None = None,
    x_label: str | None = None,
    slug: str | None = None,
    out_dir: Path | None = None,
    figsize: tuple[float, float] = (7.5, 4.5),
    position_filter: PositionFilter | None = None,
    peer_axis: PeerAxis | None = None,
) -> Path:
    configure_matplotlib_mathtext()
    axis = peer_axis or PeerAxis()
    x_col = x_col or axis.x_col(spec)
    is_ew = str(binning).strip().lower() == "equal_width"
    bin_tag = f"EW{n_bins}" if is_ew else f"Q{n_bins}"
    is_loo_x = x_col == spec.loo_col or str(x_col).startswith("_loo_")
    x_label = x_label or (
        axis.x_label(bin_tag=bin_tag)
        if x_col == axis.x_col(spec)
        else (f"Teammate LOO ({bin_tag})" if is_loo_x else f"{bin_tag} bins")
    )
    slug = slug or (f"{'ew' if is_ew else 'q'}{n_bins}_{axis.slug_part()}")
    table = _bin_table_on(work, spec, x_col, n_bins=n_bins, binning=binning)
    fig, ax = plt.subplots(figsize=figsize)
    x = table["bin"].to_numpy(dtype=float)
    y = table["y_rate"].to_numpy(dtype=float)
    n = table["n"].to_numpy(dtype=int)
    x_mean = table["x_mean"].to_numpy(dtype=float)
    if is_ew:
        bar_colors = count_weighted_bar_colors(n, cmap_name="Blues")
    else:
        bar_colors = ["steelblue"] * len(n)
    ax.bar(x, y, color=bar_colors, edgecolor="white", alpha=0.95, width=0.82)
    ax.set_xlabel(x_label, fontsize=10)
    ax.set_ylabel(f"P({spec.y_pos_label})", fontsize=10)
    title_x = slug.replace("_", " ").replace("perf ", "")
    ax.set_title(
        _with_positions(f"{spec.prefix} HERO — {title_x} ({bin_tag})", position_filter),
        fontsize=10,
        fontweight="bold",
    )
    ymax = float(np.max(y)) if len(y) else 0.05
    ax.set_ylim(0, min(1.0, max(0.05, ymax * 1.22)))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    if is_ew:
        annotate_bar_n(ax, x, y, n, bar_colors)
        ax.set_xticks(x)
        ax.set_xticklabels([format_poolq_tick(v) for v in x_mean], fontsize=6.5, rotation=50, ha="right")
    else:
        for xi, yi, ni in zip(x, y, n):
            ax.text(xi, yi + 0.01, str(ni), ha="center", va="bottom", fontsize=6, color="0.35")
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    hero_dir = out_dir or paths["hero"]
    hero_dir.mkdir(parents=True, exist_ok=True)
    out = hero_dir / f"HERO_{spec.key}_{slug}_slide.png"
    csv = hero_dir / f"HERO_{spec.key}_{slug}_binned.csv"
    table.to_csv(csv, index=False)
    fig.savefig(out, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.relative_to(REPO)}")
    return out


def run_legends_component_heroes(work: pd.DataFrame, spec: DomainSpec, paths: dict[str, Path]) -> list[Path]:
    """HERO porches for selected metrics — P(Y) vs teammate LOO on each component."""
    outs: list[Path] = []
    for col, label, modes in LEGENDS_HERO_COMPONENTS:
        loo_col = metric_loo_column(work, spec, col)
        sub = work.dropna(subset=[loo_col, spec.y_col]).copy()
        if sub.empty:
            print(f"Skip {col}: no LOO rows")
            continue
        short = col.replace("z_", "")
        for mode in modes:
            is_ew = mode == "equal_width"
            tag = "ew16" if is_ew else "q16"
            x_label = (
                f"Teammate LOO · {label} ({'EW16' if is_ew else 'Q16'})"
            )
            outs.append(
                run_hero_porch(
                    sub,
                    spec,
                    paths,
                    x_col=loo_col,
                    x_label=x_label,
                    slug=f"{tag}_loo_{col}",
                    binning=mode,
                )
            )
    return outs


def run_perf_metric_story(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    loo_pool: pd.DataFrame | None = None,
    panel_audit: dict[str, Any] | None = None,
    show_footer: bool = True,
    page_size: str = "screen",
    position_filter: PositionFilter | None = None,
) -> Path:
    """Q16 + EW16 HERO porch per metric: P(Y) vs teammate LOO on that metric."""
    metrics = DOMAIN_PERF_METRICS.get(spec.key)
    if not metrics:
        raise SystemExit(f"No perf metrics defined for domain {spec.key!r}")
    if spec.key == "football":
        work = attach_football_diy_zscores(work)
        if loo_pool is not None:
            loo_pool = attach_football_diy_zscores(loo_pool)
        for raw, zcol in FOOTBALL_DIY_Z_SOURCES:
            n = int(work[zcol].notna().sum()) if zcol in work.columns else 0
            print(json.dumps({"diy_z": zcol, "from": raw, "n": n}))
    configure_matplotlib_mathtext()
    panel_dir = paths["perf"] / "panels"
    panel_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    compact = (6.4, 3.6)
    recompute_loo = position_filter is not None

    for col, short, label in metrics:
        loo_col = metric_loo_column(
            work,
            spec,
            col,
            loo_pool=loo_pool,
            recompute_loo=recompute_loo,
        )
        sub = work.dropna(subset=[loo_col, spec.y_col]).copy()
        if sub.empty:
            print(f"Skip perf metric {col}: no LOO rows")
            continue
        metric_rows: dict[str, Any] = {
            "col": col,
            "loo_col": loo_col,
            "short": short,
            "label": label,
            "n": len(sub),
        }
        for mode in ("quantile", "equal_width"):
            is_ew = mode == "equal_width"
            tag = "ew16" if is_ew else "q16"
            bin_tag = "EW16" if is_ew else "Q16"
            x_label = f"Teammate LOO · {short} ({bin_tag})"
            out = run_hero_porch(
                sub,
                spec,
                paths,
                x_col=loo_col,
                x_label=x_label,
                slug=f"perf_{tag}_loo_{col}",
                binning=mode,
                out_dir=panel_dir,
                figsize=compact,
                position_filter=position_filter,
            )
            metric_rows[f"{tag}_png"] = str(out.relative_to(REPO))
        rows.append(metric_rows)

    out_png = paths["story"] / f"{spec.prefix}_PERF_METRIC_STORY.png"
    manifest_name = f"{spec.key}_perf_metric_story_manifest.json"
    if position_filter is not None:
        manifest_name = f"{spec.key}_perf_metric_story_{position_filter.slug}_manifest.json"
    manifest_path = paths["story"] / manifest_name
    rows_per_page = LEGENDS_PERF_ROWS_PER_PAGE if spec.key == "legends" else None
    perf_title = _with_positions(PERF_STORY_TITLES[spec.key], position_filter)
    built_pages = build_perf_metric_story_pages(
        rows,
        paths["story"],
        f"{spec.prefix}_PERF_METRIC_STORY",
        suptitle=perf_title,
        repo=REPO,
        show_footer=show_footer,
        page_size=page_size,
        footer_tag=f"{spec.prefix} perf metric story · big_fish_data_story.py",
        rows_per_page=rows_per_page,
    )
    manifest_path.write_text(
        json.dumps(
            {
                "domain": spec.key,
                "deck": "perf_metric_story",
                "title": perf_title,
                "panel_rows": spec.panel_rows,
                "position_groups": list(position_filter.groups) if position_filter else None,
                "panel_audit": panel_audit,
                "show_footer": show_footer,
                "page_size": page_size,
                "rows_per_page": rows_per_page,
                "n": len(work),
                "n_players": int(work[spec.athlete_id_col].nunique()) if spec.athlete_id_col else None,
                "y_rate": float(work[spec.y_col].mean()),
                "output_png": str(built_pages[0].relative_to(REPO)),
                "output_pages": [str(p.relative_to(REPO)) for p in built_pages],
                "panels_dir": str(panel_dir.relative_to(REPO)),
                "metrics": rows,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {manifest_path.relative_to(REPO)}")
    for p in built_pages:
        print(f"Wrote {p.relative_to(REPO)}")
    return built_pages[-1]


def _wilson(successes: int, n: int) -> tuple[float, float]:
    if n <= 0:
        return float("nan"), float("nan")
    p = successes / n
    z = 1.96
    z2 = z * z
    denom = 1 + z2 / n
    center = (p + z2 / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) / n + z2 / (4 * n * n))) / denom
    return max(0, center - margin), min(1, center + margin)


def run_cct_probe(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    position_filter: PositionFilter | None = None,
    peer_axis: PeerAxis | None = None,
) -> Path:
    configure_matplotlib_mathtext()
    axis = peer_axis or PeerAxis()
    z = (work[spec.ai_col] - work[spec.ai_col].mean()) / work[spec.ai_col].std()
    band = work.loc[(z >= 1.0) & (z <= 2.0)].copy()
    n_bins = 8
    table = _bin_table(band, spec, n_bins=n_bins, peer_axis=axis)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x = np.arange(len(table))
    rates = table["y_rate"].to_numpy(dtype=float)
    ns = table["n"].to_numpy(dtype=int)
    yerr = []
    for r, n in zip(rates, ns):
        s = int(round(r * n))
        lo, hi = _wilson(s, n)
        yerr.append([max(0, r - lo), max(0, hi - r)])
    yerr = np.array(yerr).T
    ax.errorbar(x, rates, yerr=yerr, fmt="o-", color="#2ecc71", capsize=3)
    ax.set_xticks(x)
    ax.set_ylabel(f"P({spec.y_pos_label})")
    peer_label = r"$\hat{T}_j$" if axis.use_team_mean else "LOO"
    ax.set_xlabel(f"{peer_label} bins (Â z∈[1,2], n={len(band)}, Q{n_bins})")
    ax.set_title(
        _with_positions(f"{spec.prefix} CCT probe — fixed Â band", position_filter),
        fontsize=10,
        fontweight="bold",
    )
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    suffix = "_tj" if axis.use_team_mean else ""
    out = paths["act2"] / f"CCT_{spec.key}_ai_z1_2_q{n_bins}{suffix}.png"
    fig.savefig(out, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.relative_to(REPO)}")
    return out


def run_elite_probe(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    *,
    position_filter: PositionFilter | None = None,
    peer_axis: PeerAxis | None = None,
) -> Path:
    configure_matplotlib_mathtext()
    axis = peer_axis or PeerAxis()
    cut = work[spec.ai_col].quantile(0.8)
    elite = work.loc[work[spec.ai_col] >= cut].copy()
    n_bins = 5
    table = _bin_table(elite, spec, n_bins=n_bins, peer_axis=axis)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    x = np.arange(len(table))
    rates = table["y_rate"].to_numpy(dtype=float)
    ax.plot(x, rates, "o-", color="#e67e22", linewidth=2)
    ax.set_xticks(x)
    ax.set_ylabel(f"P({spec.y_pos_label})")
    peer_label = r"$\hat{T}_j$" if axis.use_team_mean else "LOO"
    ax.set_xlabel(f"{peer_label} bins (top 20% Â, n={len(elite)}, {n_bins} bins)")
    title_peer = "T̂_j" if axis.use_team_mean else "LOO"
    ax.set_title(
        _with_positions(f"{spec.prefix} elite pond {title_peer} probe", position_filter),
        fontsize=10,
        fontweight="bold",
    )
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    suffix = "_tj" if axis.use_team_mean else "_loo"
    out = paths["act2"] / f"ELITE_{spec.key}_top20{suffix}_pw{n_bins}.png"
    fig.savefig(out, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out.relative_to(REPO)}")
    return out


def cohort_text_lines(
    work: pd.DataFrame,
    spec: DomainSpec,
    *,
    position_filter: PositionFilter | None = None,
    peer_axis: PeerAxis | None = None,
) -> list[str]:
    n = len(work)
    y_rate = work[spec.y_col].mean()
    axis = peer_axis or PeerAxis()
    lines = list(spec.cohort_lines)
    if position_filter is not None:
        lines = [f"Positions: {', '.join(position_filter.groups)}", *lines]
    peer_stat = (
        f"With T̂_j = {work['team_mean_ai'].notna().sum():,}"
        if axis.use_team_mean
        else f"With LOO = {work[spec.loo_col].notna().sum():,}"
    )
    stats = [
        f"N = {n:,}",
        f"{spec.y_pos_label} rate = {y_rate:.1%}",
        peer_stat,
    ]
    # Insert stats before reigning tag block (blank line before "Reigning tag:")
    try:
        idx = lines.index("Reigning tag:") - 1
    except ValueError:
        idx = len(lines)
    lines[idx:idx] = stats + [""]
    if spec.key == "legends":
        lines.extend(["Panels 7–8: scaled Act II", "(z∈[1,2] CCT · top 20% elite)"])
    elif spec.key in ("nels88", "hsb80_soph", "hsb80_senior"):
        act2_peer = "T̂_j bins" if axis.use_team_mean else "LOO bins"
        lines.extend(
            [
                "Panels 7–9: Act II + HERO (exploratory)",
                f"({act2_peer} · {y_rate:.0%} BA rate · not draft selection)",
            ]
        )
    else:
        act2_peer = "T̂_j bins" if axis.use_team_mean else "LOO bins"
        lines.extend(["Panels 7–9: scaled Act II + HERO", f"({act2_peer} · sparse Y · exploratory)"])
    return lines


def write_manifest(
    work: pd.DataFrame,
    spec: DomainSpec,
    paths: dict[str, Path],
    outputs: dict[str, str],
    *,
    page_size: str = "screen",
    position_filter: PositionFilter | None = None,
    peer_axis: PeerAxis | None = None,
) -> Path:
    axis = peer_axis or PeerAxis()
    rel = lambda p: str(Path(p).relative_to(REPO))
    peer_note = r"T̂_j bins (team mean incl. self)" if axis.use_team_mean else "LOO bins (excl. self)"
    hero_title = (
        "9 · HERO (Pass A · T̂_j bins)"
        if axis.use_team_mean
        else "9 · HERO (Pass A · LOO bins)"
    )
    grid = [
        {
            "type": "text",
            "title": "1 · Cohort",
            "lines": cohort_text_lines(
                work, spec, position_filter=position_filter, peer_axis=axis
            ),
        },
        {"type": "image", "title": "2 · Â_i and T̂_j", "path": rel(outputs["ai_tj"])},
        {"type": "image", "title": "3 · Team LOO distribution", "path": rel(outputs["loo"])},
        {"type": "image", "title": "4 · Outcome mass vs Â (ECDF)", "path": rel(outputs["mass"])},
        {"type": "image", "title": "5 · Team interval overlap", "path": rel(outputs["overlap"])},
        {"type": "image", "title": "6 · Team roster size |T_j|", "path": rel(outputs["pool"])},
        {"type": "image", "title": "7 · CCT — fixed Â z∈[1,2]", "path": rel(outputs["cct"]), "note": peer_note},
        {"type": "image", "title": "8 · Elite pond — top 20% Â", "path": rel(outputs["elite"]), "note": peer_note},
        {"type": "image", "title": hero_title, "path": rel(outputs["hero"])},
    ]
    manifest = {
        "domain": spec.key,
        "deck": "big_fish_data_story",
        "title": _with_positions(spec.title, position_filter),
        "subtitle": _with_positions(spec.subtitle, position_filter),
        "output_png": rel(paths["story"] / f"{spec.prefix}_DATA_STORY_3x3.png"),
        "page_size": page_size,
        "footer": f"{spec.prefix} Big Fish · big_fish_data_story.py",
        "grid": grid,
        "verdict": {
            "reigning_tag": spec.reigning_tag,
            "panel_rows": spec.panel_rows,
            "position_groups": list(position_filter.groups) if position_filter else None,
            "peer_axis": axis.key,
            "n": len(work),
            "y_rate": float(work[spec.y_col].mean()),
        },
    }
    manifest_name = f"{spec.key}_3x3_manifest.json"
    if position_filter is not None:
        manifest_name = f"{spec.key}_3x3_{position_filter.slug}_manifest.json"
    if axis.use_team_mean:
        manifest_name = manifest_name.replace("_manifest.json", "_tj_manifest.json")
    out = paths["story"] / manifest_name
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    return out


def run_mosaic(
    manifest: Path,
    *,
    show_footer: bool = True,
    page_size: str = "screen",
) -> Path:
    cmd = [
        sys.executable,
        str(REPO / "sports/scripts/build_data_story_mosaic.py"),
        "--manifest",
        str(manifest.relative_to(REPO)),
    ]
    if not show_footer:
        cmd.append("--no-footer")
    cmd.extend(["--page-size", page_size or "screen"])
    subprocess.run(cmd, cwd=REPO, check=True)
    spec = json.loads(manifest.read_text())
    return REPO / spec["output_png"]


def _manifest_path(
    spec: DomainSpec,
    paths: dict[str, Path],
    position_filter: PositionFilter | None,
    peer_axis: PeerAxis | None = None,
) -> Path:
    axis = peer_axis or PeerAxis()
    name = f"{spec.key}_3x3_manifest.json"
    if position_filter is not None:
        name = f"{spec.key}_3x3_{position_filter.slug}_manifest.json"
    if axis.use_team_mean:
        name = name.replace("_manifest.json", "_tj_manifest.json")
    return paths["story"] / name


def run_domain(
    spec: DomainSpec,
    *,
    mode: str,
    show_footer: bool = True,
    page_size: str = "screen",
    position_filter: PositionFilter | None = None,
    peer_axis: PeerAxis | None = None,
) -> None:
    if position_filter is not None and spec.key != "football":
        raise SystemExit("--positions / trailing POSITION args are football-only")
    axis = peer_axis or PeerAxis()
    paths = _paths(spec, position_filter=position_filter, peer_axis=axis)
    for d in paths.values():
        d.mkdir(parents=True, exist_ok=True)
    plot_kw = {"position_filter": position_filter}
    act2_kw = {**plot_kw, "peer_axis": axis}
    if mode == "mosaic":
        man = _manifest_path(spec, paths, position_filter, axis)
        if not man.is_file():
            raise SystemExit(f"Missing manifest: {man} — run --mode all first")
        run_mosaic(man, show_footer=show_footer, page_size=page_size)
        return
    if mode == "perf-story":
        if spec.key not in DOMAIN_PERF_METRICS:
            raise SystemExit(f"--mode perf-story not configured for {spec.key!r}")
        work, panel_audit = load_cohort_with_audit(spec, position_filter=position_filter)
        loo_pool = (
            load_cohort(spec, for_loo_pool=True, position_filter=position_filter)
            if spec.panel_rows == PANEL_ROWS_LAST
            else None
        )
        summary = {
            "domain": spec.key,
            "panel_rows": spec.panel_rows,
            "position_groups": list(position_filter.groups) if position_filter else None,
            "n": len(work),
            "y_rate": float(work[spec.y_col].mean()),
        }
        if panel_audit:
            summary["panel_audit"] = panel_audit
        print(json.dumps(summary, indent=2))
        run_perf_metric_story(
            work,
            spec,
            paths,
            loo_pool=loo_pool,
            panel_audit=panel_audit,
            show_footer=show_footer,
            page_size=page_size,
            position_filter=position_filter,
        )
        return
    work, panel_audit = load_cohort_with_audit(spec, position_filter=position_filter)
    summary = {
        "domain": spec.key,
        "panel_rows": spec.panel_rows,
        "position_groups": list(position_filter.groups) if position_filter else None,
        "peer_axis": axis.key,
        "n": len(work),
        "y_rate": float(work[spec.y_col].mean()),
    }
    if panel_audit:
        summary["panel_audit"] = panel_audit
    print(json.dumps(summary, indent=2))
    outputs: dict[str, str] = {}
    if mode in ("all", "bdp"):
        outputs["ai_tj"] = str(run_ai_tj(work, spec, paths, **plot_kw))
        outputs["loo"] = str(run_loo_hist_ecdf(work, spec, paths, **plot_kw))
        outputs["mass"] = str(run_mass_ecdf(work, spec, paths, **plot_kw))
        outputs["overlap"] = str(run_overlap(work, spec, paths, **plot_kw))
        outputs["pool"] = str(run_pool_size(work, spec, paths, **plot_kw))
    if mode in ("all", "hero"):
        outputs["hero"] = str(run_hero_porch(work, spec, paths, **act2_kw))
        if spec.key == "legends":
            run_legends_component_heroes(work, spec, paths)
    if mode in ("all", "act2"):
        outputs["cct"] = str(run_cct_probe(work, spec, paths, **act2_kw))
        outputs["elite"] = str(run_elite_probe(work, spec, paths, **act2_kw))
    if mode == "all":
        man = write_manifest(
            work,
            spec,
            paths,
            outputs,
            page_size=page_size,
            position_filter=position_filter,
            peer_axis=axis,
        )
        run_mosaic(man, show_footer=show_footer, page_size=page_size)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Big Fish 3×3 data story (legends / football / nels88 / hsb80_soph / hsb80_senior)"
    )
    parser.add_argument("--domain", choices=sorted(DOMAINS), required=True)
    parser.add_argument("--mode", choices=("all", "bdp", "hero", "act2", "mosaic", "perf-story"), default="all")
    parser.add_argument(
        "--no-footer",
        action="store_true",
        help="Omit bottom-left footer on STORY mosaic PNGs (better for Preview print)",
    )
    parser.add_argument(
        "--page-size",
        choices=MOSAIC_PAGE_SIZE_CHOICES,
        default="screen",
        help="3×3 mosaic: letter-landscape (recommended handout). Perf-story maps landscape→portrait.",
    )
    parser.add_argument(
        "--positions",
        nargs="+",
        metavar="POSITION",
        default=None,
        help=(
            "Football only: filter to position_group values "
            f"({', '.join(FOOTBALL_POSITION_GROUPS)}). "
            "LOO is recomputed among teammates in these groups."
        ),
    )
    parser.add_argument(
        "positions_tail",
        nargs="*",
        metavar="POSITION",
        help="Same as --positions; may trail the command (e.g. ... --mode hero QB RB_FB).",
    )
    parser.add_argument(
        "--team-mean",
        action="store_true",
        help=(
            "Panels 7–9 only: bin on team T̂_j (mean index incl. self) instead of teammate LOO. "
            "Outputs under peer_tj/ (does not overwrite LOO decks)."
        ),
    )
    args = parser.parse_args()
    position_tokens = args.positions or args.positions_tail or None
    position_filter = PositionFilter.parse(position_tokens)
    if position_filter is not None and args.domain != "football":
        raise SystemExit("--positions / trailing POSITION args are football-only")
    peer_axis = PeerAxis.from_flag(args.team_mean)
    run_domain(
        DOMAINS[args.domain],
        mode=args.mode,
        show_footer=not args.no_footer,
        page_size=args.page_size,
        position_filter=position_filter,
        peer_axis=peer_axis,
    )


if __name__ == "__main__":
    main()
