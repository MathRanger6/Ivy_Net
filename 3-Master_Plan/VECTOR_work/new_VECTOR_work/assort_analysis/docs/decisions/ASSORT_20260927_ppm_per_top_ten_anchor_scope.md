# PPM and PER: fixed top-ten-minute anchors and a matched-size reference

**Date:** September 27, 2026  
**Authorization:** Charles instructed, “lets apply the ten minute anchor comparison to ppm and per.” In the immediately preceding discussion, the proposed contrast was the ten players with the highest total season minutes per team. VECTOR uses that existing definition; this is not a ten-minutes-per-game rule.

## Question and rationale

The earlier playing-time comparisons were conditional on season points per minute (PPM). Their results do not establish that the same player-pool definitions are uninformative for Player Efficiency Rating (PER). This bounded comparison asks whether the already defined top-ten-minute anchors change PER team intervals and measured sorting differently from PPM. It does not search for the best filter, optimize sorting, or change which players can compete in a later model.

## Fixed identities and source boundary

Start with the accepted 4,267-player, 351-team 2015 rotation-audit file and verify its checksum. Reconstruct the original anchors by descending total verified season minutes and ascending player identifier for ties; use all players on teams with fewer than ten. Verify those identifiers against SCOUT's saved version-two high-minute selections. Freeze this definition before using PER availability or either performance value.

Join the saved Sports-Reference PER column by player, season, and team. Both measures will be compared on players with finite PER and PPM. A finite BPM is unnecessary for this two-measure question; this deliberately includes the two players with usable PER but missing BPM excluded from the previous three-measure comparison. Record the resulting population and excluded teams.

For the anchor condition, intersect the original anchors with the common two-measure population. **Do not replace unavailable anchors with the next highest-minute player.** Report lost anchors and effective per-team counts. Stop if a team present in the comparison population has zero available anchors. The original full player file and its competition-pool status remain intact.

## Three cases for each measure

1. All players in the common PPM/PER population.
2. Original top-ten-minute anchors with available PER, using the same identities for both measures.
3. One hundred fresh within-team random subsets. For each team, draw without replacement exactly as many players as the available fixed anchors. Thus every random subset has the anchor condition's team counts and total count. Use master seed `20260927`, sorted teams, sorted player identifiers, and record NumPy's generator implementation. Use the **same selected identities** for both measures and for every statistic within a repetition. These are random subsets, not random reassignments between teams.

Each measure is standardized once using the full common two-measure population mean and population standard deviation. Hold that reference fixed for anchors and random subsets, so width changes do not partly arise from restandardizing each subset.

## Calculations and checks

For each case, calculate the overall sorting index ($H_{\mathrm{sort}}$), standardized team minimum-to-maximum intervals, equal-team mean width, and coverage counts on a fixed grid. The sorting index is the equal-player fraction of total variation accounted for by team means; cross-check its between/total and one-minus-within/total expressions. Confirm identical identities across measures, exact matched counts for random subsets, fixed scale, subset containment, and no changes in source hashes.

Use a common grid spanning both full-population standardized measures for the comparison figure. Summarize random widths as the mean of the 100 repetition-level mean widths, not the mean of team-wise medians. Summarize random sorting indices with mean, median, range, and the number at or above the fixed-anchor result. Coverage plots may use pointwise medians and central 80% repetition ranges; label them literally. The count among 100 draws is descriptive and is not a population-level causal or inferential p-value.

## Interpretation and stopping point

An anchor change larger than the matched-size reference supports an association between playing-time-based selection and measured team distributions for that measure. An increase in sorting that is also produced by random subsets may reflect subset size rather than the minutes criterion. Neither outcome proves latent talent, selective recruiting, or congestion. PER and PPM use different source constructions; prior source-minute and matching-lineage qualifications remain.

Keep new code, numerical outputs, figure, report, and execution record under `assort_analysis/`, using a distinct `ppm_per_top_ten_anchor_2015` output folder. Do not modify prior data, plots, pipeline code, or research artifacts. No additional anchor sizes, thresholds, seasons, metrics, draft curves, calibration, or simulations are authorized by this comparison. Report before proceeding.
