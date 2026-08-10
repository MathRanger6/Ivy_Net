# COMPASS Detailed Instructions — ASSIGN Grandchild Prototype

**Date:** 2026-08-10  
**Task:** Add and test an experimental Grandchild ASSIGN model while preserving the Parent and Child models unchanged.

---

## 1. Mission

We need a minimal, domain-general ASSIGN mechanism for capacity-limited pools (player → team, officer → unit, academic → institution/department, etc.). This is **ASSIGN only**; do not redesign SCORE or SELECT.

Add the Grandchild as a clearly named experimental arm. Do not overwrite, refactor away, or silently alter the Parent or Child.

Scientific question:

> Can initially identical teams differentiate endogenously when each arriving individual is attracted by similarity to the team's current membership centroid, subject to fixed roster capacity?

---

## 2. Ingredients and provenance

**Configuration/stub logic:** $R_j^{(s)}$ is our notation for remaining roster positions / unmatched team-side stubs at assignment step $s$. Structural lineage: configuration-model stub matching (Fosdick et al., 2018).

**Quayle-style homophily:** use the scalar exponential distance kernel:

$$
e^{-\rho|A_i-\mu_j|}.
$$

Here $\rho$ is homophilic preference strength. Conceptual lineage: Quayle, Siddiqui & Jones (2006).

The complete weighted-stub probability is **our synthesis**; do not attribute the combined equation wholesale to either source.

---

## 3. The three models

### Parent — dynamic constrained homophilic bipartite formation

Individuals have $A_{i,t}$; teams have lagged $\mu_{j,t-1}$. During period $t$, the centroid is frozen:

$$
P(i\rightarrow j\mid t,s)=
\frac{R_{j,t}^{(s)}e^{-\rho|A_{i,t}^{*}-\mu_{j,t-1}|}}
{\sum_lR_{l,t}^{(s)}e^{-\rho|A_{i,t}^{*}-\mu_{l,t-1}|}}.
$$

After assignment to $j$:

$$
R_{j,t}^{(s+1)}=R_{j,t}^{(s)}-1.
$$

After the period, a new $\mu_{j,t}$ can govern the next period:

$$
\mu_{j,t-1}\rightarrow\text{ASSIGN at }t\rightarrow\mu_{j,t}\rightarrow\text{ASSIGN at }t+1.
$$

This is the general future-facing model for turnover, tenure, reassignment, attrition, and steady-state work. Do not implement those extensions now.

### Child — fixed-centroid one-shot generator

Inputs are fixed empirical $\mu_j$, individual $A_i$, uniform capacity $C$, and $\rho$.

Initialize:

$$
R_j^{(0)}=C\qquad\forall j.
$$

Randomly permute players and assign:

$$
P(i\rightarrow j\mid s)=
\frac{R_j^{(s)}e^{-\rho|A_i-\mu_j|}}
{\sum_lR_l^{(s)}e^{-\rho|A_i-\mu_l|}}.
$$

The empirical $\mu_j$ values remain frozen for the complete formation run.

$$
\boxed{\text{one formation run}=\text{one stochastic realization}.}
$$

Repeated runs are independent realizations, not longitudinal periods.

### Grandchild — endogenous-centroid one-shot generator

**Code this model now.**

Retain bipartite assignment, hard capacity, $R_j$, random player order, exponential homophily, and one formation pass.

Change the centroid assumption. All teams begin identical:

$$
\boxed{\mu_j^{(0)}=\mu_0=\bar A\qquad\forall j}
$$

where:

$$
\bar A=\frac{1}{N}\sum_iA_i.
$$

All teams begin empty:

$$
\boxed{R_j^{(0)}=C\qquad\forall j.}
$$

At step $s$:

$$
\boxed{
P(i\rightarrow j\mid s)=
\frac{R_j^{(s)}e^{-\rho|A_i-\mu_j^{(s)}|}}
{\sum_lR_l^{(s)}e^{-\rho|A_i-\mu_l^{(s)}|}}.
}
$$

After $i$ joins $j$, decrement $R_j$, then immediately update the receiving team's centroid from actual members. If it previously contained $n_j^{(s)}>0$ members:

$$
\mu_j^{(s+1)}=
\frac{n_j^{(s)}\mu_j^{(s)}+A_i}{n_j^{(s)}+1}.
$$

**First-member rule:** $\mu_0$ is a starting signal, not a pseudo-player. When the first player attaches to an empty team:

$$
\boxed{\mu_j=A_i.}
$$

Only the receiving team's state changes at that event.

---

## 4. Why test the Grandchild?

The Child's fixed empirical centroids may not generate enough endogenous sorting. The Grandchild begins with **zero between-team heterogeneity**. Any final differentiation must emerge from:

1. stochastic early assignments;
2. immediate centroid updating;
3. similarity-biased later assignments;
4. finite capacity.

Using $\mu_0=\bar A$ creates no initial team advantage or differentiation.

---

## 5. Prototype algorithm

For one realization at chosen $\rho$:

1. Load/construct the existing empirical player ability vector $\{A_i\}$ where practical.
2. Use a full-capacity test with $N=\sum_jC_j$.
3. Initial MBB capacity: $C_j=C=15$.
4. Compute $\mu_0=\bar A$.
5. Initialize every team with $R_j=C$, $n_j=0$, $\mu_j=\mu_0$.
6. Uniformly randomize player order; never sort by $A_i$.
7. For player $i$, consider all teams with $R_j>0$.
8. Compute $w_{ij}=R_je^{-\rho|A_i-\mu_j|}$.
9. Normalize $p_{ij}=w_{ij}/\sum_lw_{il}$.
10. Sample team $j$ stochastically.
11. Attach $i$ to $j$.
12. Set $R_j\leftarrow R_j-1$.
13. Immediately update that team's centroid from actual members; first member implies $\mu_j=A_i$.
14. Continue until all players are assigned and intended slots filled.
15. Save assignments, final centroids, seed, and diagnostics.

Each independent realization resets $\{A_i\}$, $C$, $\rho$, $\mu_0$, team states, and player queue. No final state carries forward.

---

## 6. Rho sweep

Characterize:

$$
\rho\longrightarrow\text{realized compositional sorting}.
$$

Begin at $\rho=0$ and sweep upward over a range broad enough to reveal shape/saturation. Existing project sweep conventions may be reused, but do not assume the old range is optimal.

Run multiple independent realizations per $\rho$ with reproducible seeds and distinct random streams.

**Do not assume linearity.** The exponential kernel, path dependence, and hard capacity make nonlinear/saturating behavior plausible.

---

## 7. Outcome diagnostics

### Within-team MSE

For final team mapping $g(i)$:

$$
\boxed{
D=\frac{1}{N}\sum_i(A_i-\mu_{g(i)}^{\mathrm{final}})^2.
}
$$

Call this **within-team MSE/dispersion**, not assortativity.

Hypothesized direction:

$$
\rho\uparrow\Rightarrow D\downarrow.
$$

Test it; do not impose it.

### Normalized sorting index

Also calculate:

$$
\boxed{
H=
1-
\frac{\sum_i(A_i-\mu_{g(i)}^{\mathrm{final}})^2}
{\sum_i(A_i-\bar A)^2}.
}
$$

This is an explained-variance-style partition statistic. Hypothesized direction:

$$
\rho\uparrow\Rightarrow H\uparrow.
$$

Also retain final $\mu_j$ distribution, SD/variance of final team centroids, within-team distributions, roster sizes, assignment order, and seed.

---

## 8. Required plots

Produce at minimum:

1. $D$ vs. $\rho$: ensemble mean plus variation.
2. $H$ vs. $\rho$: ensemble mean plus variation.
3. Final team-centroid dispersion vs. $\rho$.
4. Representative final centroid/team-composition distributions at low, intermediate, and high $\rho$.

Do not begin by fitting a linear relationship. Visualize the empirical curve first.

---

## 9. Validation locks

Assert/check:

- every player has exactly one team;
- no team exceeds $C$;
- full-capacity runs finish with every team at exactly $C$;
- $\sum_jR_j=0$ at completion;
- probabilities sum to 1 at every event;
- full teams have zero assignment probability;
- at $\rho=0$:
  $$
  P(i\rightarrow j\mid s)=\frac{R_j^{(s)}}{\sum_lR_l^{(s)}};
  $$
- initially all $\mu_j=\bar A$;
- first player on an empty team makes $\mu_j=A_i$ exactly;
- $\mu_0$ is never counted as an observation;
- repeated realizations reset all states;
- Parent and Child code paths/results remain unchanged.

Add lightweight assertions/tests.

---

## 10. Terminology locks

- $A_i$: individual ability/performance signal.
- $\mu_j$: team/pool centroid.
- $C$: team capacity.
- $R_j$: remaining capacity/unmatched team stubs.
- $\rho$: homophilic preference strength.
- $s$: sequential assignment event within one realization.
- $t$: longitudinal period in the Parent only.
- Homophily $\neq$ realized assortativity/sorting.
- One formation run = one stochastic realization.
- Repeated realizations $\neq$ longitudinal iterations.

---

## 11. Do not do these things

Do not modify SCORE or SELECT; add prestige/popularity/preferential attachment; add tenure/turnover; add heterogeneous capacities; carry state between realizations; use empirical team $\mu_j$ in the Grandchild; sort players by $A_i$; use Quayle's analytic homophily-to-assortativity mapping; call $D$ assortativity; delete/overwrite Parent or Child; or turn this prototype into a large refactor.

---

## 12. Deliverables from COMPASS

Return:

1. Grandchild implementation;
2. short README/method note stating what was added and what remained untouched;
3. validation/test output;
4. $\rho$-sweep plots;
5. compact results table by $\rho$ with realization count, mean/SD of $D$, mean/SD of $H$, and mean/SD final-centroid dispersion;
6. short interpretation of observed curve shapes without overclaiming;
7. any numerical/pathological issues.

---

# 13. Recent VECTOR/User Documents to Attach

These are the recent task-specific documents COMPASS may not have in the repo.

### `VECTOR_ASSIGN_Dynamic_to_OneShot_Model.pptx` - this can be found in the 3-Master_Plan/VECTOR_work/VECTOR_ASSIGN_Dynamic_to_OneShot_Model folder of slide images

Two-slide briefing of Parent and Child; configuration/stub component, Quayle component, and our combined synthesis.

### `VECTOR_One_Page_Homophilic_Initial_League_Model.md` - this can be found in the 3-Master_Plan/VECTOR_work folder

Clean Parent-to-Child derivation, notation, fixed empirical-centroid Child, and the corrected identity:

$$
\text{one formation run}=\text{one stochastic realization}.
$$

### `VECTOR_Bipartite_Assortative_Formation_Model.md` - this can be found in the 3-Master_Plan/VECTOR_work folder

Broader domain-general working specification. It contains the earlier frozen-centroid architecture, capacity, notation, and future longitudinal concepts. Read as background; **the Grandchild intentionally changes the frozen-centroid assumption within a one-shot run.**

### Helpful optional Quayle context

If useful, attach `Quayle_One_Page_Formula_Concept_Sheet.md` and/or `Quayle_Companion_Volume.md` for the distinction between similarity, homophily, stochastic attachment, and realized assortativity.

---

# 14. Repo / Previously Supplied Context COMPASS Already Has

Because COMPASS has Cursor access to the repo, inspect these first rather than asking for duplicate uploads.

### `tier1_pool_assignment.py`

Start here for current ASSIGN implementation, interfaces, one-shot league generation, randomization, seeds, and code paths the Grandchild should preserve.

### `empirical_rho_coverage_overlay.py`

Use for existing $\rho$-sweep architecture, experiment harness, plotting conventions, and reusable diagnostics.

### `09_PD18_Alex_meeting_takeaways.md`

Use for project-level separation of ASSIGN from SCORE/SELECT and the role of $\rho$ as the ASSIGN-side knob.

### `20260807_VECTOR_PD18_literature_brief.md`

Use for the PD18 problem statement, empirical motivation, constraints, and context that initiated the ASSIGN modeling search.

### Existing Quayle source/material

Use the Quayle paper and any existing project notes for the original homophily mechanism: homophily is a **generative attachment preference**; realized assortativity is an **emergent outcome**.

Do not reopen the broad Saracco/Bomiriya search unless a concrete implementation problem requires it.

---

## 15. Success criterion

The prototype succeeds if it reproducibly tells us whether:

$$
\boxed{
\text{initially identical teams}
+
\text{sequential centroid updating}
+
\text{homophilic attachment}
+
\text{hard capacity}
}
$$

produces increasing endogenous compositional differentiation as $\rho$ increases, and what the empirical shape of that relationship is.

We are testing the mechanism, not yet declaring it the final ASSIGN model.
