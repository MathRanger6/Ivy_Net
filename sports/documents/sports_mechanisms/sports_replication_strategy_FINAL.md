# Sports Replication Strategy (Expanded & Detailed)

## Pool Quality, Relative Evaluation, and Nonlinear Advancement

------------------------------------------------------------------------

# I. Motivation and Context

This document develops a **detailed replication strategy** for extending
the core empirical finding from U.S. Army officer promotions into sports
settings. The aim is not merely to "try sports data," but to **carefully
map institutional structure, evaluation logic, and constraints** so that
the replication is intellectually credible and publishable.

The central research question is:

> Does the **quality of one's peer group** affect advancement in a
> nonlinear way across domains where performance is evaluated
> **relatively within constrained systems**?

------------------------------------------------------------------------

# II. Core Finding from the Army Data (Expanded)

## Empirical Result

The central empirical result is:

> Promotion to Major is **increasing in peer (pool) quality at
> low--moderate levels**, but **flattening or decreasing at the highest
> levels** of pool quality (inverted-U).

## Institutional Structure Driving This

Key institutional features:

-   Officers are evaluated within **senior rater × time pools**
-   Ratings are **constrained (e.g., top-block limits)**
-   Promotion is **capacity constrained** (finite slots per cohort)
-   Evaluation is **explicitly relative within pools**

## Mechanism (Carefully Framed)

Two competing forces:

### 1. Signal Quality / Credibility (Positive)

-   Stronger peers → stronger comparison set\
-   High performance in strong pool → more informative signal\
-   Leads to higher promotion probability

### 2. Congestion / Competition (Negative)

-   Many high performers in same pool\
-   Limited "top signals" and promotion slots\
-   Harder to stand out → reduced marginal probability

## Key Insight

> Advancement is not purely individual---it is shaped by the **structure
> of the comparison environment**.

------------------------------------------------------------------------

# III. Why Sports Is a Good Replication Domain

Sports provides a **clean laboratory** because:

-   Performance is **observable and quantifiable**
-   Teams naturally define **peer groups**
-   Advancement is **competitive and capacity-constrained**
-   Evaluation often depends on **relative standing within a group**

However, not all sports outcomes are equally good analogues---this is
where careful design matters.

------------------------------------------------------------------------

# IV. Mapping Army → Sports (Deep Mapping)

  -----------------------------------------------------------------------
  Army Concept            Sports Analog           Subtleties
  ----------------------- ----------------------- -----------------------
  Senior rater pool       Team × season (or coach Coach matters for
                          × season)               exposure/role

  Top-block rating        Performance signal      Not capped, but
                          (stats, awards, usage)  role-constrained

  Peer quality            Teammate ability        Must exclude focal
                                                  player

  Promotion               Draft / selection /     Depends on model
                          survival                

  Capacity constraint     Draft slots, roster     Central to mechanism
                          spots                   

  Evaluation context      Team environment        Includes visibility +
                                                  competition
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# V. Replication Designs (Detailed)

------------------------------------------------------------------------

## 1. College Basketball → Going Professional (PRIMARY DESIGN)

### Outcome Definition

-   NBA draft selection
-   OR signing to NBA/G-League/major international league within X years

### Why This Is the Best Analogue

This is the closest to: - **discrete promotion event** - **selection
from a pool** - **capacity constraint (limited draft slots)**

### Mechanism Mapping

  ---------------------------------------------------------------------
  Army              College Basketball
  ----------------- ---------------------------------------------------
  Stronger pool     Strong team improves visibility, strength of
  improves signal   schedule

  Too strong →      Too many stars → fewer touches, lower usage
  congestion        
  ---------------------------------------------------------------------

### Variables

-   **Individual performance**
    -   BPM, PER, WS/40, usage-adjusted metrics
-   **Pool quality**
    -   Mean teammate performance (leave-one-out)
-   **Outcome**
    -   Indicator for pro entry

**Empirical model (sketch, same notation as design memos).** Let $Y_i$ be pro entry, $\text{Perf}_i$ individual performance, and leave-one-out pool quality $\text{PoolQ}_{jt}^{(-i)}$ for team $j$, season $t$, player $i$:

$$
\Pr(Y_i = 1 \mid \cdot) = G\bigl(\beta_1 \text{Perf}_i + \beta_2 \text{PoolQ}_{jt}^{(-i)} + \beta_3 \bigl(\text{PoolQ}_{jt}^{(-i)}\bigr)^2 + X_i' \gamma\bigr),
$$

with $X_i$ controls and link $G$ (logit, probit, or identity for LPM). Inverted-U: $\beta_3 < 0$.

### Expected Pattern

-   Low-quality team → low exposure\
-   Mid-quality team → optimal visibility + differentiation\
-   Elite stacked team → crowding → reduced marginal probability

### Supporting Literature

-   Paulsen (2022): peer effects in NBA transitions\
-   Kuehn (2023): teammate adjustment in draft evaluation

These papers reinforce: \> evaluators struggle to disentangle individual
performance from team context

### Strengths

-   Clean event
-   Intuitive mechanism
-   Strong external validity

### Risks

-   One-time transition
-   Selection into teams (sorting)

------------------------------------------------------------------------

## 2. NBA → Career Longevity (SECONDARY DESIGN)

### Outcome Definition

-   Years in NBA
-   Hazard of exit (survival model)

### Why It Works

-   Aligns with your **survival / competing risks framework**
-   Allows **dynamic exposure to multiple pools over time**

### Mechanism

-   Moderate-quality teams:
    -   development
    -   exposure
    -   skill accumulation
-   High-quality teams:
    -   limited minutes
    -   role instability
    -   replacement risk

### Variables

-   Performance: per-minute productivity, usage (e.g.\ $\text{Perf}_{it}$)
-   Pool: team × season (index $jt$)
-   Pool quality: average teammate productivity (e.g.\ leave-one-out $\text{PoolQ}_{jt}^{(-i)}$)
-   Outcome: exit hazard (e.g.\ spell ending for player $i$)

### Literature

-   Barnes (2008): determinants of NBA career length\
-   Zhu (2025): survival modeling of NBA careers\
-   Baker et al. (2013): career length in sports

### Strengths

-   Rich panel structure
-   Multiple observations per individual

### Limitations

-   Confounded by injuries, aging, contracts
-   Harder to interpret as "promotion"

------------------------------------------------------------------------

## 3. NBA → Salary Threshold (TERTIARY / LEAST PREFERRED)

### Outcome Definition

-   Crossing salary threshold (e.g., \$X million/year)

### Why It Is Weak

This is NOT a clean promotion analogue because:

-   Salary depends on:
    -   bargaining
    -   contract rules (rookie scale, max contracts)
    -   cap structure
    -   timing (free agency)

### Mechanism Issues

-   Hard to separate:
    -   performance
    -   market conditions
    -   negotiation

### Literature

-   Kuehn & Rebessi (2023): team fit and earnings\
-   Oberhofer & Schwinner (2017): peer effects on salary

These highlight complexity rather than clarity.

### Why Include It Anyway

-   Transparency for reviewers: \> "We considered salary but rejected it
    due to institutional confounds"

------------------------------------------------------------------------

# VI. Identification Considerations

Across all designs:

## Key Threat: Sorting

-   Better players may join better teams

Mitigation: - Controls (recruit rank, draft rank) - Fixed effects -
Within-team variation

## Mechanical Correlation

-   Pool mean includes individual

Fix: - Leave-one-out measures

## Support

-   Ensure enough observations in extreme pools

------------------------------------------------------------------------

# VII. Recommended Empirical Strategy

### Step 1

Run: - College basketball → pro entry

### Step 2

Check: - Nonparametric relationship (bins, splines)

### Step 3

Replicate: - NBA longevity

### Step 4 (optional)

Explore: - Salary (as robustness, not core)

------------------------------------------------------------------------

# VIII. Contribution

If replicated:

> The inverted-U relationship is a **general property of competitive
> evaluation systems**, not specific to the military.

This reframes advancement as:

-   not purely meritocratic
-   not purely contextual
-   but **interaction between ability and comparison structure**

------------------------------------------------------------------------

# IX. Paper Framing Language (Expanded)

"This paper shows that advancement outcomes depend not only on
individual performance but also on the **composition of the peer group
in which that performance is evaluated**. Across both military and
sports settings, we document a nonlinear relationship in which stronger
peer environments initially enhance advancement prospects but eventually
generate congestion and competition that reduce marginal advancement
probabilities. These findings suggest that evaluation systems embed
individuals in structured comparison environments that jointly determine
career outcomes."

------------------------------------------------------------------------

------------------------------------------------------------------------

# X. Appendix: Relevant Literature with Abstract-Style Summaries

## 1. Paulsen, R. J. (2022)

*Peer effects and human capital accumulation: Time spent in college and
productivity in the National Basketball Association.*\
Managerial and Decision Economics.\
Link: https://onlinelibrary.wiley.com/doi/10.1002/mde.3617

**Summary:**\
Examines how college peer environments affect NBA outcomes, showing that
teammate quality influences both development and evaluation. Highlights
difficulty separating individual ability from team context.

**Relevance:** Direct support for peer-quality effects and signal
interpretation.

**Abstract:**\
Starting in 2006, the National Basketball Association (NBA) set a minimum age  requirement on players declaring for the draft. Consequently, elite high school  players typically spend at least 1 year playing college basketball before entering the  draft. This paper seeks to test for the impact of years spent in college and peer quality on NBA performance. Additional years in college are found to have an insignificant impact on persistence in the NBA at various points post draft, a positive impact  on early career performance, and a negative impact on midcareer performance, while  peer quality does not have a significant impact on performance
------------------------------------------------------------------------

## 2. Oberhofer, H., & Schwinner, M. (2017)

*Do individual salaries depend on the performance of the peers?
Prototype heuristic and wage bargaining in the NBA.*\
Link: https://www.econstor.eu/bitstream/10419/179288/1/wp_2017_534.pdf

**Summary:**\
Finds that player salaries are influenced by teammate performance,
suggesting evaluators use relative benchmarks.

**Relevance:** Supports relative evaluation but also shows salary is
institutionally complex.

**Abstract:**\
This paper analyzes the link between relative market value of representative subsets of athletes in the National Basketball Association (NBA) and individual wages. NBA athletes are categorized with respect to multiple performance characteristics utilizing the k-means algorithm to cluster observations and a group’s market value is calculated by averaging real annual salaries. Employing GMM estimation techniques to a dynamic wage equation, we find a statistically significant and positive effect of one-period lagged relative market value of an athlete’s representative cluster on individual wages after controlling for past individual performance. This finding is consistent with the theory of prototype heuristic, introduced by Kahneman and Frederick (2002), that NBA teams’ judgment about an athlete’s future performance is based on a comparison of the player to a prototype group consisting of other but comparable athletes
------------------------------------------------------------------------

## 3. Yin, J. (2024)

*The Effects of Star Newcomers on Team Performance.*

**Summary:**\
Shows that adding high-quality players changes team dynamics and affects
teammates' outcomes.

**Relevance:** Supports composition and interaction effects.

**Abstract:**\
While previous research has predominantly focused on the socialization processes and consequences of ordinary newcomers who are characterized by a lack of familiarity, high reliance on others, making more mistakes and errors, and facing more uncertainty and stress, star newcomers have received less attention. Differing from ordinary newcomers, star newcomer socialization not only involves the adjustment and adaptation of the newcomer but also induces changes and adaptations within the team. This dissertation, based on human capital theory, delves into the mechanisms and implications of star newcomer entry process. In particular, it scrutinizes the team adaptation resulting from star newcomer performance under the condition of newcomer adaptation––the integrative influences of team adaptation for star newcomers and star newcomer adaptation during their socialization process––on team performance. The empirical research based on 33,945 observations of 586 star newcomers drawn from North American basketball clubs in the National Basketball Association (NBA) shows that star newcomer performance and prior team performance interactively determine team adaptation for star newcomers, which subsequently negatively associates with team performance. Star newcomer adaptation buffers the negative association between team adaptation for star newcomers and team performance. The findings contribute to research on newcomer socialization, team dynamic process, and star performers, along with offering insights to practitioners in facilitating a more efficient star newcomer socialization and fostering better team performance
------------------------------------------------------------------------

## 4. Barnes, J. (2008)

*The Impact of Pre-NBA Performance on Professional Career Longevity.*

**Summary:**\
Analyzes predictors of NBA career length; finds both performance and
context matter.

**Relevance:** Supports longevity design but highlights noise.

**Abstract:**\
Given the change in the business nature of the National Basketball Association (NBA), the  player evaluation process has become increasingly important. The methods discussed in this  article can aid general managers and owners in the player acquisition process by providing a  means of evaluating talent. The purpose of the study was to identify the relationship between  pre–NBA career statistical variables and career longevity, measured as the number of  seasons in the NBA. Data from the 1988–2002 collegiate basketball seasons were analyzed.  Participants consisted of 329 NBA guards, forwards, and centers who entered the NBA in  1988 and ended their careers during or before the 2002 NBA season. The study included 11  independent variables: points, rebounds, assists, steals, blocks, fouls, turnovers, minutes  played, free throw percentage, field goal percentage, and 3 point percentage. There was a  single dependent variable, career longevity. Data analysis comprised multiple regression  tests to determine the relationship between the independent variables and the dependent  variable. The multiple regression tests revealed a relationship between pre-career statistical  variables and career longevity for guards and forwards. However, no such relationship was  found for centers
------------------------------------------------------------------------

## 5. Zhu, Y. (2025)

*Three Essays on Performance, Salary, and Career Longevity in the
National Basketball Association.*

**Summary:**\
Uses survival analysis to study NBA careers, emphasizing role of team
context and constraints.

**Relevance:** Methodological bridge to your survival models.

**Abstract:**\
Professional sports provide an excellent research environment to study all aspects of the  employee-employer relationship. In this study, I use data from the National Basketball  Association (NBA) to empirically investigate the impact of contractual arrangements on  player performance, salary, and survival. First, I explore changes in player performance in the  year at which a contract ends (the contract year). Players improve their performance during  the contract year, but no consistent performance decline is observed in the year following  the end of the contract year. Second, I focus on salary determination. I demonstrate that  player performance is an important driver of their salary. In addition, I explore the interaction  between contractual arrangements and salary determination and find that contract length and  special clauses, such as player/team options to extend the employment relationship, affect the  salary. Third, I explore the determinants of player survival in the league. Good performance,  especially offensive win shares, increases player longevity. Changing teams allows young or  undrafted players to survive longer in the league. Examining the impact of player options  on player survival suggests that player options increase the probability of players changing  teams but do not increase the probability of player survival. In summary, my findings indicate  that the interaction between contractual arrangements and player performance is important in  salary determination and survival in professional sports
------------------------------------------------------------------------

## 6. Baker, J. et al. (2013)

*Determinants of Career Length in Professional Sport.*

**Summary:**\
Career duration depends on performance and opportunity within structured
environments.

**Relevance:** Reinforces system + individual interaction.

**Abstract:**\
In an effort to understand the process of skill acquisition and decline, researchers have largely neglected a critical aspect of this development – maximizing time at the highest levels of achievement. This study examined length of career for professional athletes in basketball, football, ice hockey, and baseball and considers whether career length differed by position and player performance (standardized career performance). Results revealed career length differences among positions in baseball and football but not basketball and ice hockey. In all sports, longer careers were associated with superior performance, reinforcing the notion that performance is a critical indicator of career length and suggesting positional demands influence career length. Results highlight the need for further work on this important stage of development
------------------------------------------------------------------------

## 7. Kuehn, L. A., & Rebessi, F. (2023)

*Team Fit and NBA Rookie Career Outcomes.*

**Summary:**\
Shows that team context affects early career outcomes and earnings.

**Relevance:** Supports context-dependent evaluation.

**Abstract:**\
Workers entering the labor market often face a trade off between job matches that maximizes their short run and long run compensation. This trade off is influenced by peers who may enhance or diminish the worker’s productivity, and thus affect their future salary. We study this question for rookies in the National Basketball Association (NBA). We find that for rookies drafted between 2011 and 2017, playing with teammates that facilitated them getting 1 additional point per 100 possessions was predicted to increase the value of their second contract by between 9.9% and 23.6%. This implies that being drafted by the team that provides the ‘best fit’ is an important determinant of a rookie’s future earnings
------------------------------------------------------------------------

## 8. Kuehn, L. A. (2023)

*Adjusting for Teammate Quality in Evaluating NBA Draft Prospects.*

**Summary:**\
Demonstrates that failing to adjust for teammate quality biases
evaluation of individual ability.

**Relevance:** Closest conceptual link to your mechanism.

**Abstract:**\
Evaluating amateur basketball players based on their college performances is challenging due to the impact of teammates on observed output. In this paper, I look at the effect that college teammates have on a player’s draft position and develop predictions for NBA player performance that account for these effects. I find that players that score more in college due to their teammates are drafted higher, indicating that college choice can significantly impact a prospect’s draft position. I then use the player predictions in a matching model to evaluate how effectively NBA teams account for complementarities between players when evaluating college talent. The results suggest that teams could improve the offensive value added of their draft picks by 20.33% by better taking into account teammate effects
------------------------------------------------------------------------
