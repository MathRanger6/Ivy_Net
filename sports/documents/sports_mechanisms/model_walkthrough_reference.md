
# Model Walkthrough Reference
## Nonlinear Peer Effects in Promotion

---

# 1. Model Specification

\[
Y_i = \beta_1 \text{Perf}_i 
+ \beta_2 \text{PoolQ}_{jt}^{(-i)} 
+ \beta_3 \left(\text{PoolQ}_{jt}^{(-i)}\right)^2 
+ X_i' \gamma 
+ \varepsilon_i
\]

---

# 2. Big Picture

This model states:

> Advancement depends on individual performance AND peer-group quality, with nonlinear effects driven by signal quality and congestion.

---

# 3. Components

## Outcome: \(Y_i\)

- Indicator for advancement (e.g., going professional)
- \(Y_i = 1\) if advancement occurs, 0 otherwise

---

## Individual Performance: \(\text{Perf}_i\)

- Measures individual ability (e.g., BPM, efficiency)
- Coefficient \(\beta_1 > 0\)

Interpretation:
Higher individual performance increases probability of advancement.

---

## Pool Quality: \(\text{PoolQ}_{jt}^{(-i)}\)

- Average quality of peers (team \(j\), season \(t\))
- Excludes individual \(i\) (leave-one-out)

Interpretation:
Captures evaluation environment.

---

## Linear Effect: \(\beta_2\)

- Effect of increasing peer quality at low levels
- Expected: positive

---

## Nonlinear Effect: \(\beta_3\)

- Captures curvature in peer effects

\[
\beta_3 < 0
\]

Interpretation:
At high levels of peer quality, marginal effects become negative.

---

# 4. Combined Effect of Peer Quality

\[
\beta_2 \cdot \text{PoolQ} + \beta_3 \cdot \text{PoolQ}^2
\]

This creates an inverted-U relationship:

- Low pool quality → weak signal
- Moderate pool quality → strongest advancement
- High pool quality → congestion

---

# 5. Turning Point

\[
\text{Turning Point} = -\frac{\beta_2}{2\beta_3}
\]

Interpretation:
The level of pool quality where marginal returns switch from positive to negative.

---

# 6. Marginal Effect

\[
\frac{\partial Y_i}{\partial \text{PoolQ}} = \beta_2 + 2\beta_3 \text{PoolQ}
\]

- Positive at low values
- Negative at high values

---

# 7. Controls: \(X_i'\gamma\)

Includes:
- Position
- Class year
- Team performance
- Year effects

Purpose:
Hold constant other determinants of advancement.

---

# 8. Error Term: \(\varepsilon_i\)

Captures:
- Unobserved factors
- Random variation

---

# 9. Core Empirical Test

\[
\beta_3 < 0
\]

This is the defining test of the inverted-U relationship.

---

# 10. Interpretation Summary

| Pool Quality | Effect on Advancement |
|-------------|---------------------|
| Low | Low signal → low advancement |
| Medium | Strong signal → highest advancement |
| High | Congestion → reduced advancement |

---

# 11. One-Sentence Insight

> Peer quality improves advancement—until congestion dominates.
