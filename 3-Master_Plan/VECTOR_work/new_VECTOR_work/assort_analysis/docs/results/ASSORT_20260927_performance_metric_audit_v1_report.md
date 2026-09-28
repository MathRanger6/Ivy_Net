# 2015 basketball performance-measure audit: what changed, and what did not

**Date:** September 27, 2026  
**Status:** Executed descriptive audit; VECTOR reviewed the identity sample, numerical checks, and output checksums. No draft curve, model calibration, assignment simulation, or source refresh was run.  
**Scope:** Season points per minute (PPM), Player Efficiency Rating (PER), and Box Plus/Minus (BPM) for the same accepted 2015 players. This does not change the adopted research measure or authorize another analysis.

## The result in plain language

Changing the performance measure changes how much players cluster by team. On the same 4,161 players and 350 teams, the sorting index ($H_{\mathrm{sort}}$) is **0.06338 for PPM, 0.10892 for PER, and 0.32515 for BPM**. PER therefore reveals more measured team clustering than scoring rate alone. However, PER's average team minimum-to-maximum interval is almost the same width as PPM's after each is expressed in population standard-deviation units. It has not transformed the teams into narrow, separated talent pools.

BPM produces substantially greater measured team clustering and narrower average intervals. That result needs a different interpretation: BPM incorporates team performance in its construction. Its larger sorting index cannot independently establish that teams recruit more similar latent talent than the other measures suggest. We did not quantify how much of its observed sorting comes from that adjustment.

**VECTOR's recommendation, awaiting Charles's decision:** retain PPM as the existing baseline, treat PER as one named sensitivity measure, and keep BPM as a contextual comparator. Do not launch a wider metric search or select a primary measure by its sorting-index magnitude. This is a recommendation about a bounded way forward, not a declaration that PER measures portable talent or predicts selection better.

## How we reached this point

First we examined whether advanced measures were available on the accepted 2015 population. Nearly 98% of players had usable matched values. That told us a comparison was feasible, but not that the identities were correct. SCOUT then confirmed the coverage counts, identified true key misses separately from matched rows with missing values, and pointed out that the matching file lacked an exact historical construction record.

Next Charles authorized a small identity check followed by a same-player descriptive comparison. We fixed 24 players from 24 distinct teams using identifier hashes before examining results. For each, we compared the accepted name and team with the saved Sports-Reference school/year/name key and compared saved PER/BPM values with the corresponding raw-source values. All 24 had one raw-source candidate, all values agreed, and VECTOR found no obvious displayed name or school mismatch. All sampled raw records carried a scrape date of **August 27, 2026**.

That check supports internal consistency between our saved files. It does **not** estimate match accuracy over the entire population, independently verify original website identities, or prove the exact historical matching procedure. It uses the documented name-normalization and school-crosswalk route, so agreement does not independently validate that route.

We then compared the three measures only where both advanced values were finite. Finally, we checked the variance decomposition, verified that standardization leaves the sorting index unchanged, read the sampled identities, and verified every saved numerical output checksum.

## Population and source qualifications

The accepted audit starts with **4,267 players on 351 teams**. The advanced matching file supplies 4,176 key matches, 4,174 finite BPM values, and 4,163 finite PER values. The shared comparison includes **4,161 players on 350 teams**, excluding **106 players, or 2.48%** of the accepted population. The smallest retained team has eight players.

The 106 exclusions comprise 91 absent matching keys, two matched records with missing BPM but finite PER, and 13 matched records with finite BPM but missing PER. **All 13 accepted Cleveland State players lack PER and therefore the entire team leaves the common sample.** This is a property of the saved values, not a deliberate team-selection rule. We did not diagnose or repair the source of those missing values. Using the common sample makes the three measures comparable over the same people; it does not make the exclusions scientifically ignorable or justify generalization to every accepted player.

The PPM sorting index moves from **0.06194 on all 4,267 players** to **0.06338 on the shared 4,161-player sample**. Thus the sample restriction alone makes only a small change to this particular index. That does not prove it has negligible effects on other results or on the excluded team.

There is also a distinction between *the same people* and *identical underlying game records*. Four of the 24 sampled players have different minute totals in the accepted audit and Sports-Reference: Jon Octeus, 977 versus 978; Martez Harrison, 1,070 versus 1,057; Drew Brandon, 1,101 versus 1,139; and Kwesi Abakah, 113 versus 112. No values were altered. These discrepancies show that the comparison changes both the measure and its source construction; it is not a perfectly isolated formula change applied to identical season box totals. The audit does not explain the differences.

Two provenance statements are now narrower than the earlier SCOUT report: the saved matched file spans **2009–2021**, not only 2011–2021, and the raw file spans **2005–2021**. Finite BPM coverage can have a narrower historical range than the table itself. The current `bpm_merge.run_match` saves only rows with nonmissing BPM, whereas the saved matched file contains rows without BPM and additional columns. The sampled August 27 scrape dates strengthen source attribution, but the exact script/panel/version that produced the entire matching file remains unresolved. Historical files were not edited or refreshed.

## What the three measures show

All following results use the same players and team assignments. Each standardized measure uses its own common-population mean and population standard deviation. The mean interval width weights every team equally; the sorting index weights every player equally.

- **PPM:** sorting index **0.06338**; mean standardized team interval width **3.258**; median width **3.212**. Raw player median is 0.2953 points per minute, with the middle 90% from 0.1092 to 0.4894.
- **PER:** sorting index **0.10892**; mean standardized team interval width **3.247**; median width **3.166**. Raw player median is 12.8, with the middle 90% from 1.4 to 23.1.
- **BPM:** sorting index **0.32515**; mean standardized team interval width **2.826**; median width **2.544**. Raw player median is -1.5, with the middle 90% from -10.7 to 6.6.

PER raises the sorting index by approximately **0.0455**, or 4.55 percentage points of explained player variation, relative to PPM. Its mean standardized interval is only about **0.35% narrower**. The two statistics describe different things: team means can explain more variation while each team's observed range remains broad. Neither statistic alone measures the overlap among all team intervals; this audit did not calculate interval-coverage counts or construct a new raster plot.

The Spearman rank correlation between PPM and PER is **0.819**. PPM and BPM have a rank correlation of **0.536**, and PER and BPM **0.757**. PER therefore largely preserves the scoring-rate ordering while changing some player rankings; BPM rearranges the ordering more substantially. These correlations do not validate any ranking as talent or as selection potential.

As mathematical context, uniformly permuting a fixed nonconstant vector over fixed team sizes gives an expected sorting index of $(J-1)/(N-1)$. For this shared population that benchmark is $349/4160 \approx 0.08389$. The descriptive PPM index lies below it, PER modestly above it, and BPM further above it. **No permutations were executed and no reference distribution or significance test was calculated.** This benchmark was added during review to prevent interpreting every positive sorting index as above-chance sorting. It does not remove the team component from BPM or settle whether PER's departure is statistically unusual.

## Scientific interpretation

PPM records scoring production relative to playing time. PER summarizes broader box production and is described as a per-minute rating in the [Basketball-Reference methodology](https://www.basketball-reference.com/about/per.html). The exact college formula/version behind every saved PER value has not been reconstructed here. Neither measure establishes portable latent ability, and both can reflect role, teammates, opponents, opportunity, and measurement error.

The [Sports-Reference college BPM 2.0 announcement](https://www.sports-reference.com/blog/2020/05/bpm-2-0-on-college-basketball-reference/) explicitly describes player box information and team overall performance as ingredients. The [BPM methodology](https://www.basketball-reference.com/about/bpm2.html) explains the team adjustment. Those are reasons to interpret BPM's team clustering cautiously, not reasons to discard BPM for every scientific purpose. A performance measure designed partly to reflect team impact answers a different question from an environment-independent player characteristic.

For example, if two players have similar personal box production but play on teams with different performance, a team-based adjustment can help separate their reported values by team. That can be useful for evaluating contribution in context. It also means that sorting calculated from those reported values partly tests the estimator's construction. A larger index does not automatically reveal a recruiting mechanism.

The present results support the narrow conclusion that **the low PPM sorting result is somewhat measure-dependent**. They do not support either “basketball has no talent assortativity” or “BPM has uncovered the true assortativity.” PER's stronger index and nearly unchanged team ranges are evidence against treating a broader box measure as an immediate cure for the mixed-player-pool problem. Underlying talent sorting, causal congestion, selection relevance, and the correct performance proxy remain distinct questions.

## Next decision and stopping point

The high-value next decision is whether to retain the existing PPM baseline and allow **one PER sensitivity** in the later authorized mechanism comparison. Such a sensitivity would have to make the common player population and source differences explicit. This audit does not authorize that experiment or alter the established scoring/selection specification. There is no current reason from this result alone to add seasons, measures, filters, or a search for a better draft curve.

If Charles instead adopts PER as the primary input, that would be a substantive scientific decision. Its ability standardization, viability threshold, congestion reference, population, and capacities would need to be specified for that new input; the PPM-based settings cannot simply be assumed to carry over unchanged. Those are downstream design consequences, not work performed here.

### Subsequent discussion — pool findings are conditional on the measure

Charles correctly pointed out that our earlier player-pool and playing-time diagnostics tested **PPM**, not every possible performance measure. Their negative findings therefore concern the specific pool definitions, year, and PPM construction tested. They do not establish that revisiting those same definitions would be uninformative for PER or BPM. This qualification narrows the preceding recommendation against additional filters: a single scientifically motivated pool comparison under a different measure is a reasonable proposal, even though a broad threshold search remains unjustified.

The reason is that measure and pool can interact. A player with few minutes may have an unstable scoring rate, an unstable broader box-production rate, or both. Changing the measure changes the contribution of assists, rebounds, turnovers, and other recorded production; consequently, the same retained or excluded players can affect the team distribution differently. A higher sorting index after restricting the pool would still not establish a truer talent measure. Roster size, coach selection of minutes, statistical reliability, and the scientific definition of the competition pool remain alternative explanations.

**Proposal only:** if Charles wishes to revisit this, use one previously defined playing-time contrast for PPM and PER on matched identities, rather than search new thresholds or treat BPM's team-adjusted sorting as the target. The previous top-ten-minute anchor diagnostic is a candidate because it is already specified and can describe team measurements without automatically excluding bench players from the eventual competition pool. Anchor membership would need to stay fixed across measures, unavailable values must not cause silent replacement of anchors, and a roster-size reference would be needed before crediting minutes-based selection for an increase in sorting. Those details have not yet been settled or implemented.

The same-pool three-measure audit did not calculate a measure-by-pool comparison or new interval-overlap counts. Its results show how measured clustering changes with the measure on the shared population; they do not settle the best measure/pool combination. No new execution is authorized by this discussion update.

## Evidence and reproducibility

- Protocol: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260927_performance_metric_audit_scope.md`.
- Driver: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/ASSORT_20260927_performance_metric_audit_v1.py`.
- Execution record: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/run_records/ASSORT_20260927_performance_metric_audit_v1_run_record.json`.
- Input population: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz`; its checksum matched the original rotation-audit execution record.
- Advanced sources: `datasets/mbb/DO_NOT_ERASE/bpm_player_season_matched.csv`, `bpm_player_season_raw.csv`, and `sr_school_slug_crosswalk.csv`.
- Numerical outputs: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/performance_metric_audit_2015/`, with the common-player data, excluded-player data, identity sample, measure summaries, team intervals, rank correlations, and JSON summary.
- Prior source review: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260927_SCOUT_response_performance_metric_provenance.md`. Its join counts were reproduced; its unresolved lineage questions remain explicit above.

The driver verified that input/code hashes were unchanged during execution. A separate read-only verification confirmed every numerical-output checksum and the sample-minute differences and excluded team. VECTOR reviewed all 24 displayed identity records. No source files, older outputs, matching pipeline, or model code were modified. Direct methodology pages returned access errors during this review; indexed excerpts from the primary official pages supplied the cited definitions. The full version-specific college estimators were not independently reconstructed.
