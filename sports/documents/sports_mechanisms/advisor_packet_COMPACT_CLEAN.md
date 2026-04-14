# Advisor Packet (Compact, High-Density)

## Nonlinear Peer Effects in Promotion

------------------------------------------------------------------------

## I. Executive Summary + II. Army Finding (Combined)

**Claim.** Advancement depends on individual performance **and**
peer-group quality, with **nonlinear effects** due to signal quality (↑)
and congestion (↓).

**Army setting.** Evaluation within senior-rater × time pools;
constrained top ratings; finite promotion slots; explicitly relative
evaluation.

**Result.** Promotion probability can be written as

$$
\Pr(\text{Promote}_i) = f\bigl(\text{Perf}_i,\, \text{PoolQ}_{jt}^{(-i)}\bigr),
$$

which is **inverted-U** in pool quality: in a spec with linear and squared pool terms, expect $\beta_3 < 0$ on $\bigl(\text{PoolQ}_{jt}^{(-i)}\bigr)^2$.

**Mechanism.** - **Signal quality ( + )**: stronger peers → more
credible signal\
- **Congestion ( − )**: many strong peers + scarce slots → harder to
stand out

------------------------------------------------------------------------

## III. Why Sports (Replication Logic)

Sports provide observable performance, natural pools (teams), and
capacity constraints (draft/rosters). Test whether the same inverted-U
emerges outside the military.

**Mapping** - Pool: senior rater × time → **team × season** -
Performance: TB/rating → **BPM/efficiency** - Advancement: Major → **pro
entry / survival** - Constraint: slots → **draft/roster limits**

------------------------------------------------------------------------

## IV. Designs (Keep to 2)

### A. College Basketball → Pro Entry (Primary)

-   **Outcome** ($Y_i=1$) if pro entry within $k$ years\
-   **Pool**: team × season\
-   **Mechanism**: visibility (↑) vs role/touch congestion (↓)

### B. NBA → Career Longevity (Secondary)

-   **Outcome**: years in league / exit hazard\
-   **Mechanism**: development (↑) vs role crowding (↓)

------------------------------------------------------------------------

## V. Empirical Design (College; concise)

**Data.** Sports-Reference (college), Basketball-Reference (draft/NBA)

**Sample.** NCAA D1, 2000--2023, player×season, minutes ≥ threshold

**Key variables** — leave-one-out pool quality:

$$
\text{PoolQ}_{jt}^{(-i)} = \frac{1}{N_{jt}-1} \sum_{k \in \mathcal{P}_{jt},\, k \neq i} \text{Perf}_{kt}.
$$

**Model (LPM/logit)**

$$
Y_i = \beta_1 \text{Perf}_i + \beta_2 \text{PoolQ}_{jt}^{(-i)} + \beta_3 \bigl(\text{PoolQ}_{jt}^{(-i)}\bigr)^2 + X_i' \gamma + \varepsilon_i.
$$

**Test:** $\beta_3 < 0$.\
**Turning point**

$$
-\frac{\beta_2}{2\beta_3}.
$$

**Controls**: year FE, position, class, team win%, (optional conference
FE)

------------------------------------------------------------------------

## VI. Diagnostics (keep tight)

-   **Bins/plot**: deciles of $\text{PoolQ}$ → visualize inverted-U\
-   **Leave-one-out**: avoid mechanical bias\
-   **Clustering**: team-level SEs\
-   **Support**: check tails

------------------------------------------------------------------------

## VII. Identification (one-liners)

-   **Sorting** (better players → better teams): control for
    observables; robustness\
-   **Exposure vs ability**: part of mechanism, not pure bias\
-   **Measurement**: BPM as proxy for overall contribution

------------------------------------------------------------------------

## VIII. Expected Pattern

Low $\text{PoolQ}$ → weak signals; mid → peak advancement; high
→ congestion → decline.

------------------------------------------------------------------------

## IX. Literature (short anchors)

-   Paulsen (2022): peer effects & NBA outcomes\
-   Kuehn (2023): adjust for teammate quality\
-   Barnes (2008); Zhu (2025): longevity/survival\
-   Oberhofer & Schwinner (2017): peer effects in pay (complex outcome)

------------------------------------------------------------------------

## X. Contribution (one line)

Generalizes that **relative evaluation under capacity constraints**
yields **nonlinear peer effects** on advancement.

------------------------------------------------------------------------

## XI. Advisor Questions (quick)

1)  Outcome: draft vs broader pro entry?\
2)  Performance metric: BPM sufficient?\
3)  Need recruiting controls?\
4)  Framing: replication vs general theory?
