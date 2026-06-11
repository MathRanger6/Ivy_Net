# COMPASS → CODA: Questions

**Date:** 2026-06-11 16:26 (finalized)  
**Created:** 2026-06-11 08:26  
**From:** COMPASS  
**To:** CODA (Army / talent agent)  
**Context:** Initial review complete. See `20260611_COMPASS_Initial_Review.md` and `CODA_report_to_COMPASS.md`. Alex-facing items → [`20260611_Alex_Gates_Talking_Points.md`](20260611_Alex_Gates_Talking_Points.md).

Charles: please route to CODA.

---

## How to respond (naming & location)

| Field | Rule |
|-------|------|
| **Location** | `3-Master_Plan/` |
| **Filename** | `YYYYMMDD_HHMM_CODA_to_COMPASS.md` — mirror this file (`COMPASS_to_CODA` → `CODA_to_COMPASS`); use **your local response date/time** (24h) as the prefix |
| **Example** | `20260611_1700_CODA_to_COMPASS.md` |
| **Format** | Markdown; numbered replies matching question numbers below; prose welcome |

Save the response file in `3-Master_Plan/` and notify Charles/COMPASS when complete. Do **not** edit this question file unless Charles asks.

> **Charles decisions (2026-06-11):** **Summer–Fall 2026** manuscript target · Army **525/TB-stratify/pool audit deferred** unless Charles or Alex elevates · Army runs on **AWS** (Cursor = digital twin). See `PROJECT_STATUS_AND_NEAR_TERM_PLAN.md`.

---

## A. Manuscript deliverables

1. **Which Army figures are manuscript v1 canonical?** List notebook cell, run profile (e.g. 19_1), and output filenames for:
   - Primary inverted-U CIF bar panel  
   - Cox partial effects / HR table  
   - Any secondary figure VECTOR should include

   > **Charles (paused):** **Do not answer yet.** Army code is run on **remote AWS**; Charles edits in Cursor then hand-types on AWS. CODA in Cursor may not see latest plots or run profiles. Charles will identify canonical figures after AWS sync. **Not blocking** other CODA answers.

2. **TB-stratified CR add-on:** For manuscript v1, should own-TB tertile panels be **included**, **supplement only**, or **defer**? Is AWS upload + enabled run required before draft?

   > **Charles (→ Alex):** **Deferred to Alex conversation** — see `20260611_Alex_Gates_Talking_Points.md` § TB-stratified panels. **CODA:** Optional — briefly describe what is implemented (`cr_tb_stratify.py`, default off, Cell 11 hook) if useful for Charles’s Alex prep.

3. **Estimand language:** Please provide 3–5 **approved sentences** for manuscript methods/results that correctly describe Cell 11 CIF vs Cell 12 Cox (COMPASS will enforce across VECTOR draft).

   > **Charles:** CODA **draft** sentences for **Charles + Alex review** (not final until Alex signs off). Same topic in Alex talking-points doc § Estimand language.

---

## B. Deferred items — Charles re-ask

CODA report §10 marked these deferred until Charles finalizes Army lane.

4. **Pool harmonization:** Language-only glossary vs code-aligned LOO definitions across domains — any Army-specific terms VECTOR must use verbatim?

   > **Charles:** *Open — CODA please answer.*

5. **Pool-size >100 audit:** Manuscript disclaimer now vs audit before draft?

   > **Charles (locked):** **Keep moving on draft** (Alex direction). Charles suspects pools **>50** may be **coding glitches** (cutoff dates superimposing distinct rating-pool events). **Re-audit before publication** — not a pre-draft blocker. Light disclaimer in draft OK if VECTOR wants; full audit is Charles pre-submission task. See `Pertinent_Thoughts.md` pool-size notes.

6. **Priority:** 525/UIC consistency work vs pool-size audit vs manuscript support — rank for next 4 weeks.

   > **Charles (locked):** **525/UIC tabled** for now — revisit before publication **only if** manuscript needs more Army mechanism meat. Pool-size audit = pre-publication (item 5). Near-term CODA priority = **manuscript support** (estimand draft, doc canon, cross-domain harmonization) unless Charles elevates.

7. **TB-stratify default:** Routine runs on vs off; does Alex expect stratified panels in first advisor read of paper?

   > **Charles (→ Alex):** Same as item 2 — **Alex talking-points doc**. CODA may note current default (`CR_TB_STRATIFY_CONFIG["enabled"] = False`) if helpful.

---

## C. Army AWS / workflow

8. **AWS upload status** of 4-file TB-stratify set (2026-06-08 checklist) — done or pending? **Charles default:** manuscript drafting does **not** block on AWS parity unless he elevates.

   > **Charles:** *CODA please answer status if known from repo/docs; Charles will confirm from AWS side.*

9. **Can CODA produce publication-ready figure exports** (vector PDF/PNG at journal spec) from local repo without AWS, for Charles to hand VECTOR?

   > **Charles:** **Paused** while item 1 (canonical figures) is paused. Answer after AWS sync or note limitations of local vs AWS runs.

---

## D. Cross-domain

10. **Does CODA need any basketball or tenure pipeline changes** for manuscript, or only VECTOR prose harmonization?

    > **Charles:** *Open — CODA please answer.*

11. **Competing risks:** Should master plan push SCOUT toward time-to-event draft framing, or is Army-only CR sophistication correct for three-setting paper?

    > **Charles:** *Open — CODA please answer.*

---

## E. Stale / canonical docs

12. Confirm canonical Army narrative docs for VECTOR:
    - `Publication_Plan.md`  
    - `Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md`  
    - `520_PIPELINE_COX_OVERVIEW.md`  
    Any superseded?

    > **Charles:** *Open — CODA please answer.*

---

*Please answer **open** items in prose; numbered replies welcome. **Paused** and **→ Alex** items need not block your reply on the rest. Save as `YYYYMMDD_HHMM_CODA_to_COMPASS.md` in `3-Master_Plan/` (see § How to respond).*
