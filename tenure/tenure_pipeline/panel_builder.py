"""
Stage 7 — Enriched annual faculty panel
========================================
Collapses the multi-capture Cell 5 panel to one row per (faculty_id × year),
joins OpenAlex publication counts (Cell 6B), derives career events
(tenure / attrition / censoring), and writes the analysis-ready JSONL.

Usage (from Cell 7 in 540_tenure_pipeline.ipynb):

    import tenure.tenure_pipeline.panel_builder as pb
    loss = pb.build_annual_panel(
        panel_path  = STAGE5_OUT,
        works_path  = STAGE6_WORKS,
        author_path = STAGE6_AUTHORS,
        out_path    = STAGE7_OUT,
    )

Output schema (one JSON record per faculty_id × year):
    faculty_id, uni_slug, university, name_key, name_display,
    openalex_id, match_confidence,
    year, rank, n_snapshots,
    pubs_year, pubs_cumulative,
    years_as_asst_so_far,          # non-null only when rank == assistant
    ever_assistant,                # person ever observed as assistant
    first_asst_year, last_asst_year,
    tenure_event,                  # True = became assoc/full within gap_tolerance yrs
    year_of_tenure,
    attrition,                     # True = last asst year without promotion, before data ends
    censored,                      # True = still assistant near end of data window
"""

import json
import time
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Rank taxonomy
# ---------------------------------------------------------------------------

# Lower number = more informative / tenure-track relevant; used to pick the
# "best" rank when multiple snapshots in a year disagree.
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

_ASSISTANT_RANKS  = frozenset({"assistant"})
_PROMOTED_RANKS   = frozenset({"associate", "full", "endowed", "distinguished"})


def _best_rank(ranks):
    """Return the most specific rank from a list, using _RANK_PRIORITY."""
    return min(ranks, key=lambda r: _RANK_PRIORITY.get(r, 98))


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
    gap_tolerance=2,
):
    """
    Build the Stage 7 enriched year-level panel.

    Parameters
    ----------
    panel_path    : faculty_panel.jsonl          (Cell 5 output)
    works_path    : openalex_works_by_year.jsonl (Cell 6B output)
    author_path   : openalex_author_ids.jsonl    (Cell 6A output; adds openalex_id + confidence)
    out_path      : enriched panel output path   (faculty_panel_enriched.jsonl)
    min_year      : earliest year to include in output
    max_year      : latest year to include in output
    gap_tolerance : max gap (years) to link a promotion event to the last assistant year

    Returns
    -------
    dict  — sample-loss accounting table (also printed to stdout)
    """
    t0 = time.time()

    # ── 1. Load OpenAlex author IDs → {faculty_id: (openalex_id, confidence)} ─
    print("  Loading OpenAlex author IDs …")
    author_path = Path(author_path)
    oa_ids: dict[str, tuple[str, str]] = {}
    if author_path.exists():
        with open(author_path, encoding="utf-8") as f:
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

    # ── 2. Load OpenAlex works → {faculty_id: {year: n_works}} ─────────────────
    print("  Loading OpenAlex works …")
    works_path = Path(works_path)
    works: dict[str, dict[int, int]] = defaultdict(dict)
    n_works_rows = 0
    if works_path.exists():
        with open(works_path, encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    fid = r["faculty_id"]
                    yr  = int(r["year"])
                    works[fid][yr] = int(r.get("n_works", 0))
                    n_works_rows += 1
                except Exception:
                    pass
    print(f"    {n_works_rows:,} works rows for {len(works):,} faculty_ids")

    # ── 3. Load panel → {faculty_id: {year: [rank, …]}} ────────────────────────
    print("  Loading faculty panel …")
    panel_path = Path(panel_path)
    # by_person[fid][year] = list of rank strings seen that year
    by_person: dict[str, dict[int, list[str]]] = defaultdict(lambda: defaultdict(list))
    meta: dict[str, dict] = {}   # one metadata dict per faculty_id
    n_panel_rows = 0
    with open(panel_path, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            fid = r.get("faculty_id")
            yr  = r.get("year")
            if not fid or yr is None:
                continue
            yr = int(yr)
            if yr < min_year or yr > max_year:
                continue
            rank = r.get("rank") or "unknown"
            by_person[fid][yr].append(rank)
            if fid not in meta:
                meta[fid] = {
                    "faculty_id":   fid,
                    "uni_slug":     r.get("uni_slug", ""),
                    "university":   r.get("university", ""),
                    "name_key":     r.get("name_key", ""),
                    "name_display": r.get("name_display", ""),
                }
            n_panel_rows += 1
    print(f"    {n_panel_rows:,} panel rows  →  {len(by_person):,} unique faculty_ids")

    # ── 4. Collapse to (faculty_id × year) with best rank ───────────────────────
    print("  Collapsing to annual observations …")
    # annual[fid][year] = {"rank": str, "n_snapshots": int}
    annual: dict[str, dict[int, dict]] = {}
    for fid, yr_ranks in by_person.items():
        annual[fid] = {}
        for yr, ranks in yr_ranks.items():
            annual[fid][yr] = {
                "rank":        _best_rank(ranks),
                "n_snapshots": len(ranks),
            }
    del by_person  # free ~500 MB

    # ── 5. Derive career events per faculty_id ────────────────────────────────
    print("  Deriving career events …")
    person_events: dict[str, dict] = {}

    for fid, yr_obs in annual.items():
        sorted_years      = sorted(yr_obs.keys())
        ranks_by_year     = {yr: yr_obs[yr]["rank"] for yr in sorted_years}

        asst_years     = [y for y in sorted_years if ranks_by_year[y] in _ASSISTANT_RANKS]
        promoted_years = [y for y in sorted_years if ranks_by_year[y] in _PROMOTED_RANKS]

        if not asst_years:
            person_events[fid] = {
                "ever_assistant": False,
                "first_asst_year": None,
                "last_asst_year":  None,
                "tenure_event":    False,
                "year_of_tenure":  None,
                "attrition":       False,
                "censored":        False,
            }
            continue

        first_asst = min(asst_years)
        last_asst  = max(asst_years)

        # Tenure event: appeared as promoted within gap_tolerance years after last assistant year.
        # We also accept promotions that appeared in the same year (could be same-year transition).
        tenure_year = None
        for py in sorted(promoted_years):
            if py >= first_asst and py <= last_asst + gap_tolerance:
                # Promoted while or shortly after being an assistant — count it.
                # (If they're simultaneously listed as "associate" in one snapshot
                # and "assistant" in another in the same year, that year is the transition.)
                if py > last_asst or (py == last_asst and ranks_by_year.get(py) in _PROMOTED_RANKS):
                    tenure_year = py
                    break
                # Promoted in same year as last assistant — transition year
                if py == last_asst:
                    tenure_year = py
                    break

        # If no close promoted year, check further out (different path — longer gap)
        if tenure_year is None:
            future = [py for py in promoted_years if py > last_asst]
            if future:
                candidate = min(future)
                if candidate <= last_asst + gap_tolerance:
                    tenure_year = candidate

        attrition = False
        censored  = False
        if tenure_year is None:
            # Not promoted within tolerance: attrition if disappeared before end of window,
            # censored if still active near the end.
            if last_asst >= max_year - gap_tolerance:
                censored = True   # right-censored (still in data at the end)
            else:
                attrition = True  # disappeared before data ends

        person_events[fid] = {
            "ever_assistant":  True,
            "first_asst_year": first_asst,
            "last_asst_year":  last_asst,
            "tenure_event":    tenure_year is not None,
            "year_of_tenure":  tenure_year,
            "attrition":       attrition,
            "censored":        censored,
        }

    # ── 6. Write enriched panel ─────────────────────────────────────────────────
    print("  Writing enriched panel …")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    n_out = 0

    with open(out_path, "w", encoding="utf-8") as fout:
        for fid in sorted(annual.keys()):
            m         = meta[fid]
            ev        = person_events[fid]
            fid_works = works.get(fid, {})
            oa_id, oa_conf = oa_ids.get(fid, ("", "NONE"))
            sorted_years = sorted(annual[fid].keys())

            cum = 0
            years_as_asst_so_far = 0
            for yr in sorted_years:
                obs    = annual[fid][yr]
                rank   = obs["rank"]
                n_pubs = fid_works.get(yr, 0)
                cum   += n_pubs
                if rank in _ASSISTANT_RANKS:
                    years_as_asst_so_far += 1

                rec = {
                    **m,
                    "openalex_id":         oa_id,
                    "match_confidence":    oa_conf,
                    "year":                yr,
                    "rank":                rank,
                    "n_snapshots":         obs["n_snapshots"],
                    "pubs_year":           n_pubs,
                    "pubs_cumulative":     cum,
                    # years_as_asst_so_far: count of prior + current assistant-rank years
                    # non-null only when rank == assistant so analysis can filter cleanly
                    "years_as_asst_so_far": (years_as_asst_so_far
                                             if rank in _ASSISTANT_RANKS else None),
                    # Career-level event flags (same value for all rows of this person)
                    "ever_assistant":  ev["ever_assistant"],
                    "first_asst_year": ev["first_asst_year"],
                    "last_asst_year":  ev["last_asst_year"],
                    "tenure_event":    ev["tenure_event"],
                    "year_of_tenure":  ev["year_of_tenure"],
                    "attrition":       ev["attrition"],
                    "censored":        ev["censored"],
                }
                fout.write(json.dumps(rec) + "\n")
                n_out += 1

    # ── 7. Sample-loss accounting ────────────────────────────────────────────────
    n_fids          = len(annual)
    n_asst          = sum(1 for e in person_events.values() if e["ever_assistant"])
    n_tenure        = sum(1 for e in person_events.values() if e["tenure_event"])
    n_attrition     = sum(1 for e in person_events.values() if e["attrition"])
    n_censored      = sum(1 for e in person_events.values() if e["censored"])
    n_with_works    = sum(1 for fid in annual if works.get(fid))
    n_asst_w_works  = sum(
        1 for fid, e in person_events.items()
        if e["ever_assistant"] and works.get(fid)
    )

    elapsed = time.time() - t0
    print(f"\n  {'─'*60}")
    print(f"  Stage 7 complete in {elapsed:.1f}s")
    print(f"  Output rows          : {n_out:,}")
    print(f"  Unique faculty_ids   : {n_fids:,}")
    print(f"  ├─ ever assistant    : {n_asst:,}  ({n_asst/n_fids*100:.1f}%)")
    print(f"  │   ├─ tenure event  : {n_tenure:,}  ({n_tenure/max(n_asst,1)*100:.1f}% of asst)")
    print(f"  │   ├─ attrition     : {n_attrition:,}  ({n_attrition/max(n_asst,1)*100:.1f}% of asst)")
    print(f"  │   └─ censored      : {n_censored:,}  ({n_censored/max(n_asst,1)*100:.1f}% of asst)")
    print(f"  Faculty w/ OA works  : {n_with_works:,}  ({n_with_works/n_fids*100:.1f}% of all)")
    print(f"  Asst. faculty w/ OA  : {n_asst_w_works:,}  ({n_asst_w_works/max(n_asst,1)*100:.1f}% of asst)")
    print(f"  {'─'*60}")
    print(f"  ⚠  NOTE: {n_asst - n_asst_w_works:,} assistant faculty have no OA publication data.")
    print(f"     Peer-pool models using pubs will be restricted to the {n_asst_w_works:,}-person subset.")
    print(f"  {'─'*60}")

    loss = {
        "panel_rows_loaded":        n_panel_rows,
        "unique_faculty_ids":       n_fids,
        "ever_assistant":           n_asst,
        "tenure_event":             n_tenure,
        "attrition":                n_attrition,
        "censored":                 n_censored,
        "faculty_with_oa_works":    n_with_works,
        "asst_faculty_with_oa":     n_asst_w_works,
        "output_rows":              n_out,
        "gap_tolerance_yrs":        gap_tolerance,
        "year_range":               f"{min_year}–{max_year}",
    }
    return loss
