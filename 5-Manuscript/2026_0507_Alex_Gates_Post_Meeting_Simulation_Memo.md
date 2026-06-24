# 2026-05-07 Alex Gates Post-Meeting Simulation Memo

Source transcript: `transcripts/20260507_Paper_Directions_10_ab_otter_ai_transcript.pdf`

Purpose: convert the raw advisor conversation into a usable research memo. This is not a polished paper section yet. It is the working interpretation of what Alex was pushing toward, what changed relative to the current Tier 1 narrative, and what simulations should be built next.

## 1. Bottom Line

The meeting shifted the center of gravity from "fit an inverted-U with a quadratic" toward "explain how the inverted-U can emerge from a minimal generative mechanism."

The promising mechanism is:

> Assortative sorting into local pools, combined with local comparison or local rank, can create the nonlinear advancement pattern.

In plainer language:

1. People have underlying ability or performance.
2. People are not placed randomly into local environments.
3. Higher-ability people tend to cluster in higher-quality local pools.
4. Selection/promotion is not based only on raw global ability; it also depends on comparison within the local pool.
5. When own ability and local rank both matter, high-quality pools can become places where strong people lose distinction because they are surrounded by other strong people.

That is the clean story Alex seemed most excited about.

## 2. What Alex Liked

Alex did not reject the local/global framing. He seemed to accept the core ingredients:

- local environments matter;
- global advancement is scarce or selective;
- the empirical pattern is nonlinear;
- local peer quality is a useful first empirical object;
- there is an internal tension between benefits from strong peers and costs from comparison/congestion;
- the model should eventually explain why the observed curve exists, not merely describe it.

The strongest point of agreement was that the phenomenon likely depends on local pools not being random. The important new language is **assortative sorting**: people of similar ability or status tend to cluster in similar local environments.

That means the empirical pool-quality variable is not just a descriptive measure. It may be evidence of an underlying sorting process.

## 3. What Alex Pushed Back On

Alex's major pushback was methodological:

> Do not make the quadratic curve the first principle of the model.

The quadratic is useful as an empirical diagnostic. It can summarize the inverted-U and produce a turning point \(Q^*\). But if the model begins by assuming:

\[
\Pr(Y_i=1) \approx \alpha + \beta_1 Q_i + \beta_2 Q_i^2
\]

then the nonlinearity is partly baked in from the start.

Alex wants a more natural evolution:

1. Begin with a bare model of promotion based on ability.
2. Add rank or comparison.
3. Add local pools.
4. Add nonrandom sorting into local pools.
5. See whether the nonlinear pattern appears from those ingredients.

The practical implication is that the quadratic should remain in the empirical notebook and narrative as a descriptive/fitting tool, but it should not be presented as the generative mechanism.

## 4. Revised Mechanism

The revised mechanism has three essential pieces.

### Piece 1 - Ability

Each individual has an underlying ability, performance, or quality:

\[
A_i
\]

For the first simulation, this can be drawn from a simple distribution such as:

\[
A_i \sim U(0,1)
\]

This creates the baseline world. In the most naive model, promotion probability is proportional to own ability:

\[
\Pr(Y_i=1) \propto A_i
\]

After normalization:

\[
\Pr(Y_i=1) =
\frac{A_i}{\sum_j A_j}
\]

Alex also mentioned the possibility of a Gibbs/softmax-style form:

\[
\Pr(Y_i=1) =
\frac{e^{A_i}}{\sum_j e^{A_j}}
\]

That is an extension. The first version can start with the simpler normalized ability form.

### Piece 2 - Comparison Or Rank

Selection may depend not only on raw ability but on rank:

\[
\gamma_i = \operatorname{rank}(A_i)
\]

The model can compare two worlds:

- promotion probability based on raw ability;
- promotion probability based on ability rank.

If ranking is global, this should still produce a monotone relationship. It should not by itself produce the local inverted-U.

The important point is conceptual: rank introduces comparison. Selection is no longer purely "how good are you?" It becomes "where do you stand relative to others?"

### Piece 3 - Local Pools With Assortative Sorting

Individuals are assigned to local pools:

\[
\ell_i \in \{1,\dots,L\}
\]

Each pool has a pool quality, for example:

\[
\pi_\ell = \frac{1}{n_\ell}\sum_{i:\ell_i=\ell} A_i
\]

The core modeling question is how individuals are assigned to pools.

Alex's key claim is that random assignment should not generate the main nonlinear effect. If people are randomly assigned to pools, local pool quality should have little systematic relationship with promotion probability.

The nonlinear effect should appear when local pools are correlated by ability:

> Higher-ability people are more likely to be grouped with other higher-ability people.

This is assortative sorting. It can happen through many real mechanisms:

- prestige sorting;
- selective hiring or recruiting;
- self-selection into high-status groups;
- evaluators sorting people into stronger local environments;
- institutional tracks such as honors classes, elite teams, prestigious departments, or high-visibility jobs.

Alex's point was not that we need to know the exact real sorting mechanism immediately. The first task is to show that some degree of assortative sorting plus local comparison can generate the pattern.

## 5. What "Congestion" Becomes

The term "congestion" is still useful, but Alex reframed it.

In the current narrative, congestion sounds like crowding: too many strong people competing for limited roles, minutes, attention, or recognition.

Alex's reframing is more structural:

> What we are calling congestion may be the observable consequence of correlated local pools plus local rank comparison.

In this view, the crucial fact is not simply that the pool is crowded. The crucial fact is that the local pool contains people who are similar in ability. When everyone around you is strong, your absolute ability may be high, but your local rank and distinctiveness may be lower.

So the vocabulary may evolve:

- **pool quality**: the average strength of the local environment;
- **assortative sorting**: the process that creates correlated local pools;
- **local rank/comparison**: the mechanism that converts pool composition into advantage or disadvantage;
- **congestion/crowding**: the experienced consequence when high-quality pools make distinction harder.

This is more theoretically powerful than treating congestion as just a second covariate.

## 6. The Simulation Program Alex Proposed

Alex's advice was to build the model in layers, not all at once.

### Simulation 1 - Ability Only

Create a mock population:

- \(N=100\) individuals;
- each individual gets ability \(A_i \sim U(0,1)\);
- select/promote \(K=10\) individuals using probabilities proportional to ability.

Run many repetitions, for example 1,000 simulated populations.

Plot:

- promotion probability versus ability \(A_i\);
- promotion probability versus global ability rank \(\gamma_i\).

Expected result:

- monotone relationship;
- no local-pool effect because there are no local pools yet.

Purpose:

- establish the naive meritocratic baseline.

### Simulation 2 - Global Rank

Use the same population, but base selection probability on global rank rather than raw ability.

Expected result:

- still monotone;
- still no local inverted-U;
- confirms that rank/comparison alone, when global, does not produce the local phenomenon.

Purpose:

- separate "selection by ability" from "selection by rank."

### Simulation 3 - Random Local Pools

Assign individuals randomly into equal-sized pools, for example:

- \(N=100\);
- \(L=10\) pools;
- \(10\) individuals per pool.

Compute each pool's mean ability:

\[
\pi_\ell
\]

Compute local rank:

\[
\gamma_{i\ell}
\]

Test promotion rules based on:

- own ability;
- global rank;
- local rank.

Plot:

- promotion probability versus own ability;
- promotion probability versus global rank;
- promotion probability versus pool quality \(\pi_\ell\).

Expected result:

- if pools are random, pool quality should be tightly clustered;
- local pool quality should not generate the main nonlinear pattern;
- this is the "null local-pool" condition.

Purpose:

- show that locality alone is not enough.

### Simulation 4 - Perfect Assortative Sorting

Sort individuals by ability and place similar individuals into the same pools:

- top ability group into top pool;
- next ability group into next pool;
- and so on.

This is the extreme case of assortative sorting.

Then use a promotion rule that includes local rank.

Expected result:

- the local-pool structure should now matter strongly;
- the relationship may become sawtooth, step-like, monotone, or otherwise too extreme;
- this is likely a useful limit case, not the final realistic model.

Purpose:

- show what happens when local sorting is maximized.

### Simulation 5 - Stochastic Assortative Sorting

Replace perfect sorting with a tunable sorting process.

There should be a parameter controlling how strongly ability predicts pool assignment:

\[
\rho
\]

where:

- \(\rho=0\): random assignment;
- intermediate \(\rho\): noisy/prestige/assortative sorting;
- high \(\rho\): near-perfect assortative sorting.

This is probably the most important simulation.

Expected result:

- at \(\rho=0\), little or no nonlinear pool-quality effect;
- at very high \(\rho\), possibly an overly strong or sawtooth pattern;
- at intermediate \(\rho\), the desired inverted-U may appear.

Purpose:

- test whether the empirical inverted-U can be generated by the interaction of ability, local comparison, and assortative sorting.

## 7. The Central Hypothesis After The Meeting

The new central hypothesis is:

> The inverted-U is not fundamentally caused by quadratic pool quality. It may emerge when individuals are assortatively sorted into local pools and evaluated through a mixture of own ability and local rank.

This preserves the old intuition but gives it a stronger mechanism.

Old framing:

> Stronger peers help at first, then hurt because of congestion.

Revised framing:

> Stronger local pools arise through sorting. They improve absolute environment quality, but they also change the individual's local rank and distinctiveness. The observed inverted-U may be the aggregate footprint of this sorting-plus-comparison process.

That is a much more network-science-compatible explanation.

## 8. Attrition As The Rival Mechanism

Alex also raised a second possible explanation:

> The nonlinear pattern might be driven by attrition or competing risks rather than local rank.

In basketball, Army, and academia, high-ability people can leave the focal advancement path:

- basketball players may transfer, stop playing, or pursue other options;
- Army officers may leave for civilian opportunities;
- academics may move institutions or leave academia.

If attrition is correlated with ability and local pool quality, then the observed nonlinear pattern could partly reflect who remains eligible for advancement, not only who wins local comparison.

Alex seemed to treat this as the less exciting but still important rival framework.

The immediate implication is:

- do not ignore attrition;
- but first test whether the sorting/local-rank mechanism can generate the effect without attrition.

If it can, then attrition can become an extension or robustness layer. If it cannot, attrition may be a necessary component.

## 9. What This Means For The Current Narrative Document

The existing narrative is still useful, but it needs a second-generation update.

Keep:

- competing local forces;
- distinction as the scarce object;
- local/global distinction;
- \(L\) as a reduced-form local environment;
- \(Q\) as the first empirical proxy;
- \(Q^*\) as a descriptive fitted object.

Revise:

- make clear that the quadratic is a descriptive approximation, not the generative assumption;
- add the naive ability-only baseline before the local term;
- introduce local rank/comparison as a core mechanism;
- introduce assortative sorting as the candidate mechanism that creates correlated local pools;
- describe congestion as the consequence of correlated local pools and local comparison, not only as raw crowding;
- put simulations before analytic fitting.

The new narrative order should probably be:

1. The empirical inverted-U.
2. Bare meritocratic baseline: own ability predicts advancement.
3. Global rank/comparison baseline.
4. Local pools by themselves.
5. Random local pools should not create the pattern.
6. Assortative sorting creates correlated local pools.
7. Local rank inside correlated pools creates the distinction tradeoff.
8. The inverted-U may emerge from the mixture of own ability and local rank.
9. The quadratic fit remains a descriptive diagnostic and way to summarize \(Q^*\).

## 10. Immediate Work Plan

Alex's practical instruction was clear: build simulations first.

The immediate deliverable before the next check-in should be a small simulation notebook or script that can generate:

1. ability-only baseline;
2. global-rank baseline;
3. random local-pool baseline;
4. perfectly assortative local-pool limit;
5. noisy assortative local-pool model with a tunable sorting parameter.

Each simulation should produce the same diagnostic plots:

- advancement probability versus own ability;
- advancement probability versus global rank;
- advancement probability versus local pool quality;
- advancement probability versus local rank, once local pools exist.

The key diagnostic question:

> Under which sorting rules does the local-pool-quality curve become inverted-U shaped?

## 11. Questions To Resolve Before Coding Too Much

The transcript suggests several open design choices.

1. What distribution should ability come from first?
   Start with uniform \(U(0,1)\), then test normal, lognormal, or empirical-like distributions.

2. How should promotion probabilities be normalized?
   Start with simple normalized ability or rank weights. Later test softmax/Gibbs forms.

3. How should global scarcity enter?
   Start by selecting \(K\) winners from \(N\) individuals. Later test threshold or probabilistic selection.

4. How should local rank be scored?
   Options include percentile rank, inverse rank, distance from local mean, or local z-score.

5. How should assortative sorting be tuned?
   Need a parameter that smoothly moves from random sorting to strong assortative sorting.

6. Should disassortative sorting be included?
   Yes, eventually. It may function as a contrast case against assortative sorting.

7. When should attrition be introduced?
   Not in the first simulation layer. Add it only after the sorting/local-rank mechanism is tested.

## 12. Why This Meeting Matters

This meeting was not a rejection of the Tier 1 work. It was a sharpening.

The original Tier 1 model found a useful empirical object: an inverted-U relating advancement to local peer quality. Alex's guidance points toward a deeper explanation:

> The curve may be a signature of how people are sorted into local pools and then evaluated through local comparison.

That is a stronger dissertation-level mechanism. It connects the basketball evidence to Army and academia more naturally because all three domains involve:

- ability or performance;
- sorting into local environments;
- local comparison;
- constrained advancement;
- imperfectly global evaluation.

If the simulations work, the paper can move from "we observe an inverted-U" to "we can generate the inverted-U from minimal assumptions about sorting and local rank."

That is the exciting part.
