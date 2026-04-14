# Cox Methods Brief (Cells 11–12)

This short brief explains what the pipeline is doing in **Cell 11** (KM + competing risks plots) and **Cell 12** (Cox model fitting and model‑based plots). It is written for quick advisor briefings.

---

## 1) Cell 11: KM and Competing Risks (empirical views)

Cell 11 generates **descriptive survival plots** that do **not** control for other covariates.

### 2.1 Kaplan‑Meier (KM)
KM plots show the **empirical survival curve** for promotion.

**Survival function (KM):**
$$
S(t) = P(T > t)
$$

**Meaning:**  
Here, $T$ is the **time‑to‑event** random variable (time‑to‑promotion).  
$S(t)$ is the probability an officer is **not yet promoted** by time $t$ (i.e., still at the source rank).

**What it answers:**  
“Among officers in group A vs group B, who tends to promote sooner, on average?”

**Key limitation:**  
KM curves are **unadjusted**. They compare groups **without controlling for other factors**, so apparent differences can reflect confounding.  
Example: if one group has more officers with high `prestige_sum` or `cum_tb_rcvd_ratio_snr`, the KM curve may look better even if the group label itself has no causal effect.

### 2.2 Competing Risks (CR)
Competing risks plots show the **cumulative incidence** of promotion when **attrition** is treated as a competing event.  
This is important because attrition removes officers from the risk set for promotion.

**What it answers:**  
“Given that attrition can occur, what is the cumulative probability of promotion by time *t*?”

**Key limitation:**  
Like KM, CR plots are **descriptive** and do **not** adjust for other covariates.  
Example: if a division has higher attrition due to job mix or `job_code`, the CR curve for promotion may look worse even if division membership itself is not the driver.

---

## 2) What is being modeled? (Cox / CPH)

We are modeling **time‑to‑promotion** using a **Cox proportional hazards model**. The key output is the **hazard ratio (HR)**, which tells us how much an officer’s **instantaneous promotion rate** changes with covariates, holding other variables constant.

**Interpretation:**
- **$HR > 1$**: Higher instantaneous promotion risk.
- **$HR < 1$**: Lower instantaneous promotion risk.
- **$HR = 1$**: No change relative to baseline.

**Baseline in this context:**  
The baseline is the model’s **reference profile**: all covariates set to their reference values (often medians for continuous variables, and **reference categories** for categorical variables). In our pipeline, baseline values are typically **medians** for continuous covariates, with dummies set to the **reference category** (usually the most common category unless explicitly specified).  
So “$HR = 1$” means **no change relative to that reference profile**.

The Cox model is **semi‑parametric**: it estimates covariate effects without assuming a specific baseline hazard shape.  
Concretely, it models:

$$
h(t \mid X) = h_0(t)\, e^{X\beta}
$$

- $h_0(t)$ is the **baseline hazard** (left unspecified, non‑parametric).
- $\exp(X\beta)$ is the **parametric** part that scales the hazard based on covariates.

This means we can estimate **hazard ratios** robustly (relative risk between covariate profiles) **without** making a strong assumption about the absolute time‑shape of the hazard.

---

## 3) Cell 12: Cox Models (adjusted effects)

Cell 12 fits **Cox proportional hazards models** and then uses those models to produce interpretable plots.

**What the Cox model is (and how it differs from KM/CR):**  
KM and CR are **empirical summaries** of observed outcomes. The Cox model is **model‑based**: it estimates how covariates shift the hazard rate, while holding other covariates constant. This is why Cox outputs are **adjusted effects**, not raw group comparisons.

### 3.1 Static vs Full models
- **Static model**: only time‑invariant covariates (e.g., demographics).  
- **Full model**: static + time‑varying covariates (OER metrics, prestige metrics, etc.).

### 3.2 Coefficients and hazard ratios
The model estimates **coefficients ($\beta$)** for each covariate.  
Exponentiating a coefficient gives the **hazard ratio**:

$$
HR = e^{\beta}
$$

If $\beta = 0.30$, then $HR \approx 1.35$ (about a **35% higher** instantaneous promotion rate).

**Important detail:**  
For a continuous variable, the HR is per **one‑unit increase** in that variable (or per **one‑SD** if you used z‑scores).  
For a binary variable, the HR compares **1 vs 0** relative to the reference category.  
For categorical variables (dummies), each HR compares a category **to the chosen reference**.

**Reference category (what it means):**  
The reference category is the **baseline category** that all other categories are compared to.  
In our pipeline, if you do not manually set a reference, the code typically uses the **most common category** as the reference (to stabilize estimates).  
Example: if `job_code` is turned into dummies and `IN` is most common, then `job_IN` becomes the reference and the model reports HRs for all other job codes **relative to IN**.

---

## 4) Cell 12 plots (conceptual interpretation)

### 12.6 Partial effects
Shows the **modeled effect of one variable** while holding all others at baseline (usually the median).

**Baseline here:**  
All other covariates are fixed at their reference values (median for continuous, reference category for dummies). This isolates the **marginal modeled effect** of the focal variable.

**Read as:**  
“If only this variable changes, how does the model predict the hazard ratio changes?”

### 12.7 Interaction surface
Shows the **modeled joint effect of two variables** across a grid.  
The red dashed line marks **$HR = 1.0$** (no change vs baseline).

**Read as:**  
“What combinations of X and Y keep the predicted hazard the same?  
Where does HR rise above or fall below 1?”

### 12.8 Model‑based promotion curves
Fixes two variables and varies time to show **predicted promotion curves** derived from the Cox model.

**Read as:**  
“Holding covariates fixed at selected values, how does the model predict promotion probability over time?”

---

## 5) Why model plots can differ from KM/CR

KM/CR plots are **unadjusted**; Cox plots are **adjusted**.  
That means a variable can appear positive in KM but flip in the Cox model if:
- it is correlated with another variable,
- it acts differently **after controlling** for other covariates, or
- it has an interaction effect.

---

## 6) Practical briefing takeaway

- **Cell 11** = *empirical, descriptive patterns* (good for intuition).  
- **Cell 12** = *model‑adjusted effects* (good for inference).  
- Differences between the two are expected and often reveal confounding or conditional effects.
