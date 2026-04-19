# VA Weekend Checklist — Tenure Pipeline
**Goal:** Get pipeline fully up to speed before introducing new URLs from `faculty_url_suggestions.csv`

---

## ⚡ TONIGHT — Do These Two Things Before You Log Off

> Cell 0 flags are **already set correctly** — do NOT change them. Just commit and launch.

### 1. Commit everything in Cursor Source Control
- Stage all → paste this message → commit → push:
```
cleanup: remove current_documents symlink deps, fix broken notebook path + Cell 0 flags for overnight run
```

### 2. Launch both Slurm jobs from the terminal
```bash
cd ~/Ivy_Net
sbatch build_openalex_cache.slurm   # overnight cache builder — runs alone, no conflicts
sbatch pipe_job.slurm               # fills HTML gaps + rebuilds panel + runs analysis
```

### 3. Verify both jobs are queued
```bash
squeue -u dzk3ja
# Should see TWO jobs listed
```

### 4. Log off — both jobs run unattended overnight

**What runs tonight in pipe_job:**
- Cell 3 Download → fills 553 missing HTML files
- Cell 3 Retry → retries any CDX failures (CDX discovery is OFF — quota protected)
- Cell 4 → re-parses all HTML
- Cell 5 → rebuilds longitudinal panel
- Cell 7 → enriched annual panel (GAP_TOLERANCE = 4)
- Cell 8 → LOO peer pool metrics
- Cell 9 → inverted-U plot

**What does NOT run (intentional):**
- Cell 6A — author ID resolution (not needed yet)
- Cell 6B — OpenAlex works fetch — OFF to avoid conflict with cache builder writing same file

---

## ☀️ TOMORROW MORNING — Check Results

### Check jobs finished
```bash
squeue -u dzk3ja         # should be empty if both finished
ls -lh ~/Ivy_Net/slurm-*.out   # check log files exist
tail -50 slurm-pipe_job-*.out  # read pipe_job summary
tail -20 slurm-build_openalex_cache-*.out  # read cache builder summary
```

### If pipe_job finished — check the output
Look for in the log:
- `Panel rows` count (should be > previous run)
- `Unique faculty` count
- Stage 9 inverted-U plot saved
- No ERROR lines

### If cache builder finished — run Cell 6B
```bash
# In the notebook Cell 0, change:
#   RUN_CELL6B = False  →  RUN_CELL6B = True
#   (all other flags: set to False except 6B)
cd ~/Ivy_Net && sbatch pipe_job.slurm
```

---

## 📋 NEXT STEPS (After overnight jobs) — In Order

### Phase 3 — Expand Pilot to Top-40 Schools

**Step A — Resolve author IDs for schools 21–40 (Cell 6A)**
- [ ] In Cell 0: set `STAGE6_PILOT_TOP_N = 40`
- [ ] Set `RUN_CELL6A = True`, all others `False`
- [ ] `sbatch pipe_job.slurm`
- [ ] Confirm: author ID count grows from 15,519

**Step B — Fetch works by year for new authors (Cell 6B)**
- [ ] In Cell 0: set `RUN_CELL6B = True`, all others `False`
- [ ] `sbatch pipe_job.slurm`
- [ ] Confirm: works file grows; snapshot cache used where available

**Step C — Re-run full analysis**
- [ ] In Cell 0: set `RUN_CELL7 = True`, `RUN_CELL8 = True`, `RUN_CELL9 = True`, all others `False`
- [ ] `sbatch pipe_job.slurm`
- [ ] Compare Stage 9 inverted-U plot to previous run

---

### Phase 4 — Review URL Suggestions (Mac Local)

*Do this AFTER Phase 3 is complete and results look stable.*

**Step D — rsync results back to Mac**
```bash
# From your Mac terminal:
./scripts/rsync_pull_from_hpc.sh
```

**Step E — Review suggestions CSV**
- [ ] Open: `tenure/tenure_pipeline/faculty_url_suggestions.csv`
- [ ] Sort by `mean_recs` ascending (worst schools first)
- [ ] For each school: check `suggested_url` — does it look like a **CS faculty page**?
- [ ] **Red flags:** generic university staff directories, aging/CTE/HR pages
- [ ] **Green flags:** subdomain has `cs`, `eecs`, `cse`, `computing`; path has `faculty`, `people`
- [ ] Promising leads:
  - Rice University (score 97, 2000–2024) — `rice.edu/Computer/facultystaff.html`
  - Kent State (score 84, 2019–2025) — `kent.edu/cs/faculty-staff-directory`
  - Lehigh (score 83, 2014–2026) — `lehigh.edu/academics/faculty`
  - Northwestern (score 83, 2012–2024) — check if it's the CS directory

**Step F — Add good URLs to the pipeline**
```bash
# Edit tenure/tenure_pipeline/r1_cs_departments.csv
# Then re-run: Cell 2 → Cell 3A → Cell 3B → Cell 4 → Cell 5
```

---

## Git Sync Rule — After Every sbatch + Results Look Good

```bash
cd ~/Ivy_Net
git add -A
git status        # verify: no *.jsonl, no *.html, no slurm-*.out staged
git commit -m "Weekend run: <brief description>"
git push
```

---

## Quick Reference — Key Commands

```bash
# Check queue
squeue -u dzk3ja

# Monitor a job live
tail -f slurm-<JOBNAME>-<JOBID>.out

# Submit jobs
cd ~/Ivy_Net && sbatch pipe_job.slurm
cd ~/Ivy_Net && sbatch build_openalex_cache.slurm

# Pull data to Mac (run from Mac terminal)
./scripts/rsync_pull_from_hpc.sh

# Push code to Rivanna (run from Mac terminal)
./scripts/rsync_push_to_hpc.sh
```

---

## Workspace Notes

| Workspace | When to Use |
|-----------|------------|
| `Rivanna.code-workspace` | Slurm jobs, HPC data, remote debugging |
| `Ivy_Net.code-workspace` | Code edits, git, rsync, local runs |

Explorer shows 3 roots: `Ivy_Net`, `tenure`, `sports` — notebooks are directly visible, no symlinks.

---

*Last updated: 2026-04-15 — overnight run plan + for-dummies rewrite*
