#!/usr/bin/env python3
"""
build_openalex_cache.py — standalone first-run cache builder for OpenAlex snapshot data
========================================================================================

Scans the CDH OpenAlex relational CSV snapshot and writes two output files
incrementally (safe to interrupt — progress is preserved on disk as it runs):

  openalex_snapshot_cache.jsonl   — one line per author: {openalex_id, works_by_year}
  openalex_works_by_year.jsonl    — one line per (author, year): {openalex_id, faculty_id,
                                     uni_slug, year, n_works}

On a subsequent run, only authors NOT already in the cache are scanned.
Authors already cached are served immediately from cache (no snapshot I/O).

Usage
-----
  # From Ivy_Net repo root, in the tenure_net conda env:
  python tenure/tenure_pipeline/build_openalex_cache.py

  # Via Slurm (recommended for the first full run):
  sbatch build_openalex_cache.slurm

Environment variables
---------------------
  OPENALEX_SNAPSHOT_ROOT   override default ~/cdh/OpenAlex1125
  OPENALEX_CONFIDENCE_MIN  override default HIGH  (HIGH | MEDIUM | LOW)
  OPENALEX_REPORT_EVERY    override default 5     (report every N authors)
"""

import csv
import glob
import gzip
import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────
_HERE  = Path(__file__).resolve().parent          # tenure/tenure_pipeline/
_REPO  = _HERE.parent.parent                      # Ivy_Net/
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_HERE))

from openalex_resolver import (
    openalex_author_url_to_int,
    _load_snapshot_cache,
    _append_snapshot_cache,
)

# ── Config (override via environment) ────────────────────────────────────────
_oas = (os.environ.get("OPENALEX_SNAPSHOT_ROOT") or "").strip()
SNAPSHOT_ROOT    = Path(_oas).expanduser() if _oas else (Path.home() / "cdh" / "OpenAlex1125")
CONFIDENCE_MIN   = (os.environ.get("OPENALEX_CONFIDENCE_MIN") or "HIGH").strip().upper()
REPORT_EVERY     = int(os.environ.get("OPENALEX_REPORT_EVERY") or 5)

AUTHOR_IDS_PATH  = _HERE / "openalex_author_ids.jsonl"
CACHE_PATH       = _HERE / "openalex_snapshot_cache.jsonl"
WORKS_PATH       = _HERE / "openalex_works_by_year.jsonl"

TIER_RANK        = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "MULTI": 3, "NONE": 4}
CACHE_FLUSH_N    = 50     # flush cache to disk every N authors (safety net)
CACHE_FLUSH_SECS = 120    # also flush if this many seconds have passed


# ── Formatting helpers ────────────────────────────────────────────────────────
def _hms(seconds: float) -> str:
    s = max(0, int(seconds))
    h, rem = divmod(s, 3600)
    m, s   = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

def _ts() -> str:
    return datetime.now().strftime("%H:%M:%S")

def _sep(n: int = 68) -> str:
    return "─" * n

def _header(text: str) -> None:
    print(f"\n{'═'*68}")
    print(f"  {text}")
    print(f"{'═'*68}")

def _section(label: str) -> None:
    print(f"\n{_sep()}")
    print(f"  {label}")
    print(_sep())


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    t_run_start = time.time()

    _header(f"OpenAlex Snapshot Cache Builder  —  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Snapshot root   : {SNAPSHOT_ROOT}")
    print(f"  Confidence min  : {CONFIDENCE_MIN}")
    print(f"  Report every    : {REPORT_EVERY} authors (write phase)")
    print(f"  Cache path      : {CACHE_PATH}")
    print(f"  Works path      : {WORKS_PATH}")

    # ── 1. Load author IDs ────────────────────────────────────────────────────
    _section("Step 1 / 4 — Load author IDs")
    if not AUTHOR_IDS_PATH.exists():
        print(f"  ERROR: {AUTHOR_IDS_PATH} not found.")
        sys.exit(1)

    author_records: list = []
    with open(AUTHOR_IDS_PATH, encoding="utf-8") as f:
        for line in f:
            try:
                author_records.append(json.loads(line))
            except Exception:
                pass

    min_rank = TIER_RANK.get(CONFIDENCE_MIN, 0)
    eligible = [
        r for r in author_records
        if r.get("openalex_id") and TIER_RANK.get(r.get("match_confidence", "NONE"), 99) <= min_rank
    ]

    print(f"  Author rows loaded  : {len(author_records):,}")
    print(f"  Eligible (≥{CONFIDENCE_MIN})    : {len(eligible):,}")

    # ── 2. Load cache + works-file state ─────────────────────────────────────
    _section("Step 2 / 4 — Load existing cache and works file")
    cache: dict = _load_snapshot_cache(CACHE_PATH)
    print(f"  Cache entries loaded : {len(cache):,}  ({CACHE_PATH.name})")

    done_works_ids: set = set()
    if WORKS_PATH.exists():
        with open(WORKS_PATH, encoding="utf-8") as f:
            for line in f:
                try:
                    done_works_ids.add(json.loads(line)["openalex_id"])
                except Exception:
                    pass
    print(f"  Works IDs on disk    : {len(done_works_ids):,}  ({WORKS_PATH.name})")

    need_scan  = [r for r in eligible if r["openalex_id"] not in cache]
    from_cache = [r for r in eligible if r["openalex_id"] in cache and r["openalex_id"] not in done_works_ids]

    print(f"\n  {'─'*50}")
    print(f"  Need snapshot scan   : {len(need_scan):,}")
    print(f"  Serve from cache     : {len(from_cache):,}  → write to works file, no scan")
    print(f"  Already complete     : {len(eligible) - len(need_scan) - len(from_cache):,}  → skip")

    # ── 2b. Write cache-hits straight to works file ───────────────────────────
    if from_cache:
        print(f"\n  Writing {len(from_cache):,} cached authors to works file …", flush=True)
        t0 = time.time()
        n_yr = 0
        with open(WORKS_PATH, "a", encoding="utf-8") as fout:
            for auth in from_cache:
                wby = cache[auth["openalex_id"]]
                for year in sorted(wby.keys()):
                    fout.write(json.dumps({
                        "openalex_id": auth["openalex_id"],
                        "faculty_id":  auth["faculty_id"],
                        "uni_slug":    auth["uni_slug"],
                        "year":        year,
                        "n_works":     wby[year],
                    }) + "\n")
                    n_yr += 1
        print(f"  Done — {n_yr:,} year-records in {_hms(time.time()-t0)}", flush=True)

    if not need_scan:
        print(f"\n  All eligible authors already cached — snapshot scan skipped.")
        _final_summary(t_run_start)
        return

    # ── 3. Scan PAA shards ────────────────────────────────────────────────────
    paa_dir  = SNAPSHOT_ROOT / "publicationauthoraffiliation"
    p2y_path = SNAPSHOT_ROOT / "pub2year.csv.gz"

    for p, label in [(paa_dir, "publicationauthoraffiliation/"), (p2y_path, "pub2year.csv.gz")]:
        if not p.exists():
            print(f"  ERROR: missing {label}  →  {p}")
            sys.exit(1)

    # Build integer-ID lookup for targets
    target_ints: set  = set()
    int_to_auth: dict = {}
    for auth in need_scan:
        aid = openalex_author_url_to_int(auth["openalex_id"])
        if aid is not None:
            target_ints.add(aid)
            int_to_auth[aid] = auth

    paa_files = sorted(glob.glob(str(paa_dir / "*.csv.gz")))
    n_shards  = len(paa_files)

    _section(f"Step 3a / 4 — PAA shard scan  ({n_shards:,} shards, {len(target_ints):,} target IDs)")
    print(f"  [{_ts()}]  Starting …\n", flush=True)

    pubs_by_author: dict = defaultdict(set)
    t_paa   = time.time()
    t_last  = t_paa
    total_rows = 0
    total_hits = 0
    SHARD_REPORT_SECS = 30    # also report after this many seconds

    for i, fp in enumerate(paa_files, 1):
        shard_rows = 0
        shard_hits = 0
        with gzip.open(fp, "rt", encoding="utf-8", newline="") as gz:
            reader = csv.DictReader(gz)
            for row in reader:
                total_rows += 1
                shard_rows += 1
                try:
                    aid = int(row["AuthorId"])
                    pid = int(row["PublicationId"])
                except (KeyError, ValueError, TypeError):
                    continue
                if aid in target_ints:
                    pubs_by_author[aid].add(pid)
                    shard_hits += 1
                    total_hits += 1

        now     = time.time()
        elapsed = now - t_paa
        inc     = now - t_last
        pct     = i / n_shards * 100
        rate_s  = i / elapsed if elapsed > 0 else 0   # shards/sec
        eta_s   = (n_shards - i) / rate_s if rate_s > 0 else 0
        eta_ts  = datetime.fromtimestamp(now + eta_s).strftime("%H:%M:%S") if rate_s > 0 else "??"

        # Report every N shards (aim for ~15-20 reports total) OR every 30s
        report_every_n = max(1, n_shards // 20)
        if i % report_every_n == 0 or i == n_shards or inc >= SHARD_REPORT_SECS:
            t_last = now
            n_authors_found = sum(1 for v in pubs_by_author.values() if v)
            print(
                f"  [{_ts()}]  Shard {i:>4,}/{n_shards:,}  ({pct:5.1f}%)\n"
                f"    elapsed       : {_hms(elapsed)}   since last report: {inc:.0f}s\n"
                f"    ETA           : {_hms(eta_s)}  (≈ {eta_ts})\n"
                f"    shard rows    : {shard_rows:,}   shard hits: {shard_hits:,}\n"
                f"    cumulative    : {total_rows:,} rows scanned   {total_hits:,} hits\n"
                f"    authors found : {n_authors_found:,} of {len(target_ints):,} have ≥1 pub\n"
                f"    unique pubs   : {sum(len(v) for v in pubs_by_author.values()):,}",
                flush=True,
            )
            print(f"  {_sep(50)}")

    all_pids = set()
    for s in pubs_by_author.values():
        all_pids.update(s)

    paa_elapsed = time.time() - t_paa
    print(f"\n  PAA scan finished in {_hms(paa_elapsed)}")
    print(f"  Total rows scanned    : {total_rows:,}")
    print(f"  Unique pub IDs found  : {len(all_pids):,}")
    print(f"  Authors with ≥1 pub   : {sum(1 for v in pubs_by_author.values() if v):,}")
    print(f"  Authors with 0 pubs   : {len(target_ints) - sum(1 for v in pubs_by_author.values() if v):,}  (will be cached as empty)", flush=True)

    # ── 3b. Scan pub2year ─────────────────────────────────────────────────────
    _section(f"Step 3b / 4 — pub2year scan  ({len(all_pids):,} target pub IDs)")
    print(f"  [{_ts()}]  Starting …\n", flush=True)

    pub_year: dict = {}
    t_p2y  = time.time()
    t_last = t_p2y
    rows_p2y   = 0
    matched_p2y = 0

    with gzip.open(p2y_path, "rt", encoding="utf-8", newline="") as gz:
        reader = csv.DictReader(gz)
        for row in reader:
            rows_p2y += 1
            try:
                pid = int(row["PublicationId"])
            except (KeyError, ValueError, TypeError):
                continue
            if pid not in all_pids:
                continue
            try:
                y = int(row["Year"])
            except (KeyError, ValueError, TypeError):
                continue
            pub_year[pid] = y
            matched_p2y += 1

            now = time.time()
            if now - t_last >= 60:
                t_last   = now
                elapsed  = now - t_p2y
                pct_done = matched_p2y / len(all_pids) * 100 if all_pids else 0
                print(
                    f"  [{_ts()}]  pub2year rows: {rows_p2y:,}\n"
                    f"    pubs matched  : {matched_p2y:,} / {len(all_pids):,}  ({pct_done:.1f}%)\n"
                    f"    elapsed       : {_hms(elapsed)}",
                    flush=True,
                )
                print(f"  {_sep(50)}")

    p2y_elapsed = time.time() - t_p2y
    print(f"\n  pub2year finished in {_hms(p2y_elapsed)}")
    print(f"  Rows scanned     : {rows_p2y:,}")
    print(f"  Pub IDs matched  : {matched_p2y:,} / {len(all_pids):,}", flush=True)

    # ── 4. Aggregate + write ──────────────────────────────────────────────────
    n_total = len(need_scan)
    _section(f"Step 4 / 4 — Aggregate & write  ({n_total:,} authors, every {REPORT_EVERY})")
    print(f"  [{_ts()}]  Starting …\n", flush=True)

    n_authors_written  = 0
    n_records_written  = 0
    n_zero_pub         = 0
    new_cache_entries: dict = {}
    t_write    = time.time()
    t_last     = t_write
    t_ckpt     = t_write

    with open(WORKS_PATH, "a", encoding="utf-8") as fworks:
        for i, auth in enumerate(need_scan, 1):
            aid   = openalex_author_url_to_int(auth["openalex_id"])
            pids  = pubs_by_author.get(aid, set()) if aid else set()
            counts = Counter()
            for pid in pids:
                y = pub_year.get(pid)
                if y is not None:
                    counts[y] += 1

            if not counts:
                n_zero_pub += 1

            # Always cache, even 0-pub authors — prevents re-scanning them
            new_cache_entries[auth["openalex_id"]] = dict(counts)

            for year in sorted(counts.keys()):
                fworks.write(json.dumps({
                    "openalex_id": auth["openalex_id"],
                    "faculty_id":  auth["faculty_id"],
                    "uni_slug":    auth["uni_slug"],
                    "year":        year,
                    "n_works":     counts[year],
                }) + "\n")
                n_records_written += 1
            fworks.flush()
            n_authors_written += 1

            # Flush cache to disk periodically — safe interrupt recovery
            now = time.time()
            if len(new_cache_entries) >= CACHE_FLUSH_N or (now - t_ckpt) >= CACHE_FLUSH_SECS:
                _append_snapshot_cache(new_cache_entries, CACHE_PATH)
                new_cache_entries = {}
                t_ckpt = now

            # ── Progress report ───────────────────────────────────────────────
            if i % REPORT_EVERY == 0 or i == n_total:
                now          = time.time()
                elapsed_tot  = now - t_write
                elapsed_inc  = now - t_last
                t_last       = now

                rate     = i / elapsed_tot if elapsed_tot > 0 else 0    # authors/sec
                avg_ms   = elapsed_tot / i * 1000 if i > 0 else 0       # ms/author
                eta_s    = (n_total - i) / rate if rate > 0 else 0
                eta_ts   = (datetime.fromtimestamp(now + eta_s).strftime("%H:%M:%S")
                            if rate > 0 else "??:??:??")
                pct      = i / n_total * 100

                print(
                    f"  [{_ts()}]  Authors {i:>5,} / {n_total:,}  ({pct:5.1f}%)\n"
                    f"    elapsed total : {_hms(elapsed_tot)}   since last report: {elapsed_inc:.1f}s\n"
                    f"    year-records  : {n_records_written:,}   zero-pub authors so far: {n_zero_pub:,}\n"
                    f"    avg per author: {avg_ms:.1f}ms   rate: {rate*60:.1f} authors/min\n"
                    f"    ETA remaining : {_hms(eta_s)}  (≈ {eta_ts})",
                    flush=True,
                )
                print(f"  {_sep(50)}")

    # Final cache flush
    if new_cache_entries:
        _append_snapshot_cache(new_cache_entries, CACHE_PATH)

    write_elapsed = time.time() - t_write
    print(f"\n  Write phase finished in {_hms(write_elapsed)}")
    print(f"  Authors written   : {n_authors_written:,}")
    print(f"  Year-records      : {n_records_written:,}")
    print(f"  Zero-pub authors  : {n_zero_pub:,}  (cached — won't be re-scanned)", flush=True)

    _final_summary(t_run_start)


def _final_summary(t_start: float) -> None:
    elapsed = time.time() - t_start
    print(f"\n{'═'*68}")
    print(f"  ALL DONE")
    print(f"  Total elapsed    : {_hms(elapsed)}")
    print(f"  Finished         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for path in (CACHE_PATH, WORKS_PATH):
        if path.exists():
            mb = path.stat().st_size / 1e6
            # count lines
            with open(path) as f:
                n = sum(1 for _ in f)
            print(f"  {path.name:<45}  {n:>8,} lines   {mb:.1f} MB")
    print(f"{'═'*68}\n")


if __name__ == "__main__":
    main()
