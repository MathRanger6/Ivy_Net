# Manifest — VECTOR onboarding (repo-connected)

**Folder:** `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/`  
**Repo root:** Charles’s PDE dissertation workspace (`Cursor Workspace PDE/`) on Mac  
**Last updated:** 2026-09-24  
**Audience:** VECTOR — **ChatGPT desktop app**, repo-connected (successor to browser Scholar GPT).

**Primary mode (Sep 2026):** VECTOR has **direct repo read access** on the Mac. **No zip handoff required.** The numbered files in this folder are the **curated narrative layer** — read them first, then follow repo paths below.

**Legacy:** Zip-only handoff (browser-era) is **obsolete** unless repo access fails.

**Scope:** VECTOR reads paths and prose for story work; VECTOR does **not** modify code, run Army notebooks, or use Git unless Charles explicitly asks.

---

## Onboarding (repo-connected)

| Step | What VECTOR reads |
|------|-------------------|
| **1** | This manifest + `00_READ_ME_FIRST_FOR_VECTOR.md` |
| **2** | Numbered handoff files **01–10** in this folder |
| **3** | Tier 1 re-entry + binding docs (§2 below) |
| **4** | Living threads + domain memos as needed (§2) |
| **5** | Figures via **repo paths** (HEROs, `talent/re_entry/output/`, flipbook decks in-repo) |

---

## Rules (binding — all eight)

### 1. Start with the handoff pack

Read **in this order** before any repo archaeology:

| Order | Path (repo-relative from handoff folder) | Role |
|-------|------------------------------------------|------|
| **0** | `00_READ_ME_FIRST_FOR_VECTOR.md` | Phase, deliverable, binding rules |
| **0b** | `MANIFEST_upload_to_VECTOR.md` | This file |
| **1** | `01_ASSIGNMENT_story_outline.md` | Deliverable spec + template |
| **2** | `03_CHARLES_locks_Sep16.md` | Judgment calls + gap priorities |
| **3** | `09_PD30_Alex_notes.md` | Alex mandate (“what’s the story?”) |
| **4** | `04_Problem_in_Plain_English.md` | Thesis / phenomenon |
| **5** | `06_BINDING_Selection_is_its_own_step.md` | **Binding** — environment ≠ advancement; score ≠ select |
| **6** | `02_paper_flipbook_PD30.md` | Slide claims — mine for story; don’t mirror 1:1 |
| **7** | `05_Three_Kinds_of_Model.md` | Layer A / B / C |
| **8** | `07_PAPER_Campaign_Plan.md` | Campaign sequencing |
| **9** | `08_Pass_A_and_Pass_B_plain_English.md` | Mechanism sim vocabulary |
| **10** | `10_Army_band_excellence_and_theta_Sep24.md` | **Sep 24** — Act I band of excellence, θ vs MLE, PDE/Vantage, PD41 link |
| **—** | `99_BACKGROUND_COMPASS_questionnaire_full.md` | Optional deep dive (~730 lines) |

Full paths: `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/<file>`.

### 2. Read canonical re-entry before raw conversations

After §1, read **Tier 1 re-entry** (authoritative repo prose) **before** SpecStory agent chats:

| Order | Path | Role |
|-------|------|------|
| 1 | `3-Master_Plan/re_entry/00_READ_ME_FIRST.md` | Repo entry |
| 2 | `3-Master_Plan/re_entry/01_The_Problem_in_Plain_English.md` | Problem statement |
| 3 | `3-Master_Plan/re_entry/02_Three_Kinds_of_Model.md` | Assign / score / select |
| 4 | `3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md` | Pass A / Pass B |
| 5 | `3-Master_Plan/BINDING_Selection_is_its_own_step.md` | Binding rule |
| 6 | `3-Master_Plan/re_entry/PAPER_Campaign_Plan.md` | Paper campaign |
| 7 | `3-Master_Plan/re_entry/03_Three_Day_Basketball_Focus.md` | Near-term scope |
| 8 | `3-Master_Plan/re_entry/05_Alex_Magnitude_Spec.md` | Phase C magnitude |
| 9 | `3-Master_Plan/re_entry/06_Lambda_threshold_and_KN_memo.md` | λ, θ vs K/N |
| 10 | `3-Master_Plan/re_entry/07_Phase_B_Characterization_Slides_Explained.md` | Phase B deck |
| 11 | `3-Master_Plan/re_entry/08_PD16_Alex_meeting_takeaways.md` | PD16 |
| 12 | `3-Master_Plan/re_entry/09_PD18_Alex_meeting_takeaways.md` | PD18 |
| 13 | `transcripts/PD15_notes.md` … `transcripts/PD41_notes.md` | Curated Alex meeting notes |

**Living threads** (Charles judgment — not canonical):  
`3-Master_Plan/re_entry/_DISPOSABLE_paper_flipbook_PD30.md`,  
`_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md`,  
`HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md`.

### 3. SpecStory = conversation archive

**Include:** `.specstory/history/*.md` (SpecStory Markdown v2.1.0 exports).

**Exclude:**

| Path | Reason |
|------|--------|
| `.specstory/history/debug/` | Raw session JSON |
| `.specstory/debug/` | CLI diagnostics |
| `.specstory/history/bin/` | Binaries |
| `.specstory/history/cli/` | Local CLI config |

**Index (metadata only):** `.specstory/history/statistics.json`

### 4. Deduplicate UTC vs local-time sessions

Keep **local offset** filenames (`-0400` / `-0500`); drop **`Z`** duplicates:

| Exclude | Keep |
|---------|------|
| `.specstory/history/2025-11-17_22-43-36Z-coda.md` | `.specstory/history/2025-11-17_17-43-36-0500-coda.md` |
| `.specstory/history/2026-04-02_21-36-36Z-peer.md` | `.specstory/history/2026-04-02_17-36-36-0400-peer.md` |
| `.specstory/history/2026-04-03_17-55-35Z-peer.md` | `.specstory/history/2026-04-03_13-55-35-0400-peer.md` |
| `.specstory/history/2026-04-04_20-22-41Z-conversations-about-coda.md` | `.specstory/history/2026-04-04_16-22-41-0400-conversations-about-coda.md` |
| `.specstory/history/2026-05-24_16-52-09Z-scout.md` | `.specstory/history/2026-05-24_12-52-09-0400-scout.md` |
| `.specstory/history/2026-06-11_12-19-11Z-compass.md` | `.specstory/history/2026-06-11_08-19-11-0400-compass.md` |

### 5. Chunk large COMPASS archives

**Primary file:** `.specstory/history/2026-06-11_08-19-11-0400-compass.md` (~20 MB)

- Split on markdown `#` headings or `<!-- Cursor IDE Session` chronological blocks.
- **Every chunk** must cite: `specstory:<filename> § "<heading or date block>"`.
- Apply same rule to large `…-coda.md` (~2.6 MB) and `…-scout.md` (~2.7 MB) if indexed.

### 6. Distinguish four evidence types

Tag every claim when building the story outline:

| Tag | Meaning |
|-----|---------|
| **📋 PROPOSAL** | Agent plan, flipbook row, open `[WHOA]`, Alex “maybe” |
| **🔧 REPORTED** | Chat says something was implemented or run |
| **📁 CODE** | File exists at cited path (read source — may be stale) |
| **✅ VERIFIED** | Manifest/meta JSON, regen command, or Charles-approved artifact |

**Default for SpecStory:** 📋 or 🔧 until cross-checked against re-entry or a domain manifest.  
**Do not** treat chat prose as ✅ VERIFIED.

### 7. Do not import

| Category | Paths |
|----------|-------|
| **Restricted Army data** | `talent/talent_pipeline/ofcr_oers.csv`, `pid_snaps.csv`, `fake_oer_snapshots.csv`, `talent/Army_AWS_download/`, `2-Sequestered/` |
| **Credentials** | `.env`, `.env.local`, `*.pem`, `ivy_net_keys` |
| **Debug logs** | `.specstory/history/debug/`, `.specstory/debug/`, `slurm-*.out`, `slurm_out/` |
| **Unapproved outputs** | Ad-hoc PNGs without manifest; flipbook rows 🟡/⏸ in `_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md` |
| **Large bulk** (unless Charles approves) | `datasets/mbb/**` (see `datasets/mbb/README_TRACKED_ARTIFACTS.md` for exceptions), multi-100MB Big Fish CSVs, `tenure/tenure_pipeline/faculty_panel*.jsonl`, `**/faculty_snapshots/` |

### 8. Read-only during onboarding

VECTOR **must not** modify analytical code, execute notebooks, or perform Git operations while onboarding or drafting `STORY_OUTLINE_Charles_Alex.md`.

---

## Repository orientation (where to look)

Concise map for ChatGPT desktop repo access. All paths **repository-relative**; verify before citing.

### Army (scientific origin · Cox · BDP)

| What | Path |
|------|------|
| Main notebook | `talent/talent_pipeline/520_pipeline_cox_working.ipynb` |
| Pipeline config | `talent/talent_pipeline/pipeline_config.py` |
| Cox docs | `talent/documents/520_PIPELINE_COX_OVERVIEW.md`, `talent/documents/PIPELINE_RUN_ORDER.md` |
| BDP + data story | `talent/re_entry/build_army_data_story.py`, `talent/re_entry/run_army_bdp_pipeline.sh` |
| 3×3 manifest | `talent/re_entry/manifests/army_run1_3x3_manifest.json` |
| Generated mosaic | `talent/re_entry/output/data_story/ARMY_DATA_STORY_run1_3x3.png` (when built) |
| Figure extracts | `3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/` |
| Pool-grain primer | `3-Master_Plan/re_entry/ARMY_fwd_bwd_and_pool_fix_for_dummies.md` |

**Symlink:** `talent_pipeline/` → `talent/talent_pipeline/`. **Not ground truth:** `talent/Army_AWS_download/`.

### MBB (basketball · reigning hero)

| What | Path |
|------|------|
| Sandbox index | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/README.md` |
| Reigning 3×3 PNG | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/MBB_DATA_STORY_reigning_3x3.png` |
| Reigning manifest | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/mbb_reigning_3x3_manifest.json` |
| Talk track | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/MBB_DATA_STORY_plot_highlights.md` |
| Reigning hero artifacts | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/` |
| Pass A (empirical) | `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/` |

### Tenure (portability test)

| What | Path |
|------|------|
| Sandbox index | `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/README.md` |
| PD29 3×3 PNG | `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/TENURE_DATA_STORY_pd29_3x3.png` |
| PD29 manifest | `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/tenure_pd29_3x3_manifest.json` |
| Talk track | `3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/data_story/TENURE_DATA_STORY_plot_highlights.md` |
| Perf-story builder | `tenure/scripts/tenure_perf_metric_story.py` |
| PD29 notes | `transcripts/PD29_notes.md` |

### Mosaic / data-story plotting

| What | Path |
|------|------|
| Shared 3×3 compositor | `sports/scripts/build_data_story_mosaic.py` |
| Perf-metric mosaic | `sports/scripts/build_perf_metric_mosaic.py` |
| Layout / styling | `sports/scripts/story_page_layout.py` |
| MBB perf story | `sports/scripts/mbb_perf_metric_story.py` |
| Big Fish multi-domain | `scripts/big_fish_data_story.py` (legends, football, NELS, HSB) |
| Flipbook figure deck | `scripts/build_flipbook_figure_deck.py` |

### ASSIGN → SCORE → SELECT (model layer)

| Layer | Path |
|-------|------|
| **ASSIGN** | `sports/541_grandchild_homophily_assign.py` |
| **ASSIGN** | `sports/documents/541_grandchild_homophily_assign_README.md` |
| **ASSIGN** | `3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/` |
| **ASSIGN** (prose) | `3-Master_Plan/VECTOR_work/VECTOR_Bipartite_Assortative_Formation_Model.md`, `COMPASS_BRIEF_ASSIGN_GRANDCHILD.md` |
| **SCORE** | `3-Master_Plan/re_entry/HEROs_and_PASSes/sort_chop_lambda/` |
| **SCORE** | `3-Master_Plan/re_entry/06_Lambda_threshold_and_KN_memo.md` |
| **SELECT** (Pass A) | `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/` |
| **SELECT** (Pass B) | `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_b/` |
| **SIM** | `sports/540_READ_ME_SIM.md`, `sports/540_three_step_sim.ipynb`, `sports/sim_config.py` |
| **SIM outputs** | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/sim_hero/` |

**Campaign dirs:** `HEROs_and_PASSes/pd20_temperature/`, `pd21_rho/`, `pd22_minutes/`

### Big Fish backup portfolio (not core story legs)

| Path | Domain |
|------|--------|
| `HEROs_and_PASSes/legends_sandbox/data_story/LEGENDS_DATA_STORY_3x3.png` | LoL |
| `HEROs_and_PASSes/football_sandbox/data_story/FOOTBALL_DATA_STORY_3x3.png` | Football |
| `HEROs_and_PASSes/education_sandbox/nels88/` | NELS |
| `HEROs_and_PASSes/education_sandbox/hsb80_soph/`, `hsb80_senior/` | HSB |
| `HEROs_and_PASSes/EDUCATION_dataset_primer.md` | Education framing |

*(Prefix `3-Master_Plan/re_entry/` on all `HEROs_and_PASSes/…` paths above.)*

### VECTOR_work + plans (beyond handoff folder)

| Path | Role |
|------|------|
| `3-Master_Plan/VECTOR_work/COMPASS_Dissertation_Core_Deck_Materials_Questionnaire.md` | Deck questionnaire |
| `3-Master_Plan/VECTOR_work/COMPASS_Dissertation_Core_Deck_Materials_Questionnaire_COMPASS_draft.md` | COMPASS prefill |
| `3-Master_Plan/VECTOR_work/VECTOR_Alex_ASSIGN_Configuration_Model_Response.md` | Alex ASSIGN response |
| `3-Master_Plan/plans/README.md` | Plan mirrors index |
| `3-Master_Plan/COMPASS_AGENT_IDENTITY.md` | Agent naming |

---

## SpecStory keep-list (22 unique sessions)

After deduping §4, these are the conversation files worth indexing:

`.specstory/history/2025-11-17_17-43-36-0500-coda.md` ·  
`.specstory/history/2026-03-26_18-29-18-0400-scout.md` ·  
`.specstory/history/2026-04-02_17-36-36-0400-peer.md` ·  
`.specstory/history/2026-04-03_13-55-35-0400-peer.md` ·  
`.specstory/history/2026-04-04_16-22-41-0400-conversations-about-coda.md` ·  
`.specstory/history/2026-04-26_16-19-16-0400-conversations-about-coda.md` ·  
`.specstory/history/2026-04-27_09-24-06-0400-conversations-about-malejko.md` ·  
`.specstory/history/2026-04-27_09-25-37-0400-analytics-conversations-in-transcripts.md` ·  
`.specstory/history/2026-04-27_13-51-58-0400-conversations-about-tom-and.md` ·  
`.specstory/history/2026-04-30_13-25-36-0400-binary-files-in-repository.md` ·  
`.specstory/history/2026-05-18_11-14-35-0400-medium-conversations-in-agent.md` ·  
`.specstory/history/2026-05-24_12-52-09-0400-scout.md` ·  
`.specstory/history/2026-06-11_08-19-11-0400-compass.md` ·  
`.specstory/history/2026-08-06_13-07-25-0400-regenerate-pd17-auto-slide.md` ·  
`.specstory/history/2026-08-12_14-35-46-0400-find-plot-label-bugs.md` ·  
`.specstory/history/2026-08-19_09-30-12-0400-pd20-22-campaign-slide.md` ·  
`.specstory/history/2026-08-20_09-34-35-0400-fitting-parameters-for-alex.md` ·  
`.specstory/history/2026-08-25_14-24-30-0400-find-old-hero-specs.md` ·  
`.specstory/history/2026-08-25_14-26-39-0400-run-hero-mg-0.md` ·  
`.specstory/history/2026-08-28_10-53-57-0400-explore-player-loo-and.md` ·  
`.specstory/history/2026-09-04_10-10-49-0400-explore-tenure-mbb-plot.md` ·  
`.specstory/history/2026-09-15_15-17-14-0400-explore-repo-for-vector.md`

**Path archaeology entry point:** `…-explore-repo-for-vector.md` (feeds the deck questionnaire).

---

## Included in this folder (preserved — do not reorder)

| File | Description |
|------|-------------|
| `00_READ_ME_FIRST_FOR_VECTOR.md` | **Start here** |
| `01_ASSIGNMENT_story_outline.md` | Deliverable spec + skeleton |
| `03_CHARLES_locks_Sep16.md` | Judgment calls + gap priorities |
| `02_paper_flipbook_PD30.md` | Slide claims |
| `04_Problem_in_Plain_English.md` | Thesis / phenomenon |
| `05_Three_Kinds_of_Model.md` | Layer A/B/C |
| `06_BINDING_Selection_is_its_own_step.md` | **Binding** score ≠ select |
| `07_PAPER_Campaign_Plan.md` | Campaign sequencing |
| `08_Pass_A_and_Pass_B_plain_English.md` | Mechanism sim plain English |
| `09_PD30_Alex_notes.md` | Alex PD30 locks |
| `99_BACKGROUND_COMPASS_questionnaire_full.md` | Optional — full COMPASS prefill |

---

## Send separately (Mode A — not in repo for VECTOR)

| Asset | Why |
|-------|-----|
| `_DISPOSABLE_paper_flipbook_PD30_FIGURE_DECK.pptx` (or `.html`) | Talk skeleton — visual skim |
| `_DISPOSABLE_paper_flipbook_PD30_FIGURE_INVENTORY.pptx` (or `.html`) | Full figure catalog |
| `_DISPOSABLE_paper_flipbook_PD30.pdf` | Flipbook print-friendly |
| Optional PNGs: Army G1, MBB 3×3, tenure 3×3, λ knockout | Visual literacy |

---

## VECTOR returns

| File | To |
|------|-----|
| `STORY_OUTLINE_Charles_Alex.md` | Charles + Alex → COMPASS if useful |

---

## Regenerate handoff copies (Charles / COMPASS only — not VECTOR)

Refresh numbered copies when flipbook or locks change materially.

**Handoff copies last synced:** 2026-09-16 · **Manifest last updated:** 2026-09-22
