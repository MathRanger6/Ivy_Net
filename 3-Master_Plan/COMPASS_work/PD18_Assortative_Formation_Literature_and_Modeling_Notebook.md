# PD18 Assortative Formation Literature & Modeling Notebook

**Last synced:** 2026-08-07 **Project:** Cross-domain minimal model of
local talent pools, finite distinction, and advancement  
**Status:** Living research notebook  
**Started:** 2026-08-07 (PD18)

**Standalone:** This notebook contains the current PD18 research
question, design locks, candidate mechanisms, literature path, and
decision log; no other file is required to follow the argument.

> **Working principle:** Basketball is the calibration sandbox, not the
> ontology. The intended model is a minimal, portable mechanism for
> agents entering finite local pools across basketball, Army
> advancement, and academic tenure.

------------------------------------------------------------------------

## Immediate research question

Can one simple assortative network-formation rule generate realistic
overlapping local talent pools, preserve fixed finite group capacity,
and eliminate pre-drawn pool targets $T_{j^*}$, leaving $\rho$ as the
sole substantive ASSIGN-stage assortment control?

The broader sequence is:

**Empirical regularity → minimal mechanism → counterintuitive prediction
→ cross-domain validation.**

------------------------------------------------------------------------

## PD18 mandate — source-derived

Alex's requested search sequence is:

1.  Search first for **assortative growth models for bipartite
    networks**.
2.  If inadequate, study **assortative growth models for ordinary
    networks**.
3.  Determine whether a natural bipartite extension exists.
4.  Test whether **fixed and equal group size** preserves or breaks the
    assortativity mechanism.
5.  If the network route fails, broaden to **urn/combinatorial
    assortment models**.
6.  If no clean replacement survives, return to the existing
    $T_{j^*} + \rho$ assignment code.

The hoped-for simplification is:

$$
A_i + T_{j^*} + \rho \rightarrow \text{ASSIGN}
$$

becoming:

$$
A_i + \rho \rightarrow \text{ASSIGN},
$$

with $T_j$ calculated afterward as a realized descriptive property.

The central technical breakpoint is finite capacity: does imposing a
hard cap preserve the mapping

$$
\rho \rightarrow \text{realized assortativity},
$$

or do late forced placements and saturated pools distort the mechanism?

------------------------------------------------------------------------

## Cross-domain design lock

The ontology to protect is:

$$
\text{Agents with ability } A_i
\overset{\rho}{\longrightarrow}
\text{finite local pools}
\longrightarrow
\text{local comparison/congestion}
\longrightarrow
\text{SCORE}
\longrightarrow
\text{scarce SELECT}.
$$

Basketball instantiates agents as players and pools as teams. Army may
instantiate them as officers and units/cohorts/competitive pools.
Academia may instantiate them as scholars and
departments/fields/evaluation neighborhoods.

**Do not prefer a mechanism merely because it is realistic for NCAA
recruiting. Cross-domain portability is a model-selection criterion.**

------------------------------------------------------------------------

## ASSIGN / SCORE / SELECT separation

1.  **ASSIGN:** Which local pool does an agent enter?
2.  **SCORE:** How does ability interact with local context/congestion?
3.  **SELECT:** How are finite advancement slots allocated?

PD18 concerns **ASSIGN only**.

The downstream scoring rule remains conceptually separate:

$$
S_i = A_i - \lambda L_C
$$

and the current winner rule remains top-$K$ unless explicitly changed in
a later stage.

------------------------------------------------------------------------

## Empirical basketball diagnostic

PD17 shows that real roster talent windows overlap substantially, have
heterogeneous nonzero widths, and are unlike disjoint sort-and-chop
slices.

Desired qualitative transition:

$$
\text{low } \rho
\rightarrow
\text{broad mixing / high overlap}
$$

$$
\text{higher } \rho
\rightarrow
\text{stronger within-pool similarity / narrower overlap}.
$$

Track:

- interval coverage curve;
- maximum coverage;
- fraction of the talent grid covered by more than one pool;
- mean and median pool span;
- distribution of realized $T_j$;
- within-pool variance;
- realized assortativity;
- sensitivity to capacity saturation;
- sensitivity to formation order.

Exact empirical curve fitting is not the immediate objective.

------------------------------------------------------------------------

## Literature search map

### Tier 1 — Assortative bipartite growth

Search homophilic bipartite attachment, affiliation-network growth,
actor-group formation, and capacity-constrained bipartite attachment.

**Status:** Active. Initial scholarly search has not yet revealed an
obvious canonical model satisfying all constraints. This is preliminary.

### Tier 2 — Assortative ordinary-network growth

Study preferential attachment with homophily, similarity-biased
attachment, preference-function models, and attribute-conditioned
attachment.

**Required question:** What does the published assortment parameter
actually control, and does that mathematical object survive bipartite
translation?

### Tier 3 — Fixed-capacity / fixed-margin ensembles

Candidate families:

- bipartite configuration models;
- hard-margin bipartite null models;
- constrained exponential random graph models;
- Gibbs matching;
- degree-preserving swaps with homophily statistics.

**Status:** Promising fallback, but not a substitute for doing the
requested growth-model search first.

### Tier 4 — Urn / combinatorial assortment

Candidate families:

- biased urn allocation;
- weighted sampling without replacement;
- noncentral hypergeometric models;
- constrained random partitions.

**Status:** Explicit fallback if finite capacity makes the
network-growth formulation unnatural.

------------------------------------------------------------------------

## Initial literature leads — provisional

These are **scholarly-search leads**, not yet fully adjudicated core
citations.

### Newman — assortative mixing

**Role:** Foundational framework for defining assortative and
disassortative mixing.

**Useful for:** Measurement and language.

**Does not yet solve:** Generative formation under exact finite group
capacity.

### Romanescu (2024) — preference functions and assortative mixing

**Role:** High-priority candidate connecting an explicit preference
function to controlled assortative mixing.

Key questions:

1.  Is the parameter generative or descriptive?
2.  Does the model require unbounded degree?
3.  Can the preference rule be ported to an agent-pool bipartite graph?
4.  What happens when one mode has hard equal capacity?
5.  Does realized assortativity remain monotonic under the cap?

### Bipartite configuration / hard-margin models

**Role:** Mathematical fallback for exact capacities.

**Attraction:** Every agent can have degree 1 and every pool degree $r$
by construction.

**Concern:** This may be better described as constrained assignment than
network *growth*, sacrificing some of the generative network-science
value sought in PD18.

------------------------------------------------------------------------

## Candidate Rule A — capacity-constrained assortative growth

**Status:** Placeholder, not endorsed.

A generic candidate rule is:

$$
P(i \rightarrow j)
\propto
K_{\rho}(A_i,S_j)\,
\mathbf{1}(n_j < r),
$$

where:

- $A_i$ = ability of agent $i$;
- $S_j$ = an **emergent** property of the current members of pool $j$;
- $n_j$ = current pool size;
- $r$ = fixed pool capacity;
- $K_{\rho}$ = similarity kernel controlled by $\rho$.

Possible definitions of $S_j$:

- current pool mean;
- current pool distribution;
- similarity to existing members.

### Attraction

- one visible assortment parameter;
- simple growth interpretation;
- $T_j$ emerges after formation.

### Failure risks

- early members may become implicit stochastic targets;
- saturated pools disappear from the choice set;
- late placements may be driven more by capacity than by $\rho$.

The decisive question is whether hard capacity distorts the intended
assortment mechanism.

------------------------------------------------------------------------

## Candidate Rule B — fixed-degree assortative ensemble

**Status:** Strong fallback, intentionally demoted until the growth
literature is reviewed.

Restrict legal assignments so every agent belongs to exactly one pool
and every pool has exactly $r$ agents.

Define a within-pool similarity statistic:

# \$\$ H(G)

-\sum_j \sum\_{i \in j} \left(A_i-\bar{A}\_j\right)^2 \$\$

and a one-parameter distribution over legal assignments:

$$
P(G \mid A,\rho)
\propto
\exp\left\{\rho H(G)\right\}.
$$

Interpretation:

- $\rho = 0$: uniform balanced random partition;
- increasing $\rho$: increasing within-pool similarity;
- very large $\rho$: increasingly segregated pools.

### Advantages

- exact capacities;
- one assortment parameter;
- no $T_{j^*}$;
- realized $T_j$ emerges;
- portable abstraction.

### Concern

This is an ensemble/matching mechanism rather than clearly a
network-growth mechanism.

------------------------------------------------------------------------

## Capacity distortion test

For every serious growth candidate, compare the relationship

$$
\rho
\rightarrow
r_{\text{realized}}^{\text{unbounded}}
$$

with

$$
\rho
\rightarrow
r_{\text{realized}}^{\text{bounded}}.
$$

The notation above is conceptual: $r_{\text{realized}}$ denotes the
realized assortativity statistic, not roster size.

Ask:

1.  Is realized assortment monotonic in $\rho$?
2.  Does capacity merely rescale the relationship?
3.  Does capacity create saturation or flattening?
4.  Do late forced placements reverse assortment?
5.  Does formation order matter?
6.  Are empirical-like overlapping intervals still produced?

A finite cutoff is acceptable only if it does not destroy the mechanism
being claimed.

------------------------------------------------------------------------

## Wang-style minimality test

Evaluate every candidate on:

- **Minimality:** Is $\rho$ the only substantive ASSIGN knob?
- **Emergence:** Does $T_j$ emerge rather than being pre-specified?
- **Capacity:** Are equal finite pools cleanly handled?
- **Interpretability:** Can $\rho$ be explained in one sentence?
- **Portability:** Can the same rule be relabeled across basketball,
  Army, and academia?
- **Prediction:** Does it generate consequences not used in calibration?
- **Separation:** Is ASSIGN distinct from SCORE and SELECT?
- **Empirical plausibility:** Can it generate overlapping pool windows?
- **Network value:** Is it genuinely a network-formation mechanism
  rather than network vocabulary applied after the fact?
- **Temporal extensibility:** Can the snapshot formation rule be
  iterated for reassignment without changing the meaning of $\rho$?

------------------------------------------------------------------------

## Prediction horizon — not calibration targets

Potential future prediction families, **not current claims**:

### Threshold sensitivity

Near-threshold agents may be more sensitive to local congestion than
clearly dominant or clearly noncompetitive agents.

### Scarcity interaction

The effect of local talent concentration may shift systematically with
selectivity:

$$
K/N.
$$

### Non-monotonic environment effect

Increasing assortment may initially improve environment quality while
eventually increasing local competition enough to reduce advancement
probability for some agents.

### Cross-domain invariance

If the mechanism is truly generic, qualitatively similar comparative
statics should survive when “team” is replaced by Army or academic
local-pool structure.

These should emerge from the mechanism rather than be programmed into
it.

------------------------------------------------------------------------

## Parked / rejected ideas

### Exact empirical curve fitting

**Parked.** Current aim is qualitative mechanism validation, not tuning
$\rho$ until one basketball curve is reproduced exactly.

### NCAA-specific recruiting logic

**Rejected as the foundational abstraction** because it compromises
cross-domain portability.

### Pre-drawn $T_{j^*}$

**Parked, not deleted.** Existing code remains the fallback if the
network excursion fails.

### Immediate Gibbs matching adoption

**Parked pending the requested growth-literature review.**

------------------------------------------------------------------------

## Open questions

1.  What is the strongest canonical paper on assortative bipartite
    growth?
2.  Is “assortativity” in that literature attribute similarity,
    degree-degree correlation, or both?
3.  Which notion corresponds to the desired $\rho$?
4.  Can homophilic attachment operate without an exogenous pool
    attribute?
5.  Does the first member become a hidden target?
6.  Can hard capacity be imposed analytically?
7.  Does capacity preserve monotonic control of realized assortment?
8.  How severe are end-stage forced assignments?
9.  Is simultaneous constrained matching cleaner than sequential growth?
10. If growth fails, which urn model is the closest one-parameter
    analogue?
11. What empirical statistic should calibrate $\rho$?
12. Which quantities should remain invariant across domains?

------------------------------------------------------------------------

## Immediate research plan

### Step 1 — Literature

Identify 3–5 papers that collectively establish the closest legitimate
mechanism.

### Step 2 — Mathematical translation

For every serious candidate, write the actual rule:

$$
P(\text{attachment or assignment}
\mid
A,\rho,\text{current state}).
$$

### Step 3 — Capacity audit

Determine how hard capacity changes the process.

### Step 4 — Minimal prototype

Implement the smallest viable candidate without changing SCORE or
SELECT.

### Step 5 — PD17 comparison

Run the existing overlap diagnostics across a small $\rho$ sweep.

### Step 6 — Decision

**GO:** clean $\rho$-only mechanism + plausible pools + capacity-stable
assortment.  
**PIVOT:** growth fails but fixed-margin or urn model is promising.  
**REVERT:** restore $T_{j^*}+\rho$.

------------------------------------------------------------------------

## Current position — 2026-08-07

The literature path is credible enough to justify the weekend
exploration, but no direct solution has yet been established.

Current ordering:

1.  assortative bipartite growth;
2.  bipartite extension of ordinary assortative growth;
3.  fixed-degree assortative ensemble;
4.  urn/constrained partition model;
5.  existing $T_{j^*}+\rho$ baseline.

Decision criteria:

**minimality, capacity stability, portability, predictive usefulness.**

------------------------------------------------------------------------

## Decision log

### 2026-08-07 — PD18

**Decision:** Investigate whether assortative network formation can
remove $T_{j^*}$ from ASSIGN.

**Reason:** Simplification, network-science foundation, and
extensibility.

**Hard constraint:** Equal finite group size may break ordinary growth
behavior and must be tested.

**Fallback:** Preserve current assignment code.

### 2026-08-07 — Cross-domain clarification

**Decision:** Treat all candidates as domain-agnostic local-pool
formation rules.

**Lock:** **Basketball is the calibration sandbox, not the ontology.**

------------------------------------------------------------------------


### 2026-08-07 — Temporal affiliation literature update

**Decision:** Expand the search vocabulary from static bipartite formation to **dynamic group affiliation**, **temporal affiliation networks**, and **higher-order group dynamics**.

**Reason:** The one-agent/one-pool constraint is cross-sectional. In many domains, agents can move among finite pools over time.

**New priority read:** Geard & Bullock (2010), *Competition and the Dynamics of Group Affiliation*, followed by Quayle et al. (2006), Nikolaev & Mneimneh (2023), and Iacopini et al. (2024).

**Modeling implication:** Evaluate candidate mechanisms not only for snapshot capacity stability and cross-domain portability, but also for whether repeated reassignment can preserve the substantive meaning of $\rho$.

---

## Sources and reading queue

### Project source

- `20260807_Paper_Directions_18_otter_ai_transcript.docx` — primary
  source for PD18 mandate, search sequence, capacity concern, and
  network-extension motivation.

### Initial scholarly-search leads

- Newman — assortative mixing framework.
- Romanescu, R. G. (2024), *Building a network with assortative mixing
  starting from preference functions, with application to the spread of
  epidemics*, *Frontiers in Physics*.
- Bipartite configuration / hard-margin ensemble literature.
- Homophilic and attribute-based preferential-attachment literature.
- Urn and constrained-allocation literature.

------------------------------------------------------------------------

## Update protocol

For each research round:

1.  Preserve earlier decisions unless explicitly superseded.
2.  Date substantive updates.
3.  Distinguish **source-derived facts**, **published-literature
    findings**, **our inference**, and **candidate decisions**.
4.  Move rejected approaches rather than deleting them.
5.  For each serious paper record:
    - exact generative rule;
    - role of assortativity parameter;
    - bipartite status;
    - capacity behavior;
    - portability;
    - verdict.
6.  Refresh **Current Position** after each major round.
7.  Keep the notebook readable when rendered to PDF.

------------------------------------------------------------------------

*End of initial PD18 notebook — 2026-08-07.*

------------------------------------------------------------------------

# Appendix A — Assortative Bipartite Formation: Initial Reading Path

**Added:** 2026-08-07  
**Status:** Preliminary literature reconnaissance; papers below are
leads for deeper mathematical adjudication, not yet endorsed as the PD18
formation rule.

## A.1 Updated literature position

The initial search can now be stated more precisely.

There **are** specific papers worth reading on assortative network
growth, bipartite/affiliation-network growth, and related actor-group
formation. What has **not** yet emerged is a single canonical paper that
simultaneously supplies all of the ingredients required by PD18:

$$
\text{assortative growth}
\cap
\text{bipartite agent--pool formation}
\cap
\text{hard equal pool capacity}.
$$

The literature therefore appears to contain strong candidates in the
first two components, while the fixed-capacity requirement remains the
likely technical breakpoint.

This matters because the PD18 object is not merely an arbitrary
bipartite network. The desired abstraction imposes a particularly
restrictive degree structure:

$$
d_i = 1,
\qquad
d_j = r,
$$

where every agent belongs to exactly one local pool and every pool
contains exactly $r$ agents.

The central research question is therefore becoming:

> Can an established assortative-growth mechanism be translated into an
> actor-to-pool bipartite formation process while preserving meaningful
> control by $\rho$ after hard equal capacity is imposed?

### Snapshot constraint versus longitudinal structure

The requirement that every agent occupy exactly one finite local pool
should be interpreted **cross-sectionally**, not as a lifetime
affiliation constraint. At any observation time $t$, the stylized
assignment structure is:

$$
d_i(t)=1,
\qquad
d_j(t)\le r,
$$

or, in the equal-capacity version of the model:

$$
d_j(t)=r.
$$

Longitudinally, however, an agent may move through a sequence of
affiliations:

$$
i:\quad j_1 \rightarrow j_2 \rightarrow j_3 \rightarrow \cdots
$$

The more general object can therefore be understood as a **temporal
bipartite affiliation network**:

$$
G(t)=\left(A,P,E(t)\right),
$$

where the agent set $A$ may persist, pools $P$ may persist or change,
and membership edges $E(t)$ can dissolve and reform through time.

The persistence of those affiliations can differ substantially by
domain. NCAA men's basketball and the tenure-stage university
affiliation of many academics may be relatively sticky over the relevant
observation window, whereas Army careers commonly involve repeated
reassignment across units or other local organizational pools. Thus,
“one agent, one pool” means **one contemporaneous pool at a snapshot**,
not “one pool for life.”

The immediate PD18 problem remains formation of a single cross-sectional
assignment. A successful domain-general mechanism should, however,
ideally admit temporal iteration without changing its core assortative
logic. In a later dynamic extension, the same basic formation rule could
be reapplied when memberships dissolve and agents become eligible for
reassignment:

$$
P(i\rightarrow j \text{ at } t)
\propto
K_\rho\left(A_i,S_j(t)\right)
\mathbf{1}\left(n_j(t)<r_j(t)\right).
$$

This suggests an additional evaluation criterion for candidate
mechanisms:

> **Temporal extensibility:** Can the static formation mechanism
> naturally become a reassignment mechanism across periods without
> changing the substantive meaning of $\rho$?

This distinction strengthens the network interpretation. The target is
not a permanently fixed partition of agents, but a cross-sectional
capacity-constrained affiliation structure that may be embedded in a
longer sequence of assignments.


## A.2 Temporal wrinkle — revised literature path

**Update:** Interpreting the one-agent/one-pool condition as a **snapshot constraint** materially improves the literature search. The relevant vocabulary is not only “bipartite network formation,” but also **dynamic group affiliation**, **temporal affiliation networks**, and **higher-order group dynamics**.

This suggests that the primitive mechanism may be better described as:

$$
\text{agents}
+
\text{assortative affiliation}
+
\text{capacity-limited local pools}
$$

rather than simply “form a bipartite network.” The bipartite graph is then the mathematical representation of contemporaneous affiliations at time $t$.

Across periods, the same logic can in principle generate a sequence:

$$
G_1 \rightarrow G_2 \rightarrow \cdots \rightarrow G_T,
$$

with agents remaining in or moving among pools while the substantive meaning of $\rho$ remains stable.

### New priority lead — Geard & Bullock (2010)

**Citation:** Geard, N., & Bullock, S. (2010). *Competition and the dynamics of group affiliation.* *Advances in Complex Systems*.  
https://www.worldscientific.com/doi/abs/10.1142/S0219525910002712

**Why it moved to the front:** A targeted search on dynamic group affiliation surfaced this paper as an explicit **group-formation process** involving competition and homophily. Search metadata also points to a capacity/cost constraint on groups. That combination is unusually close to the PD18 problem:

$$
\text{agents}
+
\text{groups}
+
\text{homophily}
+
\text{competition}
+
\text{capacity}
+
\text{dynamic affiliation}.
$$

This may be a more direct conceptual fit than beginning with a generic assortative network-growth model and then translating it into actor-to-pool language.

**Evidence caution:** The publisher blocked full-text extraction during the initial reconnaissance. The description above is therefore based on scholarly-search metadata and abstract-level evidence and must be verified against the paper itself before its equations or capacity mechanism are adopted.

**Deep-reading questions:**

1. What is the exact group-affiliation rule?
2. How is homophily represented mathematically?
3. What does “competition” mean in the model?
4. What exactly is capacity-limited: agents, groups, resources, or affiliation opportunities?
5. Are memberships persistent, dissolvable, or repeatedly re-formed?
6. Can the model produce a snapshot in which every agent has exactly one affiliation?
7. Can equal pool capacity be imposed without adding another substantive mechanism parameter?
8. Is there a natural quantity that could play the role of our $\rho$?
9. Does the mechanism preserve a stable interpretation of assortment across repeated reassignment?

**Preliminary PD18 role:** New first-read candidate because it may join group affiliation, homophily, competition, capacity, and temporal movement in a single modeling framework.

### New temporal anchor — Iacopini, Karsai & Barrat (2024)

**Citation:** Iacopini, I., Karsai, M., & Barrat, A. (2024). *The temporal dynamics of group interactions in higher-order social networks.* *Nature Communications*.  
https://www.nature.com/articles/s41467-024-50918-5

**Why it matters:** This recent paper explicitly studies how individuals' group memberships change through time in higher-order social networks. Search metadata describes group change and selection together with homophily, and the paper cites Geard & Bullock as relevant prior work.

That creates a potentially useful literature lineage:

$$
\text{Geard \& Bullock (2010)}
\rightarrow
\text{dynamic group affiliation}
\rightarrow
\text{Iacopini et al. (2024)}.
$$

The newer paper may help distinguish which aspects of dynamic group membership are now considered structurally important and which older mechanisms have survived into contemporary higher-order network modeling.

**Preliminary PD18 role:** Modern temporal-group benchmark and possible bridge from static affiliation formation to repeated reassignment.

### Broader dynamic-homophily context

Two additional literatures become relevant but are not currently ahead of the group-affiliation papers:

- **Jackson, Nei, Snowberg & Yariv (2023), *The Dynamics of Networks and Homophily*.** NBER Working Paper 30815.  
  https://www.nber.org/papers/w30815
- **Graham — dynamic network formation with homophily and transitivity.**

These are useful for understanding homophily in evolving networks generally, but they are less directly aligned with the immediate finite group-affiliation problem than Geard & Bullock.

### Revised conceptual language

The temporal interpretation suggests a potentially cleaner domain-general description of ASSIGN:

> **Agents assortatively affiliate with capacity-limited local pools.**

At any snapshot, those affiliations can be represented as a bipartite network. Longitudinally, memberships may dissolve and reform, producing repeated cross-sectional networks.

This language travels naturally across domains:

- player → team;
- officer → unit;
- academic → institution/department;
- employee → work group;
- scientist → collaboration/team.

The key modeling requirement is that repeated assignment should not require redefining what $\rho$ means.

### Revised reading order

The current priority order is now:

1. **Geard & Bullock (2010)** — *Competition and the Dynamics of Group Affiliation*.
2. **Quayle, Siddiqui & Jones (2006)** — *Modeling Network Growth with Assortative Mixing*.
3. **Nikolaev & Mneimneh (2023)** — affiliation-network growth architecture.
4. **Iacopini, Karsai & Barrat (2024)** — temporal dynamics of group interactions.
5. **Lomi et al. (2014)** — organizational bipartite formation and assortative mixing.
6. **Giroire et al. (2022)** — hypergraph/group representation alternative.

The immediate research strategy is therefore no longer simply to combine Quayle's assortative mechanism with Nikolaev–Mneimneh's affiliation architecture. First determine whether **Geard & Bullock already provides a closer group-affiliation mechanism**, and then use the other papers to fill whatever mathematical pieces remain missing.

## A.3 Priority reading 1 — Quayle, Siddiqui & Jones (2006)

**Citation:** Quayle, A. P., Siddiqui, A. S., & Jones, S. J. M. (2006).
*Modeling network growth with assortative mixing.* *The European
Physical Journal B*.  
<https://link.springer.com/article/10.1140/epjb/e2006-00170-5>

**Why it matters:** This is the clearest initial lead on the
**assortative-growth** side of the problem. It explicitly concerns
generative network growth with assortative mixing rather than merely
measuring assortativity after a network has formed.

The scholarly search record also indicates that the paper discusses
bipartite modeling in developing or situating its mechanism. That makes
it a high-priority bridge candidate, but the publisher full text was not
retrievable during the initial search. Accordingly, no claim is yet made
that its bipartite component directly supplies the PD18 actor-to-pool
mechanism.

**Questions to extract during deep reading:**

1.  What is the exact attachment probability?
2.  What parameter controls assortative mixing?
3.  Is assortment based on node degree, node attributes, or another
    state variable?
4.  Does the model require unbounded growth?
5.  Can the preference mechanism be rewritten for an agent choosing
    among pools?
6.  What mathematical feature would be altered by imposing $n_j \le r$?
7.  Does the original mechanism imply a monotonic relationship between
    its assortment parameter and realized assortativity?

**Preliminary PD18 role:** Best current starting point for the
assortative-growth mechanism itself.

## A.4 Priority reading 2 — Nikolaev & Mneimneh (2023)

**Citation:** Nikolaev, A., & Mneimneh, S. (2023). *Modeling and
analysis of affiliation networks with preferential attachment and
subsumption.* *Physical Review E, 108*, 014310.  
<https://journals.aps.org/pre/abstract/10.1103/PhysRevE.108.014310>

**Why it matters:** An affiliation network is structurally close to the
ontology required by PD18: one mode represents actors and the other
represents groups or affiliations, with an edge indicating membership.

This paper therefore appears particularly valuable on the **bipartite
growth architecture** side of the problem. Its mechanism is based on
preferential attachment and affiliation formation, not necessarily the
continuous ability-based assortment represented by the desired $\rho$.

**Questions to extract during deep reading:**

1.  What exactly grows: actors, affiliations, memberships, or all three?
2.  How is an actor's probability of joining an affiliation defined?
3.  What variables characterize an affiliation before an actor joins?
4.  Are affiliation sizes endogenous and unbounded?
5.  Can preferential attachment be replaced or augmented by a similarity
    kernel $K_\rho$?
6.  What happens if affiliation degree is capped at exactly $r$?
7.  Does the growth process remain meaningful if every actor has final
    degree 1?

**Preliminary PD18 role:** Best current candidate for the actor-to-group
bipartite growth architecture.

## A.5 Priority reading 3 — Lomi, Conaldi, Tonellato & Pallotti (2014)

**Citation:** Lomi, A., Conaldi, G., Tonellato, M., & Pallotti, F.
(2014). *Participation motifs and the emergence of organization in open
productions.* *Structural Change and Economic Dynamics*.  
<https://www.sciencedirect.com/science/article/pii/S0954349X13000039>

**Why it matters:** The paper studies an evolving bipartite network in
which participants affiliate with organizational objects and explicitly
discusses processes including preferential attachment and **bipartite
assortative mixing**.

Conceptually, this is attractive because the nodes are not merely
abstract mathematical objects: the formation process concerns
participation in organizational structures. That is closer to the
intended cross-domain interpretation of people sorting into teams,
units, departments, cohorts, or other local pools.

**Questions to extract during deep reading:**

1.  How is bipartite assortative mixing defined?
2.  Is it a formation mechanism or an observed network tendency?
3.  Which attributes or structural quantities are being matched?
4.  Is the process sequential?
5.  Are group sizes constrained?
6.  Can its formation statistic be translated into a one-parameter
    $\rho$ mechanism?
7.  Does the organizational interpretation survive relabeling across
    basketball, Army, and academia?

**Preliminary PD18 role:** Potential conceptual bridge between bipartite
formation and organizational sorting.

## A.6 Priority reading 4 — Giroire, Nisse, Trolliet & Sulkowska (2022)

**Citation:** Giroire, F., Nisse, N., Trolliet, T., & Sulkowska, M.
(2022). *Preferential attachment hypergraph with high modularity.*
*Network Science*.  
<https://www.cambridge.org/core/journals/network-science/article/preferential-attachment-hypergraph-with-high-modularity/C0FE5B536E02817ADCEA781532249E8C>

**Why it matters:** This paper is adjacent rather than identical to the
PD18 formulation. Hypergraphs represent multi-person group relations
directly, and actor-group hypergraph structures can also be represented
through bipartite incidence networks.

The paper therefore raises a useful modeling question: is a local pool
most naturally represented as a second-mode node in a bipartite graph,
or as a hyperedge containing several agents?

Its reported use of assortative structure through a mixing matrix makes
it relevant to the search for a generative grouping mechanism.

**Questions to extract during deep reading:**

1.  What determines membership in a new hyperedge?
2.  Where does assortativity enter the process?
3.  Is assortment categorical, continuous, or structural?
4.  Are hyperedge sizes fixed, distributed, or endogenous?
5.  Can equal hyperedge size be imposed without changing the basic
    mechanism?
6.  Would the hypergraph representation simplify or complicate the
    cross-domain ontology?

**Preliminary PD18 role:** Important alternative representation if
bipartite growth becomes awkward under fixed roster size.

## A.7 The potentially useful synthesis

The most promising immediate intellectual experiment is not necessarily
to adopt any one paper wholesale.

Instead, the literature may provide complementary pieces:

- **Quayle et al. (2006):** assortative-growth mechanism;
- **Nikolaev & Mneimneh (2023):** affiliation/bipartite growth
  architecture;
- **Lomi et al. (2014):** organizational bipartite formation and
  assortative mixing;
- **Giroire et al. (2022):** group formation through a hypergraph
  representation.

That suggests the following research question:

> Can the assortative preference logic of an established growth model be
> transplanted into an affiliation-network architecture and then
> subjected to hard equal capacity without destroying the intended
> mapping from $\rho$ to realized assortment?

Schematically:

$$
\text{assortative preference}
+
\text{actor--pool affiliation growth}
+
\text{capacity } r
\longrightarrow
\text{emergent overlapping talent pools}.
$$

This is a **research hypothesis**, not a proposed final model.

## A.8 Why capacity may be the decisive boundary

Ordinary network growth often permits node degree to increase
indefinitely or according to an endogenous distribution. PD18 instead
requires:

$$
n_j \le r
$$

during formation and, ultimately,

$$
n_j = r
$$

for every completed pool.

Once a pool reaches capacity it disappears from the feasible choice set.
Therefore the effective assignment probability is no longer merely an
assortative preference. It becomes an assortative preference
**conditional on remaining capacity**.

A generic representation is:

$$
P(i \rightarrow j)
\propto
K_\rho(A_i,S_j)\,
\mathbf{1}(n_j < r).
$$

The concern is that the indicator term may increasingly dominate the
kernel as formation proceeds. Early agents may experience the intended
$\rho$-driven assortment process, while late agents may be forced into
whichever pools retain capacity.

The empirical and mathematical test is therefore not simply whether
capacity can be added. It is whether:

$$
\rho
\longrightarrow
r_{\mathrm{realized}}
$$

remains stable, monotonic, and interpretable after capacity is imposed.

## A.9 Current reading order

For the next deep-reading round:

1.  **Quayle, Siddiqui & Jones (2006)** — establish the
    assortative-growth mathematics.
2.  **Nikolaev & Mneimneh (2023)** — establish the affiliation-network
    growth architecture.
3.  **Lomi et al. (2014)** — inspect bipartite assortative mixing in an
    organizational formation setting.
4.  **Giroire et al. (2022)** — evaluate the hypergraph alternative.

The first decisive comparison should be **Quayle + Nikolaev &
Mneimneh**.

The specific question is:

> Can Quayle-style assortative preference be married to
> Nikolaev–Mneimneh-style affiliation formation, and what exactly breaks
> when every affiliation is forced to stop at $r$?

## A.10 Updated literature conclusion

The literature search should no longer be summarized as “there are no
specific papers.”

A more accurate statement is:

> There are identifiable literatures on assortative network growth and
> on bipartite/affiliation growth, with several concrete papers that
> approach the PD18 mechanism from different directions. What remains
> unresolved is whether the literature already contains—or can naturally
> yield—a minimal one-parameter assortative formation rule under exact
> equal pool capacity.

That unresolved intersection is now the focus of the literature review.

------------------------------------------------------------------------

*End Appendix A — initial assortative bipartite formation reading path.*
