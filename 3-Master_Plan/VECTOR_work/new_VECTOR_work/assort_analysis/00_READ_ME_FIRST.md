# ASSORT — Assortativity Investigation Workspace

**Structured research outline — start here for rapid review:** [Question → evidence → result → meaning → limits → next step](docs/briefings/ASSORT_20260928_Stop_the_Presses_Structured_Research_Outline.md). This preserves the full investigation in a scan-friendly outline and leaves the chronological narrative unchanged.

**Research narrative — start here:** [Consolidated research narrative](docs/briefings/ASSORT_20260928_Alex_Rehearsal_Stop_the_Presses_to_Three_Questions.md). It narrates the stop-the-presses pool/measure audits, separates the draft-ranking diagnostic, explains the model experiments, assesses the three questions, embeds ten key figures, and registers all 34 saved plots. Prepared for research review; no new experiment or PDF generation.

**Latest direct test:** [Rho-by-scarcity comparison](docs/results/ASSORT_20260927_rho_scarcity_v1_report.md), fixed lambda four, 50% versus 1%, rho one versus 0.05. Relative profiles remain different at 1%; changing rho changes about 24–27% of selected identities versus 2.5–2.7% at 50%, though fewer people change in absolute terms. No simple neutralization of rho by scarcity was demonstrated. [All model plots and reports in order](docs/results/ASSORT_20260927_model_plot_trail.md). Stop for interpretation.

**Latest rho comparison:** [Rho one versus 0.05](docs/results/ASSORT_20260927_rho005_v1_report.md), at 50% selection and lambda four. New matched assignments at 0.05 largely flatten the broad profile around 50%, with a modest upper-end decline. Sorting falls from about 0.36 to 0.088; extreme peer environments largely vanish. Empty EW bins are missing environments, not zero success. This shows substantial shape dependence in the tested configuration, not universal necessity. Stop for interpretation.

**Latest requested pivot:** [50% selection sweep](docs/results/ASSORT_20260927_selection50_v1_report.md) compared lambda 0, 1, 2, 4, 8, 16 at rho one. Eight gives a clear EW rise-and-fall visual candidate across the three seasons; four already declines. No unique match or empirical lambda claimed. Rho 0.6 fallback was unnecessary and not run. Prior fixed-penalty scarcity result remains separate. Pause for Charles's visual judgment.

**Latest completed stage:** [Fixed-penalty scarcity report](docs/results/ASSORT_20260927_scarcity_bars_v1_report.md): lambda four and rho one held fixed, selection reduced from 10% through 5%, 2.7%, and 1%. Absolute bars shrink, but relative EW downturns persist visually across the three seasons; 2015's peak shifts right. Sparse tail counts remain a limitation. This does not demonstrate scarcity erasing the relative downturn in the tested configurations. All checks passed; pause for interpretation before any rho comparison.

**Latest visual exploration:** [Penalty bar-chart report](docs/results/ASSORT_20260927_penalty_bars_v1_report.md): at 10% selection and rho = 1, lambda 0, 1, 2, 4 were compared using 16 EW and quantile bins. At four, EW bars rise then fall in all three seasons while quantile bars rise; far-right EW bins are sparse. Pause for joint visual interpretation. No automatic criterion, penalty choice, scarcity comparison, or rho comparison. Earlier automatic-search draft was never executed and has been disabled.

**Latest diagnostic:** The [penalty-magnitude report](docs/results/ASSORT_20260927_penalty_magnitude_v1_report.md) explains why raw congestion at $\lambda=1$ can change marginal winners without producing a downturn. Penalty standard deviations were 0.026–0.033 against a performance standard deviation of one. In 2015 with assignment preference, the highest peer group's 0.292 mean performance advantage over the next group faced only 0.049 additional penalty. This is descriptive evidence, not proof about curve shape or necessity. Saved results were checked in sports_net; no new assignments or coefficient sweep. Pause for interpretation and a penalty-scale decision.

**Latest comparison:** Charles authorized [2.7% versus 10% selection](docs/results/ASSORT_20260927_selection_rate_comparison_v1_report.md) on exactly the same saved teams and scores. At 10%, more people lost a selected spot when congestion was enabled, but they were a smaller fraction of the selected group in all three seasons and both assignment conditions. Averaged curves still did not demonstrate a clear downturn. All original 2.7% selections were reproduced exactly; 20% remains parked. Execution is complete; stop for interpretation.

**Latest completed experiment:** The [three-season mechanism report](docs/results/ASSORT_20260927_three_season_mechanism_v1_report.md) documents 100 paired repetitions per season at 2.7% selection. Congestion displaced some winners without preference and more with preference, but the averaged curves did not demonstrate a clear downturn under either assignment setting. Independent reconstruction checks passed. Execution is complete; stop for interpretation. Earlier source-gate and proposal statements below are historical.

**Active execution checkpoint:** Charles authorized the revised three-season, 2.7% mechanism comparison. The [2014/2016 source preflight](docs/results/ASSORT_20260927_three_season_mechanism_v1_preflight_report.md) ran and found point/minute inconsistencies. Simulations have not started; the brief's source-quality gate requires a decision on extending the documented omission fallback. Audit code, data, and run record are isolated under the three_season_mechanism_v1 name. This supersedes the pending-authorization language in earlier checkpoints.

**Latest orientation — September 27, evening:** Read the [return-to-assortativity brief](docs/decisions/ASSORT_20260927_return_to_assortativity_brief.md). It recovers the original choices, distinguishes winner changes from explaining a downturn, and proposes a four-case first stage for Charles's review. The proposed stage has not been authorized or executed. Older checkpoints below are historical; the accepted later population is 4,267 players, not the provisional counts in the September 25 construction records.

**Created:** 2026-09-25

This folder contains newly created documentation, code, notebooks, derived data, outputs, and provenance records for the assortativity investigation.

## Scope

The investigation concerns the interaction among assortative assignment, congestion, and selection scarcity. The scientific brief provides the broader research rationale. The [detailed experiment decision record](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260925_experiment_choices_and_rationale.md>) records Charles's subsequent choices, detailed explanations, and questions still open. Read both before proposing implementation; accepted design choices are distinct from execution authorization.

## Documentation style

**Live execution feedback:** Charles wants real-time computational feedback as well as narrative updates. Announce code start and completion, relay actual script milestones (season, completed/total repetitions, elapsed time when available), and distinguish machine execution from reading, interpretation, and document editing. Use measured progress only; never invent percentages or imply that code is running after it has finished. For future long-running drivers, preserve resumable progress and concise periodic logging.

**Game-box listing checkpoint (September 27):** Charles clarified that the proposed continuity pool first required checking whether “did not play” game-box listings were consistent. The bounded [2015 source audit](docs/results/ASSORT_20260927_box_listing_consistency_v1_report.md) found coherent flags and widespread no-play listings, but 4,258 of 4,267 accepted players already appear in at least half their team's captured boxes, including all 339 short-stint players. That proposed half-season listing rule would exclude only nine and has been withdrawn as a useful alternative pool for this population. The [run record](docs/run_records/ASSORT_20260927_box_listing_consistency_v1_run_record.json) and [source diagnostics](outputs/box_listing_consistency_2015/) are isolated here. No new pool was implemented.

**Position checkpoint (September 27):** Charles requested a [descriptive 2015 points-per-minute distribution by recorded position](docs/results/ASSORT_20260927_ppm_by_position_v1_report.md). The three-panel plot shows 2,310 guards, 1,602 forwards, and 347 centers; one hybrid and seven unavailable labels were counted separately, not reassigned. The player pool and points-per-minute values were unchanged. [Run record](docs/run_records/ASSORT_20260927_ppm_by_position_v1_run_record.json); [plot and data](outputs/ppm_by_position_2015/). No position-adjusted performance measure or new sorting test was run.

**Participation-and-duration checkpoint (September 27):** Charles requested a [joint comparison of games played and minutes per appearance](docs/results/ASSORT_20260927_participation_duration_crosscheck_v1_report.md), followed by a holistic assessment of the twenty-minute player floor, eleven-captured-game team rule, and relative participation measures. Among 339 players averaging under five minutes per appearance, 268 appeared in fewer than half their team's captured games and only one appeared in at least 90%. The [report](docs/results/ASSORT_20260927_participation_duration_crosscheck_v1_report.md) records the recommendation and limitations; [plots and counts](outputs/participation_duration_2015/) and the [run record](docs/run_records/ASSORT_20260927_participation_duration_crosscheck_v1_run_record.json) remain isolated here. No new filter or simulation was executed.

**Latest descriptive checkpoint (September 27):** Charles requested [two 2015 game-participation plots](docs/results/ASSORT_20260927_games_played_distributions_v1_report.md): positive-minute games played and the percentage of each team's captured games with positive player minutes. The median eligible player appeared in 30 games and 93.9% of their team's captured games. The [run record](docs/run_records/ASSORT_20260927_games_played_distributions_v1_run_record.json) identifies the frozen source, accepted audit population, plotting code, and image outputs. The percentage denominator is captured games, not a verified complete official schedule. No new sorting or draft analysis was run for these plots.

**Current checkpoint (September 27):** The bounded 2015 [rotation and measured-peer audit](docs/results/ASSORT_20260927_rotation_audit_v1_report.md) has been executed and internally checked. It compares all eligible focal players' peer averages using every eligible teammate versus teammates averaging at least five minutes per played appearance. The [decision record](docs/decisions/ASSORT_20260927_rotation_audit_decisions.md) explains the source rules and scientific limits; the [run record](docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json) contains code, input, and output hashes. No draft-outcome curve, new sorting estimate, or assignment simulation was run. The earlier assortativity experiment remains paused.

**Latest checkpoint (September 27):** Charles authorized and we completed the bounded [five-minute sorting-sensitivity comparison](docs/results/ASSORT_20260927_sorting_sensitivity_v1_report.md) under its [pre-run plan](docs/decisions/ASSORT_20260927_sorting_sensitivity_plan.md). The observed sorting index rose from 0.06194 in the full 4,267-player population to 0.07127 among the 3,928 regular-playing players, but the random-allocation reference rose too. The reference-adjusted descriptive change was only +0.00206, and both observed indices were below their own random-reference ranges. The isolated [run record](docs/run_records/ASSORT_20260927_sorting_sensitivity_v1_run_record.json) records the input, code, output hashes, and 1,000 shuffles per group. No assignment simulation or draft-outcome curve was run; stop for Charles's interpretation before proposing the next test.

**Execution stop (September 25):** The first authorized construction attempt exposed [two source-data decisions](docs/source_review/ASSORT_20260925_initial_execution_stop.md). The experiment has not run. Keep this stop report with the decision record and construction specification until Charles settles the questions.

**Construction checkpoint (September 25):** The design and reporting decisions are settled. Read the [construction specification and source audit](docs/decisions/ASSORT_20260925_construction_specification_and_source_audit.md) for the implementation plan, code compatibility findings, and checks pending authorized construction. No analytical code or experiment has been executed for this investigation.

**Current reading checkpoint:** read the [data hygiene and model-history review](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_data_hygiene_and_model_history.md>) and companion [questions for SCOUT](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_questions_for_SCOUT.md>) before freezing the input population. Charles's one-game-opponent explanation prompted this review. The accepted 2015 season and experiment settings remain recorded; exact eligible rosters and filters are provisional. Existing generated outputs are historical evidence, not inputs or resumed runs for the new investigation.

Charles welcomes detailed explanations and brief examples. Unless Charles has himself used a shorthand expression, write the full term followed by the proposed shorthand in parentheses, and continue doing so until he uses that shorthand. Explain symbols in ordinary language. Ask one necessary design question at a time.

Before executing local analysis code or a data-check script, tell Charles plainly that code is about to run; say when the run completes. Keep those notices distinct from scientific reasoning and document editing.

## Folder rules

- General Markdown belongs in `docs/`.
- New analysis code belongs in `code/`.
- New notebooks belong in `notebooks/`.
- Derived data and input manifests belong in `data/`.
- Tables, figures, and diagnostics belong in `outputs/`.
- Execution and provenance records belong in `docs/run_records/`.
- Superseded material belongs in `archive/`.

Existing source code, source data, historical outputs, and authoritative repository documents remain in their original locations. This workspace may link to those sources but does not silently replace them.

## Naming

Use the `ASSORT_YYYYMMDD_` prefix and a version suffix where needed. Related code, notebooks, outputs, and run records should share a common stem. Avoid ambiguous names such as `final.py`, `results.csv`, or `new_notebook.ipynb`.

## Evidence and execution status

Label artifacts as one of:

`proposed` · `authorized` · `executed` · `verified` · `superseded`

Every executed analysis must have a run record identifying the code, inputs, parameters, outputs, date, and verification status. Creating files here does not authorize execution of experiments or modification of existing repository research artifacts.

## Initial state

The folder structure was created on September 25, 2026. No analysis code, notebook, data file, figure, table, or experiment has been created yet.
