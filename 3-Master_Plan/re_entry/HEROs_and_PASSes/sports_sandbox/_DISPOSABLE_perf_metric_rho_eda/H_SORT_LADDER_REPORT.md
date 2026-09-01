# Sorting index (H_sort) ladder — performance-metric comparison (disposable EDA)

**Generated:** 2026-08-28  
**Folder:** `_DISPOSABLE_perf_metric_rho_eda/` — safe to delete without affecting reigning-hero work.

## Acronym and stat reference

**Read this table first.** Every acronym below is defined here before it appears alone in the rest of this report.

| Acronym | Full name | Definition |
|---------|-----------|------------|
| **2PT** | Two-point field goal | Basket scored from inside the three-point arc (counts as one field goal made). |
| **3PA** | Three-point attempts | Shot attempts from beyond the three-point arc. |
| **3PM** | Three-pointers made | Baskets scored from beyond the three-point arc. |
| **AST** | Assists | Passes that directly lead to a teammate’s made field goal. |
| **BLK** | Blocks | Defensive deflection of an opponent shot attempt. |
| **BPM** | Box plus/minus | Estimated net team point differential per 100 possessions attributable to the player (offense + defense), from a box-score regression. |
| **DBPM** | Defensive box plus/minus | Defensive component of box plus/minus (BPM): estimated defensive impact per 100 possessions. |
| **DWS** | Defensive win shares | Estimated share of team wins due to the player’s defense. |
| **eFG%** | Effective field-goal percentage | Field-goal accuracy with three-pointers weighted 1.5× vs two-pointers. |
| **ESPN box** | ESPN play-by-player box scores | Game-level counting stats in `mbb_df_player_box.csv` (our primary box source). |
| **FG%** | Field-goal percentage | Share of field-goal attempts that result in a made basket. |
| **FGA** | Field-goal attempts | Two-point and three-point shot attempts (excludes free throws). |
| **FGM** | Field goals made | Made baskets from the field (includes both two-pointers and three-pointers). |
| **FTA** | Free-throw attempts | Uncontested shots from the free-throw line after a foul. |
| **FTM** | Free throws made | Made free throws. |
| **FT** | Free throw | Uncontested shot worth one point from the foul line. |
| **H_sort** | Sorting index | Fraction of cross-player variance in z-scored performance explained by team assignment (realized homophily). |
| **LOO** | Leave-one-out | Teammate pool quality computed excluding the focal player. |
| **LG** | League generator | Grandchild assignment simulation used to calibrate homophily (ρ). |
| **MIN** | Minutes | Playing time (sum of game minutes in a season). |
| **OBPM** | Offensive box plus/minus | Offensive component of box plus/minus (BPM): estimated offensive impact per 100 possessions. |
| **OWS** | Offensive win shares | Estimated share of team wins due to the player’s offense. |
| **PER** | Player efficiency rating | Pace-adjusted per-minute production index (league average ≈ 15). |
| **PPM** | Points per minute | Total season points divided by total season minutes. |
| **PTS** | Points | Total points scored (field goals + free throws). |
| **ρ** | Homophily (rho) | Grandchild assignment parameter calibrated so simulated sorting index matches empirical H_sort. |
| **REB** | Rebounds | Offensive + defensive rebounds. |
| **SR** | Sports-Reference | Third-party site; advanced stats scraped into `bpm_player_season_matched.csv`. |
| **STL** | Steals | Defensive takeaways of the ball from the opponent. |
| **TOV** | Turnovers | Lost possessions (bad passes, steals against, violations, etc.). |
| **TS%** | True shooting percentage | Points scored per true shooting attempt (field goals + free throws on one scale). |
| **WS** | Win shares | Estimated number of team wins credited to the player (offense + defense). |

**ESPN column map** (box stats summed to player-season before rate stats):

| Acronym | ESPN `mbb_df_player_box` column |
|---------|----------------------------------|
| Points (PTS) | `points` |
| Minutes (MIN) | `minutes` |
| Field goals made (FGM) | `field_goals_made` |
| Field-goal attempts (FGA) | `field_goals_attempted` |
| Three-pointers made (3PM) | `three_point_field_goals_made` |
| Three-point attempts (3PA) | `three_point_field_goals_attempted` |
| Free throws made (FTM) | `free_throws_made` |
| Free-throw attempts (FTA) | `free_throws_attempted` |

**Note:** Field goals made (FGM) includes three-pointers made (3PM). Two-point makes = FGM − 3PM.

## Question

Does near-zero homophily (ρ) on **points per minute (PPM)** reflect weak men's college basketball assortativity, or a performance measure that washes out team sorting (congestion / minutes / role noise)? Compare empirical **sorting index (H_sort)** across candidate performance (`perf`) measures.

## Aperture (this run)

| Setting | Value |
|---------|-------|
| Seasons | 2009–2021 |
| Min minutes | 20 |
| Min team-season games | 10 (mg10) |
| Panel rows | all player-seasons (all-ps) |
| `perf` transform | within-season z-score |
| Pool quality | leave-one-out (LOO) teammate mean on same `perf` |

## Sorting index (H_sort)

**Sorting index (H_sort)** = fraction of cross-player variance in z-scored `perf` explained by team assignment (Grandchild realized sorting index). Higher → players on the same team look more alike on that metric.

PD21 calibrates league-generator (LG) **homophily (ρ)** so simulated sorting index (H_sort) matches the empirical target. Low sorting index (H_sort) on points per minute (PPM) → estimated ρ̂ ≈ 0.

## Results (pooled 2009–2021)

Perf keys match `perf_metric` codes; full metric names and formulas are in **Per-metric definitions** below.

| Rank | Key | H_sort (pooled) | vs PPM | N rows |
|------|-----|-----------------|--------|--------|
| 1 | `bpm` | 0.3366 | 5.23× | 45,156 |
| 2 | `ws` | 0.1627 | 2.53× | 52,906 |
| 3 | `tspct` | 0.1247 | 1.94× | 53,197 |
| 4 | `ts_pct_box` | 0.1243 | 1.93× | 54,568 |
| 5 | `efg_pct` | 0.1215 | 1.89× | 54,552 |
| 6 | `per` | 0.1113 | 1.73× | 49,086 |
| 7 | `fg_pct` | 0.0948 | 1.47× | 54,552 |
| 8 | `ppm` | 0.0644 | 1.00× | 54,582 |
| 9 | `minutes` | 0.0534 | 0.83× | 54,582 |

Per-season CSVs: `h_sort/Hsort_{metric}_mg10_min20_2009_2021_by_season.csv`

## Metric glossary — per-metric definitions

Acronyms are defined in **Acronym and stat reference** above. Formulas use standard notation; each section spells out the performance measure name once, then uses its key.

### Per-metric definitions

### `bpm` — Box plus/minus (BPM)

**What it measures:** Estimated net team point differential per 100 possessions attributable to the player (offense + defense), from a regression on box stats.

**Source:** Sports-Reference advanced merge (`BPM`, `OBPM`, `DBPM`).

**Formula:** $\mathrm{BPM} = \mathrm{OBPM} + \mathrm{DBPM}$

**Components:**

- **Offensive box plus/minus (OBPM)** — estimated offensive contribution per 100 possessions from box stats (scoring, shooting efficiency, playmaking, etc.).
- **Defensive box plus/minus (DBPM)** — estimated defensive contribution per 100 possessions.
- **Per 100 possessions** — box plus/minus (BPM) is *not* per minute; it is pace-normalized via Sports-Reference (SR) possession model.
- **Regression-based** — coefficients fit so that player box plus/minus (BPM) values sum (with minutes weights) to team efficiency vs league; not a simple rate stat.
- **Coverage** — Sports-Reference (SR) publishes box plus/minus (BPM) reliably ~2011+; 2009–10 largely missing in our matched file.

**In this pipeline:** SR season value merged by player match.

**Notes:** Highest sorting index (H_sort) in ladder; strong team clustering. Distinct from points per minute (PPM) (no minutes denominator in the same way; possession-based estimate).

### `ws` — Win shares (WS)

**What it measures:** Estimated number of team wins credited to the player’s offense and defense for the season.

**Source:** Sports-Reference advanced merge (`WS`; also `OWS`, `DWS` in raw scrape).

**Formula:** $\mathrm{WS} = \mathrm{OWS} + \mathrm{DWS}$

**Components:**

- **Offensive win shares (OWS)** — offensive contribution to wins (scoring, creation, efficiency).
- **Defensive win shares (DWS)** — defensive contribution to wins.
- **Team constraint** — player win shares (WS) on a team sum to roughly team wins (allocation problem across roster).
- **Not a rate** — season total; high-minute stars accumulate more win shares (WS) by construction.

**In this pipeline:** SR season value merged by player match.

**Notes:** Team-context composite; sorting index (H_sort) ~2.5× points per minute (PPM). Related to box plus/minus (BPM) family but in wins units not points/100.

### `tspct` — True shooting percentage (TS%), Sports-Reference

**What it measures:** Same construct as box TS%: scoring efficiency per true shooting attempt.

**Source:** Sports-Reference advanced table → `bpm_player_season_matched.csv` column `ts_pct_sr`; perf key `tspct`.

**Formula:** $\mathrm{TS\%} = \dfrac{\mathrm{PTS}}{2 \times (\mathrm{FGA} + 0.44 \times \mathrm{FTA})}$

**Components:**

- **Points (PTS), field-goal attempts (FGA), free-throw attempts (FTA)** — Sports-Reference (SR) season totals for the player on that team (from SR’s advanced page, not re-derived here).
- **0.44 × FTA** — same free-throw possession weight as standard true shooting percentage (TS%) (Dean Oliver / basketball-reference convention).
- Sports-Reference (SR) may round or compute from slightly different possession accounting than ESPN box totals; expect small drift vs `ts_pct_box`.

**In this pipeline:** Taken as published on SR; merged onto panel by name + team-season.

**Notes:** Strong sorting index (H_sort) vs points per minute (PPM); ~2009+ in raw scrape. Same *definition* as box true shooting percentage (TS%), different *source* totals.

### `ts_pct_box` — True shooting percentage (TS%), box-built

**What it measures:** Points scored per scoring attempt, where attempts combine field goals and free throws on one scale.

**Source:** ESPN box (`ts_pct_box` column in panel); same definition as Sports-Reference (SR) true shooting percentage (TS%) but built from ESPN season totals.

**Formula:** $\mathrm{TS\%} = \dfrac{\mathrm{PTS}}{2 \times (\mathrm{FGA} + 0.44 \times \mathrm{FTA})}$

**Components:**

- **Points (PTS)** — total points (two-pointers ×2 + three-pointers ×3 + free throws made (FTM) ×1).
- **Field-goal attempts (FGA)** — field goal attempts.
- **Free-throw attempts (FTA)** — free throw attempts.
- **Denominator** `2 × (FGA + 0.44 × FTA)` — “true shooting attempts”: each field-goal attempt counts as one possession ending in a shot; each free-throw attempt counts as 0.44 of a possession (standard Dean Oliver factor reflecting and-ones and shooting fouls).
- **Factor 2** — converts the attempt scale to points-per-shot equivalent (max per field-goal attempt is 2 points on a two-point make before threes).

**In this pipeline:** Sum PTS, FGA, FTA across games; compute TS%. Requires positive denominator.

**Notes:** Panel key `ts_pct_box`; distinct from Sports-Reference (SR) merge column `ts_pct_sr` (`tspct` perf key). Full 2009–21 box coverage.

### `efg_pct` — Effective field-goal percentage (eFG%)

**What it measures:** Field-goal accuracy with three-pointers weighted 1.5× (one three = one and a half two-pointers).

**Source:** ESPN box, season totals.

**Formula:** $\mathrm{eFG\%} = \dfrac{\mathrm{FGM} + 0.5 \times \mathrm{3PM}}{\mathrm{FGA}}$

**Components:**

- **Field goals made (FGM)** — all field goals made (two-pointers + three-pointers).
- **Three-pointers made (3PM)** — baskets from beyond the three-point arc only.
- **Field-goal attempts (FGA)** — all field goal attempts.
- The **0.5 × 3PM** term adds half a made field goal for each three beyond what field goals made (FGM) already counts (since FGM includes 3PM).

**In this pipeline:** Sum FGM, 3PM, FGA across games, then apply formula. Requires FGA > 0.

**Notes:** Standard “shooting efficiency” rate; still attempt-conditional like field-goal percentage (FG%).

### `per` — Player efficiency rating (PER)

**What it measures:** John Hollinger’s pace-adjusted summary of per-minute box production, league-normalized so 15 ≈ average.

**Source:** Sports-Reference advanced merge (`PER` column).

**Formula:** $\mathrm{PER} = f(\mathrm{MIN}, \mathrm{PTS}, \mathrm{FGM}, \mathrm{FGA}, \mathrm{FTM}, \mathrm{FTA}, \mathrm{REB}, \mathrm{AST}, \mathrm{STL}, \mathrm{BLK}, \mathrm{TOV}, \ldots)$

**Components:**

- **Inputs** — counting stats per minute (points, field goals, rebounds, assists, etc.), adjusted for team pace and league context.
- **Pace adjustment** — rewards production in fewer possessions (fast-paced teams don’t inflate raw counting stats).
- **League normalization** — scaled so league average ≈ 15 each season (not comparable raw across eras without z-scoring).
- **Not transparent in our pipeline** — we ingest Sports-Reference (SR) published player efficiency rating (PER), not re-implement Hollinger’s formula.

**In this pipeline:** SR season value merged by player match; ~2010+ non-null in matched file (2009 sparse).

**Notes:** Model-based composite; mixes scoring, playmaking, and rebounding. Not purely a shooting rate.

### `fg_pct` — Field-goal percentage (FG%)

**What it measures:** Share of field-goal attempts that score (two-pointers and three-pointers combined).

**Source:** ESPN box, season totals.

**Formula:** $\mathrm{FG\%} = \dfrac{\mathrm{FGM}}{\mathrm{FGA}}$

**Components:**

- **Field goals made (FGM)** — baskets from inside the arc or beyond the three-point line.
- **Field-goal attempts (FGA)** — shot attempts that count as field goals (includes two-pointers and three-pointers; excludes free throws).

**In this pipeline:** Sum FGM and FGA across games, then divide. Requires FGA > 0.

**Notes:** Conditional on getting attempts; does not penalize low usage. No minutes in denominator.

### `ppm` — Points per minute (PPM)

**What it measures:** Scoring output per unit of playing time.

**Source:** ESPN box (`mbb_df_player_box.csv`), aggregated to player-season in `panel_rebuild`.

**Formula:** $\mathrm{PPM} = \dfrac{\sum \mathrm{PTS}}{\sum \mathrm{MIN}}$

**Components:**

- **Points (PTS)** — total points scored (field goals + free throws); summed across all games in the season.
- **Minutes (MIN)** — playing time; summed across all games in the season.

**In this pipeline:** Sum PTS and MIN at game level, then divide. Rows with MIN = 0 get missing PPM.

**Notes:** Not a pure skill rate: high PPM can reflect role (usage), efficiency, or garbage-time minutes. Sensitive to roster congestion (fewer minutes on deep teams).

### `minutes` — Season minutes (MIN)

**What it measures:** Total playing time — opportunity, not efficiency.

**Source:** ESPN box, player-season sum.

**Formula:** $\mathrm{MIN} = \sum_{\mathrm{games}} \mathrm{minutes}$

**Components:**

- **minutes** — per-game playing time from ESPN box score (not stints or possessions).

**In this pipeline:** Sum across all games for `(athlete_id, season, team_id)`.

**Notes:** Lowest sorting index (H_sort) in the ladder: minutes are allocated by role/coach within team, so cross-team sorting is weak on this scale alone.

## What the sorting-index (H_sort) ladder tells you — and does not

- **Points per minute (PPM)** sorting index (H_sort) = 0.0644 — among the lowest.
- **Minutes (MIN)** lower still → opportunity alone barely clusters by team.
- **Field-goal percentage (FG%)**, **effective field-goal percentage (eFG%)**, and **true shooting percentage (TS%)** sit ~**1.5–2×** points per minute (PPM).
- **Box plus/minus (BPM)** sorting index (H_sort) ≈ **5.2×** points per minute (PPM) — strongest team sorting here (2011+ coverage only).
- **Higher sorting index (H_sort)** only means players on the same team look more alike on that axis → helps **homophily (ρ) / league-generator (LG) assign** identification.
- **It does not** automatically buy a better **advancement** story (draft rate vs leave-one-out pool quality).
- High-sorting metrics can make **ability (Â) vs pool quality (poolq_LOO)** *more* monotone: team sorting and teammate context move together → boring positive slope, less room for crowding / inverted-U.

## Promotion gate (COMPASS — what actually matters)

Do **not** promote a performance metric on sorting index (H_sort) alone.

Alternate `perf` is valuable only if it **breaks the naive monotone** readout on outcome vs leave-one-out pool quality (poolq_LOO) on the **reigning hero porch** (09–21 · last-ps · EW16 · min20 · mg10).

| Check | Pass if… |
|-------|----------|
| **P(Y=1) vs poolq_LOO** (EW16, last-ps) | Not strictly monotone ↑; visible peak or tail drop |
| **Linear probability model (LPM) β₂** on poolq_LOO | Negative / clearly concave (not ≈ 0) |
| **Â vs poolq_LOO** marginal | Optional — expect positive corr on most metrics; don't use alone |

**Points per minute (PPM) baseline (reigning, locked):** LPM β₂ ≈ +0.0017 → flat / not concave; shape tags “robust tail drop,” not a clean inverted-U. Sim can still show inverted-U at reigning λ, t — generative model has curvature; empirical points per minute (PPM) does not show it cleanly in the hero bin plot.

## Honest prior (before LOO-shape batch)

| Metric type | Sorting index (H_sort) | Likely Â vs poolq_LOO / draft vs poolq_LOO |
|-------------|------------------------|---------------------------------------------|
| Points per minute (PPM), minutes | Low | Monotone / flat (opportunity + congestion) |
| True shooting % (TS%), field-goal % (FG%), effective FG% (eFG%) | ~2× PPM | Maybe slightly less monotone; still skeptical |
| Box plus/minus (BPM), player efficiency rating (PER), win shares (WS) | High | More team-aligned → often *more* monotone, not less |

Box plus/minus (BPM) helping homophily (ρ) while **worsening** hero geometry is a real possibility. A metric fork (BPM for assign, PPM for advancement) is a heavy lift unless one metric clearly wins the LOO-shape test.

## Campaign status (this thread)

- **Homophily (ρ) ≈ 0 on points per minute (PPM)** — keep locked for reigning men's college basketball.
- **γ, λ, t + Pass B** — proceed; that's where fitting still has bite.
- **This ladder** — necessary context for assign (ρ); **not sufficient** to switch the hero metric.

## LOO-shape batch (built)

Ran `python3 sports/scripts/perf_metric_loo_shape_batch.py` — see [`loo_shape/LOO_SHAPE_REPORT.md`](loo_shape/LOO_SHAPE_REPORT.md).

**Headline:** points per minute (PPM) **marginal** (flat LPM β₂); box plus/minus (BPM) / player efficiency rating (PER) / win shares (WS) **fail** (convex β₂); no hero-metric switch.

