#!/usr/bin/env python3
"""
tenure_pipeline/apply_url_updates.py
─────────────────────────────────────────────────────────────────────────────
URL management tool for the tenure pipeline.

WORKFLOW
--------
1. Open url_update_worksheet.csv in Excel / Numbers / VS Code.
2. For any school, paste a new candidate URL into the `new_url` column.
   (You can also leave new_url blank and just review the status columns.)
3. Save the CSV.
4. Run:  python tenure_pipeline/apply_url_updates.py
5. Run notebook Cells 0 → 2 → 3A → 3B → 4 as needed.

Clean rebuild (empty plan/index so Cell 3A re-CDX-queries every URL): see
tenure_pipeline/rebuild_plan.py  (e.g.  python tenure_pipeline/rebuild_plan.py --force).

WHAT THE SCRIPT DOES
--------------------
- For each row with a non-empty `new_url`:
    • If the URL is already in r1_schools_data.py for that school → tell you (skip)
    • If the URL has already been tried (in plan) → tell you with status details
    • Otherwise → add the URL to the school's urls list in r1_schools_data.py
- Rebuilds url_update_worksheet.csv with fresh per-URL stats and status tags.

Each URL row is duplicated with the same school-level totals:
  school_snaps — unique snapshot slots in the plan for this uni_slug (deduped by local_path)
  school_html  — count of *.html under faculty_snapshots/<uni_slug>/ (recursive: legacy/, <source_id>/, …)
Sort defaults to school_snaps ascending so schools with little or no coverage rise to the top.

STATUS VALUES IN WORKSHEET
--------------------------
  ok        - Plan has snapshot rows for this URL (or a normalized variant); HTML
              counts dedupe by file path (duplicate plan lines are ignored)
  empty     - CDX query found 0 Wayback snapshots for this URL
  condemned - Plan sentinel with n_snaps=-1 and a reason (Cell 3B / Cell 4)
  untried   - URL is in the list but has never been queried yet

URL matching: stats are keyed by normalize_faculty_url() so http/https, :80, and
trailing slashes match the plan’s source_url strings. CDX success bookmarks use
plan_row_type=cdx_bookmark (new) or legacy n_snaps=-1 without reason; both are
treated as ok, not condemned.
"""

import hashlib
import json, re, csv, sys, shutil, unicodedata
from pathlib import Path
from collections import defaultdict
from urllib.parse import urlparse

# ── Paths ─────────────────────────────────────────────────────────────────
TP          = Path(__file__).resolve().parent
WORKSPACE   = TP.parent
SCHOOLS_PY  = TP / 'r1_schools_data.py'
WORKSHEET   = TP / 'url_update_worksheet.csv'
PLAN_JSONL  = TP / 'faculty_snapshots_plan.jsonl'
PARSED_JSONL= TP / 'faculty_snapshots_parsed.jsonl'
HTML_DIR    = TP / 'faculty_snapshots'

# ── Utilities ─────────────────────────────────────────────────────────────
def slugify(name: str) -> str:
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')


# Hosts where the bare subdomain redirects to www (plan/CDX often use www only).
_WWW_PAIR = frozenset({
    'cse.msu.edu',
})


def normalize_faculty_url(u: str) -> str:
    """
    Canonical key so plan rows match school-list URLs despite:
    - http vs https, :80 / :443 in CDX output, trailing slashes,
    - www vs non-www when the site treats them as the same faculty page,
    - accidental paste of a full web.archive.org replay URL as a 'live' URL.
    """
    u = (u or '').strip()
    if not u:
        return ''
    p = urlparse(u)
    # User pasted Wayback replay link into urls[] — recover original
    if (p.hostname or '').lower() == 'web.archive.org' and '/web/' in (p.path or ''):
        m = re.search(r'(https?://[^\s]+)', p.path or '')
        if m:
            u = m.group(1).rstrip('/')
            p = urlparse(u)
    host = (p.hostname or '').lower()
    if not host:
        return u
    if host in _WWW_PAIR:
        host = 'www.' + host
    path = p.path or '/'
    if path != '/' and not path.endswith('/'):
        path = path + '/'
    q = (p.query or '')
    return f'{host}{path}{("?" + q) if q else ""}'


def faculty_source_id(url: str) -> str:
    """
    Stable short id for Option B storage paths:
    faculty_snapshots/<uni_slug>/<source_id>/<year>_<season>_<timestamp>.html
    (legacy two-part <year>_<season>.html may exist until rebuilt)
    Derived from normalize_faculty_url() so worksheet and plan stay aligned.

    On disk, ``legacy/`` (moved flat snapshots) is a normal subfolder alongside
    each ``<source_id>/`` directory — use iter_school_html_files() to list HTML.
    """
    nu = normalize_faculty_url(url)
    if not nu:
        return 'unknown'
    return hashlib.sha256(nu.encode('utf-8')).hexdigest()[:8]


def load_disk_html_by_slug() -> dict[str, int]:
    """uni_slug → count of *.html on disk (one scan of faculty_snapshots/)."""
    out: dict[str, int] = {}
    if not HTML_DIR.is_dir():
        return out
    for d in HTML_DIR.iterdir():
        if d.is_dir():
            out[d.name] = sum(1 for _ in d.rglob('*.html'))
    return out


def iter_school_html_files(school_dir: Path) -> list[Path]:
    """
    All ``*.html`` under ``faculty_snapshots/<uni_slug>/``: top-level (legacy flat),
    ``legacy/``, ``<source_id>/``, etc. — same rule as Cell 4 and 3D/3E rescue cells.
    """
    school_dir = Path(school_dir)
    if not school_dir.is_dir():
        return []
    return sorted(school_dir.rglob('*.html'))


def load_schools() -> list:
    """Import PILOT_SCHOOLS from r1_schools_data.py via exec (avoids stale sys.modules)."""
    ns = {}
    exec(compile(SCHOOLS_PY.read_text(), str(SCHOOLS_PY), 'exec'), ns)
    return ns['PILOT_SCHOOLS']


def save_schools(schools: list) -> None:
    """Write PILOT_SCHOOLS back to r1_schools_data.py."""
    shutil.copy2(SCHOOLS_PY, SCHOOLS_PY.with_suffix('.py.bak'))
    lines = [
        '# tenure_pipeline/r1_schools_data.py',
        '# ---------------------------------------------------------------------------',
        '# Master list of R1 CS departments for the PEER tenure pipeline.',
        '# Each school has a flat "urls" list — all URLs are equal candidates.',
        '# Add new URLs directly to the list; the pipeline tracks per-URL stats.',
        '#',
        "# To add a new URL for a school: put it in the 'new_url' column of",
        '# url_update_worksheet.csv and run apply_url_updates.py.',
        '# Cell 3A will query any URL not yet in the plan — no other action needed.',
        '#',
        '# Wave history:',
        '#   Original 9  : Cornell, UIUC, Indiana, UT Austin, UW-Madison, Purdue,',
        '#                 Georgia Tech, UMD, Brown',
        '#   Wave 2 +25  : Added April 4, 2026',
        '#   Wave 3 +80  : Added April 5, 2026',
        '# ---------------------------------------------------------------------------',
        '',
        'PILOT_SCHOOLS = [',
    ]
    for i, s in enumerate(schools):
        lines.append('    {')
        lines.append(f'        "university" : {json.dumps(s["university"])},')
        lines.append(f'        "dept_name"  : {json.dumps(s.get("dept_name", ""))},')
        urls = s.get('urls', [])
        if len(urls) == 0:
            lines.append('        "urls"       : [],')
        elif len(urls) == 1:
            lines.append(f'        "urls"       : [{json.dumps(urls[0])}],')
        else:
            lines.append('        "urls"       : [')
            for j, u in enumerate(urls):
                comma = ',' if j < len(urls) - 1 else ''
                lines.append(f'            {json.dumps(u)}{comma}')
            lines.append('        ],')
        lines.append(f'        "notes"      : {json.dumps(s.get("notes", ""))},')
        lines.append('    },')
    lines.append(']')
    lines.append('')
    SCHOOLS_PY.write_text('\n'.join(lines), encoding='utf-8')


# ── Load plan state (URL-level) ────────────────────────────────────────────
def load_url_stats() -> tuple[set, dict, dict, dict, dict]:
    """
    Returns:
        tried_urls   : set of all source URLs that have been CDX-queried
        url_html     : url → count of HTML files on disk for that source_url
        url_parsed   : uni_slug → count of parsed records
        url_status   : url → 'ok' | 'empty' | 'condemned' | 'untried'
        school_snaps : uni_slug → count of unique plan rows (by local_path) with n_snaps >= 1
    """
    tried_urls  = set()
    url_html_raw = defaultdict(int)
    url_status_by_norm = {}   # normalize_faculty_url(u) → status
    _counted_files = set()    # (norm_url, local_path) — plan JSONL may contain duplicate lines
    slug_plan_paths = defaultdict(set)  # uni_slug → set of local_path (deduped snapshot slots)

    if PLAN_JSONL.exists():
        for line in PLAN_JSONL.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r.get('plan_row_type') == 'cdx_bookmark':
                for key in ('source_url', 'tried_primary_url'):
                    u = r.get(key)
                    if u:
                        tried_urls.add(u)
                        nu = normalize_faculty_url(u)
                        url_status_by_norm.setdefault(nu, 'ok')
                for u in r.get('tried_urls', []):
                    tried_urls.add(u)
                    nu = normalize_faculty_url(u)
                    url_status_by_norm.setdefault(nu, 'empty')
                continue
            n = r.get('n_snaps', 1)
            slug = r.get('uni_slug') or ''
            lp = r.get('local_path')
            if slug and n >= 1 and lp:
                slug_plan_paths[slug].add(lp)
            for key in ('source_url', 'tried_primary_url'):
                u = r.get(key)
                if u:
                    tried_urls.add(u)
                    nu = normalize_faculty_url(u)
                    if n == 0:
                        url_status_by_norm.setdefault(nu, 'empty')
                    elif n == -1:
                        # Real condemnation has a reason; Cell 3A bookmarks use -1 without reason
                        if r.get('reason'):
                            url_status_by_norm[nu] = 'condemned'
                        else:
                            url_status_by_norm.setdefault(nu, 'ok')
                    else:
                        url_status_by_norm.setdefault(nu, 'ok')
            for u in r.get('tried_urls', []):
                tried_urls.add(u)
                nu = normalize_faculty_url(u)
                url_status_by_norm.setdefault(nu, 'empty')
            # Count HTML files via local_path (aggregate by normalized URL)
            if n >= 1 and r.get('local_path') and r.get('source_url'):
                lp = r['local_path']
                nu = normalize_faculty_url(r['source_url'])
                key = (nu, lp)
                if key in _counted_files:
                    continue
                p = WORKSPACE / lp
                if p.exists():
                    _counted_files.add(key)
                    url_html_raw[nu] += 1

    # Also expose tried_urls under normalized keys for apply_updates duplicate detection
    for u in list(tried_urls):
        tried_urls.add(normalize_faculty_url(u))

    # Parsed record counts per slug → attribute to the school's first 'ok' URL
    url_parsed = defaultdict(int)
    if PARSED_JSONL.exists():
        slug_parsed = defaultdict(int)
        for line in PARSED_JSONL.read_text(encoding='utf-8').splitlines():
            if not line.strip(): continue
            r = json.loads(line)
            slug_parsed[r.get('uni_slug', '')] += 1
        # Map slug → parsed count; we'll distribute to URLs in the worksheet builder
        url_parsed = dict(slug_parsed)   # keyed by slug, resolved per-school in build_worksheet

    # Per-row lookups use the school list URL string; bridge via normalize → stats
    url_html = dict(url_html_raw)
    url_status = url_status_by_norm
    school_snaps = {s: len(paths) for s, paths in slug_plan_paths.items() if s}

    return tried_urls, url_html, url_parsed, url_status, school_snaps


# ── Build worksheet ────────────────────────────────────────────────────────
def build_worksheet() -> None:
    schools    = load_schools()
    tried_urls, url_html, slug_parsed, url_status, school_snaps = load_url_stats()
    disk_by_slug = load_disk_html_by_slug()

    rows = []
    for s in schools:
        uni   = s['university']
        slug  = slugify(uni)
        urls  = s.get('urls', [])
        total_parsed = slug_parsed.get(slug, 0)

        disk_total = disk_by_slug.get(slug, 0)
        s_snaps = school_snaps.get(slug, 0)
        s_html = disk_total

        for url in urls:
            nu = normalize_faculty_url(url)
            status = url_status.get(nu, 'untried')
            n_html = url_html.get(nu, 0)
            # Primary row: if plan keys still do not match (sync/path issues), show disk total.
            # Do not attribute disk files to a primary URL that CDX marked empty (wrong alt URL first).
            if url == urls[0] and n_html == 0 and disk_total > 0 and status != 'empty':
                n_html = disk_total
            # Only show parsed count on the first (primary) URL to avoid duplication
            n_parsed = total_parsed if url == urls[0] else 0
            rows.append({
                'university'    : uni,
                'dept_name'     : s.get('dept_name', ''),
                'uni_slug'      : slug,
                'url'           : url,
                'n_html_files'  : n_html,
                'n_parsed_recs' : n_parsed,
                'status'        : status,
                'school_snaps'  : s_snaps,
                'school_html'   : s_html,
                'new_url'       : '',
            })

    # Sort: low school coverage first (same value on every row for that school), then URL status
    def sort_key(r):
        order = {'untried': 0, 'empty': 1, 'condemned': 2, 'ok': 3}
        return (
            int(r['school_snaps'] or 0),
            int(r['school_html'] or 0),
            order.get(r['status'], 9),
            -int(r['n_html_files'] or 0),
            r['university'],
            r['url'],
        )

    rows.sort(key=sort_key)

    fieldnames = ['university', 'dept_name', 'uni_slug', 'url',
                  'n_html_files', 'n_parsed_recs', 'status',
                  'school_snaps', 'school_html', 'new_url']
    with open(WORKSHEET, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    n_ok       = sum(1 for r in rows if r['status'] == 'ok')
    n_untried  = sum(1 for r in rows if r['status'] == 'untried')
    n_empty    = sum(1 for r in rows if r['status'] == 'empty')
    n_condemned= sum(1 for r in rows if r['status'] == 'condemned')
    print(f"  Worksheet rebuilt: {len(rows)} URL rows across {len(schools)} schools")
    print(f"    ok={n_ok}  untried={n_untried}  empty={n_empty}  condemned={n_condemned}")
    print(f"  Output: {WORKSHEET}")


# ── Apply updates ─────────────────────────────────────────────────────────
def apply_updates() -> None:
    if not WORKSHEET.exists():
        print("No worksheet found — building it now.")
        build_worksheet()
        return

    rows = list(csv.DictReader(WORKSHEET.read_text(encoding='utf-8').splitlines()))
    updates = [(r['university'].strip(), r['new_url'].strip())
               for r in rows if r.get('new_url', '').strip()]

    if not updates:
        print("No new_url entries found in worksheet — nothing to apply.")
        build_worksheet()
        return

    tried_urls, url_html, slug_parsed, url_status, _school_snaps = load_url_stats()
    schools = load_schools()
    school_idx = {s['university']: i for i, s in enumerate(schools)}

    changed       = []
    already_there = []
    already_tried = []

    for uni, new_url in updates:
        if uni not in school_idx:
            print(f"  ⚠  '{uni}' not found in r1_schools_data.py — skipping")
            continue
        idx  = school_idx[uni]
        urls = schools[idx].get('urls', [])

        if new_url in urls:
            # URL already in the list
            nn = normalize_faculty_url(new_url)
            status = url_status.get(nn, 'untried')
            if status == 'ok':
                n_html   = url_html.get(nn, 0)
                n_parsed = slug_parsed.get(slugify(uni), 0)
                msg = f"already in urls list — {n_html} HTML files, {n_parsed} parsed records"
            elif status == 'empty':
                msg = "already in urls list — CDX found 0 Wayback snapshots for this URL"
            elif status == 'condemned':
                msg = "already in urls list — URL was condemned by Cell 4 (bad parse)"
            else:
                msg = "already in urls list — status: untried (will be queried next run)"
            already_there.append((uni, new_url, msg))
            continue

        if normalize_faculty_url(new_url) in tried_urls or new_url in tried_urls:
            status = url_status.get(normalize_faculty_url(new_url), 'unknown')
            already_tried.append((uni, new_url, f"URL was previously tried as status='{status}'"))
            continue

        # New URL — add it
        schools[idx]['urls'].append(new_url)
        changed.append((uni, new_url))

    if changed:
        save_schools(schools)
        print(f"\n  ✅  Added {len(changed)} new URL(s) to r1_schools_data.py:")
        for uni, url in changed:
            print(f"      {uni}: {url}")
        print("  → Run Cells 0 → 2 → 3A → 3B → 4 to scrape.")
    else:
        print("\n  No new URLs to add.")

    if already_there:
        print(f"\n  ℹ  {len(already_there)} URL(s) already present:")
        for uni, url, msg in already_there:
            print(f"      {uni}: {url[:70]}")
            print(f"        → {msg}")

    if already_tried:
        print(f"\n  ⚠  {len(already_tried)} URL(s) previously tried (not added):")
        for uni, url, msg in already_tried:
            print(f"      {uni}: {url[:70]}")
            print(f"        → {msg}")
        print("  Tip: change the URL and try again, or accept that Wayback has no data for it.")

    print()
    build_worksheet()


# ── Entry point ───────────────────────────────────────────────────────────
if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Apply URL updates and rebuild worksheet')
    p.add_argument('--build-only', action='store_true',
                   help='Just rebuild the worksheet without applying updates')
    args = p.parse_args()

    if args.build_only:
        build_worksheet()
    else:
        apply_updates()
