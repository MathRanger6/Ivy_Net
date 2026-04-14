# COX MODELING CHAPTER OUTLINE

## I. WHY TIME-IN-GRADE AS A METRIC OF SUCCESS

### A. The Challenge of Measuring Officer Success
- Officers of the same rank receive identical compensation
- Need for a metric that captures differential performance and potential
- Limitations of binary promotion outcomes (promoted vs. not promoted)
- The importance of timing in career progression

### B. The Army's Promotion System and Assessment of Potential
- Promotion decisions are primarily based on potential, not just performance
- Performance serves as a signal that reinforces assessments of potential
- Structured promotion timelines create standardized expectations
- The role of year groups in determining promotion eligibility windows

### C. Network Context and the Assessment of Potential
- **Information sources**: ORBs (assignment histories) and OERs (rater narratives on performance, senior rater narratives on potential, and box checks)
- **Box checks as enumeration**: Compulsory categorical ratings that serve as standardized enumeration mechanism
- **Rating profiles**: HRC maintains profiles with a finite maximum percentage cap on top block awards
- **Network context**: Peer group quality varies across organizations; box checks occur within organizational context
- **Prestige in assignment history**: ORBs show organizational contexts of evaluations
- **Key question**: Do boards account for prestige of organizations when interpreting box checks?
- **Network structure**: Relationships between officers, units, and evaluators shape assessment

### D. Early Promotion as the Primary Differentiator
- **Standard promotion timeline**: Officers promoted within their Primary Zone (PZ)
- **Below Zone (BZ) promotions**: Officers promoted one year early
- **Double Below Zone (Double BZ) promotions**: Officers promoted two years early
- Early promotion as the Army's primary mechanism for recognizing exceptional potential
- **Codified regulations (Title 10 U.S. Code)**:
  - **10 U.S.C. § 616(b)**: Maximum **10%** of active-duty officers authorized for promotion can be selected BZ
  - **Actual usage**: While 10% is the maximum, actual annual averages are typically lower
  - **Strategic use**: Army uses BZ percentages to align distribution of officers with operational needs
  - **Expansion to 15%**: Secretary of Defense may increase limit to 15% if "needs of the service" require it
  - **10 U.S.C. § 619(d)**: Secretary of the Army may restrict BZ consideration to officers determined "exceptionally well qualified"
- Limited opportunities for early promotion (very few officers receive BZ/Double BZ)
- Regulatory constraints ensure early promotion remains highly selective

### E. Time-in-Grade as the Outcome Variable
- **Time-in-grade as Captain**: Days/months/years from Captain promotion (DOR CPT) to Major promotion (DOR MAJ)
- **Why Captain?** Officer timelines are more uniform at this early career stage
  - Initial service obligation period typically ends when officers are new captains (natural transition point)
  - Army prepares company grade officers (Lieutenants and Captains) uniformly with same developmental background minimums
  - Uniform preparation increases breadth of pool for later command position selections
  - Field grade officers (Major and above) have different knowledge, skills, and behaviors
  - Company grade set is relatively uniform until Major, making time-in-grade as Captain a meaningful metric within a standardized developmental framework
- Captures the continuum of promotion timing, not just binary outcomes
- Earlier promotion (shorter time-in-grade) indicates higher assessed potential
- Later promotion (longer time-in-grade) indicates standard or delayed progression
- Enables analysis of factors associated with faster career progression
- Provides a continuous, meaningful metric of career success

---

## II. WHY SURVIVAL ANALYSIS: OUR SPECIAL APPLICATION AND ANALOGOUS COMPONENTS

### A. The Time-to-Event Framework in Military Promotion Context
- Promotion timing as a time-to-event problem
- The "event" of interest: promotion to Major (positive outcome, not failure)
- Time scale: days/months/years from Captain promotion (Date of Rank)
- Time origin: Date of Rank (DOR) for Captain promotion
- All officers start "at risk" for Major promotion from CPT promotion date

### B. Analogous Components: Mapping Medical Survival Analysis to Promotion Analysis

#### 1. Survival Function: From "Survival" to "Remaining Unpromoted"
- **Medical context**: S(t) = probability patient survives (doesn't die) by time t
- **Promotion context**: S(t) = probability officer remains unpromoted by time t
- **Key difference**: In medical context, "survival" is the desired outcome; in promotion context, "survival" (remaining unpromoted) is the intermediate state before the desired outcome (promotion)
- **Interpretation**: S(t) answers "What proportion of officers remain unpromoted by time t?"

#### 2. Hazard Function: From "Death Rate" to "Promotion Intensity"
- **Medical context**: h(t) = instantaneous rate of death at time t
- **Promotion context**: h(t) = instantaneous rate of promotion at time t ("promotion intensity")
- **Key difference**: In medical context, hazard represents risk of undesirable event; in promotion context, hazard represents intensity of desirable event
- **Interpretation**: h(t) answers "Among officers still unpromoted at time t, how likely are they to be promoted in the next instant?"
- **Terminology note**: "Risk" in promotion context means probability/intensity of positive outcome, not negative outcome

#### 3. Censoring: From "Lost to Follow-up" to "Still in Service"
- **Medical context**: Right-censoring when patient lost to follow-up or study ends
- **Promotion context**: Right-censoring when officer still in service at study end, not yet promoted
- **Key similarity**: Both provide partial information—we know the individual "survived" (didn't experience event) up to censoring time
- **Military-specific nuance**: Officers censored while still in Below Zone window provide different information than those censored after passing through Primary Zone

#### 4. Competing Events: From "Death vs. Other Causes" to "Promotion vs. Attrition"
- **Medical context**: Competing risks (e.g., death from disease A vs. disease B)
- **Promotion context**: Competing events—promotion (positive) vs. attrition (negative from Army's perspective)
- **Key difference**: In medical context, all competing risks are typically negative; in promotion context, one event is positive (promotion) and one is negative (attrition)
- **Complexity**: Cannot treat attrition as simple censoring because officers who leave have different underlying promotion probability structure

#### 5. Left-Truncation: From "Late Entry" to "Eligibility Windows"
- **Medical context**: Left-truncation when individuals enter study at different ages
- **Promotion context**: Left-truncation when officers' eligibility windows (BZ/PZ) begin before study period
- **Key difference**: Military promotion has structured eligibility windows (Below Zone, Primary Zone) that create natural entry points
- **Complexity**: Officers whose DOR CPT predates study but whose eligibility window begins during study are not left-truncated—they haven't had opportunity yet

### C. What Makes Our Application Special

#### 1. Structured Promotion Windows
- Military promotion operates on structured timelines with specific eligibility windows
- Below Zone (BZ) window for early promotion
- Primary Zone (PZ) window for standard promotion
- Above Zone (AZ) for delayed promotion
- Baseline hazard should theoretically reflect these institutional structures

#### 2. Year Group Stratification
- Officers organized into year groups (cohorts commissioned in same year)
- Promotion policies can change by year group but don't cross year group boundaries
- Requires stratification by year group in Cox model (separate baseline hazards for each year group)
- Different year groups may have different BZ/PZ/AZ windows

#### 3. Time-Varying Covariates at Scale
- Performance metrics accumulate over time (cumulative top blocks, evaluations)
- Unit assignments change throughout career
- Prestige unit service is time-varying
- Pool metrics (peer comparisons) evolve as officers move between units
- Large-scale data: 201,038 officers with millions of time-varying intervals

#### 4. Network Context in Evaluation
- Officers evaluated among peers in their organization
- Peer group quality varies substantially across organizations
- Box checks serve as enumeration mechanism, constrained by rating profiles
- Selection boards may interpret box checks differently based on organizational prestige

#### 5. Competing Events with Different Interpretations
- Promotion: Positive outcome (desired)
- Attrition: Negative outcome from Army's perspective, but may occur for various reasons
  - Officers leaving for reasons unrelated to promotion potential
  - Officers leaving because they recognize low promotion likelihood
  - High-performing officers leaving for better opportunities elsewhere
- Cannot assume independence between promotion and attrition hazards

---

## III. WHY TRADITIONAL METHODS FAIL

### A. The Censoring Problem
- Standard regression methods (OLS, logistic) cannot appropriately handle censored observations
- OLS requires complete outcome values—but we don't know true time-to-promotion for censored officers
- Logistic regression treats all "not yet promoted" officers the same, regardless of observation time
- Excluding censored observations introduces severe selection bias
- In our dataset: substantial proportion of officers still in service at study end

### B. The Timing Problem
- Standard methods fail to capture the essential temporal dimension
- OLS treats time as a covariate, not the outcome of interest
- Logistic regression ignores timing entirely, focusing only on binary occurrence
- Loses critical information about *when* events occur
- Example: Finding prestige unit assignment correlates with promotion is valuable, but finding it correlates with *earlier* promotion provides richer insights

### C. Time-Varying Covariates
- Military careers characterized by variables that change over time
- Performance metrics accumulate (cumulative top blocks, evaluations)
- Unit assignments change throughout career
- Standard regression requires constant covariates or ad-hoc approaches (baseline values, time-averaged measures)
- Both approaches discard valuable information about how changing circumstances affect promotion intensity

### D. Information Loss from Censored Observations
- Standard methods ignore valuable partial information
- An officer who has served as Captain for 8 years without promotion provides meaningful information about lower tail of promotion time distribution
- Survival analysis uses this through risk set concept—both promoted and censored officers contribute to hazard estimation
- Discarding this information results in less precise estimates and potentially biased conclusions

### E. Competing Events
- Standard survival analysis treats attrition as simple censoring
- Implicitly assumes censored individuals (those who attrit) would have same promotion hazard as those who remain
- This assumption is likely violated—officers who leave have different underlying promotion probability structure
- Requires specialized competing events framework

---

## IV. THE COX PROPORTIONAL HAZARDS MODEL: FORMULATION AND ESTIMATION

### A. Model Formulation
- Semi-parametric approach (no assumption about baseline hazard distribution)
- Model formulation: h(t|X) = h₀(t) × exp(β₁X₁ + β₂X₂ + ... + βₚXₚ)
- **Proportional hazards assumption**: Hazard ratios are constant over time
- Baseline hazard h₀(t): Common to all individuals, unspecified form
- Covariate effects: Multiplicative on baseline hazard

### B. Why Cox Model for This Application
- **Handles censoring appropriately**: Uses information from censored observations through risk sets
- **Accommodates time-varying covariates**: Naturally handles changing performance metrics and assignments
- **No distributional assumptions**: Baseline hazard can reflect structured promotion windows
- **Computational efficiency**: Well-suited for large datasets (201,038 officers)
- **Competing risks capability**: Can model promotion and attrition separately

### C. Partial Likelihood Estimation
- Why partial likelihood (avoids specifying baseline hazard distribution)
- Uses only information from observed event times, not censored times
- Still incorporates information from censored observations through risk sets
- Handling tied event times (multiple promotions on same day)
- Maximum partial likelihood estimation

### D. Interpretation: Hazard Ratios
- **Hazard ratio (HR)**: exp(β) = relative change in promotion intensity
- HR > 1: Increased hazard (faster promotion)
- HR < 1: Decreased hazard (slower promotion)
- Comparing groups (e.g., prestige unit vs. typical unit)
- Continuous covariates: Change in hazard per unit increase

---

## V. OPERATIONALIZATION: IMPLEMENTING COX REGRESSION FOR OFFICER PROMOTION ANALYSIS

### A. Data Structure: Time-Varying Survival Intervals
- **Snapshot-based structure**: Each officer has multiple snapshots (quarterly records)
- **Interval creation**: Convert snapshots to survival intervals [start_time, stop_time)
- **Time-varying covariates**: Each interval includes covariate values from its corresponding snapshot
- **Event determination**: Last interval for each officer determines event type

### B. Software and Library Selection
- **Why scikit-survival (sksurv)**: Robust competing risks framework, proper handling of multiple event types, supports time-varying covariates with competing risks
- **Key components**: `sksurv.util.Surv`, `sksurv.linear_model.CoxPHSurvivalAnalysis`, `sksurv.metrics.concordance_index_censored`

### C. Model Specification
- **Static variables**: Demographics, year group, age at Captain promotion
- **Time-varying covariates**: OER performance metrics, prestige unit assignments, pool metrics, ratings given metrics
- **Model types**: Static model (demographics only), Full model (static + time-varying), Competing risks model

### D. Handling Competing Risks
- **Two event types**: Promotion (event=1) and Attrition (event=2)
- **Separate hazard functions**: h₁(t|X) for promotion, h₂(t|X) for attrition
- **Implementation**: Fit separate Cox models, compare coefficients, calculate cumulative incidence

### E. Model Evaluation
- **Concordance Index (C-index)**: Measure of predictive accuracy
- **Proportional Hazards Assumption**: Test using Schoenfeld residuals
- **Model comparison**: Static vs. Full model, nested model comparison

### F. Special Considerations for Military Data
- **Cohort effects**: Year group differences, stratification by year group
- **Data quality**: Missing DOR, invalid intervals, multiple promotions
- **Computational considerations**: Large sample size (201,038 officers, millions of intervals)

---

## VI. SURVIVAL ANALYSIS IN LABOR ECONOMICS AND BUSINESS APPLICATIONS

### A. Job Duration and Employee Turnover Studies
- Time until job separation
- Factors influencing retention
- Organizational commitment and turnover
- Examples from management and HR research
- **Key parallel**: Similar to our attrition analysis, but we also model promotion as competing event

### B. Promotion Timing in Organizations
- Corporate promotion ladders
- Academic tenure decisions
- Executive succession studies
- Time-to-promotion in hierarchical organizations
- **Key parallel**: Similar to our promotion timing analysis, but military context has structured eligibility windows

### C. Career Progression and Leadership Development
- Career trajectory studies
- Talent management and succession planning
- Early career indicators of leadership potential
- **Key parallel**: Similar focus on identifying factors associated with accelerated career progression

### D. Network Effects and Organizational Prestige
- Studies examining how organizational affiliations influence career outcomes
- Prestige effects in academic hiring (e.g., Clauset et al. 2015)
- Reputation and success in creative fields (e.g., Fraiberger et al. 2018)
- **Key parallel**: Similar to our investigation of prestige unit effects on promotion timing

### E. Lessons for Military Officer Research
- How organizational context shapes career outcomes
- The role of performance signals in career progression
- Network effects on career advancement
- Prestige and reputation in organizational advancement
- **Our contribution**: Applying these methods to military context with structured promotion windows and competing events

---

## VII. SUMMARY AND CONNECTIONS TO RESEARCH QUESTIONS

### A. How Cox Modeling Addresses Research Questions
- **Q1 (Unit Prestige)**: Prestige unit service as time-varying covariate
- **Q2 (Peer Effects)**: Pool metrics capture peer influence
- **Q3 (Prestige vs. Performance)**: Interaction between prestige and OER metrics

### B. Advantages of This Approach
- Handles complex temporal structure of officer careers
- Incorporates time-varying performance measures
- Accounts for competing risks (promotion vs. attrition)
- Enables identification of factors associated with accelerated career progression

### C. Limitations and Future Directions
- Proportional hazards assumption may not hold for all covariates
- Competing risks framework assumes independence of event types
- Large sample size enables detection of small effects (practical vs. statistical significance)
- Future work: Time-dependent coefficients, frailty models, machine learning extensions
