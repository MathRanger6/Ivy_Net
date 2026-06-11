# Plan update for Alex Gates — status, model duality, and path ahead (full)

**Date:** 2026-06-11  
**From:** Charles Levine (draft for your edit)  
**One-page summary:** [20260611_Brief_for_Alex_Gates_brief.md](20260611_Brief_for_Alex_Gates_brief.md) — Charles converts to PDF when ready (`pdf_styles_one_page.css` via `convert_single_md_to_pdf.sh`).

**Purpose:** Keep you aligned on project status, the main modeling tension, and **what I'm going with** for a **Summer–Fall 2026** core manuscript draft/submission. This is not a decision memo — I'm informing you of my sequencing choices after a cross-project COMPASS review.

---

## 1. Where we stand

We have a **credible three-setting empirical story**: inverted-U in advancement vs **leave-one-out (LOO) peer-pool quality** in Army (anchor) and college basketball (replication), with academia (tenure) as a **preliminary third panel (stage 9 bins)**. The scientific bottleneck is no longer “find the curve” but **converge on claim language**, **minimal generative mechanism**, and **2–3 testable predictions** for a Wang-style paper — without letting Army 525/UIC work, network extensions, or generative perfectionism block the draft.

---

## 2. What is solid

| Area | Status |
|------|--------|
| **Empirical inverted-U (LOO axis)** | Army ✅ · Basketball ✅ (`poolq_loo` / draft rate) · Tenure ⚠️ preliminary |
| **Wang empirical ladder (basketball)** | Bins → LPM → logit in `538`; \(L^*\) reported |
| **Minimal score equation** | \(S_i = A_i - \lambda \cdot L_{C,\text{LOO}}\) implemented in `538D` CELL 10 |
| **Ability-only generative null** | Confirmed — congestion term needed for nonlinear readout |
| **Generative POC (one axis)** | Inverted-U vs **pool mean** (`team_mean`, includes self) under current top-\(K\) knobs |
| **Tenure measurement** | End-to-end stage 9 on existing data per your April direction; sample loss logged |

---

## 3. The model duality (context)

Two related programs have been running in parallel. They are **not** the same estimand unless we nest them explicitly in prose.

### A. Empirical stylized fact (cross-domain)

- **Axis:** **LOO pool quality** — mean teammate performance **excluding self** (`poolq_loo` in basketball; analogous objects in Army and tenure).
- **Finding:** Draft / promotion / tenure rates rise through mid-quality peer environments, then fall in the elite tier (**inverted-U**).
- **Role in paper:** Wang **Rung 1** — the replicated phenomenon.

### B. Generative minimal model (Alex score + assignment)

- **Score:** \(S_i = A_i - \lambda \cdot L_{C,\text{LOO}}\) — own ability minus **LOO congestion** (viable peers excluding self).
- **Current readout:** Inverted-U appears when success is conditioned on **pool mean** (whole-roster average, **not** LOO).
- **On the empirical axis:** With the same knobs, generative readout vs **LOO pool quality** is **mostly decreasing**, not inverted-U.
- **Role in paper:** Wang **Rung 2** — proof that finite distinction / congestion can bend advancement; **partial** match to Rung 1 unless axis language is careful.

### C. Decomposition / predictions track

- **Structure:** Local environment as one object: \(L_{\text{net}} = B(\cdot) - D(\cdot)\) — **benefit (development)** minus **constraint (congestion / distinction cost)**.
- **Empirical mechanism columns** (`congestion_quality`, LOO dispersion, minutes, etc.) intended as **diagnostics of B vs D**, not a second mechanism.
- **Tension:** Prior guidance sounded like “**Alex model for curves, multivariate empirical for predictions**” — workable only if nested in **one** ontology; otherwise it reads as **two models**. My plan below commits to **one story in writing**.

### D. Terminology lock

| Quantity | Name rule |
|----------|-----------|
| Excluding self | Must say **LOO** (e.g. LOO pool quality, LOO congestion) |
| Whole roster including self | **Pool mean** / `team_mean` — **not** LOO |

The program is **not** stuck on whether the empirical U exists. The work ahead is making the **generative object**, **empirical decomposition**, and **conditioning axis** read as **one scientific story** in the manuscript — with honest language about the LOO generative gap.

---

## 4. What I'm going with (near-term)

### My sequencing choices

| Area | My call |
|------|---------|
| **Timeline** | Core manuscript draft/submission **Summer–Fall 2026** |
| **Generative path** | **Manuscript-first:** draft on empirical LOO U + honest generative POC (pool-mean readout) + explicit **two-row axis table**; **not** blocking on generative LOO-pool-quality bin-for-bin match before first draft |
| **Mechanism prose** | Alex score = **constraint-leg POC**; empirical decomposition for predictions — **one** \(L = B - D\) story in §3–§4 (SCOUT to supply nesting chain for VECTOR) |
| **Tenure (Setting 3)** | Stage 9 + limitations → start Setting 3 prose now; **one Cell 12 Cox** in parallel before submission; Fine–Gray deferred |
| **Deferred** | Army 525/TB-stratify · network extensions · full HPC sweeps · LOO generative bin-for-bin match |

### Manuscript layers (what blocks draft vs not)

| Layer | Manuscript role | Blocks first draft? |
|-------|-----------------|---------------------|
| Empirical LOO inverted-U (3 settings) | Main empirical contribution | No |
| Alex score + assignment (pool-mean readout) | Minimal generative POC + axis table | No |
| B–D nesting prose + mechanism-column predictions | §3 mechanism + §4 predictions | Yes — needs SCOUT/VECTOR write-up |
| Generative match on LOO pool quality | Ideal upgrade | **No** |

### Scientific north star (longer run — parallel, not gating)

I still think the cleanest end state is a **single decomposable generative model** that keeps the Alex score as the constraint leg (\(D\)), adds an explicit benefit/exposure channel (\(B\)) where needed, and reproduces an inverted-U on **LOO pool quality** — the same axis as the empirical stylized fact. I will pursue that **in parallel if time allows** (e.g. a bounded SCOUT nesting sprint). If it lands before submission, we upgrade §3; if not, we ship with limitations.

---

## 5. Sequenced work (next ~6–10 weeks)

```text
Week 1–2   Lock claim language · SCOUT exports (empirical Fig 2 + generative + axis table)
           · PEER Cell 12 Cox in parallel (not blocking first VECTOR draft)
           · CODA manuscript figures + estimand-checked captions

Week 2–4   VECTOR drafts Wang-structure manuscript (empirical triad → minimal model → predictions)
           · SCOUT supplies nesting chain (see §6)

Parallel   Optional SCOUT work toward LOO generative nesting (north star)
           · Tenure Cox table before submission
           · Defer: Army 525/TB-stratify, network extensions, full HPC sweeps, Fine–Gray
```

---

## 6. Internal next step (SCOUT — for your awareness)

Charles routes to SCOUT: `3-Master_Plan/20260611_0911_COMPASS_to_SCOUT_model_coherence_questions.md`

Under the manuscript-first plan, SCOUT will supply:

1. **Nesting chain** — where the Alex score lives in \(L_{\text{net}} = B - D\); mechanism-column map to B vs D.
2. **Exact sentence** VECTOR may use in §3 so reviewers do not read “two mechanisms.”
3. **Deliverables** — axis table, frozen score equation, figure paths, one prediction from the same story.
4. **Single next coding task** on the manuscript path (not an open-ended rebuild first).

This follows your April–May themes (theory ≠ minimal model; quadratic as diagnostic; assortative pools + local comparison) as I understand them. If you see a conflict with that framing, I'd like to know.

---

## 7. Tenure (Setting 3) — how I'm applying your April direction

- **Stage 9 binned figure** + honest limitations: sufficient for VECTOR to **start** Setting 3 prose.
- **One basic Cell 12 Cox run** (mirror Army: z-scored LOO pool quality, quadratic, own-performance control) — **parallel before submission**, not a pre-draft blocker.
- **Fine–Gray:** deferred.
- Matches your “end-to-end on existing data, log sample loss, then move on” guidance as I'm interpreting it.

---

## 8. Where I'd value your perspective (optional)

Not asking you to choose a path — the table in §4 is my call. If anything below looks off, I'm happy to adjust:

- Whether **manuscript-first** with honest LOO generative limitations is acceptable for a core paper you'd stand behind, vs. needing LOO generative match pre-submission.
- How you'd **nest** “score for generative curve / decomposed empirical for predictions” in one Wang object — if that's still your operational framing.
- Whether a minimal **\(B\)** (development/exposure) term in sim is the right lever for the LOO axis, vs. primarily an estimand/conditioning issue.
- Whether **CELL 7 robustness**, **CELL 4D heterogeneity**, or **Army TB-stratify** should move up from the defer list.

---

## 9. Key repo pointers

| Doc | Content |
|-----|---------|
| `3-Master_Plan/PROJECT_STATUS_AND_NEAR_TERM_PLAN.md` | Full near-term plan |
| `3-Master_Plan/20260611_COMPASS_Initial_Review.md` | Structured situational review |
| `3-Master_Plan/SCOUT_report_to_COMPASS.md` | Basketball / generative status |
| `3-Master_Plan/PEER_report_to_COMPASS.md` | Tenure status |
| `3-Master_Plan/CODA_report_to_COMPASS.md` | Army status |
| `sports/documents/538_Cell10_Generative_Manual.md` | CELL 10 implementation reference |

---

*Draft for Charles review and edit before sending to Alex.*
