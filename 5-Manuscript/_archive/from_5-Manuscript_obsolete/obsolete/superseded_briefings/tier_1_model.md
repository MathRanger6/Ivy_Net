# Tier 1 Minimal Model — Basketball Application

## Core Structural Insight

Basketball represents an especially clean application of the framework because:

\[
\textbf{selection pool is global}
\qquad \text{while} \qquad
\textbf{opportunity pool is local}
\]

The NBA draft selects globally across all eligible players, but opportunities to generate draft-relevant signals are allocated locally through:
- team membership,
- minutes,
- role,
- usage,
- and coaching decisions.

---

# Core Tier 1 Logic

The minimal proposed mechanism is:

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

The goal of Tier 1 is to determine whether these minimal ingredients alone can generate the observed inverted-U relationship.

---

# Basic Structure

Let player \(i\) belong to team \(j\) during season \(t\).

---

## Latent Ability

\[
A_i
\]

where:
- \(A_i\) = latent player ability.

In empirical applications, the observable own-performance metric (OPM) may serve as a proxy for latent ability \(A_i\).

Examples:
- basketball: points per minute (PPM),
- Army: TB ratio / evaluation quality,
- academia: publications, citations, or productivity measures.

Throughout discussion, “OPM” may therefore refer to the domain-specific empirical proxy used to operationalize latent ability.

---

## Local Pool Quality

Define leave-self-out teammate quality:

\[
Q_{jt}^{(-i)}
=
\frac{1}{|P_{jt}|-1}
\sum_{\ell \in P_{jt},\ell\neq i}
A_\ell
\]

where:
- \(P_{jt}\) = team roster / local opportunity pool,
- \(Q_{jt}^{(-i)}\) = average teammate quality excluding ego.

---

## Observed Signal

Observed signal is generated through both:
- individual ability,
- and local environmental effects.

\[
S_{ijt}
=
A_i
+
B(Q_{jt}^{(-i)})
+
\varepsilon_{ijt}
\]

where:
- \(S_{ijt}\) = observed player signal,
- \(B(Q)\) = developmental / signaling benefit from stronger teammates,
- \(\varepsilon_{ijt}\) = stochastic noise term.

---

## Local Opportunity Allocation

Opportunities are allocated locally.

\[
O_{ijt}
=
O(A_i,Q_{jt}^{(-i)},C_{jt})
\]

where:
- \(O_{ijt}\) = opportunity allocation,
- examples include:
  - minutes,
  - usage,
  - touches,
  - offensive role,
  - visibility,
- \(C_{jt}\) = local congestion / competition intensity.

---

## Draft-Relevant Realized Signal

Realized draft signal depends on both:
- observed ability signal,
- and opportunity exposure.

\[
R_{ijt}
=
S_{ijt}\cdot O_{ijt}
\]

where:
- \(R_{ijt}\) = realized draft-relevant signal.

---

# Global Selection

Define:

\[
\Lambda_t
=
\text{annual global selection capacity}
\]

For the NBA draft:

\[
\Lambda_t \approx 60
\]

Draft outcome:

\[
Y_i = 1
\]

if player \(i\) is selected among the top \(\Lambda_t\) players globally.

Potential probabilistic formulation:

\[
P(Y_i=1)
=
\text{logit}^{-1}
\left(
\alpha
+
\beta_1 A_i
+
\beta_2 Q_{jt}^{(-i)}
-
\beta_3 C_{jt}
\right)
\]

---

# Source of the Inverted-U

The central tradeoff:

\[
\frac{\partial B(Q)}{\partial Q}>0
\]

but:

\[
\frac{\partial O}{\partial Q}<0
\]

at sufficiently high local pool quality.

Interpretation:
- stronger environments may improve development and signaling,
- but concentrated talent may reduce opportunity share.

Therefore:

\[
\frac{\partial P(Y_i=1)}{\partial Q}
=
\text{development/signaling gains}
-
\text{opportunity congestion costs}
\]

Potential turning point:

\[
B'(Q^*)
=
G'(Q^*)
\]

where:
- \(Q^*\) = optimal local pool quality,
- \(G(Q)\) = congestion/opportunity-cost function.

---

# Variable Glossary / Model Ontology

| Symbol | Type | Meaning | Formulation / Construction |
| :--- | :--- | :--- | :--- |
| \(i\) | index | player | row-level player identifier |
| \(j\) | index | team | team identifier |
| \(t\) | index | season | season identifier |
| \(A_i\) or \(A_{ijt}\) | latent / proxied | player ability or own performance | empirical proxy varies by domain; basketball: \(PPM_{ijt}\) |
| \(P_{jt}\) | set | local opportunity pool | players on team \(j\) in season \(t\) |
| \(Q_{jt}^{(-i)}\) | constructed variable | leave-self-out local pool quality | \(\frac{1}{|P_{jt}|-1}\sum_{\ell\in P_{jt},\ell\neq i}A_{\ell jt}\) |
| \(S_{ijt}\) | latent signal | observed/evaluated player signal | \(A_i+B(Q_{jt}^{(-i)})+\varepsilon_{ijt}\) |
| \(B(Q)\) | function | developmental / signaling benefit from local environment | increasing benefit term; candidate: \(B'(Q)>0\) |
| \(\varepsilon_{ijt}\) | noise term | stochastic signal noise | distribution TBD |
| \(O_{ijt}\) | observed / constructed | locally allocated opportunity | minutes, usage, role, touches, visibility |
| \(C_{ijt}\) | constructed variable family | local congestion / roster pressure | candidate forms: \(C_{ijt}^{\tau}\), \(C_{ijt}^{sum}\) |
| \(C_{ijt}^{\tau}\) | constructed variable | threshold pressure | \(\sum_{\ell\in P_{jt},\ell\neq i}\mathbf{1}(A_{\ell jt}>\tau)\) |
| \(C_{ijt}^{sum}\) | constructed variable | total roster pressure / talent mass | \(\sum_{\ell\in P_{jt},\ell\neq i}A_{\ell jt}\) |
| \(R_{ijt}\) | constructed variable | realized draft-relevant signal | \(S_{ijt}\cdot O_{ijt}\) |
| \(\Lambda_t\) | parameter | annual global selection capacity | NBA draft: \(\Lambda_t\approx 60\) |
| \(Y_i\) | outcome | draft outcome | \(1\) if eventually drafted, else \(0\) |

---

# Current Empirical Mapping

Current empirical operationalization:

| Concept | Current Empirical Variable |
| :--- | :--- |
| individual ability proxy | points per minute (PPM) |
| local pool quality | leave-self-out teammate PPM |
| success event | eventual NBA draft selection |

---

# Important Conceptual Clarification

This framework distinguishes:

| Structure | Basketball Example |
| :--- | :--- |
| global selection pool | NBA draft |
| local opportunity pool | team roster |
| local opportunity allocation | minutes, role, usage |
| global advancement outcome | draft selection |

This distinction may become one of the central conceptual foundations of the broader theory.


---

# Addendum — Candidate Definitions of Local Congestion / Roster Pressure

An important emerging distinction is:

\[
Q_{jt}^{(-i)}
\neq
C_{ijt}
\]

where:
- \(Q_{jt}^{(-i)}\) captures average local pool quality,
- while \(C_{ijt}\) captures local crowding pressure / roster pressure.

This distinction may become theoretically important.

Examples:
- a team may have moderate average talent but very high crowding pressure,
- or a team may have high average talent concentrated in only one or two players.

Thus:
- average environment quality,
- and competition for scarce opportunity,

may represent distinct mechanisms.

---

## Candidate Interpretation of \(C_{ijt}\)

Conceptually:

\[
C_{ijt}
=
\text{competition for scarce local opportunity}
\]

Examples:
- minutes,
- usage,
- touches,
- command opportunities,
- authorship prominence,
- evaluator attention.

---

## Candidate Formulation 1 — Threshold Pressure

\[
C_{ijt}^{\tau}
=
\sum_{\ell \in P_{jt},\ell\neq i}
\mathbf{1}(A_{\ell jt}>\tau)
\]

Interpretation:
- number of teammates above some meaningful performance threshold.

Potential strengths:
- interpretable,
- threshold can be tuned empirically,
- captures “how many legitimate competitors surround ego?”

Potential limitation:
- does not capture intensity above threshold.

---

## Candidate Formulation 2 — Total Roster Pressure

\[
C_{ijt}^{sum}
=
\sum_{\ell \in P_{jt},\ell\neq i}
A_{\ell jt}
\]

Interpretation:
- total local performance pressure generated by surrounding teammates.

Potential strengths:
- captures total competitive talent mass,
- reflects cumulative crowding pressure,
- avoids reducing congestion to simple averages.

Potential limitation:
- may require normalization for roster size or opportunity supply.

---

## Important Conceptual Distinction

\[
Q_{jt}^{(-i)}
\]

asks:

> “How strong is the average local environment?”

while:

\[
C_{ijt}
\]

asks:

> “How much local competition exists for scarce opportunity?”

These may produce substantially different dynamics.

---

## Cross-Domain Interpretation

| Domain | OPM | Local Pool Quality | Crowding / Pressure |
| :--- | :--- | :--- | :--- |
| Basketball | points per minute (empirical proxy for $A$) | mean teammate quality | count/sum of strong teammates |
| Army | TB ratio / evaluation quality | mean officer quality | concentration of strong officers in SR pool |
| Academia | publications / citations | mean department productivity | concentration of highly productive peers |

Importantly, different congestion formulations may ultimately prove more appropriate in different domains.

The framework should therefore initially treat:

\[
C_{ijt}
\]

as a family of candidate congestion measures rather than a single finalized variable.

---

# Current Direction

The immediate next goal is not full realism, but:

\[
\textbf{
identifying the minimal mechanism set capable of reproducing the observed empirical shape.
}
\]

The Tier 1 framework should therefore remain:
- modular,
- interpretable,
- empirically testable,
- and computationally simple enough for preliminary simulation and fitting.
