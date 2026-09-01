# PEER → COMPASS — Tenure hero on Mac (handoff)

**Last synced:** 2026-09-01

**Audience:** COMPASS + Charles (analysis on Mac). PEER owns Rivanna scrape bolster when scheduled.

**Standalone:** Mac is synced with Rivanna; exploratory HERO/F-HERO uses `faculty_panel_with_pools.jsonl` locally — no HPC join required for v0.

**Charles checklist doc (scrape bolster, later):** [`20260901_COMPASS_to_PEER_tenure_scrape_bolster.md`](20260901_COMPASS_to_PEER_tenure_scrape_bolster.md) — parallel track, not blocking hero sandbox.

---

## YOU ARE HERE

| Step | Task | Status |
|------|------|--------|
| **0** | Rsync tenure pipeline to Mac | ✓ 2026-09-01 |
| **1** | Lock exploratory panel + columns | ✓ `with_pools` |
| **2** | Write tenure ↔ MBB hero pipeline map (COMPASS) | ✓ |
| **3** | Exploratory HERO (+ F-HERO?) on Mac | Pending |
| **4** | Alex lock: Y, Â, aperture, generative or not | Pending |
| **5** | PEER scrape bolster (parallel, when scheduled) | Parked |

---

## Sync status (2026-09-01)

Charles ran `./scripts/rsync_pull_recent_hpc.sh tenure`. Panel spine **same bytes/mtimes** on HPC and Mac — **current**, not stale. **No Rivanna re-run** for date hygiene.

---

## Canonical artifacts (Cells 7–9 executed)

| Artifact | Cell | Stamp | Size | Rows |
|----------|------|-------|------|------|
| `faculty_panel_enriched.jsonl` | 7 | 2026-05-04 | ~55 MB | 106,559 person–years |
| `faculty_panel_with_pools.jsonl` | 8 | 2026-05-04 | ~72 MB | 106,559 person–years |
| `stage9_inverted_u.png`, `stage9_binned_table.csv` | 9 | 2026-04-19 | small | 18 bins |

**Primary spine for HERO/F-HERO:** `tenure/tenure_pipeline/faculty_panel_with_pools.jsonl`

- Grain: **person–year** (~106.6K) — **not** `faculty_panel.jsonl` (2.56M snapshot rows).
- Key columns: `tenure_event`, `attrition`, `censored`, `pubs_year`, `pubs_cumulative`, `openalex_id`, `match_confidence`, `poolq_loo_mean`, `pool_rank_loo`, `pool_pctile_loo`, `pool_size_oa_loo`, …

Also useful:

| File | Role |
|------|------|
| `R1_tenure_data.csv` (~21 MB) | Flat 543-style export; same grain |
| `faculty_panel_inference_v1.csv` + manifest | Locked inference slice — not full exploratory universe |

---

## OpenAlex

Already joined in Cell 7 build. Rsync’d JSONL on Mac: `openalex_author_ids.jsonl`, `openalex_works_by_year.jsonl`, `openalex_low_confidence.jsonl`. **No extra HPC join** for Mac hero exploration on this corpus.

Re-run 6A→6B→7→8→9 only after **material scrape expansion** or author-resolution change.

---

## Rsync

```bash
./scripts/rsync_pull_recent_hpc.sh tenure
```

**Sufficient** for hero work. Excludes by design: `faculty_snapshots/` HTML, `dblp_parsed/`, IPEDS caches.

**Must stay on Rivanna:** HTML archive, CDX/download, `build_openalex_cache.slurm`, full DBLP parse.

---

## Match quality & inference slice (caveats)

OpenAlex tiers on 106,559 person–years (manifest):

| Tier | Person–years |
|------|----------------|
| NONE | 62,099 |
| HIGH | 18,332 |
| MEDIUM | 10,531 |
| MULTI | 13,647 |
| LOW | 1,950 |

Strict inference sample (HIGH/MEDIUM + non-null `poolq_loo_mean`): **796 persons, 52 departments, 2,396 assistant person–years** — for locked prose, not “full roster hero coverage.”

**Bake in:**

- Coverage quality ≠ timestamp; scrape bolster is round 2 before publication-ready heroes.
- Stage 9 = exploratory inverted-U sanity check (Apr 2026), not tenure HERO deliverable.
- Alex lock still pending: Y, aperture, Â for F-HERO, LOO definition, empirical vs generative replay.

---

## Work split

| Track | Where | Who |
|-------|-------|-----|
| Hero sandbox | Mac | Charles + COMPASS |
| Scrape bolster | Rivanna | PEER (when scheduled) |

**Bottom line:** Analyze `faculty_panel_with_pools.jsonl` locally; MBB analogue = `sports_sandbox/`.

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-01 | PEER handoff ingested after rsync; Mac = Rivanna for panel spine. |
