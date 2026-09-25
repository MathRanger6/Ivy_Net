# VECTOR to SCOUT — basketball data hygiene and model history

**Prepared:** September 25, 2026  
**Revised after Charles's answers:** September 25, 2026  
**For:** Charles to pass to SCOUT  
**Purpose:** Recover the reasoning and evidence behind earlier population and modeling decisions before VECTOR freezes the input population for a new assortativity investigation.

## Scope and requested response

Charles reminded VECTOR of the one-game-opponent problem: a team's single captured game was entering as if it represented a season. Cleaning substantially changed the empirical curve. VECTOR had inspected current code and saved summaries without adequately absorbing that history.

Please answer from existing documents, conversations, source code, and saved execution records. Separate direct evidence, previously computed results, recollection, interpretation, and unresolved questions. Give repository paths, relevant sections or transcript timestamps, and exact artifact names where possible. A previous note saying “verified” is useful history, but identifying the underlying saved evidence is more helpful.

This request is for historical explanation and documentary reconciliation. It is not a request to run new analyses, regenerate plots, change source files, restore a preferred curve, or revive old sweeps. If answering an item requires new execution, please identify the missing evidence and proposed check for Charles to consider separately.

A detailed statement of what VECTOR has already read is in [VECTOR's history review](</Users/charleslevine/Library/CloudStorage/Dropbox/1-Documents/00- Dissertation/0-Next_Chapter/Code_and_Data/New SQL and PY Code/Cursor Workspace PDE/3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_data_hygiene_and_model_history.md>). A reply can follow the numbered sections below. If Charles authorizes a saved response, a companion file in this same documentation folder named **ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md** would keep the exchange together.

## Charles's answers and present recollections

VECTOR asked Charles the questions that could reasonably be answered before sending this request. His answers should guide the historical search, but they should not be treated as substitutes for the underlying records:

1. **Low-minute players:** different analyses used different policies. Some removed players with fewer than twenty total recorded season minutes, while others retained them under a zero-points-per-minute treatment. Charles no longer remembers the rationale for assigning the policies to particular analyses and expects SCOUT to recover it thoroughly.
2. **Before-and-after curve comparison:** Charles remembers the minimum-games rule as the only change between the relevant pre-cleaning and post-cleaning plots. SCOUT should identify the exact paired artifacts and verify whether the saved specifications support that recollection.
3. **Scientific concern behind the game-coverage rule:** Charles remembers that sparsely captured weak teams could receive an exaggerated measured team-quality value, denoted historically as $T_j$. His concern was therefore more specific than simply removing unusual small-school observations or approximating a Division I membership list. SCOUT should explain the mathematical and data-construction route by which fragmentary capture exaggerated $T_j$, identify whether the distortion was upward, and show how that moved observations along the plotted horizontal axis or changed other derived quantities.

Please distinguish what these recollections correctly identify, what needs qualification, and what the preserved evidence cannot establish.

## 1. What led from the one-game discovery to the final coverage threshold?

The initial August 17 rollout drops team-seasons with five or fewer captured games. The later policy and current normal configuration drop ten or fewer, retaining at least eleven.

Please identify the original decisions supporting both thresholds and the reason for moving from five to ten. What alternatives were considered? What evidence concerned season coverage, player-performance reliability, or observed curve shape? Was eleven selected before inspecting its curve, after sensitivity checks, or for a practical convention?

Please distinguish captured games in the extract, games available from ESPN, and games actually played. The saved forty-team-season spot check supports a source-coverage issue for most sampled cases, but does not establish complete season coverage or official division membership.

Charles remembers that fragmentary coverage exaggerated $T_j$ for weak teams. Please reconstruct this mechanism carefully. Define the exact historical $T_j$ used in the affected plots; identify the observations that made it too large; explain whether the distortion arose from opponent sampling, player inclusion, minutes, within-season standardization, aggregation, or a combination; and distinguish a documented result from a plausible explanation.

## 2. Which exact figures demonstrate the change Charles remembers?

Please identify the pre-cleaning inverted-U figure and its comparable post-cleaning figure, with their source snapshot, code/configuration, run record, and saved bin counts.

Charles remembers that these were otherwise identical plots and that only the minimum-games rule changed. Please test that recollection against the saved provenance. For each figure, specify season window, minutes policy, team coverage rule, ability transformation, teammate calculation, any trimming of extreme teammate values, draft outcome definition, focal observation rule, and binning. State plainly whether all settings except the coverage rule were held fixed. Also state whether season standardization and bin boundaries were recalculated as consequences of applying that one rule; those downstream recalculations would be part of the treatment even if no other setting changed.

The August 19 exchange reports 2,557 excluded records among 3,886 observations in the highest pre-cleaning bin, and post-cleaning rates of 3.25% then 3.21% in the last two bins. Where are the saved records underlying those statements? The same exchange alternates between 65.80% and 66.8%; please clarify the intended number.

## 3. How was the individual minutes policy decided?

Charles confirms that different analyses used different policies: some dropped players below twenty total season minutes, while others retained them under a zero-points-per-minute treatment. He does not remember the rationale now and expects SCOUT to explain it thoroughly.

Please recover the arguments, observations, and decisions behind each policy. Map each policy to the analyses in which it was used, including roster construction, assignment calibration, measured assortativity, and the displayed draft curve. Explain whether a retained low-minute player entered teammate context, the focal sample, or both. Identify which policy was primary, which was a contrast or sensitivity analysis, and whether that status changed over time.

The original Paper Directions 23 transcript at approximately 28:47–29:26 appears to switch from dropping players to assigning zero. The derived notes call that closing garbled and explicitly retain the dropping policy. Please identify the contemporaneous clarification supporting that interpretation, or mark it as unresolved recollection.

The transcript also occasionally says “per game,” whereas current construction uses total season minutes. Please identify any historical implementation that actually used a different unit.

## 4. What caused the old two-player analytical rosters?

The older Grandchild 2015 file has 635 teams and 6,030 retained rows, including six two-player teams with identifiers 2069, 2800, 2827, 3086, 3166, and 108818. Later saved twenty-minute summaries have 351 teams and 4,270 rows, with minimum roster size nine.

If existing audits permit, please trace the six cases: captured games, recorded players, retained players, exclusion reasons, and source/construction version. Were they one-game opponent appearances, another coverage issue, or something else? Please do not infer the answer merely from their roster size.

Are the later saved totals comparable apart from cleaning, or do season windows, other filters, source versions, or population definitions differ? We will not require a fresh construction to reproduce an old count merely because it is saved.

## 5. Which population supplied each transformation and analysis?

Please document the historical order: placeholder removal, team coverage filtering, aggregation, individual minutes filtering, season standardization, teammate calculation, any trimming of extreme teammate values, and final focal-row selection.

In particular:

- Was ability standardized over all retained player-season-team records or over a narrower analytical subset?
- Were full eligible rosters used to construct context before selecting each athlete's final season for the displayed curve?
- How were transfers or multiple teams within a season handled?
- Which exported objects retain player identifiers and unique row definitions suitable for preserving identity in a new assignment experiment?
- Did any relevant run use a prebuilt panel that bypassed the later cleaning?

Please distinguish the current implementation from historical variants.

## 6. How should we interpret the draft indicator and excluded athletes?

The current rebuild assigns one to an identifier found in the matched draft lookup and zero otherwise. What coverage/linkage checks justify interpreting unmatched cases as undrafted rather than unlinked or not yet observed?

Please locate the saved basis for the report that only Derrick White was ever drafted among the distinct athletes with excluded team-season observations. Was the denominator defined before or after the individual minute filter? Did the statement concern people, player-seasons, or final-season observations?

The small number of drafted observations lost does not imply unchanged draft rates: removing undrafted denominator observations can materially change them. What limits did you and Charles recognize at the time?

## 7. How do the changing descriptions of the empirical curve fit together?

The original meeting account says the inverted U survived cleaning. The August 19 equal-count-bin report shows a much weaker final-bin decline. The later named hero uses 2009–2021, final-season observations, sixteen equal-width bins, and reports a positive quadratic coefficient near +0.00172 while retaining a “tail drop” label.

Please map those statements to their actual figures and specifications. Were they different populations, different binning, simulations versus observations, or different meanings of “survived”? Please keep local tail behavior distinct from global quadratic curvature.

The original Paper Directions 23 file has a September 18 filename but an August 18 internal date. Please confirm the intended chronology without renaming the source.

## 8. Which old modeling choices best explain the intellectual history?

Please point VECTOR to the most useful decision records for:

- Ordered assignment versus the later Levine–Gates assignment process; fixed-size rosters versus observed filtered capacities.
- Team mean ability versus leave-one-out teammate ability as the displayed horizontal axis.
- Noise in assignment, noise in scoring, and stochastic selection after scoring.
- Automatic congestion scaling, treatment of negative scores, selection temperature, and whether the number selected was fixed.
- Historical Pass A/B/C labels and their changes across campaigns.
- Why artificial playing-time allocation was rejected or deferred, and how measured points per minute was understood as potentially reflecting the team environment.

Please explain the reasons and limitations, not just the final settings. Our new deterministic selection design need not copy those choices, but should not accidentally misrepresent them.

## 9. What was regenerated, what remained historical, and what is still missing?

Please identify which principal post-cleaning outputs have a saved execution record and which were merely planned, requested, or reported completed. Include any known outputs still based on the older population.

Two specific documentation issues need clarification: the description of a three-game Jarvis roster as still included despite the exclusion rule, and the code's fallback threshold of five when a configuration object lacks the threshold attribute, despite ten in the normal configuration. Did either affect an actual run, or are these remnants without a known result consequence?

Finally, recommend the few original records VECTOR should read next to understand your and Charles's reasoning. Please flag missing logs, source snapshots, or ambiguous recollections plainly.

## Present boundary for the new investigation

Charles has chosen a fixed 2015 population in principle, observed capacities, and several controlled model settings. Its exact eligible population is not yet frozen. Historical generated outputs are reference evidence, not inputs to be reused or overwritten. This exchange is intended to make the next population decision informed and explicit; it is not execution authorization.
