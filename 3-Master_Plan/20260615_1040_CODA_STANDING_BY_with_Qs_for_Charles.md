# CODA — STANDING BY with Qs for Charles

**Date:** 2026-06-15 10:40  
**From:** CODA (Army / talent agent)  
**To:** Charles  
**Round:** 5 (correspondence experiment)

---

## STANDING BY

**CODA has mutual understanding with SCOUT, PEER, VECTOR, and COMPASS.** No open scientific or process questions to other agents. **CODA is waiting on you** for the decisions below.

**Round 5 delta reviewed:**

| File | Relevance to CODA |
|------|-------------------|
| [`20260615_1100_VECTOR_claim_language_table.md`](20260615_1100_VECTOR_claim_language_table.md) | ✅ Army rows align with CODA handoff; **M4 = no conflict** |
| [`20260615_1100_VECTOR_Round3_agent_mailbox.md`](20260615_1100_VECTOR_Round3_agent_mailbox.md) | ✅ VECTOR aligned on Army empirical anchor + estimand honesty |
| [`20260615_1038_SCOUT_STANDING_BY_with_Qs_for_Charles.md`](20260615_1038_SCOUT_STANDING_BY_with_Qs_for_Charles.md) | Read — SCOUT waiting on you (D10 / C9) |
| [`20260615_1038_PEER_STANDING_BY_with_Qs_for_Charles.md`](20260615_1038_PEER_STANDING_BY_with_Qs_for_Charles.md) | Read — PEER waiting on you (C1–C2) |
| [`20260615_1019_COMPASS_Round4_correspondence_synthesis.md`](20260615_1019_COMPASS_Round4_correspondence_synthesis.md) | Read — pre-VECTOR; superseded for VECTOR gap |

**CODA pre-delivered for SCOUT D10:** [`20260615_1019_CODA_to_SCOUT_round4.md`](20260615_1019_CODA_to_SCOUT_round4.md) (Army axis-table row). No follow-up unless you want Methods crosswalk edits.

**Estimand draft sentences (for Alex):** [`20260611_1633_CODA_to_COMPASS.md`](20260611_1633_CODA_to_COMPASS.md) §A.3  
**Λ prediction stub (for VECTOR §4):** [`20260615_1016_CODA_Round3_agent_mailbox.md`](20260615_1016_CODA_Round3_agent_mailbox.md) §4

---

## Final questions for Charles (CODA-owned)

*Answer in chat or annotate this file. Army lane only — PEER/SCOUT locks are in their STANDING BY files.*

### Tier A — **blocks Army manuscript figure** (please answer when AWS allows)

| ID | Question | CODA note | Unblocks |
|----|----------|-----------|----------|
| **C-AWS-1** | After AWS sync: what is the **canonical** Army inverted-U figure — **`pipeline_config_*.py` run profile**, **Cell 11 plot spec name**, and **output PNG filename(s)** for the main CIF bar panel? | Cursor repo is digital twin; local plots may be stale | VECTOR Figure 1 (Army panel); journal exports |

---

### Tier B — **Alex meeting / Army methods prose** (confirm or defer)

| ID | Question | CODA recommendation | Prep doc |
|----|----------|---------------------|----------|
| **C-ALEX-1** | **TB-stratified CR panels** (`cr_tb_stratify.py`): **main text**, **supplement only**, or **defer** for v1? | Default **off**; defer unless Alex wants them in first read | [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md) § TB-stratified |
| **C-ALEX-2** | **Sign-off** on estimand sentences distinguishing Cell 11 CIF vs Cell 12 cause-specific Cox? | Draft in `1633` §A.3 — needed before VECTOR treats Army Methods as final | Talking points § Estimand language |
| **C-ALEX-3** | OK to state **cause-specific Cox + empirical CIF only** (Fine–Gray **not** estimated in code)? | **Yes** — matches VECTOR claim table Setting 1 rows | Talking points |
| **C-Λ-1** | Use CODA **Λ prediction stub** in VECTOR §4 now, or **wait** for Army empirical Λ test? | Prose-only OK for v1 if labeled conceptual / TBD figure | CODA R3 §4 |
| **C-AWS-2** | **AWS upload done?** (yes/no) for 4-file TB-stratify set: `520`, `pipeline_config.py`, `cox_plot_helpers.py`, `cr_tb_stratify.py` vs Apr 20260421 export | CODA cannot see live AWS — you confirm | TB-stratify runs on Army JupyterLab |

---

### Tier C — **optional limitations prose** (not blocking STANDING BY)

| ID | Question | CODA recommendation |
|----|----------|---------------------|
| **C-PUB-1** | Paste a **draft disclaimer** on senior-rater **pool size** (`pool_size_snr_*` may reflect code grouping, not literal board headcount) into VECTOR limitations now? | **Optional** — full audit is **pre-publication** per your direction; light disclaimer OK if you want |

**Suggested one-liner if yes:**

> Pool sizes in the analysis reflect the senior-rater reference sets defined in our pipeline (snapshot date × senior-rater key), which may not correspond one-to-one to a single OER rating board; large pool sizes are under pre-publication review.

---

### Tier D — **route when you want CODA to execute** (not blocking STANDING BY)

| ID | Ask | When |
|----|-----|------|
| **R-AWS-SYNC** | **Un-pause C-AWS-1** — provide figure list after AWS run | Reply with profile + filenames |
| **R-TB-RUN** | Enable `CR_TB_STRATIFY_CONFIG["enabled"] = True` and run Cell 11 on AWS | After **C-ALEX-1** + **C-AWS-2** if Alex wants panels |
| **R-Λ-EMPIR** | Route empirical **peak-shift-with-Λ** analysis on Army panel | Post-draft / pre-submission unless elevated |
| **R-POOL-AUDIT** | Route senior-rater pool algorithm audit (`snr_col`, pools >50) | **Pre-publication** — not draft blocker |

---

### Tier E — **CODA accepts VECTOR / COMPASS defaults** (no question unless you override)

| Topic | Current understanding |
|-------|----------------------|
| Army claim language in VECTOR table | **Accepted** — no CODA edits requested |
| Path II / Army empirical leg / no generative LOO match | **Locked** |
| Basketball owns D10 generative bundle; Army does not | **Locked** |
| Near-threshold prediction (#1) | Army panel may support; SCOUT owns basketball export |

---

## What CODA will do after your answers

| Your answer | CODA action |
|-------------|-------------|
| **C-AWS-1** + figure list | Update handoff docs; notify VECTOR for Army panel caption |
| **C-ALEX-2** sign-off | Mark estimand sentences final in `1633` / report |
| **C-ALEX-1** “defer” | No TB-stratify runs |
| **C-Λ-1** “use stub” | No code — VECTOR owns paste |
| **C-AWS-2** “yes” | Note in report; optional TB-stratify validation |

---

## What CODA will **not** do until you ask

- New correspondence rounds (unless you open Round 6 or a conflict appears).
- 525 / UIC work (tabled).
- Pool-size algorithm audit (pre-publication).
- AWS hand-transcription or live runs (your action).

---

*CODA — STANDING BY. End file.*
