# Empirical Design: College Basketball → Professional Entry

## Replicating Nonlinear Peer Effects in Advancement

------------------------------------------------------------------------

# I. Objective

This document provides a **fully specified empirical design** for
testing whether the nonlinear relationship observed in U.S. Army
promotions---an inverted-U relationship between peer quality and
advancement---replicates in a sports setting.

The goal is to construct a setting where: - individuals are evaluated
within **peer groups (teams)**, - advancement is **competitive and
capacity-constrained**, and - performance is interpreted **relative to
peers**.

------------------------------------------------------------------------

# II. Conceptual Mapping

  Army Setting                  College Basketball
  ----------------------------- ----------------------------------------------
  Senior rater × time pool      Team × season
  Top-block rating              Performance metrics (BPM, efficiency, usage)
  Peer quality (mean TB rate)   Average teammate quality
  Promotion to Major            Entry into professional basketball
  Capacity constraint           Draft slots, roster limits

------------------------------------------------------------------------

# III. Sample Definition

## Population

-   NCAA Division I men's basketball players

## Time Period

-   Recommended: 2000--2023

## Unit of Observation

-   Player × season panel

## Inclusion Criteria

-   Minimum playing time (e.g., ≥ 200 minutes)
-   Exclude redshirt-only seasons
-   Drop observations with missing key stats

------------------------------------------------------------------------

# IV. Data Sources

## 1. College Performance Data

-   Sports-Reference (College Basketball)
    -   https://www.sports-reference.com/cbb/
-   Variables:
    -   minutes, points, rebounds, assists
    -   advanced metrics (BPM, WS, PER)

## 2. Professional Outcomes

-   Basketball-Reference (NBA Draft and player pages)
    -   https://www.basketball-reference.com/

## 3. Matching Strategy

-   Name + school + year
-   Clean duplicates and spelling variations

------------------------------------------------------------------------

# V. Variable Construction

## A. Outcome Variable

Primary outcome:

$Y_i = 1$ if the player enters professional basketball within $k$ years

Operational definitions: - Drafted into NBA (cleanest) - OR plays ≥1 NBA
game - Optional: include G-League or major international leagues

------------------------------------------------------------------------

## B. Individual Performance

Candidate measures: - Box Plus-Minus (BPM) - Points per minute -
Usage-adjusted scoring - Win shares per 40 minutes

Goal: Capture performance that evaluators plausibly observe.

------------------------------------------------------------------------

## C. Pool Definition

$\text{Pool}_{jt}$ = team $j$ × season $t$

Optional: - Coach × season

------------------------------------------------------------------------

## D. Pool Quality (Key Independent Variable)

Leave-one-out mean:

$$
\text{PoolQ}_{jt}^{(-i)} = \frac{1}{N_{jt}-1} \sum_{k \in \mathcal{P}_{jt},\, k \neq i} \text{Perf}_{kt},
$$

i.e.\ average teammate performance excluding player $i$.

Rationale: Avoid mechanical correlation between individual and pool
measure.

------------------------------------------------------------------------

## E. Control Variables

-   Year fixed effects
-   Position (guard/forward/center)
-   Class year (freshman, sophomore, etc.)
-   Team success (win percentage)
-   Conference fixed effects (optional)

------------------------------------------------------------------------

# VI. Empirical Specification

## Baseline Model

Linear index (LPM uses it directly; logit/probit apply a link $G$):

$$
\Pr(Y_i = 1 \mid \cdot) = G\bigl(\beta_1 \text{Perf}_i + \beta_2 \text{PoolQ}_{jt}^{(-i)} + \beta_3 \bigl(\text{PoolQ}_{jt}^{(-i)}\bigr)^2 + X_i' \gamma\bigr).
$$

Key coefficient: $\beta_3 < 0$ on the quadratic term → evidence of inverted-U.

------------------------------------------------------------------------

## Estimation

-   Logistic regression OR linear probability model
-   Cluster standard errors at team level

------------------------------------------------------------------------

# VII. Nonparametric Analysis

Before imposing functional form:

1.  Bin pool quality into deciles
2.  Plot promotion probability vs pool quality

Goal: Visually confirm inverted-U pattern.

------------------------------------------------------------------------

# VIII. Identification Concerns

## 1. Sorting into Teams

-   Better players may join better teams

Mitigation: - Control for observable ability - Optional: recruit
rankings (if available)

------------------------------------------------------------------------

## 2. Mechanical Correlation

-   Pool includes individual

Solution: - Leave-one-out mean ✔

------------------------------------------------------------------------

## 3. Exposure vs Ability

-   Strong teams provide visibility

Interpretation: - This is part of the mechanism, not purely bias

------------------------------------------------------------------------

# IX. Extensions

## Interaction Effects

$\text{Performance} \times \text{Pool quality}$ (e.g.\ $\text{Perf}_i \times \text{PoolQ}_{jt}^{(-i)}$)

## Heterogeneity

-   By position
-   By class year
-   By team quality

## Alternative Pool Definitions

-   Team × season
-   Coach × season
-   Position group within team

------------------------------------------------------------------------

# X. Expected Findings

-   Low-quality teams → low advancement probability\
-   Moderate-quality teams → highest advancement probability\
-   High-quality teams → declining marginal advancement probability

Interpretation: Tradeoff between signal quality and congestion.

------------------------------------------------------------------------

# XI. Pseudocode (Illustrative)

# Construct leave-one-out pool quality

df\['pool_mean'\] =
df.groupby(\['team','year'\])\['perf'\].transform('mean')
df\['pool_lo'\] = (df\['pool_mean'\]\*df\['n'\] - df\['perf'\]) /
(df\['n'\] - 1)

# Estimate model

import statsmodels.formula.api as smf

model = smf.logit( 'pro_entry \~ perf + pool_lo + I(pool_lo\*\*2) +
C(year) + C(position)', data=df ).fit()

------------------------------------------------------------------------

# XII. Contribution

If results replicate:

> Nonlinear peer effects in advancement are a general feature of
> competitive evaluation systems, not unique to the military.

This would demonstrate that: - advancement depends on both **individual
performance** and **peer context** - and that peer context operates
through **both signal enhancement and congestion**
