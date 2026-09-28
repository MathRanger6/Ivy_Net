# Penalty-first demonstration: can scarcity suppress a model downturn?

**Last synced:** 2026-09-27  
**Status:** SUPERSEDED, UNEXECUTED DRAFT. Charles rejected adopting numerical downturn criteria without discussion. The historical draft below is not execution authority. Its automatic script has been disabled. The agreed replacement is `ASSORT_20260927_penalty_bars_v1_specification.md`: charts first, then joint interpretation; no automatic scarcity stage.

## Purpose and sequence

Earlier experiments changed some winners but did not demonstrate a downturn. Charles now asks us to first establish a model configuration with a substantial downturn at 10% selection, then hold that penalty fixed while making selection scarcer. This is an intentionally constructed model demonstration, not estimation of a basketball parameter. A successful demonstration could motivate a hypothesis about basketball; it would not validate that explanation empirically.

Use only the saved 2014, 2015, and 2016 populations and their 100 preferential-assignment repetitions ($\rho=1$). This is a declared implementation choice: the earlier rising curves provide a starting point for a penalty-driven downturn. Do not compare different $\rho$ values now. Actual team sizes are preserved in these simulated assignments, but these are not the observed team memberships.

Keep ability, assignments, viability threshold at the 99th percentile, viability sharpness 10, raw team-mean congestion including the focal player, sixteen fixed equal-count peer-quality bins, and deterministic score ranking unchanged. Score is $S_i=A_i-\lambda C_j$; selection takes the highest $K$ scores, with ascending player identifier breaking ties.

## Stage one: bounded construction at 10%

Try $\lambda=1,2,4,8,16,32$ in order. Stop at the first value meeting the definition below in all three seasons. Use one common value across seasons. Do not refine between grid values or claim to identify the smallest possible coefficient. If none passes, stop and report failure within this bounded range; do not extend the range automatically.

For each season, construct the mean selection curve across the 100 saved repetitions. Aggregate counts over adjacent bins so each broad group is weighted by its player count. Let the low group be bins 1–4 and the high group be bins 13–16. Among the four-bin windows starting at bins 1 through 9 (ending no later than bin 12), identify the window with the largest mean selection rate. Choose the lower starting bin in an exact tie. This is the interior comparison group; choosing it is part of the descriptive search, not independent confirmation.

Require all of the following:

- The interior group's mean rate exceeds the low group's mean rate by at least 0.05 (five percentage points).
- Its mean rate exceeds the high group's mean rate by at least 0.05.
- The high-group drop is at least 20% of the interior group's mean rate.
- At least 80 of the 100 repetitions have a positive interior-minus-high difference using that same chosen window.

These are transparent working thresholds for a visible rise and fall, not a significance test or proof of a quadratic parabola. They reduce reliance on an isolated last-bin dip. The 100 repetitions describe assignment variation within the fixed populations, not 100 independent empirical seasons.

## Stage two: freeze penalty, lower selection fraction

If stage one succeeds, use its common coefficient at fractions 10%, 5%, 2.7%, 1%, and 0.5%. Round $K=qN$ to the nearest integer, with halves upward. Also save the zero-penalty comparison at each fraction. No 20% comparison, new assignments, data reconstruction, or coefficient retuning.

Keep each season's stage-one interior window fixed as selection changes. Report its rate, the high-group rate, their percentage-point difference, the relative difference (difference divided by interior rate), and difference divided by the achieved overall selection rate. Report the full sixteen-bin curves as well, so a moving peak or other shape change remains visible. A second adaptive-window diagnostic can describe such movement but must not replace the fixed-window primary comparison.

For positive drop $D$, relative drop is $D/P$ where $P$ is the interior rate. If $P=0$, the relative drop is undefined and must not be replaced by zero. Report the central 95% assignment range of the absolute difference, and the proportion of repetitions with a positive difference. These are descriptive assignment summaries, not confidence intervals.

A smaller percentage-point drop alone does not establish disappearance of the relative shape: all selection rates shrink as fewer people are chosen. We must inspect both scales, the full curve, and assignment variation. Any claim about empirical basketball remains a hypothesis.

## Filing and validation

Keep code/settings under code/penalty_boundary_v1, new outputs under outputs/penalty_boundary_v1, the execution record under docs/run_records, and the narrative report under docs/results. Refuse to overwrite an existing output directory. Verify source hashes, independently reconstruct congestion, check exact selection counts and ranking, reproduce the previous 10% result at lambda one, verify nesting as selection fractions decrease, and preserve input hashes. Use sports_net. Charles handles PDF conversion.
