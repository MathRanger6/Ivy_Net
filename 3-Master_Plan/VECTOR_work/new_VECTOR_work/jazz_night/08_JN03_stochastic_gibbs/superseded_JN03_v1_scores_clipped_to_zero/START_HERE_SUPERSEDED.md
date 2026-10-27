# SUPERSEDED JN-03 version 1 — negative scores were incorrectly changed to zero

**Why this folder exists:** This is the first stochastic-selection figure built on 27 October 2026. We preserved it so the research history remains intelligible. It is not a competing model recommendation and should not be used for the manuscript or temperature fitting.

**What went wrong:** The legacy shared selection routine replaced negative standardized PPM scores with zero before calculating Gibbs weights. This erased differences among 11,673 nonpositive-score players. The intended model retains the original score, including negative values.

**What replaced it:** Corrected JN-03 version 2, in the parent folder, uses unclipped scores. The same players, bins, K=615, temperature grid, 12,000 replicates per temperature and seeds were retained. The wider project’s shared selection routine was not modified.

**Where to read the story:** Walkthrough Section 14 shows the original and corrected plots, explains the cause, and records the numerical changes. The progression shows only the corrected figure. You do not need to inspect this archive to follow the manuscript story.

The files originally saved by SCOUT are preserved unchanged, including the original README, provenance and validation. Their claims describe the superseded run and do not override this correction. The two Markdown documents here are snapshots from before correction, not current documents. `SUPERSEDED_JN03_v1_negative_scores_changed_to_zero.png` is a clearly labeled rendering of the same saved v1 numbers; the original PNG is also retained unchanged.
