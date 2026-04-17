# `discover_faculty_urls.py` — Usage Guide

**Script:** `tenure/tenure_pipeline/discover_faculty_urls.py`
**Agent:** PEER | **Written:** 2026-04-16 | **Revised:** 2026-04-16 (rev 2 — matchType=domain algorithm)

---

## What It Is

A detective script that automatically answers the question:

> *"For each school where our parser is getting weak results, what better URL should we be feeding into the CDX scraper?"*

It replaces the manual 30-minute-per-school Wayback browsing workflow with a single automated run of ~15–20 minutes covering all 36 low-quality schools at once.

---

## Prerequisites — What Must Exist Before You Run It

| File | Required? | Why |
|------|-----------|-----|
| `tenure_pipeline/faculty_snapshots_strategy_audit.jsonl` | **Yes** | How the script identifies poor-quality schools. Cell 4 writes it. |
| `tenure_pipeline/r1_cs_departments.csv` | **Yes** | Provides the known URL list per school. |
| `tenure_pipeline/faculty_snapshots_plan.jsonl` | Optional | Flags already-tried URLs. If missing, all candidates are treated as novel. |

You also need an **internet connection** — the script makes live CDX API calls to the Wayback Machine.

---

## How to Run It

**Basic run** (from `~/Ivy_Net`):

```bash
python tenure/tenure_pipeline/discover_faculty_urls.py
```

**With live test-parse** — downloads one Wayback snapshot per top candidate, runs it through the HTML parser, and reports real faculty-record counts. Adds ~3–5 seconds per candidate but gives you a verified quality score:

```bash
TEST_PARSE=1 python tenure/tenure_pipeline/discover_faculty_urls.py
```

**To investigate more schools** — lower the threshold at the top of the file, then re-run:

```python
# In discover_faculty_urls.py, change:
QUALITY_THRESHOLD_MEAN_RECS = 20   # default — change to e.g. 50 to cast a wider net
```

---

## What It Actually Does, Step by Step

### Phase 1 — Identify Low-Quality Schools

Reads `faculty_snapshots_strategy_audit.jsonl` and computes `mean_recs`
(average number of faculty names parsed per HTML file) for every school.
Any school below the threshold (default: 20) goes on the investigation list.

Current state: **36 schools**, ranked worst-first:

```
 1.  vanderbilt_university              5.9 recs/file  (128 files)
 2.  university_of_nevada_reno          7.1 recs/file  (340 files)
 3.  mississippi_state_university       7.3 recs/file  (136 files)
 4.  penn_state_university              7.9 recs/file  (284 files)
 5.  university_of_hawaii               8.1 recs/file  (648 files)
 ... (31 more schools)
```

### Phase 2 — Load Known URLs

Reads `r1_cs_departments.csv` to get each school's current URL list and
reads the CDX plan to know which URLs have already been tried.

### Phase 3 — CDX Domain Query (Starting from the University Root)

This is the core algorithm and differs from a naive "query what we already know"
approach. Here is the reasoning:

**The problem with starting from a known subdomain:**
If our only known URL is `engineering.vanderbilt.edu/cs/`, a query for
`engineering.vanderbilt.edu/*` only finds pages *under that subdomain*. But CS
might have been housed at `cs.vanderbilt.edu/` in earlier years — and we would
miss it entirely.

**The manual workflow that inspired the fix:**
When you browse Wayback manually, you start at `www.vanderbilt.edu`, choose a
year, then navigate from the university homepage to wherever CS lived that year.
That naturally discovers `cs.vanderbilt.edu` in 2005 and `engineering.vanderbilt.edu/eecs/`
in 2012, even though you started from the same place.

**How the script automates this:**
For each known URL, the script strips off the subdomain to get the *apex domain*
(e.g., `cs.vanderbilt.edu` → `vanderbilt.edu`), then fires a CDX
`matchType=domain` query:

```
web.archive.org/cdx/search/cdx?url=vanderbilt.edu&matchType=domain&collapse=urlkey&...
```

`matchType=domain` returns **all URLs across all subdomains** — one query
discovers `cs.vanderbilt.edu/people/`, `engineering.vanderbilt.edu/eecs/`,
`www.vanderbilt.edu/academics/cs/`, and anything else Wayback ever crawled
under that university. This is exactly the university-root-first navigation
pattern you do manually, but done programmatically.

One CDX call per university (regardless of how many subdomain URLs we already
know), with polite delays: 1.5s between apex domains, 3s between schools.

### Phase 4 — Score and Rank Every Candidate URL

Each URL gets a composite score (max ~115 pts). Higher = more promising.

| Score Component | Max Points | What It Rewards |
|-----------------|-----------|----------------|
| **Keyword match** | 35 pts | Path contains `faculty`, `people`, `staff`, `phonebook`, `directory`, `personnel` — more keywords = higher score; high-value keywords get an extra bonus |
| **CS subdomain bonus** | 15 pts | The *subdomain itself* is a CS/engineering token: `cs.vanderbilt.edu`, `eecs.mit.edu`, `computing.utah.edu` → strong signal we found the right department. Partial bonus (8 pts) if CS tokens appear in the *path* instead (`/cs/`, `/eecs/`). This bonus is only possible because the `matchType=domain` query discovers subdomains we never knew about. |
| **Path depth** | 15 pts | 1–3 path segments is the sweet spot (e.g., `/people/faculty`); too deep suggests a profile page not a listing |
| **Snapshot count** | 20 pts | URLs captured 100+ times by Wayback are well-archived and stable |
| **Year span** | 15 pts | A URL archived from 2003–2024 is far more valuable than one captured only in 2019 |
| **Novelty bonus** | 15 pts | URLs not already in your school list get a bonus |
| **Hard penalty** | −999 pts | Paths containing `/course`, `/event`, `/news`, `.pdf`, `.js`, images, etc. → immediately discarded |

After initial ranking, the script does a **follow-up CDX count query** for
the top candidates to get their real snapshot counts and year ranges,
then re-scores with that precision data.

### Phase 5 — Output

Prints a ranked table per school to the console, then writes two files
(described below).

---

## Reading the Console Output

```
  [1/36]  Vanderbilt University  (cumulative 00:00)
    Known URLs: ['https://engineering.vanderbilt.edu/cs/...']
    CDX domain query: *.vanderbilt.edu/* …  18,443 unique URLs in 7.3s
    Refining counts for top 16 candidates …

  ──────────────────────────────────────────────────────────────────────────
  School    : Vanderbilt University  (vanderbilt_university)
  Quality   : 5.9 mean records/file  (128 audited files)
  Known URLs: 1
  ──────────────────────────────────────────────────────────────────────────
  Rank  Score   Count      Yrs  Depth  URL
  ────  ─────  ──────  ────────  ─────  ─────────────────────────────────────
     1   87.5     347  2005–2024      2  https://cs.vanderbilt.edu/people/     ★
     2   81.0     201  2008–2024      3  https://cs.vanderbilt.edu/people/faculty/ ★
     3   71.2      89  2010–2022      2  https://engineering.vanderbilt.edu/faculty/ ★
  ──────────────────────────────────────────────────────────────────────────
```

Note: scores are now higher than before (max ~115) because the CS-subdomain bonus
can add up to 15 pts to URLs like `cs.vanderbilt.edu/...`.

The `★` marks your **top 3** — those are the ones to try first.

**Column meanings:**

| Column | Meaning |
|--------|---------|
| **Score** | Composite score 0–~115 (higher = more promising; CS-subdomain URLs score higher) |
| **Count** | How many times Wayback captured this URL (347 = very well-archived) |
| **Yrs** | Year range of Wayback captures (2005–2024 = long-lived, stable page) |
| **Depth** | Path depth (2 = `/people/`, the sweet spot) |

---

## The Two Output Files

### `faculty_url_suggestions.csv` — the one you work with

Open this in Excel or Numbers. One row per candidate URL, sorted by school then rank.

| Column | Meaning |
|--------|---------|
| `uni_slug` | School identifier |
| `university` | Full school name |
| `mean_recs` | Current parse quality — why this school is on the list |
| `rank` | 1 = best candidate for that school |
| `score` | Composite score (0–100) |
| `snapshot_count` | How many Wayback captures exist for this URL |
| `year_min` / `year_max` | Year range of Wayback coverage |
| **`suggested_url`** | **The URL to paste into your worksheet** |
| `test_parse_recs` | Faculty records found if `TEST_PARSE=1`; blank otherwise |

### `faculty_url_suggestions.jsonl` — machine-readable

Same data in structured JSON, one object per school with a ranked `candidates` list.
Useful for filtering or processing programmatically; you will rarely need to open this directly.

---

## The Exact Workflow After It Runs

```
Step 1 — Review suggestions
    Open:  tenure_pipeline/faculty_url_suggestions.csv
    Filter to:  rank = 1 or 2 per school
    Prefer:     high snapshot_count  +  wide year range  +  high score
    Note the suggested_url values you want to try.

Step 2 — Add to worksheet
    Open:  tenure_pipeline/url_update_worksheet.csv
    For each school: find its rows, paste the suggested_url into new_url column
    Save the file.

Step 3 — Apply the updates
    python tenure/tenure_pipeline/apply_url_updates.py
    (adds the new URL to the school's list in r1_schools_data.py)

Step 4 — Re-run the pipeline for new URLs
    In the notebook:  Cell 0 → Cell 2 → Cell 3A → Cell 3B → Cell 4
    Cell 3A will CDX-query the new URL
    Cell 3B will download those snapshots
    Cell 4 will parse them and update the audit file

Step 5 — Verify improvement
    Re-run discover_faculty_urls.py
    The school's mean_recs should have increased
    If still low, try the rank 2 or rank 3 candidate
```

---

## Configuration Knobs

All at the top of the script file — easy to find and edit.

| Constant | Default | When to Change |
|----------|---------|----------------|
| `QUALITY_THRESHOLD_MEAN_RECS` | `20` | **Lower** to focus only on the very worst schools. **Raise** (e.g., to 40–50) to investigate more schools. |
| `QUALITY_MIN_AUDIT_FILES` | `3` | Ignore schools with fewer audit rows than this — too little evidence to judge quality. |
| `TOP_N_CANDIDATES` | `8` | Raise if you want more options per school (increases CDX count queries). |
| `SKIP_KNOWN_URLS` | `True` | Set `False` to see all candidates, including ones already in your list. Useful for debugging why a URL is not working. |
| `CDX_LIMIT` | `200,000` | Max unique URLs fetched per domain. Rarely needs changing. |
| `CDX_DELAY_BETWEEN_DOMAINS` | `1.5s` | Polite pause between CDX calls. Lower only if you accept more rate-limit risk. |
| `CDX_DELAY_BETWEEN_SCHOOLS` | `3.0s` | Polite pause between schools. |
| `TEST_PARSE` | `False` | Set via environment variable `TEST_PARSE=1`. Downloads and HTML-parses one Wayback snapshot per candidate. Gives verified record counts but adds time. |

---

## Timing Expectations

| Mode | Estimated Runtime |
|------|------------------|
| Default (36 schools, no test-parse) | ~15–20 minutes |
| With `TEST_PARSE=1` (8 candidates/school) | ~25–35 minutes |
| Single school (edit threshold to isolate) | ~1–3 minutes |

Most of the time is the polite CDX delays, not compute. The `matchType=domain`
query covers the entire university in one call (typically 5–15 seconds), replacing
the old approach that fired one query per known subdomain. The follow-up count
refinement queries add ~0.5s × top candidates per school.

---

## Scoring Logic Summary (for reference)

The script is not magic — it is a weighted heuristic. It will occasionally
suggest a URL that turns out to be a redirect or a sparse page. That is normal.
The right mental model is:

> **The script surfaces the 8 most-promising leads per school. You choose which ones to actually try. The pipeline then tells you if they worked.**

Rank 1 is right most of the time. When it is not, rank 2 or rank 3 usually is.
If none of the top 3 work for a school, that school may have no good faculty
listing in Wayback at all — which is a real data limitation, not a script bug.

---

*Written by PEER, 2026-04-16.*
