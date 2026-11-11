# VECTOR One-Page Model — Homophilic Formation of an Initial League

**Last synced:** 2026-08-10  
**Purpose:** Define the general dynamic formation model first, then
derive the one-shot version used to generate an initial league for the
current paper.

------------------------------------------------------------------------

## 1. Parent Model: Dynamic Bipartite Formation

The general model is a **bipartite affiliation process** between
individuals $i$ and teams $j$.

Each individual has performance/ability $A_{i,t}$. Each team has a
lagged centroid:

$$
\mu_{j,t-1}
=
\frac{1}{n_{j,t-1}}
\sum_{i\in T_{j,t-1}}A_{i,t-1}.
$$

Each team has finite capacity $C_j$, with remaining openings at
assignment step $s$:

$$
R_{j,t}^{(s)}
=
C_j-n_{j,t}^{(s)}.
$$

Define individual–team distance:

$$
d_{ij,t}
=
|A_{i,t}^{*}-\mu_{j,t-1}|.
$$

The Quayle-inspired homophily weight is $e^{-\rho d_{ij,t}}$, where
$\rho$ controls similarity attraction.

The general assignment rule is:

$$
\boxed{
P(i\rightarrow j\mid t,s)
=
\frac{
R_{j,t}^{(s)}e^{-\rho d_{ij,t}}
}{
\sum_l R_{l,t}^{(s)}e^{-\rho d_{il,t}}
}
}
$$

for teams with $R_{j,t}^{(s)}>0$.

After assigning $i$ to $j$:

$$
R_{j,t}^{(s+1)}
=
R_{j,t}^{(s)}-1.
$$

At the end of period $t$, new centroids can be calculated and the
process repeated:

$$
\boxed{
\mu_{j,t-1}
\rightarrow
\text{homophilic constrained assignment at }t
\rightarrow
\mu_{j,t}
\rightarrow
\text{assignment at }t+1.
}
$$

This parent model accommodates later turnover, tenure, reassignment,
attrition, and steady-state centroid analysis.

------------------------------------------------------------------------

## 2. Current Paper: One-Shot Initial-League Specialization

For the present paper, we do **not** need the full longitudinal process.

Use empirical team centroids as fixed initial conditions:

$$
\boxed{\mu_j=\mu_{j,0}^{\mathrm{empirical}}.}
$$

Use the observed or empirically informed set of individual abilities:

$$
\boxed{A_i.}
$$

All roster positions are initially open:

$$
\boxed{
R_j^{(0)}=C
\qquad\forall j.
}
$$

For NCAA men’s basketball:

$$
\boxed{C=15.}
$$

Randomly permute the players:

$$
\pi=(\pi_1,\pi_2,\ldots,\pi_N).
$$

At assignment step $s$, player $i=\pi_s$ chooses among all teams with
remaining capacity according to:

$$
\boxed{
P(i\rightarrow j\mid s)
=
\frac{
R_j^{(s)}e^{-\rho|A_i-\mu_j|}
}{
\sum_l R_l^{(s)}e^{-\rho|A_i-\mu_l|}
}
}
$$

with $R_j^{(s)}>0$.

When $R_j^{(s)}=0$, team $j$ automatically has zero probability
thereafter.

The algorithm stops when all players are assigned and all roster slots
are filled.

------------------------------------------------------------------------

## 3. Interpretation

At $\rho=0$:

$$
P(i\rightarrow j\mid s)
=
\frac{R_j^{(s)}}{\sum_l R_l^{(s)}}.
$$

This is the random capacity-preserving bipartite matching baseline.

As $\rho$ increases, assignments increasingly favor teams whose
empirical centroids are close to the player’s $A_i$:

$$
\boxed{
\text{remaining capacity}
\times
\text{homophilic similarity attraction}.
}
$$

The model keeps four concepts separate:

$$
\boxed{
\mu_j=\text{team state},
\qquad
A_i=\text{individual state},
\qquad
C=\text{structural constraint},
\qquad
\rho=\text{homophilic preference}.
}
$$

Realized league sorting is an **outcome** of matching, not the same
object as $\rho$.

------------------------------------------------------------------------

## 4. One Formation Round, Many Realizations

The current model uses **one formation round per generated league**.

We can rerun that same one-shot algorithm many times at fixed $\rho$:

$$
G^{(1)},G^{(2)},\ldots,G^{(M)},
$$

but these are **independent stochastic realizations**, not longitudinal
time steps.

Thus:

$$
\boxed{
\text{one-shot formation}
\neq
\text{one stochastic realization only}.
}
$$

Multiple reruns characterize league-composition variance under the same
model conditions without introducing longitudinal dynamics.

------------------------------------------------------------------------

## 5. Why This Is the Right Baseline

The current ASSIGN mechanism is deliberately minimal:

$$
\boxed{
\text{empirical team centroids}
+
\text{individual }A_i
+
\text{capacity }C
+
\text{homophily }\rho.
}
$$

No team prestige term, preferential-attachment term, longitudinal
updating, tenure process, or additional sorting parameter is required
for the baseline.

Quayle supplies the conceptual precedent: **homophily is a generative
preference, while assortativity is measured after formation**. The
present model preserves that distinction while replacing one-mode growth
with finite-capacity bipartite assignment.

> **Current paper:** generate an initial league from fixed empirical
> centroids, then repeat independent realizations only as needed to
> understand variance across generated leagues.

> **Later extension:** allow $\mu_{j,t}$, roster turnover, tenure,
> attrition, and reassignment to evolve through time.
