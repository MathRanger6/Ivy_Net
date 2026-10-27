# Jazz night: what we tried, why we tried it, and what we learned

**Last synced:** 27 October 2026 — canonical starter reproduced; standalone progression created  
**For:** Charles — a running record to read alongside the figures and return to without retracing the conversation.  
**Current position:** Charles chose to continue with PPM. Section 13 records the first deterministic top-K comparison, now JN-02 in the progression and ready for review. JN-01 remains locked; BPM remains a documented side comparison.

This document is the chronological record of the Jazz night experiments. It includes the plots themselves, not just a list of filenames. The separate [Jazz night manuscript outline](../Jazz_night.md) records the scientific story we intend to build. Neither document is the manuscript, and the experiments below have not rewritten it.

The plots are preserved records of what we examined. SCOUT has now reconciled their source path with the earlier production decisions, and we have independently checked the final-record selection against the current snapshots. This establishes consistency with that policy, not a fresh game-by-game data audit or proof that every multiple-team record is accurate.

## 1. First, we wanted to see the basic empirical relationship

### What we wanted to learn

We wanted to start with the simplest empirical question: **As a player's own measured performance increases, how does the observed draft rate change?** This is what Charles has long called the “naïve plot.” It is not the model's deterministic top-K benchmark, and it is not a HERO plot with teammate quality on the horizontal axis.

The purpose was to establish the shape from the data before assuming that it is exponential, fitting a selection model, or introducing congestion. At this stage, each bar is simply the number labeled ever drafted divided by the number of observations in that performance bin.

### What we plotted

Charles requested 2011–2021, MG10, a minimum of 20 minutes, and 12 bins in both equal-width and quantile versions. We initially carried forward box plus/minus (BPM), standardized within season, from the recent BPM work. We used all eligible colleges and one saved final observed record per player.

Equal-width (EW) bins divide the numerical performance range into equal intervals. Quantile (Q) bins divide the observations into nearly equal-sized groups. Thus, an EW tail bin can have very few observations, while the highest Q bin can cover a large numerical range. Tied values are split in fixed source order, consistent with Charles's earlier preference.

For this run, there were **19,289 players, including 510 ever drafted**, an overall rate of **2.64%**. MG10 means more than 10 captured games for the team-season, not 10 appearances by each player. The 20-minute minimum means total recorded season minutes, not minutes per game.

### Here is what we got

![First experiment: BPM, final observed season, 12 equal-width and 12 quantile bins](01_naive_BPM_EW12_vs_Q12.png)

*Figure 1. The original BPM view, retained with its original full probability scale.*

The highest quantile bin contained **410 drafted players out of 1,607, or 25.5%**. The preceding bin contained **76 out of 1,607, or 4.7%**. The broad pattern placed substantially more drafted players at higher measured performance, but the highest bin represented roughly the top 8.33% of this cohort, not a narrowly defined superstar category.

The equal-width view exposed another issue: the standardized BPM range ran from about −12.75 to 8.55, and several extreme bins contained only one player. The last two bins each had zero drafted out of one. Those zeros did not establish a downturn. The counts were essential to interpreting the picture.

**What we carried forward:** Show both binning methods and their counts. Do not infer a reliable tail shape from one or two observations. Do not assume that the highest bin is a group of near-certain draft picks.

## 2. Then we reduced the number of bins from 12 to eight

### Why we changed it

Charles asked to see the same relationship with eight bins before changing the performance metric. This gave us a coarser summary and let us examine how much the visible pattern depended on the binning resolution. This was a requested comparison, not a finding that 12 bins were mathematically wrong.

### What changed, and what stayed fixed

Only the number of bins changed. We retained BPM, the same 19,289 players and 510 drafted labels, the same filters, and the same final-observed-season definition. Both EW and Q were rebuilt with eight bins.

### Here is what we got

![Second experiment: the same BPM players summarized in eight bins](02_eight_bin_comparison/display_before_zoom/bpm_8bins/naive_BPM_EW8_vs_Q8.png)

*Figure 2. The original eight-bin BPM result, before the later display-scale adjustment.*

The highest quantile bin now contained **463 drafted players out of 2,411, or 19.2%**. That was lower than the 25.5% in the earlier highest bin, but the bin now covered approximately the top 12.5% rather than the top 8.33%. We had broadened the group; no player's outcome had changed.

The equal-width tail still remained sparse. Bin 7 contained seven drafted players out of 31, while bin 8 contained zero out of two. Reducing the number of bins did not make the most extreme observations abundant.

**What we learned:** A highest-bin rate is inseparable from the width and definition of that bin. Changing its rate by changing the binning does not mean the underlying relationship changed.

## 3. Next, we switched from BPM to PPM while keeping eight bins

### Why we changed it

Charles wanted to return to points per minute (PPM) and said that we would probably continue with it. The immediate task was to see the familiar performance measure in the same plot format. We did not treat visual smoothness as proof that PPM is the superior measure.

### What changed, and what stayed fixed

We retained 2011–2021, all eligible colleges, MG10, at least 20 recorded season minutes, final observed records, and eight EW and Q bins. PPM was standardized within season using the eligible full roster before selecting the final records.

Metric coverage changed the sample: PPM was available for **19,803 players, including 520 ever drafted**, compared with 19,289 and 510 for BPM. The additional **514 players include 10 ever-drafted players** whose final rows lacked BPM. Consequently, this comparison changed the metric and its available sample; it was not a strict matched-player experiment isolating the metric alone.

### Here is what we got

![Third experiment: PPM, final observed season, eight bins](02_eight_bin_comparison/display_before_zoom/ppm_8bins/naive_PPM_EW8_vs_Q8.png)

*Figure 3. The original eight-bin PPM result, before the display-scale adjustment.*

The PPM quantile rates increased toward the right, reaching **297 drafted players out of 2,475, or 12.0%**, in the highest bin. The equal-width rates also increased through bin 7. However, that seventh bin contained only **18 players and four drafted**, and the eighth contained **one player and no draft**.

The overall PPM rate was **520 out of 19,803, or 2.63%**. This is a pooled ever-drafted fraction, not an annual quota of draft opportunities.

**What we carried forward:** PPM became the working metric for the next comparison, at Charles's request. We preserved BPM rather than overwriting it. We had not established that one measure predicts selection better, nor resolved whether the low-minute eligibility rule is sufficient for our eventual purpose.

## 4. Then we made the observed rates easier to see

### Why we changed it

Charles pointed out that a vertical axis extending to 100% left most of the informative bars compressed near the bottom. We needed a clearer display of the actual rates and counts.

### What changed

We changed all four eight-bin panels to the same **0–35%** vertical scale and added percentage labels above the bars. Counts remained underneath. Hatching identifies bins with fewer than 30 observations. An upward triangle means that the uncertainty interval continues above the displayed range; its complete value remains in the saved count file.

No players, outcomes, bin definitions, rates, or interval calculations changed. This was a display improvement, not an additional analysis. We preserved the original full-scale images shown above.

### Here is the clearer BPM view

![Eight-bin BPM after tightening the display scale and adding rate labels](02_eight_bin_comparison/bpm_8bins/naive_BPM_EW8_vs_Q8.png)

*Figure 4. Exactly the same BPM results as Figure 2, now displayed from 0% to 35%.*

### Here is the clearer PPM view

![Eight-bin PPM after tightening the display scale and adding rate labels](02_eight_bin_comparison/ppm_8bins/naive_PPM_EW8_vs_Q8.png)

*Figure 5. Exactly the same PPM results as Figure 3, on the same 0–35% scale as BPM.*

**What we learned:** The change made the differences among observed rates legible. It did not make sparse tail bins more reliable, and the long intervals in those bins still matter.

## 5. Then we asked: are these all player-seasons or final player-seasons?

### The clarification that prompted the comparison

The plots up to this point used **final-PS**: one final observed record per player. Charles then asked to see **all-PS** alongside it, using the same PPM filters and eight bins.

“Final observed” is important. A player active at the 2021 boundary may not have finished their college career. More precisely, this is the **latest eligible season after the source filters**, with the largest-total-minutes team record retained when that season has multiple teams. We are not independently determining career completion. SCOUT’s response and our verification of this rule are recorded in Section 7.

### What changed, and what stayed fixed

We retained the same 19,803 unique players and the same 520 unique ever-drafted players. We also retained PPM, its within-season standardization, the season window, colleges, eligibility filters, eight bins, and the 0–35% scale.

The difference was the records entering the bars:

- **Final-PS:** 19,803 records, including 520 positive records; overall rate **2.63%**.
- **All-PS:** 46,306 player–team–season records, including 1,133 positive records; overall record-weighted rate **2.45%**.

Those 1,133 positive records are not 1,133 distinct draft selections. A player with three retained seasons and an ever-drafted label contributes three positive records to all-PS, possibly at three different performance levels. Players with longer observed histories receive more weight.

### Here is what we got

![PPM final-PS on the left and all-PS on the right, with equal-width bins above and quantile bins below](03_ppm_all_vs_final_ps/PPM_8bins_final_vs_all_PS_mosaic.png)

*Figure 6. Final-PS versus all-PS. The upper pair uses identical numerical EW boundaries; the lower pair has equal-count Q bins within each view, so numerical boundaries differ.*

Both quantile curves increased toward higher PPM. In the highest quantile bin, final-PS had **297 out of 2,475, or 12.0%**, compared with **511 out of 5,788, or 8.83%**, for all-PS. However, the lower boundary also moved from approximately 1.28 to 1.16 standardized PPM, so these are not identical performance intervals.

The equal-width comparison holds the numerical boundaries fixed. In bin 5, approximately 1.70–2.80 standardized PPM, final-PS had **170 out of 1,122, or 15.15%**, while all-PS had **247 out of 2,072, or 11.92%**. Earlier records redistribute outcome labels across performance levels and change how much each person contributes. This comparison describes that change; it does not identify its causal explanation.

The extreme final EW bin moved from zero of one record to one of three records, or 33.3%. A large percentage calculated from three records is not a reliable new tail finding.

For larger images, open the [EW pair](03_ppm_all_vs_final_ps/PPM_EW8_final_vs_all_PS.png) or [Q pair](03_ppm_all_vs_final_ps/PPM_Q8_final_vs_all_PS.png). The four-panel view above is sufficient to follow the comparison on paper.

### A data detail we found and deliberately did not silently “fix”

The all-PS snapshot contains 46,233 unique player-season combinations but 46,306 player/team/season records. Seventy-three player-seasons, involving 71 players, appear under two teams. We retained those inherited records and saved an audit list. Their presence does not establish that they are genuine transfers; it also does not establish that they are errors.

Charles recalled that decisions about such cases had already been made. That is why the next step became historical reconciliation rather than inventing a new cleaning rule on the spot.

**What we learned:** Final-PS and all-PS answer different descriptive questions. The first relates a person's last observed performance to an ever-drafted label. The second relates all their retained performance records to that label, weighting people by their number of records. We have not yet chosen which should anchor the manuscript's first plot.

## 6. We paused to recover what SCOUT and Charles already learned

### Why this pause matters

Charles reminded us that earlier work had identified one-game or fragmentary season records, multiple-team cases, and consequential cleaning decisions. Repeating those investigations without recovering the earlier reasoning would waste time and risk making inconsistent choices.

The [new request to SCOUT](../../VECTOR_work/new_VECTOR_work/20261027_Request_to_SCOUT_MBB_Lessons_for_Jazz_Night.md) asks for the discoveries, decisions, rationale, implementation, and evidence that each rule reached the present data. It asks SCOUT to distinguish decisions that were adopted for all basketball work from rules used only in a particular audit or exploratory branch.

### What an earlier SCOUT record already tells us

We located SCOUT's [September 25 data-hygiene reconciliation](../../VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md). It reports that the team-coverage rule moved from no minimum to more than five captured games, then to more than ten; that the production path dropped records below 20 total season minutes rather than setting their PPM to zero; and that PPM was calculated as retained season points divided by retained season minutes after box-data filtering.

It also distinguishes an incomplete **team's captured season** from an individual playing only a small number of games on an otherwise adequately captured team. A team-coverage rule does not automatically impose a player-appearance minimum. That distinction helps explain why “MG10 and min20” is not a complete answer to every low-exposure concern.

SCOUT's [September 27 population reconciliation](../../VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_selection_population_and_reigning_alignment.md) distinguishes the canonical-team ASSORT audit population from the HERO pipeline population. We therefore cannot assume that a multiple-team rule used in one analysis applies automatically to the other.

These are findings reported in existing historical documents, not newly completed audits of our current snapshots. The new request asks SCOUT to consolidate the history, identify later changes, and tell us exactly where the current data agree or disagree with the intended policy. The historical report's conclusions about particular cleaned HERO tails must not be generalized to every performance band or to these own-performance plots.

### Status of that pause

At this point in the sequence, we prepared the request and held the data fixed. SCOUT then replied on 27 October 2026. The following entry records the response and supersedes the earlier waiting status. No multiple-team records were merged, no minutes threshold was raised, and no new sweep was run during this reconciliation.

## 7. SCOUT replied: what we already knew, what needs correction, and what remains open

**Reconciliation added: 27 October 2026.** Source: [SCOUT’s response on the basketball data lessons](../../VECTOR_work/new_VECTOR_work/20261027_SCOUT_Response_MBB_Lessons_for_Jazz_Night.md). SCOUT reviewed the recorded history and current code without rebuilding the panel. Our follow-up checks below also left the source data and figures unchanged.

### What was already settled, and is already in our data

The old one-game problem was principally **inadequately captured team-seasons**, compounded by placeholder athlete rows and the few players surviving a minutes filter on those incomplete rosters. The remedy was to remove dash-name placeholders and require **at least 11 captured team games**, then aggregate the retained box records and drop player/team/season rows below **20 total minutes**. Those are the production rules inherited by our snapshots. We are not unknowingly using the old no-coverage-filter population.

The 20-minute rule is an exclusion rule, not an instruction to set low-minute PPM to zero. PPM is the sum of retained points divided by the sum of retained minutes, not an average of game-level PPM ratios. Performance is standardized within season before final-record subsetting. These choices were already established; we do not need to rediscover or replace them merely because a current tail bin looks unusual.

Production HERO data retain one record per **player, team, and season**. When a player has two eligible team records in the same season, both remain in all-PS. Final-PS selects the latest eligible season and, within that season, the record with the greatest total minutes. SCOUT confirmed that the separate ASSORT audit used a different canonical-team rule: positive-minute game counts first, then total minutes, with unresolved ties stopped for review. That audit rule was not a universal replacement for the HERO definition.

The ever-drafted outcome is also intentional. It repeats across all retained records for a drafted player. The current all-PS count of 1,133 positive records and final-PS count of 520 drafted players are therefore compatible; they are not competing counts of NBA draft selections.

### What our current plots need corrected

**No changed bar heights, bin counts, or population rebuild is indicated by this reconciliation.** SCOUT explicitly concludes that retaining the current frozen sources is appropriate for the declared HERO-style population. The corrections are to scope, wording, and interpretation:

1. **Say “final eligible observed season,” not “career-final season.”** Filtering occurs first. If a later raw season fails eligibility but an earlier season survives, the earlier season can become the final eligible record. The player is not automatically removed solely because the later season failed. If multiple teams remain in that selected season, the most-minutes record is used. This clarifies a potentially misleading sentence in SCOUT’s missing-final-row discussion as well as our own shorter labels.
2. **Distinguish the source window from the plotted window.** The caches were built for 2009–2021. These Jazz night plots explicitly use 2011–2021. The full PPM final cache has 22,795 players and 615 drafted; our narrower window has 19,803 and 520. Neither total corrects the other. Removing whole earlier seasons does not itself change later seasons’ within-season standardization; our scripts check the reconstructed values.
3. **Describe all-PS as player–team–season records.** It contains 46,306 records for 19,803 players, including 73 same-season two-team cases. Retaining them follows production policy. They have not been individually established as valid transfers, nor established as errors. An audit remains open; silently merging them would introduce a new population rather than repair a demonstrated implementation mistake.
4. **Keep the BPM coverage qualification.** The BPM-to-PPM comparison added 514 players, including 10 drafted players. It is not a matched-sample test of which metric is better. Missing BPM on the already selected final row causes exclusion in that comparison; it does not trigger selection of an earlier BPM-available season. This differs from eligibility filtering before the PPM final-row selection.
5. **Keep the outcome and uncertainty qualifications.** A pooled ever-drafted proportion is not an annual K/N or a same-season selection probability. All-PS repeats people, and the displayed Wilson intervals do not adjust for that repetition or for college grouping. We have not tested whether differences between the views are statistically significant.

The existing all-PS comparison already labels records and repeated outcomes; its bars do not need regenerating to enact these clarifications. This entry supplies the missing final-record rule and source-window context. When we prepare manuscript figures, the caption should explicitly carry those definitions rather than rely on the shorthand “final-PS.” The earlier embedded figures remain intact as records of the experiment.

### What we independently checked after reading SCOUT

We rechecked the frozen-source fingerprints and confirmed that **all 19,803 current PPM final-PS records** belong to their player’s latest eligible season and have the maximum total minutes among that season’s team records. **Twenty-four players** have more than one team record in that latest eligible season. None is tied at the maximum minutes, so the current sample does not depend on an additional equal-minutes tie rule. The broader count of 73 two-team player-seasons includes cases outside those final eligible seasons.

These checks corroborate the source-selection explanation. They are not a fresh review of every underlying box score, draft match, or multiple-team identity.

### Which earlier lessons should constrain the next interpretation

SCOUT’s earlier cleaning comparison showed that a right-tail dip in a particular **LOO teammate-mean HERO plot** was driven by fragmentary team-season records under the old no-minimum-games setting. That finding belongs to that comparison. It does not establish that every downturn is an artifact, or that every new plot should be made to show one. Our current horizontal axis is own performance, and we must judge it on its own population and counts.

Likewise, a saved MLE fit, the empirical HERO plotting population, and a generative exact-K selection experiment are not interchangeable. Before using earlier fitted parameters, we would need to reconcile the candidate rows, outcome timing, likelihood, and parameter scale. That is a later modeling step, not something resolved by the present naïve bars.

### What remains genuinely open

The unresolved question is no longer whether we forgot to apply the ASSORT team-collapse rule to these HERO data: that was a different analysis. What remains is which observational unit best serves the manuscript’s first empirical question, whether PPM should be the definitive performance measure, and whether any specific record-level audit warrants a new cleaning decision. The individual status of the 73 two-team cases and possible low-exposure issues remain open; there is no newly authorized rule to remove them.

PPM and 2011–2021 remain the working choices already requested for this comparison. Listing historical alternatives does not reopen them automatically or require another sweep.

## 8. How to read the uncertainty throughout this record

The error bars are pointwise 95% Wilson intervals using a working assumption that observations are independent. They are not adjusted for college grouping. In all-PS, they also do not account for repeated players and repeated outcome labels. They should not be used here to declare a statistically significant difference between views; final-PS is itself contained within all-PS.

All percentages are based on the inherited ever-drafted lookup, not same-season selection. No likelihood has been fitted, no exponential shape has been established, and no congestion mechanism has been selected by these plots. We are assembling the empirical starting point and making its definitions explicit.

## 9. Our recommendation after SCOUT’s reply, before choosing the canonical starter

**Historical recommendation:** The following was our return point at that stage. Charles’s subsequent choice in Section 10 supersedes the proposed 2011–2021/eight-bin starter; those plots remain supporting exploration.

**Recommended next decision:** Choose the observational unit for the first manuscript figure. My recommendation is to retain **PPM final-PS as the provisional main naïve view**, because each player contributes once to the ever-drafted outcome, and keep **all-PS as the documented companion comparison**. This is a recommendation for Charles, not a decision already made. It does not make the last eligible season a true draft-eligibility date or remove possible follow-up limitations.

Keep the current 2011–2021 window, MG10/min20 filters, eight bins, and 0–35% display while making that decision. No new metric, coverage, or minutes sweep is needed to resolve the policy questions SCOUT has now answered. If we want to investigate a specific suspicious multi-team or low-exposure record, document that as a bounded audit, not as an unannounced replacement of the current population.

Once the observational unit is chosen, settle the comparison between the empirical naïve curve and the performance-only top-K benchmark. **Before running that benchmark, specify the actual selection pool, outcome timing, and meaning of K.** The pooled ever-drafted rate cannot simply be used as an annual quota. The manuscript outline already identifies this requirement; we should resolve it rather than jump straight to fitting temperature or congestion.

The experimental return point at that stage was: **PPM, 2011–2021, eight bins; existing production data rules confirmed; final-PS versus all-PS choice still to be made; no new fits or significance tests.** The preserved figures and their counts remain valid descriptions of their declared snapshots, subject to the audit and uncertainty limitations above.

The complete counts, memberships, settings, source fingerprints, and validation results remain beside each figure. The original 12-bin material is in this folder; eight-bin metric comparisons are in `02_eight_bin_comparison/`; the record-unit comparison is in `03_ppm_all_vs_final_ps/`. The final-PS results in the latter reproduce the preceding output’s counts, rates, and intervals.

Continue this document with a dated entry for each actual next decision or experiment: the question, why we changed something, what changed and stayed fixed, the embedded result, the counts, the interpretation, and the decision or unresolved question. If a future audit changes the data, preserve the earlier figures and show the correction explicitly.


## 10. We recovered the canonical starter and made it the first figure in the progression

**27 October 2026.** Charles clarified that the immediate aim was a demonstrative upward own-performance plot from which to develop the model, rather than more exploratory comparisons. SCOUT identified the original Pass A naïve PPM plot. Charles asked us to reproduce it using the same underlying data in a reusable visual format, and then requested a separate **JN progression** document around which to rebuild the manuscript and lock figures one at a time.

### What we used and checked

We recovered the original 16-bin ability CSV and reproduced it from the frozen player-level final-PS source. Every bin count, draft rate, mean performance, and median performance matches the original saved summary. The population is **22,795 players and 615 ever drafted**, covering **2009–2021**, with PPM standardized within season, all eligible colleges, MG10, and at least 20 total recorded season minutes. Final-PS uses the latest eligible season and largest-minutes team record when needed.

This intentionally returns to **2009–2021 and 16 quantile bins**, rather than retaining the earlier Jazz **2011–2021 and eight bins**. Both years and bin count change to recover the established starting figure; this is not a one-factor sensitivity experiment. We did not search new settings to manufacture a rising curve.

### Here is the reproduced starter

![Canonical naïve PPM plot reproduced in the new story format](04_canonical_naive/canonical_naive_PPM_Q16_2009_2021.png)

*Figure 7 / progression figure JN-01. The canonical own-performance result, now in the Jazz night format. Same original bar heights; added counts, percentage labels and pointwise Wilson intervals; 0–20% y-axis.*

The highest bin has **228 drafted players out of 1,424, or 16.0%**. All 16 rates are nondecreasing. This supports the opening observation that higher measured performance is associated with a higher draft rate, rising sharply toward the upper end. No exponential model was fitted. We corrected the original inherited footer, which incorrectly described a teammate-performance axis.

### What we decided about the documents and display

[**JN_progression.md**](JN_progression.md) is now the standalone manuscript story outline with figures, proposed prose, transitions, and lock status. This walkthrough remains the chronological experiment record. Earlier alternatives stay here rather than becoming obligatory detours in the manuscript story.

The new figure is **ready for Charles’s visual review; it is not yet marked LOCKED**. Its verified data, style settings, high-resolution PNG, scalable SVG, memberships and validation are saved in `04_canonical_naive/`. Charles’s acceptance will be recorded in the progression document.

We will preserve a consistent visual structure, but do not impose the current 0–20% scale or 16 bins on every future result regardless of need. If a later comparison requires a change, record why, show all relevant values, and update its paired plots consistently. The final manuscript sequence will receive a standardization pass once its scientific story is established.

**Current next step:** Review and lock JN-01 and its opening message in the progression document, then develop Step 2. No top-K, stochastic selection, fitting, or congestion comparison was run as part of this reproduction.


## 11. We locked the quantile starter and added an equal-width companion

**27 October 2026.** Charles accepted the reproduced canonical Q16 opening figure, then requested an EW plot to discuss the difference between the two binning methods early in the story. JN-01 version 1 is now recorded as **LOCKED** in the progression. The new companion awaits review.

We used the exact same 22,795 player records, 615 ever-drafted labels, and season-standardized PPM values. Sixteen EW intervals span the full observed performance range; each is approximately 0.552 standardized PPM units wide. No filters, outcome definitions or performance values changed.

![EW companion to the locked Q16 starter](05_canonical_EW_companion/naive_PPM_EW16_2009_2021.png)

*Figure 8 / progression figure JN-01-EW. Equal-width binning of the locked starter’s population.*

The counts vary from zero to 4,472 players per EW bin, compared with 1,424–1,425 in each quantile bin. The last five EW bins have 28, 16, 5, 0 and 1 players. Bin 14 has two drafted players out of five, or 40%; bin 15 has no observations, so its rate is undefined rather than zero. These sparse bins help explain why the equal-width tail looks less smooth.

The new display uses 0–50% so all observed rates are shown; intervals continuing beyond that range are marked with arrows. We also saved a [common-scale Q/EW comparison](05_canonical_EW_companion/naive_PPM_Q16_vs_EW16_same_scale.png) with both panels on 0–50%. The accepted Q16 standalone plot remains untouched at 0–20%.

**What this adds to the story:** Q bins hold approximate player counts fixed; EW bins hold numerical performance width fixed. They describe the same observations with different resolutions. Bin numbers are not interchangeable between them. The purpose here is to explain the choice, not to select a binning because it guarantees a smooth curve.

**Next action:** Review the EW companion in [JN_progression.md](JN_progression.md), then continue the model progression. Counts, exact boundaries, player memberships and validation are preserved in `05_canonical_EW_companion/`.


## 12. We checked BPM in the same standardized 16-bin format

**Added: 27 October 2026. Scope: walkthrough only.** Charles asked to see the same quantile and equal-width plots using BPM, without moving this experiment into the manuscript progression.

### What we wanted to learn

We had established a reusable visual format for the PPM starter. We now wanted to see how the observed own-performance relationship looks when performance is BPM, standardized within season. This is an exploratory comparison, not a decision to replace the PPM starter or to fit a model.

### What stayed fixed, and what had to change

We retained all eligible colleges, MG10 (more than 10 captured team-season games), at least 20 total season minutes, one final eligible record per player, and the ever-drafted outcome. We requested the same 2009–2021 source window and used 16 bins in both versions. As before, the final record is the latest eligible season and, when necessary, the highest-minutes team record in that season.

**BPM is unavailable for every 2009–2010 record in this frozen source.** It is also missing from some later final records. Starting from the canonical PPM sample of 22,795 players and 615 ever drafted, the BPM version includes **19,289 players and 510 ever drafted (2.64%)**, with actual coverage **2011–2021**. The 3,506 excluded final records comprise:

- 2,992 players, including 95 ever drafted, whose final eligible season is 2009 or 2010.
- 514 players, including 10 ever drafted, whose final eligible season is 2011–2021 but lacks BPM.

We did not substitute an earlier season with BPM for a missing final record. Within-season BPM standardization uses the mean and sample standard deviation across all eligible finite-BPM roster records, before taking the final-record subset. The resulting players and standardized performance values reproduce our earlier Jazz BPM cohort exactly.

Consequently, comparison against the locked 2009–2021 PPM plot changes both the metric and its available population. It does not isolate the effect of changing the metric alone.

### Here is the quantile view

![BPM own performance and ever-drafted proportion in 16 equal-count bins](06_BPM16_walkthrough_comparison/naive_BPM_Q16_available_2011_2021.png)

Each bin contains 1,205 or 1,206 players. Quantile bins split ties in stable source order when necessary; the outcome is not used to allocate ties. The highest bin has **370 drafted out of 1,205 players (30.7%)**. The preceding bins have **93 of 1,206 (7.7%)** and **26 of 1,205 (2.2%)**. The strong rise at the upper end is evident, although the entire series is not strictly monotonic: bin 8 contains one drafted player, while bins 9 and 10 contain none.

The highest PPM quantile bin was 228 of 1,424 (16.0%). The higher BPM endpoint is worth recording, but it does not by itself establish that BPM is the better predictor: the cohort and the people occupying the highest bins differ.

### Here is the equal-width view

![BPM own performance and ever-drafted proportion in 16 equal-width bins](06_BPM16_walkthrough_comparison/naive_BPM_EW16_available_2011_2021.png)

The full standardized BPM range, approximately −12.75 to 8.55, is retained without compression or removal of the tails. Sixteen equal intervals therefore span about 1.331 standardized BPM units each. Bins are displayed at equally spaced categorical positions in both plots; equal-count bins do not represent equal numerical performance intervals.

The EW view reaches **244 drafted out of 522 players (46.7%) in bin 12**. The next bin contains **7 of 28 (25.0%)**. Bins 14–16 have only **3, 1, and 1 players**, respectively, with no drafted players. Those far-right zeros do not establish that extremely high BPM reduces draft prospects. Bin 2 is empty and has no estimated rate.

### Comparing the two binning choices directly

![The BPM quantile and equal-width plots on the same vertical scale](06_BPM16_walkthrough_comparison/naive_BPM_Q16_vs_EW16_same_scale.png)

Both BPM plots use a **0–50% vertical scale**, matching the PPM equal-width companion and the paired PPM display. The locked standalone PPM quantile plot retains its original 0–20% scale. All observed BPM rates fit within the new display; arrows identify uncertainty intervals extending above 50%. Full interval endpoints remain in the saved bin tables. Intervals are pointwise 95% Wilson intervals, without a college-clustering adjustment.

The quantile view concentrates enough players in each bin to show the broad relationship clearly. The equal-width view reveals how unevenly players occupy the numerical BPM range and why the sparse extremes need care. Neither binning choice changes the underlying players or outcomes within this BPM comparison.

### What we keep, and where we return

**This is a documented side comparison, not a change to the manuscript progression.** We have not changed JN_progression.md, the JN-01 lock, the accepted PPM figures, the source data, or the notebooks. No fitting or significance tests were run. Our return point remains the PPM starter and the next step in the model story; any decision to replace that starter should be made explicitly.

The [BPM comparison folder](06_BPM16_walkthrough_comparison/README.md) contains the individual PNG/SVG figures, paired PNG, exact bin counts and intervals, player membership, missing-BPM records, season coverage, source fingerprints, and validation record. This preserves both what we saw and how to reproduce it.


**Display clarification (27 October 2026):** At Charles’s request, the BPM plots now lead with the years actually used, **2011–2021**, and explicitly annotate **“BPM unavailable for 2009–2010.”** The labels also identify the 514 missing-BPM final records within 2011–2021. The plotted data, rates and counts are unchanged.


## 13. We returned to PPM and tested strict performance ranking

**Added: 27 October 2026.** Charles chose to continue with PPM and asked for the next plot in the JN progression: a direct comparison showing what deterministic top-K selection misses.

### What we wanted to learn

The starter shows an increasing observed draft rate with own performance. We asked whether simply selecting the highest-scoring players could reproduce that distribution. We deliberately kept the source population and bins fixed, so the comparison changes the selection rule rather than the empirical target.

### What we did

We used all 22,795 players in the locked 2009–2021 PPM starter, retaining its final eligible records, MG10/min20 filters, within-season standardized PPM and 16 quantile-bin memberships. SCORE sets each score equal to standardized PPM. SELECT ranks the scores and chooses the highest 615, matching the observed count of ever-drafted players.

This is one pooled descriptive benchmark across the historical sample. We did not reconstruct annual NBA draft pools or treat 2.70% as an annual quota. The observed labels determine the total capacity only, never the ranking. Stable source order breaks exact score ties if needed, but the 615th and 616th scores differ here. No simulation, likelihood fit or significance test was performed.

### Here is what we got

![JN-02: Same PPM players and bins, observed outcomes versus deterministic top-K](07_JN02_deterministic_topK/JN02_PPM_observed_vs_topK_Q16.png)

All 615 top-K selections lie in the highest bin, containing 1,424 players: **43.2% selected within that bin**, with zero benchmark selections in every lower bin. The observed highest-bin rate is **228/1,424 = 16.0%**. The other **387 actually drafted players are below that highest bin**. Those observed counts match the locked starter exactly.

The orange rate is a binned fraction, not stochastic individual selection: each benchmark player is either selected or not. The selection threshold falls inside bin 16, between standardized PPM values 2.174506 and 2.174822. Even a deterministic rule can produce an intermediate bar height when a bin spans its cutoff.

### Why the display changed

Both series use a common 0–50% vertical axis so that the 43.2% benchmark bar is fully visible. JN-01’s locked standalone figure remains at 0–20%; its observed values are unchanged here. We retained the observed blue color and added orange for the benchmark, along with a third count row showing benchmark selections. Observed error bars are pointwise 95% Wilson intervals without college-clustering adjustment; the fixed benchmark needs no simulation interval.

### What we learned and what comes next

Strict ranking by PPM in this pooled sample concentrates selections more strongly at the upper end than the observed outcomes. That gives us a specific failure for the next model step to address. It does not prove intrinsic randomness or invalidate every deterministic model: actual pools, omitted selection criteria and measurement limitations could also explain discrepancies.

We will next consider uncertainty in SELECT while retaining the same performance-only SCORE. JN-02 is **ready for review, not yet locked**; no stochastic comparison has been run. The experiment and its proposed manuscript placement are now in Step 2 of [JN_progression.md](JN_progression.md).

Reproduction files are in [07_JN02_deterministic_topK](07_JN02_deterministic_topK/README.md), including exact bin counts, player memberships and top-K indicators, source hashes and validation. This is our current return point; the BPM exploration remains in Section 12.
