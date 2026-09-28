# How strong was the congestion penalty at λ = 1?

**Date:** September 27, 2026  
**Status:** Completed diagnostic of existing results. No new assignments, parameter sweep, or PDF regeneration.

## Why we took this step

First we compared selection with and without congestion in 2014, 2015, and 2016. Congestion changed some winners even without preferential assignment, and changed more with preferential assignment. But the averaged curves did not demonstrate a clear high-peer-quality downturn. That answered a question about whether congestion could affect selection; it did not establish whether assortativity is necessary for a downturn.

Next we increased the selection fraction from 2.7% to 10%, using exactly the same saved assignments and scores. More people changed selection status, but they represented a smaller share of the selected group. The downturn still did not clearly appear.

So we stopped expanding the experiment and asked a narrower question: **how large was the penalty we had actually applied?** A coefficient of one sounds substantial, but its effect depends on the size of the quantity it multiplies.

This diagnostic read the saved results for all three seasons and all 100 paired assignment repetitions per season. It did not generate new teams or try another penalty coefficient.

## What the penalty means in this experiment

Individual performance, denoted by $A_i$, is season-standardized points per minute (PPM). Its population standard deviation is one. It is a measured performance variable, not an independently identified measure of innate talent.

The score is

$$
S_i=A_i-\lambda C_j.
$$

Here $C_j$ is the mean viability of all eligible players assigned to team $j$, including the focal player:

$$
C_j=\frac{1}{n_j}\sum_{i\in j}
\frac{1}{1+\exp[-10(A_i-\theta)]}.
$$

The threshold $\theta$ is the season's fixed 99th percentile of standardized performance. Thus the congestion measure emphasizes exceptionally high measured performance. Most players contribute very little; the team average further dilutes each contribution. For illustration, one player with viability almost one on a twelve-player team contributes about $1/12=0.083$ to congestion if all other contributions are negligible.

At $\lambda=1$, the numerical score deduction equals $C_j$. These are scenario settings, not newly fitted empirical parameters.

## What we found about the overall scale

Across the three seasons, the standard deviation of the penalty was about **0.026–0.027 without assignment preference** and **0.032–0.033 with assignment preference**. The corresponding standard deviation of individual performance was one.

In plain English, the penalty varied across players much less than measured performance did. The ratio was approximately 2.6%–3.3%. This is a comparison of standard deviations—not the percentage of selection outcomes explained or changed.

The average deduction was about 0.011 in either assignment condition. Reassignment preserves this player-weighted mean because each team member receives the team's average viability. What changes is where those deductions fall and how unevenly they are distributed.

The average is not the whole story. In the 2015 preferential-assignment condition, the average within-run 99th percentile of the penalty was about 0.155. Some players therefore faced appreciably larger deductions. A small population-wide spread does not imply that every individual effect is negligible.

## Why a modest penalty can still change a winner

Consider one saved example from the first 2015 preferential-assignment repetition at 2.7% selection.

Corey Walden's standardized performance was 2.0355 and Keifer Sykes's was 1.9934. Without congestion, Walden was selected and Sykes was not.

Their deductions were 0.0675 and 0.0014 respectively. Their resulting scores were therefore:

$$
S_{\text{Walden}}=2.0355-0.0675\approx1.9679,
$$

$$
S_{\text{Sykes}}=1.9934-0.0014\approx1.9920.
$$

Walden lost a selected place and Sykes gained one. The difference in penalties exceeded the original performance advantage.

These were **simulated team assignments**, not their actual college environments or a claim about their real draft prospects. The example was selected mechanically: the first repetition and the smallest player identifier among those losing and gaining places. We did not search for a dramatic case. Nor does this pairing imply that the algorithm explicitly matched one departing player to one incoming player.

The lesson is simple: a modest deduction can matter when competitors are close to the selection boundary.

## Why that does not necessarily bend the entire curve downward

We also compared the highest peer-quality group with the next-highest group. These are the existing sixteen equal-count groups based on teammates' mean performance excluding the focal player.

In the 2015 preferential-assignment condition, averaging over the 100 repetitions:

- The highest group had a **0.2924** advantage in mean individual performance.
- Its additional mean penalty was **0.0489**.
- Its remaining mean score advantage was **0.2435**.

The same pattern appeared in 2014 and 2016: performance advantages of roughly 0.30, extra penalties of roughly 0.05, and remaining score advantages of roughly 0.25.

This supports an explanation for the continuing upward curve: stronger players were concentrated in stronger environments, and the additional penalty did not remove their group-average performance advantage.

However, group means do not determine top-$K$ selection rates. Those depend on the full score distributions and the selection cutoff. These comparisons are descriptive clues, not a mathematical proof that a downturn is impossible.

## What this adds—and what remains open

We now have evidence that the tested raw penalty is modest on the overall performance scale, while still large enough to rearrange some closely ranked players. That reconciles two observations that initially seemed difficult to square: selection changes occurred, but the averaged curve did not turn downward.

We have not shown that increasing $\lambda$ will produce a downturn, that a larger value would be empirically defensible, or that assortativity is necessary or unnecessary for the phenomenon. These runs also do not implement a five-player court-capacity mechanism. The 2.7% setting remains a scarcity scenario, not an annual draft probability.

Our next decision should concern a scientifically interpretable penalty scale, before any further execution. The earlier fixed-reference standardization proposal is relevant to that discussion, but it has not been executed here. We should not search across coefficients merely until a desired curve appears.

## Evidence and execution record

The diagnostic ran in Charles's **sports_net** environment. It checked 600 saved assignment conditions and 1,200 selection-rate conditions, independently reconstructed congestion from the saved rosters, verified saved selections against their scores, checked balanced losses and gains, and confirmed unchanged input hashes.

Detailed cutoff summaries average performance and penalty gaps only over repetitions with selection changes; a repetition with no changes has no lost-versus-gained gap.

- [Earlier three-season report](ASSORT_20260927_three_season_mechanism_v1_report.md)
- [Selection-rate comparison](ASSORT_20260927_selection_rate_comparison_v1_report.md)
- [Diagnostic code](../../code/penalty_magnitude_v1/ASSORT_20260927_penalty_magnitude_v1.py)
- [Penalty scale summary](../../outputs/penalty_magnitude_v1/penalty_scale_summary.csv)
- [Selection-boundary summary](../../outputs/penalty_magnitude_v1/cutoff_summary.csv)
- [Mechanically selected examples](../../outputs/penalty_magnitude_v1/first_repetition_examples.csv)
- [Execution record and input hashes](../run_records/ASSORT_20260927_penalty_magnitude_v1_run_record.json)

**Stopping point:** Diagnostic complete. No additional experiment, coefficient change, or PDF regeneration has been performed.

