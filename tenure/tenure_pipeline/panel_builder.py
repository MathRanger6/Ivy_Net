"""
Stage 7 — Enriched annual faculty panel
========================================
Collapses the multi-capture Cell 5 panel to one row per (faculty_id × year),
joins OpenAlex publication counts (Cell 6B), derives career events
(tenure / attrition / censoring / transfer), and writes the analysis-ready JSONL.

Outcome policy (Charles lock — Sep 2026):
  • Department-scoped only — no global dataset-end attrition/censoring.
  • Default gap_tolerance=0: dept has scrape for calendar year Y+1 and person
    absent from that dept → attrition (failed promotion / left).
  • No dept scrape for Y+1 → censored (outcome not observable).
  • Same-dept reappearance after a gap → data gap (extend spell / tenure), not attrition.
  • Same name_key at a different department later → transferred (flagged; excluded
    from metric computation until policy is set).
  • Year Y+1 at same dept with a non-tenured title (not assistant, not associate/full)
    → attrition + off_tenure_track (OTT).
  • asst_time replaces years_as_asst_so_far.

Usage (from Cell 7 in 540_tenure_pipeline.ipynb):

    import tenure.tenure_pipeline.panel_builder as pb
    loss = pb.build_annual_panel(
        panel_path  = STAGE5_OUT,
        works_path  = STAGE6_WORKS,
        author_path = STAGE6_AUTHORS,
        out_path    = STAGE7_OUT,
    )
"""

from __future__ import annotations

import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Rank taxonomy
# ---------------------------------------------------------------------------

_RANK_PRIORITY = {
    "assistant":        0,
    "associate":        1,
    "full":             2,
    "endowed":          3,
    "distinguished":    4,
    "emeritus":         5,
    "research_prof":    6,
    "teaching_prof":    7,
    "senior_lecturer":  8,
    "lecturer":         9,
    "instructor":      10,
    "adjunct":         11,
    "visiting":        12,
    "clinical":        13,
    "postdoc":         14,
    "fellow":          15,
    "research_scientist": 16,
    "senior_researcher":  17,
    "research_associate": 18,
    "affiliate":       19,
    "scientist":       20,
    "courtesy":        21,
    "other":           22,
    "unknown":         99,
}

_ASSISTANT_RANKS = frozenset({"assistant"})
_PROMOTED_RANKS = frozenset({"associate", "full", "endowed", "distinguished"})


def _best_rank(ranks: list[str]) -> str:
    return min(ranks, key=lambda r: _RANK_PRIORITY.get(r, 98))


def _build_dept_coverage(panel_path: Path, min_year: int, max_year: int) -> tuple[set[tuple[str, int]], dict[str, int]]:
    """(uni_slug, year) pairs with any scrape row; max calendar year per dept."""
    dept_years: set[tuple[str, int]] = set()
    dept_max: dict[str, int] = {}
    with panel_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            slug = r.get("uni_slug")
            yr = r.get("year")
            if not slug or yr is None:
                continue
            yr = int(yr)
            if yr < min_year or yr > max_year:
                continue
            dept_years.add((slug, yr))
            dept_max[slug] = max(dept_max.get(slug, yr), yr)
    return dept_years, dept_max


def _build_name_key_index(
    meta: dict[str, dict[str, Any]],
    annual: dict[str, dict[int, dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    """name_key -> episodes at other faculty_ids / departments."""
    index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for fid, yr_obs in annual.items():
        m = meta.get(fid, {})
        nk = (m.get("name_key") or "").strip()
        if not nk:
            continue
        asst_years = sorted(y for y, o in yr_obs.items() if o["rank"] in _ASSISTANT_RANKS)
        if not asst_years:
            continue
        index[nk].append({
            "faculty_id": fid,
            "uni_slug": m.get("uni_slug", ""),
            "asst_years": asst_years,
            "first_asst_year": min(asst_years),
        })
    return dict(index)


def _find_transfer(
    *,
    faculty_id: str,
    uni_slug: str,
    name_key: str,
    exit_year: int,
    name_index: dict[str, list[dict[str, Any]]],
) -> tuple[bool, str | None, int | None, str | None]:
    """
    Detect cross-department move via name_key.
    Returns (transferred, transfer_to_uni, transfer_year, transfer_faculty_id).
    """
    episodes = name_index.get(name_key, [])
    for ep in episodes:
        if ep["faculty_id"] == faculty_id:
            continue
        if ep["uni_slug"] == uni_slug:
            continue
        later = [y for y in ep["asst_years"] if y > exit_year]
        if later:
            return True, ep["uni_slug"], min(later), ep["faculty_id"]
    return False, None, None, None


def _effective_last_asst_year(ranks_by_year: dict[int, str]) -> int | None:
    """Last assistant year, extending through same-dept observation gaps."""
    asst_years = sorted(y for y, rk in ranks_by_year.items() if rk in _ASSISTANT_RANKS)
    if not asst_years:
        return None
    last = asst_years[-1]
    observed = sorted(ranks_by_year.keys())
    for y in observed:
        if y > last and ranks_by_year[y] in _ASSISTANT_RANKS:
            last = y
    return last


def _tenure_year_at_dept(ranks_by_year: dict[int, str]) -> int | None:
    """First promoted year on or after first assistant year at this department."""
    asst_years = [y for y, rk in ranks_by_year.items() if rk in _ASSISTANT_RANKS]
    if not asst_years:
        return None
    first_asst = min(asst_years)
    promoted = sorted(y for y, rk in ranks_by_year.items() if rk in _PROMOTED_RANKS and y >= first_asst)
    return promoted[0] if promoted else None


def derive_dept_episode_outcome(
    *,
    ranks_by_year: dict[int, str],
    uni_slug: str,
    faculty_id: str,
    name_key: str,
    dept_years: set[tuple[str, int]],
    dept_max: dict[str, int],
    name_index: dict[str, list[dict[str, Any]]],
    gap_tolerance: int = 0,
) -> dict[str, Any]:
    """
    Derive tenure / attrition / censored / transferred for one person at one department.
    """
    base: dict[str, Any] = {
        "ever_assistant": False,
        "first_asst_year": None,
        "last_asst_year": None,
        "asst_time_at_exit": None,
        "tenure_event": False,
        "year_of_tenure": None,
        "attrition": False,
        "censored": False,
        "off_tenure_track": False,
        "ott_year": None,
        "ott_rank": None,
        "transferred": False,
        "transfer_to_uni_slug": None,
        "transfer_year": None,
        "transfer_faculty_id": None,
        "exclude_from_metrics": False,
    }

    asst_years = sorted(y for y, rk in ranks_by_year.items() if rk in _ASSISTANT_RANKS)
    if not asst_years:
        return base

    first_asst = min(asst_years)
    tenure_year = _tenure_year_at_dept(ranks_by_year)
    last_asst = _effective_last_asst_year(ranks_by_year)
    assert last_asst is not None

    asst_time_at_exit = sum(1 for y in range(first_asst, last_asst + 1) if ranks_by_year.get(y) in _ASSISTANT_RANKS)

    base.update({
        "ever_assistant": True,
        "first_asst_year": first_asst,
        "last_asst_year": last_asst,
        "asst_time_at_exit": asst_time_at_exit,
    })

    if tenure_year is not None:
        base.update({
            "tenure_event": True,
            "year_of_tenure": tenure_year,
        })
        return base

    Y = last_asst
    observed_years = set(ranks_by_year.keys())

    transferred, to_uni, t_year, t_fid = _find_transfer(
        faculty_id=faculty_id,
        uni_slug=uni_slug,
        name_key=name_key,
        exit_year=Y,
        name_index=name_index,
    )
    if transferred:
        base.update({
            "transferred": True,
            "transfer_to_uni_slug": to_uni,
            "transfer_year": t_year,
            "transfer_faculty_id": t_fid,
            "exclude_from_metrics": True,
        })
        return base

    next_year = Y + 1
    dept_has_next = (uni_slug, next_year) in dept_years

    if dept_has_next:
        if next_year not in observed_years:
            dept_last = dept_max.get(uni_slug, next_year)
            if gap_tolerance > 0 and next_year >= dept_last - gap_tolerance + 1:
                base["censored"] = True
            else:
                base["attrition"] = True
        else:
            rank_next = ranks_by_year[next_year]
            if rank_next in _ASSISTANT_RANKS:
                # Still assistant in Y+1 — effective_last_asst should have extended; censor.
                base["censored"] = True
            elif rank_next in _PROMOTED_RANKS:
                base.update({
                    "tenure_event": True,
                    "year_of_tenure": next_year,
                })
            else:
                # Listed at dept in Y+1 under a non-tenured title → OTT attrition.
                base.update({
                    "attrition": True,
                    "off_tenure_track": True,
                    "ott_year": next_year,
                    "ott_rank": rank_next,
                })
    else:
        base["censored"] = True

    return base


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_annual_panel(
    panel_path,
    works_path,
    author_path,
    out_path,
    min_year=2000,
    max_year=2024,
    gap_tolerance=0,
    transfers_audit_path=None,
):
    """
    Build the Stage 7 enriched year-level panel.

    Parameters
    ----------
    panel_path    : faculty_panel.jsonl          (Cell 5 output)
    works_path    : openalex_works_by_year.jsonl (Cell 6B output)
    author_path   : openalex_author_ids.jsonl    (Cell 6A output)
    out_path      : faculty_panel_enriched.jsonl
    min_year, max_year : calendar years retained in output rows
    gap_tolerance : benefit-of-doubt years at dept scrape boundary (default 0)
    transfers_audit_path : optional JSONL of transferred episodes

    Returns
    -------
    dict  — sample-loss accounting table
    """
    t0 = time.time()
    panel_path = Path(panel_path)

    print("  Building department-year coverage index …")
    dept_years, dept_max = _build_dept_coverage(panel_path, min_year, max_year)
    print(f"    {len(dept_years):,} dept-year scrape pairs · {len(dept_max):,} departments")

    print("  Loading OpenAlex author IDs …")
    author_path = Path(author_path)
    oa_ids: dict[str, tuple[str, str]] = {}
    if author_path.exists():
        with author_path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    fid = r.get("faculty_id", "")
                    oa_ids[fid] = (
                        r.get("openalex_id", "") or "",
                        r.get("match_confidence", "NONE") or "NONE",
                    )
                except Exception:
                    pass
    print(f"    {len(oa_ids):,} author-ID records loaded")

    print("  Loading OpenAlex works …")
    works_path = Path(works_path)
    works: dict[str, dict[int, int]] = defaultdict(dict)
    n_works_rows = 0
    if works_path.exists():
        with works_path.open(encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    fid = r["faculty_id"]
                    yr = int(r["year"])
                    works[fid][yr] = int(r.get("n_works", 0))
                    n_works_rows += 1
                except Exception:
                    pass
    print(f"    {n_works_rows:,} works rows for {len(works):,} faculty_ids")

    print("  Loading faculty panel …")
    by_person: dict[str, dict[int, list[str]]] = defaultdict(lambda: defaultdict(list))
    meta: dict[str, dict[str, Any]] = {}
    n_panel_rows = 0
    with panel_path.open(encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            fid = r.get("faculty_id")
            yr = r.get("year")
            if not fid or yr is None:
                continue
            yr = int(yr)
            if yr < min_year or yr > max_year:
                continue
            rank = r.get("rank") or "unknown"
            by_person[fid][yr].append(rank)
            if fid not in meta:
                meta[fid] = {
                    "faculty_id": fid,
                    "uni_slug": r.get("uni_slug", ""),
                    "university": r.get("university", ""),
                    "name_key": r.get("name_key", ""),
                    "name_display": r.get("name_display", ""),
                }
            n_panel_rows += 1
    print(f"    {n_panel_rows:,} panel rows  →  {len(by_person):,} unique faculty_ids")

    print("  Collapsing to annual observations …")
    annual: dict[str, dict[int, dict[str, Any]]] = {}
    for fid, yr_ranks in by_person.items():
        annual[fid] = {}
        for yr, ranks in yr_ranks.items():
            annual[fid][yr] = {
                "rank": _best_rank(ranks),
                "n_snapshots": len(ranks),
            }
    del by_person

    print("  Deriving department-scoped career events …")
    name_index = _build_name_key_index(meta, annual)
    person_events: dict[str, dict[str, Any]] = {}
    transfer_records: list[dict[str, Any]] = []

    for fid, yr_obs in annual.items():
        m = meta[fid]
        ranks_by_year = {yr: obs["rank"] for yr, obs in yr_obs.items()}
        ev = derive_dept_episode_outcome(
            ranks_by_year=ranks_by_year,
            uni_slug=m.get("uni_slug", ""),
            faculty_id=fid,
            name_key=(m.get("name_key") or "").strip(),
            dept_years=dept_years,
            dept_max=dept_max,
            name_index=name_index,
            gap_tolerance=gap_tolerance,
        )
        person_events[fid] = ev
        if ev.get("transferred"):
            transfer_records.append({
                "faculty_id": fid,
                "name_display": m.get("name_display"),
                "name_key": m.get("name_key"),
                "from_uni_slug": m.get("uni_slug"),
                "last_asst_year": ev.get("last_asst_year"),
                "asst_time_at_exit": ev.get("asst_time_at_exit"),
                "transfer_to_uni_slug": ev.get("transfer_to_uni_slug"),
                "transfer_year": ev.get("transfer_year"),
                "transfer_faculty_id": ev.get("transfer_faculty_id"),
            })

    if transfers_audit_path:
        audit_path = Path(transfers_audit_path)
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_path.open("w", encoding="utf-8") as af:
            for rec in transfer_records:
                af.write(json.dumps(rec) + "\n")
        print(f"    Wrote {len(transfer_records):,} transfer audit rows → {audit_path.name}")

    print("  Writing enriched panel …")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    n_out = 0

    with out_path.open("w", encoding="utf-8") as fout:
        for fid in sorted(annual.keys()):
            m = meta[fid]
            ev = person_events[fid]
            fid_works = works.get(fid, {})
            oa_id, oa_conf = oa_ids.get(fid, ("", "NONE"))
            sorted_years = sorted(annual[fid].keys())

            asst_time = 0
            cum = 0
            for yr in sorted_years:
                obs = annual[fid][yr]
                rank = obs["rank"]
                n_pubs = fid_works.get(yr, 0)
                cum += n_pubs
                if rank in _ASSISTANT_RANKS:
                    asst_time += 1

                rec = {
                    **m,
                    "openalex_id": oa_id,
                    "match_confidence": oa_conf,
                    "year": yr,
                    "rank": rank,
                    "n_snapshots": obs["n_snapshots"],
                    "pubs_year": n_pubs,
                    "pubs_cumulative": cum,
                    "asst_time": asst_time if rank in _ASSISTANT_RANKS else None,
                    "ever_assistant": ev["ever_assistant"],
                    "first_asst_year": ev["first_asst_year"],
                    "last_asst_year": ev["last_asst_year"],
                    "tenure_event": ev["tenure_event"],
                    "year_of_tenure": ev["year_of_tenure"],
                    "attrition": ev["attrition"],
                    "censored": ev["censored"],
                    "off_tenure_track": ev.get("off_tenure_track", False),
                    "ott_year": ev.get("ott_year"),
                    "ott_rank": ev.get("ott_rank"),
                    "transferred": ev["transferred"],
                    "transfer_to_uni_slug": ev.get("transfer_to_uni_slug"),
                    "transfer_year": ev.get("transfer_year"),
                    "transfer_faculty_id": ev.get("transfer_faculty_id"),
                    "exclude_from_metrics": ev.get("exclude_from_metrics", False),
                }
                fout.write(json.dumps(rec) + "\n")
                n_out += 1

    n_fids = len(annual)
    n_asst = sum(1 for e in person_events.values() if e["ever_assistant"])
    n_tenure = sum(1 for e in person_events.values() if e["tenure_event"])
    n_attrition = sum(1 for e in person_events.values() if e["attrition"])
    n_ott = sum(1 for e in person_events.values() if e.get("off_tenure_track"))
    n_censored = sum(1 for e in person_events.values() if e["censored"])
    n_transferred = sum(1 for e in person_events.values() if e["transferred"])
    n_resolved = n_tenure + n_attrition
    n_with_works = sum(1 for fid in annual if works.get(fid))
    n_asst_w_works = sum(
        1 for fid, e in person_events.items()
        if e["ever_assistant"] and works.get(fid)
    )

    elapsed = time.time() - t0
    print(f"\n  {'─'*60}")
    print(f"  Stage 7 complete in {elapsed:.1f}s")
    print(f"  Output rows          : {n_out:,}")
    print(f"  Unique faculty_ids   : {n_fids:,}")
    print(f"  ├─ ever assistant    : {n_asst:,}  ({n_asst/n_fids*100:.1f}%)")
    print(f"  │   ├─ tenure        : {n_tenure:,}  ({n_tenure/max(n_asst,1)*100:.1f}% of asst)")
    print(f"  │   ├─ attrition     : {n_attrition:,}  ({n_attrition/max(n_asst,1)*100:.1f}% of asst · incl. OTT {n_ott:,})")
    print(f"  │   ├─ censored      : {n_censored:,}  ({n_censored/max(n_asst,1)*100:.1f}% of asst)")
    print(f"  │   ├─ transferred   : {n_transferred:,}  ({n_transferred/max(n_asst,1)*100:.1f}% of asst · excluded from metrics)")
    print(f"  │   └─ resolved      : {n_resolved:,}  (tenure + attrition)")
    print(f"  Faculty w/ OA works  : {n_with_works:,}  ({n_with_works/n_fids*100:.1f}% of all)")
    print(f"  Asst. faculty w/ OA  : {n_asst_w_works:,}  ({n_asst_w_works/max(n_asst,1)*100:.1f}% of asst)")
    print(f"  gap_tolerance        : {gap_tolerance}")
    print(f"  {'─'*60}")

    return {
        "panel_rows_loaded": n_panel_rows,
        "unique_faculty_ids": n_fids,
        "ever_assistant": n_asst,
        "tenure_event": n_tenure,
        "attrition": n_attrition,
        "off_tenure_track": n_ott,
        "censored": n_censored,
        "transferred": n_transferred,
        "resolved": n_resolved,
        "faculty_with_oa_works": n_with_works,
        "asst_faculty_with_oa": n_asst_w_works,
        "output_rows": n_out,
        "gap_tolerance_yrs": gap_tolerance,
        "year_range": f"{min_year}–{max_year}",
        "dept_year_pairs": len(dept_years),
        "transfer_audit_rows": len(transfer_records),
    }
