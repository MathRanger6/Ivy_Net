# Pertinent Thoughts for Dissertation

This document contains important considerations, potential confounding factors, and ideas that should be incorporated into various sections of the dissertation.

---

## OER Updates and Deduplication Keys

**Topic**: OER updates vs. true duplicates in source data

**Content to consider including**:

Some OER rows appear duplicated on officer + rater + senior rater + date ranges, but they may actually be updates to a previously filed OER rather than merge errors. To avoid discarding valid updates, consider including **rater box** and **senior rater box** values in any de-duplication key when curating OER data.

**Potential placement**:
- Data cleaning / preprocessing section
- Limitations section (data quality + potential updates in admin systems)

**Key points**:
- Duplicate metadata may represent revised evaluations
- Dedup keys that omit box checks can accidentally drop valid updates
- Consider adding `rater_box` and `snr_rater_box` (or their source codes) to dedup logic

---

## Missing OER Dates and Imputation

**Topic**: Handling missing eval start/thru dates

**Content to consider including**:

If `eval_strt_dt` or `eval_thru_dt` is missing, it may be possible to impute a plausible rating window (e.g., derive from fiscal year or typical evaluation length). This could increase usable OER coverage, but risks introducing **unrated-time confounding** if the imputed window is incorrect or overlaps gaps.

**Potential placement**:
- Data cleaning / preprocessing section
- Limitations section (missing data + imputation risk)

**Key points**:
- Missing OER dates can force row drops during join or assignment
- Imputation could recover signal but may distort overlap logic
- Any imputation strategy should be explicitly documented and sensitivity‑tested

**Suggested implementation rules (if you decide to impute)**:
- **Rule 1 (single missing date)**: If only one boundary is missing, infer the other using the typical evaluation length (e.g., 365 days) and keep within reasonable bounds.
- **Rule 2 (both missing, FY known)**: If FY is known, set `eval_strt_dt` to FY start and `eval_thru_dt` to FY end, then flag as imputed.
- **Rule 3 (both missing, FY unknown)**: Do not impute; drop or quarantine these rows.
- **Rule 4 (sanity bounds)**: Require `eval_strt_dt < eval_thru_dt` and a duration within a plausible range (e.g., 90–550 days).
- **Rule 5 (traceability)**: Add `eval_date_imputed` and `eval_impute_rule` columns for auditing.
- **Rule 6 (sensitivity)**: Run models with and without imputed rows and compare effects.

---

## OER Coverage Window and Survival Analysis

**Topic**: Upper bound of OER coverage in performance metrics

**Content to consider including**:

OER data have a maximum `eval_thru_dt`. When creating performance metrics or running survival analysis, avoid using snapshot rows **after** that maximum OER date, because performance covariates would be undefined or stale. Restricting the analysis window to the OER coverage period prevents bias from post‑coverage time.

**Potential placement**:
- Data preparation section (analysis window selection)
- Limitations section (coverage boundaries)

**Key points**:
- OER coverage ends at a known max `eval_thru_dt`
- Snapshots beyond that date should be excluded from survival models using OER metrics
- Treat the OER coverage window as the valid covariate window

---

## Winsorization and Tail Importance

**Topic**: Risks of trimming extreme but meaningful performance

**Content to consider including**:

Winsorization can stabilize models, but it also compresses extreme values that may represent **small, high‑impact subgroups** (e.g., rare top performers or outliers of special interest to the Army). If tails carry operational or strategic meaning, overly aggressive winsorization could mute the signal you care about.

**Potential placement**:
- Methods section (data transformations)
- Limitations section (tail sensitivity)
- Discussion of robustness checks

**Key points**:
- Tail values may be rare but substantively important
- Winsorization thresholds should be justified and sensitivity‑tested
- Consider reporting results with and without winsorization

---

## Combat Casualties and Attrition

**Topic**: Data noise and potential confounding factors in competing risks analysis

**Content to consider including**:

When discussing things that can create noise in the data, or potentially confound the legitimacy of our models, we should mention that another way that officers might attrit is through combat death or disqualifying wounds. 

For certain job codes, there may be at least a mild correlation between probability of being a casualty and being a high-performing, aggressive officer. Anecdotally, it often seems like some of the best officers are the ones that get "whacked" (killed or seriously wounded in combat).

**Potential placement**: 
- Discussion of competing risks (attrition types)
- Limitations section
- Discussion of potential confounding factors
- When discussing selection bias or unobserved heterogeneity

**Key points**:
- Combat casualties represent a distinct form of attrition that may not be random
- Potential correlation between high performance/aggression and combat casualty risk
- This could create selection bias if high-performing officers are systematically removed from the promotion pool through combat casualties
- Particularly relevant for certain job codes (combat arms, special operations, etc.)

---

## Year Groups and Structured Promotion Timelines

**Topic**: Need for stratification by year group due to structured promotion timelines

**Content to consider including**:

The military promotion system uses "structured timelines" that are purposefully altered to change the force composition, but these changes do NOT cross year group lines. When the Army makes a change to the standard time-in-grade or promotion eligibility windows, it applies to all officers in year group 200X and going forward until it is changed again (which could possibly be even the next fiscal year).

This creates a need for **stratification** by year group in the Cox model analysis. Stratification means fitting separate baseline hazards h₀(t) for each year group, allowing the baseline hazard shape (which should reflect the BZ/PZ/AZ promotion windows) to differ across year groups while keeping the covariate effects (β coefficients) the same across groups. This is different from simply including year group as a covariate, which would assume the same baseline hazard shape for all year groups.

**Potential placement**: 
- Discussion of left-truncation and promotion eligibility windows
- Data preparation/methodology section
- When discussing Cox model specification (stratification vs. covariates)
- When explaining the structure of the promotion system
- When discussing how the baseline hazard should reflect BZ/PZ/AZ windows

**Key points**:
- Promotion timeline changes apply to entire year groups, not individual officers
- Changes are forward-looking from a specific year group (e.g., all of 200X and later)
- Year group boundaries are fixed - changes don't retroactively affect earlier year groups
- Different year groups may have different BZ/PZ/AZ windows, so their baseline hazards should differ
- Stratification allows separate baseline hazards for each year group while keeping covariate effects constant
- The baseline hazard should theoretically reflect the BZ/PZ/AZ structure (low before BZ, higher during BZ, highest during PZ, lower after PZ)

---

## Left-Truncation and Analysis Window Selection

**Topic**: Methodological choice regarding analysis window to potentially avoid left-truncation

**Content to consider including**:

If we choose the analysis window to be a subset of our available data window, we could potentially eliminate the left-truncation issue because we would know how many of those left-truncated officers DID get promoted to Captain. By starting the analysis window at a point where we have complete information about officers' promotion to Captain (and their entry into eligibility windows), we could avoid left-truncation for those officers since we'd have their full history from DOR CPT (or from the start of their eligibility window).

**Potential placement**: 
- Methodology/data preparation section when discussing analysis window selection
- Discussion of left-truncation and how it was handled
- Limitations section noting trade-offs between sample size and methodological complexity
- When explaining why a particular analysis window was chosen

**Key points**:
- Trade-off between avoiding left-truncation vs. maximizing sample size
- Starting analysis window later could eliminate left-truncation but reduces sample size
- Starting analysis window earlier includes more data but requires handling left-truncation
- This represents a deliberate methodological choice that should be justified
- Need to explain why the chosen approach (handling left-truncation vs. avoiding it) was preferred

---

## Landmark Analysis for Time-Varying Covariates

**Topic**: Alternative approach to visualizing time-varying covariate effects in survival analysis

**Content to consider including**:

When plotting survival curves or cumulative incidence functions, time-varying covariates present a challenge: officers may change groups over time (e.g., an officer's cumulative TB ratio may move from Q1 to Q2 to Q3 as they accumulate more evaluations). Standard plotting approaches aggregate to officer-level using final values, which is practical but doesn't capture the dynamic nature of time-varying covariates.

**Landmark analysis** offers an alternative approach: instead of grouping officers by their final characteristics, we can group them by their characteristics at a specific "landmark" time point (e.g., day 1000, day 2000). This allows us to answer questions like: "Among officers who had a TB ratio in Q3 by day 1000, what is their subsequent promotion probability?"

**How it works**:
1. Choose a landmark time point (e.g., 1000 days from DOR CPT, or the start of Primary Zone)
2. For each officer, determine their covariate values at that landmark time
3. Group officers based on their landmark-time characteristics
4. Calculate survival/CIF curves starting from the landmark time (not from time 0)
5. This shows the effect of having certain characteristics by a specific point in time

**Advantages**:
- Captures time-varying effects more dynamically than final-value aggregation
- Allows examination of "early achievers" vs. "late bloomers"
- Can answer questions about the importance of reaching certain milestones by specific times
- More clinically/practically relevant (e.g., "What if an officer hasn't achieved X by day 1000?")

**Disadvantages**:
- Requires choosing landmark time points (somewhat arbitrary)
- Reduces sample size (only includes officers who survive to the landmark time)
- More complex to implement and explain
- Multiple landmark analyses may be needed to fully capture time-varying effects

**Potential applications for this study**:
- **Primary Zone landmark**: Group officers by their cumulative TB ratio at the start of Primary Zone (6 years), then examine subsequent promotion probability
- **Early performance landmark**: Group officers by their TB ratio at day 1000, examining whether early performance signals matter more than later performance
- **Milestone-based analysis**: Examine promotion probability for officers who reached certain performance thresholds (e.g., TB ratio > 0.5) by specific time points

**Potential placement**: 
- Methodology section when discussing visualization of time-varying covariates
- Discussion of alternative approaches to plotting survival curves
- Limitations section noting trade-offs between different visualization approaches
- When explaining why final-value aggregation was chosen over landmark analysis (if applicable)
- Future research directions section as a potential extension

**Key points**:
- Landmark analysis groups officers by their characteristics at a specific time point, then analyzes subsequent outcomes
- Useful for examining time-varying covariate effects more dynamically than final-value aggregation
- Requires choosing landmark time points and reduces sample size (only officers surviving to landmark)
- Could be valuable for examining "early achievers" vs. "late bloomers" or milestone-based effects
- Current approach (final-value aggregation) is simpler and more standard, but landmark analysis could be a useful extension

---

## Attrition Patterns and Selection Bias

**Topic**: Complex reasons for attrition that create selection bias in promotion analysis

**Content to consider including**:

Attrition is not random and occurs for multiple, often countervailing reasons that create complex selection bias:

1. **"Leave before they tell me no thanks"**: Many officers see "the writing on the wall" and leave early because they don't want to be told they weren't good enough. This tendency increases as officers get to higher ranks. These officers are likely lower-performing and would have lower promotion probability.

2. **High performers leaving for better opportunities**: A HUGE factor in attrition could be directly DUE TO an officer's high potential for promotion. These officers recognize they have greater opportunities elsewhere that don't have such firm promotion timelines and may offer more meaningful or more lucrative opportunities to them personally. These officers are likely high-performing and would have higher promotion probability.

3. **Reasons unrelated to promotion potential**: Officers may leave for family considerations, personal circumstances, or other reasons unrelated to their promotion prospects.

**Potential placement**: 
- Discussion of competing events (attrition types)
- Information loss from censored observations section
- Limitations section
- Discussion of selection bias
- When explaining why competing events models are necessary
- Discussion of unobserved heterogeneity

**Key points**:
- Attrition is not random - creates selection bias in multiple directions
- Low performers may leave early to avoid being passed over (negative selection)
- High performers may leave for better opportunities (positive selection)
- This creates complex selection bias that standard censoring assumptions don't capture
- Competing events models are essential to properly account for these different attrition mechanisms
- The "leave before they tell me no thanks" tendency increases at higher ranks
- High performers leaving for better opportunities is a significant factor that could bias results if not properly modeled

---

## Acknowledging Methodological Limitations

**Topic**: Importance of acknowledging when generalizations may not hold, while noting that assumptions are reasonable for the specific case

**Content to consider including**:

When discussing methodological assumptions (such as proportional hazards), it's important to:
1. Acknowledge that the assumption may not hold in all contexts or for all generalizations
2. Explain what would happen if the assumption were violated
3. Note what could be done to address violations (alternative methods, diagnostic tests, etc.)
4. Explicitly state that for the specific case being studied, the assumption is reasonable

For example, when discussing proportional hazards:
- Acknowledge that covariate effects might vary over time in some contexts (e.g., prestige unit service might matter more for early promotions than later ones)
- Explain that if violated, the estimated effect represents an average over time
- Note that diagnostic tests can assess the assumption
- State that for promotion to Major (a specific, early-career milestone within a narrow time window), the assumption is reasonable

This approach demonstrates methodological sophistication and awareness of assumptions while reassuring readers that the methods are appropriate for the specific research question.

**Potential placement**: 
- When discussing key model assumptions (proportional hazards, etc.)
- Limitations section
- Methodology section when explaining model choices
- When comparing to alternative approaches

**Key points**:
- Show awareness that assumptions may not hold in all contexts
- Explain what would be done if assumptions were violated
- Explicitly state why assumptions are reasonable for the specific case
- This demonstrates methodological rigor and reassures readers
- Example: Proportional hazards may not hold across all career stages, but is reasonable for promotion to Major within the observation window

---

## Prestige Unit Service and Context-Dependent Promotion Effects

**Topic**: Prestige unit service as a signal of quality, with effects that vary by organizational context and relative to performance ratings

**Content to consider including**:

All units should have a measurable level of prestige. If we strictly define prestige units (e.g., Ranger Regiment, 160th SOAR), we can examine how prestige unit service relates to promotion outcomes, both in absolute terms and relative to performance ratings.

### A. Context-Dependent Effects

**Expected relationships**:

1. **Overall correlation with early promotion**: If we plot the correlation of `prestige_sum` (cumulative prestige unit experience) with early promotion, we expect to find that the more experience in prestige units an officer has, the more likely he or she is to be promoted early. A similar relationship should hold for `tb_ratio_snr` (top block ratio from senior rater).

2. **Context-dependent effects**: The effect of prestige unit service on promotion probability may vary depending on the organizational context. If we filter our analysis to just those officers who ever served in a "less prestigious" unit (e.g., 1st Infantry Division), we might find a **greater difference** in promotion probability between prestige unit veterans and non-prestige unit veterans, compared to if we look at officers who served in a "more prestigious" unit like the 82nd Airborne Division.

3. **Performance as the underlying mechanism**: This difference between more prestigious and less prestigious units should narrow or disappear when we look at `tb_ratio_snr`. This suggests that prestige unit service may serve as a signal of underlying performance quality, and when we directly control for performance (via `tb_ratio_snr`), the prestige unit effect diminishes because actual performance is what really drives promotion decisions.

**Theoretical interpretation**:
- Prestige unit service signals quality/performance
- In less prestigious units, prestige unit veterans stand out more because the baseline performance level is lower (bigger effect)
- In more prestigious units, everyone is already high-performing, so prestige unit service matters less (smaller effect)
- When controlling for actual performance (`tb_ratio_snr`), the prestige unit effect should diminish because performance is the underlying mechanism

### B. Relative Predictive Power: Prestige Unit Service vs. Performance Ratings

**Research questions to explore**:

1. **Comparative predictive power**: If we plot the correlation of `tb_ratio_snr` alongside `prestige_sum` (or a normalized version of it), is one more predictive than the other consistently? Do they provide complementary or redundant information?

2. **When prestige trumps performance**: Is there ever a time when average ratings in a prestige unit trump superior ratings in an average unit? This would suggest that the organizational context (prestige unit service) can sometimes override individual performance signals, perhaps because prestige units are seen as inherently more selective or because service in prestige units provides additional signals beyond what performance ratings capture.

3. **Context-dependent gaps**: Does the gap between the predictive power of `prestige_sum` and `tb_ratio_snr` change for:
   - **Demographics**: Do the relative effects differ by gender, race, or other demographic characteristics?
   - **Unit type**: Does the relationship differ across different types of units (combat arms, support, etc.)?
   - **Promotion zone**: Does the relative importance of prestige vs. performance ratings differ for below-zone (BZ), primary-zone (PZ), or above-zone (AZ) promotions? For example, prestige unit service might matter more for BZ promotions (where it signals exceptional potential), while performance ratings might matter more for PZ/AZ promotions (where demonstrated performance is the key criterion).

**Theoretical implications**:
- If prestige unit service consistently trumps performance ratings, it suggests that organizational affiliation provides signals beyond individual performance
- If performance ratings are consistently more predictive, it suggests that prestige unit effects are primarily mediated through performance
- If the relationship varies by context (demographics, unit type, promotion zone), it suggests complex interactions between organizational signals and individual performance
- Understanding when prestige trumps performance (or vice versa) can inform how these variables should be weighted or combined in models

**Potential placement**: 
- Discussion of prestige unit variables and their construction
- Model specification section when explaining covariate selection and relative importance
- Results section when interpreting prestige unit coefficients and comparing to performance rating effects
- Discussion of interaction effects or stratified analyses
- When explaining how organizational context may moderate the effect of prestige unit service
- When discussing the relative importance of different signals for promotion decisions
- Limitations section noting that prestige unit effects may be context-dependent and may interact with performance ratings

**Key points**:
- Prestige unit service is expected to correlate positively with early promotion
- The effect of prestige unit service may be stronger in less prestigious organizational contexts
- The effect of prestige unit service may be weaker in more prestigious organizational contexts
- When controlling for actual performance (`tb_ratio_snr`), prestige unit effects should diminish
- This suggests prestige unit service signals underlying performance quality
- Organizational context may moderate the relationship between prestige unit service and promotion
- The relative predictive power of prestige unit service vs. performance ratings may vary by context
- Average performance in prestige units may sometimes trump superior performance in average units
- The gap between prestige and performance effects may vary by demographics, unit type, or promotion zone
- This has implications for how prestige unit variables should be interpreted and potentially modeled (e.g., interaction terms, stratified analyses, relative weighting)

---

## Small Things to Check Later

- `dor_cpt` and `dor_maj` appear to be computed in both `502` and `520`; verify whether this duplication is intentional.
- Year group appears to be calculated in more than one place; standardize on the most complete algorithm.

---

## Rater-Senior Rater Rating Discrepancies

**Topic**: Investigating factors that correlate with differences between rater and senior rater top block ratios

**Content to consider including**:

When plotting histograms of cumulative top blocks received ratios by raters versus senior raters, the distributions are close to identical but not identical. This raises questions about what factors correlate with discrepancies between rater and senior rater ratings.

**Research questions to explore**:

1. **Rated officer characteristics**: Do certain rated officers engender this discrepancy? Are there officer-level characteristics (performance level, career trajectory, demographic factors, etc.) that predict when raters and senior raters will give different ratings?

2. **Rater and senior rater characteristics**: Are certain raters or senior raters more likely to be associated with these discrepancies? Do some raters consistently rate higher or lower than their corresponding senior raters? Do some senior raters consistently rate higher or lower than their corresponding raters?

3. **Demographic and contextual factors**: Are there demographic commonalities or differences (of the rated officer, rater, or senior rater) that affect whether ratings are identical versus different? Do factors like gender, race, branch, unit type, or organizational context predict rating discrepancies?

4. **Direction of discrepancy**: When discrepancies occur, are they systematic (e.g., raters consistently more generous, or senior raters consistently more generous) or random? Are there patterns in which direction the discrepancy goes?

**Potential analytical approaches**:
- Calculate discrepancy metrics (e.g., difference between rater and senior rater top block ratios, absolute difference, signed difference)
- Examine correlations between discrepancy and officer, rater, and senior rater characteristics
- Identify raters/senior raters with consistently high or low discrepancy patterns
- Explore demographic and contextual factors that predict discrepancies
- Analyze whether discrepancies are associated with promotion outcomes

**Potential placement**: 
- Data exploration and descriptive analysis section
- Discussion of OER rating patterns and potential biases
- Limitations section noting potential rater effects or rating inconsistencies
- When discussing the construction of performance metrics (e.g., `tb_ratio_rater` vs. `tb_ratio_snr`)
- When explaining why both rater and senior rater metrics are included in models
- Discussion of potential confounding factors or unobserved heterogeneity
- When discussing the reliability and validity of OER ratings as performance measures

**Key points**:
- Rater and senior rater top block ratios are highly correlated but not identical
- Understanding what drives discrepancies could reveal important insights about rating patterns
- Discrepancies may reflect different perspectives, biases, or contextual factors
- Certain officers, raters, or senior raters may be systematically associated with discrepancies
- Demographic or contextual factors may influence rating alignment
- Rating discrepancies could potentially affect promotion outcomes and should be understood
- This analysis could inform how rater and senior rater metrics are used in models (e.g., whether to use both, whether to create a discrepancy variable, whether to weight them differently)
- Understanding discrepancies may help identify potential biases or systematic patterns in the rating system

---

## Cox Model Results (Promotion to Major, CS/CSS, YG 2002–2012)

**Topic**: Statistical significance and interpretation of the Cox proportional hazards model for promotion to Major, with attrition as a competing risk

**Content to consider including**:

Among Combat Support and Combat Service Support Army officers in year groups 2002–2012, a Cox proportional hazards model for **promotion to Major** (treating **attrition as a competing event**) showed that all predictors were statistically significant. Higher standardized TB ratio (forward, SNR) was associated with substantially higher hazard of promotion to Major (HR ≈ 10.4 per standard deviation; 95% CI excluding 1; p < 0.001). Higher standardized pool-minus-mean (forward) was associated with lower promotion hazard (HR ≈ 0.34 per SD; 95% CI excluding 1; p < 0.001), consistent with a comparative or competitive effect relative to the pool. Squared terms for both TB ratio and pool-minus-mean were significant and negative, indicating **non-linear** effects: the positive effect of TB ratio weakened at higher values, and the effect of relative standing (pool minus mean) was curved rather than linear. The TB ratio × pool-context interaction was also significant (HR ≈ 1.54; p < 0.001), indicating that the effect of TB ratio on promotion hazard depended on pool context (and vice versa). In sum, promotion to Major in this sample was associated with individual top-block performance, relative standing within the pool, non-linearities in both, and their interaction, with attrition explicitly treated as a competing risk.

**Potential placement**:
- Results section (Cox model / survival analysis)
- When reporting hazard ratios and statistical significance from the lifelines output
- Discussion of competing risks (promotion vs. attrition)

**Key points**:
- All model terms (TB ratio, pool minus mean, their squares, and the interaction) are statistically significant
- TB ratio: strong positive association with promotion hazard (per SD)
- Pool minus mean: strong negative association (comparative/competitive effect)
- Squared terms support non-linear (curved) effects and justify quadratic specification
- Interaction supports effect of one predictor depending on the other
- Attrition is explicitly treated as a competing event

---

