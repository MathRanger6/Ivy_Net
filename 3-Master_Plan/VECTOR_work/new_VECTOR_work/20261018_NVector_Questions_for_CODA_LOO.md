# Questions for CODA about Army peer measures

Charles and NVector | Clarification requested from existing records | 18 October 2026

We are deciding how much prominence leave-one-out (LOO) deserves in Chapter 4. Before calling the Army figures evidence about peer quality, we need to distinguish the average of other officers from own rating minus that average. Please answer from the existing code and saved runs. No new analysis is requested at this stage.

Both the March 20 archived helper and the current helper calculate pool_minus_mean as own rating minus pool_tb_ratio_mean. Older explanatory memos describe it as the peer mean itself. The later STRAIGHT_LOO_MOSAIC_AWS_GUIDE explicitly distinguishes the two. Please help establish which outputs are authoritative and whether a corrected straight-LOO run was actually completed.

### 1  Which Army result is authoritative now

Please identify the latest notebook/script, configuration, saved figure and data/export version for the main promotion HERO and Cox results. Are we still using the March 20–25 outputs, or did later AWS runs replace them? Give paths, dates, actual officer and observation counts, and the analytic year window.

### 2  What exactly is the horizontal variable

For each main HERO, conditional plot and Cox-effect figure, give the exact field name and formula. Is it the LOO peer mean, own minus LOO mean, its negative, a standardized version, or a full mean? Identify which own rating enters, and how standardization is computed. In particular, was the older prose definition of pool_minus_mean an error, or did a different data preparation step overwrite that column?

### 3  Was the straight LOO change completed

The guide proposes switching panels 1, 3, 7, 8 and 9 to pool_tb_ratio_mean_snr_fwd. Did that happen? If so, please provide the actual outputs and run settings, and distinguish plot-only changes from a Cox or competing-risk refit. The current local plotting defaults still use pool_minus_mean in several places.

### 4  Who belongs to each officer’s pool

For the authoritative result, specify rater versus senior rater, rank restrictions, timing anchor, active rating intervals versus snapshot grouping, self-exclusion by person versus row, duplicate handling, valid-value rules, minimum peers and zero-rating treatment. Were the overly large legacy pools repaired before that result was generated?

### 5  What outcome does each plot estimate

Is the plotted height a cumulative incidence accounting for competing events, a last-snapshot indicator rate, an ever-promoted rate or a model-predicted hazard ratio? For cumulative incidence, state the endpoint, competing event, censoring rule and time horizon. Please distinguish these outputs even if all were called HERO.

### 6  What supports the strongest or most robust finding

Please point to saved coefficient tables, uncertainty intervals or formal tests and sensitivity runs supporting the Army peak and downturn. Identify whether the evidence remains after own-performance adjustment and under straight LOO. If no such comparison was completed, please say so rather than rerunning it now.

### 7  Which Cox specification was fit

List the fitted variables, transformations, interaction, time-varying setup and dependence treatment. The saved local record includes own rating and own-minus-peer rating with quadratic and interaction terms. How should the plotted combined-effect curve be read in that full model? Please supply the saved model summary and clarify which promotion outcome it fits.

### 8  Are there completed unit level results or additional reasons for LOO

Do any completed battalion, brigade or division analyses use a genuine self-excluded performance mean rather than rating pools or unit covariates? If so, give their definitions and outputs. Also identify any dated decision or reference explaining why LOO was chosen beyond excluding own performance from peer quality.

### 9  Please resolve the figure naming discrepancy

ARMY_partial_effects_pool_minus_mean.png visibly plots z_pool_minus_mean_snr_fwd. ARMY_combined_effect_pool_minus_mean_stdz.png visibly plots z_tb_ratio_fwd_snr despite its filename. Which file should be cited for each scientific statement, and is the latter simply an incorrectly named extraction?

### Files establishing the questions

**Army pool definitions and current settings**

[talent/talent_pipeline/add_cum_oer_metrics_mod_working.py](../../../talent/talent_pipeline/add_cum_oer_metrics_mod_working.py)

[talent/talent_pipeline/pipeline_config.py](../../../talent/talent_pipeline/pipeline_config.py)

**Archived Army implementation and figure provenance**

[talent/Army_AWS_download/TALENT_NET_export_20260320-1000/add_cum_oer_metrics_mod_working.py](../../../talent/Army_AWS_download/TALENT_NET_export_20260320-1000/add_cum_oer_metrics_mod_working.py)

[3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/EXTRACT_MANIFEST.txt](../../re_entry/HEROs_and_PASSes/army_sandbox/EXTRACT_MANIFEST.txt)

**Army Cox configuration and saved execution record**

[talent/talent_pipeline/pipeline_config_17_1.py](../../../talent/talent_pipeline/pipeline_config_17_1.py)

[talent/talent_pipeline/pipeline_config_div_name.py](../../../talent/talent_pipeline/pipeline_config_div_name.py)

[talent/talent_pipeline/520_pipeline_cox_working.ipynb](../../../talent/talent_pipeline/520_pipeline_cox_working.ipynb)

**Conflicting Army descriptions and later correction**

[talent/documents/Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md](../../../talent/documents/Coda_Vector_Brief_Army_Evidence_For_Brian_Memo.md)

[talent/documents/Coda_Summary_For_Scout_and_Vector_Post_Replication.md](../../../talent/documents/Coda_Summary_For_Scout_and_Vector_Post_Replication.md)

[talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md](../../../talent/re_entry/STRAIGHT_LOO_MOSAIC_AWS_GUIDE.md)

Please separate verified answers from recollection and outstanding uncertainty. We can finalize the Army portion of the audit after Charles brings back your response.
