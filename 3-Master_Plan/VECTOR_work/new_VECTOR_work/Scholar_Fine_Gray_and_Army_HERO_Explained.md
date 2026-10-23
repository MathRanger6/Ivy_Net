# Fine–Gray and the Army HERO plots: a plain-English guide

*For Charles • 19 October 2026*

**Main finding:** The reviewed Army HERO bars show recorded outcome fractions. A Fine–Gray analysis may exist elsewhere, but its connection to these figures remains unverified. The pattern deserves investigation; its appearance alone does not establish robustness or causation.

This guide primarily condenses NVector’s 18 October memo, especially §§3–4 and 7. The archived bar calculation and Cox input construction were also checked directly. No analyses were rerun.

## 1. What Fine–Gray does

Imagine following Captains toward promotion to Major. Before promotion, some leave the Army and lose eligibility for that transition. Departure is then a **competing event**. Someone still eligible when observation stops is **censored**: we do not know what happens afterward. Leaving and becoming unobserved are different things.

**Fine–Gray asks about promotion probability over time while accounting for competing departure.** Its target is the *cumulative incidence*: the chance of promotion by a specified time, before a competing departure. For example: “What is the chance of promotion within eight years of becoming Captain?” Eight years is illustrative, not an established Army analysis horizon.

Three methods answer different questions:

- **Raw observed proportion:** “What fraction of the included officers have a recorded promotion?” Forty promotions among 100 officers gives 40%. This describes the records. If some officers were observed much longer than others, it does not automatically estimate their promotion probability by the same career year.
- **Cause-specific Cox:** “Among officers still eligible and not yet promoted, how does the promotion rate differ with ratings or peer context?” Officers leave that promotion risk set when they depart. A separate departure model can examine the competing rate. These are rates among people still awaiting either event, rather than cumulative percentages. Both event rates together can produce promotion probabilities. [1]
- **Fine–Gray:** Models a different rate, the *subdistribution hazard*, linked to cumulative promotion probability. Officers who departed remain part of its special statistical accounting, with censoring weights where needed. This does not mean they remain eligible. The model can generate predicted probabilities at a stated time. [2, 3]

A hazard ratio of 1.5 does **not** mean a 50% promotion probability or a 50-percentage-point increase. For either regression, a probability requires an additional prediction calculation. Fine–Gray is useful for probability questions; it is not mandatory for every competing-risks analysis.

With complete observation through one common horizon, simple counts can estimate that horizon’s probability. With earlier censoring, **Aalen–Johansen** provides a standard way to estimate competing-event probabilities without regression. Such estimates and Fine–Gray predictions still require appropriate assumptions about censoring. [1, 2]

## 2. What Charles actually did in the reviewed Army workflow

**First, define the horizontal axis correctly.** In the historical example, it was standardized **own rating minus the leave-one-out peer average**. “Leave-one-out” (LOO) means excluding the focal officer from the peer average. If your rating is 0.80 and your peers average 0.60, your relative standing is 0.20. Peer quality is 0.60. These are different measures. Standardizing a difference does not turn it into a peer average.

The memo traces this display to the March 20 export of notebook 520, Cell 11:

1. **Select a final record for each officer** during plot preparation and apply the display’s filters.
2. **Divide officers into eight groups** using the selected relative-standing measure.
3. **Draw a promotion curve for each group.** Time runs from promotion to Captain. Each curve counts recorded promotions up to that time and divides by the group’s fixed included population.
4. **Show those groups as bars.** Each bar counts all recorded promotions in its group and divides by the included group population. With matching records and filters, this equals the curve’s final endpoint. The code calculates the fraction directly; it does not read the rendered graph.
5. **Repeat for attrition.**

Turning curves into bars makes the rise and upper-group downturn easier to see. It preserves the endpoint but removes timing information. “Final” means the available endpoint, **not necessarily the same career horizon for everyone**. Cropping a curve at 4,500 days does not restrict the bar calculation to promotions by day 4,500.

**The reviewed bars do not use fitted Cox coefficients, Fine–Gray predictions, or Aalen–Johansen calculations.** Censored officers retained in a group remain in its denominator; the calculation does not correct for unequal follow-up. Separate promotion and attrition Cox fits appear in Cell 12.5.

Charles remembers Fine–Gray work. The inspected notebooks do not establish where that fit occurred or whether it generated another version of these figures. CODA also reports completed newer plots using the peer average directly, but their exact outputs and settings still need independent verification. Neither point should be resolved by assumption.

## 3. What remains before stronger scientific claims

**1. Establish which analysis produced which figure.** When Army access returns, locate the remembered Fine–Gray fit and save its notebook version, input preparation, fitting call, execution record, and outputs. Trace its connection to the displayed curves and bars. A “CIF” title does not identify an estimator. Even a Cox fitting call can implement Fine–Gray when special expanded, weighted inputs are used. [3]

**2. Fix the scientific question, population, and clock.** Specify who enters, when follow-up begins, what promotion and competing departure mean, and a substantively justified common horizon. Count promotions, departures, censored cases, and exclusions. Check late entry, follow-up differences, and whether ratings and peer membership were known before the outcomes they are meant to explain. A final-record plot does not establish that timing.

**3. Audit the longitudinal Cox construction before trusting its inference.** Archived Cell 12.3 passes each interval’s length—stop minus start—to ordinary Cox fitting, without preserving its position on the career clock. Multiple intervals belong to the same officer. That is not the usual start–stop construction for changing covariates. Establish whether the authoritative run repaired this; otherwise use an appropriate longitudinal method and account for dependence. Correcting standard errors alone would not restore missing risk-set timing. [4]

**4. Estimate and test the intended pattern.** Retain the existing bars as descriptive evidence. For common-horizon probabilities, use a justified censoring-aware method; for adjusted probabilities, specify covariates and the population over which predictions are averaged. Report group counts and confidence intervals. Check model assumptions and whether the downturn survives reasonable changes in bins, peer definitions, cohort, and horizon. Clearly label exploratory choices and guard against selecting only favorable specifications.

**5. Match the claim to the evidence.** LOO removes your own contribution to a peer average; it does not remove selection or confounding. Relative standing mixes own performance with peer performance. Stronger causal claims about peers require a credible identification strategy. Similar Army, basketball, and tenure shapes also require separate checks of populations, outcomes, and follow-up before being treated as equivalent evidence.

**What is defensible now:** The reviewed selected Army sample shows a descriptive promotion pattern across relative-standing groups. Its magnitude, uncertainty, sensitivity to follow-up and specification, and explanation still need validation. Publishable descriptive or associational science is possible without proving causality; the methods and wording must match what was established.

**Sources:** Primary: [NVector’s LOO/HERO methods memo](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/20261018_NVector_to_SVector_LOO_and_HERO_Methods_Conclusion.md>), §§3–4, 7, R5/R7. Methods: [1] [Competing risks and Aalen–Johansen](https://cran.r-project.org/web/packages/survival/vignettes/compete.pdf); [2] [Fine–Gray regression](https://search.r-project.org/CRAN/refmans/cmprsk/html/crr.html); [3] [Weighted Fine–Gray construction](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/finegray.html); [4] [Reviewed Cox fitting interface](https://scikit-survival.readthedocs.io/en/stable/api/generated/sksurv.linear_model.CoxPHSurvivalAnalysis.html).
