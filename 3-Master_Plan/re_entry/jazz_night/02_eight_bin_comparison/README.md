# Jazz night: eight bins, then PPM

**Date:** 27 October 2026.  
**Requested sequence:** First reduce BPM from 12 to 8 bins; then switch the eight-bin plots to PPM. Charles indicated a preference to continue with PPM. This preference is recorded here; the existing notebooks and manuscript have not been switched or edited.

## 1. BPM, eight bins

[Open equal-width and quantile plots](bpm_8bins/naive_BPM_EW8_vs_Q8.png).

The cohort is unchanged from the first Jazz night plot: 19,289 players, 510 ever drafted. Only the number of bins changes. Eight equal-width bins still leave a sparse upper tail: bin 7 contains 7 drafted out of 31 players, and bin 8 contains 0 out of 2. The highest quantile bin contains 463 drafted out of 2,411 players (19.2%). With eight quantile bins, each bin represents approximately 12.5% of the cohort; this highest bin is not a narrow superstar band.

## 2. PPM, eight bins

[Open equal-width and quantile plots](ppm_8bins/naive_PPM_EW8_vs_Q8.png).

PPM means points per minute. It is standardized within season using the eligible full roster mean and sample standard deviation, before selecting the final-observed-season rows. The reconstructed values match the historical saved PPM values.

The same eligibility rules yield 19,803 players and 520 ever drafted. PPM is available for 514 players whose final observed row lacks BPM; 10 of these additional players were ever drafted. They are included here, so this is the requested change of metric with all available eligible observations, not a strict matched-player comparison isolating only the metric.

The PPM quantile rates rise from approximately zero in the lowest bins to 12.0% in the highest bin (297 of 2,475). The populated equal-width bins also show rising rates through bin 7. The final bin contains one player and no draft, so its drop should not be interpreted as established evidence of a downturn. The second-highest EW bin has 18 players and four drafts. The two plot types summarize the same observations at different numerical resolutions; neither is an exponential fit.

## Settings retained

- 2011–2021; all colleges; one saved final observed season per player.
- MG10: more than 10 team games. Minimum 20 total recorded season minutes, not minutes per game.
- Observed outcome: ever drafted, not necessarily selected in the plotted season. The final observed season may be the 2021 data boundary rather than the end of a career.
- Season-standardized own performance on the horizontal axis; bin ranges printed below categorical bin positions.
- Eight equal-width bins spanning the full range, and eight nearly equal-count quantile bins. Quantile ties are split in stable source order without using outcomes.
- Counts and pointwise 95% Wilson intervals, without college-clustering adjustment. Full range retained; no clipping, compression, or extra minutes filter. All four panels use the same 0–35% vertical scale, with observed percentages labeled above the bars. Upward triangles mark confidence intervals extending beyond 35%; their full values remain in the bin-count CSV files.
- No fitted parameters, simulated selection, significance tests, or congestion calculation in these plots.

## Saved records

Each metric subfolder contains the combined comparison, separate EW and Q PNGs, bin counts, exact player membership, season totals, split-tie records, provenance and validation results. The original 12-bin BPM files remain in the parent folder.

The shared build script reconstructs standardization from the fingerprint-verified frozen sources, checks identities and outcome labels, and verifies that both binnings account for every player and draft. Running it with `--metric BPM` or `--metric PPM` regenerates that metric's subfolder. The source snapshots and original notebooks are unchanged.

**Next discussion:** Inspect PPM together before deciding on the next model comparison or additional filtering. The smoother appearance of a particular binning alone does not establish which performance measure best predicts selection.

## Display refinement: 27 October 2026

At Charles’s request, reduced the shared vertical scale to 0–35% to make the observed rates visible, and added percentage labels. No observations, bin definitions, rates, counts, or uncertainty calculations changed. The earlier full-scale images are retained in `display_before_zoom/`.
