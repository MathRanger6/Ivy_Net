# Leave one out measures across the dissertation

NVector to Charles | Repository audit | 18 October 2026

## Executive conclusion

Keep leave-one-out (LOO) in the chapter, but give it a different job. It is scientifically useful for describing the peers surrounding a particular person and is embedded in several empirical plots. It is not required by the later, shared congestion mechanism. The verified record supports introducing the full-group mean first, briefly defining LOO as an empirical peer measure, and placing the derivation and alternative LOO congestion model in the appendix. This is option B, with an explicit main-text definition rather than an unexplained cross-reference. [B1, T1, M1–M4]

The most consequential audit finding concerns the Army. In both archived and current code, pool_minus_mean is the officer’s own rating minus the mean of other officers, not simply that peer mean. Some older explanatory memos say otherwise. The saved Army cumulative-incidence figure and its Cox-effect counterpart therefore concern relative standing built from an LOO mean. They cannot be described as direct evidence of an inverted U against peer quality without resolving that distinction. [A1–A6]

The recommendation for Chapter 4 is supported now. A final claim about the strongest current Army result requires CODA’s confirmation of the authoritative run and its exact inputs. A separate questions document accompanies this memo. No analyses were rerun and the manuscript was not edited.

### Three quantities that answer three different questions

| Quantity | Question answered | Role |
| --- | --- | --- |
| $T_{j}$ | How strong is this entire group on average? | Full-group mean of A, including the focal person. |
| $L_{Q,i}$ | How strong are the other people around this person? | LOO mean of A; useful empirical descriptor. |
| $C_{j}$ | How concentrated is competitive relevance in this group? | Full-group mean of transformed relevance v; shared congestion in SCORE. |

These are proposed mathematical labels for the revised exposition. Historical code uses different names. In particular, an LOO plotting axis need not be the congestion variable used to calculate a simulated score. The later simulation implementation deliberately retains both. [M1, M4]

## Major Army uses

| Use and evidence | Exact measure and exclusion | Sample and consequence of replacement |
| --- | --- | --- |
| Pool construction<br>Implemented [A1, A2] | pool_tb_ratio_mean_snr_fwd<br>Straight peer mean. Own record/person excluded when POOL_EXCLUDE_SELF=True. Rater and backward counterparts also exist. | Senior-rater or rater pools, with timing rules. Current settings use active_at_eval_thru and at least 3 eligible peers. Replacing LOO with a full mean changes the quantity and potentially the eligible sample. |
| Historical HERO<br>Saved figure [A2, A3] | z_pool_minus_mean_snr_fwd<br>Standardized own rating minus LOO peer mean. Self excluded from the peer component; own rating explicitly remains in the difference. | Saved eight-bin promotion/competing-event cumulative-incidence curves. Source label says EW and 2002–2022; exact analytic population must be confirmed. Replacing this with a full mean changes the construct, not just its scale. |
| Cox promotion work<br>Saved execution and figure [A3, A4] | z_tb_ratio_fwd_snr and z_pool_minus_mean_snr_fwd; squares and interaction. Division covariates also listed. | Time-varying officer records. Relative standing enters alongside own performance. Interpret the fitted specification jointly; its peer term is not an independently fitted sigmoid $C_{j}$. Full-mean substitution requires model verification/refitting. |
| Newer Army plot code<br>Defaults verified [A5, A6] | army_act2_probes uses z_pool_minus_mean_snr_fwd. army_hero_slide_plot defaults to the same variable. COL_TJ in basic plots is pool_tb_ratio_mean_snr_fwd. | Last-snapshot promotion indicators and own-performance subsets. These are not automatically the historical cumulative-incidence analysis. A later guide proposes straight LOO, but a completed authoritative replacement run was not verified. |

### Rater pools are not automatically military units

The code calculates separate rater and senior-rater means. Those rating relationships need not coincide with battalions, brigades or divisions. Verified division code constructs assignment labels, time-in-division measures and covariates; it does not establish that the cited HERO result uses a division-level LOO mean. The historical data-search brief treats further UIC linkage as future work. I did not verify a completed battalion-, brigade- or division-LOO result in the reviewed material. CODA should identify one if it exists. [A1, A7]

## Major basketball and tenure uses

| Use and evidence | Exact measure and exclusion | Sample and consequence of replacement |
| --- | --- | --- |
| Basketball panels 7 and 8<br>Saved plots and tests [B1, B2] | poolq_loo<br>Mean of other eligible team-season players’ performance, with performance standardized within season. Own performance excluded. | 2009–2021: panel 7 uses own z in [2,3], 534 rows; panel 8 uses the pooled top 7%, 1546 rows. At least 20 minutes and more than 10 recorded team games; colleges with a draftee in the window; ever-drafted outcomes. Full means can move rows between bins and change the curve. |
| Basketball panel 9 and first-test cohort<br>Saved [B3] | poolq_loo<br>Other teammates’ same-season performance, retained on the player’s final observed season. | 2009–2021 all eligible teams; one final row per player. First-test provenance records 22795 players, including 1596 in the top 7% own-performance band. This differs from panels 7 and 8. Replacing LOO changes the axis, not draft outcomes. |
| Tenure original pipeline<br>Implemented [T1] | poolq_loo_mean; poolq_loo_sd; poolq_loo_cum_mean<br>Self-excluded annual publication mean, dispersion, or cumulative-publication mean. | Assistant-professor pools and matched bibliometric data; final-assistant-row variants also exist. Missing peers and roster timing matter. A full mean can admit singletons that have no LOO mean unless eligibility is held fixed. |
| Tenure PD29 HERO and conditional plots<br>Saved [T1, T2] | decision_loo / dept_loo_metric / loo_mean<br>Mean career publication rate among other faculty in the whole department at the decision year. | 389 resolved cases with peer values; 191 tenured and 198 attrited. This roster includes all ranks, not only assistants. Fixed-own-performance and elite-subset diagnostics also exist. Full means would change each person’s measured environment. |

Other self-excluded basketball features include the share of teammates above a hard threshold, raw performance sums, minute-weighted performance sums and peer standard deviation. These are different statistics. The column congestion_quality is still a peer-performance mean. Their implementation alone does not establish a completed structural fit using individual-specific LOO congestion. [B1]

Names also require checking: tenure pool_rank_loo and pool_pctile_loo use the full matched pool for ranking. Army ranks likewise use their full grouped sample, while deviations can use a LOO mean. Not every field near a LOO calculation is itself self-excluded. [A1, T1]

## Simulation and other domains

| Use and evidence | Measure and exclusion | What the record establishes |
| --- | --- | --- |
| Earlier simulations<br>Historical outputs and notes [M1–M3] | poolq_loo; pool_c_loo; pool_c_smooth_loo<br>Other members’ mean ability, hard viability share or mean sigmoid relevance. | LOO congestion was used in characterization work. A historical axis table reports a mostly decreasing LOO-quality readout, cautioning against claiming a bin-for-bin empirical match. |
| Later SCORE and saved MLE<br>Implemented and fitted [M1, M4] | pool_c_smooth_team<br>Mean relevance across all group members, including the focal person. pool_mean and poolq_loo are retained separately. | Saved joint Bernoulli fit uses shared congestion on observed rosters. The script explicitly calls add_team_pool_columns. This is completed work supporting the three-object distinction. |
| Football<br>Saved manifests [O1] | Team LOO performance index; separate team_mean axis variant. LOO excludes self according to the manifest. | 29403 eligible final-season FBS players. Both LOO and full-mean plot bundles are recorded. Some labels remain stale; exact generating-field provenance needs checking before a publication claim. |
| Education<br>Code and documented inventory [O2] | Romania peer_mean_exam excludes own exam score; gym_mean_exam is shared. NELS/HSB peer_mean_loo and peer_mean_z_loo describe sampled school peers. | Romania includes both student-specific peer plots and shared gymnasium bins. Observed applicants or surveyed classmates are not necessarily complete school rosters. These are additional measurement uses, not evidence requiring LOO SCORE. |

### The historical simulation record needs dates and settings

The August 4 PD16 digest explicitly redirects the score mechanism from LOO congestion to shared team congestion while retaining earlier characterization work. Current helper code implements both. However, the old D10 axis table says LOO congestion whereas the saved knockout metadata specifies crowding_smooth_team. Those artifacts must be cited with their own settings; the folder cannot be treated as one immutable model. [M1–M3]

The saved August 28 MLE estimates are γ = 19.5723, λ = 1.3024 and t = 1.0699 under a season-softmax Bernoulli likelihood using shared congestion. The JSON labels the window 2009–2021 but records 11 fitted seasons and 46306 player-seasons. It does not support silently claiming 13 included seasons or an exact-K fit. These qualifications do not alter the verified fact that its congestion is full-group. [M4]

## How strong are the findings that use LOO

### Army evidence needs a precise description

The archived cumulative-incidence figure shows a visible peak and decline, and the saved Cox partial-effects image also uses relative standing. Neither image alone establishes robustness to pool definitions, binning, uncertainty or alternative samples. More fundamentally, the x-variable must first be named correctly. Older CODA memos describe pool_minus_mean as a peer average, but the corresponding archived implementation subtracts that average from own performance. [A2, A3, A6]

There is a second provenance warning: ARMY_combined_effect_pool_minus_mean_stdz.png actually displays a curve titled z_tb_ratio_fwd_snr plus its square. The separate ARMY_partial_effects_pool_minus_mean.png displays the relative-standing curve. Filenames are therefore insufficient evidence of which effect is shown. The later straight-LOO guide recognizes the conceptual distinction, but its proposed execution path is not proof that the corrected outputs were produced. [A3, A6]

### Basketball evidence varies across the saved tests

In the saved 2009–2021 run, panel 7 compares chosen peak bin 8 with bins 15–16; panel 8 compares peak bin 8 with bins 10–11. Their one-sided p-values are shown below. These are existing outputs, not new calculations. [B2]

| Allowance in saved test | Panel 7 | Panel 8 |
| --- | --- | --- |
| Neither dependence nor peak search | 0.0181 | 0.0219 |
| College and repeated-player dependence only | 0.0399 | 0.0339 |
| Peak-location search only | 0.1721 | 0.1005 |
| Both allowances | 0.2802 | 0.1479 |

The earlier 2011–2021 panel 8 result is 0.0081 with both allowances. The saved final-season first-test cohort instead has p = 0.5958 with both allowances. Thus some LOO results are encouraging, but they are not uniformly robust. Peak correction covers 14 locations for panel 7 and 9 for panel 8, not every historical specification. Existing full-mean versus LOO mosaics are descriptive checks, not tests establishing equal significance on the two axes. [B2–B4]

### Tenure does not supply an unqualified replication

The saved PD29 HERO has a higher middle-bin rate than its upper tail. However, its fixed-own-performance comparison reports equal rates of 0.5 in the designated middle and upper ranges, and its top-20-percent diagnostic records no visible downturn. Small cells and different peer populations matter. These results justify retaining LOO’s definition, not claiming that every domain has established the same robust phenomenon. [T2]

## Why self exclusion matters

### Documented reasons and limits

The clearest documented rationale is measurement: the basketball replication handoff identifies contamination by the focal person’s own performance and specifies LOO as the remedy. The plain-English problem statement defines teammate quality as everyone except that player. Simulation comments likewise say own ability should not inflate the surrounding pool’s quality or crowding. Later code retains LOO for compatibility with empirical readouts even after the SCORE mechanism becomes shared. [R1, M1]

I did not find a verified decision establishing LOO by itself as a causal identification strategy, or a specific cited paper whose estimator required all these implementations. Exclusion removes the direct inclusion of $A_{i}$ in its own peer average. It does not eliminate sorting, common shocks, measurement error, repeated outcomes or mutual influence among peers. That limitation is statistical reasoning, not a claim of a newly documented historical decision.

### Changing to a full mean is not guaranteed to be a small change

For a fixed roster of $n_{j}$ people with observed performance, $n_{j}$ > 1, the two means obey the following identity. This is algebra, not a new empirical analysis:

$$
L_{Q,i} = \frac{n_{j} T_{j} - A_{i}}{n_{j} - 1} = T_{j} + \frac{T_{j} - A_{i}}{n_{j} - 1}
$$

A star in a small group can have a substantially lower LOO mean than the group’s full mean. Replacing LOO can change individual ordering across groups, bin membership and curve shape. At fixed group size and exactly fixed own performance, the two axes are related monotonically. Real plots use performance bands and varying group sizes, so that special case does not make them interchangeable.

This identity does not prove that LOO creates a spurious downturn. It explains why the full-mean comparisons are scientifically useful. Those comparisons must hold eligibility, performance definition, clipping, outcome and bins under explicit control. Missing observations also matter: the basketball poolq_loo helper uses roster row counts, while some newer peer-statistic helpers count valid performance values. [B1, B4]

For the Army difference $D_{i}$ = $A_{i}$ − $L_{Q,i}$, a common fixed roster gives $D_{i}$ = $n_{j}$($A_{i}$ − $T_{j}$)/($n_{j}$ − 1). This is relative standing. With focal-date active rating pools, officers may not share one identical roster, so that common-roster simplification must not be imposed automatically. A model containing both own performance and this difference needs joint interpretation. [A1]

## Recommended treatment of Section 4 4

Choose option B, while keeping the short definition visible in the main body. LOO is an empirical convention with a substantive meaning: the performance of other people. Calling it a convention should not make it sound arbitrary or unimportant. The empirical chapters need that definition even though the canonical model does not require individual-specific congestion.

### Suggested sequence without rewriting the chapter yet

1. Introduce $T_{j}$ as the mean performance of the full group. Explain the population and averaging operation before discussing self-exclusion.

2. Define $L_{Q,i}$ briefly as the mean performance of the other members, for $n_{j}$ > 1. State that several empirical analyses use this quantity to describe the focal person’s peers. Send the derivation from $T_{j}$, the small-group implications and singleton handling to the appendix.

3. Explain why performance averages alone need not represent credible competition. Introduce competitive relevance $v_{h}$, then the shared mean $C_{j}$, and finally $S_{i}$ = $A_{i}$ − λ $C_{g(i)}$.

4. Identify shared congestion as a deliberate model choice. Retain individual-specific LOO congestion as a historical or alternative specification in the appendix, with its consequences stated explicitly.

5. In each empirical chapter, identify the actual axis, roster and outcome. The Army needs a separate relative-standing definition when $D_{i}$ is used; it must not be relabeled $L_{Q,i}$.

### What should move and what should remain

The current 4.4.1 presents LOO as the first congestion approximation, then full-group performance, and derives the relation at length. That is a permissible pedagogical sequence, but the completed later fit and shared SCORE implementation do not require that ladder. It currently gives LOO congestion more prominence than its role in the later canonical mechanism warrants. Move the long derivation and the alternative score specification; retain the peer-measure definition and the reason for it. [C1, M1–M4]

Removing LOO entirely would make important empirical axes harder to interpret, conceal the distinction between own performance and peer quality, and leave the Army terminology problem unresolved. Conversely, treating all empirical peer measures as $C_{j}$ would incorrectly imply that the plots directly measured the model’s mean sigmoid relevance. The proposed three-object distinction prevents that confusion. [A1–A6, B1, T1, M1]

A LOO relevance penalty also changes the model, not only the graph. With $C_{-i}$ = ($n_{j}$ $C_{j}$ − $v_{i}$)/($n_{j}$ − 1), the score difference between using LOO and shared congestion is λ($v_{i}$ − $C_{j}$)/($n_{j}$ − 1). Members of one team can then receive different penalties. Preserve this as an appendix comparison, not as an unacknowledged replacement for shared SCORE.

## Repository evidence

Paths below are relative to the Cursor Workspace PDE repository root. Each path is a clickable link to the inspected local file. Source IDs in the text distinguish code, saved outputs and dated descriptions; a description or run guide is not treated as proof of execution.

**[A1] Army pool definitions and current settings**

[talent/talent_pipeline/add_cum_oer_metrics_mod_working.py](../../../talent/talent_pipeline/add_cum_oer_metrics_mod_working.py)

[talent/talent_pipeline/pipeline_config.py](../../../talent/talent_pipeline/pipeline_config.py)

_add_pool_mean_size; _add_pool_mean_size_active_at_anchor; _add_pool_ranks; POOL_EXCLUDE_SELF and POOL_GROUPING_MODE.

**[A2] Archived Army implementation and figure provenance**

[talent/Army_AWS_download/TALENT_NET_export_20260320-1000/add_cum_oer_metrics_mod_working.py](../../../talent/Army_AWS_download/TALENT_NET_export_20260320-1000/add_cum_oer_metrics_mod_working.py)

[3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/EXTRACT_MANIFEST.txt](../../re_entry/HEROs_and_PASSes/army_sandbox/EXTRACT_MANIFEST.txt)

Archived _add_pool_mean_size, especially line 320. Manifest identifies the March 20 export notebook and extracted figures.

**[A3] Saved Army plots**

[3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/ARMY_G1_pool_minus_mean_fwd_cif_b8.png](../../re_entry/HEROs_and_PASSes/army_sandbox/ARMY_G1_pool_minus_mean_fwd_cif_b8.png)

[3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/ARMY_partial_effects_pool_minus_mean.png](../../re_entry/HEROs_and_PASSes/army_sandbox/ARMY_partial_effects_pool_minus_mean.png)

[3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/ARMY_combined_effect_pool_minus_mean_stdz.png](../../re_entry/HEROs_and_PASSes/army_sandbox/ARMY_combined_effect_pool_minus_mean_stdz.png)

Inspect actual axes and titles. The third file displays own rating despite its filename.

**[A4] Army Cox configuration and saved execution record**

[talent/talent_pipeline/pipeline_config_17_1.py](../../../talent/talent_pipeline/pipeline_config_17_1.py)

[talent/talent_pipeline/pipeline_config_div_name.py](../../../talent/talent_pipeline/pipeline_config_div_name.py)

[talent/talent_pipeline/520_pipeline_cox_working.ipynb](../../../talent/talent_pipeline/520_pipeline_cox_working.ipynb)

RUN1_PROFILE, RUN_CR_PLOT_DEFAULTS; saved March 25 outputs list standardized own rating and pool_minus_mean covariates, squares, interaction and division.

**[A5] Army plotting defaults**

[talent/re_entry/army_basic_plots.py](../../../talent/re_entry/army_basic_plots.py)

[talent/re_entry/army_act2_probes.py](../../../talent/re_entry/army_act2_probes.py)

[talent/re_entry/army_hero_slide_plot.py](../../../talent/re_entry/army_hero_slide_plot.py)

COL_TJ, COL_LOO, COL_LOO_Z; hero plot_var and outcome_mode. A file containing code is not evidence that its latest configuration was run.

**[A6] Conflicting Army descriptions and later correction**

[talent/documents/Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md](../../../talent/documents/Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md)

[talent/documents/Coda_Summary_For_Scout_and_Vector_Post_Replication.md](../../../talent/documents/Coda_Summary_For_Scout_and_Vector_Post_Replication.md)

[talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md](../../../talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md)

Older memos describe pool_minus_mean as a peer average. Later guide explicitly distinguishes relative standing from straight LOO and proposes switching plots.

**[A7] Army pool timing and unit hierarchy**

[3-Master_Plan/re_entry/ARMY_fwd_bwd_and_pool_fix_for_dummies.md](../../re_entry/ARMY_fwd_bwd_and_pool_fix_for_dummies.md)

[talent/talent_pipeline/py_503_hierarchies.py](../../../talent/talent_pipeline/py_503_hierarchies.py)

[talent/documents/External_Data_Search_Brief.md](../../../talent/documents/External_Data_Search_Brief.md)

Pool grouping repair and dated defaults; add_division_metrics; unit identifiers and proposed future linkage. Do not substitute unit membership for rater-pool membership.

**[B1] Basketball empirical measurement**

[sports_pipeline/panel_build.py](../../../sports_pipeline/panel_build.py)

[sports_pipeline/tier1_mechanism_vars.py](../../../sports_pipeline/tier1_mechanism_vars.py)

recompute_teammate_loo_pool_quality; congestion_quality, congestion_crowding, congestion_crowding_sum, congestion_crowding_weighted and peer_perf_sd_loo.

**[B2] Basketball common window saved tests**

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/provenance.json](manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/provenance.json)

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/interpretation.md](manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/interpretation.md)

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/panel7_four_versions.csv](manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/panel7_four_versions.csv)

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/panel8_four_versions.csv](manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/panel8_four_versions.csv)

2009–2021 runs; one-sided comparisons. Panel 7 retains chosen bin 8 despite a tied maximum at bin 2.

**[B3] Basketball earlier window and final season population**

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/runs/panel8_20261015_103422/panel8_four_versions.csv](manuscript_figures/section_4_5/pd46_statistics/runs/panel8_20261015_103422/panel8_four_versions.csv)

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/first_test_curve_provenance.json](manuscript_figures/section_4_5/pd46_statistics/first_test_curve_provenance.json)

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/runs/20261014_190006_722614/peak_tail_four_versions.csv](manuscript_figures/section_4_5/pd46_statistics/runs/20261014_190006_722614/peak_tail_four_versions.csv)

2011–2021 panel 8; first-test final-season top-seven-percent cohort; saved peak versus tail results for that cohort.

**[B4] Existing full mean versus LOO comparisons**

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/printable_mosaics/READ_ME_methods_and_next_steps.md](manuscript_figures/section_4_5/pd46_statistics/printable_mosaics/READ_ME_methods_and_next_steps.md)

[3-Master_Plan/VECTOR_work/new_VECTOR_work/manuscript_figures/section_4_5/pd46_statistics/printable_mosaics/methods_and_provenance.json](manuscript_figures/section_4_5/pd46_statistics/printable_mosaics/methods_and_provenance.json)

Readout definitions, unclipped axes, rank-first quantiles, roster construction before own-performance filters; no significance tests added for these comparisons.

**[T1] Tenure pool construction**

[tenure/tenure_pipeline/pool_metrics.py](../../../tenure/tenure_pipeline/pool_metrics.py)

[tenure/tenure_pipeline/hero_panel_prep.py](../../../tenure/tenure_pipeline/hero_panel_prep.py)

[tenure/tenure_pipeline/decision_hero_prep.py](../../../tenure/tenure_pipeline/decision_hero_prep.py)

Stage 8 assistant pools; attach_loo_cumulative; PD29 decision-year whole-department peer roster and focal faculty ID exclusion.

**[T2] Tenure saved decision-year results**

[3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM_provenance.json](../../re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM_provenance.json)

[3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/act2/CCT_tenure_rate_ai_band_dept_loo_pd29_z1_2_q8.json](../../re_entry/HEROs_and_PASSes/tenure_sandbox/act2/CCT_tenure_rate_ai_band_dept_loo_pd29_z1_2_q8.json)

[3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/act2/ELITE_pond_loo_pw3p5_pd29_top20.json](../../re_entry/HEROs_and_PASSes/tenure_sandbox/act2/ELITE_pond_loo_pw3p5_pd29_top20.json)

September 2–3 saved results. N=389 resolved cases for HERO; fixed-band N=33 and top-20-percent N=56 diagnostics.

**[M1] Simulation definitions and explicit rationale**

[sports/tier1_pool_assignment.py](../../../sports/tier1_pool_assignment.py)

add_loo_pool_columns, add_team_pool_columns and add_pool_columns_for_l_mode. Comments explain own-performance exclusion and the PD16 shift to team congestion.

**[M2] Documented change in canonical congestion**

[3-Master_Plan/re_entry/08_PD16_Alex_meeting_takeaways.md](../../re_entry/08_PD16_Alex_meeting_takeaways.md)

[3-Master_Plan/re_entry/06_Lambda_threshold_and_KN_memo.md](../../re_entry/06_Lambda_threshold_and_KN_memo.md)

August 4 meeting, digest last synced August 7; compare the older L_C_LOO definition and characterization experiments.

**[M3] Saved simulation readouts and historical inconsistency**

[3-Master_Plan/re_entry/HEROs_and_PASSes/pass_b/PASS_B_D10_axis_table.md](../../re_entry/HEROs_and_PASSes/pass_b/PASS_B_D10_axis_table.md)

[3-Master_Plan/re_entry/HEROs_and_PASSes/pass_b/PASS_B_D10_congestion_poolq_loo_readout.png](../../re_entry/HEROs_and_PASSes/pass_b/PASS_B_D10_congestion_poolq_loo_readout.png)

[3-Master_Plan/re_entry/HEROs_and_PASSes/pass_b/PASS_B_generative_knockout_meta.json](../../re_entry/HEROs_and_PASSes/pass_b/PASS_B_generative_knockout_meta.json)

D10 table describes LOO congestion and warns the LOO-axis curve is mostly decreasing. Saved knockout metadata instead specifies crowding_smooth_team and a pool_mean axis.

**[M4] Completed basketball fitting uses shared congestion**

[sports/scripts/pd21_draft_bernoulli_mle.py](../../../sports/scripts/pd21_draft_bernoulli_mle.py)

[3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json](../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json)

LC_COL=pool_c_smooth_team; attach_player_level_lc calls add_team_pool_columns. Saved joint fit, generated August 28.

**[R1] Documented empirical motivation**

[talent/documents/Army_to_College_Basketball_Replication_Handoff.md](../../../talent/documents/Army_to_College_Basketball_Replication_Handoff.md)

[3-Master_Plan/re_entry/01_The_Problem_in_Plain_English.md](../../re_entry/01_The_Problem_in_Plain_English.md)

[sports/documents/Pertinent_Thoughts_Scout.md](../../../sports/documents/Pertinent_Thoughts_Scout.md)

Handoff own-performance contamination risk and LOO mitigation; teammate interpretation; distinction between draft rates and Army cumulative incidence.

**[O1] Football saved LOO and full mean manifests**

[3-Master_Plan/re_entry/HEROs_and_PASSes/football_sandbox/data_story/football_3x3_manifest.json](../../re_entry/HEROs_and_PASSes/football_sandbox/data_story/football_3x3_manifest.json)

[3-Master_Plan/re_entry/HEROs_and_PASSes/football_sandbox/peer_tj/data_story/football_3x3_tj_manifest.json](../../re_entry/HEROs_and_PASSes/football_sandbox/peer_tj/data_story/football_3x3_tj_manifest.json)

Final-season eligible FBS sample, N=29403, team peer axis. The second manifest has stale LOO wording despite peer_axis=team_mean; inspect generating code before publication.

**[O2] Education uses and scope**

[3-Master_Plan/VECTOR_work/new_VECTOR_work/education_analysis/code/EDUCATION_20261009_romania_ct_ph_tm_cj_descriptive_pilot.py](education_analysis/code/EDUCATION_20261009_romania_ct_ph_tm_cj_descriptive_pilot.py)

[3-Master_Plan/re_entry/education_dataset_primer.md](../../re_entry/education_dataset_primer.md)

Romania peer_mean_exam formula near line 166 and _pooled_gymnasium_mean_bins near line 300; NELS/HSB primer describes sampled-school peers, not entire schools.

**[C1] Current chapter under review**

[3-Master_Plan/VECTOR_work/new_VECTOR_work/Model_Chapter_Shared_Working_Draft.docx](Model_Chapter_Shared_Working_Draft.docx)

Saved October 18 copy, Sections 4.4.1–4.4.4. Read only; no chapter changes made.
