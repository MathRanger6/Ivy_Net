# JN-02: observed PPM outcomes versus deterministic top-K

Created 27 October 2026. **Ready for review; not locked.**

[View the figure](JN02_PPM_observed_vs_topK_Q16.png). A scalable SVG is also provided.

Use exactly JN-01’s 22,795 players, 2009–2021 final eligible records, PPM standardized within season and Q16 bins. All eligible colleges, >10 captured team games, ≥20 total season minutes. Outcome: ever drafted.

SCORE sets S_i=A_i. SELECT picks the highest 615 scores, matching the observed count of ever-drafted players. This is a single pooled descriptive comparison, not an annual draft reconstruction. Exact ties use source order, never outcomes; no boundary tie occurs here.

All benchmark selections are in bin 16: 615/1,424 (43.2%). Observed: 228/1,424 (16.0%) in bin 16 and 387 drafted players below. Both series use 0–50%; the locked starter is unchanged.

`observed_vs_topK_bin_counts.csv` preserves original counts, intervals and the benchmark counts/rates. `player_membership_and_topK.csv.gz` saves exact scores, ranks and outcomes. `provenance.json` records source hashes and selection boundary. `build_topk.py` reproduces the figure; `validation.txt` records completed checks.

See [progression Step 2](../JN_progression.md) and [walkthrough Section 13](../Jazz_Night_Experimental_Walkthrough.md) for interpretation. No stochastic simulation, fitting or significance test was run.
