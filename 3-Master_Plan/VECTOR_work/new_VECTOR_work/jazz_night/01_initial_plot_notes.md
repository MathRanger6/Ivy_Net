# Jazz night: figures and evidence record

**Started:** 27 October 2026.  
**Companion outline:** [Jazz_night.md](history/Original_Jazz_Night_Outline.md).

## Step 1: the empirical naïve plot

**Question:** How does observed draft frequency vary with a player's own performance?

Charles requested 2011–2021, MG10, min=20, and 12 bins using both equal-width (EW) and quantile (Q) binning. We carried forward BPM (box plus/minus), standardized within season, and the existing all-college final-observed-season cohort. This retains the population used in our recent BPM investigation while changing the plotted axis to own performance and the number of bins to 12. There is no high-performance-band restriction here.

**Open the comparison:** [EW and Q together](01_naive_BPM_EW12_vs_Q12.png).

Individual high-resolution images:

- [12 equal-width bins](01_naive_BPM_2011_2021_MG10_min20_EW12.png)
- [12 quantile bins](01_naive_BPM_2011_2021_MG10_min20_Q12.png)

## Exactly who and what are plotted

- 19,289 distinct players; one saved final observed season per player, 2011–2021. All eligible colleges are included, not only colleges with a draftee.
- 510 players are labeled ever drafted, an overall rate of 2.64%. This is an observed fraction, not an annual draft quota or a same-season outcome.
- MG10 retains team-seasons with more than 10 games. The inherited min=20 filter means at least 20 **total recorded season minutes**, not 20 minutes per game.
- The horizontal measure is BPM standardized using each season's mean and sample standard deviation on the full eligible roster with finite BPM, before restricting to final-season candidates.
- A bar estimates P(Y = 1 | own performance lies in that bin) using drafted players divided by all players in that bin. Player and drafted counts appear below each chart.
- Error bars are pointwise 95% Wilson binomial intervals. They use a working independence assumption; they are neither college-cluster-adjusted nor simultaneous intervals. No significance comparison has been performed.

## Binning choices

EW divides the full observed BPM z-score range into 12 intervals of identical numerical width. The first interval includes the minimum; subsequent intervals are open on the left and closed on the right. Empty intervals remain visible and have no estimated rate or interval.

Q ranks players by BPM z-score and divides them into 12 nearly equal-sized groups. Ties are split in the fixed source-row order, consistent with Charles's earlier decision. Outcome labels never determine the order. Because tied values can cross a bin boundary, numerical ranges can touch or overlap. The exact assignments are saved.

Both plots use categorical bin positions with the numerical ranges printed below them. The equal visual widths of the Q bars do not mean equal numerical widths. Both use the same 0–100% probability scale. There is no winsorization, clipping, tail compression, or omitted performance region in these plots. Hatching marks bins containing fewer than 30 players; it does not remove them.

## Interpretation limits carried forward

**First observations from this run:** The highest quantile bin contains 1,607 players, of whom 410 were ever drafted (25.5%). The preceding bin contains 1,607 players with 76 drafted (4.7%). With 12 quantile bins, the highest bin spans approximately the top 8.33%, so it does not isolate our narrower top 2% band.

The EW range extends from -12.75 to 8.55 BPM z-score units. EW bins 1, 2, 3, 11 and 12 each contain just one player. The two populated high-performance bins contain 390 drafted out of 1,383 (28.2%) and 7 out of 31 (22.6%). The last two bins each have zero drafted out of one. Those very small counts do not establish a downturn. Across the complete cohort, 3,428 players have fewer than 100 recorded season minutes; the requested 20-minute minimum remains unchanged.

“Final season” is the last observed season in the source window, not necessarily the final season of a player's career. In particular, players active at the 2021 boundary remain in this cohort. Missing BPM on a saved final row leads to exclusion; we do not substitute an earlier available season. The source pool was originally assembled through the existing PPM pipeline before its available BPM was used, so this is the inherited comparison cohort, not an independently rebuilt BPM population.

The low minutes cutoff is retained exactly as requested. Large positive or negative BPM values among low-exposure players can influence the horizontal range; no additional exposure screen was silently imposed. The two binnings show the consequences of those choices. This step does not fit an exponential curve, select a BOE, introduce theta or gamma, or simulate winners.

## Reproducibility and checks

- [Bin rates, counts, ranges and intervals](naive_bin_counts.csv)
- [Season counts](naive_counts_by_season.csv)
- [Exact player membership in both binnings](naive_candidate_membership.csv.gz)
- [Quantile ties split across bins](quantile_split_ties.csv)
- [Settings and source fingerprints](provenance.json)
- [Validation record](validation.txt)

The build script reads the saved October 25 candidate snapshot and verifies its identities, outcomes and BPM standardization against the fingerprint-checked frozen roster sources. Each binning must account for all 19,289 players and all 510 drafted players. Q counts must differ by at most one player. The same local script can regenerate the figures; it does not fetch data or modify the manuscript, notebooks, or original sources.

**Next discussion:** Inspect the naïve plot together before choosing the next comparison. Creating this first plot does not authorize fitting temperature, new performance filters, or a congestion sweep.


## Comparison 03 — PPM, all-PS versus final-PS (27 October 2026)

[Read the comparison and view the plots](03_ppm_all_vs_final_ps/README.md). Same PPM definition, 2011–2021, MG10, minimum 20 season minutes and eight bins. Both views contain 19,803 unique players; final-PS has 19,803 records and all-PS has 46,306 records. The notes explain repeated outcome labels, quantile boundary changes and uncertainty limitations. Earlier products remain the baseline; no manuscript or notebook changes.
