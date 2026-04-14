# Different Plot Comparisons (KM/CR vs 12.6/12.7/12.8)

This document explains what you are actually looking at in the KM/CR plots (CELL 11) and the model-based plots in CELL 12 (12.6, 12.7, 12.8), using the example variables `cum_tb_rcvd_ratio_snr` and `tb_ratio_rank_norm_snr`. It focuses on plain-English interpretation, what each plot does and does not tell you, and why the pictures are not expected to match.

---

## Table of Contents

1. [Where These Plots Live in the Pipeline](#where-these-plots-live-in-the-pipeline)
2. [KM Plot: What You Are Looking At](#km-plot-what-you-are-looking-at)
3. [Competing Risks Plot: What You Are Looking At](#competing-risks-plot-what-you-are-looking-at)
4. [12.6 Partial Effects: What You Are Looking At](#126-partial-effects-what-you-are-looking-at)
5. [12.7 Interaction Surface: What You Are Looking At](#127-interaction-surface-what-you-are-looking-at)
6. [12.8 Model-Based Curves: What You Are Looking At](#128-model-based-curves-what-you-are-looking-at)
7. [Why 12.7 Does Not Look Like 12.6](#why-127-does-not-look-like-126)
8. [What These Plots Can and Cannot Tell You](#what-these-plots-can-and-cannot-tell-you)

---

## Where These Plots Live in the Pipeline

- **KM/CR plots** are in **CELL 11** (empirical plots from data after filtering and binning).
- **12.6, 12.7, 12.8** are in **CELL 12** and require the **full Cox model (`cph_full`)**.
- The CELL 12 plots are **model-based** (they use fitted coefficients and controlled covariate profiles).

---

## KM Plot: What You Are Looking At

Example variables: `cum_tb_rcvd_ratio_snr` and `tb_ratio_rank_norm_snr`

In plain English:

- A KM plot shows **observed promotion timing** (or survival) for **groups** of officers.
- For these variables, the plot usually **bins** officers (low, mid, high) and shows the observed survival curve for each bin.

What it tells you:

- "In the raw data, officers in group A tend to promote sooner or later than group B."

What it does not tell you:

- It does **not adjust** for other variables (confounding is possible).
- It does **not isolate** the independent effect of the variable.

---

## Competing Risks Plot: What You Are Looking At

Example variables: `cum_tb_rcvd_ratio_snr` and `tb_ratio_rank_norm_snr`

In plain English:

- A competing risks plot is still an **observed curve**, but it separates **promotion vs attrition** risks.
- It tells you **how likely** each group is to promote or attrit over time.

What it tells you:

- "For this binned variable, promotion and attrition happen at different rates across groups."

What it does not tell you:

- It still **does not control** for other covariates.
- It is not a model projection; it is an empirical summary.

---

## 12.6 Partial Effects: What You Are Looking At

Example variables: `cum_tb_rcvd_ratio_snr` and `tb_ratio_rank_norm_snr`

In plain English:

- This is a **model-based curve** showing what the Cox model says happens **if you change one variable** and **hold everything else fixed**.
- It is a **controlled "what-if" curve**, not an observed survival curve.

What you see:

- A curve of **relative hazard** (risk) as the variable changes.
- The baseline is the **median officer profile** in the model.

What it tells you:

- "Holding all other variables constant, the model estimates higher/lower hazard as this variable increases."

What it does not tell you:

- It does **not show real-world group survival**, only a model prediction.
- It does **not reflect how officers actually co-vary on other traits**.

---

## 12.7 Interaction Surface: What You Are Looking At

Example variables: `cum_tb_rcvd_ratio_snr` (X axis) and `tb_ratio_rank_norm_snr` (Y axis)

In plain English:

- This is a **3D surface** showing how the model's predicted hazard changes when **both variables change together**.
- All other variables are held fixed at their median values.

What you see:

- A surface or contour map of **relative hazard**.
- Each point on the surface is a model prediction, not an observed outcome.

What it tells you:

- "The model believes the effect of X depends on Y (or vice versa)."

What it does not tell you:

- It is not a combination of KM or CR curves.
- It does not show any empirical group sizes or counts.

---

## 12.8 Model-Based Curves: What You Are Looking At

Example variables: `cum_tb_rcvd_ratio_snr` and `tb_ratio_rank_norm_snr`

In plain English:

- This is a **model-based promotion curve** computed for a **few fixed X/Y values**.
- It is the Cox model's **projected curve**, not an empirical curve.

What you see:

- A small set of curves, each representing a **hypothetical officer profile** with fixed X/Y values and median values for everything else.

What it tells you:

- "If we hold everything constant and set these two variables to specific values, the model projects different promotion timing."

What it does not tell you:

- It does not show the real promotion curve for actual officers with those exact values.

---

## Why 12.7 Does Not Look Like 12.6

In plain English:

- **12.6** is a **single-variable slice** of the model.
- **12.7** is a **two-variable surface** of the model.

So they look different because:

1. **12.6 ignores the joint effect**
   - It only changes one variable at a time.
2. **12.7 exposes interactions**
   - The model might change the effect of X depending on Y.
3. **Different ranges**
   - 12.6 uses full observed range, 12.7 uses 5th to 95th percentiles.

---

## Why `tb_ratio_rank_norm_snr` Can Flip Direction in 12.7

In plain English:

- The KM plot is a **raw group comparison**. It can show higher promotion probability for higher `tb_ratio_rank_norm_snr` because that group also tends to have other favorable traits (including higher `cum_tb_rcvd_ratio_snr`).
- The 12.7 surface is a **controlled model prediction**. It asks: "If we hold everything else constant, what does the model predict when only X and Y change?"

That means a reversal can happen for several reasons:

1. **Confounding in the raw data**
   - In the real data, higher rank and more TBs tend to move together.
   - KM reflects that combined advantage, not the isolated effect of rank.

2. **Conditional effect in the model**
   - The Cox model is estimating the **effect of rank after controlling for `cum_tb_rcvd_ratio_snr` and all other covariates**.
   - If the model finds that rank contributes less (or even negatively) once TBs are held fixed, the slope can flip.

3. **Collinearity and shared signal**
   - The two variables overlap in what they measure.
   - When you include both, the model assigns the "shared effect" to one of them, which can make the other look smaller or negative.

4. **Model form is log-linear**
   - The surface is just $\exp(\beta_x X + \beta_y Y)$ relative to a baseline.
   - If $\beta_y$ is negative in the fitted model, the surface will **decrease with Y** no matter what X is.

So the 12.7 surface is not "wrong"; it is answering a **different question**: it shows the model's **conditional** prediction after accounting for other variables, not the raw pattern in the data.

---

## What These Plots Can and Cannot Tell You

What they can tell you:

- Whether a variable is **associated** with promotion timing (KM/CR).
- Whether the model estimates an **independent effect** (12.6).
- Whether the model estimates an **interaction** (12.7).
- What the model projects for **fixed profiles** (12.8).

What they cannot tell you:

- Causality (all are observational).
- Real-world outcomes without considering confounders (KM/CR).
- Real-world outcomes without model assumptions (12.6/12.7/12.8).


