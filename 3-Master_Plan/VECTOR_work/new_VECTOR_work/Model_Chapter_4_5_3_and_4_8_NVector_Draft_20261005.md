# Stochastic selection and empirical fitting

Chapter 4 sections 4.5.3 and 4.8  
5 October 2026

Editorial placement: replace the current Section 4.5.3 with the first section below. Insert the second section immediately after the existing Section 4.8 heading and before its currently outlined subsections. This insert preserves the chapter's group congestion notation, $C_j$. Source numbers refer to the repository evidence notes at the end; they are working citations for review.

## 4.5.3 Stochastic selection and selection temperature

Many selection processes contain uncertainty even after competitive scores have been established. A higher score can increase an individual's chance of selection without guaranteeing a place. To represent this uncertainty while preserving a fixed number of opportunities, we define a stochastic SELECT rule that draws exactly $K$ distinct individuals without replacement. This is the intended fixed-capacity rule adopted for stochastic replay in the model's development history. Earlier deterministic experiments remain separate implementations of SELECT. [1]

Let $\mathcal I$ be the eligible population, with $N$ individuals and an integer capacity satisfying $0\le K\le N$. Each individual enters SELECT with the score $S_i=A_i-\lambda C_{g(i)}$ defined in Section 4.4.5. Scores and group membership remain fixed throughout selection. We denote the selection temperature by $t_{\mathrm{SELECT}}>0$, distinguishing it from the temperature parameter used in the earlier empirical fitting procedure, $t_{\mathrm{MLE}}$, discussed in Section 4.8.

Selection proceeds through successive draws. If $I_r$ denotes the individual chosen at draw $r$, the population remaining before that draw is

$$
R_r=\mathcal I\setminus\{I_1,\ldots,I_{r-1}\},\qquad r=1,\ldots,K.
$$

For each $i\in R_r$, define the conditional probability of the next draw as

$$
\Pr(I_r=i\mid I_1,\ldots,I_{r-1},\mathbf S)
=\frac{\exp(S_i/t_{\mathrm{SELECT}})}
{\sum_{h\in R_r}\exp(S_h/t_{\mathrm{SELECT}})}.
$$

Previously selected individuals have probability zero of being selected again. After each draw, the selected individual is removed and the denominator is recomputed over those who remain. The final outcome is therefore

$$
Y_i=\mathbf{1}\{i\in\{I_1,\ldots,I_K\}\},
\qquad \sum_{i\in\mathcal I}Y_i=K.
$$

These equations give an explicit statement of the sequential weighted sampling procedure described in the development records. The exponential terms are often called Gibbs weights, while sequential proportional sampling is also described there as a Plackett–Luce procedure. The displayed conditional probability describes the next draw. It is not the marginal probability that individual $i$ belongs to the final set of $K$ winners. The latter depends on all possible sequences through which that set can be formed. Draw order is a device for defining the selection distribution; it need not represent an observed institutional ranking. [1, 2]

Temperature controls how strongly score differences influence each draw. For two remaining individuals, the ratio of their next-draw probabilities is

$$
\frac{\Pr(I_r=i\mid\cdot)}{\Pr(I_r=h\mid\cdot)}
=\exp\left(\frac{S_i-S_h}{t_{\mathrm{SELECT}}}\right).
$$

Thus, lowering temperature magnifies the advantage associated with a given score difference. As temperature approaches zero, the selected set approaches the deterministic top-$K$ set when there is no tie at the selection boundary. Boundary ties require a stated tie convention; the limiting stochastic rule does not itself impose the fixed-order convention used in deterministic code. As temperature becomes arbitrarily large, the next draw approaches uniform sampling from the remaining population and each individual's final inclusion probability approaches $K/N$. Temperature changes uncertainty in SELECT without changing the scores or the number of opportunities.

The mathematical rule permits any finite real score. Negative scores still yield positive exponential weights, and adding the same constant to every score leaves every draw probability unchanged. This matters when comparing the definition with legacy code. The shared selection helper first replaces negative scores by zero and sets the draw count to the smaller of $K$ and the number of strictly positive scores. If no score is positive, it returns no selections. It also uses deterministic fallbacks at very small temperatures or when the numerical weights collapse. Consequently, some historical runs through that helper need not follow the unrestricted equation above or return exactly $K$ winners. The cap does not mean that every zero-clipped candidate is excluded: when Gibbs sampling occurs, such candidates receive positive exponential weights. [3]

The equation above defines the intended model. Establishing which completed runs implement it requires identifying the code version and selection path used in each run, checking whether clipping, capping, or numerical fallbacks were active, and determining whether any reported result changes under an implementation that preserves the stated rule. That verification remains open. It should be completed before describing all legacy stochastic results as realizations of this exact model.

## 4.8 Model scope, limitations, and the bridge to empirical fitting

The empirical fitting work estimated parameters on fixed observed basketball rosters using a probability model distinct from the fixed-capacity SELECT rule. The fitting procedure did not regenerate teams through ASSIGN or simulate a set of winners during optimization. Instead, it evaluated how well a season-wise probability specification accounted for the recorded binary outcomes on the observed rosters. The existing estimates therefore document a completed Bernoulli calibration. They do not constitute an exact-$K$ likelihood fit of the stochastic model defined in Section 4.5.3. [4]

For season $s$, let $\mathcal I_s$ denote the player-season observations entering the likelihood. The measured performance quantity $A_{is}$ was points per minute standardized within season by the analysis pipeline. The binary outcome $Y_{is}$ indicated whether the player was ever drafted. The fitting panel retained all eligible player-season observations rather than restricting outcomes to one final-season observation per athlete. Accordingly, the same eventual draft outcome could appear on several rows belonging to one player. These are the observational units of the historical fit; they should not be described as independent annual draft decisions or as distinct draft selections merely because the likelihood multiplies contributions across rows. A revision intended to model annual selection would need to establish a corresponding eligible population and outcome timing. [5]

Congestion was computed on the observed team-season rosters using the full-group definition introduced in Section 4.4.5. With $g_s(i)$ denoting the group containing individual $i$ in season $s$, the fitted congestion term was

$$
C_{js}(\gamma,\theta_s)
=\frac{1}{n_{js}}\sum_{h:g_s(h)=j}
\sigma\bigl(\gamma(A_{hs}-\theta_s)\bigr),
\qquad \sigma(x)=\frac{1}{1+\exp(-x)}.
$$

The mean included the focal player as well as the other retained members of the group. In the code this quantity was stored as pool_c_smooth_team and was often denoted $L^C$ in development documents. Here we use $C_{js}$ to preserve the chapter's notation. This congestion quantity differs from the leave-one-out peer-quality mean used on some HERO horizontal axes. A plot conditioned on peer quality and a likelihood using congestion can coexist, but the two quantities must remain identified separately when interpreting an empirical comparison. [6]

The intermediate quantity supplied to the probability calculation, called the board logit in the implementation, was

$$
\eta_{is}
=\frac{A_{is}}{t_{\mathrm{MLE}}}
-\lambda_{\mathrm{MLE}}C_{g_s(i),s}(\gamma,\theta_s).
$$

The script converted these quantities to probabilities by applying a softmax within each season:

$$
p_{is}
=\frac{\exp(\eta_{is})}
{\sum_{h\in\mathcal I_s}\exp(\eta_{hs})},
\qquad \sum_{i\in\mathcal I_s}p_{is}=1.
$$

The softmax specifies the probabilities; the Bernoulli model specifies how those probabilities contribute to the likelihood of the observed binary outcomes. The historical likelihood and log-likelihood were

$$
\mathcal L_B(\lambda_{\mathrm{MLE}},\gamma,t_{\mathrm{MLE}})
=\prod_s\prod_{i\in\mathcal I_s}
p_{is}^{Y_{is}}(1-p_{is})^{1-Y_{is}},
$$

$$
\ell_B(\lambda_{\mathrm{MLE}},\gamma,t_{\mathrm{MLE}})
=\sum_s\sum_{i\in\mathcal I_s}
\left[Y_{is}\log p_{is}
+(1-Y_{is})\log(1-p_{is})\right].
$$

For numerical evaluation, the implementation clipped each probability to the interval $[10^{-15},1-10^{-15}]$ before taking logarithms. It minimized the negative log-likelihood using L-BFGS-B over the logarithms of the positive parameters $\lambda_{\mathrm{MLE}}$, $\gamma$, and $t_{\mathrm{MLE}}$. Congestion was recomputed as $\gamma$ changed during joint optimization. A separate option held $\gamma$ fixed and optimized the other two parameters. Reported overlap between the highest-probability observations and positive outcomes was a diagnostic, not the objective being optimized. [4]

The season normalization has a consequential implication. Before numerical clipping, the working independent Bernoulli model, conditional on the thresholds treated as fixed during fitting, satisfies

$$
\operatorname{E}\left[\sum_{i\in\mathcal I_s}Y_{is}\mid\mathbf A,\mathbf g,\theta_s\right]
=\sum_{i\in\mathcal I_s}p_{is}=1.
$$

The code did not multiply the probabilities by the observed number of positive outcomes, fit a season intercept to that count, or condition the likelihood on selecting exactly $K_s$ individuals. This is the historical working Bernoulli specification, but its normalization does not match a season containing many observed positive outcomes. Consequently, the saved probabilities should not be presented as validated individual draft probabilities. What remains to be established is whether this objective is defensible as a working calibration criterion for the intended scientific comparison, or whether a different outcome likelihood and observational unit are required. Neither a satisfactory ranking diagnostic nor a successful optimizer convergence message resolves that question.

The viability threshold $\theta_s$ was fixed during optimization, although its value was calculated separately for each season. The preprocessing routine counted positive draft labels among that season's rows with observed performance, used $K_s^Y=\max(1,\sum_iY_{is})$, and set

$$
\theta_s=Q_{1-K_s^Y/N_s}\bigl(\{A_{is}\}\bigr),
$$

where $N_s$ and the empirical quantile refer to that preprocessing population. The superscript $Y$ distinguishes this count of positive labels from a separately established institutional capacity. Because the labels describe eventual drafting on player-season rows, their season total is not automatically the number drafted in that calendar year. Thus, the outcome count affected the fit indirectly through the construction of congestion, even though the Bernoulli likelihood imposed no fixed-capacity constraint. The interpretation and timing of this threshold must be revisited if the outcome population is changed. [7]

Assignment preference $\rho$ was outside the outcome likelihood because team membership was observed and held fixed. A separate calibration compared simulated and empirical values of the sorting statistic $H_{\mathrm{sort}}$. The saved longitudinal result selected $\rho=0$, at the lower boundary of the assignment calibration. The empirical mean sorting statistic remained below the simulated mean at that boundary, so this result does not establish that actual team assignment was random. It describes the closest setting reported for that calibration. The Gibbs selection temperature was also treated separately: it was swept in simulation, with a replay starting value of one, rather than jointly estimated as part of an exact-$K$ likelihood. [1, 8]

The joint fitting artifact saved on 28 August 2026 reports

$$
\hat\gamma=19.57233208,\qquad
\hat\lambda_{\mathrm{MLE}}=1.30243058,\qquad
\hat t_{\mathrm{MLE}}=1.06989673,
$$

with log-likelihood $-8865.70116079$, 46,306 player-season observations, and 1,133 positive outcome flags across 11 season batches. The optimizer reported convergence. These are historical point estimates, not evidence by themselves of precise identification, causal effects, or a validated generative selection model. [9]

The run's analysis-window documentation is internally inconsistent. Its filename, saved metadata, and campaign description identify 2009–2021. However, the inspected panel loader constructs a 2011–2021 panel before applying the requested window, which is consistent with the saved total of 11 seasons. We therefore report both the recorded 2009–2021 run label and the implemented 2011–2021 restriction rather than asserting that the fit contains all thirteen seasons. Confirmation of the original run's input seasons and code version remains necessary to finalize its sample description. An earlier 2013–2021 fit, with $\gamma=18$ fixed, instead reported $\hat\lambda_{\mathrm{MLE}}=2.57150065$ and $\hat t_{\mathrm{MLE}}=1.06556159$. Those estimates belong to a different fitting specification and should not be merged with the later joint estimates. [5, 9, 10]

There is a further distinction between the scale of the fitted logit and the score used in the generative model. In the fitting code, temperature divides measured performance alone; in stochastic SELECT it divides the entire score. Algebraically,

$$
\frac{A_i}{t_{\mathrm{MLE}}}-\lambda_{\mathrm{MLE}}C_{g(i)}
=\frac{A_i-t_{\mathrm{MLE}}\lambda_{\mathrm{MLE}}C_{g(i)}}{t_{\mathrm{MLE}}}.
$$

For fixed congestion values, reproducing those same logits with a score of the chapter's form would require a score coefficient $\lambda=t_{\mathrm{MLE}}\lambda_{\mathrm{MLE}}$ and, for the Gibbs weights, $t_{\mathrm{SELECT}}=t_{\mathrm{MLE}}$. This identity clarifies the change of parameter scale; it is not a historical decision to equate the two temperatures or evidence that their likelihoods are equivalent. Even ranking by the fitted probabilities need not agree with ranking by $A_i-\lambda_{\mathrm{MLE}}C_{g(i)}$ when the numerical penalty coefficient is transferred unchanged. [4, 11]

An exact-$K$ fit would evaluate the probability of the observed selected set under the without-replacement process. If selection order is unobserved, that probability sums over the possible orders of the selected individuals. It is not the product of the independent Bernoulli contributions used above. Development documents considered such a likelihood, but explicitly retained Bernoulli estimation for the completed fitting procedure. No completed exact-$K$ refit has been established in the verified record. [2, 12]

The empirical bridge consequently remains a separate methodological task. Before treating the historical estimates as fitted parameters of deterministic top-$K$ or stochastic exact-$K$ selection, the analysis must align the outcome population and timing, the congestion definition and scale, the selection implementation, and the probability model used for estimation. A refit or an explicit justification for using the earlier estimates is still required. This distinction allows the completed fitting work and mechanism experiments to be documented together while preserving the limits of what their combination currently establishes. [13]

## Repository evidence notes for review

These notes identify the code and saved records supporting the draft. They are not an external literature bibliography. The mathematical statements about sequential draw probabilities, temperature limits, score-shift invariance, the Bernoulli expected count, and the coefficient reparameterization are explicit algebraic consequences of the stated rules. They are not new empirical results or claims that these derivations were previously written verbatim.

[1] The stochastic replay decision and distinction between temperatures are documented in [MBB_empirical_roster_select_replay.md](../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md), lines 370–418 and 454–462. The direct user instruction is preserved in [.specstory/history/2026-06-11_08-19-11-0400-compass.md](../../../.specstory/history/2026-06-11_08-19-11-0400-compass.md), line 331818, with the subsequent implementation authorization at line 332351. The lock was for empirical-roster replay; it does not retroactively change earlier deterministic runs.

[2] [PD20_softmax_K_winners_explainer.md](../../Alex_stuff/PD20_softmax_K_winners_explainer.md), lines 190–199, describes the observed-set likelihood for sequential proportional sampling. [PD20_notes.md](../../../transcripts/PD20_notes.md), lines 121–127, identifies the weighted without-replacement procedure as Plackett–Luce.

[3] [sports/tier1_pool_assignment.py](../../../sports/tier1_pool_assignment.py), lines 1111–1128 and 1131–1215, defines the shared helper. Score clipping occurs at line 1159; the positive-score cap at lines 1161–1165; deterministic fallback branches at lines 1193–1197 and 1203–1209; weighted sampling without replacement at line 1212. This caveat concerns the inspected helper and runs invoking it, not every SELECT implementation in the repository.

[4] [sports/scripts/pd21_draft_bernoulli_mle.py](../../../sports/scripts/pd21_draft_bernoulli_mle.py), lines 111–191 and 327–409, implements fixed-roster congestion, the exact board logits, softmax, the numerically clipped Bernoulli objective, and joint optimization. LOG_EPS is defined at line 60; the logit temperature guard is at line 164. The fixed-gamma optimization option and main dispatch are in the same script. No fitting code was run for this draft.

[5] [ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md](assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md), lines 94–115, documents all-player-season rows and repeated ever-drafted labels. The loader is [sports/scripts/grandchild_selection_inverted_u_diagnostic.py](../../../sports/scripts/grandchild_selection_inverted_u_diagnostic.py), lines 89–122. It sets within-season standardized points per minute and fixes the initial panel bounds from FULL_PANEL_SEASON_MIN = 2011 and FULL_PANEL_SEASON_MAX = 2021 at lines 46–47. The later requested-window filter cannot restore excluded 2009–2010 rows. Historical input-season provenance remains to be confirmed rather than inferred solely from a filename.

[6] [sports/tier1_pool_assignment.py](../../../sports/tier1_pool_assignment.py), lines 772–781 and 870–912, implements logistic viability and full-team mean congestion. It clips the logistic argument to [-500, 500] for numerical stability. The distinction from the leave-one-out HERO axis also appears in [MBB_empirical_roster_select_replay.md](../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md), lines 464–471.

[7] [sports/scripts/grandchild_selection_inverted_u_diagnostic.py](../../../sports/scripts/grandchild_selection_inverted_u_diagnostic.py), lines 139–158, specifies the season threshold, positive-outcome count, and max(1, count) guard. The MLE script invokes this routine before attaching congestion. This is a preprocessing rule, not a free threshold estimated by the optimizer.

[8] [REIGNING_PD21_rho_hsort_calibrate_2009_2021_mg10_min20_09_21_fit_bracket.json](../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/rho/REIGNING_PD21_rho_hsort_calibrate_2009_2021_mg10_min20_09_21_fit_bracket.json), lines 332–345, reports longitudinal rho = 0, simulated mean H_sort = 0.0823114512, and empirical mean H_sort = 0.0644102092. These are assignment-calibration results, not output-likelihood estimates.

[9] [REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json](../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json), lines 2–21 and 76–85, supplies the date, window label, counts, estimates, objective value, and convergence flag. Full stored estimates are gamma = 19.572332081866243, lambda = 1.3024305834948529, t = 1.0698967300656186, and log-likelihood = -8865.70116078651. The campaign label is also in [calibration/manifest.json](../../re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/manifest.json). [sports/scripts/reigning_hero_calibration.py](../../../sports/scripts/reigning_hero_calibration.py), lines 40–41 and 82–99, requests the 2009–2021 window. Read these alongside note [5] when describing the effective sample.

[10] [PD21_draft_bernoulli_mle_2013_2021.json](../../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2013_2021.json), lines 2–21, records the fixed-gamma fit: gamma = 18, lambda = 2.571500648851351, t = 1.065561586816066, 38,123 rows, 882 positive flags, and nine seasons. The older [PD21_draft_bernoulli_mle_2011_2021.json](../../re_entry/HEROs_and_PASSes/pd21_mle/PD21_draft_bernoulli_mle_2011_2021.json) records a grid-best point with gamma = 10 fixed, lambda = 2, t = 1, and bfgs = null; it must not be substituted for the later joint estimate.

[11] [MBB_empirical_roster_select_replay.md](../../re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md), lines 374–387, explicitly distinguishes A/t - lambda L_C from the Gibbs weight exp(S/t). The coefficient identity in the draft explains that mismatch algebraically; no equivalence of Bernoulli and exact-K likelihoods is asserted.

[12] [MLE_basics.md](../../MLE/MLE_basics.md), lines 208, 244–250, and 420–426, states that empirical fitting ended with the Bernoulli optimization, with no Phase B re-estimation, while describing exact-K estimation as an alternative. The later replay lock in note [1] kept that fitting procedure unchanged.

[13] [VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md](VECTOR_PD44_Dissertation_Work_Map_and_Model_Chapter_Outline.md), lines 197–201, requires an equivalence argument or justified approximation before claiming parameter transfer and flags implementation verification. This draft adds explicit descriptions of the verified mismatches without resolving them by assumption.

Editorial consistency checks before merging: retain the existing Section 4.5.4 distinction between Bernoulli and fixed-capacity selection; change the selection-temperature symbol in the Section 4.6.6 heading and its planned figure description to $t_{\mathrm{SELECT}}$ when integrating this insert. The rest of Section 4.8 remains at the current outline stage pending the next transcript and a separate writing pass. These broader portions of the live chapter have not been edited.

