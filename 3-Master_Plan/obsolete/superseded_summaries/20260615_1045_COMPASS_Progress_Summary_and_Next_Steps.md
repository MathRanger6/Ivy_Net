# COMPASS — Progress summary & next steps (post–STANDING BY)

**Date:** 2026-06-15 10:45  
**From:** COMPASS  
**To:** Charles (+ CODA, PEER, SCOUT, VECTOR for reference)  
**Trigger:** All agents filed **STANDING BY**; Charles requested ordered summary and forward steps.

**Source files merged:**

- [`20260615_1038_SCOUT_STANDING_BY_with_Qs_for_Charles.md`](20260615_1038_SCOUT_STANDING_BY_with_Qs_for_Charles.md)
- [`20260615_1038_PEER_STANDING_BY_with_Qs_for_Charles.md`](20260615_1038_PEER_STANDING_BY_with_Qs_for_Charles.md)
- [`20260615_1040_CODA_STANDING_BY_with_Qs_for_Charles.md`](20260615_1040_CODA_STANDING_BY_with_Qs_for_Charles.md)
- [`20260615_1130_VECTOR_STANDING_BY_with_Qs_for_Charles.md`](20260615_1130_VECTOR_STANDING_BY_with_Qs_for_Charles.md)
- [`20260615_1040_COMPASS_STANDING_BY_with_Qs_for_Charles.md`](20260615_1040_COMPASS_STANDING_BY_with_Qs_for_Charles.md)
- Correspondence arc: Jun 11 `1626` Q&A → Rounds 1–5 → [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md)

---

## 1. Where we are (executive summary)

### Correspondence experiment — **success**

Five agents ran **five rounds** of cross-agent mail in `3-Master_Plan/`. Outcome:

| Result | Status |
|--------|--------|
| Jun 11 COMPASS Q&A (`1626` → all agents) | ✅ Complete |
| Cross-agent scientific disputes | **None** |
| Mutual understanding (all agents) | ✅ Declared |
| VECTOR claim language table + M1–M5 | ✅ [`1100`](20260615_1100_VECTOR_claim_language_table.md) |
| SCOUT Tier 2 stop rule / closure checklist | ✅ [`1012`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) |
| All agents **STANDING BY** | ✅ Five files on disk |

**The project is no longer blocked by “what is the model?” or “do agents agree?”** It is blocked by **your decisions** (locks) and **packaging execution** (SCOUT D10, PEER inference export, VECTOR prose).

### Scientific architecture (locked — do not relitigate)

```text
Wang ladder (v1 manuscript)
├── Rung 1  Empirical triad — inverted-U on LOO peer-quality proxy
│           Army ✅ established  |  Basketball ✅  |  Tenure ⚠️ preliminary (stage 9)
├── Rung 2  Minimal generative — basketball only (Path II)
│           Score S_i = A_i − λ·L_{C,LOO}; talent-only fails; pool-mean readout POC
│           NOT bin-for-bin LOO-pool-quality generative match
└── Rung 3  Predictions
            #1 Near-threshold heterogeneity (SCOUT export + Army panel)
            #2 Peak shift with global Λ (CODA prose hook; no Λ-sweep figure yet)
```

**Tier 2 stop rule (Alex one-liner):** Basketball generative POC frozen in export bundle — talent-only fails, congestion bends curves on pool mean, axis table + limitation prose on disk — Army and tenure stay empirical legs at honest maturity.

**Checklist today:** 3 green · 4 yellow · 0 red → **5 green after SCOUT D10**.

**Manuscript stack (VECTOR):** Dakota v03 RTF (spine) · Tier1 narrative (voice) · Alex sequential outline (methods order). **Paper first; dissertation second.**

### Primary risk (VECTOR, all agents concur)

Not missing ideas — **failure to converge** on completed minimal model, clear prediction story, and publishable draft. Favor **convergence over expansion**.

---

## 2. Deliverables status

| Deliverable | Owner | Status | Blocker |
|-------------|-------|--------|---------|
| Domain handoff reports (`*_report_to_COMPASS`) | All | ✅ Jun 8 | — |
| Jun 11 numbered Q&A responses | All | ✅ | — |
| SCOUT model coherence + nesting chain | SCOUT | ✅ `1640` | — |
| SCOUT minimal-model closure | SCOUT | ✅ `1012` | — |
| VECTOR claim language table | VECTOR | ✅ `1100` | — |
| **SCOUT D10 export bundle** | SCOUT | ❌ Not built | Charles **Q-D10 go** + **Q-SCOUT-9** |
| **PEER inference CSV** | PEER | ❌ Not built | Charles **C1–C2** |
| Army canonical figure list | CODA | ⏸ Paused | Charles **C-AWS-1** (AWS sync) |
| VECTOR manuscript §1–§5 draft | VECTOR | ⏳ Ready to start | SCOUT D10 + PEER C1–C2 preferred |
| Update [`20260611_1642_COMPASS_to_Charles.md`](20260611_1642_COMPASS_to_Charles.md) | COMPASS | ⏳ | After your Tier A batch |

---

## 3. Itemized steps to move forward

### Phase A — Your one sitting (~30 min): batch unlock

**Goal:** Unblock SCOUT packaging, PEER export, and VECTOR drafting in one message.

| Step | Action | You say / decide |
|------|--------|------------------|
| **A1** | Lock SCOUT bundle path | **Q-SCOUT-9:** `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/` *(recommended)* |
| **A2** | Authorize SCOUT D10 build | **Q-D10:** **go** (1–2 sessions packaging) |
| **A3** | Lock tenure inference policy | **C1:** HIGH + MEDIUM primary; **C2:** `R1_tenure_data.csv` + `faculty_panel_inference_v1.csv` |
| **A4** | Confirm manuscript locks | **C12–C13:** predictions #1/#2; Dakota / Tier1 / Alex stack *(VECTOR V1–V2)* |
| **A5** | Close soft defaults | **“Use agent defaults for Tier C”** — PEER C3–C11, SCOUT Q-C7-C8, Q-FIG2, G1–G3 |

**Copy-paste batch reply:**

```text
Tier A — go:
- Q-SCOUT-9: datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/
- Q-D10: go — SCOUT implement D10
- C1: HIGH + MEDIUM primary (HIGH-only robustness; exclude MULTI from primary)
- C2: R1_tenure_data.csv + faculty_panel_inference_v1.csv
- C12–C13 / V1–V2: confirmed — near-threshold + Λ; paper-first; begin VECTOR draft after D10 + PEER export
- Tier C: use agent defaults
```

---

### Phase B — Agent execution (after Phase A)

| Step | Agent | Task | Effort | Output |
|------|-------|------|--------|--------|
| **B1** | **SCOUT** | Build `export_scout_manuscript_bundle_v1.py` → D10 bundle | 1–2 sessions | Empirical Fig 2 (June slug), generative contrast PNGs, axis table, score one-pager, manifest |
| **B2** | **PEER** | Apply C1 filter → write `faculty_panel_inference_v1.csv` | ~1 session | Inference sample + N footnote for VECTOR |
| **B3** | **VECTOR** | Begin §1–§5 draft using claim table §F discipline | Ongoing | Manuscript prose; §3 after B1 lands |
| **B4** | **COMPASS** | Update `1642` rollup + `PROJECT_STATUS_AND_NEAR_TERM_PLAN.md` | 1 pass | Single Charles-facing status doc |

**Pre-delivered for B1 (no agent ping needed):**

- Army axis row: [`1019_CODA_to_SCOUT_round4`](20260615_1019_CODA_to_SCOUT_round4.md)
- Tenure axis row: [`1020_PEER_to_SCOUT_round4`](20260615_1020_PEER_to_SCOUT_round4.md)

---

### Phase C — Alex meeting (Army prose — Tier B)

**Goal:** Finalize Setting 1 methods language before submission-quality Army section.

| Step | Question | Prep | Default |
|------|----------|------|---------|
| **C1** | **C-ALEX-1** TB-stratify panels: main / supplement / defer? | [`Alex_Gates_Talking_Points`](20260611_Alex_Gates_Talking_Points.md) | Defer |
| **C2** | **C-ALEX-2** Sign-off estimand sentences (CIF vs Cox)? | [`1633` §A.3](20260611_1633_CODA_to_COMPASS.md) | Needed before Army Methods “final” |
| **C3** | **C-ALEX-3** Fine–Gray deferred OK in prose? | Talking points | Yes |
| **C4** | **C-Λ-1** Use CODA Λ stub in VECTOR §4 now? | [CODA R3 §4](20260615_1016_CODA_Round3_agent_mailbox.md) | Prose-only OK if labeled conceptual |

**Brief for Alex:** [`20260611_Brief_for_Alex_Gates_full.md`](20260611_Brief_for_Alex_Gates_full.md) · [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md)

---

### Phase D — AWS / Army figures (when sync allows)

| Step | Question | Agent | When |
|------|----------|-------|------|
| **D1** | **C-AWS-2** Upload done? (4-file TB-stratify set) | Charles | Before TB-stratify runs |
| **D2** | **C-AWS-1** Canonical Cell 11 profile + PNG filenames | CODA → VECTOR | After AWS sync |
| **D3** | Optional **R-TB-RUN** if Alex wants stratified panels | CODA on AWS | After C-ALEX-1 |

---

### Phase E — Pre-submission (explicitly not draft blockers)

| Step | Task | Agent | When |
|------|------|-------|------|
| **E1** | Layer B Cox in `540` (port Army `520`) | PEER | Charles: **“route Layer B”** |
| **E2** | Army pool-size algorithm audit | CODA / Charles | Pre-publication |
| **E3** | Empirical Army Λ-sweep figure | CODA | Post-draft if elevated |
| **E4** | Generative LOO-pool-quality match | SCOUT | Parallel science only |
| **E5** | Network extensions, mean×dispersion primary | All | Defer |

---

## 4. Your questions — merged & ordered

*Answer top-to-bottom. Tier A unblocks the most work per minute.*

### Tier 0 — Orchestration (COMPASS)

| ID | Question | Recommendation |
|----|----------|----------------|
| *(done)* | Create this summary? | ✅ This document |
| **Q-COMPASS-2** | Update `1642` rollup after you answer Tier A? | Yes — COMPASS will do after your batch reply |

---

### Tier A — **Do first** (unblocks SCOUT + PEER + VECTOR)

| ID | Agent | Question | Default |
|----|-------|----------|---------|
| **Q-SCOUT-9** | SCOUT | Bundle path: `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/` vs `3-Master_Plan/manuscript_exports/`? | Use `datasets/mbb/.../scout_manuscript_v1/` |
| **Q-D10** | SCOUT | **Go** on D10 export bundle (1–2 sessions)? | Hold until you say **go** |
| **C1** | PEER | OpenAlex tier: HIGH+MEDIUM primary? | HIGH + MEDIUM; exclude MULTI from primary |
| **C2** | PEER | Artifact names: `R1_tenure_data.csv` + `faculty_panel_inference_v1.csv`? | Confirm as named |
| **V1** | VECTOR | Immediate objective = minimal model → predictions → manuscript draft; defer dissertation planning? | **Yes** |
| **V2** | VECTOR | Primary predictions = near-threshold + Λ peak-shift? | **Yes** |
| **V3** | VECTOR | Begin prose after D10 + PEER C1–C2? | **Yes** — recommended |
| **C12** | SCOUT/VECTOR | Confirm prediction + outline locks (same as V2 + Dakota stack)? | Confirmed per `1700` + claim table |

---

### Tier B — Alex / Army (schedule meeting)

| ID | Agent | Question |
|----|-------|----------|
| **C-ALEX-1** | CODA | TB-stratify: main / supplement / defer? |
| **C-ALEX-2** | CODA | Estimand sentences sign-off (`1633` §A.3)? |
| **C-ALEX-3** | CODA | Cause-specific Cox only (no Fine–Gray) OK? |
| **C-Λ-1** | CODA/VECTOR | Λ stub in §4 now vs wait for Army empirical test? |

---

### Tier C — **Say “use agent defaults”** to skip

| ID | Agent | Topic | Default |
|----|-------|-------|---------|
| **Q-C7-C8** | SCOUT | Fig 2: PPM z within-season + ventiles | Yes |
| **Q-FIG2** | SCOUT | June-dated Fig 2 in D10 | Yes if D10 go |
| **C3** | PEER | Report 168 roster + inference N both | Both |
| **C4** | PEER | Freeze corpus + targeted URL fixes | Freeze |
| **C10–C11** | PEER | Prestige controls; subfield heterogeneity | Defer |
| **G1–G3** | PEER | Stage 9 draft OK; Layer B pre-submission; no Fine–Gray | Locked |
| **C-PUB-1** | CODA | Pool-size disclaimer in limitations now? | Optional / defer |

---

### Tier D — AWS (when ready)

| ID | Agent | Question |
|----|-------|----------|
| **C-AWS-1** | CODA | Canonical Army figure profile + filenames after sync |
| **C-AWS-2** | CODA | AWS 4-file upload done? (yes/no) |

---

### Tier E — Route explicitly when wanted

| ID | Agent | Ask |
|----|-------|-----|
| **R1** | PEER | Route Layer B Cox build |
| **R2** | PEER | Fix `543` notebook markdown |
| **R-TB-RUN** | CODA | Run TB-stratify on AWS |
| **R-Λ-EMPIR** | CODA | Army empirical Λ analysis |
| **R-POOL-AUDIT** | CODA | Pool-size audit (pre-publication) |

---

## 5. Agent status (all STANDING BY)

| Agent | Understanding | Waiting on you for | Will execute after your go |
|-------|---------------|--------------------|-----------------------------|
| **SCOUT** | ✅ All | Q-SCOUT-9, Q-D10 | D10 bundle |
| **PEER** | ✅ All | C1–C2 (+ Tier C defaults) | `faculty_panel_inference_v1.csv` |
| **CODA** | ✅ All | AWS, Alex Tier B | Figure list, optional TB-stratify |
| **VECTOR** | ✅ All | V1–V3 confirm (Tier A) | §1–§5 draft |
| **COMPASS** | ✅ All | Tier A batch; then maintain rollup | Update `1642`, near-term plan |

---

## 6. Recommended timeline (Summer–Fall 2026)

| When | Milestone |
|------|-----------|
| **This week** | Charles Phase A batch → SCOUT D10 + PEER inference export |
| **Week 2** | VECTOR §1–§3 draft (claim table + D10 artifacts) |
| **Week 3–4** | VECTOR §4–§5 + limitations; Alex meeting (Phase C) |
| **Ongoing** | AWS figure lock (Phase D) when sync allows |
| **Pre-submission** | PEER Layer B; pool audit; optional Army Λ figure |

---

## 7. Key reference documents (single spine)

| Role | Path |
|------|------|
| **Claim discipline** | [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) |
| **Tier 2 stop rule** | [`20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) |
| **Nesting / §3 prose** | [`20260611_1640_SCOUT_to_COMPASS_model_coherence.md`](20260611_1640_SCOUT_to_COMPASS_model_coherence.md) |
| **Near-term plan (pre-update)** | [`PROJECT_STATUS_AND_NEAR_TERM_PLAN.md`](PROJECT_STATUS_AND_NEAR_TERM_PLAN.md) |
| **Prior rollup** | [`20260611_1642_COMPASS_to_Charles.md`](20260611_1642_COMPASS_to_Charles.md) |
| **Alex prep** | [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md) |

---

## 8. COMPASS bottom line

> **The multi-agent correspondence experiment succeeded.** All agents agree on Path II, triad maturity, predictions, and claim discipline. **Charles: one Tier A batch reply unlocks SCOUT D10, PEER inference export, and VECTOR manuscript drafting.** Schedule Alex for Army estimand sign-off. AWS figure canonicalization can trail the draft. **Do not reopen model architecture** — execute packaging and prose.

---

*End COMPASS progress summary. COMPASS STANDING BY until Charles answers Tier A or routes agent work.*
