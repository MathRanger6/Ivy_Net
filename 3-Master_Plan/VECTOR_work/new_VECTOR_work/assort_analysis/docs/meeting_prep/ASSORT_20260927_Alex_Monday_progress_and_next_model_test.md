# Progress for Alex: basketball measurement and the next model comparison

**Prepared:** Sunday, September 27, 2026, for the Monday morning discussion.  
**Status:** Meeting preparation based on completed, reviewed analyses. This document introduces no new numerical result. The fitted-model selection replay and the no-preference assignment comparison remain unexecuted in this campaign.

## What Charles can say at the start

> We investigated whether basketball's weak measured sorting was a consequence of the player pool or the performance measure. The pool changes did not uncover stronger sorting for points per minute. But the same-player comparison showed that the result depends on the performance measure: Player Efficiency Rating shows more team sorting, and the high-minute anchor comparison strengthens it beyond a matched-size random-subset reference. Box Plus/Minus shows substantially more sorting, although its construction includes team performance. We therefore cannot conclude from the points-per-minute result that basketball has negligible sorting in every relevant sense.
>
> We have not yet answered whether assortative assignment is necessary for the model's downturn. The next focused task is to apply the fitted selection model to the actual rosters and compare its choices with actual draft outcomes, then examine what happens when assignment has no assortative preference.

This is a statement of completed progress and an explicitly unfinished question. It does not turn the measurement investigation into a model-validation claim.

## First we examined the player pool

The accepted 2015 audit contains **4,267 players on 351 teams**. Earlier playing-time and pool diagnostics examined season points per minute (PPM). They provided reasons to stop searching those particular restrictions for a stronger PPM sorting result.

Charles then suggested keeping the broader player pool while using the ten players with the greatest total season minutes to describe each team's performance distribution. This separates a team's descriptive anchors from the complete pool of potential competitors: bench players do not automatically disappear from the competition model.

The PPM anchor comparison narrowed team intervals but did not reveal stronger sorting than comparable random subsets. That result concerns the tested PPM definition and population. It does not establish that every performance measure would respond identically.

## Next we changed the measure while holding player identities fixed

We compared PPM, Player Efficiency Rating (PER), and Box Plus/Minus (BPM) on the same **4,161 players and 350 teams**. Their overall sorting indices were:

- **PPM:** $H_{\mathrm{sort}}=0.06338$.
- **PER:** $H_{\mathrm{sort}}=0.10892$.
- **BPM:** $H_{\mathrm{sort}}=0.32515$.

The sorting index describes the share of measured player variation accounted for by differences in team means. It is not the LG assignment-preference parameter $\rho$, and it is not an estimate of innate talent.

PER therefore gives a different account of measured team clustering from scoring rate alone. However, its average standardized team interval remained almost the same width as PPM's. More separation among team means did not make the teams' observed player ranges disjoint.

BPM produces much more measured clustering. Its team-performance adjustment makes that result unsuitable as independent proof of recruiting-based talent sorting. This does not disqualify BPM from describing realized contribution or studying selection in context. Its appropriate role depends on the scientific question.

These results establish **measurement dependence**, not which measure is uniquely correct. The measures were not chosen by their ability to produce a desired downturn.

Source: [same-player performance-measure audit](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/results/ASSORT_20260927_performance_metric_audit_v1_report.md>).

## Then we tested Charles's measure-by-pool qualification

We applied the original fixed high-minute anchors to PPM and PER on the same usable-PER population: **4,163 players on 350 teams**, with **3,413 available original anchors**. Missing PER values did not cause replacement of anchors by different players.

We compared those anchors with **100 random within-team subsets of exactly the same team-specific sizes**. Each repetition used identical player membership for PPM and PER.

For PPM, anchor sorting was **0.06995**, compared with a random-subset mean of **0.08102**. **99 of 100** random subsets had sorting at least as high as the anchors.

For PER, anchor sorting was **0.13768**, compared with a random-subset mean of **0.12602**. The anchor value exceeded all 100 random-subset values. Its advantage over their mean was approximately **0.01166**, or 1.17 percentage points of explained measured variation.

PER's average team interval narrowed by **20.7%** relative to its full matched pool; PPM's narrowed by **13.1%**. Extensive central overlap remained: the maximum coverage on the recorded grid was 349 of 350 teams for PER and 350 for PPM.

The random subsets were drawn **within existing teams**. This is a reference for the effect of selecting fewer players, not an experiment that removes assortative assignment. The repetition counts are not independent seasons or a population-level significance claim.

**What this told us:** the descriptive pool and performance measure interact. The earlier PPM-only negative finding cannot be generalized to PER.

**What it did not tell us:** whether the difference reflects reliability, roles, coaching, recruitment, source differences, or another mechanism; whether PER is portable talent; or whether assortativity is necessary for congestion's effect on selection.

Source: [fixed high-minute anchor comparison](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/results/ASSORT_20260927_ppm_per_top_ten_anchor_v1_report.md>).

![Completed 2015 PPM and PER anchor comparison](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/ppm_per_top_ten_anchor_2015/ASSORT_20260927_ppm_per_top_ten_anchor_v1_comparison.png>)

## The specific model questions remain the priority

Charles's written record in `Assortativity_MBB_issues.docx`, before the later “stop the presses” discussion, identifies two concrete model requests. His subsequent conversation clarified that the empirical comparison should include the identities selected by the algorithm versus those actually drafted.

**Actual-roster replay:** preserve the empirical players and assignments, apply the existing fitted scoring and selection specification, and compare model selections with the properly defined actual draft outcome. Report overlap in selected identities and their distribution across teammate environments. If the outcomes were used for fitting, agreement measures fit rather than independent predictive validation.

**No-preference assignment comparison:** use a basketball-like population and LG assignment with $\rho=0$, retain the specified scoring and selection ingredients, and examine whether the relevant downturn persists. At $\rho=0$, assignment follows remaining seats without performance-based preference. Chance can still produce nonzero realized sorting.

With observed rosters fixed, $\rho^*$ has no reassignment to perform. The scoring and selection parameters govern that replay. Existing fitted numerical values must be interpreted under compatible equations: the previously identified Bernoulli-calibration versus selection-replay discrepancy remains explicit. A different selection rule can be explored as a scenario, but must not be represented as an unchanged calibrated replay.

A downturn without preference would provide a counterexample to necessity at the tested configuration. Establishing that assortativity strongly shapes the downturn would require a positive-preference comparison. Attributing persistence specifically to scarce selection would require a less-scarce comparison. Neither conclusion follows from a zero-preference result alone.

The empirical five-player court limit may shape minutes, roles, and recorded performance. The current model does not explicitly simulate five simultaneous court positions, so its results cannot identify that limit as a cause.

## Recommendation under the Monday deadline

Pause additional metric-ranking diagnostics, anchor sizes, filter searches, and added seasons. This is VECTOR's deadline-driven recommendation, not a claim that those questions have been scientifically settled.

Use the completed figure and findings above as the immediate meeting deliverable. If Charles authorizes new execution tonight, prioritize the **actual-roster selection replay** before expanding the experiment. Confirm the relevant fitted-parameter record, selection equations, population, and draft-outcome definition first. Do not silently substitute a different selection algorithm or treat the historical approximately 2.7% ever-drafted proportion as a verified annual selection rate.

The next model output should be saved separately under `assort_analysis/`, with visible code and settings, selected-player identities, and an execution record. Existing results and source files should remain identifiable and preserved.

The reported basketball target is a local upper-tail decline; the reviewed current curve also has positive fitted global quadratic curvature. The two descriptions must not be silently merged into a universally downward-opening parabola.

For Monday, the strongest defensible message is: **we have established that weak PPM sorting does not settle the broader measurement question, and we have narrowed the next task to the model comparisons Alex requested. We have not yet demonstrated whether assortative preference is necessary.**
