# Chapter 4 drafting pass — 8 October 2026

Working manuscript: `Model_Chapter_Shared_Working_Draft.docx`.

Charles authorized direct editing after archiving the preceding version. This pass implements Alex’s PD44/PD45 direction, the Scholar VECTOR handoff, and Charles’s clarification that environmental effects on advancement require joint interpretation with selection, while SCORE and SELECT remain mathematically distinct operations.

## Organization of the revised chapter

1. **4.1 — The problem the model explains.** Motivation, scope, and “How peer environments shape later selection.” The officer example distinguishes the local unit from the broader promotion population.
2. **4.2 — A performance based selection benchmark.** Population, notation, scarcity, deterministic global top-K, and the compositional explanation for an unconditional peer-quality gradient.
3. **4.3 — Stochastic selection under a fixed capacity.** Exact-K sequential weighted sampling without replacement, conditional draw probabilities, temperature limits, and invariance. The selection temperature remains distinct from the historical MLE parameter.
4. **4.4 — Competitive congestion in the score.** Smooth relevance, full-group mean congestion, score adjustment, within-group rank preservation, and cross-group comparisons. The normalized measure is a concentration rather than an unscaled headcount.
5. **4.5 — Mathematical behavior and parameter regimes.** Derivatives, limiting cases, score crossings, penalty scale, scarcity, winner changes, and conditions under which plots are informative.
6. **4.6 — Generating artificial teams with controlled sorting.** ASSIGN appears here as a simulation device, with fixed roster capacities and metadata-based similarity preference. It is not presented as a coequal theory of advancement. The preferred H_sort explanation, full-group centroid convention, variance decomposition, and finite-population random reference are retained or developed.
7. **4.7 — What the completed mechanism experiments establish.** Documented 2014–2016 deterministic experiments, their settings and limits, and two existing 2015 figures. These figures were reused, not regenerated through new experiments.
8. **4.8 — The bridge to empirical fitting.** The historical softmax/Bernoulli fitting equations, jointly estimated parameters, and reasons they do not establish an exact-K fit.

**Appendix 4A** preserves the detailed fitting record, original source qualifications, alternative specifications, and legacy SELECT mismatch. **Appendix 4B** provides repository provenance. Development history is separated from the main model narrative without discarding dissertation-relevant technical material.

## Mathematical additions and limits

The new derivations are consequences of the declared equations, not newly executed experiments: score crossings as lambda varies; sigmoid sensitivity and the own-score derivative under full-group averaging; temperature limits and invariance; the cancellation of a common group penalty under fixed within-group selection; the within/between variance decomposition of H_sort; and its expected value (J−1)/(N−1) under uniform assignment into fixed nonempty group sizes.

The chapter does not claim a universal inverted-U theorem. It distinguishes changing winner identities from changing a plotted curve, and it explains sparse-tail and binning sensitivity. A formal developmental-benefit function is not introduced. A_i retains its interpretation as the characteristic supplied to the model, not automatically innate ability.

## Items still requiring scientific decisions or verification

- Determine which historical stochastic runs were affected by negative-score clipping, positive-score caps, or deterministic numerical fallbacks. The clean exact-K definition is stated separately from those implementation details.
- Resolve the historical MLE sample-window documentation: the saved label requests 2009–2021, while the inspected loader restricts to 2011–2021 and the saved count is eleven seasons.
- Revisit eventual-draft labels repeated across player-season rows, the one-expected-positive-per-season consequence of softmax/Bernoulli normalization, and outcome-based threshold construction before claiming calibrated advancement probabilities.
- Justify parameter transfer or fit the intended selection likelihood. Matching logits by reparameterization does not equate Bernoulli and exact-K likelihoods. No completed exact-K refit is asserted.
- Add final external scholarly citations alongside the existing repository provenance. The source appendix explicitly distinguishes these two types of reference.
- Choose any additional experiment only to address a specific unresolved scientific claim. This drafting pass executed no new model experiments, empirical outcome analyses, or parameter fits.

## Editing and verification

Equations are native, editable Word math. The document was rendered and visually reviewed, including equations and the two saved figures. Source material and the pre-edit manuscript were retained during preparation. Section references were updated to the new order. This is a substantive working draft for Charles and Alex to edit, not a claim that the unresolved fitting issues have been settled.
