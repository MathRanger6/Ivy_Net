# PEER → VECTOR — Research history handoff

**Agent:** PEER (Cursor agent; R1 CS faculty tenure / Wayback scrape / OpenAlex / panel / survival analysis)  
**Date:** 2026-09-22  
**Prepared for:** VECTOR (ChatGPT Work research partner with direct repo access)  
**Prepared by:** PEER from repository documents, implementation artifacts, SpecStory sessions, and agent context — **not** by re-running code.

**How to use this file:** An annotated map and history guide. Read cited paths in the repo for primary evidence. This document does **not** replace `tenure/documents/TENURE_PIPELINE_OVERVIEW.md` (~900 lines of cell-level wiring).

**Obsolete assumption:** The package under `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/` was built when VECTOR lacked repo access. VECTOR can now open originals at the paths below.

---

## 1. My role and our working relationship

### What PEER is

PEER is Charles’s Cursor agent for **Setting 3 — academia / R1 CS faculty tenure** in the Ivy_Net dissertation. Domain root: **`tenure/`**; canonical data and code: **`tenure/tenure_pipeline/`**. Conductor notebook: **`tenure/540_tenure_pipeline.ipynb`** (Cell 0 = flags and paths).

**Source:** `3-Master_Plan/obsolete/pre_tier1_locks/PEER_report_to_COMPASS.md` §0–§1; `AGENTS.md` (repo root).

### PEER responsibilities (in scope)

| Area | PEER owns |
|------|-----------|
| Wayback CDX planning, HTML download, parse rescues (Cells 3A–3E) | Implementation, ops docs, URL adjudication loop |
| HTML parsing, longitudinal panel (Cells 4–5) | `html_parser.py`, `faculty_linker.py`, panel JSONL |
| OpenAlex institution map, author resolution, works-by-year (Cells 6A–6B) | `openalex_resolver.py`, `build_openalex_cache.py`, Rivanna CDH bulk |
| Enriched panel, LOO pool metrics, Stage 9 binned check (Cells 7–9) | `panel_builder.py`, `pool_metrics.py`, `stage9_analysis.py` |
| HPC / Mac sync for tenure data | `scripts/rsync_*`, `tenure/documents/HPC_SETUP_CHECKLIST.md` |
| Advisor-facing feasibility memos and pipeline truth for tenure **data** | e.g. `tenure/documents/20260720_Preliminary_Pipeline_Feasibility_Memo_for_Alex_Gates.md` |
| Alex handoff bundle (code + samples, not multi-GB data) | `tenure/alex_tenure_handoff/` |

### PEER boundaries (out of scope)

| Area | Owner | PEER relationship |
|------|-------|-------------------|
| Cross-project sequencing, hero campaign framing, MBB mirror docs | **COMPASS** | PEER supplies data truth; COMPASS writes `3-Master_Plan/re_entry/` campaign plans |
| NCAA men’s basketball empirical + sim | **SCOUT** | Parallel Setting 2; shared inverted-U thesis only |
| Army OER / promotion / competing risks | **CODA** | Setting 1; Army Cox pattern is **template** for planned tenure Layer B |
| Manuscript prose, Dakota brief wording, defense narrative | **VECTOR** + Charles | PEER provided `5-Manuscript/obsolete/superseded_status_updates/PEER_Status_Update_for_VECTOR_2026-06-03.md`; VECTOR does not implement scrape |
| Tenure **HERO/F-HERO plotting scripts** on Mac (Sep 2026) | **COMPASS + Charles** | Uses PEER panel outputs; see `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/` |
| Grandchild / ρ / H_sort diagnostics across domains | **COMPASS + SCOUT** | PD41 (2026-09-22) assortativity screen includes tenure H_sort ~0.121 — not PEER’s primary build target |

### Working style with Charles

- **Document-first:** strategic intent in `tenure/documents/TENURE_DATA_GAMEPLAN.md`; wiring in `TENURE_PIPELINE_OVERVIEW.md`.
- **Checkpointed pipeline:** heavy stages write JSONL/HTML; Cell 0 `RUN_CELL*` flags skip completed work.
- **Human loops:** URL fixes via `url_update_worksheet.csv` → `apply_url_updates.py` → `r1_schools_data.py`.
- **Rivanna for scrape/download; Mac for analysis** after rsync (confirmed Sep 2026). See `tenure/documents/TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md`.
- **SpecStory:** PEER sessions archived under `.specstory/history/*peer*.md` (Apr 2026 primary archive). Live Cursor threads are **not** automatically portable Mac ↔ Rivanna; files in git are the durable bridge.

---

## 2. Chronological research history

*Non-linear by design — several priority reversals are documented below.*

### Phase A — Pipeline construction (approx. 2025–Apr 2026)

**Goal:** Build scrape → parse → panel machinery for R1 CS faculty via Internet Archive.

- **Cells 0–5:** DBLP spine (Cell 1), school roster expansion toward **168** departments (`r1_schools_data.py`), CDX plan + HTML download + multi-strategy parse, snapshot-level longitudinal panel.
- **Option B on disk:** `faculty_snapshots/<uni_slug>/<source_id>/<year>_<season>_<timestamp>.html` — documented in gameplan and overview.
- **Pilot rescues:** Sub-page rescues for Cornell, UMD, UIUC, UW–Madison; redirect rescue for NC State (Cells 3C–3E) — often one-off school fixes, not re-run every batch.

**Evidence:** `tenure/documents/TENURE_PIPELINE_OVERVIEW.md` §3–§7; `tenure/documents/TENURE_DATA_GAMEPLAN.md` §G8–G10.

**SpecStory:** `.specstory/history/2026-04-02_17-36-36-0400-peer.md`, `.specstory/history/2026-04-03_13-55-35-0400-peer.md` — Stage 6 pilot, HPC/SpecStory setup, path fixes, git/rsync policy.

### Phase B — Alex direction shift (Apr 9–10, 2026)

**Change:** De-prioritize “scrape more schools every week”; prioritize **end-to-end measurement** on existing corpus — assistant→associate transitions, attrition, peer pools, inverted-U plausibility.

**Source:** `tenure/documents/TENURE_DATA_GAMEPLAN.md` §G6 (Advisor direction — 2026-04-09); Otter PDF cited there: `2-Way_Ahead/20260410_Paper_directions_4_otter_ai.pdf` *(path in gameplan — VECTOR should verify file exists before citing in prose)*.

**PEER response:** Shift engineering effort toward OpenAlex linkage, enriched panel, pool metrics, Stage 9 — not roster breadth.

### Phase C — OpenAlex at scale + Stage 6 pilot (Apr 2026)

- **`build_openalex_cache.py`** + **`openalex_snapshot_cache.jsonl`** for UVA CDH bulk on Rivanna; Mac uses rsync’d cache.
- **Stage 6A pilot:** coverage-ordered schools, sanity filter dropping schools with broken HTML (`stage6_pilot.py`) — avoid API spend on junk inputs.

**Evidence:** Overview §4; SpecStory 2026-04-02 session (Stage 6A pilot commit `afc7b89` referenced in chat).

### Phase D — Cells 7–9 complete (May 2026)

- **Cell 7:** `faculty_panel_enriched.jsonl` — annual person–year grain; pubs + tenure/attrition/censoring.
- **Cell 8:** `faculty_panel_with_pools.jsonl` — LOO peer pool metrics (`poolq_loo_mean`, etc.).
- **Cell 9:** Binned inverted-U check → `stage9_inverted_u.png`, `stage9_binned_table.csv`.

**Artifact stamps (Mac after rsync, verified PEER read 2026-09-01):** enriched and with_pools **2026-05-04**; stage9 **2026-04-19**.

**Evidence:** `tenure/documents/TENURE_PIPELINE_OVERVIEW.md` rev 19–20 history (2026-06-11); gameplan §G11–G12 marked fast path complete.

### Phase E — COMPASS / VECTOR reporting (Jun 2026)

- **`PEER_report_to_COMPASS.md`** (June 8): full Setting 3 narrative for planning agent.
- **`PEER_Status_Update_for_VECTOR_2026-06-03.md`:** preliminary inverted-U, OpenAlex quality table, “Layer B Cox planned.”
- **Tier-1 locks + inference export (Jun 24):** `faculty_panel_inference_v1.csv` + manifest — HIGH/MEDIUM only, **796 persons / 52 departments / 2,396 assistant person–years**.

**Evidence:** `3-Master_Plan/obsolete/pre_tier1_locks/PEER_report_to_COMPASS.md`; `3-Master_Plan/obsolete/original_filenames/20260624_PEER_inference_export_complete.md`; manifest at `tenure/tenure_pipeline/faculty_panel_inference_v1_manifest.json`.

### Phase F — Alex feasibility memo (Jul 20, 2026)

External-facing summary of pipeline stage stats, department–year coverage proxy (~650 DYs at internal 98% stability), person-year counts.

**Evidence:** `tenure/documents/20260720_Preliminary_Pipeline_Feasibility_Memo_for_Alex_Gates.md`.

### Phase G — Alex Gates handoff package (Jul 2026)

Lean zip for Alex: code, docs, examples — **not** multi-GB Rivanna HTML. Rivanna paths documented separately.

**Evidence:** `tenure/alex_tenure_handoff/README_HANDOFF.md` *(PEER contributed to packaging per prior agent session; transcript `6447dea8-1461-4fd5-8167-b9e4c78e10c3` — not fully re-read for this handoff)*.

### Phase H — Tenure HERO campaign + PD29 locks (Sep 2026)

**Shift:** COMPASS leads Mac hero exploration on existing panel; PEER parallel on scrape bolster when scheduled.

- **2026-09-01:** Mac/Rivanna sync confirmed; `TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md` created; COMPASS↔PEER handoffs on hero vs scrape.
- **PD29 (Sep 2):** Alex locks decision-year cohort, career pubs rate, whole-dept pond — **differs from v0 person–year HERO grain**.
- **Engineering:** `build_author_year_career_master.py` → `author_year_career_master.jsonl` (Sep 2); COMPASS/Charles hero artifacts under `tenure_sandbox/hero/`.

**Evidence:** `transcripts/PD29_notes.md`; `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_hero_pipeline.md` § PD29 delta; `3-Master_Plan/re_entry/20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md`.

### Phase I — PD41 context (Sep 22, 2026)

**Not PEER-led:** Alex reframes week priority to **assortativity (H_sort) blocker** + one-day education probe + narrative restructure. Tenure remains in **primary trio** (Army · MBB · Tenure) with H_sort ~0.121 discussed.

**PEER relevance:** Data corpus unchanged; hero/scrape sequencing subordinate to COMPASS PD41 stack unless Charles reprioritizes scrape bolster.

**Evidence:** `transcripts/PD41_notes.md`.

---

## 3. Work actually completed

*“Completed” = artifact exists in repo or on disk via rsync — not independent statistical validation.*

### Pipeline implementation (Cells 0–9 in `540`)

| Stage | Status | Key artifacts |
|-------|--------|---------------|
| 0–2 | ✅ | `tenure/540_tenure_pipeline.ipynb` Cell 0; `r1_schools_data.py`; `r1_cs_departments.csv` (168 schools) |
| 3A–3E | ✅ operational | `faculty_snapshots_plan.jsonl`, HTML under `faculty_snapshots/` (HPC-primary), rescues documented |
| 4 | ✅ | `faculty_snapshots_parsed.jsonl`, `faculty_snapshots_strategy_audit.jsonl` |
| 5 | ✅ | `faculty_panel.jsonl` (~2.56M snapshot-level rows — **wrong grain for HERO**) |
| 6A–6B | ✅ | `openalex_author_ids.jsonl`, `openalex_works_by_year.jsonl`, `openalex_snapshot_cache.jsonl`, `build_openalex_cache.py` |
| 7–8 | ✅ | `faculty_panel_enriched.jsonl`, `faculty_panel_with_pools.jsonl` (106,559 person–years each) |
| 9 | ✅ | `stage9_inverted_u.png`, `stage9_binned_table.csv` (18 bins) |
| 543 | ✅ | `R1_tenure_data.csv`, advisor export path via `543_package_panel.ipynb` |
| 10–12 Layer B Cox | 📋 **Not in `540`** | Planned port from Army `520` — see overview §4 |

**Source:** `tenure/documents/TENURE_PIPELINE_OVERVIEW.md` §2 table; `tenure/documents/TENURE_DATA_GAMEPLAN.md` §Stage map.

### Python modules (representative)

| Module | Role |
|--------|------|
| `tenure/tenure_pipeline/html_parser.py` | Multi-strategy parse competition |
| `tenure/tenure_pipeline/apply_url_updates.py` | URL worksheet → school list |
| `tenure/tenure_pipeline/discover_faculty_urls.py` | Automated URL suggestions for weak schools |
| `tenure/tenure_pipeline/panel_builder.py` | Cell 7 enriched panel |
| `tenure/tenure_pipeline/pool_metrics.py` | Cell 8 LOO pools |
| `tenure/tenure_pipeline/stage9_analysis.py` | Cell 9 binned inverted-U |
| `tenure/tenure_pipeline/build_faculty_panel_inference_v1.py` | Inference slice export |
| `tenure/tenure_pipeline/build_author_year_career_master.py` | PD29 career master table |

### Operations / documentation

| Deliverable | Path |
|-------------|------|
| Scrape re-entry guide | `tenure/documents/TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md` |
| HPC + rsync | `tenure/documents/HPC_SETUP_CHECKLIST.md`, `scripts/DATA_SYNC.md` |
| Slurm batch | `pipe_job.slurm` (repo root), `tenure/HPC_SLURM_PIPELINE_GUIDE.md` |
| URL discovery guide | `tenure/documents/DISCOVER_FACULTY_URLS_GUIDE.md` |

### Empirical artifacts (descriptive — not causal claims)

| Finding | Artifact | PEER verification |
|---------|----------|-------------------|
| Preliminary inverted-U in LOO bins | `stage9_binned_table.csv`, `stage9_inverted_u.png` | File exists; bin 18 drop documented in `PEER_Status_Update_for_VECTOR_2026-06-03.md` §4 |
| Feasibility counts for Alex | `20260720_Preliminary_Pipeline_Feasibility_Memo_for_Alex_Gates.md` | Memo text; **not** re-validated Sep 2026 |
| Inference-ready subset | `faculty_panel_inference_v1.csv` + manifest | Manifest counts read by PEER 2026-09-22 |

### Work completed by others using PEER data (Sep 2026)

COMPASS/Charles built tenure HERO sandbox outputs **downstream** of PEER panel — PEER did not author all scripts:

| Artifact | Path | Owner |
|----------|------|-------|
| Decision-cohort HERO v0 | `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q10_decision_own_career_infHM_*` | COMPASS campaign (provenance JSON cites PEER inputs) |
| PD29 3×3 data story | `tenure_sandbox/data_story/TENURE_DATA_STORY_pd29_3x3.png` | COMPASS |
| Career master table | `tenure/tenure_pipeline/author_year_career_master.jsonl` (Sep 2) | Script in PEER tree; built per COMPASS→PEER spec |

**Provenance example:** `tenure_sandbox/hero/HERO_tenure_q10_decision_own_career_infHM_provenance.json` — n_cohort **391** resolved; **280** with career rate.

---

## 4. Proposed but unfinished work

| Item | Proposed in | Status |
|------|-------------|--------|
| **Layer B Cox survival** (Cells 10, 10.5, 12) | Gameplan §G11; PEER report §2.5 | Not wired in `540`; Army `520` port discussed |
| **Full R1 CS roster (~187 Carnegie)** | Gameplan §Outcomes coverage | 168 in `PILOT_SCHOOLS`; expansion deferred |
| **Scrape bolster round** (URL adjudication + Phase 2 Rivanna) | `20260901_COMPASS_to_PEER_tenure_scrape_bolster.md` | Checklist steps 2–7 pending as of doc |
| **OpenAlex re-run after scrape** | For-dummies doc Workflow E | Only needed after material corpus change |
| **Entity resolution / global name merge** | Gameplan human loops | v0 = within-school linking only |
| **Formal regression / Cox quotes for manuscript** | VECTOR status update Jun 2026 | Stage 9 binned only for Setting 3 |
| **PD29-aligned decision-year spine fully replacing v0** | PD29 notes; T5 handoff | Career master built; full T1–T4 slice campaign ongoing under COMPASS |
| **Act II F-HERO, Act III ρ, Act IV sim replay** | `TENURE_HERO_Campaign_Plan.md` | Pending Alex locks |
| **Alex handoff Rivanna data access for Alex** | `tenure/alex_tenure_handoff/RIVANNA_DATA_PATHS.md` | Options A–D; permissions TBD *(PEER has not verified Sep 2026)* |

**Do not treat as verified complete:** Any checklist “✅” in campaign docs without matching artifact mtime or manifest.

---

## 5. Negative results and abandoned approaches

| Approach | Outcome | Reason / evidence |
|----------|---------|-------------------|
| **Scrape-first as weekly priority** | Deprioritized Apr 2026 | Alex Apr 9 — gameplan §G6 |
| **Manual OpenAlex ID fixes for subsets** | Rejected as policy | Alex: bias unless rule applies everywhere — gameplan §G6 item 6 |
| **DBLP as primary pub source for panel** | Superseded by OpenAlex in Cell 7 | `panel_builder.py` docstring; Cell 1 DBLP remains spine artifact |
| **Bad faculty URLs** (homepage, HR, single bio) | Low parse counts | `Pertinent_Thoughts_Tenure.md`; UW–Madison `/people/pb` bug documented in overview |
| **`discover_faculty_urls.py` without parse audit** | N/A — script requires Cell 4 audit | `DISCOVER_FACULTY_URLS_GUIDE.md` prerequisites |
| **Auburn** | Poor/no Wayback coverage | `PEER_Status_Update_for_VECTOR_2026-06-03.md` §3 known problems |
| **NC State redirect shells** | Empty parses unless Cell 3E rescue | Overview Phase E |
| **High NONE OpenAlex rate** (~58% person–years in manifest) | Limits pub-based metrics | `faculty_panel_inference_v1_manifest.json` |
| **Lateral moves coded as attrition** | Known competing-risk limitation | Gameplan + PEER report §2.1 |
| **Self-contained browser handoff for VECTOR** | Obsolete Sep 2026 | Repo access per this assignment; `handoff_upload_no_repo/` historical |
| **Expecting Cursor chat portability Mac ↔ Rivanna** | Documented failure mode | `RIVANNA_CURSOR_REMOTE_SSH_FOR_DUMMIES.md` §6; Sep 2026 PEER↔Charles exchange *(agent context, not yet in SpecStory export)* |

---

## 6. Current state as of September 22, 2026

### Verified artifacts (PEER read filesystem / manifests)

| Artifact | Location | Notes |
|----------|----------|-------|
| Analysis spine | `tenure/tenure_pipeline/faculty_panel_with_pools.jsonl` | 106,559 rows; May 2026 stamp; synced Mac=Rivanna Sep 1 |
| Career master | `tenure/tenure_pipeline/author_year_career_master.jsonl` | Sep 2 2026; ~30 MB |
| Stage 9 | `stage9_inverted_u.png`, `stage9_binned_table.csv` | Apr 2026 |
| Inference slice | `faculty_panel_inference_v1.csv` + manifest | Jun 24 2026 |
| Roster | 168 departments in `r1_schools_data.py` | CSV synced May 2026 |

### Documented empirical findings (not independently re-estimated here)

- Stage 9: tenure rate rises mid-bins, peaks bins 16–17 (~0.67–0.70), drops bin 18 (~0.42) — `PEER_Status_Update_for_VECTOR_2026-06-03.md`.
- Jul 2026 memo: 2,331 ever-assistant; 422 tenure / 570 attrition / 1,339 censored at person level — memo §Pipeline performance.
- Sep 2026 HERO (decision cohort): n=391 resolved in provenance JSON — **different grain** from 106K person–years.

### Working hypotheses (not locked)

- Inverted-U in tenure vs LOO peer quality portable from Army/MBB — **exploratory** only.
- Mid-tier departments may show highest tenure rates; elite dept congestion — narrative aligned with dissertation frame; **not** causal identification in Setting 3.

### Proposed / in progress (Sep 2026)

| Track | Owner | State |
|-------|-------|-------|
| HERO Acts II–IV, PD29 spine | COMPASS + Charles | Act I exploratory figures exist |
| Scrape bolster | PEER + Charles when scheduled | Doc ready; not executed Sep 2026 |
| Assortativity blocker (PD41) | COMPASS | P0 over tenure scrape |

### Reported but not PEER-verified Sep 2026

- Rivanna `pipe_job` last run date — not inspected by PEER this session.
- Whether H_sort ~0.121 for tenure in PD41 used same pool definition as `pool_metrics.py` — **needs COMPASS/Charles confirmation**.
- Full `author_year_career_master` coverage vs OpenAlex NONE rate.

### Dependencies

- **Mac hero work:** rsync `tenure/tenure_pipeline/` — `./scripts/rsync_pull_recent_hpc.sh tenure`.
- **Scrape expansion:** Rivanna VPN + `540` Cell 0 + `sbatch pipe_job.slurm`.
- **OpenAlex bulk refresh:** Rivanna CDH + `build_openalex_cache.slurm`.
- **Manuscript Setting 3 prose:** VECTOR + Charles; PEER data memos as input.

---

## 7. Contradictions, uncertainty, and unresolved decisions

| Issue | Sources | Notes |
|-------|---------|-------|
| **Grain for tenure hero** | Stage 9 / inference v1 (person–year) vs PD29 (decision-year) vs provenance n=391 | **Not contradictory if labeled** — different questions; VECTOR must not merge without explicit filter |
| **168 schools “in panel” vs 52 in inference** | Manifest vs roster | 168 = construction roster; inference filter drops weak OA / poolq |
| **Bin 16–17 peak vs bin 18 drop vs PD41 “respectable” H_sort** | `stage9_binned_table.csv`; PD41 notes | Different statistics (binned tenure rate vs H_sort); both can be true |
| **Apr “don’t scrape more” vs Sep scrape bolster doc** | Gameplan §G6 vs `20260901_COMPASS_to_PEER_tenure_scrape_bolster.md` | Priority reversal when Alex interest in tenure HERO + corpus quality; **parallel tracks** not contradiction if hero uses existing panel first |
| **Layer B “planned” vs Jun memo “complete pipeline”** | Overview vs VECTOR update | End-to-end **Cells 0–9** complete; **Cox Layer B** not |
| **Person-year count in VECTOR update (~106K) vs memo 106,559** | Jun VECTOR doc | Consistent rounding |
| **OpenAlex HIGH ~32% (Jun VECTOR) vs manifest NONE 62,099/106,559 (~58%)** | Different denominators / rounding | Reconcile from manifest before quoting in manuscript |

### Requires Charles confirmation

1. Is scrape bolster still scheduled, or fully parked behind PD41 assortativity?
2. Is `faculty_panel_with_pools.jsonl` May 2026 build still the canonical spine for all Sep hero figures?
3. Alex handoff: did Rivanna data access get resolved for Alex Gates?
4. Should PEER re-run Cells 7–9 after any future scrape, or only Cells 2–4 first?

### Evidence needed to resolve

- Fresh Slurm log tail for last successful `pipe_job`.
- Side-by-side H_sort computation script path for tenure PD41 number vs `541_grandchild_homophily_assign.py` (if used for tenure).

---

## 8. Annotated repository reading list

*Priority order for VECTOR understanding PEER / Setting 3. Read originals — do not rely on this summary alone.*

### Tier 1 — Start here (current status + grain)

| Path | Purpose | Why important |
|------|---------|---------------|
| `3-Master_Plan/re_entry/20260901_PEER_to_COMPASS_tenure_hero_mac_handoff.md` | Mac/rsync + canonical artifacts | Sep 2026 sync truth; **`with_pools` spine** |
| `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_hero_pipeline.md` | MBB mirror + **PD29 delta** | Explains v0 vs Alex-locked grain — **§ PD29 delta** |
| `transcripts/PD29_notes.md` | Alex tenure locks (Sep 2) | Decision cohort, career rate, dept pond |
| `transcripts/PD41_notes.md` | Alex priorities (Sep 22) | Assortativity P0; tenure in trio — **current week context only** |

**Type:** current-status + advisor direction.

### Tier 2 — Pipeline contract and implementation

| Path | Purpose | Why important |
|------|---------|---------------|
| `tenure/documents/TENURE_DATA_GAMEPLAN.md` | Strategic contract | Stage boundaries, durable files, advisor Apr 2026 — **§G6, §G11–G13** |
| `tenure/documents/TENURE_PIPELINE_OVERVIEW.md` | Implementation map | Cell flags, file tree, scraper playbook — **§0 table, §2, §4, §7** |
| `tenure/documents/TENURE_SCRAPE_AND_ADJUDICATE_FOR_DUMMIES.md` | Scrape re-entry | Phase 1 Mac / Phase 2 Rivanna — **If you are expanding data** |
| `tenure/540_tenure_pipeline.ipynb` | Conductor | **Cell 0** = `RUN_CELL*` flags |

**Type:** technical specification + working plan.

### Tier 3 — Historical PEER reports (June 2026 snapshot)

| Path | Purpose | Why important |
|------|---------|---------------|
| `3-Master_Plan/obsolete/pre_tier1_locks/PEER_report_to_COMPASS.md` | Full Setting 3 narrative | Best single PEER-authored history through Jun 2026 — **§2–§3** |
| `5-Manuscript/obsolete/superseded_status_updates/PEER_Status_Update_for_VECTOR_2026-06-03.md` | VECTOR-facing snapshot | Stage 9 table, OpenAlex tiers — **may be stale vs Sep sandbox** |
| `3-Master_Plan/obsolete/original_filenames/20260624_PEER_inference_export_complete.md` | Inference export note | Links to manifest + filter rules |

**Type:** implementation record + historical context. **Superseded in part** by Sep hero campaign.

### Tier 4 — External / advisor-facing

| Path | Purpose | Why important |
|------|---------|---------------|
| `tenure/documents/20260720_Preliminary_Pipeline_Feasibility_Memo_for_Alex_Gates.md` | Alex feasibility | Stage stats, coverage proxy — Jul 2026 |
| `tenure/documents/PANEL_CSV_GLOSSARY.md` | Column definitions | Advisor CSV export |
| `tenure/alex_tenure_handoff/README_HANDOFF.md` | Alex code handoff | Historical; Rivanna data separate |

**Type:** external brief / handoff.

### Tier 5 — Operations

| Path | Purpose |
|------|---------|
| `tenure/documents/HPC_SETUP_CHECKLIST.md` | Mac vs Rivanna scenarios |
| `scripts/DATA_SYNC.md` | rsync push/pull policy |
| `tenure/documents/DISCOVER_FACULTY_URLS_GUIDE.md` | URL discovery algorithm |
| `tenure/documents/RIVANNA_CURSOR_REMOTE_SSH_FOR_DUMMIES.md` | Remote SSH + agent chat limits |

**Type:** technical specification.

### Tier 6 — Hero campaign (COMPASS-owned; uses PEER data)

| Path | Purpose |
|------|---------|
| `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/TENURE_HERO_Campaign_Plan.md` | Four-act campaign |
| `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/_DISPOSABLE_tenure_hero_thread.md` | YOU ARE HERE thread |
| `3-Master_Plan/re_entry/20260901_COMPASS_to_PEER_tenure_scrape_bolster.md` | Scrape bolster checklist |
| `3-Master_Plan/re_entry/20260902_COMPASS_to_PEER_author_year_career_master.md` | T5 career master spec |

**Type:** working plan (COMPASS).

### Tier 7 — SpecStory (conversation evidence)

| Path | Subject |
|------|---------|
| `.specstory/history/2026-04-02_17-36-36-0400-peer.md` | Stage 6 pilot, HPC, SpecStory, rsync, git |
| `.specstory/history/2026-04-03_13-55-35-0400-peer.md` | Continued PEER Apr 2026 session |

**Type:** historical context. **Gap:** Sep 2026 PEER sessions (scrape re-entry, COMPASS handoff) may not yet appear as exported SpecStory files — see agent transcript `6447dea8-1461-4fd5-8167-b9e4c78e10c3` if needed.

### Tier 8 — Obsolete VECTOR package (orientation only)

| Path | Note |
|------|------|
| `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/00_READ_ME_FIRST_FOR_VECTOR.md` | Written for **no repo access** — assumptions obsolete |
| `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md` | File catalog; use repo paths instead |

---

## Source legend

| Tag | Meaning |
|-----|---------|
| **Repo verified** | PEER read file or listed artifact on 2026-09-22 |
| **Conversation** | SpecStory or agent transcript cited |
| **Infer** | Reasonable inference from multiple docs — not directly verified |
| **Unknown** | Needs Charles or fresh run |

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-09-22 | PEER handoff created for VECTOR repo-access onboarding assignment |
