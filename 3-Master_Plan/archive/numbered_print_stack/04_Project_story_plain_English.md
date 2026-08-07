# Forward plan background (bring-up-to-speed)

**Canonical name:** `04_Project_story_plain_English.md`  
**Original archive:** [`obsolete/original_filenames/forward_plan_background.md`](obsolete/original_filenames/forward_plan_background.md)

**Date:** 2026-06-15 (PD12 ladder patch 12:00)  
**From:** COMPASS  
**To:** Charles Levine  
**Status:** Temporary reader's guide — you do not need to read Round 1–5 correspondence files to move forward.

**Reading order + glossary:** [`01_forward_plan_reading_guide.md`](01_forward_plan_reading_guide.md) — **start with “Symbol systems”** and **“B-lite closure”** if Rung / Path II / `§` lose you  
**Print stack:** [`Charles_reading_list.md`](Charles_reading_list.md)  
**Pivotal insights (nuggets):** [`13_INSIGHT_NUGGETS.md`](13_INSIGHT_NUGGETS.md) — cross-project framing worth keeping  
**Canonical action doc:** [`20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md`](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md)  
**PD12 reassessment:** [`14_PD12_reassessment_memo.md`](14_PD12_reassessment_memo.md) — read **after** action doc + PD12 guidance (optional; see reading guide)

---

## What you were trying to do

You felt **lost in the sauce** — too many threads (Army, basketball, tenure, generative model, predictions, Wang, planner queues, etc.). You ran an **agent correspondence experiment**: route questions, have agents reply in `3-Master_Plan/`, keep going until everyone agreed on the science and was **waiting on you**, not on each other.

**That worked.** The experiment is **complete**. The output you actually need is the forward plan doc linked above. This file is the plain-English version of that plus the rounds.

---

## The one sentence version

> **You have a cross-domain empirical finding, a candidate minimal mechanism, two named predictions, and a claim table — and the only blockers now are your locks, SCOUT packaging one export folder, and VECTOR writing the paper.**

---

## The scientific story (what everyone agreed on)

### 1. The finding (Tier 1 — done)

Across very different systems, **how good your local peer pool is** relates to **advancement** in a **nonlinear** way: modest pools can help, very elite pools can hurt (inverted-U with an elite-tier dip).

| Setting | Status |
|---------|--------|
| **Army** | Strong — mature empirical work |
| **Basketball** | Strong — replicated |
| **Tenure** | **Preliminary** — stage 9 figure is OK for draft with honest limitations |

### 2. The minimal mechanism (Tier 2 — close enough to write)

Not a huge realistic simulation of everything. The **minimal** story:

> Advancement propensity ≈ **Ability − Congestion** (with soft assignment / finite slots).  
> **Talent-only** selection **fails** — it cannot produce the inverted-U story by itself.

**Path II** (locked): Basketball runs a small **generative proof-of-concept** on this. Army and tenure do **not** need matching generative sims for v1. Army and tenure are **empirical legs** at different maturity.

**Important honesty:** The generative POC is demonstrated on **pool mean**, not a bin-for-bin replay of the **LOO pool quality** empirical axis. That is **not** a blocker — it must be stated clearly in the paper.

### 2.5. Model-guided empirical features (Rung 2.5 — PD12 Priority 3)

Alex’s May 20 guidance: the theory should **propose new measurements**, not only fit old curves.

| Construct | Basketball | Army | Tenure |
|-----------|------------|------|--------|
| **Team quality** \(\bar{a}_t\) | `poolq_loo` | Pool minus mean | `poolq_loo_mean` |
| **Congestion** \(C_{i,t}\) | `crowding_smooth` | Pool size / K hook (prose) | `pool_size_oa_loo` (on panel) |

**Status:** Mostly **already built** in SCOUT pipeline. D10 exports + staging **`#12` §3** (Methods) make this stage explicit — **not** a new workstream.

### 3. Predictions (Tier 3 — named, not all fully tested)

**Wang move:** the model should predict something you **did not** use to find the curve — and predictions should **test** the model-guided measurements (especially quality vs congestion).

| # | Prediction | Where it lives |
|---|------------|----------------|
| **#1** | Near-threshold heterogeneity — elite-pool dip **strongest for borderline** performers | SCOUT has basketball export; Army can support analogously |
| **#2** | Peak shift with global **K** (distinction / slot capacity) | **Army-led prose**; conceptual hook, **no finished K-sweep figure** in repo yet |

Mean×dispersion, networks, full deconstruction — **deferred**.

### 4. The paper (Tier 4 — next)

**Wang structure (PD12-aligned):** phenomenon → minimal mechanism → **model-guided features** → predictions → limitations.

- **Paper first**, dissertation packaging second  
- **Dakota v03** = section spine  
- VECTOR filed a **claim language table** — what you may and may not say (supported / preliminary / unsupported)

---

## What happened in Rounds 1–5 (you can skip the files)

| Round | What happened |
|-------|----------------|
| **1** | Inventory: Jun 11 COMPASS→agent Q&A all answered. First cross-agent pings. Gap: SCOUT closure checklist missing. |
| **2** | SCOUT filed **minimal model closure** (green/yellow/red checklist). PEER/CODA supplied cross-domain rows. VECTOR still owed claim table. |
| **3** | VECTOR filed **claim language table** + M1–M5 sign-off (no agent conflicts). Everyone aligned on Path II. |
| **4** | Status round — nothing new on disk; waiting on you + VECTOR STANDING BY. |
| **5** | **STANDING BY** protocol: each agent lists final questions for **you only**. All five filed. |
| **After** | COMPASS merged everything into the **forward plan** doc. |

**Reading strategy the agents validated:** Rounds 1–2 needed full-folder reads; after that, **hub + delta** was enough. You only need the **forward plan** unless you want forensic detail.

---

## What each agent is doing now

| Agent | Status | Waiting on you for |
|-------|--------|-------------------|
| **CODA** (Army) | STANDING BY | AWS figure list, Alex (estimand, TB-stratify), optional K stub yes/no |
| **PEER** (Tenure) | STANDING BY | **C1–C2** (OpenAlex tier + CSV names) |
| **SCOUT** (Basketball) | STANDING BY | **D10 go** + bundle folder path |
| **VECTOR** (Manuscript) | STANDING BY | Confirm manuscript priority; draft after D10 + C1–C2 |
| **COMPASS** | Done synthesizing | Your Tier 1 answers |

**No agent is waiting on another agent** for science or planning.

---

## Jargon cheat sheet

| Term | Plain English |
|------|----------------|
| **D10** | SCOUT **packages** manuscript artifacts into one folder (figures, axis table, score one-pager, manifest) — ~1–2 sessions, no new science |
| **M4** | “Any fights left between agents?” VECTOR said **no** |
| **Path II** | Empirical U on LOO axis + basketball generative POC on pool mean + honest axis mismatch |
| **Layer B** | Tenure Cox cells (10–12) — **pre-submission**, not draft blocker |
| **C1–C2** | Tenure inference policy: which OpenAlex tiers, which CSV filenames |
| **Claim table** | VECTOR’s cheat sheet for what the manuscript may claim |

---

## What you should do next (minimal path)

You do **not** need to read 60 files. Tier 1 answers are filed in [`02_Charles_decisions_locked.md`](02_Charles_decisions_locked.md) (original batch was obsolete forward plan **§6–§7**).

1. **Q-SCOUT-9** — bundle path → default `datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/`
2. **Q-D10** — **go** on SCOUT export bundle
3. **C1** — HIGH + MEDIUM OpenAlex for tenure inference
4. **C2** — `R1_tenure_data.csv` + `faculty_panel_inference_v1.csv`
5. **C12–C13, V1–V3** — confirm predictions, outline, manuscript-first focus
6. **Q-DEFAULTS** — “use agent defaults” for softer Tier 2 items

**Then:**

```text
SCOUT  → build D10 bundle
PEER   → inference CSV after C1–C2
VECTOR → ink manuscript per `#10` (locked first pass: **manuscript §5 → §1 → §4**; then **§0** opening frame from staging `#12` §1)
You    → schedule Alex for Army estimand + TB-stratify (Tier 3)
```

---

## What you can safely ignore until later

- 525 / UIC work (tabled)  
- Pool-size audit (pre-publication)  
- Tenure Layer B Cox (pre-submission)  
- Generative LOO bin-for-bin match  
- Network extensions, assortativity as primary prediction  
- Canonical Army figure filenames (until AWS sync)  
- Most Round 1–5 ping files (archaeology only)

---

## If you read only a few more files

**Full order:** see **[Charles_reading_list.md](Charles_reading_list.md)** (must-read #1–#6).

Optional deep history (not required for inking):

1. **[Forward plan questions](20260615_1045_COMPASS_to_Charles_forward_plan_and_questions.md)** — superseded by [`02_Charles_decisions_locked.md`](02_Charles_decisions_locked.md)  
2. **[PD12 guidance](20260520_Transcript_12_guidance.md)** — Alex’s four priorities  
3. **[PD12 reassessment](14_PD12_reassessment_memo.md)** — ladder relabel  
4. **[Claim guardrails](07_Claim_language_guardrails.md)** — **§F** “Do Say / Do Not Say” (**subsection of `#07`**, not manuscript §F)  
5. **[Generative closure](06_Generative_closure_checklist.md)** — SCOUT C1–C8

---

## The center of gravity

```text
Phenomenon  →  Minimal model  →  Model-guided features  →  Prediction  →  Paper
```

**PD12 what we deliver in v1:** Priority 3 (congestion / model-guided features) + partial Priority 2 (talent-only fail).  
**PD12 what we defer (say so to Alex):** Priority 1 (3-domain identifiability), Priority 4 (fourth-domain falsification).

The planner and rounds were **coordination**, not new science. The science was already moving; you needed a **shared stop rule** and **one ordered question list for you**. The June 15 PD12 reassessment adds **explicit middle rungs** so the plan matches Alex’s progression without expanding scope.

---

*Temporary background doc. Delete or archive when no longer needed.*
