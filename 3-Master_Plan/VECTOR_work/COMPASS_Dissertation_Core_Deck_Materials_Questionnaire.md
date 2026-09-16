# COMPASS Questionnaire — Dissertation Core Deck Handoff to VECTOR

**Purpose:** Alex and I are beginning to build the slide deck that will
become the narrative core of the dissertation. The current plan is to
build/write the dissertation first, defend it, and then finish the
paper. VECTOR will help construct an evolving **slide-placeholder
outline** and then flesh it into the dissertation/defense story.

You have been closest to the coding, experiment planning, agent
coordination, current repo state, and decisions made since VECTOR’s last
intensive involvement. Please use this questionnaire to identify the
**authoritative materials VECTOR should read**, not to rewrite the
dissertation yourself.

The broad story as I currently understand it is:

> **Army discovery → cross-domain replication in NCAA men’s basketball
> and R1 academic tenure → simple Wang-style mechanism/model → model
> characterization → predictions and tests.**

That is provisional. If current evidence or project state makes any part
inaccurate, incomplete, or premature, flag it.

## Response rules

For each section, give exact filenames/paths whenever possible.
Distinguish **LOCKED/canonical**, **current best interpretation**,
**provisional**, and **superseded** material. Prefer the smallest
authoritative set over dumping the entire repo. If a claim has already
been demonstrated, point VECTOR to the evidence rather than proposing
that it be rerun.

------------------------------------------------------------------------

# 1. Current State

### 1.1 Canonical handoff

What is the single best current handoff/status document for VECTOR to
read first?

**COMPASS:**

### 1.2 Project map

What current document best explains the overall research questions,
domains, model architecture, and present state?

**COMPASS:**

### 1.3 Major changes since VECTOR’s last close involvement

Summarize only substantive changes: new findings, changed
interpretations, model changes, abandoned approaches, locked decisions,
or important negative results. Point to authoritative files.

**COMPASS:**

### 1.4 Locked versus provisional

What claims, definitions, modeling choices, and findings should VECTOR
treat as **LOCKED**, **CURRENT BEST INTERPRETATION**, **PROVISIONAL**,
or **SUPERSEDED**?

**COMPASS:**

------------------------------------------------------------------------

# 2. Army — Discovery and Bedrock Evidence

### 2.1 Origin of the phenomenon

Which minimum set of files documents how the phenomenon was discovered
in Army data: motivating puzzle, sample, individual performance/talent
measure, pool/unit measure, advancement outcome, original empirical
relationship, and why it was surprising?

**COMPASS:**

### 2.2 Canonical Army figures

Which figures/tables are must-show Army results for a defense? For each
give path, axes/variables, one-sentence interpretation, result type, and
whether defense-ready.

**COMPASS:**

### 2.3 Robustness and identification

Which documents contain the strongest Army robustness, alternative
specifications, controls/fixed effects, subsamples, identification
discussion, and limitations? Which belong in the core deck versus
backup?

**COMPASS:**

### 2.4 Canonical Army terminology

What current terms should VECTOR use, and what older terminology should
be avoided?

**COMPASS:**

------------------------------------------------------------------------

# 3. NCAA Men’s Basketball — Cross-Domain Replication

### 3.1 Canonical dataset/sample

Which documents/scripts define the current NCAA sample, years, player
population, team/pool construction, talent/performance measure, and NBA
Draft outcome?

**COMPASS:**

### 3.2 Canonical NCAA finding

Which files contain the cleanest current evidence that the Army
phenomenon appears among NCAA men’s basketball players seeking NBA Draft
selection?

**COMPASS:**

### 3.3 LOO versus team-mean geometry

Where is the current explanation of leave-one-out PoolQ versus ordinary
team mean, including which empirical patterns appear on each axis?

**COMPASS:**

### 3.4 Remaining QC/data issues

Which NCAA QC/data issues remain material enough for the dissertation
story?

**COMPASS:**

### 3.5 Must-show NCAA figures

List the 3–5 highest-priority NCAA figures/tables, with paths and
one-sentence purposes.

**COMPASS:**

------------------------------------------------------------------------

# 4. R1 Academic Tenure — Third Domain

### 4.1 Dataset/outcome

Which files define the R1 academic dataset, pool/unit, individual
quality/performance measure, tenure outcome, observation window, and
inclusion rules?

**COMPASS:**

### 4.2 Canonical tenure finding

Which files contain the strongest evidence that the same qualitative
phenomenon appears in the academic tenure domain?

**COMPASS:**

### 4.3 Cross-domain mapping

Where have we mapped **individual → pool/team → scarce advancement
outcome** across Army, NCAA, and academia? If no authoritative crosswalk
exists, say so.

**COMPASS:**

### 4.4 Domain-specific differences

What differences across the three domains must the dissertation
acknowledge?

**COMPASS:**

### 4.5 Must-show tenure figures

List the 2–4 highest-priority academic figures/tables.

**COMPASS:**

------------------------------------------------------------------------

# 5. Cross-Domain Empirical Phenomenon

### 5.1 Current best statement

What is our most defensible one- or two-sentence statement of the
cross-domain phenomenon, without overclaiming causality or universality?

**COMPASS:**

### 5.2 Common statistical object

Is there a canonical mathematical/statistical definition of the
Hero/inverted-U/local-competition phenomenon across domains? If not, how
is it operationalized in each?

**COMPASS:**

### 5.3 Cross-domain comparison visual

Do we already have a three-domain comparison figure? If not, do existing
outputs support one without new analysis?

**COMPASS:**

### 5.4 Alternative explanations

What are the strongest alternative explanations currently recognized,
and where are they addressed?

**COMPASS:**

------------------------------------------------------------------------

# 6. Theory and Literature

### 6.1 Core literature

Which works are indispensable? Separate empirical antecedents,
homophilic/assortative formation, local competition/congestion,
selection/advancement, and Wang-style simple-model methodology.

**COMPASS:**

### 6.2 Companion/literature documents

Which companion volumes, nugget guides, one-pagers, or literature briefs
should VECTOR reread?

**COMPASS:**

### 6.3 Abandoned literature paths

Which papers/models were explored but ultimately judged overkill,
mismatched, or unnecessary?

**COMPASS:**

------------------------------------------------------------------------

# 7. Current Canonical Simple Model

### 7.1 Architecture

Describe the canonical **ASSIGN → SCORE → SELECT** architecture and
point to authoritative specification/code.

**COMPASS:**

### 7.2 Levine–Gates (LG) ASSIGN

Identify authoritative documents/code for the current fixed-size
bipartite homophilic network generator. VECTOR needs the formation
equation; definitions of $A_i$, $\mu_j$, $R_j$, $C$, $\rho$, and $s$;
initialization; centroid update; capacity rule; relationship to earlier
Parent/Child formulations; and validation evidence.

**COMPASS:**

### 7.3 SCORE

What is the current SCORE equation and interpretation of $\lambda$?
Where is the canonical implementation and characterization?

**COMPASS:**

### 7.4 SELECT

What is the current SELECT rule? How are $K$ or $K/N$ and advancement
scarcity represented?

**COMPASS:**

### 7.5 Model behavior already demonstrated

Which behaviors are established and need not be rerun merely for
confirmation: $\rho$ changing roster geometry, within-team
dispersion/sorting, centroid differentiation, $\lambda$ producing
curvature, threshold behavior, empirical peak alignment, etc.? Point to
evidence.

**COMPASS:**

### 7.6 Known failures/discrepancies

What does the minimal model not reproduce yet? Which discrepancies
matter scientifically?

**COMPASS:**

------------------------------------------------------------------------

# 8. Wang-Style Strategy

### 8.1 Exact Wang source

Which Wang paper is the methodological inspiration, and where is our
best summary?

**COMPASS:**

### 8.2 Modeling logic

Is the intended sequence still:

$$
\text{Empirical regularity}\rightarrow\text{minimal mechanism}\rightarrow\text{prediction}\rightarrow\text{validation}\rightarrow\text{extension}?
$$

If refined, explain.

**COMPASS:**

### 8.3 Parameter classification

Classify $\rho$, $\lambda$, $C$, $K/N$, and $N$ as behavioral/mechanism
parameters, empirical structural constraints, or simulation choices.

**COMPASS:**

------------------------------------------------------------------------

# 9. Predictions — Next Scientific Step

### 9.1 Predictions proposed

What model-derived predictions/comparative statics have already been
proposed?

**COMPASS:**

### 9.2 Predictions tested

Which have already been tested? Give code, plots, and results.

**COMPASS:**

### 9.3 Phase structure

Have we run or planned a $\rho\times\lambda$ phase map or analogous
regime analysis? What is known and what remains?

**COMPASS:**

### 9.4 Highest-value next experiments

What are the next 3–5 model experiments currently regarded as highest
value? Distinguish agreed plans from your recommendation.

**COMPASS:**

### 9.5 Prospective validation

Which empirical tests could provide genuinely prospective or relatively
untouched validation in Army, NCAA, academia, or another domain?

**COMPASS:**

------------------------------------------------------------------------

# 10. Dissertation Narrative and Defense Deck

### 10.1 Existing outlines

List current dissertation, defense, or paper outlines and identify the
authoritative/newest version.

**COMPASS:**

### 10.2 Candidate narrative

What narrative order has already been discussed? For example:
puzzle/discovery → Army → NCAA → tenure → common mechanism → minimal
model → characterization → predictions → validation → implications.

**COMPASS:**

### 10.3 Core versus backup

Which results are **must-show core story**, **supporting robustness**,
**technical/model validation**, or **backup only**?

**COMPASS:**

### 10.4 Dissertation versus paper

What differences have Alex/the team discussed between the
dissertation/defense story and eventual paper?

**COMPASS:**

### 10.5 Claims we cannot yet make

List attractive-sounding claims that are not yet supported.

**COMPASS:**

------------------------------------------------------------------------

# 11. Figures, Slides, and Visual Assets

### 11.1 Existing decks

List current PPTX/PDF decks in priority order; identify canonical versus
superseded slides.

**COMPASS:**

### 11.2 Figure inventory

Is there a current figure manifest? If not, identify authoritative Army,
NCAA, tenure, and model figure directories.

**COMPASS:**

### 11.3 Figures needing rebuild

Which scientifically current figures are visually obsolete, mislabeled,
based on superseded data, or otherwise need regeneration?

**COMPASS:**

### 11.4 Missing visuals

Which concepts lack a good visual: three-domain crosswalk,
ASSIGN→SCORE→SELECT schematic, LG formation, phase map, prediction
diagram, etc.?

**COMPASS:**

------------------------------------------------------------------------

# 12. Code and Reproducibility

### 12.1 Canonical entry points

Give current scripts/notebooks for Army, NCAA, tenure, LG ASSIGN,
SCORE/SELECT, model sweeps/predictions, and figure generation.

**COMPASS:**

### 12.2 Superseded code

Which old scripts should VECTOR ignore?

**COMPASS:**

### 12.3 Reproducibility

Can the key empirical/model figures currently be regenerated? Identify
gaps.

**COMPASS:**

------------------------------------------------------------------------

# 13. Agent Knowledge and Handoffs

### 13.1 Other agents

Which agents possess specialized knowledge VECTOR should request
directly? Give lane and best handoff document.

**COMPASS:**

### 13.2 Recent handoffs

List the most recent authoritative handoffs/status documents from SCOUT,
COMPASS, and other major agents.

**COMPASS:**

### 13.3 Unresolved disagreements

Are there current disagreements about data, interpretation, model
specification, or next steps that VECTOR should know before outlining?

**COMPASS:**

------------------------------------------------------------------------

# 14. Prioritized Upload Manifest for VECTOR

After answering above, give a **prioritized upload manifest**, not a
repo dump.

### Tier 1 — Read before VECTOR builds the first slide-placeholder outline

Aim for the smallest sufficient set.

**COMPASS:**

### Tier 2 — Read while fleshing out empirical/model sections

**COMPASS:**

### Tier 3 — Reference / robustness / backup

**COMPASS:**

### Do not upload unless requested

Superseded, redundant, or rabbit-hole material.

**COMPASS:**

------------------------------------------------------------------------

# 15. Final Executive Handoff

End with concise answers to:

1.  **What have we discovered?**
2.  **What have we replicated across domains?**
3.  **What mechanism are we proposing?**
4.  **What has the simple model already demonstrated?**
5.  **What predictions are we about to test?**
6.  **What are the biggest unresolved threats or gaps before a
    dissertation defense?**

For substantive claims, point VECTOR to authoritative evidence/files.

**COMPASS:**
