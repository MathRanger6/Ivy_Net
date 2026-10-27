# JN-03: observed vs top-K vs Gibbs SELECT (rule D)

Created 27 October 2026. **Ready for review; not locked.**

[View the figure](JN03_PPM_observed_topK_gibbs_Q16.png). SVG included.

Same cohort as JN-01 / JN-02: 22,795 players, K = 615 ever-drafted count, Q16 bins, PPM within season, 2009–2021 final eligible records.

**SCORE:** \(S_i = A_i\). **SELECT:** PD20 Gibbs rule D (`tier1_pool_assignment.choose_selected`, choice `"D"`) — weights \(\propto \exp(S/t_{\mathrm{sel}})\), then \(K\) draws without replacement per replicate.

Green / purple / teal **lines** are Monte Carlo **inclusion frequencies** (12,000 replicates each) at illustrative \(t_{\mathrm{sel}} \in \{0.25, 0.7, 2.5\}\). This is Step 3 only: **no MLE** for temperature (Step 4).

| File | Role |
|------|------|
| `gibbs_t_sweep_bin_rates.csv` | Full bin rates for nine temperatures |
| `observed_topK_gibbs_bin_counts.csv` | Observed, top-K, and featured Gibbs bin summaries |
| `player_gibbs_inclusion_by_t.csv.gz` | Player-level mean inclusion by \(t_{\mathrm{sel}}\) |
| `build_gibbs.py` | Reproduces outputs |
| `provenance.json` / `validation.txt` | Hashes and checks |

Cold \(t\) approaches JN-02 top-K in bin 16; large \(t\) flattens inclusion toward \(K/N\). Intermediate \(t\) spreads some mass into lower bins but does not yet claim a best fit.

See [JN progression Step 3](../JN_progression.md).
