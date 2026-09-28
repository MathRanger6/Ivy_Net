# 2015 men's basketball rotation and measured-peer audit

**Status:** Executed and internally checked on September 27, 2026. This is one bounded descriptive audit at a five-minute threshold. It is not a new draft-outcome curve, an estimate of assortative assignment, or a simulation result.

## The data question and the answer

The immediate question was whether the measured peer environment changes when teammates with very brief captured playing time are left out of the peer average. On the accepted 2015 construction, **339 of 4,267 eligible players (7.95%)** averaged fewer than five minutes per game in which they logged positive minutes. They accounted for only **0.672% of all captured minutes among eligible players**. At least one such player appeared on **213 of 351 teams**.

Keeping every focal player fixed, the five-minute rule changed the leave-one-out teammate ability average for **2,556 of 4,267 players (59.9%)**. The restricted average was **0.071 season-wide points-per-minute standard deviations higher on average**; the median change was zero, and the 90th percentile of the *absolute* change was 0.257. The full range of signed changes was −0.533 to +0.686. The minimum restricted peer count was **seven**. Thus Charles's expectation was confirmed at this threshold: **no focal player had zero or one qualifying peer**.

The positive average shift means that the players omitted by this *measured playing-time rule* tended to pull down the original measured peer average. It does **not** establish that those players had lower underlying talent, that the team assignment process lacked assortativity, or that congestion changed draft outcomes. Points per minute reflects scoring role and opportunity as well as ability. This audit did not draw a draft curve or recompute the sorting index.

## How much of the underlying data was affected by the source fallback?

The source review began with 37 player-game rows that recorded points but zero minutes. Independent game-specific box scores provided positive minutes for **15 rows** (115 points and 267 minutes), which were retained. They could not establish positive minutes for the remaining **22 rows**: 16 had the same zero-minute/positive-point pairing in the independent box, and six players were absent from the expected team table. Charles accepted omitting both recorded points and minutes for those 22 rows **only in this audit's working copy**. Their game identifiers still counted toward the previously accepted team-coverage rule. The frozen game file and historical results were not changed.

The size of that fallback depends on the denominator:

| Denominator | Affected amount | Fraction |
| --- | ---: | ---: |
| All frozen 2015 game rows | 22 of 182,657 rows | **0.0120%** |
| Game rows retained after this audit's coverage and canonical-team steps | 22 of 153,633 rows | **0.0143%** |
| Eligible players with at least one fallback row | 18 of 4,267 players | **0.422%** |
| Points in the full frozen 2015 game file | 42 of 797,355 points | **0.00527%** |
| Points for this audit's eligible players before the fallback | 33 of 771,946 points | **0.00427%** |

The row fraction is small, but the 18-player count is the more useful warning for an individual points-per-minute rate. The excluded points are concentrated in particular player seasons rather than spread evenly across all 4,267 players. The individual rows and source statuses are in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/data/source_recovery_2015/ASSORT_20260927_zero_minutes_recovery_overlay.csv`; the source reasoning is in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260927_zero_minute_positive_point_source_stop.md`.

## Canonical-team incidence and population

After the eleven-captured-game team-coverage rule, **85 athletes** appeared on more than one team; **76** had any recorded positive playing time. Applying the newly approved rule—most distinct games with positive verified minutes, then total verified minutes—changed **four of the 85** assignments relative to the earlier all-captured-game rule. Each changed assignment moved from a team with zero recorded minutes to a team with positive playing time:

| Athlete | Earlier choice | Playing-time choice | Captured minutes on new team | Eligible under new choice? |
| --- | --- | --- | ---: | --- |
| Sherron Dorsey-Walker | Oakland | Iowa State | 39 | Yes |
| Deonte Burton | Iowa State | Marquette | 129 | Yes |
| Schuyler Rimmer | Florida | Stanford | 6 | No; below twenty-minute floor |
| Semi Ojeleye | Southern Methodist | Duke | 63 | Yes |

The resulting population has **4,267 unique eligible athletes on 351 teams**. This explains the difference from the earlier stopped construction's 4,263: three athletes above return under the played-game team rule, and Tim Hasbargen crosses the twenty-minute floor when his verified Cleveland State minutes from the earlier six-game source recovery are included. The population was rebuilt from `datasets/mbb/mbb_df_player_box.csv`, not taken from a prior panel export. The complete candidate comparison is in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/data/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_canonical_team_candidates.csv`; the eight old/new candidate rows for the four changes are in the adjacent `..._canonical_team_changes.csv`.

## Precisely what was compared

For an eligible player, *minutes per played appearance* equals total verified captured minutes divided by distinct captured games with positive verified minutes. The first restricted peer pool includes teammates averaging **at least five minutes per played appearance**. A focal player's own standardized points-per-minute value, team, and place in the comparison remain fixed; the focal player is excluded from both versions of their own peer average. The unrestricted version uses all other eligible teammates. The restricted version uses only other eligible teammates meeting the five-minute rule. The ability standardization uses the final eligible 2015 population's mean and population standard deviation.

The saved player comparison records both peer counts, both averages, and the restricted-minus-unrestricted difference. A restricted average with one peer would have been retained and labeled; with zero peers it would have been missing. Neither occurred. The first pass deliberately did **not** vary the five-minute boundary, remove low-minute focal players, estimate a new sorting index, fit a quadratic, or construct a draft-outcome curve. If Charles later wants to raise the threshold incrementally, the next value and stopping rule should be recorded before a follow-up run rather than chosen from a favorable curve.

## Why the next question follows

First, we rebuilt the 2015 player population from frozen game records and checked anomalous minutes against game-specific box scores. That gave us a named, auditable population of 4,267 eligible players. Next, we counted who actually played at least five minutes per positive-minute appearance. The 339 players below that boundary supplied less than one percent of the eligible players' captured minutes, so a full-roster peer average gives them much more weight than their court time alone might suggest.

Next, we held every focal player fixed and changed only which teammates entered the peer average. The peer average changed for about 60 percent of focal players and rose by 0.071 standardized points-per-minute units on average. That told us the *measured peer axis* is sensitive to brief-playing teammates. It did **not** tell us whether the measured player values are more sorted across teams: the sorting index cannot change when its player values and team assignments are held fixed. It also told us nothing yet about the draft-outcome curve or a causal congestion mechanism.

So the next agreed scientific question is narrower than a new model campaign: with the five-minute boundary fixed, does the **sorting index of the observed player values** differ between the full 2015 population and the regular-playing subset, relative to a random-allocation reference for each population's own team sizes? The bounded proposed comparison is specified in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260927_sorting_sensitivity_plan.md`. Its result would tell us whether this *particular sample definition* changes measured sorting; even then, it would not identify underlying talent, coach decisions, congestion, or draft outcomes.

## Reproducibility and limits

The isolated driver is `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/ASSORT_20260927_rotation_audit_v1.py`. It reads the frozen game source through the existing version-one 2015 reader, validates both source-recovery overlays by original source-row identity, and writes its outputs only under `assort_analysis/`. It did not run the paused assignment experiment. The full parameter and file-hash record is `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json`; independent arithmetic and peer-average checks are recorded in the companion validation note. The primary results are `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_summary.json`, the adjacent compressed player comparison, and team summary.

The accepted eleven-game rule establishes a minimum *captured* schedule, not complete season coverage. Minutes per appearance and the five-minute criterion describe observed court time within that capture. A scorer on a strong team may have limited minutes for reasons besides ability; team offense, pace, opponent strength, position, injuries, and coaching choices remain unseparated. The measured peer shift is therefore a reason to examine the pool definition carefully, not a conclusion about the dissertation's causal mechanism or the high-tail outcome curve.
