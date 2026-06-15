# COMPASS → Charles: Progress summary & next steps

**Date:** 2026-06-15 10:44  
**From:** COMPASS  
**To:** Charles (+ all agents for reference)  
**Trigger:** All agents filed **STANDING BY**; you asked COMPASS to synthesize and order your decisions.

**Sources merged:**  
[`20260615_1040_CODA_STANDING_BY_with_Qs_for_Charles.md`](20260615_1040_CODA_STANDING_BY_with_Qs_for_Charles.md) ·  
[`20260615_1038_PEER_STANDING_BY_with_Qs_for_Charles.md`](20260615_1038_PEER_STANDING_BY_with_Qs_for_Charles.md) ·  
[`20260615_1038_SCOUT_STANDING_BY_with_Qs_for_Charles.md`](20260615_1038_SCOUT_STANDING_BY_with_Qs_for_Charles.md) ·  
[`20260615_1130_VECTOR_STANDING_BY_with_Qs_for_Charles.md`](20260615_1130_VECTOR_STANDING_BY_with_Qs_for_Charles.md) ·  
[`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) ·  
[`20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) ·  
Rounds 1–4 hubs in `3-Master_Plan/`

---

## 1. Executive summary

**The correspondence experiment succeeded.** Five agents (CODA, PEER, SCOUT, VECTOR, COMPASS) report **mutual understanding** and **no open scientific disputes**. Everyone is **STANDING BY — waiting on you**, not on each other.

**Center of gravity:** You are past “find the curve” and past “do agents agree?” The bottleneck is **convergence on a v1 manuscript**: lock a small set of Charles decisions → SCOUT packages generative exports → PEER ships inference sample → VECTOR drafts prose under the unified claim table.

**Paper first, dissertation second.** Minimal model (Path II), empirical triad, two primary predictions — not 525/UIC, network extensions, generative LOO match, or tenure scrape expansion for v1.

---

## 2. Where we are — scientific consensus (locked)

Do **not** reopen in agent chat unless you explicitly redirect.

| Topic | Locked position |
|-------|-----------------|
| **Thesis** | Advancement under **constrained distinction** — LOO peer-pool quality vs advancement is **nonlinear (inverted-U)** in nested pools |
| **Path II** | **One** generative proof-of-concept (basketball); Army + tenure = **empirical legs** at different maturity |
| **Tier 2 stop rule** | Minimal model “complete enough” when SCOUT **D10 bundle** freezes talent-only failure, congestion POC, axis table, score one-pager ([`1012` closure](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md)) |
| **Generative LOO match** | **Out of scope** for v1 — honest axis-mismatch limitation required |
| **Claim discipline** | Unified table filed — [`1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) §F “Do say / Do not say” |
| **Predictions** | **#1** near-threshold heterogeneity · **#2** peak shift with Λ (Army-led prose; not fully exported empirically) |
| **Competing risks** | Army = full CR framing · Basketball = binned draft rates (no draft Cox gate) · Tenure = cause-specific planned pre-submission; Fine–Gray deferred |
| **Tenure soft gate** | Stage 9 + limitations OK for **draft now**; Layer B Cox **pre-submission only** |
| **Terminology** | `poolq_loo` (SCOUT) ≡ `poolq_loo_mean` (PEER) conceptually — **do not merge code column names** |

---

## 3. Empirical & packaging maturity (honest labels)

| Setting | Agent | Inverted-U (Rung 1) | Mechanism (Rung 2) | Predictions (Rung 3) | Manuscript-ready? |
|---------|-------|---------------------|--------------------|-----------------------|-------------------|
| **Army** | CODA | ✅ Established (CIF + Cox) | N/A (empirical leg) | Near-threshold testable; Λ hook conceptual | **Strongest** — figure list pending AWS |
| **Basketball** | SCOUT | ✅ Replicated (ventiles) | ✅ POC done; **D10 export pending** | 4D heterogeneity on disk | **Strong empirical**; §3 ink after D10 |
| **Tenure** | PEER | ⚠️ Preliminary (stage 9 bins) | N/A | Thin for v1 | **Preliminary figure + limitations** |
| **Manuscript** | VECTOR | Triad prose | §3 partial until D10 | §4 partial | **Draft after your Tier 1 locks** |

---

## 4. Correspondence experiment — outcome

| Milestone | Status |
|-----------|--------|
| Jun 11 `1626` Q&A (all agents) | ✅ Complete |
| Rounds 1–4 cross-agent mail | ✅ Complete |
| SCOUT minimal-model closure | ✅ [`1012`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) |
| VECTOR claim language table + M1–M5 | ✅ [`1100`](20260615_1100_VECTOR_claim_language_table.md) |
| All agents STANDING BY | ✅ Five files (incl. COMPASS `1040`) |
| Cross-agent scientific conflicts | **None** |
| Pre-delivered for D10 axis table | ✅ Army [`1019_CODA_to_SCOUT_round4`](20260615_1019_CODA_to_SCOUT_round4.md) · Tenure [`1020_PEER_to_SCOUT_round4`](20260615_1020_PEER_to_SCOUT_round4.md) |

**Read strategy going forward:** COMPASS hub + agent STANDING BY docs + delta pings — **not** full-folder re-read each round.

---

## 5. Itemized steps to move forward

### Phase 0 — You decide (one sitting, ~30–45 min)

**Goal:** Unblock all agents with batched answers (§6).

1. Read §6 **Tier 1 batch** below (or use copy-paste block in §7).
2. Optionally reply **“use agent defaults for Tier 2–3”** to accept PEER C3–C11, SCOUT Q-C7-C8, etc.
3. Answer **VECTOR V1–V3** (manuscript priority, predictions, draft timing).
4. Schedule **Alex meeting** for Tier 3 Army prose (or defer TB-stratify explicitly).

### Phase 1 — Immediate agent execution (after Tier 1)

| Step | Agent | Action | Depends on |
|------|-------|--------|------------|
| **1.1** | **SCOUT** | Implement **D10** export bundle (`export_scout_manuscript_bundle_v1.py` → `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/`) | **Q-D10 = go**, **Q-SCOUT-9** path |
| **1.2** | **PEER** | Build **`faculty_panel_inference_v1.csv`** + filter manifest | **C1–C2** |
| **1.3** | **VECTOR** | Begin manuscript prose: §2 Theory, §5 Discussion, §1 triad skeleton using claim table §F | After **1.1–1.2** (or parallel §2/§5 now) |
| **1.4** | **COMPASS** | Update [`20260611_1642_COMPASS_to_Charles.md`](20260611_1642_COMPASS_to_Charles.md) with closure greens + claim table status | After **1.1** |

**D10 unlocks:** 5 closure checklist greens; frozen generative PNGs; axis table; score one-pager; manifest for VECTOR §3.

### Phase 2 — Manuscript draft (Summer–Fall 2026 target)

| Step | Agent | Action |
|------|-------|--------|
| **2.1** | **VECTOR** | Ink §3 minimal model + generative figures (post-D10); §4 predictions; Setting 1–3 methods/results with claim discipline |
| **2.2** | **SCOUT** | Optional CELL 7 robustness **post-draft** (not v1 gate) |
| **2.3** | **PEER** | Setting 3 prose from stage 9; honest N footnotes |
| **2.4** | **CODA** | Supply Army estimand sentences to VECTOR after **C-ALEX-2** sign-off |

### Phase 3 — Alex meeting outcomes

| Step | Agent | Action |
|------|-------|--------|
| **3.1** | **CODA + VECTOR** | Finalize Army Methods estimand language |
| **3.2** | **CODA** | TB-stratify panels **only if** C-ALEX-1 ≠ defer |
| **3.3** | **All** | Align Alex on Path II, predictions, tenure preliminary label |

### Phase 4 — AWS / Army figures (when you sync)

| Step | Agent | Action |
|------|-------|--------|
| **4.1** | **Charles** | Run canonical Army profile on AWS; confirm figure filenames |
| **4.2** | **CODA** | Update handoff docs with **C-AWS-1** list |
| **4.3** | **VECTOR** | Lock Army panel captions |

### Phase 5 — Pre-submission (explicitly not draft blockers)

| Step | Agent | Action |
|------|-------|--------|
| **5.1** | **PEER** | **Layer B** Cox in `540` (~4–7 Mac days) — route **R1** |
| **5.2** | **CODA** | Pool-size audit; optional Λ empirical test |
| **5.3** | **PEER** | Prestige controls, subfield splits (if elevated) |
| **5.4** | **All** | Journal-spec figure exports |

### Explicitly parked (do not route unless you reopen)

525/UIC · Network extensions · Generative LOO bin-for-bin · Tenure roster expansion · Fine–Gray v1 · Basketball draft Cox · Mean×dispersion primary prediction

---

## 6. Your decision queue — ordered for one sitting

*Agent defaults in **bold** where agents recommend silence = accept.*

### Tier 1 — Unblocks draft work this week (answer first)

| Order | ID | Question | Agent | Default / recommendation |
|-------|-----|----------|-------|--------------------------|
| 1 | **Q-D10** | **Go** on SCOUT D10 export bundle (1–2 sessions packaging)? | SCOUT | Hold until you say **go** |
| 2 | **Q-SCOUT-9** | Bundle path: `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/` vs `3-Master_Plan/manuscript_exports/`? | SCOUT | **`datasets/mbb/.../scout_manuscript_v1/`** |
| 3 | **C1** | Tenure OpenAlex tier for inference v1 | PEER | **HIGH + MEDIUM** primary; exclude MULTI |
| 4 | **C2** | Tenure release names: `R1_tenure_data.csv` + `faculty_panel_inference_v1.csv`? | PEER | **Confirm as stated** |
| 5 | **V1** | Manuscript priority: complete minimal model → predictions → draft; defer dissertation planning? | VECTOR | **Yes** |
| 6 | **V2** | Primary predictions = near-threshold + Λ peak-shift? | VECTOR | **Yes** |
| 7 | **V3** | VECTOR begins prose after D10 + PEER C1–C2? | VECTOR | **Yes** (§2/§5 may start earlier) |
| 8 | **C12** | Confirm VECTOR prediction lock (#1 / #2; defer mean×dispersion)? | VECTOR/SCOUT | **Confirmed** per Jun 11 |
| 9 | **C13** | Confirm outline stack: Dakota spine / Tier1 voice / Alex methods order? | VECTOR | **Confirmed** per Jun 11 |

### Tier 2 — Confirm or batch-accept defaults

| Order | ID | Question | Agent | Default |
|-------|-----|----------|-------|---------|
| 10 | **Q-C7-C8** | Fig 2: PPM z within-season + ventile bins? | SCOUT | **Yes** |
| 11 | **Q-FIG2** | June-dated Fig 2 re-export in D10? | SCOUT | **Yes** if Q-D10 = go |
| 12 | **C3** | Report both 168 roster + inference N in prose? | PEER | **Both** |
| 13 | **C4** | Freeze tenure corpus vs resume scraping? | PEER | **Freeze** + targeted URL fixes |
| 14 | **C10–C11** | Defer prestige controls + subfield heterogeneity? | PEER | **Defer** |
| 15 | **G1–G3** | Tenure soft gate / Layer B pre-submission / Fine–Gray defer? | PEER | **Locked** unless you override |
| 16 | **Q-DEFAULTS** | Accept all Tier 2 agent defaults above in one line? | COMPASS | **Recommended** |

### Tier 3 — Alex meeting / Army prose (schedule; not blocking VECTOR §2/§5)

| Order | ID | Question | Agent | Default |
|-------|-----|----------|-------|---------|
| 17 | **C-ALEX-1** | TB-stratify panels: main / supplement / defer? | CODA | **Defer** |
| 18 | **C-ALEX-2** | Sign-off on estimand sentences (CIF vs Cox)? | CODA | Draft in [`1633` §A.3](20260611_1633_CODA_to_COMPASS.md) |
| 19 | **C-ALEX-3** | Fine–Gray deferred OK in Army prose? | CODA | **Yes** |
| 20 | **C-Λ-1** | Use CODA Λ stub in VECTOR §4 now vs wait for Army test? | CODA/VECTOR | Prose-only OK if labeled conceptual |
| 21 | **C-PUB-1** | Optional pool-size disclaimer in limitations now? | CODA | **Optional** — see CODA STANDING BY |

### Tier 4 — AWS / when you have Army JupyterLab access

| Order | ID | Question | Agent |
|-------|-----|----------|-------|
| 22 | **C-AWS-2** | AWS 4-file upload done? (yes/no) | CODA |
| 23 | **C-AWS-1** | Canonical Army figure: run profile + Cell 11 spec + PNG names? | CODA → VECTOR |

### Tier 5 — Route explicitly when ready (not STANDING BY blockers)

| ID | Ask | Agent | When |
|----|-----|-------|------|
| **R1** | Route Layer B tenure Cox build | PEER | Pre-submission |
| **R2** | Fix `543` markdown path mismatch | PEER | Cosmetic |
| **R-TB-RUN** | Run TB-stratify on AWS | CODA | After C-ALEX-1 + C-AWS-2 |
| **R-Λ-EMPIR** | Army empirical Λ test | CODA | Post-draft unless elevated |
| **R-POOL-AUDIT** | Senior-rater pool algorithm audit | CODA | Pre-publication |

---

## 7. Suggested copy-paste batch reply (Tier 1 + defaults)

Paste in chat to unlock most agents in one message:

```text
Tier 1:
Q-D10 = go
Q-SCOUT-9 = datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/
C1 = HIGH + MEDIUM primary (exclude MULTI from primary)
C2 = confirm R1_tenure_data.csv + faculty_panel_inference_v1.csv
V1 = yes (manuscript first)
V2 = yes (near-threshold + Λ peak-shift)
V3 = yes (VECTOR draft after D10 + PEER C1–C2; §2/§5 may start now)
C12 = confirmed
C13 = confirmed

Tier 2: use agent defaults (Q-C7-C8, Q-FIG2, C3, C4, C10–C11, G1–G3)

Tier 3: schedule Alex — C-ALEX-1 defer; C-ALEX-3 yes; C-Λ-1 use stub with conceptual label; C-PUB-1 optional later

Tier 4: C-AWS-* when AWS synced — I'll reply separately
```

---

## 8. Agent routing after you reply

| Your answer | Route to | They will |
|-------------|----------|-----------|
| Q-D10 + Q-SCOUT-9 | **SCOUT** | Build D10 bundle (1–2 sessions) |
| C1 + C2 | **PEER** | `faculty_panel_inference_v1.csv` + counts |
| V1–V3 + claim table | **VECTOR** | Manuscript draft phases |
| C-ALEX-* | **CODA + VECTOR** | Army Methods finalization |
| C-AWS-* | **CODA** | Figure list → VECTOR captions |
| Batch complete | **COMPASS** | Update rollup `1642`; mark experiment **closed** if you wish |

---

## 9. Key files index (living artifacts)

| Purpose | File |
|---------|------|
| **Claim discipline (manuscript law)** | [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) |
| **Minimal model stop rule** | [`20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md`](20260615_1012_SCOUT_to_COMPASS_minimal_model_closure.md) |
| **Domain handoffs** | [`CODA_report_to_COMPASS.md`](CODA_report_to_COMPASS.md) · [`SCOUT_report_to_COMPASS.md`](SCOUT_report_to_COMPASS.md) · [`PEER_report_to_COMPASS.md`](PEER_report_to_COMPASS.md) |
| **Alex brief** | [`20260611_Brief_for_Alex_Gates_full.md`](20260611_Brief_for_Alex_Gates_full.md) · [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md) |
| **Prior rollup** | [`20260611_1642_COMPASS_to_Charles.md`](20260611_1642_COMPASS_to_Charles.md) *(COMPASS will refresh after D10)* |
| **Agent STANDING BY** | `20260615_*_{AGENT}_STANDING_BY_with_Qs_for_Charles.md` (×5) |

---

## 10. COMPASS bottom line

> **Agents agree on the v1 architecture. You hold the keys.** Answer Tier 1 (§6 rows 1–9 or §7 batch paste) → SCOUT packages → PEER exports → VECTOR drafts. Schedule Alex for Tier 3. AWS when ready for Tier 4. Pre-submission evidence (tenure Cox, pool audit) stays parked until you route it.

**Correspondence experiment:** **Complete** from COMPASS’s view once you accept this summary and reply to Tier 1. Further rounds only if you reopen scope or an agent reports conflict.

---

*End COMPASS progress summary. COMPASS remains STANDING BY for your decisions.*
