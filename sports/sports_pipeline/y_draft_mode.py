"""``Y_draft`` labeling and panel-row scope for Pass A / CCT plots.

Two **orthogonal** CLI knobs (do not conflate):

1. **``--y-draft-mode``** — how ``Y_draft`` is assigned:
   - ``ever``: panel-rebuild default; draftee rows carry ``Y=1`` per ever-draft rule.
   - ``season``: ``apply_y_draft_last_season`` — draftees get ``Y=1`` on **last college PS
     only**; earlier seasons stay in the panel with ``Y=0``.

2. **``--panel-rows``** — which rows enter the plot panel:
   - ``all-ps`` (default): every player-season passing filters (fr/soph/jr/sr/…).
   - ``last-ps``: ``restrict_to_last_season_rows`` — one row per athlete at ``max(season)``.

Common pairs:

| panel-rows | y-draft-mode | Estimand |
|------------|--------------|----------|
| all-ps | ever | Canonical HERO (full panel, ever-draft) |
| all-ps | season | Full panel; ``Y=1`` only on each draftee's last PS |
| last-ps | ever | Final-season cross-section; ever-draft label on that row |
| last-ps | season | Final-season cross-section; ``Y=1`` only if drafted |

For ``season`` labeling, call ``apply_y_draft_last_season`` on a **pre-min-minutes,
pre-min-games** panel, then apply analysis filters and ``audit_y1_survival`` after
each step that can drop labeled draftees.
"""

from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any

import pandas as pd

from sports_pipeline import paths

Y_DRAFT_RULE_LAST_COLLEGE_PREMIN = "last_college_season_v1_premin"
Y_DRAFT_MODES = frozenset({"ever", "season"})
PANEL_ROWS_ALL = "all-ps"
PANEL_ROWS_LAST = "last-ps"
PANEL_ROWS_MODES = frozenset({PANEL_ROWS_ALL, PANEL_ROWS_LAST})

_last_survival_audit: list[dict[str, Any]] | None = None


def normalize_y_draft_mode(mode: str) -> str:
    m = str(mode).strip().lower()
    if m not in Y_DRAFT_MODES:
        raise ValueError(f"y_draft_mode must be one of {sorted(Y_DRAFT_MODES)!r}, got {mode!r}")
    return m


def normalize_panel_rows(mode: str) -> str:
    m = str(mode).strip().lower().replace("_", "-")
    aliases = {
        "all": PANEL_ROWS_ALL,
        "allps": PANEL_ROWS_ALL,
        "last": PANEL_ROWS_LAST,
        "lastps": PANEL_ROWS_LAST,
    }
    m = aliases.get(m, m)
    if m not in PANEL_ROWS_MODES:
        raise ValueError(
            f"panel_rows must be one of {sorted(PANEL_ROWS_MODES)!r}, got {mode!r}"
        )
    return m


def panel_rows_is_last_only(panel_rows: str) -> bool:
    return normalize_panel_rows(panel_rows) == PANEL_ROWS_LAST


def resolve_panel_rows_from_args(args: object) -> str:
    """Resolve ``--panel-rows``; map retired ``--last-season-only`` / ``--all-seasons``."""
    panel_rows = getattr(args, "panel_rows", None)
    last_season_only = bool(getattr(args, "last_season_only", False))
    all_seasons = bool(getattr(args, "all_seasons", False))

    if last_season_only and all_seasons:
        raise SystemExit("Use only one of --last-season-only and --all-seasons (prefer --panel-rows).")

    legacy_used = last_season_only or all_seasons
    if panel_rows is not None and legacy_used:
        raise SystemExit(
            "Use --panel-rows only; --last-season-only and --all-seasons are retired."
        )

    if last_season_only:
        warnings.warn(
            "--last-season-only is retired; use --panel-rows last-ps",
            DeprecationWarning,
            stacklevel=2,
        )
        return PANEL_ROWS_LAST
    if all_seasons:
        warnings.warn(
            "--all-seasons is retired; use --panel-rows all-ps (the default)",
            DeprecationWarning,
            stacklevel=2,
        )
        return PANEL_ROWS_ALL

    if panel_rows is None:
        return PANEL_ROWS_ALL
    return normalize_panel_rows(str(panel_rows))


def load_draft_lookup() -> pd.DataFrame:
    lu_path = paths.draft_lookup_csv()
    if not lu_path.is_file():
        raise FileNotFoundError(f"Missing draft lookup {lu_path}")
    lu = pd.read_csv(lu_path, low_memory=False)
    if "athlete_id" not in lu.columns:
        raise ValueError(f"Draft lookup must have athlete_id: {lu_path}")
    lu = lu.copy()
    lu["athlete_id"] = pd.to_numeric(lu["athlete_id"], errors="coerce")
    lu = lu.dropna(subset=["athlete_id"])
    lu["athlete_id"] = lu["athlete_id"].astype(int)
    return lu.drop_duplicates(subset=["athlete_id"], keep="first")


def apply_y_draft_last_season(
    panel: pd.DataFrame,
    lookup: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """One ``Y_draft=1`` per lookup draftee on ``max(season)`` (pre-min panel only).

    Transfer tie at max season: row with largest ``minutes``.
    """
    if lookup is None:
        lookup = load_draft_lookup()
    out = panel.copy()
    drafted_ids = set(lookup["athlete_id"].astype(int))
    n_lookup = int(len(drafted_ids))

    out["athlete_id"] = pd.to_numeric(out["athlete_id"], errors="coerce")
    out = out.dropna(subset=["athlete_id"])
    out["athlete_id"] = out["athlete_id"].astype(int)

    in_panel = drafted_ids & set(out["athlete_id"].unique())
    n_in_panel = int(len(in_panel))
    not_in_panel = sorted(drafted_ids - in_panel)

    out["Y_draft"] = 0
    sub = out.loc[out["athlete_id"].isin(in_panel)].copy()
    if sub.empty:
        audit = {
            "step": "label_last_season",
            "y_draft_rule": Y_DRAFT_RULE_LAST_COLLEGE_PREMIN,
            "n_lookup_draftees": n_lookup,
            "n_draftees_in_panel": n_in_panel,
            "n_draftees_labeled": 0,
            "n_y1_rows": 0,
            "n_not_in_panel": len(not_in_panel),
            "n_transfer_ties": 0,
            "not_in_panel_sample": not_in_panel[:20],
        }
        return out, audit

    sub["_season"] = pd.to_numeric(sub["season"], errors="coerce")
    max_season = sub.groupby("athlete_id", observed=True)["_season"].transform("max")
    at_last = sub.loc[sub["_season"] == max_season].copy()
    if "minutes" not in at_last.columns:
        raise ValueError("Panel missing minutes column — required for transfer tie-break")
    at_last["_minutes"] = pd.to_numeric(at_last["minutes"], errors="coerce").fillna(-1.0)
    tie_counts = at_last.groupby("athlete_id", observed=True).size()
    n_transfer_ties = int((tie_counts > 1).sum())
    pick = (
        at_last.sort_values(["athlete_id", "_minutes"], ascending=[True, False])
        .drop_duplicates(subset=["athlete_id"], keep="first")
    )
    out.loc[pick.index, "Y_draft"] = 1

    n_labeled = int(out.groupby("athlete_id", observed=True)["Y_draft"].max().sum())
    audit = {
        "step": "label_last_season",
        "y_draft_rule": Y_DRAFT_RULE_LAST_COLLEGE_PREMIN,
        "n_lookup_draftees": n_lookup,
        "n_draftees_in_panel": n_in_panel,
        "n_draftees_labeled": n_labeled,
        "n_y1_rows": int((out["Y_draft"] == 1).sum()),
        "n_not_in_panel": len(not_in_panel),
        "n_transfer_ties": n_transfer_ties,
        "not_in_panel_sample": not_in_panel[:20],
    }
    return out, audit


def restrict_to_last_season_rows(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    """One row per ``athlete_id``: ``max(season)``; transfer tie → max ``minutes``."""
    if "athlete_id" not in panel.columns or "season" not in panel.columns:
        raise ValueError("restrict_to_last_season_rows requires athlete_id and season")
    work = panel.copy()
    work["athlete_id"] = pd.to_numeric(work["athlete_id"], errors="coerce")
    work = work.dropna(subset=["athlete_id", "season"])
    work["athlete_id"] = work["athlete_id"].astype(int)
    work["_season"] = pd.to_numeric(work["season"], errors="coerce")
    max_season = work.groupby("athlete_id", observed=True)["_season"].transform("max")
    at_last = work.loc[work["_season"] == max_season].copy()
    if "minutes" not in at_last.columns:
        raise ValueError("Panel missing minutes column — required for transfer tie-break")
    at_last["_minutes"] = pd.to_numeric(at_last["minutes"], errors="coerce").fillna(-1.0)
    pick = (
        at_last.sort_values(["athlete_id", "_minutes"], ascending=[True, False])
        .drop_duplicates(subset=["athlete_id"], keep="first")
    )
    out = panel.loc[pick.index].copy()
    audit = {
        "step": "last_season_only",
        "n_rows_before": int(len(panel)),
        "n_rows_after": int(len(out)),
        "n_athletes": int(pick["athlete_id"].nunique()),
        "n_transfer_ties": int((at_last.groupby("athlete_id", observed=True).size() > 1).sum()),
    }
    return out, audit


def filter_team_seasons_min_games(panel: pd.DataFrame, min_g: int) -> pd.DataFrame:
    """Drop ``(team_id, season)`` with ``games_rostered <= min_g`` (matches rebuild QC)."""
    mg = int(min_g)
    if mg <= 0:
        return panel
    if "games_rostered" not in panel.columns:
        raise ValueError("filter_team_seasons_min_games requires games_rostered on panel")
    ts = panel.groupby(["team_id", "season"], observed=True)["games_rostered"].max()
    keep = ts[ts > mg].reset_index()[["team_id", "season"]]
    return panel.merge(keep, on=["team_id", "season"], how="inner")


def _y1_athlete_ids(panel: pd.DataFrame) -> set[int]:
    if "Y_draft" not in panel.columns or "athlete_id" not in panel.columns:
        return set()
    y = pd.to_numeric(panel["Y_draft"], errors="coerce").fillna(0).astype(int)
    ids = pd.to_numeric(panel.loc[y == 1, "athlete_id"], errors="coerce").dropna().astype(int)
    return set(ids.tolist())


def audit_y1_survival(
    before: pd.DataFrame,
    after: pd.DataFrame,
    step: str,
    *,
    max_log_ids: int = 25,
) -> dict[str, Any]:
    """Compare draftee athlete_ids with ``Y_draft=1`` before vs after a filter step."""
    ids_before = _y1_athlete_ids(before)
    ids_after = _y1_athlete_ids(after)
    lost = sorted(ids_before - ids_after)
    audit = {
        "step": step,
        "n_draftees_y1_before": len(ids_before),
        "n_draftees_y1_after": len(ids_after),
        "n_draftees_lost": len(lost),
        "lost_athlete_ids": lost[:max_log_ids],
        "lost_athlete_ids_truncated": len(lost) > max_log_ids,
    }
    if lost:
        msg = (
            f"Y_draft survival alarm [{step}]: {len(lost)} draftee(s) lost their Y=1 row "
            f"({len(ids_before)} → {len(ids_after)}). "
            f"Sample athlete_id: {lost[:5]}"
        )
        warnings.warn(msg, UserWarning, stacklevel=2)
        print(f"ALARM · {msg}", flush=True)
    return audit


def emit_survival_summary(audits: list[dict[str, Any]]) -> None:
    """Print one-line summary after a season-``Y`` panel build."""
    label = next((a for a in audits if a.get("step") == "label_last_season"), None)
    if label:
        print(
            f"Season-Y label · lookup={label['n_lookup_draftees']} · "
            f"in_panel={label['n_draftees_in_panel']} · "
            f"labeled={label['n_draftees_labeled']} · Y=1 rows={label['n_y1_rows']}",
            flush=True,
        )
    drops = [a for a in audits if int(a.get("n_draftees_lost", 0)) > 0]
    if not drops:
        print("Season-Y survival · no draftees dropped by min-games / min-minutes / +DFT filters", flush=True)
        return
    for a in drops:
        print(
            f"ALARM · [{a['step']}] lost {a['n_draftees_lost']} draftee(s): "
            f"{a['n_draftees_y1_before']} → {a['n_draftees_y1_after']}",
            flush=True,
        )


def set_last_survival_audit(audits: list[dict[str, Any]] | None) -> None:
    global _last_survival_audit
    _last_survival_audit = None if audits is None else list(audits)


def get_last_survival_audit() -> list[dict[str, Any]] | None:
    return _last_survival_audit


def assert_season_y_output_path(path: Path | str, y_draft_mode: str) -> None:
    """Refuse to write season-``Y`` artifacts outside an experiment path."""
    if normalize_y_draft_mode(y_draft_mode) != "season":
        return
    s = str(path).replace("\\", "/")
    if "season_y" not in s:
        raise ValueError(
            f"season y_draft_mode requires output path containing 'season_y' (got {path!r})"
        )


def season_y_output_dir(base: Path) -> Path:
    return base / "season_y_experiment"
