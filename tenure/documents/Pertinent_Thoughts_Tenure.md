# Pertinent Thoughts — Tenure Pipeline

Observations worth carrying into **dissertation prose**, **limitations**, or **methods** — not a substitute for **`TENURE_PIPELINE_OVERVIEW.md`** (implementation) or **`TENURE_DATA_GAMEPLAN.md`** (contract).

**Re-verify after each major scrape/parse:** Coverage counts, “red tier” schools, and rescue outcomes change when you re-run Cells 3A–4. Use current **`faculty_snapshots_plan.jsonl`**, **`pipeline_health_audit.csv`**, and **stage 4 viz** as ground truth, not the illustrative numbers below unless you have re-checked them. For **enrollment-colored** Stage 3 figures and **IPEDS** rebuild steps, see overview **§7.5–§7.6** (notebook **`541`** / `build_school_enrollment_from_ipeds.py`). **OpenAlex bulk** at UVA is **not** available yet — see overview **§4** and gameplan advisor direction.

---

## Internet Archive / URL limitations (school-level)

### Auburn — often no usable Wayback replay

CSSE URLs have repeatedly shown **no usable CDX/replay** (timeouts, 403-style behavior), consistent with **robots.txt / exclusion** from replay. Treat as a **coverage limitation**, not a parser bug. **Re-verify** against your latest plan and health audit before claiming Auburn is unique among the roster.

### NC State — redirect shells

Historically, many captures were **tiny `<meta refresh>` shells** pointing at `/directories/faculty.php` while Wayback did not always serve parseable content at the redirect target. **CELL 3E** in the notebook attempts rescue; success depends on Archive availability at re-run time. For prose: distinguish **shell on disk** vs **parseable faculty HTML**. Mechanics: **`TENURE_PIPELINE_OVERVIEW.md`** (Phase E).

### UW–Madison / UIUC — sub-page and era gaps

**CELL 3D** addresses the **JS hub → static sub-page** pattern. Residual **404s** or **missing nav links** in early years are **Archive gaps**, not necessarily code bugs. Panel coverage for these schools may **truncate** earlier or later than the global 2000–2024 window—report **empirical** year ranges from parsed output.

---

## UIUC — homepage vs faculty listing (method note)

Wayback sometimes captured the **department homepage** instead of the **All Faculty** listing for earlier eras, which **depresses** extracted counts before the site reorganisation. **Do not** interpret long-run faculty-count trends at UIUC without checking **page type** (title, link density, URL) for each interval. If the canonical faculty URL in **`r1_schools_data.py`** was updated, **re-CDX** and re-parse before locking conclusions.

---

## Parser — compound titles vs rank (`html_parser.py`)

The rank normaliser can match the **first** recognised rank token, so strings like **“adjunct assistant professor”** may map to **`assistant`** instead of **`adjunct`**. A **modifier-first** pass (adjunct / visiting / research / clinical) before base rank would better support tenure-track filtering later. Scale: order **~few %** of rows in large runs—worth a logged fix, not a silent assumption in the thesis.

---

## “Bad URL” schools (ongoing QA)

Some departments plot **low average faculty per snapshot** in **stage 4 diagnostics** (`plot_stage4_diag` in **`viz_pipeline.py`**) because CDX hit a **homepage or wrong path**, not because the department is tiny. **Examples** that have appeared in QA: **UCLA**, **Duke** — use as illustrations only; the current list is whatever the latest diagnostic shows. Fix path: **`url_update_worksheet.csv`** → **`apply_url_updates.py`** → **`r1_schools_data.py`** → Cell 2 → re-scrape.

---

---

## Rivanna HPC — Operational Notes and Gotchas

### The "part everyone misses" — Playwright browser binaries

When installing Playwright (the headless-browser PDF converter used by
`convert_single_md_to_pdf.sh`), there are **two separate steps** and almost
everyone only does one:

**Step 1 — install the Python library** (conda or pip, your choice):
```bash
conda install -n tenure_net -c conda-forge playwright
# or:
/home/dzk3ja/.conda/envs/tenure_net/bin/pip install playwright
```

**Step 2 — install the Chromium browser binary** (always required, always Playwright's own CLI):
```bash
/home/dzk3ja/.conda/envs/tenure_net/bin/python -m playwright install chromium
```

Step 2 is what trips everyone up. The browser binary is not a Python package —
it is a bundled Chromium executable that Playwright downloads and manages
separately from conda or pip. Conda has no equivalent mechanism for this.
If you skip Step 2, the Python import works fine but any attempt to launch
a browser crashes with `ImportError: Playwright not installed` (misleading
error message — the library is there; the *browser* is not). The fix is
always Step 2, not re-installing the library.

**This also applies after environment rebuilds.** If you ever recreate the
`tenure_net` conda environment from scratch, you must re-run Step 2 — the
browser binary lives outside the conda env tree.

---

### Cursor on Rivanna — two workflows and how they fit together

You have two distinct ways to use Cursor with this project, and they serve
different purposes. Understanding the distinction prevents confusion about
which files are "live."

#### Workflow A — Cursor Remote SSH (primary heavy-compute workflow)

Connect Cursor on your Mac to Rivanna via SSH remote. Cursor opens the
`~/Ivy_Net` workspace *on Rivanna* directly — you edit files there, run
terminals there, and submit Slurm jobs there. The notebook kernel also
runs on Rivanna, so all HPC data (OpenAlex snapshot, CDH files) is
accessible natively.

**Best for:**
- Running Slurm batch jobs (`sbatch build_openalex_cache.slurm`)
- Cells that touch the OpenAlex snapshot (Cell 6B in snapshot mode)
- Anything that needs the `~/cdh/OpenAlex1125/` data tree
- Running `discover_faculty_urls.py` (CDX queries, internet access)
- Generating PDFs with `convert_single_md_to_pdf.sh` (Playwright/Chromium)

**The workspace is Rivanna.** Edits are immediately live there.

#### Workflow B — Local Mac (coffee-shop / offline workflow)

Clone the repo on your Mac (`git clone`). Open the `~/Ivy_Net` local copy
in Cursor on your Mac — no SSH connection needed. All code cells that
don't need the HPC snapshot run fine locally, including Stages 7, 8, 9
and the `discover_faculty_urls.py` CDX script.

**Best for:**
- Stages 7–9 (pure pandas/numpy — no large data files needed)
- Editing code and documentation
- Running `discover_faculty_urls.py` (internet access fine on Mac)
- Reviewing plots and outputs from a prior Rivanna run

**The workspace is your Mac.** Edits stay local until you push/pull.

---

### Keeping the two workspaces in sync — git and rsync

**Code and docs → git (always)**

All `.py`, `.ipynb`, `.md`, `.slurm`, `.sh`, `.csv` (schema files), and
`.json` (config files) files live in git. The standard loop:

```bash
# On Rivanna: after making changes
git add -A && git commit -m "message" && git push

# On Mac: pull those changes
git pull
```

**Large data files → rsync (never git)**

The gitignore explicitly excludes the large output files. Transfer them
with rsync when you need them locally after a Rivanna run:

```bash
# From your Mac — pull the two OpenAlex data files after a Rivanna run:
rsync -avz --progress \
  rivanna:~/Ivy_Net/tenure/tenure_pipeline/openalex_snapshot_cache.jsonl \
  ~/path/to/Ivy_Net/tenure/tenure_pipeline/

rsync -avz --progress \
  rivanna:~/Ivy_Net/tenure/tenure_pipeline/openalex_works_by_year.jsonl \
  ~/path/to/Ivy_Net/tenure/tenure_pipeline/
```

Once those two files are local, Cell 6B in the notebook automatically
detects it is not on Rivanna and serves from cache — Stages 7–9 run
entirely offline. See `STAGE6B_API_FALLBACK` in Cell 0 and
`openalex_resolver.py` Route 2 documentation for details.

**Rule of thumb:**
- If the file is code or config → git
- If the file is data (JSONL, large CSV, HTML snapshots) → rsync
- If you are unsure → check `.gitignore`

---

## The Iron Rule of Long-Running Jobs: Save As You Go

> **Any script with a multi-iteration loop over network or large disk I/O must write and flush results after each iteration — never batch at the end.**

This lesson came up painfully when `discover_faculty_urls.py` ran for 2+ hours and
would have lost everything to a dropped connection. The fix is always the same:

```python
# ✅ CORRECT — write + flush after every unit of work
with open(OUT_JSONL, 'a', encoding='utf-8') as f:
    for item in big_collection:
        result = expensive_network_call(item)
        f.write(json.dumps(result) + '\n')
        f.flush()   # push to OS immediately — safe against kill signals

# ❌ WRONG — all work lost if killed at any point before the final write
results = []
for item in big_collection:
    results.append(expensive_network_call(item))
with open(OUT_JSONL, 'w') as f:
    json.dump(results, f)
```

**Always pair this with a resume/skip check at startup** — read back what is already
on disk and skip those items. The output file IS the checkpoint.  This is how both
`build_openalex_cache.py` (per author) and `discover_faculty_urls.py` (per school)
work. When a job is cancelled or times out, re-submit and it picks up where it left off.

The pattern is codified as a Cursor project rule in
`.cursor/rules/incremental-writes.mdc` so it is enforced automatically.

---

*Last tightened: **2026-04-16** — added Rivanna operational notes: Playwright
two-step install gotcha; Cursor Remote SSH vs local Mac workflows; git vs
rsync data management. Prior: **2026-04-12** — cross-links to overview
§7.5–§7.6 (IPEDS + viz) and §4 / gameplan (OpenAlex API vs bulk access
pending).*
