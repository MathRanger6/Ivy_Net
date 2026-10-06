# NVector to SVector MLE Bernoulli response

**Date:** 2026-10-05  
**From:** New VECTOR  
**To:** Scholar VECTOR  
**Purpose:** Repository-verified reconstruction of canonical stochastic SELECT and historical maximum likelihood estimation (MLE), for Chapter 4 Sections 4.5.3 and 4.8.  
**Scope:** Full response supplied to Charles, with Markdown math formatting and repository-relative source links. No new fits, experiments, or manuscript edits were performed. Source links identify repository files; uploading this document alone does not upload those source files.

I found and read [Model_Chapter_First_Draft.docx](Model_Chapter_First_Draft.docx). I have not changed it.

**The central distinction is clear: we chose Gibbs selection of $K$ individuals without replacement for stochastic replay, but the saved parameter estimates came from a Bernoulli likelihood. I found no completed exact-$K$ refit.** One legacy implementation detail also needs attention before the chapter claims complete agreement between that definition and the code.

**1. What stochastic SELECT rule did we choose?**

**Gibbs weighted sampling without replacement, selecting exactly $K$ individuals.**

Your recorded instruction was: “let’s start using Gibbs K draw.” The subsequent decision document explicitly preserves **Bernoulli fitting unchanged** while choosing **Gibbs $K$-draw for generative replay**. Deterministic top-$K$ and Bernoulli replay were designated subsequent sensitivity comparisons. [Recorded instruction — line 331818][history]; [SELECT decision — line 454][replay-decision].

The historical decision specifically governed **empirical-roster replay**. Your current Chapter 4 draft adopts that fixed-capacity approach as its canonical stochastic rule. We should not imply that all earlier experiments used it; many used deterministic top-$K$.

**2. What is its exact probability equation?**

Let $R_r$ contain the eligible individuals remaining before draw $r$, and let scores remain fixed during selection. Then:

$$
S_i=A_i-\lambda L_i^C,
\qquad
\boxed{
\Pr(I_r=i\mid I_1,\ldots,I_{r-1})
=
\frac{\exp(S_i/t_{\mathrm{SELECT}})}
{\displaystyle\sum_{j\in R_r}\exp(S_j/t_{\mathrm{SELECT}})}
}
$$

for $i\in R_r$, $r=1,\ldots,K$, and $t_{\mathrm{SELECT}}>0$. After each draw, remove the selected individual. Consequently,

$$
Y_i=\mathbf 1\{i\in\{I_1,\ldots,I_K\}\},
\qquad \sum_iY_i=K.
$$

**Plain English:** choose one person using score-dependent weights, remove that person, and repeat until all $K$ opportunities are filled. Lower temperature concentrates selection on higher scores; higher temperature makes the draw more random.

This is the explicit mathematical expansion of the repository’s documented **sequential proportional sampling / Plackett–Luce** process. The softmax fraction is a **next-draw probability**, not an individual’s final probability of being among all $K$ winners. An ordered sequence has probability equal to the product of its successive draw probabilities; an unordered winning set requires summing over its possible orders. [Documented sampling interpretation — line 190][sequential]; [Gibbs sampling code — line 1188][gibbs-code].

**3. What likelihood did the MLE actually optimize?**

For each season $s$, the code constructed:

$$
\eta_{is}=\frac{A_{is}}{t_{\mathrm{MLE}}}
-\lambda_{\mathrm{MLE}}L^C_{is}(\gamma),
\qquad
p_{is}=
\frac{\exp(\eta_{is})}
{\displaystyle\sum_{h\in\mathcal I_s}\exp(\eta_{hs})}.
$$

It then used the independent Bernoulli likelihood:

$$
\mathcal L_B
=
\prod_s\prod_{i\in\mathcal I_s}
p_{is}^{Y_{is}}(1-p_{is})^{1-Y_{is}},
$$

with log-likelihood

$$
\boxed{
\ell_B=
\sum_s\sum_{i\in\mathcal I_s}
\left[
Y_{is}\log p_{is}
+(1-Y_{is})\log(1-p_{is})
\right].
}
$$

Numerically, the code clips probabilities to $[10^{-15},1-10^{-15}]$ before taking logarithms. It maximizes this objective jointly over **$\lambda,\gamma,t_{\mathrm{MLE}}$** using L-BFGS-B in log-parameter space. [Probability and likelihood implementation — line 162][likelihood]; [Joint optimizer — line 346][optimizer].

Here, congestion was the **team mean, including the focal player**, of logistic viability:

$$
L^C_{is}(\gamma)
=
\frac{1}{n_{js}}
\sum_{h:g(h,s)=j}
\sigma\!\left(\gamma(A_{hs}-\theta_s)\right),
\qquad j=g(i,s).
$$

It was not the leave-one-out peer mean used on the HERO horizontal axis. [Congestion implementation — line 870][congestion].

Two consequential details:

- **Temperature placement differs:** $A/t-\lambda L^C$ is not $(A-\lambda L^C)/t$ with the same numerical $\lambda$.
- **There is no $K$ multiplier in these probabilities.** They sum to one per season. Mathematically, the specified Bernoulli model therefore has expected total successes of one per season, rather than $K_s$. That is a consequence of the actual formula, not a newly proposed interpretation.

**4. Which parameter values were estimated?**

The saved August 28 **joint three-parameter fit** reports:

$$
\boxed{
\hat\gamma=19.572332081866243,\quad
\hat\lambda=1.3024305834948529,\quad
\hat t_{\mathrm{MLE}}=1.0698967300656186
}
$$

with $\ell_B=-8865.70116078651$. [Saved joint-fit artifact — line 13][joint-fit].

That artifact contains **46,306 player-season observations across 11 observed seasons**. Its 1,133 positive flags are sums across those rows, not 1,133 distinct draft selections. The fitting population used all player-seasons with an “ever drafted” outcome, rather than only career-exit rows. [Population audit — line 94][population].

Earlier saved work differs:

- **2013–2021 fit:** $\gamma=18$ fixed; $\hat\lambda=2.571500648851351$, $\hat t=1.065561586816066$. [Artifact — line 7][older-fit].
- **Earlier 2011–2021 artifact:** $\gamma=10$ fixed, grid-best $(\lambda,t)=(2,1)$, and no BFGS result. This was a grid result, not the later joint fit. [Artifact — line 7][grid-fit].

Other parameters were handled separately:

- **$\theta_s$:** preset to the empirical $1-K_s/N_s$ examination/performance quantile, with $K_s$ derived from that season’s positive outcome flags. It was not jointly estimated. Thus $K_s$ affected preprocessing through $\theta_s$, despite not imposing a capacity constraint in the likelihood. [Code — line 139][theta].
- **$\rho$:** absent from this outcome fit because empirical rosters were held fixed. Separate assignment calibration against $H_{\mathrm{sort}}$ returned longitudinal $\rho^*=0$ in the reigning artifact—a boundary calibration result, not proof of random assignment. [Artifact — line 332][rho].
- **$t_{\mathrm{SELECT}}$:** separately swept/chosen, with replay starting at $1$. It was explicitly distinguished from fitted $t_{\mathrm{MLE}}\approx1.07$. [Two-temperature decision — line 370][temperatures].

**5. Did we decide to refit under exact-$K$?**

**I found no verified adopted or completed exact-$K$ refit.**

An exact-$K$ likelihood was discussed as an alternative. However, the fitting documentation explicitly says **“no Phase B re-estimation in v1,”** and the later replay decision kept Bernoulli fitting unchanged. Subsequently, the PD44 work map warned that transfer between these probability models requires demonstrated equivalence or an explicitly justified approximation. [No second optimization — line 244][no-refit]; [Exact-$K$ alternative — line 420][alternative]; [Later transfer warning — line 197][transfer].

**6. What is settled, and what remains unresolved?**

- **Actually fitted:** the Bernoulli likelihood above, on fixed empirical rosters.
- **Chosen stochastic rule and current manuscript intention:** Gibbs weighted selection without replacement until $K$ individuals are selected.
- **Unresolved fitting bridge:** an exact-$K$ refit or a defensible justification for transporting the earlier estimates.
- **Implementation discrepancy:** the legacy `choose_selected` helper clips negative scores to zero and caps the number selected at the number of positive scores. Therefore, it does not implement the clean, unrestricted equation above in every case. It also contains deterministic numerical fallbacks. [Relevant code — line 1157][clipping].

For **§4.5.3**, use the conditional draw equation above as the **intended model definition**, while retaining an implementation note until that discrepancy is resolved.

For the **opening of §4.8**, this wording is supported:

> Our earlier calibration estimated $\gamma$, $\lambda$, and $t_{\mathrm{MLE}}$ jointly on fixed empirical rosters using independent Bernoulli outcomes with season-normalized softmax probabilities. The fitted logit was $A_i/t_{\mathrm{MLE}}-\lambda L_i^C(\gamma)$. This estimation model differs from the fixed-capacity stochastic SELECT rule defined in Section 4.5.3. The resulting estimates therefore document the earlier calibration; they are not estimates obtained under an exact-$K$ likelihood. Establishing that fitting bridge remains unresolved.

[history]: ../../../.specstory/history/2026-06-11_08-19-11-0400-compass.md "Recorded user instruction, line 331818"
[replay-decision]: ../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md "SELECT decision, line 454"
[sequential]: ../../Alex_stuff/PD20_softmax_K_winners_explainer.md "Sequential proportional sampling, line 190"
[gibbs-code]: ../../../sports/tier1_pool_assignment.py "Gibbs sampling implementation, line 1188"
[likelihood]: ../../../sports/scripts/pd21_draft_bernoulli_mle.py "Board logits, softmax, and Bernoulli log-likelihood, line 162"
[optimizer]: ../../../sports/scripts/pd21_draft_bernoulli_mle.py "Joint optimizer, line 346"
[congestion]: ../../../sports/tier1_pool_assignment.py "Team congestion including focal player, line 870"
[joint-fit]: ../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json "Joint estimates, line 13"
[population]: assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md "Population and outcome behind saved coefficients, line 94"
[older-fit]: ../../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2013_2021.json "Fixed-gamma fit, line 7"
[grid-fit]: ../../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2011_2021.json "Earlier grid result, line 7"
[theta]: ../../../sports/scripts/grandchild_selection_inverted_u_diagnostic.py "Per-season theta construction, line 139"
[rho]: ../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/rho/REIGNING_PD21_rho_hsort_calibrate_2009_2021_mg10_min20_09_21_fit_bracket.json "Separate longitudinal rho calibration, line 332"
[temperatures]: ../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md "Two distinct temperatures, line 370"
[no-refit]: ../../MLE/MLE_basics.md "No Phase B re-estimation, line 244"
[alternative]: ../../MLE/MLE_basics.md "Exact-K likelihood discussed as alternative, line 420"
[transfer]: VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md "Transfer warning, line 197"
[clipping]: ../../../sports/tier1_pool_assignment.py "Score clipping and K cap, line 1157"

