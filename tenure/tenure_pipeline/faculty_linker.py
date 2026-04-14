"""
faculty_linker.py  —  Stage 5: Longitudinal Faculty Panel Builder
==================================================================
Takes the per-snapshot parsed records from Stage 4 and links the same
person across snapshot years within a school, producing a tidy panel with
one row per (uni_slug, faculty_id, year, season, rank).

Key functions
-------------
    normalize_faculty_name(name)  →  str   canonical match key
    build_panel(parsed_records)   →  list[dict]   linked panel records (one row per snapshot file when local_path differs)
    collision_report(panel)       →  list[dict]   ambiguous name keys
    load_plan_snapshot_lookup(plan_path) → dict   join key → Wayback fields
    attach_wayback_metadata(panel, lookup) → (list, meta)

Panel record schema
-------------------
    uni_slug        str     e.g. 'cornell_university'
    university      str     e.g. 'Cornell University'
    faculty_id      str     '<uni_slug>|<name_key>'
    name_key        str     normalised name used for linking
    name_display    str     most-common raw name for this key (for display)
    year            int
    season          str     'spring' | 'fall'
    rank            str     canonical rank label  ('unknown' when not visible on page)
    rank_raw        str     raw rank string from HTML
    parse_strategy  str     winning html_parser strategy for this snapshot
    local_path      str     workspace-relative HTML path (for joining CDX plan)
    collision       bool    True if two different display names share this key

After attach_wayback_metadata (Cell 5)
----------------------------------------
    wayback_timestamp str   14-digit Internet Archive timestamp (from plan)
    snpsht_dt         str   ISO 8601 datetime derived from wayback_timestamp
    wayback_url       str
    source_url        str   faculty-list URL archived
    source_id         str   first 8 hex of hash(source_url) when present
    plan_join         str   'ok' (full path) | 'ok_basename' (legacy vs Option B) | 'missing'

Note on 'unknown' rank
----------------------
Since Apr 2026 the parser captures EVERYONE on the page — postdocs, research
staff, lecturers, etc. People whose title isn't visible in the HTML receive
rank='unknown'. RANK_PRIORITY ensures any named rank beats 'unknown' when
deduplicating within a (school, person, year, season).
"""

import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# Name normalisation
# ---------------------------------------------------------------------------

def normalize_faculty_name(name: str) -> str:
    """
    Canonical match key for cross-year linking within a school.

    Steps applied in order:
      1. Unicode → ASCII (José → jose, Müller → muller)
      2. Lowercase
      3. Strip generational suffixes  (Jr, Sr, II, III, IV, V)
      4. Strip middle initials  (John A. Smith → john smith)
      5. Strip remaining punctuation
      6. Collapse whitespace
    """
    if not name or not str(name).strip():
        return ""

    s = str(name).strip()

    # Step 1: Transliterate accented chars to ASCII (é→e, ü→u, ñ→n …)
    s = unicodedata.normalize("NFD", s)
    s = s.encode("ascii", "ignore").decode("ascii")

    # Step 2: Lowercase
    s = s.lower()

    # Step 3: Strip generational suffixes at end of string (abbreviations and full words)
    s = re.sub(r"\s+(junior|senior|jr\.?|sr\.?|ii|iii|iv|v)\s*$", "", s, flags=re.I)

    # Step 4: Strip middle initials — single letter followed by period (John A. Smith)
    #         Also handles: "John A Smith" (initial without period, surrounded by spaces)
    s = re.sub(r"\b[a-z]\.\s*", " ", s)          # with period  — J. → removed
    s = re.sub(r"(?<=\s)[a-z](?=\s)", " ", s)    # without period — " A " → " "

    # Step 5: Strip punctuation (apostrophes, hyphens kept as space for compound names)
    s = re.sub(r"['\-]", " ", s)    # O'Brien → o brien, Smith-Jones → smith jones
    s = re.sub(r"[^a-z0-9\s]", "", s)

    # Step 6: Collapse whitespace
    s = re.sub(r"\s+", " ", s).strip()

    return s


# ---------------------------------------------------------------------------
# Panel builder
# ---------------------------------------------------------------------------

def build_panel(parsed_records: list) -> tuple:
    """
    Link faculty across snapshot years within each school.

    Parameters
    ----------
    parsed_records : list of dicts from faculty_snapshots_parsed.jsonl
        Required keys: uni_slug, university, year, season, name, rank, rank_raw

    Returns
    -------
    panel   : list[dict]   — one row per (uni_slug, faculty_id, year, season, local_path)
    meta    : dict         — summary statistics
    """
    # --- 1. Build name_key for every raw record ---
    keyed = []
    for r in parsed_records:
        key = normalize_faculty_name(r.get("name", ""))
        if not key:
            continue
        keyed.append({**r, "name_key": key})

    # --- 2. Per school: pick best display name for each name_key
    #         (most-frequently seen raw name → stable label)
    school_key_names: dict[str, dict[str, Counter]] = defaultdict(lambda: defaultdict(Counter))
    for r in keyed:
        school_key_names[r["uni_slug"]][r["name_key"]][r["name"]] += 1

    display_name: dict[tuple, str] = {}   # (uni_slug, name_key) → display name
    for slug, keys in school_key_names.items():
        for key, name_counter in keys.items():
            display_name[(slug, key)] = name_counter.most_common(1)[0][0]

    # --- 3. Collision detection
    #         A collision occurs when two *distinct* display names share the same key
    #         at the same school (e.g. "J. Smith" → john smith ← "Joan Smith")
    collision_keys: set[tuple] = set()
    for (slug, key), disp in display_name.items():
        # All raw names that produced this key at this school
        all_names = list(school_key_names[slug][key].keys())
        # Normalise each raw name and check uniqueness
        normed = {normalize_faculty_name(n) for n in all_names}
        if len(normed) > 1:
            collision_keys.add((slug, key))

    # --- 4. Deduplicate within (uni_slug, name_key, year, season)
    #         Keep the row with the highest-confidence rank.
    #         'unknown' is last — any named rank beats it.
    RANK_PRIORITY = {
        # tenure-track / tenured
        "full":              0,
        "associate":         1,
        "assistant":         2,
        # named distinguished chairs (usually full)
        "distinguished":     3,
        "endowed":           4,
        # post-tenure
        "emeritus":          5,
        # research-track professors
        "research_prof":     6,
        "teaching_prof":     7,
        # affiliated / modified appointments
        "clinical":          8,
        "adjunct":           9,
        "visiting":         10,
        "courtesy":         11,
        "affiliate":        12,
        # non-tenure-track named roles
        "senior_researcher": 13,
        "research_scientist":14,
        "research_associate":15,
        "senior_lecturer":   16,
        "lecturer":         17,
        "instructor":       18,
        "scientist":        19,
        "fellow":           20,
        "postdoc":          21,
        # catch-all named
        "other":            22,
        # no rank visible on page — lowest priority
        "unknown":          99,
    }

    # One row per (school, person, calendar year, season, **snapshot file**).
    # Multiple Wayback captures in the same nominal season → distinct local_path → keep all.
    seen: dict[tuple, dict] = {}   # (slug, key, year, season, local_path) → best row
    for r in keyed:
        lp = r.get("local_path", "") or ""
        uid = (r["uni_slug"], r["name_key"], r["year"], r["season"], lp)
        if uid not in seen:
            seen[uid] = r
        else:
            existing_pri = RANK_PRIORITY.get(seen[uid]["rank"], 99)
            new_pri      = RANK_PRIORITY.get(r["rank"],         99)
            if new_pri < existing_pri:
                seen[uid] = r

    # --- 5. Build output panel rows ---
    panel = []
    for (slug, key, year, season, _lp), r in sorted(seen.items()):
        is_collision = (slug, key) in collision_keys
        panel.append({
            "uni_slug":       slug,
            "university":     r["university"],
            "faculty_id":     f"{slug}|{key}",
            "name_key":       key,
            "name_display":   display_name[(slug, key)],
            "year":           int(year),
            "season":         season,
            "rank":           r["rank"],
            "rank_raw":       r.get("rank_raw", ""),
            "parse_strategy": r.get("parse_strategy", ""),
            "local_path":     r.get("local_path", ""),
            "collision":      is_collision,
        })

    # --- 6. Summary metadata ---
    unique_people = {(r["uni_slug"], r["name_key"]) for r in panel}
    n_faculty     = len(unique_people)
    n_collision   = len(collision_keys)
    n_schools     = len({r["uni_slug"] for r in panel})

    # Rank breakdown across unique people (use their most-common non-unknown rank)
    TENURE_TRACK = {"full", "associate", "assistant", "distinguished", "endowed"}
    person_best_rank: dict[tuple, str] = defaultdict(lambda: "unknown")
    for r in panel:
        pid = (r["uni_slug"], r["name_key"])
        cur = person_best_rank[pid]
        new = r["rank"]
        if RANK_PRIORITY.get(new, 99) < RANK_PRIORITY.get(cur, 99):
            person_best_rank[pid] = new

    rank_counts = Counter(person_best_rank.values())
    n_tenure_track = sum(v for k, v in rank_counts.items() if k in TENURE_TRACK)
    n_unknown      = rank_counts.get("unknown", 0)

    meta = {
        "n_records":       len(panel),
        "n_faculty":       n_faculty,
        "n_tenure_track":  n_tenure_track,
        "n_unknown_rank":  n_unknown,
        "n_other_named":   n_faculty - n_tenure_track - n_unknown,
        "n_schools":       n_schools,
        "n_collisions":    n_collision,
        "rank_breakdown":  dict(rank_counts.most_common()),
    }

    return panel, meta


# ---------------------------------------------------------------------------
# Collision report (for QA)
# ---------------------------------------------------------------------------

def collision_report(panel: list) -> list:
    """
    Return one dict per collision key showing the competing display names.
    Useful for manual inspection or building an alias table.
    """
    collisions = [r for r in panel if r.get("collision")]
    by_key: dict[tuple, list] = defaultdict(list)
    for r in collisions:
        by_key[(r["uni_slug"], r["name_key"])].append(r["name_display"])

    report = []
    for (slug, key), names in sorted(by_key.items()):
        unique_names = sorted(set(names))
        report.append({
            "uni_slug":      slug,
            "name_key":      key,
            "display_names": unique_names,
            "n_names":       len(unique_names),
        })
    return report


# ---------------------------------------------------------------------------
# Wayback / CDX plan join (exact timestamps for analysis clock)
# ---------------------------------------------------------------------------

def normalize_local_path(p: str) -> str:
    """Stable key for matching parsed rows to faculty_snapshots_plan.jsonl lines."""
    if not p or not str(p).strip():
        return ""
    return Path(str(p).strip()).as_posix()


def wayback_timestamp_to_iso(ts: str) -> str:
    """Parse 14-digit IA timestamp to ISO datetime string; empty if invalid."""
    if not ts:
        return ""
    s = "".join(ch for ch in str(ts) if ch.isdigit())
    if len(s) < 8:
        return ""
    s = (s + "00000000000000")[:14]
    try:
        return datetime.strptime(s, "%Y%m%d%H%M%S").isoformat()
    except ValueError:
        return ""


def load_plan_snapshot_lookup(plan_path: Path) -> tuple:
    """
    Build two lookups from faculty_snapshots_plan.jsonl:

    1. **by_path** — (uni_slug, year, season, local_path_norm) → plan fields.
       Matches Cell 4 rows when parsed ``local_path`` equals the plan path.

    2. **by_basename_unique** — (uni_slug, year, season, filename) → plan fields,
       only when **exactly one** plan row exists for that tuple (e.g. legacy flat
       ``.../2007_fall.html`` vs Option B ``.../<source_id>/2007_fall.html``).

    Returns (by_path, by_basename_unique).
    """
    import json as _json

    by_path: dict[tuple, dict] = {}
    basename_bucket: dict[tuple, list] = defaultdict(list)
    plan_path = Path(plan_path)
    if not plan_path.exists():
        return by_path, {}

    def _meta_from_row(r: dict) -> dict:
        wts = str(r.get("timestamp", ""))
        return {
            "wayback_timestamp": wts,
            "snpsht_dt":         wayback_timestamp_to_iso(wts),
            "wayback_url":       r.get("wayback_url", "") or "",
            "source_url":        r.get("source_url", "") or "",
            "source_id":         r.get("source_id", "") or "",
        }

    with open(plan_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = _json.loads(line)
            except _json.JSONDecodeError:
                continue
            if r.get("year") is None or not r.get("local_path") or not r.get("timestamp"):
                continue
            slug = r.get("uni_slug") or ""
            if not slug:
                continue
            lp = normalize_local_path(r["local_path"])
            meta = _meta_from_row(r)
            by_path[(slug, int(r["year"]), r.get("season", ""), lp)] = meta
            fname = Path(lp).name
            basename_bucket[(slug, int(r["year"]), r.get("season", ""), fname)].append(meta)

    by_basename_unique: dict[tuple, dict] = {}
    for k, metas in basename_bucket.items():
        if len(metas) == 1:
            by_basename_unique[k] = metas[0]

    return by_path, by_basename_unique


def attach_wayback_metadata(panel: list, plan_lookups: tuple) -> tuple:
    """
    Add exact Wayback fields from the CDX plan to each panel row.

    ``plan_lookups`` is the pair returned by ``load_plan_snapshot_lookup``:
    (by_path, by_basename_unique). Match order: full path, then basename when unique.

    Rows without a match get empty strings and plan_join='missing'.
    """
    if isinstance(plan_lookups, tuple) and len(plan_lookups) == 2:
        by_path, by_bn = plan_lookups
    elif isinstance(plan_lookups, dict):
        by_path, by_bn = plan_lookups, {}
    else:
        by_path, by_bn = {}, {}

    out = []
    n_ok = n_ok_bn = n_miss = 0
    for row in panel:
        lp = normalize_local_path(row.get("local_path", ""))
        slug = row.get("uni_slug", "")
        yr = int(row["year"])
        season = row.get("season", "")
        key_full = (slug, yr, season, lp)
        meta = by_path.get(key_full)
        join_how = "path"

        if not meta and lp:
            bn_key = (slug, yr, season, Path(lp).name)
            meta = by_bn.get(bn_key)
            join_how = "basename_unique"

        new = dict(row)
        if meta:
            new.update(meta)
            new["plan_join"] = "ok" if join_how == "path" else "ok_basename"
            if join_how == "path":
                n_ok += 1
            else:
                n_ok_bn += 1
        else:
            new["wayback_timestamp"] = ""
            new["snpsht_dt"] = ""
            new["wayback_url"] = ""
            new["source_url"] = ""
            new["source_id"] = ""
            new["plan_join"] = "missing"
            n_miss += 1
        out.append(new)

    join_meta = {
        "n_plan_join_ok":           n_ok,
        "n_plan_join_ok_basename":  n_ok_bn,
        "n_plan_join_missing":      n_miss,
    }
    return out, join_meta
