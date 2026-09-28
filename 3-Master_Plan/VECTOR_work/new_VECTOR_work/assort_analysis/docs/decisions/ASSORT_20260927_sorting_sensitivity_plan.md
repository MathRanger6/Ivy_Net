# Next bounded question: does the rotation definition change measured sorting?

**Status:** Charles accepted this as the next scientific question on September 27, 2026. This is a documented plan, not an executed analysis. Under Charles's standing rule, agreement with a question or plan does not itself authorize coding or an experimental run. The five-minute boundary is fixed for this first comparison.

**Execution addendum (September 27):** Charles subsequently instructed, “ok let's go.” The one comparison specified here was executed and internally checked. See [the result report](../results/ASSORT_20260927_sorting_sensitivity_v1_report.md) and [run record](../run_records/ASSORT_20260927_sorting_sensitivity_v1_run_record.json). The original plan text below is retained as the pre-run specification and historical decision record.

## The research trail in ordinary language

We first rebuilt one 2015 men's basketball population from the frozen game data. We checked two kinds of inconsistent minutes against game-specific box scores, recovered values that could be matched, and kept an explicit fallback for unresolved rows. That gave us 4,267 eligible players on 351 teams, with a source and run record that can be audited.

Next we asked how many players were brief participants *when they played*. At the provisional boundary of five minutes per positive-minute appearance, 339 eligible players fell below it, but they supplied only 0.672% of the captured minutes among eligible players. This told us brief participants are a meaningful fraction of the *unweighted player pool* even though they use little court time. It did not tell us whether they were less talented or less competitive for roster spots.

Next we kept every focal player fixed and changed only the teammates counted in that focal player's peer average. About 60% of peer averages changed; the restricted average rose by 0.071 season-wide points-per-minute standard deviations on average. There were no zero- or one-peer cases. This told us the *measured peer axis* is sensitive to the pool definition. It could not tell us whether overall player performance is more assorted across teams, because the sorting index uses player values and team membership, both of which remained fixed in that comparison. Nor did it test a draft outcome or a congestion mechanism.

So the next question is: **If we define the observed player population as those averaging at least five minutes when they play, does the sorting index of their measured points-per-minute values look different from the full eligible population's index, after accounting for the different number of players and team capacities?** This is one descriptive sensitivity, not a search for the best-looking threshold.

## Exact proposed comparison

Use the already verified `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz` as the fixed input, after verifying its checksum against `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json`. Do not silently use a historical panel export or regenerate the population under different rules.

1. **Full observed population:** all 4,267 eligible 2015 players, their accepted season points-per-minute values, and their accepted canonical team assignments.
2. **Regular-playing population:** the 3,928 members of that same group who averaged at least five minutes per positive-minute appearance. Keep their same season points-per-minute values and team assignments. The prior audit shows at least eight qualifying players on each of the 351 teams, but verify those counts again from the exact input.
3. Calculate the **sorting index** ($H_{\mathrm{sort}}$) separately in each population, using the repository's player-weighted definition:

   $$
   H_{\mathrm{sort}}
   =1-\frac{\sum_i(p_i-\bar p_{g(i)})^2}
            {\sum_i(p_i-\bar p)^2},
   $$

   where $p_i$ is the accepted season points per minute for player $i$, $g(i)$ is that player's team, $\bar p_{g(i)}$ is the mean among included players on that team, and $\bar p$ is the mean among all included players in that population. Use raw points per minute for transparent units. A single common standardization of the same population would leave this ratio unchanged. Cross-check the computation against `sports/541_grandchild_homophily_assign.py`, function `realized_sorting_index_H_sort`, and `sports/scripts/pd21_rho_hsort_calibrate.py`, function `empirical_h_sort`.
4. For **each population separately**, hold its observed player values and exact team sizes fixed, then randomly shuffle those values among the existing team slots. This is a random-allocation *reference*, not a fitted assignment model. With $J$ nonempty teams and $N$ players, the exchangeable reference has expected index $(J-1)/(N-1)$; report that value and check it against the mean of 1,000 reproducible shuffles. Use a recorded seed of `20260927`. The shuffles supply a reference range, not an estimate of sampling uncertainty for all Division I seasons.
5. Report only the observed index for each population, its random-reference mean and 2.5th–97.5th percentile range, the observed-minus-reference value, and the raw and reference-adjusted full-to-regular differences. Include player and team counts, team-size ranges, and the number of regular-playing players removed from the full sample. Keep individual shuffle results in an isolated output file for reproducibility.

The reference-adjusted difference means

$$
\bigl(H_{\mathrm{regular}}-E_{\mathrm{regular}}\bigr)
-\bigl(H_{\mathrm{full}}-E_{\mathrm{full}}\bigr),
$$

where each $E$ is the random-allocation reference mean for *that population*. It is a descriptive contrast, not a causal effect or a formal test of the difference between two nested samples. A higher raw index alone would be hard to read: removing players raises the expected random index even if there is no measured sorting preference, because $N$ becomes smaller while the number of teams remains 351.

## Interpretation boundary and stop point

If the **reference-adjusted** index rises from the full population to the regular-playing population, that supports the narrow proposition that brief participants mask **measured points-per-minute sorting** in this 2015 population. If it does not, this particular five-minute definition does not resolve the low measured sorting result. Either outcome still leaves underlying talent, coaching and role selection, the draft-outcome curve, and congestion mechanisms untested. No conclusion about the necessity of assortative assignment follows from this comparison alone. The archived 2015 index near 0.061 and its earlier zero-preference model run used a different historical panel; neither is a substitute for the two new same-population random references.

Do not change the five-minute threshold, fit the assignment-preference parameter, rerun the paused assortativity simulation, reconstruct the empirical hero curve, or add a second performance measure within this task. Report the one comparison and stop for Charles's interpretation before deciding on any further test. When execution is separately authorized, announce clearly when local code starts and when it finishes, as Charles requested.

Proposed new artifacts, if authorized: one isolated driver under `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/`, reference draws and summary under `.../outputs/sorting_sensitivity_2015/`, a run record under `.../docs/run_records/`, and a narrated result under `.../docs/results/`. The frozen data, prior audit outputs, and older simulation outputs remain unchanged.
