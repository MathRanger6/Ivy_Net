# OR / Systems Approach

## Overview

This document presents a **fully expanded Operations Research / Systems
framing** of the empirical finding---an inverted-U relationship between
promotion probability and peer pool quality---using the language of
**dynamic allocation, queueing systems, and network flows**.

The central interpretation is that promotion operates as a
**capacity-constrained flow system**, where individuals are processed
through evaluation nodes that generate signals used in downstream
allocation decisions.

This document is intentionally positioned for: - Operations Research
(INFORMS-style audiences) - Queueing and stochastic systems - Workforce
allocation and service systems

Throughout, we explicitly distinguish: - **Descriptive / associational
evidence (what the data show)**\
- **Systems / optimization interpretations (how an OR model would
interpret it)**

------------------------------------------------------------------------

# (a) Mechanism (OR / Systems Language)

From an operations-research perspective, the promotion system can be
modeled as a **dynamic resource allocation process over a network of
evaluation nodes**. Officers flow through a sequence of assignments and
evaluation pools (senior rater × time), where each pool functions as a
**local processing node** that transforms underlying performance into
observable signals used for downstream promotion decisions.

The key empirical object---mean top-block rate in a pool---can be
interpreted as a **state variable capturing node composition and
effective signal environment**. Pools with higher average performance
may correspond to nodes with higher human-capital density, stronger
evaluators, or more informative signal generation processes. In such
environments, an individual's observed output may be more informative
about latent ability, effectively increasing their **priority weight**
in the downstream promotion queue. This produces the upward-sloping
portion of the empirical relationship: as node quality increases, signal
quality and interpretability improve, increasing throughput probability.

However, promotion operates under **capacity constraints**, and these
constraints interact with node composition to generate congestion. When
a node contains many high-performing individuals, it generates a **high
arrival rate of high-priority candidates** into the promotion stage.
Because downstream capacity is limited, this produces a **crowding
effect**: multiple strong candidates compete for limited promotion
slots, and the marginal probability of selection declines for each
individual. In queueing terms, the system experiences **priority-class
congestion**, where the arrival rate of high-priority jobs increases
relative to service capacity.

This produces a **non-monotonic (inverted-U) relationship** between node
quality and individual promotion probability. At low to moderate node
quality, improvements in signal precision dominate. At high node
quality, congestion effects dominate, reducing individual throughput
probability. This interpretation is consistent with a
**capacity-constrained, priority-based allocation system**, but should
be understood as a **systems-consistent interpretation of observational
evidence**, not as causal identification.

------------------------------------------------------------------------

# (b) Conceptual Model Sketch (OR-Oriented)

## System Structure

-   Discrete time periods t = 1,...,T\
-   Agents move through a network of **evaluation nodes (pools)**\
-   A downstream **promotion stage** allocates limited capacity

The system resembles a **multi-stage service system with preprocessing
nodes**.

------------------------------------------------------------------------

## State Variables

-   q_pt: pool quality (mean TB rate)\
-   n_pt: pool size\
-   x_it: individual performance signal\
-   μ_pt: signal precision at node p\
-   λ_t: promotion capacity\
-   F_pt: distribution of performance within pool

------------------------------------------------------------------------

## Decision Variables (Latent)

-   Assignment of individuals to pools\
-   Evaluation rules within pools\
-   Promotion selection policies

These are not observed but define the underlying system.

------------------------------------------------------------------------

## Flow Representation

1.  Individuals enter pools\
2.  Pools generate signals (ranking / evaluation)\
3.  Signals enter a promotion queue\
4.  Capacity-constrained selection occurs

------------------------------------------------------------------------

## Constraints

-   Capacity constraint: total promotions ≤ λ_t\
-   Relative evaluation: signals interpreted within pools\
-   Information constraint: signals are noisy and context-dependent

------------------------------------------------------------------------

## Objective (Interpretive, Not Estimated)

Maximize expected quality of promoted individuals subject to: - capacity
constraints\
- information limitations\
- decentralized evaluation

------------------------------------------------------------------------

## Operational Meaning of Inverted-U

The inverted-U reflects a tradeoff between:

1.  **Signal Quality Effect**\
    Higher q_pt improves μ_pt (signal precision)

2.  **Congestion Effect**\
    Higher q_pt increases arrival rate of high-priority candidates

This implies an interior operating region balancing: - information
quality\
- congestion costs

Analogous to: - optimal utilization in queues\
- bottleneck dynamics in service systems

------------------------------------------------------------------------

# (c) Analysis Extensions

## Feasible with Current Data

-   Heterogeneity by branch / cohort\
-   Pool size effects (proxy for congestion)\
-   Distributional measures within pool\
-   Leave-one-out pool means\
-   Alternative functional forms (splines)\
-   Stability across time\
-   Competing risks robustness\
-   Support diagnostics

------------------------------------------------------------------------

## Requires Additional Data

-   Assignment mechanisms\
-   Promotion capacity over time\
-   Network structure\
-   Rater behavior\
-   Full career paths

------------------------------------------------------------------------

# (d) Reviewer-Risk Table

  -----------------------------------------------------------------------
  Critique             Why It Arises               Preemption
  -------------------- --------------------------- ----------------------
  Endogeneity of       Non-random pool placement   Controls, sensitivity
  assignment                                       analyses

  Mechanical           Shared rating structure     Leave-one-out measures
  correlation                                      

  Lack of structural   OR expectation              Provide conceptual
  model                                            model

  Congestion           Inferred indirectly         Use proxies (size,
  unobserved                                       dispersion)

  Capacity unobserved  Missing key constraint      Treat as latent

  Nonlinearity         Binning concerns            Nonparametric checks
  artifact                                         

  Limited dynamics     OR preference for dynamic   Emphasize repeated
                       models                      structure
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# (e) Literature Streams

## Queueing & Congestion

-   Dynamic assignment in queues\
-   Heterogeneous server models\
-   Priority queues and congestion

## Workforce / Service Systems

-   Workforce agility\
-   Service operations as queueing systems

## Dynamic Allocation

-   Staffing and allocation under uncertainty

## Behavioral Queueing

-   Visibility and prioritization in queues

------------------------------------------------------------------------

# Final Bridge

This OR/systems framing interprets promotion as **flow through
capacity-constrained evaluation nodes**, where signal generation and
congestion jointly determine outcomes.

The key insight is that: \> increasing node quality improves information
but also increases competition for limited capacity, producing nonlinear
advancement outcomes.

This provides a systems-based interpretation of the empirical inverted-U
pattern while remaining consistent with observational identification.
