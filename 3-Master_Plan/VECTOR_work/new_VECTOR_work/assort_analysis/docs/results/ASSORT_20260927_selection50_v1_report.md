# At 50% selection, a clear EW downturn is available at lambda eight

**Last synced:** 2026-09-27  
**Status:** Exploratory model sweep completed; rho 0.6 fallback not needed or executed.

Charles asked whether a curve resembling the 2015 10%-selection, lambda-four reference could be produced at 50% selection while retaining rho one. We paused the lower-selection-rate discussion and tested lambda 0, 1, 2, 4, 8, and 16 on the same 100 saved assignments in each of 2014, 2015, and 2016.

The only changes from the reference were the number selected and the congestion multiplier. Player performance, congestion construction, teams, EW edges, quantile memberships, and deterministic ranking remained unchanged. Exact 50% counts were 2,124 of 4,248 (2014), 2,134 of 4,267 (2015, rounded upward), and 2,117 of 4,234 (2016). No Army data were analyzed: 50% was a model scenario inspired by Charles's comparison, not an independently verified Army selection rate.

## What we see

**Lambda eight is a useful visual candidate at rho one.** EW curves rise and then fall in all three seasons. Lambda four already produces a downturn, but eight produces a more pronounced descending side. Sixteen moves the peak farther left and suppresses more of the upper region; it is not required just to establish a downturn.

For the 2015 comparison, the 10% reference peaks near EW bin 12 at 32.3%, then reaches about 27.8% in bin 14 and 11.9% in bin 15. At 50% and lambda eight, the peak is near bin 11 at 76.1%, followed by 73.9%, 63.8%, 47.2%, and 18.9% in bins 12–15. Thus the general rise-and-fall pattern is present, but its peak, width, and heights are not identical.

At 50% and lambda four, the 2015 peak is 82.4% near bin 12, with 77.9% in bin 14 and 64.6% in bin 15. Showing this intermediate candidate makes clear why eight was highlighted: the decline extends more visibly across the upper region rather than being concentrated in the last bar.

Eight is a visual candidate from the displayed grid, not an optimized coefficient, the uniquely correct match, or an empirical estimate. There was no automatic threshold. Charles should judge whether this is the resemblance intended.

## Important interpretation

A curve whose player-weighted average is 50% cannot match the actual heights of one averaging 10%. Indeed, even after dividing by the overall selection rate, the maximum possible relative rate at 50% is two, whereas the reference peak exceeds three times its 10% overall rate. Exact relative-profile matching is therefore impossible here. Similarity refers to the rise-and-fall form, not mathematical equality.

This exercise changed both selection fraction and penalty relative to the reference. It demonstrates an available model configuration, not the isolated causal effect of changing selection fraction. The earlier fixed-lambda scarcity experiment remains a separate result and is not superseded.

The far-right EW bins are still sparse. In 2015, bins 12–16 average approximately 95, 32, 11, 2.4, and 0.26 players per assignment. The zero last-bin bar at lambda eight should not drive the interpretation. At 50%, even lambda zero has small far-tail irregularities in some seasons; a tiny isolated last-bin decline by itself is not unique evidence of congestion.

## See the comparison

![2015 reference and 50% candidates](../../outputs/selection50_v1/2015_reference_comparison.png){width=100%}

Full EW and quantile sweeps:

- [2014](../../outputs/selection50_v1/2014_sweep.png)
- [2015](../../outputs/selection50_v1/2015_sweep.png)
- [2016](../../outputs/selection50_v1/2016_sweep.png)

## Verification and files

All 1,800 selected sets passed independent ranking checks and exact selection counts. The lambda-four 50% sets contained the corresponding prior 10% sets. Both binning methods accounted for all players and winners. Input hashes were unchanged. The script ran in sports_net; all sweep sheets and the comparison figure were visually inspected.

- [Specification](../decisions/ASSORT_20260927_selection50_v1_specification.md)
- [Sweep code](../../code/selection50_v1/ASSORT_20260927_selection50_v1.py)
- [Pooled counts and rates](../../outputs/selection50_v1/bar_summary.csv)
- [Per-assignment counts](../../outputs/selection50_v1/counts_by_repetition.csv)
- [Run record](../run_records/ASSORT_20260927_selection50_v1_run_record.json)

**Stopping point:** Demonstration available at rho one; rho 0.6 not run. No further scarcity experiments or PDF regeneration.

