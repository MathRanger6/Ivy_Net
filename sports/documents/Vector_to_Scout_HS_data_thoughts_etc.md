# Vector → Scout: Where Charles and I Are Headed (High School Data + Next Steps)

## Context

This note is meant to give you visibility into where **Charles and I are heading conceptually** in terms of strengthening the replication strategy.  

You already have the core pipeline and replication structure in place. What follows is **not a change in direction**, but rather an extension of the data layer that we think could meaningfully improve robustness and interpretability.

We especially wanted to share this now because:

> You may encounter points in the pipeline where certain relationships feel difficult to resolve or where signals appear confounded.

What we describe below is intended to help **unlock those constraints algorithmically**.

---

# 1. Why We Are Thinking About High School Data

Players are not randomly assigned to teams.

Stronger players tend to sort into stronger programs, which makes it difficult to cleanly interpret peer effects.

This may show up to you as:
- unstable estimates  
- difficulty separating individual vs pool effects  
- unclear signal attribution  

We are exploring **pre-college ability (high school recruiting rankings)** as a way to address this.

---

# 2. Why This Matters for You (Algorithmically)

This data enables:

## Decomposition
Separates:
- ability  
- environment  

## Stability
Provides a fixed anchor for player quality.

## Heterogeneity
Enables:
- talent-based differences in peer effects  
- clearer mechanism testing  

---

# 3. Data Source Direction

Primary:
- 247Sports Composite Rankings  

Secondary:
- Rivals / ESPN  
- McDonald’s All-American  

---

# 4. Model Extension

\[
Y_i =
\beta_1 \text{Perf}_i +
\beta_2 \text{PoolQ}_{jt}^{(-i)} +
\beta_3 (\text{PoolQ}_{jt}^{(-i)})^2 +
\gamma \text{HSRank}_i +
X_i'\delta +
\varepsilon_i
\]

---

# 5. Mission Alignment

This helps coordinate:
- Army setting  
- Basketball setting  

Toward identifying:
> a generalizable phenomenon in advancement systems.

---

# 6. Interpretation

This is not a pipeline change.

It is a **future unlock layer**.

Some constraints you encounter now:
- are structural  
- not implementation issues  

This data is designed to resolve those.

---

# 7. Bottom Line

Charles and I are exploring this to:

- improve identification  
- stabilize results  
- enable cross-domain comparison  
- support generalization  

---

## One-line summary

High school recruiting data will allow you to resolve current identification limits and better execute the mission.
