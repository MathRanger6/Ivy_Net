# LG exploration decision log

## 6 October 2026

Agent nickname: Leo, chosen at Charles's request.

Charles clarified that remaining seats supply opportunities, not a preference
for large teams. Homophily is the only preference. Use “remaining-seat
opportunities” versus “one opportunity per open team” in scientific captions.

Charles approved the first composition demonstration in successive discussion:

- Total capacity equals population size, holding final team sizes identical.
- 2,000 players, 100 teams, 20 seats per team.
- Homophily rho = 0, 0.5, 1, 2, 4.
- One fixed standard-normal population, 30 paired assignments per rho.
- Reuse arrival orders and underlying uniform draws between the two rules.

Both rules use actual-member centroids and identical empty-team initialization.
The seat-opportunity rule is LG. The team-opportunity rule is a separately
labeled alternative, even though this first experiment also fixes final sizes.
This demonstration has no scoring, selection, or MLE stage.

The notebook is the execution interface. Charles controls running it. Leo
performs only small correctness, plotting and resume checks during preparation.
The full experiment is 300 saved divisions and awaits notebook execution.

## Explicit implementation conventions

Seeds 6102026 (population) and 6102027 (assignment) are reproducible engineering
choices, exposed in settings rather than empirical estimates. Streams for
arrival order and inverse-CDF choices are separate and independent of scheduling.
Their inputs are shared across rho as well as between opportunity rules.

Normal draws retain their realized sample moments; theoretical N(0,1) scaling
requires no further transformation. Original draws are preserved.

Within-team variances use the population convention (ddof=0). Distribution
curves average empirical CDFs across complete divisions. Shading and error bars
show one standard deviation across assignments, conditional on this one
population, rather than confidence intervals obtained by pooling players or teams.

The roster heatmap displays repetition 1, selected before observing results.
Each panel orders teams separately by mean talent and members by talent; team
rank is not a shared team identity.

Shifted log weights implement the declared normalized kernels without the
legacy all-underflow fallback. The five approved rho values are unchanged.
The random-grouping expected H_sort is (J-1)/(M-1) for this equal-size, random
arrival, rho=0 design; a small exact-enumeration check verifies both mechanisms.

No scientific output from validation runs should be presented as the approved
2,000-player experiment. Validation files are explicitly named under
results/validation/.

## Still open

Excess-capacity experiments and large-cap convergence remain follow-ups. Their
cap grids and other settings are unapproved. SCORE scaling/clipping, thresholds,
selection settings and MLE choices remain open. No HPC submission, synchronization
or broad sweep is authorized by these files.
