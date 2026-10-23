# NVector to SVector: LOO, Army survival models, and what the HERO plots measure

**Prepared:** 18 October 2026  
**Audience:** SVector and Charles  
**Purpose:** Conclude the LOO review, reconcile CODA's response, and explain the distinctions needed before comparing the Army, basketball, and tenure HERO plots. This document is self-contained; repository links supply supporting evidence.  
**Status:** Repository and saved-output review only. No analyses were rerun; no manuscript or analysis code was changed. Charles expects full access to the Army code and data in about a week.

**Update, 18 October 2026:** Charles supplied the paired promotion/attrition time curves and endpoint bar charts and explained how he used that transformation to construct the Army HERO display. Section 3.1.1 records the process. **The Fine–Gray estimator question remains open for verification when Army access returns next week**, as specified in Sections 3.2 and 7.

## 1. What Charles and NVector have agreed

Retain a concise definition of leave-one-out (LOO) performance in Chapter 4 because readers need it to understand the empirical analyses. Do not make individual-specific LOO congestion a necessary stage in the development of the later shared congestion model.

Introduce full-group mean performance, explain the LOO peer mean briefly, and then develop competitive relevance and shared roster pressure. Put the longer LOO derivation and alternative LOO congestion specification in the appendix. This is option B from the original audit, with a visible main-text definition.

Keep these objects separate:

- **Full-group mean performance, $T_j$:** average performance of everyone in group $j$.
- **LOO peer performance, $L_{Q,i}$:** average performance of the other members surrounding individual $i$.
- **Relative standing:** own performance minus the LOO peer mean.
- **Shared congestion, $C_j$:** the full-group average of transformed competitive relevance in the refined model.

The first three describe performance or relative position. The fourth is a particular model specification. An empirical graph against a peer average does not directly measure $C_j$, and its outcome rate is not the SCORE equation or the SELECT rule. [R1]

This recommendation is ready for manuscript planning. The outstanding Army questions affect the empirical claims and methods description.

## 2. What CODA resolved

### 2.1 The Army naming discrepancy

CODA confirms that archived and current Army code distinguish two columns:

- `pool_tb_ratio_mean_snr_fwd`: the average rating of eligible peers, excluding the focal officer when self-exclusion is enabled.
- `pool_minus_mean_snr_fwd`: the officer's own rating minus that peer average.

TB means the top-block rating category; SNR identifies the senior-rater context. The own measure is `tb_ratio_fwd_snr`. The archived subtraction is explicit:

~~~python
df[f'pool_tb_ratio_mean_{prefix}_{suffix}'] = mean
df[f'pool_minus_mean_{prefix}_{suffix}'] = df[value_col] - mean
~~~

The `z_` prefix indicates standardization of the named quantity. Standardization does not turn a difference into a peer average. Older memos that called `pool_minus_mean` the peer mean contained a wording error, not evidence of a different archived formula. [R2, R3]

An officer rated 0.80 among peers averaging 0.60 has peer quality 0.60 and relative standing 0.20. Those numbers answer different questions.

### 2.2 Newer direct-peer-average plots

CODA reports that Charles executed newer descriptive runs using the peer mean directly and testing different peer-pool definitions. My earlier audit verified the guides but could not verify those completed runs from saved local outputs.

The appropriate status is: **reported completed by CODA from his work with Charles; the specific outputs, input files, and settings still need independent verification.** Do not describe those runs as merely proposed, but do not assign an unidentified plot the status of a verified replacement. [R2, R4]

Changing the plotting axis and refitting a statistical model are separate operations. CODA does not establish that a direct-peer-mean Cox refit was completed.

## 3. What the exported Army notebooks establish

Charles clarified that the relevant plots were exported inside the talent notebooks from the locked-down AWS server. I inspected embedded PNG outputs as well as generating source.

- **March 20 export of notebook 520:** 29 embedded PNG outputs. The cell headed “CELL 11: COX ANALYSIS & PLOTTING,” at zero-based cell index 51, contains observed outcome curves and bars. Relative-standing curves and bars are at output indices 7 and 9; output index 11 contains their metadata. Cell index 68 contains promotion-versus-attrition coefficient comparisons. Cell index 73 contains combined-effect plots.
- **Notebook 513 in the current talent pipeline:** 14 embedded PNG outputs. Cell index 37, headed “CELL 10: COMPETING RISKS ANALYSIS (CIF),” contains three cumulative-outcome figures. Its generating function calculates running event counts divided by a fixed group population.
- **April 21 export of notebook 520 and current notebook 520:** no embedded PNG outputs in the copies inspected. Source remains available. We should not call March the latest code merely because it retains useful figures. [R5, R6]

These observations do not establish that Charles never ran another version.

### 3.1 The historical Army HERO bars are observed proportions

For each bin, the archived bar-chart helper computes

$$
\widehat p_b
=
\frac{\text{included officers in bin }b\text{ with recorded promotion}}
{\text{all included officers in bin }b}.
$$

The numerator counts `event == 1`; the denominator counts retained rows after plot preparation and valid-time filtering. Cell 11 first collapses the data toward one final observation per officer. The bars do not use fitted Cox coefficients. [R5, R7]

The corresponding time curves accumulate recorded events by time and divide by the same fixed population. In the inspected code, they are not generated by a Fine–Gray fit or an Aalen–Johansen risk-set calculation.

This corrects CODA's October description of the bars as model-based cumulative incidence and sharpens my original audit's terminology. CODA's June documentation already explained the methods distinction correctly: descriptive running proportions in Cell 11, separate Cox fits in Cell 12. Its peer-variable labels were wrong, but that methods distinction remains useful. [R8]

Two details matter:

- Censored observations retained in a bin contribute to its denominator. The plotting calculation itself does not adjust for unequal follow-up.
- Limiting the displayed time axis to 4,500 days crops the graph. It does not make the endpoint bars promotion probabilities by day 4,500; the bars count all included recorded events.

The safe description is **observed promotion proportions by relative-standing bin, using the final observations selected for that plot**. A fixed-horizon or censoring-adjusted estimate requires an explicit additional calculation.

### 3.1.1 How Charles turned the time curves into HERO bars

**Each HERO bar summarizes the final height of one group's time curve.** Charles's examples show the same eight groups first as trajectories through time and then as endpoint comparisons. The transformation makes the rise and downturn across groups easier to see. [R5, R7]

The process is:

1. **Assign officers to eight bins using the chosen performance-related measure.** In this example, that measure is standardized own rating minus the senior-rater peer average. Each officer's group is fixed for this display using the record selected during plot preparation.
2. **Draw one promotion curve for each bin.** The horizontal axis is days since promotion to Captain. As recorded promotions occur, the curve rises. In the inspected implementation, its height is the cumulative number of recorded promotions divided by the number of included officers in that bin.
3. **Summarize each curve by its endpoint.** Using the same included officers and filters, the endpoint is the final recorded promotion fraction for that bin. The bar-chart helper calculates that fraction directly from the event counts; it does not extract a value from the rendered image.
4. **Place the eight endpoint values side by side in bin order.** Time is no longer the horizontal axis. The horizontal positions now identify the eight groups, and each bar's height records its group's final promotion fraction.
5. **Repeat the operation for attrition.** The orange curves become orange bars using the recorded attrition events within the corresponding groups.

In Charles's example, promotion bin 6 ends near **70%**, bin 7 near **62%**, and bin 8 near **42%**. Those approximate heights reappear in the blue bars, making the upper-bin downturn immediately visible. These percentages are read from the supplied figures, not newly estimated results.

**The transformation preserves the endpoint while leaving out the timing.** Two groups could have equal final promotion fractions even if one group's promotions occurred much earlier. The bars also do not carry over information about the length of follow-up. Here, “final” means the endpoint available for that group's included observations, not automatically a common career horizon or the end of the promotion board's primary zone.

The endpoint comparison is the useful connection to the basketball and tenure HERO displays: it compares advancement outcomes across groups defined by a performance-related measure. The specific axis, population, outcome, and observation period must still be stated for each domain. For this Army example, the horizontal measure is relative standing, not the peer average by itself.

**Turning curves into bars does not establish which statistical estimator produced the curves.** That method must be identified from the generating code. The reviewed local implementation computes observed event fractions; whether a separate Fine–Gray fit was part of Charles's broader Army analysis remains the historical question below.

### 3.2 The inspected regressions are Cox fits; Fine–Gray remains unverified

March 520 Cell 12.5 constructs separate promotion and attrition indicators and fits `CoxPHSurvivalAnalysis` for each. The specification is intended as cause-specific Cox analysis. The available source and older CODA documentation do not identify a Fine–Gray subdistribution-hazard fit. [R5, R8]

Charles remembers Fine–Gray models and identifies the exported talent notebooks as their surviving source. **That is an open historical question.** The notebooks inspected so far do not substantiate that estimator identity. We should locate the exact cell, model call, and output when access returns rather than conclude that Charles never used it.

**For verification next week:** locate the Fine–Gray model Charles remembers and establish its relationship to these particular figures. Did it generate predicted cumulative-incidence curves that were summarized as bars in another version, or was it a separate analysis alongside the observed-proportion displays? Record the exact notebook version, input preparation, fitting call, saved model output, and plotting cell. Until that connection is verified, SVector should describe this pair as the observed-proportion curves and endpoint HERO bars documented above and label the Fine–Gray attribution as unresolved.

A Cox fitting function does not always rule out Fine–Gray: R's survival package can fit Fine–Gray using specially expanded and weighted data followed by Cox fitting. The reviewed Army path does not show that construction. Input preparation matters as well as the function name. [M3]

### 3.3 An additional implementation issue needs review

Archived Cell 12.3 uses all officer intervals, constructs `full_time = stop_time - start_time`, and passes the event flag and duration to `Surv.from_arrays` and `CoxPHSurvivalAnalysis.fit`. Officer identifiers and start times are excluded from the fitting inputs. Saved output reports multiple intervals per officer.

This is not the standard start-stop construction of time-dependent Cox risk sets. An interval length alone does not identify where that interval falls on a career timeline. The documented fitting interface takes an event indicator and one event/censoring time per row. [R5, M4]

The later `cox_lifelines_significance.py` helper also calls ordinary `CoxPHFitter` with durations and event flags. That helper alone does not establish a repair of the longitudinal risk-set issue. [R9]

**Consequence:** a historical fitted output is not automatically a validated longitudinal analysis. Do not yet endorse the old coefficients or significance claims as the strongest established inferential result. Check the authoritative version Charles actually ran. This issue does not change the separate descriptive bars' arithmetic.

## 4. What Fine–Gray would mean

This section defines methods. It does not claim that every method was used in the saved Army work.

### 4.1 First define the event and the clock

Suppose the Army clock begins at promotion to Captain. The event of interest is promotion to Major. Departure before promotion is a competing event if it ends eligibility for that transition. An officer still eligible when observation ends is censored: the later outcome is unknown, rather than known to be failure.

This is a first-event framework. Promotion does not make later Army departure impossible; it means the transition being studied has occurred. Operational event coding must match this interpretation.

Let $U$ denote time to the first event, $J$ its type, $\mathbf x$ the covariates, and $\tau$ a chosen follow-up horizon. The promotion cumulative incidence function (CIF) is

$$
F_{\mathrm{prom}}(\tau\mid\mathbf x)
=
\Pr(U\leq\tau,\ J=\mathrm{promotion}\mid\mathbf x).
$$

It asks: **By this point in the career, what proportion would have been promoted before a competing departure?**

With complete observation through a common horizon, direct counts can estimate that probability. With earlier right censoring, a raw proportion generally needs a censoring-aware alternative; Aalen–Johansen is a standard nonparametric estimator. [M1]

### 4.2 Cause-specific Cox concerns those still eligible

The promotion cause-specific hazard asks how quickly promotion occurs among people who have experienced neither promotion nor competing departure. It is a rate, not a cumulative percentage.

Promotion cumulative incidence depends on both promotion and departure hazards. Let $G(u\mid\mathbf x)$ be the probability of remaining free of either event and $h_{\mathrm{prom}}$ the promotion hazard. Then

$$
F_{\mathrm{prom}}(\tau\mid\mathbf x)
=
\int_0^\tau
G(u-\mid\mathbf x)\,
h_{\mathrm{prom}}(u\mid\mathbf x)\,du.
$$

Consequently, a higher promotion hazard need not imply a higher eventual promotion probability if competing departure also changes. [M1]

### 4.3 Fine–Gray links covariates to cumulative incidence through a different hazard

For continuous event times, the promotion subdistribution hazard is

$$
\widetilde h_{\mathrm{prom}}(u\mid\mathbf x)
=
\frac{\partial F_{\mathrm{prom}}(u\mid\mathbf x)/\partial u}
{1-F_{\mathrm{prom}}(u\mid\mathbf x)}.
$$

Its denominator differs from the event-free population. People who experienced a competing event still contribute to the subdistribution construction. They are not literally still eligible for promotion; this is a statistical risk-set and weighting device. [M2, M3]

For proportional subdistribution hazards with fixed covariates,

$$
\widetilde h_{\mathrm{prom}}(u\mid\mathbf x)
=
\widetilde h_0(u)\,e^{\mathbf x^\top\boldsymbol\beta}.
$$

Here $\boldsymbol\beta$ contains fitted coefficients and $\widetilde h_0$ is the baseline subdistribution hazard. A subdistribution hazard ratio is not a probability ratio or a percentage-point change. [M2]

Let $\widetilde H_0(\tau)$ be the baseline cumulative subdistribution hazard. The predicted probability is

$$
F_{\mathrm{prom}}(\tau\mid\mathbf x)
=
1-e^{-\widetilde H_0(\tau)e^{\mathbf x^\top\boldsymbol\beta}}.
$$

A verified Fine–Gray fit could generate a HERO-style plot on this probability scale. State the horizon, vary the peer measure, and specify whether other covariates are held fixed or predictions are averaged over a reference population. Such a plot differs from observed fractions and hazard ratios. [M5]

Changing officer ratings over time needs additional specification. Substituting a time-varying column into the fixed-covariate formula is insufficient; handling covariates after a competing event also matters. [M3]

## 5. How the three domains' HERO plots relate

HERO here means the project's empirical outcome-versus-peer-context plot. It is a presentation role, not one estimator shared across all domains.

### Army

The inspected historical bars show observed promotion fractions against standardized own-minus-peer standing. Newer direct-peer-average plots reported by CODA use a different horizontal quantity. Cox effect figures are separate outputs; a Fine–Gray fit has not yet been identified.

For every selected Army figure, establish its horizontal variable, peer-pool timing, outcome, observation period, denominator, and any model adjustment. A senior-rater pool is not automatically a battalion, brigade, or division. [R2–R8]

### Basketball

The saved 2009–2021 panel 7 and 8 comparisons retain eligible player-team-season observations within their performance subsets. Panel 7 has 534 rows from 441 players; panel 8 has 1,546 rows from 1,127 players. The outcome is whether a player is ever recorded as drafted, not drafting in that specific season. Repeated seasons can carry the same eventual outcome. These are descriptive row-based fractions with separate uncertainty calculations. [R10]

The final-season HERO and associated first-test cohort instead use one final observed season per player. Its provenance records 22,795 eligible players and 1,596 in the top-seven-percent performance subset. It also uses an ever-drafted label. These populations are not interchangeable. The reviewed plots do not use Fine–Gray or a common time-to-draft horizon. [R11]

### Tenure

The saved decision-year HERO contains 389 people with peer measurements: 191 tenured and 198 classified as attrited. The cohort excludes censored and transferred cases. Its axis is the LOO mean career publication rate among other faculty in the whole department at the decision year. [R12]

The vertical quantity is the tenure share among included resolved cases. It is not automatically tenure probability by a fixed year among everyone who entered an assistant-professor cohort. Excluding unresolved cases changes the denominator.

### What the comparison can establish

The plots motivate a common substantive question: how does advancement vary with the competitive environment surrounding a person? Similarity of shape alone does not establish the same population, probability, estimator, or mechanism.

Three distinctions are essential:

1. **Horizontal meaning:** peer quality, own-minus-peer standing, and shared model congestion.
2. **Vertical meaning:** observed outcome shares, cumulative incidence at a stated horizon, and hazard ratios.
3. **Who is represented and when:** final-observation officers, repeated player-seasons, final-season players, and resolved tenure cases.

LOO removes the focal person's direct contribution to a peer average. It does not itself standardize follow-up, handle censoring, remove sample selection, or identify a causal peer effect.

## 6. Implications for the manuscript

**Chapter 4 should explain the model without becoming a software-history audit.** Keep the short LOO definition and its empirical role. Explain shared congestion as a deliberate choice. Put detailed alternative LOO algebra in the appendix.

**Empirical methods should identify what each HERO figure measures.** Define its population, peer variable, outcome, timing, and estimator before comparing domains. Captions should distinguish observed proportions, estimated cumulative incidence at a stated horizon, and fitted hazard ratios.

**Fine–Gray belongs in the completed-methods account if the fit is identified, or in a clearly labeled proposed analysis if it is not.** We can explain the method now without retrospectively attributing existing bars to it.

Suggested framing:

> The empirical analyses examine how advancement varies with an individual's surrounding peer environment. The outcome measures differ across settings. The reviewed Army displays summarize recorded promotion outcomes, while separate regressions examine promotion and departure rates. Basketball plots summarize recorded draft outcomes, and the reviewed tenure plots summarize tenure among cases with resolved outcomes. We therefore identify the population, peer measure, observation period, and statistical method for each figure before comparing their patterns. Similar curves motivate a common theoretical question, but do not by themselves establish equivalent probabilities or a shared causal mechanism.

Update this paragraph if the selected Army figure uses verified censoring-adjusted or Fine–Gray predictions.

## 7. Checks when Army access returns

Charles expects access in about a week. First identify and verify the historical work; do not automatically rerun everything.

1. **Priority for next week: resolve the Fine–Gray attribution and the curve-to-bar connection.** Locate the remembered fit in the accessible Army notebooks or saved run artifacts. Record notebook version, cell heading, execution date, fitting call, input preparation, coefficients, and output. Trace whether that fit generated the displayed curves, a different version of those curves, or separate results. Verify the endpoint operation with matching officers, bins, filters, and follow-up. Distinguish subdistribution regression, empirical cumulative displays, and cause-specific Cox; do not infer the estimator from the words “CIF” or “competing risks” in a figure title.
2. **Check longitudinal Cox inputs.** Confirm whether the authoritative fit preserves start and stop times on a common career clock and handles repeated officer records appropriately. Determine whether the exported interval-duration implementation was replaced.
3. **Identify the current direct-peer-average HERO.** Preserve exact input reference, pool definition, filtering, denominator, bins, and output metadata. Confirm separately whether a matching regression was refitted.
4. **Reconstruct follow-up and endpoints.** Count promotion, departure, and censored cases. Verify event coding, time origin, delayed entry where relevant, and a meaningful common horizon. Determine whether existing bars combine unequal observation lengths.
5. **Match figures to generating cells.** The sandbox file ARMY_combined_effect_pool_minus_mean_stdz.png visibly shows own TB rating. It matches the own-rating plot family in archived Cell 12.6A. The relative-standing curve is a separate output; filenames alone cannot establish the scientific variable.
6. **Then choose the comparison strategy.** Retain descriptive figures as descriptive evidence. If model-based probabilities are desired, specify horizon, peer measure, covariate treatment, and estimator. Check the basketball and tenure populations before claiming equivalent probabilities.

## 8. Evidence and source locations

Links are relative to this document where possible. The conclusions above do not require opening them.

### Repository evidence

**[R1]** [Original LOO repository audit](20261018_NVector_LOO_Repository_Audit.md). Cross-domain inventory, shared-congestion implementation, and recommendation B.

**[R2]** [CODA's October 18 response](20261018_CODA_Response_NVector_Army_LOO_Questions.md). Confirms subtraction, reports direct-LOO plot runs, and leaves the corresponding refit unresolved.

**[R3]** [Archived Army pool helper](../../../talent/Army_AWS_download/TALENT_NET_export_20260320-1000/add_cum_oer_metrics_mod_working.py), lines 319–320. Peer mean and own-minus-peer difference.

**[R4]** [Straight-LOO guide](../../../talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md) and [run matrix](../../../talent/re_entry/ARMY_RUN_MATRIX_CHECKLIST.md). Instructions distinguish plotting, pool definitions, and possible model changes; they are not themselves execution records.

**[R5]** [March 20 exported 520 notebook](../../../talent/Army_AWS_download/TALENT_NET_export_20260320-1000/520_pipeline_cox_working.ipynb). Cell 11 / index 51: final-observation plots and running proportions. Cell 12.3 / index 63: interval-duration fit. Cell 12.5 / index 68: event-specific Cox fits. Cell 12.6A / index 73: combined effects. Indices are zero-based and refer to the inspected file.

**[R6]** [513 notebook](../../../talent/talent_pipeline/513_marry_cox_with_perf_models_working.ipynb), Cell 10 / index 37; [April 21 exported 520 notebook](../../../talent/Army_AWS_download/TALENT_NET_export_20260421-0802/520_pipeline_cox_working.ipynb); [current 520 notebook](../../../talent/talent_pipeline/520_pipeline_cox_working.ipynb). Saved-image inventory and generating source.

**[R7]** [Archived bar helper](../../../talent/Army_AWS_download/TALENT_NET_export_20260320-1000/cox_plot_helpers.py), function plot_competing_risks_cif_bars, lines 863–871; [current helper](../../../talent/talent_pipeline/cox_plot_helpers.py), same function. Event counts divided by bin counts.

**[R8]** [Older CODA report](../../obsolete/pre_tier1_locks/CODA_report_to_COMPASS.md), Section 2.3, and [June 11 CODA reply](../../obsolete/pre_tier1_locks/20260611_1633_CODA_to_COMPASS.md), Section 3. Explicitly separate empirical proportions from Cox fits and say Fine–Gray was not implemented in that stack. Their peer-variable wording is superseded by the code and October response.

**[R9]** [Cox significance helper](../../../talent/talent_pipeline/cox_lifelines_significance.py), fit_and_test_significance, lines 88–97. Ordinary duration/event fitting interface.

**[R10]** [Basketball common-window provenance](manuscript_figures/section_4_5/pd46_statistics/runs/common_window_20261015_110901/provenance.json). Rows, players, repeated observations, outcome, and exploratory-test limitations.

**[R11]** [Final-season first-test provenance](manuscript_figures/section_4_5/pd46_statistics/first_test_curve_provenance.json). Final observed season and ever-drafted outcome.

**[R12]** [Tenure decision-year HERO provenance](../../re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM_provenance.json). Resolved-case denominator, exclusions, peer definition, and counts.

### Primary methodological references

**[M1]** Therneau, Crowson, and Atkinson, [Multi-state models and competing risks](https://cran.r-project.org/web/packages/survival/vignettes/compete.pdf). Cumulative incidence, event-free survival, cause-specific hazards, and Aalen–Johansen estimation.

**[M2]** Bob Gray, [cmprsk: crr](https://search.r-project.org/CRAN/refmans/cmprsk/html/crr.html), describing Fine and Gray (1999), *A proportional hazards model for the subdistribution of a competing risk*, JASA 94:496–509. Subdistribution regression and weighting.

**[M3]** Terry Therneau, [survival: finegray](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/finegray.html). Expanded weighted data, delayed entry, and time-dependent-covariate limitations.

**[M4]** [CoxPHSurvivalAnalysis documentation](https://scikit-survival.readthedocs.io/en/stable/api/generated/sksurv.linear_model.CoxPHSurvivalAnalysis.html). Fit interface using an event indicator and event/censoring time.

**[M5]** [cmprsk: predict.crr](https://search.r-project.org/CRAN/refmans/cmprsk/html/predict.crr.html). Predicted cumulative incidence from estimated cumulative subdistribution hazard.

