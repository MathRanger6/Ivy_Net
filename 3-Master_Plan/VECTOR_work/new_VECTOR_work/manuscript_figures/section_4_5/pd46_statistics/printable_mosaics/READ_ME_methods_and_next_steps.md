# Printable comparisons

Print ALL_FOUR_printable_mosaics.pdf: four landscape US-letter pages. Individual PDF and high-resolution PNG versions are alongside it. Original figures and statistical results are untouched.

Rows: 2011-2021 then 2009-2021. Columns: LOO (self excluded), then T_j (self included). Two own-performance definitions, each shown with quantile and equal-width bins. All means are calculated on full eligible rosters before filtering own performance. Both axes are UNCLIPPED. This deliberately differs from the historical winsorized LOO curves. Quantile boundaries are recalculated in each panel; EW boundaries are common across the four panels of each mosaic. No coarse/fine binning in this set. All four mosaics have matching display axes.

## Squid and Jackal source definitions

sports/scripts/pass_a_congestion_conditional.py defines SQUID_VENT_16=(5,6,7) and JACKAL_VENT_16=(13,14,15), zero-indexed, corresponding to displayed bins 6-8 and 14-16. _pool_summary pools positive rows and total rows before calculating the rate. These are proxies within a matched own-performance band, not permanent player identities. The new quantile mosaics apply those region definitions descriptively to both axes and performance bands. On EW plots, shaded bands show the minimum-to-maximum peer scores of those same quantile-defined groups. Green denotes Squid and orange denotes Jackal. Counts and rates below the plots retain exact quantile membership, not overlapping EW-bin membership. Each range is recomputed for its own window, performance band, and peer measure. Shading cannot distinguish members from nonmembers sharing a tied boundary score; an EW point may pool observations inside and outside a shaded range. Exact extents and group counts are saved in squid_jackal_score_ranges.csv.

The original Panel 8 mixed-width version uses four lower and seven upper intervals. Its orange color labels finer upper-region bins, not the original Panel 7 Jackal category. Compression means fewer wider lower intervals, not deletion of the lower observations. Historical source figures remain available separately.

## DO NOT FORGET: compare quantile tie handling later

Charles explicitly requested the original rank-first quantile method on October 15, 2026. Equal x values may be split across bins according to existing row order to keep counts nearly equal. Later compare this with tie-preserving quantiles, particularly for T_j where teammates share the same value. Do not silently substitute the alternative. The task is recorded here and in notebook Section 4G.

## Limits

These are descriptive plots with unchanged own-score and population definitions. Repeated player-team-seasons are observations; outcomes are ever-drafted labels, not annual selection. No new significance tests were run. The within-window college restriction is outcome based. Data identity and historical coverage qualifications from the preceding audits still apply.
