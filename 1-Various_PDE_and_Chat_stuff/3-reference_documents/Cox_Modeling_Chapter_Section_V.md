# Section V: Operationalization: Implementing Cox Regression for Officer Promotion Analysis

## A. Data Structure: Time-Varying Survival Intervals

The transition from theoretical model to empirical implementation requires transforming the complex, dynamic structure of military officer careers into a format that survival analysis methods can process. Unlike traditional regression models that assume a single observation per individual, survival analysis with time-varying covariates requires a more sophisticated data structure that captures how officers' characteristics evolve over time. This structure, known as the **time-varying survival interval format**, allows us to model how changing circumstances—such as accumulating performance metrics, shifting unit assignments, or evolving peer group contexts—influence promotion intensity throughout an officer's career.

### From Snapshots to Survival Intervals: The Data Transformation Challenge

Our analysis begins with **snapshot data**: periodic records (typically quarterly) that capture each officer's status at specific points in time. Each snapshot includes the officer's current rank, unit assignment, and other time-varying characteristics as of that date. However, survival analysis requires a different structure: **survival intervals** that represent periods during which an officer's covariates remain constant, with each interval contributing to the analysis of promotion timing.

The transformation from snapshots to survival intervals involves creating records of the form [start_time, stop_time), where each interval represents a period during which an officer's covariates are constant. At the start of each interval, we know the officer's covariate values (performance metrics, unit assignment, etc.), and the interval ends either when the covariates change (creating a new interval) or when an event occurs (promotion or attrition). This structure allows the Cox model to update covariate values over time, capturing how changing circumstances influence promotion intensity.

### Interval Creation: Capturing Temporal Dynamics

For each officer, we create a sequence of survival intervals that span their career from their Captain promotion date (Date of Rank, or DOR CPT) until either promotion to Major, attrition, or the end of the study period. Each interval [t_start, t_stop) includes:

1. **Time boundaries**: The start and stop times for the interval, measured in days from the officer's Captain promotion date
2. **Covariate values**: All time-varying covariates as of the start of the interval, including:
   - Cumulative OER performance metrics (top blocks received, evaluations received)
   - Current unit assignment (prestige unit indicator)
   - Pool metrics (peer group characteristics)
   - Ratings given metrics (evaluations provided to subordinates)
3. **Event indicator**: Whether the interval ended with an event (promotion or attrition) or was censored

This structure ensures that each interval represents a period of constant covariates, allowing the Cox model to properly account for time-varying effects. When an officer's characteristics change—for example, when they receive a new evaluation or move to a different unit—a new interval begins with updated covariate values.

### Event Determination: Identifying Promotion and Attrition

The final interval for each officer determines the event type. Officers who are promoted to Major during the study period have an event indicator of 1 (promotion), with the promotion date serving as the stop time for their final interval. Officers who leave service before promotion have an event indicator of 2 (attrition), with their last service date as the stop time. Officers still in service at the end of the study period without promotion are right-censored (event = 0), with the study end date as their stop time.

This event coding is critical for the competing risks framework, which models promotion and attrition as separate, mutually exclusive events. An officer cannot both be promoted and attrit during the same time period, and the competing risks model allows us to estimate separate hazard functions for each event type, recognizing that the factors influencing promotion may differ from those influencing attrition.

### Scale and Complexity: Managing Large-Scale Administrative Data

The transformation from snapshots to survival intervals creates a substantial dataset: with 201,038 officers observed over 24 years, each with multiple quarterly snapshots, the resulting survival interval dataset contains millions of records. Each officer may contribute dozens of intervals, as their covariates change throughout their career. This scale presents both opportunities and challenges: the large sample size provides statistical power to detect subtle effects, but it also requires careful attention to computational efficiency and data quality.

Data quality checks are essential at this stage. We must ensure that intervals are properly ordered, that there are no gaps or overlaps in coverage, and that event indicators are correctly assigned. Invalid intervals—such as those with negative duration or stop times before start times—must be identified and addressed. Similarly, officers with missing critical information (such as Captain promotion dates) cannot be included in the analysis, as the time origin is undefined.

## B. Software and Library Selection

The choice of statistical software and libraries for implementing Cox regression is not merely a technical detail—it fundamentally shapes what analyses are possible and how results are interpreted. For our analysis of military officer promotion with competing risks and time-varying covariates, the available options differ substantially in their capabilities, and the choice of software determines whether we can properly address our research questions.

### Why scikit-survival Over Alternatives: The Competing Risks Imperative

We selected **scikit-survival (sksurv)**, a Python library that extends the scikit-learn ecosystem to survival analysis, over alternatives such as **lifelines** or **R's survival package**. This choice was driven primarily by the need to properly handle competing risks—the simultaneous modeling of promotion and attrition as separate, mutually exclusive events.

**Lifelines**, while popular and user-friendly, has significant limitations for our application:
- It cannot adequately handle competing risks in a unified framework
- Its support for time-varying covariates in competing risks contexts is limited
- It cannot model the separate hazard functions for promotion and attrition that our research questions require

**scikit-survival** addresses these limitations by providing:
- A robust competing risks framework that allows separate hazard functions for different event types
- Proper handling of multiple event types with time-varying covariates
- Better integration with the scikit-learn ecosystem, enabling consistent workflows for data preprocessing, model fitting, and evaluation
- Support for regularization (L1/L2 penalties) for variable selection in high-dimensional settings

### Key scikit-survival Components: Building Blocks of the Analysis

The implementation relies on several key components from scikit-survival:

**`sksurv.util.Surv`**: The fundamental data structure for survival analysis, combining event indicators and survival times into a single object that the Cox model can process. This structure encodes both whether an event occurred (and what type) and when it occurred (or when observation ended for censored cases).

**`sksurv.linear_model.CoxPHSurvivalAnalysis`**: The Cox proportional hazards regression model, which estimates the regression coefficients **β** that determine how covariates influence promotion intensity. This class provides methods for fitting the model, accessing coefficient estimates and hazard ratios, and making predictions.

**`sksurv.metrics.concordance_index_censored`**: A measure of model predictive accuracy, the concordance index (C-index) evaluates how well the model ranks officers by their promotion timing. A C-index of 1.0 indicates perfect prediction, while 0.5 indicates performance no better than random. This metric is essential for comparing different model specifications and assessing model fit.

**Regularization support**: scikit-survival supports L1 and L2 penalties for variable selection and handling high-dimensional covariate spaces. This capability is valuable when exploring large sets of potential predictors, allowing the model to automatically identify the most important factors while penalizing unnecessary complexity.

### Integration with Data Processing Pipeline

scikit-survival integrates seamlessly with the broader Python data science ecosystem, including pandas for data manipulation, NumPy for numerical computations, and scikit-learn for preprocessing. This integration enables a streamlined workflow: data preparation, model fitting, and evaluation can all be performed within a single environment, reducing the complexity of moving data between different software packages and ensuring consistency in data handling.

## C. Model Specification: From Research Questions to Statistical Models

Model specification is the bridge between our research questions and the statistical analysis. It requires translating theoretical concepts—such as "prestige unit service influences promotion timing" or "peer group quality affects evaluation outcomes"—into specific variables and functional forms that the Cox model can estimate. The specification process involves selecting which covariates to include, determining how to measure them, and deciding on the appropriate model structure.

### Static (Time-Invariant) Variables: Stable Characteristics

**Demographics and basic characteristics** provide baseline information about each officer that does not change over time:

- **Sex**: Binary indicator for officer sex, allowing examination of potential gender differences in promotion timing
- **Year group (YG)**: The cohort year in which the officer was commissioned, captured through dummy encoding to allow for cohort-specific baseline hazards. Year group is critical because promotion policies can vary by cohort, and officers in different year groups face different promotion environments
- **Age at Captain promotion**: Continuous variable measuring the officer's age when promoted to Captain, which may influence subsequent promotion timing

These static variables serve as controls, accounting for baseline differences between officers that might otherwise confound the effects of time-varying covariates such as performance metrics or unit assignments.

### Time-Varying Covariates: Capturing Career Dynamics

**OER Performance Metrics** track how an officer's evaluation history evolves over time. These metrics are computed cumulatively, meaning that at each snapshot date, we calculate the officer's performance history up to that point:

- **Cumulative top blocks received**: The ratio of top block evaluations (the highest possible rating) received from raters and senior raters, calculated as the number of top blocks divided by total evaluations received. This metric captures the officer's performance trajectory, with higher values indicating consistently strong evaluations
- **Cumulative evaluations received**: The total number of evaluations received from raters and senior raters, which may influence promotion timing both directly (more evaluations provide more information to selection boards) and indirectly (officers with more evaluations have had more opportunities to demonstrate performance)
- **Grade-based metrics**: Separate cumulative metrics for the Captain period versus earlier periods, recognizing that evaluations received as a Captain may be more relevant for Major promotion than evaluations received as a Lieutenant
- **Rolling window metrics**: Performance metrics calculated over the last N evaluations, capturing recent performance trends that may be more influential than distant history

**Prestige and Unit Metrics** capture the organizational context of an officer's career:

- **Prestige unit indicator**: Binary variable indicating whether the officer is currently assigned to a prestige unit at each snapshot date. This time-varying covariate allows us to model how current assignment in a prestige unit influences promotion intensity
- **Cumulative prestige unit service**: The total quarters or proportion of career spent in prestige units, capturing the cumulative effect of prestige unit experience

**Pool Metrics** measure the peer group context in which evaluations occur:

- **OER pool metrics**: Characteristics of the peer group within the officer's organization at the time of each evaluation, such as the average performance level of peers or the distribution of evaluations within the pool. These metrics capture how an officer's performance is evaluated relative to their peers
- **Prestige pool metrics**: The proportion of officers in prestige units within the officer's peer group, measuring the organizational prestige context of evaluations

**Ratings Given Metrics** track the officer's role as an evaluator:

- **Cumulative ratings given**: The number of evaluations the officer has provided to subordinates, which may signal leadership experience and organizational influence
- **Top blocks given ratio**: The proportion of top block evaluations the officer has given, which may reflect their standards or the quality of their subordinates

### Model Types: Progressive Complexity

We fit multiple model specifications to understand how different sets of covariates influence promotion timing:

**Static Model**: Includes only time-invariant variables (demographics, year group, age at Captain promotion). This baseline model establishes how much of the variation in promotion timing can be explained by stable characteristics alone.

**Full Model**: Adds all time-varying covariates (OER metrics, prestige unit assignments, pool metrics, ratings given metrics). This comprehensive specification addresses our primary research questions about how performance, organizational context, and peer group effects influence promotion timing.

**Competing Risks Model**: Extends the full model to separately estimate hazard functions for promotion and attrition, recognizing that these are distinct events with potentially different determinants. This model allows us to examine whether factors that increase promotion intensity also reduce attrition intensity, or whether these relationships are more complex.

## D. Handling Competing Risks: Promotion vs. Attrition

A fundamental challenge in analyzing military officer promotion is that officers can exit the promotion process through two distinct pathways: promotion to Major (the desired outcome) or attrition from service (an alternative outcome). These events are **competing risks**—mutually exclusive events that can terminate the observation period. Treating attrition as simple censoring (as in standard survival analysis) implicitly assumes that officers who leave would have had the same promotion hazard as those who remain, an assumption that is likely violated in practice.

### Why Competing Risks Matter: The Attrition Problem

Officers who attrit may have different underlying promotion probabilities than those who remain. Some officers may leave because they recognize low promotion likelihood, while others may leave despite high promotion potential because they receive better opportunities elsewhere. Still others may leave for reasons unrelated to promotion (family circumstances, health issues, etc.). Treating all attrition as simple censoring ignores these distinctions and can lead to biased estimates of promotion hazard.

The competing risks framework addresses this by modeling promotion and attrition as separate events with potentially different hazard functions. This allows us to:
- Estimate how covariates influence promotion intensity separately from how they influence attrition intensity
- Understand whether factors that increase promotion likelihood also reduce attrition likelihood, or whether these relationships are more complex
- Calculate **cumulative incidence functions** that show the probability of promotion accounting for the competing risk of attrition

### Implementation: Separate Hazard Functions

In the competing risks framework, we estimate two separate Cox models:

**Promotion Model**: h₁(t|X) = h₀₁(t) × exp(**β₁**ᵀ**X**), where h₁(t|X) is the hazard of promotion at time t, h₀₁(t) is the baseline promotion hazard, and **β₁** are the regression coefficients for promotion.

**Attrition Model**: h₂(t|X) = h₀₂(t) × exp(**β₂**ᵀ**X**), where h₂(t|X) is the hazard of attrition at time t, h₀₂(t) is the baseline attrition hazard, and **β₂** are the regression coefficients for attrition.

Each model is fit using only the relevant events: the promotion model uses intervals ending in promotion (event = 1), treating attrition and censoring as censored observations. The attrition model uses intervals ending in attrition (event = 2), treating promotion and censoring as censored observations.

### Comparing Coefficients: Understanding Differential Effects

Comparing the coefficients **β₁** and **β₂** reveals how covariates influence promotion versus attrition. For example, if prestige unit assignment has a positive coefficient in the promotion model but a negative coefficient in the attrition model, this suggests that prestige unit service both increases promotion intensity and reduces attrition intensity—a "win-win" scenario. Alternatively, if a covariate has opposite signs in the two models, this suggests a trade-off: the factor may increase promotion likelihood but also increase attrition likelihood, or vice versa.

### Cumulative Incidence: Accounting for Competing Risks

The **cumulative incidence function** for promotion, F₁(t), represents the probability of being promoted by time t, accounting for the competing risk of attrition. This differs from the standard survival function, which treats attrition as censoring. The cumulative incidence function recognizes that officers who attrit are no longer at risk for promotion, and it properly accounts for this in calculating promotion probabilities.

Calculating cumulative incidence requires estimating both hazard functions and then combining them appropriately. This provides a more accurate picture of promotion probabilities than standard survival analysis, which would overestimate promotion probabilities by treating attrition as if those officers might still be promoted.

## E. Model Evaluation: Assessing Fit and Predictive Accuracy

Model evaluation serves multiple purposes: it helps us understand how well the model fits the data, identifies potential problems with model assumptions, and allows us to compare different model specifications. For Cox regression, evaluation focuses on two key aspects: **predictive accuracy** (how well the model ranks officers by promotion timing) and **assumption validity** (whether the proportional hazards assumption holds).

### Concordance Index: Measuring Predictive Accuracy

The **concordance index (C-index)**, also known as Harrell's C-statistic, measures how well the model ranks officers by their promotion timing. For each pair of officers where one is promoted before the other (or one is promoted and the other is censored), the C-index asks: does the model assign higher predicted hazard to the officer who was promoted first?

The C-index ranges from 0.5 to 1.0:
- **C-index = 0.5**: The model performs no better than random chance
- **C-index = 1.0**: The model perfectly ranks all officer pairs
- **C-index > 0.7**: Generally considered good predictive performance
- **C-index > 0.8**: Excellent predictive performance

In practice, C-index values above 0.65 are often considered acceptable for survival models, particularly when working with complex, real-world data where many factors influencing outcomes may be unobserved. For our analysis of 201,038 officers, even modest improvements in C-index represent substantial gains in predictive accuracy.

The C-index is calculated using `sksurv.metrics.concordance_index_censored`, which properly handles censored observations by only comparing pairs where the outcome is known (both promoted, or one promoted and one censored with censoring time after promotion time).

### Testing the Proportional Hazards Assumption

The **proportional hazards assumption**—that hazard ratios are constant over time—is fundamental to the Cox model. Violations of this assumption can lead to biased coefficient estimates and incorrect inferences. Testing this assumption involves examining **Schoenfeld residuals**, which measure the difference between observed and expected covariate values at each event time.

For each covariate, we test whether the Schoenfeld residuals are correlated with time. If they are, this suggests that the covariate's effect changes over time, violating the proportional hazards assumption. Statistical tests (such as the Grambsch-Therneau test) provide formal tests of this assumption.

When violations are detected, several approaches are available:
- **Stratification**: Fit separate baseline hazards for different groups (e.g., by year group), allowing the baseline to vary while maintaining proportional hazards within each stratum
- **Time-varying coefficients**: Allow covariate effects to change over time, though this requires more complex modeling
- **Time-dependent covariates**: Include interactions between covariates and time, allowing effects to vary with time

For our analysis, we test the proportional hazards assumption for all covariates and report any violations. In practice, minor violations may not substantially affect results, particularly when the primary interest is in identifying which factors influence promotion timing rather than precisely estimating hazard ratios.

### Model Comparison: Static vs. Full Model

Comparing the static model (demographics only) to the full model (including all time-varying covariates) reveals how much additional explanatory power comes from dynamic career characteristics. We compare models using:
- **C-index improvement**: How much does predictive accuracy increase when adding time-varying covariates?
- **Likelihood ratio test**: A formal statistical test comparing nested models (static model is nested within full model)
- **Coefficient significance**: Which time-varying covariates have statistically significant effects?

This comparison addresses our research questions directly: if prestige unit assignment or performance metrics significantly improve model fit and have substantial coefficients, this provides evidence that these factors influence promotion timing.

## F. Special Considerations for Military Data

Military administrative data presents unique challenges that require careful attention throughout the analysis. These challenges stem from the scale of the data, the complexity of military career structures, and the nature of administrative record-keeping. Addressing these considerations is essential for producing reliable, interpretable results.

### Cohort Effects and Year Group Stratification

Officers are organized into **year groups**—cohorts of officers commissioned in the same year. Promotion policies can vary by year group, with different Below Zone and Primary Zone windows for different cohorts. These policy differences create **cohort effects**: officers in different year groups face different promotion environments, even if their individual characteristics are identical.

To account for cohort effects, we **stratify** the Cox model by year group. Stratification fits separate baseline hazards for each year group while estimating common regression coefficients across all groups. This approach recognizes that the baseline promotion intensity may differ by year group (reflecting policy differences) while assuming that the effects of covariates (such as performance metrics or prestige unit assignment) are similar across year groups.

Stratification is implemented in scikit-survival by including year group as a stratification variable, which creates separate baseline hazards h₀(t) for each year group while maintaining a single set of regression coefficients **β** that apply to all groups.

### Data Quality Challenges: Missing Dates and Invalid Intervals

Administrative data inevitably contains errors and missing information. Critical challenges include:

**Missing Date of Rank (DOR)**: Officers without a valid Captain promotion date cannot be included in the analysis, as the time origin is undefined. We identify and exclude these cases, reporting the number of excluded officers.

**Invalid Intervals**: Survival intervals must have positive duration (stop_time > start_time) and must be properly ordered (each interval's start_time equals the previous interval's stop_time). Invalid intervals are identified and either corrected (when possible) or excluded.

**Multiple Promotions**: Rare cases where an officer appears to have multiple promotion dates (data entry errors) require careful handling. We use the first valid promotion date and flag cases for manual review.

**Date Inconsistencies**: Snapshot dates that don't align with known career events (e.g., a snapshot showing an officer as a Captain after their Major promotion date) indicate data quality issues that must be addressed.

### Computational Considerations: Scale and Efficiency

With 201,038 officers and millions of survival intervals, computational efficiency is essential. Several strategies help manage this scale:

**Vectorized Operations**: Using pandas and NumPy vectorized operations rather than row-by-row processing dramatically improves performance. Operations on entire columns are orders of magnitude faster than iterating over rows.

**Efficient Data Structures**: Storing survival intervals in a format that minimizes memory usage while enabling fast lookups and joins is critical. We use pandas DataFrames with appropriate data types (e.g., categorical variables for year groups) to reduce memory footprint.

**Parallel Processing**: For computationally intensive steps (such as calculating pool metrics), we leverage parallel processing using Ray, which distributes computations across multiple CPU cores. This is particularly valuable for pool metrics, which require comparing each officer to their peer group.

**Incremental Processing**: Rather than processing all officers simultaneously, we can process year groups or other subsets separately and combine results, reducing memory requirements and enabling checkpointing of intermediate results.

### Handling Large Sample Sizes: Statistical vs. Practical Significance

With 201,038 officers, even very small effects can achieve statistical significance due to the large sample size. This requires careful interpretation: a coefficient may be statistically significant (p < 0.05) but practically negligible (e.g., a hazard ratio of 1.01, representing a 1% increase in promotion intensity).

We address this by:
- **Reporting effect sizes**: Focusing on hazard ratios and their practical interpretation, not just p-values
- **Confidence intervals**: Providing 95% confidence intervals for hazard ratios to show the range of plausible effects
- **Practical significance thresholds**: Considering effects with hazard ratios very close to 1.0 (e.g., between 0.95 and 1.05) as practically insignificant, even if statistically significant

This approach ensures that we identify factors with meaningful influence on promotion timing, not just factors with detectable but trivial effects.

---

*This section has detailed the operationalization of Cox regression for military officer promotion analysis, from data structure transformation through model specification, competing risks handling, evaluation, and special considerations. The following section will place this methodological approach in the broader context of survival analysis applications in labor economics and business research, highlighting both the commonalities and unique aspects of the military promotion context.*






