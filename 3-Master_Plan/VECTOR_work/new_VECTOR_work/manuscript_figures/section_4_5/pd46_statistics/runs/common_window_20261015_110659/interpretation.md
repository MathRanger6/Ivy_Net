# Common-window check: Panels 7 and 8, 2009-2021

## Comparability decision before testing

The saved ESPN box source and the same athlete-ID draft lookup feed all seasons. Performance is points per minute, standardized within season; teammate averages exclude the focal player. The legacy game filter actually requires more than 10 distinct games, not at least 10. Player minutes must be at least 20. No definitions were changed for this extension.

The early seasons have comparable internal coverage to adjacent years: 2009 and 2010 have 345 and 347 eligible teams, compared with 345 in 2011 and 2012. Median recorded games per eligible team are 31,31,31,32. Eligible player-team-season counts are 4093,4183,4086,4097. Raw missing points/minutes rates are about 24-25% in these years; these are game-row diagnostics, not percentages of missing eligible players, and were not presumed to establish completeness. Raw median points per minute is about 0.293-0.297 across these four seasons. No duplicated game/team/player keys were found in 2009-2013. Later years have their own imperfections, including some duplicate keys and reduced 2021 game coverage. No early-year discontinuity in these checks warrants excluding 2009-2010 from this exploratory comparison.

This does not independently validate every historical schedule, identity match, or draft label. It supports internal measurement/coverage comparability rather than proving exchangeable cohorts.

## Rules preserved

Panel 7 retains z scores 2-3, not an own-performance percentile band. Panel 8 recalculates the pooled top-7% cutoff: 1.4997377331260051 rather than 1.4935605333531061 in 2011-2021. Each panel recalculates peer bins and the set of colleges represented by an ever-drafted player within the window. These changes follow the original definitions. The longer-window original bin totals were reproduced exactly from previously saved comparison artifacts.

Highest-rate pre-tail bin is selected, ties resolved by lowest bin number. Each pre-tail bin versus the same final two pooled bins forms the correction family: 14 comparisons in Panel 7, nine in Panel 8. This is not a frozen-bin comparison and not a test only of the earlier upper-peer local peak. All comparisons are saved. It also does not harmonize the all-season and college restrictions with Panel 9's final-season/all-college population.

## Results

Panel 7: 534 rows. Peak bin 2 is 15/33 (45.45%); tail bins 15-16 are 16/66 (24.24%). Decline 21.21 percentage points. One-sided p-values: neither correction 0.0179; grouping only 0.0239; peak correction only 0.1721; both 0.2029.

Panel 8: 1546 rows. Peak bin 8 is 33/102 (32.35%); tail bins 10-11 are 12/64 (18.75%). Decline 13.60 percentage points. One-sided p-values: neither correction 0.0219; grouping only 0.0339; peak correction only 0.1005; both 0.1479.

Both observed declines remain, but neither meets 0.05 with the peak-search correction. The earlier Panel 8 result with both corrections (0.0081) is therefore sensitive to this expanded-window specification. More observations do not guarantee a smaller p-value because the rates, bin boundaries, eligible colleges and within-group dependence change. Keep both windows in the record, rather than selecting whichever is significant.

These approximate multiplier tests use 9999 draws and seed 46. They account only for the stated location family, not all historical choices of years, bands, panel and binning. Grouping OFF treats repeated player records independently. Grouping ON joins repeated players and colleges across years. Multiple-college records in one season remain source qualifications, recorded in provenance. Tail group support remains limited. This is exploratory evidence, not a causal test or proof of the whole curve shape.

## Panel 7 tied peaks

Bins 2 and 8 both have 15/33, so both are highest-rate bins. The automatic first-bin tie rule above chooses bin 2; it does not imply bin 8 ceased to be a peak. For transparency, the previously chosen bin 8 comparison is also saved in panel7_tied_peak_bin8_four_versions.csv. Its four one-sided p-values, in row order (neither, peak only, grouping only, both), are 0.0181, 0.1721, 0.0399, 0.2802. Neither tied-peak comparison passes the peak correction.
