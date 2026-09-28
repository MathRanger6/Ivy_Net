# 2015 basketball audit: six-game minutes source recovery

**Status:** Completed, bounded source recovery on September 27, 2026. This is a source audit, not a rotation-analysis result. No frozen game data, season panel, or existing simulation artifact was changed. The rotation audit remains pending the remaining design questions.

## Why this was done

The frozen basketball game file has 105 player-game rows in six games with recorded points but missing minutes. Exactly 100 of those rows belong to the previously identified eligible player-season set. Excluding all 105 rows would discard substantial recorded play, so Charles authorized a six-game source check before applying the agreed fallback rule: when minutes cannot be verified, exclude both that row's points and minutes from the new audit.

The original archived game JSON for game `400588733` also reports missing player minutes, so re-reading that same feed would not recover them. Independent game-specific box scores at Sports-Reference report player minutes and points for all six games. Their team points match `datasets/mbb/mbb_df_sched.csv`; each regulation team has 200 total player-minutes, and each team in the Boston University–Holy Cross overtime game has 225.

| Frozen game ID | Game-specific box score | Frozen score check | Rows matched |
| --- | --- | --- | ---: |
| `400588733` | [Kennesaw State at Northern Kentucky, January 14](https://www.sports-reference.com/cbb/boxscores/2015-01-14-northern-kentucky.html) | 72–76 | 19 |
| `400587124` | [Boston University at Holy Cross, December 31](https://www.sports-reference.com/cbb/boxscores/2014-12-31-holy-cross.html) | 75–72, overtime | 19 |
| `400595623` | [Central Baptist at New Orleans, December 30](https://www.sports-reference.com/cbb/boxscores/2014-12-30-new-orleans.html) | 60–90 | 11, New Orleans only |
| `400586911` | [Western Illinois at Cleveland State, December 7](https://www.sports-reference.com/cbb/boxscores/2014-12-07-cleveland-state.html) | 54–76 | 26 |
| `400595585` | [Langston at Southeastern Louisiana, November 30](https://www.sports-reference.com/cbb/boxscores/2014-11-30-southeastern-louisiana.html) | 80–92 | 10, Southeastern Louisiana only |
| `400586692` | [Arkansas at Southern Methodist, November 25](https://www.sports-reference.com/cbb/boxscores/2014-11-25-southern-methodist.html) | 78–72 | 20 |

The repository schedule stores some evening games under the next calendar date in Coordinated Universal Time; the displayed game dates above are the local dates shown by the box scores.

## Match rule and result

The reproducible reconciliation is in `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/data/source_recovery_2015/reconcile_boxscores.py`. It selects the expected team table for each frozen game ID and accepts a player only when normalized names and points agree. Two explicit spelling/suffix aliases were checked against their team and identical points: frozen `Mohammed Conde` ↔ source `Mohamed Conde` (8 points); frozen `Ben Emelogu II` ↔ source `Ben Emelogu` (0 points). The script does not fuzzy-match or estimate minutes.

The row-level result is `3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/data/source_recovery_2015/minutes_recovery_overlay.csv`. It retains the frozen row identifiers, frozen points, source name, source points, recovered minutes, source URL, and SHA-256 hash of the saved source page. All **105 of 105 rows matched** on game, team, name (including the two documented aliases), and points. Together they account for **757 recorded points**. Of those rows, **101 have positive minutes** and **four have zero minutes and zero points**. The latter four are not court appearances. Among the previously identified 100 eligible player-season rows, 99 have positive recovered minutes and one has zero.

The six HTML source snapshots and one original-feed JSON example are kept only in `data/source_recovery_2015/` to make this audit reproducible. The frozen source `datasets/mbb/mbb_df_player_box.csv` is unchanged. The overlay is **not automatically applied** to any panel or prior result. A subsequent audit may explicitly join the overlay by frozen source row, count only positive verified minutes as play, and retain the agreed exclusion fallback for any later unmatched row. These recovered minutes are independently published observations, not values calculated from the team's 200- or 225-minute total.

**Remaining limitation:** This check uses one independent box-score publisher for row-level minutes. Game/team/points agreement is strong internal corroboration, but this step did not compare every player minute against each school's original box score. No claim about the substantive rotation pattern follows from this recovery alone.
