# PEER → COMPASS: Handoff Report (Academia / Tenure Domain)

> **Rename (2026-06-11):** Formerly `PEER_report_to_master_planner.md`; planning agent is **COMPASS**. See [COMPASS_AGENT_IDENTITY.md](COMPASS_AGENT_IDENTITY.md).

**Agent:** **PEER** (Cursor agent; R1 CS faculty tenure / Wayback scrape / OpenAlex / Cox survival research)  
**Domain root:** `./tenure/` (canonical code + data: `tenure/tenure_pipeline/`; root symlink: `tenure_pipeline/` → same tree)  
**Report date:** 2026-06-08  
**Prepared for:** Charles Levine → future **COMPASS** agent (Cursor)  
**Charles’s explicit instruction:** This report feeds the COMPASS. **Do not** begin drafting the cross-project master plan until Charles assigns that agent and asks for planning work.

---

## 0. What this document is (and is not)

### What it is
- A **ground-truth status snapshot** of the academia/tenure lane as PEER understands it after work through **June 2026** (pipeline Cells 0–9 complete, Cox wired, stage 9 inverted-U preliminary, advisor CSV, Dakota committee brief, Rivanna/conda/Git ops).
- A **research narrative** (§2) for a COMPASS with **zero prior context**: why academic careers and tenure matter, what PEER is testing, why the findings matter, and how the **inverted-U** links Army and basketball — not just file paths.
- A **file map** so the COMPASS can navigate without re-deriving context from chat logs or SpecStory `.md` exports alone.
- A **list of open questions** where Charles’s intent is not fully locked — PEER prefers explicit answers over assumptions.
- Pointers to **CODA** (Army), **SCOUT** (basketball), and **VECTOR** (manuscript) without claiming authority over those domains.

### What it is not
- **Not** the master plan itself.
- **Not** a promise that every figure is publication-ready (tenure is **Setting 3 — preliminary replication** relative to Army and basketball).
- **Not** a substitute for reading **`TENURE_PIPELINE_OVERVIEW.md`** when implementing or debugging cells in **`540_tenure_pipeline.ipynb`**.

---

## 1. Thesis frame (why PEER exists in this repo)

Charles’s dissertation tests whether **upward mobility** in nested talent pools follows a **nonlinear (inverted-U)** pattern: mid-quality peer environments produce the highest individual advancement rates; elite environments create **congestion / signal compression** that drives rates back down.

| Setting | Agent | Repo home | Outcome | Pool-quality construct |
|--------|-------|-----------|---------|-------------------------|
| 1 — Army | **CODA** | `talent/` | Promotion to Major vs attrition (competing risks) | Senior-rater pool minus mean (LOO-style), CIF panels |
| 2 — Basketball | **SCOUT** | `sports/` | NBA draft (`Y_draft`, LOO teammate quality) | `poolq_loo` (leave-one-out teammate PPM) |
| 3 — Academia | **PEER** | `tenure/` | Tenure (Asst → Assoc) vs attrition vs censoring | `poolq_loo_mean` (LOO dept assistant pub intensity) |

**PEER’s job:** Build a **reproducible scrape → parse → panel → OpenAlex → pool metrics → analysis** pipeline for R1 CS faculty; deliver **honest sample-loss accounting**; produce **preliminary third-setting evidence** for VECTOR’s manuscript without over-claiming relative to CODA/SCOUT maturity.

**Cross-setting manuscript doc (VECTOR + Charles, June 2026):**  
`1-Various_PDE_and_Chat_stuff/5-Manuscript/advancement_under_constrained_distinction_dakota_feedback_v03.rtf` — sent to dissertation committee member with tenure expertise (“Dakota”). Section 4 describes PEER setting in prose aligned with this report.

**Army research frame (Setting 1):** If the COMPASS has not read CODA’s handoff, start with **`3-Master_Plan/CODA_report_to_COMPASS.md` §2** for the originating inverted-U story (ranks, competing risks, CIF panels). PEER is Setting 3 of the same dissertation.

---

## 2. Academia research program — zero-background primer

*This section is for a COMPASS who has never seen the tenure data or Charles’s dissertation thread. Status, files, and open tasks are in §3 onward.*

### 2.1 Why academic careers — and why tenure specifically

**Academic careers are a canonical “nested talent pool” system.** Junior faculty are evaluated relative to peers in the same department and field; departments compete within universities and disciplines; promotion to **tenure** (typically Assistant → Associate Professor) is a **scarce, irreversible upward-mobility gate** — analogous to Army promotion boards and NBA draft slots.

**Why tenure matters for this dissertation:**

| Reason | Plain English |
|--------|---------------|
| **Third empirical setting** | Charles needs **three** domains for the dissertation bar (Army + basketball + academia), not a single-industry story. |
| **Public, partially replicable data** | Unlike proprietary Army OERs, faculty rosters (Wayback) and publications (OpenAlex) can be described and partially reproduced — strengthening the interdisciplinary claim. |
| **Advisor direction (Apr 2026)** | Alex Gates shifted priority from “scrape more schools” to **end-to-end measurement on existing data**: how many assistant→associate transitions, how much attrition, whether the **inverted-U** is plausible before perfecting every linkage. |
| **Committee expertise** | Dakota (committee member) received the **`advancement_under_constrained_distinction_dakota_feedback_v03.rtf`** brief — academic careers are the setting where tenure norms, FTE scarcity, and peer comparison are most natural to a reader. |
| **Mechanism test** | If “mid-quality peer environments help individual advancement; elite environments compress signals and congest slots” is a **general** phenomenon, it should appear where **peer quality** is measured by **publication intensity** in **CS departments**, not only OER scores or PPM. |

**What tenure is in this pipeline:** Not a legal contract analysis — an **observable rank transition** (assistant professor → associate professor within a tolerance window) inferred from archived faculty web pages over ~2000–2024. **Attrition** = assistant disappears without that promotion (competing outcome, with known limitation: lateral moves look like attrition). **Censoring** = still assistant at end of window.

### 2.2 Research question (plain English)

**Does individual tenure success depend nonlinearly on the quality of one’s peer reference pool?**

Specifically: among CS assistant professors at R1 universities, does **leave-one-out mean publication intensity of same-department assistant peers** (`poolq_loo_mean`) predict **tenure rate** in a **non-monotone (inverted-U)** way — lowest rates in weak peer environments, rising through mid/strong environments, then **falling again in the most elite peer environments**?

That is the **same qualitative target** as Army (promotion vs senior-rater pool quality) and basketball (draft vs LOO teammate quality). The parallel is **strategic** (nested pools, finite distinction capacity), not a claim that tenure probability equals promotion hazard or draft odds.

### 2.3 Setting, population, and constructs

| Element | Academia (PEER) implementation |
|--------|--------------------------------|
| **Population** | Computer science faculty at **R1** universities — **168** departments in `PILOT_SCHOOLS` (`r1_schools_data.py`) |
| **Analysis focus** | Faculty observed as **assistant professor** at least once (~2,330 persons in current panel) |
| **Individual performance** | Annual publications (`pubs_year`) and cumulative pubs from **OpenAlex** (primary); DBLP as cross-check spine |
| **Peer pool** | Same **department × year**: other **assistant** professors with OpenAlex linkage |
| **Pool quality (LOO)** | **`poolq_loo_mean`** — mean annual pubs of pool peers **excluding self** (leave-one-out), analogous to Army “pool minus mean” and SCOUT `poolq_loo` |
| **Primary outcome** | **`tenure_event`** — promotion to associate (or full) within `gap_tolerance=2` years |
| **Competing outcome** | **`attrition`** — left assistant rank without tenure event in window |
| **Right censoring** | **`censored`** — still assistant near end of data |
| **Data sources** | **Wayback Machine** HTML (historical rosters) + **OpenAlex** (publications); proprietary Army data **not** used here |

**Pipeline path:** Wayback CDX/download (Cells 3A–3E) → HTML parse (4) → longitudinal panel (5) → OpenAlex match (6A–6B) → enriched events (7) → LOO pools (8) → analysis (9+).

### 2.4 What we were looking for — and why it would matter if true

**What we were looking for:**

1. **A defensible longitudinal panel** with explicit **sample-loss accounting** at each filter (advisor requirement).
2. **A first empirical curve** — tenure rate vs binned pool quality — even if data are “dirty OK” (`TENURE_DATA_GAMEPLAN.md` fast path).
3. **Structural similarity to Army/basketball:** mid/upper bins outperform weak bins; **top bin dips** (elite-tier congestion).
4. **Formal survival models (next):** Cox with pool-quality linear + quadratic terms, paralleling Army Cell 12.

**Why findings would matter:**

| Audience | Why it matters |
|----------|----------------|
| **Dissertation committee** | Demonstrates the inverted-U is **not an Army artifact** — it survives in a public, knowledge-work setting with different performance metrics and institutions. |
| **Mechanism story (“advancement under constrained distinction”)** | Supports the idea that **being surrounded by strong peers helps up to a point**, then **hurts at the extreme** because distinction is **finite within a local comparison set** (promotion slots, draft picks, tenure lines). |
| **Literature** | Connects to promotion tournaments, relative performance evaluation, and organizational networks — framed for management science / people analytics / OR audiences (`Publication_Plan.md` in talent domain; Dakota brief for academic careers). |
| **Policy / practice (hedged)** | Departments and rating systems that assume “always hire/benchmark against the strongest peers” may face **diminishing or negative returns** at the elite tier — but PEER is **not yet causal**; this is a pattern claim. |

### 2.5 Two analysis layers (do not conflate)

#### Layer A — Cell 9: **Preliminary binned inverted-U** (current signature figure)

- **What:** 18 **equal-width bins** of `poolq_loo_mean`; **tenure rate** = tenure events / (tenure + attrition) per bin; Wilson 95% CIs.
- **Artifacts:** `stage9_inverted_u.png`, `stage9_binned_table.csv`.
- **What we found (May 2026 run):**
  - Weak pools (bins 1–2): tenure rates ~**0.30–0.35**
  - Mid rise (e.g. bins 3, 7, 9–11): ~**0.49–0.56**
  - Strong pools (bins 16–17): peak ~**0.67–0.70** (LOO median ~8–9 pubs/yr among peers)
  - **Elite-tier dip (bin 18):** ~**0.42** (LOO median ~12.7 pubs/yr) ← **inverted-U feature**
- **Honest label:** **Preliminary / unconditional** — no dept fixed effects, no individual controls, no formal p-values on curvature.

#### Layer B — Cells 10 / 10.5 / 12: **Cox survival** (wired, not yet reported)

- **Intent:** Time-to-tenure with time-varying pool metrics; z-scored covariates + **quadratic** + interaction (mirroring Army).
- **Status:** Intervals and z-scored frame exist; **Cell 12 model fit and HR tables not yet archived**.
- **Competing risks:** Attrition flag exists; **Fine-Gray / explicit competing-risks Cox not yet estimated** — same honesty as CODA handoff on estimands.

**Conceptual bridge:** Stage 9 answers “what does the **binned tenure curve** look like by dept peer quality?” Cox (when run) answers “holding time and covariates fixed, what are **hazard ratios** for pool quality and curvature?”

### 2.6 Cross-domain replication status (June 2026)

| Setting | Agent | Outcome | Pool construct | Inverted-U status |
|---------|-------|---------|----------------|-------------------|
| Army officers | **CODA** | CPT→MAJ promotion (vs attrition) | Senior-rater LOO pool TB | **Established** — CIF panels + Cox |
| College basketball | **SCOUT** | NBA draft | LOO teammate `poolq_loo` | **Replicated** |
| Academic tenure | **PEER** | Asst → Assoc tenure | LOO dept `poolq_loo_mean` | **Preliminary** — stage 9 bins |

Charles’s dissertation requires **all three** in one manuscript (Charles confirmed 2026-06-08; §11). PEER is the **least mature** quantitatively but provides the **knowledge-work / public-data** leg of the triad.

### 2.7 What we can and cannot claim today

**Can claim (with caveats):** Preliminary unconditional binned tenure rates show a **non-monotone** pattern with a **drop in the top pool-quality bin**, structurally similar to Army Q-bin CIF panels and basketball ventile charts.

**Cannot yet claim:** Formal Cox HRs; causal effects; full R1-universe representativeness; robustness across alternative peer definitions (citations, subfield, broader cohort).

**Manuscript-ready framing:** See **`PEER_Status_Update_for_VECTOR_2026-06-03.md` §6** for supported vs hedged sentences.

### 2.8 Known limitations (COMPASS should not bury these)

- **OpenAlex linkage partial:** ~58% of person–years `match_confidence=NONE`; pool quality itself depends on matched peers.
- **High censoring:** ~58% of ever-assistant persons still censored; small N per bin (~18–46 resolved cases).
- **168 schools ≠ 168 equal quality:** parse depth, URL health, and OA linkage vary enormously — distinguish **roster breadth** from **inference sample**.
- **Attrition vs lateral move:** Wayback cannot always distinguish leaving academia from moving institutions.
- **Title parsing noise:** e.g. “adjunct assistant professor” may misclassify rank — affects tenure-track filtering.

### 2.9 Where to read more (research, not just status)

| Document | Content |
|----------|---------|
| **`tenure/documents/TENURE_DATA_GAMEPLAN.md`** | Strategic contract: outcomes, advisor direction, stage map, inverted-U fast path |
| **`tenure/documents/Pertinent_Thoughts_Tenure.md`** | Stage 9 pattern, limitations, parser/coverage notes |
| **`5-Manuscript/PEER_Status_Update_for_VECTOR_2026-06-03.md`** | VECTOR handoff: binned results, caveats, manuscript sentences |
| **`5-Manuscript/advancement_under_constrained_distinction_dakota_feedback_v03.rtf`** | External committee brief — §4 = academic setting |
| **`3-Master_Plan/CODA_report_to_COMPASS.md` §2** | Army originating research narrative |
| **`talent/documents/Publication_Plan.md` §0** | Cross-domain replication status and mechanism roadmap |
| **`tenure/documents/TENURE_PIPELINE_OVERVIEW.md`** | Full cell wiring and file schemas |

---

## 3. Current status — tenure / PEER (high level)

### Established / working (end-to-end for current corpus)

| Layer | Status | Primary artifacts |
|-------|--------|-------------------|
| Scrape plan + download | ✅ | `faculty_snapshots_plan.jsonl`, HTML tree under `faculty_snapshots/` |
| Parse | ✅ | `faculty_snapshots_parsed.jsonl`, `faculty_snapshots_strategy_audit.jsonl` |
| Longitudinal panel | ✅ | `faculty_panel.jsonl` (~1.7 GB), `faculty_panel_collisions.jsonl` |
| OpenAlex 6A–6B | ✅ | `openalex_author_ids.jsonl`, `openalex_works_by_year.jsonl`, `openalex_snapshot_cache.jsonl` |
| Enriched panel (Cell 7) | ✅ | `faculty_panel_enriched.jsonl` (55 MB) |
| Pool metrics (Cell 8) | ✅ | `faculty_panel_with_pools.jsonl` (72 MB); `pool_metrics.py` |
| Stage 9 inverted-U | ✅ preliminary | `stage9_inverted_u.png`, `stage9_binned_table.csv` |
| Cox survival (Cells 10 / 10.5) | ✅ wired, not formally reported | `df_pipeline_09_filtered`, `df_pipeline_10_5_cox_zscored` |
| Advisor export (543) | ✅ | `faculty_panel_advisor.csv`, `R1_tenure_data.csv`; `543_package_panel.ipynb` |
| IPEDS enrollment viz (541) | ✅ | `school_enrollment_annual.csv`, `541_ipeds_enrollment.ipynb` |

### Panel scale (May 2026 run — re-verify after re-runs)

| Metric | Approximate value |
|--------|-------------------|
| Person–year rows | ~106,600 |
| Unique `faculty_id` | ~29,300 |
| `uni_slug` count | **168** (full pilot roster) |
| Years | 2000–2024 |
| Persons `ever_assistant=True` | ~2,330 |
| Person-level outcomes | tenure ~422; attrition ~570; censored ~1,340 |
| Row-level `match_confidence=HIGH` | ~17% |
| Row-level `match_confidence=NONE` | ~58% |

**Critical nuance for COMPASS:** **168 schools in panel ≠ 168 equally inference-ready departments.** Parse depth, assistant spell length, and OpenAlex linkage vary enormously. Early PEER docs sometimes said “~60 usable schools” — that reflected **quality** concerns, not the raw roster count. Master plan should distinguish **coverage breadth**, **parse quality**, and **inference sample**.

### Inverted-U (stage 9) — what we can and cannot claim

**Can claim (preliminary):** Unconditional binned tenure rates vs `poolq_loo_mean` show a **non-monotone** pattern with a **drop in the top bin** (bin 18: LOO median ~12.7 pubs/yr, tenure rate ~0.42 after peaks ~0.67–0.70 in bins 16–17). Structurally similar to Army/basketball “elite tier dip.”

**Cannot yet claim:**
- Formal Cox hazard ratios or p-values on pool-quality quadratic terms
- Causal interpretation
- Full R1-universe representativeness
- Robustness across alternative peer definitions

**Manuscript-ready sentence (VECTOR draft):** See **`PEER_Status_Update_for_VECTOR_2026-06-03.md` §6**.

### Not done / open

- **Cell 12 Cox output** — run and archive HR tables, inverted-U test on `z_pool_minus_mean_snr_fwd_sq`
- **Fine-Gray / explicit competing risks** — flags exist; formal model not estimated
- **School prestige covariate** — NRC / USNews merge not in panel
- **Subfield heterogeneity** — not implemented
- **URL / parse QA pass** — ongoing (`url_update_worksheet.csv`, `discover_faculty_urls.py`)
- **Formal master plan** — deferred until Charles assigns COMPASS

---

## 4. Infrastructure — Git, conda, Rivanna (PEER-relevant)

Charles runs a **monorepo** (`Cursor Workspace PDE/`) containing `talent/`, `sports/`, `tenure/`, and manuscript docs. PEER-specific ops:

| Topic | Doc | Notes |
|-------|-----|-------|
| Git + `.gitignore` | `WORKSPACE_CLEANUP_ROADMAP.md`, `PHASE1_GIT_NEXT_STEPS.md` | Large trees (`faculty_snapshots/`, JSONL) gitignored; code + docs tracked |
| Conda env | `environment-tenure_net.yml` (repo root) | Cross-platform spec; Rivanna: `sbatch myjob.slurm` pattern |
| HPC setup | `HPC_SETUP_CHECKLIST.md` | rsync data, OpenAlex CDH path, Slurm |
| Remote SSH + workspace | `RIVANNA_CURSOR_REMOTE_SSH_FOR_DUMMIES.md` | `Rivanna.code-workspace`, Ivy_Net clone |
| Streamlining digest | `TENURE_STREAMLINING_AND_RESEARCH_PRIORITIES.md` | conda vs Git vs folders; updated Part 3 June 2026 |

**OpenAlex on Rivanna:** CDH bulk snapshot at `~/cdh/OpenAlex1125/` (when mounted); **`build_openalex_cache.py`** + **`openalex_snapshot_cache.jsonl`** for incremental cache. Mac: rsync cache, run Cells 7–9 offline.

**SpecStory:** Charles syncs chat history to cloud; `.specstory/history/*.md` in repo. PEER threads may appear as `peer`, `coda`, `scout` in filenames — not a substitute for this handoff doc.

---

## 5. Pipeline architecture (540 conductor)

**Notebook:** `tenure/540_tenure_pipeline.ipynb` (root symlink: `540_tenure_pipeline.ipynb`).

**Design principles:** (1) append-only JSONL checkpoints, (2) resume-skip on re-run, (3) heavy logic in `tenure_pipeline/*.py`.

### Cell map (current)

| Cell | Purpose | Status |
|------|---------|--------|
| 0 | Flags, paths, imports | ✅ |
| 1 | DBLP parse (cross-check spine) | ✅ |
| 2 | R1 schools → CSV | ✅ |
| 3A–3E | CDX, download, rescues (UIUC, UW, NC State) | ✅ (3E spotty) |
| 4 | HTML parse | ✅ |
| 5 | Longitudinal panel | ✅ |
| 6A–6B | OpenAlex institution + authors + works | ✅ |
| 7 | Enriched panel | ✅ |
| 8 | LOO pool metrics | ✅ |
| 9 | Binned inverted-U | ✅ preliminary |
| 10 | Cox intervals / survival setup | ✅ wired |
| 10.5 | Z-score + quadratic + interaction | ✅ implemented |
| 12 | Model fit | ⏳ run pending |

**Related notebooks:**
- **`541_ipeds_enrollment.ipynb`** — IPEDS headcount for stage 3 viz
- **`543_package_panel.ipynb`** — CSV export for advisors

**Full cell semantics:** `tenure/documents/TENURE_PIPELINE_OVERVIEW.md` (rev 19, June 2026).

---

## 6. Key design decisions (tenure-specific)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data source | Wayback Machine HTML | Historical faculty rosters; no single API |
| Publication source | **OpenAlex** (primary); DBLP (cross-check) | Advisor direction Apr 2026; bulk on HPC |
| Panel grain | `(faculty_id × year)` | Matches survival / event-history framing |
| Tenure event | Asst → Assoc/Full within `gap_tolerance=2` | `panel_builder.py` |
| Outcomes | tenure / attrition / censored (mutually exclusive for ever-assistant) | Parallels Army competing risks |
| Pool definition | LOO mean `pubs_year` among **assistants** in same dept-year with OA data | Analogous to Army LOO OER, SCOUT LOO PPM |
| Rank capture | All titles parsed; filter at analysis | Flexibility; known adjunct/assistant confusion |
| Storage | Option B HTML paths + JSONL checkpoints | Re-parse cheap; re-download expensive |

---

## 7. PEER document inventory (updated June 2026)

| Document | Purpose | Current? |
|----------|---------|----------|
| **`TENURE_DATA_GAMEPLAN.md`** | Strategic contract, stage map, advisor direction, open points | ✅ Updated 2026-06-08 |
| **`TENURE_PIPELINE_OVERVIEW.md`** | Implementation map, cell wiring, file inventory | ✅ Rev 19, 2026-06-08 |
| **`Pertinent_Thoughts_Tenure.md`** | Dissertation-facing limitations + stage 9 notes | ✅ Updated 2026-06-08 |
| **`PANEL_CSV_GLOSSARY.md`** | Column definitions for advisor CSV | ✅ May 2026 |
| **`TENURE_STREAMLINING_AND_RESEARCH_PRIORITIES.md`** | Git/conda/HPC digest + research priorities | ✅ Part 3 updated 2026-06-08 |
| **`TARGET_WORKSPACE_TREE.md`** | Folder layout + symlinks | ✅ Includes 543 |
| **`WORKSPACE_CLEANUP_ROADMAP.md`** | Phased cleanup | ✅ Includes 543 |
| **`HPC_SETUP_CHECKLIST.md`** | Rivanna operations | ✅ Reference (ops) |
| **`DISCOVER_FACULTY_URLS_GUIDE.md`** | URL discovery tool | ✅ Reference |
| **`RIVANNA_CURSOR_REMOTE_SSH_FOR_DUMMIES.md`** | Remote dev | ✅ Reference |
| **`PHASE1_GIT_NEXT_STEPS.md`** | Git bootstrap | ✅ Reference |
| **`VA_WEEKEND_CHECKLIST.md`** | Weekend run checklist | ⚠️ Partially stale — many items now done; use stage table in overview instead |

### Manuscript / VECTOR-facing (outside `tenure/documents/` but PEER-authored or PEER-relevant)

| Document | Purpose |
|----------|---------|
| **`5-Manuscript/PEER_Status_Update_for_VECTOR_2026-06-03.md`** | VECTOR handoff: status, inverted-U, caveats, framing |
| **`5-Manuscript/advancement_under_constrained_distinction_dakota_feedback_v03.rtf`** | Committee brief (Dakota); §4 = academic setting |
| **`5-Manuscript/Scout_Status_Update_for_VECTOR_Laszlo_Briefing_2026-06-02.md`** | SCOUT status (sister setting — read for cross-setting alignment) |

---

## 8. Code map (`tenure_pipeline/` essentials)

| Module / artifact | Role |
|-------------------|------|
| `r1_schools_data.py` | **Source of truth** — 168 `PILOT_SCHOOLS`, URLs |
| `html_parser.py` | Multi-strategy faculty page parser |
| `apply_url_updates.py` | URL worksheet → schools data |
| `discover_faculty_urls.py` | CDX wildcard URL discovery |
| `faculty_linker.py` | Cell 5 panel builder |
| `panel_builder.py` | Tenure / attrition / censoring logic |
| `openalex_resolver.py` | 6A–6B author match + confidence tiers |
| `build_openalex_cache.py` | HPC bulk cache builder |
| `pool_metrics.py` | Cell 8 LOO pool metrics |
| `stage9_analysis.py` | Cell 9 binned inverted-U |
| `viz_pipeline.py` | Stage diagnostic plots |
| `build_school_enrollment_from_ipeds.py` | IPEDS enrollment (541) |
| `functionsG_working.py` | Shared utilities (repo root import) |

**Key JSONL outputs:** see **`TENURE_DATA_GAMEPLAN.md`** durable files table.

---

## 9. Sister agents — what PEER knows (read their reports; don’t merge pipelines)

| Agent | Handoff / gameplan | PEER relationship |
|-------|-------------------|-------------------|
| **CODA** | `3-Master_Plan/CODA_report_to_COMPASS.md`, `talent/documents/TENURE_DATA_GAMEPLAN` analog = gameplan in talent | **Most mature** quantitative stack (`520` Cox + CIF). PEER adapts **competing-risk framing**, not the 520 code path. |
| **SCOUT** | `sports/documents/SPORTS_DATA_GAMEPLAN.md`, `Scout_Status_Update_for_VECTOR_*.md` | **Replicated** inverted-U on basketball; generative congestion modeling advanced. PEER stage 9 is **cruder** (unconditional bins only). |
| **VECTOR** | `5-Manuscript/*.md`, ScholarGPT (external) | Owns manuscript prose. PEER supplies **Setting 3** facts, figures, limitations. |

**Agent reports:** `{AGENT}_report_to_COMPASS.md` in `./3-Master_Plan/` — CODA, SCOUT, PEER complete; VECTOR consumes via `5-Manuscript/` and status docs.

---

## 10. Harmonization notes for COMPASS (language only — not code merge)

These are **conceptual** links across settings; implementations differ by necessity.

| Concept | Army (CODA) | Basketball (SCOUT) | Academia (PEER) |
|---------|-------------|-------------------|-----------------|
| Individual performance | OER / TB metrics | PPM, draft outcome | `pubs_year`, `pubs_cumulative` |
| Pool | Senior-rater board | Teammates (team-season) | Dept assistants (uni-year) |
| LOO peer quality | Pool minus mean SNR | `poolq_loo` | `poolq_loo_mean` |
| Primary outcome | Promotion / attrition (CR) | `Y_draft` | `tenure_event` / `attrition` / `censored` |
| Elite-tier dip | CIF Q-bins | Ventile bar chart | Stage 9 bins 16–18 |
| Maturity | Highest | High (empirical + generative) | **Preliminary** |

**Manuscript framing (VECTOR + Dakota brief):** “Advancement under constrained distinction” — developmental benefits vs competitive constraints; **finite distinction capacity** within local comparison sets. PEER’s attrition + censoring parallel Army’s competing risks; basketball is sparser on attrition.

---

## 11. Clarifying questions for Charles — COMPASS update (2026-06-11)

**COMPASS assigned.** Charles locked several items; PEER still needs answers on open rows.

| # | Topic | Status |
|---|--------|--------|
| 1 | COMPASS identity | **Assigned** — cross-project planner COMPASS |
| 2 | Single paper vs chapters | **One manuscript** (all settings) — CODA §10 |
| 3 | Tenure maturity target | **Resolved — soft gate:** stage 9 + limitations → start VECTOR prose; one Cell 12 Cox parallel before submission |

**Still open:**

4. **OpenAlex confidence policy:** HIGH only vs HIGH+MEDIUM vs MULTI with disclaimer?
5. **Coverage expansion vs analysis lock-in:** Resume scraping or freeze corpus on current 168?
6. **Prestige controls:** NRC/USNews vs subfield vs neither for v1?
7. **Advisor CSV (`R1_tenure_data.csv`):** Canonical external share vs filtered inference export?
8. **Rivanna vs Mac division** for Cell 12 execution?
9. **Monorepo vs split repos?**
10. **Dakota feedback loop:** PEER pipeline changes vs VECTOR prose-only first?

---

## 12. Suggested first tasks for COMPASS

*Several items below are **done** (2026-06-11); remainder is living work.*

1. Collect all four `{AGENT}_report_to_COMPASS.md` files (CODA done; PEER this file; SCOUT/VECTOR TBD).
2. Read **`advancement_under_constrained_distinction_dakota_feedback_v03.rtf`** as the current **external-facing** synthesis.
3. Build a **maturity matrix**: figure ready / model ready / manuscript paragraph ready — per setting.
4. Resolve **shared glossary** for “pool quality,” “LOO,” “congestion,” “inverted-U” across CODA/SCOUT/PEER docs.
5. Timeline: VECTOR may draft Setting 3 on stage 9 now; PEER Cell 12 Cox in parallel before submission.
6. Git + data policy: what COMPASS treats as **release artifacts** vs **local-only** (snapshots, cache JSONL).

---

## 13. Agent identity note

This report was authored by **PEER** in Cursor sessions covering tenure pipeline work with Charles (540 cells, stage 9 inverted-U, 543 advisor CSV, glossary, Rivanna env, SpecStory workflow, document updates for COMPASS handoff). If Charles intended a different agent name for this thread, relabel this file accordingly.

---

*End PEER handoff. COMPASS active — see `PROJECT_STATUS_AND_NEAR_TERM_PLAN.md` and `20260611_0826_COMPASS_to_PEER_questions.md`.*
