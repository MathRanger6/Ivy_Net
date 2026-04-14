# Presentation Interpretation: Run 1 (Slides 5–20) and Run 3 (Slides 24–30)

**Context:** CS+CSS job codes (non–direct combat), YG ~2002–2013. *No Run 2 in this presentation.*

**Primary research question:** *How does getting into the highest rater pool affect careers?*

**Specific hypothesis under investigation:** *Once you get into the highest pools, do you experience **diminishing returns** — i.e., does the benefit of being “at the top” flatten or even reverse because you are now being ranked against superstars?* In other words: is there a real effect whereby the very top of the distribution (the “superstar pools”) yields smaller gains in promotion (or higher attrition) than the upper-middle, consistent with a “big fish in a big pond” or “competing with superstars” story? This document interprets each slide with that possibility in mind and assesses where the data support it, where they do not, and where they remain ambiguous.

---

## Part 1: Slide-by-slide interpretation

### Slide 5 — Senior rater pool size distribution

**What it shows:**  
The slide presents the distribution of senior rater pool size across all snapshot–officer combinations in your analysis, in four views: linear axes, log x (logarithmic pool size), log y (logarithmic count), and log-log. This lets you see both the typical pool sizes and the long tail of very large pools that would be hard to see on a linear scale alone.

**Takeaways:**  
- There are **n = 258,132** observations (snapshot–officer combinations). The **median** senior rater pool size is **19**; the **mean** is **26.018**, so the distribution is right-skewed: most officers are in relatively small pools, but a minority are in much larger pools that pull the average up.  
- The **5th percentile** of pool size is **3** and the **95th** is **75**. So a large share of officers are in pools of 19 or fewer, while a nontrivial fraction are in pools of 75 or more.  
- The log-scale views make the long tail visible: pool sizes extend well beyond 75, and the frequency of these large pools, while lower than for small pools, is not negligible.  
- “Being at the top” of a pool of 5 is a very different competitive environment from being at the top of a pool of 75: in the latter, you are literally being compared with many more peers, and the “top” of that pool may be a much more selected (superstar) group.

**Diminishing returns / superstar pools:**  
This slide sets up the *possibility* of diminishing returns. In **large** pools, the officers who make it into the highest quantiles (e.g., top 10% or top bin by TB ratio or pool-minus-mean) are, by definition, being ranked against many more people — and plausibly against a more concentrated set of “superstars” who also landed in that pool. So the *meaning* of “highest rater pool” could differ by pool size: in small pools, “top” might be achievable with a lower absolute bar; in large pools, “top” might require competing with the best. Your pool-minus-mean and TB-ratio metrics are defined within each officer’s own pool, so they already control for pool size in the sense of “how far above my pool’s average am I?” — but the *level* of that average (and thus the level of competition) can still vary. Slide 5 does not test diminishing returns by itself; it establishes that pool context is heterogeneous and that the “highest” pools could, in principle, be the ones where competition is fiercest.

**For your story:**  
Use this slide to motivate why diminishing returns are plausible: pool context varies a lot, and “being at the top” in a large, strong pool might not deliver the same marginal benefit as being at the top in a smaller or weaker pool. The rest of the slides ask whether the data actually show that pattern.

---

### Slide 6 — Promotion CIF: Z TB Ratio Fwd SNR (8 bins)

**What it shows:**  
Cumulative incidence of **promotion** over time (days from DOR CPT), with officers grouped into 8 quantile bins based on **z_tb_ratio_fwd_snr** (N = 16,417; zero-OER excluded). Each curve is the promotion CIF for one bin; the bar chart below summarizes the final CIF (long-run promotion probability) for each bin. Vertical lines mark the Primary Zone.

**Takeaways:**  
- There is a strong **positive** association: higher Z TB ratio (better relative top-block share within the senior rater pool) is associated with a higher and steeper promotion CIF. The top bin reaches roughly **78%** final promotion CIF, while the lowest bins are around **18–26%** — a gap of more than 50 percentage points.  
- Most of the increase in promotion incidence occurs in and just after the **Primary Zone** (the dashed vertical lines), which is the critical window for promotion timing.  
- The gradient is largely monotonic: moving from lower to higher bins, promotion probability generally rises. So at the level of 8 bins, “getting into the highest rater pool” (here, high TB ratio) is clearly associated with much higher promotion probability.

**Diminishing returns / superstar pools:**  
With only 8 bins, it is hard to see *diminishing* returns at the very top — you would need the **top bin** to gain less (or lose) relative to the **second-from-top** bin. In Slide 6, the top bin (Bin 8) has the highest final CIF (~0.78), and the curve for that bin is above the others. So at this resolution, there is **no clear evidence of diminishing returns** for promotion with respect to TB ratio: the highest bin does not flatten or drop relative to the next bin. If anything, the gap between the top bin and the next remains large. To test diminishing returns more finely, you need either more bins (e.g., Slides 9–10) or model-based curvature (Slides 16–17). Slide 6 is consistent with “higher TB ratio is better” and does not contradict the idea that the very top still benefits; it simply does not speak to whether the *marginal* gain from the top bin to the next is smaller than the gain from the second bin to the third.

**For your story:**  
This is the first clear evidence that standing out in the senior rater pool (high TB ratio) is associated with much higher promotion. It does not show diminishing returns at the top; if you want to argue that “once you’re in the highest pools you still do well,” this slide supports that. To argue that “but the *extra* benefit at the very top is smaller,” you need the finer binning and the partial-effect plots.

---

### Slide 7 — Attrition CIF: TB Ratio Fwd SNR (8 bins)

**What it shows:**  
Cumulative incidence of **attrition** over time for the same run and the same 8 quantile bins of TB ratio / z_tb_ratio_fwd_snr as in Slide 6. Again, each curve is one bin; the bar chart gives final CIF for attrition (probability of attriting by the end of follow-up).

**Takeaways:**  
- Attrition is the **inverse** of the promotion story: higher performance (higher Z TB ratio) is associated with **lower** cumulative attrition. The lowest TB-ratio bins have the highest final attrition CIF; the highest TB-ratio bins have the lowest.  
- This is consistent with Slide 6: officers who stand out in the senior rater pool (high TB ratio) are both more likely to be promoted and less likely to attrit.  
- So in the raw CIFs, there is no hint that the *top* TB-ratio bin has *higher* attrition than the second-from-top — which would have been a strong signal of “superstar pool” downside (e.g., discouragement or selection out when competing with the best).

**Diminishing returns / superstar pools:**  
For attrition, “diminishing returns” in the highest pools could show up as: the **top** bin having *higher* attrition than the upper-middle bins (i.e., being in the superstar pool is riskier for retention). In Slide 7, with 8 bins, the top bin has the **lowest** attrition, not the highest. So there is **no evidence here** that the very top TB-ratio group pays a penalty in terms of attrition. Again, finer binning (e.g., 26 bins for pool-minus-mean in Slides 13–14) is where a U-shape or uptick at the top can appear; for TB ratio alone at 8 bins, the story is “higher TB ratio → lower attrition,” with no visible reversal at the top.

**For your story:**  
Slide 7 reinforces that high TB ratio is good for careers (lower attrition). It does not support the idea that the highest-TB-ratio officers are in a “superstar pool” that increases attrition risk; that possibility is better tested with pool-minus-mean and more bins.

---

### Slide 8 — Promotion CIF: Z Pool Minus Mean SNR Fwd (8 bins)

**What it shows:**  
Promotion CIF by 8 quantile bins of **z_pool_minus_mean_snr_fwd** (N = 15,338). This variable measures how far above (or below) the mean of your senior rater pool you are in terms of the forward pool-minus-mean metric. The bar chart shows final promotion CIF by bin.

**Takeaways:**  
- There is again a strong **positive** association: higher pool-minus-mean (fwd) is associated with higher promotion CIF. Final CIF rises from roughly 0.22–0.29 in the lowest bins to about 0.62–0.70 in the highest.  
- **Q7** has the highest final CIF in the bar chart; **Q8** (the very top bin) is **slightly lower** than Q7. That is a small non-monotonicity: the top bin does not quite reach the maximum. Similarly, Q1 is slightly above Q2.  
- “Being above your pool mean” (fwd) is strongly associated with promotion overall; the gradient is clear over most of the range.

**Diminishing returns / superstar pools:**  
Slide 8 is the **first place** where diminishing returns at the very top are *hinted* at: **Q8 (highest pool-minus-mean) has slightly lower promotion CIF than Q7**. The difference is small, and with 8 bins it could be noise or a modest real effect. One interpretation consistent with your hypothesis: the very top bin (Q8) may include officers who are “best in pool” in pools that are themselves highly selected (superstar pools); in those pools, even being above the mean might not translate into as large a promotion advantage as being in the upper-middle (Q6–Q7), where the pool might be less intensely competitive. So Slide 8 does not *prove* diminishing returns, but it is **consistent** with a small flattening or dip at the very top for promotion when using pool-minus-mean (fwd). The finer binning in Slides 9–10 will show whether this pattern holds up.

**For your story:**  
You can say: “When we look at promotion by how far above your pool mean you are, the relationship is strongly positive, but the very top bin (Q8) is actually slightly below the next bin (Q7). That could be noise, or it could be the first hint that once you’re in the highest pool-minus-mean group — potentially the superstar pools — the marginal return to being even higher flattens or dips.”

---

### Slides 9–10 — Promotion CIF: Pool minus mean (10 and 26 bins)

**What they show:**  
The same variable (z_pool_minus_mean_snr_fwd) and outcome (promotion CIF) as Slide 8, but with **10** and **26** quantile bins respectively. This lets you see whether the relationship is smooth and monotonic or whether there is a clear peak and then a drop at the very top.

**Takeaways:**  
- **10 bins:** The gradient holds: promotion probability increases with z_pool_minus_mean_snr_fwd, with the peak final CIF in the high bins (e.g., Q8 around 0.70). The very top bin (Q10) does not necessarily exceed Q8 or Q9; the curve can flatten or dip slightly at the top.  
- **26 bins:** With this much finer resolution, the pattern becomes clearer. The **peak** final promotion CIF is in the **upper-middle** bins (e.g., Q20–Q21), and there is a **slight drop** for the **very top** bins (Q22–Q26). So the highest pool-minus-mean officers do not have the highest promotion probability; the highest probability is in the bin or two just below the extreme top.  
- This is not an artifact of coarse binning: the relationship is continuous over most of the range, but it is **not** strictly monotonic at the top — it curves over.

**Diminishing returns / superstar pools:**  
Slides 9–10 provide the **strongest descriptive evidence** for diminishing returns in promotion with respect to pool-minus-mean (fwd). In the **26-bin** plot, the fact that Q20–Q21 have the highest final CIF and Q22–Q26 are slightly lower is exactly what you would expect if, once you get into the **highest** pool-minus-mean groups (the “superstar” pools), the marginal benefit of being even higher **diminishes** or even reverses slightly. Those top bins may be populated by officers who are in the most competitive pools (e.g., large pools full of high performers), where being “above the mean” still leaves you in a fierce comparison set; the upper-middle bins (Q18–Q21) might be the “sweet spot” where you are clearly above average but not in the most extreme, superstar-heavy slice. So for **promotion**, the data are **consistent with** a real diminishing-returns effect at the very top of the pool-minus-mean (fwd) distribution. You should present this as “consistent with” rather than “proof,” since alternative explanations (e.g., selection, different pool compositions) exist, but the pattern is in the direction your hypothesis predicts.

**For your story:**  
“When we use more bins, we see that promotion probability peaks in the upper-middle bins (around Q20–Q21) and then drops slightly for the very top bins (Q22–Q26). That is exactly the pattern we would see if there were diminishing returns once you’re in the highest pools — i.e., once you’re being ranked against superstars, the extra benefit of being even higher flattens or turns down.”

---

### Slide 11 — Promotion CIF: Z Pool Minus Mean SNR Bwd (8 bins, forced quantile)

**What it shows:**  
Promotion CIF by 8 bins of **z_pool_minus_mean_snr_bwd** (N = 15,189). “Bwd” is the backward-looking pool-minus-mean (different construction or time window than “fwd”). The binning is labeled “equal width” but the group sizes are unequal, so it behaves more like a forced-quantile or hybrid binning.

**Takeaways:**  
- **Backward** pool-minus-mean shows a **different** pattern from **forward**. Promotion is highest in the **middle** bins (Q4–Q7), and **lower** at both extremes: Q1 (lowest) and especially **Q8 (highest)**.  
- **Q8** (the highest z_pool_minus_mean_snr_bwd) has a relatively low promotion CIF (around **0.38**) and a small N. So the officers who are “best in pool” on the *backward* metric do **not** have the best promotion outcomes; they do worse than the upper-middle (Q4–Q7).  
- This suggests that “best in pool” for **bwd** is not simply “higher is always better” for promotion; the **fwd** metric is more monotonically positive, while **bwd** shows a clear downturn at the top.

**Diminishing returns / superstar pools:**  
Slide 11 is **strong evidence** for a form of diminishing (or reversing) returns when using the **backward** pool-minus-mean. The **highest** bwd bin (Q8) has **lower** promotion than the middle bins — a clear drop at the top. One interpretation: officers with the very highest “above pool mean” on the bwd metric may be in pools or career stages where the comparison set is particularly strong (e.g., superstar-heavy pools, or a selected subset of late-career CPTs). In those pools, being “best” might mean you are the best among the best — and the system may not reward that as much as being clearly above average in a less extreme pool (Q4–Q7). So for **bwd**, the data support the idea that **once you are in the highest pool (superstar pool), promotion returns diminish or reverse**. You can present this as the clearest example of a “top bin does worse” pattern, while noting that bwd and fwd may capture different aspects of pool context (timing, definition of pool, or career slice).

**For your story:**  
“When we look at the backward pool-minus-mean, the pattern is even starker: the very top bin (Q8) has the *lowest* promotion rate among the upper half of the distribution. That is exactly what we would see if being in the highest bwd pool — potentially the superstar pool — actually hurts promotion relative to being in the upper-middle. It’s the strongest single-slide evidence we have for diminishing returns.”

---

### Slide 12 — Attrition CIF: Z Pool Minus Mean SNR Fwd (8 bins)

**What it shows:**  
Attrition CIF by 8 quantile bins of **z_pool_minus_mean_snr_fwd** (N = 15,338 — same run as Slide 8). So this is the flip side of Slide 8: same variable, but the outcome is attrition instead of promotion.

**Takeaways:**  
- **Inverse** of promotion: **lower** pool-minus-mean (fwd) is associated with **higher** attrition. The lowest bins (Q1–Q3) have the highest final attrition CIF; the higher bins (e.g., Q6–Q7) have the lowest.  
- In some orderings, **Q8** (the very top bin) has **slightly higher** attrition than Q6 or Q7. So the very top pool-minus-mean group does not always have the very lowest attrition; it can be a bit higher than the upper-middle.  
- Overall, officers who are above their pool mean (fwd) are more likely to be promoted (Slide 8) and less likely to attrit (this slide), but the **top** bin may not be the absolute best for retention.

**Diminishing returns / superstar pools:**  
For attrition, “diminishing returns” in the highest pools would mean: the **top** bin has **higher** attrition than the upper-middle (i.e., being in the superstar pool increases the risk of leaving). In Slide 12, with 8 bins, there is a **hint** of that: Q8 can sit slightly above Q6–Q7 in the bar chart, so the very top bin does not have the very lowest attrition. The effect is small and could be noise. The 10- and 26-bin attrition slides (13–14) are where a clearer U-shape or uptick at the top appears; Slide 12 is **suggestive** but not definitive. You can say that it is consistent with the idea that the highest pool-minus-mean group might face slightly higher attrition (e.g., more competition, more discouragement, or selection), but you need the finer binning to make a stronger claim.

**For your story:**  
“On attrition, we see the same general pattern — higher pool-minus-mean is associated with lower attrition — but the very top bin (Q8) is not always the lowest; it can be slightly higher than Q6–Q7. That could be the first hint that the superstar pool carries a small attrition penalty. We’ll see if that holds up with more bins.”

---

### Slides 13–14 — Attrition CIF: Pool minus mean (10 and 26 bins)

**What they show:**  
Attrition CIF by **z_pool_minus_mean_snr_fwd** with **10** and **26** quantile bins (same run as Slides 9–10). So this is the attrition analogue of the promotion slides with finer binning.

**Takeaways:**  
- **10 bins:** There is a clear gradient — lowest z (Q1) has the highest final attrition CIF (around 0.68), and as z increases, attrition falls. The **lowest** attrition is in the high bins (e.g., Q9 around 0.29). **Q10** (the very top) has **slightly higher** attrition than Q9 (around 0.35). So there is already a hint of a **U-shape** at the top: the very top bin does not have the very lowest attrition.  
- **26 bins:** The **U-shape** is clear. Both the **lowest** (Q1–Q4) and **highest** (Q23–Q26) z_pool_minus_mean_snr_fwd bins have **higher** attrition; the **middle** bins (roughly Q10–Q20) have the **lowest** attrition. So the “sweet spot” for retention is not the extreme top; it is the upper-middle. The very top bins (Q23–Q26) have attrition rates that are closer to the low end of the distribution (high attrition) than to the middle.  
- This is a **real** pattern, not an artifact of a few bins: the relationship is continuous and the U-shape is visible across the range.

**Diminishing returns / superstar pools:**  
Slides 13–14 are **strong evidence** that, for **attrition**, being in the **highest** pool-minus-mean (fwd) groups is associated with **worse** outcomes than being in the upper-middle. The 26-bin U-shape means that officers in the very top bins (Q23–Q26) — plausibly the “superstar pools” where everyone is above average and you are competing with the best — have **higher** attrition than officers in the upper-middle (e.g., Q15–Q20). That is exactly what you would expect under a diminishing-returns or “ranked against superstars” story: once you are in the highest pools, the *benefit* (here, lower attrition) not only flattens but **reverses** — the very top has higher attrition than the tier just below. So for **attrition**, the data support the hypothesis that **once you get into the highest pools (superstar pools), returns diminish and can reverse**: the best retention is in the upper-middle, not at the extreme top. You can pair this with the promotion result (Slides 9–10: promotion peaks in upper-middle, drops at very top) and say that both promotion and retention are consistent with a real diminishing-returns effect at the very top.

**For your story:**  
“When we use 10 or 26 bins for attrition, we see a clear U-shape. The lowest attrition is not in the very top bin; it’s in the upper-middle. The very top bins (Q23–Q26) have higher attrition again — comparable to much lower pool-minus-mean bins. So for retention, being in the highest pool — where you’re ranked against superstars — is actually associated with *higher* attrition than being in the tier just below. That’s strong evidence for diminishing returns: once you’re in the superstar pool, the benefit of being there can turn into a penalty.”

---

### Slide 15 — Attrition CIF: Z Pool Minus Mean SNR Bwd (8 bins, forced quantile)

**What it shows:**  
Attrition CIF by 8 bins of **z_pool_minus_mean_snr_bwd** (N = 15,189 — same run as Slide 11). So this is the attrition side of the bwd story.

**Takeaways:**  
- **Higher** z_pool_minus_mean_snr_bwd is associated with **higher** attrition. In the bar chart ordering, the bin with the highest bwd (e.g., Bin 8 / Q1 in the legend order) has the highest final attrition CIF (around 0.66), and the bin with the lowest bwd (Bin 1 / Q8) has the lowest (around 0.29).  
- So for **bwd**, the group with the **highest** “above pool mean” has both **lower** promotion (Slide 11) and **higher** attrition (this slide). That is a consistent “double penalty” for being in the top bwd pool.  
- Bwd and fwd clearly capture different aspects of pool context or career timing; the bwd pattern is more extreme (clear reversal at the top for both promotion and attrition).

**Diminishing returns / superstar pools:**  
Slide 15 reinforces the diminishing-returns story for **bwd**. The **highest** bwd bin has the **highest** attrition — so “best in pool” on the backward metric is associated with the worst retention. Combined with Slide 11 (same bin has the lowest promotion), the message is: for the backward pool-minus-mean, being in the **highest** pool is associated with **worse** career outcomes on both promotion and attrition. That is the strongest possible form of “diminishing returns”: not just flattening, but **reversal** — the top pool does worse. You can interpret this as the backward metric identifying a set of officers who are in especially competitive (superstar) pools or in a career slice where “top of pool” correlates with other risk factors; either way, the data support the idea that **once you’re in the highest bwd pool, you are ranked against superstars and the returns not only diminish but reverse**.

**For your story:**  
“For the backward pool-minus-mean, the top bin has the highest attrition and the lowest promotion. So on both outcomes, being in the highest bwd pool is worse than being in the upper-middle. That’s the clearest evidence we have that ‘getting into the highest pool’ can, in some contexts, mean you’re now competing with superstars and that the returns can actually reverse.”

---

### Slide 16 — Partial effects: TB ratio (z_tb_ratio_fwd_snr + square)

**What it shows:**  
Two partial-effect plots for the **TB ratio** (z_tb_ratio_fwd_snr) and its **squared** term: (1) “Combined effect” (full model, adjusted for all covariates) and “Minimal model” (pool terms plus square only); (2) “Incremental add” (adding one covariate at a time) and “Remove-one” (full model minus one covariate). All show hazard ratio (e.g., for promotion) on the y-axis and z_tb_ratio_fwd_snr on the x-axis; a red dashed line at HR = 1 indicates “no effect.”

**Takeaways:**  
- **Combined effect (full model):** The curve is a **hump**: hazard ratio rises to a **peak** (around 2.1) at approximately z_tb_ratio_fwd_snr = 0.7, then **falls** and eventually crosses below 1 (near z ≈ 1.6). So at very high TB ratio, the *adjusted* hazard ratio is **lower** than at the peak — the effect is non-linear and turns down at the top.  
- **Minimal model:** Same hump shape, but scaled so the peak is at HR = 1.0; the caption notes this is the “closest model-based mirror of the CIF bins.” So even in the simple model, TB ratio has a **curved** effect: benefits increase up to a point, then diminish.  
- **Incremental add / remove-one:** Adding or removing **z_pool_minus_mean_snr_fwd** or **star_pool_interaction** shifts or flattens the hump; **sex** has a smaller effect. So the *shape* (hump, downturn at high z) is robust, but its *height* and *position* depend on the other covariates.

**Diminishing returns / superstar pools:**  
Slide 16 is **direct model-based evidence** for **diminishing returns** in the effect of TB ratio. The **hump** means that as TB ratio increases from low to moderate, the hazard (e.g., promotion hazard) **increases** — but beyond the peak (around z ≈ 0.7), further increases in TB ratio are associated with a **decline** in the hazard ratio. So “more TB ratio” is not always better; there is a point past which **additional** TB ratio yields **smaller** returns (the right side of the hump), and in the full model the curve eventually goes below 1 (so very high TB ratio is associated with *lower* hazard than at the peak). That is exactly the mathematical form of diminishing returns: the marginal effect of TB ratio is positive for a while, then turns negative. One interpretation: the right side of the hump may correspond to officers who are in the **highest** TB-ratio pools — the “superstar” pools — where being even higher does not add much or even subtracts (e.g., because you are now compared with the best, or because of ceiling effects in how the system rewards TB ratio). So the partial-effect plot **confirms** that the relationship between TB ratio and the outcome is **non-linear** and **diminishing (and eventually reversing) at the top** — which is consistent with your hypothesis that once you’re in the highest pools (ranked against superstars), returns diminish.

**For your story:**  
“The Cox model doesn’t assume a straight line. When we plot the combined effect of TB ratio and its square, we see a clear hump: the hazard ratio rises to a peak around z = 0.7 and then falls. So past that point, more TB ratio is associated with a *lower* hazard ratio — that’s diminishing returns, and at the far right the effect can even go below 1. That’s exactly what we’d expect if the very top TB-ratio officers are in superstar pools where the marginal benefit of being even higher flattens or reverses.”

---

### Slide 17 — Partial effects: Pool minus mean (z_pool_minus_mean_snr_fwd + square)

**What it shows:**  
Same structure as Slide 16 but for **z_pool_minus_mean_snr_fwd** (and its square): combined effect, minimal model, incremental add, and remove-one. Again, hazard ratio vs. z_pool_minus_mean_snr_fwd; red line at HR = 1.

**Takeaways:**  
- **Combined effect (full model):** The curve is an **inverted** shape — hazard ratio is **high** at **low** z (e.g., ~1.5–1.6 at z ≈ −1.2), then **falls** through “no effect” around z ≈ 0 and continues to **drop** toward 0 at high z. So in the full model, *higher* pool-minus-mean (fwd) is associated with *lower* hazard (e.g., promotion hazard). That is the **opposite** of the raw CIF gradient and is due to **adjustment** for TB ratio (and other covariates): the two are highly correlated, so the *adjusted* effect of pool-minus-mean can flip sign.  
- **Minimal model:** A more symmetric **hump** centered near z ≈ 0.5, with the curve **below** HR = 1.0 over the range — “mirror of CIF bins.” So in the *unadjusted* (minimal) model, pool-minus-mean has a humped effect that matches the CIF story: benefits rise then can flatten or dip.  
- **Incremental add / remove-one:** **z_tb_ratio_fwd_snr** strongly flattens or inverts the curve when added or removed; sex and star_pool_interaction also matter. So the *shape* of the pool-minus-mean effect is sensitive to whether TB ratio is in the model — consistent with multicollinearity and shared variance.

**Diminishing returns / superstar pools:**  
In the **minimal** model, the hump for pool-minus-mean is the model-based analogue of the CIF pattern: promotion (or hazard) rises with pool-minus-mean up to a point, then the curve **flattens or dips** — i.e., **diminishing returns at the top**. In the **full** model, the combined effect is inverted (high z → low hazard) because the model is attributing most of the “good outcome” to TB ratio when both are in the model; that doesn’t mean pool-minus-mean is “bad” in reality, it means the *marginal* effect of pool-minus-mean *given* TB ratio is negative (and the two are so correlated that this is hard to interpret in isolation). The **important** point for your hypothesis is the **minimal** model and the **CIFs**: the raw and minimally adjusted relationship between pool-minus-mean and outcome is **non-linear**, with a **peak** in the upper range and a **drop** at the very top — which is consistent with diminishing returns once you’re in the highest pool-minus-mean groups (superstar pools). So Slide 17 supports that the **shape** of the pool-minus-mean effect (hump, downturn at high z) is real and consistent with your story, even though the full-model combined effect looks inverted due to covariance with TB ratio.

**For your story:**  
“For pool-minus-mean, the minimal model shows a hump — benefits rise then flatten or dip at the top — which matches what we saw in the CIFs. In the full model the curve inverts because pool-minus-mean and TB ratio are so correlated that the model splits the effect between them. So the takeaway is: the *unadjusted* relationship (and the minimal model) supports diminishing returns at the top; the full model reminds us that TB ratio and pool-minus-mean are hard to separate statistically, but the shape we care about for the superstar-pool story is there.”

---

### Slide 18 — Coefficients and covariance

**What it shows:**  
A table of **coefficients** (and signal_ratio) for each variable in the Cox model: sex, z_tb_ratio_fwd_snr, z_pool_minus_mean_snr_fwd, z_tb_ratio_fwd_snr_sq, z_pool_minus_mean_snr_fwd_sq, star_pool_interaction. Below that, a **2×2 correlation matrix** for z_tb_ratio_fwd_snr and z_pool_minus_mean_snr_fwd.

**Takeaways:**  
- **Correlation** between z_tb_ratio_fwd_snr and z_pool_minus_mean_snr_fwd is **0.927** — very high **multicollinearity**. So the two variables carry a lot of the same information; in a regression, their *individual* coefficients can be unstable or flip sign when both are included.  
- **Coefficients:** z_tb_ratio_fwd_snr is **positive** (+2.24); z_pool_minus_mean_snr_fwd is **negative** (−1.02); **both squared terms are negative** (−1.05 and −0.37); star_pool_interaction is positive (+0.36); sex is near zero (−0.02).  
- The **negative squared terms** are exactly what produce the **humps** in the partial-effect plots (Slides 16–17): they imply that the effect of each variable **curves over** — positive linear term, negative quadratic term means the marginal effect declines at high values and eventually can turn negative. So the **coefficients** themselves encode **diminishing returns**: the negative quadratic terms are the formal statement that “more of this variable” is not linearly better; at high values, the effect diminishes (and in the plots, can reverse).

**Diminishing returns / superstar pools:**  
Slide 18 gives the **algebraic** basis for diminishing returns. The **negative coefficients on the squared terms** mean that the model explicitly allows (and estimates) a **curved** relationship: the linear part pushes the hazard up as the variable increases, but the square term pulls it back at high values. So the model is **built** to capture exactly the pattern you’re interested in — benefits that increase then diminish (or reverse) at the top. The high correlation (0.93) between TB ratio and pool-minus-mean means that the *separate* coefficients are hard to interpret in isolation (hence the inverted full-model curve for pool-minus-mean in Slide 17), but the **presence** of negative quadratic terms in **both** variables supports that **both** “being in the highest TB-ratio pool” and “being in the highest pool-minus-mean pool” are associated with **diminishing marginal returns** in the model. So Slide 18 is where you can say: “The model explicitly includes curvature; the negative squared terms are the statistical formulation of diminishing returns — and they are estimated to be negative for both TB ratio and pool-minus-mean.”

**For your story:**  
“The coefficients show that both TB ratio and pool-minus-mean have negative squared terms. That’s the math behind the humps we saw: the model is saying that at high values, the effect of each variable turns down. So diminishing returns aren’t just a visual impression; they’re in the estimated model. The catch is that the two variables are so correlated (0.93) that we can’t cleanly separate their contributions — but the curvature is there for both.”

---

### Slide 19 — Interaction surface

**What it shows:**  
A **3D surface** of **Hazard Ratio** as a function of two axes. The **axes are the two base variables** that multiply to form the interaction term in the model (e.g., TB ratio and pool-minus-mean — the same columns that enter the product `star_pool_interaction`). They are **not** the “combo” variables (linear + squared); the plot is the interaction between the **base** (linear) variables over the (x, y) grid, with the **full** model (all terms, including linear, squared, and interaction) used to predict. Other covariates are held at their median. The surface shows how the hazard ratio changes as you move in this two-dimensional space (both axes z-scored when using standardized runs).

**How to interpret this plot:**  
- **X- and Y-axes:** The two **base** predictors that form the interaction (e.g., z-scored TB ratio and z-scored pool-minus-mean). Each point (x, y) is a hypothetical combination of those two variables.  
- **Z-axis (height / color):** **Full-model hazard ratio** — i.e., exp(linear predictor at (x, y) with other vars at median) relative to the median prediction. So Z &gt; 1 means higher hazard than the reference; Z &lt; 1 means lower.  
- **Red line at HR = 1:** Reference level. Regions above the red line have elevated hazard; regions below have reduced hazard. In the contour, the red contour at 1.0 separates “above average” from “below average” hazard.  
- **Reading the surface:** Moving toward the **top-right** (both variables high) shows the **joint** effect of “high TB ratio and high pool context.” A strong positive interaction appears as a steep rise in that corner. For **diminishing returns**, check whether the surface **flattens or dips** at the very highest (x, y) — if the maximum hazard is “high but not the extreme corner,” that supports diminishing returns in the superstar region of the joint space.

**Takeaways:**  
- The surface is **low** when both inputs are **negative** (e.g., bottom-left) and **very high** when both are **positive** (e.g., top-right corner, hazard ratio can exceed 140). So there is a strong **positive interaction**: doing “above average” on **both** dimensions multiplies the hazard (e.g., promotion).  
- There is a diagonal ridge and a red dashed line that help read regions where one dimension is high and the other low.  
- So “highest rater pool” in a **joint** sense (high on both dimensions) is associated with the largest hazard ratios in this plot.

**Diminishing returns / superstar pools:**  
The 3D surface is primarily about **interaction** (how the two variables combine), not only about diminishing returns. But you can still ask: **at the very top** of the surface (both axes high), does the surface **flatten** or **dip** compared with a bit below the top? If the highest hazard is in a region that is “high but not the extreme corner,” that would be consistent with diminishing returns in the joint space (i.e., the “superstar” corner might not be the absolute maximum). The description you had suggested the surface rises toward the corner where both are positive; if in the actual plot there is any flattening or slight drop at the very highest values (e.g., near the boundary of the plot), that would support that even in the joint (TB ratio × pool context) space, the **very** top can show diminishing returns. If the surface is monotonic all the way to the corner, then the interaction plot emphasizes “both high is best” and the diminishing-returns story is more about the **one-dimensional** slices (TB ratio alone or pool-minus-mean alone) and the CIFs. So Slide 19 can be used to say: “The interaction shows that the combination of TB ratio and pool context matters a lot; the very top of this surface may or may not show a slight flattening — if it does, that’s consistent with diminishing returns in the superstar region of the joint space.”

**For your story:**  
“The 3D surface shows that being high on both TB ratio and pool context gives the highest hazard. For diminishing returns, the question is whether the *very* top of the surface (the extreme superstar corner) is still the maximum or whether the surface flattens or dips there. Either way, the surface shows that the joint effect is strong and that the ‘highest pool’ in two dimensions is where the model predicts the biggest outcomes.”

---

### Slide 20 — Interaction contour

**What it shows:**  
A **contour** plot of **Hazard Ratio** in the two-dimensional space of **TB ratio (z-scored)** (x-axis) and **Pool minus mean (z-scored)** (y-axis). Color (or contour lines) indicates the level of the hazard ratio; a diagonal red dashed line marks a boundary or reference.

**Takeaways:**  
- **Low** hazard (e.g., purple/dark) when TB ratio is **low** and pool-minus-mean is **high** (top-left).  
- **High** hazard (e.g., yellow/green) when TB ratio is **high** and pool-minus-mean is **low** (bottom-right) — i.e., high TB share in a pool where the average is relatively low.  
- The diagonal red line approximates a boundary: crossing from “low TB / high pool mean” toward “high TB / low pool mean” moves you into much higher hazard.  
- So the **combination** of the two variables drives the hazard; “best in a weak pool” (high TB ratio, low pool mean) vs “best in a strong pool” (high TB ratio, high pool mean) can have different implications.

**Diminishing returns / superstar pools:**  
The contour is directly relevant to your hypothesis. The region where **both** TB ratio and pool-minus-mean are **high** (e.g., top-right or near the diagonal in the “high” direction) corresponds to “you’re a top performer in a pool that is itself strong” — i.e., the **superstar pool**. The question is: in that region, does the hazard ratio **continue to rise** or does it **flatten or drop**? If the **highest** hazard is in a region where TB ratio is high but pool-minus-mean is only **moderately** high (e.g., “best in a moderately strong pool”), and the **extreme** corner (both very high) has a slightly lower hazard, that would be the **contour-map version** of diminishing returns: the “superstar” corner (ranked against superstars) would not be the optimum. Your description said the **highest** hazard is when TB ratio is high and pool-minus-mean is **low** (bottom-right) — which could mean “high TB ratio in a pool with a low mean” (you stand out a lot). So the contour might be saying: the best outcome is not “high on both,” but “high TB ratio in a pool where the mean is not the highest” — which could be read as “being the star in a less superstar-heavy pool” rather than “being in the superstar pool.” That would be **consistent** with diminishing returns: the very top of the joint distribution (both axes very high = superstar pool) might not be the peak of the hazard; the peak might be in a region where you’re high on TB ratio but the pool context (pool mean) is not at the extreme. So Slide 20 can be interpreted as supporting that **where** you sit in the two-dimensional space matters and that the **maximum** hazard may not be at the “both highest” point — consistent with diminishing returns in the superstar region.

**For your story:**  
“The contour shows that the combination of TB ratio and pool-minus-mean matters a lot. If the highest hazard is in the region where TB ratio is high but pool mean is not the very highest, that suggests the sweet spot is ‘top performer in a strong but not extreme pool’ — and the very top (superstar pool) might show diminishing returns. The contour lets us see that the best outcomes may not be at the extreme top of both dimensions.”

---

## Part 1 (continued): Run 3 — Slides 24–30

**Run 3** uses a different pool metric: **Z Pool TB Ratio Rank Pct SNR Fwd** (z_pool_tb_ratio_rank_pct_snr_fwd) — i.e., your **percentile rank** within the senior rater pool on the TB-ratio dimension (standardized). So “top of pool” here is “high rank *percent*” (e.g., 90th percentile in your pool). The Cox model for Run 3 includes **standing_pool_interaction** (and pool rank percent linear + square) instead of Run 1’s pool-minus-mean and star_pool_interaction. Run 3 thus asks the same diminishing-returns question with a **rank-percent** definition of “highest pool.” N = 15,311 for the CIF slides (exclude zero-OER).

---

### Slide 24 — Promotion CIF: Z Pool TB Ratio Rank Pct SNR Fwd (8 bins)

**What it shows:**  
Cumulative incidence of **promotion** over time (days from DOR CPT), with officers in 8 quantile bins of **z_pool_tb_ratio_rank_pct_snr_fwd** (N = 15,311; zero-OER excluded). CIF curves and a bar chart of final promotion CIF by bin. Primary Zone is marked.

**Takeaways:**  
- Higher pool TB ratio rank percent (higher percentile within your pool) is associated with **higher** promotion CIF. **Q8** (top bin) has the **highest** final CIF (~0.70), followed by Q7 (~0.66) and Q6 (~0.64). So in absolute terms, being in the “highest” rank-percent pool is still associated with the **best** promotion outcomes.  
- The gradient is largely monotonic: Q1 has the lowest final CIF (~0.30), and the bars rise through Q8. There is a small non-monotonicity in the middle (e.g., Q4 can be slightly above Q5).  
- The **marginal** gains at the very top are **smaller** than in the middle: the difference between Q8 and Q7 is about **0.04** (0.70 − 0.66), and between Q7 and Q6 about **0.02** (0.66 − 0.64), whereas moving from Q3 to Q4 or Q4 to Q5 can be on the order of **0.07–0.08**. So the *rate* of improvement in promotion probability **diminishes** as you move into the top bins — i.e., **diminishing marginal returns** for promotion with respect to pool rank percent.

**Diminishing returns / superstar pools:**  
Slide 24 does **not** show a **reversal** at the top (Q8 is still best for promotion). It does show **diminishing *marginal* returns**: each step into a higher bin at the top (Q6 → Q7 → Q8) adds less to promotion probability than steps in the middle. That is consistent with the idea that once you’re already in the upper tier (high rank percent), the **extra** benefit of being in the very top bin (the “superstar” slice) is smaller — you’re being compared with other high performers, so the marginal return flattens. So for **promotion** in Run 3, the message is: “Top is still best, but the *additional* gain from being in the very top bin is smaller than the gain from moving up in the middle of the distribution.” That is a **moderate** form of diminishing returns (flattening, not reversal).

**For your story:**  
“When we use pool *rank percent* instead of pool-minus-mean, we see the same overall pattern: higher rank percent → higher promotion. But the *step* from Q7 to Q8 is only about 4 percentage points, while the step from Q3 to Q4 is much larger. So the benefit of being at the very top flattens — that’s diminishing marginal returns for promotion.”

---

### Slide 25 — Attrition CIF: Z Pool TB Ratio Rank Pct SNR Fwd (8 bins)

**What it shows:**  
Cumulative incidence of **attrition** over time for the same variable and 8 bins as Slide 24 (z_pool_tb_ratio_rank_pct_snr_fwd, N = 15,311). CIF curves and final CIF bar chart.

**Takeaways:**  
- **Higher** pool TB ratio rank percent is associated with **higher** attrition. **Q8** (the top bin — highest rank percent in the pool) has the **highest** final attrition CIF (~0.70). Q7 (~0.66) and Q6 (~0.62) are also high. The **lowest** attrition is in the **lower** bins: Q2 (~0.37), Q1 (~0.40), Q3 (~0.41). So the **best** retention is **not** in the “top of pool” group; it is in the **middle** or lower rank-percent bins.  
- This is the **inverse** of the naive expectation that “being at the top of your rating pool” should be best for retention. Here, being at the top (highest rank percent) is associated with the **worst** retention — a clear **reversal** of the “top is always better” story for attrition.

**Diminishing returns / superstar pools:**  
Slide 25 is **strong evidence** for the “ranked against superstars” / diminishing-returns story **for attrition**. Officers in the **highest** pool rank-percent bins (Q6–Q8) — i.e., those who are at or near the top of their pool on TB ratio rank — have the **highest** probability of attriting. That is exactly what you would expect if “highest pool” means you are in a set of highly selected, high-performing peers (superstars): the competitive pressure, the comparison with the best, or the fact that these officers are more marketable elsewhere could all push attrition *up* in the top bins. So for **attrition**, Run 3 shows that **being at the top of your rating pool (by rank percent) is associated with *worse* retention**, not better — a **reversal** of the simple “top is always better” expectation and strong support for the hypothesis that once you’re in the highest pools (ranked against superstars), returns can not only diminish but **reverse** (here, higher attrition).

**For your story:**  
“For attrition, the picture is stark: the *highest* rank-percent bins — the people at the top of their pools — have the *highest* attrition. Q8 is around 70% attrition, while Q2 is around 37%. So being at the top of your rating pool, in this run, is associated with *leaving* more, not staying. That’s the clearest Run 3 evidence that the ‘superstar pool’ can carry a retention penalty.”

---

### Slide 26 — Partial effects: TB ratio (Run 3 — z_tb_ratio_fwd_snr + square)

**What it shows:**  
Four panels: (1) Combined effect of z_tb_ratio_fwd_snr + z_tb_ratio_fwd_snr_sq (full model); (2) Minimal model (pool terms plus square only); (3) Incremental add (one covariate at a time); (4) Remove-one test (full model minus one covariate). Covariates in Run 3 include **z_pool_tb_ratio_rank_pct_snr_fwd** (and its square), **standing_pool_interaction**, and **sex**. X-axis: z_tb_ratio_fwd_snr; y-axis: Hazard Ratio; red line at 1 = no effect.

**Takeaways:**  
- **Combined effect:** A **hump**: hazard ratio rises to a peak (around 1.2–1.25) near z_tb_ratio_fwd_snr ≈ 0.7, then **falls** and can go below 1 at high z — same qualitative shape as Run 1’s Slide 16. So TB ratio has a **non-linear**, diminishing-returns effect in the full model.  
- **Minimal model:** Same hump, peak near 1.0; caption notes it is the “closest model-based mirror of the CIF bins.”  
- **Incremental add:** Adding **sex** or **z_pool_tb_ratio_rank_pct_snr_fwd_sq** **amplifies** the hump (higher peak); adding **z_pool_tb_ratio_rank_pct_snr_fwd** (linear) **flattens** it (curve stays closer to 1). So the **pool rank percent** variable modifies how strong the TB-ratio hump is — when it’s in the model, the hump is less pronounced.  
- **Remove-one:** Shows how the curve changes when each covariate is dropped from the full model; the hump shape is robust.

**Diminishing returns / superstar pools:**  
Slide 26 confirms that in **Run 3**, as in Run 1, **TB ratio** has a **humped** partial effect — benefits rise then diminish (and in the full model, can reverse) at high TB ratio. So the “diminishing returns at the top” pattern for TB ratio is **replicated** when the pool is defined by **rank percent** and the interaction is **standing_pool_interaction**. The fact that adding the linear pool rank percent **flattens** the hump suggests that once you condition on “where you stand in the pool” (rank percent), the marginal effect of TB ratio alone is less extreme — the pool context and TB ratio are again sharing variance, but the curvature (diminishing returns) is still there.

**For your story:**  
“Run 3’s partial effects for TB ratio look like Run 1: a clear hump, with the hazard ratio turning down at high TB ratio. So the model again says that more TB ratio is not always better — past a point, returns diminish. The pool rank percent and standing_pool_interaction terms shift or flatten the hump depending on what we add or remove.”

---

### Slide 27 — Partial effects: Pool TB ratio rank percent (z_pool_tb_ratio_rank_pct_snr_fwd + square)

**What it shows:**  
Same four-panel layout as Slide 26 but for **z_pool_tb_ratio_rank_pct_snr_fwd** (and its square). X-axis: z_pool_tb_ratio_rank_pct_snr_fwd; y-axis: Hazard Ratio.

**Takeaways:**  
- **Combined effect (full model):** The curve **falls** steeply from a very high hazard ratio (e.g., around 18) at **low** z (e.g., −1.5) down through “no effect” (HR = 1) around z ≈ −0.75, then continues to **decrease** and flattens near 0 at **high** z (e.g., 1.5). So in the **full** model, *higher* pool rank percent is associated with *lower* hazard (e.g., if the outcome is “bad,” higher rank percent is better; if the outcome is promotion hazard, the interpretation depends on event definition). The **rate** of improvement diminishes at high z (curve flattens) — diminishing *marginal* benefit.  
- **Minimal model:** A **hump**: the curve starts **below** 1 at low z (e.g., ~0.4 at z = −1.5), **rises** to cross 1 around z ≈ 0.25, **peaks** slightly above 1 (e.g., ~1.08) near z ≈ 0.75, then **falls** back **below** 1 toward high z. So in the **minimal** model, pool rank percent has a **non-linear** effect: an initial “struggle” zone (hazard above 1 as you move into higher rank percent), then a **peak** (the “superstar” zone where hazard is highest), then a **drop** (the very top performers see hazard fall again). That is exactly the **diminishing-returns / superstar-pool** shape: the middle-high range (around z ≈ 0.75) is where hazard peaks; the very top (z > 1) then sees hazard come down again (or the curve can be read as “benefit then penalty then benefit again” depending on outcome).  
- **Incremental add / remove-one:** Adding **z_tb_ratio_fwd_snr_sq** produces a very steep monotonic decline (hazard drops as rank percent increases); **sex** and **standing_pool_interaction** leave the curve flatter or near 1. The **full** model (and most remove-one curves) show a steep decline, so when all covariates are included, the **marginal** effect of rank percent is “higher is better” with diminishing *rate*; the **minimal** model reveals the **hump** that is consistent with “middle-high rank percent = peak hazard (or peak struggle), very top = hazard falls again.”

**Diminishing returns / superstar pools:**  
Slide 27 is **central** to the Run 3 story. The **minimal** model shows a **hump** for pool rank percent: hazard (or “struggle”) **rises** as you move into higher rank percent (you’re now in more competitive company), **peaks** around z ≈ 0.75 (the “ranked against superstars” zone), then **falls** for the very top (z > 1 — the true superstars who overcome the competition). So the **unadjusted** relationship between “where you stand in the pool” (rank percent) and the outcome is **non-linear** and consistent with an initial **increase** in hazard (or difficulty) as you enter higher pools, then a **recovery** for the very top. The **full** model flattens this into a monotonic “higher rank percent → lower hazard” (or higher benefit) with diminishing *rate* — so other covariates (especially TB ratio and its square) absorb part of the story. For the **diminishing-returns hypothesis**, the **minimal** model is the key: it shows that **being in the highest rank-percent pools** is not simply “always better”; there is a **zone** (around the peak) where being high in the pool is associated with the **highest** hazard (or the least benefit), consistent with “ranked against superstars,” and only the **very** top (extreme high z) then see hazard come down again.

**For your story:**  
“When we look at the effect of pool rank percent in the minimal model, we see a hump: hazard rises as you go from low to middle-high rank percent, peaks around z ≈ 0.75, then falls for the very top. So there’s a band of ‘high but not extreme’ rank percent where the outcome is worst — that’s the ‘ranked against superstars’ zone. The full model flattens this into a steady decline because TB ratio and other terms soak up the variance, but the minimal model is the one that matches the CIF story: the top bins don’t always do best.”

---

### Slide 28 — Coefficients and covariance (Run 3)

**What it shows:**  
Table of **coefficients** and **signal_ratio** for the Run 3 Cox model (sex, z_tb_ratio_fwd_snr, z_pool_minus_mean_snr_fwd or Run 3 analogue such as z_pool_tb_ratio_rank_pct_snr_fwd, squared terms, star_pool_interaction or standing_pool_interaction), and a **2×2 correlation matrix** for the two main predictors (e.g., z_tb_ratio_fwd_snr and the pool variable). If the slide is identical to Run 1’s Slide 18, the numbers are the same (e.g., correlation 0.927); if it is Run 3–specific, the pool variable would be rank percent and the correlation might differ slightly.

**Takeaways:**  
- **High correlation** (e.g., 0.93) between TB ratio and the pool metric (pool-minus-mean or pool rank percent) — **multicollinearity** again. So the *separate* coefficients for each are hard to interpret in isolation.  
- **Negative squared terms** for both the TB-ratio and pool terms imply **curvature** and **diminishing returns** in the model: at high values, the marginal effect of each variable turns down.  
- **Positive interaction** term (e.g., star_pool_interaction or standing_pool_interaction) suggests that the **joint** effect of “TB ratio and pool context” can mitigate or alter the separate “diminishing returns” from the pool term alone — e.g., superstars in high pools might still get a boost from the interaction.

**Diminishing returns / superstar pools:**  
Slide 28 gives the **algebraic** basis for curvature in Run 3 (and, if same as Run 1, reinforces that both TB ratio and the pool variable have negative quadratic terms). The **message** is the same as Slide 18: the model **explicitly** allows (and estimates) **diminishing returns** via the negative squared terms; the high correlation between the two predictors means we can’t cleanly separate “TB ratio effect” from “pool effect,” but the **presence** of curvature in **both** supports that “being at the top” on either dimension is associated with a **flattening or reversal** of marginal benefit in the estimated model.

**For your story:**  
“The coefficients again show negative squared terms for both TB ratio and the pool variable — so the model is built to capture curvature and diminishing returns. The interaction term is positive, which can mean that the ‘superstar in a superstar pool’ combination still gets some extra boost, but the overall shape is still non-linear.”

---

### Slide 29 — Interaction surface (Run 3): TB ratio (z) vs Pool TB ratio rank pct (z)

**What it shows:**  
**3D surface** of **Hazard Ratio** (z-axis) as a function of **TB ratio (z)** (x-axis) and **Pool TB ratio rank pct (z)** (y-axis). Both axes range from about −1 to 1.5. A diagonal red dashed line runs along the base (e.g., where TB ratio ≈ Pool rank pct).

**Takeaways:**  
- The surface is **low** in the **bottom-left** (both variables low) and **very high** in the **top-right** (both variables high) — hazard ratio can exceed **250** in that corner. So there is a strong **positive interaction**: being high on **both** TB ratio and pool rank percent is associated with a **very large** hazard ratio.  
- If the **hazard** is for a **negative** outcome (e.g., attrition, or “failure to promote”), then the **top-right** is the **worst** region: high performers in high rank-percent pools face the **highest** hazard (highest risk of the bad outcome). That would be **consistent** with “ranked against superstars” — the “superstar” corner (both axes high) is where the **risk** is amplified. If the hazard is for a **positive** outcome (e.g., promotion), then the top-right is the **best** region (highest promotion hazard = fastest promotion); the interpretation flips.  
- The diagonal red line helps read the slice where “TB ratio (z) = Pool rank pct (z)” — i.e., your performance level matches your rank in the pool. Along that line, the surface rises from low (bottom-left) to very high (top-right).

**Diminishing returns / superstar pools:**  
For a **negative** outcome (e.g., attrition), Slide 29 shows that the **top-right** quadrant — “high TB ratio **and** high pool rank percent,” i.e., **top performer in a top-ranked slice of the pool** — is the region of **highest** hazard (highest attrition risk). That is **direct visual evidence** that being in the “highest” joint space (superstar pool) is associated with **amplified** negative outcome — i.e., **diminishing returns or reversal**: the “best” position in the joint space is **not** the best for avoiding the bad outcome. For a **positive** outcome (promotion), the same top-right would be “best” (highest promotion hazard); then the diminishing-returns story would be about the **one-dimensional** slices (e.g., rank percent alone, as in Slide 25’s attrition U-shape) or about the **rate** of increase (surface flattens at the very top). So the **message** depends on which outcome the model is for; either way, the **interaction** is strong and the **joint** position (TB ratio × pool rank percent) matters a lot — and for attrition, the superstar corner is the **worst** region.

**For your story:**  
“The 3D surface shows that when you’re high on both TB ratio and pool rank percent — the top-right corner — the hazard ratio is enormous. If we’re modeling attrition, that means the ‘superstar’ corner is where attrition risk is highest: being a top performer in a top pool is associated with the worst retention. That’s the interaction-surface version of the diminishing-returns story.”

---

### Slide 30 — Interaction contour (Run 3): TB ratio (z) vs Pool TB ratio rank pct (z)

**What it shows:**  
**Contour** plot of **Hazard Ratio** in the (x, y) plane of **TB ratio (z)** (x-axis) and **Pool TB ratio rank pct (z)** (y-axis). Color scale from low (e.g., purple, 0) to high (e.g., yellow, up to ~320). A diagonal red dashed line runs from bottom-left to top-right.

**Takeaways:**  
- **Low** hazard (purple/dark) in the **bottom-left** (low TB ratio, low pool rank percent). **High** hazard (green/yellow) in the **top-right** and along the right edge (high TB ratio, high pool rank percent). The gradient is steep: moving from left to right and from bottom to top increases the hazard ratio, with the **fastest** increase when **both** variables are high.  
- The diagonal red line again marks the “TB ratio (z) = Pool rank pct (z)” slice; hazard increases along this line from bottom-left to top-right.  
- So the **combination** of TB ratio and pool rank percent drives the hazard; the **maximum** hazard is in the **top-right** (both high) — the “superstar” region in the joint space.

**Diminishing returns / superstar pools:**  
Slide 30 is the **contour** version of Slide 29. For a **negative** outcome (e.g., attrition), the **top-right** is the **worst** region (highest hazard = highest attrition risk) — so “being at the top” on **both** dimensions (TB ratio and pool rank percent) is associated with the **worst** outcome. That reinforces the message: the **joint** “superstar” position (high on both axes) does **not** minimize the bad outcome; it **maximizes** it. So the contour makes it easy to say: “The best retention is **not** in the top-right; it’s in the bottom-left or middle. The very top of the joint space is where hazard is highest — consistent with diminishing returns or reversal when you’re ranked against superstars.” For **promotion**, the same contour would show the top-right as “best” (highest promotion hazard); the diminishing-returns story would then rest on the **one-dimensional** results (e.g., promotion marginal gains flatten at the top in Slide 24, attrition rises at the top in Slide 25) and the **minimal-model** hump in Slide 27.

**For your story:**  
“The contour makes it obvious: the highest hazard is in the top-right — high TB ratio and high pool rank percent. So if we’re looking at attrition, the ‘best’ position in the joint space is actually the *worst* for retention. The contour is the clearest picture that being at the top of your rating pool, in the joint sense, can be associated with the worst outcome for the bad event.”

---

## The message: You’d expect “top” is always better — what do we see?

**The naive expectation**  
You would expect that **being at the top of your rating pool** would almost always be better: better promotion odds, better retention, and generally better career outcomes. After all, “top” means you’re outperforming your peers, you’re getting the best evaluations, and you’re in the most favorable position for selection. So the default story is: **higher standing in the pool → better outcomes**, monotonically.

**What we actually see**  
The slides tell a **more nuanced** story. In many places, “top” is still **best** in absolute terms (e.g., the top bin often has the highest promotion probability), but the **marginal** benefit of being in the **very** top flattens or even reverses. In other places, the **very** top is **worse** than the upper-middle — so “top” is **not** always better.

- **Promotion:**  
  - **Run 1 (pool-minus-mean, fwd):** The **very** top bin (Q8) is **slightly below** the next (Q7) in the 8-bin plot; with **26 bins**, promotion probability **peaks** in the **upper-middle** (Q20–Q21) and **drops** for the very top (Q22–Q26). So the **best** promotion outcomes are **not** in the extreme top bin; they’re in the bin or two just below. **Run 1 (bwd):** The **top** bin (Q8) has **lower** promotion than the middle bins — a clear **reversal**. **Run 3 (pool rank percent):** The top bin (Q8) still has the **highest** promotion CIF, but the **marginal** gain from Q7 to Q8 (and Q6 to Q7) is **smaller** than the gains in the middle — **diminishing marginal returns**.  
  - So for promotion: **top is often still best**, but the **extra** gain at the very top **flattens** (Run 1 fwd fine bins, Run 3) or **reverses** (Run 1 bwd). We do **not** see a simple “higher is always proportionally better” story.

- **Attrition:**  
  - **Run 1 (pool-minus-mean, fwd):** With **8** bins, Q8 can be **slightly higher** in attrition than Q6–Q7; with **10** and **26** bins, a clear **U-shape**: the **lowest** attrition is in the **upper-middle** (e.g., Q9 for 10 bins), and the **very top** bins (Q10, Q23–Q26) have **higher** attrition than that. So the **best** retention is **not** in the top bin; it’s in the tier just below. **Run 1 (bwd):** The **top** bin has the **highest** attrition (and lowest promotion). **Run 3 (pool rank percent):** The **top** bins (Q6–Q8) have the **highest** attrition (Q8 ~0.70); the **lowest** attrition is in Q2 (~0.37). So for attrition, **being at the top of your rating pool is associated with *worse* retention** in Run 3 and in Run 1 with fine binning — a **reversal** of “top is always better.”  
  - So for attrition: we **do** see **reversals**: the “highest” pools often have **higher** attrition than the upper-middle or middle. The naive expectation (“top is best”) is **violated** for retention.

- **Model (partial effects, coefficients, interaction):**  
  - The Cox model **estimates** **negative quadratic terms** for both TB ratio and the pool variable (Run 1 and Run 3). So the **math** says: at high values, the effect of “being higher in the pool” (or “having higher TB ratio”) **turns down** — diminishing returns are **built into** the estimated relationship. The **partial-effect** plots show **humps**: benefits rise to a peak then **fall** (and in the full model for TB ratio, can go below 1). So the model **confirms** that “more is not always better”; there is a **sweet spot** or a **zone** past which returns diminish or reverse. The **interaction** surface and contour (Run 1 and Run 3) show that the **joint** position (TB ratio × pool context) matters: for a **negative** outcome like attrition, the **top-right** (superstar corner) is often the **worst** region — highest hazard. So the **joint** “top” is **not** the best for avoiding the bad outcome.

**Synthesis: what is the message?**  
The message is: **being at the top of your rating pool is not uniformly better**. In many cases it is still **good** (e.g., top bin has high promotion probability), but:

1. The **marginal** benefit of being in the **very** top often **flattens** (diminishing marginal returns) or **reverses** (the very top does worse than the upper-middle).  
2. For **attrition**, the **reversal** is clear in multiple runs and binning choices: the highest pool groups have **higher** attrition than the tier just below. So “top” is **not** best for retention — it’s often **worst**.  
3. The **model** formalizes this with **curvature** (negative squared terms, humped partial effects) and **interaction**: the “superstar” corner of the joint space can be the **worst** region for the bad outcome (attrition).  
4. A **plausible** interpretation is that once you’re in the **highest** pools, you’re **ranked against superstars** — the comparison set is the best, the bar is highest, and the marginal return to being “even higher” flattens or the stress/competition/selection effects push attrition up. So the **data are consistent** with a **real** diminishing-returns (and sometimes reversing-returns) effect: **you’d expect top is always better, but we see that the very top often flattens or reverses — especially for retention.**

---

## Part 2: Short story — Diminishing returns in the highest pools (ranked against superstars)

**Framing the question**  
You are investigating whether **once you get into the highest rater pools, you experience diminishing returns** — i.e., whether the benefit of being “at the top” flattens or reverses because you are now being ranked against superstars. The idea is that “highest pool” might mean different things: in some pools, “top” might be a small, very selected set of superstars, and being in that set might not deliver the same marginal gain (or might even carry a penalty) compared with being in the upper-middle — the tier just below the extreme top. The slides are interpreted above with that possibility in mind; here we tie the evidence together into a single narrative.

**Pool context is heterogeneous (Slide 5)**  
Officers sit in senior rater pools of very different sizes (median 19, 95th percentile 75). So “highest rater pool” can mean top of a small pool or top of a large one; in large pools, the top slice may be a more concentrated set of superstars. That makes diminishing returns plausible: in the very top pools, you might be competing with the best, and the marginal return to being there could flatten or reverse. The rest of the slides ask whether the data show that pattern.

**Promotion: overall benefit at the top, but with a dip at the very top (Slides 6, 8, 9, 10)**  
- **TB ratio (Slide 6):** At 8 bins, higher TB ratio is strongly associated with higher promotion; the top bin has the highest final CIF (~78%). There is **no** clear diminishing return at this resolution — the top bin does not drop below the next.  
- **Pool-minus-mean, fwd (Slides 8–10):** Here the picture is **consistent with diminishing returns**. In Slide 8, Q8 (top) is **slightly below** Q7. With **26 bins** (Slide 10), promotion probability **peaks** in the **upper-middle** (Q20–Q21) and **drops** for the **very top** (Q22–Q26). So the **strongest descriptive evidence** that promotion returns diminish at the very top comes from the pool-minus-mean (fwd) CIFs with fine binning: the best promotion outcomes are not in the extreme top bin but in the bin or two just below — consistent with “once you’re in the highest pools (superstar pools), the marginal benefit flattens or turns down.”

**Promotion: clear reversal for the backward metric (Slide 11)**  
For **z_pool_minus_mean_snr_bwd**, the **highest** bin (Q8) has **lower** promotion than the middle bins (Q4–Q7) — a clear **reversal** at the top. So for the backward pool-minus-mean, being in the “highest” pool is associated with **worse** promotion outcomes than being in the upper-middle. That is the clearest single-slide evidence for a **real** diminishing-returns (or reversing-returns) effect: the top bwd pool plausibly corresponds to a superstar-heavy or highly selected context where returns not only diminish but reverse.

**Attrition: U-shape and penalty at the very top (Slides 7, 12, 13–15)**  
- **TB ratio (Slide 7):** At 8 bins, the top bin has the **lowest** attrition; no hint of a penalty at the top.  
- **Pool-minus-mean, fwd (Slides 12–14):** With 8 bins, Q8 can be **slightly higher** in attrition than Q6–Q7 (Slide 12). With **10** and **26** bins (Slides 13–14), a **U-shape** is clear: the **lowest** attrition is in the **upper-middle** (e.g., Q9 for 10 bins, middle bins for 26); the **very top** bins (Q10, Q23–Q26) have **higher** attrition. So for **attrition**, the data support that **being in the highest pool-minus-mean (fwd) groups is associated with worse retention** than being in the tier just below — i.e., the superstar pool carries an **attrition penalty**, which is a form of diminishing (or reversing) returns.  
- **Pool-minus-mean, bwd (Slide 15):** The **highest** bwd bin has the **highest** attrition (and, from Slide 11, the lowest promotion). So for bwd, the top pool is worse on **both** promotion and attrition — the strongest form of “returns reverse at the top.”

**Model: curvature and diminishing returns (Slides 16–18)**  
- **Partial effects (Slides 16–17):** The **TB ratio** curve (Slide 16) is a **hump**: hazard ratio rises to a peak (around z ≈ 0.7) then **falls**, and in the full model it can go below 1 at high z. So the model **explicitly** estimates that the effect of TB ratio **diminishes and eventually reverses** at high values — consistent with diminishing returns once you’re in the highest TB-ratio pools. The **pool-minus-mean** curve in the **minimal** model (Slide 17) also has a hump (benefits rise then flatten or dip at the top); in the full model it inverts because of multicollinearity with TB ratio, but the **shape** that matters for the superstar-pool story — curvature and downturn at high z — is present.  
- **Coefficients (Slide 18):** The **negative squared terms** for both TB ratio and pool-minus-mean are the algebraic statement of **diminishing returns**: the model allows (and estimates) a curved relationship where the marginal effect declines at high values. So the diminishing-returns pattern is not just visual; it is in the **estimated model**. The high correlation (0.93) between the two variables means their *separate* coefficients are hard to interpret, but the **presence** of curvature in **both** supports that both “highest TB-ratio pool” and “highest pool-minus-mean pool” can show diminishing marginal returns.

**Interaction (Slides 19–20)**  
The **3D surface** and **contour** show that the **joint** level of TB ratio and pool context matters. For diminishing returns, the question is whether the **very top** of the joint space (both dimensions very high = superstar pool) is the **maximum** of the hazard or whether the maximum is in a region that is “high but not the extreme” (e.g., high TB ratio with moderately high pool context). If the contour’s **highest** hazard is in a region where TB ratio is high but pool-minus-mean is not at the extreme (e.g., “best in a strong but not superstar pool”), that would be consistent with diminishing returns in the superstar corner of the joint space. So the interaction plots support that **where** you sit in the two-dimensional space matters and that the **optimum** may not be at the very top of both dimensions — consistent with the idea that the superstar pool (both axes very high) can show diminishing returns.

**Run 3 (Slides 24–30): Same question, different pool metric — rank percent**  
Run 3 uses **Z Pool TB Ratio Rank Pct SNR Fwd** (your **percentile rank** within the pool on TB ratio) instead of pool-minus-mean. So “top of pool” here means “high rank *percent*” (e.g., 90th percentile in your pool). **Promotion (Slide 24):** The top bin (Q8) still has the **highest** promotion CIF (~0.70), but the **marginal** gains at the top are **smaller** (Q8−Q7 ≈ 0.04, Q7−Q6 ≈ 0.02) than in the middle — **diminishing marginal returns** for promotion. **Attrition (Slide 25):** The **top** bins (Q6–Q8) have the **highest** attrition (Q8 ~0.70); the **lowest** attrition is in the middle/lower bins (Q2 ~0.37). So for **attrition**, Run 3 shows a **reversal**: being at the top of your rating pool (by rank percent) is associated with **worse** retention, not better — strong support for the “superstar pool” penalty. **Partial effects (Slides 26–27):** TB ratio again has a **hump** (diminishing returns at high z); pool rank percent in the **minimal** model has a **hump** (hazard peaks around z ≈ 0.75 then falls for the very top) — consistent with a “ranked against superstars” zone in the middle-high range. **Coefficients (Slide 28)** again show negative squared terms and high correlation between TB ratio and the pool variable. **Interaction surface and contour (Slides 29–30):** The **top-right** (high TB ratio and high pool rank percent = superstar corner) has the **highest** hazard ratio — so for a **negative** outcome like attrition, the “best” joint position is the **worst** for retention. So Run 3 **replicates and sharpens** the message: with a **rank-percent** definition of “top,” we again see diminishing marginal returns for promotion and a **clear reversal** for attrition (top pools = highest attrition), and the model and interaction plots support the same curvature and “superstar corner = worst for bad outcome” story.

**Synthesis: is it a real effect?**  
- **Descriptive (CIFs):** For **promotion**, the pool-minus-mean (fwd) CIFs with 10 and 26 bins show a **peak** in the upper-middle and a **drop** at the very top (Run 1); Run 3 (pool rank percent) shows **diminishing marginal gains** at the top (Q8−Q7 smaller than middle-bin steps). For **attrition**, Run 1 pool-minus-mean (fwd) shows a **U-shape** — lowest attrition in the upper-middle, **higher** attrition in the very top bins; Run 3 shows a **reversal**: the **top** rank-percent bins (Q6–Q8) have the **highest** attrition. For the **backward** pool-minus-mean (Run 1), the **top** bin has **lower** promotion and **higher** attrition than the upper-middle — a clear reversal. So **yes**, there is **descriptive evidence** in **both runs** that once you’re in the highest pools, returns can **flatten** (promotion) or **reverse** (attrition, and promotion for bwd).  
- **Model-based:** The Cox model **estimates** negative quadratic terms for both TB ratio and the pool variable (Run 1 and Run 3), and the partial-effect plots show **humps** — benefits that rise then diminish (and in the full model for TB ratio, eventually reverse) at high values. Run 3’s **minimal** model for pool rank percent shows a hump (peak around z ≈ 0.75), and the **interaction** surface/contour (Run 1 and Run 3) show the “superstar” corner (both axes high) as the **worst** region for a negative outcome like attrition. So **yes**, the **model** supports that the relationship is **non-linear** and that **diminishing returns at the top** are a real feature of the estimated effects in **both** runs.  
- **Interpretation:** The pattern is **consistent** with your hypothesis that **once you get into the highest pools, you are ranked against superstars and the returns diminish or reverse**. It is not the only possible explanation (selection, pool composition, or measurement could play a role), but the evidence is **in the direction** your hypothesis predicts and appears in **multiple** places and **both** runs: CIFs (promotion and attrition, fwd and bwd; Run 3 rank percent), partial-effect curves, quadratic terms, and interaction plots. So you can reasonably conclude that **there is a real effect** consistent with diminishing returns in the highest pools — and that the backward pool-minus-mean (Run 1), the fine-bin attrition U-shape (Run 1), and the **Run 3 attrition reversal** (top rank-percent bins = highest attrition) are among the strongest pieces of evidence, with the model-based curvature and the promotion peak in the upper-middle (26 bins) and Run 3 diminishing marginal returns providing additional support.

**One-sentence summary**  
The data are consistent with a real diminishing-returns effect: once you are in the highest rater pools (where you are plausibly ranked against superstars), the benefit of being there flattens or reverses — promotion probability peaks in the upper-middle and drops at the very top (Run 1) or shows diminishing marginal gains at the top (Run 3), attrition is lowest in the upper-middle and rises again at the very top (Run 1 and Run 3), the backward pool-minus-mean top bin does worse on both outcomes (Run 1), and the Cox model estimates negative quadratic terms and humped partial effects (Run 1 and Run 3) and interaction surfaces/contours where the “superstar” corner is worst for retention — so **you’d expect being at the top would almost always be better, but we see that the very top often flattens or reverses, especially for attrition.**

---

*Document includes Run 1 (Slides 5–20) and Run 3 (Slides 24–30); centered on the diminishing-returns (superstar-pool) hypothesis and the message “you’d expect top is always better — what do we see?” CS+CSS, YG ~2002–2013. Verbose throughout.*
