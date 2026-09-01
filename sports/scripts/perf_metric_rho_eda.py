#!/usr/bin/env python3
"""Disposable EDA — empirical H_sort (and optional ρ calibration) across perf metrics.

All outputs go under ``population_sandbox/_DISPOSABLE_perf_metric_rho_eda/``.
Delete that folder to discard this exploration without touching reigning-hero artifacts.

Run (repo root):
  python sports/scripts/perf_metric_rho_eda.py
  python sports/scripts/perf_metric_rho_eda.py --metrics ppm fg_pct efg_pct per bpm
  python sports/scripts/perf_metric_rho_eda.py --run-rho --rho-quick
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import subprocess
import sys
from datetime import date
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import (
    PERF_METRIC_RHO_EDA,
    PERF_METRIC_RHO_EDA_H_SORT,
    PERF_METRIC_RHO_EDA_RHO,
    ensure_hero_dirs,
)
from pd21_rho_hsort_calibrate import PanelPrepConfig, empirical_h_sort, prepare_calibration_panel
from sports_pipeline.perf_metric import resolve_perf_metric

DEFAULT_SPEC = dict(season_min=2009, season_max=2021, min_minutes=20.0)
DEFAULT_METRICS = (
    "ppm",
    "fg_pct",
    "efg_pct",
    "ts_pct_box",
    "per",
    "bpm",
    "tspct",
    "ws",
    "minutes",
)

# Human-readable glossary for the ladder report (key → fields).
# ``components`` = list of "SYMBOL — definition" strings rendered as bullets.
METRIC_GLOSSARY: dict[str, dict[str, str | list[str]]] = {
    "ppm": {
        "name": "Points per minute (PPM)",
        "measures": "Scoring output per unit of playing time.",
        "source": "ESPN box (`mbb_df_player_box.csv`), aggregated to player-season in `panel_rebuild`.",
        "formula": r"$\mathrm{PPM} = \dfrac{\sum \mathrm{PTS}}{\sum \mathrm{MIN}}$",
        "components": [
            "**Points (PTS)** — total points scored (field goals + free throws); summed across all games in the season.",
            "**Minutes (MIN)** — playing time; summed across all games in the season.",
        ],
        "aggregation": "Sum PTS and MIN at game level, then divide. Rows with MIN = 0 get missing PPM.",
        "notes": "Not a pure skill rate: high PPM can reflect role (usage), efficiency, or garbage-time minutes. Sensitive to roster congestion (fewer minutes on deep teams).",
    },
    "minutes": {
        "name": "Season minutes (MIN)",
        "measures": "Total playing time — opportunity, not efficiency.",
        "source": "ESPN box, player-season sum.",
        "formula": r"$\mathrm{MIN} = \sum_{\mathrm{games}} \mathrm{minutes}$",
        "components": [
            "**minutes** — per-game playing time from ESPN box score (not stints or possessions).",
        ],
        "aggregation": "Sum across all games for `(athlete_id, season, team_id)`.",
        "notes": "Lowest sorting index (H_sort) in the ladder: minutes are allocated by role/coach within team, so cross-team sorting is weak on this scale alone.",
    },
    "fg_pct": {
        "name": "Field-goal percentage (FG%)",
        "measures": "Share of field-goal attempts that score (two-pointers and three-pointers combined).",
        "source": "ESPN box, season totals.",
        "formula": r"$\mathrm{FG\%} = \dfrac{\mathrm{FGM}}{\mathrm{FGA}}$",
        "components": [
            "**Field goals made (FGM)** — baskets from inside the arc or beyond the three-point line.",
            "**Field-goal attempts (FGA)** — shot attempts that count as field goals (includes two-pointers and three-pointers; excludes free throws).",
        ],
        "aggregation": "Sum FGM and FGA across games, then divide. Requires FGA > 0.",
        "notes": "Conditional on getting attempts; does not penalize low usage. No minutes in denominator.",
    },
    "efg_pct": {
        "name": "Effective field-goal percentage (eFG%)",
        "measures": "Field-goal accuracy with three-pointers weighted 1.5× (one three = one and a half two-pointers).",
        "source": "ESPN box, season totals.",
        "formula": r"$\mathrm{eFG\%} = \dfrac{\mathrm{FGM} + 0.5 \times \mathrm{3PM}}{\mathrm{FGA}}$",
        "components": [
            "**Field goals made (FGM)** — all field goals made (two-pointers + three-pointers).",
            "**Three-pointers made (3PM)** — baskets from beyond the three-point arc only.",
            "**Field-goal attempts (FGA)** — all field goal attempts.",
            "The **0.5 × 3PM** term adds half a made field goal for each three beyond what field goals made (FGM) already counts (since FGM includes 3PM).",
        ],
        "aggregation": "Sum FGM, 3PM, FGA across games, then apply formula. Requires FGA > 0.",
        "notes": "Standard “shooting efficiency” rate; still attempt-conditional like field-goal percentage (FG%).",
    },
    "ts_pct_box": {
        "name": "True shooting percentage (TS%), box-built",
        "measures": "Points scored per scoring attempt, where attempts combine field goals and free throws on one scale.",
        "source": "ESPN box (`ts_pct_box` column in panel); same definition as Sports-Reference (SR) true shooting percentage (TS%) but built from ESPN season totals.",
        "formula": r"$\mathrm{TS\%} = \dfrac{\mathrm{PTS}}{2 \times (\mathrm{FGA} + 0.44 \times \mathrm{FTA})}$",
        "components": [
            "**Points (PTS)** — total points (two-pointers ×2 + three-pointers ×3 + free throws made (FTM) ×1).",
            "**Field-goal attempts (FGA)** — field goal attempts.",
            "**Free-throw attempts (FTA)** — free throw attempts.",
            "**Denominator** `2 × (FGA + 0.44 × FTA)` — “true shooting attempts”: each field-goal attempt counts as one possession ending in a shot; each free-throw attempt counts as 0.44 of a possession (standard Dean Oliver factor reflecting and-ones and shooting fouls).",
            "**Factor 2** — converts the attempt scale to points-per-shot equivalent (max per field-goal attempt is 2 points on a two-point make before threes).",
        ],
        "aggregation": "Sum PTS, FGA, FTA across games; compute TS%. Requires positive denominator.",
        "notes": "Panel key `ts_pct_box`; distinct from Sports-Reference (SR) merge column `ts_pct_sr` (`tspct` perf key). Full 2009–21 box coverage.",
    },
    "tspct": {
        "name": "True shooting percentage (TS%), Sports-Reference",
        "measures": "Same construct as box TS%: scoring efficiency per true shooting attempt.",
        "source": "Sports-Reference advanced table → `bpm_player_season_matched.csv` column `ts_pct_sr`; perf key `tspct`.",
        "formula": r"$\mathrm{TS\%} = \dfrac{\mathrm{PTS}}{2 \times (\mathrm{FGA} + 0.44 \times \mathrm{FTA})}$",
        "components": [
            "**Points (PTS), field-goal attempts (FGA), free-throw attempts (FTA)** — Sports-Reference (SR) season totals for the player on that team (from SR’s advanced page, not re-derived here).",
            "**0.44 × FTA** — same free-throw possession weight as standard true shooting percentage (TS%) (Dean Oliver / basketball-reference convention).",
            "Sports-Reference (SR) may round or compute from slightly different possession accounting than ESPN box totals; expect small drift vs `ts_pct_box`.",
        ],
        "aggregation": "Taken as published on SR; merged onto panel by name + team-season.",
        "notes": "Strong sorting index (H_sort) vs points per minute (PPM); ~2009+ in raw scrape. Same *definition* as box true shooting percentage (TS%), different *source* totals.",
    },
    "per": {
        "name": "Player efficiency rating (PER)",
        "measures": "John Hollinger’s pace-adjusted summary of per-minute box production, league-normalized so 15 ≈ average.",
        "source": "Sports-Reference advanced merge (`PER` column).",
        "formula": r"$\mathrm{PER} = f(\mathrm{MIN}, \mathrm{PTS}, \mathrm{FGM}, \mathrm{FGA}, \mathrm{FTM}, \mathrm{FTA}, \mathrm{REB}, \mathrm{AST}, \mathrm{STL}, \mathrm{BLK}, \mathrm{TOV}, \ldots)$",
        "components": [
            "**Inputs** — counting stats per minute (points, field goals, rebounds, assists, etc.), adjusted for team pace and league context.",
            "**Pace adjustment** — rewards production in fewer possessions (fast-paced teams don’t inflate raw counting stats).",
            "**League normalization** — scaled so league average ≈ 15 each season (not comparable raw across eras without z-scoring).",
            "**Not transparent in our pipeline** — we ingest Sports-Reference (SR) published player efficiency rating (PER), not re-implement Hollinger’s formula.",
        ],
        "aggregation": "SR season value merged by player match; ~2010+ non-null in matched file (2009 sparse).",
        "notes": "Model-based composite; mixes scoring, playmaking, and rebounding. Not purely a shooting rate.",
    },
    "bpm": {
        "name": "Box plus/minus (BPM)",
        "measures": "Estimated net team point differential per 100 possessions attributable to the player (offense + defense), from a regression on box stats.",
        "source": "Sports-Reference advanced merge (`BPM`, `OBPM`, `DBPM`).",
        "formula": r"$\mathrm{BPM} = \mathrm{OBPM} + \mathrm{DBPM}$",
        "components": [
            "**Offensive box plus/minus (OBPM)** — estimated offensive contribution per 100 possessions from box stats (scoring, shooting efficiency, playmaking, etc.).",
            "**Defensive box plus/minus (DBPM)** — estimated defensive contribution per 100 possessions.",
            "**Per 100 possessions** — box plus/minus (BPM) is *not* per minute; it is pace-normalized via Sports-Reference (SR) possession model.",
            "**Regression-based** — coefficients fit so that player box plus/minus (BPM) values sum (with minutes weights) to team efficiency vs league; not a simple rate stat.",
            "**Coverage** — Sports-Reference (SR) publishes box plus/minus (BPM) reliably ~2011+; 2009–10 largely missing in our matched file.",
        ],
        "aggregation": "SR season value merged by player match.",
        "notes": "Highest sorting index (H_sort) in ladder; strong team clustering. Distinct from points per minute (PPM) (no minutes denominator in the same way; possession-based estimate).",
    },
    "ws": {
        "name": "Win shares (WS)",
        "measures": "Estimated number of team wins credited to the player’s offense and defense for the season.",
        "source": "Sports-Reference advanced merge (`WS`; also `OWS`, `DWS` in raw scrape).",
        "formula": r"$\mathrm{WS} = \mathrm{OWS} + \mathrm{DWS}$",
        "components": [
            "**Offensive win shares (OWS)** — offensive contribution to wins (scoring, creation, efficiency).",
            "**Defensive win shares (DWS)** — defensive contribution to wins.",
            "**Team constraint** — player win shares (WS) on a team sum to roughly team wins (allocation problem across roster).",
            "**Not a rate** — season total; high-minute stars accumulate more win shares (WS) by construction.",
        ],
        "aggregation": "SR season value merged by player match.",
        "notes": "Team-context composite; sorting index (H_sort) ~2.5× points per minute (PPM). Related to box plus/minus (BPM) family but in wins units not points/100.",
    },
}


# Master acronym table: full name + definition. Report places this **before** any standalone acronym use.
ACRONYM_REFERENCE: list[tuple[str, str, str]] = [
    ("2PT", "Two-point field goal", "Basket scored from inside the three-point arc (counts as one field goal made)."),
    ("3PA", "Three-point attempts", "Shot attempts from beyond the three-point arc."),
    ("3PM", "Three-pointers made", "Baskets scored from beyond the three-point arc."),
    ("AST", "Assists", "Passes that directly lead to a teammate’s made field goal."),
    ("BLK", "Blocks", "Defensive deflection of an opponent shot attempt."),
    ("BPM", "Box plus/minus", "Estimated net team point differential per 100 possessions attributable to the player (offense + defense), from a box-score regression."),
    ("DBPM", "Defensive box plus/minus", "Defensive component of box plus/minus (BPM): estimated defensive impact per 100 possessions."),
    ("DWS", "Defensive win shares", "Estimated share of team wins due to the player’s defense."),
    ("eFG%", "Effective field-goal percentage", "Field-goal accuracy with three-pointers weighted 1.5× vs two-pointers."),
    ("ESPN box", "ESPN play-by-player box scores", "Game-level counting stats in `mbb_df_player_box.csv` (our primary box source)."),
    ("FG%", "Field-goal percentage", "Share of field-goal attempts that result in a made basket."),
    ("FGA", "Field-goal attempts", "Two-point and three-point shot attempts (excludes free throws)."),
    ("FGM", "Field goals made", "Made baskets from the field (includes both two-pointers and three-pointers)."),
    ("FTA", "Free-throw attempts", "Uncontested shots from the free-throw line after a foul."),
    ("FTM", "Free throws made", "Made free throws."),
    ("FT", "Free throw", "Uncontested shot worth one point from the foul line."),
    ("H_sort", "Sorting index", "Fraction of cross-player variance in z-scored performance explained by team assignment (realized homophily)."),
    ("LOO", "Leave-one-out", "Teammate pool quality computed excluding the focal player."),
    ("LG", "League generator", "Grandchild assignment simulation used to calibrate homophily (ρ)."),
    ("MIN", "Minutes", "Playing time (sum of game minutes in a season)."),
    ("OBPM", "Offensive box plus/minus", "Offensive component of box plus/minus (BPM): estimated offensive impact per 100 possessions."),
    ("OWS", "Offensive win shares", "Estimated share of team wins due to the player’s offense."),
    ("PER", "Player efficiency rating", "Pace-adjusted per-minute production index (league average ≈ 15)."),
    ("PPM", "Points per minute", "Total season points divided by total season minutes."),
    ("PTS", "Points", "Total points scored (field goals + free throws)."),
    ("ρ", "Homophily (rho)", "Grandchild assignment parameter calibrated so simulated sorting index matches empirical H_sort."),
    ("REB", "Rebounds", "Offensive + defensive rebounds."),
    ("SR", "Sports-Reference", "Third-party site; advanced stats scraped into `bpm_player_season_matched.csv`."),
    ("STL", "Steals", "Defensive takeaways of the ball from the opponent."),
    ("TOV", "Turnovers", "Lost possessions (bad passes, steals against, violations, etc.)."),
    ("TS%", "True shooting percentage", "Points scored per true shooting attempt (field goals + free throws on one scale)."),
    ("WS", "Win shares", "Estimated number of team wins credited to the player (offense + defense)."),
]


def _acronym_reference_lines() -> list[str]:
    lines = [
        "## Acronym and stat reference",
        "",
        "**Read this table first.** Every acronym below is defined here before it appears alone in the rest of this report.",
        "",
        "| Acronym | Full name | Definition |",
        "|---------|-----------|------------|",
    ]
    for acro, full, defn in ACRONYM_REFERENCE:
        lines.append(f"| **{acro}** | {full} | {defn} |")
    lines.extend(
        [
            "",
            "**ESPN column map** (box stats summed to player-season before rate stats):",
            "",
            "| Acronym | ESPN `mbb_df_player_box` column |",
            "|---------|----------------------------------|",
            "| Points (PTS) | `points` |",
            "| Minutes (MIN) | `minutes` |",
            "| Field goals made (FGM) | `field_goals_made` |",
            "| Field-goal attempts (FGA) | `field_goals_attempted` |",
            "| Three-pointers made (3PM) | `three_point_field_goals_made` |",
            "| Three-point attempts (3PA) | `three_point_field_goals_attempted` |",
            "| Free throws made (FTM) | `free_throws_made` |",
            "| Free-throw attempts (FTA) | `free_throws_attempted` |",
            "",
            "**Note:** Field goals made (FGM) includes three-pointers made (3PM). Two-point makes = FGM − 3PM.",
            "",
        ]
    )
    return lines


def write_ladder_report(
    summary: pd.DataFrame,
    cfg: PanelPrepConfig,
    *,
    out_path: Path | None = None,
) -> Path:
    """Markdown report: metric glossary + H_sort ladder results."""
    out = out_path or (PERF_METRIC_RHO_EDA / "H_SORT_LADDER_REPORT.md")
    out.parent.mkdir(parents=True, exist_ok=True)

    df = summary.sort_values("H_sort_pooled", ascending=False).copy()
    ppm_h = float(df.loc[df["perf_metric"] == "ppm", "H_sort_pooled"].iloc[0]) if (df["perf_metric"] == "ppm").any() else float("nan")
    df["H_sort_vs_ppm"] = df["H_sort_pooled"] / ppm_h if ppm_h > 0 else float("nan")

    lines: list[str] = [
        "# Sorting index (H_sort) ladder — performance-metric comparison (disposable EDA)",
        "",
        f"**Generated:** {date.today().isoformat()}  ",
        "**Folder:** `_DISPOSABLE_perf_metric_rho_eda/` — safe to delete without affecting reigning-hero work.",
        "",
    ]
    lines.extend(_acronym_reference_lines())
    lines.extend(
        [
        "## Question",
        "",
        "Does near-zero homophily (ρ) on **points per minute (PPM)** reflect weak men's college basketball assortativity, "
        "or a performance measure that washes out team sorting (congestion / minutes / role noise)? "
        "Compare empirical **sorting index (H_sort)** across candidate performance (`perf`) measures.",
        "",
        "## Aperture (this run)",
        "",
        f"| Setting | Value |",
        f"|---------|-------|",
        f"| Seasons | {cfg.season_min}–{cfg.season_max} |",
        f"| Min minutes | {cfg.min_minutes:g} |",
        f"| Min team-season games | 10 (mg10) |",
        f"| Panel rows | all player-seasons (all-ps) |",
        f"| `perf` transform | within-season z-score |",
        f"| Pool quality | leave-one-out (LOO) teammate mean on same `perf` |",
        "",
        "## Sorting index (H_sort)",
        "",
        "**Sorting index (H_sort)** = fraction of cross-player variance in z-scored `perf` explained by team assignment "
        "(Grandchild realized sorting index). Higher → players on the same team look more alike on that metric.",
        "",
        "PD21 calibrates league-generator (LG) **homophily (ρ)** so simulated sorting index (H_sort) matches the "
        "empirical target. Low sorting index (H_sort) on points per minute (PPM) → estimated ρ̂ ≈ 0.",
        "",
        "## Results (pooled 2009–2021)",
        "",
        "Perf keys match `perf_metric` codes; full metric names and formulas are in **Per-metric definitions** below.",
        "",
        "| Rank | Key | H_sort (pooled) | vs PPM | N rows |",
        "|------|-----|-----------------|--------|--------|",
        ]
    )
    for rank, row in enumerate(df.itertuples(index=False), start=1):
        lines.append(
            f"| {rank} | `{row.perf_metric}` | {row.H_sort_pooled:.4f} | "
            f"{row.H_sort_vs_ppm:.2f}× | {int(row.n_panel_rows):,} |"
        )

    lines.extend(
        [
            "",
            f"Per-season CSVs: `h_sort/Hsort_{{metric}}_mg10_min20_{cfg.season_min}_{cfg.season_max}_by_season.csv`",
            "",
            "## Metric glossary — per-metric definitions",
            "",
            "Acronyms are defined in **Acronym and stat reference** above. Formulas use standard notation; "
            "each section spells out the performance measure name once, then uses its key.",
            "",
            "### Per-metric definitions",
            "",
        ]
    )
    for key in df["perf_metric"]:
        g = METRIC_GLOSSARY.get(key, {})
        lines.extend(
            [
                f"### `{key}` — {g.get('name', key)}",
                "",
                f"**What it measures:** {g.get('measures', '—')}",
                "",
                f"**Source:** {g.get('source', '—')}",
                "",
                f"**Formula:** {g.get('formula', '—')}",
                "",
            ]
        )
        comps = g.get("components") or []
        if comps:
            lines.append("**Components:**")
            lines.append("")
            for c in comps:
                lines.append(f"- {c}")
            lines.append("")
        if g.get("aggregation"):
            lines.append(f"**In this pipeline:** {g['aggregation']}")
            lines.append("")
        if g.get("notes"):
            lines.append(f"**Notes:** {g['notes']}")
            lines.append("")

    if (df["perf_metric"] == "ppm").any():
        bpm_ratio = (
            float(df.loc[df["perf_metric"] == "bpm", "H_sort_vs_ppm"].iloc[0])
            if (df["perf_metric"] == "bpm").any()
            else float("nan")
        )
        bpm_line = (
            f"- **Box plus/minus (BPM)** sorting index (H_sort) ≈ **{bpm_ratio:.1f}×** points per minute (PPM) — "
            "strongest team sorting here (2011+ coverage only)."
            if math.isfinite(bpm_ratio)
            else "- **Box plus/minus (BPM)** — highest sorting index (H_sort) in ladder (2011+ coverage only)."
        )
        lines.extend(
            [
                "## What the sorting-index (H_sort) ladder tells you — and does not",
                "",
                f"- **Points per minute (PPM)** sorting index (H_sort) = {ppm_h:.4f} — among the lowest.",
                "- **Minutes (MIN)** lower still → opportunity alone barely clusters by team.",
                "- **Field-goal percentage (FG%)**, **effective field-goal percentage (eFG%)**, and "
                "**true shooting percentage (TS%)** sit ~**1.5–2×** points per minute (PPM).",
                bpm_line,
                "- **Higher sorting index (H_sort)** only means players on the same team look more alike on that axis → "
                "helps **homophily (ρ) / league-generator (LG) assign** identification.",
                "- **It does not** automatically buy a better **advancement** story (draft rate vs leave-one-out pool quality).",
                "- High-sorting metrics can make **ability (Â) vs pool quality (poolq_LOO)** *more* monotone: "
                "team sorting and teammate context move together → boring positive slope, less room for crowding / inverted-U.",
                "",
                "## Promotion gate (COMPASS — what actually matters)",
                "",
                "Do **not** promote a performance metric on sorting index (H_sort) alone.",
                "",
                "Alternate `perf` is valuable only if it **breaks the naive monotone** readout on outcome vs "
                "leave-one-out pool quality (poolq_LOO) on the **reigning hero porch** (09–21 · last-ps · EW16 · min20 · mg10).",
                "",
                "| Check | Pass if… |",
                "|-------|----------|",
                "| **P(Y=1) vs poolq_LOO** (EW16, last-ps) | Not strictly monotone ↑; visible peak or tail drop |",
                "| **Linear probability model (LPM) β₂** on poolq_LOO | Negative / clearly concave (not ≈ 0) |",
                "| **Â vs poolq_LOO** marginal | Optional — expect positive corr on most metrics; don't use alone |",
                "",
                "**Points per minute (PPM) baseline (reigning, locked):** LPM β₂ ≈ +0.0017 → flat / not concave; "
                "shape tags “robust tail drop,” not a clean inverted-U. Sim can still show inverted-U at reigning λ, t — "
                "generative model has curvature; empirical points per minute (PPM) does not show it cleanly in the hero bin plot.",
                "",
                "## Honest prior (before LOO-shape batch)",
                "",
                "| Metric type | Sorting index (H_sort) | Likely Â vs poolq_LOO / draft vs poolq_LOO |",
                "|-------------|------------------------|---------------------------------------------|",
                "| Points per minute (PPM), minutes | Low | Monotone / flat (opportunity + congestion) |",
                "| True shooting % (TS%), field-goal % (FG%), effective FG% (eFG%) | ~2× PPM | Maybe slightly less monotone; still skeptical |",
                "| Box plus/minus (BPM), player efficiency rating (PER), win shares (WS) | High | More team-aligned → often *more* monotone, not less |",
                "",
                "Box plus/minus (BPM) helping homophily (ρ) while **worsening** hero geometry is a real possibility. "
                "A metric fork (BPM for assign, PPM for advancement) is a heavy lift unless one metric clearly wins the LOO-shape test.",
                "",
                "## Campaign status (this thread)",
                "",
                "- **Homophily (ρ) ≈ 0 on points per minute (PPM)** — keep locked for reigning men's college basketball.",
                "- **γ, λ, t + Pass B** — proceed; that's where fitting still has bite.",
                "- **This ladder** — necessary context for assign (ρ); **not sufficient** to switch the hero metric.",
                "",
                "## LOO-shape batch (built)",
                "",
                "Ran `python3 sports/scripts/perf_metric_loo_shape_batch.py` — see `loo_shape/LOO_SHAPE_REPORT.md`.",
                "",
                "**Headline:** PPM **marginal** (flat β₂); BPM/PER/WS **fail** (convex β₂); no hero-metric switch.",
                "",
            ]
        )

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(REPO)}", flush=True)
    return out


def _load_gc():
    return importlib.import_module("541_grandchild_homophily_assign")


def pooled_h_sort(panel: pd.DataFrame) -> float:
    gc = _load_gc()
    work = panel.dropna(subset=["perf", "team_id"]).copy()
    work["perf"] = pd.to_numeric(work["perf"], errors="coerce")
    work = work.dropna(subset=["perf"])
    pool_id = work.groupby(["team_id", "season"], observed=True).ngroup().to_numpy(dtype="int64")
    return float(gc.realized_sorting_index_H_sort(work["perf"].to_numpy(dtype=float), pool_id))


def season_h_sort_table(panel: pd.DataFrame, season_min: int, season_max: int) -> pd.DataFrame:
    rows: list[dict] = []
    for season in range(int(season_min), int(season_max) + 1):
        sub = panel.loc[panel["season"] == season]
        if sub.empty:
            continue
        rows.append(
            {
                "season": season,
                "n_rows": int(len(sub)),
                "H_sort": empirical_h_sort(sub),
            }
        )
    return pd.DataFrame(rows)


def prepare_panel(perf_metric: str, cfg: PanelPrepConfig) -> pd.DataFrame:
    resolve_perf_metric(perf_metric)
    return prepare_calibration_panel(cfg, perf_metric=perf_metric)


def run_h_sort_ladder(
    metrics: list[str],
    cfg: PanelPrepConfig,
    out_dir: Path,
) -> pd.DataFrame:
    out_dir.mkdir(parents=True, exist_ok=True)
    summary_rows: list[dict] = []

    for metric in metrics:
        print(f"\n=== H_sort · {metric} ===", flush=True)
        panel = prepare_panel(metric, cfg)
        n_valid = int(panel["perf"].notna().sum()) if "perf" in panel.columns else 0
        h_pooled = pooled_h_sort(panel)
        by_season = season_h_sort_table(panel, cfg.season_min, cfg.season_max)
        stem = f"Hsort_{metric}_mg10_min20_{cfg.season_min}_{cfg.season_max}"
        by_season.to_csv(out_dir / f"{stem}_by_season.csv", index=False)
        meta = {
            "perf_metric": metric,
            "date": date.today().isoformat(),
            "panel_mode": cfg.describe(),
            "n_panel_rows": int(len(panel)),
            "n_valid_perf": n_valid,
            "H_sort_pooled": h_pooled,
        }
        (out_dir / f"{stem}.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        print(f"  rows={len(panel):,} valid perf={n_valid:,} H_sort_pooled={h_pooled:.4f}", flush=True)
        summary_rows.append(
            {
                "perf_metric": metric,
                "n_panel_rows": len(panel),
                "n_valid_perf": n_valid,
                "H_sort_pooled": h_pooled,
                "H_sort_mean_by_season": float(by_season["H_sort"].mean()) if len(by_season) else float("nan"),
            }
        )

    summary = pd.DataFrame(summary_rows).sort_values("H_sort_pooled", ascending=False)
    summary_path = out_dir / f"Hsort_ladder_summary_{cfg.season_min}_{cfg.season_max}.csv"
    summary.to_csv(summary_path, index=False)
    print(f"\nWrote {summary_path.relative_to(REPO)}", flush=True)
    return summary


def run_rho_for_metrics(
    metrics: list[str],
    cfg: PanelPrepConfig,
    *,
    rho_quick: bool,
    n_seeds: int,
    n_jobs: int,
) -> None:
    rho_root = PERF_METRIC_RHO_EDA_RHO
    rho_root.mkdir(parents=True, exist_ok=True)
    pd21 = SCRIPTS / "pd21_rho_hsort_calibrate.py"
    for metric in metrics:
        out_dir = rho_root / metric
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = f"EDA_PD21_rho_{metric}_mg10_min20_{cfg.season_min}_{cfg.season_max}"
        cmd = [
            sys.executable,
            str(pd21),
            "--perf-metric",
            metric,
            "--season-min",
            str(cfg.season_min),
            "--season-max",
            str(cfg.season_max),
            "--min-minutes",
            str(cfg.min_minutes),
            "--out-dir",
            str(out_dir),
            "--output-stem",
            stem,
            "--fresh",
            "--n-seeds",
            str(n_seeds),
            "--n-jobs",
            str(n_jobs),
        ]
        if rho_quick:
            cmd.append("--quick")
        print(f"\n=== ρ calibration · {metric} ===", flush=True)
        print(" ".join(cmd), flush=True)
        subprocess.run(cmd, cwd=str(REPO), check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Perf-metric homophily EDA (disposable sandbox outputs).")
    parser.add_argument(
        "--metrics",
        nargs="+",
        default=list(DEFAULT_METRICS),
        help=f"Perf keys to compare (default: {' '.join(DEFAULT_METRICS)})",
    )
    parser.add_argument("--season-min", type=int, default=DEFAULT_SPEC["season_min"])
    parser.add_argument("--season-max", type=int, default=DEFAULT_SPEC["season_max"])
    parser.add_argument("--min-minutes", type=float, default=DEFAULT_SPEC["min_minutes"])
    parser.add_argument(
        "--run-rho",
        action="store_true",
        help="Also run PD21 ρ bracket/grid calibrations per metric (slow)",
    )
    parser.add_argument(
        "--rho-quick",
        action="store_true",
        help="With --run-rho: 2015 only, 8 seeds (smoke test)",
    )
    parser.add_argument("--n-seeds", type=int, default=50)
    parser.add_argument("--n-jobs", type=int, default=8)
    args = parser.parse_args()

    ensure_hero_dirs()
    cfg = PanelPrepConfig.from_args(
        min_minutes=float(args.min_minutes),
        ppm_zero_below_minutes=None,
        season_min=int(args.season_min),
        season_max=int(args.season_max),
    )

    readme = PERF_METRIC_RHO_EDA / "README.md"
    if not readme.is_file():
        readme.write_text(
            "# Disposable perf-metric × ρ/H_sort EDA\n\n"
            "Delete this entire `_DISPOSABLE_perf_metric_rho_eda/` folder to discard "
            "all exploration outputs. Reigning-hero and canonical PD21 paths are untouched.\n",
            encoding="utf-8",
        )

    metrics = [str(m).strip().lower() for m in args.metrics]
    summary = run_h_sort_ladder(metrics, cfg, PERF_METRIC_RHO_EDA_H_SORT)

    manifest = {
        "date": date.today().isoformat(),
        "spec": {"season_min": cfg.season_min, "season_max": cfg.season_max, "min_minutes": cfg.min_minutes},
        "metrics": metrics,
        "H_sort_ladder": summary.to_dict(orient="records"),
        "outputs_root": str(PERF_METRIC_RHO_EDA.relative_to(REPO)),
    }
    manifest_path = PERF_METRIC_RHO_EDA / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {manifest_path.relative_to(REPO)}", flush=True)

    write_ladder_report(summary, cfg)

    if args.run_rho:
        run_rho_for_metrics(
            metrics,
            cfg,
            rho_quick=bool(args.rho_quick),
            n_seeds=int(args.n_seeds),
            n_jobs=int(args.n_jobs),
        )


if __name__ == "__main__":
    main()
