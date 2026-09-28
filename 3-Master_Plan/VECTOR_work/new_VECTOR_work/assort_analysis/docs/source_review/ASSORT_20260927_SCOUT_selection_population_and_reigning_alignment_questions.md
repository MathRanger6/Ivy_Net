# VECTOR to SCOUT: review the selection comparison before we proceed

**Date:** September 27, 2026  
**Requested by:** Charles  
**Task:** Read-only methodological and implementation review; write your response in the location below. This request does not authorize analytical code changes, experiment execution, refitting, figure rebuilding, or edits to previous results.

## Why we need your feedback

Charles wants a bounded, scientifically defensible comparison he can discuss with Alex. He reports that Alex suggested applying the existing fitted model to empirical players and comparing the model's selections with observed draft outcomes. The larger question remains whether assortativity is necessary for the observed downturn, or primarily shapes its strength. Identity prediction and reproducing the outcome curve are separate objectives; neither should silently replace the other.

VECTOR ran a narrow 2015 comparison, but Charles expected us to account for last player-season (last-ps) versus all player-seasons (all-ps). Your account of the reigning aperture exposed a mismatch between our diagnostic and the established HERO question. We need your knowledge of historical decisions and executable methods before specifying a replacement. Please challenge our assumptions rather than seeking agreement.

Charles is under a deadline and wants to avoid another expanding investigation. Recommend the smallest scientifically defensible correction, with explicit limits.

## What VECTOR actually ran

The completed experiment is ASSORT_20260927_empirical_selection_replay_v1. All paths in this section are relative to assort_analysis/.

Start with:

- docs/decisions/ASSORT_20260927_empirical_selection_replay_v1_scope.md
- code/empirical_selection_replay_2015/ASSORT_20260927_empirical_selection_replay_v1_settings.json
- code/empirical_selection_replay_2015/ASSORT_20260927_empirical_selection_replay_v1.py
- docs/results/ASSORT_20260927_empirical_selection_replay_v1_report.md
- docs/run_records/ASSORT_20260927_empirical_selection_replay_v1_run_record.json

We used the accepted 2015 population: 4,267 players, 351 actual teams, including players who continued college after 2015. The primary outcome was draft year equal to 2015, with 45 observed draftees. A secondary comparison used the 105 players ever drafted according to the saved lookup.

We transported the saved 2009–2021 PPM calibration:

$$
\gamma^*=19.572332081866243,\qquad
\lambda^*=1.3024305834948529,\qquad
t^*=1.0698967300656186.
$$

The implemented quantities were

$$
\theta=Q_{1-105/4267}(A),\qquad
C_j=\frac{1}{n_j}\sum_{h\in j}\sigma\left[\gamma^*(A_h-\theta)\right],
$$

$$
z_i=A_i/t^*-\lambda^*C_{g(i)}.
$$

The congestion mean includes the focal player. The plot axis is a separate leave-one-out teammate mean. We selected the highest 45 scores deterministically and compared them with the highest 45 ability values. The secondary comparison selected 105 from the same score vectors. No assignment, parameter refit, filters, stochastic selection, or sensitivity sweep was added.

The calibration uses a Bernoulli likelihood built from season softmax probabilities summing to one. We explicitly treated top-K as a ranking diagnostic rather than a stochastic replay of that likelihood. Please verify this description against the exact saved fit and producing code.

Both top-45 lists matched the same three annual draftees; the lists shared 43 players. Both top-105 lists matched 10 ever-drafted players. These are results of the executed diagnostic, not evidence that PPM is generally uninformative or that congestion/assortativity is unnecessary. The frozen population differs from the old fit population, and 2015 is inside the estimation window.

## Your historical account, as relayed by Charles

You described the reigning aperture as 2009–2021, last-ps, ever-Y, equally weighted 16-bin leave-one-out HERO. You distinguished panels 1–4 and 9 from the all-ps roster geometry of panels 5–6, and the older 2011–2021 +DFT screening specifications of panels 7–8.

We accept this as your reported account pending source reconciliation. Please cite the data-story lock, reigning manifest, season-Y work, and relevant functions. The question is not whether every panel should become last-ps; it is how to align this new selection comparison with the intended scientific question.

## Questions we need answered

### 1. What is the authoritative outcome population?

Locate the exact reigning command, settings, manifest, and output. Explain the order of window restriction, source filters, last-ps restriction, and outcome assignment. Is max(season) computed before or after the 2009–2021 restriction and other exclusions? How are transfers, multiple team rows in a season, missing later seasons, and the final observation window handled?

Distinguish final observed season, verified career exit, and actual draft eligibility. Do not equate them without evidence. Explain whether a 2015 exit population can be identified using the available longitudinal sources and what unresolved censoring remains.

### 2. Who defines each player's peer environment?

Trace when ability standardization, team summaries, congestion, and leave-one-out peer measures are calculated relative to last-ps filtering. Are they based on full eligible team-season rosters, only final-season athletes, or different populations in different paths?

VECTOR's scientific proposal is to preserve the full roster when measuring the environment and restrict only the evaluated outcome rows to the intended exit population. A departing senior still competes with a talented sophomore. This is a proposal, not a claim about the existing implementation. If historical code does something different, report it explicitly rather than silently repairing it.

### 3. What population and outcome produced the saved coefficients?

Trace the exact calibration JSON used by our driver to the generating command/code and its row/outcome conventions. Was that fit all-ps or last-ps? Was its outcome ever-drafted, annual-drafted, or another timing convention? How were standardization, threshold, and congestion formed?

The saved JSON is:
3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json

Do not infer its population from the word “reigning.” Identify which elements of a last-ps comparison would remain an unchanged fitted specification, which would transport parameters to a different population, and which would change the model. Distinguish score preservation from winner-rule preservation. Check the placement of temperature and lambda against the implemented code.

### 4. What is the smallest aligned comparison?

Recommend one bounded specification. State separately:

- The roster population used to construct performance and peer context.
- The candidates eligible for model selection and outcome evaluation.
- The outcome label and how K is counted.
- Whether selection is conducted separately by season or across pooled exit observations.
- The source and normalization of ability, congestion, and the threshold.
- Which saved coefficients can be used as a declared transport exercise.
- Whether the current sources support a 2015-only comparison or require a wider window.

Explain any tradeoff between staying close to the reigning HERO and evaluating actual draft-year choices. A last-ps/ever-Y comparison is not automatically equivalent to reconstructing the NBA's eligible candidate pool.

Please do not launch a new fit or recommend an open-ended sweep. If an essential source is missing, identify that specific blocker and the narrowest alternative.

### 5. What should we say about the completed run?

Identify any implementation error separately from a mismatch in research question. Confirm or challenge the three-of-45 interpretation using existing outputs. Explain what remains interpretable and what should be qualified in the report.

Recommend how to compare the observed and model-generated outcome curves on a common population and peer axis, alongside individual selection overlap. Keep descriptive curve agreement separate from prediction, causality, and the necessity of assortative assignment. Fixed observed rosters alone cannot answer an assignment counterfactual.

## Requested response

Write one new Markdown response:

docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md

That path is relative to:
3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/

Lead with your recommendation in plain English. Then answer the five questions with repository-relative paths and function names or line references. Label each important statement as directly inspected, previously reported, inferred, or unresolved. Include exact existing commands/settings where available, but do not execute analytical commands.

End with a compact proposed specification and any essential question Charles must decide. Preserve conflicting historical conventions. Do not modify the original comparison, source data, historical manifests, or other agents' documents.

VECTOR will review your response with Charles before implementation. The task now is to make the scientific target and existing implementation agree explicitly.

