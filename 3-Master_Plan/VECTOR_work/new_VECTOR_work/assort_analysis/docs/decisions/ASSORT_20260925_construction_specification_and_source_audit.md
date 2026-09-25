# ASSORT — Construction Specification and Source Audit

**Last synced:** 2026-09-25

**Status:** Proposed implementation specification based on Charles's accepted design. Documentation only; no analytical construction or experiments executed during this audit.

## 1. Purpose and evidence boundary

This document translates the accepted decisions into a bounded construction and execution plan. The companion decision record explains the scientific reasons. The immediate scientific question is whether congestion changes selected winners without assortative assignment preference, and how the answer differs between the two chosen selection fractions.

Source-code inspection establishes what the existing routines implement. It does not verify their numerical outputs. The previously recorded target of 4,266 unique athletes and the canonical-team anomaly are earlier audit findings; this pass has not independently recomputed them. Final population size, roster capacities, missing-value counts, and reference congestion spread must be verified during separately authorized construction.

## 2. Input construction

Read the preserved source at repository-relative path `datasets/mbb/mbb_df_player_box.csv`. Its inspected header includes game, season, athlete and team identifiers, points, and minutes; points per minute is not a source field.

Record the input path, byte size, modification time, and content checksum at construction. Record checksums of reused code and software versions as well.

Follow this order:

1. Select season 2015. Validate numeric identifiers and preserve original source-row references for the audit.
2. Remove dash-name placeholders. Count distinct captured games by team-season and retain teams with at least eleven. Explicitly supply the threshold ten to existing code that retains counts strictly greater than its threshold.
3. Resolve each athlete to the canonical team with most distinct captured games among retained records, then greatest total minutes. Stop on an unresolved tie. Preserve every removed athlete-team record and the quantities supporting the choice.
4. Aggregate retained points and minutes by athlete and canonical team. Calculate points per minute once as total points divided by total minutes. Remove players below twenty total minutes.
5. Verify unique, nonmissing, integer-valued athlete identifiers and finite accepted rates. Do not silently impute anomalous missing or invalid source statistics; report whether they affect an eligible athlete before proceeding.
6. Standardize the final eligible rates using their population mean and population standard deviation, with denominator $N$. Keep athletes ordered by ascending numeric athlete identifier.
7. Count eligible athletes per observed team. Preserve the ordered team-identifier-to-capacity mapping, and require capacities to sum to $N$. Verify the previously reported correction from 18 to 14 eligible Arkansas–Pine Bluff records and the target of 4,266 unique athletes. A discrepancy requires explanation, not trimming to force the expected count.

The existing panel builder does not perform the canonical-team step. Its draft lookup and optional Sports-Reference merge are unnecessary dependencies for this mechanism experiment: observed draft outcomes neither define eligibility nor determine simulated winners. The authorized implementation should construct only the fields required by the accepted specification.

## 3. Assignment

Use the existing Grandchild assignment mechanism directly with the newly constructed capacity vector. For each arriving athlete, team weights are

$$
w_{ij}=R_j\exp[-\rho|A_i-\mu_j|],
$$

where $R_j$ is remaining capacity and $\mu_j$ is the team's current average ability. Empty teams begin at the population mean; the first actual member replaces that initial value. At $\rho=0$, probabilities are proportional to remaining seats.

Use 100 paired repetitions with master seed 20260925. Before execution, record a deterministic method for deriving the 100 distinct repetition seeds. Initialize both assignment conditions from the same repetition seed, with identical input ordering and generator type.

Inspection finds one random player permutation followed by one probability-weighted team choice per player. This supports the intended pairing structurally, but runtime verification must confirm the same order and aligned random consumption. Record the generator and library version; a seed alone is insufficient provenance across arbitrary software changes.

Require every athlete to appear exactly once and every labeled team to receive exactly its prescribed capacity. Reuse each completed assignment across all scoring and selection conditions.

## 4. Congestion, score, and selection

Calculate the linearly interpolated 99th ability percentile once and hold it fixed. With transition sharpness ten,

$$
v_i=\frac{1}{1+\exp[-10(A_i-\theta)]},
\qquad C_j=\frac{1}{n_j}\sum_{i\in j}v_i.
$$

Include the focal player in this team average. Everyone on a team shares its congestion.

Calculate the equal-player-weighted observed-roster congestion mean and population standard deviation once. Stop if the latter is nonfinite or at most $10^{-8}$; preserve the diagnostic values. Report the passing spread and its reciprocal.

For $\lambda\in\{0,1\}$, calculate

$$
S_i^{\mathrm{raw}}=A_i-\lambda C_{g(i)},
\qquad
S_i^{\mathrm{standardized}}
=A_i-\lambda\frac{C_{g(i)}-\mu_{C,\mathrm{ref}}}{s_{C,\mathrm{ref}}}.
$$

Apply no additional automatic scale, score clipping, or selection randomness. Rank by descending score, then ascending numeric athlete identifier. Select exactly $K$, rounding the target fraction times $N$ to the nearest integer with exact halves rounded upward. At the target population, the counts are 43 and 427.

Verify identical ability-only winners across assignments at each $K$, preservation of within-team ability order, and unchanged scores when only $K$ changes.

## 5. Reporting

Winner displacement is unbinned. For each assignment, compare congestion-on winners with ability-only winners at the same $K$. Save displacement counts, fractions, and the paired difference between $\rho=1$ and $\rho=0$. Summarize mean, median, full range, frequency of any displacement, and central 95% simulation ranges.

The secondary display uses sixteen approximately equal-count bins of leave-one-out mean teammate ability. Within an assignment, freeze membership across all scoring and scarcity conditions. Use ascending athlete identifier to order tied peer-quality values. Preserve individual repetition summaries; aggregate corresponding percentile-bin positions across repetitions and show mean selection rates with pointwise 2.5th-to-97.5th percentile simulation ranges. Show average actual peer-quality coordinates as well.

Corresponding bins can span different numerical peer-quality ranges across assignments. Therefore the aggregate curve is a summary by relative peer-quality position, not an estimate at one identical fixed numerical environment. Its simulation range is neither a confidence interval for the mean nor a simultaneous band. With 100 repetitions, tail percentiles are necessarily approximate.

The diagnostic uses the same number of bins as earlier displays but does not thereby reproduce their binning method. The current empirical HERO is described as equal-width; the accepted diagnostic uses approximately equal counts. Retain that difference alongside the population and outcome differences. No quadratic fit or formal inverted-U classification is included.

## 6. Existing routines: specific reuse boundaries

- `sports/sports_pipeline/panel_rebuild.py`, functions `_apply_box_qc` and `build_from_box`: supports coverage filtering and sum-then-divide construction, but lacks the canonical-team correction. Its fallback coverage threshold is five when the configuration attribute is absent; supply ten explicitly.
- `sports/sports_pipeline/panel_build.py`, functions `standardize_perf_zscore_by_season` and `standardize_perf_zscore_cross_section`: use default sample-standard-deviation calculations. They must not supply the accepted population standardization unchanged.
- `sports/541_grandchild_homophily_assign.py`, function `grandchild_assign`: accepts unequal capacities directly through `roster_caps`. Its weight formula and centroid update match the accepted assignment mechanism.
- The same file's empirical loaders call an older panel-preparation path and do not preserve the new canonical-athlete construction. Do not use them as experimental input loaders.
- `sports/tier1_pool_assignment.py`, function `simulate_generative_rosters`: assumes equal capacities and draws team targets before dispatching to Grandchild. Use the direct unequal-capacity assignment entry point instead.
- The same file's `build_roster_dataframe` creates positional identifiers. Preserve real athlete identifiers explicitly so the accepted tie rule and displacement comparison use people rather than accidental row positions.
- The same file's `add_team_pool_columns` supplies the full-team smooth congestion and separate leave-one-out mean ability. Pass the frozen threshold and sharpness explicitly.
- The same file's `selection_weights` and `choose_selected` clip scores at zero; selection also limits $K$ to positive-weight players. Their tie behavior is not the accepted explicit ascending-identifier rule. These routines cannot implement the agreed selection unchanged.
- Automatic congestion scaling through `effective_l_for_selection` is an ability-spread multiplier, not our fixed-reference congestion standardization.
- `sports/scripts/gallery_knobs.py` currently defaults to shared team congestion. That current default does not establish which mode every historical output used.

## 7. Storage and completion gate

All new analytical artifacts belong under this investigation's existing folders: code in `code/`, derived inputs and manifests in `data/`, results in `outputs/`, and execution records in `docs/run_records/`. Existing raw files, prior sweeps, and shared research code remain reference sources.

The next execution authorization should cover a small isolated driver, input construction, integrity checks, the 100 paired repetitions, and the accepted outputs. It should not encompass new parameter sweeps, empirical HERO reconstruction, or changes to shared pipelines.

This audit required no additional scientific design question. Data-integrity checks and runtime pairing checks remain pending until execution is authorized. If they expose a substantive population or mechanism choice, stop and return that specific issue to Charles.

