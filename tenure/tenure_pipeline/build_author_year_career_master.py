#!/usr/bin/env python3
"""
build_author_year_career_master.py — PD29 career spine from openalex_works_by_year
==================================================================================

Derives Alex's cumulative career pubs rate from existing works JSONL (no OpenAlex
snapshot scan). Safe to run on Mac or Rivanna.

  Input : openalex_works_by_year.jsonl, openalex_author_ids.jsonl
  Output: author_year_career_master.jsonl (+ meta JSON)

Usage (repo root):
  python tenure/tenure_pipeline/build_author_year_career_master.py

Environment:
  CONFIDENCE_MIN   HIGH | MEDIUM | LOW | ALL  (default ALL — only authors with works)
  MIN_PUB_YEAR     default 1950 (drop bad OA years e.g. 1742)
  REPORT_EVERY     default 200 authors
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent

WORKS_PATH = _HERE / "openalex_works_by_year.jsonl"
AUTHOR_IDS_PATH = _HERE / "openalex_author_ids.jsonl"
OUT_PATH = _HERE / "author_year_career_master.jsonl"
META_PATH = _HERE / "author_year_career_master_meta.json"

TIER_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "MULTI": 3, "NONE": 4}
CONFIDENCE_MIN = (os.environ.get("CONFIDENCE_MIN") or "ALL").strip().upper()
MIN_PUB_YEAR = int(os.environ.get("MIN_PUB_YEAR") or 1950)
MAX_PUB_YEAR = int(os.environ.get("MAX_PUB_YEAR") or 2030)
REPORT_EVERY = int(os.environ.get("REPORT_EVERY") or 200)


def _load_author_meta(path: Path) -> dict[str, dict]:
    meta: dict[str, dict] = {}
    if not path.exists():
        return meta
    with path.open(encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            fid = r.get("faculty_id")
            if fid:
                meta[fid] = r
    return meta


def _load_works(path: Path) -> tuple[dict[str, dict[int, int]], dict[str, dict]]:
    """faculty_id -> {year: n_works}, faculty_id -> {openalex_id, uni_slug}."""
    by_fid: dict[str, dict[int, int]] = defaultdict(dict)
    ids: dict[str, dict] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            fid = r.get("faculty_id")
            yr = r.get("year")
            if not fid or yr is None:
                continue
            yr = int(yr)
            if yr < MIN_PUB_YEAR or yr > MAX_PUB_YEAR:
                continue
            n = int(r.get("n_works") or 0)
            # works file may contain duplicate (faculty_id, year) lines — take max, do not sum
            prev = by_fid[fid].get(yr)
            by_fid[fid][yr] = n if prev is None else max(prev, n)
            if fid not in ids:
                ids[fid] = {
                    "openalex_id": r.get("openalex_id") or "",
                    "uni_slug": r.get("uni_slug") or "",
                }
    return by_fid, ids


def _passes_confidence(conf: str) -> bool:
    if CONFIDENCE_MIN == "ALL":
        return True
    min_rank = TIER_RANK.get(CONFIDENCE_MIN, 0)
    return TIER_RANK.get(conf, 99) <= min_rank


def _career_rows(
    fid: str,
    works: dict[int, int],
    *,
    openalex_id: str,
    uni_slug: str,
    match_confidence: str,
) -> list[dict]:
    if not works:
        return []
    pos_years = [y for y, n in works.items() if n > 0]
    if not pos_years:
        return []
    first_pub = min(pos_years)
    last_pub = max(works)
    cum = 0
    rows: list[dict] = []
    for yr in range(first_pub, last_pub + 1):
        n = int(works.get(yr, 0))
        cum += n
        age = yr - first_pub
        rate = (cum / age) if age > 0 else None
        rows.append(
            {
                "openalex_id": openalex_id,
                "faculty_id": fid,
                "uni_slug": uni_slug,
                "match_confidence": match_confidence,
                "year": yr,
                "n_works": n,
                "cum_works": cum,
                "first_pub_year": first_pub,
                "career_age_years": age,
                "pubs_per_career_year": rate,
            }
        )
    return rows


def main() -> None:
    t0 = time.time()
    if not WORKS_PATH.exists():
        print(f"ERROR: missing {WORKS_PATH}", file=sys.stderr)
        sys.exit(1)

    print(f"Loading author IDs from {AUTHOR_IDS_PATH.name} …")
    author_meta = _load_author_meta(AUTHOR_IDS_PATH)
    print(f"  {len(author_meta):,} author records")

    print(f"Loading works from {WORKS_PATH.name} …")
    works_by_fid, work_ids = _load_works(WORKS_PATH)
    print(f"  {len(works_by_fid):,} faculty with ≥1 year in [{MIN_PUB_YEAR}, {MAX_PUB_YEAR}]")

    # Resume: skip faculty already present in output (any row)
    done_fids: set[str] = set()
    if OUT_PATH.exists():
        with OUT_PATH.open(encoding="utf-8") as f:
            for line in f:
                try:
                    done_fids.add(json.loads(line)["faculty_id"])
                except (json.JSONDecodeError, KeyError):
                    pass
        print(f"  resume: {len(done_fids):,} faculty already in {OUT_PATH.name}")

    mode = "a" if done_fids else "w"
    n_authors = 0
    n_rows = 0
    tier_counts: Counter = Counter()
    year_min, year_max = 9999, 0

    candidates = sorted(works_by_fid)
    with OUT_PATH.open(mode, encoding="utf-8") as fout:
        for i, fid in enumerate(candidates, start=1):
            if fid in done_fids:
                continue
            am = author_meta.get(fid, {})
            conf = am.get("match_confidence") or "NONE"
            if not _passes_confidence(conf):
                continue

            wi = work_ids.get(fid, {})
            rows = _career_rows(
                fid,
                works_by_fid[fid],
                openalex_id=wi.get("openalex_id") or am.get("openalex_id") or "",
                uni_slug=wi.get("uni_slug") or am.get("uni_slug") or "",
                match_confidence=conf,
            )
            for rec in rows:
                fout.write(json.dumps(rec) + "\n")
                n_rows += 1
                year_min = min(year_min, rec["year"])
                year_max = max(year_max, rec["year"])
            fout.flush()
            n_authors += 1
            tier_counts[conf] += 1

            if REPORT_EVERY and i % REPORT_EVERY == 0:
                print(f"  … {i:,}/{len(candidates):,} faculty scanned, {n_rows:,} rows this run")

    # Full output stats (re-read if resume appended)
    total_rows = 0
    authors_out: set[str] = set()
    if OUT_PATH.exists():
        with OUT_PATH.open(encoding="utf-8") as f:
            for line in f:
                try:
                    r = json.loads(line)
                    total_rows += 1
                    authors_out.add(r["faculty_id"])
                    year_min = min(year_min, int(r["year"]))
                    year_max = max(year_max, int(r["year"]))
                except (json.JSONDecodeError, KeyError, ValueError):
                    pass

    meta = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "script": "build_author_year_career_master.py",
        "pd29": True,
        "inputs": {
            "works_path": str(WORKS_PATH.name),
            "works_mtime": datetime.fromtimestamp(WORKS_PATH.stat().st_mtime).isoformat(),
            "author_ids_path": str(AUTHOR_IDS_PATH.name),
            "author_ids_mtime": (
                datetime.fromtimestamp(AUTHOR_IDS_PATH.stat().st_mtime).isoformat()
                if AUTHOR_IDS_PATH.exists()
                else None
            ),
        },
        "filters": {
            "confidence_min": CONFIDENCE_MIN,
            "min_pub_year": MIN_PUB_YEAR,
            "max_pub_year": MAX_PUB_YEAR,
        },
        "n_authors_this_run": n_authors,
        "n_rows_this_run": n_rows,
        "n_authors_total": len(authors_out),
        "n_rows_total": total_rows,
        "year_range": [year_min, year_max] if total_rows else None,
        "authors_by_tier_this_run": dict(tier_counts),
        "note": (
            "Derived from openalex_works_by_year only; MEDIUM has no works rows until "
            "build_openalex_cache is extended on Rivanna."
        ),
    }
    META_PATH.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    elapsed = time.time() - t0
    print(f"Wrote {OUT_PATH.relative_to(_REPO)} · {total_rows:,} rows · {len(authors_out):,} authors")
    print(f"Wrote {META_PATH.relative_to(_REPO)}")
    print(f"Done in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
