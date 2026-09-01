# COMPASS → PEER — tenure dataset bolstering (scrape + adjudicate)

**Last synced:** 2026-09-01

**Audience:** Charles + PEER (working session). COMPASS planning handoff — not for Alex yet.

**Standalone:** Alex wants HERO / F-HERO-style metrics on tenure soon; the panel is not robust enough yet. This doc is the ordered checklist to expand scrape coverage before any tenure hero work.

**Deep reference:** [`tenure/documents/TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md`](../../tenure/documents/TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md) · [`scripts/DATA_SYNC.md`](../../scripts/DATA_SYNC.md)

---

## YOU ARE HERE

| Step | Task | Owner | Status |
|------|------|-------|--------|
| **0** | Mac/Rivanna/git synced (`0d1802a`) | Charles | ✓ |
| **1** | Pull latest tenure outputs to Mac | Charles | → **NEXT** |
| **2** | Review audit + pick expansion lane(s) A–E | Charles + PEER | Pending |
| **3** | Adjudicate URLs / add schools (Phase 1) | Charles + PEER | Pending |
| **4** | Commit worksheet changes + push/rsync to Rivanna | Charles | Pending |
| **5** | Run scrape chain (Cells 2–4) on Rivanna | PEER or Charles | Pending |
| **6** | Morning check + rsync pull to Mac | Charles | Pending |
| **7** | Rebuild panel (Cells 5–9) if scrape healthy | PEER or Charles | Pending |
| **8** | Lock tenure HERO spec with Alex | Charles + Alex | After 7 |

**Alex one-liner (context only):** Explore hero / F-HERO on tenure — **after** the faculty panel is worth plotting.

---

## Why now (30 seconds)

MBB Wang-arc work is in good shape on the sports side (empirical HERO/F-HERO, reigning-hero calibration, sim replay on 2009–21). The **next domain** is tenure. The pipeline code exists; the **corpus** (HTML coverage, URL quality, panel rows) needs a deliberate expansion round before hero metrics mean anything.

Reading docs does **not** add HTML. New data = **Phase 1 (Mac inputs) + Phase 2 (Rivanna Wayback run)**.

---

## The two-phase loop (memorize this)

```
Phase 1 — Mac: edit school list / URL worksheet → apply → git push + rsync push
Phase 2 — Rivanna: 540_tenure_pipeline.ipynb Cell 0 → sbatch pipe_job.slurm
```

After Phase 2: **rsync pull tenure** to Mac so Cursor sees new JSONL/logs.

---

## Expansion lanes — pick with PEER

| Lane | You want… | Mac edit | Rivanna flags (minimum) |
|------|-----------|----------|-------------------------|
| **A** | New R1 CS schools | `r1_cs_departments.csv`, `r1_schools_data.py` | CELL2, 3A CDX, 3B download, 4 |
| **B** | Better URL for weak school | `url_update_worksheet.csv` → `apply_url_updates.py` | Same as A |
| **C** | URLs never CDX-queried | Often none | 3A CDX (+ download, 4) |
| **D** | CDX done, HTML missing | None | **3A CDX=False**, download, 4 |
| **E** | Prior CDX timeouts | None | 3 retry + download, 4 |

**Most common today:** **B** (fix weak parsers) and/or **A** (grow toward full R1 list).

Optional URL leads:

```bash
python tenure/tenure_pipeline/discover_faculty_urls.py
# → faculty_url_suggestions.csv → paste into new_url → apply_url_updates.py
```

---

## Itemized checklist

### Before the PEER session (Charles — ~30 min)

- [ ] **1.** From repo root on Mac:
  ```bash
  ./scripts/rsync_pull_recent_hpc.sh tenure
  ```
- [ ] **2.** Open and skim (share screen with PEER):
  - `tenure/tenure_pipeline/faculty_snapshots_strategy_audit.jsonl`
  - `tenure/tenure_pipeline/url_update_worksheet.csv`
  - `faculty_url_suggestions.csv` (if present after pull)
- [ ] **3.** Have [`TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md`](../../tenure/documents/TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md) open — PEER does not need the 900-line overview.

### During the PEER session — decide together

- [ ] **4.** **Scope:** How many schools this round? (fix worst parsers only vs add N new departments)
- [ ] **5.** **Lane(s):** Mark A / B / C / D / E from table above
- [ ] **6.** **Split labor:**
  - Who edits `new_url` rows?
  - Who adds new schools to CSV?
  - Who submits Slurm on Rivanna?
- [ ] **7.** **Quality bar:** What counts as “good enough” to run panel rebuild? (e.g. audit red schools cleared, min HTML count per school)
- [ ] **8.** **OpenAlex this round?** Cell 6A/6B now, or scrape/HTML first and OA later?

### Mac — Phase 1 (after decisions)

- [ ] **9.** Edit worksheets / school list per lane A or B
- [ ] **10.** If URLs changed:
  ```bash
  python tenure/tenure_pipeline/apply_url_updates.py
  ```
- [ ] **11.** Stage + commit worksheet/school-list changes (small, focused commit)
- [ ] **12.** Push to GitHub + push code to Rivanna:
  ```bash
  git push origin main
  ./scripts/rsync_push_to_hpc.sh
  ```

### Rivanna — Phase 2 (PEER or Charles)

- [ ] **13.** Confirm clone current:
  ```bash
  cd ~/Ivy_Net && git pull origin main
  ```
- [ ] **14.** Open `tenure/540_tenure_pipeline.ipynb` — Cell 0 for **new scrape minimum:**
  - `RUN_CELL2`, `RUN_CELL3_CDX`, `RUN_CELL3_DOWNLOAD`, `RUN_CELL4` = **True**
  - All other `RUN_CELL*` = **False** (unless step 8 said otherwise)
- [ ] **15.** Submit:
  ```bash
  cd ~/Ivy_Net && sbatch pipe_job.slurm
  squeue -u dzk3ja
  ```
- [ ] **16.** Next morning — read log:
  ```bash
  tail -80 ~/Ivy_Net/slurm_out/slurm-pipe_job-*.out
  ```
  Look for: ERROR lines, download counts, parse summary

### After a healthy scrape — Phase 3

- [ ] **17.** Mac pull:
  ```bash
  ./scripts/rsync_pull_recent_hpc.sh tenure
  ```
- [ ] **18.** **Workflow E** (panel + LOO metrics + plots) — Cell 0:
  - Cell 5 → `faculty_panel.jsonl`
  - Cells 7–9 → enriched panel, pools, inverted-U plot
- [ ] **19.** Sanity before Alex / tenure HERO:
  - Panel row count ↑ vs last run?
  - Weak schools improved in audit?
  - Ready to lock **Y**, **Â**, LOO pool definition (separate Alex memo — not this doc)

---

## Who owns what (default split)

| Piece | Mac | Rivanna |
|-------|-----|---------|
| URL research + worksheet | Charles + PEER | — |
| `apply_url_updates.py`, git commit | Charles | — |
| Wayback CDX / download / parse | — | PEER or Charles |
| Slurm submit / log triage | — | PEER or Charles |
| rsync pull for Cursor | Charles | — |
| Panel rebuild (Cells 5–9) | trigger from either | runs on HPC |

**Git** = code + small CSVs. **rsync** = JSONL, HTML tree, slurm logs. See [`DATA_SYNC.md`](../../scripts/DATA_SYNC.md).

---

## Success criteria (this round)

1. Chosen expansion lane(s) executed without Slurm hard failure
2. Audit shows material improvement for targeted weak schools **or** new schools have first HTML + parse rows
3. Mac has fresh `tenure/tenure_pipeline/` outputs via rsync
4. Charles can answer: “How many person-years in panel? How many schools at min coverage?”

---

## After bolstering — what COMPASS needs from Charles + Alex

Not for PEER session. After step 19, open a short **tenure HERO lock** with Alex:

1. Outcome **Y** (tenure granted? promotion event?)
2. Panel aperture (years, schools, activity filters)
3. **Â** field(s) for talent / F-HERO slices
4. LOO pool definition for tenure HERO
5. Empirical-only first vs generative replay (MBB template)

COMPASS turns that into scripts and sandbox paths.

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-01 | COMPASS draft after Mac git recovery; Alex tenure HERO interest; PEER scrape round queued. MBB at `0d1802a`; Rivanna pulled same. |
