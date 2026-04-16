"""
Stage 8 — Leave-Self-Out (LOO) peer pool metrics
==================================================
Adds publication-based peer quality columns to the enriched panel from
Stage 7.  For each (uni_slug, year), the peer pool is all faculty observed
as *assistant professor* that year.  Pool quality is measured using
OpenAlex publication counts (``pubs_year``).

Because only ~17% of assistant faculty have OpenAlex data, pool quality is
computed over the OA-matched subset.  Both the full pool size and the
OA-matched subset size are reported so the advisor can see coverage.

Output schema (adds to every row in faculty_panel_enriched.jsonl):

    pool_size_all       : int    — total assistants in dept-year
    pool_size_oa        : int    — assistants with OA data in dept-year
    pool_size_oa_loo    : int    — OA assistants after excluding person i
                                   (= pool_size_oa - 1 if i has OA, else pool_size_oa)
    poolq_loo_mean      : float  — LOO mean pubs (None if pool_size_oa_loo == 0)
    poolq_loo_sd        : float  — LOO std dev pubs (None if pool_size_oa_loo < 2)
    pool_rank_loo       : int    — person i's rank in full OA pool (1=lowest pubs;
                                   None if i has no OA data)
    pool_pctile_loo     : float  — percentile (0–100) in OA pool (None if no OA data)

Usage (Cell 8):

    import pool_metrics as pm
    summary = pm.build_pool_metrics(
        in_path  = STAGE7_OUT,
        out_path = STAGE8_OUT,
    )
"""

import json
import math
import statistics
import time
from collections import defaultdict
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mean_sd(vals):
    """Return (mean, sd) or (None, None) for an empty list."""
    if not vals:
        return None, None
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return m, None
    sd = math.sqrt(sum((v - m) ** 2 for v in vals) / (len(vals) - 1))
    return m, sd


def _rank_pctile(val, pool_vals):
    """
    Rank of val within pool_vals (1 = lowest, len = highest).
    Returns (rank, percentile_0_to_100) or (None, None) if pool is empty.
    """
    if not pool_vals:
        return None, None
    n = len(pool_vals)
    rank = sum(1 for v in pool_vals if v <= val)   # number <= val (1-indexed)
    pctile = (rank - 1) / max(n - 1, 1) * 100.0
    return rank, round(pctile, 1)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def build_pool_metrics(
    in_path,
    out_path,
    pool_rank_filter=("assistant",),
):
    """
    Compute LOO peer-pool publication metrics and write augmented JSONL.

    Parameters
    ----------
    in_path           : faculty_panel_enriched.jsonl  (Stage 7 output)
    out_path          : faculty_panel_with_pools.jsonl (Stage 8 output)
    pool_rank_filter  : ranks that count as pool members (default: assistant only)

    Returns
    -------
    dict  — summary / sample-loss table (also printed)
    """
    t0 = time.time()
    in_path  = Path(in_path)
    out_path = Path(out_path)

    # ── 1. First pass: build pool lookup {(uni_slug, year): list of member dicts} ─
    print("  Pass 1: building dept-year pools …")
    # pool_members[key] = [ {fid, pubs_year, has_oa}, … ]
    pool_members = defaultdict(list)
    n_rows = 0
    with open(in_path, encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            n_rows += 1
            if r.get("rank") in pool_rank_filter:
                key = (r["uni_slug"], r["year"])
                pool_members[key].append({
                    "fid":      r["faculty_id"],
                    "pubs":     r.get("pubs_year") or 0,
                    "has_oa":   bool(r.get("openalex_id")),
                })

    n_dept_years      = len(pool_members)
    n_oa_ge1          = sum(1 for v in pool_members.values()
                            if sum(1 for m in v if m["has_oa"]) >= 1)
    n_oa_ge2          = sum(1 for v in pool_members.values()
                            if sum(1 for m in v if m["has_oa"]) >= 2)
    n_oa_zero         = n_dept_years - n_oa_ge1

    print(f"    {n_rows:,} input rows")
    print(f"    {n_dept_years:,} dept-years with pool-rank faculty")
    print(f"    ├─ dept-years with ≥1 OA member : {n_oa_ge1:,}")
    print(f"    ├─ dept-years with ≥2 OA members: {n_oa_ge2:,}  (LOO computable)")
    print(f"    └─ dept-years with 0 OA members : {n_oa_zero:,}  (LOO = None)")

    # ── 2. Precompute pool stats for each dept-year ──────────────────────────────
    # pool_stats[key] = { all_pubs, oa_pubs_by_fid }
    pool_stats = {}
    for key, members in pool_members.items():
        oa_members  = [m for m in members if m["has_oa"]]
        oa_pubs     = {m["fid"]: m["pubs"] for m in oa_members}
        all_pubs    = [m["pubs"] for m in oa_members]  # OA pool values
        pool_stats[key] = {
            "size_all":  len(members),
            "size_oa":   len(oa_members),
            "oa_pubs":   oa_pubs,     # fid → pubs for OA members
            "all_pubs":  all_pubs,    # list of pubs for full OA pool (for rank)
        }

    # ── 3. Second pass: write augmented rows ─────────────────────────────────────
    print("  Pass 2: writing augmented panel …")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    n_out           = 0
    n_loo_computable = 0
    n_loo_none      = 0
    n_rank_computable = 0

    with open(in_path, encoding="utf-8") as fin, \
         open(out_path, "w", encoding="utf-8") as fout:
        for line in fin:
            try:
                r = json.loads(line)
            except Exception:
                continue

            key     = (r["uni_slug"], r["year"])
            ps      = pool_stats.get(key)

            if ps is None or r.get("rank") not in pool_rank_filter:
                # Not an assistant row (or dept-year not in pools) — pass through
                # with null pool columns so the file is uniform
                r.update({
                    "pool_size_all":    ps["size_all"] if ps else None,
                    "pool_size_oa":     ps["size_oa"]  if ps else None,
                    "pool_size_oa_loo": None,
                    "poolq_loo_mean":   None,
                    "poolq_loo_sd":     None,
                    "pool_rank_loo":    None,
                    "pool_pctile_loo":  None,
                })
            else:
                fid     = r["faculty_id"]
                has_oa  = bool(r.get("openalex_id"))
                oa_pubs = ps["oa_pubs"]   # {fid: pubs} for OA pool

                # LOO pool: all OA members except person i (if i is OA-matched)
                loo_pubs = [p for f, p in oa_pubs.items() if f != fid]
                loo_size = len(loo_pubs)

                m, sd = _mean_sd(loo_pubs)

                # Rank: person i's position within the FULL OA pool (incl. themselves)
                if has_oa and ps["all_pubs"]:
                    my_pubs = oa_pubs.get(fid, 0)
                    rank, pctile = _rank_pctile(my_pubs, ps["all_pubs"])
                    n_rank_computable += 1
                else:
                    rank, pctile = None, None

                if m is not None:
                    n_loo_computable += 1
                else:
                    n_loo_none += 1

                r.update({
                    "pool_size_all":    ps["size_all"],
                    "pool_size_oa":     ps["size_oa"],
                    "pool_size_oa_loo": loo_size,
                    "poolq_loo_mean":   round(m, 4) if m is not None else None,
                    "poolq_loo_sd":     round(sd, 4) if sd is not None else None,
                    "pool_rank_loo":    rank,
                    "pool_pctile_loo":  pctile,
                })

            fout.write(json.dumps(r) + "\n")
            n_out += 1

    elapsed = time.time() - t0
    print(f"\n  {'─'*60}")
    print(f"  Stage 8 complete in {elapsed:.1f}s")
    print(f"  Output rows              : {n_out:,}")
    print(f"  Asst rows w/ LOO computable : {n_loo_computable:,}")
    print(f"  Asst rows w/ LOO = None     : {n_loo_none:,}  (no OA peers after LOO)")
    print(f"  Asst rows w/ rank computable: {n_rank_computable:,}")
    print(f"  {'─'*60}")
    print(f"  ⚠  LOO is None for ~{n_loo_none/(n_loo_computable+n_loo_none)*100:.0f}% of assistant rows — OA coverage gap.")
    print(f"     Inverted-U analysis will use the {n_loo_computable:,}-row subset with computable LOO.")
    print(f"  {'─'*60}")

    summary = {
        "input_rows":              n_rows,
        "output_rows":             n_out,
        "dept_years_in_pool":      n_dept_years,
        "dept_years_oa_ge2":       n_oa_ge2,
        "dept_years_oa_zero":      n_oa_zero,
        "asst_rows_loo_computable": n_loo_computable,
        "asst_rows_loo_none":      n_loo_none,
        "asst_rows_rank_computable": n_rank_computable,
    }
    return summary
