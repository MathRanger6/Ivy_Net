# Does the five-minute playing rule change measured basketball sorting?

**Status:** Executed and internally checked on September 27, 2026. This is one descriptive comparison in the accepted 2015 men's basketball population. It is not an assignment simulation, a draft-outcome analysis, or an estimate of underlying talent assortativity.

## The answer in ordinary language

Removing the 339 players who averaged fewer than five minutes in games where they logged positive minutes raised the observed points-per-minute sorting index from **0.0619 to 0.0713**. At first glance, that looks like more sorting. But random allocation within each group's own fixed team slots also has a higher expected index after the population shrinks: its simulated mean rose from **0.0820 to 0.0893**. Relative to each population's own random reference, the increase was only **0.0021**.

Both observed indices were *below* the lower end of their respective 1,000-shuffle reference ranges. Thus this particular five-minute rule does **not** reveal strong across-team sorting of measured points per minute that was hidden by brief-playing roster members. That is a statement about this performance measure and this constructed population. It does not say players lack underlying talent differences or that Division I teams are assigned at random.

## Precisely what we calculated

The **sorting index** ($H_{\mathrm{sort}}$) is the share of player-to-player points-per-minute variation that lies between team means:

$$
H_{\mathrm{sort}}
= 1-\frac{\sum_i (p_i-\bar p_{g(i)})^2}
         {\sum_i (p_i-\bar p)^2}.
$$

Here $p_i$ is player $i$'s accepted 2015 season points per minute; $g(i)$ is that player's accepted team; $\bar p_{g(i)}$ is the mean among the included players on that team; and $\bar p$ is the mean of all included players. Each player has one vote in the index, regardless of playing time. A common standardization of the same population's points per minute would leave the index unchanged. The direct calculation exactly matched `sports/541_grandchild_homophily_assign.py` (`realized_sorting_index_H_sort`) and `sports/scripts/pd21_rho_hsort_calibrate.py` (`empirical_h_sort`) for both groups.

The **full group** is all 4,267 eligible players on 351 teams from the previously verified rotation audit. The **regular-playing group** is the 3,928 of those players averaging at least five minutes per positive-minute appearance, with the same individual points-per-minute values and team labels. No new game data were read, and no score or team assignment was changed. All 351 teams remained represented, with at least eight regular-playing players per team.

For each group separately, we held its player values and exact team sizes fixed and uniformly shuffled values among team slots 1,000 times. This creates a **random-allocation reference**, not a fitted model of basketball recruiting or a confidence interval for all seasons. For $J$ nonempty teams and $N$ players, its mathematical expected index is $(J-1)/(N-1)$; each simulated mean agreed with that benchmark.

| Group | Players; teams | Team-size range | Observed $H_{\mathrm{sort}}$ | Random mean | Random 2.5th–97.5th percentile | Observed minus random mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Full eligible population | 4,267; 351 | 9–18 | 0.06194 | 0.08203 | 0.07085–0.09305 | −0.02009 |
| Regular-playing population | 3,928; 351 | 8–17 | 0.07127 | 0.08929 | 0.07708–0.10206 | −0.01803 |

The **raw change** from full to regular-playing is $0.07127-0.06194=+0.00932$. The random-reference mean itself changes by $0.08929-0.08203=+0.00726$ because this is a smaller population with the same 351 teams. Therefore the **reference-adjusted descriptive change** is

$$
(0.07127-0.08929)-(0.06194-0.08203)=+0.00206.
$$

These rounded substitutions reproduce the unrounded result approximately; the [saved summary](../../outputs/sorting_sensitivity_2015/ASSORT_20260927_sorting_sensitivity_v1_summary.json) carries full precision. The 2.5th–97.5th percentile range describes repeated *random reallocations conditional on these measured players and team capacities*. It is not a confidence interval for the difference between the two overlapping populations. We did not run a formal nested-sample difference test.

## Why we asked, and what we learned next

First, we rebuilt the 2015 player population from the frozen game records, checked anomalous minutes against game-specific sources, and fixed the canonical-team rule. That produced an auditable 4,267-player population. Next, the [rotation and measured-peer audit](ASSORT_20260927_rotation_audit_v1_report.md) found that 339 brief-playing players supplied only 0.672% of captured eligible minutes yet changed about 60% of measured peer averages when omitted from the peer calculation. The mean peer average rose by 0.071 season-wide standardized points-per-minute units. This told us that the *peer axis* depends on who is counted; it could not tell us whether team rosters themselves are more sorted.

So we next changed the *population entering the sorting calculation*: all eligible players versus those meeting the fixed five-minute rule. The raw sorting index rose. But the random reference rose almost as much, and both observed indices stayed below their reference ranges. This tells us that excluding brief participants at this one preselected threshold yields only a small reference-adjusted increase in measured points-per-minute sorting. It does **not** explain why the measured index is low, establish whether players are matched by latent talent, show that brief participants are untalented, or test whether congestion affects draft selection. Points per minute may reflect role, defensive specialization, coaching, pace, and opportunity as well as talent.

The old index near 0.061 came from a different historical panel. Its numerical similarity to the new full-group 0.06194 does not make the populations or construction rules interchangeable. We did not reuse its model fits, historical shuffles, or generated data.

## Provenance and stop point

The comparison used the [saved player audit](../../outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz) only after its SHA-256 checksum matched the [prior audit run record](../run_records/ASSORT_20260927_rotation_audit_v1_run_record.json). The isolated [driver](../../code/ASSORT_20260927_sorting_sensitivity_v1.py) checked player counts, uniqueness, points-per-minute arithmetic, and five-minute indicators before calculation. Its observed index matched both repository functions exactly. The saved [summary](../../outputs/sorting_sensitivity_2015/ASSORT_20260927_sorting_sensitivity_v1_summary.json) and [2,000 individual shuffled values](../../outputs/sorting_sensitivity_2015/ASSORT_20260927_sorting_sensitivity_v1_random_draws.csv) have file hashes in the [run record](../run_records/ASSORT_20260927_sorting_sensitivity_v1_run_record.json). Those hashes were checked after the run, and the shuffle file contains exactly 1,000 records for each group.

We stopped at this one comparison. We did not move the five-minute threshold, fit the assignment-preference parameter, redraw the draft curve, or resume the paused assortativity experiment. The result is ready for Charles's interpretation before any next test is designed.
