# Jazz night: building the manuscript’s scientific story

**Started:** 27 October 2026, during Charles’s hotel-lobby jazz evening.  
**Status:** Working outline, Part I. We will develop the complete story together before returning to plot selection, new comparisons, and manuscript rewriting.

Much of the existing manuscript remains useful. Charles’s working assessment is that roughly 90% may be retained. Our task is to organize that material around the scientific argument and identify the evidence needed at each transition, rather than begin again. The amount ultimately retained will depend on that review.

## The organizing principle

Begin with a simple explanation. Show what it accounts for, identify a specific discrepancy, and introduce the next ingredient to address that discrepancy. Each addition must earn its place through a scientific question and a comparison.

This follows Alex’s direction in PD49. The sequence below is our proposed way of implementing it; the comparisons are planned, not results already established. If a simpler model succeeds, we should report that rather than manufacture a reason to complicate it.

## 1. Begin with the empirical naïve plot

**Question:** How strongly does individual performance relate to selection?

- “Naïve plot” is Charles’s longstanding name for the empirical plot of own performance against selection probability, estimated by observed selection rates. It predates the naïve benchmark model.
- Introduce the performance measure, the candidate population, and the selection outcome.
- Show the observed relationship, plotting \(A_i\) vs \(P(Y=1|A_i)\), including counts and uncertainty. Establish its strength and shape from the data rather than assume an exponential relationship.
- Use this plot to understand where selection is rare, uncertain, or common. Do not assume that a fixed top percentile identifies superstars or a band of excellence in every domain.

**Proposed graphic:** The empirical own-performance curve. Later comparisons will use this same population, outcome definition, and binning.

**Transition:** How much of this relationship can the simplest performance-based selection rule explain?

## 2. Construct the simplest model: performance determines ranking, and the top K are selected

**Question:** What would selection look like if candidates were chosen strictly by measured performance?

- Assign each candidate a score equal to individual performance:

$$
S_i = A_i.
$$

- Specify selection separately: rank those scores and select the top K candidates. Top-K selection is an additional rule, not a consequence of the score equation alone.
- Introduce N eligible candidates and K available opportunities here. The ratio K/N describes scarcity within that specified selection pool.
- Within a single pool, this rule creates a sharp cutoff, apart from boundary ties: candidates above the cutoff are selected and those below it are not.

**Proposed comparison:** Apply deterministic top-K to the same observed candidates and summarize its predictions in the same bins as the empirical naïve plot. Overlay the two curves.

**What we need to establish:** Whether strict performance ranking reproduces the observed selections and the own-performance curve. Pooling seasons with different cutoffs can smooth a deterministic curve, so smoothness alone is not proof of stochastic selection.

**Transition, if the comparison supports it:** Higher performance favors selection, but strict ranking does not account for who receives the opportunities.

## 3. Introduce uncertainty in selection

**Question:** Can a probabilistic selection rule explain the departures from strict ranking?

- Retain the performance-only score and introduce Gibbs-weighted selection without replacement.
- Higher scores receive larger positive weights. Select one candidate, remove that candidate, and repeat until K distinct candidates have been selected.
- Introduce selection temperature, t_sel, to control how strongly score differences affect selection.
- Distinguish the exponential selection weight from the final probability of inclusion among K winners. The latter is not simply an exponential curve in own performance.

**Proposed comparison:** Retain the observed candidates and performance values. Repeatedly apply the stochastic selection rule to estimate selection frequencies. Put the observed rates, deterministic predictions, and stochastic predictions on the same axes. Inventing synthetic players is not necessary for this initial comparison.

**What we need to establish:** Whether stochastic selection improves the match, and what discrepancies remain. This comparison alone does not identify the source of uncertainty, such as unmeasured qualities or imperfect performance measurement.

## 4. Estimate temperature for the performance-only baseline

**Question:** How much selection uncertainty is consistent with the observed outcomes?

- Fit t_sel for the specified performance-only model instead of choosing a visually appealing value.
- Define a likelihood appropriate to the observed outcome and selection process. Distinguish an observed ordered sequence from an unordered selected set; do not silently substitute independent Bernoulli outcomes for exact-K selection.
- Assess the fit graphically and quantitatively, with predictive assessment where feasible.
- First resolve the empirical selection pools, timing, and K. The current pooled “ever drafted” fraction is not automatically an annual draft quota.
- Treat this estimate as a baseline. It may absorb omitted group effects. Re-estimate temperature alongside congestion parameters when those are introduced.

**Transition:** Having assessed selection against own performance, ask whether the model also explains its relationship with the group environment.

## 5. Introduce groups and motivate congestion

**Question:** Among people with comparable own performance, does selection also vary with the composition of their group?

- Introduce the empirical HERO relationship and the band-of-excellence (BOE) comparisons, with their populations, performance bands, and environmental axes explicitly defined.
- Project the performance-only model’s predictions onto those same environmental axes, using the observed rosters and the same focal bands.
- Identify the mismatch that a group-dependent score would need to explain. Sorting and changing performance composition can generate aggregate patterns even without congestion in SCORE; we must test what the baseline actually predicts.

**First extension:** Introduce a simple congestion measure, such as group mean performance, and assess a score of the form

$$
S_i = A_i - \lambda C_i.
$$

Here C_i denotes the congestion assigned to individual i under the particular definition being tested. An empirical plotting axis and the congestion term in SCORE are distinct choices; using an axis does not establish that it belongs in the score equation.

**Possible next limitation:** A group mean may not distinguish groups containing different concentrations of plausible competitors. Two groups with the same mean can have different performance distributions. This motivates asking whether competitive relevance improves the explanation; it does not itself demonstrate improved fit.

### When the sigmoid enters

Introduce the sigmoid when the narrative reaches the question of which peers are competitively relevant. Explain theta as the location of the transition and gamma as its sharpness, then aggregate competitive relevance into roster pressure.

- Lambda controls the effect of congestion on scores.
- Theta and gamma define how performance contributes to competitive relevance.
- Selection temperature controls uncertainty in selection.

The sigmoid refines the systematic congestion measure. It does not, by itself, add stochasticity to selection. Shared and leave-one-out specifications remain candidates to compare; this outline does not settle their notation or choose a winner.

### When scarcity returns

K/N has already been introduced with the original allocation problem. Return to it here to ask whether the competitive-relevance threshold should depend on the scarcity of opportunities. A rule linking theta to a performance quantile based on K/N is a hypothesis or modeling specification to examine, not an identity established by the definitions.

**Proposed evaluation:** Assess whether each extension improves the relevant curves. Where an interior peak exists, examine its location and curvature on a declared scale. Do not add parameters solely to move an apex or deepen a downturn without a corresponding mechanism and evidence of improvement.

## Where we stop for now

This is the opening portion of the story. The later mathematical development, parameter exploration, assignment discussion, and full fitting argument remain to be outlined together.

**Working sequence:** Finish the outline together → identify or generate the required comparisons → interpret the results → reorganize and revise the manuscript using the substantial material already written.

No plots, analyses, or manuscript text were changed in creating this outline.
