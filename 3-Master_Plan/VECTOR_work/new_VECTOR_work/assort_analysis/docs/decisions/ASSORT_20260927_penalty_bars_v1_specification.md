# Penalty exploration — look at the bar charts first

**Last synced:** 2026-09-27
**Status:** Charles authorized this first stage after discussing the choices individually.

We want to find out whether the model can produce a meaningful downturn before asking whether scarcity suppresses it. For now select 10% of players, use the existing rho = 1 simulated assignments for 2014–2016 (100 repetitions each), and compare lambda = 0, 1, 2, 4. Charles and VECTOR will inspect the charts together. There is no numerical pass/fail criterion, fitted parabola, automatic choice of lambda, or lower-selection-fraction experiment. Values 8 and 16 are an agreed possible extension if the first charts give us nothing; stop for review first. Comparing rho values is later work.

Score remains $S_i=A_i-\lambda C_j$. Keep the existing player performance, raw full-team congestion including the focal player, and deterministic highest-K selection. Round 10% of each season's population to the nearest integer (halves upward); break score ties by ascending player identifier. Do not reconstruct the source data or generate new assignments.

## How the charts are constructed

Show 16 equal-width bins (EW) and 16 quantile bins side by side for each season and penalty. Both use the same peer-quality variable: mean standardized performance of teammates excluding the focal player. Quantile bins reuse the saved equal-count bin memberships in each assignment. For EW bins, use one set of equally spaced edges from the minimum to maximum peer quality across all 100 assignments within that season. Keep these edges unchanged across penalties. These are model charts, not a replication of the empirical HERO's exact plotting pipeline.

Each bar is the total selected player-assignment observations divided by total player-assignment observations in that bin across the 100 repetitions. That weights occupied bins by the number of players represented; empty assignments add neither successes nor players. It does not turn repeated appearances of a player into independent empirical people. Save per-repetition counts and rates as well. Quantile bars correspond to relative rank groups, while EW bars correspond to fixed peer-quality intervals.

Show the mean number of players per assignment in each bin below the selection panels. Counts do not change with lambda. Save the number of assignments in which each bin is occupied, so a sparsely populated tail can be identified rather than mistaken for strong evidence. An entirely empty bin has an undefined selection rate, not zero. Use a common selection-rate vertical scale across all twelve conditions and both binning methods. Plot counts on their own clearly labeled scale.

The implementation choices about pooling and fixed EW edges preserve comparability; they are not definitions of a meaningful downturn. Interpretation remains joint and exploratory. These conditional model results could motivate an empirical hypothesis, but cannot establish that scarcity explains basketball's observed curve.

## Checks and filing

Use sports_net; verify prior input hashes, reconstruct congestion independently, verify highest-K winners with a separate sorting implementation, reproduce saved lambda-one 10% winners, and check that both binning methods account for every player and selected player. Save code under code/penalty_bars_v1, outputs under outputs/penalty_bars_v1, an execution record under docs/run_records, and the narrative under docs/results. Do not overwrite earlier results. Charles regenerates PDFs.
