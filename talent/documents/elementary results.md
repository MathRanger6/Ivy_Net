# Counterintuitive Result and How We Resolved It (Run 1 vs Run 2)

This document explains the initial “contradiction” between empirical Competing Risks plots and Cox model partial effects, and then summarizes what we did in Run 1 and Run 2 to drill down and identify the underlying drivers.

---

## Table of Contents

1. [The Initial Contradiction](#the-initial-contradiction)
2. [Why the Contradiction Happens](#why-the-contradiction-happens)
3. [Run 1: Cumulative TB vs Pooled TB](#run-1-cumulative-tb-vs-pooled-tb)
4. [Run 2: Rank-Normalized TB vs Pooled TB](#run-2-rank-normalized-tb-vs-pooled-tb)
5. [What We Found](#what-we-found)
6. [Takeaway for Interpretation](#takeaway-for-interpretation)

---

## The Initial Contradiction

In the empirical Competing Risks (CIF) plots, we observe that `tb_ratio_rank_norm_snr` appears **positively** related to promotion (higher values show higher promotion incidence).  
But in the Cox model partial effects (CELL 12.6), the relationship appears to **reverse** when `cum_tb_rcvd_ratio_snr` is in the model.

That looks contradictory at first glance.

---

## Why the Contradiction Happens

The two plots answer **different questions**:

- **Competing Risks (CIF)** plots show **raw, unadjusted** patterns by group.
- **Cox partial effects** show **conditional, adjusted** effects: the model asks “what happens if we change one variable while holding the others fixed?”

Because `tb_ratio_rank_norm_snr` and `cum_tb_rcvd_ratio_snr` are correlated, the CIF plot reflects their **combined advantage**, while the Cox model separates them and assigns shared signal to one or the other. This is a standard confounding/collinearity situation.

---

## Run 1: Cumulative TB vs Pooled TB

**Goal:** Compare cumulative TB exposure to pooled mean TB while allowing interaction.

**Variables:**
- `z_cum_tb_rcvd_ratio_snr`
- `z_pool_tb_ratio_mean_snr`
- `z_star_pool_interaction`

**What this isolates:**  
Whether cumulative TB or pooled TB is the dominant signal once both are modeled together, and how their effects trade off at constant hazard.

**Interaction variable explanation (`z_star_pool_interaction`):**  
This term captures whether the effect of cumulative TB depends on pooled TB (and vice versa). In practice, it tests whether the slope of `z_cum_tb_rcvd_ratio_snr` changes across levels of `z_pool_tb_ratio_mean_snr`. If the interaction coefficient is:
- **Positive**, the effect of one variable becomes stronger as the other increases.
- **Negative**, the effect of one variable becomes weaker (or can even flip) as the other increases.

In the Cox model:
$$
\log(HR) = b_1 x + b_2 y + b_3 x y
$$
with $x = z\_cum\_tb\_rcvd\_ratio\_snr$ and $y = z\_pool\_tb\_ratio\_mean\_snr$, the interaction term $b_3$ tells us whether cumulative TB and pooled TB **reinforce** each other (synergy) or **substitute** for each other (trade-off).

---

## Run 2: Rank-Normalized TB vs Pooled TB

**Goal:** Replace cumulative TB with rank-normalized TB and see whether the rank-normalized signal holds once pooled TB is included.

**Variables:**
- `z_tb_ratio_rank_norm_snr`
- `z_pool_tb_ratio_mean_snr`
- `z_rank_pool_interaction`

**What this isolates:**  
Whether the rank-normalized TB metric adds independent explanatory power, or whether the positive empirical association is mostly explained by pooled TB.

**Interaction variable explanation (`z_rank_pool_interaction`):**  
This term tests whether the effect of rank-normalized TB depends on pooled TB. It answers: “Does rank-based TB matter more (or less) for promotion when pooled TB is high?” If the interaction coefficient is:
- **Positive**, the rank-normalized TB effect strengthens at higher pooled TB.
- **Negative**, the rank-normalized TB effect weakens at higher pooled TB.

In the Cox model:
$$
\log(HR) = b_1 x + b_2 y + b_3 x y
$$
with $x = z\_tb\_ratio\_rank\_norm\_snr$ and $y = z\_pool\_tb\_ratio\_mean\_snr$, the interaction term $b_3$ quantifies whether rank-normalized TB and pooled TB act **multiplicatively** (interaction present) rather than **additively** (no interaction).

---

## What We Found

- The empirical (CIF) plots show the **net, real-world association**, which can be positive because TB metrics move together.
- The Cox model shows the **conditional effect**, which can **flip** once the correlated TB metric is held fixed.
- Run 1 and Run 2 clarify **which TB construct carries the dominant signal**, and whether the alternative metric is redundant or reverses direction once adjusted.
- The interaction terms allow us to quantify **how much change in one metric offsets the other** at constant hazard:
  - If the fitted model is
    $$
    \log(HR) = b_1 x + b_2 y + b_3 x y
    $$
    then:
    $$
    \frac{\partial \log(HR)}{\partial x} = b_1 + b_3 y, \quad
    \frac{\partial \log(HR)}{\partial y} = b_2 + b_3 x
    $$
  - If $b_3 = 0$, the trade-off at constant HR simplifies to:
    $$
    \frac{dx}{dy} = -\frac{b_2}{b_1}
    $$

---

## Takeaway for Interpretation

The “contradiction” is not an error; it is the difference between **raw association** and **conditional effect**.  
Run 1 and Run 2 are the deliberate drill-down: they test which TB construct is really driving promotion outcomes, and they quantify trade-offs so we can interpret the relative magnitudes in z-score units.

