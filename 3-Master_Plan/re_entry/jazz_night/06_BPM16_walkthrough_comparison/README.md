# BPM 16-bin comparison — walkthrough only

Created 27 October 2026. See Section 12 of [the experimental walkthrough](../Jazz_Night_Experimental_Walkthrough.md) for the question, findings, and return point.

- [Quantile plot](naive_BPM_Q16_available_2011_2021.png)
- [Equal-width plot](naive_BPM_EW16_available_2011_2021.png)
- [Same-scale comparison](naive_BPM_Q16_vs_EW16_same_scale.png)

Requested source window: 2009–2021. Available BPM window: 2011–2021. All colleges, MG10 (>10 captured team games), ≥20 total season minutes, final eligible player record; outcome ever drafted. N=19,289; 510 drafted. No replacement of missing final BPM with earlier-season values.

`Q16_bin_counts.csv` and `EW16_bin_counts.csv` retain rates, counts, full Wilson interval endpoints and performance ranges. Membership, missing-final-record and coverage files make exclusions explicit. `provenance.json` records frozen source hashes and rules. `build_bpm.py` reproduces the figures from the saved source snapshots. `validation.txt` records the completed checks.

Both displays retain all observed rates and use a 0–50% y-axis. Intervals above the display limit have upward arrows. No source data, notebook, locked PPM artifact, or JN_progression.md was changed.
