# Coda → Scout & Vector: Post-replication sync (Army thread)

**From:** Coda (Army / `520` Cox & competing-risks plotting thread with Charles)  
**Date:** 2026-04-02 (update as needed)  
**Purpose:** Align all three agents on what the Army side **did** and **showed**, now that Scout has reproduced the **inverted-U** pattern in college basketball.

---

## 1. Status

Charles and Scout replicated the **qualitative shape** of the Army finding in a **public, replicable** setting: draft propensity vs **leave-one-out teammate pool quality** in MBB. The parallel is **strategic and interpretive** (nested talent pools, congestion at the top), not a claim that promotion hazards equal draft odds.

---

## 2. Army setting (what Coda’s stack is built for)

- **Population:** U.S. Army officers observed after promotion to Captain; time-to-event is framed from that anchor through promotion to Major, attrition, or censoring (competing risks).
- **Core empirical pattern (paper / advisor narrative):** Upward mobility vs **peer pool quality** is **nonlinear**: stronger association in the **middle** of the pool-quality distribution, with **lower** estimated promotion incidence at the **highest** pool-quality bins—consistent with **scarce slots**, **congestion**, or **signal** stories at the elite tier.
- **Figure type Charles shared (CIF bar panel):** Eight ordered bins (**Q1–Q8**) on a **pool-quality** construct; **y-axis** = **final cumulative incidence** of **promotion** (promotion as the event of interest in the competing-risks display). The bars show a **rise** through the mid bins and a **drop** in the top bins (inverted-U / “elite tier” dip).

---

## 3. Pool-quality definition (Army — Charles’s clarification)

**Naming note:** “Pool minus mean” in Charles’s usage means **the pool mean computed without the officer’s own contribution** to that mean (leave-self-out / LOO logic on the rating pool), **not** “pool minus a fixed cohort mean” as a separate operation.

**Implementation detail:** Built from **OER / senior-rater** style inputs in the time-varying survival panel (`df_time_varying` → `df_cox`), with plotting in **`520_pipeline_cox_working.ipynb`** and **`cox_plot_helpers.py`**. For **competing-risks bar panels**, officers are **stratified** by binned pool quality; **within each bin** the display summarizes **promotion** incidence over follow-up (see earlier CR_AND_HR / pipeline notes: Cell-11-style curves are **nonparametric within-bin** summaries, not a Cox fit on pool inside that plot).

**What to stress to outsiders:** Each officer’s **bin** reflects **peers’** contributions to the pool measure **excluding self**; **own** rating is **not** averaged into **own** pool statistic by construction.

---

## 4. Code / document map (Army)

| Item | Role |
|------|------|
| `520_pipeline_cox_working.ipynb` | End-to-end Cox + Cell 11 plotting (KM / competing risks, binning, filters). |
| `cox_plot_helpers.py` | `plot_competing_risks_cif_bars`, palettes, `apply_unknown_group_by_filter`, etc. |
| `pipeline_config.py` / overrides (e.g. `pipeline_config_div_name.py`) | Plot specs, bin counts, filters. |
| `current_documents/Army_to_College_Basketball_Replication_Handoff.md` | Longer **replication design** handoff (still useful for history). |
| `current_documents/Agent_Read_First_Coda_Runbook.md` | Short runbook + copy-paste message to Scout. |

---

## 5. For Scout (what Coda needs you to mirror in prose)

Please keep your companion note **technical**: grain (**player–season**), **`poolq_loo`**, **`PERF_METRIC`** (e.g. **ppm**), **z-score within season** if used, **binning** (quantile vs equal-width, **n** bins), **winsorization**, **min minutes**, **team draftee restriction** on/off, **season window** (e.g. **2011–2021**), **`Y_draft`** definition (ever-draft v0), and **draft register / ESPN box** provenance. Charles’s **8-bin** college bar chart should be described **side-by-side** with the Army **Q1–Q8** panel for advisors.

---

## 6. For Vector (memo + Brian email)

- Use **`Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md`** (companion file) for **Army-only** bullets safe to merge with Scout’s basketball brief.
- Charles’s **intro** (nested pools, middle hierarchy, elite-tier scarcity) is the **shared frame** across Army and basketball; keep **estimands distinct** (promotion CIF in bins vs **mean draft rate** in bins).

---

## 7. Re: “Should Scout re-read the old Coda handoff only?”

**Recommendation:** Keep **`Army_to_College_Basketball_Replication_Handoff.md`** and the **runbook** as **reference** for pipeline archaeology and design intent. For **current alignment** after successful replication, **this file + `Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md`** are the **primary** updates—so Scout should read **those** in addition to (not instead of) the handoff if they need full Cox detail.

---

## 8. Next horizon (tenure / academia)

Charles noted a possible **third setting**: academic careers and tenure. Coda’s stack is **not** the vehicle for that; Vector + Charles should specify **grain** (person-year? department?), **pool** (LOO coauthor? department peers?), and **outcome** (tenure, placement). Army + basketball docs become **templates** for measurement discipline, not copy-paste code.

---

*End Coda summary.*
