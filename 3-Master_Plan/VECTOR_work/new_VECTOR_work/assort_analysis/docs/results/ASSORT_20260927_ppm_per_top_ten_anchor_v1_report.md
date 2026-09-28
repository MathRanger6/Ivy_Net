# Fixed top-ten-minute anchors: a different result for PPM and PER

**Date:** September 27, 2026  
**Status:** Executed and reviewed by VECTOR.  
**Authorization:** Charles requested application of the previously discussed ten-player minute-anchor comparison to season points per minute (PPM) and Player Efficiency Rating (PER). “Ten minute anchor” means the **ten players with the highest total season minutes**, not a ten-minutes-per-game cutoff.

## What this comparison tells us

Charles's qualification was consequential: the earlier negative player-pool findings concerned PPM. Applying the same fixed playing-time anchor identities to PER gives a different sorting result.

For **PPM**, the overall sorting index ($H_{\mathrm{sort}}$) increases from **0.06317** with all matched players to **0.06995** with the fixed minute anchors. However, random within-team subsets of the same sizes have a mean index of **0.08102**. Ninety-nine of the 100 random-subset indices are at or above the anchor index. Thus minutes-based anchoring again does not reveal stronger PPM sorting than the size-matched reference.

For **PER**, the index increases from **0.10894** to **0.13768**, compared with a random-subset mean of **0.12602**. The fixed anchor index exceeds all 100 random-subset values, whose range is **0.11709–0.13619**. The anchor index is about **0.01166**, or 1.17 percentage points of explained player variation, above the random-subset mean. That departure is modest in absolute size, but it is a different result from PPM in this bounded reference.

PER's intervals also narrow more under the minute-anchor rule. Their equal-team mean width falls **20.7%**, compared with **13.1% for PPM**, on fixed standardized scales. Both measures narrow more under minute anchoring than under random subsets. Importantly, narrower intervals and stronger sorting are separate findings: PPM achieves extra narrowing without extra sorting relative to its reference; PER achieves both.

**The supported conclusion is that the measure and the playing-time-based descriptive pool interact in this 2015 comparison.** It is no longer appropriate to carry the PPM pool result over to PER. We have not established a truer measure of talent, a causal effect of playing time, or a new definition for who competes in the model.

## The narrated sequence

First we tested player-pool definitions using PPM. Some intervals narrowed, but the tested minute restrictions did not uncover stronger sorting relative to suitable references. We then compared three performance measures on the same players. PER showed more sorting than PPM, but their full-pool interval widths were nearly identical.

Charles then observed that changing the measure could change which pool definition is informative. We therefore applied one existing definition rather than search additional thresholds: the original ten-highest-minute anchors, held fixed across PPM and PER. We preserved the accepted season minutes, source values, and team assignments. We also drew 100 fresh within-team random subsets, identical across the two measures, with exactly the same per-team counts as the available anchors.

Next we calculated intervals, overlap coverage, and sorting from each same membership. The result tells us that PER's high-minute anchors are more clustered by team than its matched-size random subsets, whereas PPM's are less clustered than their random reference on average. This answers the narrow proposed contrast. It does not establish why PER behaves differently; reliability, roles, coaching, recruitment, and source construction remain possible contributors.

Finally, we verified original anchor identities, recorded memberships and counts, variance decompositions, scale invariance, subset containment, and source/output checksums. VECTOR inspected the comparison figure and redrew its sorting and width panels on matching vertical scales. That visual amendment did not change numerical outputs.

## Exactly which players and teams were compared

The fixed source remains the accepted **4,267-player, 351-team 2015 rotation audit**. Selecting the ten highest total-minute players per team, with player identifier resolving minute ties and all players retained on smaller teams, gives the original **3,501 anchors**. Their identities agree exactly with SCOUT's saved version-two selections.

The PPM/PER comparison needs finite PER but does not need BPM. It therefore uses **4,163 players on 350 teams**, including the two usable-PER players omitted from the earlier three-measure comparison because BPM was missing. The **104 comparison exclusions are 2.44%** of the accepted source. All 13 accepted Cleveland State players lack saved PER, so that team is absent from every case here.

Intersecting the original anchors with PER availability leaves **3,413 anchors**. The **88 unavailable original anchors** include ten on the excluded Cleveland State team and 78 on the remaining teams. No next-ranked player replaced an unavailable anchor. Effective counts among comparison teams are ten on 278 teams, nine on 58 teams, eight on 13 teams, and seven on one team. Some counts below ten reflect originally small eligible rosters; others reflect missing PER. The saved team-count table distinguishes these cases.

The anchor and random cases use exactly the same team counts and total count. Random draws sample from each team's full matched population without replacement. They do not shuffle players between teams. The fresh 100 draws use NumPy's PCG64 generator, master seed `20260927`, sorted team identifiers, and sorted player identifiers. Memberships are saved for all **341,300 player-by-repetition records**.

**The original competition pool is unchanged.** Players outside the descriptive anchor group remain in the accepted audit file. PER-unavailable players are absent from this comparison because the measure cannot be evaluated for them; they have not been declared ineligible for future research.

## Numerical comparison

For each measure, the standardized scale is fixed using its own full 4,163-player comparison-population mean and population standard deviation. The anchor and random groups are not independently restandardized. The sorting index weights players equally; mean interval widths weight teams equally.

**PPM:**

- All matched players: sorting **0.06317**; mean interval width **3.259** standard deviations.
- Fixed minute anchors: sorting **0.06995**; mean width **2.832**.
- Random matched-size subsets: mean sorting **0.08102**, range **0.06624–0.08868**; mean of repetition-level mean widths **3.072**, range **3.018–3.119**.
- Minute anchoring narrows mean widths by **13.1% versus all matched players** and **7.8% versus the random mean**. No random repetition has a mean width as small as the fixed anchors. However, 99 of 100 random repetitions have sorting at least as high as the anchors.

**PER:**

- All matched players: sorting **0.10894**; mean interval width **3.246** standard deviations.
- Fixed minute anchors: sorting **0.13768**; mean width **2.574**.
- Random matched-size subsets: mean sorting **0.12602**, range **0.11709–0.13619**; mean of repetition-level mean widths **3.035**, range **2.991–3.086**.
- Minute anchoring narrows mean widths by **20.7% versus all matched players** and **15.2% versus the random mean**. No random repetition has a mean width as small as the fixed anchors, and none has sorting as high as the fixed anchors.

The raw anchor-minus-full sorting increase is about **0.00679 for PPM** and **0.02873 for PER**. Their difference is **0.02195**, or 2.19 percentage points. Those raw changes include the effect of selecting fewer players. The matched-size references are necessary before attributing a change specifically to the minute criterion.

The counts among 100 random repetitions describe this fixed, within-team subset reference. They are not presented as a population-level p-value, evidence from 100 independent seasons, or proof of a causal mechanism. In particular, “above all 100” does not establish that no possible random subset could exceed the PER anchor result.

## What the figure shows

![2015 PPM and PER anchor comparison](../../outputs/ppm_per_top_ten_anchor_2015/ASSORT_20260927_ppm_per_top_ten_anchor_v1_comparison.png)

The upper panels count team intervals containing each standardized performance value. Blue uses all matched players, orange uses fixed minute anchors, and the dashed gray curve is the pointwise median across random-subset repetitions. The gray band is the pointwise central 80% of those repetitions. Those summaries describe repeated subset draws, not confidence intervals for a larger population.

PER's anchor curve contracts more visibly on the low-performance side. Nevertheless, **central overlap remains extensive**: the maximum coverage on the saved 801-point grid is 349 of 350 teams for both full and anchor PER intervals. PPM reaches 350 for both. Unchanged maximum coverage does not negate the narrowing elsewhere; it shows that narrower ranges have not made the team intervals disjoint. Coverage counts and their maxima are evaluated on the recorded finite grid, rather than asserted as exact continuous maxima.

The middle panels compare mean interval widths; the lower panels compare sorting indices. Both columns use identical vertical scales within each row. Do not read interval width as latent-talent variance or a mean of the anchor players as the full team's measured mean.

## Scientific interpretation and limits

PER records more box-score dimensions than scoring rate alone. Selecting established high-minute players can affect its lower-end distribution differently from PPM. The observed result is consistent with low-exposure or role-dependent PER values broadening the full-pool distributions, but this audit did not isolate those mechanisms. Playing time is itself selected by coaches and may reflect quality, role, health, roster depth, or congestion. A high-minute anchor analysis therefore changes the descriptive target as well as possibly changing measurement reliability.

The original PPM-versus-PER source qualification also remains: PER is a saved Sports-Reference season estimator; PPM is rebuilt from our accepted ESPN-based source rules. Earlier sampled minute totals did not always agree. This is a comparison of recorded measures and source constructions, not a pure formula substitution on identical game totals. The small prior identity audit supports internal consistency; it does not establish full linkage accuracy. Cleveland State's complete PER absence and other missing values are not repaired here.

There is no single “true assortativity” established by these calculations. The result supports considering PER and this fixed rotation-anchor definition together for a **named descriptive sensitivity**. It does not justify redefining every low-minute player out of the competition pool, adopting PER as portable ability, or changing the model's congestion term to the anchor mean without a separate scientific decision.

**Stopping point:** one previously proposed anchor definition has now been evaluated for two measures. This is evidence against generalizing the earlier PPM-only dead end, and a reason to discuss PER's intended role. It is not a reason to launch additional anchor sizes or filtering sweeps. No further analysis or simulation was started.

## Reproducibility record

- Scope and decisions: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260927_ppm_per_top_ten_anchor_scope.md`.
- Driver: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/ASSORT_20260927_ppm_per_top_ten_anchor_v1.py`.
- Execution record: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/run_records/ASSORT_20260927_ppm_per_top_ten_anchor_v1_run_record.json`.
- Accepted input: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz`.
- PER source: `datasets/mbb/DO_NOT_ERASE/bpm_player_season_matched.csv`.
- Frozen original anchors: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v2_player_selections_high_minute.csv`.
- New numerical exports and figure: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/ppm_per_top_ten_anchor_2015/`. These include player memberships, unavailable anchors, team counts, fixed interval tables, fixed summaries, all random memberships and repetition summaries, the coverage grid, and a JSON summary.

The first launch in bundled Python stopped at import because Matplotlib was unavailable; it created no analysis results. The completed run used the existing local Python 3.9.6, NumPy 2.0.2, pandas 2.3.3, and Matplotlib 3.9.4 without installing packages. The record preserves the numerical-run code hash and a separate code/figure hash for the visual-only common-scale amendment. A separate read-only verification recomputed anchor indices, checked every random membership's team counts and uniqueness, and confirmed every output hash. VECTOR inspected the figure. No source, previous output, pipeline, or model file changed.
