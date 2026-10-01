# PD44 — Dissertation work map and proposed model-chapter outline

**Date:** September 30, 2026  
**Status:** Proposed writing structure for Charles's review. This is a work map, not a completed chapter or a new analysis plan.  
**Controlling direction:** PD44 and Charles's accompanying priority update. Earlier education-first and experiment-first plans remain history.

## 1. The change in direction

**Begin writing the dissertation now, starting with the model chapter.** We already have enough model structure, development history, and completed computational work to explain what we built and why. We do not need to finish national Romania analysis or resolve every empirical discrepancy before writing that explanation.

Writing now serves two purposes:

- **Preserve the scientific argument.** Explain the question, each modeling decision, what the existing experiments taught us, and where the explanation remains incomplete.
- **Expose specific gaps.** If a sentence cannot be supported, write down exactly what is missing. A missing result becomes a bounded question for later review, not permission to launch another sweep.

**Primary source:** `transcripts/20260930_Paper_Directions_44_otter_ai_transcript.docx`. The writing-first instruction begins at 00:00; the model architecture discussion is at approximately 03:56–05:56; the recommendation to start with the model chapter and let writing expose gaps is at 12:01–13:06.

## 2. Dissertation work map

### Foreground: explain the model

**Immediate product:** A dissertation-level model chapter that stands on its own. A reader should understand what goes into the model, what each stage changes, what emerges from it, and what the completed investigations do and do not establish.

**Working sequence:**

1. Explain the overall question and ASSIGN → SCORE → SELECT architecture.
2. Explain assignment, including the Levine–Gates model and its development history.
3. Explain the congestion score, its assumptions, and the meaning of its parameters.
4. Explain selection capacity and the distinct deterministic and stochastic selection rules.
5. Organize existing experiments by the questions they answered.
6. Identify the remaining bridge from mechanism demonstrations to empirical fitting.

Start with the architecture section rather than another data search. Then write the three component sections before polishing the experimental narrative.

### Background: bounded Romania national acquisition

**Continue the already authorized data-gathering task using the frozen Alba definitions and existing source-completeness gates.** The work is to recover, checkpoint, and audit sources. It is not permission to retune program categories, eligibility, success definitions, or binning to obtain a desired curve.

Before a national outcome analysis can begin, both conditions are required:

- **Source readiness:** Coverage, unresolved pages, duplicates, identifiers, score fields, placement joins, and origin-school applicant populations meet the documented gates. A successful download alone does not meet them. Applicant groups must not silently become claims about all graduating students.
- **Explicit execution authorization:** Charles approves national outcome analysis after reviewing the source audit.

This documentation update does not start or restart an acquisition process. Charles's existing notebook workflow remains the execution route.

PD44 also mentions academic-data gathering in parallel at approximately 13:35–14:02. That remark does not start a new tenure acquisition job here.

### Preserve: Army outcome and survival methodology

**Keep the work on promotion timing, attrition, censoring, survival, and competing risks in the dissertation map.** Whether it becomes its own chapter or a substantial methods section is still open.

PD44 explicitly supports retaining this methodological contribution at approximately 09:10–11:31. The journal paper may use only part of it.

Do not collapse the methods into one label. Empirical cumulative-incidence curves, cause-specific Cox models, and Fine–Gray subdistribution models answer different questions. The existing Army documentation distinguishes empirical competing-risk curves from fitted Cox analyses. Fine–Gray was mentioned in the meeting, but its implemented and completed status still needs verification.

### Defer: further model experiments and presentation restructuring

No new parameter sweeps, model fitting, national outcome analysis, repository restructuring, or slide rebuilding is authorized by this work map.

A useful writing gap might be: “We cannot yet justify carrying these calibrated coefficients into this replay because the selection probabilities differ.” That points to a particular specification problem. It does not justify searching broadly for a better-looking result.

## 3. Provisional dissertation arrangement

PD44 suggests three central content blocks:

1. **The empirical phenomenon:** What the existing domain evidence shows about own performance, peer environment, and advancement.
2. **The model:** How assignment, scoring, and selection can generate different outcomes and curves.
3. **Connecting model and evidence:** Estimation, fit, interpretation, and eventually supported counterfactuals.

Introduction/literature and a concluding synthesis could surround those blocks. This is a working interpretation of the discussion, **not an approved final five-chapter table of contents**.

The Army outcome-methodology material may precede the empirical-effects discussion or occupy a separate chapter. PD44 raises both the value of this work and flexibility about its placement. We should preserve that option without delaying the model chapter.

The model-to-data block is currently less settled than the model itself. The dissertation outline should show that honestly rather than promise validated fitting or counterfactual conclusions that have not been established.

## 4. Proposed model-chapter outline

### 4.1. The question and the three-stage architecture

**Main point:** Being in a strong group and receiving a scarce distinction are different events.

Explain the sequence:

- **ASSIGN:** Who ends up with whom?
- **SCORE:** How does the specified environment enter an individual's modeled score?
- **SELECT:** Who receives the available opportunities under the stated selection rule?

**Why each stage is needed:** Assignment creates the peer environments. Scoring specifies how those environments matter. Selection converts scores into outcomes under a capacity constraint or probability rule. An outcome curve alone cannot tell us which of these stages produced its shape.

Use a small verbal example: two equally scored individuals can face different environments; even a modest score change can alter who receives the last available place. Then distinguish that example from evidence that real institutions use the same scoring rule.

Keep the environmental benefits-minus-drawbacks idea, $L=B-D$, separate from an advancement probability. The current subtractive congestion score does not independently estimate both $B$ and $D$.

**Sources:** `3-Master_Plan/BINDING_Selection_is_its_own_step.md`; `3-Master_Plan/re_entry/02_Three_Kinds_of_Model.md`; PD44, 03:56–05:16.

### 4.2. What the model treats as individual performance and environment

**Main point:** $A_i$ is the model's specified individual input. When constructed from an observed performance statistic, it is not automatically innate or portable talent.

Explain:

- The population and time unit: individual, player-season, career exit, or another explicitly defined unit.
- The performance measure and its standardization.
- Group membership, group size, and capacity.
- Mean peer performance excluding the focal individual, when used as the curve's horizontal axis.
- The distinction between a peer-performance axis and the congestion quantity actually subtracted from the score.

For the recent basketball experiments, standardized season points per minute supplied $A_i$. The experimental population retained those values while assignment changed. That does not reconstruct what each player's performance would actually have been on another team.

**Sources:** `assort_analysis/docs/results/ASSORT_20260927_three_season_mechanism_v1_report.md` and the source/design records it links; `3-Master_Plan/re_entry/LG_model_desk_reference.md`.

### 4.3. ASSIGN: the Levine–Gates grouping mechanism

**Main point:** Similarity preference shapes assignments; realized sorting is measured afterward.

For the documented sequential Grandchild implementation, describe the probability of assigning individual $i$ to group $j$ at the current step:

$$
p_{ij}=
\frac{R_j\exp[-\rho|A_i-\mu_j|]}
{\sum_{\ell:R_\ell>0}R_\ell\exp[-\rho|A_i-\mu_\ell|]}.
$$

Here $R_j$ is the number of remaining seats and $\mu_j$ is the current group centroid. Explain the initial-centroid convention, randomized arrival order, immediate centroid updates, and capacity constraints.

**Plain-language example:** When $\rho=0$, a group with eight remaining seats has twice the assignment probability of a group with four. This is uniform assignment over remaining seats, not uniform selection of a team.

Then introduce the measured sorting index:

$$
H_{\mathrm{sort}}
=1-\frac{\sum_j\sum_{i\in j}(A_i-\bar A_j)^2}
{\sum_i(A_i-\bar A)^2}.
$$

Explain why random finite groups generally have a positive index. Input $\rho$ and output $H_{\mathrm{sort}}$ are not interchangeable.

Preserve the history:

- Earlier target-based assignment used a different distance/probability specification.
- Parent and Child variants were design stages.
- The implemented Grandchild updates group composition during assignment.
- The model's similarity concerns performance metadata, rather than node degree alone.

**Sources:** `3-Master_Plan/re_entry/LG_model_desk_reference.md`; `sports/documents/541_grandchild_homophily_assign_README.md`; `3-Master_Plan/re_entry/model_OPORD.md`. Implementation anchors for detailed equation-to-code verification: `sports/541_grandchild_homophily_assign.py` and `sports/tier1_pool_assignment.py`.

### 4.4. SCORE: how the specified congestion penalty operates

For the recent full-team smooth-congestion version:

$$
v_i=\frac{1}{1+\exp[-\gamma(A_i-\theta)]},
\qquad
C_j=\frac{1}{n_j}\sum_{i\in j}v_i,
\qquad
S_i=A_i-\lambda C_{g(i)}.
$$

**Explain each parameter separately:**

- **$\gamma$: transition sharpness.** How abruptly a player's contribution rises around the threshold.
- **$\theta$: transition location.** Where that rise occurs on the performance scale.
- **$\lambda$: penalty weight.** How strongly the constructed congestion quantity reduces the score.
- **$C_j$: constructed congestion.** In this version, the mean includes the focal player, and everyone on the team receives the same subtraction.

For fixed memberships, a shared team penalty preserves score ordering within that team while potentially changing ordering across teams.

**Do not merge historical specifications.** Earlier material used leave-one-out congestion. The recent experiment used full-team congestion while retaining leave-one-out peer performance as a plotting variable. Standardizing congestion also changes the meaning of a numerical $\lambda$.

Explain why the recent experiments held $\theta$ fixed when changing selection capacity: moving $K$ alone then changes SELECT without also changing SCORE. Other routines coupled $\theta$ to $K/N$; that is a different comparison.

Include the historical threshold argument near $\lambda\approx4/\gamma$ as an argument whose assumptions must be spelled out, not a universal downturn theorem. A local sigmoid derivative is not by itself a population selection-curve result.

**Sources:** `3-Master_Plan/re_entry/LG_model_desk_reference.md`; `3-Master_Plan/re_entry/06_Lambda_threshold_and_KN_memo.md`; `3-Master_Plan/re_entry/HEROs_and_PASSes/theta/THETA_KN_sweep_summary.md`; the three-season report.

### 4.5. SELECT: capacity, ranking, and selection noise

**Main point:** A score does not specify selection until the rule and capacity are given.

For deterministic selection:

$$
Y_i=\mathbf{1}\{i\text{ is among the }K\text{ highest scores}\},
\qquad q=K/N,
$$

with a documented tie rule.

Explain:

- $N$ is the defined eligible population and $K$ is the number selected.
- A smaller $K/N$ means greater scarcity.
- Deterministic top-$K$ has no random selection after scoring.
- Random assignment can still make outcomes vary across repeated runs.
- Stochastic selection adds another source of variation; temperature must be defined through the actual probability equation.

The historical Bernoulli calibration and selection of exactly $K$ individuals without replacement are different probability models. Temperature's placement and the scaling of $\lambda$ matter. Do not call calibrated parameters transferable until equivalence or an explicitly justified approximation is established.

The 2.7% used in the recent mechanism experiment was a scenario motivated by the career-exit outcome proportion; it was not the observed annual selection rate of each experimental season.

**Sources:** `VECTOR_PD41_Assortativity_Scientific_Brief.md`, especially its calibration/replay cautions; the three-season report; historical temperature scripts referenced in the desk reference. The final stochastic equations require direct implementation verification before chapter prose treats them as settled.

### 4.6. What the completed experiments taught us

Organize by scientific question, retaining dates and model versions. The following are **findings documented in saved reports**, not freshly rerun results in this update.

1. **Can congestion change winners without similarity preference?** The three-season experiment says yes at its tested settings. Preferential assignment increased the average number changed. This does not establish a downturn without preference.
2. **Was the initial penalty large enough to visibly reshape the curve?** The penalty audit put the raw congestion subtraction on the scale of individual performance. Later penalty comparisons made the curve's response visible.
3. **How does the shape depend on the penalty and binning?** The $\lambda=4$, $\rho=1$, 10% selection comparison displayed a rise and decline in equal-width bins; the quantile view differed. The chapter must show support counts and explain the different views.
4. **Does a low selection fraction make assignment preference irrelevant?** The direct 50% versus 1% comparison did not support that blanket conclusion. Fewer winners changed in absolute number at 1%, but a larger fraction of the small selected set changed.
5. **How does reduced assignment preference change the environment?** It altered measured sorting and the range of peer environments, as well as the selection profile. Empty extreme bins are missing support, not zero success.

Use the existing plot trail as the figure register. Preserve the 50% selection detour and its purpose. Do not describe the chosen $\lambda$ as an estimated optimum or the visually selected downturn as a preregistered discovery.

**Sources:** `assort_analysis/docs/results/ASSORT_20260927_model_plot_trail.md` and its linked reports: three-season mechanism, selection-rate comparison, penalty magnitude, penalty bars, scarcity bars, selection at 50%, assignment preference at 0.05, and the direct preference/scarcity comparison.

### 4.7. Established scope, limits, and the bridge to fitting

**We can explain now:** The documented architecture, implemented model families, parameter roles, and bounded conclusions of the saved experiments.

**We should not claim yet:**

- Universal necessity of assortative preference for a downturn.
- That a hump proves congestion.
- That scarce NBA selection or five-player court capacity explains the empirical basketball curve. The current experiments did not explicitly model five simultaneous court positions.
- That one calibrated parameter set applies unchanged across likelihoods, selection rules, normalizations, or domains.
- That the Romania descriptive patterns identify a causal peer penalty.
- That Army, basketball, tenure, and education share an already verified identical empirical effect.

End with a short list of specific unresolved bridges. That list should guide later decisions without becoming a new experimental campaign.

## 5. Evidence discipline for drafting

Use these labels in working prose:

- **Definition or assumption:** We chose a mechanism or outcome rule. Its existence is not evidence that an institution follows it.
- **Implemented:** A code path exists; execution and scientific validity are separate questions.
- **Documented completed result:** A saved report records a run and its outputs. Follow its provenance before using an exact figure in the dissertation.
- **Independently checked:** State which check was done and when. This update read sources; it did not reproduce computations.
- **Proposed or unresolved:** No supporting completed result is established.
- **Historically superseded:** Preserve why a previous specification existed and what replaced it.

Use descriptive experiment names alongside historical Pass A/B/C labels. Those labels changed across documents. Likewise, spell out the intended meaning of “Layer B” each time rather than assume a shared meaning.

Keep these unresolved discrepancies visible:

- **Army:** Peer definitions; $H_{\mathrm{sort}}=0.131$ versus approximately 0.255–0.279; Mac/AWS run-to-result mapping; completed component plots versus an unfinished mosaic.
- **Basketball:** Binned tail behavior versus fitted quadratic curvature; annual versus career-exit outcomes; empirical versus simulated axes; calibration versus replay.
- **Tenure:** Construction roster versus inference sample versus decision cohort; person-year versus decision-year analyses; completed versus unfinished survival work.

These are provenance tasks for the claims that require them. They do not all have to be solved before the model architecture can be drafted.

## 6. First writing packet and remaining verification

**Recommended first draft:** The chapter opening and Sections 4.1–4.2 above: the motivating question, the three stages, the quantities, and the interpretation of measured performance. Then develop ASSIGN, SCORE, and SELECT in order.

**Retain dissertation detail:** Explain rejected alternatives when they clarify a scientific choice, show equations with verbal interpretation, preserve parameter regimes, and attach each experimental claim to its saved report. Compress later for a paper.

**Targeted verification while writing:**

- Trace each displayed model equation to its actual implementation and version.
- Recover the precise stochastic calibration/replay equations before asserting parameter comparability.
- Verify the assumptions and provenance of historical threshold/shape arguments.
- Identify the completed Army estimator for each figure, especially before using “Fine–Gray.”
- For every proposed missing analysis, record the unsupported sentence, existing evidence, smallest necessary check, and authorization status.

This is sufficient to begin a chapter. It is not a requirement to finish another suite of experiments first.

## 7. Source register and access limits

All paths are repository-relative unless identified as relative to this VECTOR workspace.

**Primary priority evidence:**

- `transcripts/20260930_Paper_Directions_44_otter_ai_transcript.docx` — read in full. This is the controlling meeting record.
- Charles's PD44 priority update in this conversation — explicit sequencing, background-acquisition limits, and national-analysis authorization gate.

**Model sources inspected:**

- `3-Master_Plan/BINDING_Selection_is_its_own_step.md`.
- `3-Master_Plan/re_entry/LG_model_desk_reference.md`.
- `3-Master_Plan/re_entry/02_Three_Kinds_of_Model.md`.
- `3-Master_Plan/re_entry/model_OPORD.md`.
- `sports/documents/541_grandchild_homophily_assign_README.md`.
- `3-Master_Plan/re_entry/06_Lambda_threshold_and_KN_memo.md` — relevant threshold, congestion-definition, and parameter passages inspected.
- `3-Master_Plan/re_entry/HEROs_and_PASSes/theta/THETA_KN_sweep_summary.md`.

**VECTOR workspace sources inspected:**

- `VECTOR_CURRENT_STATE.md` — current/historical priority and evidence records.
- `VECTOR_PD41_Assortativity_Scientific_Brief.md` — relevant specification and unresolved-transfer passages.
- `assort_analysis/docs/results/ASSORT_20260927_model_plot_trail.md`.
- `assort_analysis/docs/results/ASSORT_20260927_three_season_mechanism_v1_report.md`.
- `assort_analysis/docs/results/ASSORT_20260927_rho_scarcity_v1_report.md`.
- `education_analysis/00_READ_ME_FIRST.md` — status and gate records.

**Army sources inspected:**

- `talent/documents/COX_METHODS_BRIEF.md`.
- `talent/documents/CR_AND_HR_FOR_DUMMIES.md` — competing-risk/Cox distinction and timing caveats.

**Limits of this update:** No research computation, live acquisition, figure regeneration, or new model experiment was performed. Named code files are implementation anchors for chapter verification, not a claim that every code path was audited here. Saved reports supply the numerical history. Army source refreshes still depend on their authorized environment. No missing source prevents beginning the conceptual model draft.

## 8. Decision for review

**Proposed next step:** Draft the opening architecture section, then the three model components, using the evidence distinctions above. Keep the final dissertation chapter count provisional. Let national acquisition proceed only within its already approved scope, and bring any proposed analysis back for an explicit decision.

