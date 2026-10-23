# Dissertation work map and current model chapter outline

**Updated:** 13 October 2026. Originally prepared after PD44 on 30 September.  
**Purpose:** Keep the dissertation’s developing structure, current writing, and possible additional chapters in one place.  
**Status:** Working plan for Charles. Alex’s documented proposals, Charles’s subsequent decisions, and our proposed next steps are distinguished below. This is not an approved final table of contents.

The dissertation connects the science of success with network science: people perform and pursue advancement within groups, and the composition of those groups may affect who receives scarce opportunities. Army, basketball, education, and academic careers supply possible evidence and examples. The dissertation should remain organized around the scientific question rather than become an account of one domain.

Our immediate writing task remains the model chapter. Its current draft now develops the naïve benchmark before adding uncertainty, competitive congestion, and artificial group formation. A separate Levine–Gates (LG) exploration has also developed far enough to warrant reserving a possible chapter, while its eventual claims and place in the dissertation remain open.

## 1. What Alex proposed

### PD44 on 30 September

Alex described three central **content chapters**, with introductory and surrounding material bringing the dissertation to roughly five chapters. His “first,” “second,” and “third” refer to those content chapters, not settled dissertation chapter numbers.

1. **Establish the empirical phenomenon.** Explain the relationship among individual performance, group environment, and advancement. At 02:52 he recommends bringing together evidence from several datasets, including comparisons among people with similar performance and the band of excellence.
2. **Develop the model.** Explain its construction, assumptions, parameter behavior, and completed investigations in dissertation-level detail. At 05:56–08:43 he distinguishes this detailed treatment from the much shorter account an eventual paper would contain.
3. **Connect the model to the evidence.** At 06:31 he identifies maximum likelihood estimation and fitting the model to data as the next content chapter. This is a research destination, not a declaration that the fitting bridge is already complete.

At approximately 09:10–11:31, Alex also supports preserving the Army work on defining success, promotion timing, and survival or competing risks. He suggests that this could become a chapter before the peer-effects discussion. He does not settle its final placement.

At 12:24 he recommends starting the writing with the model chapter. Writing should reveal specific missing analyses; it should not wait for every empirical problem to be resolved.

**Primary source:** [PD44 transcript](../../../transcripts/20260930_Paper_Directions_44_otter_ai_transcript.docx).

### PD45 on 7 October and the email on the first draft

Alex’s later guidance changes the model chapter’s exposition, not the distinction between scoring and selection. PD45 recommends starting with the simplest performance-based selection model and adding complexity as the reader encounters a reason for it. Assignment comes later as a way to construct groups for simulations; the advancement model can begin with groups already observed.

His email likewise says not to introduce ASSIGN as an equal part of the scientific model, to reduce repetition, and to move the internal development-history account out of the main scientific narrative. Detailed mathematics still belongs in the dissertation when it explains the model or supports a claim.

Charles clarified that Alex’s concern about “separating environmental effects from later selection” should not be read as merging SCORE and SELECT into a single operation. They remain mathematically distinct; explaining advancement requires considering their combination.

**Sources:** [PD45 transcript](../../../transcripts/20261007_Paper_Directions_45_otter_ai_transcript.docx); Alex’s email reproduced by Charles in this conversation; [the October 8 change memo](Model_Chapter_PD45_Change_Memo_20261008.md). The email is identified as conversational evidence rather than an independently located email file.

### Framing recorded by Charles

[Dissertation Tone](Dissertation%20Tone.docx) records Charles’s account of a conversation with Alex. It emphasizes the bridge between network science and the science of success, the balance of readable narrative with mathematical development, and the need to return from domain examples to the general phenomenon. This is Charles’s written account, not a verbatim transcript.

## 2. Our current proposed dissertation arrangement

The following is **our updated planning arrangement for discussion**, not a chapter list approved by Alex. We retain the working label “Chapter 4” for the manuscript already in progress. We should choose final numbers only after deciding whether the Army methods and LG contributions stand alone.

### Introduction and literature

Set out the scientific question and connect work on success, peer environments, group composition, and scarce advancement. Define what the dissertation contributes beyond demonstrating that strong individuals tend to be surrounded by other strong individuals.

**Basis:** Alex explicitly calls for introduction and literature material in PD44. The wording and scope here are our proposed organization.

### Measuring advancement and the empirical phenomenon

Establish how success is measured and then describe the observed patterns across suitable domains. Explain population definitions, time windows, group membership, performance measures, and which comparisons hold own performance approximately fixed. Describe similarities and differences across domains without assuming all show one identical effect.

**Basis:** This is Alex’s first central content block. Our proposed treatment keeps measurement and source limitations close to the claims they qualify.

**Possible separate Army methods chapter:** Preserve the work on promotion timing, attrition, censoring, survival, and competing risks. If it contains a sufficiently distinct methodological contribution, place it before the empirical peer-effects chapter. Otherwise retain a substantial methods section and appendix. Alex supported the possibility; the separate-chapter decision is still open. Verify which estimators were actually fitted before naming them as completed work.

### The congestion and advancement model

This is the current **Chapter 4**, described in Section 3 below. Begin with the naïve performance-only benchmark, introduce uncertain selection, develop congestion, examine its mathematics, and then explain how artificial groups are generated.

**Basis:** Alex’s model content block, revised through PD45 and Charles’s subsequent editing decisions. Assignment remains a simulation device within this chapter even if LG receives a separate chapter elsewhere.

### Possible chapter on LG and group formation

Study how metadata-based attachment preference and prescribed roster capacities produce group composition. Then compare clearly identified alternatives that change the opportunity rule or relax fixed roster sizes.

**Basis:** Charles’s later proposal and the separate LG exploration specification. We have not verified an explicit endorsement from Alex of a separate LG chapter. The executive summary calls it a possibility for discussion.

**Proposed placement:** After the core advancement model and before the model-to-data chapter is a useful working option. It would let the main model chapter explain the assignment algorithm briefly, while the LG chapter develops group formation as its own scientific subject. Placement remains open; avoid duplicating the same derivation and figures in both chapters.

### Connecting the model to evidence

Explain the historical fitting work, what it estimates, and what is still needed to connect those estimates to the intended model. Distinguish empirical fitting, simulation-based parameter recovery, and counterfactual claims.

**Basis:** Alex’s third central content block. A completed exact-K refit or validated counterfactual analysis is not currently established by the sources reviewed for this map. Chapter 4’s present Section 4.8 introduces this bridge; it need not duplicate an eventual full fitting chapter.

### Synthesis and conclusions

Bring the theoretical and empirical contributions together, state their limits, and identify the next scientific questions. A synthesis chapter is our proposed completion of the structure, not a separately verified detailed instruction from Alex in PD44.

This arrangement deliberately leaves the final chapter count open. Adding both Army methods and LG as standalone chapters would expand Alex’s initial rough five-chapter conception; we should make that an explicit discussion rather than silently relabel his original proposal.

## 3. Where the model chapter stands now

The authoritative manuscript is [Model Chapter Shared Working Draft](Model_Chapter_Shared_Working_Draft.docx). The Markdown and LaTeX copies are earlier working versions, not automatic substitutes for Charles’s current Word edits. This map records the current headings and direction; it does not certify that every paragraph is finished.

### 4.1 Individual performance and success in groups

Introduce the phenomenon in ordinary language and connect it to the dissertation’s network-science question. Establish why later selection matters without presenting every mechanism and parameter before the reader needs them.

### 4.2 Selecting the highest performing individuals

Develop the **naïve benchmark**: measured performance supplies the score, the eligible population contains N individuals, and deterministic selection awards K opportunities to the highest scores. Introduce notation before using it and explain what group membership does and does not change in this benchmark.

### 4.3 Allowing uncertainty in selection

Explain why winners may differ even when supplied scores are unchanged. Define exact-K sequential selection using Gibbs weights, including the conditional probability of each next draw, removal of selected individuals, temperature, and limiting cases. Selection temperature is distinct from the parameter in the historical fitting equation.

### 4.4 Introducing local competitive congestion

Begin with average peer performance as an approximation, then motivate credible competitors and their smooth competitive relevance. Explain the conscious choice to average relevance over the full group, including the focal individual, producing shared roster pressure. Keep group mean T_j, leave-one-out quantities, individual relevance, and shared congestion C_j distinct. Explain why a common group penalty changes cross-group comparisons but cancels in rankings within a group under a fixed local selection quota.

### 4.5 Mathematical behavior and parameter regimes

Develop threshold location, transition sharpness, penalty strength, score scale, scarcity, and selection margins. Charles’s later direction emphasizes domains with scarce opportunities and broadly aligned scarcity and relevance thresholds. Mathematically permissible independent changes to K and theta need not receive equal narrative attention. Describe historical experiments according to what they actually held fixed; do not retroactively relabel their designs.

The figure work now includes illustrations of relevance curves, score crossings and winners, and scarcity changing together with a threshold. Illustrative inputs are not empirical estimates or newly established historical findings.

### 4.6 Generating artificial groups with controlled sorting

Explain fixed roster capacities, sequential metadata-based assignment, evolving group centroids, and measured sorting. The current figure notebook also illustrates assignment step by step. This section supplies enough construction detail to understand the congestion experiments; a possible LG chapter can carry the more extensive group-formation investigation.

### 4.7 What the completed mechanism experiments establish

Retain the documented experiments and their scientific limits. Distinguish changed winner identities from a downturn in a plotted curve; report support and sensitivity to binning. Identify settings and implementation versions for figures before treating them as evidence for the current mathematical definition.

### 4.8 The bridge to empirical fitting

Explain that historical estimation used observed rosters and a season-wise softmax probability inside an independent Bernoulli likelihood. That fitting model differs from exact-K selection without replacement. The saved joint estimates concern gamma, lambda, and the fitting temperature; threshold construction and assignment calibration require their own explanation. Preserve the unresolved questions about the fitted sample, outcome timing, normalization, and parameter transfer.

### Appendices 4A and 4B

Appendix 4A retains technical qualifications, the historical fitting record, and consequential differences between earlier implementations and the stated model. Appendix 4B records sources for equations and completed results. Repository provenance supports traceability but does not replace scholarly citations. Keep implementation history out of the main narrative unless it changes how a result must be interpreted.

## 4. The LG chapter possibility and its present status

### Scientific purpose

The original LG model combines attachment preference based on individual and group metadata with **fixed prescribed roster sizes**. Remaining seats represent available assignment opportunities, not attraction to high degree. A separate chapter could establish what this combination contributes to sorting, variation within and between teams, and the concentration of credible competitors.

Relaxing fixed rosters changes the model. The exploration should name each alternative and explain its kernel instead of treating every variant as LG.

### What is documented now

The October 6 [executive summary](LG_Model_Exploration_Executive_Summary.docx) and [handoff](LG_Model_Exploration_Agent_Handoff.md) set out the proposed study. The newer [LG decision log](lg_exploration/documents/LEO_DECISION_LOG.md) records subsequent implementation and Charles’s approvals. It supersedes the handoff’s statements that the working code has yet to be built.

A working [composition notebook](lg_exploration/notebooks/01_composition_opportunity_rules.ipynb), Python modules, and settings files now exist. The decision log reports completed saved divisions for the first fixed-roster composition comparison. It also records contender-count diagnostics, an uncapped extension, alternative initial attachment signals and mean-versus-sum signals, and an optional one-plus-members opportunity multiplier. That last option introduces a size-dependent preference and must be distinguished from original fixed-roster LG and from uncapped metadata-only assignment.

This update inspected the implementation inventory and decision record; it did not rerun experiments or independently audit those saved results. The existence of code or a plotting option is not evidence that a scientific conclusion has been established.

### Proposed chapter development

1. Define fixed-roster LG and its scientific question.
2. Explain and compare the assignment opportunity rules while holding populations and relevant constraints constant.
3. Present verified composition and sorting results with repetitions and uncertainty described correctly.
4. Treat relaxed capacities and other attachment kernels as explicit extensions, identifying which assumption changes in each comparison.
5. Connect selected group-formation findings to congestion and advancement only where the scoring and selection analyses have actually been completed.
6. Use synthetic parameter recovery to diagnose fitting when the generating and fitted probability models are specified and aligned.

The last two items remain planned stages in the reviewed materials, not completed results certified here. Matching-model recovery should precede claims about fitting data generated under another selection rule. This map does not authorize new sweeps, fits, or high-performance-computing jobs.

### Decision still needed

Charles and Alex should decide whether the verified LG findings support a distinct chapter with its own question and conclusion. Until then, reserve the possibility and preserve the work, while maintaining the short assignment explanation in Chapter 4.

## 5. Empirical work alongside writing

### Romania

Romania has progressed well beyond the initial Alba-only acquisition described in the September map. Charles has authorized additional county acquisition, reconciliation, and descriptive plots in subsequent work. Sources now include school-level results, admitted and unassigned or rejected lists, and cross-county information. Each source type still needs its own completeness and linkage checks.

The current background priority is to preserve and assess those downloads, keep unresolved records open, and distinguish download progress from reconciliation and eligibility for analysis. A county whose placement reports reconcile is not thereby proven to have a complete origin-school applicant population. Incoming and outgoing students require explicit treatment; an unmatched student must not automatically count as an unsuccessful placement.

The historical source gates remain relevant, but the September statement that no outcome exploration has been authorized is no longer an adequate description of subsequent county work. Existing descriptive analysis permissions do not constitute blanket permission for a new national outcome model. Charles controls execution and any expansion in scientific scope.

A dedicated [offline county progress notebook](education_analysis/notebooks/EDUCATION_20261013_Romania_2001_county_progress.ipynb) now summarizes acquisition and reconciliation from saved records. Run its settings and refresh cells once, then rerun the refresh cell whenever an updated table is needed. Its role is monitoring, not resolving uncertainty by labeling missing data permanently unavailable. This map does not assert a current complete-county count or restart any worker.

### Army, basketball, and academic careers

Preserve domain-specific measurement and methodological work. The dissertation can compare domains without assuming identical outcomes, sampling, or peer definitions. Army survival and competing-risk work remains dissertation-relevant even if an eventual paper compresses it. The historical basketball fitting and mechanism experiments need separate accounts. Further academic-career claims depend on the evidence actually available, not the intended breadth of the eventual dissertation.

## 6. Immediate writing sequence and remaining decisions

**Agreed direction:** Continue the current Word model chapter, with readable introductions before mathematical definitions and enough derivation for the committee to assess the claims. Charles’s current edits take precedence over older outlines and status notes. Preserve source records and backups.

**Our proposed next sequence:**

1. Finish the current pass through Chapter 4, including the distinction between completed experiments and the fitting bridge.
2. Inventory which empirical figures and claims can support the phenomenon chapter, including their population definitions and unresolved limitations.
3. Review the LG exploration’s verified results and decide whether its independent contribution warrants a chapter.
4. Decide the placement of the Army methodological material and the final chapter numbering with Alex.
5. Address only the specific missing analyses required by a proposed scientific claim. Record the question, what evidence already exists, and the smallest necessary additional investigation.

The immediate scientific questions still include the effect of earlier score clipping and selection caps on reused results; historical fitting-window and outcome-label definitions; threshold and normalization choices; transfer or refitting between probability models; and the empirical interpretation of cross-county student movement. They should remain visible without turning this work map into an authorization for broad experiments.

### NCAA roster pressure comparisons for an evening session

**Added October 21, 2026. First descriptive comparison completed October 23, 2026, at Charles’s request.** The manuscript is unchanged; no additional significance tests were run.

- [x] Build a notebook comparison of the empirical NCAA HERO plots corresponding to basketball mosaic panels 7, 8, and 9. Use actual observed draft outcomes, not simulated winners.
- [x] First identify each panel’s current population, season window, own-performance bands, peer roster, and outcome definition from the existing notebook. Preserve those definitions within each side-by-side comparison.
- [x] Compare three horizontal axes: ordinary LOO mean performance, shared roster pressure (the mean competitive relevance of all group members), and LOO roster pressure (the mean competitive relevance of the other members only). LOO roster pressure is distinct from the manuscript’s existing C_LOO,i performance average.
- [x] Use the same threshold and gamma settings for shared and LOO roster pressure. State the performance scale and threshold rule, and examine a declared range of settings rather than choosing the combination that produces the strongest downturn. Any threshold derived from data should remain fixed within each shared-versus-LOO comparison.
- [x] Keep binning rules, clipping, performance-band colors, and labels consistent and explicit. State quantile versus equal-width binning and any squid/jackal compression or extension. Common bin edges for shared and LOO roster pressure allow direct comparison on their common scale; ordinary LOO performance has different units. Include observations, drafted players, and contributing groups per bin so changes in support are visible. Mark singleton LOO values as undefined.
- [x] Export clearly labeled printable comparisons and describe whether peaks, downturns, and differences across performance bands persist, weaken, or move. These are descriptive associations; changing the horizontal axis does not change the observed draft outcomes. Hold off on significance tests and simulated selection comparisons in this first pass.

**Completed first pass:** [NCAA shared versus LOO roster pressure notebook](manuscript_figures/section_4_5/roster_pressure_comparison/NCAA_Shared_vs_LOO_Roster_Pressure.ipynb). It preserves the verified 2009–2021 cohort definitions, calculates pressure before focal-player filtering, and exports quantile and EW mosaics with bin support. EW pressure boundaries are common across the shared and LOO columns; quantile membership is independently recalculated using the original rank-first tie rule. These new figures use 16 bins in every row, without historical mixed-width compression or LOO winsorization. Default theta is the 93rd percentile of full-roster performance and gamma is 2; the declared comparison grid uses theta percentiles 80, 90, and 93 with gamma 0.5, 2, and 8. Source-specific score scaling is retained and stated.

**Initial descriptive observation:** At the default settings, the final-season all-player cohort has a much more pronounced upward relationship under shared roster pressure than under LOO roster pressure. In the high-performance bands, removing the focal individual lowers pressure for every included observation at these settings, but the curves are irregular and tail appearance varies with binning and parameters. This is a comparison of environmental summaries, not evidence of a causal effect or a significance claim. The notebook saves distinct-player and distinct-college-season counts. A separate tie-preserving quantile comparison remains open.

**Question motivating the notebook:** Does the concentration of competitively relevant teammates reveal a pattern that an average of teammate performance obscures, and does excluding the focal player materially change that pattern?

**Starting points:** [Figure notebook](manuscript_figures/section_4_5/Chapter_4_5_Mathematical_Illustrations.ipynb), [PD46 comparisons notebook](manuscript_figures/section_4_5/pd46_statistics/PD46_Draft_Rate_Comparisons.ipynb), and [printable mosaic methods](manuscript_figures/section_4_5/pd46_statistics/printable_mosaics/READ_ME_methods_and_next_steps.md). The October 23 notebook is a separate exploration; these earlier notebooks and their results remain intact.

## 7. Source register and revision record

The sources below distinguish direct advisor evidence from our own plans and current artifacts:

- **Alex’s direct recorded proposals:** PD44 transcript, especially 00:00–03:35, 06:31, 09:10–11:31, and 12:24; PD45 transcript, especially 02:26–03:35 and 04:16–06:14. The PD45 export is not ordered chronologically.
- **Advisor email:** The four comments and model introduction reproduced by Charles in this conversation. No separate email file was verified for this update.
- **Charles’s account of framing:** `Dissertation Tone.docx`.
- **Current manuscript:** `Model_Chapter_Shared_Working_Draft.docx`, headings inspected on 13 October. Its live content takes priority over the October 8 change memo and earlier Markdown outline.
- **LG proposed scope:** `LG_Model_Exploration_Executive_Summary.docx` and `LG_Model_Exploration_Agent_Handoff.md`.
- **LG later decisions and implementation status:** `lg_exploration/documents/LEO_DECISION_LOG.md`, the composition notebook, and the current code/settings inventory. Results were not recomputed or fully audited for this update.
- **Historical model evidence trail:** `assort_analysis/docs/results/ASSORT_20260927_model_plot_trail.md` and `NVector_to_SVector_MLE_Bernoulli_response.md`. These remain entry points for claim-specific verification, not fresh verification of all their contents in this update.

**Revision note:** This October 13 version replaces the September 30 work map in place so existing links still work. The preceding Markdown file was backed up under `manuscript_backups/work_map_before_update_*`. The older PDF beside this file has not been regenerated and does not reflect this update. No manuscript prose, research code, or experimental results were changed by this work-map revision.
