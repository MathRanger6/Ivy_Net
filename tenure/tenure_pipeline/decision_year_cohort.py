"""Decision-year cohort — resolved assistant exits joined to career master (Alex Â).

One row per faculty_id at last assistant year (exit cross-section):
  • Resolved only: tenure or attrition (includes off_tenure_track / OTT)
  • Excludes: censored, transferred, exclude_from_metrics
  • No default filter on asst_time (optional diagnostic band via CLI)
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterator

PRIMARY_TIERS = frozenset({"HIGH", "MEDIUM"})

# Alex expected decision band — tracked in stats, not an inclusion filter
REFERENCE_ASST_TIME_MIN = 5
REFERENCE_ASST_TIME_MAX = 6


def load_career_lookup(path: Path) -> dict[tuple[str, int], dict[str, Any]]:
    """(faculty_id, year) -> career master row."""
    out: dict[tuple[str, int], dict[str, Any]] = {}
    if not path.is_file():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            fid = r.get("faculty_id")
            yr = r.get("year")
            if fid and yr is not None:
                out[(str(fid), int(yr))] = r
    return out


def load_panel_by_person(
    panel_path: Path,
    *,
    tiers: frozenset[str] = PRIMARY_TIERS,
) -> dict[str, list[dict[str, Any]]]:
    by_person: dict[str, list[dict[str, Any]]] = defaultdict(list)
    with panel_path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("match_confidence") not in tiers:
                continue
            if not r.get("ever_assistant"):
                continue
            if r.get("transferred") or r.get("exclude_from_metrics"):
                continue
            fid = r.get("faculty_id")
            if fid:
                by_person[str(fid)].append(r)
    return by_person


def _decision_row(asst_rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Assistant row at last_asst_year (exit cross-section)."""
    if not asst_rows:
        return None
    asst_rows = sorted(asst_rows, key=lambda r: int(r["year"]))
    last_asst = asst_rows[-1].get("last_asst_year")
    if last_asst is not None:
        for r in asst_rows:
            if int(r["year"]) == int(last_asst):
                return r
    return asst_rows[-1]


def _is_resolved(row: dict[str, Any]) -> bool:
    if row.get("transferred") or row.get("exclude_from_metrics"):
        return False
    tenure = bool(row.get("tenure_event"))
    attrition = bool(row.get("attrition"))
    return tenure or attrition


def _asst_time_from_row(row: dict[str, Any]) -> int | None:
    """asst_time at decision row; fall back to legacy field if needed."""
    raw = row.get("asst_time")
    if raw is None:
        raw = row.get("years_as_asst_so_far")
    if raw is None:
        return None
    return int(raw)


def _record_from_row(
    fid: str,
    row: dict[str, Any],
    career: dict[tuple[str, int], dict[str, Any]],
) -> dict[str, Any]:
    dy = int(row["year"])
    c = career.get((fid, dy), {})
    pubs_year = row.get("pubs_year")
    try:
        pubs_year_f = float(pubs_year) if pubs_year is not None else None
    except (TypeError, ValueError):
        pubs_year_f = None

    asst_time = _asst_time_from_row(row)
    return {
        "faculty_id": fid,
        "name_display": row.get("name_display"),
        "uni_slug": row.get("uni_slug"),
        "match_confidence": row.get("match_confidence"),
        "decision_year": dy,
        "asst_time": asst_time,
        "last_asst_year": row.get("last_asst_year"),
        "tenure_event": bool(row.get("tenure_event")),
        "attrition": bool(row.get("attrition")),
        "off_tenure_track": bool(row.get("off_tenure_track")),
        "ott_year": row.get("ott_year"),
        "ott_rank": row.get("ott_rank"),
        "pubs_year": pubs_year_f,
        "pubs_cumulative": row.get("pubs_cumulative"),
        "poolq_loo_mean": row.get("poolq_loo_mean"),
        "openalex_id": row.get("openalex_id"),
        "first_pub_year": c.get("first_pub_year"),
        "cum_works": c.get("cum_works"),
        "career_age_years": c.get("career_age_years"),
        "pubs_per_career_year": c.get("pubs_per_career_year"),
    }


def iter_resolved_exit_records(
    panel_path: Path,
    *,
    tiers: frozenset[str] = PRIMARY_TIERS,
) -> Iterator[dict[str, Any]]:
    """All resolved persons at last assistant year (no asst_time filter)."""
    by_person = load_panel_by_person(panel_path, tiers=tiers)
    for fid, rows in by_person.items():
        asst = [r for r in rows if r.get("rank") == "assistant"]
        row = _decision_row(asst)
        if row is None or not _is_resolved(row):
            continue
        rec = _record_from_row(fid, row, {})
        yield rec


def build_decision_cohort_records(
    panel_path: Path,
    career_path: Path,
    *,
    tiers: frozenset[str] = PRIMARY_TIERS,
    asst_time_min: int | None = None,
    asst_time_max: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Decision cohort: all resolved (tenure or attrition), last assistant year row.

    Optional asst_time_min/max for diagnostic slices only — default includes all
    resolved assistant-time values.
    """
    career = load_career_lookup(career_path)
    by_person = load_panel_by_person(panel_path, tiers=tiers)

    asst_time_hist: Counter[int] = Counter()
    records: list[dict[str, Any]] = []

    for fid, rows in by_person.items():
        asst = [r for r in rows if r.get("rank") == "assistant"]
        row = _decision_row(asst)
        if row is None or not _is_resolved(row):
            continue

        asst_time = _asst_time_from_row(row)
        if asst_time is None:
            continue

        asst_time_hist[asst_time] += 1

        if asst_time_min is not None and asst_time < asst_time_min:
            continue
        if asst_time_max is not None and asst_time > asst_time_max:
            continue

        records.append(_record_from_row(fid, row, career))

    n_all = sum(asst_time_hist.values())
    n_ref = sum(
        c for t, c in asst_time_hist.items()
        if REFERENCE_ASST_TIME_MIN <= t <= REFERENCE_ASST_TIME_MAX
    )

    stats: dict[str, Any] = {
        "n_resolved_all_asst_time": n_all,
        "asst_time_histogram": dict(sorted(asst_time_hist.items())),
        "n_cohort": len(records),
        "n_with_career_rate": sum(1 for r in records if r.get("pubs_per_career_year") is not None),
        "n_tenure": sum(1 for r in records if r["tenure_event"]),
        "n_attrition": sum(1 for r in records if r["attrition"]),
        "n_off_tenure_track": sum(1 for r in records if r.get("off_tenure_track")),
        "reference_asst_time_band": [REFERENCE_ASST_TIME_MIN, REFERENCE_ASST_TIME_MAX],
        "n_in_reference_band": n_ref,
        "pct_in_reference_band": round(100 * n_ref / n_all, 2) if n_all else 0.0,
    }
    if asst_time_min is not None:
        stats["asst_time_min_filter"] = asst_time_min
    if asst_time_max is not None:
        stats["asst_time_max_filter"] = asst_time_max

    return records, stats
