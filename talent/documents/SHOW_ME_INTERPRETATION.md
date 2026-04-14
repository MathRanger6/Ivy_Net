# Show_Me Interpretation (Parts 1–2)

This document follows the story arc you described:
- **Part 1: Prestige story** (Run 8)<br>
- **Part 2: Pool story** (Run 1, then Run 2)<br>

All interpretations refer to the **specific slide sets you provided** for these runs. Effects are in **hazard (instantaneous risk) units**, not direct promotion probabilities.

**Model formula (Cox PH, with interaction):**
$$
h(t \mid X)=h_0(t)\,\exp\left(\beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_k x_k\right)
$$
$$
\text{With interaction: } \eta = \beta_1 x + \beta_2 y + \beta_3 (x \cdot y)
$$
$$
\text{Hazard ratio for }x_j:\ \mathrm{HR}_j=\exp(\beta_j)
$$

---<br>

## Part 1 — Prestige story (big fish / strong pond)

### Run 8 — YGs 2002–2011, **no SF / no Aviation** (regular officers rotating through prestige)
**Variables:** `z_prestige_mean`, `z_cum_tb_rcvd_ratio_snr`, `z_prestige_tb_interaction`

**CR (CIF) plots — slides 4, 5, 6**
- **Promotion CIF:** Higher `z_cum_tb_rcvd_ratio_snr` bins show a large step‑up in promotion incidence. `z_prestige_mean` shows a smaller but visible lift.<br>
- **Attrition CIF:** Higher TB ratio corresponds to lower attrition; prestige effect is weaker but in the same direction.<br>

**Model comparison — slide 7**  
- Full model improves C‑index vs static → time‑varying effects add real signal.<br>
- **What each of the four panels shows:**<br>
- **Top‑left (C‑index comparison):** Predictive performance of static vs full model; higher is better, and the gap shows added signal from time‑varying covariates.<br>
- **Top‑right (Top 15 signal ratios):** Largest hazard ratios in the full model; bars > 1 increase promotion hazard, highlighting strongest positive effects.<br>
- **Bottom‑left (Coefficient comparison, common vars):** How coefficients for shared variables shift when time‑varying covariates are added; shrinkage suggests shared explanatory power.<br>
- **Bottom‑right (Signal ratio distribution):** Histogram of hazard ratios in the full model; the HR=1 line marks “no effect,” with right‑side mass indicating positive effects.<br>

**Competing risks comparison — slide 8**  
- Promotion vs attrition coefficients diverge, consistent with the CIF patterns.<br>
- **What the two panels show:**<br>
- **Left (Promotion vs Attrition Coefficients):** Side‑by‑side coefficients for the same variables; promotion > 0 and attrition < 0 indicates a variable helps promotion while reducing attrition.<br>
- **Prestige_mean in this panel:** small positive promotion coefficient and near‑zero/slightly negative attrition coefficient → a modest, “clean” signal (helps promotion, does not increase attrition).<br>
- **Right (Signal Ratio Comparison):** Scatter of promotion HR (x) vs attrition HR (y); points below the diagonal indicate stronger promotion effects, and the bottom‑right quadrant (x>1, y<1) is the most favorable pattern.<br>
- **Interpretation for this run:** `z_cum_tb_rcvd_ratio_snr` should sit to the right of 1 on the x‑axis and below 1 on the y‑axis (strong promotion signal and lower attrition), while `z_prestige_mean` should also be right of 1 but closer to 1 (positive but smaller effect).<br>

**Signal ratio (hazard ratio) reminder:**
- Signal ratio = **exp(coefficient)**.<br>
- **> 1** increases promotion hazard; **< 1** decreases promotion hazard; **= 1** is no effect.<br>

**Partial effects — slide 9**
- `z_prestige_mean` ↑ → HR ↑ (modest slope).<br>
- `z_cum_tb_rcvd_ratio_snr` ↑ → HR ↑ (strong slope).<br>
- `z_prestige_tb_interaction` shows a **negative slope** → **dampening interaction**.<br>
- **Negative interaction concept:** the joint effect is **less than additive**; the marginal gain of one variable shrinks as the other increases.<br>
- **Strong positive vs strong negative (rule of thumb):**<br>
  - Interaction **> +0.05 to +0.10** → clear positive synergy.<br>
  - Interaction **< −0.05 to −0.10** → clear negative (dampening).<br>
  - **Between −0.01 and +0.01** → essentially additive.<br>

**Distributions — slide 10**
- Prestige is **highly skewed** (most near 0), so effects are concentrated in a smaller subgroup.<br>

**Surface + contour — slide 11**
- Surface rises strongly with TB, weakly with prestige.<br>
- **Negative interaction**: combined boost is **less than additive** when both are high.<br>
- **How to read the surface:** moving along the TB axis produces a steep rise in HR; moving along the prestige axis yields a smaller lift, so TB dominates the vertical “tilt.”<br>
- **How to read the contour:** contour bands are close to horizontal because TB drives most of the change; the HR=1 line shows the trade‑off combinations that keep promotion risk constant. **On the HR>1 side**, promotion hazard is above baseline (faster promotion). **On the HR<1 side**, promotion hazard is below baseline (slower promotion).<br>

**Full model coefficients — slide 11**
- `z_prestige_mean` **b = 0.0783**, HR ≈ **1.081**<br>
- `z_cum_tb_rcvd_ratio_snr` **b = 0.3235**, HR ≈ **1.382**<br>
- `z_prestige_tb_interaction` **b = −0.0159**, HR ≈ **0.984**<br>
**How to read coefficient strength (rule‑of‑thumb):**
- The **interaction coefficient (b3)** is a **slope parameter**, not the x‑axis value; it controls how steeply the interaction curve rises/falls.<br>
- Rough guide: **|b3| ≥ 0.05–0.10** is a clearly strong interaction; **|b3| ≤ 0.01** is near‑additive.<br>
- The interaction **x‑axis range** (often wide, e.g., −10 to +15) is the *value of the interaction variable*, not the coefficient magnitude.<br>

**Run 8 interpretation (plain English):**
- In regular‑officer populations, **TB ratio is the dominant signal** for promotion.<br>
- **Prestige helps**, but modestly.<br>
- The **negative interaction** supports the “strong pond” story: high TB in high‑prestige environments yields **diminishing marginal returns**.<br>

---<br>

**Run 8 note (mentioned verbally, not shown):**  
I will mention that Run 9 (combat‑arms only) showed **even stronger TB dominance**, **smaller prestige effect**, and a **slightly positive interaction** (nearly additive), but I am not showing those slides.

## Part 2 — Pool story (why Run 1 + Run 2)

Run 1 and Run 2 were both necessary because **the two individual TB metrics move together**. `z_cum_tb_rcvd_ratio_snr` is absolute performance and `z_tb_ratio_rank_norm_snr` is relative standing, but in practice they’re collinear. If we put both in one model, the effects blur together, so we split them into two runs.

**Run 1 (absolute performance):**  
We use `z_cum_tb_rcvd_ratio_snr` with `z_pool_tb_ratio_mean_snr` and `z_star_pool_interaction` to ask: **Does a strong pool amplify or dampen raw performance?** In plain terms: if two officers have the same raw TB ratio, does the pool context change their promotion signal?

**Run 2 (relative performance):**  
We swap the individual metric to `z_tb_ratio_rank_norm_snr` and keep the same pool variable. Now we ask: **Does standing within your pool add signal beyond the pool’s strength itself?** This cleanly separates “how you rank” from “how strong your pool is.”

**Bottom line:**  
We run two models so we can talk about **both** “how good you are” and “how strong your environment is,” without the two individual TB signals stepping on each other.

### Run 1 — absolute TB vs pool TB
**Variables:** `z_cum_tb_rcvd_ratio_snr`, `z_pool_tb_ratio_mean_snr`, `z_star_pool_interaction`

**CR (CIF) plots — slides 17, 18, 19**
- I will walk each variable: higher bins show **higher promotion** and **lower attrition** overall.<br>
- For `z_cum_tb_rcvd_ratio_snr`, the curves separate the most → **raw performance is a strong signal**.<br>
- For `z_pool_tb_ratio_mean_snr`, the curves also separate → **environment strength matters on its own** (even before modeling).<br>
- For `z_star_pool_interaction`, separation is weaker (as expected for a constructed interaction), but it does not contradict the model‑based interaction.<br>

**Model comparison — slide 20**
- Full model > static (time‑varying signal adds value).<br>
- I will say: “Adding pool variables improves ranking performance, so pool context carries real predictive signal.”<br>

**Competing risks — slide 21**
- Promotion vs attrition coefficients diverge as expected.<br>
- I will emphasize: positive promotion + negative attrition is the clean signature of a promotion signal.<br>
- I’ll call out that pool mean behaves like a **promotion‑leaning signal**, not an attrition‑driving one.<br>

**Partial effects — slide 22**
- All three partial effects are positive.<br>
- I will compare slopes: **pool mean often rises steeply**, showing a large effect size relative to individual TB ratio.<br>
- I will note curvature: non‑linear shapes imply that **signal strengthens at higher z‑scores**.<br>

**Surface + contour — slides 23, 24**
- Surface slopes upward in both directions → both variables contribute positively.<br>
- HR=1 line shows compensating trade‑offs between individual TB and pool strength.<br>
- I will describe the “strong‑pool amplification” idea: the surface lifts faster when **both** are high, which is exactly what a positive interaction means.<br>

**Coefficients — slide 24**
- `z_cum_tb_rcvd_ratio_snr` **b = 0.2455**<br>
- `z_pool_tb_ratio_mean_snr` **b = 0.3596**<br>
- `z_star_pool_interaction` **b = 0.1079**<br>
**How to read coefficient strength (rule‑of‑thumb):**
- The interaction coefficient is a **slope parameter**; it governs how much the joint effect departs from additivity.<br>
- **|b3| ≥ 0.05–0.10** indicates a strong interaction; **|b3| ≤ 0.01** indicates near‑additive effects.<br>

**Interpretation:**
- Pool TB mean has the **larger main effect**.<br>
- Interaction is **positive**, so strong pools **amplify** individual TB effects.<br>
- Plain English: “Being good helps everywhere, but being good in a strong pool helps **even more**.”<br>

---<br>

### Run 2 — rank‑normalized TB vs pool TB
**Variables:** `z_tb_ratio_rank_norm_snr`, `z_pool_tb_ratio_mean_snr`, `z_rank_pool_interaction`

**CR (CIF) plots — slides 29, 30, 31**
- Higher bins → higher promotion; lower attrition.<br>
- I will explain that `z_tb_ratio_rank_norm_snr` is **relative standing**, so it tests whether “ranking high inside a pool” still matters.<br>
- `z_pool_tb_ratio_mean_snr` again shows separation → **pool strength remains a strong signal** even when we swap the individual metric.<br>
- The interaction CIF may be subtle, which is fine because interaction is best interpreted via the model plots.<br>

**Model comparison — slide 32**
- Full model > static.<br>
- I will emphasize: the improvement persists even when the individual metric is rank‑normalized, so pool context is robust.<br>

**Competing risks — slide 33**
- Promotion vs attrition coefficients diverge.<br>
- I will say: rank‑normalized TB increases promotion and does not increase attrition — a clean signal of “standing.”<br>

**Partial effects — slide 34**
- All three partial effects are positive.<br>
- I’ll note that rank‑normalized TB is positive but often **less steep** than pool mean, reinforcing that environment strength is a major driver.<br>

**Surface + contour — slides 35, 36**
- Upward slope in both directions → both variables push promotion up.<br>
- HR=1 line shows trade‑off between rank‑standing and pool strength.<br>
- With a near‑zero interaction, the surface looks **close to additive** (little twist).<br>

**Coefficients — slide 36**
- `z_tb_ratio_rank_norm_snr` **b = 0.3620**<br>
- `z_pool_tb_ratio_mean_snr` **b = 0.5123**<br>
- `z_rank_pool_interaction` **b = 0.00335**<br>
**How to read coefficient strength (rule‑of‑thumb):**
- The interaction coefficient is the **slope** of the interaction effect (not the interaction axis range).<br>
- **|b3| ≤ 0.01** means the surface is almost additive.<br>

**Interpretation:**
- Pool TB mean is still the **largest main effect**.<br>
- Interaction is **near zero**, so effects are **almost additive**.<br>
- Plain English: “Pool strength matters a lot; ranking high helps, but the two mostly stack rather than amplify.”<br>

---<br>

### Run 1 vs Run 2 (pool story contrast)
- Pool TB mean is the **dominant driver in both runs**.<br>
- Rank‑normalized TB (Run 2) is **stronger** than cumulative TB (Run 1).<br>
- Interaction differs:<br>
  - **Run 1:** positive and meaningful (pool amplifies individual TB).<br>
  - **Run 2:** near zero (little interaction).<br>
- **Branch‑filtered check:** Infantry‑only runs show **stronger pool dominance**, while CS/CSS runs look **more balanced**.<br>

**Story takeaway for Part 2:**  
Pool strength consistently matters, but **how “individual performance” is defined** changes the interaction. Absolute TB shows **amplification in strong pools**, while rank‑normalized TB is **mostly additive**.

---<br>

## Interpretation reminder
These are **hazard ratios** in standardized units. They describe **relative risk of promotion** (earlier promotion), not literal promotion probabilities.

---<br>

## How to read each plot type

### CR (CIF) plots (Competing Risks)
- **What it is:** Empirical (unadjusted) cumulative incidence for promotion and attrition by group/bin.<br>
- **How to read:** Higher promotion curves mean faster/greater promotion incidence; lower attrition curves mean less attrition.<br>
- **What to emphasize:** Separation between bins (wide gaps) implies strong empirical differences; crossings imply non‑monotone behavior or heterogeneous groups.<br>
- **Pitfalls:** Binning method matters; small top bins can look unstable; these are not adjusted for other covariates.<br>
- **Use:** Descriptive sanity check before modeling; good for audience intuition.<br>
- **Data source:** `df_analysis` from Cell 11 (post‑filtering, binned/grouped for plotting).<br>
- **Speaker point:** “These curves are the raw data story — before the model — showing who promotes or attrits faster by group.”<br>

### Model comparison panel (C‑index)
- **What it is:** Predictive accuracy (ranking ability) of static vs full model.<br>
- **How to read:** Higher C‑index is better; the gap shows the added value of time‑varying covariates.<br>
- **What to emphasize:** The **delta** (full − static) is the key story, not the absolute value.<br>
- **Pitfalls:** C‑index is about ranking, not calibration; a small gain can still be meaningful in large samples.<br>
- **Use:** Demonstrates whether the model improves with added covariates.<br>
- **Data source:** Model outputs from Cell 12 (static model vs full model fit).<br>
- **Speaker point:** “The only thing I’m selling here is the improvement — time‑varying info adds real signal.”<br>

### Top signal ratios (bar chart)
- **What it is:** Largest hazard ratios (exp(b)) in the full model.<br>
- **How to read:** Bars > 1 increase promotion hazard; < 1 decrease it.<br>
- **What to emphasize:** Look for **magnitude** and **consistency** with your theory (e.g., TB ratio should be among the largest).<br>
- **Pitfalls:** Only shows the top effects; omits negative or smaller but meaningful effects.<br>
- **Use:** Quick scan of strongest positive effects.<br>
- **Data source:** Full model coefficients from Cell 12 (`full_model_coefficients*.csv`).<br>
- **Speaker point:** “This is the ‘big hitters’ list — which variables move the needle the most.”<br>

### Coefficient comparison (common variables)
- **What it is:** Coefficient values for variables shared between static and full models.<br>
- **How to read:** Shifts indicate how much the effect changes once time‑varying covariates are added.<br>
- **What to emphasize:** Large shrinkage suggests overlap/mediation; sign flips indicate potential confounding.<br>
- **Pitfalls:** Different scales or standardization can change coefficient size; compare direction first, then magnitude.<br>
- **Use:** Detects overlap or confounding with added variables.<br>
- **Data source:** Static vs full model coefficient tables from Cell 12.<br>
- **Speaker point:** “If a static effect shrinks, it’s because the time‑varying measures are explaining it.”<br>

### Signal ratio distribution (histogram)
- **What it is:** Distribution of all hazard ratios in the full model.<br>
- **How to read:** HR=1 line is “no effect”; right‑side mass = positive effects.<br>
- **What to emphasize:** A tight distribution near 1 implies modest effects; a long right tail signals a few strong drivers.<br>
- **Pitfalls:** This mixes many variable types (continuous, binary, interactions); don’t over‑interpret the shape.<br>
- **Use:** Overall balance and spread of model effects.<br>
- **Data source:** Full model coefficients from Cell 12.<br>
- **Speaker point:** “Most effects are modest; a few variables do most of the work.”<br>

### Competing risks coefficients (left panel)
- **What it is:** Side‑by‑side promotion vs attrition coefficients for the same variables.<br>
- **How to read:** Promotion > 0 and attrition < 0 means a variable helps promotion and reduces attrition.<br>
- **What to emphasize:** Opposite signs are the “clean success signal”; same‑sign effects imply mixed trade‑offs.<br>
- **Pitfalls:** Coefficients are on the log‑hazard scale; compare signs first, then relative size.<br>
- **Use:** Quick sign check and magnitude comparison.<br>
- **Data source:** Competing‑risks model outputs from Cell 12.<br>
- **Speaker point:** “I’m checking if variables push promotion up while pushing attrition down.”<br>

### Competing risks signal ratio scatter (right panel)
- **What it is:** Promotion HR (x) vs attrition HR (y) for the same variables.<br>
- **How to read:** Bottom‑right quadrant (x>1, y<1) is ideal; points below diagonal mean stronger promotion than attrition effect.<br>
- **What to emphasize:** Distance from the diagonal reflects imbalance between promotion and attrition effects.<br>
- **Pitfalls:** If many points cluster near (1,1), effects are weak even if signs differ.<br>
- **Use:** Visual check of trade‑offs across outcomes.<br>
- **Data source:** Competing‑risks model outputs from Cell 12.<br>
- **Speaker point:** “Bottom‑right is the sweet spot: higher promotion, lower attrition.”<br>

### Partial effects
- **What it is:** Model‑based effect of a single variable holding others fixed.<br>
- **How to read:** Upward curve = increasing hazard; downward curve = decreasing hazard.<br>
- **What to emphasize:** The **shape** (linear vs curved) and **steepness** reflect strength.<br>
- **Pitfalls:** These are conditional on other variables being fixed at baseline values; interpret as “all else equal.”<br>
- **Use:** Shows direction and non‑linearity of each covariate.<br>
- **Data source:** Full model + `df_full_model` from Cell 12.<br>
- **Speaker point:** “This is the clean, one‑variable‑at‑a‑time effect after controlling for everything else.”<br>

### Interaction surface (3D)
- **What it is:** Model‑based hazard ratio surface across two variables.<br>
- **How to read:** Steeper axis = stronger driver; curvature/twist indicates interaction.<br>
- **What to emphasize:** Look for flattening or steepening at high‑high values to diagnose dampening vs synergy.<br>
- **Pitfalls:** The surface reflects model structure and the chosen baseline; extreme corners may be data‑sparse.<br>
- **Use:** Visualizes how two variables combine to affect hazard.<br>
- **Data source:** Full model + `df_full_model` from Cell 12 (Cell 12.7).<br>
- **Speaker point:** “The tilt shows which variable dominates; the twist shows interaction.”<br>

### Interaction contour (2D)
- **What it is:** Top‑down view of the interaction surface (iso‑HR lines).<br>
- **How to read:** HR=1 line is baseline; HR>1 side = higher promotion hazard, HR<1 side = lower hazard.<br>
- **What to emphasize:** The slope of the HR=1 line encodes the trade‑off between x and y.<br>
- **Pitfalls:** Small shifts in the line can look dramatic; always connect to coefficient signs.<br>
- **Use:** Shows trade‑off combinations that keep risk constant.<br>
- **Data source:** Full model + `df_full_model` from Cell 12 (Cell 12.7).<br>
- **Speaker point:** “The HR=1 line is the break‑even trade‑off; one side is better‑than‑baseline.”<br>

### Variable distributions
- **What it is:** Histogram of each variable used in interaction plots.<br>
- **How to read:** Reveals skew, tails, and where most observations lie.<br>
- **What to emphasize:** If most mass is near zero, extreme surface regions are not well supported by data.<br>
- **Pitfalls:** Z‑score distributions can hide zero‑inflation; check raw distributions when needed.<br>
- **Use:** Context for how much of the surface is supported by data.<br>
- **Data source:** `df_full_model` from Cell 12 (post‑filtering, same sample as interaction plots).<br>
- **Speaker point:** “This tells us how much of the surface is real data vs extrapolation.”<br>

### Correlation table (interaction variables)
- **What it is:** Pearson correlation between interaction inputs.<br>
- **How to read:** |r| near 1 = strong collinearity; near 0 = weak.<br>
- **What to emphasize:** High correlation means interaction terms may be unstable or hard to interpret.<br>
- **Pitfalls:** Correlation does not imply causation; it only signals potential collinearity in estimation.<br>
- **Use:** Flags potential collinearity that can distort interaction interpretation.<br>
- **Data source:** `df_full_model` from Cell 12 (same sample as interaction plots).<br>
- **Speaker point:** “High correlation means the interaction is harder to separate cleanly.”<br>

---<br>

## Slide-by-slide speaker notes (Show_Me_final_working.pdf)

### Part 1 — Run 8 (model validation; TB ratio as the obvious signal)

**Slide 4 — CR/CIF: `z_cum_tb_rcvd_ratio_snr`**  
This is the empirical (unmodeled) story: higher `z_cum_tb_rcvd_ratio_snr` groups promote faster and more often. The promotion curves separate early and stay separated, which is what we would expect if TB ratio is a real performance signal. On the attrition panel, higher TB ratio groups sit lower, showing a “stay in” pattern that mirrors the promotion story. This slide validates that the raw data aligns with intuition before modeling.

**Slide 5 — CR/CIF: `z_prestige_mean`**  
Prestige shows a smaller, more modest separation than TB ratio. I’ll emphasize that this is expected: prestige service matters, but it is not as strong a signal as cumulative TB ratio. The main takeaway is that the effect is in the expected direction and visible even in the raw curves.

**Slide 6 — CR/CIF: `z_prestige_tb_interaction`**  
Interaction groups are less clean in raw CIF because the interaction is a combined construct, not a direct observation. If separation is present, I’ll frame it as “consistent with interaction,” but I won’t over‑interpret. This slide mainly prepares the audience for the modeled interaction effects later.

**Slide 7 — Model comparison panel**  
I’ll say: “This tells us the model actually improves when we add the time‑varying covariates.” The key message is the jump in C‑index from static to full. The top‑15 signal ratios show TB ratio among the strongest effects, which matches the validation story. I’ll remind the audience that HR>1 means higher promotion hazard.

**Slide 8 — Competing risks comparison**  
Left: promotion vs attrition coefficients for the same variables; right: signal ratio scatter. I’ll point out that for TB ratio the promotion effect is positive and the attrition effect is negative, which is exactly the signature of a clean promotion signal. If any point lies below the diagonal on the scatter, I’ll say it “leans more toward promotion than attrition.” For `z_prestige_mean`, I’ll note the small positive promotion coefficient with near‑zero/slightly negative attrition — a modest but clean signal (helps promotion, doesn’t increase attrition).

**Slide 9 — Partial effects**  
These are model‑based marginal effects. I will emphasize the steep curve for TB ratio versus the gentler curve for prestige. The interaction term slopes downward, which means **as the interaction increases, the model predicts a lower promotion hazard** (HR falls below 1). That is a **negative/dampening interaction**: the combined effect is **less than additive**. In plain English, when both `z_prestige_mean` and `z_cum_tb_rcvd_ratio_snr` are high, the extra boost from one is **smaller** because the other is already high. This does **not** mean prestige or TB “hurts” promotion on its own; it means the **synergy is negative**, so being strong on both doesn’t give as big a lift as adding the two effects separately.

**Slide 10 — Distributions**  
This slide is the reality check: prestige is skewed (most near zero), TB ratio is more spread. I’ll explain that the extreme upper‑right corner of the surface plots is supported by fewer observations, so we interpret that region carefully.

**Slide 11 — Surface/contour + coefficient notes**  
I’ll explain the surface tilt: the hazard rises strongly with TB ratio and only modestly with prestige. On the contour, the HR=1 line is the “break‑even” trade‑off; one side is faster promotion, the other is slower. I’ll add the rule‑of‑thumb: the interaction coefficient (b3) is the slope driver of the twist, not the axis range.

---<br>

### Part 2 — Why two runs (pool effects)

**Transition script (before Slide 17):**  
We do two runs because individual TB metrics and pool‑mean TB are correlated. Run 1 uses absolute performance (`z_cum_tb_rcvd_ratio_snr`) plus pool mean, which captures raw performance and environment together. Run 2 switches the individual measure to rank‑normalized TB, which isolates “standing within pool” and separates it from pool strength. Together these runs distinguish “how good you are” from “how strong your environment is.”

---<br>

### Run 1 — `z_cum_tb_rcvd_ratio_snr`, `z_pool_tb_ratio_mean_snr`, `z_star_pool_interaction`

**Slide 17 — CR/CIF: `z_cum_tb_rcvd_ratio_snr`**  
This is the absolute performance signal. Higher bins show faster promotion and lower attrition. I’ll say this confirms the basic validity of the performance metric in the raw data.

**Slide 18 — CR/CIF: `z_pool_tb_ratio_mean_snr`**  
This shows the “environment” signal. Higher pool mean is associated with higher promotion incidence, which implies that being in a strong pool matters beyond individual performance.

**Slide 19 — CR/CIF: `z_star_pool_interaction`**  
This is the raw interaction grouping. I’ll be careful: separation here is weaker, and that’s normal because interaction variables are derived. The purpose is to show the raw data doesn’t contradict the modeled interaction.

**Slide 20 — Model comparison panel**  
Full model improves C‑index over static. I’ll highlight that adding pool‑based variables adds real signal, not just noise.

**Slide 21 — Competing risks comparison**  
For the key variables, promotion coefficients are positive and attrition coefficients are negative. I’ll say: “This is the clean success signature — higher TB or stronger pool pushes promotion up while pushing attrition down.”

**Slide 22 — Partial effects**  
All three curves are upward. I’ll emphasize that pool mean is steep, often steeper than individual TB, which is a critical insight: pool strength itself carries a strong signal.

**Slide 23 — Surface/contour**  
The surface slopes upward in both directions; the contour HR=1 line shows trade‑offs between individual TB and pool mean. I’ll say: “Strong pools amplify individual performance — you see that as the surface rises more sharply when both are high.”

**Slide 24 — Coefficient table / trade‑off**  
I’ll read the coefficients and translate them: “Pool mean has the larger main effect; interaction is positive, so effects reinforce.” If needed, I’ll quote the trade‑off rate shown on the slide as the practical conversion between the two z‑scores.

---<br>

### Run 2 — `z_tb_ratio_rank_norm_snr`, `z_pool_tb_ratio_mean_snr`, `z_rank_pool_interaction`

**Slide 29 — CR/CIF: `z_tb_ratio_rank_norm_snr`**  
This is “standing within the pool.” Higher ranks still predict faster promotion and lower attrition, validating the rank‑normalized metric.

**Slide 30 — CR/CIF: `z_pool_tb_ratio_mean_snr`**  
The pool signal remains strong in the raw data. This reinforces that pool strength matters even after shifting the individual measure to rank‑normalized TB.

**Slide 31 — CR/CIF: `z_rank_pool_interaction`**  
Raw interaction separation is limited, which is expected. I’ll say: “Interaction is mostly a modeled effect; we mainly interpret it through the coefficients and surface.”

**Slide 32 — Model comparison panel**  
Full > static again. This shows that pool metrics still improve model fit even when the individual measure is rank‑normalized.

**Slide 33 — Competing risks comparison**  
Promotion coefficients are positive; attrition coefficients are negative for key variables. I’ll point out whether pool mean or rank‑normalized TB is the larger promotion signal based on the bars/scatter.

**Slide 34 — Partial effects**  
Rank‑normalized TB is positive but often less steep than absolute TB. Pool mean remains strong. I’ll say: “This suggests environment is a consistent driver, while individual standing is meaningful but slightly smaller.”

**Slide 35 — Surface/contour**  
Surface rises with both variables; the interaction looks close to additive (little twist). I’ll say: “This means pool strength and rank‑standing stack rather than amplify.”

**Slide 36 — Coefficient table / trade‑off**  
I’ll read the coefficients: pool mean is the strongest main effect, interaction is near zero. I’ll emphasize that the trade‑off is close to linear and additive here.
