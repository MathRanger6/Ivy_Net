# VA Weekend Checklist — Tenure Pipeline
**Goal:** Get pipeline fully up to speed before introducing new URLs from `faculty_url_suggestions.csv`

---

## Before You Start — Orientation

| Workspace | When to Use |
|-----------|------------|
| `Rivanna.code-workspace` | Slurm jobs, OpenAlex snapshot, HPC data |
| `Ivy_Net.code-workspace` | Code edits, git, rsync, local pipeline runs (Cells 7–9) |

**Rule:** Code changes → git commit + push. Data files → rsync only (never git).

---

## Phase 1 — Fill Gaps in Current Data (Rivanna)

### Step 1 — Fill 553 missing HTML downloads
- [ ] In Cell 0: set `RUN_CELL3_DOWNLOAD = True`, all others `False`
- [ ] `cd ~/Ivy_Net && sbatch pipe_job.slurm`
- [ ] Monitor: `tail -f slurm-pipe_job-<JOBID>.out`
- [ ] Confirm: 4 partial schools → complete (164 → 168 complete schools)

### Step 2 — Re-parse all HTML
- [ ] In Cell 0: set `RUN_CELL4 = True`, all others `False`
- [ ] `sbatch pipe_job.slurm`
- [ ] Confirm output: parsed_records count increases from 2,580,266

### Step 3 — Rebuild longitudinal panel
- [ ] In Cell 0: set `RUN_CELL5 = True`, all others `False`
- [ ] `sbatch pipe_job.slurm`  *(or run interactively — takes ~30 sec)*
- [ ] Confirm: panel rows, unique faculty, rank breakdown printed
- [ ] Check: tenure-track % looks reasonable (~60–70%)

---

## Phase 2 — Grow the OpenAlex Cache (Rivanna, run overnight)

### Step 4 — Run cache builder
- [ ] `cd ~/Ivy_Net && sbatch build_openalex_cache.slurm`
- [ ] Let run overnight — it resumes from checkpoint if interrupted
- [ ] Current cache: 836K (sparse). Target: covers all 168-school faculty

---

## Phase 3 — Expand Pilot to Top-40 Schools (Rivanna)

### Step 5 — Resolve author IDs for schools 21–40 (Cell 6A)
- [ ] In Cell 0: set `STAGE6_PILOT_TOP_N = 40`
- [ ] Set `RUN_CELL6A = True`, all others `False`
- [ ] `sbatch pipe_job.slurm`  *(network-heavy — let Slurm handle it)*
- [ ] Confirm: author ID count grows from 15,519
- [ ] Note: MULTI confidence cases (2,419) may be worth a manual heuristic pass later

### Step 6 — Fetch works by year for new authors (Cell 6B)
- [ ] In Cell 0: set `RUN_CELL6B = True`, all others `False`
- [ ] `sbatch pipe_job.slurm`
- [ ] Confirm: works file grows; snapshot cache used where available

---

## Phase 4 — Run Analysis with GAP_TOLERANCE = 4 (Mac Local or Rivanna)

### Step 7 — Enriched panel + pool metrics + inverted-U (Cells 7, 8, 9)
- [ ] In Cell 0: set `RUN_CELL7 = True`, `RUN_CELL8 = True`, `RUN_CELL9 = True`
- [ ] `STAGE7_GAP_TOLERANCE = 4`  *(already set)*
- [ ] `sbatch pipe_job.slurm`
- [ ] Compare Stage 9 inverted-U plot to previous run (GAP_TOLERANCE = 3)
- [ ] Note changes in resolved cases, censored %, tenure/attrition rates

---

## Phase 5 — Git Sync (after each Phase above)

Run after completing each phase — commit code changes only, never data:

```bash
cd ~/Ivy_Net
git add -A
git status        # verify: no *.jsonl, no *.html, no slurm-*.out staged
git commit -m "Weekend run: <brief description of what changed>"
git push
```

**Best commit points:**
- After changing Cell 0 flags (before each sbatch)
- After any code/`.py` edits
- After this checklist itself is updated

---

## Phase 6 — Review URL Suggestions (Mac Local)

*Do this AFTER Phases 1–5 are complete and results look stable.*

### Step 8 — rsync results back to Mac
```bash
# From your Mac:
./scripts/rsync_pull_from_hpc.sh
```

### Step 9 — Review suggestions CSV
- [ ] Open: `tenure/tenure_pipeline/faculty_url_suggestions.csv`
- [ ] Sort by `mean_recs` ascending (worst schools first)
- [ ] For each school: check `suggested_url` — does it look like a **CS faculty page**?
- [ ] **Red flags:** generic university staff directories, aging/CTE/HR pages
- [ ] **Green flags:** subdomain has `cs`, `eecs`, `cse`, `computing`; path has `faculty`, `people`
- [ ] Promising leads to investigate first:
  - Rice University (score 97, 2000–2024) — `rice.edu/Computer/facultystaff.html`
  - Kent State (score 84, 2019–2025) — `kent.edu/cs/faculty-staff-directory`
  - Lehigh (score 83, 2014–2026) — `lehigh.edu/academics/faculty`
  - Northwestern (score 83, 2012–2024) — check if it's the CS directory

### Step 10 — Add good URLs to the pipeline
```bash
# Edit r1_cs_departments.csv or use apply_url_updates.py
# Then re-run Cell 0 → Cell 2 → Cell 3A → Cell 3B → Cell 4
```

---

## Workspace File Notes

### `Rivanna.code-workspace`
- Opens Cursor → SSH Remote → Rivanna
- Terminal auto-activates `tenure_net` conda env in `~/Ivy_Net`
- Use for: Slurm, HPC data, remote debugging

### `Ivy_Net.code-workspace` (Mac local)
- Opens Dropbox workspace locally
- Use for: code edits, git, rsync, Cells 7–9 offline
- TODO: add Mac terminal profile to auto-activate `tenure_net`
  ```json
  "terminal.integrated.profiles.osx": {
      "tenure_net": {
          "path": "bash",
          "args": ["-c", "conda activate tenure_net && bash"]
      }
  },
  "terminal.integrated.defaultProfile.osx": "tenure_net"
  ```
- TODO: remove stale Windows PowerShell settings (harmless but cluttered)

---

## Quick Reference — Key Commands

```bash
# Submit a job
cd ~/Ivy_Net && sbatch pipe_job.slurm

# Monitor live
tail -f slurm-pipe_job-<JOBID>.out

# Check queue
squeue -u dzk3ja

# Pull results to Mac
./scripts/rsync_pull_from_hpc.sh

# Push code to Rivanna
./scripts/rsync_push_to_hpc.sh

# Cache builder
sbatch build_openalex_cache.slurm

# URL discovery
sbatch discover_faculty_urls.slurm
```

---

*Created by PEER — 2026-04-18*
