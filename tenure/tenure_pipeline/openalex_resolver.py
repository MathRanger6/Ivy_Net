"""
openalex_resolver.py  —  Stage 6: OpenAlex Author ID Resolution + Works Fetch
==============================================================================
Two-phase pipeline:

  Phase A  resolve_authors()
    For each unique faculty member in the panel, search OpenAlex by name +
    institution and assign an OpenAlex Author ID with a confidence score.
    Output: openalex_author_ids.jsonl

  Phase B  fetch_works_by_year()
    For each resolved author, pull publication counts grouped by year via
    OpenAlex's group_by endpoint (one request per author, very efficient).
    Output: openalex_works_by_year.jsonl

Data source (API only)
----------------------
This module talks **only** to ``https://api.openalex.org`` (see ``_get`` / ``_BASE``).
It does **not** read a local OpenAlex bulk snapshot (e.g. downloaded ``.csv.gz`` table
shards). Those are a possible future optimization when a mount path exists; until
then, Cells 6A–6B and any CLI use of this file are entirely API-based.

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

import json
import os
import time
import re
import unicodedata
from collections import deque
from pathlib import Path
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
# Phase B: Works by year
# ---------------------------------------------------------------------------

def fetch_works_by_year(author_records: list,
                        out_path: Path,
                        confidence_min: str = "MEDIUM",
                        delay: float = _DELAY,
                        skip_done: bool = True) -> list:
    """
    For each resolved author (confidence >= confidence_min), fetch publication
    counts grouped by year using OpenAlex group_by (1 request per author).

    Parameters
    ----------
    author_records  : list[dict]  — from openalex_author_ids.jsonl
    out_path        : Path        — write JSONL results here incrementally
    confidence_min  : str         — minimum confidence to include ('HIGH'|'MEDIUM'|'LOW')
    delay           : float       — seconds between requests

    Returns
    -------
    list[dict]  — one record per (openalex_id, year):
        openalex_id, faculty_id, year, n_works, n_works_oa (open-access)
    """
    TIER_RANK = {"HIGH": 0, "MEDIUM": 1, "LOW": 2, "MULTI": 3, "NONE": 4}
    min_rank  = TIER_RANK.get(confidence_min, 1)

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

    eligible = [r for r in author_records if _eligible(r)]
    todo = [r for r in eligible if r["openalex_id"] not in done_ids]
    n_todo = len(todo)

    est_total_sec = n_todo * delay
    print(f"\n  Authors to fetch   : {n_todo:,}  ({len(done_ids):,} OpenAlex IDs already in {out_path.name})")
    print(f"  Eligible (≤{confidence_min}) w/ ID : {len(eligible):,}  (from {len(author_records):,} author rows)")
    print(f"  Confidence floor   : {confidence_min}")
    print(f"  Est. total time    : {_hms(est_total_sec)}  (network adds ~30–60%)")
    print(f"  {'─'*60}")

    if not todo:
        if eligible and done_ids:
            print(
                "  Nothing to fetch — every eligible author ID already has ≥1 row in the works file "
                "(skip_done). Delete or rename the works file to rebuild, or set skip_done=False."
            )
        elif not eligible:
            print(
                "  Nothing to fetch — no author rows with both openalex_id and "
                f"match_confidence ≤ {confidence_min}."
            )
        else:
            print("  Nothing to fetch — works file empty or skip_done has nothing new.")
        return []

    reset_api_metrics()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    results = []
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
            groups = data.get("group_by", [])
            n_new  = 0
            for g in groups:
                year = g.get("key")
                try:
                    year = int(year)
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
                n_new += 1

            fout.flush()

            if i % 100 == 0 or i == n_todo:
                elapsed = time.time() - t_start
                rate    = i / elapsed if elapsed > 0 else 0
                remain  = (n_todo - i) / rate if rate > 0 else 0
                print(
                    f"  [{i:>5,}/{n_todo:,}] {i/n_todo*100:5.1f}%  "
                    f"elapsed {_hms(elapsed)}  ETA {_hms(remain)}  "
                    f"rate {rate*60:.0f}/min  │  "
                    f"{len(results):,} year-records written\n"
                    f"    {api_metrics_line()}",
                    flush=True
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
    from collections import Counter
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
