# DISPOSABLE — Chapter 3, data and empirics (started 2026-11-05)

**Purpose:** Working record for the data-and-empirics chapter. Source of the chapter order: PD52, 11-04, Alex. Transcript: `3-Master_Plan/VECTOR_work/new_VECTOR_work/Introduction_Agent_Handoff_20261027/transcripts/20261104_Paper_Directions_52_otter_ai_transcript.docx`.
**Say `anchor`** in chat to paste **YOU ARE HERE**.

The literature-review thread stays in `_DISPOSABLE_FOUNDY_Introduction_thread.md`. This file does not reopen it.

---

## YOU ARE HERE

| Step | Task | Status |
|------|------|--------|
| **0** | Executive summary of this chapter, readable without column names | **Next.** About **2 pages.** Alex, 11-05: same pattern as the literature review. Draft the argument and the four systems first. Revise after the detailed sections exist. The 10–20 page remark is set aside. |
| **1** | State the criteria for a system in which the question can be measured cleanly | **Stated below**, from Alex on 11-04. Belongs in the executive summary in prose. |
| **2** | Army detail, from raw columns up | **The draft below starts too late.** `tb_ratio_fwd_snr` is a late column. The chain to read is `talent/talent_pipeline/`: 501, 502, 503, 504/509, 512, `build_df_masters.py`, then 520. |
| **2a** | Army outcome (Charles + Alex, 11-05) | **Decided.** The Army result in this chapter is the two final-probability histograms: promotion and attrition, by band. Survival analysis, Cox models, and the 3D plots are out of scope for the deadline; alluded to in the data section and synthesis; a later paper or chapter if time allows. **Open:** is the promotion bar early promotion or any promotion to major? |
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
| Quality of the group | Mean of the others' top-box shares, leaving the officer out. Charles's name for this is "pool minus mean": the mean of the pool without oneself. It is not the officer's own share minus that mean. | `pool_minus_mean_snr_fwd` |
| The outcome | Promotion from captain to major. Leaving the Army is the other way a career ends, so it is kept as a competing event rather than dropped. | Survival panel in notebook 520 |

The group-quality column uses the forward top-box share as the number being averaged, and the backward senior-rater identity as the person who defines the group.

### The cleaning problem that changes the group

The pool is currently everyone on the same snapshot date who has the same senior-rater identity. A senior rater's real rating pool is the officers in one rating chain for one evaluation window. The snapshot-day rule pulls in officers from different windows, so computed pools run larger than the pool size written on the evaluation itself.

Checked 2026-09-20: the computed pool size at the last snapshot has median 23, and 19 percent of those pools exceed 50. The official count of how many in that grade the senior rater rates has median 12. Until the pool is redefined as one senior rater and one evaluation window, the group in the file is wider than the group the Army rated.

### Not in this section yet

Results. Also not re-counted here: the September deck's figures for the captain-to-major panel (on the order of 258,000 person-intervals, and a Cox subsample of about 15,000). Branch and year-group restrictions used in particular figures stay with those figures.

## Thread log

- **2026-11-05 14:24** — Charles: literature review is in good shape; start data and empirics. Opened this file. Next piece is the Army as a match to the criteria, then its provenance and variable mapping. Results wait.
- **2026-11-05 14:40** — Charles: go. Army data section drafted from the 520 overview and the 2026-09-20 pool note. "Pool minus mean" is the leave-one-out mean of the others, following Charles's naming note, not own performance minus that mean. Pool membership is still the known problem: snapshot day plus senior rater, which inflates the pool. Results not started.
- **2026-11-05 14:49** — Charles, after talking to Alex. (1) The Army draft starts too far downstream; raw columns are synthesized in `talent/` long before `tb_ratio_fwd_snr`. (2) This chapter gets an executive summary first, then the detailed sections, then a revision of the summary. (3) The summaries are what the committee actually reads.
- **2026-11-05 14:51** — Charles corrects (3): the 10–20 pages is the sum of every executive summary in the dissertation, not the length of this chapter's summary.
- **2026-11-05 14:52** — Charles: set the 10–20 pages aside. This chapter's executive summary should be about 2 pages.
- **2026-11-05 15:06** — Charles, after Alex. Survival analysis had no place in the PD52 chapter plan. History to tell: early promotion was the first candidate measure of success, because promotion is one of the few ways the Army can treat a high performer differently (no pay incentive; per the proposal). The competing-risks curves were cumulative curves for bands of performance. Their endpoints became two histograms, final promotion and final attrition. Those histograms are where HERO first appeared, and they led to the other domains. Decision: the chapter uses the final promotion and attrition histograms. Survival analysis and the 3D plots were a large body of work and could be their own paper or chapter; they are mentioned, not developed, unless time allows.
- **2026-11-05 15:09** — What the bar is, checked in `talent/talent_pipeline/cox_plot_helpers.py` (`plot_competing_risks_cif_bars`) and `talent/documents/CR_Red_Line_Flow_Explanation.md`. Promotion bar = officers in the band with a promotion event ÷ officers in the band; attrition bar the same for exits. Officers still open at the last snapshot stay in the denominator and count as not promoted. The band is assigned from each officer's last row. The curves are a running share out of a fixed group, not a censoring-adjusted incidence estimate. Chapter needs: the number still open per band, or a year-group restriction.
- **2026-11-05 15:12** — Charles recalls choosing year groups and the window so the last year group had time to be promoted. Configs: base `pipeline_config.py` and `pipeline_config_19_1.py` restrict to YG 2002–2011; `pipeline_config_17_1.py` sets `filter_ygs['enabled'] = False` (list present, not applied). The date filter is off everywhere; 2000-01-01 to 2022-06-30 is written but not applied, so the window is the extract's coverage. The 2026-09-20 note says Run 1 = base + 17_1, which would mean no YG restriction in Run 1. The September deck said "~2002–2013" for CS+CSS. **To settle on AWS:** (a) which config produced the HERO histograms; (b) count per band of officers with no promotion and no exit (event 0) at the last snapshot; (c) snapshot date range of the extract.
- **2026-11-05 15:15** — Charles: the Army system has moved from AWS to **Palantir Army Vantage** over the last six weeks; confirmation waits on that. Settled from the repo first. `3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/EXTRACT_MANIFEST.txt`: the HERO bars (`ARMY_G1_pool_minus_mean_fwd_cif_b8.png`) came from `talent/Army_AWS_download/TALENT_NET_export_20260320-1000/520_pipeline_cox_working.ipynb`, original name `cr_z_pool_minus_mean_fw_none_b8_ew_noOER_2002-2022_cif_bars.png`. In that export, the base config restricts YG 2002–2011 and `17_1` does not override it; the `enabled: False` exists only in the later local `17_1`. Filename code: `b8_ew` = 8 equal-width bins, `noOER` = officers with no OER excluded, `2002-2022` = first and last snapshot year in the plotted data. Promotion + attrition per band ≈ 0.95–1.00, so at most about 5% unresolved in any band. Band sizes, from the curve legend: 49, 1,423, 7,644, 8,131, 7,906, 4,130, 2,153, 256 (total 31,692); the top-band drop rests on 256 officers. **Vantage to confirm:** run of record; exact open count per band; snapshot dates.
