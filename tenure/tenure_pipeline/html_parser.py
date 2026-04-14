"""
html_parser.py  —  Faculty name + rank extractor for Tenure Pipeline Stage 4
=============================================================================
Multi-strategy parser for R1 CS department faculty pages.

Design change (Apr 2026): capture EVERYONE on the page regardless of rank —
postdocs, visiting faculty, instructors, research scientists, staff, etc.
Rank is recorded as metadata when present; records without a recognisable rank
receive rank='unknown'.

Strategies (all rank-optional except the last):
  Strategy 1  Drupal Views containers  (div/li.views-row, .person-listing)
  Strategy 2  Table rows               (column detection, then name extraction)
  Strategy 3  Div / li person cards    (person-box, PeopleEntry, faculty-card, …)
  Strategy 4  Profile link harvester   (anchors with name-like text in faculty sections)
  Strategy 5  Generic rank-anchor      (rank required — broad fallback)

Name formats (cross-cutting — not a separate numbered strategy):
  ``_extract_name()`` tries "First Last" word patterns first, then "Lastname, Firstname"
  comma format (legacy directory tables). Every strategy that calls ``_extract_name`` or
  ``_is_name_like`` benefits automatically. Strategy 3b still applies an extra
  ``_extract_name_lastfirst(full)`` pass on multi-line chunks where needed.

Entry point:
    records = extract_faculty(html_path, uni_slug=None)
    # returns list of dicts: {name, rank, rank_raw, parse_strategy}

    records, meta = extract_faculty(html_path, return_meta=True)
    # meta = {'winner': 'strategy_3_div_cards',
    #         'counts': {'strategy_1_drupal': 0, ...}}
"""

import re
from pathlib import Path
from lxml import etree

# ---------------------------------------------------------------------------
# Rank vocabulary  (ORDER MATTERS — most specific first)
# ---------------------------------------------------------------------------
_RANK_PAIRS = [
    # --- emeritus ---
    (r'professor\s+emerit(?:us|a)',                             'emeritus'),
    (r'emerit(?:us|a)\s+professor',                             'emeritus'),
    # --- compound modifiers (adjunct / visiting / research / clinical) ---
    (r'adjunct\s+(?:associate\s+|assistant\s+)?professor',      'adjunct'),
    (r'visiting\s+(?:associate\s+|assistant\s+)?professor',     'visiting'),
    (r'research\s+(?:associate\s+|assistant\s+)?professor',     'research_prof'),
    (r'clinical\s+(?:associate\s+|assistant\s+)?professor',     'clinical'),
    (r'teaching\s+professor|professor\s+of\s+practice',         'teaching_prof'),
    (r'distinguished\s+professor',                              'distinguished'),
    (r'endowed\s+(?:associate\s+|assistant\s+)?professor',      'endowed'),
    (r'courtesy\s+(?:associate\s+|assistant\s+)?professor',     'courtesy'),
    # --- plain tenure-track ranks ---
    (r'assistant\s+professor',                                  'assistant'),
    (r'associate\s+professor',                                  'associate'),
    (r'professor',                                              'full'),
    # --- bare emeritus (after compound patterns) ---
    (r'emerit(?:us|a)',                                         'emeritus'),
    # --- non-tenure-track academic roles ---
    (r'postdoctoral\s+(?:research\s+)?(?:associate|fellow|scholar|researcher)?',  'postdoc'),
    (r'post[-\s]doc(?:toral)?',                                 'postdoc'),
    (r'research\s+scientist',                                   'research_scientist'),
    (r'senior\s+research(?:er|er\s+scientist)?',                'senior_researcher'),
    (r'research\s+(?:associate|fellow|engineer)',               'research_associate'),
    (r'senior\s+lecturer',                                      'senior_lecturer'),
    (r'lecturer',                                               'lecturer'),
    (r'instructor',                                             'instructor'),
    (r'fellow',                                                 'fellow'),
    (r'scientist',                                              'scientist'),
    (r'affiliate\s+(?:associate\s+|assistant\s+)?(?:professor|faculty)',  'affiliate'),
    (r'affiliate',                                              'affiliate'),
]

RANK_RE = re.compile(
    r'\b(' + '|'.join(p for p, _ in _RANK_PAIRS) + r')\b', re.I
)


def _norm_rank(raw: str) -> str:
    """Normalise a raw rank string to a canonical label."""
    raw_l = raw.lower().strip()
    for pattern, label in _RANK_PAIRS:
        if re.search(pattern, raw_l, re.I):
            return label
    return 'other'


# ---------------------------------------------------------------------------
# Name pattern  —  2–5 words, each starting with a capital letter
#   Allows hyphens, apostrophes, accented chars, and middle initials like "A."
# ---------------------------------------------------------------------------
_NAME_WORD = r"[A-ZÀ-Ý][a-zA-Zà-ÿ'\-]+"
_INIT      = r'[A-Z]\.'
_NAME_RE   = re.compile(
    rf'\b({_NAME_WORD}(?:\s+(?:{_INIT}|{_NAME_WORD})){{1,4}})\b'
)

_REJECT_NAME = re.compile(
    r'\b(Computer|Science|Engineering|Department|University|Research|Institute'
    r'|Laboratory|School|College|Professor|Associate|Assistant|Director'
    r'|Chair|Dean|Machine|Learning|Artificial|Intelligence|New\s+York'
    r'|Los\s+Angeles|San\s+Diego|North\s+Carolina|Carnegie\s+Mellon'
    r'|Collegiate|Herbert|Scholar|Visiting|Emeritus|Adjunct|Clinical'
    r'|Distinguished|Endowed|Regents|Honorary|Courtesy|Affiliate'
    r'|Bio\b|Email|Phone|Office|Building|Room|Hall|Center|Track|Tenure'
    r'|Joined|Faculty|Directory|Investigators|Staff|People|Scientist'
    r'|Graduate|Undergraduate|Doctoral|Program|Division|Systems'
    r'|Network|Software|Hardware|Theory|Security|Database|Graphics'
    r'|Postdoctoral|Postdoc|Lecturer|Instructor|Fellow|Teaching'
    r'|Methods|Algorithms|Verification|Cryptography|Robotics|Biology'
    r'|Interfaces|Visualization|Bioinformatics|Parallelism|Compilers'
    r'|Complexity|Architecture|Networking|Computing|Languages|Distributed'
    r'|Embedded|Multimedia|Analytics|Informatics|Simulation|Modeling)\b',
    re.I
)

_PREFIX_STRIP = re.compile(r'^\s*(?:Bio|Dr\.?|Prof\.?|Mr\.?|Ms\.?|Mrs\.?)\s+', re.I)

# "Lastname, Firstname" / "Lastname, Firstname M." — used by _extract_name (all strategies)
# and explicitly in strategy_3b for multi-line li cards.
_COMMA_NAME_RE = re.compile(
    r'^([A-ZÀ-Ý][a-zA-Zà-ÿ\'\-]+),\s*([A-ZÀ-Ý][a-zA-Zà-ÿ\'\-]+(?:\s+[A-Z]\.)?)'
)


def _extract_name_lastfirst(text: str):
    """Handle 'Last, First [Middle]' reversed-name format → return 'First Last'."""
    m = _COMMA_NAME_RE.match(text.strip())
    if not m:
        return None
    last, first = m.group(1), m.group(2)
    name = f'{first} {last}'
    if _REJECT_NAME.search(name):
        return None
    return name


def _extract_name(text: str):
    """Return best candidate person name from a text chunk, or None."""
    text = _PREFIX_STRIP.sub('', text)
    candidates = _NAME_RE.findall(text)
    for cand in reversed(candidates):
        words = cand.split()
        if len(words) < 2:
            continue
        if _REJECT_NAME.search(cand):
            continue
        if all(w.isupper() and len(w) > 2 for w in words):
            continue
        if len(words) > 5:
            continue
        return cand
    # Legacy directory tables: "Lastname, Firstname" in one cell / anchor (see module docstring).
    return _extract_name_lastfirst(text) or None


def _is_name_like(txt: str) -> bool:
    """True if txt looks like a person name (2–4 capitalised words, short)."""
    txt = txt.strip()
    if not txt or len(txt) > 55 or len(txt) < 4:
        return False
    return _extract_name(txt) is not None


# ---------------------------------------------------------------------------
# DOM helpers
# ---------------------------------------------------------------------------
SKIP_TAGS = frozenset(['script', 'style', 'head', 'noscript', 'meta',
                       'link', 'nav', 'footer', 'header', 'aside', 'form'])


def _el_text(el) -> str:
    """Concatenate all text within an element, skipping SKIP_TAGS subtrees."""
    parts = []
    for node in el.iter():
        if not isinstance(node.tag, str):
            continue
        if node.tag in SKIP_TAGS:
            continue
        try:
            if node.text:
                parts.append(node.text.strip())
            if node.tail:
                parts.append(node.tail.strip())
        except (UnicodeDecodeError, ValueError):
            pass
    return ' '.join(p for p in parts if p)


def _safe_text(el) -> str:
    """Return el.text as a stripped string, safely handling encoding errors."""
    try:
        return (el.text or '').strip()
    except (UnicodeDecodeError, ValueError):
        return ''


def _extract_name_structural(el) -> str | None:
    """
    Find a person name from structural markup within a container element:
    anchors → headings → bold/strong.
    Rank keywords are NOT required.
    """
    # 1. <a> links with name-like text (profile links)
    for a in el.findall('.//a'):
        txt = _safe_text(a)
        if _is_name_like(txt):
            return _extract_name(txt)
    # 2. Heading tags
    for tag in ('h2', 'h3', 'h4', 'h5'):
        for h in el.findall(f'.//{tag}'):
            txt = _el_text(h).strip()
            name = _extract_name(txt)
            if name:
                return name
    # 3. Bold / strong
    for tag in ('strong', 'b'):
        for s in el.findall(f'.//{tag}'):
            txt = _safe_text(s)
            if _is_name_like(txt):
                return _extract_name(txt)
    # 4. Full text fallback
    return _extract_name(_el_text(el))


def _dedupe(records: list) -> list:
    """Deduplicate by normalised name (rank may differ; keep first seen)."""
    seen = set()
    out  = []
    for r in records:
        key = re.sub(r'\s+', ' ', r['name'].lower().strip())
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def _make_record(name: str, rank_raw: str = '', rank: str = '',
                 strategy: str = '') -> dict:
    return {
        'name':           name,
        'rank':           rank     or ('unknown' if not rank_raw else _norm_rank(rank_raw)),
        'rank_raw':       rank_raw,
        'parse_strategy': strategy,
    }


# ---------------------------------------------------------------------------
# Strategy 1 — Drupal Views  (rank OPTIONAL)
# ---------------------------------------------------------------------------
def _strategy_drupal_views(root) -> list:
    records = []
    containers = root.xpath(
        '//*[contains(@class,"views-row") or contains(@class,"person-listing")]'
    )
    for cont in containers:
        txt = _el_text(cont)
        if len(txt) > 800:
            continue

        m = RANK_RE.search(txt)
        if m:
            rank_raw = m.group(0)
            name     = _extract_name(txt[:m.start()])
        else:
            rank_raw = ''
            name     = _extract_name_structural(cont)

        if name:
            records.append(_make_record(name, rank_raw, strategy='strategy_1_drupal'))
    return records


# ---------------------------------------------------------------------------
# Strategy 2 — Table rows  (rank OPTIONAL — uses column detection)
# ---------------------------------------------------------------------------
def _strategy_tables(root) -> list:
    records = []
    for tbl in root.findall('.//table'):
        rows     = tbl.findall('.//tr')
        all_txts = [' '.join(_el_text(td) for td in r.findall('.//td')) for r in rows]

        # Decide if this table has rank-bearing cells
        has_rank = any(RANK_RE.search(t) for t in all_txts)
        prev_name = None

        for row, row_txt in zip(rows, all_txts):
            cells = [_el_text(td) for td in row.findall('.//td')]
            if not cells:
                ths = [_el_text(th) for th in row.findall('.//th')]
                cand = _extract_name(' '.join(ths))
                if cand:
                    prev_name = cand
                continue

            m = RANK_RE.search(row_txt)
            if m:
                rank_raw = m.group(0)
                name = None
                for i, cell in enumerate(cells):
                    if RANK_RE.search(cell):
                        for earlier in cells[:i]:
                            name = _extract_name(earlier)
                            if name:
                                break
                        if not name:
                            cm = RANK_RE.search(cell)
                            if cm:
                                name = _extract_name(cell[:cm.start()])
                        break
                if not name:
                    for cell in cells:
                        cm = RANK_RE.search(cell)
                        if cm:
                            name = _extract_name(cell[:cm.start()])
                            break
                if not name and prev_name:
                    name = prev_name
                if name:
                    records.append(_make_record(name, rank_raw, strategy='strategy_2_table'))
                    prev_name = None
                else:
                    prev_name = None

            elif has_rank:
                # Table has rank elsewhere — still try to harvest names from rank-less rows
                cand = _extract_name(cells[0]) if cells else None
                if cand:
                    prev_name = cand
            else:
                # No rank in whole table — try first cell as name
                cand = _extract_name(cells[0]) if cells else None
                if cand:
                    records.append(_make_record(cand, strategy='strategy_2_table'))

    return records


# ---------------------------------------------------------------------------
# Strategy 3 — Div / li person cards  (rank OPTIONAL)
# ---------------------------------------------------------------------------
_CARD_RE = re.compile(
    r'\b(person|faculty|people|member|profile|staff|directory|card|vcard'
    r'|PeopleEntry|eecs_person|facultyCard|faculty-card|person-box'
    r'|faculty-item|people-item|staff-item|person-wrapper|faculty-member)\b',
    re.I
)


def _strategy_div_cards(root) -> list:
    records = []
    for el in root.iter(etree.Element):
        if el.tag in SKIP_TAGS:
            continue
        cls = el.get('class', '')
        if not _CARD_RE.search(cls):
            continue
        txt = _el_text(el)
        if len(txt) > 1000 or len(txt) < 4:
            continue

        m = RANK_RE.search(txt)
        if m:
            rank_raw = m.group(0)
            name     = _extract_name(txt[:m.start()])
            if not name:
                name = _extract_name_structural(el)
        else:
            rank_raw = ''
            name     = _extract_name_structural(el)

        if name:
            records.append(_make_record(name, rank_raw, strategy='strategy_3_div_cards'))
    return records


# ---------------------------------------------------------------------------
# Strategy 3b — Alphabetical li cards  (e.g. NYU cs.nyu.edu/dynamic/people/)
# Pattern: <li id="faculty_A"> … <div class="col-sm-8"> Name\nRank … </div>
# Also handles any <li id^="faculty_"> or <li id^="person_"> pattern.
# Comma-name fallback: _extract_name() already tries Last, First; the extra
# _extract_name_lastfirst(full) below covers multi-line chunks where the first line
# alone is not the full name line.
# ---------------------------------------------------------------------------
def _strategy_alpha_li_cards(root) -> list:
    """
    Handles pages (e.g. NYU cs.nyu.edu/dynamic/people/) where faculty are in a
    <ul class='people-listing'> or <ul class='contacts'> (or similar), with li
    items that may optionally have id="faculty_A" etc. as alphabetical anchors.
    All li siblings in the detected ul are processed, not just the anchored ones.
    Also handles 'Last, First' reversed-name format (e.g. NYU researchers page).
    """
    records = []

    # Find parent ul via class names — covers both people-listing and contacts styles
    parent_uls = root.xpath(
        './/ul[contains(@class,"people") or contains(@class,"faculty") '
        'or contains(@class,"listing") or contains(@class,"directory") '
        'or contains(@class,"contacts")]'
    )

    # Fallback: find any li with faculty_/person_/staff_ id, use its parent
    if not parent_uls:
        anchor_li = root.xpath(
            './/li[@id and ('
            'starts-with(@id,"faculty_") or starts-with(@id,"person_") '
            'or starts-with(@id,"staff_") or starts-with(@id,"member_")'
            ')]'
        )
        parents = []
        for li in anchor_li:
            p = li.getparent()
            if p is not None and p not in parents:
                parents.append(p)
        parent_uls = parents

    if not parent_uls:
        return records

    for ul in parent_uls:
        all_li = ul.findall('li')
        if len(all_li) < 3:   # skip tiny navigation lists
            continue
        for li in all_li:
            # Prefer the text div; use div-only xpath to skip img with col-sm class
            content_div = li.xpath(
                './/div[contains(@class,"col-sm") or contains(@class,"col-xs") '
                'or contains(@class,"content") or contains(@class,"info")]'
            )
            target = content_div[0] if content_div else li
            full = _el_text(target)
            if not full or len(full) < 4 or len(full) > 1200:
                continue

            m = RANK_RE.search(full)
            rank_raw = m.group(0) if m else ''
            before   = full[:m.start()] if m else full.split('\n')[0]

            # Try normal First Last extraction first
            name = _extract_name(before)
            # Fallback: Last, First format (e.g. NYU contacts list)
            if not name:
                name = _extract_name_lastfirst(full)
            if not name:
                name = _extract_name_structural(target)

            if name:
                records.append(_make_record(name, rank_raw, strategy='strategy_3b_alpha_li'))

    return records


# ---------------------------------------------------------------------------
# Strategy 4 — Profile link harvester  (rank OPTIONAL — pure structural)
# Finds <a> elements with name-like text inside known faculty-section containers.
# ---------------------------------------------------------------------------
_SECTION_RE = re.compile(
    r'\b(faculty|people|directory|staff|person|member|profile|bio|team)\b',
    re.I
)
# URL patterns that suggest a personal faculty page
_PROFILE_URL_RE = re.compile(
    r'/(faculty|people|person|profile|bio|staff|team|directory)/', re.I
)


def _strategy_profile_links(root) -> list:
    records = []
    seen    = set()

    # Find containers that look like faculty sections
    section_els = []
    for el in root.iter(etree.Element):
        if el.tag in SKIP_TAGS:
            continue
        cls  = el.get('class', '') or ''
        id_  = el.get('id', '') or ''
        if _SECTION_RE.search(cls) or _SECTION_RE.search(id_):
            section_els.append(el)

    # If no labelled sections, fall back to entire body
    if not section_els:
        body = root.find('.//body')
        if body is not None:
            section_els = [body]

    for section in section_els:
        for a in section.findall('.//a'):
            href = a.get('href', '') or ''
            txt  = _safe_text(a)
            if not _is_name_like(txt):
                continue
            # Prefer links that look like profile URLs; allow any link
            # but reject mailto / javascript / anchor-only
            if href.startswith(('mailto:', 'javascript:', '#', 'tel:')):
                continue
            name = _extract_name(txt)
            if name and name not in seen:
                seen.add(name)
                records.append(_make_record(name, strategy='strategy_4_profile_links'))

    return records


# ---------------------------------------------------------------------------
# Strategy 5 — Generic rank-anchor fallback  (rank REQUIRED)
# Broad: any short text block containing a rank keyword.
# Kept rank-required to control noise as a last resort.
# ---------------------------------------------------------------------------
def _strategy_generic(root) -> list:
    records   = []
    seen_pos  = set()

    for el in root.iter(etree.Element):
        if el.tag in SKIP_TAGS:
            continue
        child_count = sum(1 for c in el if isinstance(c.tag, str))
        if child_count > 15:
            continue
        txt = _el_text(el)
        if len(txt) < 5 or len(txt) > 400:
            continue

        m = RANK_RE.search(txt)
        if not m:
            continue

        sig = (txt[:60], m.start())
        if sig in seen_pos:
            continue
        seen_pos.add(sig)

        rank_raw = m.group(0)
        name     = _extract_name(txt[:m.start()])
        if name:
            records.append(_make_record(name, rank_raw, strategy='strategy_5_generic'))

    return records


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------
_STRATEGIES = [
    ('strategy_1_drupal',        _strategy_drupal_views),
    ('strategy_2_table',         _strategy_tables),
    ('strategy_3_div_cards',     _strategy_div_cards),
    ('strategy_3b_alpha_li',     _strategy_alpha_li_cards),
    ('strategy_4_profile_links', _strategy_profile_links),
    ('strategy_5_generic',       _strategy_generic),
]


def extract_faculty(html_path, uni_slug=None, return_meta=False):
    """
    Parse an HTML faculty page and return a list of faculty records.

    Parameters
    ----------
    html_path   : str | Path
    uni_slug    : str | None   (reserved for future school-specific overrides)
    return_meta : bool         If True, return (records, meta_dict) instead of records.
                               meta_dict = {'winner': str, 'counts': {strategy: int}}

    Returns
    -------
    list of dict  with keys: name, rank, rank_raw, parse_strategy
    (or tuple if return_meta=True)
    """
    html_path = Path(html_path)
    try:
        raw = html_path.read_bytes()
        for enc in (None, 'latin-1', 'cp1252'):
            try:
                parser = etree.HTMLParser(recover=True, encoding=enc)
                root   = etree.fromstring(raw, parser)
                if root is not None:
                    break
            except Exception:
                continue
        else:
            empty_meta = {'winner': 'none', 'counts': {k: 0 for k, _ in _STRATEGIES}}
            return ([], empty_meta) if return_meta else []
    except Exception:
        empty_meta = {'winner': 'none', 'counts': {k: 0 for k, _ in _STRATEGIES}}
        return ([], empty_meta) if return_meta else []

    counts = {}
    best   = []
    winner = 'none'

    for name, fn in _STRATEGIES:
        records = _dedupe(fn(root))
        counts[name] = len(records)
        if len(records) > len(best):
            best   = records
            winner = name

    meta = {'winner': winner, 'counts': counts}
    return (best, meta) if return_meta else best


# Wayback rewrites HTML with absolute links like web.archive.org/web/YYYYMMDDHHMMSS/...
WAYBACK_TS_IN_HTML = re.compile(r'web\.archive\.org/web/(\d{8,14})(?:/|")', re.I)


def sniff_wayback_timestamp_from_html_file(path, max_bytes: int = 65536) -> str:
    """
    Read the first ``max_bytes`` of a saved Wayback HTML file and extract the capture
    timestamp from an embedded ``web.archive.org/web/<ts>/`` URL.  Returns a 14-digit
    string (padded) or '' if not found.

    Useful for legacy files named ``{year}_{season}.html`` without the timestamp in
    the filename — cheap (one small read) and good enough for QA or one-off backfills.
    """
    path = Path(path)
    try:
        with open(path, 'rb') as f:
            chunk = f.read(max_bytes)
    except OSError:
        return ''
    text = chunk.decode('utf-8', errors='ignore')
    m = WAYBACK_TS_IN_HTML.search(text)
    if not m:
        return ''
    ts = m.group(1)
    return (ts + '00000000000000')[:14]


def iter_html_zero_records(html_root: Path):
    """
    Yield paths to ``*.html`` under ``html_root`` where ``extract_faculty`` returns
    no records (still broken layouts, empty captures, non-faculty pages, etc.).

    Use after changing name/rank heuristics to find files worth spot-checking.
    Can be slow on a full ``faculty_snapshots`` tree.
    """
    html_root = Path(html_root)
    if not html_root.is_dir():
        return
    for p in sorted(html_root.rglob('*.html')):
        try:
            if len(extract_faculty(p)) == 0:
                yield p
        except Exception:
            yield p


# ---------------------------------------------------------------------------
# Quick test  (run directly to spot-check one HTML file)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2 and sys.argv[1] == '--scan':
        root = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        if not root or not root.is_dir():
            print("Usage: python html_parser.py --scan <faculty_snapshots_dir>")
            sys.exit(1)
        n = 0
        for p in iter_html_zero_records(root):
            print(p)
            n += 1
        print(f"\nTotal HTML files with 0 parsed faculty: {n}")
        sys.exit(0)

    path = sys.argv[1] if len(sys.argv) > 1 else None
    if not path:
        print("Usage: python html_parser.py <path/to/file.html>")
        print("       python html_parser.py --scan <faculty_snapshots_dir>")
        sys.exit(1)
    records, meta = extract_faculty(path, return_meta=True)
    print(f"\n{len(records)} records  |  winner: {meta['winner']}")
    print("Strategy counts:", meta['counts'])
    print()
    for r in records[:30]:
        rr = (r.get('rank_raw') or '')[:40]
        print(f"  {r['name']:<40} {r['rank']:<20} ({rr})")
