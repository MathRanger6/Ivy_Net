# VECTOR Reading Guide — Saracco + Bomiriya for the ASSIGN Mechanism

**Last synced:** 2026-08-10  
**Purpose:** Distill the two papers most immediately relevant to
replacing a bespoke ASSIGN model with a literature-grounded bipartite
formation mechanism.

> **Reading lens:** We are not asking either paper to solve the entire
> model. We are asking what structural or behavioral component each
> paper gives us, what it does *not* give us, and how the two might be
> combined with Quayle.

------------------------------------------------------------------------

## Executive Synthesis

The two papers solve different pieces of our problem.

**Saracco et al. (2015)** gives us the **bipartite configuration-model
skeleton**: preserve specified degree information on the two node layers
while otherwise randomizing the bipartite network. This is directly
relevant to a system in which individuals have one affiliation and teams
have finite roster sizes.

**Bomiriya et al. (2023)** addresses the **homophily problem in
bipartite networks directly**, without collapsing the bipartite graph to
a one-mode projection. Its central message is especially important for
us: homophily can be modeled while preserving the two-mode structure,
rather than projecting first and losing information.

**Quayle et al. (2006)** supplies the behavioral idea we already like:
similarity is an input to a stochastic attachment rule, while realized
assortativity is an outcome.

$$
\boxed{
\text{Saracco: bipartite structural constraints}
+
\text{Quayle: similarity-weighted choice}
+
\text{Bomiriya: precedent for bipartite homophily}
}
$$

The simplest candidate ASSIGN rule remains:

$$
\boxed{
P(i\rightarrow j)
=
\frac{
R_j e^{-\rho d_{ij}}
}{
\sum_l R_l e^{-\rho d_{il}}
}
}
$$

where $R_j$ is remaining capacity and $d_{ij}$ is
individual-to-team-centroid distance.

**Important:** That exact sequential rule is our proposed synthesis. It
is **not claimed here to be an equation from either Saracco or
Bomiriya**.

------------------------------------------------------------------------

# Paper 1 — Saracco et al. (2015)

## Citation

Saracco, F., Di Clemente, R., Gabrielli, A., & Squartini, T. (2015).
*Randomizing bipartite networks: the case of the World Trade Web*.
Scientific Reports, 5, 10595. https://doi.org/10.1038/srep10595

## The Problem They Are Solving

Saracco et al. are primarily concerned with **null models for bipartite
networks**: what portion of the observed bipartite structure should be
preserved while everything else is randomized?

For ASSIGN, the structural facts include one affiliation per individual
at a snapshot and finite team sizes. Those constraints should not be
confused with behavioral attraction.

## Bipartite Representation

$$
\boxed{
\text{Layer 1: individuals}
\qquad
\text{Layer 2: teams/pools}
}
$$

An edge means individual $i$ belongs to team $j$. This is more faithful
to our formation problem than beginning with an individual-to-individual
projection.

## Configuration-Model Logic

For our baseline snapshot:

$$
k_i=1
$$

for each individual, while a filled team has:

$$
k_j=C_j.
$$

For baseline NCAA men’s basketball:

$$
C_j=C=15.
$$

The conceptual payoff is:

$$
\boxed{
\text{degree/capacity}
\neq
\text{similarity preference}.
}
$$

Roster size belongs in the structural constraint, not inside the
homophily parameter.

## Hard vs. Soft Constraint Warning

This distinction matters. Saracco’s maximum-entropy BiCM constrains
degree information at the **ensemble expectation** level. Our roster cap
is operationally a **hard constraint**:

$$
n_j\le C_j.
$$

If every roster position is filled:

$$
n_j=C_j.
$$

Therefore we can borrow the **configuration-model principle** without
assuming that Saracco’s particular soft-constraint sampling
implementation is our final algorithm.

## What Saracco Gives Us

- A defensible bipartite foundation.
- Degree information as the structural baseline.
- A clean null-model interpretation.
- Separation of degree/capacity effects from higher-order organization.
- A reason to preserve bipartite structure when it contains substantive
  information.

At $\rho=0$, our natural analogue is a capacity-constrained random
assignment baseline.

## What Saracco Does NOT Give Us

Saracco does not directly supply:

- team-centroid similarity;
- Quayle’s exponential homophily kernel;
- yearly roster turnover or tenure;
- evolving individual performance;
- lagged endogenous centroids;
- our exact sequential assignment rule;
- a single $\rho$ controlling individual–team attraction.

**Use Saracco as the structural parent, not as the complete ASSIGN
model.**

## What to Mark While Reading

Look for passages on bipartite null models, degree sequences on both
layers, maximum entropy, canonical/soft constraints, edge probabilities,
independence of links, projection, and what degree constraints explain
or fail to explain.

**Reading question:** Can we preserve the configuration-model structural
logic while replacing unbiased edge formation with a similarity-biased
matching process?

------------------------------------------------------------------------

# Paper 2 — Bomiriya et al. (2023)

## Citation

Bomiriya, R. P., Kuvelkar, A. R., Hunter, D. R., & Triebel, S. (2023).
*Modeling Homophily in Exponential-Family Random Graph Models for
Bipartite Networks*. arXiv:2312.05673. https://arxiv.org/abs/2312.05673

## The Problem They Are Solving

Bomiriya et al. ask how homophily should be modeled when ties connect
**two different classes of nodes**. They explicitly address the common
practice of collapsing a bipartite network into a one-mode projection,
which can discard meaningful two-mode information.

That supports working with the actual affiliation process rather than
forcing a one-mode model to represent it.

## Why This Is Relevant

Our cross-mode comparison is:

$$
\text{individual performance}
\longleftrightarrow
\text{team characteristic}.
$$

With a lagged endogenous centroid:

$$
\mu_{j,t-1},
$$

our dyadic distance is:

$$
d_{ij,t}
=
|A_i^*-\mu_{j,t-1}|.
$$

Bomiriya provides literature precedent for studying **homophily directly
in the bipartite graph**.

## ERGM Logic in One Sentence

Schematically, an exponential-family random graph model assigns
probability to an entire network:

$$
P(Y=y)
\propto
\exp\{\theta^\top g(y)\}.
$$

$Y$ is the random network, $y$ a possible realization, $g(y)$ selected
network statistics, and $\theta$ their parameters.

The lesson for us is not necessarily to fit a full ERGM. It is:

> **Bipartite structure does not prevent us from defining and modeling
> homophily.**

## Why Projection Is Not Necessary

Our causal question is:

$$
\boxed{
\text{Who affiliates with which team?}
}
$$

not merely which individuals become co-members after affiliation.
Projection may remain useful as an outcome or diagnostic, but it need
not be the formation mechanism.

## What Bomiriya Gives Us

- Direct precedent for bipartite homophily.
- A warning against solving the problem by projection alone.
- A vocabulary for cross-mode similarity.
- Evidence that homophily can coexist with formal bipartite network
  modeling.

## What Bomiriya Does NOT Automatically Give Us

It does not automatically provide:

- hard roster capacity;
- Quayle’s exponential distance kernel;
- lagged centroids;
- tenure turnover;
- sequential vacancy filling;
- our desired $\rho=0$ random-assignment baseline;
- the exact weighted-stub algorithm.

**Use Bomiriya as conceptual and methodological precedent, not
necessarily as the ASSIGN engine.**

## What to Mark While Reading

Look for why projection is inadequate, definitions of bipartite
homophily, how attributes on the two layers enter the model, cross-mode
similarity statistics, degree structure, parameter interpretation, and
computational complexity.

**Reading question:** Can we borrow their conceptual treatment of
bipartite homophily without inheriting machinery we do not need?

------------------------------------------------------------------------

# Putting Saracco + Bomiriya + Quayle Together

| Source              | Piece we want                                                                        |
|---------------------|--------------------------------------------------------------------------------------|
| **Saracco et al.**  | Bipartite configuration logic; degree/capacity as structural constraints             |
| **Quayle et al.**   | Similarity-dependent stochastic attachment; preference $\neq$ realized assortativity |
| **Bomiriya et al.** | Direct bipartite homophily; projection is not required                               |

A defensible description is:

> **ASSIGN is a constrained bipartite configuration-style assignment
> process augmented with a Quayle-inspired similarity bias.**

## Candidate Minimal Mechanism

Let $R_{j,t}^{(s)}$ be remaining openings on team $j$ at assignment step
$s$ and define:

$$
d_{ij,t}
=
|A_i^*-\mu_{j,t-1}|.
$$

Then:

$$
\boxed{
P(i\rightarrow j\mid t,s)
=
\frac{
R_{j,t}^{(s)}e^{-\rho d_{ij,t}}
}{
\sum_l R_{l,t}^{(s)}e^{-\rho d_{il,t}}
}.
}
$$

After assignment:

$$
R_{j,t}^{(s+1)}
=
R_{j,t}^{(s)}-1.
$$

When $R_{j,t}^{(s)}=0$, the team has no remaining opening and receives
zero probability.

## Why Remaining Capacity Matters

At $\rho=0$:

$$
\boxed{
P(i\rightarrow j)
=
\frac{R_j}{\sum_l R_l}.
}
$$

This is the configuration-style random matching baseline: an individual
stub is matched to the remaining team stubs.

Similarity then biases that baseline:

$$
\boxed{
\text{available team stubs}
\times
\text{similarity attraction}.
}
$$

------------------------------------------------------------------------

# Conceptual Payoff

$$
\boxed{C_j=\text{structural capacity}}
$$

$$
\boxed{\mu_{j,t-1}=\text{lagged endogenous team state}}
$$

$$
\boxed{d_{ij,t}=\text{individual–team difference}}
$$

$$
\boxed{\rho=\text{strength of similarity preference}}
$$

$$
\boxed{\text{realized assortment}=\text{outcome of constrained matching}}
$$

Therefore:

$$
\boxed{
\rho
\neq
\text{realized assortativity}.
}
$$

Capacity can prevent strong homophilic preference from producing equally
strong realized sorting. That may be an important property rather than a
defect.

------------------------------------------------------------------------

# Cautions Before Locking the Model

1.  **Saracco’s BiCM is not identical to hard roster filling.** Be
    precise about whether the final implementation is a BiCM, hard
    bipartite configuration model, or configuration-style sequential
    matching algorithm.

2.  **The weighted-stub equation is presently our synthesis.** The
    factor $R_j e^{-\rho d_{ij}}$ is parsimonious, but we should verify
    whether an established model already uses the exact or equivalent
    form.

3.  **Do not import Quayle’s analytic $\alpha\leftrightarrow r$
    mapping.** Our bipartite capacity constraints change that
    relationship. Initially establish $\rho\rightarrow$ realized sorting
    through simulation.

4.  **Projection can remain a diagnostic.** It need not be the formation
    mechanism.

------------------------------------------------------------------------

# Suggested Reading Order

**Saracco first — structure.** Ask what exactly the bipartite
configuration model preserves and whether constraints are hard or
expected.

**Bomiriya second — behavior.** Ask how homophily is defined when the
node classes differ, and which ideas can be borrowed without a full
ERGM.

**Quayle third — mechanism.** Re-read Equation (4) asking which
component is structural, which is similarity preference, and what should
replace $f(k_j)$ for a finite-capacity team.

------------------------------------------------------------------------

# Five-Year Memory

> **Saracco gives us the container. Quayle gives us the attraction.
> Bomiriya tells us it is legitimate to study that attraction without
> destroying the bipartite network.**

$$
\boxed{
\text{bipartite degree/capacity constraints}
+
\text{Quayle-style similarity bias}
\rightarrow
\text{realized team formation}.
}
$$

Protect this question throughout development:

> **How much realized sorting emerges from a given similarity preference
> once finite team capacities constrain what can actually be realized?**

------------------------------------------------------------------------

## Sources

Saracco, F., Di Clemente, R., Gabrielli, A., & Squartini, T. (2015).
*Randomizing bipartite networks: the case of the World Trade Web*.
Scientific Reports, 5, 10595. https://doi.org/10.1038/srep10595

Bomiriya, R. P., Kuvelkar, A. R., Hunter, D. R., & Triebel, S. (2023).
*Modeling Homophily in Exponential-Family Random Graph Models for
Bipartite Networks*. arXiv:2312.05673. https://arxiv.org/abs/2312.05673

Quayle, A. P., Siddiqui, A. S., & Jones, S. J. M. (2006). *Modeling
network growth with assortative mixing*. European Physical Journal B,
50, 617–630.
