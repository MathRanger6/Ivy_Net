# DISPOSABLE — Chapter 3, data and empirics (started 2026-11-05)

**Purpose:** Working record for the data-and-empirics chapter. Source of the chapter order: PD52, 11-04, Alex. Transcript: `3-Master_Plan/VECTOR_work/new_VECTOR_work/Introduction_Agent_Handoff_20261027/transcripts/20261104_Paper_Directions_52_otter_ai_transcript.docx`.
**Say `anchor`** in chat to paste **YOU ARE HERE**.

**FOUNDY (thesis drafting):** comprehensive Q&A — [`20261109_FOUNDY_Response_Ch3_Army_data_questions.md`](../VECTOR_work/new_VECTOR_work/20261109_FOUNDY_Response_Ch3_Army_data_questions.md) (answers the morning questions list). Index: [`20261109_FOUNDY_Handoff_Chapter3_data_empirics.md`](../VECTOR_work/new_VECTOR_work/20261109_FOUNDY_Handoff_Chapter3_data_empirics.md). This disposable = live log + Army prose seed.

The literature-review thread stays in `_DISPOSABLE_FOUNDY_Introduction_thread.md`. This file does not reopen it.

---

## YOU ARE HERE

| Step | Task | Status |
|------|------|--------|
| **0** | Executive summary of this chapter, readable without column names | **Drafted 11-09** (about 1,100 words): `3-Master_Plan/VECTOR_work/new_VECTOR_work/20261109_Ch3_executive_summary_DRAFT.md`. Waiting on Charles; six bracketed items inside. Revise after the detailed sections exist. Original brief: About **2 pages.** Alex, 11-05: same pattern as the literature review. Draft the argument and the four systems first. Revise after the detailed sections exist. The 10–20 page remark is set aside. |
| **1** | State the criteria for a system in which the question can be measured cleanly | **Stated below**, from Alex on 11-04. Belongs in the executive summary in prose. |
| **2** | Army detail, from raw columns up | **The draft below starts too late.** `tb_ratio_fwd_snr` is a late column. The chain to read is `talent/talent_pipeline/`: 501, 502, 503, 504/509, 512, `build_df_masters.py`, then 520. |
| **2a** | Army outcome (Charles + Alex, 11-05) | **Decided.** Two final-probability histograms: promotion and attrition, by band. **Promotion = any promotion to major** (`dor_maj`). **BZ / survival backstory (Alex, 11-09):** **footnote only (A)** or **omit from Ch.3 (D)** — not a full paragraph. Default recommendation: **A** (one footnote) so readers know why attrition sits beside promotion; Cox/survival still not developed. |
| **2b** | Army **placeholder figures** (Charles, 11-09) | **Picked.** Promotion yes/no only — no sex, prestige, MOS, or other descriptive CR panels. Use flipbook CIF bars + optional Way_Ahead mosaic; annotate **as-run** filters + Vantage TBD. See **§ Army placeholder kit** below. |
| **3** | Romanian education: same two parts | Waiting |
| **4** | Basketball / NBA draft: same two parts | Waiting. Points per minute is the performance measure Alex named. |
| **5** | Tenure: same two parts | Waiting. Charles, 11-04: include it with the other three. |
| **6** | Results | **Not yet.** Alex: build the data story before presenting results. No model in this chapter. |

**One-sentence line:** A system is worth studying when a person's performance can be measured, the person sits in a group that is not a random draw, a fixed number of slots is filled from across the system, and outsiders are not constantly entering.

---

## What this chapter is

Chapter 3 is the empirical chapter. It has two movements, in this order.

1. **The systems.** The literature review has stated the question. This chapter says what a system has to be like for that question to be measurable, then shows that the systems we use are that kind of system. For each one: where the data came from, how they were cleaned, and which column corresponds to which concept. Alex said this data description is the science, and that in a paper it becomes the supplementary data section.
2. **The results.** Only after that. No model. Assignment, and the fact that groups are not random, is Chapter 5. Development is not the subject.

Alex said "five data sets" without naming a fifth. In the same stretch he named three: the Army, Romanian education, and the NBA draft (the transcript says "MBA draft"; that is the draft). He used basketball points per minute as the example of a performance measure, so the draft and the college-basketball performance are one system in that telling. Charles, later on 11-04: the chapter includes four — those three, plus tenure.

## Criteria (Alex, 11-04)

A usable system has all of these.

- An individual performance measure that can actually be observed. Sales might work. A general business setting usually does not, because there is no such measure.
- People in groups, and the groups have structure. They are not a purely random draw.
- Global selection. The slots are filled from across the system, not only inside one group.
- A finite number of slots. The bar moves with how many slots there are. It is not a fixed passing score that everyone can clear.
- Little outside noise. Not an open system with people constantly coming and going. The Army case of this is no lateral entry.

The same criteria are why other systems were not used. They are also why a system not in the dissertation, such as League of Legends, could be one later. The chapter should say that the criteria travel, and that these are the systems in hand.

What the criteria are not: a claim about development, and not a prediction that more peer talent eventually hurts.

## Army — draft of the data section

The Army is the first system because it matches the criteria, and because the records exist. The section does not open with how often captains are promoted, and it does not compare the Army with basketball. Those are results.

### Why it matches

Officers are evaluated, and the evaluation is a recorded performance measure. They are rated inside senior-rater pools, which are organized groups rather than a random draw. Promotion boards select from across the Army. The number of officers who may be promoted is set in advance, so the bar moves with the number of slots. Mid-career lateral entry does not refill the pool; the pool changes by commissioning and by exit.

One complication belongs in the mapping, not in a footnote. The rating a performance receives already depends on the other officers in the same pool. The performance measure is therefore not a pure record of what the officer did.

### Where the records come from

Two files are joined.

The first is a series of personnel snapshots from the Army's human-resources system. Each row is an officer on a snapshot date. Notebook 502 produces this extract. The analysis keeps commissioned officers and drops inconsistent appointment dates when it builds the year group.

The second is the officer evaluation report file. Notebook 512 attaches the rater and the senior rater to each evaluation, including the unit codes those raters need. The analysis notebook, 520, joins that file to the snapshots.

Every row then sits on two clocks. The snapshot date is a day on the personnel calendar. The evaluation has its own start and through dates. Those two clocks are not the same day.

### Which variable is which concept

| Concept | What is used | Column in the current run |
|---------|----------------|---------------------------|
| Own performance | Share of completed evaluations, as of the snapshot date, on which the senior rater gave the top box. "As of the snapshot" means the latest evaluation whose through date is on or before that day. | `tb_ratio_fwd_snr` |
| Who the senior rater is | The senior rater on the evaluation whose window covers the snapshot date. | `snr_rater_bwd` |
| The group | Officers who share that senior rater. | Pool built from `snr_rater_bwd` |
| Own performance relative to the group (the horizontal axis of the HERO bars) | **Own** top-box share **minus** the mean of the **others'** top-box shares in the pool (the officer is left out of that mean). **Corrected 2026-11-09:** an earlier version of this row said the opposite. Confirmed in `_add_pool_mean_size` in the 20260320 export's `add_cum_oer_metrics_mod_working.py`: `pool_minus_mean = value_col - mean`, with `exclude_self=True`. | `pool_minus_mean_snr_fwd` (z-scored in the plots) |
| Quality of the group alone | Mean of the others' top-box shares, officer left out. This is the pure peer measure ("straight LOO"). **Not** what the March HERO bars plot. | `pool_tb_ratio_mean_snr_fwd` |
| The outcome | **Promotion to major (any timing)** when `dor_maj` is observed; attrition if the officer leaves the extract before study end without major. Below-zone timing was the original research motivation but is **not** the coded event on the chapter histograms. | Cell 10 `event` 1/2/0; chapter bars from Cell 11 CIF bars / HERO |

Both columns average the forward top-box share, and the backward senior-rater identity defines who is in the group.

### The cleaning problem that changes the group

The pool is currently everyone on the same snapshot date who has the same senior-rater identity. A senior rater's real rating pool is the officers in one rating chain for one evaluation window. The snapshot-day rule pulls in officers from different windows, so computed pools run larger than the pool size written on the evaluation itself.

Checked 2026-09-20: the computed pool size at the last snapshot has median 23, and 19 percent of those pools exceed 50. The official count of how many in that grade the senior rater rates has median 12. Until the pool is redefined as one senior rater and one evaluation window, the group in the file is wider than the group the Army rated.

### Cohort window: year groups and snapshots

Officers who are still in the file at the last snapshot, without a major promotion and without a recorded exit, count as **not promoted** in the bar charts but are **censored** with respect to full career time. Charles controls **which year groups enter** and **how far the snapshot series runs** so that included cohorts have had a fair chance to reach the major board before the extract ends. That is why **`filter_ygs`** matters: drop the newest YGs that are still inside the captain window at study end; keep a band old enough that promotion and attrition are largely resolved. FOUNDY should state this design intent in the Army subsection (see CODA response §2, `filter_ygs` row).

### Component (`compo`) — Regular Army (`R`) (Charles, 2026-11-09)

In PDE, **`compo` is a string**; **`R` = Regular Army** (reserve/guard use other codes). The **502 → 520** path does **not** drop every `pid_pde` who **ever** had a non-`R` row. **`compo == 'R'`** is used when building year group and some duplicate-date checks (CPT rows, RA appointment rows). An officer can still appear later as CPT (or other rank) with **non-`R` component** on some snapshots.

**Chapter framing (Charles):** The study is the **Regular Army CPT→MAJ promotion pool**. Leaving active-duty Regular Army (including transfer to another component) **exits that pool**—same practical consequence as attrition for this chapter. **Major promotion in another component** is a **different selection system** and is **out of scope**; we do not need a separate component-level event code if disappear-from-RA is already coded as attrition (`event = 2`) when the officer leaves the extract before study end.

**Still to run on Vantage:** count officers with **mixed component** histories (e.g. CPT with both `R` and non-`R` snapshots). Until then, methods prose can state the rule above and note that counts are **TK**.

**Annotation draft (methods or footnote):** *Analyses restrict interpretation to officers observed in the Regular Army competitive category for promotion to major; officers who leave Regular Army service before major selection are treated like other exits from the study pool (attrition), not as censored promotion opportunities in reserve or guard components.*

### Not in this section yet

Results. Also not re-counted here: the September deck's figures for the captain-to-major panel (on the order of 258,000 person-intervals, and a Cox subsample of about 15,000). Per-figure branch filters stay with those figures; **global YG/window logic** belongs in methods above.

## Army placeholder kit (Vantage TBD — Charles 11-09)

**Scope:** Promotion yes/no (any promotion to major) plus attrition band beside it. **Out of scope for now:** sex, prestige, MOS/job-code **faceted CR panels**, Kaplan–Meier demos (`First_good_plots.pdf` → archive only).

**Still in scope (methods):** **Year-group filter + snapshot/study window** — Charles uses these to keep officers inside realistic CPT→MAJ promotion possibility and **reduce censoring** (unresolved `event = 0` at last snapshot). Chapter prose must explain *why* the YG list and extract end date were chosen, not only that they were applied. March placeholder run: **YG 2002–2011** (`filter_ygs` enabled in export `20260320-1000` base config); filename years `2002–2022` = snapshot span in plotted data.

### Plug-in now (repo)

| Slot | File | Why |
|------|------|-----|
| **Hero — peer environment** | `3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/ARMY_G1_pool_minus_mean_fwd_cif_b8.png` | Alex’s two **final-incidence** bar panels by performance band; peer = z pool minus mean (fwd). **Run of record** until Vantage matches. |
| **Companion — own measure** | `…/ARMY_own_tb_ratio_fwd_cif_b8.png` | Same filters/binning; own TB ratio (fwd). Optional second figure in data section. |
| **Optional — shows time** | `…/ARMY_G1_pool_minus_mean_fwd_CR_curves.png` | Same variable; cumulative curves (mention in caption, not survival chapter). |

**Do not use for Ch.3 placeholders:** `ARMY_tb_by_division_cif_b1`, interaction/Cox diagnostic PNGs, `Show_me/Army Figure.png` (single promo bar only, no attrition).

### Optional — pre-shutdown data story (Dropbox, not git)

`2-Way_Ahead/Army_Combination_Data_Stories/Slide66.png` (or **one** variant you choose — 15/38/56/76 differ on panel 9). Use for **“pipeline produces a data story”** illustration only; **N ≈ 39,517** and straight-LOO story ≠ March CIF run. Caption as **exploratory mosaic**, not run of record.

### Figure note (paste under each placeholder)

> **As run (March 2026 AWS export, Run 1 · `pipeline_config_17_1` in export `20260320-1000`).** Officers at last snapshot; **promotion = any event to major**; attrition = exit without promotion. Bins: 8 equal-width on **z-scored pool minus mean (forward SNR)**; officers with no OER excluded (`noOER`); year-group filter **2002–2011** in that export’s base config. **N = 31,692** across bins (per sandbox legend). *Planned Vantage rerun:* [straight LOO / pool grain / YG — TBD]; bands and counts may change—figure will be replaced when bars match.*

### After Vantage

Replace files in place; keep the same caption template with “Vantage run [date]” and updated filter line.

---

## Army — decisions and placeholder language (2026-11-09, 13:55)

**Decision (Charles):** the Army horizontal axis in this chapter is **peer quality alone**: the leave-one-out mean of the others' top-box shares in the pool (`pool_tb_ratio_mean_snr_fwd`, then z-scored). The March bars plot `pool_minus_mean_snr_fwd` (own minus that mean), so they are **placeholders** until the Vantage rerun.

**Decision (Charles):** use placeholder language wherever the Vantage rerun will change a number.

Sentences to use until the rerun (bracketed text is filled in later):

- **Figure caption.** "Placeholder. This figure was produced in March 2026 and plots each officer's own top-box share minus the mean of the other officers in the senior-rater pool. The version for this chapter will plot the mean of the other officers alone. Bands and counts will change when it is rerun."
- **Counts.** "[N officers in the analysis, from the Vantage log.] In the March run, 31,692 officers fall in eight performance bands."
- **Flow table.** "[Officers retained at each filter step, from the Vantage log.]"
- **Officers still open.** "[Number in each band with no promotion and no exit by the end of the data.] In the March run, promotion and exit together account for roughly 95 to 100 percent of each band."
- **Exits.** "An officer who leaves the data without having been promoted to major is counted as an exit. [Component: the analysis refers to the Regular Army promotion pool. Whether an officer who moves to the reserve components drops out of the data, and so counts as an exit, depends on the source extract. Fill in once the count of officers with more than one component is known. See the 14:15 log entry.]"

---

## Thread log

- **2026-11-05 14:24** — Charles: literature review is in good shape; start data and empirics. Opened this file. Next piece is the Army as a match to the criteria, then its provenance and variable mapping. Results wait.
- **2026-11-05 14:40** — Charles: go. Army data section drafted from the 520 overview and the 2026-09-20 pool note. [Corrected 11-09, see the log entry at the bottom: "pool minus mean" is own performance minus the leave-one-out mean of the others, not the mean alone.] Pool membership is still the known problem: snapshot day plus senior rater, which inflates the pool. Results not started.
- **2026-11-05 14:49** — Charles, after talking to Alex. (1) The Army draft starts too far downstream; raw columns are synthesized in `talent/` long before `tb_ratio_fwd_snr`. (2) This chapter gets an executive summary first, then the detailed sections, then a revision of the summary. (3) The summaries are what the committee actually reads.
- **2026-11-05 14:51** — Charles corrects (3): the 10–20 pages is the sum of every executive summary in the dissertation, not the length of this chapter's summary.
- **2026-11-05 14:52** — Charles: set the 10–20 pages aside. This chapter's executive summary should be about 2 pages.
- **2026-11-05 15:06** — Charles, after Alex. Survival analysis had no place in the PD52 chapter plan. History to tell: early promotion was the first candidate measure of success, because promotion is one of the few ways the Army can treat a high performer differently (no pay incentive; per the proposal). The competing-risks curves were cumulative curves for bands of performance. Their endpoints became two histograms, final promotion and final attrition. Those histograms are where HERO first appeared, and they led to the other domains. Decision: the chapter uses the final promotion and attrition histograms. Survival analysis and the 3D plots were a large body of work and could be their own paper or chapter; they are mentioned, not developed, unless time allows.
- **2026-11-05 15:09** — What the bar is, checked in `talent/talent_pipeline/cox_plot_helpers.py` (`plot_competing_risks_cif_bars`) and `talent/documents/CR_Red_Line_Flow_Explanation.md`. Promotion bar = officers in the band with a promotion event ÷ officers in the band; attrition bar the same for exits. Officers still open at the last snapshot stay in the denominator and count as not promoted. The band is assigned from each officer's last row. The curves are a running share out of a fixed group, not a censoring-adjusted incidence estimate. Chapter needs: the number still open per band, or a year-group restriction.
- **2026-11-05 15:12** — Charles recalls choosing year groups and the window so the last year group had time to be promoted. Configs: base `pipeline_config.py` and `pipeline_config_19_1.py` restrict to YG 2002–2011; `pipeline_config_17_1.py` sets `filter_ygs['enabled'] = False` (list present, not applied). The date filter is off everywhere; 2000-01-01 to 2022-06-30 is written but not applied, so the window is the extract's coverage. The 2026-09-20 note says Run 1 = base + 17_1, which would mean no YG restriction in Run 1. The September deck said "~2002–2013" for CS+CSS. **To settle on AWS:** (a) which config produced the HERO histograms; (b) count per band of officers with no promotion and no exit (event 0) at the last snapshot; (c) snapshot date range of the extract.
- **2026-11-05 15:15** — Charles: the Army system has moved from AWS to **Palantir Army Vantage** over the last six weeks; confirmation waits on that. Settled from the repo first. `3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/EXTRACT_MANIFEST.txt`: the HERO bars (`ARMY_G1_pool_minus_mean_fwd_cif_b8.png`) came from `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/520_pipeline_cox_working.ipynb`, original name `cr_z_pool_minus_mean_fw_none_b8_ew_noOER_2002-2022_cif_bars.png`. In that export, the base config restricts YG 2002–2011 and `17_1` does not override it; the `enabled: False` exists only in the later local `17_1`. Filename code: `b8_ew` = 8 equal-width bins, `noOER` = officers with no OER excluded, `2002-2022` = first and last snapshot year in the plotted data. Promotion + attrition per band ≈ 0.95–1.00, so at most about 5% unresolved in any band. Band sizes, from the curve legend: 49, 1,423, 7,644, 8,131, 7,906, 4,130, 2,153, 256 (total 31,692); the top-band drop rests on 256 officers. **Vantage to confirm:** run of record; exact open count per band; snapshot dates.
- **2026-11-09 12:35** — Charles asked whether CODA needs questions (CODA built most Army products from raw data). Drafted `3-Master_Plan/VECTOR_work/new_VECTOR_work/20261109_Ch3_Questions_for_CODA_raw_to_dataframes.md` (8 questions: raw sources, filters in order with counts, event definitions, top-box build, run of record, superseded files, quirks, what can be printed). Draft only; Charles approves before sending. Row 2 (Army raw-column trace) waits on the answers or on reading the code; row 2a open question (early vs any promotion) is Q3.
- **2026-11-09 ~12:40** — Charles: stop MCQ drill; confirms history (BZ → survival/CR → CIF bars → HERO). **Lock Ch.3:** any promotion to major. CODA response updated §3a + header; disposable row 2a closed.
- **2026-11-09 ~12:48** — Charles: OER/EES evaluation data **approved** (Combined Data / Talent Net DUAs). CODA §8 updated; Ch.3 OER methods prose cleared. Vantage = same PDE-A (cite PDE in print).
- **2026-11-09 ~12:54** — Charles + Alex: BZ/survival **history** in Ch.3 = **footnote (A)** or **omit (D)** only; no short paragraph / sidebar unless Alex changes mind.
- **2026-11-09** — Charles: exported AWS ≠ live configs; screen captures may beat repo. **`3-Master_Plan/re_entry/ARMY_PLOT_PROVENANCE_AUDIT.md`** — figure inventory, filename filters, config-tree warnings, hunt list.
- **2026-11-09 ~13:32** — Charles: Ch.3 placeholders = **promotion yes/no only**; sex/prestige OBE. Locked flipbook CIF bars + caption template (Vantage TBD); optional Way_Ahead mosaic non-canonical.
- **2026-11-09 ~13:36** — Charles: FOUNDY needs max context for Ch.3 drafting. **`20261109_FOUNDY_Handoff_Chapter3_data_empirics.md`** created (VECTOR_work); links disposable, CODA, figures, locked decisions.
- **2026-11-09 ~13:40** — Charles: **YG + snapshot window** are core methods (minimize censoring / follow promo possibility)—not retired with sex/prestige panels. Handoff + disposable updated.
- **2026-11-09 ~13:44** — Charles: FOUNDY needs **answers to the morning questions doc**, not a tasking memo. **`20261109_FOUNDY_Response_Ch3_Army_data_questions.md`** (comprehensive §1–8).
- **2026-11-09 13:50** — FOUNDY read the CODA answers to the eight questions (`20261109_FOUNDY_Response_Ch3_Army_data_questions.md`). Checked the one point that conflicted with this file in code: in the 20260320 export, `pool_minus_mean = own value - LOO mean of others` (`exclude_self=True`). **My 11-05 statement (and the variable table) was wrong and is corrected above.** Consequence: the HERO bars plot own relative standing in the pool, not peer quality alone; the pure peer measure is `pool_tb_ratio_mean_snr_fwd`, which the March bars do not use. Chapter wording and the figure caption ("peer environment") must follow. Open for Charles: which framing the chapter uses. Settled by CODA answers: raw sources (PDE, 502/512), filter order (502 then 520), event codes (1 = any promotion to major, 2 = exit without major, 0 = open), top box = 50, run of record, citable files, DUA wording. Still open: per-band open counts and the filter flow table (Vantage), attrition vs reserves vs ID break.
- **2026-11-09 13:55** — Charles: (1) peer axis / placeholders. (2) **Component:** recalls non-`R` filter; repo check = no global “ever non-R” drop on 502→520; `R` for YG/QC at CPT. **14:07 — Charles resolved:** mixed `compo` possible; **leaving Regular Army ≈ attrition** for this chapter; MAJ in other component out of scope; annotate in methods (see § Component above). Count mixed-component officers on Vantage — TK.
- **2026-11-09 14:15** — Charles: settled list for drafting (any promotion to major via `dor_maj`; attrition = left the extract before study end; open = not promoted, kept in the denominator; one optional below-zone footnote; March 20260320-1000 Run 1 placeholders, YG 2002-2011, noOER, N = 31,692, captions say Vantage TBD; YG and snapshot window in methods; PDE print rules; compo as above). Still TK: flow-table counts, per-band open cases, mixed-component count, exact snapshot end. **FOUNDY checks, two issues.** (1) **Axis:** at 13:55 Charles chose peer quality alone for the chapter; the 14:10 note says the placeholder bars plot own-minus-peer (`pool_minus_mean_snr_fwd`), "not pond LOO alone". Treated as: the PNG shows own-minus-peer; the chapter variable stays peer-alone after the rerun. **Asked Charles to confirm.** (2) **Component and event codes:** in 502 (March export, Cell 5), `dor_maj` is taken from any snapshot with `rank_pde == MAJ`, with no component test. In 520, event 1 = promoted, event 2 = last snapshot before the study end date (the max `snpsht_dt` in the data), otherwise 0. So "leaving the Regular Army pool = attrition" holds only if non-R rows are absent from the extract. If the extract keeps non-R snapshots, then (a) an officer who moves to a reserve component and is still listed at the end is event 0, not attrition, and (b) an officer who appears as a major in a non-R snapshot is event 1, which contradicts "other-component major out of scope." The mixed-component count decides this. Prose should not assert the annotation as fact until then.
- **2026-11-09 14:40** — Charles: draft the chapter executive summary in the format of the other chapters; the literature review summary is hard to read as a model because of its footnote lists, so also look at the model chapter. Read the opening of `Model_Chapter_Shared_Working_Draft.docx` (phenomenon, question, roadmap, plain prose, no citation lists, stops before results) and `11_executive_summary_PD54.md`. Facts for Romania, basketball and tenure taken from the repo: `education_analysis/outputs/romania_2001_all_scraped_counties_descriptive_pilot/.../report.md` (22 counties; top-one and top-two program tiers; masked ID, linked by name and score; peers are admission-round applicants), `MBB_empirical_roster_select_replay.md` (2009-2021, points per minute, leave-one-out teammates), `SPORTS_DATA_GAMEPLAN.md` (ESPN box scores linked to draft list; Sports-Reference added), `TENURE_hero_pipeline.md` (decision year about 5-6, department pond, pubs per career year, archived department pages). **Drafted** `20261109_Ch3_executive_summary_DRAFT.md`, about 1,100 words, no counts, no column names, no model, no results. Brackets: Army peer-quality wording versus the March figure, Romanian score components, basketball seasons, tenure missing outcomes, tenure fixed-places wording, Army component handling.
- **2026-11-09 14:55** — Charles: the lit-review executive summary is the closer model, per Alex. Read PD52, PD53, PD54. Alex's brief: stand-alone; "no one is going to read the chapter, what do you need to know"; one sentence per part on what it contributes and misses; say why the parts belong together; citations in bulk; stay out of the model. For this chapter (PD52): first half = systems and how the records were built; second half = results, "the same shape, the same effect" across systems, all empirics. **Rewrote** `20261109_Ch3_executive_summary_DRAFT.md` as v2 (about 1,040 words): opens from the last sentence of Chapter 2; criteria; one paragraph per system with a "what it cannot give us" sentence; the four common constructs; results paragraph with a bracketed pattern sentence to write last. Version 1 (built on the model chapter's opening) is replaced. Open items now eight, listed in the file.
- **2026-11-09 ~14:08** — Pre-FOUNDY send: **March hero axis = `pool_minus_mean_snr_fwd` (own − LOO peer mean)**, not pond LOO alone; align captions/prose. **`20261109_Charles_to_FOUNDY_Ch3_kickoff.md`** regenerated as cover letter + pointer to response doc.
