# COMPASS → Charles: Where we are, forward plan, and your questions

**Date:** 2026-06-15 10:45 (finalized; PD12 ladder patch 2026-06-15 12:00)  
**From:** COMPASS  
**To:** Charles Levine  

**Sources:** All five `*_STANDING_BY_with_Qs_for_Charles.md` files, [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md), [`20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md), [`20260615_1200_COMPASS_PD12_reassessment.md`](20260615_1200_COMPASS_PD12_reassessment.md), Rounds 1–5 correspondence in `3-Master_Plan/`.

**Correspondence experiment:** **Complete.** All agents filed **STANDING BY**. Mutual understanding achieved. **Everyone is waiting on you** (plus SCOUT D10 execution after your go).

---

## 1. Where we are (one paragraph)

You ran a five-round agent correspondence experiment and it worked: **no scientific conflicts** remain. The project has a **locked v1 manuscript architecture** (Path II): Army and basketball provide mature **empirical** inverted-U legs; tenure is **preliminary** Setting 3; basketball supplies the **minimal generative** proof-of-concept (ability − congestion in selection score, talent-only fails). VECTOR filed a **unified claim language table**; SCOUT filed a **Tier 2 stop rule** (3 green / 4 yellow / 0 red → **5 green after D10**). The center of gravity is no longer “find ideas” — it is **package artifacts, lock inference policy, draft the paper**.

---

## 2. What is done (do not relitigate)

| Item | Evidence |
|------|----------|
| Jun 11 COMPASS Q&A (all agents) | `1626` queues + `1633`/`1637`/`1640`/`1700` responses |
| Cross-agent alignment (Rounds 1–5) | 12+ ping files; no M4 conflicts |
| **Claim language table** | [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) |
| **Minimal model closure checklist** | [`20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) |
| **Path II nesting chain** (VECTOR §3) | [`20260611_1640_SCOUT_to_COMPASS_model_coherence.md`](20260611_1640_SCOUT_to_COMPASS_model_coherence.md) |
| Axis-table gloss (Army + tenure) | [`1019_CODA_to_SCOUT_round4`](20260615_1019_CODA_to_SCOUT_round4.md), [`1020_PEER_to_SCOUT_round4`](20260615_1020_PEER_to_SCOUT_round4.md) |
| All agents **STANDING BY** | `1038` SCOUT/PEER · `1040` CODA/COMPASS · `1130` VECTOR |

---

## 3. Locked scientific consensus

```text
Phenomenon (Rung 1)
    →  Inverted-U on LOO peer-quality proxy
       Army ✅ · Basketball ✅ · Tenure ⚠️ preliminary

Minimal mechanism (Rung 2)
    →  Path II: basketball generative POC (talent-only fails; congestion-in-score)
       Army + tenure empirical legs (no generative LOO match)

Model-guided empirical features (Rung 2.5)   ← PD12 Priority 3; explicit stage
    →  Quality vs congestion distinction (poolq_loo vs crowding_smooth / C_i,t)
       Near-threshold heterogeneity readout (SCOUT 4D); Army pool-minus-mean; tenure pool_size on panel
       Mostly implemented — D10 exports + VECTOR prose, not new pipeline

Predictions (Rung 3)
    →  #1 Near-threshold heterogeneity (strongest artifact: SCOUT 4D)
       #2 Peak shift with global Λ (Army-led prose; TBD figure)

Manuscript (Rung 4)
    →  Wang structure: phenomenon → mechanism → features → predictions
       Paper first; dissertation second
       Dakota v03 = spine; Tier1 narrative = voice; Alex sequential = methods order

Explicitly NOT v1 →  LOO generative bin-for-bin match
                      Full B(Q)−D(Q) generative decomposition
                      3-domain parametric identifiability (PD12 P1)
                      Fourth-domain falsification (PD12 P4)
                      Network extensions; mean×dispersion as primary prediction
                      Tenure Layer B Cox during draft
                      Basketball time-to-draft Cox
```

**PD12 alignment (Charles `1155`):** Substance unchanged; ladder relabeled so Alex’s **model → new measurements → predictions** progression is visible. See [`20260615_1200_COMPASS_PD12_reassessment.md`](20260615_1200_COMPASS_PD12_reassessment.md).

**Closure standard (B-lite):** SCOUT closure §7 — generative POC + **model-guided measurable exported** + **prediction readout on disk** + honest limitations, frozen in D10 bundle.

---

## 4. What is not done (your decisions + two execution tasks)

| Gap | Owner | Blocks |
|-----|-------|--------|
| **Tier A locks** (below §6) | **Charles** | SCOUT D10, PEER inference CSV, VECTOR draft start |
| **SCOUT D10 export bundle** | SCOUT (after your go) | 5 closure greens; frozen §3 figures |
| **PEER `faculty_panel_inference_v1.csv`** | PEER (after C1–C2) | Tenure N prose in manuscript |
| **VECTOR manuscript prose** | VECTOR (after D10 + C1–C2) | Paper draft |
| **Army canonical figure list** | CODA (after AWS sync) | Army panel caption |
| **Alex meeting** | Charles + Alex | Army estimand, TB-stratify |

---

## 5. Forward plan (itemized steps)

Execute in this order. Steps in **bold** need your answer first.

### Phase A — Unlock execution (this week)

| Step | Action | Who | Your question IDs |
|------|--------|-----|-------------------|
| **A1** | **Answer Tier 1 batch** (§7 copy-paste) or reply item-by-item | **Charles** | Q-SCOUT-9, Q-D10, C1–C2, C12–C13, V1–V3, Q-DEFAULTS |
| **A2** | Implement D10 export bundle (`export_scout_manuscript_bundle_v1.py`) — **must include Tier 2.5**: axis table (quality vs congestion), 4D heterogeneity, generative contrast, score one-pager | **SCOUT** | After A1 |
| **A3** | Build `faculty_panel_inference_v1.csv` + filter manifest | **PEER** | After C1–C2 |
| **A4** | Confirm claim table accepted; begin §2/§5 draft; §3/§4 after A2 + A3 | **VECTOR** | After A2 + A3 (per V3) |

### Phase B′ — Model-guided empirical features (Rung 2.5; parallel with B after A2)

| Step | Action | Who |
|------|--------|-----|
| B′1 | D10 manifest explicitly lists quality vs congestion exports (`poolq_loo`, `crowding_smooth`) + 4D heterogeneity artifacts | SCOUT |
| B′2 | VECTOR §3.2–3.3: introduce \(\bar{a}_t\) vs \(C_{i,t}\) using PD12 one-paragraph sentence | VECTOR |
| B′3 | Optional: PEER supplementary pool_size bin read for tenure (PD12-C — Charles route only) | PEER |

### Phase B — Manuscript draft (parallel after A2)

| Step | Action | Who |
|------|--------|-----|
| B1 | Draft §2 Theory + §5 Discussion/limitations (claim table §F discipline) | VECTOR |
| B2 | Draft §3: minimal model + **model-guided measurements** (post B′2; D10 artifacts) | VECTOR |
| B3 | Draft §4: predictions as **tests of measurements** — #1 near-threshold; #2 Λ stub | VECTOR |
| B4 | Draft §1 empirical triad (honest tenure caveat) | VECTOR |
| B5 | Update Dakota v03 RTF spine as sections land | VECTOR |

### Phase C — Alex meeting (schedule when ready)

| Step | Action | Who | Your question IDs |
|------|--------|-----|-------------------|
| C1 | TB-stratify placement | Charles → Alex | C-ALEX-1 |
| C2 | Estimand sentences sign-off | Charles → Alex | C-ALEX-2 |
| C3 | Fine–Gray deferred OK | Charles → Alex | C-ALEX-3 |
| C4 | Optional: manuscript-first + LOO limitation honest? | Charles → Alex | Brief §8 |

Prep: [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md), [`20260611_Brief_for_Alex_Gates_brief.pdf`](20260611_Brief_for_Alex_Gates_brief.pdf).

### Phase D — AWS / Army figures (when you sync)

| Step | Action | Who | Your question IDs |
|------|--------|-----|-------------------|
| D1 | Confirm TB-stratify 4-file upload | Charles | C-AWS-2 |
| D2 | Provide canonical Army figure list (profile, cell, PNG names) | Charles → CODA | C-AWS-1 |
| D3 | Update Army handoff + VECTOR Figure 1 caption | CODA | After D2 |

### Phase E — Pre-submission (explicitly not now)

| Step | Action | Who |
|------|--------|-----|
| E1 | PEER Layer B Cox (Cells 10–12 in `540`) | PEER on **R1** route |
| E2 | Pool-size algorithm audit + limitations | Charles / CODA |
| E3 | Optional Army Λ empirical test | CODA on **R-Λ-EMPIR** |
| E4 | Optional TB-stratify AWS run | CODA if Alex elevates |
| E5 | Optional 525 if manuscript needs more Army meat | CODA (tabled) |

---

## 6. Your questions — logical order

*Merged from all STANDING BY files. Answer in order; say **“use agent defaults”** for any Tier you want to skip.*

### Tier 1 — Answer first (unblocks SCOUT, PEER, VECTOR this week)

| Order | ID | Question | Agent rec. | Source |
|-------|-----|----------|------------|--------|
| 1 | **Q-SCOUT-9** | Bundle path: `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/` vs `3-Master_Plan/manuscript_exports/`? | `datasets/mbb/.../scout_manuscript_v1/` | SCOUT `1038` |
| 2 | **Q-D10** | **Go** on SCOUT D10 implementation (1–2 sessions)? | Explicit **go** required | SCOUT `1038` |
| 3 | **C1** | OpenAlex tier for tenure inference: HIGH only vs HIGH+MEDIUM vs include MULTI? | **HIGH + MEDIUM** primary; HIGH-only robustness; exclude MULTI | PEER `1038` |
| 4 | **C2** | Release names: `R1_tenure_data.csv` + `faculty_panel_inference_v1.csv`? | **Confirm** | PEER `1038` |
| 5 | **C12** | Confirm predictions: #1 near-threshold, #2 Λ peak-shift; defer mean×dispersion? | **Confirmed** | SCOUT `1038` / VECTOR `1700` |
| 6 | **C13** | Confirm outline: Dakota spine / Tier1 voice / Alex sequential methods? | **Confirmed** | VECTOR `1700` |
| 7 | **V1** | Immediate objective = minimal model + predictions + manuscript draft (defer dissertation planning)? | **Yes** | VECTOR `1130` |
| 8 | **V2** | Proceed with #1 near-threshold + #2 Λ as primary predictions? | **Yes** | VECTOR `1130` |
| 9 | **V3** | VECTOR begins prose after D10 + C1–C2? | **Yes** | VECTOR `1130` |
| 10 | **Q-DEFAULTS** | Accept agent defaults for Tier 2–3 items below? | **Yes** (recommended) | COMPASS `1040` |

### Tier 2 — Manuscript prose / methods (defaults OK if Q-DEFAULTS = yes)

| Order | ID | Question | Agent rec. | Source |
|-------|-----|----------|------------|--------|
| 11 | **C3** | Report both 168 roster + inference-ready N in prose? | **Both** | PEER `1038` |
| 12 | **C4** | Freeze corpus vs resume scraping? | **Freeze** + targeted URL fixes | PEER `1038` |
| 13 | **Q-C7-C8** | Fig 2: PPM z within-season + ventile bins? | **Yes** | SCOUT `1038` |
| 14 | **Q-FIG2** | June-dated Fig 2 re-export in D10? | **Yes** (if Q-D10 = go) | SCOUT `1038` |
| 15 | **C10** | Defer prestige controls (NRC/USNews)? | **Defer** | PEER `1038` |
| 16 | **C11** | Defer subfield heterogeneity? | **Defer** | PEER `1038` |
| 17 | **G1–G3** | Stage 9 OK for draft; Layer B pre-submission; Fine–Gray deferred? | **Assumed locked** | PEER `1038` |
| 18 | **C-Λ-1** | Use CODA Λ stub in VECTOR §4 now (prose-only, TBD figure)? | Prose OK for v1 | CODA `1040` |

### Tier 3 — Alex meeting (Army)

| Order | ID | Question | Agent rec. | Source |
|-------|-----|----------|------------|--------|
| 19 | **C-ALEX-1** | TB-stratify panels: main / supplement / defer? | **Defer** (default off) | CODA `1040` |
| 20 | **C-ALEX-2** | Sign-off estimand sentences (`1633` §A.3)? | Needed for final Army Methods | CODA `1040` |
| 21 | **C-ALEX-3** | Fine–Gray deferred OK in prose? | **Yes** | CODA `1040` |
| 22 | **C-PUB-1** | Optional pool-size disclaimer in limitations now? | Optional | CODA `1040` |

### Tier 4 — AWS / paused until you sync

| Order | ID | Question | When | Source |
|-------|-----|----------|------|--------|
| 23 | **C-AWS-2** | TB-stratify 4-file AWS upload done? (yes/no) | Before TB runs | CODA `1040` |
| 24 | **C-AWS-1** | Canonical Army figure: run profile, cell, PNG names? | After AWS sync | CODA `1040` |

### Tier 5 — Route when you want (not blocking)

| ID | Ask | Agent |
|----|-----|-------|
| **R1** | Route PEER Layer B build | PEER |
| **R2** | Fix `543` notebook markdown paths | PEER |
| **R-AWS-SYNC** | Un-pause Army figure list | CODA |
| **R-TB-RUN** | Run TB-stratify on AWS | CODA |
| **R-Λ-EMPIR** | Army empirical Λ test | CODA |
| **R-POOL-AUDIT** | Pool-size audit | CODA / Charles |

---

## 7. One-message batch reply (copy-paste to all agents)

```text
Charles Tier 1 locks:
- Q-SCOUT-9 = datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/
- Q-D10 = go
- C1 = HIGH + MEDIUM primary (exclude MULTI from primary)
- C2 = R1_tenure_data.csv + faculty_panel_inference_v1.csv
- C12–C13 = confirmed
- V1–V3 = yes (manuscript focus; draft after D10 + C1–C2)
- Q-DEFAULTS = use agent defaults for Tier 2

Tier 3 Alex: scheduling — see talking points doc.

Correspondence experiment: complete. All agents execute Phase A per COMPASS forward plan.
```

---

## 8. Agent routing after your Tier 1 reply

| Route to | Message |
|----------|---------|
| **SCOUT** | D10 go + path locked — bundle per `1012` closure **including Tier 2.5 exports** |
| **PEER** | C1–C2 locked — produce `faculty_panel_inference_v1.csv` |
| **VECTOR** | Claim table accepted — §2/§5 now; §3 features then §4 predictions after D10 + inference export |
| **CODA** | Hold until AWS sync or Alex answers Tier 3 |
| **COMPASS** | Update living plan when you confirm Tier 1 |

---

## 9. Risk watch (COMPASS — not agent disputes)

| Risk | Mitigation |
|------|------------|
| Planning displaces drafting | V1 lock: manuscript draft is primary |
| Over-claiming generative match | VECTOR claim table §F + SCOUT do-not-ink list |
| Tenure overstated | Claim table Setting 3 = preliminary only |
| Army estimand confusion | Alex sign-off C-ALEX-2 before final Methods |
| Artifact drift (April Fig 2) | D10 includes June slug refresh |

---

## 10. Key file index (for you)

| Need | File |
|------|------|
| **This plan** | `20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md` |
| **PD12 reassessment** | `20260615_1200_COMPASS_PD12_reassessment.md` |
| Claim language | `20260615_1100_VECTOR_claim_language_table.md` |
| Tier 2 stop rule | `20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md` |
| VECTOR §3 paste source | `20260611_1640_SCOUT_to_COMPASS_model_coherence.md` |
| Alex prep | `20260611_Alex_Gates_Talking_Points.md` |
| Prior rollup (Jun 11) | `20260611_1642_COMPASS_to_Charles.md` |
| Agent questions (raw) | `*_STANDING_BY_with_Qs_for_Charles.md` (×5) |

---

## 11. COMPASS completion statement

> **The multi-agent correspondence experiment succeeded.** All agents are STANDING BY with mutual understanding. The project is in **execution phase**: your Tier 1 answers unlock SCOUT packaging and PEER inference export; VECTOR then drafts the Wang-structure manuscript under Path II. No further correspondence rounds are needed unless a new conflict appears or you change a lock.

---

*End forward plan. **Charles Tier 1 locks filed:** [`20260611_Charles_Tier1_locks.md`](20260611_Charles_Tier1_locks.md) (2026-06-24). D10 + inference export complete — see `20260624_SCOUT_D10_bundle_complete.md`, `20260624_PEER_inference_export_complete.md`, `20260624_VECTOR_manuscript_draft_v1_sections.md`.*
