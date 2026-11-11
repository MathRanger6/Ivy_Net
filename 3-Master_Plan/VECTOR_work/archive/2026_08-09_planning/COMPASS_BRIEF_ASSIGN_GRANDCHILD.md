# COMPASS Brief — Prototype the ASSIGN Grandchild Model

COMPASS — this is a **quick experimental coding task for ASSIGN only**. Preserve all existing ASSIGN code and prior model variants. Add the Grandchild as a new experimental arm; do not replace the Parent or Child.

## Model family

**Parent — dynamic constrained homophilic bipartite formation.** Individuals $i$ attach to finite-capacity teams $j$. During longitudinal period $t$, the prior-period centroid $\mu_{j,t-1}$ is frozen:

$$
P(i\rightarrow j\mid t,s)=
\frac{R_{j,t}^{(s)}e^{-\rho|A_{i,t}^{*}-\mu_{j,t-1}|}}
{\sum_lR_{l,t}^{(s)}e^{-\rho|A_{i,t}^{*}-\mu_{l,t-1}|}}.
$$

After the period, centroids can be recalculated for the next period.

**Child — one-shot fixed-centroid generator.** No longitudinal evolution. Use fixed empirical $\mu_j$, individual $A_i$, uniform $C$, initialize $R_j^{(0)}=C$, randomize player order, and make one complete pass:

$$
P(i\rightarrow j\mid s)=
\frac{R_j^{(s)}e^{-\rho|A_i-\mu_j|}}
{\sum_lR_l^{(s)}e^{-\rho|A_i-\mu_l|}}.
$$

The $\mu_j$ remain frozen. One complete pass = one stochastic realization; repeated runs are independent realizations, not longitudinal iterations.

**Grandchild — code this now.** Retain the Child's finite-capacity sequential assignment, but initialize every team identically:

$$
\mu_j^{(0)}=\mu_0=\bar A,\qquad R_j^{(0)}=C.
$$

At each event:

$$
P(i\rightarrow j\mid s)=
\frac{R_j^{(s)}e^{-\rho|A_i-\mu_j^{(s)}|}}
{\sum_lR_l^{(s)}e^{-\rho|A_i-\mu_l^{(s)}|}}.
$$

After player $i$ attaches to $j$, decrement $R_j$ and **immediately recompute that team's centroid from its actual attached players before the next player enters**. For the first actual player on an empty team, set $\mu_j=A_i$; $\mu_0$ is an initial signal, not a pseudo-observation.

## Experiment

Sweep $\rho$ from $0$ upward. At each $\rho$, run multiple independent realizations from identical initial conditions. Do not carry state between realizations.

For each league calculate within-team MSE:

$$
D=\frac{1}{N}\sum_i(A_i-\mu_{g(i)}^{\mathrm{final}})^2,
$$

and normalized sorting:

$$
H=1-\frac{\sum_i(A_i-\mu_{g(i)}^{\mathrm{final}})^2}
{\sum_i(A_i-\bar A)^2}.
$$

Call $D$ within-team dispersion, **not assortativity**. Plot ensemble mean and variation of $D$ and $H$ versus $\rho$. We expect $D$ generally to decline and $H$ to rise if the mechanism works, but **do not assume linearity or monotonicity in individual realizations**.

Keep this isolated from SCORE and SELECT. Preserve Parent and Child unchanged.

**Immediate question:** Does sequential centroid updating plus homophilic attraction generate endogenous between-team differentiation under hard roster capacity, and how does that differentiation vary with $\rho$?

See the accompanying detailed instructions for implementation locks, validation checks, and context files.
