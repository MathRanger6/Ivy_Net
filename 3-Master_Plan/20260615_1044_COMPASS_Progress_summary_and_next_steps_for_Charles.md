# COMPASS → Charles: Progress summary & next steps

**Date:** 2026-06-15 10:44  
**From:** COMPASS  
**To:** Charles Levine (+ CODA, PEER, SCOUT, VECTOR for read receipt)  
**Trigger:** All five agents filed **STANDING BY** (Round 5 complete). Charles requested ordered summary and forward plan.

**Agent STANDING BY files (source of truth for per-agent questions):**

| Agent | File |
|-------|------|
| CODA | [`20260615_1040_CODA_STANDING_BY_with_Qs_for_Charles.md`](20260615_1040_CODA_STANDING_BY_with_Qs_for_Charles.md) |
| PEER | [`20260615_1038_PEER_STANDING_BY_with_Qs_for_Charles.md`](20260615_1038_PEER_STANDING_BY_with_Qs_for_Charles.md) |
| SCOUT | [`20260615_1038_SCOUT_STANDING_BY_with_Qs_for_Charles.md`](20260615_1038_SCOUT_STANDING_BY_with_Qs_for_Charles.md) |
| VECTOR | [`20260615_1130_VECTOR_STANDING_BY_with_Qs_for_Charles.md`](20260615_1130_VECTOR_STANDING_BY_with_Qs_for_Charles.md) |
| COMPASS | [`20260615_1040_COMPASS_STANDING_BY_with_Qs_for_Charles.md`](20260615_1040_COMPASS_STANDING_BY_with_Qs_for_Charles.md) |

---

## 1. Executive summary — where we are

### Correspondence experiment (Rounds 1–5)

**Outcome: success.** All domain agents declare **mutual understanding** and **no scientific conflicts**. Every agent is **waiting on Charles** (SCOUT also needs your explicit **go** before coding D10 — not waiting on another agent).

| Milestone | Status |
|-----------|--------|
| Jun 11 COMPASS Q&A (`1626` round) | ✅ All five agents answered |
| Cross-agent mail (Rounds 1–4) | ✅ Complete |
| SCOUT Tier 2 stop rule | ✅ [`1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) |
| VECTOR claim language + M1–M5 | ✅ [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) |
| All agents STANDING BY | ✅ Five files (table above) |
| **Manuscript draft** | ⏳ Blocked on **your Tier A batch** + SCOUT D10 + PEER inference export |

### Scientific consensus (locked — do not relitigate)

```text
Question     →  Does LOO peer-pool quality relate nonlinearly to upward mobility?
Phenomenon   →  Inverted-U (mid/strong pools up, elite tier dip)
Settings     →  Army ✅ established | Basketball ✅ replicated | Tenure ⚠️ preliminary
Architecture →  Path II: basketball generative POC (mechanism) +
                  Army + tenure empirical legs (no generative LOO match for v1)
Predictions  →  #1 Near-threshold heterogeneity (SCOUT export + Army panel)
                  #2 Peak shift with global Λ (Army-led prose; TBD figure)
Paper          →  Paper first; dissertation packaging second
Timeline       →  Summer–Fall 2026 core manuscript draft/submission
```

**Tier 2 stop rule (Alex one-liner)** — from SCOUT closure §7:

> We call the minimal model complete when the basketball generative score POC is frozen in a manuscript export bundle — talent-only fails, congestion-in-score bends curves on pool mean, axis table and limitation prose on disk — while Army and tenure stay empirical inverted-U legs at honest maturity, without generative LOO bin-for-bin match.

**SCOUT closure checklist today:** 3 green · 4 yellow · 0 red → **5 green after D10 bundle**.

### Deliverables on disk vs still owed

| Deliverable | Status | Owner | Your lock |
|-------------|--------|-------|-----------|
| Claim language table | ✅ | VECTOR | Accept or edit [`1100`](20260615_1100_VECTOR_claim_language_table.md) |
| SCOUT D10 export bundle | ❌ | SCOUT | **Q-D10 go** + **Q-SCOUT-9** path |
| PEER `faculty_panel_inference_v1.csv` | ❌ | PEER | **C1–C2** |
| Army canonical figure list | ⏸ | CODA | **C-AWS-1** (after AWS sync) |
| Manuscript §1–§5 prose | ❌ | VECTOR | After D10 + C1–C2 (+ claim table accepted) |
| Tenure Layer B Cox | ⏸ pre-submission | PEER | **R1** when you route |
| Pool-size algorithm audit | ⏸ pre-publication | CODA | Deferred |
| 525 / UIC Army depth | ⏸ | CODA | Tabled |

### Primary risk (VECTOR + COMPASS agree)

Not missing ideas — **failure to converge on packaging and prose**. The bottleneck is **your decision batch**, then **1–2 SCOUT sessions (D10)** and **PEER export**, then **VECTOR drafting**.

---

## 2. Itemized plan — steps to move forward

### Phase 0 — You (today or one sitting, ~30–45 min)

**Goal:** Unlock all agents with one batch reply. Copy-paste block in §4.1.

| Step | Action | Unblocks |
|------|--------|----------|
| **0.1** | Send **Tier A batch** (§4.1) in chat or annotate this file | SCOUT D10, PEER export, VECTOR draft timing |
| **0.2** | Reply **“use agent defaults for Tier C”** (optional) | PEER C3–C11, SCOUT Q-C7–C8, etc. |
| **0.3** | Skim VECTOR claim table — reply **“claim table accepted”** or list edits | VECTOR prose discipline |
| **0.4** | Confirm **V1–V3** (VECTOR STANDING BY) or say “VECTOR defaults OK” | Manuscript priority lock |

### Phase 1 — Agent execution (after Phase 0; ~1 week wall-clock)

| Step | Owner | Task | Output |
|------|-------|------|--------|
| **1.1** | **SCOUT** | Implement D10 (`export_scout_manuscript_bundle_v1.py`) | `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/` — manifest, axis table, score one-pager, generative contrast PNGs, refreshed empirical Fig 2 slug |
| **1.2** | **PEER** | Apply C1 filter → write inference export | `tenure_pipeline/faculty_panel_inference_v1.csv` + filter manifest + N counts for VECTOR |
| **1.3** | **VECTOR** | Begin manuscript draft (per V3) | §1 empirical triad, §2 theory, §3 minimal model (use SCOUT ink rules + claim table §F), §5 limitations |
| **1.4** | **COMPASS** | Update [`20260611_1642_COMPASS_to_Charles.md`](20260611_1642_COMPASS_to_Charles.md) with closure greens + claim table status | Single rollup for committee prep |

**Parallel (no block):** VECTOR may draft §2 and §5 while waiting for D10; **§3 ink** should wait for D10 axis table on disk (or use SCOUT coherence doc with caveats already listed).

### Phase 2 — Alex meeting (schedule when ready)

**Prep docs:** [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md) · [`20260611_Brief_for_Alex_Gates_brief.md`](20260611_Brief_for_Alex_Gates_brief.md)

| Step | Topic | Question IDs |
|------|-------|--------------|
| **2.1** | Army estimand language (CIF vs Cox) | **C-ALEX-2** — draft in [`20260611_1633_CODA_to_COMPASS.md`](20260611_1633_CODA_to_COMPASS.md) §A.3 |
| **2.2** | TB-stratified CR panels | **C-ALEX-1** |
| **2.3** | Fine–Gray deferred OK? | **C-ALEX-3** |
| **2.4** | Manuscript-first / generative limitations | SCOUT closure §6 + VECTOR claim table |
| **2.5** | Optional: show Tier 2 stop rule one-screen checklist | [`1012`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) §1 |

### Phase 3 — Army AWS (when you sync from live environment)

| Step | Owner | Task | Question IDs |
|------|-------|------|--------------|
| **3.1** | **Charles** | Confirm TB-stratify 4-file upload | **C-AWS-2** |
| **3.2** | **Charles → CODA** | Canonical figure list (profile, Cell 11 spec, PNG names) | **C-AWS-1** |
| **3.3** | **VECTOR** | Lock Army panel caption / Figure 1 reference | After C-AWS-1 |
| **3.4** | **CODA** (if Alex says yes) | TB-stratify run on AWS | **R-TB-RUN** after C-ALEX-1 |

### Phase 4 — Manuscript iteration (weeks 2–6)

| Step | Owner | Task |
|------|-------|------|
| **4.1** | **VECTOR** | Full draft all sections; enforce claim table labels |
| **4.2** | **Charles + Alex** | Advisor read; revise claims per feedback |
| **4.3** | **SCOUT** | Optional: near-threshold figure refresh in bundle if VECTOR requests |
| **4.4** | **CODA** | Optional: **C-PUB-1** pool-size disclaimer in limitations if you want |
| **4.5** | **CODA** | Optional: **C-Λ-1** — paste Λ stub in §4 ([`1016_CODA_Round3`](20260615_1016_CODA_Round3_agent_mailbox.md) §4) |

### Phase 5 — Pre-submission (explicitly not draft blockers)

| Step | Owner | When |
|------|-------|------|
| **5.1** | **PEER** | Layer B Cox (`540` Cells 10–12) — reply **“route Layer B”** | **R1** |
| **5.2** | **CODA** | Senior-rater pool algorithm audit | **R-POOL-AUDIT** |
| **5.3** | **CODA** | Optional Army Λ empirical test | **R-Λ-EMPIR** |
| **5.4** | **PEER** | Prestige / subfield robustness | C10–C11 if elevated |
| **5.5** | **All** | 525/UIC Army mechanism meat | Only if manuscript needs it |

---

## 3. Mutual understanding dashboard (final)

| Agent | STANDING BY | Waits on Charles? | Waits on other agents? | Still owes work after your go? |
|-------|-------------|-------------------|-------------------------|--------------------------------|
| **CODA** | ✅ | Yes (AWS, Alex) | No | Only if you route R-* |
| **PEER** | ✅ | Yes (C1–C2) | No | Inference CSV after C1–C2 |
| **SCOUT** | ✅ | Yes (Q-D10, Q-SCOUT-9) | No | D10 after **go** |
| **VECTOR** | ✅ | Yes (V1–V3 confirm) | No | Manuscript draft after locks |
| **COMPASS** | ✅ | Yes (this plan) | No | Rollup update after Phase 1 |

**Correspondence experiment:** COMPASS recommends **declare complete** unless you want Round 6 for audit only.

---

## 4. Your questions — merged and ordered

*Answer in chat, annotate agent STANDING BY files, or reply to sections below. **Tier A first** unlocks the most work.*

### 4.1 Copy-paste batch — Tier A (recommended first message)

```text
Charles batch — Tier A (2026-06-15):

PEER: C1 = HIGH+MEDIUM primary; HIGH-only robustness; exclude MULTI from primary
PEER: C2 = R1_tenure_data.csv + faculty_panel_inference_v1.csv (paths as PEER STANDING BY)

SCOUT: Q-SCOUT-9 = datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/
SCOUT: Q-D10 = go
SCOUT: Q-C7-C8, Q-FIG2, Q-C12, Q-C13 = confirmed / use defaults

VECTOR: V1–V3 = yes (manuscript-first; predictions #1 and #2; draft after D10 + PEER C1–C2)
VECTOR: claim table accepted (or: [edits])

Optional: use agent defaults for Tier C (PEER C3–C11, etc.)
```

### 4.2 Tier A — unblock execution (detail)

| ID | Question | Agent | Recommendation | Source |
|----|----------|-------|----------------|--------|
| **C1** | OpenAlex tier for tenure inference v1 | PEER | HIGH+MEDIUM primary; HIGH-only robustness; exclude MULTI | PEER `1038` |
| **C2** | Release artifact names | PEER | `R1_tenure_data.csv` + `faculty_panel_inference_v1.csv` | PEER `1038` |
| **Q-SCOUT-9** | D10 bundle directory | SCOUT | `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/` | SCOUT `1038` |
| **Q-D10** | Go on SCOUT D10 implementation? | SCOUT | **go** (1–2 sessions packaging) | SCOUT `1038` |
| **V1** | Manuscript-first; defer broad dissertation planning? | VECTOR | Yes | VECTOR `1130` |
| **V2** | Primary predictions = near-threshold + Λ peak-shift? | VECTOR | Yes | VECTOR `1130` |
| **V3** | VECTOR draft after D10 + PEER C1–C2? | VECTOR | Yes | VECTOR `1130` |
| **—** | Accept VECTOR claim table? | VECTOR | Review [`1100`](20260615_1100_VECTOR_claim_language_table.md) | — |

### 4.3 Tier B — Alex meeting (Army + cross-cutting prose)

| ID | Question | Agent | Recommendation | Source |
|----|----------|-------|----------------|--------|
| **C-ALEX-1** | TB-stratify panels: main / supplement / defer? | CODA | Defer (default off) | CODA `1040` |
| **C-ALEX-2** | Sign-off estimand sentences (CIF vs Cox)? | CODA | Review `1633` §A.3 | CODA `1040` |
| **C-ALEX-3** | Fine–Gray deferred OK in Army prose? | CODA | Yes | CODA `1040` |
| **C-Λ-1** | Use Λ stub in VECTOR §4 now vs wait for Army test? | CODA/VECTOR | Prose OK with “conceptual / TBD figure” | CODA `1040` |

### 4.4 Tier C — accept defaults? (optional one-liner: “use agent defaults for Tier C”)

| ID | Question | Agent | Default |
|----|----------|-------|---------|
| **C3** | Tenure N prose (168 roster + inference N) | PEER | Both |
| **C4** | Freeze corpus vs scrape more | PEER | Freeze + targeted URL fixes |
| **C10–C11** | Prestige / subfield controls | PEER | Defer |
| **Q-C7–C8** | Fig 2 PPM z + ventiles | SCOUT | Yes |
| **Q-FIG2** | June-dated Fig 2 in D10 | SCOUT | Yes if D10 go |
| **G1–G3** | Stage 9 OK for draft; Layer B pre-submission; Fine–Gray defer tenure | PEER | Locked |

### 4.5 Tier D — paused until AWS or pre-submission

| ID | Question | Agent | When |
|----|----------|-------|------|
| **C-AWS-1** | Canonical Army figure list | CODA | After AWS sync |
| **C-AWS-2** | TB-stratify 4-file AWS upload done? | CODA | You confirm yes/no |
| **C-PUB-1** | Pool-size disclaimer in draft limitations? | CODA | Optional now |
| **R1** | Route PEER Layer B Cox build | PEER | Pre-submission |
| **R-POOL-AUDIT** | Army pool-size audit | CODA | Pre-publication |
| **R-Λ-EMPIR** | Army Λ empirical test | CODA | Post-draft unless elevated |

### 4.6 Tier E — low priority (no action needed unless you care)

| ID | Topic | Default |
|----|-------|---------|
| **P1** | Monorepo vs split repos | Monorepo OK (PEER) |
| **P2** | Dakota → PEER code vs VECTOR prose first | Prose first (PEER) |
| **Q-COMPASS-3** | Declare correspondence experiment complete? | COMPASS: **yes**, now that all STANDING BY filed |

---

## 5. What each agent does after your Tier A batch

| Agent | Immediate next action |
|-------|----------------------|
| **SCOUT** | Build D10 bundle → ping VECTOR when `scout_manuscript_v1/manifest.json` exists |
| **PEER** | Write `faculty_panel_inference_v1.csv` → send N footnote to VECTOR |
| **VECTOR** | Start §1–§5 draft using claim table + Dakota spine |
| **CODA** | Hold unless C-AWS-1 un-paused or Alex answers Tier B |
| **COMPASS** | Update `1642` rollup; track Phase 1 completion |

---

## 6. Key reference documents (manuscript stack)

| Role | Document |
|------|----------|
| Section spine | `5-Manuscript/advancement_under_constrained_distinction_dakota_feedback_v03.rtf` |
| Claim discipline | [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) |
| §3 mechanism / ink rules | [`20260611_1640_SCOUT_to_COMPASS_model_coherence.md`](20260611_1640_SCOUT_to_COMPASS_model_coherence.md) + [`1012`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) §6 |
| Army methods drafts | [`20260611_1633_CODA_to_COMPASS.md`](20260611_1633_CODA_to_COMPASS.md) §A.3 |
| Near-term plan (context) | [`PROJECT_STATUS_AND_NEAR_TERM_PLAN.md`](PROJECT_STATUS_AND_NEAR_TERM_PLAN.md) |

---

## 7. COMPASS completion statement

> **Cross-agent alignment is complete. The project center of gravity is Charles’s Tier A batch (§4.1), then SCOUT D10 + PEER inference export, then VECTOR manuscript drafting. Army AWS figures and Alex sign-offs parallelize with drafting; pre-submission work (Layer B, pool audit) stays deferred.**

**Correspondence experiment:** **Complete** pending your acknowledgment.

---

*End COMPASS progress summary. Charles: reply with §4.1 batch when ready.*
