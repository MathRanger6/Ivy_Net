# Scholar VECTOR → new VECTOR: Romania Scientific Quantity Map

**Date:** 2026-09-29  
**Purpose:** Preserve the scientific discussion and proposed next step before any substantive Romania analysis is run.  
**Status:** Scientific-design document. This does **not** authorize substantive analysis or code execution.

## Why this document exists

Romania has passed the practical peer-pool gate. The public replication data appear to provide a strong structure for studying prior performance, assigned educational environment, peer composition, relative position, and later Baccalaureate performance.

Charles raised an important question while thinking aloud:

> The published Baccalaureate result appears monotonically positive with access to stronger schools, but perhaps raw later performance is not the only—or even the most informative—quantity. Should we instead think about development relative to prior performance, peer means, relative position, or some other derived quantity?

We should take that seriously **without searching transformations for an inverted-U**.

The next task is therefore to construct a scientific **quantity map**: identify what is observed, what can be defensibly derived, what each mathematical quantity means, and which estimands actually correspond to the mechanisms we care about.

---

## 1. Start from the variables, not the desired curve

Using the actual Romania files already inspected, construct a compact map of the quantities we can defensibly observe or derive.

At minimum consider:

### Own prior performance

\[
P_i
\]

based on the pre-assignment transition score.

### Peer environment

\[
Q_i=\bar P_{-i,g}
\]

the leave-one-out mean prior performance of the other students in the student's assigned peer pool.

### Relative position

\[
R_i=P_i-Q_i
\]

and/or an appropriate within-pool percentile/rank.

### Later performance

\[
B_i
\]

based on Baccalaureate performance.

### Development / value-added quantity

Consider whether a defensible development quantity can be defined, for example:

\[
D_i=B_i-\widehat{E}[B_i\mid P_i]
\]

or another pre-specified measure of later performance relative to what would be expected from prior performance.

Do **not** adopt this formula merely because Scholar VECTOR proposed it. Evaluate whether it is appropriate given the scales, missingness, test construction, cohort structure, and actual variables.

---

## 2. Decide what the peer pool should be

Scholar VECTOR currently favors:

\[
\text{cohort}\times\text{school}\times\text{track}
\]

because tracks are institutionally meaningful instructional groups.

New VECTOR should challenge that choice.

Compare it with school × cohort using:

- institutional meaning;
- actual identifiers in the public files;
- pool-size distribution;
- within- versus between-track variation;
- leave-one-out stability;
- what Pop-Eleches and Urquiola considered the relevant peer environment.

Do not choose whichever pool produces a more attractive curve.

---

## 3. Separate the possible scientific questions

Several different questions may be present.

### A. Environment question

Conditional on own prior performance, how does later performance vary with peer quality?

\[
E[B_i\mid P_i,Q_i]
\]

### B. Development question

Conditional on prior performance, do students develop more or less than expected as peer quality changes?

\[
E[D_i\mid Q_i]
\]

### C. Relative-position question

Does later performance depend on where the student sits relative to the pond?

\[
E[B_i\mid P_i,R_i]
\]

### D. Interaction question

Does the relationship between entering a stronger pond and later performance differ across the student's own prior-performance distribution?

### E. Assignment / identification question

What does the admission-cutoff regression-discontinuity design tell us that the full-distribution descriptive analysis cannot?

These are different estimands. Do not collapse them into one generic “peer effect.”

---

## 4. Think algebraically about the quantities

Charles specifically wants us to consider whether the phenomenon might appear in **changes, residuals, derivatives, relative quantities, or interactions** even when raw Baccalaureate performance is monotonically increasing.

Explore that conceptually before touching the data.

For each candidate transformation or estimand, explain:

- what it means substantively;
- why it follows from the scientific mechanism;
- what null relationship we would expect;
- what a monotonic relationship would mean;
- what nonlinearity would mean;
- whether an inverted-U would actually be theoretically meaningful;
- what artifacts could manufacture apparent curvature.

We are **not looking for a mathematical transformation that creates our expected shape**.

We are asking whether our mechanism predicts a particular relationship in a scientifically defensible quantity.

---

## 5. A useful conceptual decomposition

One possibility worth considering is that later performance reflects competing mechanisms:

\[
\text{Net outcome}
=
\text{environment benefit}
-
\text{relative-position/congestion cost}.
\]

For students of comparable prior performance, stronger peers may initially improve later development through learning, resources, norms, or other environmental channels:

\[
\frac{\partial B}{\partial Q}>0.
\]

At sufficiently high peer quality, relative-position mechanisms could increasingly oppose that benefit.

That **could** produce an inverted-U, but it does not have to.

If the positive environmental effect dominates throughout the observed support, later performance could remain monotonically increasing even while a negative relative-position mechanism is operating underneath.

This possibility is particularly relevant because the published Romania study reports improved Baccalaureate performance alongside evidence that marginal students entering stronger schools perceive themselves as relatively weaker and report more negative peer interactions.

Thus, a monotonic academic outcome would not necessarily imply that relative-position mechanisms are absent.

---

## 6. Keep Romania distinct from Army and MBB

Romania's scarce allocation governs **entry into the pond**.

Army and MBB contain scarce downstream distinctions after individuals are already in their environments.

Therefore determine explicitly which parts of:

\[
\text{ASSIGN}\rightarrow\text{SCORE}\rightarrow\text{SELECT}
\]

Romania can test and which it cannot.

Romania may primarily be an:

\[
\text{ASSIGN}\rightarrow\text{environment}\rightarrow\text{development}
\]

domain rather than a full congestion/selection replication.

That would still be scientifically useful.

Do not force Romania into the Army/MBB institutional structure merely to create symmetry across domains.

---

## 7. Use the paper's behavioral evidence carefully

Pop-Eleches and Urquiola independently report that students marginally admitted to stronger schools:

- encounter stronger peers;
- perceive themselves as relatively weaker;
- experience somewhat more negative peer interactions;
- experience changes in parental behavior;
- enter an environment where teachers themselves sort.

These findings provide plausible mechanism evidence.

However, the paper explicitly cautions that several dimensions of school quality change simultaneously. It does **not** identify peer quality as the single causal channel.

Use these findings to motivate candidate mechanisms, not to claim that the peer mechanism has already been causally established.

---

## 8. What the published result does—and does not—tell us

The paper finds that students just above admission cutoffs gain access to stronger environments and later achieve modestly higher Baccalaureate scores than nearly identical students just below the cutoff.

That is **not an inverted-U result**.

But the paper's regression-discontinuity estimand is also not our proposed full-distribution HERO-style estimand.

The authors ask approximately:

> What happens when a student barely gains access to a better school than an almost-identical student who barely misses?

Our proposed descriptive question is closer to:

> Among students with comparable prior performance, how does later performance vary across the full distribution of peer environments they actually enter?

The positive RD result therefore does not establish that our full-distribution relationship is monotonic, nor does it imply that an inverted-U exists.

The Romania data should be allowed to answer that question without imposing either shape in advance.

---

## 9. Requested new VECTOR deliverable

Create a short **Romania Scientific Quantity Map** in the VECTOR workspace containing:

1. observed variables;
2. defensible derived quantities;
3. candidate peer-pool definition;
4. candidate estimands;
5. scientific interpretation of each estimand;
6. major identification and confounding limitations;
7. which one or two quantities should be examined first and why;
8. what different result patterns would mean—including monotonic, null, threshold, and nonlinear results;
9. which findings would bear on the broader assortativity/congestion theory and which would be Romania-specific.

Do **not** execute substantive analysis yet.

Scholar VECTOR and Charles should review the quantity map with new VECTOR before authorizing a first Romania run.

---

## Immediate scientific question

Do not ask merely:

> “Does Romania have an inverted-U?”

Ask:

> **Given students with comparable prior performance, what scientifically meaningful quantity should change as the quality and composition of their assigned peer environment changes—and what would different shapes of that relationship tell us about environment benefits, relative position, sorting, and congestion?**

That is the question to settle before plotting the data.
