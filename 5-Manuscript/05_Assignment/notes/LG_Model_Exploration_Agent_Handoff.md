# LG exploration implementation handoff

Prepared 6 October 2026. For the advisor-facing overview, read `LG_Model_Exploration_Executive_Summary.docx`. For the full specification, read `LG_Model_Exploration_for_Alex.docx` (six-page detail retained for Charles; native editable Word equations). That document contains the agreed design and the explanatory text for Alex. Charles's original `LG Model exploration.docx` remains unchanged. No new experiments, simulation code, jobs, or fits were run to prepare this package.

## Defining model distinction

Charles clarified: LG combines metadata-based attachment preference with FIXED prescribed roster sizes. Varying prescribed r across experiments remains LG. Allowing realized sizes to vary under excess or absent capacity is a DIFFERENT model, provisionally the variable-roster extension. Never call it variable-size LG. No degree-based preferential attachment is intended. Uncapped assignment uses only exp(-rho*abs(A_i-T_j)), normalized across all teams; at rho=0 this is uniform over teams. Finite-cap remaining-seat weighting is a capacity effect and still requires specification for excess capacity.

## Mission and scope

Build a modular, notebook-led LG simulation exploration inside the supplied `lg_exploration/` folder. The folder already exists and contains this handoff and reference snapshots; the runnable implementation is still to be built. Preserve the paper chapter, Romania acquisition, legacy production code, and unrelated repository changes. Start with a small equal-roster normal-talent construction example; expand only after Charles reviews the settings and output. Do not assume all open choices below are approved. Do not launch a broad sweep or Slurm job merely because this handoff exists.

## Folder-only access and missing supporting files

Charles will give the implementing agent access only to `lg_exploration/`. Treat this folder as the project root. Do not request broader repository visibility as a prerequisite, search outside this folder, or import research modules from the original repository. Paths in the code map below identify historical sources: find their supplied copies under `reference_snapshot/`, preserving the recorded repository-relative path. The source manifest records provenance, not permission to access those original locations.

Keep `reference_snapshot/` unchanged. Create adapted working code in `code/`, notebooks in `notebooks/`, and configuration in `settings/`. Use project-local output folders and explicit configuration; remove legacy assumptions about the parent repository, empirical datasets, and output destinations before executing copied code. Do not copy unrelated data or silently replace a missing scientific component with an invented approximation.

The reference collection has not been verified to contain every supporting module. If a required file is missing, report its exact filename or import name, the supplied file that needs it, and why it is necessary. Charles and NVector will supply a copy into this folder. Continue independent work while waiting; do not broaden access. Record any supplied file and its provenance in a dependency log.

The installed `sports_net` Python environment may provide third-party libraries. This does not authorize access to other research folders and does not require copying Python or creating a new Git repository. Keep project code independent of the parent checkout so it can later run on Rivanna with an appropriate Python environment.

## Agreed decisions

- Fixed total M in the equal-roster experiment; vary r with J=M/r. Initial r values divide M exactly. J=1000 is dropped.
- Reuse exactly the same A_i values across roster and rho settings within a population repetition. Fresh population for each population repetition.
- Start with standard normal talent. Later include Beta(2,2) and other specified distributions. Default transformation uses theoretical mean and standard deviation, not forced sample standardization; retain original draws and an original-scale option.
- Every team starts empty with centroid equal to realized population mean. First arrival replaces it with A_i; subsequent centroid uses actual members. Empty final teams permitted in variable-size designs.
- Variable-size experiment fixes M and J. Visible cap multiplier relative to M/J, including no cap. Current engine does not implement this extension.
- Division H_sort, team means, team variances, roster sizes, empty counts. H_sort is not a per-team statistic. Compare rho=0 under corresponding constraints.
- Save reusable division checkpoints before SCORE and SELECT. Separate repetition counts for population, assignment (default 1), and stochastic selection; separate reproducible random streams.
- Existing SCORE is the scientific starting point; audit actual scaling/clipping before adopting a concrete adapter.
- Selection global only: deterministic top-K, sequential exponential-weight exact-K, and NEW logistic Bernoulli calibrated to sum(p)=K. No team quotas.
- NEW Bernoulli: p_i=expit((S_i-c)/t_B); solve c so sum(p_i)=K; independent draws. Expected K, actual count variable. Explain this prominently in notebook and run report. Neither legacy helper rule B nor legacy MLE implements this formula.
- Mosaic required, especially panels 7 and 8 for fixed A bands versus peer strength. User boundaries (90,75,50); bins visible. Additional summaries separate.
- MLE recovery last: matching-model first, then cross-model comparisons. Identify generation and fitting equations for every test.

## Verified code map

1. `sports/541_grandchild_homophily_assign.py`: `grandchild_homophily_weights`, `grandchild_assign`, `validate_grandchild_assignment`, `within_team_mse`. Weights remaining seats times exp(-rho*distance). Starts empty at mean(A); updates first member exactly. Requires sum(caps)=M (or J*r=M); validator requires zero remaining seats. Variable capacity cannot be achieved by changing configuration alone. Numerical underflow currently falls back to uniform over open teams, which differs from stub weighting. Record this issue for an explicit numerical policy.
2. `sports/tier1_pool_assignment.py`: `add_team_pool_columns` computes team MEAN logistic viability including self; `poolq_loo` is a different, leave-one-out plotting variable. `effective_l_for_selection` uses an ability-range heuristic and can automatically multiply congestion by p90-p10. `selection_weights` implements subtraction then clips negatives to zero. `choose_selected` clips again and caps K at the count of positive scores. These are consequential with normal talent. Do not call the clean signed-score exact-K equation implemented without resolving them. Legacy B uses min(K_eff*w/sum(w),1), not the new threshold logistic and not the MLE softmax.
3. `sports/scripts/pd21_draft_bernoulli_mle.py`: `board_logits`, `softmax_probs`, `bernoulli_loglik`, `fit_joint_bfgs`. eta=A/t_MLE-lambda*L; independent Bernoulli log likelihood; gamma/lambda/t jointly fitted in log space. Probability sum=1 per season. Synthetic divisions must be separate normalization batches. Reuse math through a synthetic-data adapter, not the empirical data-loading main entry point. `attach_player_level_lc` calls empirical `_season_k_theta`; avoid silently re-estimating theta from random simulated Y when testing fixed generating parameters.
4. `scripts/big_fish_data_story.py`: domain loaders are empirical, not generic synthetic input. `run_cct_probe` currently uses z in [1,2]; `run_elite_probe` uses top20 percent. User-approved percentile bands therefore need an adapter rather than blind reuse. `sports/scripts/build_data_story_mosaic.py` composes image panels via a manifest; `story_page_layout.py` supplies layout. Preserve scientific purpose of panels 7/8 and label new bands explicitly.
5. `sports/scripts/541_grandchild_rho_sweep.py`, `grandchild_roster_size_c_sweep.py`, `grandchild_lambda_select_sweep.py`: inspect for patterns, not defaults to copy wholesale. Historical lambda sweeps may regenerate rosters across lambda; this project requires saved identical rosters for score/select comparisons.
6. `3-Master_Plan/re_entry/LG_model_desk_reference.md`: assignment equations and rationale. Its historical selection framing predates later stochastic decisions; today's approved three-rule design governs this exploration.
7. `NVector_to_SVector_MLE_Bernoulli_response.md`: verified historical fitting bridge, references, and saved gamma=19.572332081866243, lambda=1.3024305834948529, t_MLE=1.0698967300656186. These are historical empirical estimates, NOT newly approved generating defaults.

## Open choices to bring to Charles one at a time

- Variable-roster extension finite-cap kernel: confirm whether to retain remaining-seat weighting for excess capacity. Uncapped metadata-only weighting is clarified above; no degree-based attraction. Keep the extension separate from fixed-roster LG.
- Resolve score/selection clipping and scale policy explicitly. Preserve raw signed score and effective legacy score separately if comparing; do not silently patch existing helpers.
- Choose M, r grid, rho grid, J for variable-size runs, cap grid, distribution parameters, lambda/gamma/theta/scaling values, temperatures and selection fractions. No numerical sweep grid has been approved yet.
- Theta fixed versus scarcity-linked. Fixing theta isolates a SELECT-only scarcity sweep; recomputing it changes SCORE too.
- Count rounding, tie handling, within-team variance convention (population variance gives zero for singleton), sparse plotting thresholds and exact band boundary ties. Singleton leave-one-out peer values are undefined; retain players for global selection and report plotting exclusions.
- Keep team mean T_j and focal-player-excluded peer mean distinct in captions. Do not silently switch axes.
- MLE synthetic adapter: threshold policy, input schema, generation and preprocessing must match. Lambda=0 leaves gamma unidentified; constant congestion cancels in softmax. Matching legacy generation expects only one winner per division, so recovery may need many independent outcome replicates. Failed or weak recovery is not automatically a bug. rho requires a separate assignment calibration if later requested.

## Mac and Rivanna implementation requirements

Charles reports MacBook Pro, M5 Pro, 48 GB RAM, '18/10 cores'; do not guess what those counts mean for CPU parallelism. Detect resources and expose N_WORKERS. One shared Python implementation, notebook UI plus CLI using the same saved settings. No hardware-specific imports or absolute Mac paths in scientific modules. Paths relative to this exploration folder and configurable data/output roots. Compact arrays/data frames, not dense player-team matrices; evaluate memory and elapsed time on a small run before choosing worker count.

Stable run IDs from scientific settings plus repetition IDs; seeds independent of worker scheduling. Save after each completed division, score configuration, selection batch, and fit. Flush progress records; atomically finish checkpoints; resume only verified complete units; retain partial/error state. Separate task output directories and no concurrent mutation of a shared notebook or result file. Log timestamps, configuration, progress counts, new vs reused work, paths, elapsed time, and failures. Aggregate only compatible configurations; do not pool repeated observations as independent new players.

Slurm array tasks can shard independent experiment units. `sports/outputs/simulation_sweeps/rivanna_stage2_array_faithful_538.slurm` is a PATTERN ONLY: it contains an old account, partition, module, reset flag, email and paths. Confirm current allocations/environment before producing operational scheduler settings; do not copy destructive reset behavior. `scripts/DATA_SYNC.md`, rsync push/pull/shared helper scripts explain existing Git versus rsync policy. Add new results path to ignore/sync scope before large runs; inspect actual transfer filters. Git tracks code/config/notebooks/scheduler; bulk checkpoints/results use rsync, not Git. No transfer or scheduler submission authorized by this packaging step.

## Working style and deliverables

Charles wants fast, incremental coding, generous code comments and visible notebook settings. He runs the notebooks. Perform small meaningful checks of formulas, counts and checkpoint resume; no extensive simulation suites without need. Standing instruction: notebook editing rule waived until further notice except Army classified-system manual-transcription work. Do not request that waiver again. Explain terminology for a graduate student who has not read the code. Preserve and extend a decision log; do not silently change definitions to find a desired curve.

Deliver notebook plus Python companion/CLI, example settings, resumable storage, readable results, then a configurable Slurm template and explicit sync instructions. Keep unapproved scientific choices visible. No independent new fitting theory or change to the dissertation manuscript is requested.

## Package provenance

The handoff bundle contains the two Word specifications, this handoff, start-here instructions, and selected reference source copies with SHA-256 provenance records. These are reference materials, not a completed executable distribution: supporting imports and third-party dependencies still need checking. The implementing agent has access only to the supplied exploration folder. Verify supplied snapshot files against the included manifest when needed; do not try to verify them against the inaccessible original repository. No student data or credentials are included.
