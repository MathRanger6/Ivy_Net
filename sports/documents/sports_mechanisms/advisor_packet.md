# Advisor Packet: Pool Quality and Promotion Across Domains

------------------------------------------------------------------------

# I. Core Empirical Finding (Army)

Promotion probability increases with peer pool quality up to a point,
then declines at the highest levels (inverted-U).

Mechanism: - Signal quality (positive) - Congestion / competition
(negative)

------------------------------------------------------------------------

# II. Cross-Domain Replication Strategy (Sports)

Goal: Test whether nonlinear peer effects generalize.

Mapping: - Pool → team × season - Performance → player stats - Promotion
→ advancement outcome

------------------------------------------------------------------------

# III. Designs

## A. College Basketball → Going Professional (Primary)

-   Outcome: Draft / pro entry
-   Pool: team × season
-   Mechanism: visibility vs congestion

## B. NBA → Career Longevity (Secondary)

-   Outcome: survival in league
-   Mechanism: development vs role crowding

------------------------------------------------------------------------

# IV. Empirical Design (College Basketball)

## Data

-   Sports-Reference (college)
-   Basketball-Reference (NBA)

## Variables

-   Performance: BPM, WS/40 (e.g.\ $\text{Perf}_i$ or $\text{Perf}_{it}$)
-   Pool quality: leave-one-out mean $\text{PoolQ}_{jt}^{(-i)}$
-   Outcome: pro entry indicator $Y_i$

## Model

$$
\Pr(Y_i = 1) = f\bigl(\text{Perf}_i,\, \text{PoolQ}_{jt}^{(-i)},\, \bigl(\text{PoolQ}_{jt}^{(-i)}\bigr)^2,\, X_i\bigr),
$$

with controls $X_i$ (e.g., fixed effects and covariates).

------------------------------------------------------------------------

# V. Identification

-   Sorting → controls
-   Mechanical bias → leave-one-out
-   Support → check bins

------------------------------------------------------------------------

# VI. Expected Result

Inverted-U relationship between pool quality and advancement.

------------------------------------------------------------------------

# VII. Literature Appendix

-   Paulsen (2022): peer effects and NBA productivity\
-   Oberhofer & Schwinner (2017): peer effects in salaries\
-   Barnes (2008): NBA career longevity\
-   Zhu (2025): survival models in NBA careers\
-   Kuehn (2023): teammate adjustment in draft evaluation

------------------------------------------------------------------------

# VIII. Contribution

General principle: Advancement depends on both individual performance
and peer context, with nonlinear effects due to congestion.
