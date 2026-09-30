# Scholar VECTOR ↔ new VECTOR — Romania 2001 Joint Scientific Specification

**Date:** 2026-09-29  
**Prepared by:** Scholar VECTOR  
**For:** Charles Levine and new VECTOR  
**Status:** Joint scientific-specification draft. This records the next decision gate. It does **not** authorize substantive outcome analysis.

## 1. Why we are here

The archival feasibility work has now answered the structural question well enough to stop scraping and move to scientific specification.

For Alba 2001, the Ministry archive supports a standalone reconstruction with:

- originating gymnasium/source-school code;
- national examination score;
- grades 5–8 average;
- admission composite;
- destination high school;
- destination track/specialization;
- placement information.

The bounded structural audit recovered the full Alba origin-school report family: all 168 source-directory school codes were recovered, and candidate/placement correspondences were checked without running a substantive model.

The important limitation is equally clear:

> The defensible population is **participating applicants associated with each coded gymnasium**, not automatically every eighth-grade classmate or every gymnasium graduate.

That population distinction must govern the next analysis.

---

## 2. Active Romania scope

For now, **2001 only**.

Why:

- 2001 is the only inspected year with both the national-exam component and grades 5–8 average available separately;
- 2001 has the strongest demonstrated origin-school → placement architecture;
- 2002 and 2003 remain less complete for the score decomposition we need.

Do not broaden to later years until the 2001 design either succeeds or fails scientifically.

---

## 3. Population to analyze

### Proposed population

Students participating in the 2001 computerized high-school allocation whose archived records can be associated with an originating gymnasium/source-school code and an observed placement outcome.

Call this, for now:

> **participating applicants from originating gymnasium \(g\) in 2001**

Do **not** call this population:

- all students in the gymnasium;
- all eighth-grade graduates;
- all classmates;
- the complete local adolescent population.

Those stronger labels require evidence we do not yet have.

### Immediate requirement

Before substantive analysis, new VECTOR should produce a short accounting table showing:

- recoverable applicant count;
- number of origin gymnasiums;
- gymnasium group-size distribution;
- number/proportion of applicants in groups large enough for stable leave-one-out peer measures;
- unresolved/ambiguous origin-school identities;
- known archive gaps.

---

## 4. Candidate individual-performance variables

The recovered 2001 records permit three distinct performance quantities.

### A. National examination score

\[
E_i
\]

Interpretation:

- standardized national performance measure;
- observed after years of gymnasium exposure;
- less locally subjective than school-awarded grades;
- **not** innate or latent ability.

Potential role:

> baseline/portable performance proxy when asking whether local school-grade performance differs by peer environment.

### B. Grades 5–8 average

\[
G_i
\]

Interpretation:

- school-awarded performance accumulated during the gymnasium years;
- potentially more sensitive to local grading norms, relative standing, teacher judgment, and environment;
- **not yet demonstrated to be quota-based or rank-rationed**.

Potential role:

> environment-sensitive performance measure.

### C. Admission composite

For the recovered 2001 general admission route:

\[
T_i = 0.75E_i + 0.25G_i
\]

with the documented two-decimal truncation rule.

This composite is the score used by the allocation mechanism.

Important implication:

> Because \(T_i\) mechanically drives assignment priority, it should **not automatically be treated as the only independent performance measure** in the mechanism analysis.

The 75/25 formula is supported by the recovered official rules and the Alba data. The paper's equal-weight description remains an unresolved documentary discrepancy and should be preserved as such.

---

## 5. Proposed peer environment

Primary candidate:

\[
\boxed{\text{origin gymnasium} \times \text{2001 cohort}}
\]

For student \(i\), a candidate peer-quality measure is:

\[
Q_i=\frac{\sum_{j\in g}P_j-P_i}{n_g-1},
\]

where \(P\) could be defined using \(E\), \(G\), or another pre-specified measure depending on the scientific question.

### Critical caution

Because the archive may contain only **participating applicants** from each gymnasium, \(Q_i\) should initially be described as:

> leave-one-out mean performance of other participating applicants from the same originating gymnasium

—not automatically the mean of every classmate or every eighth-grade student.

If later evidence establishes full graduating-cohort coverage, the language can be strengthened.

---

## 6. First scientific gate: do gymnasiums actually differ?

Before defining success or fitting outcome curves, determine whether the proposed peer environments contain enough meaningful variation.

Report, using only pre-placement variables:

- mean and variance of \(E_i\), \(G_i\), and \(T_i\) by gymnasium;
- between-gymnasium versus within-gymnasium variation;
- distribution of gymnasium means;
- overlap/common support in individual \(E_i\) and/or \(T_i\) across gymnasiums;
- preliminary sorting descriptions.

The key question is:

> **Do similarly performing students appear in meaningfully different gymnasium performance environments?**

A useful design needs both:

1. differentiation across gymnasiums; and
2. enough overlap to compare similar individuals across those environments.

If all gymnasiums are nearly identical, stop.

If gymnasiums are completely segregated by performance with no overlap, also stop or sharply qualify the design.

The scientifically useful case is differentiation **plus some overlap**.

---

## 7. Competitive market

Primary approximation:

\[
\boxed{\text{town/local high-school market} \times \text{2001 cohort}}
\]

The original researchers treat towns as approximate high-school markets because students were young and generally applied locally.

Important qualification:

> Town was not a legal restriction of the national allocation mechanism.

Therefore new VECTOR should distinguish:

- institutional nationwide allocation;
- empirically local competition;
- any observable cross-market placements.

The archived school-specific reports already show that county-only lists can miss genuine cross-county placements, so market construction must not rely blindly on county labels.

---

## 8. Candidate selection outcomes

We need a real allocation outcome, chosen **before** inspecting any peer-environment/outcome curve.

Three candidate outcomes remain reasonable.

### A. Binary top-school placement

\[
Y_i=1\{\text{student assigned to top-ranked high school in the local market}\}.
\]

Advantages:

- simple;
- interpretable;
- closest to a drafted/not-drafted or selected/not-selected outcome.

Limitations:

- preferences are unobserved;
- not being assigned to the top school does not prove rejection from a preferred opportunity;
- top-school ranking must be defined without circularity.

### B. Assigned-school selectivity rank/percentile

Continuous or ordinal rank of the student's assigned high school within the local market.

Advantages:

- uses more information than a single binary cutoff;
- less sensitive to one arbitrary “top school” definition.

Limitations:

- still realized placement, not preference-conditioned success.

### C. Assigned-school/track cutoff

Use the admission cutoff or comparable incoming-selectivity measure of the assigned destination.

Advantages:

- directly tied to the capacity-constrained allocation mechanism.

Limitations:

- may mechanically covary with the student's own transition score;
- requires careful construction to avoid leakage.

---

## 9. How to define prestige/selectivity without circularity

Avoid using **same-cohort Baccalaureate performance** as the primary prestige measure.

That would define the quality of the placement using a later outcome and risks post-treatment leakage.

Preferred hierarchy:

1. **prior-cohort admission cutoff or incoming-performance ranking**, if recoverable and stable;
2. same-cohort admission cutoff with explicit own-observation/leave-one-out protection;
3. same-cohort mean incoming performance with explicit leakage caveats.

Baccalaureate outcomes can remain a descriptive validation of long-run school quality, but should not define the primary 2001 selection outcome.

---

## 10. Preferences remain the principal interpretation limitation

Students submitted ranked school/track preferences, but those preference lists are absent from the usable archive.

Therefore:

\[
\boxed{\text{realized placement}\neq\text{pure preference-conditioned selection success}}
\]

Our most defensible language may be:

> realized placement into a more or less selective high-school opportunity

rather than:

> success/failure in obtaining the student's preferred school.

Track-specific statements such as:

> “Did the student get into the best Math program they wanted?”

are not currently observable.

---

## 11. Scarcity and \(K/N\)

The archive and institutional rules provide real capacity constraints, so \(K\) can be meaningful.

The denominator \(N\) is harder because preference rankings are absent.

Do **not** define:

\[
K/N=\text{capacity}/\text{town cohort}
\]

unless the denominator is shown to be the actual competitor pool for that opportunity.

For the first pass, **admission cutoff/selectivity** may be a cleaner scarcity measure than a forced \(K/N\).

---

## 12. Candidate mechanism decomposition

If the score components survive cleanly, one potentially useful mechanism question is:

> Among students with similar national-exam performance \(E_i\), does the gymnasium environment \(Q_i\) relate systematically to school-awarded grades \(G_i\), and does that feed into the allocation composite \(T_i\) and final placement?

This is attractive because:

- \(E_i\) is more standardized;
- \(G_i\) is accumulated within the gymnasium;
- \(T_i\) is the actual allocation priority score.

But do not claim that \(G_i\) is congestion, peer evaluation, or top-block rationing unless evidence supports that interpretation.

The first goal is to establish **environment-sensitive performance**, not to force a mechanism label.

---

## 13. Structural analogy to Army and MBB

### Romania

\[
\text{gymnasium environment}
\rightarrow
(E_i,G_i)
\rightarrow
T_i
\rightarrow
\text{local/national HS competition}
\rightarrow
\text{capacity-constrained placement}
\]

### Army

\[
\text{unit/rating environment}
\rightarrow
\text{performance/evaluation}
\rightarrow
\text{advancement competition}
\rightarrow
\text{selection}
\]

### MBB

\[
\text{team environment}
\rightarrow
\text{performance/visibility}
\rightarrow
\text{national draft competition}
\rightarrow
\text{selection}
\]

The Romania design is promising because the peer pool and competitive pool are distinct.

Its main difference is that selection is highly mechanical in the composite score, making the exam/GPA decomposition unusually important.

---

## 14. Proposed next authorized work for new VECTOR

**Recommended model: GPT-6 Astra — High.**

New VECTOR should now prepare a **Romania 2001 Scientific Specification / Go-No-Go Brief** that settles:

1. the exact applicant population;
2. gymnasium group-size/completeness accounting;
3. whether \(E_i\), \(G_i\), and \(T_i\) are sufficiently clean for distinct roles;
4. whether meaningful cross-gymnasium differentiation and overlap exist;
5. the preferred local competitive-market construction;
6. a pre-specified selectivity/placement outcome;
7. the interpretation limits created by missing preferences;
8. whether admission cutoff or another variable is the preferred scarcity measure.

### Authorized

- structural counts;
- pool-size accounting;
- overlap/support diagnostics using **pre-placement variables only**;
- verification of score formulas;
- selectivity-definition feasibility checks;
- documentation.

### Not yet authorized

- substantive peer-environment → placement regression;
- HERO curves;
- searching for an inverted-U;
- outcome-driven tuning of prestige definitions;
- track-specific “wanted program” success claims;
- causal claims;
- Git operations.

---

## 15. Explicit go/no-go gate

Proceed to substantive Romania analysis only if:

### GO condition 1 — usable peer environment

The participating-applicant gymnasium groups are large and coherent enough to support stable LOO peer measures.

### GO condition 2 — differentiation plus overlap

Gymnasiums differ meaningfully, but similarly performing students still occur across different gymnasium environments.

### GO condition 3 — interpretable performance decomposition

At least one defensible performance specification can distinguish standardized exam performance from local grades and/or the composite score.

### GO condition 4 — non-circular placement outcome

A realized selectivity/placement measure can be defined without using the same later outcome we are trying to explain and without unacceptable own-score leakage.

### GO condition 5 — honest interpretation

The design can be described as realized selective placement despite missing preferences, without pretending it measures preference-conditioned success.

If these conditions do not hold, Romania should be preserved as a useful institutional/mechanism case rather than forced into a full replication.

---

## 16. Current collaboration stance

The archival work is now sufficiently mature that the next bottleneck is **scientific definition, not data recovery**.

Scholar VECTOR and new VECTOR should reconcile the specification above before Charles authorizes substantive analysis.

The governing question is now:

> **Can 2001 Romania support a scientifically honest test of whether similarly performing students from different originating gymnasium environments have different probabilities of receiving more selective, capacity-constrained high-school placements?**

That is the question to settle before the first real outcome model runs.
