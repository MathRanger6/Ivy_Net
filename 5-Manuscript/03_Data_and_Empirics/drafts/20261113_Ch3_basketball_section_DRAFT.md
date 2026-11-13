# Chapter 3 — Basketball and the NBA draft (section draft)

FOUNDY | 13 November 2026 | DRAFT for Charles

**Built from:** SCOUT's answers (`notes/20261113_SCOUT_Response_Ch3_basketball.md`), SCOUT's source register (`notes/20261113_MBB_DATA_SOURCES_register.md`), and a read of the code and saved outputs for the run of record. No pipelines were rerun.

**How to read the footnotes:** each one starts with **Verified** (checked in code, data or a saved output on 13 November; path given), **Recalled** (from SCOUT's memory or an older document), or **TK** (still to be supplied). Scrub the footnotes before Word. Where the code disagreed with SCOUT's note, the prose follows the code and the footnote says so.

Section numbers are placeholders until the chapter is assembled. The seven-part shape matches the other systems.

---

## X.1 Why this system fits

College basketball players are measured game by game. Box scores record each player's minutes and points in every game, so a season's performance is observed directly, before and apart from the draft decision it may influence.[^fit-perf] Players belong to teams, and a team in a season is the group. Rosters are assembled by recruiting, scholarship limits and coaching decisions; they are not a random draw from the population of players.[^fit-group] The NBA draft selects from across all of college basketball at once, not separately inside each team, so selection is global. The number of places is limited: the draft has two rounds and sixty picks a year, and in the thirteen drafts from 2009 through 2021 it made 780 picks.[^fit-picks]

The system fits two criteria only partly. First, the places are limited, but college players do not have them to themselves. Players from international leagues and other paths compete for the same picks, so the number of places available to college players is not fixed in advance. Second, the system is less closed than the Army. New players enter each season, which is the normal flow of any cohort, but players also transfer between teams, and the draft brings in competitors we never observe in the college data.[^fit-closed] A third limitation concerns groups. Teams are not formed at random, but the measured sorting of players by scoring rate is weak: which team a player is on explains little of the variation in performance.[^fit-sort] Peer quality still varies from team to team, which is what this chapter needs. How groups form is the subject of the assignment chapter.

## X.2 How the data were found

The aim from the start was to link who was drafted to how strong a player's teammates were, using public data only.[^story-aim] The first durable choice was to build everything on ESPN's men's college basketball box scores, obtained through the open-source sportsdataverse and hoopR loaders. These give stable identifiers for players, teams and seasons, which a panel needs.[^story-espn] Early work moved data across several separate notebooks. It was later consolidated into a single pipeline with one entry point, so that the panel could be rebuilt in a fixed order.[^story-pipeline]

Draft outcomes came from a consolidated register of NBA draft picks.[^story-draft] Linking that register to the box scores was the most labor-intensive step. Draft records list a player's name and college as text, and neither matches ESPN's records exactly. Automatic name matching was supplemented by a hand-built list that maps the college names used in draft records to ESPN's school names, and by manual review of the players who failed to match.[^story-match] An off-the-shelf record-linkage package was considered for this step and set aside; the matching was done with the hand-checked lists instead.[^story-dedupe]

Advanced statistics from Sports-Reference were scraped later and attached to the same ESPN player records, to allow other measures of performance to be compared. An attempt to treat Sports-Reference as a separate set of players, without matching to ESPN, was dropped. Those statistics are not used in this chapter's figure.[^story-sr]

The design settled when the panel rules were fixed for the figure used here: seasons 2009 through 2021, points per minute as the performance measure, each player's final season as the unit, and teammates' leave-one-out average as peer quality.[^story-lock]

## X.3 Sources and how they were linked

Two sources feed the analysis.

**Box scores.** Each row is one player's appearance in one game, with ESPN's player identifier, the team, the season, minutes and points.[^src-box] The file on disk covers the seasons from 2003 through 2025. This chapter uses 2009 through 2021.[^src-box-years]

**Draft register.** Each row is one drafted player. The register covers the drafts from 1989 through 2021, 1,922 players in all.[^src-draft] Its original download source and date are not recorded in the repository.[^src-draft-tk]

The two are joined by matching the drafted player's name, college and year to ESPN players, using the hand-maintained college-name list and manual review of misses.[^link-method] The result is a list of ESPN player identifiers who were drafted. How many draft records were matched, how many were reviewed by hand, and which drafted college players remain unmatched have not yet been tabulated.[^link-rate] Players who were drafted without playing college basketball cannot match by design.

## X.4 Cleaning and the final sample

The panel is built in the order below.[^flow-order]

1. Keep box-score rows for the seasons 2009 through 2021.
2. Drop rows whose player name is a placeholder dash.
3. Drop team-seasons with ten or fewer distinct games in the box data, which removes fragmentary schedules.
4. Add up each player's minutes and points for each team and season.
5. Drop player-team-seasons with fewer than 20 minutes in the whole season.[^flow-min]
6. Mark each player as drafted or not, from the matched draft list.
7. Compute points per minute and standardize it within each season.
8. Compute each player's peer quality from the teammates who remain after steps 3 and 5, and trim extreme values at the 1st and 99th percentiles.
9. Keep one row per player: the player's last season in the window. A player who appears for two teams in that season keeps the team where he played more minutes.

The order matters for what peer quality means. Because steps 3 and 5 come before step 8, a teammate who played fewer than 20 minutes in the season does not count as a peer. Because step 9 comes after step 8, a player's peer quality is computed from his full team that season, not only from teammates who were also in their final season.

| Step | Count after |
|---|---|
| Box-score rows read, 2009–2021 | TK |
| After dropping placeholder names | TK |
| After dropping team-seasons with ten or fewer games | TK |
| Player-team-seasons with at least 20 minutes | TK |
| Rows with a defined peer quality | TK |
| One row per player, final season (analysis sample) | **22,795 players, 615 drafted** |

The final count and the number drafted come from the saved record of the run.[^flow-final] The intermediate counts were printed by the pipeline when it ran but were not saved, and can be recovered by rerunning the panel build.[^flow-tk]

## X.5 The four concepts

| Concept | Definition | Variable |
|---|---|---|
| Performance | Points per minute over the season, standardized within season | `perf` (from `ppm`) |
| Group | Players on the same team in the same season, after the floors in X.4 | team and season |
| Peer quality | Average standardized performance of the other players in the group | `poolq_loo` |
| Advancement | Drafted in any draft covered by the register | `Y_draft` |

**Performance.** For player $i$ in season $s$, points per minute is total points divided by total minutes. It is then standardized against every player-season in the sample that season, $z_{is} = (\mathrm{PPM}_{is} - \bar{\mathrm{PPM}}_s)/\sigma_s$, so that a value of 1 means one standard deviation above that season's average.[^c-perf]

**Group.** The group is the team in a season. A player who transferred appears in two groups, one for each team.[^c-group]

**Peer quality.** Peer quality is the leave-one-out mean of teammates' standardized performance:

$$
C_{\mathrm{LOO},i} = \frac{1}{n_g - 1} \sum_{h \in g,\ h \neq i} z_h ,
$$

where $g$ is the player's team-season and $n_g$ is the number of players in it. This is the measure labeled B2 in the chapter's comparison of peer measures. It is not the full-team average including the player, and it is not the player's own performance minus that average.[^c-peer-label] Every teammate counts equally, whether he played 25 minutes or 900.[^c-peer-unweighted] Values below the 1st percentile or above the 99th are set to those percentiles.[^c-peer-winsor] A player with no qualifying teammates has no peer quality and drops out.

**Advancement.** A player counts as advanced if he appears on the matched draft list, whatever the year of the draft. The outcome is attached to his final season in the window. Every other player in the sample counts as not drafted and stays in the denominator.[^c-adv]

## X.6 What this system cannot give us

Points per minute is one box-score statistic. It leaves out defense, passing, size, age and the scouting judgments that a draft decision weighs. The draft field is open: international players and others compete for the same picks, and we observe only the college players. The college-linked share of picks is therefore not a fixed number of places. Matching drafted players to box scores depends on names and schools, and its error rate has not been measured. Teams sort players only weakly by performance. Peer quality is an equal-weight average of teammates, so a rarely used reserve counts as much as a starter.

The edges of the window also matter. A player whose career continued after 2021 has his 2021 season treated as his last, and the draft register ends with the 2021 draft. Such a player who was drafted in 2022 or later is counted here as not drafted.[^edge]

## X.7 The descriptive result

**Placeholder figure:** `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps.png`

The figure divides the 22,795 players into sixteen groups of nearly equal size, about 1,425 each, by the quality of their teammates, and shows the share drafted in each group. The share drafted ranges from 1.9 percent to 3.5 percent. It drifts upward from the weakest-peer groups to the strongest, with no peak and no decline at the top. With about 1,425 players per group and an average draft rate near 2.7 percent, the share in any single group has a sampling error of roughly half a percentage point, so most of the variation between neighboring groups is noise.[^res-hero]

Own performance, by contrast, sorts players sharply. Grouped the same way by their own points per minute, no player in the bottom five groups was drafted, and the share rises to 16 percent in the top group.[^res-own]

On the full sample, then, stronger teammates are not associated with a lower draft rate. Whether the pattern differs for players of similar own performance, near the level at which players are drafted, is a separate display.[^res-boe]

---

## Flags for Charles before this goes into Word

1. **SCOUT's note has the filter order backward for this run.** SCOUT wrote that the 20-minute and 10-game floors are applied after peer quality is computed. In the run of record they are applied before (`panel_rebuild.build_from_box`, called through `pass_a_empirical_bundle._prepare_hero_panel` with `y_draft_mode = ever`). The "floors after peer quality" order exists only in the other labeling mode (`season`), which this figure does not use. The prose follows the code. Worth asking SCOUT to correct A5 and B6.
2. **"min20" is 20 minutes in the whole season, not per game.** That is a very low floor. Your settled list said "minute floor ≥ 20"; the prose says "in the whole season" so no reader takes it as per game.
3. **The canonical basketball figure is flat.** It shows no inverted U, and the plot itself prints "flat / not concave on this panel." This does not conflict with SCOUT, but it does conflict with the executive summary's plan to state "the same shape" across systems. The result sentence there must not claim the basketball shape until you decide whether Chapter 3 shows only this full-sample figure or also the Band of Excellence view for players near the draft level. X.7 is written to leave that open.
4. **The 2021 edge.** Players still in college after 2021 have 2021 treated as their final season, and anyone drafted in 2022 or later counts as undrafted. The box-score file runs through 2025, so the number affected can be counted from data already on disk. That is a small new count, not a rerun, but I did not do it. Your call whether to count, restrict the window, or state it as a limitation (as drafted).
5. **615 is not a match rate.** 615 drafted players in the sample against 780 picks mixes three things: non-college draftees, college draftees who failed to match, and drafted players who fall outside the sample (for example under the minutes floor). The prose does not divide one by the other.
6. **Criterion 2 is weak here.** Basketball teams are not formed at random, but measured sorting by scoring rate is near zero. The prose claims only that rosters are institutionally formed and that peer quality varies across teams. It points to the assignment chapter for the rest.
7. **Criterion 5 and the executive summary.** The summary's criteria paragraph says the peers a person is compared with are the people competing for the same places. In basketball the competitors include players we never observe. The prose treats this as the main way basketball fits the closed-system criterion only partly.
8. **Peer quality is an equal-weight average.** A reserve with 25 minutes counts as much as a starter. This is stated as a limitation, not fixed.

## Executive summary changes made

In `20261109_Ch3_executive_summary_DRAFT.md`, the basketball paragraph now says the seasons are 2009 through 2021 (verified in the run record; bracket removed). It says the draft's sixty places are shared with players from outside college basketball, and it adds the open field to what this system cannot give us. Open item 4 is marked resolved. No other paragraph was changed.

---

[^fit-perf]: **Verified.** Season totals are built from game rows in `sports/sports_pipeline/panel_rebuild.py` (`build_from_box`).
[^fit-group]: **Recalled.** Institutional description; SCOUT A1.
[^fit-picks]: **Verified.** 780 rows with draft year 2009–2021 in `datasets/mbb/DO_NOT_ERASE/nbaplayersdraft.csv` (SCOUT B1, read 13 November). Sixty per year is the two-round format.
[^fit-closed]: **Verified** for transfers (one row per player, team and season; `build_from_box` groups by athlete, season and team). **Recalled** for the share of non-college draftees; not counted.
[^fit-sort]: **Verified.** `3-Master_Plan/re_entry/HEROs_and_PASSes/MBB_empirical_roster_select_replay.md`: about 6 percent of variation in ability is between teams; estimated homophily near zero.
[^story-aim]: **Recalled.** SCOUT A2.
[^story-espn]: **Verified** that the loaders are named in `sports/sports_pipeline/ingest_box.py` and `data_integrity.py` (SCOUT register, row 1). **TK:** the download command and date of the last full refresh.
[^story-pipeline]: **Verified.** `sports/documents/SPORTS_DATA_GAMEPLAN.md` (the `530_sports_pipeline.ipynb` conductor and `sports_pipeline` modules replacing the separate notebooks).
[^story-draft]: **Verified** file and counts. **Recalled** origin: advisor memos cite Basketball-Reference; an older note suggests a hoopR or GitHub table. Not proven from the file.
[^story-match]: **Verified.** `SPORTS_DATA_GAMEPLAN.md`, Stage 2a–2c; `datasets/mbb/DO_NOT_ERASE/college_aliases.csv`; `draft_match_manual_feedback_template.csv`.
[^story-dedupe]: **Verified.** `SPORTS_DATA_GAMEPLAN.md`, working agreement, point 2.
[^story-sr]: **Verified** that the figure uses points per minute only (`perf_metric: ppm` in the provenance file). **Recalled** for the dropped Sports-Reference spine (SCOUT A2).
[^story-lock]: **Verified.** `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json`. **TK:** the date the lock was set, and whether Alex chose points per minute in a specific meeting (SCOUT tags this recalled).
[^src-box]: **Verified.** Columns read in `build_from_box`: game, athlete, season, team, names, minutes, points.
[^src-box-years]: **Verified.** SCOUT register row 1, checked 13 November.
[^src-draft]: **Verified.** SCOUT B1 and register row 3. SCOUT gives both 1,921 and 1,922 rows in different places; confirm which before print.
[^src-draft-tk]: **TK.** Register, gap 1.
[^link-method]: **Verified.** `SPORTS_DATA_GAMEPLAN.md`, Stage 2.
[^link-rate]: **TK.** The lookup file is recalled at 789 drafted players with draft years 2005–2021 (register row 5); not recounted.
[^flow-order]: **Verified** from code, not from SCOUT's note. Steps 1–6: `panel_rebuild.build_from_box` and `_apply_box_qc`. Steps 7–8: `panel_build.apply_perf_metric_for_analysis` and `recompute_teammate_loo_pool_quality`. Step 9: `y_draft_mode.restrict_to_last_season_rows`. Called in that order by `sports/scripts/pass_a_empirical_bundle.py`, `_prepare_hero_panel`, for `y_draft_mode = ever`. SCOUT's A5 and B6 say the floors come after peer quality; that is true only for the `season` labeling mode, which this figure does not use.
[^flow-min]: **Verified.** `minutes` is the sum over the season's games; the floor is `minutes >= 20`.
[^flow-final]: **Verified.** Provenance file: `n_rows` 22,795, `n_drafts` 615.
[^flow-tk]: **Verified** that `box_qc_provenance_lines` prints these counts; **TK** values.
[^c-perf]: **Verified.** `panel_build.standardize_perf_zscore_by_season`, applied before the final-season restriction, so the reference is all player-seasons in the sample that season.
[^c-group]: **Verified.** Grouping key is team and season in `recompute_teammate_loo_pool_quality`.
[^c-peer-label]: **Verified.** Labels from `3-Master_Plan/re_entry/PEER_INFLUENCE_AXES_MISMATCH.md`. The provenance file names the axis "LOO teammate mean perf z; self excluded."
[^c-peer-unweighted]: **Verified.** The formula is (team sum minus own value) divided by (count minus one), with no minutes weight.
[^c-peer-winsor]: **Verified.** `poolq_winsor_quantiles = (0.01, 0.99)`, applied to peer quality over all player-seasons before the final-season restriction.
[^c-adv]: **Verified.** `Y_draft` is membership in `athlete_id_draft_lookup.csv`, set in `build_from_box`; provenance `y_draft_mode: ever`, `panel_rows: last-ps`.
[^edge]: **Verified** from code that the window is applied before the final-season restriction, and that the register ends with 2021. **Not counted** how many players are affected. See flag 4.
[^res-hero]: **Verified.** `pass_a/PASS_A_binned_draft_rate_poolq_loo_q16_allt_min20_mg10_9_21_last_ps.csv`: lowest bin 1.90 percent, highest 3.51 percent. The figure's own annotation reports a quadratic coefficient of +0.0017, "flat / not concave on this panel." The sampling error is the binomial standard error, $\sqrt{0.027 \times 0.973 / 1425} \approx 0.004$.
[^res-own]: **Verified.** `pass_a/PASS_A_binned_draft_rate_ability_q16_allt_min20_mg10_9_21_last_ps.csv`: 0 percent in bins 1–5, 16.0 percent in bin 16.
[^res-boe]: **Recalled.** SCOUT A12 lists a Band of Excellence figure that fixes own performance in a band and varies peer quality (`basic_data_plots/CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.png`). The `dft` tag in its filename indicates a different sample (teams with at least one drafted player). Not reviewed for this draft.
