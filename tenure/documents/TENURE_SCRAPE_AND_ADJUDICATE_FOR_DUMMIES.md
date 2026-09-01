# Tenure pipeline — scrape & adjudicate re-entry (for dummies)

**Last synced:** 2026-09-01  
**Audience:** Charles, returning after a break  

**Important:** Reading this doc adds **nothing** to the corpus. **New HTML only appears after you (1) introduce new scrape candidates, then (2) run notebook cells on Rivanna.** See [If you are expanding data](#if-you-are-expanding-data--start-here) below.

---

## If you are expanding data — START HERE

**Goal:** More schools, better URLs, or HTML files you do not have yet.

Nothing downloads by itself. Expansion is always a **two-phase** loop:

```
Phase 1 — Feed new candidates into the pipeline   (Mac; human or script)
Phase 2 — Run Cells 2 → 3A → 3B → 4 on Rivanna   (actually hits Wayback)
```

### Where new scrape candidates come from

| You want… | How candidates enter the system | Then run |
|-----------|----------------------------------|----------|
| **A. New R1 CS department** | Add a row to `r1_cs_departments.csv` and/or `r1_schools_data.py` (`PILOT_SCHOOLS`) with primary URL + `alt_urls` | [Workflow D](#workflow-d--expand-the-school-list) → [Workflow A](#workflow-a--run-the-scrape-chain) |
| **B. Better URL for a weak school** | Paste into `new_url` in `url_update_worksheet.csv` — from your research, or from `faculty_url_suggestions.csv` after running `discover_faculty_urls.py` | [Workflow B](#workflow-b--adjudicate-faculty-urls-human-loop) → Workflow A |
| **C. URLs already on the list but never CDX-queried** | No edit needed — Cell 3A skips URLs already in `faculty_snapshots_plan.jsonl` and queries **untried** ones only | Workflow A with `RUN_CELL3_CDX=True` |
| **D. CDX succeeded but HTML never downloaded** | Plan rows exist; index/HTML gaps — check `faculty_snapshots_index.jsonl` vs plan | Workflow A with **`RUN_CELL3_CDX=False`**, `RUN_CELL3_DOWNLOAD=True` |
| **E. CDX timed out earlier** | URLs sitting in `cdx_retry_queue.jsonl` | Workflow A with `RUN_CELL3_RETRY=True` |

**Most common expansion path today:** **B** (fix weak parsers) or **A** (add schools toward ~187 R1). Run **`discover_faculty_urls.py`** when you want automated URL leads for schools parsing poorly (needs Cell 4 output on disk first).

### Phase 1 checklist (Mac — before any Rivanna job)

1. **Pull latest HPC outputs** (so worksheets reflect reality):
   ```bash
   ./scripts/rsync_pull_recent_hpc.sh tenure
   ```
2. **Pick your expansion type** (table above: A–E).
3. **If A or B — edit inputs:**
   - New school → `r1_cs_departments.csv` / `r1_schools_data.py`
   - New/better URL → `url_update_worksheet.csv` column **`new_url`**, then:
     ```bash
     python tenure/tenure_pipeline/apply_url_updates.py
     ```
   - Auto-suggest URLs for bad schools:
     ```bash
     python tenure/tenure_pipeline/discover_faculty_urls.py
     # → faculty_url_suggestions.csv → paste into new_url → apply_url_updates.py again
     ```
4. **Push code + worksheet changes to Rivanna:**
   ```bash
   ./scripts/rsync_push_to_hpc.sh
   ```

### Phase 2 — run the scrape (Rivanna)

Open **`540_tenure_pipeline.ipynb`**, set Cell 0 flags ([cheat sheet](#cell-0-cheat-sheet-copypaste-mindset)), then:

```bash
cd ~/Ivy_Net && sbatch pipe_job.slurm
```

Minimum flags for **new URLs or schools:** `RUN_CELL2`, `RUN_CELL3_CDX`, `RUN_CELL3_DOWNLOAD`, `RUN_CELL4` = `True`; everything else `False`.

**Only after Phase 2** do `faculty_snapshots/`, parsed JSONL, and panel files grow.

---

## YOU ARE HERE — pick your lane

| If you want to… | Start at | Adds new data? |
|-----------------|----------|----------------|
| **Expand coverage** (schools, URLs, HTML) | [If you are expanding data](#if-you-are-expanding-data--start-here) | **Yes** — after Phase 2 |
| **See whether the corpus is healthy** (no runs) | [Step 0](#step-0--orientation-only-no-new-data) | **No** — read-only |
| **Fix weak URLs then re-scrape** | [Workflow B](#workflow-b--adjudicate-faculty-urls-human-loop) → A | Yes — after re-scrape |
| **Review ambiguous OpenAlex IDs** | [Workflow C](#workflow-c--adjudicate-openalex-matches) | Only if you change match rules |
| **Rebuild panel / plots on existing scrape** | [Workflow E](#workflow-e--downstream-after-a-good-scrape) | No new Wayback HTML |

**Do not read first:** `TENURE_PIPELINE_OVERVIEW.md` (900+ lines — reference only). This file is the ordered path back in.

---

## Step 0 — Orientation only (no new data)

**This section does not query Wayback, download HTML, or change any pipeline file.** Use it to re-orient or sanity-check before you decide *what* to expand in Phase 1 above.

### The one entry point

| What | Path |
|------|------|
| **Notebook (conductor)** | `tenure/540_tenure_pipeline.ipynb` |
| **Always run first** | **Cell 0** — paths, constants, and **`RUN_CELL*`** booleans |
| **School list (code)** | `tenure/tenure_pipeline/r1_schools_data.py` |
| **School list (CSV)** | `tenure/tenure_pipeline/r1_cs_departments.csv` |
| **Human URL queue** | `tenure/tenure_pipeline/url_update_worksheet.csv` |

### Where the big files live

| Location | Role |
|----------|------|
| **Rivanna** `~/Ivy_Net/tenure/tenure_pipeline/` | Canonical scrape outputs (HTML tree, JSONL, plots) |
| **Mac** (Dropbox workspace clone) | Code, docs, small CSVs; rsync **pull** after HPC runs |
| **Git** | Code + configs only — **not** multi-GB HTML/JSONL |

**Mac ↔ Rivanna sync (from repo root on Mac):**

```bash
./scripts/rsync_push_to_hpc.sh              # code → Rivanna before a run
./scripts/rsync_pull_recent_hpc.sh tenure   # tenure_pipeline outputs → Mac after a run
```

Details: [`scripts/DATA_SYNC.md`](../../scripts/DATA_SYNC.md), [`HPC_SETUP_CHECKLIST.md`](HPC_SETUP_CHECKLIST.md).

### Quick health check (after rsync or on Rivanna)

Open or `tail` these — they tell you if you're ready to expand or need URL fixes:

| File | Good sign |
|------|-----------|
| `faculty_snapshots_plan.jsonl` | Row count stable or growing; not empty |
| `faculty_snapshots_index.jsonl` | Download log matches plan |
| `faculty_snapshots_strategy_audit.jsonl` | Exists (Cell 4 wrote it) |
| `pipeline_health_audit.csv` | Per-school coverage summary |
| Stage 4 diagnostic plots | No obvious “5 names per page” red schools |

**Rule:** After any major scrape, trust **current** audit files — not numbers from old memos.

---

## The scrape chain (what “scraping” means here)

Stages run **in order** inside `540`. You rarely run all cells every time — Cell 0 flags choose the slice.

```
Cell 0 (flags)
  → Cell 2   school list
  → Cell 3A  CDX discovery (Wayback index queries)     ← needs internet
  → Cell 3A-RETRY  slow CDX retry queue
  → Cell 3B  HTML download
  → Cell 3C–3E  rescues (sub-pages, redirects) — usually OFF unless you know you need them
  → Cell 4   parse HTML → faculty records
  → Cell 5   longitudinal panel
  → Cells 6A–6B  OpenAlex match + works
  → Cells 7–9  enriched panel, pools, inverted-U plot
```

**“Adjudicating”** in this project means **two human loops**:

1. **URL adjudication** — pick the right faculty-directory URL per school (`url_update_worksheet.csv`).
2. **OpenAlex adjudication** — resolve ambiguous author IDs (`openalex_low_confidence.jsonl`).

---

## Workflow A — Run the scrape chain

**Goal:** Turn Phase 1 candidates into HTML on disk. **If you skipped Phase 1, this run mostly re-processes what you already have** (3A skips tried URLs; 3B skips existing downloads unless gaps exist).

**Prerequisite:** Completed [If you are expanding data — Phase 1](#phase-1-checklist-mac--before-any-rivanna-job) unless you only need type **D** or **E** (download/retry gaps only).

### A1. Choose Mac vs Rivanna

| Step | Rivanna | Mac local |
|------|---------|-----------|
| Cell 3A CDX queries | ✅ Login node or Slurm* | ✅ If you have internet |
| Cell 3B download (long) | ✅ **Preferred** (`sbatch`) | Possible but slow |
| Cell 4 parse | ✅ | ✅ |
| Cells 7–9 | ✅ | ✅ (often faster on Mac) |

\*Slurm **compute nodes** may block outbound HTTP — CDX in batch can fail. **`pipe_job.slurm`** is tuned for download/parse after CDX was done on login node, or use login-node Jupyter for 3A.

### A2. Set Cell 0 flags (typical “fill HTML gaps” run)

In **`540_tenure_pipeline.ipynb` Cell 0**, set **only** what you need **`True`**; leave the rest **`False`** (skipped cells reload from disk).

| Task | Set `True` |
|------|------------|
| Refresh school list after URL edits | `RUN_CELL2` |
| New CDX queries (new/changed URLs) | `RUN_CELL3_CDX` |
| Retry timed-out CDX URLs | `RUN_CELL3_RETRY` |
| Download HTML for planned snapshots | `RUN_CELL3_DOWNLOAD` |
| Re-parse all HTML | `RUN_CELL4` |
| Rebuild person-year panel | `RUN_CELL5` |

**Usually leave `False`:** `RUN_CELL3C`, `RUN_CELL3D`, `RUN_CELL3E` (rescues — already done for pilot schools unless you're debugging one school).

**Quota safety:** CDX can 429. The notebook sleeps and retries; heavy CDX runs are better **overnight** or in **batches** (subset of schools via `PILOT_SCHOOLS` in `r1_schools_data.py`).

### A3. Run on Rivanna (recommended)

```bash
# On Rivanna, from repo root:
cd ~/Ivy_Net
git pull                                    # or rsync from Mac first
# Edit Cell 0 flags in 540 (Cursor Remote SSH or local edit + push)
sbatch pipe_job.slurm
squeue -u dzk3ja                            # confirm queued/running
tail -f slurm_out/slurm-pipe_job-*.out      # watch progress
```

Slurm details: [`HPC_SLURM_PIPELINE_GUIDE.md`](../HPC_SLURM_PIPELINE_GUIDE.md) (also at repo root `tenure/HPC_SLURM_PIPELINE_GUIDE.md`).

**CLI alternative** (Cell 0 + 3B only, no Jupyter): `tenure/run_stage3b_cli.py`.

### A4. Pull results to Mac

```bash
./scripts/rsync_pull_recent_hpc.sh tenure
```

### A5. Sanity-check

- Cell 4 / `viz_pipeline` stage-4 diagnostics: faculty counts per school look plausible?
- `url_update_worksheet.csv` — run `apply_url_updates.py` to refresh status columns (see Workflow B).

---

## Workflow B — Adjudicate faculty URLs (human loop)

**Goal:** Schools where the parser sees ~5–15 names per page instead of ~30–80 usually have the **wrong Wayback URL** (homepage, HR directory, wrong path).

### B1. Find bad schools

**Option 1 — Worksheet (sorted worst-first):**

```bash
python tenure/tenure_pipeline/apply_url_updates.py
# Opens/refreshes url_update_worksheet.csv — sort by school_snaps or mean parse quality
```

**Option 2 — Automated suggestions:**

```bash
python tenure/tenure_pipeline/discover_faculty_urls.py
# Output: faculty_url_suggestions.csv
# Guide: DISCOVER_FACULTY_URLS_GUIDE.md
```

Optional verified scoring:

```bash
TEST_PARSE=1 python tenure/tenure_pipeline/discover_faculty_urls.py
```

**Option 3 — Notebook viz:** Stage 4 diagnostic plots (`plot_stage4_diag`) — low average faculty per snapshot.

### B2. Decide on a URL (your judgment)

Open `url_update_worksheet.csv` or paste from `faculty_url_suggestions.csv` into column **`new_url`**.

| Red flag | Green flag |
|----------|------------|
| Generic staff/HR directory | Path contains `faculty`, `people`, `directory` |
| Whole-university search page | Subdomain `cs`, `eecs`, `cse`, `computing` |
| Single faculty bio (historical bug: UW–Madison `/people/pb`) | Consistent faculty list across Wayback years |

Verify in browser: `https://web.archive.org/web/*/YOUR_URL`

### B3. Apply and re-scrape

```bash
python tenure/tenure_pipeline/apply_url_updates.py
```

This updates **`r1_schools_data.py`** (and refreshes the worksheet stats).

Then on Rivanna (or Mac if small test):

1. Cell 0: `RUN_CELL2=True`, `RUN_CELL3_CDX=True`, `RUN_CELL3_DOWNLOAD=True`, `RUN_CELL4=True` (others `False` unless you need panel refresh).
2. Run notebook or `sbatch pipe_job.slurm`.

**Clean re-CDX for one school:** see `tenure/tenure_pipeline/rebuild_plan.py` (docstring in `apply_url_updates.py`).

---

## Workflow C — Adjudicate OpenAlex matches

**Goal:** Cell 6A assigns each faculty name an OpenAlex author ID with a confidence tier. Rows that need eyes are in:

`tenure/tenure_pipeline/openalex_low_confidence.jsonl`

Tiers: **HIGH / MEDIUM / LOW / MULTI / NONE** (see [`TENURE_PIPELINE_OVERVIEW.md`](TENURE_PIPELINE_OVERVIEW.md) §4).

**Advisor constraint:** Do not hand-fix IDs for a convenience subset unless the same rule applies everywhere (selection bias).

Typical loop:

1. Run or refresh Cell 6A on Rivanna (`RUN_CELL6A=True`, others `False`).
2. Pull `openalex_low_confidence.jsonl` to Mac.
3. Review MULTI (several candidates) and NONE (no match).
4. If you add override rules, encode them in resolver logic — not one-off notebook edits.
5. Cell 6B for works-by-year needs cache or CDH bulk on Rivanna — see overview §4 and `build_openalex_cache.slurm`.

---

## Workflow D — Expand the school list

**Goal:** Move toward full Carnegie R1 CS coverage (~187 schools; **168** in current list).

1. Add row to **`r1_cs_departments.csv`** (and/or edit **`r1_schools_data.py`** — Cell 2 reads the Python module).
2. Include **`alt_urls`** JSON list for domain migrations (UIUC, Georgia Tech, etc.).
3. Run Workflow A from Cell 2 onward.
4. Run Workflow B for any new school with weak parse counts.

---

## Workflow E — Downstream after a good scrape

Once HTML + Cell 4 look good:

| Step | Cell 0 | Output |
|------|--------|--------|
| Longitudinal panel | `RUN_CELL5=True` | `faculty_panel.jsonl` |
| OpenAlex IDs | `RUN_CELL6A=True` | `openalex_author_ids.jsonl` |
| Publication counts | `RUN_CELL6B=True` | `openalex_works_by_year.jsonl` |
| Enriched panel | `RUN_CELL7=True` | `faculty_panel_enriched.jsonl` |
| LOO pool metrics | `RUN_CELL8=True` | `faculty_panel_with_pools.jsonl` |
| Inverted-U plot | `RUN_CELL9=True` | `stage9_inverted_u.png` |

**Cells 7–9 run fine on Mac** with rsync'd JSONL inputs — no Slurm required.

Advisor CSV export: notebook **`543_package_panel.ipynb`**.

---

## Cell 0 cheat sheet (copy/paste mindset)

**Golden rule:** Exactly **one** “phase” per Slurm submission unless you know what you're doing. Set wanted flags `True`, everything else `False`.

| I want to… | True flags |
|------------|------------|
| URL fix → re-scrape one wave | `RUN_CELL2`, `RUN_CELL3_CDX`, `RUN_CELL3_DOWNLOAD`, `RUN_CELL4` |
| Download only (plan already good) | `RUN_CELL3_DOWNLOAD`, maybe `RUN_CELL4` |
| CDX retry queue overnight | `RUN_CELL3_RETRY` |
| Re-parse after parser fix | `RUN_CELL4`, then `RUN_CELL5` if panel should update |
| Full analysis refresh | `RUN_CELL7`, `RUN_CELL8`, `RUN_CELL9` |
| OpenAlex cache build (separate job) | `sbatch build_openalex_cache.slurm` — not the notebook |

Always read the **current** defaults at the top of Cell 0 before overwriting — they may match “resume from last run.”

---

## Git hygiene after a good run

```bash
cd ~/Ivy_Net   # or Mac clone
git add -A
git status     # verify: no *.html, huge *.jsonl, or slurm noise staged
git commit -m "Tenure scrape: <brief description>"
git push
```

Large artifacts stay on disk / rsync — see `.gitignore`.

---

## When things go wrong

| Symptom | Likely fix |
|---------|------------|
| CDX timeouts | `RUN_CELL3_RETRY=True`; check `cdx_retry_queue.jsonl` |
| Empty HTML / 404 shells | Wrong URL → Workflow B; or Cell 3C–3E rescue for known JS/sub-page schools |
| CDX 429 rate limit | Slow down; run overnight; don't parallelize CDX jobs |
| Slurm job can't reach Wayback | Run 3A on **login node**; use Slurm for 3B+ |
| Parser count suddenly dropped | Check Option B paths / `legacy/` — overview §5 |
| Mac missing OpenAlex bulk | Use rsync'd `openalex_snapshot_cache.jsonl`; run bulk build on Rivanna |

Scraper playbook (nav bars, phonebooks, JS shells): **overview §7**.

---

## Deep reference (not for first pass)

| Document | Use when |
|----------|----------|
| [`TENURE_PIPELINE_OVERVIEW.md`](TENURE_PIPELINE_OVERVIEW.md) | Cell semantics, file tree, sentinel rules |
| [`TENURE_DATA_GAMEPLAN.md`](TENURE_DATA_GAMEPLAN.md) | Research intent, stage boundaries |
| [`HPC_SETUP_CHECKLIST.md`](HPC_SETUP_CHECKLIST.md) | VPN, conda, three scenarios (Rivanna / Mac / coffee shop) |
| [`DISCOVER_FACULTY_URLS_GUIDE.md`](DISCOVER_FACULTY_URLS_GUIDE.md) | Algorithm detail for URL discovery script |
| [`HPC_SLURM_PIPELINE_GUIDE.md`](../HPC_SLURM_PIPELINE_GUIDE.md) | `pipe_job.slurm`, papermill, log paths |
| [`Pertinent_Thoughts_Tenure.md`](Pertinent_Thoughts_Tenure.md) | QA heuristics (re-verify counts after each scrape) |
| [`VA_WEEKEND_CHECKLIST.md`](VA_WEEKEND_CHECKLIST.md) | **Historical** example overnight run (Apr 2026) — patterns still valid |

**Alex handoff bundle** (code + samples): `tenure/alex_tenure_handoff/README_HANDOFF.md`.

---

## Thread log

| Date | Note |
|------|------|
| 2026-09-01 | Created — ordered re-entry doc; Charles returning to expand tenure coverage after SCOUT/COMPASS progress |
| 2026-09-01 | Clarified: Step 0 is read-only; added **If you are expanding data** as first actionable path; catalogued five candidate sources (A–E) |
