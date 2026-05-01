# Vector → Scout  
## Tier 1 Modeling Background, Direction, and Immediate Coding Objectives

---

# Purpose of This Document

Scout,

This document is intended to synchronize you with the current conceptual and modeling direction of the broader research effort.

Charles and Vector have been refining:
- the theoretical framing,
- the variable ontology,
- and the early-stage modeling architecture

behind the basketball findings that successfully replicated the Army results.

The goal now is to transition from:
- empirical discovery,
toward:
- interpretable mechanism modeling and validation.

This document summarizes:
1. where the project currently stands,
2. the emerging modeling architecture,
3. the phased (“Tiered”) modeling strategy,
4. immediate coding objectives,
5. and recommended documents for review.

---

# Big Picture

The emerging theory concerns:

\[
\textbf{
advancement under constrained distinction
}
\]

The core idea is that:
- individuals compete inside local talent pools,
- while advancement decisions occur globally under finite selection capacity.

Examples:
- Army officers competing locally for Top Blocks while promotion is global,
- NCAA players competing locally for minutes/roles while NBA draft selection is global,
- academics competing locally for recognition while tenure systems allocate finite distinction.

The basketball domain currently provides the cleanest environment for early formal modeling because:

\[
\textbf{
selection pool is global}
\qquad \text{while} \qquad
\textbf{
opportunity pool is local
}
\]

NBA draft selection is global.

However:
- minutes,
- role,
- touches,
- visibility,
- and usage

are allocated locally within teams.

This local/global distinction is now one of the central conceptual foundations of the framework.

---

# Current Empirical Finding

The replicated empirical result is an inverted-U relationship between:
- local teammate quality,
and:
- probability of eventual NBA draft selection.

Current operationalization:
- OPM (own performance metric) = points per minute (PPM),
- local pool quality = leave-self-out teammate PPM,
- success event = eventual NBA draft selection.

Empirically:
- stronger teammate environments initially improve advancement probability,
- but at sufficiently high local talent concentration, the effect reverses.

This suggests:
- developmental benefits,
- and competitive congestion

may coexist simultaneously.

---

# Current Modeling Direction

The current direction is intentionally:

\[
\textbf{
minimalist and mechanistic
}
\]

The immediate goal is NOT:
- full realism,
- causal identification,
- or complete system simulation.

Instead, the goal is:

\[
\textbf{
identify the minimal mechanism set capable of reproducing the observed nonlinear shape.
}
\]

This distinction is important.

The working philosophy increasingly resembles:
- Santa Fe Institute style modeling,
- Dashun Wang style mechanism discovery,
- and complex systems minimalism.

---

# Tiered Modeling Strategy

The project is currently organized conceptually into “tiers.”

---

# Tier 1 — Minimal Structural Models

Current focus.

Question:

\[
\textbf{
Can finite opportunity and constrained distinction alone generate the observed nonlinear relationship?
}
\]

Tier 1 intentionally excludes:
- complex network effects,
- endogenous sorting,
- dynamic adaptation,
- and advanced strategic behavior.

The current Tier 1 ingredients are:

\[
\textbf{
heterogeneous local pools
}
+
\textbf{
finite global selection capacity
}
+
\textbf{
local opportunity competition
}
\rightarrow
\textbf{
nonlinear advancement outcomes
}
\]

Current modeling document:

> `tier_1_model.md`

This document now contains:
- notation,
- ontology,
- candidate congestion measures,
- variable definitions,
- glossary,
- and preliminary formulations.

---

# Tier 2 — Network Exposure Models

Future direction.

Tier 2 introduces:
- nearest-neighbor exposure,
- hierarchical networks,
- talent centers of gravity,
- and network topology.

Examples:
- teammate exposure networks,
- Army hierarchical structures,
- prestige pipelines,
- assignment networks.

Important notation clarification:

Nearest-neighbor notation:

\[
(\cdot)_{nn}
\]

should ONLY be used relative to a specified graph.

For example:
- teammate network,
- hierarchy network,
- rating network,
- developmental network,
etc.

This distinction is theoretically important.

---

# Tier 3 — Strategic Sorting / Dynamic Systems

Longer-term direction.

Possible future ingredients:
- endogenous environment selection,
- prestige vs congestion tradeoffs,
- strategic positioning,
- equilibrium clustering,
- self-organizing talent distributions.

NOT current implementation priority.

---

# Current Tier 1 Variables

The current framework distinguishes between:

| Variable Type | Example |
| :--- | :--- |
| latent variables | \(A_i\) |
| empirical proxies | PPM |
| constructed local statistics | \(Q_{jt}^{(-i)}\) |
| congestion measures | \(C_{ijt}\) |
| outcomes | \(Y_i\) |

This distinction is important for implementation clarity.

---

# Current Candidate Congestion / Pressure Variables

One of the biggest recent conceptual developments is distinguishing:

\[
Q_{jt}^{(-i)}
\neq
C_{ijt}
\]

where:
- \(Q_{jt}^{(-i)}\) = average local pool quality,
- \(C_{ijt}\) = local congestion / roster pressure.

This is theoretically important because:
- average teammate quality,
and:
- competition for scarce opportunity

may represent different mechanisms.

---

## Candidate 1 — Threshold Pressure

\[
C_{ijt}^{\tau}
=
\sum_{\ell \in P_{jt},\ell\neq i}
\mathbf{1}(A_{\ell jt}>\tau)
\]

Interpretation:
- number of teammates above a meaningful performance threshold.

---

## Candidate 2 — Total Roster Pressure

\[
C_{ijt}^{sum}
=
\sum_{\ell \in P_{jt},\ell\neq i}
A_{\ell jt}
\]

Interpretation:
- cumulative local talent pressure generated by surrounding teammates.

Current expectation:
different congestion formulations may behave differently across domains.

For now:
treat congestion as a family of candidate variables.

---

# Immediate Coding Objectives

The immediate mission is NOT:
- publication-ready causal inference,
- or perfect specification.

The current objective is:

\[
\textbf{
rapid exploratory mechanism validation
}
\]

Specifically:

---

## Phase 1 — Variable Construction

For every player-season:

Construct:
- player PPM,
- leave-self-out teammate PPM,
- candidate congestion variables,
- opportunity measures,
- eventual draft outcome.

Potential variables:

| Variable | Meaning |
| :--- | :--- |
| \(A_i\) | player ability proxy (PPM) |
| \(Q_{jt}^{(-i)}\) | teammate quality |
| \(C_{ijt}^{sum}\) | roster pressure |
| \(C_{ijt}^{\tau}\) | threshold congestion |
| \(O_{ijt}\) | minutes / opportunity |
| \(Y_i\) | eventual draft outcome |

---

## Phase 2 — Exploratory Modeling

Potential next steps:
- logistic models,
- nonlinear terms,
- interaction terms,
- visualization,
- response surfaces,
- partial dependence,
- congestion decomposition.

Goal:
determine whether congestion and opportunity variables help explain:
- the observed inverted-U,
- or its turning point.

---

## Phase 3 — Toy Simulation Worlds

Future near-term objective.

Construct simplified simulated environments containing:
- latent ability,
- local pools,
- finite opportunity,
- global selection.

Question:

\[
\textbf{
Can the inverted-U emerge from these ingredients alone?
}
\]

This is scientifically important because:
- if the minimal structure reproduces the empirical shape,
then:
- the theory gains mechanistic credibility.

---

# Recommended Documents for Scout to Review

Highest Priority:
- `tier_1_model.md`

Strongly Recommended:
- `Vector_Master_Theory_and_Modeling_Notes_4.md`
- `2026_0430_Paper7_feedback.md`
- `Vector_Questions_and_Modeling.md`
- `Vector_HS_Data_Pathway.md`
- `Vector_to_Scout_HS_data_thoughts_etc.md`

If available:
- Army conceptual background notes,
- Basketball replication plots,
- Any latest empirical notebooks/pipelines.

**Lee A. Evans (USMA Math) — “Evans” in structural-misclassification memos**  
Same folder as other references; filenames match disk exactly:

- *Single and multi-objective parameter estimation of a military personnel system via simulation optimization* (Evans, Bae & Roy, **2017 Winter Simulation Conference** proceedings; PDF-on-disk often labeled 2018):  
  `../3-reference_documents/Evans, Bae, Roy - 2018 - Single and multi-objective parameter estimation of a military personnel system via simulation optimization.pdf`
- *Evaluating Our Evaluations: Recognizing and Countering Performance Evaluation Pitfalls* (Evans & Robinson, **Military Review**, Jan–Feb 2020):  
  `../3-reference_documents/Evans-Rob-Evals.pdf`

*Distinct from* Evans & Bae (2019) *JDMS* and from the Louisville **2018 dissertation**; see `3-reference_documents/diss_prop.md` bibliography.

---

# Important Conceptual Clarifications

## 1. OPM

“OPM” refers generally to:
- own performance metric.

Examples:
- basketball → PPM,
- Army → TB ratio / evaluation quality,
- academia → publications/citations.

In the current formal notation:
- OPM often operationalizes latent ability \(A_i\).

---

## 2. Local vs Global

This distinction is foundational.

Basketball:
- local opportunity allocation,
- global advancement selection.

Army:
- local evaluation,
- global promotion boards.

Academia:
- local departmental evaluation,
- broader prestige and tenure markets.

---

## 3. Nearest Neighbor Notation

Do NOT casually use:
- “peer average,”
- “nearest neighbor,”
- and “pool average”

interchangeably.

Nearest-neighbor notation:

\[
(\cdot)_{nn}
\]

must always be defined relative to:
- a specific graph/network structure.

---

# Current Strategic Direction

The project is increasingly transitioning from:

> “interesting empirical finding”

toward:

> “candidate general theory of advancement under constrained distinction.”

The current strategic emphasis is:
- conceptual clarity,
- variable discipline,
- minimal models,
- interpretable mechanisms,
- and iterative empirical validation.

---

# References / Influences

Important conceptual influences include:

- **Yin et al. (2019),** *Quantifying the dynamics of failure across science, startups and security* (*Nature*) — project PDF: `../3-reference_documents/Yin et al. - 2019 - Quantifying the dynamics of failure across science, startups and security.pdf` *(often discussed as Dashun Wang’s line of work; Wang is senior author).*
- **Lee A. Evans (USMA)** on finite **rating pools**, **forced distribution**, and **structural** misidentification / misclassification — PDFs under `../3-reference_documents/` (see list in *Recommended Documents* above). *Not* James A. Evans (coauthor on the Yin *Nature* paper).
- Friendship paradox / nearest-neighbor exposure literature
- Network science exposure models
- Complex systems minimal-mechanism modeling traditions

---

# Final Note

Current priority:
- get the Tier 1 variables operationalized cleanly,
- test candidate congestion formulations,
- and begin exploratory model fitting/simulation.

The immediate goal is not perfection.

The immediate goal is:

\[
\textbf{
determine which minimal structural ingredients appear necessary to reproduce the empirical phenomenon.
}
\]
