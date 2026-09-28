# Actual-roster selection comparison: scope, equations, and filing

**Date:** September 27, 2026.  
**Authorization:** Charles approved preparation and execution of the bounded empirical-roster selection comparison. The no-preference assignment experiment, refitting, new filters, and a parameter sweep are outside this authorization.

## The question

On the accepted 2015 players and actual team assignments, whom does the saved fitted PPM scoring specification rank for selection, and how do those choices compare with the players recorded as drafted in 2015?

This is a retrospective ranking diagnostic using transported parameters. It is not a new fit, a reconstruction of the old calibration population, an independent predictive validation, or a stochastic simulation of the calibration likelihood.

## Fixed population and source record

Use the existing 4,267-player, 351-team frozen population and verify its checksum against its execution record. Preserve player identities, season points per minute, stored population-standard-deviation ability scores, source filters, accepted minutes, and actual team assignments. No top-ten anchor restriction is applied to scoring or selection. No source or earlier output is rewritten.

The saved reigning calibration supplies gamma, lambda, and temperature. Its nominal window is 2009–2021; the saved likelihood contains eleven nonempty seasons and includes 2015. Its population and preprocessing are not identical to the newly audited freeze. Carrying its parameters to this population is an explicit transport check, not proof that the fitted coefficients remain optimal.

Join the saved draft lookup by athlete identifier, requiring unique lookup identifiers and nonmissing draft years. Record source names, match tiers, and match scores. All 45 lookup records for the 2015 draft are present in the accepted population. There are 105 accepted players in the lookup in total, including 60 drafted later. Absence from the lookup means no recorded draft; completeness of the original matching process has not been independently established.

## Preserve the fitted score formula

Write sigma for the logistic function, and let A_i be stored standardized PPM. The fitted calibration's threshold convention uses the proportion of roster members who were ever drafted:

$$
\theta=Q_{\,1-105/4267}(A), \qquad
C_j=\frac{1}{n_j}\sum_{h\in j}\sigma\left[\gamma^*(A_h-\theta)\right].
$$

This is a full-roster congestion term: it includes the focal player and is shared by the team. It is not the leave-one-out mean used as the plot axis.

The fitted logit, preserved without moving lambda inside the temperature division, is:

$$
z_i=\frac{A_i}{t^*}-\lambda^*C_{g(i)},\qquad
p_i=\frac{\exp(z_i)}{\sum_h\exp(z_h)}.
$$

Thus ranking by z_i is exactly equivalent to ranking by A_i minus t-star times lambda-star times congestion:

$$
\operatorname{rank}(z_i)
=\operatorname{rank}\left(A_i-t^*\lambda^*C_{g(i)}\right),
\quad t^*>0.
$$

The saved values are gamma-star 19.572332081866243, lambda-star 1.3024305834948529, and temperature-star 1.0698967300656186. The separate assignment fit reports rho-star zero, but no assignment is executed here.

The calibration uses a Bernoulli product with season-wise softmax probabilities summing to one. Its literal expected selected count is therefore one per nonempty season. We will calculate those probabilities for provenance, but will not claim they are calibrated inclusion probabilities for a 45-person winner set or multiply them by K to repair the likelihood.

The calibration code itself contains a top-K overlap diagnostic. We use that ranking interpretation to obtain a fixed-size set. Deterministic top-K is distinct from Bernoulli draws and from K weighted draws without replacement. No stochastic selector is invoked.

## Selection and comparison

The primary actual outcome is draft_year equal to 2015. Set K to its observed accepted-player count, 45. Select the highest 45 fitted logits; resolve exact ties by ascending athlete identifier. Compare with the observed 45-person draft set.

As the necessary reference, select the highest 45 own-performance scores with congestion weight zero, keeping the same population, threshold, and slot count. Report correct selections, missed draftees, other selected players, precision, recall, intersection-over-union, and the number and identities of ability-only winners displaced by fitted congestion. Compare against the mathematical expected overlap K squared over N for a uniformly random K-person set. No random draws or significance test are added.

A secondary, explicitly labeled diagnostic uses the 105 ever-drafted players and top 105 from the SAME score vectors. It distinguishes the annual target from the outcome used by the fit. Future draftees selected in the primary 2015 comparison remain primary false positives; they are not retrospectively reclassified as correct annual selections.

The primary figure uses one fixed sixteen-bin equal-count partition of the raw leave-one-out teammate mean on actual rosters. Freeze the bins across annual observed selections, fitted-ranking selections, and ability-only selections. Record denominators. This is a one-season descriptive comparison, not a recreated historical HERO, an identified peer effect, or a fitted parabola.

## Interpretation

- Better overlap than the own-performance reference supports incremental retrospective discrimination at these settings, not causal congestion.
- Similar overlap with different identities shows that congestion changed choices without improving the annual match.
- Worse overlap means the transported fitted penalty worsens this annual ranking diagnostic; it does not alone invalidate every parameter configuration.
- A displayed tail decline is a descriptive one-season feature with few events. Its presence cannot establish that preference is unnecessary because assignment remains fixed.
- No material change in winners is itself informative about this configuration.

## Files and safeguards

Keep the driver and its human-readable settings JSON together in code/empirical_selection_replay_2015/. New results go only to outputs/empirical_selection_replay_2015/. Save a report under docs/results/ and a separate execution record under docs/run_records/, all sharing the ASSORT_20260927_empirical_selection_replay_v1 prefix.

The driver requires --run, refuses to overwrite this version's existing outputs, records code/settings/input hashes and software versions, and verifies sources remain unchanged. It saves full player scores and ranks, annual and eventual-outcome flags, selected-player comparisons, team summaries, fixed curve bins, numerical summaries, and a figure.

Check exact slot counts, unique identities, score/probability rank equivalence, equivalence after correct lambda rescaling, the congestion-off reference, variance decomposition for sorting, matched draft identifiers, output conservation across bins, and source hashes. Inspect the figure and independently reconcile the selected identities before marking the execution record reviewed.

Charles can inspect code and settings in Cursor. VECTOR announces actual analytical execution. No Git operation or PDF conversion is part of this task.

## Repository evidence inspected

- sports/scripts/pd21_draft_bernoulli_mle.py: board_logits, softmax_probs, attach_player_level_lc, topk_overlap.
- sports/scripts/grandchild_selection_inverted_u_diagnostic.py: _season_k_theta.
- sports/tier1_pool_assignment.py: _viability_logistic and add_team_pool_columns.
- sports/sports_pipeline/panel_rebuild.py: lookup-membership ever-draft labeling.
- sports/sports_pipeline/y_draft_mode.py: distinctions among ever outcome, last-season outcome, and last-season row restriction.
- The original empirical-roster replay was inspected but will not be executed: its Gibbs/score/temperature conventions and multi-season outcome aggregation are different from this narrowly specified ranking diagnostic.

