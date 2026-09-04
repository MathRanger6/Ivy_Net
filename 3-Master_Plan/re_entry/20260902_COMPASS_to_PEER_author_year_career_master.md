# COMPASS → PEER — author×year career master table (PD29 / Alex lock)

**Last synced:** 2026-09-02

**Audience:** Charles → PEER (Rivanna). **Context:** Paper Directions 29 — Alex locked cumulative career pubs rate for tenure HERO; Mac needs a precomputed spine to rsync.

**Related:** [`transcripts/PD29_notes.md`](../../transcripts/PD29_notes.md) · [`TENURE_hero_pipeline.md` § PD29 delta](../re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_hero_pipeline.md#pd29-delta-sep-2-2026--alex-locks-vs-v0)

---

## One sentence

Build a **flat author×calendar-year table** (pubs + running cumulative + career-length rate) from existing OpenAlex works, so Mac (or Rivanna) can slice decision-year tenure analysis.

**Mac-first (2026-09-02):** `python tenure/tenure_pipeline/build_author_year_career_master.py` — ~2s, no snapshot. Rivanna Slurm optional for re-run after OA cache refresh.

---

## Why (30 seconds)

Alex (Sep 2): tenure decision ≈ **year 6 up-or-out**; own performance = **cumulative pubs ÷ (focus_year − first_pub_year)**; career start = **first publication year** (OpenAlex). Mac should not recompute this from scratch every HERO run — one master table, then filter.

**Inputs already on Rivanna** (per May 2026 handoff):

| File | Role |
|------|------|
| `tenure/tenure_pipeline/openalex_author_ids.jsonl` | Author universe + `faculty_id` + match tier |
| `tenure/tenure_pipeline/openalex_works_by_year.jsonl` | `{faculty_id, openalex_id, uni_slug, year, n_works}` per line |

**Do not** re-run full HTML scrape or `build_openalex_cache.slurm` unless works file is missing/stale.

---

## Deliverable

**Primary output (pick one; prefer JSONL for consistency):**

`tenure/tenure_pipeline/author_year_career_master.jsonl`

**One row per** `(openalex_id, year)` where `n_works > 0` **OR** year is on the author’s career span through `max_year` in works (see schema).

**Optional companion:** `author_year_career_master_meta.json` (row counts, build timestamp, source file mtimes).

### Schema (required columns)

| Column | Type | Definition |
|--------|------|------------|
| `openalex_id` | str | OpenAlex author ID |
| `faculty_id` | str | From author_ids join (empty if unmatched) |
| `match_confidence` | str | HIGH / MEDIUM / … from author_ids |
| `year` | int | Calendar year |
| `n_works` | int | Publications that year (= `n_works` in works file; 0 allowed on padded years if you emit full span) |
| `cum_works` | int | Running sum of `n_works` through `year` (inclusive) |
| `first_pub_year` | int | min(year) with n_works > 0 for this author |
| `career_age_years` | int | `year - first_pub_year` (0 in first pub year) |
| `pubs_per_career_year` | float | `cum_works / career_age_years` when `career_age_years > 0`, else null |

**Alex denominator check:** first pub year 0, decision year 10, 100 cum pubs → rate **10.0** (= 100 / (10−0), not ÷11).

### Universe

- **All authors** appearing in `openalex_author_ids.jsonl` with `match_confidence` ∈ **{HIGH, MEDIUM}** (configurable env `CONFIDENCE_MIN`, default HIGH).
- Join works from `openalex_works_by_year.jsonl`; authors with ID but no works → omit or emit metadata-only line in meta JSON (PEER pick — document in meta).

---

## Suggested implementation

1. **New script** (Mac can push via git before run):  
   `tenure/tenure_pipeline/build_author_year_career_master.py`  
   - Read-only on existing JSONL  
   - Incremental write + flush per author (see project incremental-write rule)  
   - Resume: skip authors already in output if re-run

2. **New Slurm wrapper** (mirror `build_openalex_cache.slurm`):  
   `build_author_year_career_master.slurm` at repo root  
   - `--mem=16G`, `--time=02:00:00`, `tenure_net` env  
   - Lightweight vs OA snapshot scan

3. **Submit:**
   ```bash
   cd ~/Ivy_Net && git pull origin main
   sbatch build_author_year_career_master.slurm
   tail -f slurm_out/slurm-build_author_year_career_master-*.out
   ```

4. **Charles pulls:**
   ```bash
   ./scripts/rsync_pull_recent_hpc.sh tenure
   ```

---

## Preflight (PEER)

- [ ] `openalex_works_by_year.jsonl` exists and mtime ≥ last panel build
- [ ] Line count sanity: `wc -l openalex_works_by_year.jsonl openalex_author_ids.jsonl`
- [ ] If works stale vs new author IDs → run `sbatch build_openalex_cache.slurm` **first**, then career master

---

## Success criteria

1. `author_year_career_master.jsonl` on Rivanna under `tenure/tenure_pipeline/`
2. Meta documents: N authors, N author-year rows, year range, tier filter
3. Spot check: pick one known faculty_id — `first_pub_year`, `cum_works` monotonic, rate at last year matches hand calc
4. Charles rsync pull succeeds; file visible on Mac for COMPASS slice (decision-year cohort = **next** step, not this job)

---

## Out of scope (this job)

- Decision-year flags / tenure outcome (Mac + `faculty_panel_with_pools.jsonl`)
- Department pond LOO at decision year
- Re-scrape / URL worksheet / Cell 2–4

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-02 | COMPASS draft after PD29; Charles to send PEER; build script TBD on git push. |
