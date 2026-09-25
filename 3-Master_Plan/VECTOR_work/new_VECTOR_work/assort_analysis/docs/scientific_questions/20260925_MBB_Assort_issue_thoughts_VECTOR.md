# Why measured basketball assortativity may be small: a scientific note for Charles and Alex

**VECTOR | September 25, 2026**  
**Status:** Scientific interpretation and proposed *bounded* diagnostic. No new calculation, model run, figure, or source-data change was made for this note. The previously authorized assortativity experiment remains paused after Charles's “stop the presses” instruction.  
**Read alongside:** [SCOUT's evidence note](20260925_MBB_Assort_issue_thoughts_SCOUT.md) and [COMPASS's framing note](20260925_MBB_Assort_issue_thoughts_COMPASS.md). They were written separately, at different points in today's discussion. I retain their positions below and mark disagreements rather than silently combining them.

## My answer to the central question

Charles's intuition is plausible: Duke and UConn probably recruit from a much stronger latent-talent pool than a randomly chosen college team. The present result does **not** test that proposition directly. It tests how much *between-team* variation exists in **observed season scoring rate**, after a specific set of data filters. The player who scores well in a small role, the elite defender who seldom shoots, and the high-usage star are not placed on a single latent-talent scale merely by dividing points by minutes. Therefore a small sorting statistic for this measure cannot establish that basketball recruiting is unassortative.

But I would not yet say we have demonstrated a measurement artifact. The measured sorting may be genuinely modest for this particular outcome-relevant skill, and the existing team's roles may produce wide within-team differences even at elite programs. The next useful question is narrower: **Does the low result persist when we describe the actual playing-time distribution and distinguish roster membership from credible rotation participation?** That is one focused diagnostic, not a search across many filters for a preferred curve.

There are **two** scarcity constraints in Charles's account. Very few players are drafted; at most five teammates can play simultaneously. They act at different stages. The first concerns the final selection outcome. The second structures opportunities for minutes, shots, and lineups, which can affect our measured ability before selection is even analyzed. Five on court does **not** mean that a team has exactly five relevant peers over a season: more than five players rotate, players at different positions may compete for different minutes, and teammates on court can also *help* one another score. The causal issue is opportunity and role, not a literal five-person roster. The proposed experiment's **one-percent selection fraction** is a chosen scarcity setting, not the measured rate of *ever* being drafted on the historical hero panel; those denominators and time horizons differ. Source: `3-Master_Plan/VECTOR_work/new_VECTOR_work/VECTOR_PD41_Assortativity_Scientific_Brief.md` §3 and `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md`.

## What the current statistics actually say

For athlete $i$ on team $j$ in season $s$, the pipeline defines season points per minute (PPM) from retained game rows as

$$
\operatorname{PPM}_{ijs}
=\frac{\sum_{g\in G_{ijs}}\operatorname{points}_{ig}}
       {\sum_{g\in G_{ijs}}\operatorname{minutes}_{ig}},
\qquad
A_{ijs}=\frac{\operatorname{PPM}_{ijs}-\overline{\operatorname{PPM}}_s}
                 {\operatorname{SD}_s(\operatorname{PPM})}.
$$

PPM is constructed once at player-season aggregation; it is not an ESPN source column. The analysis copies that column into its performance field, standardizes it within season, then computes each focal player's leave-one-out (LOO) teammate mean. These facts are visible in `sports/sports_pipeline/panel_rebuild.py` and `sports/sports_pipeline/panel_build.py`, and are traced in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_SCOUT_response_data_hygiene_and_model_history.md` §3.6.

The empirical sorting index is

$$
H_{\mathrm{sort}}
=1-\frac{\sum_i(A_i-\overline A_{j(i)})^2}
         {\sum_i(A_i-\overline A)^2}.
$$

It is the share of the measured player-level variance accounted for by team means, using the players retained in that season. It is **not** the assignment preference parameter $\rho$, a measure of teammate exposure, or a coefficient for congestion in advancement. See `sports/541_grandchild_homophily_assign.py`, `realized_sorting_index_H_sort`, and `sports/scripts/pd21_rho_hsort_calibrate.py`, `empirical_h_sort`.

Two mathematical details matter here:

1. Within a single season, replacing raw PPM by its season-wide z-score **cannot by itself reduce or increase this $H_{\mathrm{sort}}$**. It subtracts the same mean and divides every player's value by the same positive standard deviation; the numerator and denominator above change by the same factor. The *choice of PPM and of retained players* can change the index. The z-score merely changes units. COMPASS's revised note now acknowledges this; its earlier wording, and some remaining shorthand about z-scores “absorbing” tiers, should not be used to explain a low $H_{\mathrm{sort}}$.
2. Under a random allocation of a fixed set of measured player values into a fixed collection of team sizes, $H_{\mathrm{sort}}$ is generally **positive** because finite random teams have different sample means. Under the exchangeable null, its expected value is $(J-1)/(N-1)$ for $J$ nonempty teams and $N$ athletes. Thus $H_{\mathrm{sort}}\approx0.06$ is not self-interpreting as “six percent sorting” without a same-population random-allocation reference. The August 19 calibration already supplies one model-specific comparison: its 2015 empirical value is about **0.061**, while its $\rho=0$ simulated mean is about **0.081**. In that run the nonnegative $\rho$ bracket lands at zero because the empirical target is *below* the model's zero-preference result; zero is the closest boundary, **not an exact match**. Source: `3-Master_Plan/re_entry/HEROs_and_PASSes/pd21_rho/PD21_rho_hsort_calibrate_2013_2021_fit_bracket.json`. A fresh permutation benchmark on the finally agreed population would be the clean reference, but has not been run.

### A timing correction, now reflected in SCOUT's revised note

SCOUT's first draft cited a 2015 empirical value near **0.114** and a fitted $\rho$ near **0.08** as though it came from the minimum-eleven-games-era panel. SCOUT's **revised** note now correctly labels that run as earlier. The cited file, `3-Master_Plan/re_entry/HEROs_and_PASSes/pd21_rho/PD21_rho_hsort_calibrate_2015_fit_bracket.json`, says **generated August 14** with eight simulation seeds. The eleven-game coverage rule was adopted **August 17** in `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md` §3b. The later August 19, 2013–2021 file gives the 2015 value near **0.061**. These values belong to different historical panel versions; the August 14 figure should not describe today's cleaned panel. The saved JSON does not provide a complete source checksum and every quality-control setting, so exact run-to-run attribution still has a provenance limit.

## Where Charles's five-on-court insight could matter

The production floor of **twenty total captured season minutes** does not establish that a person was a regular rotation player. Someone with twenty minutes spread across ten appearances averaged two minutes per appearance. Conversely, a strong player may log substantial minutes over fewer captured games because of injury or a transfer. A proposed **five minutes per game** rule must say whether “game” means *games with positive minutes*, *games listed on the roster*, or *all captured team games*. Those denominators answer different questions. SCOUT correctly reports that the existing production pipeline has no five-minute-per-game rule; the twenty-minute rule is a season total. Source: `sports/sports_pipeline/panel_rebuild.py` and SCOUT's data-hygiene response §3.

Short playing time makes PPM statistically unstable because a few points can dominate a small denominator. It is also potentially **selected**: a coach may award minutes based on talent, seniority, injury, matchup, and team depth. On a great team, a very capable player can be buried in the rotation. So I would not declare everyone below five minutes per game “not competition,” nor treat a minutes cutoff as a neutral cleaning step. We should distinguish **reliability of that player's measured scoring rate** from **whether that player competed for a role**.

There is a second distinction to keep explicit when reading the proposed diagnostics. The leave-one-out teammate mean is the **horizontal axis of the empirical draft curve**. The sorting index above uses **each player's ability and team label**, not the leave-one-out mean. If we hold focal players and their ability values fixed and only exclude some teammates from the curve's peer average, the curve can change, but $H_{\mathrm{sort}}$ **cannot**. To change $H_{\mathrm{sort}}$, we would have to change the athlete sample, ability measure, or team assignment. This matters for a clean diagnosis: a peer-set sensitivity is not automatically an assortativity sensitivity. COMPASS's rotation-peer hypothesis can move both quantities only if it includes a *separate* change to those inputs.

Similarly, the current experimental congestion score averages a smooth high-ability measure over every *eligible simulated team member*, including the focal player; it is not computed from court-sharing records. A rotation-restricted empirical peer average cannot be substituted into that simulation without declaring a **different model**. Source: `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/decisions/ASSORT_20260925_construction_specification_and_source_audit.md` §§3–5.

### An additional implication of five players sharing the court

The five-player constraint does more than limit *who plays*. It limits the sum of recorded player-minutes in a game. With complete regulation-game box records, the five players on court collectively account for about $5T_g$ player-minutes over $T_g$ elapsed minutes (overtime changes $T_g$). Because team points are distributed among players, the minutes-weighted average of their individual points-per-minute rates obeys approximately

$$
\frac{\sum_i M_{ig}\operatorname{PPM}_{ig}}{\sum_i M_{ig}}
=\frac{\sum_i P_{ig}}{\sum_i M_{ig}}
\approx\frac{\operatorname{team\ points}_g}{5T_g}.
$$

Here $M_{ig}$ and $P_{ig}$ are player minutes and points in game $g$. The approximation flags incomplete box records and unusual accounting; it is not a claim that our saved data already satisfy the identity. The implication is conceptual: even if **every** Duke player is highly capable, they cannot all occupy the primary scoring role in the same forty minutes. Their observed scoring rates reflect a shared production-and-role budget. Greater collective talent can raise team scoring, but individual rates need not rise in proportion to latent talent. The sorting index, moreover, uses an **unweighted** player mean, so brief appearances can influence the team's measured average as much as major rotation players. This combination offers a distinct possible route from strong recruiting sort to modest measured PPM sort. It does **not** predict the direction or size of the bias without data.

Opponent difficulty and team pace may further affect that points budget. A strong program may face stronger defenses or play a different pace than a weaker program; PPM adjusts for an individual's minutes, not for either context. I would treat that as a *possible competing explanation* alongside low-minute measurement error, rather than asserting that a rotation cutoff solves the entire mismatch. This idea needs no new modeling decision now; it tells us what a future interpretation of the bounded audit must leave open.

## Direct answers to the filter and population questions

- **Is PPM the culprit?** It is a credible suspect, because it measures scoring *rate*, not total contribution or underlying talent, and it is noisy at low minutes. It is not yet established as *the* cause of low sorting. Total points would reintroduce playing time directly, so a simple swap is not an automatic improvement. If we ever compare a second performance measure, it should be framed as a different scientific construct with its own missingness and coverage audit.
- **Is the twenty-season-minute floor too low?** Possibly for stable PPM and rotation interpretation. Its historical purpose and its consequences were already studied; it remains the reigning hero definition. We should first count how many retained athletes have very few minutes *per positive-minutes appearance* and what share of each team's measured peer pool they form. Any alternative floor changes the population and therefore the question being asked.
- **Is the eleven-captured-game team rule the problem?** It addresses fragmentary team-season capture, especially one-game opponents, rather than identifying true varsity rotation players. It is necessary data hygiene, not a guarantee of complete seasons or Division I status. We should preserve it unless a separate source audit justifies changing it. Source: `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md`.
- **Should we use Division I only?** If our claim is specifically about Division I men's basketball, then the population definition must be verified against **season-specific** institutional membership and sport sponsorship. The box file's team labels and the eleven-game rule are not by themselves a historical Division I flag. The NCAA provides a [historical membership resource](https://www.ncaa.org/news/media-center-new-ncaa-historical-resource-details-membership-history-of-schools-conferences/) that could support such a crosswalk. A present-day Division I list should not simply be applied to 2015.
- **Should we use only teams that ever produced a draftee?** Not as the main population. That conditions team inclusion on the very career outcome we study and looks forward through time. It can make a specific descriptive comparison among draft-producing programs, but it cannot answer what sorting or congestion looks like throughout Division I. We also should not select thresholds or subsets because they recover a desired inverted-U.

The **hero shape** itself needs careful labels. SCOUT documents that the July pre-cleaning, equal-count-bin tail dip was substantially driven by fragmentary teams. The later *reigning* hero uses a **last-player-season, equal-width sixteen-bin** definition and retains a right-tail drop in its saved presentation, while its fitted quadratic is flat or positively curved. These are different samples and bins, not one contradiction that can be settled by saying the downturn either “survived” or “vanished.” Sources: SCOUT's data-hygiene response §§2, 7 and `3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md`. Neither shape alone identifies the causal effect of congestion or the necessity of assortative assignment.

## One bounded check before returning to the original experiment

I recommend **one descriptive rotation audit**, on a named 2015 panel definition, before changing any model mechanism or launching another parameter sweep. For each retained athlete, report total captured minutes, games with positive minutes, and minutes per such appearance; for each team, report the count and minute share of players below a provisional five-minute threshold. Then display how the *same focal players*' leave-one-out peer values change when low-minute teammates are omitted from the peer mean. That last comparison probes the pool-axis concern while keeping the focal sample, PPM values, outcome labels, and team-game rule fixed. It does **not** estimate a new $H_{\mathrm{sort}}$ or show that the full-team congestion model is wrong.

If that audit reveals a material change, we can decide together whether a **separate**, explicitly labeled rotation-population analysis is warranted. Its sorting index must then be compared with a random-allocation baseline for its own team sizes and athlete set. We should not infer in advance that filtering will raise $H_{\mathrm{sort}}$: the direction is empirical. This is deliberately smaller than COMPASS's and SCOUT's longer diagnostic menus and respects Alex's request to settle the assortativity question without getting lost in a new campaign.

**Execution gate:** The 2015 rebuild for the original experiment already stopped on 100 otherwise eligible athletes with recorded points but missing minutes across some game rows; the canonical-team choice was approved in conversation but not yet documented or applied after the stop. Those issues matter directly to PPM and any rotation audit. The findings and file paths are in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/source_review/ASSORT_20260925_initial_execution_stop.md`. I would not call an audit result final until these source rules are settled. No such audit was executed for this note, and the original simulation remains paused pending Charles's direction.
