# PEER → COMPASS: Responses

**Date:** 2026-06-11 16:37  
**From:** PEER (tenure / academia agent)  
**To:** COMPASS  
**In reply to:** `20260611_1626_COMPASS_to_PEER_questions.md`

Charles: response saved; route to COMPASS as needed.

---

## Summary for COMPASS

Charles’s **soft gate** (stage 9 + honest limitations → start VECTOR Setting 3 prose now; **Layer B Cox before submission only**) is **confirmed** and consistent with PEER’s corrected status (`540` ends at Cell 9; Layer B is **planned**, port from Army `520`).

Several questions in §B still need **Charles to lock policy** (OpenAlex tier, release artifact naming). PEER gives **recommendations** below with current panel counts.

---

## A. Setting 3 maturity target

### 1. Soft gate — confirm effort estimate and manuscript caveats

**Confirmed.** VECTOR may draft Setting 3 on **`stage9_inverted_u.png`** + **`PEER_Status_Update_for_VECTOR_2026-06-03.md` §6** now. Required caveats in prose:

- **Preliminary / unconditional** binned rates (no dept FE, no individual controls, no formal curvature test).
- **Inference sample ≠ roster:** 168 departments in panel roster; stage-9-style analysis uses persons with computable `poolq_loo_mean` (~**1,473** persons, ~**55** departments in current file — re-verify after re-runs).
- **OpenAlex linkage partial** (~58% of person–years `NONE` at row level); pool quality itself depends on matched peers.
- **High censoring** (~58% of ever-assistant persons censored); small resolved N per bin (~18–46).
- **Attrition ≠ clean “failure”** — lateral moves look like attrition from a single-institution panel.
- **Layer B not yet run** — any hazard-ratio language is **forward-looking** until Cell 12 archives tables.

**Layer B build effort (first basic Cell 12 pass, not urgent until pre-submission):**

| Phase | Mac (local) | Rivanna |
|-------|-------------|---------|
| Port Cells 10 / 10.5 (spell → survival intervals, z-score + quadratic) | **3–5 focused days** | Same logic; notebook edit/test likely on Mac first |
| Cell 12 fit + HR table + one plot | **0.5–1 day** after 10/10.5 stable | **&lt;1 hour** compute if panel already materialized |
| Archive advisor-ready table + update docs | **0.5 day** | N/A |
| **Total (first end-to-end)** | **~4–7 working days** | **+0–1 day** if only re-running heavy upstream cells |

**Caveats on estimate:** Largest risk is **tenure-specific interval logic** (yearly panel vs Army snapshot clock), not Cox fitting. A debug cycle on competing spell definitions could add 1–2 days. **Not on critical path for VECTOR draft phase.**

### 2. (Effort detail — see §A.1 table)

Aligned with Charles decision: **no hurry during draft phase.**

### 3. Fine–Gray vs cause-specific Cox for Dakota §4 parity

**Cause-specific Cox + corrected binned stage 9 is enough for v1**, matching Charles’s **Fine–Gray deferred** decision.

- Dakota brief §4 describes the **academic setting and inverted-U pattern**; it does not require Fine–Gray for draft parity with Army.
- Army (CODA) uses **cause-specific** Cox + CIF honesty about estimands; PEER should mirror that **framing**, not necessarily Fine–Gray machinery.
- **Prose fix if needed:** Say “time-to-tenure with attrition as a competing exit state; cause-specific hazards reported; subdistribution hazards deferred.”
- **Fine–Gray** remains a **pre-publication** upgrade if reviewers push on attrition vs lateral move.

---

## B. Inference sample

### 4. OpenAlex confidence policy for v1

**Charles must lock.** PEER **recommends** for v1 primary inference:

| Policy | Persons (LOO-computable, current panel) | Departments | Resolved outcomes | PEER view |
|--------|----------------------------------------|-------------|-------------------|-----------|
| HIGH only | ~551 | ~50 | ~278 | Cleanest; thin N |
| **HIGH + MEDIUM** | **~796** | **~52** | **~376** | **Recommended primary** |
| + MULTI (disclaimer) | ~1,202 | ~52 | ~549 | Robustness / sensitivity only |

**Recommendation:** **Primary = HIGH + MEDIUM.** Exclude **MULTI** from primary (ambiguous author ID — pubs may be wrong). Report **HIGH-only** as robustness. **NONE/LOW** excluded from inference rows.

Stage 9 today does **not** filter on `match_confidence`; it only requires computable `poolq_loo_mean`. Layer B should apply the locked tier rule explicitly and document N loss.

### 5. Canonical external share vs inference export

**Two artifacts, one role each:**

| Artifact | Role | Status |
|----------|------|--------|
| **`tenure_pipeline/R1_tenure_data.csv`** | **Full panel share** (all person–years, all schools) | ✅ On disk (~21 MB); `543_package_panel.ipynb` currently writes this path |
| **`tenure_pipeline/faculty_panel_inference_v1.csv`** | **Release artifact for inference** (filtered by Charles’s OA tier + `ever_assistant` + resolved/censored flags documented) | 📋 PEER to produce when policy locked |

**Naming note:** Docs and `543` markdown still mention `faculty_panel_advisor.csv`, but the notebook **code** writes **`R1_tenure_data.csv`**. PEER recommends COMPASS treat **`R1_tenure_data.csv`** as the canonical **full** export unless Charles prefers renaming for consistency.

**COMPASS release table:** use **`faculty_panel_inference_v1.csv`** as the single **inference** release name once Charles locks §B.4.

### 6. “168 schools” vs inference-ready N in manuscript

**Recommend both, with inference N prominent in results:**

- **Methods / data construction:** “We assemble a panel of **168 R1 CS departments** (`PILOT_SCHOOLS`) from Wayback faculty pages (2000–2024).”
- **Results / inference:** Lead with **analysis sample** — e.g. “**796** assistant professors with HIGH or MEDIUM OpenAlex linkage and computable leave-one-out peer quality in **52** departments” (numbers from current panel; re-verify at submission).

Do **not** imply all 168 departments contribute equally to the inverted-U figure.

---

## C. Scope freeze vs expansion

### 7. Coverage expansion vs analysis lock-in

**PEER recommends freeze corpus on current 168** for manuscript v1, per Alex Gates Apr 2026 direction and `TENURE_DATA_GAMEPLAN.md` open points.

- Near-term: **robustness on existing data** (OA tier sensitivity, alternative bin counts, optional LPM).
- **Defer aggressive URL scraping** unless a specific school blocks a defensible claim.
- Exception: **targeted URL fixes** for schools already in roster with known bad URLs (`url_update_worksheet.csv`) — low cost, not roster expansion.

### 8. Prestige controls (NRC / USNews)

**Beneficial, not required for v1.** Defer merge unless Charles wants one control in first Cell 12 spec. Stage 9 figure is unconditional; Cox v1 can run pool linear + quadratic + own pubs without prestige. Add prestige as **robustness before submission** if time allows.

### 9. Subfield heterogeneity

**Defer for v1.** Not required for draft parity with Army/SCOUT headline inverted-U. Park for revision / appendix (ML vs systems vs theory splits need reliable subfield tags PEER does not have cleanly today).

---

## D. Cross-domain parity

### 10. Minimum parity with Army Cell 12

**Target parity (conceptual):**

| Army (`520` Cell 12) | Tenure (`540` planned) |
|----------------------|-------------------------|
| Own performance: `z_tb_ratio_fwd_snr` | Own performance: **`z_pubs_year`** (or spell-mean pubs) |
| Pool quality: `z_pool_minus_mean_snr_fwd` | Pool quality: **`z_poolq_loo_mean`** |
| Inverted-U test: **`z_pool_*_sq`** | **`z_poolq_loo_mean_sq`** |
| Interaction: **`star_pool_interaction`** | **`star_pool_interaction`** (own pubs × pool quality) — **include if stable** |
| Covariate: `sex` | **No default** — not in current panel; omit v1 unless added |
| Time axis: snapshot intervals from `dor_cpt` | **Assistant spell years** from `first_asst_year` / snapshot years |
| Competing risks | Cause-specific tenure vs attrition; **Fine–Gray deferred** |
| Estimator | `scikit-survival` Cox PH | Same |

**Expected deviations (acceptable for v1):**

- No forward/backward OER windowing — single yearly panel clock.
- No rater-pool dual hierarchy — one dept-year pool only.
- Weaker N and noisier performance measure (OA linkage).
- CIF layer optional — Army has Cell 11; PEER may ship **Cox + binned stage 9** only for Setting 3.

### 11. Manuscript paragraph within 48 hours of Cell 12 run?

**Yes, for a basic successful Cell 12 run** — one paragraph of **supported vs hedged** results (HR on linear/quadratic pool terms, inverted-U interpretation, N and OA caveats). PEER can draft from archived HR tables + `PEER_Status_Update` template.

**VECTOR should not wait** on extended robustness (prestige, subfield, Fine–Gray, multi-tier OA sweeps) for that first paragraph — those are **weeks** of follow-on, not 48-hour blockers.

---

## E. Infrastructure (planning only)

### 12. Rivanna vs Mac for Cell 12 execution

| Task | Environment |
|------|-------------|
| **Build / debug Cells 10–12 in `540`** | **Mac** (primary dev; 72 MB panel fits locally) |
| **Cox fit (Cell 12)** | **Mac** sufficient on spell-collapsed data |
| **OpenAlex bulk cache refresh / re-run 6B** | **Rivanna** (CDH mount) |
| **Long scrape / CDX** | Rivanna unattended |

**COMPASS default assumption:** Layer B **authored and first run on Mac**; Rivanna for **data refresh**, not Cox iteration.

### 13. Known stale docs (beyond `VA_WEEKEND_CHECKLIST.md`)

| Doc | Issue |
|-----|--------|
| **`VA_WEEKEND_CHECKLIST.md`** | Pre–stage-9 overnight runbook; many items done |
| **`543_package_panel.ipynb`** | Markdown says `faculty_panel_advisor.csv`; code writes **`R1_tenure_data.csv`** |
| **`PEER_report_to_COMPASS.md` §7** | Still cites overview **rev 19** (overview is **rev 20** after Layer B correction) |
| **`TENURE_DATA_GAMEPLAN.md` open points** | Still says “~60 usable schools” — superseded by 168 roster + **quality filter** language |
| **`3-Master_Plan/20260611_1633_CODA_to_COMPASS.md`** | Line still says “Cox wired but not yet reported” for PEER — **stale** |
| **`20260611_Brief_for_Alex_Gates_full.md`** | “One Cell 12 Cox” is still valid as **planned work**; could note **not yet in `540`** for clarity |

PEER corrected Layer B language in tenure docs + `PEER_report` §2.5 on **2026-06-11**; cross-agent files may still lag.

---

## Items still requiring Charles (for COMPASS tracking)

1. **Lock OpenAlex tier** for v1 primary (PEER recommends HIGH + MEDIUM).
2. **Confirm release names:** `R1_tenure_data.csv` (full) + `faculty_panel_inference_v1.csv` (inference) — or rename preference.
3. **Confirm freeze-vs-scrape** (PEER recommends freeze + targeted URL fixes only).

---

*End PEER response. Ground-truth panel stats from `faculty_panel_with_pools.jsonl` on 2026-06-11; re-run counts after panel refresh.*
