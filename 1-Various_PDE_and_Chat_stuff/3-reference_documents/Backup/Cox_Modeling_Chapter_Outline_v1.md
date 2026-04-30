# COX MODELING CHAPTER OUTLINE

## 0. TIME-IN-GRADE AS A METRIC OF SUCCESS

### A. The Challenge of Measuring Officer Success
- Officers of the same rank receive identical compensation
- Need for a metric that captures differential performance and potential
- Limitations of binary promotion outcomes (promoted vs. not promoted)
- The importance of timing in career progression

### B. The Army's Promotion System and Potential
- Promotion decisions are primarily based on potential, not just performance
- Performance serves as a signal that reinforces assessments of potential
- Structured promotion timelines create standardized expectations
- The role of year groups in determining promotion eligibility windows

### C. Network Context and the Assessment of Potential
- **Information sources**: ORBs (assignment histories) and OERs (rater/senior rater comments and box checks)
- **Senior rater enumeration**: Officers ranked among peers within their organization
- **Network context**: Peer group quality varies across organizations; enumeration occurs within organizational context
- **Prestige in assignment history**: ORBs show organizational contexts of evaluations
- **Key question**: Do boards account for prestige of organizations when interpreting enumeration?
- **Network structure**: Relationships between officers, units, and evaluators shape assessment

### D. Early Promotion as the Primary Differentiator
- **Standard promotion timeline**: Officers promoted within their Primary Zone (PZ)
- **Below Zone (BZ) promotions**: Officers promoted one year early
- **Double Below Zone (Double BZ) promotions**: Officers promoted two years early
- Early promotion as the Army's primary mechanism for recognizing exceptional potential
- **Codified regulations (Title 10 U.S. Code)**:
  - **10 U.S.C. § 616(b)** (Active-Duty List) and **10 U.S.C. § 14307** (Reserve Active-Status List): Maximum **10%** of officers authorized for promotion can be selected BZ
  - **Expansion to 15%**: Secretary of Defense may increase limit to 15% if "needs of the service" require it
  - **10 U.S.C. § 619(d)**: Secretary of the Army may restrict BZ consideration to officers determined "exceptionally well qualified"
- Limited opportunities for early promotion (very few officers receive BZ/Double BZ)
- Regulatory constraints ensure early promotion remains highly selective

### D. Time-in-Grade as the Outcome Variable
- **Time-in-grade as Captain**: Days/months/years from Captain promotion (DOR CPT) to Major promotion (DOR MAJ)
- Captures the continuum of promotion timing, not just binary outcomes
- Earlier promotion (shorter time-in-grade) indicates higher assessed potential
- Later promotion (longer time-in-grade) indicates standard or delayed progression
- Enables analysis of factors associated with faster career progression

### E. Why This Matters for Research
- Provides a continuous, meaningful metric of career success
- Allows for nuanced analysis beyond simple promotion/non-promotion
- Enables identification of factors associated with accelerated career progression
- Connects to broader questions about talent identification and development

---

## I. SURVIVAL ANALYSIS: THE FOUNDATION

### A. The Time-to-Event Framework
- Promotion timing as a time-to-event problem
- Time-in-grade as the outcome of interest
- The "event" of interest: promotion to Major
- Time scale: days/months/years from Captain promotion (Date of Rank)

### B. Key Concepts: Survival Function, Hazard Function, Censoring
- **Survival Function S(t)**: Probability of not being promoted by time t
- **Hazard Function h(t)**: Instantaneous rate of promotion at time t
- **Right-censoring in military careers**: Officers still in service at study end
- **Competing risks**: Promotion vs. attrition (officers may leave service before promotion)
- **Left-truncation**: Officers already promoted before study period begins

### C. Why Standard Regression Methods Fail for Time-to-Event Data
- Censored observations cannot be handled by OLS or logistic regression
- Time-varying covariates require specialized methods
- Need to account for the timing of events, not just occurrence
- Standard methods ignore information from censored observations

---

## II. COX PROPORTIONAL HAZARDS MODEL

### A. The Cox Model: Formulation and Assumptions
- Semi-parametric approach (no assumption about baseline hazard distribution)
- Model formulation: h(t|X) = h₀(t) × exp(β₁X₁ + β₂X₂ + ... + βₚXₚ)
- **Proportional hazards assumption**: Hazard ratios are constant over time
- Baseline hazard h₀(t): Common to all individuals, unspecified form
- Covariate effects: Multiplicative on baseline hazard

### B. Partial Likelihood Estimation
- Why partial likelihood (avoids specifying baseline hazard distribution)
- Uses only information from event times, not censored times
- Handling tied event times (multiple promotions on same day)
- Maximum partial likelihood estimation

### C. Interpretation: Hazard Ratios and Their Meaning
- **Hazard ratio (HR)**: exp(β) = relative change in promotion hazard
- HR > 1: Increased hazard (faster promotion)
- HR < 1: Decreased hazard (slower promotion)
- Comparing groups (e.g., prestige unit vs. typical unit)
- Continuous covariates: Change in hazard per unit increase

### D. Advantages: Semi-Parametric Flexibility
- No need to specify baseline hazard distribution
- Robust to distributional assumptions
- Can handle large sample sizes efficiently
- Allows for time-varying covariates

---

## III. WHY COX MODELING FOR MILITARY OFFICER PROMOTION RESEARCH

### A. Promotion Timing as a Time-to-Event Problem
- **Primary outcome**: Time from Captain promotion (DOR CPT) to Major promotion (DOR MAJ)
- **"Below the Zone" (BZ) promotions**: Early promotion events of particular interest
- **Time-in-grade**: Key metric for career progression analysis
- **Cohort effects**: Year group (YG) differences in promotion timing

### B. Handling Time-Varying Covariates
- **OER performance metrics** that change over time
  - Cumulative top blocks received
  - Cumulative evaluations received
  - TB ratios (performance ratios)
  - Grade-based metrics (Captain vs. Major period performance)
- **Prestige unit assignments** that vary across career
  - Time-varying binary indicator (in prestige unit or not)
  - Cumulative prestige quarters
- **Cumulative performance measures**
  - Pool metrics (comparison to peers evaluated by same rater)
  - Ratings given metrics (experience as evaluator)
- **Other time-varying factors**
  - Job code changes
  - Marital status changes
  - Unit assignments

### C. Competing Risks: Promotion vs. Attrition
- Officers may be **promoted** OR **leave service** (attrition)
- Need to model both outcomes simultaneously
- Cannot treat attrition as simple censoring (informative censoring)
- Competing risks framework: Separate hazards for promotion and attrition
- **Event types**: 
  - Event = 0: Censored (still in service, not yet promoted)
  - Event = 1: Promoted to Major
  - Event = 2: Attrited (left service before promotion)

### D. Advantages Over Alternative Approaches
- **Compared to logistic regression**: 
  - Accounts for timing, not just occurrence
  - Uses information from censored observations
  - Handles time-varying covariates naturally
- **Compared to parametric survival models**: 
  - More flexible (no distributional assumptions)
  - Better for exploratory analysis
- **Ability to handle large sample sizes**: 
  - 201,038 officers over 24 years
  - Efficient computation with partial likelihood
- **Integration with network science methods**: 
  - Can incorporate network-derived prestige measures
  - Allows for complex covariate structures

---

## IV. COX MODELING IN LABOR ECONOMICS AND ORGANIZATIONAL RESEARCH

### A. Job Duration and Employee Turnover Studies
- Time until job separation
- Factors influencing retention
- Organizational commitment and turnover
- Examples from management and HR research

### B. Promotion Timing in Organizations
- Corporate promotion ladders
- Academic tenure decisions
- Executive succession studies
- Time-to-promotion in hierarchical organizations

### C. Leadership Development and Career Progression
- Military leadership research (if available)
- Career trajectory studies
- Talent management and succession planning
- Early career indicators of leadership potential

### D. Lessons for Military Officer Research
- How organizational context shapes promotion timing
- The role of performance signals in career progression
- Network effects on career outcomes
- Prestige and reputation in organizational advancement

---

## V. OPERATIONALIZATION: IMPLEMENTING COX REGRESSION FOR OFFICER PROMOTION ANALYSIS

### A. Data Structure: Time-Varying Survival Intervals

#### 1. Creating Time-Varying Intervals
- **Snapshot-based structure**: Each officer has multiple snapshots (quarterly records)
- **Interval creation**: Convert snapshots to survival intervals
  - Each interval: [start_time, stop_time)
  - start_time: Days from DOR CPT to interval start
  - stop_time: Days from DOR CPT to interval end
- **Time-varying covariates**: Each interval includes covariate values from its corresponding snapshot
- **Event determination**: Last interval for each officer determines event type

#### 2. Time Scale and Origin
- **Time origin**: Date of Rank (DOR) for Captain promotion
- **Time scale**: Days from DOR CPT
- **Rationale**: All officers start "at risk" for Major promotion from CPT promotion date
- **Handling missing DOR**: Officers without DOR CPT excluded from analysis

#### 3. Event Coding
- **Event = 0 (Censored)**: Officer still in service at study end, not yet promoted
- **Event = 1 (Promoted)**: Officer promoted to Major (has DOR MAJ)
- **Event = 2 (Attrited)**: Officer left service before promotion (last snapshot < study end date)

### B. Software and Library Selection

#### 1. Why scikit-survival (sksurv) Over Alternatives
- **Lifelines limitations**: 
  - Cannot adequately handle competing risks
  - Limited support for time-varying covariates in competing risks context
  - Cannot model "probability of early promotion" vs. "probability of not being promoted"
- **scikit-survival advantages**: 
  - Robust competing risks framework
  - Proper handling of multiple event types
  - Better integration with scikit-learn ecosystem
  - Supports time-varying covariates with competing risks

#### 2. Key scikit-survival Components Used
- `sksurv.util.Surv`: Survival data structure (event indicator + time)
- `sksurv.linear_model.CoxPHSurvivalAnalysis`: Cox regression model
- `sksurv.metrics.concordance_index_censored`: Model evaluation (C-index)
- Regularization support: L1/L2 penalties for variable selection

### C. Model Specification and Variable Selection

#### 1. Static (Time-Invariant) Variables
- **Demographics**: 
  - Sex
  - Year group (YG) - dummy encoded
  - Age at Captain promotion
- **Career characteristics**: 
  - Final job code (last job code held)
  - Commissioning source (if available)

#### 2. Time-Varying Covariates
- **OER Performance Metrics** (from cumulative OER metrics module):
  - `cum_tb_recvd_ratio_rtr`: Cumulative TB ratio from raters
  - `cum_tb_recvd_ratio_snr`: Cumulative TB ratio from senior raters
  - `cum_evals_rcvd_rtr`: Cumulative evaluations from raters
  - `cum_evals_rcvd_snr`: Cumulative evaluations from senior raters
  - Grade-based metrics (Captain period vs. Major period)
  - Rolling window metrics (last N evaluations)
- **Prestige and Unit Metrics**:
  - `prestige_unit`: Binary indicator (current assignment in prestige unit)
  - `prestige_sum`: Cumulative quarters in prestige units
  - `prestige_mean`: Rolling mean of prestige assignments
- **Pool Metrics** (comparative performance):
  - `pool_cum_tb_mean_rtr`: Mean cumulative TBs in rater pool
  - `cum_tb_diff_rtr`: Individual TB minus pool mean
  - `cum_tb_rank_norm_rtr`: Normalized rank in rater pool
- **Ratings Given Metrics**:
  - `cum_tb_given_rtr`: Cumulative TBs given as rater
  - `cum_evals_given_rtr`: Cumulative evaluations given as rater

#### 3. Model Types
- **Static Model**: Demographics only (baseline model)
- **Full Model**: Static + time-varying covariates
- **Competing Risks Model**: Separate models for promotion vs. attrition

### D. Handling Competing Risks

#### 1. Competing Risks Framework
- **Two event types**: Promotion (event=1) and Attrition (event=2)
- **Separate hazard functions**: 
  - h₁(t|X): Hazard of promotion
  - h₂(t|X): Hazard of attrition
- **Cumulative incidence functions**: Probability of each event type over time
- **Cause-specific hazards**: Model each event type separately

#### 2. Implementation Approach
- Use scikit-survival's competing risks capabilities
- Fit separate Cox models for promotion and attrition
- Compare coefficients across models
- Calculate cumulative incidence for each event type

### E. Model Evaluation and Diagnostics

#### 1. Model Fit Assessment
- **Concordance Index (C-index)**: Measure of predictive accuracy
  - C-index = 0.5: No predictive power (random)
  - C-index = 1.0: Perfect prediction
  - Interpretation: Proportion of pairs where predicted order matches observed order
- **Proportional Hazards Assumption**: 
  - Test using Schoenfeld residuals
  - Visual inspection of log(-log(S(t))) plots
  - Time-dependent coefficients if assumption violated

#### 2. Variable Importance
- **Coefficient magnitudes**: Larger |β| = stronger effect
- **Hazard ratios**: exp(β) = multiplicative effect on hazard
- **Signal ratios**: Interpretation of HR in context of promotion timing
- **Confidence intervals**: Statistical significance of effects

#### 3. Model Comparison
- **Static vs. Full Model**: Does adding time-varying covariates improve fit?
- **Nested model comparison**: Likelihood ratio tests
- **C-index comparison**: Predictive accuracy improvement

### F. Special Considerations for Military Data

#### 1. Cohort Effects
- **Year group (YG) differences**: Different promotion rates across cohorts
- **Temporal trends**: Changes in promotion policies over time
- **Inclusion of YG**: As both covariate and stratification variable

#### 2. Data Quality
- **Missing DOR**: Officers without DOR CPT excluded
- **Invalid intervals**: Remove intervals where start_time ≥ stop_time
- **Multiple promotions**: Handle officers with multiple DOR dates (use mode)
- **Censoring patterns**: Right-censoring at study end date

#### 3. Computational Considerations
- **Large sample size**: 201,038 officers, millions of intervals
- **Efficient computation**: Vectorized operations, parallel processing
- **Memory management**: Progressive saves, intermediate checkpoints
- **Modular design**: Separate cells for data prep, model fitting, evaluation

### G. Pipeline Structure and Reproducibility

#### 1. Modular Pipeline Design
- **CELL 10**: Cox data preparation (create time-varying intervals)
- **CELL 11**: Cox analysis and plotting (Kaplan-Meier, competing risks plots)
- **CELL 12**: Cox regression models (scikit-survival implementation)
  - 12.1: Data preparation and quality checks
  - 12.2: Static model (demographics only)
  - 12.3: Full model (static + time-varying)
  - 12.4: Model comparison and signal ratios
  - 12.5: Competing risks analysis
  - 12.6: Partial effects plots
  - 12.7: Interaction effects (3D plots)

#### 2. Progressive Saves
- Intermediate data files at each stage
- Saved models (.pkl files) for reuse
- Results tables (.csv files) for analysis
- Enables selective re-execution and troubleshooting

#### 3. Reproducibility
- Version-controlled code
- Documented data transformations
- Saved random seeds (if applicable)
- Clear variable definitions and sources

---

## VI. SUMMARY AND CONNECTIONS TO RESEARCH QUESTIONS

### A. How Cox Modeling Addresses Research Questions
- **Q1 (Unit Prestige)**: Prestige unit service as time-varying covariate
- **Q2 (Peer Effects)**: Pool metrics capture peer influence
- **Q3 (Prestige vs. Performance)**: Interaction between prestige and OER metrics

### B. Advantages of This Approach
- Handles complex temporal structure of officer careers
- Incorporates time-varying performance measures
- Accounts for competing risks (promotion vs. attrition)
- Enables causal-like inference through proper modeling

### C. Limitations and Future Directions
- Proportional hazards assumption may not hold for all covariates
- Competing risks framework assumes independence of event types
- Large sample size enables detection of small effects (practical vs. statistical significance)
- Future work: Time-dependent coefficients, frailty models, machine learning extensions




