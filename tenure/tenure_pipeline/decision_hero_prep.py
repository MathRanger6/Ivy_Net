"""Decision-year HERO prep — dept pond at decision calendar year (PD29).

One person row per resolved decision-cohort member:
  • X = LOO mean of peers' pubs_per_career_year in same dept × decision year
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


def _mean(vals: list[float]) -> float | None:
    if not vals:
        return None
    return sum(vals) / len(vals)


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


def _career_rate(career: dict[tuple[str, int], dict[str, Any]], fid: str, year: int) -> float | None:
    row = career.get((fid, year))
    if not row:
        return None
    raw = row.get("pubs_per_career_year")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


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
