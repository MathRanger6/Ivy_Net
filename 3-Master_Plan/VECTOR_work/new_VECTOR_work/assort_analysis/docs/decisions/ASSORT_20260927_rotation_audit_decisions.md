# 2015 basketball rotation audit: decisions and reasons

**Status:** Working decision record. The rotation audit has not been run. The earlier assortativity simulation remains paused. This record distinguishes choices Charles has accepted from questions still open; it does not change the production basketball panel or any earlier empirical result.

## Purpose and fixed context

The bounded audit asks whether a team's measured peer environment is sensitive to including teammates who saw very little court time. It is a diagnostic of the *measured player pool*, not a new estimate of latent talent, an experiment establishing causation, or a search for a more attractive draft curve. The intended starting point is the named 2015 population and source rules in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260925_construction_specification_and_source_audit.md`. A fresh source build must be explicit; an old exported panel is not silently substituted.

## Accepted decisions

### Verify missing game minutes before excluding rows

**Charles's decision:** Seek game-specific source minutes for the six affected games. If a player's minutes cannot be independently matched, exclude both that row's points and minutes from this new audit. Do not carry its points forward with a missing minute denominator.

**Reason:** The frozen game file recorded points but lacked minutes for 105 player-game rows. Retaining the points alone would distort a points-per-minute rate; automatically dropping all 105 rows could discard real playing time. The bounded source recovery matched all 105 rows by game, team, player name, and points. It found 101 positive-minute appearances and four zero-minute, zero-point rows. The row-level evidence, two explicit name aliases, source snapshots, and source limitations are in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260927_six_game_minutes_source_recovery.md` and `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/data/source_recovery_2015/minutes_recovery_overlay.csv`. This overlay is isolated and has not been applied to the frozen file or a rebuilt panel.

### Define minutes per appearance using games with positive minutes

**Charles's decision (September 27):** For each player, define a *played appearance* as a distinct captured game in which verified player minutes are greater than zero. Define **minutes per played appearance** as total verified captured minutes divided by the number of those appearances. Report the appearance count separately. Also report the team's captured-game count separately; it is not the denominator of this particular rate.

**Example:** A player with 40 captured minutes over four games with positive playing time on a team with ten captured games has 10 minutes per played appearance and four appearances. Dividing by all ten team games would produce four minutes per team game, a different measure that mixes playing time when used with whether the player appeared at all.

**Reason:** The immediate question is how much court time a player received *when the player played*. Reporting appearance count alongside the average prevents the same average from hiding very different participation histories. A zero-minute, zero-point row is not a played appearance. An unmatched row subject to the agreed exclusion fallback contributes neither minutes nor an appearance. The captured-game count is a property of the available data, not proof of full-season coverage. This is a descriptive audit definition, not yet an eligibility rule or a judgment that players below any threshold were unimportant competitors.

### Hold focal players fixed in the peer-pool comparison

**Charles's decision (September 27):** Use the same focal player-season observations in both versions of the comparison. Keep each focal player's recorded points-per-minute value, team assignment, and draft outcome fixed. Compute that player's leave-one-out peer average first from the current eligible teammate pool, then from the teammates who meet the provisional playing-time criterion. Exclude the focal player from their own peer average in both versions, whether or not that player meets the provisional criterion.

**Reason:** This isolates the consequence of describing the *peer pool* differently. If we simultaneously remove low-minute focal players, changes in the curve could arise from changing the population of players being plotted rather than changing their peer measure. This comparison alone does not re-estimate the sorting index, because it holds player abilities and team assignments fixed.

### Start the restricted peer pool at five minutes per played appearance

**Charles's decision (September 27):** For the first restricted-peer comparison, include teammates whose total verified captured minutes divided by their number of positive-minute appearances is **at least five minutes**. A player averaging exactly five minutes qualifies. This threshold changes who contributes to the restricted peer average; it does not remove low-minute focal players from the fixed comparison population or alter the underlying production eligibility rule.

**Reason:** Five minutes is the simple provisional value raised in Charles's question about brief appearances. It lets us inspect whether very limited court exposure is affecting the measured peer pool while preserving the existing focal observations. For example, 40 minutes in four played appearances qualifies; 16 minutes in four does not. We must also report how many teammates each focal player retains and how much of the team's captured playing time the retained group accounts for. The threshold does not establish latent ability or whether a player competed for minutes.

**Incremental option:** Charles wants the ability to raise the threshold if the initial audit shows that five minutes does not adequately separate brief appearances from the regular playing group. The first run uses five minutes alone. Any higher threshold, increment, and stopping point should be chosen and recorded after inspecting the initial descriptive counts, before a follow-up run. This avoids automatically searching thresholds for a preferred outcome curve. No higher value has yet been selected.

### Retain one-person peer averages; mark zero-person averages missing

**Charles's decision (September 27):** If exactly one teammate meets the five-minute criterion, calculate the restricted leave-one-out peer average from that one teammate and report that its peer count is one. If no teammate qualifies, leave the restricted peer average missing and count that focal observation explicitly. Do not replace a missing peer average with zero or remove the focal player from the audit roster.

**Reason:** A one-person mean is mathematically defined, but it is a fragile description of a broader peer environment. Showing its count makes that limitation visible. An additional minimum-peer exclusion would change which focal players can be compared and add another arbitrary threshold. A zero-person mean has no mathematical value.

### Limit the first audit to playing time and peer averages

**Charles's decision (September 27):** In the first pass, report the 2015 playing-time patterns and the paired full-pool versus five-minute restricted-pool peer averages for the same focal players. Do not draw a new draft-outcome curve in this pass. Count any focal observations with zero or one qualifying peer rather than assuming those cases are present or absent. Charles expects such cases to be rare, but that is an empirical expectation to check.

**Reason:** This directly tests whether brief appearances materially change the *measured peer axis* before introducing a second outcome-curve interpretation. It keeps the first audit small and makes the next decision depend on observed counts and paired changes.

### Choose canonical team using games with actual playing time

**Charles's decision (September 27):** For this 2015 audit, assign an athlete who appears on multiple teams to the team with the most distinct games in which the athlete has positive, verified minutes. Break a tie with the athlete's total verified minutes on each team; stop for review if both measures tie for a potentially eligible athlete. Preserve the former all-captured-game choice for comparison. Record the incidence of changed team assignments across all affected athletes, including those whose old choice had zero minutes. No-play roster listings do not outrank observed playing appearances.

**Reason:** The saved first-build audit showed that the prior rule could select a zero-minute roster listing over a team where the athlete actually played. That dropped three athletes with at least twenty recorded minutes from the otherwise eligible population. The new ordering aligns the canonical team with observed playing time while retaining a single team per athlete. The numerical incidence and any other changes must be measured from the full set of multi-team athletes; the three known examples are not assumed to be the total.

### Exclude unresolved positive-point, zero-minute rows from the new audit

**Charles's decision (September 27):** Apply the previously accepted missing-minute fallback to the 22 positive-point, zero-minute game rows for which a positive minute value could not be verified. In this audit's *working copy only*, omit both those rows' 42 points and their zero minutes from season point and minute totals. Preserve their game identifiers for the previously settled team-season coverage count, but do not count them as played appearances. Keep the 15 rows for which independent game boxes supplied positive minutes, and retain every row's original values and source status in the isolated audit files. Do not alter the frozen game file or historical analyses.

**Reason:** A zero-minute denominator paired with positive points can distort a season points-per-minute rate. The independent source also reports zero minutes for 16 rows; six other player names were not found in the expected source team box. None has a verified positive numerical minute value. Excluding both statistics from the *new* construction is more defensible than inventing minutes or retaining points without minutes. The fraction of total source rows and the fraction of eligible players affected must be reported, because a small row fraction can still matter for those players. Source: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260927_zero_minute_positive_point_source_stop.md`.

## Remaining execution checks

- Verify source-row identity, six-game overlay matches, and the accepted 2015 construction filters before reporting a final number.
- Report population, team, and peer-count denominators alongside the summaries; count zero- and one-peer cases explicitly.
- Keep this audit's source build, code, and outputs isolated inside `assort_analysis`. Do not overwrite the frozen box file, saved panel exports, prior figures, or the paused simulation outputs.
