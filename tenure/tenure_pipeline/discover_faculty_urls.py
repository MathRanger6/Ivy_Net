#!/usr/bin/env python3
"""
tenure_pipeline/discover_faculty_urls.py
─────────────────────────────────────────────────────────────────────────────
Automated discovery of better faculty page URLs for schools with low parse
quality.  Replaces the manual "browse Wayback Machine in a browser" workflow.

WHAT IT DOES
────────────
1.  Reads faculty_snapshots_strategy_audit.jsonl and identifies schools where
    the HTML parser is returning few faculty records per file.

2.  For each low-quality school, queries the Wayback Machine CDX API with a
    wildcard over ALL known base domains to get every path ever captured.

3.  Scores each discovered path:
      • Keyword match  — faculty / people / staff / directory / phonebook / …
      • Depth score    — prefer 1–3 path segments (not too generic, not too deep)
      • Penalty        — courses / events / publications / static assets → skip
      • Snapshot count — how often Wayback captured this URL (= well-archived)
      • Year span      — did Wayback capture it consistently across many years?
      • Novelty        — bonus if the URL is not already in our school list

4.  Prints a rich per-school report to stdout with timing + ranked candidates.

5.  Writes two output files:
      faculty_url_suggestions.jsonl  — machine-readable; one object per school
      faculty_url_suggestions.csv    — human-readable; paste the `suggested_url`
                                       column into `new_url` in url_update_worksheet.csv

NEXT STEPS AFTER RUNNING
─────────────────────────
    # 1.  Review faculty_url_suggestions.csv — pick the URLs that look promising
    # 2.  Paste them into the new_url column of url_update_worksheet.csv
    # 3.  python tenure_pipeline/apply_url_updates.py
    # 4.  In notebook: Cell 0 → Cell 2 → Cell 3A → Cell 3B → Cell 4
    # 5.  Re-run this script to see if quality improved

CONFIGURATION  (edit the constants below)
──────────────────────────────────────────
    QUALITY_THRESHOLD_MEAN_RECS   schools with mean parsed records/file below
                                  this value get investigated  (default 20)
    QUALITY_MIN_AUDIT_FILES       need at least this many audit rows to judge
                                  a school's quality  (default 3)
    TOP_N_CANDIDATES              how many candidate URLs to keep per school
    CDX_LIMIT                     max rows per CDX wildcard query (cap at 200k)
    TEST_PARSE                    if True, downloads + parses one Wayback snapshot
                                  per candidate to get a live quality score.
                                  Adds HTTP requests; useful for final shortlisting.
"""

import csv
import json
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# ── CONFIGURATION ─────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

QUALITY_THRESHOLD_MEAN_RECS = 20   # investigate schools below this mean rec/file
QUALITY_MIN_AUDIT_FILES     = 3    # ignore schools with too few audit rows to judge
TOP_N_CANDIDATES            = 8    # ranked candidates to surface per school
SKIP_KNOWN_URLS             = True # suppress URLs already in the school's url list
                                   # (set False if you want to see all, even known ones)

# CDX API behaviour
CDX_LIMIT                   = 200_000   # max Wayback rows per wildcard query
CDX_TIMEOUT                 = 45        # seconds per CDX HTTP request
CDX_DELAY_BETWEEN_DOMAINS   = 1.5       # polite pause between each domain CDX call
CDX_DELAY_BETWEEN_SCHOOLS   = 3.0       # polite pause between schools

# Optional: download + parse one snapshot per top candidate to score URLs live.
# Adds ≈ 2–5 seconds per candidate.  False by default; run with TEST_PARSE=True
# or set the env var  TEST_PARSE=1  to enable.
import os as _os
TEST_PARSE = _os.environ.get('TEST_PARSE', '').strip() in ('1', 'true', 'True', 'yes')

# Keywords that suggest a faculty / people / directory page (in the PATH)
FACULTY_KEYWORDS = [
    'faculty', 'people', 'staff', 'directory', 'phonebook', 'personnel',
    'members', 'academics', 'department', 'about',
]

# Subdomain tokens that strongly suggest a CS / engineering department.
# A URL like cs.vanderbilt.edu or eecs.mit.edu gets a large bonus because
# the subdomain itself confirms we found the right department — exactly what
# the manual "navigate from the university homepage" workflow discovers.
CS_SUBDOMAIN_KEYWORDS = [
    'cs', 'cse', 'eecs', 'ece', 'computing', 'computer', 'engineering',
    'scs', 'ics', 'cis', 'informatics', 'sci', 'cecs', 'coe',
]

# Path segments that strongly suggest this is NOT a faculty listing
PENALTY_PATTERNS = [
    r'/course', r'/class', r'/seminar', r'/event',
    r'/news', r'/blog', r'/publicat', r'/paper',
    r'/project', r'/download', r'/software', r'/dataset',
    r'/video', r'/image', r'\.pdf$', r'\.zip$',
    r'\.(jpg|jpeg|png|gif|svg|js|css|woff|ico)$',
    r'feed', r'rss', r'sitemap', r'/search', r'/login',
    r'/admin', r'/cgi-bin', r'mailto',
]

# ─────────────────────────────────────────────────────────────────────────────
# ── PATHS ─────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

TP          = Path(__file__).resolve().parent
WORKSPACE   = TP.parent
AUDIT_JSONL = TP / 'faculty_snapshots_strategy_audit.jsonl'
DEPTS_CSV   = TP / 'r1_cs_departments.csv'
PLAN_JSONL  = TP / 'faculty_snapshots_plan.jsonl'
OUT_JSONL   = TP / 'faculty_url_suggestions.jsonl'
OUT_CSV     = TP / 'faculty_url_suggestions.csv'

CDX_API     = 'http://web.archive.org/cdx/search/cdx'
CDX_HEADERS = {
    'User-Agent': (
        'TenurePipelineBot/1.0 (academic research; '
        'UVA dissertation pipeline; dzk3ja@virginia.edu)'
    )
}

# ─────────────────────────────────────────────────────────────────────────────
# ── UTILITIES ─────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """Convert a university name to a filesystem-safe slug."""
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')


def _hms(sec: float) -> str:
    """Format seconds as HH:MM:SS."""
    sec = max(0, int(sec))
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return f'{h:02d}:{m:02d}:{s:02d}' if h else f'{m:02d}:{s:02d}'


def _base_domain(url: str) -> str:
    """Extract host from a URL, stripping www. prefix.
    e.g. https://cs.vanderbilt.edu/people/ → cs.vanderbilt.edu
    """
    host = urllib.parse.urlparse(url).hostname or ''
    return re.sub(r'^www\.', '', host.lower())


def _top_level_domain(url: str) -> str:
    """
    Extract the registrable (apex) domain from any URL — stripping subdomains.

    This is the KEY function for the discovery algorithm:
      cs.vanderbilt.edu       →  vanderbilt.edu
      engineering.mit.edu     →  mit.edu
      www.cmu.edu             →  cmu.edu
      eecs.berkeley.edu       →  berkeley.edu

    Why we need this: the manual Wayback workflow starts at the UNIVERSITY's
    root URL (vanderbilt.edu), then navigates to wherever CS lives that year.
    Starting from a known sub-domain (cs.vanderbilt.edu) would MISS years when
    CS was housed elsewhere (e.g. engineering.vanderbilt.edu/eecs/).
    """
    host = urllib.parse.urlparse(url).hostname or ''
    host = host.lower().lstrip('www.')
    parts = host.split('.')
    # Return the last two segments: domain + TLD
    # Handles edu, com, org, etc.  Does not handle .co.uk — not needed for US universities.
    if len(parts) >= 2:
        return '.'.join(parts[-2:])
    return host


def _get_subdomain(url: str) -> str:
    """
    Return just the subdomain token(s) from a URL.
    e.g. cs.vanderbilt.edu → 'cs'
         eecs.mit.edu       → 'eecs'
         www.cmu.edu        → ''   (no meaningful subdomain)
    Used by the scorer to give a CS-subdomain bonus.
    """
    host  = urllib.parse.urlparse(url).hostname or ''
    host  = host.lower()
    apex  = _top_level_domain(url)          # vanderbilt.edu
    # Everything before the apex domain is the subdomain portion
    sub   = host[:-(len(apex) + 1)] if host.endswith('.' + apex) else ''
    # Strip leading www.
    sub   = re.sub(r'^www\.?', '', sub)
    return sub


def _path_depth(url: str) -> int:
    """Count non-empty path segments."""
    path = urllib.parse.urlparse(url).path
    return len([s for s in path.split('/') if s])


def _score_candidate(url: str, count: int, year_min: int, year_max: int,
                      known_urls: set) -> float:
    """
    Score a candidate URL on a 0–115 scale.  Higher = more likely to be a
    useful faculty page that is well-archived and not yet in our list.

    Component weights (approximate):
      keyword score    — 0–35 pts  (faculty/people/directory keywords in path)
      CS-subdomain     — 0–15 pts  (subdomain itself signals CS dept: cs.x.edu, eecs.x.edu)
      depth score      — 0–15 pts  (path depth sweet spot = 1–3 segments)
      snapshot count   — 0–20 pts  (how often Wayback archived it)
      year span        — 0–15 pts  (coverage across many calendar years)
      novelty bonus    — 0–15 pts  (not already in our school URL list)
      penalty          — large negative (clearly not a faculty page)

    The CS-subdomain bonus is the key improvement over the old algorithm.
    When we query *.vanderbilt.edu/* (all subdomains), we discover URLs like
    cs.vanderbilt.edu/people/ — the subdomain 'cs' itself tells us we found
    the CS department, independent of what the path says.  This mirrors the
    manual Wayback workflow: navigate from the university homepage to wherever
    CS lived that year, letting the department's own URL structure guide you.
    """
    import math

    url_lower = url.lower()
    path      = urllib.parse.urlparse(url).path.lower()

    # ── Hard penalty: clear non-faculty content ────────────────────────────
    for pat in PENALTY_PATTERNS:
        if re.search(pat, url_lower):
            return -999.0

    # ── Keyword score (0–35): faculty-page keywords in the PATH ───────────
    kw_hits  = sum(1 for kw in FACULTY_KEYWORDS if kw in path)
    kw_score = min(kw_hits * 10, 35)
    # Extra bonus for the single most diagnostic keyword
    high_value = {'faculty', 'people', 'staff', 'phonebook', 'directory', 'personnel'}
    if any(kw in path for kw in high_value):
        kw_score = min(kw_score + 10, 35)

    # ── CS-subdomain bonus (0–15) ──────────────────────────────────────────
    # A URL whose SUBDOMAIN is a CS/engineering token (cs.vanderbilt.edu,
    # eecs.mit.edu) is almost certainly in the right department.  This is the
    # core insight: after a matchType=domain query we discover subdomains we
    # never knew about — the subdomain itself is evidence of CS relevance.
    sub = _get_subdomain(url)
    sub_tokens = re.split(r'[\.\-]', sub)   # 'eecs' or ['grad', 'cs'] etc.
    cs_sub = any(tok in CS_SUBDOMAIN_KEYWORDS for tok in sub_tokens)
    subdomain_score = 15 if cs_sub else 0

    # Also check the path for CS department tokens (cs/, cse/, eecs/, etc.)
    path_tokens = re.split(r'[/\.\-_]', path)
    cs_path = any(tok in CS_SUBDOMAIN_KEYWORDS for tok in path_tokens if len(tok) >= 2)
    if cs_path and not cs_sub:
        subdomain_score = 8   # partial bonus: path confirms CS area

    # ── Depth score (0–15) ────────────────────────────────────────────────
    depth = _path_depth(url)
    if depth == 0:           depth_score = 0     # bare domain — unlikely a listing
    elif depth <= 3:         depth_score = 15    # sweet spot: /people, /cs/faculty
    elif depth <= 5:         depth_score = 8
    else:                    depth_score = 2     # very deep path — less likely a listing

    # ── Snapshot count score (0–20) ────────────────────────────────────────
    # Logarithmic: 1 snap → 0, 10 → ~7, 100 → ~13, 1000 → ~20
    count_score = min(math.log1p(count) / math.log1p(1000) * 20, 20) if count > 0 else 0

    # ── Year span score (0–15) ────────────────────────────────────────────
    span = max(0, year_max - year_min) if year_max and year_min else 0
    span_score = min(span / 20 * 15, 15)   # 20-year span → full marks

    # ── Novelty bonus (0–15) ──────────────────────────────────────────────
    novelty = 15 if url not in known_urls else 0

    total = kw_score + subdomain_score + depth_score + count_score + span_score + novelty
    return round(total, 1)


def _cdx_query(url_pattern: str, match_type: str = 'prefix') -> list:
    """
    Core CDX API query helper.  Returns a list of dicts:
        url, count, year_min, year_max, sample_ts

    Parameters
    ----------
    url_pattern : str
        The CDX 'url' parameter.  For matchType=domain pass just the
        apex domain (vanderbilt.edu).  For prefix pass domain/path/*.
    match_type : str
        'prefix'  — matches urls that START WITH url_pattern  (old behaviour)
        'domain'  — matches ALL subdomains of url_pattern, e.g.
                    vanderbilt.edu → cs.vanderbilt.edu, engineering.vanderbilt.edu, etc.
                    This is the KEY to the new algorithm: one query discovers
                    every subdomain the university has ever used, so we find
                    cs.vanderbilt.edu even if we only knew engineering.vanderbilt.edu.

    Uses collapse=urlkey so we get ONE row per unique URL (fast).
    A follow-up count query is done separately for the top candidates.
    """
    params = {
        'url':       url_pattern,
        'output':    'json',
        'fl':        'original,timestamp,statuscode',
        'collapse':  'urlkey',
        'limit':     str(CDX_LIMIT),
        'matchType': match_type,
    }
    query = CDX_API + '?' + urllib.parse.urlencode(params)
    req   = urllib.request.Request(query, headers=CDX_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=CDX_TIMEOUT) as resp:
            raw = json.loads(resp.read().decode('utf-8', errors='replace'))
    except Exception as exc:
        print(f'    CDX error [{match_type}] {url_pattern}: {exc}', flush=True)
        return []

    if not raw or len(raw) < 2:
        return []

    header = raw[0]   # ['original', 'timestamp', 'statuscode']
    rows   = raw[1:]

    try:
        i_url    = header.index('original')
        i_ts     = header.index('timestamp')
        i_status = header.index('statuscode')
    except ValueError:
        return []

    results = []
    for row in rows:
        try:
            url    = row[i_url]
            ts     = row[i_ts]
            status = row[i_status]
        except IndexError:
            continue

        if status in ('404', '403', '301', '302'):
            continue
        if not url.startswith('http'):
            continue

        year = int(ts[:4]) if ts and len(ts) >= 4 else 0
        results.append({
            'url':            url,
            'count':          1,          # placeholder; refined below for top N
            'year_min':       year,
            'year_max':       year,
            'sample_ts':      ts,
        })

    return results


def _cdx_count_url(url: str) -> tuple:
    """
    Count how many times Wayback captured a specific URL and get year range.
    Returns (count, year_min, year_max).  Used to refine scores for top candidates.
    """
    params = {
        'url':    url,
        'output': 'json',
        'fl':     'timestamp',
        'limit':  '10000',
    }
    query = CDX_API + '?' + urllib.parse.urlencode(params)
    req   = urllib.request.Request(query, headers=CDX_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = json.loads(resp.read().decode('utf-8', errors='replace'))
    except Exception:
        return 1, 0, 0

    if not raw or len(raw) < 2:
        return 0, 0, 0

    timestamps = [row[0] for row in raw[1:] if row]
    years      = [int(ts[:4]) for ts in timestamps if ts and len(ts) >= 4]
    return len(timestamps), (min(years) if years else 0), (max(years) if years else 0)


def _preflight_cdx_check() -> bool:
    """
    Fire one tiny CDX request (limit=1) against a known stable URL to confirm
    the Wayback CDX API is reachable before starting the main school loop.

    Returns True if the API responds correctly, False otherwise.
    Prints a clear status line either way.
    """
    test_url = 'cs.mit.edu/'    # reliable, always in CDX
    params = {
        'url':    test_url,
        'output': 'json',
        'fl':     'timestamp',
        'limit':  '1',
    }
    query = CDX_API + '?' + urllib.parse.urlencode(params)
    req   = urllib.request.Request(query, headers=CDX_HEADERS)
    print(f'  Preflight CDX check → {CDX_API} … ', end='', flush=True)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8', errors='replace'))
        elapsed = time.time() - t0
        if isinstance(data, list) and len(data) >= 1:
            print(f'✅  OK  ({elapsed:.1f}s)', flush=True)
            return True
        print(f'⚠️  Unexpected response: {data!r}', flush=True)
        return False
    except Exception as exc:
        elapsed = time.time() - t0
        print(f'❌  FAILED after {elapsed:.1f}s — {exc}', flush=True)
        return False


def _test_parse_wayback(url: str) -> int:
    """
    Download one Wayback snapshot and run it through the html_parser.
    Returns the number of faculty records extracted.  0 = bad page.
    """
    try:
        sys.path.insert(0, str(TP))
        import html_parser as hp   # type: ignore[import]
    except ImportError:
        return -1   # parser not available

    req = urllib.request.Request(url, headers=CDX_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode('utf-8', errors='replace')
    except Exception as exc:
        print(f'      Download error: {exc}', flush=True)
        return -1

    try:
        result = hp.parse_faculty_page(html)
        return len(result) if result else 0
    except Exception:
        return -1


# ─────────────────────────────────────────────────────────────────────────────
# ── PHASE 1: Load quality data ────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

def load_quality_data() -> dict:
    """
    Read faculty_snapshots_strategy_audit.jsonl.
    Returns {uni_slug: {'mean_recs': float, 'n_files': int, 'frac_zero': float}}.
    """
    school_recs = defaultdict(list)
    with open(AUDIT_JSONL, encoding='utf-8') as f:
        for line in f:
            try:
                r = json.loads(line)
                school_recs[r['uni_slug']].append(r.get('n_records', 0))
            except Exception:
                pass

    quality = {}
    for slug, recs in school_recs.items():
        if len(recs) < QUALITY_MIN_AUDIT_FILES:
            continue
        mean_r  = sum(recs) / len(recs)
        frac_z  = sum(1 for x in recs if x == 0) / len(recs)
        quality[slug] = {
            'mean_recs': round(mean_r, 1),
            'n_files':   len(recs),
            'frac_zero': round(frac_z, 3),
        }
    return quality


# ─────────────────────────────────────────────────────────────────────────────
# ── PHASE 2: Load school URL lists and plan ───────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

def load_school_urls() -> dict:
    """
    Returns {uni_slug: {urls: [str], university: str, dept_name: str}}.
    Reads r1_cs_departments.csv; the 'urls' column is a JSON list.
    """
    schools = {}
    with open(DEPTS_CSV, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            slug = slugify(row['university'])
            try:
                urls = json.loads(row.get('urls', '[]'))
            except Exception:
                urls = []
            schools[slug] = {
                'university': row['university'],
                'dept_name':  row.get('dept_name', ''),
                'urls':       [u.strip() for u in urls if u.strip()],
            }
    return schools


def load_plan_urls() -> set:
    """Return the set of source_urls already in the CDX plan."""
    tried = set()
    if not PLAN_JSONL.exists():
        return tried
    with open(PLAN_JSONL, encoding='utf-8') as f:
        for line in f:
            try:
                r = json.loads(line)
                if r.get('source_url'):
                    tried.add(r['source_url'].strip().rstrip('/'))
            except Exception:
                pass
    return tried


# ─────────────────────────────────────────────────────────────────────────────
# ── PHASE 3 & 4: CDX discovery + scoring ─────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

def discover_for_school(slug: str, school: dict, quality: dict,
                        plan_urls: set) -> list:
    """
    Run CDX discovery for a school, starting from the UNIVERSITY'S ROOT DOMAIN.

    ── Why root domain, not the known sub-domain URL? ──────────────────────────
    The old approach queried e.g. engineering.vanderbilt.edu/* — but that only
    finds URLs *under* that subdomain.  The problem we are solving is exactly
    that CS faculty might have lived under a DIFFERENT subdomain in different
    years (cs.vanderbilt.edu in 2005, engineering.vanderbilt.edu/eecs/ in 2012).

    The correct algorithm mirrors the manual Wayback workflow:
      1. Start at www.vanderbilt.edu  (the university root — stable across years)
      2. Navigate from there to wherever CS lived that year
      3. Discover the faculty page

    We automate this with CDX matchType=domain, which returns ALL URLs across
    ALL subdomains of vanderbilt.edu in one query:
      → cs.vanderbilt.edu/people/          (the CS dept's own subdomain)
      → engineering.vanderbilt.edu/cs/     (CS housed in engineering)
      → www.vanderbilt.edu/academics/...   (central portal)
      etc.

    The scorer then rewards:
      • Faculty keywords in the path       (faculty, people, directory…)
      • CS tokens in the SUBDOMAIN         (cs.*, eecs.*, computing.*…)
      • CS tokens in the PATH              (…/cs/, …/eecs/…)
      • High Wayback snapshot count        (well-archived = stable, useful URL)
      • Multi-year coverage                (the URL existed across many years)
      • Not already in our known-URL list  (novelty — we want *new* candidates)

    Each candidate dict returned:
        url, score, count, year_min, year_max, already_known, test_parse_recs
    """
    known_urls = set(school['urls'])
    all_candidates = {}   # url → best-scored entry

    # ── Collect unique apex domains across all known URLs ──────────────────
    # From cs.vanderbilt.edu  →  vanderbilt.edu
    # From engineering.mit.edu → mit.edu
    # We deduplicate so we only fire ONE matchType=domain CDX query per
    # university, no matter how many department subdomains we already know.
    apex_domains = set()
    for known_url in school['urls']:
        apex = _top_level_domain(known_url)
        if apex:
            apex_domains.add(apex)

    if not apex_domains:
        print('    No apex domain resolved — skipping.', flush=True)
        return []

    # ── Phase 3a: matchType=domain query — discover ALL subdomains at once ─
    # One query for vanderbilt.edu discovers cs.*, eecs.*, engineering.*, etc.
    for apex in sorted(apex_domains):
        print(f'    CDX domain query: *.{apex}/* …', end='  ', flush=True)
        t0       = time.time()
        raw_hits = _cdx_query(apex, match_type='domain')
        elapsed  = time.time() - t0
        print(f'{len(raw_hits):,} unique URLs in {elapsed:.1f}s', flush=True)

        for hit in raw_hits:
            url = hit['url']
            # Preliminary score using single sample data
            score = _score_candidate(
                url, hit['count'], hit['year_min'], hit['year_max'], known_urls
            )
            if score < 0:     # hard penalty: asset / redirect / clearly wrong
                continue
            if url not in all_candidates or score > all_candidates[url]['score']:
                all_candidates[url] = {
                    'url':           url,
                    'score':         score,
                    'count':         hit['count'],
                    'year_min':      hit['year_min'],
                    'year_max':      hit['year_max'],
                    'sample_ts':     hit.get('sample_ts', ''),
                    'already_known': (url in known_urls or
                                      url.rstrip('/') in plan_urls),
                }

        time.sleep(CDX_DELAY_BETWEEN_DOMAINS)

    # Sort by preliminary score and take top N * 2 for refinement
    ranked = sorted(all_candidates.values(), key=lambda x: -x['score'])
    top_for_refine = ranked[: TOP_N_CANDIDATES * 2]

    # ── Phase 3b: Refine — get exact snapshot counts for top candidates ────
    # The domain query returns count=1 per URL (collapse=urlkey).  For the
    # short-list we fire a second CDX call per URL to get real counts + year
    # ranges, then re-score.  This is where archive depth and year span matter.
    print(f'    Refining counts for top {len(top_for_refine)} candidates …', flush=True)
    for cand in top_for_refine:
        if SKIP_KNOWN_URLS and cand['already_known']:
            continue
        count, yr_min, yr_max = _cdx_count_url(cand['url'])
        cand['count']    = count
        cand['year_min'] = yr_min
        cand['year_max'] = yr_max
        cand['score'] = _score_candidate(
            cand['url'], count, yr_min, yr_max, known_urls
        )
        time.sleep(0.5)

    # ── Optional: test-parse a Wayback snapshot for each top candidate ────
    if TEST_PARSE:
        print(f'    Test-parsing top candidates …', flush=True)
        for cand in top_for_refine[:TOP_N_CANDIDATES]:
            if cand.get('already_known') and SKIP_KNOWN_URLS:
                cand['test_parse_recs'] = None
                continue
            ts  = cand.get('sample_ts', '')
            url = cand['url']
            if ts:
                wayback = f'https://web.archive.org/web/{ts}/{url}'
                print(f'      Parsing {wayback[:80]}…', end='  ', flush=True)
                n = _test_parse_wayback(wayback)
                cand['test_parse_recs'] = n
                print(f'{n} records', flush=True)
                time.sleep(2.0)
            else:
                cand['test_parse_recs'] = None
    else:
        for cand in top_for_refine:
            cand['test_parse_recs'] = None

    # ── Final sort and trim ───────────────────────────────────────────────
    final = sorted(top_for_refine, key=lambda x: -x['score'])
    if SKIP_KNOWN_URLS:
        final = [c for c in final if not c['already_known']]
    return final[:TOP_N_CANDIDATES]


# ─────────────────────────────────────────────────────────────────────────────
# ── PHASE 5: Output ───────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

def print_school_report(slug: str, school: dict, quality: dict,
                        candidates: list) -> None:
    """Print a formatted per-school report to stdout."""
    q = quality[slug]
    print(f'\n  {"─"*70}')
    print(f'  School    : {school["university"]}  ({slug})')
    print(f'  Dept      : {school["dept_name"]}')
    print(f'  Quality   : {q["mean_recs"]:.1f} mean records/file  '
          f'({q["n_files"]} audited files)')
    print(f'  Known URLs: {len(school["urls"])}')
    if not candidates:
        print(f'  ⚠️  No novel candidates found — try a broader CDX query or '
              f'check if the school uses a different base domain.')
        return

    print(f'  {"─"*70}')
    print(f'  {"Rank":<5}  {"Score":>5}  {"Count":>6}  {"Yrs":>8}  '
          f'{"Depth":>5}  URL')
    print(f'  {"────":<5}  {"─────":>5}  {"──────":>6}  {"────────":>8}  '
          f'{"─────":>5}  ────────────────────────────────────')
    for i, cand in enumerate(candidates, 1):
        yr_range = (f'{cand["year_min"]}–{cand["year_max"]}'
                    if cand['year_min'] else '?')
        depth    = _path_depth(cand['url'])
        tp_str   = (f'  [{cand["test_parse_recs"]} recs]'
                    if cand['test_parse_recs'] is not None else '')
        flag     = ' ★' if i <= 3 else ''
        print(f'  {i:<5}  {cand["score"]:>5.1f}  {cand["count"]:>6,}  '
              f'{yr_range:>8}  {depth:>5}  {cand["url"]}{tp_str}{flag}')
    print(f'  {"─"*70}')


def load_checkpoint() -> dict:
    """
    Read already-completed schools from the JSONL output file.

    This is the resume mechanism — same pattern as openalex_snapshot_cache.jsonl
    in the OpenAlex cache builder.  On startup, any school whose slug already
    appears in OUT_JSONL is treated as done and skipped in the main loop.

    Returns {uni_slug: record_dict} for every school already in the file.
    If the file does not exist (first run), returns {}.

    Why JSONL and not a separate checkpoint file?  The output IS the checkpoint.
    The file is written incrementally — one line per school as it finishes —
    so a mid-run kill leaves a valid, partial JSONL that the next run resumes from.
    The CSV is then regenerated from the complete JSONL at the end of each run.
    """
    done = {}
    if not OUT_JSONL.exists():
        return done
    with open(OUT_JSONL, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                slug = rec.get('uni_slug', '')
                if slug:
                    done[slug] = rec
            except json.JSONDecodeError:
                pass   # ignore corrupt lines from a truncated previous run
    return done


def append_school_to_jsonl(rec: dict) -> None:
    """
    Append one school's result record to the JSONL output file immediately.

    This is the core of the checkpoint pattern: we write as we go, not at the
    end.  If the job is killed after school N, schools 1…N are already on disk.
    The next run reads them back via load_checkpoint() and skips straight to N+1.

    File is opened in append mode ('a') so each call adds exactly one line
    without touching what is already there.
    """
    with open(OUT_JSONL, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec) + '\n')
        f.flush()   # push to OS buffer immediately — safe against kill signals


def write_csv_from_jsonl(all_results: list) -> None:
    """
    Write (or rewrite) the CSV summary from the full results list.

    Called once at the end of the run — after all schools are done — so the CSV
    always reflects the complete picture.  The JSONL is the authoritative
    record; the CSV is a human-friendly view derived from it.

    CSV columns:
      uni_slug, university, dept_name, mean_recs, n_audit_files,
      rank, score, snapshot_count, year_min, year_max, suggested_url,
      test_parse_recs
    """
    csv_rows = []
    for rec in all_results:
        for i, cand in enumerate(rec['candidates'], 1):
            csv_rows.append({
                'uni_slug':        rec['uni_slug'],
                'university':      rec['university'],
                'dept_name':       rec['dept_name'],
                'mean_recs':       rec['mean_recs'],
                'n_audit_files':   rec['n_audit_files'],
                'rank':            i,
                'score':           cand['score'],
                'snapshot_count':  cand['count'],
                'year_min':        cand['year_min'],
                'year_max':        cand['year_max'],
                'suggested_url':   cand['url'],
                'test_parse_recs': cand.get('test_parse_recs', ''),
            })

    if csv_rows:
        with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            writer.writeheader()
            writer.writerows(csv_rows)
        print(f'  Wrote {len(csv_rows)} candidate rows    → {OUT_CSV.name}')
        print(f'\n  To add URLs to the pipeline:')
        print(f'    1.  Open {OUT_CSV.name} — review "suggested_url" column')
        print(f'    2.  Paste promising URLs into "new_url" in url_update_worksheet.csv')
        print(f'    3.  python tenure_pipeline/apply_url_updates.py')
        print(f'    4.  Notebook: Cell 0 → Cell 2 → Cell 3A → Cell 3B → Cell 4')
    else:
        print(f'  No candidates to write to CSV.')


# ─────────────────────────────────────────────────────────────────────────────
# ── MAIN ──────────────────────────────────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    t_global = time.time()

    print('═' * 72)
    print('  Faculty URL Discovery — tenure_pipeline/discover_faculty_urls.py')
    print('═' * 72)
    print(f'  Config:')
    print(f'    Quality threshold  : mean_recs < {QUALITY_THRESHOLD_MEAN_RECS}')
    print(f'    Min audit files    : {QUALITY_MIN_AUDIT_FILES}')
    print(f'    Candidates per school: {TOP_N_CANDIDATES}')
    print(f'    Skip known URLs    : {SKIP_KNOWN_URLS}')
    print(f'    Test-parse enabled : {TEST_PARSE}')
    print(f'    CDX limit/query    : {CDX_LIMIT:,}')
    print()

    # ── Preflight: confirm CDX API is reachable before burning any searches ──
    print('  Preflight check …')
    if not _preflight_cdx_check():
        print()
        print('  ⛔  CDX API unreachable — aborting before any school queries.')
        print('  Check your internet connection (or VPN if on restricted network)')
        print('  and re-run when connectivity is confirmed.')
        return
    print()

    # ── Phase 1: Load quality data ─────────────────────────────────────────
    print('  Phase 1: Loading audit data …', flush=True)
    quality = load_quality_data()
    low_q   = {s: q for s, q in quality.items()
               if q['mean_recs'] < QUALITY_THRESHOLD_MEAN_RECS}
    low_q   = dict(sorted(low_q.items(), key=lambda x: x[1]['mean_recs']))
    print(f'  Schools in audit     : {len(quality):,}')
    print(f'  Below threshold (<{QUALITY_THRESHOLD_MEAN_RECS} mean recs): {len(low_q):,}')
    if not low_q:
        print('\n  All schools are above the quality threshold — nothing to do.')
        print(f'  Lower QUALITY_THRESHOLD_MEAN_RECS (currently {QUALITY_THRESHOLD_MEAN_RECS})')
        print(f'  to investigate more schools.')
        return

    print()
    print(f'  Schools to investigate (sorted by quality, worst first):')
    for i, (slug, q) in enumerate(low_q.items(), 1):
        print(f'    {i:>3}.  {slug:<48}  {q["mean_recs"]:>5.1f} recs/file  '
              f'({q["n_files"]} files)')

    # ── Phase 2: Load school URLs and plan ────────────────────────────────
    print(f'\n  Phase 2: Loading school URLs and CDX plan …', flush=True)
    all_schools = load_school_urls()
    plan_urls   = load_plan_urls()
    print(f'  Schools in CSV       : {len(all_schools):,}')
    print(f'  URLs in CDX plan     : {len(plan_urls):,}')

    # ── Checkpoint: load already-completed schools ─────────────────────────
    # Same resume pattern as the OpenAlex cache builder.  If OUT_JSONL already
    # exists from a previous (interrupted) run, we read back whatever schools
    # finished and skip them this time.  A fresh run finds nothing and proceeds
    # normally.  Delete OUT_JSONL to force a full re-run from scratch.
    checkpoint = load_checkpoint()
    if checkpoint:
        print(f'\n  ⚡ Resuming from checkpoint: {len(checkpoint)} schools already done '
              f'({OUT_JSONL.name})')
        print(f'  Remaining: {len(low_q) - len(checkpoint)} schools to process')
        print(f'  (Delete {OUT_JSONL.name} to force a full re-run from scratch)')
    else:
        print(f'\n  No checkpoint found — starting fresh run.')

    # ── Phase 3 & 4: CDX discovery + scoring ──────────────────────────────
    print(f'\n  Phase 3–4: CDX discovery + scoring …')
    # Count unique APEX domains (vanderbilt.edu, not cs.vanderbilt.edu) —
    # that's exactly one CDX matchType=domain query per university.
    n_apex = len(set(
        _top_level_domain(u)
        for s in low_q if s in all_schools and s not in checkpoint
        for u in all_schools[s]['urls']
    ))
    n_remaining = sum(1 for s in low_q if s not in checkpoint)
    print(f'  ({n_remaining} schools to run, {n_apex} unique apex domains → 1 CDX query each)')
    print(f'  Strategy: matchType=domain discovers ALL subdomains per university')

    # all_results collects every school — both resumed and newly processed —
    # so the final CSV is always complete regardless of how many runs it took.
    all_results = list(checkpoint.values())

    for school_num, (slug, q) in enumerate(low_q.items(), 1):

        # ── Skip schools already completed in a previous run ──────────────
        if slug in checkpoint:
            print(f'\n  [{school_num}/{len(low_q)}]  (checkpoint) {slug} — skipping.',
                  flush=True)
            continue

        school = all_schools.get(slug)
        if not school:
            print(f'\n  [{school_num}/{len(low_q)}] {slug} — not found in '
                  f'r1_cs_departments.csv; skipping.')
            continue
        if not school['urls']:
            print(f'\n  [{school_num}/{len(low_q)}] {slug} — no URLs in CSV; skipping.')
            continue

        elapsed_global = time.time() - t_global
        print(f'\n  [{school_num}/{len(low_q)}]  {school["university"]}  '
              f'(cumulative {_hms(elapsed_global)})', flush=True)
        print(f'    Known URLs: {school["urls"]}', flush=True)

        t_school   = time.time()
        candidates = discover_for_school(slug, school, quality, plan_urls)
        school_time = time.time() - t_school

        print_school_report(slug, school, quality, candidates)
        print(f'  School done in {school_time:.1f}s', flush=True)

        rec = {
            'uni_slug':      slug,
            'university':    school['university'],
            'dept_name':     school['dept_name'],
            'mean_recs':     q['mean_recs'],
            'n_audit_files': q['n_files'],
            'quality_rank':  school_num,
            'candidates':    candidates,
        }
        all_results.append(rec)

        # ── Write this school to JSONL immediately — checkpoint safe ──────
        # If the job is killed after this line, this school won't be re-run.
        append_school_to_jsonl(rec)
        print(f'  ✓ Checkpointed → {OUT_JSONL.name}', flush=True)

        if school_num < len(low_q):
            print(f'  Pausing {CDX_DELAY_BETWEEN_SCHOOLS}s …', flush=True)
            time.sleep(CDX_DELAY_BETWEEN_SCHOOLS)

    # ── Phase 5: Write CSV from complete results ───────────────────────────
    # The JSONL is already fully written (one line per school, appended live).
    # We just need to regenerate the human-friendly CSV from the full list.
    print(f'\n{"═"*72}')
    print(f'  Phase 5: Writing CSV output …')
    write_csv_from_jsonl(all_results)

    total_time = time.time() - t_global
    print(f'\n  Total runtime    : {_hms(total_time)}')
    print(f'  Schools processed: {len(all_results)} / {len(low_q)}')
    print(f'  (from checkpoint): {len(checkpoint)}')
    print(f'  (this run)       : {len(all_results) - len(checkpoint)}')
    print(f'  Candidates found : '
          f'{sum(len(r["candidates"]) for r in all_results):,} URLs')
    print('═' * 72)


if __name__ == '__main__':
    main()
