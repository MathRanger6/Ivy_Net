# Basketball data hygiene and model history — what VECTOR now understands

**Date:** September 25, 2026  
**Status:** Source review and historical reconciliation. No empirical reconstruction, new experiment, or figure regeneration.  
**Purpose:** Preserve the reasoning behind earlier decisions before freezing the population for the new assortativity investigation.

## 1. Why this review was necessary

Charles recalled that a school could appear only because it played one game against a well-covered school. Its player records then entered the season-level analysis even though almost none of that school's season was observed. He also recalled that removing these records substantially weakened the attractive inverted-U plot.

That account matches the problem described in the August records. VECTOR had previously inspected the current preparation code and saved roster summaries, but had not absorbed this decision history adequately. The earlier explanation of the six two-player teams was too definite. The historical coverage problem supplies a plausible explanation; it is not yet a team-by-team reconstruction of those six cases.

The immediate purpose is to understand how the analytical population and scientific reasoning developed. Restoring the earlier curve is not a criterion for choosing filters. Existing design decisions remain recorded, but the exact eligible 2015 population remains provisional. The question document for SCOUT is linked at the end.

## 2. Three different problems must remain separate

### Incomplete observation of a team's season

A captured game can contain perfectly real observations of both opponents while the dataset captures the rest of the season for only one opponent. The problem is treating one game's statistics as comparable to a substantially observed season.

The coverage rule counts distinct captured game identifiers for each team and season. It does not establish how many games that team actually played, and it does not require each individual player to have appeared in eleven games. The present rule is a minimum coverage requirement, not proof of a complete season or a verified Division I roster. [H3–H5; C1–C2]

The archived SCOUT conversation reports an ESPN schedule comparison for 40 low-coverage team-seasons: 39 had the same count in the frozen extract and ESPN response, while one had one captured game versus three in the response. This supports a source-coverage explanation for those inspected cases. It does not prove completeness of ESPN coverage or resolve every team. VECTOR read the saved output; VECTOR did not query ESPN or reproduce the audit. [H13]

### Placeholder identities

The August 17 correspondence describes a different problem: 99 dash-name, zero-minute entries associated with a single Brigham Young University game. SCOUT reported that the live ESPN response also contained them. These are not equivalent to real players whose season is incompletely captured. The adopted pipeline removes dash-name entries before counting team-season games. [H1–H4]

The early SCOUT response said the minutes filter was sufficient for the dash-name problem. Subsequent discussion identified real-name, fragmentary rosters that required a separate coverage rule. It would be misleading to carry the early conclusion forward as the final policy for all data problems.

### Too few observed minutes for an individual performance measure

The separate individual rule uses **twenty total observed minutes across the season**, not twenty minutes per game. The primary measure is points per minute, calculated as total observed points divided by total observed minutes. Very small minute totals can produce unstable rates. Twenty season minutes is a low exposure floor; it does not by itself identify regular rotation players.

This rule cannot solve the one-game-team problem. A player can play twenty-five minutes in one captured game and pass the individual floor while the entire team's season remains poorly observed. Conversely, a team can have many captured games while an individual has only a few minutes. [H4; H6; C2]

## 3. The recorded policy sequence

**July: minutes, binning, and sample composition were already active choices.** SCOUT's historical thoughts discuss dropping players below twenty season minutes, comparisons with lower floors, changes in the plotted curve, and the small number of drafted observations lost in particular comparisons. They also document sharply different curves when restricting the sample to teams with drafted players. Scientific reasons included unstable performance ratios and defining the population, but curve appearance was also part of the discussion. We should preserve that history rather than retrospectively describe every choice as made without seeing outcomes. [H6]

**August 17: placeholders led to the wider coverage investigation.** Charles's note raised implausibly large rosters. In the archived conversation, he explicitly asked for a distribution of captured games and questioned whether one-game seasons belonged in the analysis. The saved audit reported 1,883 one-game team-seasons among 6,557 in its 2011–2021 window. Those are historical output counts, not newly verified population totals. [H1–H3; H13]

**The initial written coverage rule retained six or more games.** The rollout note specified dropping team-seasons with five or fewer distinct game identifiers after the dash filter. [H3]

**The later recorded rule retained eleven or more games.** The policy document's evening update and the August 19 exchange specify dropping ten or fewer. The normal configuration currently sets the threshold to ten and the code retains counts strictly greater than that threshold. Thus the identifier value ten means **at least eleven captured games**, not at least ten. Subsequent reconciliation located the primary archived exchange: after being told that tightening would remove twenty-three additional team-seasons and no additional drafted player-seasons, Charles wrote, “I think we should go with 10 to get real seasons,” and authorized the changes. Six was therefore the working rule, eleven was tested, and Charles adopted eleven at that point. [H4–H5; C1–C2; H14]

**The source files were to remain preserved.** These were analytical construction rules applied when rebuilding the panel, not an instruction to erase rows from the frozen source extract. A prebuilt-panel option can bypass that rebuild, so a current default alone does not prove that an older output received the cleaning. [H4]

## 4. What the recorded curve comparison actually says

SCOUT's August 19 exchange reports that the coverage exclusion removed 45,332 aggregated player-season records, representing 30,396 distinct athletes and 2,715 team-seasons in that audit. It reports one ever-drafted athlete among excluded records: Derrick White, whose one-game Colorado Springs observation was removed while a later Colorado season remained. These are SCOUT's reported audit results. They have not been independently reproduced here. [H5, B1–B4]

The small number of drafted athletes removed does **not** mean that draft rates or their interpretation were unaffected. A rate depends on both its numerator and its denominator. For an illustrative example, ten drafted players among one hundred observations is ten percent; the same ten drafted players among two hundred observations is five percent. Adding or removing undrafted observations can therefore change a curve considerably without changing its drafted count.

The August 19 comparison makes the composition issue concrete:

- In the pre-cleaning reconstruction with sixteen equal-count peer-quality bins, the highest bin reportedly contained **2,557 excluded records out of 3,886**, or **65.80%**.
- Across bins thirteen through sixteen, the corresponding reported fraction was **30.93%**.
- After cleaning, SCOUT reported rates of **2.63%, 2.73%, 2.90%, 3.25%, and 3.21%** in bins twelve through sixteen, with 2,894 observations in each listed bin. [H5, B5–B6 and B5a]

These reports support a substantial change in the composition of the upper tail and a much weaker final-bin decline. They do not independently establish the complete numerical effect of the coverage rule alone: reconstructing matched figures requires their full specifications, intermediate population definitions, transformations, and execution records.

There is an arithmetic inconsistency in the exchange: the table reports **65.80%**, while later COMPASS prose says **66.8%**. The table's numerator and denominator support approximately 65.8%. We preserve the discrepancy rather than repeat both as equally supported.

Also, recomputing the panel may change season-standardized ability, teammate means, and bin boundaries, not just delete observations from otherwise fixed bins. The mechanism by which cleaning changes the figure needs to be traced through that entire sequence. The saved descriptions are insufficient for a new causal claim that congestion is absent, present, or wholly explains a particular downturn.

## 5. How a saved team could have only two retained players

Suppose the dataset contains only one game for a team. Two players have at least twenty observed minutes; everyone else has fewer. Applying an individual twenty-minute floor without first excluding that poorly covered team could leave just two rows. That is an illustrative route to a two-player analytical roster, not a claim that the basketball team actually had only two players.

The saved roster summaries inspected earlier in this discussion differ substantially:

- The older Grandchild 2015 roster file contains 6,030 rows across 635 teams, with a minimum roster size of two and six teams of size two.
- The saved 2015 summaries using the later twenty-minute construction contain 4,270 rows across 351 teams, with a minimum of nine.
- A saved after-cleaning version without the individual twenty-minute floor contains 5,747 rows across 351 teams, with a minimum of eleven.

The source files are listed below. These are descriptions of existing saved artifacts, not a newly rebuilt population. Their exact construction histories still need reconciliation. None of these totals should become an acceptance target that forces a fresh construction to match an old file.

The six team identifiers in the older size-two group are 2069, 2800, 2827, 3086, 3166, and 108818. Their individual captured-game counts, excluded-player records, and source versions have not been traced here. That remains a focused question for SCOUT.

Two corrections to VECTOR's earlier code explanation also matter:

1. The capacity loader calls the panel-preparation function and then counts retained rows by team. A separate minimum-of-two setting is applied in the interval-display function. That setting does not explain how each two-player roster arose and is not the same as the loader's population definition. [C4–C5]
2. The rebuild assigns the draft indicator by membership in the matched draft lookup. Unmatched identifiers become zero; the operation is not simply “drop everyone with missing draft information.” Whether zero reliably means undrafted depends on lookup coverage and linkage. [C2]

## 6. Decisions change the measured mechanism, not just the presentation

For a player whose standardized performance is $A_i$, leave-one-out mean teammate performance is

$$
L_i=\frac{\sum_{k\in g(i)}A_k-A_i}{n_{g(i)}-1},
$$

where $g(i)$ is the player's retained team roster and $n_{g(i)}$ is its number of retained players. A roster of one gives no defined teammate mean. A roster of two makes each player's teammate mean equal to the other player's value.

Removing whole poorly observed team-seasons changes which environments exist in the population. Removing low-minute individuals can change the teammate environment of players who remain. Standardizing performance using a changed season population can change the numerical values again. These changes can affect observed sorting and the reference scale for congestion in our new experiment.

In the current rebuild, the individual minute floor is applied before the subsequent performance standardization and teammate calculation. Later filtering can still change the final set of observations. We must record the population used for each transformation rather than assume every exported ability column has mean zero and standard deviation one in every final subset. [C2–C4]

Historical notes also distinguish a full retained roster used to construct team context from the final-season-per-athlete observations used to display a draft curve. The later named hero uses the latter; roster-size and overlap diagnostics use full retained team-season rosters. Using only final-season players to populate the assignment experiment would change its capacities and peer environment. [H10–H11]

## 7. Earlier modeling decisions that should remain intelligible

The June SCOUT report already distinguished an inverted-U on **team mean ability** from a different pattern on **leave-one-out teammate ability** under the same model settings. Changing the horizontal axis is therefore not merely relabeling the same scientific result. That report also distinguishes older ordered assignment and noisy scoring from later assignment and selection implementations. It is useful history, not the current experiment specification. [H7]

SCOUT's historical notes record an objection to imposing artificial playing-time allocation in the assignment simulation: minutes may themselves be an outcome of competition within a team. That concern belongs in our intellectual history even though it does not settle how to define observed ability or eligibility now. The notes also record fixed-size rosters versus observed filtered capacities, and why they can represent different populations. [H6]

The notes describe noise in assignment, noise in scores, and later stochastic selection. These are distinct operations. The new investigation's deterministic selection after scoring is an explicit design decision; it should not be described as a reproduction of all earlier stochastic models.

The August named-hero record distinguishes a binned tail drop from a positive global quadratic coefficient of about $+0.00172$. Those can coexist. It also reports empirical-roster replay and calibration results, but their probability rules and parameter transfer remain subject to the earlier model-specification review. Historical fitted parameters or plotted successes are not automatically transferable to our new experiment. [H11]

The August conditional-ability campaign review explicitly warned against making restoration of a final-bin dip the success criterion. The present investigation should likewise ask whether congestion changes outcomes under stated conditions, while separately evaluating any agreement with empirical curve shape. [H12]

## 8. Unresolved historical discrepancies

**Dropping low-minute players versus retaining them with zero points per minute.** In the original Paper Directions 23 transcript, the exchange at approximately 28:47–29:26 shifts from “you're out” to “it's zero.” SCOUT's derived notes explicitly interpret this as a garbled closing and state that dropping observations below twenty minutes remained the adopted production policy. The current construction and later hero specification support a dropping policy, but the original exchange does not independently establish the notes' interpretation. We need the clarifying conversation, approval, or run record. [H8–H9; H11; C2]

**“The inverted U survived” versus the weak or absent global hump.** Charles's opening account in that transcript says cleaning did not eliminate the inverted-U result; the August 19 equal-count-bin table and the later named hero give more qualified descriptions. These might concern different figures, settings, dates, or meanings of “survived.” The actual slides and matched execution records must resolve the referents. [H5; H8–H11]

**Threshold documentation and fallback behavior.** Some policy prose still describes the earlier threshold of five. More than a comment is involved: the filtering helper uses five as its fallback if a configuration object lacks the threshold attribute, while the ordinary configuration object supplies ten. We have not found evidence that the fallback caused a particular historical result. Explicit configuration is necessary for future provenance. [H4; C1–C2]

**Stale roster example.** The rollout/policy prose describes a three-game Jarvis roster as still in the panel, which is inconsistent with either of the stated whole-team coverage thresholds unless it describes an earlier stage or different construction. [H3–H4]

**Meeting date.** The Paper Directions 23 filename begins with September 18, but its internal header says August 18, 2026 and the derived note uses August 18. Use the internal date with this discrepancy disclosed; do not silently rename the source. [H8–H9]

**Regeneration lineage.** A current script or completed checkbox does not establish which saved plots used which threshold, minutes policy, or source snapshot. Those mappings remain incomplete.

## 9. Consequences for the new investigation

Charles selected 2015, observed roster capacities, and a fixed observed-team reference for congestion standardization. He has not yet approved a fully specified eligible-population construction. The coverage/minutes history must inform that decision before the panel and capacities are frozen.

Charles also prefers fresh outputs for this investigation. Historical sweeps and roster exports are evidence to understand past work; they will not be experimental input populations or resumed runs. Any future derived inputs and results belong inside the sequestered investigation workspace and require explicit execution authorization. Existing source extracts can be identified as candidate inputs without changing or rebuilding them now.

The smallest next step is documentary: obtain SCOUT's evidence-based response, reconcile the population and transformation history, and then return to one design question at a time. No new simulation is needed to answer the questions that can be resolved from existing records.

## 10. Sources actually inspected

A source document saying “verified” is evidence of the author's reported verification. It is not a claim that VECTOR has reproduced the computation. Selected transcript and archived-conversation passages are identified as such; this review does not claim to have read the entire SCOUT corpus.

- **H1:** [3-Master_Plan/20260817_1606_Charles_to_SCOUT_espn_dash_placeholder_rows.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/20260817_1606_Charles_to_SCOUT_espn_dash_placeholder_rows.md>). Full document; Charles's original questions about placeholders and anomalous rosters.
- **H2:** [3-Master_Plan/20260817_1610_SCOUT_to_COMPASS_espn_dash_placeholder_rows.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/20260817_1610_SCOUT_to_COMPASS_espn_dash_placeholder_rows.md>). Full document; SCOUT's source-check report, not a new ESPN verification by VECTOR.
- **H3:** [3-Master_Plan/20260817_1650_SCOUT_to_COMPASS_box_qc_rollout_and_regen.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/20260817_1650_SCOUT_to_COMPASS_box_qc_rollout_and_regen.md>). Full document; initial six-or-more-game policy and reported rollout.
- **H4:** [3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md>). Full document; later eleven-or-more-game policy alongside older unrevised passages.
- **H5:** [3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md>). Full document; August 19 exclusion and curve reports, including conflicting percentages.
- **H6:** [sports/documents/Pertinent_Thoughts_Scout.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/documents/Pertinent_Thoughts_Scout.md>). Full document; historical minutes, measurement, binning, model and advisor reasoning. Its recorded priorities are historical.
- **H7:** [3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md>). Full document; June model/axis history. Its obsolete location matters.
- **H8:** [transcripts/20260918_Paper_directions_23_otter_ai_transcript.docx](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/transcripts/20260918_Paper_directions_23_otter_ai_transcript.docx>). Selected original transcript passages read as text, especially the opening, 08:48–10:58, 16:20–23:46 and 28:41–30:26. Internal date: August 18, 2026; filename: September 18.
- **H9:** [transcripts/PD23_notes.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/transcripts/PD23_notes.md>). Full derived meeting note. Its interpretation of the closing transcript remains to be substantiated.
- **H10:** [3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260827_SCOUT_to_COMPASS_2009_21_aperture.md>). Full document; later season-window and final-season population decisions.
- **H11:** [3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md>). Full document; named hero specification, population split, and reported calibration/replay results.
- **H12:** [3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260821_SCOUT_CCT_campaign_review.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/SCOUT_and_COMPASS/20260821_SCOUT_CCT_campaign_review.md>). Full document; conditional-ability review and warning against treating restoration of the final-bin dip as the objective.
- **H13:** [.specstory/history/2026-05-24_12-52-09-0400-scout.md](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/.specstory/history/2026-05-24_12-52-09-0400-scout.md>). Targeted excerpts only: Charles's request near lines 25835–25890, archived game-count output near 25955–26190, and recorded ESPN spot-check output near 30275–30465. Historical commands were read, not executed.
- **H14:** [archived decision exchange](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/.specstory/history/2026-06-11_08-19-11-0400-compass.md:215669>). Primary archived exchange for testing and adopting the stricter eleven-captured-game rule; historical commands embedded in the archive were not executed by VECTOR.
- **C1:** [sports/sports_pipeline/config.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/sports_pipeline/config.py>). Static source inspection: normal configuration defaults.
- **C2:** [sports/sports_pipeline/panel_rebuild.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/sports_pipeline/panel_rebuild.py>). Static source inspection: game-coverage filtering, aggregation, minutes, and draft lookup.
- **C3:** [sports/sports_pipeline/panel_build.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/sports_pipeline/panel_build.py>). Static source inspection in the population review: ability standardization, peer means, and final filtering.
- **C4:** [sports/scripts/empirical_team_interval_overlap.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/scripts/empirical_team_interval_overlap.py>). Static source inspection: panel preparation and separate interval-display roster minimum.
- **C5:** [sports/541_grandchild_homophily_assign.py](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/sports/541_grandchild_homophily_assign.py>). Static source inspection: empirical ability/capacity loader.

### Saved roster artifacts inspected earlier in this discussion

These were read as historical tabular records; they were not regenerated.

- [3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_ncaa_roster_size_by_team_season_2011_2021.csv](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/GRANDCHILD_ncaa_roster_size_by_team_season_2011_2021.csv>)
- [3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_by_team_season_2011_2021_min20.csv](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_by_team_season_2011_2021_min20.csv>)
- [3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_by_team_season_2013_2021_after_qc_min20.csv](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_by_team_season_2013_2021_after_qc_min20.csv>)
- [3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_by_team_season_2013_2021_after_qc_raw.csv](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_raw_roster_size_by_team_season_2013_2021_after_qc_raw.csv>)

## Companion document

[Questions for SCOUT — data hygiene, population, and model history](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_questions_for_SCOUT.md>). Charles can pass that document to SCOUT; VECTOR has not contacted SCOUT or initiated another agent's work.
