# Alex Gates — talking points (next meeting)

**Date:** 2026-06-11  
**From:** Charles Levine (COMPASS-assisted draft — edit before meeting)  
**Companion:** Plan update [`20260611_Brief_for_Alex_Gates_full.md`](20260611_Brief_for_Alex_Gates_full.md) · near-term plan [`PROJECT_STATUS_AND_NEAR_TERM_PLAN.md`](PROJECT_STATUS_AND_NEAR_TERM_PLAN.md)

**Purpose:** Bullet list for the **next** conversation — inform, ask, and record what is **tabled** vs **pre-publication revisit**. Not a replacement for the plan-update brief.

---

## Inform — status bullets

- **Timeline:** Core manuscript draft/submission **Summer–Fall 2026** (see plan-update brief).
- **Empirical triad:** Army ✅ · basketball ✅ · tenure ⚠️ preliminary (CELL 9 + limitations OK for draft).
- **Generative path:** Manuscript-first — honest pool-mean POC + axis table; LOO generative bin-for-bin match **deferred** (parallel north star).
- **Army workflow:** Primary runs on **remote AWS**; Cursor repo is a **digital twin** (edit locally → hand-type on AWS → run). Latest Army plots may **not** match what CODA sees in Cursor until Charles syncs exports.
- **TB-stratify add-on:** Coded (`cr_tb_stratify.py`); default **off**; AWS parity not gating manuscript draft unless we elevate.

---

## Questions for Alex

### TB-stratified competing-risks panels

- For manuscript **v1**, should own-TB tertile panels be in the **main text**, **supplement only**, or **deferred**?
- Do you expect stratified panels in your **first read** of the paper, or is the pooled inverted-U CIF panel enough for now?
- Should routine runs keep TB-stratify **off** until we decide placement?
- Is an AWS re-run required before you’d comment, or prose + pooled Army figure sufficient for draft feedback?

### Estimand language (Cell 11 CIF vs Cell 12 Cox)

- CODA will **draft** 3–5 approved sentences distinguishing CIF bar panels vs cause-specific Cox HRs.
- **Ask:** Do these match how you want the Army layer described in a three-setting paper?
- Related: Fine–Gray is **deferred**; current stack is cause-specific Cox + empirical CIF — OK to frame that way?

### Manuscript-first vs generative LOO match (optional — if time)

- Is manuscript-first with honest LOO generative limitations acceptable for a core paper you’d stand behind?
- Should **CELL 7 robustness**, **CELL 4D heterogeneity**, or **Army TB-stratify** move up from defer — or stay parallel?

---

## Tabled — not blocking draft (Alex: keep moving)

| Item | Charles’s call |
|------|----------------|
| **525 / UIC consistency** | **Tabled.** Revisit before publication **only if** manuscript needs more Army mechanism meat. See `talent/documents/525_plans.md`. |
| **Canonical Army figure list** | **Paused.** Charles will identify cell/run profile/filenames after AWS sync; CODA in Cursor may not see latest plots. |
| **AWS TB-stratify upload parity** | Not blocking VECTOR draft unless elevated. |

---

## Charles pre-publication revisit (not blocking draft)

| Item | Note |
|------|------|
| **Senior-rater pool-size audit** | Pools **>50** (and extreme cases >100) may reflect **coding glitches** — e.g. cutoff dates superimposing distinct rating-pool events. Charles will re-audit algorithm and `snr_col` estimand **before publication**. Per your direction: **keep moving** on draft; come back when/if necessary. See `talent/documents/Pertinent_Thoughts.md` (pool-size notes). |
| **TB-stratify placement** | Pending your answers in §Questions above. |
| **Estimand sentences** | Pending CODA draft + your sign-off. |

---

## After the meeting

- Charles updates `20260611_1626_COMPASS_to_CODA_questions.md` and `PROJECT_STATUS_AND_NEAR_TERM_PLAN.md` if Alex elevates any deferred item.
- VECTOR uses approved estimand language once locked.

---

*Charles: edit freely; convert to PDF only if useful for the meeting (`convert_single_md_to_pdf.sh`).*
