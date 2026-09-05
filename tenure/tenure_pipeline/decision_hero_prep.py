"""Decision-year HERO prep — dept pond at decision calendar year (PD29).

One person row per resolved decision-cohort member:
  • X = LOO mean of peers' performance metric in same dept × decision year
  • Optional ability slice: own pubs_per_career_year
  • Peers = all faculty observed in panel that year (any rank), not assistant-only pool
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from decision_year_cohort import build_decision_cohort_records, load_career_lookup

PRIMARY_TIERS = frozenset({"HIGH", "MEDIUM"})

# Dept LOO metrics for perf-metric story (decision cohort · HERO only)
DECISION_LOO_METRICS: tuple[tuple[str, str, str], ...] = (
    ("career_rate", "career rate", "pubs_per_career_year"),
    ("cum_pubs", "cum pubs", "pubs_cumulative"),
    ("annual_pubs", "annum pubs", "pubs_year"),
)


def _mean(vals: list[float]) -> float | None:
    if not vals:
        return None
    return sum(vals) / len(vals)


def _to_float(raw: Any) -> float | None:
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def build_dept_year_rosters(panel_path: Path) -> dict[tuple[str, int], set[str]]:
    """(uni_slug, year) -> all faculty_ids with any row that year."""
    rosters: dict[tuple[str, int], set[str]] = defaultdict(set)
    with panel_path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            slug = r.get("uni_slug")
            yr = r.get("year")
            fid = r.get("faculty_id")
            if slug and yr is not None and fid:
                rosters[(str(slug), int(yr))].add(str(fid))
    return dict(rosters)


def build_panel_year_lookup(panel_path: Path) -> dict[tuple[str, int], dict[str, Any]]:
    """(faculty_id, year) -> first panel row (any rank)."""
    out: dict[tuple[str, int], dict[str, Any]] = {}
    with panel_path.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            fid = r.get("faculty_id")
            yr = r.get("year")
            if fid is None or yr is None:
                continue
            key = (str(fid), int(yr))
            if key not in out:
                out[key] = r
    return out


def _career_rate(career: dict[tuple[str, int], dict[str, Any]], fid: str, year: int) -> float | None:
    row = career.get((fid, year))
    if not row:
        return None
    return _to_float(row.get("pubs_per_career_year"))


def metric_value_at_decision(
    metric_key: str,
    fid: str,
    year: int,
    *,
    career: dict[tuple[str, int], dict[str, Any]],
    panel_yr: dict[tuple[str, int], dict[str, Any]],
) -> float | None:
    """Peer/own performance scalar at calendar year for dept LOO."""
    if metric_key == "career_rate":
        return _career_rate(career, fid, year)
    py = panel_yr.get((fid, year))
    if metric_key == "cum_pubs":
        if py is not None:
            v = _to_float(py.get("pubs_cumulative"))
            if v is not None:
                return v
        cr = career.get((fid, year))
        return _to_float(cr.get("cum_works")) if cr else None
    if metric_key == "annual_pubs":
        if py is not None:
            v = _to_float(py.get("pubs_year"))
            if v is not None:
                return v
        cr = career.get((fid, year))
        return _to_float(cr.get("n_works")) if cr else None
    raise ValueError(f"Unknown metric_key {metric_key!r}")


def prepare_decision_loo_persons(
    panel_path: Path,
    career_path: Path,
    metric_key: str,
    *,
    tiers: frozenset[str] = PRIMARY_TIERS,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Dept pond LOO on ``metric_key`` at decision year (HERO peer X)."""
    valid = {k for k, _, _ in DECISION_LOO_METRICS}
    if metric_key not in valid:
        raise ValueError(f"metric_key must be one of {sorted(valid)!r}, got {metric_key!r}")

    career = load_career_lookup(career_path)
    panel_yr = build_panel_year_lookup(panel_path)
    rosters = build_dept_year_rosters(panel_path)
    cohort, cohort_stats = build_decision_cohort_records(panel_path, career_path, tiers=tiers)

    persons: list[dict[str, Any]] = []
    n_no_pool = 0
    n_no_x = 0

    for rec in cohort:
        fid = str(rec["faculty_id"])
        uni = str(rec["uni_slug"])
        dy = int(rec["decision_year"])
        roster = rosters.get((uni, dy), set())

        peer_vals: list[float] = []
        n_peers_with_val = 0
        for pfid in roster:
            if pfid == fid:
                continue
            val = metric_value_at_decision(
                metric_key, pfid, dy, career=career, panel_yr=panel_yr
            )
            if val is not None:
                peer_vals.append(val)
                n_peers_with_val += 1

        loo = _mean(peer_vals)
        own = metric_value_at_decision(
            metric_key, fid, dy, career=career, panel_yr=panel_yr
        )

        if not roster:
            n_no_pool += 1
        if loo is None:
            n_no_x += 1
            continue

        persons.append({
            "faculty_id": fid,
            "loo_mean": loo,
            "tenure": bool(rec["tenure_event"]),
            "attrition": bool(rec["attrition"]),
            "censored": False,
            "uni_slug": uni,
            "decision_year": dy,
            "asst_time": rec.get("asst_time"),
            "own_metric": own,
            "dept_loo_metric": loo,
            "metric_key": metric_key,
            "pool_size_dept": len(roster),
            "pool_size_loo": n_peers_with_val,
            "off_tenure_track": bool(rec.get("off_tenure_track")),
        })

    stats = {
        **cohort_stats,
        "metric_key": metric_key,
        "x_metric": "decision_loo",
        "n_persons_with_x": len(persons),
        "n_dropped_null_x": n_no_x,
        "n_empty_dept_pool": n_no_pool,
    }
    return persons, stats


def prepare_decision_hero_persons(
    panel_path: Path,
    career_path: Path,
    *,
    tiers: frozenset[str] = PRIMARY_TIERS,
    x_metric: str = "decision_loo",
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Build stage9-compatible person rows for decision cohort HERO.

    x_metric:
      decision_loo  — dept pond LOO on pubs_per_career_year (default PD29 peer X)
      own_career    — own pubs_per_career_year (ability slice)
    """
    if x_metric not in ("decision_loo", "own_career"):
        raise ValueError("x_metric must be 'decision_loo' or 'own_career'")

    career = load_career_lookup(career_path)
    rosters = build_dept_year_rosters(panel_path)
    cohort, cohort_stats = build_decision_cohort_records(panel_path, career_path, tiers=tiers)

    persons: list[dict[str, Any]] = []
    n_no_pool = 0
    n_no_x = 0

    for rec in cohort:
        fid = str(rec["faculty_id"])
        uni = str(rec["uni_slug"])
        dy = int(rec["decision_year"])
        roster = rosters.get((uni, dy), set())

        peer_rates: list[float] = []
        n_peers_with_rate = 0
        for pfid in roster:
            if pfid == fid:
                continue
            rate = _career_rate(career, pfid, dy)
            if rate is not None:
                peer_rates.append(rate)
                n_peers_with_rate += 1

        loo = _mean(peer_rates)
        own = rec.get("pubs_per_career_year")
        own_f = float(own) if own is not None else None

        if x_metric == "own_career":
            x_val = own_f
        else:
            x_val = loo

        if not roster:
            n_no_pool += 1
        if x_val is None:
            n_no_x += 1
            continue

        persons.append({
            "faculty_id": fid,
            "loo_mean": x_val,
            "tenure": bool(rec["tenure_event"]),
            "attrition": bool(rec["attrition"]),
            "censored": False,
            "uni_slug": uni,
            "decision_year": dy,
            "asst_time": rec.get("asst_time"),
            "own_career_rate": own_f,
            "dept_loo_career_rate": loo,
            "pool_size_dept": len(roster),
            "pool_size_rate_loo": n_peers_with_rate,
            "off_tenure_track": bool(rec.get("off_tenure_track")),
        })

    stats = {
        **cohort_stats,
        "x_metric": x_metric,
        "n_persons_with_x": len(persons),
        "n_dropped_null_x": n_no_x,
        "n_empty_dept_pool": n_no_pool,
    }
    return persons, stats
