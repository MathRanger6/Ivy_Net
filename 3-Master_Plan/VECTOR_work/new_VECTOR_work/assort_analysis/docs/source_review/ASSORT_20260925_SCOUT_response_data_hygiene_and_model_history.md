# SCOUT response — basketball data hygiene and model history

**Prepared:** September 25, 2026  
**For:** VECTOR / Charles (assortativity population freeze)  
**In reply to:** [`ASSORT_20260925_questions_for_SCOUT.md`](ASSORT_20260925_questions_for_SCOUT.md)  
**Status:** Read-only historical reconciliation. No code execution, panel rebuild, or figure regeneration in this reply.

---

## How to read this document

Each claim is tagged by evidence type:

| Tag | Meaning |
|-----|---------|
| **[Direct repo]** | Verifiable in source code, config, or a named file in the repository today |
| **[Saved result]** | Numeric or graphical output preserved in a named artifact (not re-run here) |
| **[Meeting record]** | Transcript, advisor call notes, or archived SCOUT↔COMPASS correspondence |
| **[Interpretation]** | Plausible mechanism or narrative synthesis — not independently audited |
| **[Gap]** | Missing primary record; proposed check listed where helpful |

Repository paths below are relative to the workspace root unless noted.

---

## Charles's recollections — what they identify, what needs qualification

| Recollection | Verdict | Notes |
|--------------|---------|-------|
| Different analyses used **drop sub-20** vs **zero-PPM** for low-minute players | **Correct** | Production hero / LG path = drop; PD21 `--ppm-zero-below-minutes 20` = contrast only. [Direct repo] [`sports/scripts/pd21_rho_hsort_calibrate.py`](../../../../../../sports/scripts/pd21_rho_hsort_calibrate.py); [Meeting record] [`transcripts/PD23_notes.md`](../../../../../../transcripts/PD23_notes.md) |
| Before/after curve pair differed **only** in the minimum-games rule | **Mostly correct** for the August 19 Pass A sensitivity pair | Intentional spec held min20, dash filter, 2011–2021, 16 quantile bins, winsor 0.01–0.99, `poolq_loo`, within-season PPM z, ALLT fixed; **only** `min_team_season_games` changed (0 vs 10). **But** z-scores, LOO, and quantile bin membership **recomputed** on the new population — not “delete rows from fixed bins.” [Saved result] §2 |
| Fragmentary weak teams received **exaggerated** measured team quality \(\hat{T}_j\) | **Directionally aligned; mechanism partly documented for LOO, not fully audited for \(\hat{T}_j\)** | Charles’s concern matches the scientific motivation for box QC. Saved CPR work documents **elite LOO ventile contamination**, not a team-by-team \(\hat{T}_j\) audit. Mechanism for upward \(\hat{T}_j\) bias is **[Interpretation]** below (§1). |
| Inverted-U **survived** cleaning | **Qualified — depends on figure and meaning of “survived”** | Middle rise + peak largely persist; **elite right-tail dip** under July (mg=0) does **not** survive POST-QC on the canonical LOO axis. [Saved result] §2, §7 |
| **PPM was a provided column in ESPN / box data** | **Incorrect — understandable confusion** | Game-level box has **`points`** and **`minutes` only**; no `ppm`. Exported panel **shows** `ppm`, but current rebuild **always derives** it as season sum(points) ÷ sum(minutes) **after** box QC, **before** min-minutes drop. Hero analysis **copies** `ppm` → `perf`; it does not re-divide. See **§3.6**. [Direct repo] `panel_rebuild.build_from_box`; [Meeting record] Charles Sep 25 — **must recalculate after filtering** for new experiment |

---

## 1. From one-game discovery to final coverage threshold

### 1.1 Recorded policy sequence

| Date / stage | Threshold (config value) | Plain language | Primary source |
|--------------|-------------------------|----------------|----------------|
| Pre–Aug 17, 2026 | `min_team_season_games = 0` (implicit) | No team-season game-count filter; July hero panel included exhibition / one-game cameos | [Saved result] `pass_a` July replay; [Direct repo] `pass_a_hero_sensitivity_plots.py` |
| Aug 17, 2026 (initial rollout) | **`5`** → keep **`> 5`** games → **≥ 6 captured games** | Charles-approved PD22 rollout after BYU dash-row investigation | [Meeting record] [`3-Master_Plan/20260817_1650_SCOUT_to_COMPASS_box_qc_rollout_and_regen.md`](../../../../../../3-Master_Plan/20260817_1650_SCOUT_to_COMPASS_box_qc_rollout_and_regen.md) §1, §3 |
| Aug 17, 2026 (evening) → locked default | **`10`** → keep **`> 10`** → **≥ 11 captured games** | Documented as same-day tightening in policy mirror | [Direct repo] [`3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md) §3b; [`sports/sports_pipeline/config.py`](../../../../../../sports/sports_pipeline/config.py) `min_team_season_games = 10` |

**Naming convention (critical):** `mg10` / `min_team_season_games=10` means **drop team-seasons with ≤10 distinct `game_id` values** — i.e. **retain ≥11 games**, not ≥10. [Direct repo] `panel_rebuild._apply_box_qc`: `keep_ts = ts_games[ts_games > min_g]`.

### 1.2 Why the threshold moved from six to eleven captured games

**What is documented:**

1. **Initial mg5 (≥6)** removed the bulk of one-game cameos (1,883 team-seasons with exactly one game in box motivated the rule). [Meeting record] rollout memo §2; [Saved result] archived game-count output cited in `.specstory/history/2026-05-24_12-52-09-0400-scout.md` (H13 in VECTOR history review).

2. **Same-day raise to mg10 (≥11)** is recorded in `BOX_QC_panel_build_policy.md` §3b with impact table showing **zero additional drafted hero rows lost** vs mg5. [Saved result] policy §4; archived sensitivity output in `.specstory/history/2026-06-11_08-19-11-0400-compass.md` (~lines 215504–215526):
   - mg5 → mg10: **23** additional team-seasons dropped (the 6–10 game band)
   - Drafted hero player-seasons lost: **0**
   - Unique ever-drafted athletes on hero panel: **520** under both thresholds

3. **No standalone Charles memo** in repo stating “we chose eleven because …” beyond the rollout + same-day policy update. **[Gap]** Primary deliberation may live only in Aug 17 chat (SpecStory) or oral approval.

**[Interpretation] — likely reasoning (consistent with saved counts, not a quoted decision):**

- Teams with **6–10 captured games** still represent **partial seasons**, not D-I calendar completeness.
- Tightening to ≥11 removed **23** marginal team-seasons **without** draft-outcome harm — a low-cost robustness step after seeing mg5 leave residual fragmentary environments (e.g. Jarvis Christian at 3 games still in panel under any threshold ≤2). [Direct repo] policy §6.

**Alternatives considered (documented):**

| Alternative | Status | Source |
|-------------|--------|--------|
| Per-game roster cap (>25 listed athletes) | **Not implemented** | `BOX_QC_panel_build_policy.md` §6 |
| Exhibition / season-type exclusion | **Not implemented** (needs schedule metadata) | same |
| Rewrite frozen `mbb_df_player_box.csv` | **Rejected** — filter at panel build only | rollout memo §1, §4 |
| `min_minutes` alone fixes fragmentary teams | **Rejected** after PD22 — min20 cannot fix one-game **team** coverage | VECTOR history review §2; policy §1 |

### 1.3 Captured games vs ESPN vs games actually played

- **Rule counts:** distinct `game_id` per `(team_id, season)` in **`mbb_df_player_box.csv`** after dash-name filter. [Direct repo] `panel_rebuild._apply_box_qc`
- **Does not establish:** full season schedule completeness or official division membership. [Meeting record] VECTOR questions doc; Charles spot-check (40 low-coverage team-seasons vs ESPN) in SpecStory H13 — **39/40** exact game-count match, **1/40** one captured vs three in ESPN response. **[Saved result]** excerpt only; not reproduced here.

### 1.4 Charles's \(\hat{T}_j\) concern — mechanism

**Historical definition of \(\hat{T}_j\) in affected plots:**

| Context | Definition | Code / artifact |
|---------|------------|-----------------|
| Basic data plots (BDP) | Mean within-season **PPM z** (`perf`) over retained players on `(team_id, season)` | [Direct repo] `sports/scripts/bdp_ai_tj_distributions.py` — `T_j_hat = groupby(...).perf.mean()` |
| Interval overlap / PD17 | Same: `T_j_hat = mean(perf)` on roster after hero filters | [Direct repo] `empirical_team_interval_overlap.py` `_team_intervals` |
| Generative sim (538D) | Target mean **`T_j`** drawn for soft assignment — separate from empirical panel | [Meeting record] `SCOUT_report_to_COMPASS.md` §2 |

**Documented result (LOO axis — hero curve, not \(\hat{T}_j\) directly):** Under mg=0, **65.80%** of bin-16 `poolq_loo` rows were CPRs (cut player-rows from dropped team-seasons). Those rows draft at ~0%; they **mechanically depressed** elite-bin draft rates and created a **fake right-tail dip**. [Saved result] [`3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md`](../../../../../../3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md) B5–B6.

**[Interpretation] — upward exaggeration of \(\hat{T}_j\) for fragmentary weak teams (Charles's specific concern):**

1. **Selection into the extract:** Low-major / NAIA teams often appear **only** because they played one visible game vs a well-covered D-I opponent. The observed sample is **not** a random draw from that school's season.

2. **Survivorship through min20 on a one-game team-season:** Only players with **≥20 total season minutes** in the **captured** games remain. On a one-game team-season, that is typically **1–3 rotation players** from a single exposure — not a full roster average.

3. **Small-\(n\) team mean:** \(\hat{T}_j = \frac{1}{n}\sum A_i\) on \(n \in \{1,2,3\}\) has **high variance** and **no dilution** from bench players who would pull a true season mean down.

4. **Within-season z-scoring:** `perf` is z-scored across **all retained player-seasons in that season** after filters (`standardize_perf_zscore_by_season`). A weak-school player who put up acceptable minutes in one game is measured against the **full-season** cross-section — but the **team mean** still aggregates **only** those few surviving rows, not the unobserved majority of the season.

5. **Direction:** For truly weak programs, true season quality is far below D-I norms; the above biases \(\hat{T}_j\) **upward relative to a full-season counterfactual** (less negative / occasionally positive vs where a 30-game roster mean would sit). **[Gap]:** No saved CSV ranks fragmentary teams by \(\hat{T}_j\) vs schedule strength; would require audit joining game-count to `PD22_interval_overlap_*.csv`.

**Distinction for VECTOR:** Hero x-axis is **`poolq_loo` (LOO teammate quality)**, not \(\hat{T}_j\). Cleaning changes both, but the **August CPR tables** directly document LOO ventile contamination; \(\hat{T}_j\) inflation is **scientifically consistent** with Charles's memory but **less numerically audited** in saved artifacts.

---

## 2. Exact figures for the before/after curve change

### 2.1 Paired Pass A sensitivity artifacts (best match to Charles's memory)

| Role | Artifact | Spec summary |
|------|----------|--------------|
| **Pre-cleaning (July replay)** | `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/sensitivity/PASS_A_sensitivity_loo_mg0_2011_2021_b16q_w0199_july_replay_mg0.png` **[Gap: PNG not in git]** | mg=0, min20, 2011–2021, 16 **quantile**, winsor 0.01–0.99, `poolq_loo`, PPM z within season, dash filter ON, ALLT, **all player-season rows** |
| **Post-cleaning (POST-QC)** | `3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/sensitivity/PASS_A_sensitivity_loo_mg10_2011_2021_b16q_w0199.png` **[Gap: PNG not in git]** | Same except **mg=10** |
| **Index / JSON** | `PASS_A_hero_sensitivity_index.csv`, `PASS_A_hero_sensitivity_post_qc.json` | [Saved result] |
| **Gallery README** | `pass_a/sensitivity/README.txt` (generated 2026-08-19) | Lists both PNGs with headline stats |

**Generator:** [Direct repo] `sports/scripts/pass_a_hero_sensitivity_plots.py` — `run_spec()` with `subsample="july_replay_mg0"` when `mg=0`.

### 2.2 Saved bin statistics (paired comparison)

| Metric | Pre (mg=0, July replay) | Post (mg=10, POST-QC) | Source |
|--------|-------------------------|------------------------|--------|
| n (player-season rows) | **62,180** | **46,306** | [Saved result] JSON |
| Drafts | 1,134 | 1,133 | same |
| Peak bin (1-indexed) / rate | **12** @ **2.62%** | **15** @ **3.25%** | same |
| Last bin rate | **1.16%** | **3.21%** | same |
| Tail Δ (last − peak) | **−1.47 pp** | **−0.03 pp** | same |
| LPM β₂ on `poolq_sq` | **−0.0247** (concave) | **+0.0064** (not concave) | same |

**Charles's recollection test:** For this pair, **only the team coverage rule differed by design**. **Consequential downstream steps** (same code path, new population): within-season PPM z-score, LOO teammate means, winsor clip, **quantile ventile reassignment**.

### 2.3 August 19 CPR / elite-bin tables (companion to the curve story)

**Source:** [Saved result] `SCOUT_and_COMPASS_Q_and_A.md` B1–B6, B5a — SCOUT verified Aug 19, 2026.

| Statement | Value | Notes |
|-----------|-------|-------|
| CPR player-season rows removed | **45,332** | 2011–2021, mg=10 definition |
| Distinct CPR athletes | **30,396** | |
| Distinct CPR team-seasons | **2,715** | 1:1 with eliminated LOO environments |
| Ever-drafted among CPR athletes | **1** (Derrick White, Colorado Springs 2014 cameo) | |
| Bin 16 CPR share (mg=0 tagging panel) | **2,557 / 3,886 = 65.80%** | B6 table |
| Bins 13–16 combined CPR share | **4,808 / 15,545 = 30.93%** | B5 |
| POST-QC bins 12–16 draft rates | 2.63% → 2.73% → 2.90% → 3.25% → **3.21%** | B5a; flat / slightly rising tail |

**65.80% vs 66.8%:** Table supports **65.80%**. COMPASS prose in B6 note says “**66.8%**” — **typo / rounding slip**; use **65.80%** as canonical. [Saved result] numerator/denominator in B6.

### 2.4 Other hero figures (not the mg0/mg10 pair)

The **reigning hero** (slide 12 lock) uses a **different** spec: 2009–2021, **last-PS**, **equal-width 16**, mg10, min20 — β₂ ≈ **+0.00172**, “flat elite tail.” [Saved result] [`3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md); provenance [`pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/HERO_q16_allt_min20_mg10_9_21_last_ps_provenance.json).

Do **not** conflate the July replay pair (all-PS, quantile) with the reigning hero (last-PS, EW16).

---

## 3. Individual minutes policy (drop sub-20 vs zero-PPM)

### 3.1 Unit of measurement

**Always total season minutes** in current construction — sum of box `minutes` aggregated to `(athlete_id, season, team_id)` before filtering. **[Gap]:** No evidence in repo of a historical **per-game** minutes threshold in production pipeline; PD23 Otter garble may have confused “per game” orally. [Meeting record] `PD23_notes.md`.

### 3.2 Two policies and where they apply

| Policy | Rule | Role | Where used |
|--------|------|------|------------|
| **A — Drop sub-20 (production)** | Remove player-season rows with **`minutes < 20`** before z-score / LOO | **Primary estimand** for hero, BDP, LG ASSIGN input | [Direct repo] `panel_rebuild.build_from_box` (aggregation then `min_minutes`); `panel_build.filter_panel`; `_hero_pipeline_config()` in overlap scripts |
| **B — Zero-PPM contrast** | Keep all rows; set **`ppm = 0`** where **`minutes < 20`**; then z-score / LOO | **Sensitivity / wrong estimand** for ρ,H_sort slides | [Direct repo] `pd21_rho_hsort_calibrate.py` `--ppm-zero-below-minutes 20`; [Meeting record] PD23 lock |

**Low-minute players under B:** Enter **both** focal sample and teammate pools (with zeroed raw PPM → typically negative z after standardization). Under A: **excluded entirely** — they do not affect LOO for anyone.

### 3.3 Rationale (documented)

| Concern | Drop sub-20 | Zero-PPM |
|---------|-------------|----------|
| Unstable PPM ratios (small denominator) | Removes unstable rows | Keeps rows but kills rate signal |
| LOO / ventile interpretation | “Rotation-level peer environment” | Inflates roster size; changes within-team dispersion (PD23 Alex std-dev plot question) |
| Hero curve shape | **20** preferred for main text; 10/0 in robustness | Illustrates **different estimand** — ρ* ≠ 0 on contrast panel |

[Meeting record] [`sports/documents/Pertinent_Thoughts_Scout.md`](../../../../../../sports/documents/Pertinent_Thoughts_Scout.md) §`min_minutes` (Jul–Aug 2026); [Meeting record] PD23 notes §“Locked production policy.”

### 3.4 PD23 transcript (28:47–29:26) — drop vs zero

- **Otter transcript:** closing exchange garbles between “you're out” and “it's zero.” [Meeting record] `20260918_Paper_directions_23_otter_ai_transcript.docx` (internal date Aug 18).
- **Derived notes:** interpret as garble; **drop sub-20** remains production. [Meeting record] `PD23_notes.md`
- **Contemporaneous lock:** Alex operational lock at call end **mixed** drop, ppm-zero, and 2013+ window — notes **explicitly separate** these. [Meeting record] PD23 “Locked / agreed actions” table.
- **Execution record:** Aug 18 re-cal `pd21_rho_hsort_calibrate.py --ppm-zero-below-minutes 20 --fresh` for slides 15–16 only. [Meeting record] PD23 notes §ρ re-cal.

**Verdict:** Production = **drop** is supported by code + PD23 notes + post-call runs. Transcript alone **does not** independently prove the notes' garble interpretation — but **no saved artifact** treats ppm-zero as production hero policy.

### 3.5 Status over time

| Period | Minutes policy |
|--------|----------------|
| Apr 2026 early exports | min0 common (`use_prebuilt_panel` era) |
| Jul 2026 hero exploration | min20 locked for main spec with `use_prebuilt_panel_csv=False` |
| Aug 2026 PD22 / PD23 | min20 **production**; ppm-zero **contrast only** |

### 3.6 Points per minute (PPM) — not a source column; must be derived after filters

**VECTOR code inspection (Sep 25, 2026)** flagged paths that **recompute** or **mutate** PPM instead of reading a vendor field. SCOUT reconciliation below.

#### 3.6.1 What the data sources actually provide

| Layer | `ppm` present? | What is present | Evidence |
|-------|----------------|-----------------|----------|
| **Game-level ESPN box** (`mbb_df_player_box.csv`) | **No** | `points`, `minutes`, `game_id`, IDs, names | [Direct repo] `panel_rebuild.build_from_box` `usecols` — only `points` and `minutes` for rate construction; legacy `_530_extract/cell_5.py` same |
| **Sports-Reference matched file** | **No PPM** | BPM, OBPM, DBPM, PER, WS, … | [Direct repo] `merge_sr_matched_into_panel`; [Meeting record] [`Pertinent_Thoughts_Scout.md`](../../../../../../sports/documents/Pertinent_Thoughts_Scout.md) — SR `MP` is separate merge, not box PPM |
| **Exported player-season panel** (`player_season_panel_530.csv`) | **Yes (stored)** | `minutes`, `points`, **`ppm`**, … | Looks “provided” in CSV exports — **misleading label**; value was **written at panel-build time**, not ingested from ESPN |

**Charles's surprise (Sep 25):** PPM is such a standard rate that it **feels** like a feed column. In this repository it **never was** at game level. The panel `ppm` column is **project-defined**.

#### 3.6.2 Canonical definition (hero / LG / BDP lock)

Season player-season PPM is **always**:

$$
\text{ppm}_{i,j,t} = \frac{\sum_{g \in \mathcal{G}_{i,j,t}} \text{points}_{i,g}}{\sum_{g \in \mathcal{G}_{i,j,t}} \text{minutes}_{i,g}}
$$

where $\mathcal{G}_{i,j,t}$ is the set of **retained box game rows** for athlete $i$ on team $j$ in season $t$ **after** configured box QC (dash filter, minimum captured games, season window).

**Not** the mean of game-level PPM rates. **Not** a separate ESPN field.

[Direct repo] `panel_rebuild.py` line 186:

```python
agg["ppm"] = np.where(agg["minutes"] > 0, agg["points"] / agg["minutes"], np.nan)
```

[Direct repo] `perf_metric.py` — `"ppm"` maps to column `ppm` with gloss “points / minutes, ESPN box” (meaning **box counting stats**, not a vendor PPM column).

#### 3.6.3 Filter order — why “recalculate after filtering” matters

**Correct order in `build_from_box` (Aug 2026 production path):**

| Step | Action | Effect on PPM |
|------|--------|---------------|
| 1 | Read game-level box | — |
| 2 | Season window | Drops out-of-window **games** |
| 3 | **Box QC** (dash placeholders; drop team-seasons with ≤ `min_team_season_games` distinct `game_id`) | Drops **game rows** for fragmentary team-seasons |
| 4 | **Aggregate** → `minutes`, `points` sums | Totals reflect **post-QC** games only |
| 5 | **`ppm = points / minutes`** | **Single choke-point derivation** |
| 6 | **`min_minutes`** (production: 20) | Drops player-season **rows**; does **not** change surviving rows' `ppm` (already from filtered totals) |
| 7 | Draft flag, SR merge | No PPM change |
| 8 | `assign_perf_from_metric("ppm")` | **Copies** `ppm` → `perf` — **no second division** |
| 9 | Within-season z-score, LOO, … | Transforms `perf`; does not re-derive raw PPM |

**Charles's requirement (Sep 25, authoritative for assortativity freeze):** Because PPM is **not** upstream-provided, any new experiment **must** derive PPM **after** all game-level and player-level filters that define the eligible population — **not** trust a stale exported `ppm` from a different QC snapshot.

**SCOUT verdict:** The **`use_prebuilt_panel_csv=False` + `build_from_box`** path **already satisfies** this when filters match the experiment spec. The **`use_prebuilt_panel_csv=True`** bypass **does not** — it reads whatever `ppm` was frozen at export time (often pre–mg10 or min0 era). [Direct repo] `config.py`; policy §5.

#### 3.6.4 What looks like “recalculation” but is something else

| Pattern | What it is | Production hero? |
|---------|------------|------------------|
| **`assign_perf_from_metric("ppm")`** | Copy `ppm` → `perf` | **Yes** — not re-division |
| **Within-season z-score on `perf`** | Standardization after copy | **Yes** |
| **`--ppm-zero-below-minutes 20`** | **Overwrites** `ppm` with 0 for `minutes < 20` before z-score | **No** — PD21 contrast only [Direct repo] `pd21_rho_hsort_calibrate.py` |
| **`assign_career_cum_box_ppm`** | `cum_points / cum_minutes` across seasons → `perf_cum` | **No** — separate cum-PPM probe |
| **PD22 histogram scripts** | `pd.to_numeric(panel["ppm"])` — read stored column | Diagnostic only |
| **Re-dividing `points/minutes` on panel rows** | Would match stored `ppm` **if** `points`/`minutes` are post-filter aggregates | **Not** used on hero path today; only one division at step 5 |

#### 3.6.5 Implications for VECTOR 2015 population freeze

| Option | PPM handling | SCOUT recommendation |
|--------|--------------|----------------------|
| **A — Rebuild from box** with frozen filters (mg10, min20, dash, 2015 window) | PPM derived at step 5 on **filtered** game set | **Preferred** — full provenance |
| **B — Use saved export `ppm`** | No recalculation | **Risky** unless export metadata proves **identical** filter stack (Aug 11 Grandchild export = **pre–mg10**) |
| **C — Recompute `points/minutes` from export totals** | OK **only if** export `points`/`minutes` already reflect same QC as experiment | Acceptable shortcut if totals verified; still not game-level re-aggregation |

**For assortativity experiment (Charles, Sep 25):** Treat **Option A** as the default authorized construction. Standardize **after** team coverage + min20 eligibility on the **derived** PPM values (already documented in experiment choices).

#### 3.6.6 One-line summary for VECTOR docs

> **Season PPM is not an ESPN field. It is computed once as aggregated season points divided by aggregated season minutes after box QC and before the min-minutes row drop; downstream hero code copies that column into `perf` and does not re-divide.**

---

## 4. Two-player analytical rosters (Grandchild 2015)

### 4.1 Saved counts — not directly comparable without reading filters

| Artifact | Teams (2015) | Rows (2015) | min roster | Filters (from meta / JSON) |
|----------|-------------|-------------|------------|----------------------------|
| `grandchild_assign/GRANDCHILD_ncaa_roster_size_distribution_2011_2021_meta.json` | **635** | **6,030** | **2** | PPM z, **min20**; **`_prepare_panel` without explicit mg10 in Aug 11 meta** — predates Aug 17 box QC lock |
| `pd22_minutes/PD22_espn_coverage_by_season_2013_2021.json` (2015 row) | **351** after QC | **4,270** min20 | min **9** at min20 after mg10 | mg10 + dash + min20 |

The 635 / 6,030 file is **pre–box-QC** hero-style panel (62,180 player-seasons total 2011–2021 in meta — matches July replay n). The 351 / 4,270 file is **post–box-QC** PD22 diagnostic.

### 4.2 Six two-player team-seasons (2015)

From [Saved result] `GRANDCHILD_ncaa_roster_size_by_team_season_2011_2021.csv`:

| team_id | season | roster_n (retained) |
|---------|--------|---------------------|
| 2069 | 2015 | 2 |
| 2800 | 2015 | 2 |
| 2827 | 2015 | 2 |
| 3086 | 2015 | 2 |
| 3166 | 2015 | 2 |
| 108818 | 2015 | 2 |

**[Gap]:** No team-traced audit in repo listing **captured game counts**, player names, or exclusion reasons for these six IDs. They **do not appear** in the post-QC 2015 PD22 row (351 teams, min roster 9).

**[Interpretation]:** Consistent with **fragmentary coverage + min20** route (§VECTOR history §5 illustrative path): one or few games captured, only two players reach 20 season minutes. **Not verified** as one-game teams without box-level audit.

**Proposed check (not run):** Join six `(team_id, 2015)` to raw box `game_id` counts and minutes table — **[Gap]**.

---

## 5. Population supplied to each transformation and analysis

### 5.1 Canonical order (current `build_from_box` path)

[Direct repo] `panel_rebuild.build_from_box` + `panel_build.apply_perf_metric_for_analysis`:

1. Read game-level `mbb_df_player_box.csv`
2. Season window filter (`panel_season_min` / `max`)
3. **Box QC:** dash placeholders; **`games_n > min_team_season_games`**
4. Aggregate to player-season (`minutes`, `points`, …) then **`ppm = points / minutes`** on **post-QC** totals — see **§3.6** (not an ESPN column; must not use stale export without matching filters)
5. **`min_minutes`** on aggregated minutes (row drop only; surviving `ppm` unchanged)
6. **`Y_draft`** from draft lookup (0 if athlete_id ∉ lookup)
7. Optional SR advanced merge
8. **`apply_perf_metric_for_analysis`:** assign `perf` from metric → **within-season z-score** (hero path) → **`poolq_loo`** (+ optional winsor) on **full panel before row restriction**
9. **`filter_panel`:** dropna(`poolq_loo`, `Y_draft`); optional second `min_minutes`; optional draftee team restriction
10. **Focal row rule (hero):** **`restrict_to_last_season_rows`** for last-PS plots only

**Ability standardization reference:** **Within-season** over all player-season rows that survive steps 1–7 **before** LOO (and before last-PS restriction). [Direct repo] `apply_perf_metric_for_analysis(..., zscore_perf_within_season=True)`.

**LOO construction:** Computed on **full eligible roster** per `(team_id, season)` after steps 1–8 — **before** last-PS subsetting. [Direct repo] `recompute_teammate_loo_pool_quality`; [Meeting record] reigning hero README “Population split.”

**Transfers / multi-team seasons:** Panel grain is `(athlete_id, season, team_id)`; multiple rows per athlete-season possible. Last-PS rule picks one focal row per athlete for hero. [Direct repo] `y_draft_mode` / `restrict_to_last_season_rows`.

**Prebuilt panel bypass:** `use_prebuilt_panel_csv=True` skips steps 1–7 QC — **Aug 17+ runs intended `False` for hero.** [Direct repo] `config.py`; policy §5.

### 5.2 Map: population / transform / axis / selection → outputs

| Output family | Seasons | mg | min | Panel rows | Binning | Axis | Y draft | Key artifacts |
|---------------|---------|----|----|------------|---------|------|---------|---------------|
| July replay sensitivity | 11–21 | **0** | 20 | all-PS | Q16, w0199 | `poolq_loo` | ever (in panel) | `PASS_A_sensitivity_loo_mg0_*_july_replay_mg0.*` |
| POST-QC sensitivity (canonical pair) | 11–21 | **10** | 20 | all-PS | Q16, w0199 | `poolq_loo` | ever | `PASS_A_sensitivity_loo_mg10_2011_2021_b16q_w0199.*` |
| Reigning hero | **09–21** | 10 | 20 | **last-PS** | **EW16**, w0199 | `poolq_loo` | ever | `HERO_q16_allt_min20_mg10_9_21_last_ps.*` |
| Grandchild 2015 N≈6030 | 2015 | **none** (Aug 11) | 20 | all-PS | n/a (assign) | PPM z | n/a | `541_grandchild_*`, roster meta |
| LG ρ calibration (hero) | 11–21 | 10 | **20 drop** | all-PS | n/a | PPM z | n/a | `pd21_rho/PD21_rho_hsort_calibrate_*` (no ppm0 tag) |
| LG ρ calibration (contrast) | 11–21 | 10 | **0 + ppm0<20** | all-PS | n/a | PPM z | n/a | `*ppm0lt20*` outputs |
| BDP Â \| T̂_j | spec e.g. mg10 min20 11_21 | 10 | 20 | **last-PS** | n/a | `perf` → T̂_j | n/a | `basic_data_plots/BDP_Ai_Tj_*` |
| Interval overlap | 09–21 | 10 | 20 | **all-PS** | n/a | perf intervals | n/a | `reigning_hero` BDP list #1 |
| CPR tagging audit | 11–21 | 0 panel / tag CPRs | 20 | all-PS | Q16 | `poolq_loo` | ever | SCOUT Q&A B5–B6 |

---

## 6. Draft indicator and excluded athletes

### 6.1 Construction

[Direct repo] `panel_rebuild.build_from_box`: `Y_draft = 1` iff `athlete_id` ∈ `athlete_id_draft_lookup.csv`; else **0**. Unmatched = **undrafted for analysis**, not dropped.

**Coverage caveat:** Mis-linked or missing draft matches → **false negatives** (undrafted label). Alias / match QA is separate from box QC. [Meeting record] rollout memo §3.3 — box QC did not implicate draft matching.

### 6.2 Derrick White / CPR drafted count

[Saved result] SCOUT Q&A B3: **1** ever-drafted athlete among CPR rows — **Derrick White** (`athlete_id` 67845), Colorado Springs **2014**, 31 min on 1-game team-season; full Colorado 2017 season remains outside CPR.

**Denominator for “1 among CPR”:** Distinct **athletes** appearing on CPR **player-season** rows (30,396), **before** interpreting as “final-season focal rows.”

### 6.3 Rate vs count limits (recognized at the time)

- Removing **45k+ undrafted** player-seasons while losing **one** drafted row **still changes draft rates** in upper ventiles (denominator composition). [Saved result] B5–B6; VECTOR history §4.
- Campaign explicitly warned: **do not** treat restoring elite dip as success criterion. [Meeting record] `20260821_SCOUT_CCT_campaign_review.md` (H12).

---

## 7. Reconciling “inverted U survived” with flat POST-QC tail

| Statement | Referent | Verdict |
|-----------|----------|---------|
| PD23 opening: inverted-U **survived** cleaning | **Qualitative middle rise + peak**; panel defensible for Alex | [Meeting record] PD23 notes headline |
| Aug 19 POST-QC bins 12–16 | **No elite dip** — flat 2.63%→3.21% | [Saved result] B5a |
| Reigning hero β₂ ≈ +0.00172 | **Global** quadratic not concave; local “tail drop” label ≠ concavity | [Saved result] reigning hero README; LPM file |
| July replay mg=0 | **Concave** β₂; **−1.47 pp** tail drop — **artifact** driven by bin-16 CPRs | [Saved result] §2.2 |

**“Survived” ≠ “unchanged right-tail dip.”** Middle rise is robust; **elite-bin downturn under mg=0 is not** on LOO + POST-QC.

**PD23 filename vs date:** File `transcripts/20260918_Paper_directions_23_otter_ai_transcript.docx`; internal header **August 18, 2026**. Use internal date; disclose filename mismatch. [Meeting record] PD23 notes header.

---

## 8. Modeling choices — intellectual history pointers

For VECTOR mechanism context (not current experiment spec):

| Topic | Record | Limitation |
|-------|--------|------------|
| **Ordered assign vs LG (Grandchild)** | `541_grandchild_homophily_assign.py`; `541_grandchild_homophily_assign_README.md`; Aug 2025–2026 sweep meta | Grandchild = endogenous centroids + stub capacity; differs from soft τ assignment |
| **Fixed C=15 vs observed capacities** | Grandchild README; `load_empirical_roster_caps_season` | Fixed 15 vs empirical multiset is explicit fork |
| **`team_mean` / T̂_j vs `poolq_loo`** | [Meeting record] `SCOUT_report_to_COMPASS.md` §2 — inverted-U on team_mean in sim, mostly decreasing on LOO with same score | Axis ≠ relabel |
| **Assignment noise vs score noise vs SELECT** | `538D` CELL 10 manual; PD20 Gibbs gate | Distinct layers; deterministic top-K today is new design |
| **Congestion scaling / negative scores / temperature** | `tier1_sim_config.py`, `538_Cell10_Generative_Manual.md` | Historical knobs; not all map to Aug 2026 hero lock |
| **Pass A / B / C** | `pass_a/` artifacts; CCT campaign review | Pass A = empirical hero + sensitivity; Pass B/C conditional ability campaign |
| **Artificial minutes allocation rejected** | [Meeting record] Pertinent_Thoughts_Scout.md; PD11 presorting note | Minutes treated as outcome, not assigned in sim |
| **PPM as environment-reflecting measure** | Hero lock on PPM z; perf-metric LOO batch (Sep 2026) failed to dethrone PPM on LOO-shape gate | See `sports_sandbox/_DISPOSABLE_perf_metric_rho_eda/LOO_SHAPE_REPORT.md` |

---

## 9. Regeneration lineage, doc bugs, recommended reading

### 9.1 Post-cleaning outputs with saved execution records

| Output | Saved spec / date | Notes |
|--------|-------------------|-------|
| Pass A sensitivity JSON/CSV/README | 2026-08-19 | PNGs referenced; **not in git** |
| SCOUT Q&A B1–B6 counts | 2026-08-19 | Verification memo, not JSONL |
| PD22 coverage JSON | 2026-08-19 | By-season team/row counts |
| Reigning hero provenance + LPM | 2026-09 | mg10, 09–21, last-PS |
| PD21 ρ bracket (hero + ppm0) | 2026-08-18 refresh | [Meeting record] PD23 |
| Box QC rollout checklist | Aug 17 | Steps 2–7 partly **⬜ pending** in policy §8 |

### 9.2 Likely still on older population

| Item | Risk |
|------|------|
| `GRANDCHILD_ncaa_roster_size_*` (generated **2026-08-11**) | **Pre–mg10** panel |
| Early Jul 2026 exports under `datasets/mbb/exports_inverted_u_v0/pre_july_26/` | Pre-QC era |
| Any figure not re-run after Aug 17 with `prepare_panel()` | Unknown — HAND PPTX audit required |

### 9.3 Documentation / code remnants

| Issue | Affects runs? | Source |
|-------|-------------|--------|
| **Jarvis 3-game** cited as “still in panel” | **Stale example** — consistent with mg10 (≥11) **excluding** 3-game teams unless different construction | policy §6 vs §3b |
| **`_apply_box_qc` fallback `min_g=5`** if attr missing | Only if config object **lacks** attribute; normal `PipelineConfig` supplies **10** | [Direct repo] `panel_rebuild.py` line 67 vs `config.py` |
| **`config.py` docstring says “Default 5”** but value **10** | Documentation drift only | [Direct repo] `config.py` lines 48–49 |
| Policy §5 code example still shows `min_team_season_games=5` | Stale maintainer copy | [Direct repo] `BOX_QC_panel_build_policy.md` §5 |

**No evidence** fallback=5 produced a saved hero artifact after Aug 17 evening.

### 9.4 Recommended reading (short list for VECTOR)

1. [`3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md`](../../../../../../3-Master_Plan/re_entry/SCOUT_and_COMPASS/SCOUT_and_COMPASS_Q_and_A.md) — B1–B6, B5a (CPR math)
2. [`3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/BOX_QC_panel_build_policy.md) — filter order + impact table
3. [`3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/sensitivity/README.txt`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/pass_a/sensitivity/README.txt) — paired curve headline
4. [`transcripts/PD23_notes.md`](../../../../../../transcripts/PD23_notes.md) — production lock (drop, mg10, ppm-zero contrast)
5. [`3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md`](../../../../../../3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md) — current hero spec vs sensitivity
6. [`3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md`](../../../../../../3-Master_Plan/obsolete/pre_tier1_locks/SCOUT_report_to_COMPASS.md) — team_mean vs LOO generative history

---

## Unresolved gaps (summary)

1. **Primary Charles/authored memo** for mg5→mg10 beyond same-day policy table.  
2. **PNG binaries** for Pass A sensitivity pair — JSON/CSV exist; images absent from git.  
3. **Team-level audit** of six 2015 two-player IDs (games, players, names).  
4. **Quantitative \(\hat{T}_j\) inflation audit** for fragmentary teams (Charles mechanism is **[Interpretation]**).  
5. **Complete regeneration log** — which HAND slides were actually re-pictured after Aug 17.  
6. **Otter transcript alone** does not prove drop-vs-zero interpretation (notes + code do).  
7. **Whether any early export baked PPM under pre–mg10 / min0 filters** — Charles requires post-filter derivation for new experiment; verify export metadata before Option B (§3.6.5).

---

*SCOUT historical response — read-only. Does not authorize new runs or population freeze. §3.6 records Charles Sep 25 requirement: derive PPM after filtering; prefer rebuild-from-box for assortativity freeze.*
