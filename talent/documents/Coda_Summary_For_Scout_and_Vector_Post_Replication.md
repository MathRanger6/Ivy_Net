# Coda → Scout & Vector: Post-replication sync (Army thread)

**From:** Coda (Army / `520` Cox & competing-risks plotting thread with Charles)  
**Date:** 2026-06-08 (rev 2 — third setting PEER active)  
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
| **`520_pipeline_cox_working.ipynb`** | End-to-end Cox + Cell 11 plotting (KM / competing risks, binning, filters). **Cell 11 add-on:** `cr_tb_stratify` when `CR_TB_STRATIFY_CONFIG["enabled"]`. |
| **`cr_tb_stratify.py`** | Own-TB stratum tertiles (quantile or equal-width); re-runs CR + CIF bars per stratum after main Cell 11 loop. |
| **`cox_plot_helpers.py`** | `plot_competing_risks_cif_bars`, palettes, TB-stratify title suffix, etc. |
| **`pipeline_config.py` / overrides (e.g. `pipeline_config_19_1.py`, `pipeline_config_div_name.py`)** | Plot specs, bin counts, filters, **`CR_TB_STRATIFY_CONFIG`**. |
| **`talent/documents/CR_TB_STRATIFY_Advisor_Three_Panels.md`** | Advisor-facing TB-stratify feature doc (enable, upload list, interpretation). |
| **`talent/documents/CR_Red_Line_Flow_Explanation.md`** | Plain-English Cell 11 CR curve / bin construction. |
| **`talent/documents/README_Talent_Layout_Symlinks_And_AWS_Export.md`** | Canonical paths, AWS export vs ground truth. |
| **`talent/documents/Army_to_College_Basketball_Replication_Handoff.md`** | Longer **replication design** handoff (still useful for history). |
| **`talent/documents/Agent_Read_First_Coda_Runbook.md`** | Short runbook + copy-paste message to Scout. |

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

## 8. Third setting — PEER (academia / tenure) — **active June 2026**

Charles and **PEER** (`tenure/`, `540_tenure_pipeline.ipynb`) are now building Setting 3: CS faculty at R1 universities, Wayback rosters + OpenAlex pubs, LOO dept peer quality (`poolq_loo_mean`), outcome = tenure (Asst → Assoc). **Stage 9** (May–June 2026) shows a **preliminary inverted-U** in binned tenure rates (peak bins 16–17, drop bin 18). Coda’s Cox/competing-risks stack is **not** the implementation vehicle, but Army’s **advancement vs attrition** framing is the template PEER is adapting (see `tenure/documents/TENURE_DATA_GAMEPLAN.md`, `5-Manuscript/PEER_Status_Update_for_VECTOR_2026-06-03.md`). Cross-domain committee brief: `5-Manuscript/advancement_under_constrained_distinction_dakota_feedback_v03.rtf`.

---

## 9. April 2026 Army coding updates (Coda thread — post-replication)

| Item | Status |
|------|--------|
| **Own-TB stratified CR add-on** | Implemented; default **off**; enable in `CR_TB_STRATIFY_CONFIG`. |
| **AWS export merge** | Aligned live tree to `TALENT_NET_export_20260421-0802`; TB-stratify re-applied; backup in `obsolete_files/talent_pre_bar_stratify/`. |
| **Senior rater pool size audit** | **Open concern:** `pool_size_snr_*` can exceed 100 under current `(snapshot_date, snr_col)` grouping — may be definitional, not data error. See `Pertinent_Thoughts.md`. |
| **Cross-agent master plan** | Charles initiating **COMPASS** agent; feed **`3-Master_Plan/CODA_report_to_COMPASS.md`** (+ SCOUT/PEER/VECTOR reports). **Do not** start planning until Charles assigns the agent. |

---

*End Coda summary. Last updated 2026-06-08.*
