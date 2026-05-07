# 2026-05-06 Alex Gates Briefing Outline

## Purpose

This note directly answers Alex's May 5 guidance for the next briefing:

1. Articulate the minimal Tier 1 model.
2. State the model components and minimal assumptions.
3. Identify the unit of modeling and the type/domain of each variable.
4. Explain how model objects correspond to fitted data features.
5. Define a fitting plan.
6. Show how the model can return an interpretable maximizing point.

The goal for tomorrow is not to present the final dissertation model. The goal is to show a disciplined, minimal, fit-able model function that can be connected to the current basketball data and extended later.

Companion narrative: `Tier1_Narrative_Outline.md` gives the fuller story arc: competing local forces, \(L\)-first Tier 1 framing, \(\Lambda\), fitting plan, variable domains, and reference addenda.

## 1. Unit Of Modeling

Primary unit: \((i,j,t)\), where \(i\) is player, \(j\) is team / local opportunity pool, and \(t\) is season.

The empirical row is a player-season or player-team-season. The local competitive environment is the team-season roster \(P_{jt}\). The advancement outcome is global: eventual NBA draft selection from the broader annual / cohort-level selection pool.

Working interpretation:

- Local opportunity is allocated inside \(P_{jt}\).
- Global distinction is allocated across the whole eligible population.
- The model asks how local pool structure affects global advancement probability.

## 2. Minimal Model Components

The briefing should separate the **minimal Tier 1 model** from the richer set of empirical quantities we can use to estimate and diagnose it. Otherwise the model will look like it already has too many moving parts.

### Core Tier 1 Structure

Minimal claim:

\[
\text{local environment} + \text{finite global distinction} \rightarrow \text{nonlinear advancement probability}
\]

The smallest useful Tier 1 model has three objects:

| Object | Role | Current basketball anchor |
| :--- | :--- | :--- |
| \(Y_i\) | global advancement outcome | eventual NBA draft selection |
| \(L_{ijt}\) | amalgamated local environment / local pool position | initially proxied by leave-self-out teammate quality |
| \(\Lambda_t\) | finite global selection capacity | annual NBA draft slots |

The key choice is to treat \(L_{ijt}\) as the Tier 1 amalgamated object. It can contain both the upside and downside of the local pool:

\[
L_{ijt} = \text{net local environment faced by player } i \text{ on team } j \text{ in season } t.
\]

Conceptually, \(L_{ijt}\) folds together:

- developmental / signaling benefit from stronger teammates,
- local crowding or competition for opportunity,
- opportunity exposure constraints,
- relative position inside the local pool.

For tomorrow's briefing, these should not all be presented as separate minimal-model variables. They are better described as **subcomponents we may later decompose**.

### First Empirical Proxy For The Amalgamated Term

First-pass empirical proxy:

\[
L_{ijt} \approx Q_{ijt} = Q_{jt}^{(-i)}
\]

where:

\[
Q_{ijt} = \frac{1}{|P_{jt}|-1}\sum_{\ell \in P_{jt}, \ell \neq i} A_{\ell jt}
\]

Current data forms:

- legacy `poolq_loo`,
- Tier 1 `congestion_quality`.

Interpretation:

- \(Q\) is not the whole theory.
- \(Q\) is the cleanest first proxy for local environment.
- The inverted-U can be presented as evidence that the net effect of local environment is beneficial at first and costly at the high end.

### Diagnostic Decomposition Variables

These variables matter, but they are not the headline minimal model:

| Quantity | Current data feature | Role in Tier 1 |
| :--- | :--- | :--- |
| \(A_{ijt}\) | `perf` / PPM | own-performance baseline and ingredient for local-pool construction |
| \(C_{ijt}\) | `congestion_crowding` | diagnostic decomposition of local environment into crowding pressure |
| \(C_{ijt}^{weighted}\) | `congestion_crowding_weighted` | exploratory opportunity-weighted crowding diagnostic |
| \(O_{ijt}\) | `minutes` | opportunity / exposure diagnostic; possible mediator or control |

Working interpretation:

- In Tier 1, \(C\), weighted \(C\), and \(O\) are ways to open up \(L\), not separate claims that the minimal model has six independent mechanisms.
- For fitting, \(A\) may be included as a baseline/control because draft selection depends on own performance, but the theoretical mechanism of interest remains the local environment term.

### Global Selection Capacity

Symbol: \(\Lambda_t\)

Meaning:

- Annual finite global selection capacity.
- Basketball example: approximately 60 NBA draft slots per year.

Outcome: \(Y_i = 1\) if player \(i\) is eventually drafted, otherwise \(Y_i=0\).

## 3. Minimal Assumptions

### A1. Local/Global Separation

Opportunity is local; advancement is global.

- Local pool: team-season roster.
- Global distinction: NBA draft selection.

This is the central structural distinction.

### A2. Leave-Self-Out Environment

Ego's local environment must exclude ego: \(Q_{jt}^{(-i)}\).

This avoids mechanically including the player's own performance in the peer-quality variable.

### A3. Variables Must Have Interpretable Domains

Alex's guidance: state which variables are normalized, bounded, Gaussian/standardized, or binary.

Current working domains:

| Object | Type / Domain | Empirical form |
| :--- | :--- | :--- |
| \(Y_i\) | binary, \(\{0,1\}\) | `Y_draft` |
| \(L_{ijt}\) | continuous, standardized or normalized | first proxied by `poolq_loo` or `congestion_quality` |
| \(A_{ijt}\) | continuous, standardized or raw positive rate | `perf` / PPM; baseline/control, not the core mechanism |
| \(C_{ijt}\) | continuous, standardized or normalized | decomposition diagnostic: `congestion_crowding`, `congestion_crowding_weighted` |
| \(O_{ijt}\) | nonnegative exposure; optionally normalized to \([0,1]\) | decomposition diagnostic: `minutes` |
| \(\Lambda_t\) | positive integer / fixed capacity | NBA draft slots |

Immediate standardization rule:

- For exploratory fitting, estimate with standardized \(L\) and standardized diagnostic terms so coefficients are comparable and the model behaves numerically.
- If a variable is interpreted as a share or probability, normalize to \([0,1]\).
- If a variable is interpreted as approximately Gaussian, use z-scores and check distribution shape.

### A4. Minimal Mechanisms Only

Tier 1 intentionally includes only:

- heterogeneous local pools,
- finite global selection,
- an amalgamated local-environment term that can later be decomposed.

Tier 1 intentionally excludes for now:

- endogenous sorting,
- strategic behavior,
- dynamic adaptation,
- network topology,
- evaluator bias,
- full causal identification.

The goal is mechanism sufficiency: can the minimal structure reproduce the observed inverted-U?

### A5. Shape Comes From Competing Margins

The central mechanism is that the net local-environment term has competing margins:

\[
L_{\text{net}}(Q)=B(Q)-D(Q)
\]

where \(B(Q)\) is the benefit side of stronger local peers and \(D(Q)\) is the downside / drag side.

At low-to-moderate local peer quality:

\[
B'(Q) > D'(Q)
\]

At high local peer quality:

\[
D'(Q) > B'(Q)
\]

The turning point is where:

\[
B'(Q^*) = D'(Q^*)
\]

So the advancement probability can rise with local environment at first and fall once the costly part of that same environment dominates.

## 4. Data Correspondence

Current basketball pipeline mapping:

| Model object | Meaning | Current data feature |
| :--- | :--- | :--- |
| \(Y_i\) | eventual global advancement | `Y_draft` |
| \(L_{ijt}\) | amalgamated local environment / local pool position | initially `poolq_loo` or `congestion_quality` |
| \(A_{ijt}\) | own ability / performance proxy | `perf` from `PERF_METRIC`, currently PPM; baseline/control |
| \(C_{ijt}\) | decomposition of \(L\): local crowding / roster pressure | `congestion_crowding` |
| \(C_{ijt}^{weighted}\) | decomposition of \(L\): opportunity-weighted crowding | `congestion_crowding_weighted` |
| \(O_{ijt}\) | decomposition of \(L\): opportunity / exposure | `minutes` |
| \(P_{jt}\) | local pool | team-season roster |
| \(\Lambda_t\) | global draft capacity | annual NBA draft slots |

Current implementation status:

- `535_sports_tier_1.ipynb` now constructs `congestion_quality`, `congestion_crowding`, and optionally `congestion_crowding_weighted`.
- CELL 4 can reproduce the `530_sports_pipeline.ipynb` binned-bar shape and can switch between legacy `poolq_loo` and Tier 1 mechanism variables.
- The next modeling step is a cleaner CELL 5 regression / model-fitting block.

## 5. Candidate Model Functions

### Minimal Diagnostic Shape Model

First diagnostic specification, using \(L\) as the amalgamated local-environment term:

\[
\begin{aligned}
\Pr(Y_i = 1) \approx{}& \alpha + \beta_1 L_{ijt} + \beta_2 L_{ijt}^2 \\
&+ \theta A_{ijt} + \eta_t + \varepsilon_{ijt}.
\end{aligned}
\]

Expected sign pattern for inverted-U in \(L\): \(\beta_1 > 0\) and \(\beta_2 < 0\).

Purpose:

- Not the final model.
- Useful because it returns a simple turning point.
- Keeps the minimal model focused on local environment and finite distinction, while allowing \(A\) as an own-performance baseline.

First empirical implementation:

- Set \(L_{ijt} = Q_{ijt}\), using `poolq_loo` or `congestion_quality`.
- Interpret the curvature in \(L\) as the reduced-form net of benefits and costs of the local environment.

### Decomposition / Guardrail Model

Only after the minimal shape is established, open \(L\) into diagnostic pieces:

\[
\begin{aligned}
\Pr(Y_i = 1) \approx{}& \alpha + \beta_1 Q_{ijt} + \beta_2 Q_{ijt}^2 \\
&+ \gamma D_{ijt} + \theta A_{ijt} + \eta_t + \varepsilon_{ijt}.
\end{aligned}
\]

where \(D_{ijt}\) is one diagnostic decomposition term at a time:

- \(C_{ijt}\): plain local crowding,
- \(C_{ijt}^{weighted}\): opportunity-weighted crowding,
- \(O_{ijt}\): minutes / exposure.

Purpose:

- Tests where the reduced-form curvature in \(L\) is coming from.
- Avoids presenting \(Q\), \(C\), \(O\), and weighted \(C\) as four separate minimal mechanisms.
- Preserves the April 30 guidance: the model stays minimal; richer terms are interpretive decomposition.

Possible interaction variant:

\[
\Pr(Y_i = 1) \approx \alpha + \beta Q_{ijt} + \gamma C_{ijt} + \kappa (Q_{ijt}\times C_{ijt}) + \theta A_{ijt} + \varepsilon_{ijt}.
\]

This variant is useful if the question becomes whether quality is beneficial only when crowding is low, but it should be presented as a diagnostic extension, not the first minimal model.

### Probabilistic / MLE Version

Once the functional form is fixed, use a binary response model:

\[
\Pr(Y_i=1) = g^{-1}(\alpha + \beta_1 L_{ijt} + \beta_2 L_{ijt}^2 + \theta A_{ijt})
\]

where \(g^{-1}\) can be logit or probit.

Estimator:

- MLE for logit/probit.
- OLS/LPM remains the first diagnostic because it is transparent and easy to compare to binned means.

## 6. Fitting Plan

### Step 1: Descriptive Shape

Fit no model first:

- bin \(Q\),
- plot mean `Y_draft` by bin,
- compare first proxies for \(L\): `poolq_loo` and `congestion_quality`,
- treat plain `congestion_crowding` and weighted crowding as decomposition diagnostics after the reduced-form shape is clear.

Purpose:

- Confirm the phenomenon remains visible under each variable definition.
- Avoid fitting a model to an artifact of stale data or a bad binning choice.

### Step 2: Diagnostic Least Squares

Fit \(Y_i \sim L + L^2 + A\) using OLS / LPM, where \(L\) is first proxied by `poolq_loo` or `congestion_quality`.

Purpose:

- Estimate the sign and scale of the quadratic relationship.
- Recover a first-pass turning point without overloading the minimal model.

### Step 3: Binary Response / MLE

Fit the same conceptual model using logit or probit: \(Y_i \sim \text{Logit/Probit}(L, L^2, A)\).

Purpose:

- Respect binary outcome structure.
- Estimate a generalizable model function.
- Compare whether the fitted maximum is stable relative to LPM.

### Step 4: Robustness / Specification Checks

Candidate checks:

- season fixed effects,
- team or conference controls if needed,
- cluster-robust standard errors by team or player where appropriate,
- compare equal-width bins vs quantile bins,
- add one diagnostic decomposition term at a time: plain crowding, weighted crowding, or minutes,
- print unclipped predictions before trusting any plotted model curve.

### Step 5: Generalizable Function

Define a reusable function \(\widehat{p}(Y=1 \mid L,A)\), with optional decomposition diagnostics.

Inputs:

- standardized \(L\),
- ability/performance proxy \(A\),
- optional diagnostic term \(D\),
- optional season controls.

Outputs:

- predicted draft probability,
- fitted coefficients,
- estimated maximizing \(L^*\),
- uncertainty interval for \(L^*\) if feasible.

## 7. Extracting The Maximum / Turning Point

### Quadratic LPM Turning Point

If \(\widehat{p}(L) = \alpha + \beta_1 L + \beta_2 L^2 + \text{controls}\), holding controls fixed, then:

\[
\frac{\partial \widehat{p}}{\partial L} = \beta_1 + 2\beta_2 L
\]

Set derivative equal to zero:

\[
\beta_1 + 2\beta_2 L^* = 0
\]

So:

\[
L^* = -\frac{\beta_1}{2\beta_2}
\]

Interpretation:

- \(L^*\) is the estimated local-environment level at which predicted advancement probability is maximized, conditional on controls.
- If \(L\) is proxied by \(Q\), then \(L^*\) can be reported as the corresponding \(Q^*\) in the original peer-quality units.
- If \(L\) is standardized, convert the estimate back to the original units for interpretation.

### Logit / Probit Turning Point

If \(\widehat{p}(L) = g^{-1}(\alpha + \beta_1 L + \beta_2 L^2 + \text{controls})\), and \(g^{-1}\) is monotonic, then the maximum in probability occurs at the same \(L^*\) as the maximum of the linear index when the only local-environment terms are \(L\) and \(L^2\).

If a later diagnostic model includes both \(L^2\) and an \(L \times D\) interaction, then:

\[
L^*(D) = -\frac{\beta_1 + \kappa D}{2\beta_2}
\]

This is useful as a later diagnostic because it can answer: "Does the maximizing local-environment level change when a specific decomposition term is high?"

## 8. What To Show Alex Tomorrow

### Direct Answer To "What Is The Model?"

The model is a minimal local/global advancement model:

\[
\text{amalgamated local environment} + \text{finite global selection} \rightarrow \text{nonlinear advancement probability}
\]

The unit is player-team-season. The local pool is team-season. The outcome is eventual global draft selection. In the first empirical implementation, the amalgamated local-environment term is proxied by leave-self-out teammate quality.

### Direct Answer To "What Are The Minimal Assumptions?"

- Advancement is globally scarce.
- Opportunity is locally scarce.
- Teammate quality is leave-self-out.
- The Tier 1 local-environment term amalgamates benefits and costs of the local pool.
- Decomposition variables such as crowding, weighted crowding, and minutes are diagnostics, not separate minimal mechanisms.
- Variables used for fitting are standardized or normalized before fitting.
- Tier 1 excludes dynamic sorting and network structure.

### Direct Answer To "How Does This Fit The Data?"

Current data already contains or now constructs:

- outcome: `Y_draft`,
- first proxy for \(L\): `poolq_loo` / `congestion_quality`,
- own-performance baseline: `perf`,
- optional decomposition diagnostics: `congestion_crowding`, `congestion_crowding_weighted`, and `minutes`.

The next fitting block estimates \(Y \sim L + L^2 + A\) first by OLS/LPM, then by logit/probit MLE. Diagnostic extensions add one decomposition term at a time.

### Direct Answer To "What Do You Pull Out?"

The main extractable object is:

\[
L^* = -\frac{\beta_1}{2\beta_2}
\]

When \(L\) is proxied by \(Q\), this can be reported as the \(Q^*\) value that maximizes predicted advancement probability. With later decomposition interactions:

\[
L^*(D) = -\frac{\beta_1 + \kappa D}{2\beta_2}
\]

This gives the estimated local-environment level that maximizes predicted advancement probability.

### Open Decisions

- Whether `congestion_quality` should replace legacy `poolq_loo` as the first proxy for \(L\).
- Whether `congestion_crowding_weighted` helps decompose \(L\) more clearly than plain `congestion_crowding`.
- Whether the first decomposition model should add \(C\), weighted \(C\), minutes, or an interaction.
- Whether opportunity (`minutes`) should be treated as a diagnostic, control, mediator, or separately estimated component.
- Whether the first briefing should emphasize LPM transparency or MLE correctness.

## 9. Immediate Deliverable After Briefing

Implement CELL 5 in `sports/535_sports_tier_1.ipynb`:

1. Prepare standardized variables \(Y, A, L\), starting with \(L=Q\); keep \(C\), weighted \(C\), and \(O\) available as decomposition diagnostics.
2. Fit minimal diagnostic LPM: \(Y \sim L + L^2 + A\), first with \(L=Q\).
3. Print coefficients, unclipped predictions, and \(L^*\) / \(Q^*\).
4. Fit logit/probit equivalent.
5. Compare \(L^*\) across legacy `poolq_loo` and `congestion_quality`, then add plain/weighted crowding only as decomposition diagnostics.
6. Export one table and one figure only after the specification is stable.
