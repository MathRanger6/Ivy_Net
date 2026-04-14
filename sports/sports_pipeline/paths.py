"""
Filesystem layout for the college MBB pipeline.

- **`mbb/`** — working / regenerable CSVs (panel exports, draft diagnostics, …).
- **`mbb/DO_NOT_ERASE/`** — long-lived inputs: aliases, SR scrape/match, draft register
  copies, etc. (see `datasets/mbb/DO_NOT_ERASE/README.txt`).

All functions return absolute `Path` objects anchored at the repo root (the directory
that contains `datasets/` and `sports_pipeline/`).
"""

from __future__ import annotations

from pathlib import Path

# This file lives at repo_root/sports_pipeline/paths.py → parents[1] == repo root.
_REPO_ROOT = Path(__file__).resolve().parents[1]


def project_root() -> Path:
    """Repository root (contains `datasets/mbb/`)."""
    return _REPO_ROOT


def mbb_dir() -> Path:
    """`datasets/mbb` — default location for panel + working artifacts."""
    return project_root() / "datasets" / "mbb"


def durable_mbb_dir() -> Path:
    """`datasets/mbb/DO_NOT_ERASE` — do not bulk-delete; SR + alias equity lives here."""
    return mbb_dir() / "DO_NOT_ERASE"


def player_box_csv() -> Path:
    return mbb_dir() / "mbb_df_player_box.csv"


def team_box_csv() -> Path:
    return mbb_dir() / "mbb_df_team_box.csv"


def draft_lookup_csv() -> Path:
    return mbb_dir() / "athlete_id_draft_lookup.csv"


def panel_530_csv() -> Path:
    return mbb_dir() / "player_season_panel_530.csv"


def bpm_matched_csv() -> Path:
    return durable_mbb_dir() / "bpm_player_season_matched.csv"


def bpm_raw_csv() -> Path:
    return durable_mbb_dir() / "bpm_player_season_raw.csv"


def bpm_scrape_jobs_csv() -> Path:
    """Slug×season backlog from merge notebook (`bpm_merge_to_530`)."""
    return mbb_dir() / "bpm_scrape_jobs.csv"


def bpm_scrape_skip_pairs_csv() -> Path:
    """Persistent (school_slug, sr_year) pairs that returned HTTP 403 — skipped on later runs."""
    return mbb_dir() / "bpm_scrape_skip_pairs.csv"


def bpm_panel_rows_unmatched_csv() -> Path:
    """Panel rows with no SR BPM match (QA: names, slugs)."""
    return mbb_dir() / "bpm_panel_rows_unmatched.csv"


def sr_school_slug_aliases_csv() -> Path:
    """Panel slug → SR URL slug; 404 slugs append here for manual `sr_slug` fill-in."""
    return durable_mbb_dir() / "sr_school_slug_aliases.csv"


def sr_crosswalk_csv() -> Path:
    return durable_mbb_dir() / "sr_school_slug_crosswalk.csv"


def college_aliases_csv() -> Path:
    return durable_mbb_dir() / "college_aliases.csv"


def draft_athlete_match_csv() -> Path:
    return mbb_dir() / "draft_athlete_match.csv"


def nbaplayersdraft_csv() -> Path:
    return durable_mbb_dir() / "nbaplayersdraft.csv"


def draft_match_diagnostic_summary_csv() -> Path:
    return mbb_dir() / "draft_match_diagnostic_summary.csv"


def draft_unmapped_colleges_csv() -> Path:
    """Colleges from the draft register that did not map to ESPN (QA from draft-match stage)."""
    return mbb_dir() / "draft_unmapped_colleges.csv"
