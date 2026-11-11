# COMPASS agent handoff — research history for VECTOR

**Agent:** COMPASS (cross-project planning)  
**Date:** 2026-09-22  
**Audience:** VECTOR — GPT scholar / narrative craft agent with **direct repository access** (ChatGPT Work on Charles’s Mac)  
**Scope:** COMPASS’s shared history with Charles only — not CODA, SCOUT, or PEER voice.

**How to use this file:** Annotated map and chronology. **Read cited originals** in the repo; do not treat this handoff as a substitute for source documents or SpecStory sessions.

**Onboarding map (repo-connected):** `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md`

---

## 1. My role and our working relationship

### What COMPASS is

COMPASS is the **cross-project planning agent** — scientific coherence, dependency tracking, sequencing, and claim language across Army, MBB, tenure, mechanism/sim, and paper talk. Charles renamed “Master Planner” to **COMPASS** on **2026-06-11**.

**Source:** `3-Master_Plan/COMPASS_AGENT_IDENTITY.md` · `3-Master_Plan/obsolete/pre_tier1_locks/COMPASS_Initial_Guidance_v6.md` (§ Mission, § Special Responsibilities)

| COMPASS does | COMPASS does not |
|--------------|------------------|
| Plan sequencing, reconcile agent reports, draft re-entry / campaign / disposable threads | Own domain code (`talent/`, `sports/`, `tenure/`) |
| Maintain BINDING vocabulary, paper campaign, flipbook tables, VECTOR questionnaires | Run notebooks, Cox models, or scrape pipelines |
| Assess Big Fish portfolios, PD meeting reads, plan mirrors | Write dissertation manuscript prose (VECTOR’s lane) |
| Route questions to CODA / SCOUT / PEER / VECTOR | Speak for those agents’ implementation history |

**Operating bias (Charles lock):** Completion > expansion; validation > complexity; publication > exploration.  
**Source:** `COMPASS_Initial_Guidance_v6.md` § Planner Operating Procedure

### Domains where COMPASS and Charles worked together

| Area | COMPASS contribution | Primary repo homes |
|------|----------------------|-------------------|
| **Agent orchestration (Jun 2026)** | Initial review; `COMPASS_to_{CODA,SCOUT,PEER,VECTOR}_questions.md`; Path A/B on generative vs empirical | `3-Master_Plan/obsolete/pre_tier1_locks/` |
| **Re-entry narrative (Jul–Aug 2026)** | Sequenced plain-English docs 01–04; BINDING; lambda memo; PD16/18 takeaways | `3-Master_Plan/re_entry/` |
| **Hero model reset (Jul 2026)** | Plan mirror, three-layer vocabulary, Pass A/B framing | `3-Master_Plan/plans/20260721_hero_model_reset.plan.md` |
| **PD12 reassessment (Jun 2026)** | Restored model → measurements → predictions chain | `3-Master_Plan/plans/20260615_pd12_compass_reassessment.plan.md` |
| **SCOUT ↔ COMPASS porch science (Aug 2026)** | CCT band, BDP congestion memos, data-aperture correspondence | `3-Master_Plan/re_entry/SCOUT_and_COMPASS/` |
| **Paper campaign / flipbook (Sep 2026)** | `PAPER_Campaign_Plan.md`, `_DISPOSABLE_paper_flipbook_PD30.md`, PD29/30 synthesis | `3-Master_Plan/re_entry/` · `transcripts/` |
| **Big Fish portfolio (Sep 2026)** | Dataset assessment, education primer, sandbox sequencing | `3-Master_Plan/re_entry/HEROs_and_PASSes/` |
| **VECTOR onboarding (Sep 2026)** | Handoff folder, deck questionnaire, manifest for repo access | `3-Master_Plan/VECTOR_work/` |

### Overlap with other agents (boundaries)

| Agent | Domain | Where COMPASS overlapped |
|-------|--------|--------------------------|
| **CODA** | Army / `talent/` | Sequenced army BDP/data-story vs 520 Cox; pool-grain memos — **CODA implements** |
| **SCOUT** | MBB / `sports/` | Hero spec, grandchild assign briefs, sim Path A/B — **SCOUT implements** |
| **PEER** | Tenure / `tenure/` | PD29 lock synthesis, scrape bolsters, author-year master routing — **PEER implements** |
| **VECTOR** | Theory / manuscript | Question files Jun 2026; Sep 2026 story-outline assignment — **VECTOR drafts prose** |

When COMPASS cites “completed work,” verify in the **domain agent’s** code and manifests unless this handoff points to a COMPASS-authored markdown artifact.

---

## 2. Chronological research history

Non-linear timeline — priority flips are real, not mistakes to paper over.

### Phase 0 — Pre-COMPASS (before 2026-06-11)

- Charles ran **VECTOR** (theory/manuscript) and domain agents on Army, MBB, tenure separately.
- Tier-1 manuscript corpus lives under `1-Various_PDE_and_Chat_stuff/5-Manuscript/` (historical; not the re-entry entry point Charles uses now).
- **Inference:** Early framing mixed “selection,” environment, and hero curve — later corrected by BINDING (Jul 2026).

### 2026-06-11 — COMPASS stands up

- Charles commissioned **Master Planner** → **COMPASS** with `COMPASS_Initial_Guidance_v6.md`.
- COMPASS ingested domain agent reports (`CODA_report_to_COMPASS.md`, `SCOUT_report_to_COMPASS.md`, `PEER_report_to_COMPASS.md`) and VECTOR manuscript folder.
- **Key decision:** **Path A** for Summer–Fall 2026 manuscript — VECTOR may draft empirical triad + honest generative caveat; **do not block** on generative LOO bin-for-bin match.  
  **Source:** `.specstory/history/2026-06-11_08-19-11-0400-compass.md` (early session — search “Path A”, “honest B”, “generative LOO”)
- COMPASS created routed question files: `3-Master_Plan/obsolete/pre_tier1_locks/20260611_1626_COMPASS_to_{CODA,SCOUT,PEER,VECTOR}_questions.md`

### 2026-06-15 — PD12 reassessment

- Charles + VECTOR flagged **framing drift**: plans compressed to Phenomenon → Model → Paper; Alex wanted **measurements and predictions** in the chain.
- COMPASS deliverable: `3-Master_Plan/plans/20260615_pd12_compass_reassessment.plan.md` (answers Q1–Q5; agent routing table).
- **No scope expansion** — documentation alignment only.

### 2026-06-17 — Primary focus plan

- COMPASS mirrored `3-Master_Plan/plans/20260617_primary_focus_now.plan.md` — model work vs reading rabbit holes.
- **Source:** `3-Master_Plan/plans/README.md`

### 2026-07-28 — Hero model reset + BINDING sharpened

- Charles confusion peak: one word “model” for three objects.
- COMPASS coordinated vocabulary lock: **environment ≠ advancement; score ≠ select**.
- **Artifacts:** `3-Master_Plan/BINDING_Selection_is_its_own_step.md`; `3-Master_Plan/plans/20260721_hero_model_reset.plan.md`; re-entry `02_Three_Kinds_of_Model.md`, `04_Pass_A_and_Pass_B_in_Plain_English.md`
- Pass A (λ knockout) and Pass B (ρ ablation) marked **completed** in plan todos — **verify** in `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/`, `pass_b/`

### 2026-08-04 — PD16

- Team `L_C`, θ from K/N, calibration roadmap.
- **Source:** `3-Master_Plan/re_entry/08_PD16_Alex_meeting_takeaways.md` · `transcripts/PD16_notes.md`

### 2026-08-19–2026-08-28 — PD20–22 campaigns + SCOUT/COMPASS porch memos

- Temperature, ρ, minutes campaigns documented under `3-Master_Plan/re_entry/HEROs_and_PASSes/pd20_temperature/`, `pd21_rho/`, `pd22_minutes/`
- SCOUT↔COMPASS correspondence on CCT bands, big-fish small-pond wisdom: `3-Master_Plan/re_entry/SCOUT_and_COMPASS/`

### 2026-09-02 — PD29 (tenure locks + paper 50/50)

- Alex locked tenure decision cohort, cumulative pubs rate, department pond.
- **Parallel mandate:** 50% data / 50% **paper talk outline** (question → figure → claim).
- **Source:** `transcripts/PD29_notes.md` · COMPASS synthesized in disposable tenure threads (PEER-led implementation)

### 2026-09-03–04 — Big Fish tour + PD30

- Charles showed Alex all Big Fish storyboards (MBB, tenure, legends, football).
- **Priority flip #1:** Big Fish → **back burner**; **paper flipbook / story** → **P0**.
- **Source:** `transcripts/PD30_notes.md` · `3-Master_Plan/re_entry/PAPER_Campaign_Plan.md` · `_DISPOSABLE_big_fish_datasets_assessment.md`

### 2026-09-15–16 — VECTOR handoff packaging

- COMPASS built zip-oriented handoff: `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/` (00–09 copies, questionnaire background).
- Charles locks Sep 16 in `03_CHARLES_locks_Sep16.md`; checklist `_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md`
- **Assumption then:** VECTOR lacked repo access — **obsolete as of Sep 22** (see §7).

### 2026-09-22 — Education sandbox + PD41

- COMPASS lane: NELS + HSB 3×3 decks, `EDUCATION_dataset_primer.md`, manifest update for repo-connected VECTOR.
- **Same day PD41:** Alex **priority flip #2** — **assortativity (H_sort) P0**; education **one day** (college prestige?); narrative restructure by EOW/weekend.
- **Source:** `transcripts/PD41_notes.md` · `transcripts/20260922_Paper_Directions_41_otter_ai_transcript.docx`

---

## 3. Work actually completed

Distinguish **COMPASS-authored documentation** from **domain implementation** COMPASS sequenced but did not execute.

### COMPASS documentation (verified files)

| Artifact | Path | Status |
|----------|------|--------|
| Agent identity | `3-Master_Plan/COMPASS_AGENT_IDENTITY.md` | ✅ |
| BINDING rule | `3-Master_Plan/BINDING_Selection_is_its_own_step.md` | ✅ |
| Re-entry spine 00–09 | `3-Master_Plan/re_entry/0*.md` | ✅ (see `00_READ_ME_FIRST.md`) |
| Paper campaign | `3-Master_Plan/re_entry/PAPER_Campaign_Plan.md` | ✅ last synced 2026-09-05 |
| Flipbook thread | `3-Master_Plan/re_entry/_DISPOSABLE_paper_flipbook_PD30.md` | ✅ living |
| Plan mirrors | `3-Master_Plan/plans/*.plan.md` | ✅ (4 mirrors per README) |
| Big Fish assessment | `3-Master_Plan/re_entry/HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md` | ✅ updated 2026-09-22 |
| Education primer | `3-Master_Plan/re_entry/HEROs_and_PASSes/EDUCATION_dataset_primer.md` | ✅ 2026-09-22 |
| VECTOR handoff + manifest | `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/` | ✅ manifest 2026-09-22 |
| Deck questionnaire | `3-Master_Plan/VECTOR_work/COMPASS_Dissertation_Core_Deck_Materials_Questionnaire.md` (+ COMPASS draft) | ✅ |
| PD41 meeting read | `transcripts/PD41_notes.md` | ✅ 2026-09-22 |
| Grandchild briefs | `3-Master_Plan/VECTOR_work/COMPASS_BRIEF_ASSIGN_GRANDCHILD.md`, `COMPASS_DETAILED_ASSIGN_GRANDCHILD_INSTRUCTIONS.md` | ✅ |

### Domain artifacts COMPASS referenced and sequenced (verify before ✅ VERIFIED claims)

| Domain | Artifact | Path | Empirical status |
|--------|----------|------|------------------|
| MBB | Reigning 3×3 mosaic | `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/MBB_DATA_STORY_reigning_3x3.png` | ✅ PNG + `mbb_reigning_3x3_manifest.json` exist |
| Tenure | PD29 3×3 mosaic | `…/tenure_sandbox/data_story/TENURE_DATA_STORY_pd29_3x3.png` | ✅ PNG + manifest exist |
| Pass A | LPM / binned draft rates | `…/HEROs_and_PASSes/pass_a/PASS_A_lpm_hero_coefficients.txt` | ✅ files present |
| Pass B | Generative knockout meta | `…/pass_b/PASS_B_generative_knockout_meta.json` | ✅ file present |
| Grandchild | H_sort / ρ / λ meta | `…/grandchild_assign/*.json` | ✅ meta JSONs present |
| Football | 3×3 + usage twin | `…/football_sandbox/` | ✅ screened PD30 |
| Legends | 3×3 + perf story | `…/legends_sandbox/data_story/` | ✅ Sep 2026 |
| Education | NELS + HSB decks | `…/education_sandbox/{nels88,hsb80_soph,hsb80_senior}/` | ✅ built 2026-09-22 |
| Army | BDP manifest + sandbox extracts | `talent/re_entry/manifests/army_run1_3x3_manifest.json`, `…/army_sandbox/` | 📁 partial — mosaic PNG path may be generated not committed |
| Army Cox | 520 notebook | `talent/talent_pipeline/520_pipeline_cox_working.ipynb` | 📁 CODE — **not executed by COMPASS** |

**Empirical findings COMPASS treats as documented (not independently re-run):**

- MBB hero inverted-U on locked spec — Pass A artifacts + Alex PD history
- Army inverted-U as **scientific anchor** — Charles lock Sep 4 in `PAPER_Campaign_Plan.md` §1; G1 canonical PNG still 🔜 per flipbook checklist
- Tenure porch direction approved PD29 — full PD29 spine **implementation** owned by PEER
- H_sort cross-domain screen — numbers in `transcripts/PD41_notes.md`; education runs in sandbox meta JSONs

---

## 4. Proposed but unfinished work

| Item | Proposed where | Status |
|------|----------------|--------|
| **VECTOR `STORY_OUTLINE_Charles_Alex.md`** | `handoff_upload_no_repo/01_ASSIGNMENT_story_outline.md` | ⬜ VECTOR deliverable |
| **Charles + Alex meet on outline** | `_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md` P0b | ⬜ |
| **Army G1 canonical lead PNG** | Flipbook §1.1; checklist 🔜 G1a | ⬜ |
| **Generative LOO bin-for-bin match** | Jun 2026 COMPASS Path A — **explicitly deferred** | ⏸ parked (`20260721_hero_model_reset.plan.md` defer-stretch todo ✅) |
| **Cell 12 Cox before submission** | Jun 2026 COMPASS_to_PEER/VECTOR questions | 🟡 parallel track — PEER owns |
| **Tenure PD29 full spine rebuild** | `PD29_notes.md` T1–T6 | 🟡 PEER — v0 porch exists, locks partial |
| **Education college prestige / college pond** | `PD41_notes.md` · Alex one-day ask | ⬜ not started |
| **Assortativity “does it matter?” analysis** | PD41 P0 | ⬜ Charles/CODA/SCOUT — **blocks story** per Alex |
| **Narrative restructure PowerPoint** | PD41 — EOW/weekend | ⬜ |
| **Apache / new Big Fish datasets** | `_DISPOSABLE_big_fish_datasets_assessment.md` B5 | ⏸ lowest priority |
| **Weighted HERO (NELS survey weights)** | `EDUCATION_dataset_primer.md` | ⬜ discussed, not wired |
| **Handoff copy refresh** | Manifest — last synced 2026-09-16 | 🟡 flipbook/PD41 not copied into 00–09 pack |

**Reported but not verified by COMPASS:** Any SpecStory agent claim of “done” — treat as 🔧 until manifest/code checked.

---

## 5. Negative results and abandoned approaches

| Result | Evidence | Why abandoned / demoted |
|--------|----------|---------------------------|
| **Big Fish as primary time sink** | `transcripts/PD30_notes.md`; assessment PD30 row | Alex: back burner; MBB/tenure/army stay main line |
| **Legends (LoL) as lead domain** | `legends_sandbox/`; PD30 “no reigning HERO” | Weak composite; background only |
| **Football Â composite porch** | `football_sandbox/`; PD30 | Fail; **usage LOO** kept as pedagogy nugget |
| **Education HS pond → BA+ as HERO story** | `PD41_notes.md`; Alex “none of them work” | Wrong pond/Y for congestion claim; sorting contrast only |
| **Generative match on same axis as empirical LOO** | Jun 2026 COMPASS session; hero reset plan | Path A honest B — team_mean POC ≠ LOO replication |
| **Fine–Gray competing risks (immediate)** | `.specstory/…-compass.md` “Fine–Gray deferred” | Pre-submission shelf unless pushed |
| **525 / networks / full L_Q generative match** | Jun 2026 near-term plan prose | Explicitly deferred for manuscript timeline |
| **Flipbook Act V (football LOO pedagogy)** | `_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md` | ⏸ parked |
| **Slide 1.4 Cox partial effects in core story** | Flipbook red-pen 🟡 | Charles unsure value — optional |

Preserve these — PD41 **re-opens education** but does not erase PD30 demotion of Big Fish as primary.

---

## 6. Current state as of September 22, 2026

### Verified artifacts (COMPASS confidence: high)

- Re-entry narrative 00–09 + BINDING — **`3-Master_Plan/re_entry/`**, **`BINDING_Selection_is_its_own_step.md`**
- MBB + tenure 3×3 mosaics and manifests — paths in §3
- Big Fish sandboxes including **education Sep 22** — `HEROs_and_PASSes/education_sandbox/`
- Pass A/B artifact folders with meta JSON / coefficient files
- PD15–PD41 curated notes — `transcripts/PD*_notes.md` (PD41 newest)
- VECTOR onboarding manifest with repo rules — `handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md`

### Documented empirical findings (supporting docs; domain agents own numerics)

- Army strong inverted-U (anchor) — `PAPER_Campaign_Plan.md` §0–§1; Charles Sep 4 lock
- MBB low H_sort (~0.06) as boundary — `PD41_notes.md` §H_sort screen
- Cross-domain H_sort ladder — PD41 meeting; education ~0.25–0.32 in sandbox meta JSONs
- Football usage LOO congestion twin — `football_sandbox/perf_story/` (PD30 post-call doc)

### Working hypotheses (not settled)

- **Does assortativity matter** for the mechanism story? — PD41 P0; open analysis
- **MBB low H_sort** explains weak homophily sensitivity — hypothesis in PD41 Charles remarks
- **Education congestion at college**, not HS — Charles + Alex aligned PD41; not yet in data
- **Pool grain / anchor cohort** for Army H_sort vs porch — Charles Sep 21–22 CODA thread (see CODA handoff; COMPASS did not implement)

### Proposed / unfinished (blocking story per Alex)

1. Assortativity analysis nailed — **PD41**
2. Education one-day embed (college fields?) — **PD41**
3. Narrative restructure deck — **PD41** by EOW/weekend
4. VECTOR story outline — **Sep 16 assignment** still open

### Dependencies

| Blocker | Depends on | Agent |
|---------|------------|-------|
| Story outline quality | Assortativity + Charles locks | COMPASS frames; VECTOR writes |
| Army-forward flipbook | CAC access + G1 PNG refresh | CODA |
| Tenure paper-grade porch | PD29 spine + scrape | PEER |
| Mechanism § generative honesty | Pass A/B artifacts + BINDING | VECTOR prose |

### Outstanding scientific questions (COMPASS read)

- Formal link **H_sort** ↔ **ρ** calibration ↔ hero shape across domains
- Whether education can be salvaged with **college pond** or prestige Y
- Whether MBB “works anyway” at ρ≈0 is core claim or boundary footnote
- λ threshold / θ vs K/N — memo exists (`06_Lambda_threshold_and_KN_memo.md`); Phase B incomplete per checklist

---

## 7. Contradictions, uncertainty, and unresolved decisions

| Issue | Sources | COMPASS read | Resolution needed |
|-------|---------|--------------|-------------------|
| **Primary task: story vs assortativity** | PD30 P0 flipbook vs PD41 P0 H_sort | Both real — PD41 **adds blocker** before outline finalizes | Charles: sequenced plan for EOW |
| **Education decks “done” vs “don’t work”** | Sep 22 sandbox build vs PD41 Alex | **Not contradictory** — implementation ✅; **scientific claim** ❌ for core story | College-level probe per PD41 |
| **Handoff: no repo vs repo access** | `00_READ_ME_FIRST_FOR_VECTOR.md` Sep 16 vs Sep 22 manifest | Obsolete assumption in 00_READ_ME | Optional one-line patch to 00_READ_ME (Charles approval) |
| **Army H_sort 0.255 vs 0.279** | PD41 transcript | Alex: immaterial; porch changed | Report both metrics; don’t over-claim H_sort sensitivity |
| **LoL H_sort ~0.445** | PD41 Charles verbal | Not in COMPASS sandbox meta — **verify** in `legends_sandbox/basic_data_plots/` overlap meta if exists | CODA/SCOUT or Charles regen |
| **Paper campaign “P0 active” Sep 5** | `PAPER_Campaign_Plan.md` header | May be stale vs PD41 | Charles confirm whether campaign doc gets PD41 addendum |
| **Cell 12 Cox: blocker or parallel?** | Jun 2026 COMPASS questions vs later deferral | Draft OK without; submit needs Cox | PEER status — see PEER handoff |
| **VECTOR role: prose vs repo scholar** | Jun 2026 questions vs Sep 2026 repo onboarding | VECTOR now reads repo; story outline assignment unchanged | Charles confirm VECTOR’s first deliverable |

**Questions requiring Charles confirmation:**

1. Should `PAPER_Campaign_Plan.md` be updated for PD41 priorities (assortativity before flipbook polish)?
2. Is education Sep 22 sandbox for **Alex screen only** or **VECTOR story appendix**?
3. Should numbered handoff copies (`02_paper_flipbook`, `09_PD30`) gain a `10_PD41` or stay transcript-only?

---

## 8. Annotated repository reading list

Prioritized for understanding **COMPASS’s** thread with Charles. Read §1–2 of manifest first.

| Priority | Path | Type | Why read | Sections to focus |
|----------|------|------|----------|-------------------|
| **1** | `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/MANIFEST_upload_to_VECTOR.md` | Onboarding spec | Repo-connected rules; orientation map | § Rules 1–8; Repository orientation |
| **2** | `3-Master_Plan/VECTOR_work/handoff_upload_no_repo/00_READ_ME_FIRST_FOR_VECTOR.md` | Assignment | VECTOR deliverable spec (story outline) | Full — note Mode A assumptions |
| **3** | `3-Master_Plan/re_entry/00_READ_ME_FIRST.md` | Re-entry index | Charles’s canonical reading order | Table § Your only reading list |
| **4** | `3-Master_Plan/BINDING_Selection_is_its_own_step.md` | Binding spec | Non-negotiable separations | § Three separations |
| **5** | `3-Master_Plan/re_entry/02_Three_Kinds_of_Model.md` | Conceptual | Layer A/B/C — COMPASS hero reset centerpiece | Full |
| **6** | `3-Master_Plan/re_entry/PAPER_Campaign_Plan.md` | Campaign plan | Six-act talk sequencing (pre-PD41) | §0–§2; print stack table |
| **7** | `3-Master_Plan/re_entry/_DISPOSABLE_paper_flipbook_PD30.md` | Working plan | Slide-level claims + red-pen status | § Slide deck Acts 0–VI |
| **8** | `transcripts/PD30_notes.md` | Meeting record | Big Fish demotion; paper P0 | Headline + priority stack |
| **9** | `transcripts/PD41_notes.md` | Meeting record | **Current** Alex priorities Sep 22 | Headline; H_sort table; P0–P2 |
| **10** | `3-Master_Plan/plans/20260721_hero_model_reset.plan.md` | Plan mirror | Pass A/B + three-layer vocabulary | §1 three layers; todos block |
| **11** | `3-Master_Plan/plans/20260615_pd12_compass_reassessment.plan.md` | Plan mirror | Measurements → predictions chain | § Trigger; Q1 verdict |
| **12** | `3-Master_Plan/re_entry/HEROs_and_PASSes/_DISPOSABLE_big_fish_datasets_assessment.md` | Portfolio assessment | Big Fish status B1–B5 | YOU ARE HERE table |
| **13** | `3-Master_Plan/re_entry/HEROs_and_PASSes/EDUCATION_dataset_primer.md` | Domain primer | Education claim limits | §5 interpret; §8 synthesis table |
| **14** | `3-Master_Plan/re_entry/_DISPOSABLE_CHARLES_VECTOR_handoff_checklist.md` | Status thread | Sep 16 VECTOR packaging state | YOU ARE HERE |
| **15** | `3-Master_Plan/VECTOR_work/COMPASS_Dissertation_Core_Deck_Materials_Questionnaire_COMPASS_draft.md` | Background inventory | Path archaeology (730+ lines) | Use as index, not linear read |
| **16** | `3-Master_Plan/COMPASS_AGENT_IDENTITY.md` | Agent spec | COMPASS boundaries | Full |
| **17** | `.specstory/history/2026-06-11_08-19-11-0400-compass.md` | Conversation archive | COMPASS birth; Path A/B; agent questions | **Chunk** per manifest §5 — do not ingest whole file |
| **18** | `.specstory/history/2026-09-15_15-17-14-0400-explore-repo-for-vector.md` | Conversation archive | Repo map for questionnaire | User prompt + path lists |
| **19** | `3-Master_Plan/obsolete/pre_tier1_locks/COMPASS_Initial_Guidance_v6.md` | Historical spec | Original COMPASS mission | § Mission; § Stage 3 |

**Alex transcripts (historical context — read after 1–10, not instead of):**

- `transcripts/PD29_notes.md` — tenure locks + 50/50 paper mandate  
- `transcripts/PD16_notes.md`, `PD21_notes.md`, `PD25_notes.md` — mechanism campaigns  
- Raw Otter: `transcripts/20260922_Paper_Directions_41_otter_ai_transcript.docx`

**Do not start with:** `1-Various_PDE_and_Chat_stuff/5-Manuscript/` (superseded for re-entry); whole-file COMPASS SpecStory without chunking.

---

## Source legend

| Label | Meaning |
|-------|---------|
| **Repo verifies** | File exists; COMPASS read header or full doc this session |
| **Conversation documents** | SpecStory or Otter transcript cited |
| **COMPASS infers** | Synthesis across multiple sources — verify before outline claims |
| **Unknown** | Needs Charles or domain agent |

---

## Thread log (this handoff)

| Date | Entry |
|------|-------|
| 2026-09-22 | Initial COMPASS handoff for VECTOR repo-connected onboarding (`COMPASS_HANDOFF_20260922.md`). |

---

*End of COMPASS handoff. For CODA / SCOUT / PEER history, read sibling files in `3-Master_Plan/VECTOR_work/agent_handoffs/` when available.*
