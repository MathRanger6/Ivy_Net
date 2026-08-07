# PD18 Assortative Formation Literature & Modeling Notebook

**Project:** Cross-domain minimal model of local talent pools, finite
distinction, and advancement  
**Status:** Living research notebook  
**Started:** 2026-08-07 (PD18)

> **Working principle:** Basketball is the calibration sandbox, not the
> ontology. The intended model is a minimal, portable mechanism for
> agents entering finite local pools across basketball, Army
> advancement, and academic tenure.

## Immediate research question

Can one simple assortative network-formation rule generate realistic
overlapping local talent pools, preserve fixed finite group capacity,
and eliminate pre-drawn pool targets (T_j^\*), leaving (ho) as the sole
substantive ASSIGN-stage assortment control?

The broader sequence is:

**Empirical regularity → minimal mechanism → counterintuitive prediction
→ cross-domain validation.**

## PD18 mandate — source-derived

Alex’s requested search sequence is:

1.  Search first for **assortative growth models for bipartite
    networks**.
2.  If inadequate, study **assortative growth models for ordinary
    networks**.
3.  Determine whether a natural bipartite extension exists.
4.  Test whether **fixed and equal group size** preserves or breaks the
    assortativity mechanism.
5.  If the network route fails, broaden to **urn/combinatorial
    assortment models**.
6.  If no clean replacement survives, return to the existing (T_j^\*+ho)
    assignment code.

The hoped-for simplification is (A_i + T_j^\* + ho ightarrow ASSIGN)
becoming (A_i+hoightarrow ASSIGN), with (T_j) calculated afterward as a
realized descriptive property.

The central technical breakpoint is finite capacity: does imposing a
hard cap preserve the mapping from (ho) to realized assortativity, or do
late forced placements and saturated pools distort the mechanism?

## Cross-domain design lock

The ontology to protect is:

**Agents with ability → assortative formation ((ho)) → finite local
pools → local comparison/congestion → SCORE → scarce SELECT.**

Basketball instantiates agents as players and pools as teams. Army may
instantiate them as officers and units/cohorts/competitive pools.
Academia may instantiate them as scholars and
departments/fields/evaluation neighborhoods.

**Do not prefer a mechanism merely because it is realistic for NCAA
recruiting. Cross-domain portability is a model-selection criterion.**

## ASSIGN / SCORE / SELECT separation

1.  **ASSIGN:** Which local pool does an agent enter?
2.  **SCORE:** How does ability interact with local context/congestion?
3.  **SELECT:** How are finite advancement slots allocated?

PD18 concerns **ASSIGN only**.

## Empirical basketball diagnostic

PD17 shows that real roster talent windows overlap substantially, have
heterogeneous nonzero widths, and are unlike disjoint sort-and-chop
slices.

Desired qualitative transition:

- low (ho) → broad mixing / high overlap;
- higher (ho) → stronger within-pool similarity / narrower overlap.

Track interval coverage, maximum coverage, fraction of talent grid
covered by multiple pools, mean/median pool span, realized (T_j),
within-pool variance, realized assortativity, and sensitivity to
capacity saturation/formation order.

Exact empirical curve fitting is not the immediate objective.

## Literature search map

### Tier 1 — Assortative bipartite growth

Search homophilic bipartite attachment, affiliation-network growth,
actor-group formation, and capacity-constrained bipartite attachment.

**Status:** Active. Initial scholarly search has not yet revealed an
obvious canonical model satisfying all constraints. This is preliminary.

### Tier 2 — Assortative ordinary-network growth

Study preferential attachment with homophily, similarity-biased
attachment, preference-function models, and attribute-conditioned
attachment. Determine what the published assortment parameter controls
and whether it survives bipartite translation.

### Tier 3 — Fixed-capacity/fixed-margin ensembles

Bipartite configuration models, hard-margin nulls, constrained ERGMs,
Gibbs matching, and degree-preserving swaps with homophily statistics.

**Status:** Promising fallback, but not a substitute for doing the
requested growth-model search first.

### Tier 4 — Urn/combinatorial assortment

Biased urn allocation, weighted sampling without replacement, noncentral
hypergeometric models, and constrained random partitions.

## Initial literature leads — provisional

### Newman — assortative mixing

Foundational for defining assortative/disassortative mixing and realized
assortativity. It does not itself solve finite-capacity generative
formation.

### Romanescu (2024) — preference functions and assortative mixing

High-priority candidate connecting explicit preference functions to
controlled assortative mixing. Key questions: Is the parameter
generative? Does the model require unbounded degree? Can it be ported to
an agent-pool bipartite graph? Does hard equal capacity preserve
monotonic realized assortment?

### Bipartite configuration / hard-margin models

Strong mathematical fallback because agent degree 1 and pool degree (r)
can be imposed exactly. Concern: this may be constrained assignment
rather than network growth.

## Candidate Rule A — capacity-constrained assortative growth

**Status:** Placeholder, not endorsed.

Generic form: (P(iightarrow j)K_ho(A_i,S_j) I(n_j\<r)), where (S_j) is
an emergent property of current membership rather than a pre-drawn
target.

Attractions: one assortment parameter, growth interpretation, emergent
(T_j).

Risks: early members can become implicit stochastic targets; saturated
pools disappear; late placements may be driven by capacity rather than
(ho).

## Candidate Rule B — fixed-degree assortative ensemble

**Status:** Strong fallback, intentionally demoted until growth
literature is reviewed.

Restrict legal assignments so every agent belongs to one pool and every
pool has (r) agents. Define a within-pool similarity statistic such as

(H(G)=-*j*{ij}(A_i-ar A_j)^2)

and distribution

(P(G\|A,ho)).

Advantages: exact capacities, one assortment parameter, no (T_j^\*),
emergent (T_j), portable abstraction.

Concern: ensemble/matching rather than clearly network growth.

## Capacity distortion test

For every serious growth candidate ask:

1.  Is realized assortment monotonic in (ho)?
2.  Does capacity merely rescale the relationship?
3.  Does capacity create saturation/flattening?
4.  Do late forced placements reverse assortment?
5.  Does formation order matter?
6.  Are empirical-like overlapping intervals still produced?

A finite cutoff is acceptable only if it does not destroy the mechanism
being claimed.

## Wang-style minimality test

Evaluate every candidate on:

- **Minimality:** Is (ho) the only substantive ASSIGN knob?
- **Emergence:** Does (T_j) emerge?
- **Capacity:** Are equal finite pools cleanly handled?
- **Interpretability:** Can (ho) be explained in one sentence?
- **Portability:** Can the same rule be relabeled across domains?
- **Prediction:** Does it generate consequences not used in calibration?
- **Separation:** Is ASSIGN distinct from SCORE and SELECT?
- **Empirical plausibility:** Can it generate overlapping pool windows?
- **Network value:** Is it genuinely a network-formation mechanism?

## Prediction horizon — not calibration targets

Potential future prediction families, not current claims:

- near-threshold agents may be more sensitive to local congestion;
- the local-talent effect may shift with scarcity (K/N);
- assortment may create non-monotonic environment effects;
- comparative statics may survive across basketball, Army, and academia.

These should emerge from the mechanism rather than be programmed into
it.

## Parked/rejected ideas

- **Exact empirical curve fitting:** parked.
- **NCAA-specific recruiting logic:** rejected as foundational
  abstraction.
- \*\*Pre-drawn (T_j^\*):\*\* parked, not deleted; current code remains
  fallback.
- **Immediate Gibbs matching adoption:** parked pending
  growth-literature review.

## Open questions

1.  Strongest canonical assortative bipartite growth paper?
2.  Is its assortativity attribute similarity, degree-degree
    correlation, or both?
3.  Which notion maps to desired (ho)?
4.  Can homophilic attachment operate without exogenous pool attributes?
5.  Does the first member become a hidden target?
6.  Can hard capacity be imposed analytically?
7.  Does capacity preserve monotonic control of assortment?
8.  How severe are end-stage forced assignments?
9.  Is simultaneous constrained matching cleaner than sequential growth?
10. If growth fails, which urn model is closest?
11. Which empirical statistic should calibrate (ho)?
12. Which quantities should remain invariant across domains?

## Immediate research plan

1.  **Literature:** identify 3–5 papers establishing the closest
    legitimate mechanism.
2.  **Mathematical translation:** write each serious candidate as an
    explicit attachment/assignment probability.
3.  **Capacity audit:** determine how hard capacity changes the process.
4.  **Minimal prototype:** change ASSIGN only.
5.  **PD17 comparison:** run existing overlap diagnostics across (ho).
6.  **Decision:** GO, PIVOT, or REVERT.

## Current position — 2026-08-07

The literature path is credible enough to justify the weekend
exploration, but no direct solution has yet been established.

Current ordering:

1.  assortative bipartite growth;
2.  bipartite extension of ordinary assortative growth;
3.  fixed-degree assortative ensemble;
4.  urn/constrained partition model;
5.  existing (T_j^\*+ho) baseline.

Decision criteria: **minimality, capacity stability, portability,
predictive usefulness**.

## Decision log

### 2026-08-07 — PD18

Investigate whether assortative network formation can remove (T_j^\*)
from ASSIGN. Equal finite group size is the hard constraint. Preserve
current code as fallback.

### 2026-08-07 — Cross-domain clarification

Treat all candidates as domain-agnostic local-pool formation rules.

**Lock: Basketball is the calibration sandbox, not the ontology.**

## Sources and reading queue

### Project source

- `20260807_Paper_Directions_18_otter_ai_transcript.docx` — primary
  source for PD18 mandate, search sequence, capacity concern, and
  network-extension motivation.

### Initial scholarly-search leads

- Newman — assortative mixing framework.
- Romanescu, R. G. (2024), *Building a network with assortative mixing
  starting from preference functions, with application to the spread of
  epidemics*, Frontiers in Physics.
- Bipartite configuration/hard-margin ensemble literature.
- Homophilic and attribute-based preferential-attachment literature.
- Urn and constrained-allocation literature.

## Update protocol

For each research round:

1.  Preserve earlier decisions unless explicitly superseded.
2.  Date substantive updates.
3.  Distinguish source-derived facts, published-literature findings, our
    inference, and candidate decisions.
4.  Move rejected approaches rather than deleting them.
5.  For each serious paper record its exact generative rule, role of
    assortativity, bipartite status, capacity behavior, portability, and
    verdict.
6.  Refresh **Current Position** after each major round.
7.  Keep the notebook readable when rendered to PDF.

------------------------------------------------------------------------

*End of initial PD18 notebook — 2026-08-07.*
