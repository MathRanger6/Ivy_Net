"""
openalex_resolver.py  —  Stage 6: OpenAlex Author ID Resolution + Works Fetch
==============================================================================
Two-phase pipeline:

  Phase A  resolve_authors()
    For each unique faculty member in the panel, search OpenAlex by name +
    institution and assign an OpenAlex Author ID with a confidence score.
    Output: openalex_author_ids.jsonl

  Phase B  fetch_works_by_year()
    For each resolved author, aggregate publication counts by calendar year.
    Output: openalex_works_by_year.jsonl

Data source for Phase B
-----------------------
* **API (default):** ``https://api.openalex.org`` group_by on works
  (see ``_get`` / ``_BASE``) — one HTTP request per author.

* **Bulk snapshot (optional):** pass ``snapshot_root`` to ``fetch_works_by_year``,
  pointing at an OpenAlex-style tree such as ``~/cdh/OpenAlex1125`` on Rivanna.
  Uses **relational CSV exports** (not ``data/works`` JSONL):

  - ``publicationauthoraffiliation/*.csv.gz`` — PublicationId ↔ AuthorId
  - ``pub2year.csv.gz`` (at snapshot root) — PublicationId → Year

  This performs full scans of those tables (batch/HPC use); no API key required
  for Phase B in that mode.

API courtesy
------------
Requests use ``mailto=`` from env ``OPENALEX_MAILTO`` and optional Bearer
``OPENALEX_API_KEY`` (see module-level config). Polite spacing between requests
is controlled by ``_DELAY``.

Confidence tiers
----------------
  HIGH    name match + institution in author's affiliations
          + panel years overlap with affiliation years
  MEDIUM  name match + institution in affiliations, but year overlap unclear
  LOW     name match only — institution not found in affiliations
  NONE    no OpenAlex result returned
  MULTI   multiple HIGH/MEDIUM candidates — needs human review

Citation
--------
Priem, J., Piwowar, H., & Orr, R. (2022). OpenAlex: A fully-open index of
scholarly works, authors, venues, institutions, and concepts. ArXiv.
https://arxiv.org/abs/2205.01833
"""

import csv
import glob
import gzip
import json
import os
import time
import re
import unicodedata
from collections import Counter, defaultdict, deque
from pathlib import Path

from tqdm.auto import tqdm
from urllib.request import urlopen, Request
from urllib.parse import urlencode, quote
from urllib.error import HTTPError, URLError
from functionsG_working import tyme


class RateLimitExhausted(Exception):
    """Raised when OpenAlex returns 429 on every retry — daily quota likely hit."""
    pass

# ---------------------------------------------------------------------------
# API config  (secrets: set OPENALEX_API_KEY in environment or workspace `.env` — not committed)
# ---------------------------------------------------------------------------
_MAILTO = (os.environ.get("OPENALEX_MAILTO") or "").strip()
_BASE = "https://api.openalex.org"
_DELAY = 1.0  # seconds between requests — standard rate until elevated limit confirmed
# Bearer token optional; without it OpenAlex uses the polite pool (mailto-only).
_k = (os.environ.get("OPENALEX_API_KEY") or "").strip()
_API_KEY = _k if _k else None
_TIMEOUT   = 20        # seconds per HTTP request
_MAX_RETRY = 3         # retries on transient errors

# ---------------------------------------------------------------------------
# API metrics (module-level, reset by calling reset_api_metrics())
# ---------------------------------------------------------------------------
_api_metrics = {
    "n_calls":      0,       # total HTTP GETs attempted
    "n_ok":         0,       # 200 OK responses
    "n_empty":      0,       # 200 OK but zero results
    "n_429":        0,       # rate-limit hits
    "n_5xx":        0,       # server errors
    "n_timeout":    0,       # URLError / OSError (network / timeout)
    "n_other_err":  0,       # other HTTP errors
    "latencies":    deque(maxlen=200),  # rolling window of response times (s)
}


def reset_api_metrics():
    """Reset all API counters — call before starting a new resolve pass."""
    _api_metrics.update({
        "n_calls": 0, "n_ok": 0, "n_empty": 0,
        "n_429": 0, "n_5xx": 0, "n_timeout": 0, "n_other_err": 0,
    })
    _api_metrics["latencies"] = deque(maxlen=200)


def api_metrics_line() -> str:
    """One-line summary of current API health."""
    m   = _api_metrics
    lat = _api_metrics["latencies"]
    avg_ms = (sum(lat) / len(lat) * 1000) if lat else 0
    p95_ms = (sorted(lat)[int(len(lat) * 0.95)] * 1000) if len(lat) >= 20 else 0
    err    = m["n_429"] + m["n_5xx"] + m["n_timeout"] + m["n_other_err"]
    ok_pct = m["n_ok"] / max(m["n_calls"], 1) * 100
    p95_str = f"  p95 {p95_ms:.0f}ms" if p95_ms else ""
    return (
        f"API: {m['n_calls']:,} calls  {ok_pct:.1f}% OK  "
        f"avg {avg_ms:.0f}ms{p95_str}  │  "
        f"429×{m['n_429']}  5xx×{m['n_5xx']}  timeout×{m['n_timeout']}  "
        f"empty×{m['n_empty']}"
    )


def _get(endpoint: str, params: dict) -> dict:
    """GET a JSON endpoint with retries, polite delay, and metric tracking."""
    params = {**params, "mailto": _MAILTO}
    url    = f"{_BASE}/{endpoint}?{urlencode(params)}"
    _api_metrics["n_calls"] += 1

    _ua = f"TenurePipeline/1.0 ({_MAILTO})" if _MAILTO else "TenurePipeline/1.0"
    headers = {"User-Agent": _ua}
    if _API_KEY:
        headers["Authorization"] = f"Bearer {_API_KEY}"

    n_429_hits = 0
    for attempt in range(_MAX_RETRY):
        t0 = time.time()
        try:
            req  = Request(url, headers=headers)
            resp = urlopen(req, timeout=_TIMEOUT)
            data = json.loads(resp.read().decode("utf-8"))
            _api_metrics["latencies"].append(time.time() - t0)
            _api_metrics["n_ok"] += 1
            if not data.get("results") and not data.get("group_by"):
                _api_metrics["n_empty"] += 1
            return data
        except HTTPError as e:
            if e.code == 429:
                _api_metrics["n_429"] += 1
                n_429_hits += 1
                if n_429_hits >= _MAX_RETRY:
                    # Daily/hourly quota exhausted — stop the whole run cleanly
                    raise RateLimitExhausted(
                        f"OpenAlex returned 429 on all {_MAX_RETRY} retries. "
                        "Daily quota likely hit. Resume tomorrow or after limit resets."
                    )
                wait = 30 * n_429_hits   # 30s → 60s → 90s (short — quota won't reset in minutes)
                print(f"    429 rate-limit — waiting {wait}s before retry {attempt+1}/{_MAX_RETRY} …", flush=True)
                time.sleep(wait)
            elif e.code in (500, 502, 503):
                _api_metrics["n_5xx"] += 1
                time.sleep(5 * (attempt + 1))
            else:
                _api_metrics["n_other_err"] += 1
                return {}
        except (URLError, OSError):
            _api_metrics["n_timeout"] += 1
            time.sleep(5 * (attempt + 1))
    return {}


# ---------------------------------------------------------------------------
# Institution slug → OpenAlex ROR mapping  (Phase A, Step 1)
# ---------------------------------------------------------------------------

def resolve_institutions(uni_slugs: list, delay: float = _DELAY) -> dict:
    """
    Search OpenAlex for each university slug → return {uni_slug: institution_record}.
    institution_record keys: id, display_name, ror, country_code
    """
    mapping = {}
    for slug in uni_slugs:
        # Convert slug to a human-readable search string
        name = slug.replace("_", " ").replace(" university", "").strip()
        # Add "university" back for search — helps disambiguation
        query = slug.replace("_", " ").title()
        data  = _get("institutions", {"search": query, "per_page": 5})
        results = data.get("results", [])
        if results:
            # Pick highest-relevance result (first) — usually correct for R1 universities
            inst = results[0]
            mapping[slug] = {
                "id":           inst.get("id", ""),
                "display_name": inst.get("display_name", ""),
                "ror":          inst.get("ror", ""),
                "country_code": inst.get("country_code", ""),
            }
        else:
            mapping[slug] = None
        time.sleep(delay)
    return mapping


# ---------------------------------------------------------------------------
# Name normalisation (same logic as faculty_linker, kept local for independence)
# ---------------------------------------------------------------------------

def _norm(name: str) -> str:
    s = str(name).strip()
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"\s+(junior|senior|jr\.?|sr\.?|ii|iii|iv|v)\s*$", "", s, flags=re.I)
    s = re.sub(r"\b[a-z]\.\s*", " ", s)
    s = re.sub(r"(?<=\s)[a-z](?=\s)", " ", s)
    s = re.sub(r"['\-]", " ", s)
    s = re.sub(r"[^a-z0-9\s]", "", s)
    return re.sub(r"\s+", " ", s).strip()


# ---------------------------------------------------------------------------
# Phase A: Author ID resolution
# ---------------------------------------------------------------------------

def _score_candidate(candidate: dict, name_key: str, uni_slug: str,
                     inst_id: str, panel_years: set) -> str:
    """Return confidence tier for a single OpenAlex author candidate."""
    # Name similarity
    cand_key = _norm(candidate.get("display_name", ""))
    if cand_key != name_key:
        # Allow last-name + first-initial match as fallback
        cand_parts = cand_key.split()
        name_parts = name_key.split()
        if not (cand_parts and name_parts and cand_parts[-1] == name_parts[-1]):
            return "NONE"

    # Check institution affiliations
    affiliations = candidate.get("affiliations", []) or []
    inst_match   = False
    year_overlap = False

    for aff in affiliations:
        aff_inst = aff.get("institution") or {}
        aff_id   = aff_inst.get("id", "")
        aff_name = _norm(aff_inst.get("display_name", ""))
        slug_words = set(uni_slug.replace("_", " ").split())

        if (inst_id and aff_id == inst_id) or (slug_words & set(aff_name.split())):
            inst_match = True
            aff_years  = set(aff.get("years", []))
            if panel_years & aff_years:
                year_overlap = True
            break

    if inst_match and year_overlap:
        return "HIGH"
    if inst_match:
        return "MEDIUM"
    return "LOW"


def _hms(seconds: float) -> str:
    """Format seconds as H:MM:SS."""
    s = max(0, int(seconds))
    h, rem = divmod(s, 3600)
    m, s   = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def resolve_authors(panel_records: list,
                    inst_map: dict,
                    out_path: Path,
                    delay: float = _DELAY,
                    skip_done: bool = True,
                    report_every: int = 25) -> list:
    """
    Search OpenAlex for every unique faculty member in panel_records.

    Parameters
    ----------
    panel_records : list[dict]  — from faculty_panel.jsonl
    inst_map      : dict        — {uni_slug: institution_record} from resolve_institutions()
    out_path      : Path        — write JSONL results here incrementally
    delay         : float       — seconds between API requests
    skip_done     : bool        — skip faculty_ids already in out_path
    report_every  : int         — print progress every N authors

    Returns
    -------
    list[dict]  — one record per unique faculty member:
        faculty_id, name_display, uni_slug, university,
        openalex_id, openalex_name, match_confidence,
        works_count, cited_by_count, orcid
    """
    out_path = Path(out_path)

    # Checkpoint: load already-resolved IDs
    done_ids: set = set()
    if skip_done and out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done_ids.add(json.loads(line)["faculty_id"])
                except Exception:
                    pass

    # Build unique faculty list from panel, grouped by school for banner printing
    seen: dict = {}
    for r in panel_records:
        fid = r["faculty_id"]
        if fid not in seen:
            seen[fid] = {
                "faculty_id":   fid,
                "name_display": r["name_display"],
                "name_key":     r["name_key"],
                "uni_slug":     r["uni_slug"],
                "university":   r["university"],
                "years":        set(),
            }
        seen[fid]["years"].add(r["year"])

    todo = [v for k, v in seen.items() if k not in done_ids]
    n_todo = len(todo)

    # ── Pre-run plan ──────────────────────────────────────────────────────────
    est_total_sec = n_todo * delay
    key_status = "API key set (Bearer)" if _API_KEY else "no API key — polite pool only"
    print(f"\n  Faculty to resolve : {n_todo:,}  ({len(done_ids):,} already done, {len(seen):,} total)")
    print(f"  API delay          : {delay:.2f}s / request  │  {key_status}")
    print(f"  Est. total time    : {_hms(est_total_sec)}  (network latency will add ~30–60%)")
    print(f"  Reporting every    : {report_every} authors")
    print(f"  Output             : {out_path.name}")
    print(f"  {'─'*60}")

    if not todo:
        return []

    reset_api_metrics()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    results       = []
    t_start       = time.time()
    t_last_report = t_start
    conf_counts   = {t: 0 for t in ("HIGH", "MEDIUM", "LOW", "MULTI", "NONE")}
    cur_school    = None

    with open(out_path, "a", encoding="utf-8") as fout:
        for i, fac in enumerate(todo, 1):
            slug      = fac["uni_slug"]
            inst_rec  = inst_map.get(slug) or {}
            inst_id   = inst_rec.get("id", "")
            name_key  = fac["name_key"]
            panel_yrs = fac["years"]

            # School transition banner
            if slug != cur_school:
                cur_school = slug
                school_n   = sum(1 for f in todo[i-1:] if f["uni_slug"] == slug)
                print(f"\n  ── {fac['university']}  ({school_n} faculty)", flush=True)

            # Build search
            params = {"search": fac["name_display"], "per_page": 10}
            if inst_id:
                params["filter"] = f"affiliations.institution.id:{inst_id}"

            try:
                data = _get("authors", params)
            except RateLimitExhausted as exc:
                print(f"\n  *** RATE LIMIT EXHAUSTED after {i-1:,} authors ***")
                print(f"  {exc}")
                print(f"  Checkpoint saved through author {i-1:,} of {n_todo:,}.")
                print(f"  Re-run Cell 6A tomorrow — it will resume from here.\n")
                break
            candidates = data.get("results", [])

            # Score candidates
            scored = []
            for cand in candidates:
                tier = _score_candidate(cand, name_key, slug, inst_id, panel_yrs)
                if tier != "NONE":
                    scored.append((tier, cand))

            high   = [c for t, c in scored if t == "HIGH"]
            medium = [c for t, c in scored if t == "MEDIUM"]
            low    = [c for t, c in scored if t == "LOW"]

            if len(high) == 1:
                best, confidence = high[0], "HIGH"
            elif len(high) > 1:
                best, confidence = high[0], "MULTI"
            elif len(medium) == 1:
                best, confidence = medium[0], "MEDIUM"
            elif len(medium) > 1:
                best, confidence = medium[0], "MULTI"
            elif len(low) == 1:
                best, confidence = low[0], "LOW"
            else:
                best, confidence = None, "NONE"

            conf_counts[confidence] += 1

            record = {
                "faculty_id":       fac["faculty_id"],
                "name_display":     fac["name_display"],
                "uni_slug":         slug,
                "university":       fac["university"],
                "openalex_id":      best.get("id", "")           if best else "",
                "openalex_name":    best.get("display_name", "") if best else "",
                "match_confidence": confidence,
                "works_count":      best.get("works_count", 0)   if best else 0,
                "cited_by_count":   best.get("cited_by_count", 0) if best else 0,
                "orcid":            best.get("orcid", "")         if best else "",
                "n_candidates":     len(candidates),
            }

            fout.write(json.dumps(record) + "\n")
            fout.flush()
            results.append(record)

            # ── Periodic progress report ──────────────────────────────────────
            now     = time.time()
            elapsed = now - t_start
            rate    = i / elapsed if elapsed > 0 else 0          # authors/sec
            remain  = (n_todo - i) / rate if rate > 0 else 0    # seconds left
            pct     = i / n_todo * 100

            if i % report_every == 0 or i == n_todo or (now - t_last_report) >= 60:
                t_last_report = now
                high_pct = conf_counts['HIGH'] / i * 100
                print(
                    f"  [{i:>5,}/{n_todo:,}] {pct:5.1f}%  "
                    f"elapsed {_hms(elapsed)}  ETA {_hms(remain)}  "
                    f"rate {rate*60:.0f}/min\n"
                    f"    match → HIGH {conf_counts['HIGH']:,}({high_pct:.0f}%)  "
                    f"MED {conf_counts['MEDIUM']:,}  "
                    f"LOW {conf_counts['LOW']:,}  "
                    f"MULTI {conf_counts['MULTI']:,}  "
                    f"NONE {conf_counts['NONE']:,}\n"
                    f"    {api_metrics_line()}",
                    flush=True
                )

            time.sleep(delay)

    # ── Final summary ─────────────────────────────────────────────────────────
    total_elapsed = time.time() - t_start
    actual_rate   = n_todo / total_elapsed if total_elapsed > 0 else 0
    print(f"\n  {'─'*60}")
    print(f"  Resolved {n_todo:,} authors in {_hms(total_elapsed)}  ({actual_rate*60:.0f}/min)")
    print(f"  HIGH {conf_counts['HIGH']:,}  MEDIUM {conf_counts['MEDIUM']:,}  "
          f"LOW {conf_counts['LOW']:,}  MULTI {conf_counts['MULTI']:,}  "
          f"NONE {conf_counts['NONE']:,}")
    print(f"  {api_metrics_line()}")

    return results


# ---------------------------------------------------------------------------
# Phase B helpers: snapshot cache (persistent, incremental)
# ---------------------------------------------------------------------------

def _load_snapshot_cache(cache_path: Path) -> dict:
    """
    Load openalex_snapshot_cache.jsonl → {openalex_id: {year: n_works}}.
    Returns empty dict if file does not exist.
    """
    cache = {}
    cache_path = Path(cache_path)
    if not cache_path.exists():
        return cache
    with open(cache_path, encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
                oa_id = rec.get("openalex_id")
                wby = rec.get("works_by_year")
                if oa_id and isinstance(wby, dict):
                    cache[oa_id] = {int(k): v for k, v in wby.items()}
            except Exception:
                pass
    return cache


def _append_snapshot_cache(new_entries: dict, cache_path: Path) -> None:
    """
    Append new {openalex_id: {year: n_works}} entries to the cache file.
    Each author gets one line.
    """
    cache_path = Path(cache_path)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "a", encoding="utf-8") as f:
        for oa_id, works_by_year in new_entries.items():
            rec = {
                "openalex_id":   oa_id,
                "works_by_year": {str(k): v for k, v in sorted(works_by_year.items())},
            }
            f.write(json.dumps(rec) + "\n")


# ---------------------------------------------------------------------------
# Phase B helpers: bulk snapshot (CDH / OpenAlex relational CSVs)
# ---------------------------------------------------------------------------

def openalex_author_url_to_int(openalex_id: str):
    """
    Map an API-style OpenAlex author id (URL or ``A123...``) to the integer
    ``AuthorId`` used in ``publicationauthoraffiliation*.csv.gz``.
    """
    if not openalex_id:
        return None
    s = str(openalex_id).strip()
    s = s.replace("https://openalex.org/", "")
    if s.startswith("A"):
        s = s[1:]
    try:
        return int(s)
    except ValueError:
        return None


def _fetch_works_by_year_snapshot(
    author_records: list,
    out_path: Path,
    snapshot_root: Path,
    confidence_min: str,
    skip_done: bool,
    cache_path: Path = None,
) -> list:
    """
    Build the same JSONL as the API path using:

      * ``publicationauthoraffiliation/*.csv.gz`` — link AuthorId → PublicationId
      * ``pub2year.csv.gz`` — PublicationId → Year

    With incremental cache
    ---------------------
    If ``cache_path`` is provided (recommended), extracted works-by-year data is
    stored in ``openalex_snapshot_cache.jsonl``.  On subsequent runs only
    **new** author IDs — not already in the cache — trigger a snapshot scan.
    This means adding schools later costs only a marginal scan for the new
    authors, not a full re-scan of the entire snapshot.

    Cache format: one line per author —
        {"openalex_id": "...", "works_by_year": {"2010": 1, "2015": 3, ...}}
    """
    TIER_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "MULTI": 3, "NONE": 4}
    min_rank = TIER_RANK.get(confidence_min, 1)

    out_path = Path(out_path)
    done_ids: set = set()
    if skip_done and out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done_ids.add(json.loads(line)["openalex_id"])
                except Exception:
                    pass

    def _eligible(r: dict) -> bool:
        return bool(r.get("openalex_id")) and (
            TIER_RANK.get(r.get("match_confidence", "NONE"), 99) <= min_rank
        )

    eligible  = [r for r in author_records if _eligible(r)]
    # Authors not yet in out_path at all
    need_out  = [r for r in eligible if r["openalex_id"] not in done_ids]

    # ── Cache layer ───────────────────────────────────────────────────────────
    cache: dict = {}   # {openalex_id: {year(int): n_works}}
    if cache_path is not None:
        cache_path = Path(cache_path)
        cache = _load_snapshot_cache(cache_path)
        n_cached = len(cache)
    else:
        n_cached = 0

    # Authors that need output AND are already in the cache (no scan needed)
    from_cache  = [r for r in need_out if r["openalex_id"] in cache]
    # Authors that need output AND are NOT in the cache (need snapshot scan)
    need_scan   = [r for r in need_out if r["openalex_id"] not in cache]
    n_todo      = len(need_scan)

    print(f"\n  Authors eligible (≥{confidence_min}) : {len(eligible):,}  (from {len(author_records):,} rows)")
    print(f"  Already in output  : {len(done_ids):,}")
    print(f"  Cache loaded       : {n_cached:,} authors  "
          f"({'no cache file' if cache_path is None else cache_path.name})")
    print(f"  Served from cache  : {len(from_cache):,}")
    print(f"  Need snapshot scan : {n_todo:,}")
    print(f"  {'─'*60}")

    # ── Write cache-hits to output first ─────────────────────────────────────
    results = []
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if from_cache:
        with open(out_path, "a", encoding="utf-8") as fout:
            for auth in from_cache:
                wby = cache[auth["openalex_id"]]
                for year in sorted(wby.keys()):
                    rec = {
                        "openalex_id": auth["openalex_id"],
                        "faculty_id":  auth["faculty_id"],
                        "uni_slug":    auth["uni_slug"],
                        "year":        year,
                        "n_works":     wby[year],
                    }
                    fout.write(json.dumps(rec) + "\n")
                    results.append(rec)
        print(f"  Wrote {len(results):,} year-records from cache (no snapshot scan needed).")

    if not need_scan:
        print(f"\n  {'─'*60}")
        print(f"  All {len(eligible):,} eligible authors served from cache + existing output — snapshot scan skipped.")
        return results

    # ── Snapshot scan for uncached authors ────────────────────────────────────
    target_ints: set = set()
    int_to_auth: dict = {}
    for auth in need_scan:
        aid = openalex_author_url_to_int(auth["openalex_id"])
        if aid is None:
            continue
        target_ints.add(aid)
        int_to_auth[aid] = auth

    if not target_ints:
        print("  Nothing to scan — could not parse any OpenAlex author ids for the todo list.")
        return results

    paa_dir  = snapshot_root / "publicationauthoraffiliation"
    p2y_path = snapshot_root / "pub2year.csv.gz"

    pubs_by_author: dict = defaultdict(set)
    paa_files = sorted(glob.glob(str(paa_dir / "*.csv.gz")))
    if not paa_files:
        print(f"  ERROR: no *.csv.gz under {paa_dir}")
        return results

    n_shards = len(paa_files)
    report_every_shards = max(1, n_shards // 20)  # report every ~5%
    print(f"  Scanning {n_shards:,} PAA shards for {len(target_ints):,} new author IDs …")
    print(f"  (progress every {report_every_shards} shards / ~5%)", flush=True)
    _t_paa_start = time.time()
    for i, fp in enumerate(paa_files, 1):
        with gzip.open(fp, "rt", encoding="utf-8", newline="") as gz:
            reader = csv.DictReader(gz)
            for row in reader:
                try:
                    aid = int(row["AuthorId"])
                    pid = int(row["PublicationId"])
                except (KeyError, ValueError, TypeError):
                    continue
                if aid in target_ints:
                    pubs_by_author[aid].add(pid)
        if i % report_every_shards == 0 or i == n_shards:
            pct = i / n_shards * 100
            elapsed = time.time() - _t_paa_start
            rate = i / elapsed if elapsed > 0 else 0
            eta = (n_shards - i) / rate if rate > 0 else 0
            print(
                f"  PAA shards: {i:,}/{n_shards:,} ({pct:.0f}%)  "
                f"hits so far: {sum(len(v) for v in pubs_by_author.values()):,}  "
                f"elapsed: {_hms(elapsed)}  ETA: {_hms(eta)}",
                flush=True,
            )

    all_pids: set = set()
    for s in pubs_by_author.values():
        all_pids.update(s)

    print(f"  Unique publication ids for target authors : {len(all_pids):,}")

    # Use compressed file size as a proxy for progress — gzip doesn't expose total
    # decompressed row count up front, but bytes-read / total-bytes is a reliable
    # ~95% accurate proxy for fraction-complete and gives a usable ETA.
    _p2y_file_bytes = p2y_path.stat().st_size
    print(
        f"  Scanning pub2year.csv.gz  "
        f"({_p2y_file_bytes / 1_073_741_824:.2f} GB compressed) …",
        flush=True,
    )

    pub_year: dict = {}
    _p2y_rows = 0
    _p2y_hits = 0
    _t_p2y_start = time.time()
    _last_p2y_report = _t_p2y_start

    # Open the raw file in binary mode so we can track compressed bytes read;
    # wrap it with gzip so the CSV reader still sees plain text.
    with open(p2y_path, "rb") as _raw:
        with gzip.open(_raw, "rt", encoding="utf-8", newline="") as gz:
            reader = csv.DictReader(gz)
            for row in reader:
                _p2y_rows += 1
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
                _p2y_hits += 1
                # Report every 60 seconds with %, ETA, and hits-vs-needed
                _now = time.time()
                if _now - _last_p2y_report >= 60:
                    _last_p2y_report = _now
                    _elapsed = _now - _t_p2y_start
                    _bytes_done = _raw.tell()
                    _pct = _bytes_done / _p2y_file_bytes * 100 if _p2y_file_bytes else 0
                    _rate = _bytes_done / _elapsed if _elapsed > 0 else 1
                    _eta = (_p2y_file_bytes - _bytes_done) / _rate if _rate > 0 else 0
                    print(
                        f"  pub2year: {_pct:.1f}%  "
                        f"rows: {_p2y_rows:,}  "
                        f"hits: {_p2y_hits:,}/{len(all_pids):,}  "
                        f"elapsed: {_hms(_elapsed)}  ETA: {_hms(_eta)}",
                        flush=True,
                    )

    # ── Aggregate, write output, and update cache ─────────────────────────────
    new_cache_entries: dict = {}
    t_start = time.time()

    with open(out_path, "a", encoding="utf-8") as fout:
        for i, auth in enumerate(need_scan, 1):
            aid = openalex_author_url_to_int(auth["openalex_id"])
            if aid is None:
                continue
            pids   = pubs_by_author.get(aid)
            counts = Counter()
            if pids:
                for pid in pids:
                    y = pub_year.get(pid)
                    if y is not None:
                        counts[y] += 1
            # Always cache (even authors with 0 publications) to avoid re-scanning
            new_cache_entries[auth["openalex_id"]] = dict(counts)
            for year in sorted(counts.keys()):
                rec = {
                    "openalex_id": auth["openalex_id"],
                    "faculty_id":  auth["faculty_id"],
                    "uni_slug":    auth["uni_slug"],
                    "year":        year,
                    "n_works":     counts[year],
                }
                fout.write(json.dumps(rec) + "\n")
                results.append(rec)
            fout.flush()

            if i % 100 == 0 or i == n_todo:
                elapsed = time.time() - t_start
                rate    = i / elapsed if elapsed > 0 else 0
                remain  = (n_todo - i) / rate if rate > 0 else 0
                print(
                    f"  [{i:>5,}/{n_todo:,}] {i/n_todo*100:5.1f}%  "
                    f"elapsed {_hms(elapsed)}  ETA {_hms(remain)}  "
                    f"rate {rate*60:.0f}/min  │  {len(results):,} year-records written",
                    flush=True,
                )

    # Persist new cache entries
    if new_cache_entries and cache_path is not None:
        _append_snapshot_cache(new_cache_entries, cache_path)
        print(f"  Cache updated — appended {len(new_cache_entries):,} authors to {cache_path.name}")

    total_elapsed = time.time() - t_start
    print(f"\n  {'─'*60}")
    print(f"  Scanned snapshot for {n_todo:,} new authors in {_hms(total_elapsed)}")
    print(f"  Total year-records this run : {len(results):,}")
    return results


# ---------------------------------------------------------------------------
# Phase B helpers: cache-only mode (Mac / no snapshot access)
# ---------------------------------------------------------------------------

def _fetch_works_by_year_cache_only(
    author_records: list,
    out_path: Path,
    cache_path: Path,
    confidence_min: str,
    skip_done: bool,
    api_fallback: bool,
    delay: float,
) -> list:
    """
    Serve works-by-year from the snapshot cache — no HPC or snapshot required.

    Called by ``fetch_works_by_year`` when the snapshot root is unreachable
    (e.g. running on a laptop away from the HPC).  Two sub-cases:

    All authors in cache
        Write to output immediately.  No scan, no API.  Fast.

    Some authors NOT in cache
        Write the cached ones, then:
        - If ``api_fallback=False`` (default / recommended):
          Print exact SSH + rsync commands to run the cache builder on Rivanna
          and sync the result back.  Return what was written from cache.
        - If ``api_fallback=True``:
          Use the OpenAlex API for the uncached subset.  Slow and rate-limited
          but functional as a temporary fallback.
    """
    TIER_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "MULTI": 3, "NONE": 4}
    min_rank  = TIER_RANK.get(confidence_min, 1)
    out_path  = Path(out_path)

    # Load existing output to honour skip_done
    done_ids: set = set()
    if skip_done and out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done_ids.add(json.loads(line)["openalex_id"])
                except Exception:
                    pass

    def _eligible(r: dict) -> bool:
        return bool(r.get("openalex_id")) and (
            TIER_RANK.get(r.get("match_confidence", "NONE"), 99) <= min_rank
        )

    eligible = [r for r in author_records if _eligible(r)]
    need_out = [r for r in eligible if r["openalex_id"] not in done_ids]

    cache      = _load_snapshot_cache(cache_path)
    from_cache = [r for r in need_out if r["openalex_id"] in cache]
    uncached   = [r for r in need_out if r["openalex_id"] not in cache]

    print(f"\n  Stage 6B — cache-only mode  (snapshot root not accessible on this machine)")
    print(f"  {'─'*60}")
    print(f"  Cache file        : {cache_path.name}  ({len(cache):,} authors cached)")
    print(f"  Eligible (≥{confidence_min})   : {len(eligible):,}  (from {len(author_records):,} rows)")
    print(f"  Already in output : {len(done_ids):,}  (skip_done)")
    print(f"  Served from cache : {len(from_cache):,}")
    print(f"  Not in cache yet  : {len(uncached):,}")
    if uncached:
        status = "→ API fallback ENABLED" if api_fallback else "→ instructions below"
        print(f"  Uncached action   : {status}")
    print(f"  {'─'*60}")

    results: list = []

    # ── Write cache-hits straight to output ──────────────────────────────────
    if from_cache:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "a", encoding="utf-8") as fout:
            for auth in from_cache:
                wby = cache[auth["openalex_id"]]
                for year in sorted(wby.keys()):
                    rec = {
                        "openalex_id": auth["openalex_id"],
                        "faculty_id":  auth["faculty_id"],
                        "uni_slug":    auth["uni_slug"],
                        "year":        year,
                        "n_works":     wby[year],
                    }
                    fout.write(json.dumps(rec) + "\n")
                    results.append(rec)
        print(f"  Wrote {len(results):,} year-records from cache.")

    # ── Handle uncached authors ───────────────────────────────────────────────
    if not uncached:
        print(f"\n  All {len(eligible):,} eligible authors served — done.")
        return results

    if api_fallback:
        # Use OpenAlex API for the uncached subset.
        # Note: API results are NOT written to the cache (cache = snapshot data only).
        print(f"\n  {len(uncached):,} uncached authors → OpenAlex API (api_fallback=True) …")
        n_todo = len(uncached)
        est = n_todo * delay
        print(f"  Est. time : {_hms(est)}  (network adds ~30–60%)")
        print(f"  {'─'*60}")
        reset_api_metrics()
        t_start = time.time()
        with open(out_path, "a", encoding="utf-8") as fout:
            for i, auth in enumerate(uncached, 1):
                oa_id = auth["openalex_id"].replace("https://openalex.org/", "")
                try:
                    data = _get("works", {
                        "filter":   f"authorships.author.id:{oa_id}",
                        "group_by": "publication_year",
                        "per_page": 200,
                    })
                except RateLimitExhausted as exc:
                    print(f"\n  *** RATE LIMIT EXHAUSTED after {i-1:,} authors ***  {exc}")
                    print(f"  Re-run Cell 6B tomorrow (api_fallback) or build the cache on Rivanna.\n")
                    break
                for g in data.get("group_by", []):
                    try:
                        year = int(g.get("key"))
                    except (TypeError, ValueError):
                        continue
                    rec = {
                        "openalex_id": auth["openalex_id"],
                        "faculty_id":  auth["faculty_id"],
                        "uni_slug":    auth["uni_slug"],
                        "year":        year,
                        "n_works":     g.get("count", 0),
                    }
                    fout.write(json.dumps(rec) + "\n")
                    results.append(rec)
                fout.flush()
                if i % 50 == 0 or i == n_todo:
                    elapsed = time.time() - t_start
                    rate    = i / elapsed if elapsed > 0 else 0
                    remain  = (n_todo - i) / rate if rate > 0 else 0
                    print(
                        f"  [{i:>4,}/{n_todo:,}] {i/n_todo*100:4.1f}%  "
                        f"elapsed {_hms(elapsed)}  ETA {_hms(remain)}  "
                        f"{len(results):,} records\n    {api_metrics_line()}",
                        flush=True,
                    )
                time.sleep(delay)
        total_elapsed = time.time() - t_start
        print(f"\n  {'─'*60}")
        print(f"  API fallback done for {n_todo:,} authors in {_hms(total_elapsed)}")
        print(f"  {api_metrics_line()}")

    else:
        # ── No API fallback — print exact instructions ────────────────────────
        print(f"""
  ╔══════════════════════════════════════════════════════════════════╗
  ║  ACTION REQUIRED — {len(uncached):,} new author IDs need a snapshot scan  ║
  ╚══════════════════════════════════════════════════════════════════╝

  You are NOT on Rivanna (snapshot root unreachable).
  Works data for {len(from_cache):,} cached author(s) was written above.
  The remaining {len(uncached):,} author(s) need the OpenAlex snapshot scan.

  Step 1 — Submit the cache builder job on Rivanna:
    ssh rivanna 'cd ~/Ivy_Net && sbatch build_openalex_cache.slurm'

  Step 2 — Monitor progress (takes ~3–5 hours first run):
    ssh rivanna '~/Ivy_Net/scripts/track_slurm.sh'

  Step 3 — When done, rsync both data files to this machine:
    rsync -avz --progress \\
      rivanna:~/Ivy_Net/tenure/tenure_pipeline/openalex_snapshot_cache.jsonl \\
      {cache_path}
    rsync -avz --progress \\
      rivanna:~/Ivy_Net/tenure/tenure_pipeline/openalex_works_by_year.jsonl \\
      {out_path}

  Step 4 — Re-run this cell.  All authors will be served from cache.

  Alternative: Set STAGE6B_API_FALLBACK = True in Cell 0 to use the
  OpenAlex API as a temporary fallback (slow, rate-limited, ~{_hms(len(uncached)*1.0)}
  at 1 req/sec).  API results are NOT added to the cache.
  ─────────────────────────────────────────────────────────────────""")

    return results


# ---------------------------------------------------------------------------
# Phase B: Works by year — main entry point
# ---------------------------------------------------------------------------

def fetch_works_by_year(author_records: list,
                        out_path: Path,
                        confidence_min: str = "MEDIUM",
                        delay: float = _DELAY,
                        skip_done: bool = True,
                        snapshot_root: Path | None = None,
                        cache_path: Path | None = None,
                        api_fallback: bool = False) -> list:
    """
    Aggregate publication counts by calendar year for each resolved author.

    ROUTING LOGIC — THREE MODES
    ───────────────────────────
    This function auto-detects the best data source in priority order:

    Route 1 — Snapshot mode  (Rivanna / HPC)
        snapshot_root is set AND the PAA + pub2year files are accessible.
        Performs bulk CSV scans of the OpenAlex relational snapshot.
        Uses the incremental cache (cache_path) so already-scanned authors
        are never re-scanned, even across runs.  This is the primary mode.

    Route 2 — Cache-only mode  (Mac / coffee shop / no HPC connection)
        Snapshot root is unreachable (or not set) AND cache_path exists.
        Serves all cached authors from cache immediately — no scan, no API.
        For any NEW authors not yet in the cache:
          • api_fallback=False (default): prints SSH + rsync instructions
            and returns partial results.  Recommended.
          • api_fallback=True: uses the OpenAlex API for the uncached subset.
            Functional but slow and rate-limited; API results are NOT written
            to the cache (cache = snapshot data only).

    Route 3 — API-only mode  (no snapshot, no cache file)
        Only if api_fallback=True.  One HTTP request per author.
        Use for exploratory runs or small author lists where HPC is not
        worth the overhead.

    Route 4 — Blocked  (no snapshot, no cache, api_fallback=False)
        Prints a clear error and returns [].  Default safe behavior.

    Parameters
    ----------
    author_records  : list[dict]  — from openalex_author_ids.jsonl
    out_path        : Path        — write JSONL results here incrementally
    confidence_min  : str         — minimum tier to include ('HIGH'|'MEDIUM'|'LOW')
    delay           : float       — seconds between API requests (Routes 2/3 only)
    skip_done       : bool        — skip authors already in out_path
    snapshot_root   : Path | None — path to OpenAlex relational CSV tree on HPC
                                    (see module docstring for layout).
    cache_path      : Path | None — persistent per-author cache built by snapshot
                                    scans.  Set to STAGE6_WORKS_CACHE in Cell 0.
                                    Required to enable Route 2 (cache-only mode).
    api_fallback    : bool        — set True (STAGE6B_API_FALLBACK in Cell 0) to
                                    allow the OpenAlex API as a fallback.  False by
                                    default — deliberately requires an explicit opt-in
                                    so the snapshot / cache path is always preferred.

    Returns
    -------
    list[dict]  — one record per (openalex_id, year):
        openalex_id, faculty_id, uni_slug, year, n_works
    """

    # ── Route 1: Snapshot mode (Rivanna — bulk CSV scan) ─────────────────────
    # Primary path when running on HPC with access to the CDH OpenAlex snapshot.
    # Internally uses the incremental cache so only new authors are ever scanned.
    if snapshot_root is not None:
        sr  = Path(snapshot_root).expanduser()
        paa = sr / "publicationauthoraffiliation"
        p2y = sr / "pub2year.csv.gz"
        if sr.is_dir() and paa.is_dir() and p2y.is_file():
            return _fetch_works_by_year_snapshot(
                author_records, out_path, sr, confidence_min, skip_done,
                cache_path=cache_path,
            )
        # Snapshot configured but unreachable (e.g. running on local Mac).
        # Fall through to Route 2 (cache) or Route 3/4 (API / blocked).
        print(f"\n  Stage 6B: snapshot root not accessible: {sr}")
        print(f"  → Trying cache-only mode …")

    # ── Route 2: Cache-only mode (Mac / no HPC connection) ───────────────────
    # When the snapshot is unreachable but a cache file exists from a prior
    # Rivanna run (or rsync'd to this machine), serve from cache instantly.
    # For any new authors not yet in the cache, either print rsync instructions
    # (api_fallback=False) or fall back to the API (api_fallback=True).
    if cache_path is not None and Path(cache_path).exists():
        return _fetch_works_by_year_cache_only(
            author_records, out_path, Path(cache_path),
            confidence_min, skip_done, api_fallback, delay,
        )

    # ── Route 3 / 4: API or blocked ──────────────────────────────────────────
    # Reached only when BOTH snapshot root and cache file are unavailable.
    # Route 3 (api_fallback=True):  use OpenAlex API — one request per author.
    # Route 4 (api_fallback=False): print instructions and return [].
    if not api_fallback:
        cp_hint = str(cache_path) if cache_path else "STAGE6_WORKS_CACHE (see Cell 0)"
        print(
            f"\n  Stage 6B: no snapshot and no cache file found.\n"
            f"  snapshot_root : {snapshot_root}\n"
            f"  cache_path    : {cp_hint}\n\n"
            f"  Options:\n"
            f"  1. Run  sbatch build_openalex_cache.slurm  on Rivanna to build the cache,\n"
            f"     then rsync  openalex_snapshot_cache.jsonl  to this machine.\n"
            f"  2. Set  STAGE6B_API_FALLBACK = True  in Cell 0 to use the OpenAlex API\n"
            f"     (slow / rate-limited; useful only for small exploratory runs)."
        )
        return []

    # API-only path (api_fallback=True, no snapshot, no cache).
    TIER_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "MULTI": 3, "NONE": 4}
    min_rank  = TIER_RANK.get(confidence_min, 1)
    out_path  = Path(out_path)

    done_ids: set = set()
    if skip_done and out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            for line in f:
                try:
                    done_ids.add(json.loads(line)["openalex_id"])
                except Exception:
                    pass

    def _eligible(r: dict) -> bool:
        return bool(r.get("openalex_id")) and (
            TIER_RANK.get(r.get("match_confidence", "NONE"), 99) <= min_rank
        )

    eligible = [r for r in author_records if _eligible(r)]
    todo     = [r for r in eligible if r["openalex_id"] not in done_ids]
    n_todo   = len(todo)

    est_total_sec = n_todo * delay
    print(f"\n  Stage 6B — API mode  (api_fallback=True, no snapshot, no cache)")
    print(f"  Authors to fetch   : {n_todo:,}  ({len(done_ids):,} already in {out_path.name})")
    print(f"  Eligible (≥{confidence_min}) w/ ID : {len(eligible):,}  (from {len(author_records):,} rows)")
    print(f"  Est. total time    : {_hms(est_total_sec)}  (network adds ~30–60%)")
    print(f"  {'─'*60}")

    if not todo:
        print("  Nothing to fetch — every eligible author already in output (skip_done).")
        return []

    reset_api_metrics()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    results: list = []
    t_start = time.time()

    with open(out_path, "a", encoding="utf-8") as fout:
        for i, auth in enumerate(todo, 1):
            oa_id = auth["openalex_id"].replace("https://openalex.org/", "")
            try:
                data = _get("works", {
                    "filter":   f"authorships.author.id:{oa_id}",
                    "group_by": "publication_year",
                    "per_page": 200,
                })
            except RateLimitExhausted as exc:
                print(f"\n  *** RATE LIMIT EXHAUSTED after {i-1:,} authors ***")
                print(f"  {exc}")
                print(f"  Checkpoint saved through author {i-1:,} of {n_todo:,}.")
                print(f"  Re-run Cell 6B tomorrow — it will resume from here.\n")
                break
            for g in data.get("group_by", []):
                try:
                    year = int(g.get("key"))
                except (TypeError, ValueError):
                    continue
                rec = {
                    "openalex_id": auth["openalex_id"],
                    "faculty_id":  auth["faculty_id"],
                    "uni_slug":    auth["uni_slug"],
                    "year":        year,
                    "n_works":     g.get("count", 0),
                }
                fout.write(json.dumps(rec) + "\n")
                results.append(rec)
            fout.flush()

            if i % 100 == 0 or i == n_todo:
                elapsed = time.time() - t_start
                rate    = i / elapsed if elapsed > 0 else 0
                remain  = (n_todo - i) / rate if rate > 0 else 0
                print(
                    f"  [{i:>5,}/{n_todo:,}] {i/n_todo*100:5.1f}%  "
                    f"elapsed {_hms(elapsed)}  ETA {_hms(remain)}  "
                    f"rate {rate*60:.0f}/min  │  {len(results):,} year-records written\n"
                    f"    {api_metrics_line()}",
                    flush=True,
                )
            time.sleep(delay)

    total_elapsed = time.time() - t_start
    print(f"\n  {'─'*60}")
    print(f"  Fetched works for {n_todo:,} authors in {_hms(total_elapsed)}")
    print(f"  Total year-records : {len(results):,}")
    print(f"  {api_metrics_line()}")
    return results


# ---------------------------------------------------------------------------
# QA helpers
# ---------------------------------------------------------------------------

def match_summary(author_records: list) -> dict:
    """Print and return a confidence-tier breakdown."""
    counts = Counter(r.get("match_confidence", "NONE") for r in author_records)
    total  = len(author_records)
    print(f"\n  {'Tier':<10} {'N':>6}  {'%':>6}")
    print(f"  {'-'*10} {'-'*6}  {'-'*6}")
    for tier in ("HIGH", "MEDIUM", "LOW", "MULTI", "NONE"):
        n = counts.get(tier, 0)
        print(f"  {tier:<10} {n:>6,}  {n/max(total,1)*100:>5.1f}%")
    print(f"  {'TOTAL':<10} {total:>6,}")
    return dict(counts)


def low_confidence_report(author_records: list) -> list:
    """Return records needing human review (MULTI, LOW, NONE)."""
    return [
        r for r in author_records
        if r.get("match_confidence") in ("MULTI", "LOW", "NONE")
    ]
