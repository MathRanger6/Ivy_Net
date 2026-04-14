# Advisor Packet (Verbose Version)

## Nonlinear Peer Effects in Promotion: Army Evidence and Sports Replication

------------------------------------------------------------------------

# I. Executive Summary

This project documents and tests a general principle:

> Advancement in hierarchical and competitive systems depends not only
> on individual performance, but also on the **quality of the peer group
> within which that performance is evaluated**, with **nonlinear
> effects** arising from the interaction of signal quality and
> congestion.

Using U.S. Army officer data, we find an **inverted-U relationship**
between peer pool quality and promotion to Major. We propose and
implement replications in sports settings---most prominently NCAA
basketball---to test whether this pattern generalizes.

------------------------------------------------------------------------

# II. Core Empirical Finding (Army Setting)

## Institutional Structure

-   Officers are evaluated within **senior rater × time pools**
-   Evaluations include **top-block constraints** (scarce top ratings)
-   Promotion is **capacity-constrained** (finite slots)
-   Evaluation is **explicitly relative within pools**

## Empirical Result

> Promotion probability increases with pool quality at low--moderate
> levels, then flattens or declines at the highest levels.

## Mechanism (Careful Interpretation)

### 1. Signal Quality Effect (Positive)

-   Stronger peers → more informative comparison set\
-   Strong performance in strong pool → higher credibility

### 2. Congestion Effect (Negative)

-   Many strong peers → harder to stand out\
-   Limited "top signals" and promotion slots\
-   Reduced marginal promotion probability

## Key Insight

Advancement is a function of: - individual performance\
- **and the structure of the evaluation environment**

------------------------------------------------------------------------

# III. Replication Strategy: Why Sports?

Sports settings provide: - Observable performance - Natural peer groups
(teams) - Competitive, capacity-constrained advancement - Relative
evaluation environments

Goal: \> Test whether the **inverted-U relationship** appears outside
the military.

------------------------------------------------------------------------

# IV. Mapping: Army → Sports

  Army                  Sports
  --------------------- ------------------------------
  Senior rater pool     Team × season
  Top-block rating      Performance metrics / role
  Peer quality          Average teammate ability
  Promotion             Draft / pro entry / survival
  Capacity constraint   Draft slots, roster limits

------------------------------------------------------------------------

# V. Replication Designs

## A. College Basketball → Professional Entry (Primary)

### Outcome

-   Drafted OR enters professional basketball

### Mechanism Mapping

-   Moderate-quality teams:
    -   high visibility
    -   strong signal environment
-   Extremely strong teams:
    -   congestion (limited touches, role compression)
    -   reduced distinctiveness

### Why This Is the Best Design

-   Clean, discrete advancement event
-   Strong analogy to promotion
-   Intuitive to reviewers

------------------------------------------------------------------------

## B. NBA → Career Longevity (Secondary)

### Outcome

-   Years in league / hazard of exit

### Mechanism

-   Moderate-quality teams:
    -   development and exposure
-   High-quality teams:
    -   reduced minutes
    -   role crowding

### Strengths

-   Compatible with survival analysis
-   Repeated exposure to peer environments

### Limitations

-   Influenced by injuries, aging, contracts

------------------------------------------------------------------------

# VI. Fully Specified Empirical Design (College Basketball)

## Data Sources

-   Sports-Reference (college performance)
-   Basketball-Reference (NBA outcomes)

## Sample

-   NCAA Division I players (2000--2023)
-   Player × season observations
-   Minimum playing time threshold

------------------------------------------------------------------------

## Variables

### Outcome

$Y_i = 1$ if the player enters professional basketball within $k$ years

------------------------------------------------------------------------

### Individual Performance

-   BPM (preferred)
-   Points per minute
-   Efficiency metrics

------------------------------------------------------------------------

### Pool Definition

Team × season

------------------------------------------------------------------------

### Pool Quality (Key Variable)

Leave-one-out mean teammate performance

------------------------------------------------------------------------

### Controls

-   Year fixed effects
-   Position
-   Class year
-   Team success
-   Conference fixed effects

------------------------------------------------------------------------

## Empirical Specification

$$
\Pr(Y_i = 1) = f\bigl(\text{Perf}_i,\, \text{PoolQ}_{jt}^{(-i)},\, \bigl(\text{PoolQ}_{jt}^{(-i)}\bigr)^2,\, X_i\bigr),
$$

with controls $X_i$ (fixed effects and covariates). Key test: negative coefficient on $\bigl(\text{PoolQ}_{jt}^{(-i)}\bigr)^2$ (e.g.\ $\beta_3 < 0$ in a linear index with quadratic pool term).

------------------------------------------------------------------------

## Nonparametric Validation

-   Bin pool quality
-   Plot outcome vs pool quality

------------------------------------------------------------------------

# VII. Identification and Robustness

## Sorting

-   Better players → better teams\
    Mitigation: controls, robustness

## Mechanical Bias

-   Fixed via leave-one-out

## Support

-   Ensure observations in extreme bins

------------------------------------------------------------------------

# VIII. Literature (Expanded Context)

## Peer Effects & Evaluation

-   Paulsen (2022): peer effects in NBA transitions\
-   Kuehn (2023): adjusting for teammate quality

## Career Outcomes

-   Barnes (2008): NBA longevity\
-   Zhu (2025): survival models

## Context Dependence

-   Oberhofer & Schwinner (2017): peer effects in salary

------------------------------------------------------------------------

# IX. Contribution

If replicated:

> Nonlinear peer effects are a **general feature of evaluation systems
> with capacity constraints**

Implication: - Advancement systems are shaped by **interaction of
ability and context** - Not purely meritocratic, not purely contextual

------------------------------------------------------------------------

# X. Framing for Discussion

This project contributes to:

-   Management Science: evaluation systems and organizational design\
-   OR / Systems: allocation under congestion\
-   Business Dynamics: nonlinear outcomes from structural constraints

------------------------------------------------------------------------

# XI. Key Questions for Advisor Discussion

1.  Outcome definition (draft vs broader pro entry)
2.  Performance metric choice
3.  Sorting and identification strategy
4.  Framing: replication vs theory contribution

------------------------------------------------------------------------

# XII. Bottom Line

> Being surrounded by stronger peers helps---until it doesn't.

The goal of this project is to show: - where that turning point is - and
why it emerges across domains
