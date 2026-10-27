# CURRENT JN-03 version 2 — Gibbs selection using original, unclipped scores

**Updated: 27 October 2026. Ready for review; not locked. No MLE fit.**

[View the current corrected figure](JN03_PPM_observed_topK_gibbs_Q16.png).

## What this is

Step 3 of the JN progression: observed PPM outcomes and deterministic top-K alongside simulated Gibbs inclusion. Same 22,795 players, 615 selections, Q16 bins, 2009–2021 final eligible records and within-season PPM scores. All nine temperatures, seeds and 12,000 repetitions per temperature are retained from version 1. The featured temperatures remain 0.25, 0.7 and 2.5.

## Why version 2 replaced version 1

The old shared selection wrapper changed negative scores to zero before computing exponential weights. The corrected local function preserves every original score, including negative values. The shared legacy helper remains unchanged. At temperature 0.7, the highest-bin rate is now 21.24%, previously 19.64%; the lowest-bin rate is 0.056%, previously 0.752%.

## Where the complete story lives

[Walkthrough Section 14](../Jazz_Night_Experimental_Walkthrough.md#14-we-introduced-stochastic-selection-then-corrected-a-score-clipping-mistake) shows both plots and explains the intent, mistake, correction, results and return point. [Progression Step 3](../JN_progression.md) shows only the corrected figure.

The folder [SUPERSEDED JN-03 v1 — scores clipped to zero](superseded_JN03_v1_scores_clipped_to_zero/START_HERE_SUPERSEDED.md) is a historical record, not another active analysis or recommended figure.

## Reproduction and evidence

- `build_gibbs.py`: corrected local implementation; reruns the same temperature grid.
- `gibbs_t_sweep_bin_rates.csv`: corrected bin inclusion estimates for all nine temperatures.
- `observed_topK_gibbs_bin_counts.csv`: displayed observed/top-K/Gibbs summaries.
- `player_gibbs_inclusion_by_t.csv.gz`: player-level inclusion estimates.
- `correction_before_after_bin_rates.csv`: all 144 matched old/new bin-temperature comparisons.
- `check_results.py`: independent comparison checks against the preserved v1 files.
- `provenance.json` and `validation.txt`: settings, hashes and completed checks.

Every repetition selects exactly 615 distinct candidates. Negative-score weight ordering, score-shift invariance, equal-score uniformity and an all-negative test pool were checked. This is still a pooled descriptive exercise; no annual draft reconstruction, fitting or significance test has been performed.
