# Section II: Cox Proportional Hazards Model

## A. The Cox Model: Formulation and Assumptions

When analyzing how organizations identify and promote talent, a fundamental challenge emerges: how do we model the timing of career milestones when traditional regression methods fail to account for the complex temporal structure of careers? The Cox proportional hazards model, developed by Sir David Cox in 1972, provides a powerful solution to this challenge, offering a framework that has become the standard method for analyzing time-to-event data across fields ranging from medical research to labor economics. In the context of military officer promotion, where the timing of advancement serves as a key indicator of assessed potential, the Cox model's ability to handle censored observations and time-varying covariates makes it particularly well-suited for understanding the factors that influence career progression.

The model's popularity stems from its semi-parametric nature, which provides flexibility while maintaining interpretability. Unlike fully parametric models that require specifying a particular probability distribution for the time-to-event, the Cox model allows the baseline hazard to take any form, making it robust to various underlying promotion processes. This flexibility is particularly valuable when analyzing large-scale administrative data, such as our dataset of 201,038 officers over 24 years, where the true promotion process may be complex and influenced by numerous unobserved factors.

### Semi-Parametric Approach: Flexibility Without Distributional Assumptions

The Cox model is **semi-parametric** because it makes no assumptions about the form of the baseline hazard function h₀(t). Unlike fully parametric models (such as the Weibull or exponential models), which require specifying a particular probability distribution for the time-to-event, the Cox model allows the baseline hazard to take any form. This flexibility is particularly valuable when the underlying hazard distribution is unknown or complex, as is often the case in organizational and career progression research where promotion processes may be influenced by numerous unobserved factors.

The baseline hazard can take any shape—increasing, decreasing, or non-monotonic—and the model will estimate it from the data. This allows the data to determine the shape of the baseline hazard, making the model robust to various underlying promotion processes. In the context of military promotion, where structured timelines create natural promotion windows (Below Zone, Primary Zone), the baseline hazard should theoretically reflect these institutional structures, with the model learning the exact shape from the data rather than imposing a predetermined form.

### Model Formulation: Separating Time-Dependent and Individual-Specific Effects

The Cox model decomposes the hazard function into two components: a **baseline hazard** h₀(t), which represents the underlying temporal pattern of promotion intensity common to all officers (before accounting for individual characteristics), and covariate effects that modify this baseline. The baseline hazard captures how promotion intensity changes over time in the absence of covariate effects, while the covariate effects determine how individual characteristics shift an officer's promotion intensity relative to this baseline.

The Cox proportional hazards model expresses the hazard function for an individual with covariate vector **X** = (X₁, X₂, ..., Xₚ) as:

$$h(t|\mathbf{X}) = h_0(t) \times e^{\beta_1 X_1 + \beta_2 X_2 + \ldots + \beta_p X_p}$$

or more compactly:

$$h(t|\mathbf{X}) = h_0(t) e^{\beta^T \mathbf{X}}$$

where:
- h(t|**X**) is the hazard function at time t for an individual with covariates **X**
- h₀(t) is the baseline hazard function, common to all individuals but unspecified in form
- **β** = (β₁, β₂, ..., βₚ) is a vector of regression coefficients to be estimated
- **X** = (X₁, X₂, ..., Xₚ) is a vector of covariates, which may include both static variables (such as demographic characteristics or year group) and time-varying variables (such as cumulative performance metrics or current unit assignments)

The model's structure separates the time-dependent baseline hazard h₀(t) from the covariate effects, which are assumed to be constant over time (the proportional hazards assumption, discussed below). This separation is powerful because it allows us to model how promotion intensity changes over time (through the baseline hazard) while simultaneously accounting for how individual characteristics influence promotion intensity (through the covariate effects).

### The Proportional Hazards Assumption: Constant Relative Effects Over Time

A fundamental assumption of the Cox model is that of **proportional hazards**: the hazard ratio between any two individuals is constant over time. In our promotion context, where "hazard" represents promotion intensity (the instantaneous rate at which promotions occur), this means that if one officer has twice the promotion intensity of another at time t₁, they will also have twice the promotion intensity at time t₂, regardless of the values of t₁ and t₂. Mathematically, for two individuals with covariate vectors **X₁** and **X₂**, the hazard ratio is:

$$\frac{h(t|\mathbf{X}_1)}{h(t|\mathbf{X}_2)} = \frac{h_0(t) e^{\beta^T \mathbf{X}_1}}{h_0(t) e^{\beta^T \mathbf{X}_2}} = e^{\beta^T (\mathbf{X}_1 - \mathbf{X}_2)}$$

which is constant over time, as the baseline hazard h₀(t) cancels out.

This assumption implies that covariate effects are multiplicative and constant over time. For example, if being currently assigned to a prestige unit increases promotion intensity by 50%, it increases promotion intensity by 50% at all times while the officer remains in that unit. This type of time-varying covariate effect (reflecting current status) may reasonably satisfy the proportional hazards assumption.

However, the proportional hazards assumption may not hold for all types of covariates. A distinction must be made between the effect of *being* in a prestige unit (a time-varying covariate reflecting current assignment) and the effect of *having been* in a prestige unit (reflecting past experience). The effect of past prestige unit service may decay over time—for instance, having served in a prestige unit as a junior officer may have a stronger influence on promotion to Major than on later promotions to higher ranks, as the relevance of early career experiences may diminish over time. This type of non-linear decay in the influence of past experiences could violate the proportional hazards assumption. When the proportional hazards assumption is violated, the estimated hazard ratio represents an average effect over the observation period rather than a constant effect, and the model may still provide useful insights, though interpretation becomes more nuanced.

For the specific case of promotion to Major, which occurs relatively early in an officer's career and within a relatively narrow time window, the proportional hazards assumption is often reasonable. The effect of covariates such as prestige unit assignment or performance metrics on promotion to Major is likely to be relatively stable over the observation period, as officers are being evaluated for the same promotion milestone. Diagnostic tests, such as Schoenfeld residual tests, can be used to assess whether the proportional hazards assumption holds for specific covariates. If violations are detected, alternative approaches such as time-varying coefficient models or stratification by time periods can be employed.

### Baseline Hazard and Covariate Effects: Understanding the Components

The **baseline hazard** h₀(t) represents the hazard function (promotion intensity) for an individual with all covariates equal to zero (or at their reference levels). It captures the underlying temporal pattern of promotion intensity that is common to all officers, before accounting for individual characteristics. The baseline hazard is left unspecified in the Cox model, which means we do not need to assume a particular functional form (e.g., increasing, decreasing, or constant over time). This allows the data to determine the shape of the baseline hazard, making the model robust to various underlying promotion processes.

**Covariate effects** in the Cox model are multiplicative on the baseline hazard. This means that each covariate multiplies the baseline hazard by a factor e^{βᵢXᵢ}. For example, if β₁ = 0.5 for prestige unit assignment (coded as 1 for prestige unit, 0 otherwise), then officers in prestige units have a hazard that is e^{0.5} ≈ 1.65 times the baseline hazard, or 65% higher promotion intensity, at all times. This multiplicative structure is intuitive: it means that the effect of a covariate is proportional to the baseline hazard, so if the baseline hazard is high (e.g., during the Primary Zone window), the effect of a covariate is also proportionally larger.

## B. Partial Likelihood Estimation: Estimating Effects Without Specifying the Baseline

The Cox model is estimated using **partial likelihood**, a method that allows estimation of the regression coefficients **β** without specifying the baseline hazard function h₀(t). This is one of the model's key advantages, as it avoids the need to make distributional assumptions about the time-to-event. The method exploits the fact that, under the proportional hazards assumption, the baseline hazard cancels out when comparing individuals at risk at the same time.

### Why Partial Likelihood?

Partial likelihood estimation uses only information from observed event times, not from censored times, yet still incorporates information from censored observations through the risk set (the set of individuals still at risk at each event time). The partial likelihood function is constructed by considering, at each observed event time, the probability that the event occurred to the specific individual who experienced it, given that an event occurred to someone in the risk set at that time. This probability depends only on the covariate values and the regression coefficients, not on the baseline hazard.

This approach is computationally efficient, particularly for large datasets, because it requires evaluating the likelihood only at observed event times, not at all possible times. This makes the Cox model well-suited for analyzing large-scale administrative data, such as the military personnel records used in this research. In our analysis of 201,038 officers, this computational efficiency is essential for practical implementation.

### Maximum Partial Likelihood Estimation

The regression coefficients **β** are estimated by maximizing the partial likelihood function. This is typically done using iterative numerical methods, such as the Newton-Raphson algorithm, as there is no closed-form solution. The resulting estimates are consistent and asymptotically normally distributed under standard regularity conditions, providing reliable inference even with large sample sizes.

### Handling Tied Event Times: When Multiple Promotions Occur Simultaneously

A practical challenge in survival analysis is the presence of **tied event times**—multiple events occurring at the same time. In military promotion research, this is common because promotions often occur on specific dates (e.g., the first day of a fiscal year or promotion board results date), meaning many officers may be promoted on the same day.

Several methods exist for handling ties in the Cox model:
- **Breslow's method**: Approximates the partial likelihood by assuming all tied events occur at slightly different times
- **Efron's method**: Provides a better approximation by considering the order in which tied events might have occurred
- **Exact method**: Computes the exact partial likelihood for tied events, but is computationally intensive

For most applications, Efron's method provides a good balance between accuracy and computational efficiency, and is often the default in statistical software packages. In our analysis, where many promotions occur on the same dates, this method ensures accurate estimation while maintaining computational feasibility.

## C. Interpretation: Hazard Ratios and Their Meaning

The coefficients **β** in the Cox model are most commonly interpreted through **hazard ratios (HR)**, which provide intuitive measures of the effect of covariates on promotion intensity. The hazard ratio represents the multiplicative change in promotion intensity (hazard) associated with a one-unit increase in a covariate (or, for binary variables, the change associated with the covariate being present versus absent). In the context of military officer promotion, this tells us how much a covariate increases or decreases an officer's likelihood of being promoted at any given time, relative to the baseline promotion intensity.

### Hazard Ratio Definition

For a covariate Xᵢ with coefficient βᵢ, the hazard ratio is:

$$\mathrm{HR} = e^{\beta_i}$$

### Interpreting Hazard Ratios: What Do They Mean in Practice?

**HR > 1**: An increase in the covariate is associated with increased promotion intensity (faster promotion). For example, if prestige unit assignment has HR = 1.5, officers in prestige units have 50% higher promotion intensity than officers not in prestige units. This means that, at any point in their career, officers in prestige units are 50% more likely to be promoted in the next instant than officers in typical units, which translates to faster promotion timing on average.

**HR < 1**: An increase in the covariate is associated with decreased promotion intensity (slower promotion). For example, if HR = 0.8, the covariate is associated with 20% lower promotion intensity (or equivalently, 1/0.8 = 1.25 times slower promotion). In practical terms, this means officers with this characteristic take longer, on average, to be promoted to Major.

**HR = 1**: The covariate has no effect on promotion intensity, meaning it does not influence promotion timing.

### Comparing Groups: Prestige Units vs. Typical Units

Hazard ratios are particularly useful for comparing groups. For example, comparing officers in prestige units to those in typical units:

$$\mathrm{HR} = \frac{h(t|\mathrm{prestige\ unit})}{h(t|\mathrm{typical\ unit})} = e^{\beta_{\mathrm{prestige}}}$$

If β_prestige = 0.4, then HR = e^{0.4} ≈ 1.49, meaning officers in prestige units have approximately 49% higher promotion intensity than officers in typical units, at all times. This interpretation is intuitive and directly addresses the research question of whether prestige unit service influences promotion timing.

### Continuous Covariates: Accumulating Effects Over Time

For continuous covariates, the hazard ratio represents the change in promotion intensity per unit increase in the covariate. For example, if cumulative top blocks received has coefficient β = 0.1, then HR = e^{0.1} ≈ 1.105, meaning each additional cumulative top block is associated with approximately 10.5% higher promotion intensity. This demonstrates how performance metrics that accumulate over an officer's career can influence their promotion timing, with each additional top block evaluation increasing their likelihood of earlier promotion.

It is important to note that hazard ratios are multiplicative effects. If an officer has two additional cumulative top blocks compared to another officer, their promotion intensity is approximately (1.105)² ≈ 1.22, or 22% higher, not simply 2 × 10.5% = 21% (though the difference is small for small effects). This multiplicative structure reflects the compounding nature of performance signals over time.

## D. Advantages: Why the Cox Model is Well-Suited for Military Promotion Research

The Cox model's semi-parametric nature provides several key advantages that make it particularly well-suited for analyzing military officer promotion timing. These advantages are especially important when working with large-scale administrative data where the underlying promotion process may be complex and influenced by numerous factors.

### No Need to Specify Baseline Hazard Distribution

Unlike fully parametric survival models, the Cox model does not require assuming a specific functional form for the baseline hazard. This is valuable because the true promotion process may be complex and influenced by numerous factors that are difficult to model parametrically. The baseline hazard can take any shape—increasing, decreasing, or non-monotonic—and the model will estimate it from the data. In the context of military promotion, where structured timelines create natural promotion windows, this flexibility allows the model to learn the exact shape of the baseline hazard from the data rather than imposing a predetermined form.

### Robustness to Distributional Assumptions

The Cox model is robust to violations of distributional assumptions that would be required in parametric models. This robustness is particularly important in organizational research, where the underlying processes may not follow standard probability distributions. The model focuses on estimating the relative effects of covariates (the hazard ratios) rather than the absolute hazard levels, which are often less of interest in comparative analyses. This focus on relative effects makes the model particularly well-suited for understanding how factors influence promotion timing relative to a baseline, rather than requiring precise estimation of absolute promotion probabilities.

### Efficient Handling of Large Sample Sizes

The partial likelihood estimation method is computationally efficient, making the Cox model well-suited for large-scale analyses. This is particularly important for military personnel research, where datasets may include hundreds of thousands of officers observed over many years. In our analysis of 201,038 officers over 24 years, this computational efficiency is essential for practical implementation. The model can handle such large samples without requiring excessive computational resources, while still providing precise estimates of covariate effects.

### Accommodation of Time-Varying Covariates

As discussed in Section I, the Cox model naturally accommodates time-varying covariates, allowing covariate values to change over time for the same individual. This capability is essential for modeling military careers, where performance metrics, unit assignments, and other characteristics evolve throughout an officer's service. The model can update covariate values at each time point, providing a dynamic view of how changing circumstances affect promotion intensity.

Moreover, the model can include both static variables (such as demographic characteristics or year group) and time-varying variables (such as cumulative performance metrics or current unit assignments) in the same specification, allowing for comprehensive analysis of factors influencing promotion timing. This flexibility enables researchers to simultaneously account for stable characteristics that may influence career trajectories and dynamic factors that change over time, providing a more complete picture of the factors that influence promotion timing.

---

*This section has introduced the Cox proportional hazards model, its formulation, estimation, and interpretation. The following section will discuss why this model is particularly well-suited for military officer promotion research, addressing the specific challenges and opportunities presented by this application and connecting it to the broader network science framework that underlies this dissertation.*
