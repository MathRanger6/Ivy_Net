# Tenure Pipeline: End-to-End Overview
**Agent: PEER** | **Notebook: `540_tenure_pipeline.ipynb`** | **Updated: 2026-04-12 (rev 13)**

---

## 0. How this document relates to the gameplan

| Document | Role |
|----------|------|
| **`TENURE_DATA_GAMEPLAN.md`** | **Strategic contract** (same role as `../sports_documents/SPORTS_DATA_GAMEPLAN.md`): research outcomes, stage boundaries, durable artifacts, advisor alignment, fast-path checklist, open questions. |
| **`TENURE_PIPELINE_OVERVIEW.md` (this file)** | **Implementation map**: how **`540_tenure_pipeline.ipynb`** cells interact with **`tenure_pipeline/*.py`**, **`.csv`**, **`.jsonl`**, and on-disk HTML—flags, checkpoints, sentinel semantics, Option B paths, scraper playbooks. |

**Rule of thumb:** Change *intent* or *definitions* in the **gameplan** first; change *wiring* or *cell behavior* here. If you update one, check whether the other needs a cross-reference line.

### Stable anchors in `TENURE_DATA_GAMEPLAN.md`

Headings below are **Find targets** (outline / search). **§G*n*** is the order of `##` sections from top to bottom—use it when you need a stable handle in commits or PRs.

| §G | Heading (exact) | What to read it for |
|----|-----------------|---------------------|
| *(front)* | *(title + “What this file is” + lineage)* | Contract vs overview; sports parallel. |
| **G1** | Working agreement (process) | When to edit gameplan vs overview; snapshot hygiene. |
| **G2** | Target architecture: **540** as pipeline conductor | Roles of `tenure_pipeline/*.py`, notebook, human URL loop. |
| **G3** | Outcomes we want | Empirical / thesis / operational / coverage priorities. |
| **G4** | Durable team / URL equity (files on disk) | Canonical filenames (`r1_schools_data.py`, JSONL, Option B tree). |
| **G5** | Stage map (high level) | Notebook regions ↔ outputs; points here to **this** doc §2–§4. |
| **G6** | Advisor direction — 2026-04-09 conversation (Alex Gates) | Priority shift, peer groups, OpenAlex bulk, Dakota sanity check, working style. |
| **G7** | Stage 1 — DBLP parse (Cell 1) | DBLP JSONL spine. |
| **G8** | Stage 2 — R1 school list (Cell 2) | Schools CSV + URL workflow. |
| **G9** | Stage 3 — Wayback scrape (Cells 3A–3E) | CDX / download / rescues. |
| **G10** | Stage 4 — HTML parse (Cell 4) | Parsed roster JSONL, Option B + `legacy/`. |
| **G11** | Stages 6–9 — Match, enriched panel, pools, analysis (planned) | Future cells after longitudinal panel (Cell 5)—cell numbers in overview §4. |
| **G12** | Fast path — first inverted-U checkpoint (dirty OK) | Early curve + binned table checklist. |
| **G13** | Open points (negotiate next) | Peer groups, attrition vs move, coverage vs lock-in. |
| **G14** | Document history | Changelog of the gameplan itself. |

### Gameplan stage map ↔ sections *in this overview*

The gameplan **Stage map** table cites **Overview §2–§4** as follows (numbering matches headings in *this* file):

| Gameplan stage | Notebook | Primary detail here |
|----------------|----------|---------------------|
| 0 (Cell 0) | Flags, paths | **§2** Pipeline Architecture (Cell 0 / conductor). |
| 1–2 | Cells 1–2 | **§3** What Has Been Built (DBLP + schools / CSV). |
| 3A–3E | Wayback chain | **§3** (plan/download/index) and **§4** where parse boundary is discussed. |
| 4 | Cell 4 | **§3** (Cell 4 outputs) and parser notes in **§5**. |
| 5+ | Planned | **§4** What Is Planned; file inventory **§6**. |

---

## 1. Research Context

This pipeline is the **third empirical setting** in a dissertation paper testing whether upward mobility follows a nonlinear, inverted-U pattern driven by relative performance in nested talent pools. The pattern has been established in two prior settings:

- **Setting 1 (CODA):** US Army officer promotions to Major within senior-rater evaluation pools. Officers in mid-quality peer pools have the highest promotion rates; those in the very strongest pools face slot scarcity and relative rank compression that drives rates back down.
- **Setting 2 (SCOUT):** NCAA basketball players drafted into the NBA. Players on mid-quality teams are most likely to get drafted; those on elite stacked rosters face congestion and signal compression that reduces their individual draft probability.

**Setting 3 (PEER — this pipeline):** CS faculty at R1 universities receiving academic tenure. The question: do faculty in mid-prestige departments have the highest tenure rates, while those in elite departments face the same signal compression and slot scarcity seen in the Army and basketball settings?

**Core analogy across settings:**

| Dimension | Army | Basketball | Academia |
|-----------|------|-----------|---------|
| Individual performance measure | OER evaluation score | Points per minute | Publications / citations (DBLP) |
| Pool definition | Senior-rater cohort | Teammates | Department cohort |
| Peer quality measure | Leave-self-out pool mean | Teammate avg PPM | Leave-self-out dept publication rate |
| Outcome | Promoted to Major | Drafted to NBA | Tenured (Asst → Assoc Professor) |
| Slot scarcity mechanism | Literal promotion quotas | Finite draft slots | Departmental FTE / budget lines |

---

## 2. Pipeline Architecture

The entire pipeline runs from a single notebook: **`540_tenure_pipeline.ipynb`** (workspace root).

Everything is designed around three principles:

1. **Checkpoint / resume everywhere.** Each stage saves output to disk before the next stage begins. If a run is interrupted, it resumes from the last completed file — nothing is re-computed unnecessarily.
2. **Capture everything raw, filter later.** HTML files are stored as-is. All faculty titles (not just tenure-track) are recorded. Filtering to the tenure-track population happens at the analysis stage, not the collection stage.
3. **Execution flags in CELL 0.** Every heavy cell has a boolean flag (`RUN_CELL1`, `RUN_CELL2`, etc.) in CELL 0. When `False`, the cell skips computation and loads its output from disk instead, so downstream cells always have data in memory. This supports "restart and run all" without re-running expensive operations.

### Execution Flags (CELL 0)

```
RUN_CELL1          = False   # DBLP parse                    — ~30–45 min on full XML
RUN_CELL2          = True    # University list               — 168 schools (`PILOT_SCHOOLS` in `r1_schools_data.py`)
RUN_CELL3_CDX      = True    # CDX discovery (`CDX_TIMEOUT` ≈ 45s) — ~30–90+ min depending on API load
RUN_CELL3_RETRY    = True    # CDX slow retry (`CDX_RETRY_TIMEOUT` ≈ 60s) — reads `cdx_retry_queue.jsonl`; run overnight if needed
RUN_CELL3_DOWNLOAD = True    # HTML download                 — uses same inter-request delay as CDX
RUN_CELL3C         = False   # Sub-page rescue (Cornell/UMD) — complete
RUN_CELL3D         = False   # Sub-page rescue (UIUC/UW-Mad) — complete
RUN_CELL3E         = False   # Redirect rescue (NC State)    — optional; see §3 Phase E below
```

### Pipeline Stage Map

| CELL | Stage | Status | Output File(s) |
|------|-------|--------|----------------|
| CELL 0 | Imports, paths, constants, flags | ✅ Complete | — |
| CELL 1 | DBLP streaming parse | ✅ Complete | `tenure_pipeline/dblp_parsed/dblp_YYYY.jsonl` |
| CELL 2 | University list → CSV | ✅ Complete (168 schools in `PILOT_SCHOOLS`) | `tenure_pipeline/r1_cs_departments.csv` |
| CELL 3A | Wayback CDX discovery | ✅ Operational | `tenure_pipeline/faculty_snapshots_plan.jsonl` |
| *(bridge)* | Cool-down before retry (optional) | ✅ In notebook | Sleeps `CDX_SLEEP_BEFORE_RETRY_SEC` (default 30 min); hourglass display — run after 3A-VIZ, before 3A-RETRY |
| CELL 3A-RETRY | CDX slow retry (queue) | ✅ Optional pass | Appends to plan; clears `cdx_retry_queue.jsonl` as URLs resolve |
| CELL 3B | Wayback HTML download | ✅ Operational | `tenure_pipeline/faculty_snapshots/<uni>/<source_id>/<year>_<season>_<timestamp>.html` (Option B) + `faculty_snapshots_index.jsonl` |
| CELL 3C | Sub-page rescue (Cornell & UMD) | ✅ Complete | Overwrites shells + `faculty_subpage_index.jsonl` |
| CELL 3D | Sub-page rescue (UIUC & UW-Madison) | ✅ Complete | Overwrites shells + `faculty_subpage_d_index.jsonl` |
| CELL 3E | Redirect rescue (NC State) | ⏳ Optional / spotty network | Overwrites shells + `faculty_subpage_e_index.jsonl` |
| CELL 4 | Faculty page parsing | ✅ Implemented | `faculty_snapshots_parsed.jsonl` + `faculty_snapshots_strategy_audit.jsonl` |
| CELL 5 | Longitudinal panel (within-school link + Wayback plan join) | ✅ Implemented | `faculty_panel.jsonl`, `faculty_panel_collisions.jsonl` |
| CELL 6A–6B | OpenAlex: institution map, author ID resolution, works-by-year (`openalex_resolver.py`, API) | ✅ Implemented — toggle **`RUN_CELL6A` / `RUN_CELL6B`** in CELL 0 | `openalex_inst_map.json`, `openalex_author_ids.jsonl`, `openalex_works_by_year.jsonl`, `openalex_low_confidence.jsonl` |
| *(bulk)* | OpenAlex **full snapshot** at UVA (Connected Data Hub / HPC, `.csv.gz` tables) | ⏳ **Access pending** — use for large joins when provisioned; see **§4** | Same entities as API path; no per-author HTTP |
| CELL 7 | Enriched panel (pubs + events) | 📋 Planned | `faculty_panel.*` (parquet/feather TBD) |
| CELL 8 | Pool metrics (leave-self-out) | 📋 Planned | Added to panel |
| CELL 9 | Analysis (inverted-U check) | 📋 Planned | Figures + regression output |

---

## 3. What Has Been Built

### CELL 0 — Imports, Paths, Constants

CELL 0 is the control panel for the entire pipeline. It imports all libraries, sets all file paths as constants, and defines all execution flags. Key constants:

- `WORKSPACE_ROOT` — absolute path to the project root
- `DBLP_XML` — path to the 5.1 GB DBLP XML dump
- `STAGE1_OUT_DIR` — `tenure_pipeline/dblp_parsed/`
- `STAGE2_OUT` — `tenure_pipeline/r1_cs_departments.csv`
- `STAGE3_PLAN` — `tenure_pipeline/faculty_snapshots_plan.jsonl`
- `STAGE3_RETRY` — `tenure_pipeline/cdx_retry_queue.jsonl` (URLs that timed out in Cell 3A; consumed by Cell 3A-RETRY)
- `STAGE3_INDEX` — `tenure_pipeline/faculty_snapshots_index.jsonl`
- `STAGE3_HTML_DIR` — `tenure_pipeline/faculty_snapshots/`
- `CDX_YEAR_MIN / CDX_YEAR_MAX` — 2000–2024
- `CDX_SEASONS` — `{'spring': '0315', 'fall': '1015'}` (season **bands** for CDX ranking, not the analysis clock)
- `CDX_SNAPS_PER_SEASON` — **12** (max distinct Wayback captures per season **band**; primary id = `timestamp`)
- `CDX_SPACING_POOL_MULT` — **2** (when more than `CDX_SNAPS_PER_SEASON` candidates exist, pool the closest **mult × cap** to the anchor, then evenly subsample in **time** within that pool — see **CELL 3A** `_select_seasons` / `_evenly_spaced_chron_pick`)
- `CDX_SLEEP_BEFORE_RETRY_SEC` — **30 × 60** seconds default (bridge cell before **CELL 3A-RETRY**; set `0` to skip)
- `CDX_DELAY` — **2.0** seconds between requests (conservative vs. Internet Archive’s ~60/min guidance)
- `CDX_TIMEOUT` — **45** seconds per CDX request (pass 1); the Archive often needs 15–40s+ under load (20s caused false timeouts)
- `CDX_RETRY_TIMEOUT` — **60** seconds for Cell 3A-RETRY (overnight / slow pass)
- `CDX_DEFERRED_WAIT` — 90 seconds cooldown before the pass-2 deferred retry (CELL 3C)
- `CDX_DEFERRED_DELAY` — 3.0 seconds between requests in pass 2 (slower, gentler retry pace)
- `STAGE3C_TARGETS` — `tenure_pipeline/faculty_subpage_targets.json`
- `STAGE3C_INDEX` — `tenure_pipeline/faculty_subpage_index.jsonl`
- `CDX_HEADERS` — academic research User-Agent; optional contact via env `HTTP_CONTACT_EMAIL` (see CELL 0)

**Libraries loaded:** `requests`, `lxml`, `tqdm`, `pandas`, `numpy`, `json`, `time`, `datetime`, `pathlib`, and the custom `functionsG_working.py` utilities (`time_start`, `time_stop`, `hms_string`, `tymeout`, `tyme`).

---

### CELL 1 — DBLP Streaming Parse

**What it does:** Streams the full DBLP XML dump (5.1 GB) using `lxml.etree.iterparse`, extracting `article` and `inproceedings` records. Writes one JSONL file per year into `tenure_pipeline/dblp_parsed/`.

**Why streaming (iterparse)?** The full DBLP XML cannot fit in memory at once. `iterparse` processes one XML element at a time and frees memory immediately — never loading the whole tree.

**Status:** Complete. The parser has been run across all years (the final run covered 1900–2028, capturing 8.1 million records). The target analysis window is 2010–2020, but having all years gives flexibility to extend.

**Output schema (one JSON record per line):**

```json
{
  "type": "inproceedings",
  "key": "conf/nips/LeCunBH89",
  "year": "2015",
  "authors": ["Jane Smith", "John Doe"],
  "venue": "NeurIPS",
  "title": "Deep Learning for Structured Prediction"
}
```

**Key files on disk:**

| File | Size | Records (approx.) |
|------|------|-------------------|
| `dblp_2010.jsonl` | 54 MB | ~235,000 |
| `dblp_2015.jsonl` | 74 MB | ~292,000 |
| `dblp_2020.jsonl` | 113 MB | ~490,000 |

**Timing log:** `tenure_pipeline/dblp_parsed/parse_timing.json` records the parse rate (records/sec, bytes/rec) from each run. Future runs use this to seed the ETA display in the tqdm bar.

**Smart features:**
- Per-year JSONL files (not one monolithic file) — easy to inspect, reparse, or extend individual years
- Skip already-parsed years (checkpoint/resume) unless overwrite is specified
- Overwrite can target specific years: `overwrite=[2015, 2016]`
- ETA updated every 5 seconds in the tqdm bar, blending historical rate (30%) with live rate (70%)

---

### CELL 2 — University List → CSV

**What it does:** Defines R1 CS departments as a hardcoded Python list and writes `tenure_pipeline/r1_cs_departments.csv`. Fast (~0.1 seconds). The list has grown in three waves:

| Wave | Schools | Notes |
|------|---------|-------|
| Original 9 | Cornell, UIUC, Indiana, UT Austin, UW-Madison, Purdue, Georgia Tech, UMD, Brown | Initial pilot; scrapability-first selection |
| Wave 2 (+25) | CMU, MIT, UCSD, Columbia, Duke, UMass, UNC, Rice, Rutgers, Ohio State, Penn State, Virginia Tech, NC State, Florida, Stony Brook, Pittsburgh, Arizona, UCLA, Utah, Colorado, Rochester, Dartmouth, JHU, Minnesota, Michigan State | Added April 4, 2026 |
| Wave 3 (+80) | Stanford, Berkeley, UW, UVA, Michigan, Harvard, Northwestern, NYU, Yale, Penn, Chicago, UCSB, UCI, UC Davis, USC, Oregon, Oregon State, WSU, UNLV, UNR, Colorado State, Iowa State, Iowa, Nebraska, Kansas State, Kansas, Missouri, Kentucky, Wayne State, Notre Dame, Texas A&M, Houston, UTD, UTA, Texas Tech, Oklahoma, OSU, LSU, Tennessee, Vanderbilt, Clemson, Alabama, Auburn, Mississippi State, South Carolina, UCF, FSU, USF, Tulane, WVU, Drexel, Temple, Lehigh, GMU, ODU, W&M, GWU, UMBC, Delaware, UConn, Tufts, BU, Case Western, Syracuse, RPI, SUNY Buffalo, Binghamton, WPI, Vermont, Emory, Wyoming, Montana State, Idaho, NMSU, Hawaii, North Texas, UTSA, Arkansas, UC Riverside, UC Santa Cruz | Added April 5, 2026 |
| Later waves (2026) | Additional R1 CS departments | Brings **`PILOT_SCHOOLS` to 168** entries (see `r1_schools_data.py` for the authoritative list) |
| **Total (April 2026)** | **168** | A few institutions may still be blocked or empty in Wayback; sentinels + URL worksheet track fixes |

**`alt_urls` field:** Each school includes a JSON list of historical/alternate URLs so the CDX scraper queries all of them and unions the results. This is critical for schools with domain changes over time (UIUC: `cs.uiuc.edu` → `cs.illinois.edu`; Georgia Tech: `cc.gatech.edu` → `scs.gatech.edu`; UW-Madison corrected from `/people/pb` bug).

**Key lesson from CDX runs:** Many schools' best Wayback coverage is via their **base domain** (`cs.colostate.edu/`) rather than a specific faculty path (`cs.colostate.edu/people/faculty/`). Northwestern (133 snaps via `cs.northwestern.edu/`), Iowa State (289 snaps via `cs.iastate.edu/`), and Colorado State (68 snaps via `cs.colostate.edu/`) all show this pattern. The CDX union-all-URLs strategy naturally captures this.

**CSV schema:**

| Column | Description |
|--------|-------------|
| `university` | Full institution name |
| `dept_name` | Actual department name (may vary from "Computer Science") |
| `cs_dept_url` | Current primary faculty page URL |
| `alt_urls` | JSON list of historical/alternate URLs for CDX querying |
| `notes` | Flags: URL quirks, domain changes, page structure issues |
| `pilot` | `True` for all rows |

---

### CELL 3 — Wayback Machine CDX Scrape

This is a two-phase cell, each phase controlled by its own flag.

#### Phase A: CDX Discovery (CELL 3A — `RUN_CELL3_CDX`)

**What it does:** Queries the Internet Archive CDX API for every school URL (primary + all `alt_urls` from **`r1_cs_departments.csv`**) to find archived snapshots between 2000–2024. For each calendar year and each **season band** (targets near March 15 and October 15), it selects **up to `CDX_SNAPS_PER_SEASON` (default 12) distinct captures**. Candidates are deduplicated by `timestamp`, ranked by distance to the band anchor; if more than the cap remain, the closest **`CDX_SPACING_POOL_MULT` × cap** are pooled, sorted chronologically, then **evenly subsampled in time** (`_evenly_spaced_chron_pick`). **Primary identity is the Wayback `timestamp`;** `year`/`season` are labels for the band. Writes one plan row per selected capture to `faculty_snapshots_plan.jsonl`. On-disk filenames are **`{year}_{season}_{timestamp}.html`** under `<uni_slug>/<source_id>/` (see gameplan *Snapshot identity*).

**The CDX API:** `http://web.archive.org/cdx/search/cdx` — a programmatic interface to the Internet Archive's snapshot index. Returns a list of timestamps and URLs for any given web address, without downloading the HTML. Very fast.

**Key design decision — union all URLs:** Rather than picking the single URL with the most snapshots, CELL 3A queries *all* URLs for a school and unions the results. This is critical for schools like UIUC where `cs.uiuc.edu` has good coverage before 2009 and `cs.illinois.edu` has good coverage after 2009. Snapshots are deduplicated by timestamp before season selection.

**Season band selection (multi-capture):** For each year, targets are `20XX0315000000` (spring) and `20XX1015000000` (fall). Implementation: `_select_seasons(..., max_per_season, spacing_pool_mult)` in **`# === CELL 3A`**. Legacy notebooks used **one** capture per band; the default is now **multiple dated observations** per band when CDX provides them.

**Checkpointing and `tried_urls`:** CELL 3A reads the existing **`faculty_snapshots_plan.jsonl`** (if present) and builds a set **`tried_urls`** from every `source_url`, `tried_primary_url`, and entry in `tried_urls` on prior rows. **Only URLs not in that set are queried.** If the plan file is **missing** (clean slate), every URL in the CSV is untried. Schools still appear in the work queue whenever they have **at least one untried** URL; schools are not skipped wholesale solely because another URL from the same school was already tried.

**URL normalization:** `tried_urls` treats trailing slashes consistently so CDX canonical URLs do not cause duplicate queries. After a successful CDX query, Cell 3A can append a **bookmark** row (`n_snaps: -1`, `queried_at`, exact `source_url`) so the **exact URL string** you queried is remembered even when CDX returns a canonical form — preventing infinite re-queries.

**Timeouts, 429, and retry queue:** CDX requests use `CDX_TIMEOUT` (typically **45s** in CELL 0). A **429** response prints a warning, **`time.sleep(60)`**, then **one** retry of the same request (not the same as a connect/read **timeout**). If a request **times out** or fails to return usable CDX data, the URL may be appended to **`cdx_retry_queue.jsonl`**. Run **CELL 3A-RETRY** with `RUN_CELL3_RETRY = True` to re-query those URLs with `CDX_RETRY_TIMEOUT` (typically **60s**). Optional **bridge cell** (after 3A-VIZ): sleeps **`CDX_SLEEP_BEFORE_RETRY_SEC`** before you run the retry pass.

**Progress counter:** The progress print shows the school’s position in the full roster (e.g. `k/168`) and progress within the current scrape batch.

**CDX API reliability notes:** The CDX API is unreliable. Typical failures:
- `Read timed out` — Archive slow under load; URL goes to the retry queue (or gets 0 snaps and is retried next run).
- `503` / transient server errors — retry later; not a bug in the pipeline.
- `NameResolutionError` — network/DNS dropout; re-run after connectivity returns.

**Coverage:** Per-school coverage varies (full 2000–2024 for some sites, sparse or zero for others). **Gaps in coverage are real** — the Internet Archive may not have crawled a given path in a given era. Use `faculty_snapshots_plan.jsonl` and optional `pipeline_health_audit.csv` for current counts.

Gaps in coverage are a data limitation, not necessarily a bug.

**Plan JSONL schema (one record per planned download):**

```json
{
  "university": "Princeton University",
  "uni_slug": "princeton_university",
  "year": 2015,
  "season": "fall",
  "timestamp": "20151018143022",
  "source_url": "http://www.cs.princeton.edu/people",
  "wayback_url": "https://web.archive.org/web/20151018143022/http://www.cs.princeton.edu/people",
  "local_path": "tenure_pipeline/faculty_snapshots/princeton_university/a1b2c3d4/2015_fall_20151018143022.html",
  "total_snaps_union": 34
}
```

The `local_path` **middle folder** (`a1b2c3d4` in the example) is the **Option B** `source_id` — see below.

#### Phase B: HTML Download (CELL 3B — `RUN_CELL3_DOWNLOAD`)

**What it does:** Downloads each planned HTML snapshot from the Wayback Machine and saves it to disk. Appends one record to `faculty_snapshots_index.jsonl` after each file attempt (success or failure), flushed immediately to disk.

**Rate limiting:** `CDX_DELAY` (2.0s) between every request, matching a conservative reading of the Internet Archive’s ~60 requests/minute guidance. A 429 "Too Many Requests" response triggers a 60-second backoff before retrying.

**Checkpoint / resume:** On any future run, CELL 3B reads the index, identifies which files are already on disk and logged with a 200 status, and skips them. Only missing or failed files are re-attempted. Safe to interrupt at any time.

##### Option B — per–faculty-page URL paths (read this before Cell 4)

New work (and rebuilt plans) store HTML under **one folder per normalized faculty-list URL**, not as a single flat pile per school. That way the same `uni_slug` can hold snapshots from **multiple CDX `source_url`s** (e.g. domain change, or base path vs. `/people/faculty`) without filename collisions.

| Piece | Meaning |
|--------|--------|
| **`faculty_snapshots/<uni_slug>/`** | One directory per institution (same slug as `r1_schools_data` / plan). |
| **`<source_id>/`** | **8-character hex** id = first 8 chars of **SHA-256** of the **normalized** faculty URL string. Implemented as `faculty_source_id(source_url)` in `tenure_pipeline/apply_url_updates.py` (normalization matches the worksheet / plan so paths stay stable). |
| **`YYYY_season_<timestamp>.html`** | Current snapshot file name (Wayback timestamp disambiguates multiple captures per band). |
| **`YYYY_season.html`** | Legacy two-part name (no timestamp); may still appear under `legacy/` or old runs. |

**Full pattern (current):**

```text
tenure_pipeline/faculty_snapshots/<uni_slug>/<source_id>/<year>_<season>_<timestamp>.html
```

**Legacy flat files:** Older runs may have had `YYYY_season.html` **directly** under `<uni_slug>/`. Those can be moved into `faculty_snapshots/<uni_slug>/legacy/` (see `legacy_flat_snapshots.py`). **Cell 4 does not care which subfolder:** it uses the same rule as 3B — **`rglob('*.html')` under each school directory** (`iter_school_html_files()` in `apply_url_updates.py`). So `legacy/`, `<source_id>/`, and any rare top-level `*.html` are all scanned. **`sniff_wayback_timestamp_from_html_file()`** in `html_parser.py` can recover a capture time from embedded Wayback URLs when the filename stem lacks a timestamp.

**What you need for Cell 4:** Nothing special — point Cell 4 at `STAGE3_HTML_DIR` as usual. Parsed records carry through whatever path was in the plan/index. If you inspect disk, expect **mostly** `…/<uni_slug>/<8 hex>/…html` for new downloads.

**Directory structure (illustrative):**

```
tenure_pipeline/
  faculty_snapshots/
    princeton_university/
      a1b2c3d4/                    ← source_id for one normalized faculty URL
        2008_fall_20080915120000.html
        2009_spring_20090310103000.html
        ...
      e5f67890/                    ← another source_url (e.g. alternate domain)
        2010_fall_20101012141522.html
        ...
      legacy/                      ← optional: flat files moved here
        2000_spring.html
    brown_university/
      ...
  faculty_snapshots_plan.jsonl     ← download plan (from CELL 3A)
  faculty_snapshots_index.jsonl    ← download log (from CELL 3B)
```

**Index JSONL schema (one record per attempted download):**

```json
{
  "university": "Brown University",
  "uni_slug": "brown_university",
  "year": 2012,
  "season": "spring",
  "timestamp": "20120314091234",
  "source_url": "http://www.cs.brown.edu/people/faculty/",
  "wayback_url": "https://web.archive.org/web/20120314091234/...",
  "local_path": "tenure_pipeline/faculty_snapshots/brown_university/f3e4d2c1/2012_spring_20120314091234.html",
  "http_status": 200,
  "file_size_bytes": 48293,
  "error": "",
  "downloaded_at": "2026-04-04T22:35:17.123456"
}
```

**Expected download stats:** Depends on plan size; large plans can take tens of minutes at 2s between requests. File sizes typically range from a few KB (redirect shells) to hundreds of KB for full faculty listings.

---

#### Phase C: Sub-Page Rescue (CELL 3C — `RUN_CELL3C`)

**Background — the JS hub page problem:** After CELL 3B completed, inspection of the downloaded HTML revealed that Cornell and UMD's faculty pages were both JavaScript-rendered shells. The Wayback Machine captured the HTML skeleton (nav bar, headers, empty containers) but never executed the JavaScript that loads the actual faculty list. Every one of the 54 Cornell and UMD files was effectively empty.

**The discovery:** Rather than swapping out those schools, PEER parsed the nav bar links embedded in the empty HTML shells themselves. Every archived hub page contained direct Wayback links (with exact timestamps) to faculty sub-pages that were *not* JS-rendered:

| School | Era | Sub-page URL pattern | Type |
|--------|-----|----------------------|------|
| Cornell | 2005–2012 | `/People/faculty/index.htm` | Classic static `.htm` file |
| Cornell | 2013–2024 | `/people/faculty` | Static sub-page (different render path from the hub) |
| UMD | 2013–2024 | `/people/phonebook/faculty` | **Dept. Phonebook** — plain HTML table: name, title, location, phone, email |

Test downloads confirmed all pages were rich with data (67–128 professor mentions, 64–316 KB per file). No CDX queries were needed — the exact Wayback timestamps were already embedded in the nav bars we already had.

**Generalization (important for future schools):** This is a broadly reusable pattern. Many university CMS platforms render a JS hub page at `/people` but serve the actual faculty roster from a static sub-page. When a downloaded file is empty, the first diagnostic step should be: **parse the nav bar of the empty file and look for a faculty sub-page link.** Common patterns to look for across schools:

- `/people/faculty` — direct faculty sub-page (may be static even if hub is JS)
- `/people/phonebook` or `/people/phonebook/faculty` — **Dept. Phonebook pages are gold mines**: they are always simple HTML tables with name, title, location, phone, email, and homepage. Easy to parse, consistent across years, wide Wayback coverage.
- `/faculty/index.htm` or `/Faculty/index.html` — classic static-era naming (pre-2013)
- `/directory/` — some schools use a staff directory page
- `/people?type=faculty` or `/people?role=faculty` — query-parameterized static sub-pages

**CELL 3C implementation:** Rather than updating the CDX plan or re-running CELL 3A, CELL 3C operates from a separate target file (`faculty_subpage_targets.json`) that was built by extracting the sub-page links directly from the nav bars of our existing HTML files. It overwrites the empty Cornell and UMD files with the actual faculty data and logs results to `faculty_subpage_index.jsonl`.

**Two-pass deferred-pile strategy:** CELL 3C uses a two-pass download approach designed for network unreliability:
- **Pass 1:** Attempts all pending URLs at normal Wayback request pace (sub-page cells use the same delay constants as the main CDX/download path unless noted). Connection errors are held silently in a deferred pile (nothing written to the index yet). HTTP 404s are written as `http_404` (write-off, never retried). Other HTTP errors written as `http_error` (retried next run).
- **Cooldown:** If any deferred entries exist, a 90-second countdown (`CDX_DEFERRED_WAIT`) allows Wayback's connection pool to recover before retrying.
- **Pass 2:** Retries the deferred pile at a slower 3s pace (`CDX_DEFERRED_DELAY`). Successes are written as `ok`. Persistent failures are written as `connection_error` — included in pending on every future run until they succeed.
- **Self-healing checkpoint:** Only `ok` entries are considered done. Any other status (including from interrupted prior runs) is retried automatically.

**Final result:** All 54 sub-pages downloaded successfully. Cornell and UMD are fully rescued.

**Sub-page target file schema:**

```json
{
  "uni_slug": "university_of_maryland",
  "year": 2018,
  "season": "fall",
  "sub_page_url": "https://web.archive.org/web/20181015234940/http://www.cs.umd.edu/people/phonebook/faculty",
  "parent_file": "faculty_snapshots/university_of_maryland/2018_fall.html"
}
```

**Sub-page index schema (one record per download attempt):**

```json
{
  "uni_slug": "cornell_university",
  "year": 2013,
  "season": "fall",
  "sub_page_url": "https://web.archive.org/web/20131003135741/http://www.cs.cornell.edu/people/faculty",
  "status": 200,
  "nbytes": 80247,
  "subpage_status": "ok",
  "pass_num": 1
}
```

---

#### Phase D: Sub-Page Rescue — UIUC & UW–Madison (CELL 3D — `RUN_CELL3D`)

**The problem:** UIUC and UW–Madison's primary faculty pages were JS-rendered hubs — the Wayback captures contain HTML shells with empty faculty containers. This is the same pattern as Cornell and UMD, requiring sub-page extraction.

**The solution:** Same nav-bar parsing approach as CELL 3C. CELL 3D operates from a separate target file (`faculty_subpage_d_targets.json`) and logs to `faculty_subpage_d_index.jsonl`. It uses the identical two-pass deferred-pile download strategy.

**Status:** ✅ Complete. Both schools rescued.

**Output files:**
- `tenure_pipeline/faculty_subpage_d_targets.json` — sub-page URLs extracted from nav bars
- `tenure_pipeline/faculty_subpage_d_index.jsonl` — download log

---

#### Phase E: Redirect Rescue — NC State (CELL 3E — `RUN_CELL3E`)

**The problem:** NC State's primary CDX URL (`www.csc.ncsu.edu/faculty/`) pointed to a page that, even in 2007, issued a `<meta http-equiv="refresh">` redirect to `/directories/faculty.php`. The Wayback Machine faithfully captured the redirect shell — a ~2.1 KB page with zero faculty content — not the target. All 16 downloaded NC State files are identical shells.

**Why this is different from 3C/3D:** The nav bar approach doesn't apply here — these files aren't JS shells, they're redirect shells. The actual target URL is already embedded directly in the `content` attribute of the `<meta refresh>` tag:

```html
<meta http-equiv="refresh" content="0;url=https://web.archive.org/web/20070919194824/http://www.csc.ncsu.edu/directories/faculty.php">
```

**The solution (simpler):** No CDX query needed. CELL 3E reads each NC State HTML file, extracts the redirect target URL via regex (`_E_REFRESH_RE`), and downloads the actual `/directories/faculty.php` page for that exact Wayback timestamp — overwriting the shell with real content.

**CELL 3E implementation:**
- `build_e_targets()` — scans all 16 NC State HTML files, extracts embedded Wayback URLs via regex, returns list of `{year, season, wayback_url, local_path}` dicts
- `download_e_subpages()` — two-pass deferred download (same pattern as 3C/3D), overwrites the original shell files in-place, logs to `faculty_subpage_e_index.jsonl`

**Status:** An early run (April 2026) failed to download redirect targets under spotty network conditions. **Re-run CELL 3E** after NC State HTML exists on disk and connectivity is stable; success is not guaranteed if Wayback lacks the target at the embedded timestamps. Dissertation-facing limitation notes: **`Pertinent_Thoughts_Tenure.md`** (NC State).

**Output files:**
- `tenure_pipeline/faculty_subpage_e_index.jsonl` — download log

---

## 4. What Is Planned (Stages 6–9) — Through Cell 5 Implemented

### CELL 4 — Faculty Page Parsing (implemented)

**Goal:** For every downloaded HTML file under `faculty_snapshots/<uni_slug>/` (recursive: **Option B** `<source_id>/`, `legacy/`, etc.), parse faculty names and ranks using the shared multi-strategy parser in `html_parser.py`, and append structured records to **`tenure_pipeline/faculty_snapshots_parsed.jsonl`**. Strategy metadata (which heuristic won per file) goes to **`faculty_snapshots_strategy_audit.jsonl`**.

**Design:** One dispatcher tries multiple strategies (Drupal views, tables, cards, profile links, generic fallback) and keeps the best result per snapshot. This replaces the older “one parser per pilot school” idea. **You do not need a separate Cell 4 pass per `source_id` folder** — discovery is `rglob('*.html')` per school, same as `iter_school_html_files()` in `apply_url_updates.py`.

**Checkpointing:** Cell 4 skips schools already represented in the parsed JSONL (or blocked by plan sentinels). A per-school line **`→ 0 files`** in the log often means **already parsed**, not a failed parser.

**Auto-condemnation (optional, off by default):** **`CELL4_CONDEMN_ON_FAILURE = False`** in CELL 4 means failed parses **do not** append condemn sentinels or delete HTML. When set **`True`**, a catastrophic parse could append a plan sentinel (`n_snaps: -1`, `reason` starting with `Cell 4 auto-condemned:`) and remove bad HTML — use only with care. Preferred direction: **flag for manual inspection** before any URL/school lands on a permanent “condemn” list (gameplan).

**Capture everything raw:** All title strings on the page are recorded; filtering to tenure-track populations happens downstream in analysis.

**Output:** Use `faculty_snapshots_parsed.jsonl` as the master parsed faculty table (not `faculty_records.jsonl`).

---

### CELL 5 — Longitudinal faculty panel (implemented)

**Notebook:** `540_tenure_pipeline.ipynb` CELL 5. **Code:** `tenure_pipeline/faculty_linker.py`.

**Goal:** One row per `(uni_slug, faculty_id, year, season)` within each school, linking **normalized name keys** across Wayback snapshots; attach **exact Wayback metadata** from `faculty_snapshots_plan.jsonl` for the analysis clock (`snpsht_dt`, `wayback_timestamp`, `wayback_url`, `source_url`, `source_id`). Each row includes **`local_path`** to the HTML file used.

**Plan join:** Match on `(uni_slug, year, season, local_path)` after path normalization; if that fails (e.g. legacy flat `.../2007_fall.html` vs Option B `.../<source_id>/2007_fall.html`), fall back to **`YYYY_season.html`** basename when it is **unique** in the plan for that school and season (`plan_join`: `ok` | `ok_basename` | `missing`). See **§5** (*Temporal keys*, *Collisions*).

**Outputs:** `faculty_panel.jsonl`, `faculty_panel_collisions.jsonl` (name-key collision QA).

---

### CELL 6A–6B — Entity resolution: OpenAlex (implemented) + bulk snapshot (pending)

**Primary path (in code):** `tenure_pipeline/openalex_resolver.py`, invoked from **`540`** CELL **6A** (institution + author IDs) and **6B** (publication counts by year via OpenAlex `group_by`). Polite API use with `mailto` and optional API key; outputs under `tenure_pipeline/openalex_*.json` / `*.jsonl` (see CELL 0 constants: `STAGE6_*`).

**Stage 6 pilot ordering (`stage6_pilot.py`, CELL 0):** Optional **coverage-first** run: schools are ranked by **unique panel faculty** (then row count); **`STAGE6_PILOT_TOP_N`** keeps only the top *N* schools for 6A–6B. **`STAGE6_PILOT_MODE = False`** restores alphabetical order and the full panel.

- **`STAGE6_SANITY_MAX_NONE_FRAC`** — Upper bound on **bad parse files** for a school, as measured in **`faculty_snapshots_strategy_audit.jsonl`**: for each audit row, `winner == 'none'` means the HTML parser picked no winning strategy for that file. For school *S*, **`frac_none`** = (number of audit rows with `winner == 'none'`) / (rows for *S*). If **`frac_none`** is **greater than** this threshold **and** the school has enough audit rows (see next bullet), that school is **excluded** from Stage 6 so you do not burn OpenAlex quota on pages that mostly failed to parse. Example: `0.35` drops schools where more than **35%** of audited files are `none`.

- **`STAGE6_SANITY_MIN_AUDIT_ROWS`** — Minimum number of **audit rows** (parsed HTML files recorded in the strategy audit) for a school **before** the none-fraction rule applies. If a school has **fewer** than this many rows (e.g. only one or two snapshots), the rule is **skipped** for that school: we do not exclude it for being “too none-heavy” on thin evidence. Example: `3` means we need at least three audited files to judge `frac_none` against **`STAGE6_SANITY_MAX_NONE_FRAC`**.

**Confidence tiers (6A):** HIGH / MEDIUM / LOW / MULTI / NONE — `openalex_low_confidence.jsonl` holds rows needing human review. **Advisor constraint:** do **not** hand-merge OpenAlex IDs for a subset unless the same rule could apply everywhere (bias).

**DBLP:** Per-year JSONL in `dblp_parsed/` remains the **bibliographic spine** for name/year matching experiments and cross-checks; full string-matching pipeline for “CELL 6 ↔ DBLP only” is **not** the main track if OpenAlex coverage is sufficient.

**Bulk OpenAlex at UVA (preferred at scale — access pending):** The university hosts a **full OpenAlex** table snapshot (e.g. under **UVA On Demand → Files → project → Connected Data Hub** / HPC; **`.csv.gz`** shards for authors, works, and author–work–affiliation links). **Status:** path and permissions **not yet available** to this project — request through advisor. When available, join panel author IDs to bulk tables instead of (or as a supplement to) per-author API calls. **Source transcript:** `2-Way_Ahead/20260410_Paper_directions_4_otter_ai.pdf` (Apr 2026).

---

### CELL 7 — Panel Build (enriched)

**Goal:** Construct the analysis-ready panel: one row per `(person × year)` (or finer), combining **CELL 5** roster observations with DBLP publication counts and derived events.

**Panel grain:** `(uni_slug, name_clean, year)` — one row per person per year they appear in any faculty snapshot.

**Key columns:**

| Column | Source | Description |
|--------|--------|-------------|
| `university` | CELL 4 | Institution |
| `dept_rank` | CELL 4 parsed | `assistant` / `associate` / `full` / `other` |
| `year` | CELL 4 | Academic year of observation |
| `tenure_event` | Derived | 1 if promoted Asst → Assoc in this year, 0 otherwise |
| `attrition` | Derived | 1 if person disappears from page without promotion |
| `pubs_year` | CELL 1 DBLP | Publications in this calendar year |
| `pubs_cumulative` | CELL 1 DBLP | Cumulative publications through this year |
| `h_index_est` | CELL 1 DBLP | Estimated h-index through this year |
| `years_on_track` | Derived | Years observed as Assistant Professor |

**Attrition detection:** A person who appears as Assistant Professor in year T and does not appear in the faculty snapshot in year T+1 (or T+2 to allow for snapshot gaps) is flagged as a probable attrition case. This population — denied tenure, departed before the clock, or laterally moved — is essential for the research design. Studying only the survivors would bias every estimate.

---

### CELL 8 — Pool Metrics (Leave-Self-Out Peer Quality)

**Goal:** For each `(university, year)` combination, compute the leave-self-out (LOO) peer quality measure — the central independent variable in the analysis.

**The LOO measure:** For person *i* in department *d* in year *t*, peer quality is the mean publication rate of all other faculty in the same department-year, excluding person *i*:

```
poolq_loo(i, d, t) = mean( pubs_year(j, t) for j in dept(d,t) if j ≠ i )
```

This mirrors the Army setting (where each officer's pool mean excluded their own OER score) and the basketball setting (where each player's teammate quality excluded themselves).

**Why leave-self-out?** Including person *i* in their own peer quality measure creates mechanical correlation between the independent variable and the outcome. The LOO approach breaks this endogeneity.

**Additional pool metrics to compute:**
- `pool_size` — number of tenure-track faculty in the department-year
- `pool_sd` — standard deviation of publication rates (measures pool dispersion)
- `pool_rank_loo` — person *i*'s rank within their pool (relative standing)

---

### CELL 9 — Analysis: Inverted-U Check

**Goal:** Test whether the inverted-U pattern from the Army and basketball settings also appears in academic tenure.

**Primary analysis:** Bin departments by their LOO peer quality measure (ventiles or deciles, as in the basketball analysis). For each bin, compute the tenure rate (probability that an Assistant Professor is promoted to Associate within 7 years). Plot tenure rate vs bin index.

**The prediction:** If the pattern holds, the curve should rise from low-quality pools, peak somewhere in the middle of the quality distribution, and fall back at the highest quality pools — mirroring the Army and basketball figures.

**Secondary analyses:**
- Linear Probability Model (LPM): `tenure_event ~ poolq_loo + poolq_loo² + pubs_cumulative + years_on_track + dept FE`
- Survival analysis (time-to-tenure): Cox proportional hazards model
- Heterogeneity: Does the inverted-U differ by subfield (systems vs theory vs ML)?

---

## 5. Key Design Decisions (Reference)

These decisions were made in conversation and are recorded here as reference.

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Year range (DBLP) | 2010–2020 (pilot); all years parsed | Proof of concept first; data already available for expansion |
| Year range (Wayback) | 2000–2024 | Wider window captures pre-tenure history; costs almost nothing extra at pilot scale |
| CDX captures per season band | Up to **12** distinct timestamps (`CDX_SNAPS_PER_SEASON`); **temporal spacing** when many candidates (`CDX_SPACING_POOL_MULT`) | Retain dated observations; consolidate later—see gameplan *Snapshot identity* |
| HTML storage | Raw files on disk | "Capture everything" — re-parsing is free, re-downloading is expensive |
| Snapshot paths (3B / disk) | **Option B:** `faculty_snapshots/<uni_slug>/<source_id>/<year>_<season>_<timestamp>.html` | `source_id` = first 8 hex of SHA-256(normalized `source_url`); timestamp in filename keeps multi-capture per band unique; `legacy/` may hold older two-part names until rebuilt |
| Faculty title filtering | Capture all, filter at analysis | Maximum flexibility; no decisions made on ingestion |
| DBLP format | Per-year JSONL | Visual inspection, easy spot-checks, checkpoint-resume |
| In-scope departments | 168 in `PILOT_SCHOOLS` (April 2026) | Expanded from the original pilot; see `r1_schools_data.py` |
| URL strategy | Union all URLs per school | Handles domain changes over time (UIUC, Georgia Tech, UVA, Purdue) |
| Rate limiting | 2.0 sec between requests | Conservative vs. Internet Archive’s ~60 req/min guidance |
| Contact in User-Agent | `HTTP_CONTACT_EMAIL` in `.env` (optional) | Standard academic crawler courtesy |
| Analysis time axis | **Exact Wayback `timestamp`** (derive `snpsht_dt`); `year`/`season` = CDX culling strata | See **Temporal keys** below |
| Duplicate / ambiguous names | **Multiplicity + conflict flags** when needed; `faculty_linker` = default baseline, not only story | See **Collisions** below |

### Temporal keys: CDX season labels vs exact Wayback timestamps

**Spring/fall (`year` + `season`)** are the **sampling design** for Cell 3A: they define **bands** (anchors near mid-March and mid-October) used to rank and subsample captures for each calendar year — **up to `CDX_SNAPS_PER_SEASON`** per band with spacing when CDX is dense. They are useful for **stratifying** the scrape and for human-readable checkpoints.

**Exact Wayback timestamps** (from CDX / `faculty_snapshots_plan.jsonl`, echoed on index rows and joinable to parsed rows) are the **primary analysis clock** when building longitudinal panels:

- **`merge_asof`**, ordering within a career, and distinguishing multiple captures that fall under the same nominal “season” all require the **real** crawl time, not a synthetic mid-season date.
- Derive a datetime column (e.g. **`snpsht_dt`**) from the Archive **`timestamp`** string; keep **`year` / `season`** as **design strata** (how the HTML was culled), not as a substitute for true observation time.

**Rule:** Cull with spring/fall; analyze and join on **exact timestamps** (and keep **`wayback_url`** for audit).

### Collisions, co-occurring snapshots, and contradictions

**Name / identity collisions** (same normalized key, ambiguous `name` strings, or multiple plausible people) should not always be resolved by a single rule (“keep highest rank” or “first wins”). Acceptable strategies:

- **Retain multiplicity** — keep all co-occurring rows for the same school/name-key/time window when needed; **blend** downstream (e.g. majority vote on rank, union of titles) or aggregate explicitly.
- **Flag for later** — when two snapshots or two parsed rows **contradict** on rank/title for what should be one observation window, store both and set a **`conflict` / `needs_review`** flag rather than silently overwriting; **re-parse or disambiguate** in a separate QA pass (including ORCID/global-ID linkage when available).
- **`faculty_linker.py`** still provides a **default** deduplication path for a clean panel; treat its output as one **baseline**, not the only defensible longitudinal representation when collisions are informative.

This matches the broader rule: **capture wide, resolve narrow** — metadata and multiplicity are cheaper than re-scraping history.

---

## 6. Files on Disk (Current State — April 2026)

```
540_tenure_pipeline.ipynb              ← pipeline conductor notebook (workspace root)

tenure_pipeline/
  dblp_parsed/
    dblp_1936.jsonl ... dblp_2026.jsonl   ← parsed DBLP records by year (8.1M records)
    parse_timing.json                      ← parse rate log for future ETA estimation
  r1_cs_departments.csv                    ← 168 R1 CS departments with URLs and alt_urls
  cdx_retry_queue.jsonl                    ← URLs to re-try with Cell 3A-RETRY after timeouts
  faculty_snapshots_plan.jsonl             ← CDX plan + sentinels (CELL 3A / 3A-RETRY / 3B / 4)
  faculty_snapshots_index.jsonl            ← download log (from CELL 3B)
  faculty_snapshots_parsed.jsonl           ← parsed faculty records (CELL 4)
  faculty_snapshots_strategy_audit.jsonl   ← parser strategy metadata (CELL 4)
  faculty_panel.jsonl                      ← longitudinal panel + Wayback timestamps (CELL 5)
  faculty_panel_collisions.jsonl             ← name-key collision QA (CELL 5)
  school_enrollment_annual.csv             ← IPEDS fall headcount by school/year (rebuild: `541` / `build_school_enrollment_from_ipeds.py`)
  ipeds_unitid_crosswalk.json              ← name → UNITID (IPEDS builder)
  ipeds_download_errors.jsonl              ← IPEDS HTTP/cache outcomes (see §7.5)
  openalex_inst_map.json                   ← CELL 6A: slug → OpenAlex institution (when run)
  openalex_author_ids.jsonl                ← CELL 6A: faculty → author ID + confidence
  openalex_works_by_year.jsonl             ← CELL 6B: publication counts by year (when run)
  openalex_low_confidence.jsonl           ← 6A: MULTI / LOW / NONE for review
  viz_pipeline.py                          ← Stage 3–5 plots (`stage3a_summary.png`, `stage3a_enrollment_bin_heatmap.png`, …)
  faculty_subpage_targets.json             ← 54 sub-page URLs for Cornell & UMD (CELL 3C input)
  faculty_subpage_index.jsonl              ← Cornell & UMD sub-page download log (CELL 3C)
  faculty_subpage_d_targets.json           ← sub-page URLs for UIUC & UW-Madison (CELL 3D input)
  faculty_subpage_d_index.jsonl            ← UIUC & UW-Madison sub-page download log (CELL 3D)
  faculty_subpage_e_index.jsonl            ← NC State redirect rescue log (CELL 3E)
  faculty_snapshots/
    brown_university/                     ← contains <source_id>/ subdirs (Option B); may include legacy/
    cornell_university/                    ← rescued: static .htm (2005–2012) + /people/faculty (2013–2024)
    georgia_institute_of_technology/
    purdue_university/
    university_of_maryland/               ← rescued: /people/phonebook/faculty (2013–2024)
    university_of_texas_at_austin/
    university_of_virginia/
    university_of_washington/
    university_of_wisconsin_madison/      ← rescued: JS shell → static sub-page (CELL 3D)
    uiuc/                                 ← rescued: cs.uiuc.edu (pre-2009) + cs.illinois.edu (post)
    north_carolina_state_university/      ← redirect shells unless CELL 3E rescue succeeded
    ... (60+ more school folders from Wave 2/3 — actively filling)
    # Within each school: <8-hex source_id>/<year>_<season>_<timestamp>.html ; optional legacy/*.html

talent_pipeline/                        ← CODA / Army pipeline mirror (talent_net); cox_plot_helpers, 520 notebooks

python_packages/
  dblp-parser/
    dblp.xml                              ← full DBLP XML dump (5.1 GB)

current_documents/
  tenure_documents/                     ← PEER / tenure gameplan + overview
  sports_documents/                     ← SCOUT / basketball gameplan + advisor docs
  talent_documents/                     ← CODA / Army advisor + pipeline notes (incl. Venues/); mirror of AWS workflow
```

---

## 7. Scraping Playbook: Lessons from the Pilot

These are the practical techniques discovered while building the pilot. They should be consulted whenever a school's HTML appears empty or malformed during expansion toward full Carnegie R1 coverage (~187 institutions; the coded list may remain a subset).

### Rule 1: When a page is empty, read its nav bar before giving up

The most important lesson from the pilot. Both Cornell and UMD appeared to have no data — but their nav bars contained exact Wayback links to faculty sub-pages that were fully populated. The script to run:

```python
from bs4 import BeautifulSoup
# Option B: path is typically faculty_snapshots/<slug>/<source_id>/2018_fall_<timestamp>.html
soup = BeautifulSoup(open('faculty_snapshots/some_school/abcd1234/2018_fall_20180915120000.html').read(), 'html.parser')
for a in soup.find_all('a'):
    if any(k in (a.get('href','') + a.get_text()).lower()
           for k in ['faculty', 'people', 'phonebook', 'directory', 'personnel']):
        print(f"[{a.get_text(strip=True)}] -> {a.get('href','')}")
```

Look for links starting with `/web/TIMESTAMP/` — those are exact archived sub-page URLs you can download directly without any CDX queries.

### Rule 2: Department Phonebooks are gold mines

UMD's `/people/phonebook/faculty` page returned **name, title, location, phone, email, and homepage link** for every faculty member in a simple, consistent HTML table — every year from 2013 to 2024. Phonebook pages are:

- Almost always static HTML (never JS-rendered)
- Consistent in structure across years (easy single parser)
- Rich in data fields beyond just name and rank
- Well-archived by Wayback (simple pages get crawled reliably)

**When scouting a new school for the expansion, always check if they have a phonebook page before relying on the main faculty listing.** Common URL patterns:

| Pattern | Schools likely to have it |
|---------|--------------------------|
| `/people/phonebook` | Drupal-based CS sites (UMD, similar) |
| `/people/phonebook/faculty` | Same, filtered to faculty |
| `/directory/` | Older institutional CMS |
| `/faculty-staff/` | Some Engineering school sites |
| `/about/people/` | WordPress-based sites |

### Rule 3: JS-rendered hub pages often have static sub-pages

Cornell's `/people` hub page was a JavaScript shell, but `/people/faculty` — the sub-page it linked to — rendered as fully static HTML with complete faculty data. This is a common pattern in Drupal, Gatsby, and similar CMSes: the hub page is a React-rendered directory router, but the individual category pages are server-side rendered.

**When a hub page is empty:** try appending `/faculty`, `/faculty/`, or `/faculty/index.htm` to the base URL before concluding the school is unscrapable.

### Rule 4: Old-era `.htm` files are reliably static

Cornell's 2005–2012 faculty pages used the naming convention `/People/faculty/index.htm`. Files with `.htm` or `.html` extensions in path segments (as opposed to served dynamically) are almost always static. They were written to disk on the web server and are captured perfectly by Wayback. If CDX shows coverage back to the early 2000s, these older pages are almost certainly parseable even if the modern site isn't.

### Rule 5: The deferred-pile is the right pattern for network-unreliable downloads

The two-pass deferred strategy (Pass 1 → collect connection errors silently → cooldown → Pass 2 at slower pace) proved essential. On a spotty network, 9 of 54 downloads failed in pass 1 but all 9 succeeded in pass 2 after the cooldown. The key design principles:

- **Never write connection errors to the index during pass 1** — keep them in the deferred pile so pass 2 can retry them cleanly
- **Only write `ok` to the "done" set** — everything else is retried on next run
- **Distinguish error types:** `http_404` (write-off), `http_error` (transient server error, retry next run), `connection_error` (network issue, retry next run)

### Rule 6: When a file is tiny and uniform, check for meta-refresh redirect shells

NC State exposed a third failure mode beyond JS shells and empty hubs: the `<meta http-equiv="refresh">` redirect shell. Symptoms:
- All downloaded files for a school are the same small size (~2 KB)
- File content is minimal HTML with no faculty names
- Inspection shows a `<meta http-equiv="refresh" content="0;url=...">` tag

The fix is simpler than the nav-bar approach: the correct Wayback URL is already embedded in the redirect target. Extract it with regex and download directly:

```python
import re
_E_REFRESH_RE = re.compile(
    r'<meta[^>]+http-equiv=["\']refresh["\'][^>]+content=["\'][\d.]+;\s*url=(https?://[^"\'>\s]+)',
    re.IGNORECASE
)
with open(html_file) as f:
    m = _E_REFRESH_RE.search(f.read())
if m:
    wayback_url = m.group(1)  # ready to download directly
```

**Diagnostic check for this pattern:** If all files for a school are < 5 KB and identical in size, it's almost certainly redirect shells. The meta-refresh tag will be visible in the first 20 lines of the file.

### Rule 7: CDX wildcard queries reveal what paths were actually captured

For schools where the specific faculty page URL has zero snapshots, query the base domain with a wildcard to discover what *was* crawled:

```
http://web.archive.org/cdx/search/cdx?url=cs.example.edu/*&output=json&fl=timestamp,original&limit=5000
```

This returns every path the Archive captured under that domain. Sort by frequency to find the most reliably-crawled paths. Northwestern, Iowa State, and Colorado State all recovered coverage this way — the base domain (`cs.northwestern.edu/`) had 133+ snapshots even though the specific `/people/faculty/` path had zero.

---

## 7.5 IPEDS fall enrollment (notebook `541` / `build_school_enrollment_from_ipeds.py`)

**Purpose:** Fill `tenure_pipeline/school_enrollment_annual.csv` with **total fall headcount** per school and calendar year so **Stage 3 viz** (`viz_pipeline.plot_stage3a` / `plot_stage3b`) can color by enrollment tier. Data come from NCES IPEDS **Fall Enrollment, Part A** files (`ef{year}a.zip`).

**Artifacts:**

| File | Role |
|------|------|
| `school_enrollment_annual.csv` | Columns `university`, `year`, `total_enrollment` (must match `r1_cs_departments.csv` names). |
| `ipeds_unitid_crosswalk.json` | Maps each `university` string → **UNITID** used for IPEDS pulls. |
| `_ipeds_cache/` | Downloaded NCES zips. Invalid/corrupt cached files (HTML or partial downloads saved as `.zip`) are **detected and removed automatically** on the next run (`zipfile.is_zipfile`); see `stale_cache_removed` in the JSONL. |
| `ipeds_download_errors.jsonl` | **JSONL** (one JSON object per line): download/parse skips and HTTP outcomes for manual follow-up. |

**`HD_YEAR` (e.g. `--hd-year 2023`):** Which IPEDS **Institution Directory** file to load: `hd{HD_YEAR}.zip`. That directory lists **UNITID**, **INSTNM** (official name), and **IALIAS** so the script can match your pipeline’s `university` strings to a stable **UNITID**. It does **not** set the years of enrollment—those come from each fall file `ef2004a` … `ef2024a` in the year loop. UNITIDs rarely change; picking a recent HD year is usually fine. If a new campus split or rename appears, refresh overrides in the build script or bump `HD_YEAR` after NCES releases a new directory.

**`ipeds_download_errors.jsonl` — `outcome` field (and meaning):**

| `outcome` | Meaning |
|-----------|---------|
| `run_start` | Run opened; includes `year_min`, `year_max`, `hd_year`, retry settings. |
| `http_404` | NCES has no file at that URL (wrong year, not released yet, or renamed table). Use `url` / `zip_name` to search [IPEDS Data Center](https://nces.ed.gov/ipeds/datacenter/DataFiles.aspx). **Not retried.** |
| `retry_exhausted` | Transient failure (429, 5xx, timeout, connection error) persisted through all backoff retries. |
| `http_error` | Other HTTP status (e.g. 403); not treated as transient. |
| `download_failed` | Unexpected error during download (after HTTP layer); see `error`. |
| `bad_zipfile` | Bytes on disk are not a valid zip after download (rare if cache is healthy). |
| `stale_cache_removed` | A file existed at `*.zip` but failed `zipfile.is_zipfile` — removed and re-fetched. |
| `zip_no_csv` | Zip opened but no usable CSV inside. |
| `hd_schema` | Directory CSV missing expected columns (`UNITID`, `INSTNM`, `IALIAS`). |
| `ef_year_skip` | File loaded but layout unusable: `no_efalevel` (pre-2004-style) or `no_enrollment_columns`. |

**HTTP behavior:** NCES GETs use exponential backoff + jitter on **429**, **500–504**, **timeouts**, and **connection errors** (`--max-retries`, `--backoff-base`). **404** is logged once and not retried.

### 7.6 Stage visualization (`tenure_pipeline/viz_pipeline.py`)

Called from **`540`** after Cells **3A**, **3B**, **4**, **5** (see notebook “VIZ” cells). Requires **`%matplotlib inline`** in CELL 0 for inline figures.

| Function | When | Output (default under `tenure_pipeline/`) |
|----------|------|-------------------------------------------|
| `plot_stage3a` | After CDX plan exists | `stage3a_summary.png` — lollipop, band donut, **year × school** heatmap (plan presence × enrollment tier) |
| `plot_stage3a_enrollment_bin_heatmap` | Same window as 3A | `stage3a_enrollment_bin_heatmap.png` — **aggregate** year × **enrollment bin** (not per school): top panel = share of schools in bin with ≥1 plan row; bottom = **median** enrollment in bin → fixed tier colors. Params: `n_bins` (e.g. 20–40), `binning='quantile'` (equal count) or `'equal_width'` |
| `plot_stage3b` | After download index | `stage3b_summary.png` |
| `plot_stage4_diag` | After parse | Parse quality diagnostics |
| `plot_stage5` | After panel | Longitudinal summary |

**Enrollment inputs:** `STAGE3_ENROLLMENT` → `school_enrollment_annual.csv` (rebuild via notebook **`541_ipeds_enrollment.ipynb`** / `build_school_enrollment_from_ipeds.py`). Tier cutpoints (`ENROLLMENT_SMALL_MAX`, `ENROLLMENT_MEDIUM_MAX`) live in `viz_pipeline.py`.

---

## 8. Expansion Plan: Current State → Broader R1 Coverage

**Where we are:** **`PILOT_SCHOOLS` holds 168** R1 CS departments (`r1_schools_data.py`). Carnegie lists on the order of ~187 R1 universities; not every R1 has a freestanding CS department in scope, and not every department has good Wayback coverage.

**Current bottlenecks (typical):**
1. **CDX timeouts / sparse Archive coverage** — use Cell 3A-RETRY, wildcard CDX queries, and `url_update_worksheet.csv` for URL fixes.
2. **Parser quality / bad URLs** — URL worksheet + manual fixes; optional Cell 4 condemn path only if `CELL4_CONDEMN_ON_FAILURE` is enabled (default **False**).
3. **503 / Archive outages** — server-side; retry later.

**Path toward fuller coverage:**
1. **CELL 2 additions:** Add remaining departments via manual URL research in `r1_schools_data.py`, then rebuild `r1_cs_departments.csv`.
2. **CELL 3A + 3A-RETRY:** Full roster at 2s delay + ~45s/~60s timeouts is often an overnight job; optional **bridge** sleep between pass 1 and retry.
3. **CELL 3B + 4:** Large HTML corpora; checkpoint/resume everywhere.
4. **Scope:** The `dept_name` and `notes` columns track EECS vs CS naming and oddball cases.

---

*Document written by PEER, April 4, 2026. Revised April 5, 2026 (rev 3) for Wave 3 and Cells 3D/3E. Revised April 7, 2026 (rev 4) for **168-school `PILOT_SCHOOLS`**, CDX 2s delay / 20s timeout / retry queue + Cell 3A-RETRY, bookmark/`tried_urls` behavior, Cell 4 outputs (`faculty_snapshots_parsed.jsonl`), and removal of stale 71/114 coverage snapshot. Revised April 8, 2026 (rev 5) for **Option B** on-disk paths (`faculty_snapshots/<uni_slug>/<source_id>/…`), `faculty_source_id()` / `iter_school_html_files()`, and `legacy/`. Revised April 10, 2026 (rev 6): **§0** clarifies split vs **`TENURE_DATA_GAMEPLAN.md`** (gameplan restructured to mirror sports gameplan). Revised April 10, 2026 (rev 7): **§0** adds **§G1–§G14** gameplan anchors + gameplan stage map ↔ overview §2–§4 table; gameplan working agreement links to this §0. Revised April 2026 (rev 8): **§5** adds **Temporal keys** (exact Wayback timestamps vs spring/fall design strata) and **Collisions** (blending, contradiction flags, linker as baseline). Revised April 2026 (rev 9): **CELL 5** panel + plan join; pipeline table renumbered (6–9); **`faculty_linker`** basename fallback for legacy HTML paths. Revised April 2026 (rev 10): **CELL 3A** multi-capture per season band (`CDX_SNAPS_PER_SEASON`); timestamped filenames; **CELL 5** panel dedupe includes **`local_path`**; gameplan **Snapshot identity** + working agreement **fix plumbing early**. Revised **2026-04-11 (rev 11):** **`CDX_SNAPS_PER_SEASON` = 12**, **`CDX_SPACING_POOL_MULT`**, **`CDX_SLEEP_BEFORE_RETRY_SEC`** bridge cell; CDX timeouts **45s / 60s**; **`tried_urls`** / clean-slate semantics; Option B examples + index schemas use **`<year>_<season>_<timestamp>.html`**; **429** vs timeout; Cell 4 condemn = **default off** (`CELL4_CONDEMN_ON_FAILURE`). Revised **2026-04-10 (rev 12):** **§7.5** IPEDS fall enrollment (`541` / `build_school_enrollment_from_ipeds.py`): artifacts, **`HD_YEAR`** (directory vs enrollment years), **`ipeds_download_errors.jsonl`** outcomes table, HTTP backoff behavior. Revised **2026-04-12 (rev 13):** **§4** CELL **6A–6B** OpenAlex (`openalex_resolver.py`) + **bulk snapshot at UVA pending access**; pipeline table updated; **§7.5** `stale_cache_removed` outcome + auto-cache validation; **§7.6** Stage viz (`plot_stage3a`, **`plot_stage3a_enrollment_bin_heatmap`**, etc.); **§6** file list — enrollment + OpenAlex + IPEDS artifacts.*
