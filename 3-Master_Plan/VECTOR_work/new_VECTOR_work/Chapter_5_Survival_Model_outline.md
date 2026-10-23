# Chapter 5 — Survival Analysis, Competing Risks, and Army Advancement

## 5.1 Why the earlier Army HERO measure is useful but incomplete

The Army HERO analyses provided a useful descriptive view of advancement. They showed how promotion outcomes varied across groups defined by peer environment, relative standing, or related performance measures. These plots were valuable because they made the empirical phenomenon visible and helped motivate the broader competitive-congestion model.

However, advancement in the Army is inherently time-dependent. Promotion to Major is not only a question of whether an officer is eventually promoted, but also when that promotion occurs. Early promotion is one of the Army's clearest signals of exceptional organizational recognition and success.

The earlier descriptive HERO bars therefore capture only part of the process. They do not, by themselves, account for differences in follow-up time across officers, right censoring, officers who leave the Army before promotion, or the fact that promotion and departure are competing career transitions.

This chapter develops a more rigorous survival-analysis framework for measuring advancement in the Army while preserving the substantive question that motivated the original HERO analyses.

## 5.2 The Army career process as a competing-risks problem

We begin by defining the career process of interest:

- **Time origin:** promotion to Captain.
- **Event of interest:** promotion to Major.
- **Competing event:** departure from the Army before promotion to Major.
- **Right censoring:** the officer remains eligible for promotion when observation ends.

This is a competing-risks setting because departure can prevent the officer from later experiencing the event of interest.

An officer who leaves the Army before promotion should therefore not be treated simply as an officer who has "not yet" been promoted. Departure changes the set of possible future career outcomes.

The central descriptive question becomes:

> By a specified point in the career, what proportion of officers have been promoted to Major before experiencing a competing departure?

This probability is represented by the cumulative incidence function.

## 5.3 Aalen–Johansen estimation: improving the descriptive HERO

The first methodological extension is nonparametric.

The **Aalen–Johansen estimator** provides an estimate of the cumulative incidence of promotion while accounting for competing departure, right censoring, and the changing population at risk over time.

This offers a direct improvement over simple observed endpoint proportions.

Instead of asking:

> What fraction of officers in this group were ever observed to be promoted?

we can ask:

> What is the estimated cumulative incidence of promotion by a common horizon, accounting for competing departure and censoring?

This creates a natural bridge to the earlier HERO visualizations.

Possible outputs include:

1. **Cumulative-incidence curves** for groups defined by peer environment or relative standing.
2. **Fixed-horizon HERO bars**, where each bar is the Aalen–Johansen estimate of promotion incidence at a common career horizon.
3. **Mosaic plots** showing cumulative incidence across combinations of own performance and peer environment.

These plots preserve the intuitive appeal of the original HERO displays while placing the vertical measure on a more defensible time-to-event foundation.

## 5.4 Cause-specific Cox models: modeling the promotion process

A cause-specific Cox model asks a different question.

For promotion, the cause-specific hazard asks:

> Among officers who remain eligible for promotion and have not yet experienced promotion or competing departure, how does a covariate affect the instantaneous rate of promotion?

This approach is useful for understanding the promotion process itself.

Potential covariates include individual performance, peer quality, relative standing, unit prestige, branch, year group, age, sex, training and schooling, and other career characteristics.

A separate cause-specific model can also be estimated for departure.

This is important because the cumulative probability of promotion depends on both the rate at which promotion occurs and the rate at which officers leave before promotion.

Cause-specific Cox models therefore provide process-oriented insight but should not be interpreted directly as cumulative promotion probabilities.

## 5.5 Fine–Gray regression: adjusted inference on cumulative incidence

The **Fine–Gray model** addresses the cumulative incidence of the event of interest in the presence of competing risks.

Its scientific question is closer to:

> How are individual and environmental characteristics associated with the cumulative incidence of promotion when competing departure is taken into account?

Fine–Gray models the subdistribution hazard associated with the cumulative incidence function.

This makes it useful when the goal is to examine adjusted relationships between covariates and the probability of promotion over time.

Possible applications include estimating the association of peer environment, relative standing, unit prestige, performance, and other officer characteristics with the cumulative incidence of promotion.

Fine–Gray is not simply a replacement for cause-specific Cox. The two methods answer different questions.

### Cause-specific Cox

> Among officers still eligible, what changes the instantaneous rate of promotion?

### Fine–Gray

> How does a covariate relate to the cumulative incidence of promotion in the presence of competing departure?

Reporting both may therefore be useful when one model is used to understand the underlying transition process and the other is used to describe cumulative advancement outcomes.

## 5.6 Reconstructing the Army HERO with improved success measures

The central empirical test in this chapter is whether the Army HERO phenomenon persists when success is measured more rigorously.

### Step 1: Historical descriptive HERO

Reproduce the original descriptive pattern using the historical peer or relative-standing measure.

Document clearly the horizontal variable, population, outcome, observation window, and denominator.

### Step 2: Aalen–Johansen HERO

Re-estimate advancement using cumulative incidence and compare groups at a common career horizon.

Ask:

> Does the rise-and-decline pattern remain when censoring and competing departure are handled explicitly?

### Step 3: Adjusted survival models

Estimate cause-specific Cox and, where appropriate, Fine–Gray models.

Ask whether the empirical relationship persists after accounting for relevant covariates.

### Step 4: Compare the results

Compare raw observed promotion proportions, Aalen–Johansen cumulative incidence, cause-specific Cox results, and Fine–Gray cumulative-incidence relationships.

The goal is not to force these approaches to produce identical results. The goal is to understand what each one reveals about the same underlying advancement process.

## 5.7 Relationship to the competitive-congestion model

This chapter should reconnect the Army survival results to the general competitive-congestion framework.

The broader model argues that environmental effects cannot be understood independently of the selection mechanism.

In the Army, individual performance contributes to advancement, peer environment may alter competitive standing, promotion opportunities are limited, and some officers leave before promotion occurs.

The survival-analysis framework adds time and competing career transitions to that general model.

A particularly important question is whether the strongest congestion effects appear among officers near the empirically relevant selection margin.

This creates an opportunity to connect the Band of Excellence concept, competitive-relevance thresholds, scarcity, and time-to-promotion.

## 5.8 What remains to be verified before final reporting

Several historical and implementation questions remain open and should be resolved before the chapter is finalized.

### 5.8.1 Verify historical Fine–Gray usage

Determine whether a Fine–Gray model was actually run in the earlier Army analysis.

Identify the notebook and version, code cell, fitting method, input preparation, coefficients, and output figures.

Do not attribute historical figures to Fine–Gray unless the generating code confirms it.

### 5.8.2 Verify the longitudinal Cox implementation

Confirm whether the authoritative Cox model correctly preserves start and stop times, the common career clock, repeated officer records, and appropriate risk sets.

Historical interval-duration code may not represent a proper start-stop formulation.

### 5.8.3 Identify the final peer variable

For every selected Army figure, establish whether the horizontal quantity is full-group peer mean, leave-one-out peer mean, own-minus-peer relative standing, prestige, or shared congestion.

These quantities should not be treated as interchangeable.

### 5.8.4 Establish a common horizon

Choose and justify a meaningful follow-up horizon for cumulative-incidence comparisons.

Examples might include a career-year horizon, the typical Primary Zone timing, or another common point after promotion to Captain.

### 5.8.5 Reconcile event definitions and denominators

Verify promotion events, departure events, censored officers, time origin, follow-up duration, and cohort eligibility.

## 5.9 Scientific contribution of the chapter

The chapter should end with a substantive result, not a methodological one.

The main point is not that Aalen–Johansen or Fine–Gray are more sophisticated statistical methods.

The scientific contribution is that Army advancement is a **time-dependent competitive process with competing career exits**.

A simple binary or endpoint measure of success may obscure this structure.

A rigorous competing-risks framework allows us to ask whether the relationship between peer environment and advancement survives when we correctly account for timing, censoring, attrition, and competing career transitions.

If the HERO pattern remains under these stronger measures, the result becomes substantially more credible.

If the pattern changes, that is also scientifically important because it identifies which part of the earlier phenomenon was produced by differences in timing, follow-up, or attrition.

## Chapter logic in one line

**Historical Army HERO → competing-risks formulation → Aalen–Johansen cumulative incidence → cause-specific Cox → Fine–Gray regression → improved HERO → stronger definition of organizational success**
