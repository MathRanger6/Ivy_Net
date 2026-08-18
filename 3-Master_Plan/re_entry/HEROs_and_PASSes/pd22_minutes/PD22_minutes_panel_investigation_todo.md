# PD22 — Minutes filter & panel policy investigation

**Source:** Alex meeting, 17 Aug 2026  
**Transcript:** `transcripts/20260817_Paper_Directions_22_otter_ai_transcript.docx`  
**Context:** PD21 ρ calibration — drop sub-20-min players (ρ\* ≈ 0, six of eleven seasons) vs keep roster and set PPM = 0 below 20 min (ρ\* ≈ 0.5–0.8). Alex: the minutes floor is no longer arbitrary; we need a defensible policy and to understand induced homophily from identical zeros.

**Scope guardrail (Alex):** ~few hours total. Understand enough to justify the choice and tell the story; do not block main PD21 / SELECT work.

---

## Suggested execution order

```
1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12 → 13 → 14 → 15
```

Items **1–5** unblock everything else. Items **10–12** are quick if PD17 interval plots already exist. Item **13** is optional unless caps and minutes look confounded.

---

## A. Justify the minutes floor

### 1. Drafted-player retention audit

For each candidate `min_minutes` threshold (start: 0, 1, 2, 5, 10, 15, 20), list every player-season with `Y_draft = 1` and flag whether they would be **dropped** vs **kept** (or zero-PPM under the alternative policy).

**Deliverable:** table of drafted players lost at 20 min; **minimum threshold that retains 100% of draftees** (Alex: “make sure we’re under that minimum”).

**Starting point:** extend `hero_min_minutes_sensitivity_ladder.py` meta (`n_drafted`) or a small one-off audit on the raw box panel. **See Appendix A** for what the ladder already tells us, what it misses, recommended audit logic, and **figure narrative** (left ECDF + right retention curve).

---

### 2. Minutes distribution — raw panel

Histogram / empirical cumulative distribution function (ECDF) of **total season minutes** per player-season (2011–2021, full roster before filter).

**Goal:** see where mass sits and whether 20 min is arbitrary or near a natural elbow.

**See Appendix B** for a plain-English narrative of the item 2 figure (left ECDF + right histogram zoom).

---

### 3. PPM distribution — players filtered out

For each threshold (especially 20 min), plot **raw points-per-minute** of players **below** the cut (the ones dropped or zeroed).

**Goal:** Alex’s “what is the distribution of PPM for the people we’re filtering out?” — documents what we’re throwing away and why minutes matter (the 2-min / 20-pts outlier case).

**See Appendix C** for plain-English narrative of the items 3–4 figure (filtered-out PPM + hero ASSIGN input); script: `pd22_ppm_distribution.py`.

---

### 4. PPM distribution — raw vs empirically capped

Side-by-side distributions of ability input used in ASSIGN:

- **Raw PPM** (after minutes rule, before caps)
- **Empirically capped PPM** (current hero pipeline caps)

Charles named both explicitly in PD22. Also sets up item 5 and the question of recalculating **without empirical caps** under the same minutes rule.

**Implemented with item 3** in one figure: left = filtered-out raw PPM; right = hero raw PPM + PPM z within season (ASSIGN input). “Empirical roster caps” (team sizes) are documented separately in slide bullets. **See Appendix C** for narrative.

---

### 5. Find a defensible cut line

Use items 2–4 plus item 1 to propose a **meaningfully justified** `min_minutes` (not “20 because we always used 20”). Treat as informal elbow / mixture peek — Alex framed it as “almost unsupervised grouping.”

**Constraint (item 1, literal):** chosen floor ≤ draft-safe minimum from item 1 → that means **floor = 0** if you must retain every ever-draft **player-season** row.

**Substantive constraint (career level):** min 20 drops 44 player-seasons but only **one ever-draft career** entirely (Ricky Ledo); everyone else keeps their real rotation seasons. **See Appendix A — player-season vs player** for the full breakdown and zero-minute season patterns.

**Working synthesis (Aug 17):** defend min 20 on **PPM-noise grounds** (items 2–4), not as literally draft-safe in Alex’s player-season audit. The draft audit is a conservative guardrail; the career-level story is much milder.

---

## B. PPM-zero policy & induced homophily

### 6. Performance distribution under PPM-zero ✅ (Aug 18 2026)

With `--ppm-zero-below-minutes 20`, plot the **post-policy ability distribution** (expect a zero spike). Compare to min-20 **drop** panel.

**Goal:** quantify “zero-heavy” shift Alex flagged when bench players stay on roster at PPM = 0.

**Done.** `python sports/scripts/pd22_ppm_zero_ability_distribution.py` → `PD22_ppm_zero_ability_distribution_2011_2021.{csv,json,png}`.

| Headline | Drop | PPM-zero |
|----------|------|----------|
| Panel *n* | 46,306 | 59,283 |
| Bench rows forced to PPM = 0 | — | 12,977 (21.9%) |
| Raw PPM = 0 | — | 13,180 |
| ASSIGN below −1 z | 7,356 | **14,028** |
| Zeroed cohort median *z* | — | ≈ −1.39 (season-dependent pile-up) |

**Say it aloud:** PPM-zero adds ~13k identical-at-zero bench rows back onto the roster; the ability histogram gains a fat gray left tail that drop removes entirely — Alex’s “zero-heavy” shift, visible before you even run ρ.

**See Appendix D** for how zero-minute rows are handled in raw columns, PPM plots, and each panel policy (drop vs NaN-drop vs PPM-zero).

---

### 7. Sanity check — no all-zero teams ✅ (Aug 18 2026)

Under PPM-zero policy, verify **no team-season** has all players at zero ability (Alex: “double check — real data”).

Quick counts: teams with ≥ k zeros; max zero fraction per team.

**Done.** `python sports/scripts/pd22_ppm_zero_team_sanity.py` → `PD22_ppm_zero_team_sanity_2011_2021.{csv,json,png}`.

| Headline | Value |
|----------|-------|
| Team-seasons | 3,842 |
| All-zeroed teams (every player `minutes < 20`) | **0** → **PASS** |
| Max zero fraction | 0.74 (32/43, team 2655 · 2019; rotation player at 1,018 min) |
| Median / p90 zero fraction | 0.20 / 0.35 |
| Teams with ≥ half roster zeroed | 74 |

**Say it aloud:** PPM-zero does pile zeros onto deep benches, but every real team-season still has at least one rotation player above the floor — no pathological all-zero rosters in 2011–2021 box data.

---

### 8. Mechanism check — zeros clustering on rosters ✅ (Aug 18 2026)

Per team-season under PPM-zero: count sub-20-min players zeroed; correlate with **empirical H_sort**.

**Hypothesis:** teams with many identical zeros inflate sorting / homophily (“high assortativity of losers”).

**Done.** `python sports/scripts/pd22_ppm_zero_hsort_mechanism.py` → `PD22_ppm_zero_hsort_mechanism_2011_2021.{csv,json,png}`.

| Headline | Value |
|----------|-------|
| corr(zero fraction, within-team perf std) | +0.53 (confounded by roster size — big benches have both) |
| Mean $H_{\mathrm{sort}}$ drop | 0.0642 |
| Mean $H_{\mathrm{sort}}$ PPM-zero | 0.0653 |
| **Δ mean** | **+0.0010** (season range −0.003 to +0.006) |

**Say it aloud:** PPM-zero barely moves empirical $H_{\mathrm{sort}}$ (~0.001 on a ~0.064 index) — the ρ\* jump to ~0.5–0.8 under PPM-zero is **not** a simple “identical zeros inflated sorting” artifact at the league level. Item 9 still needed for bracket ρ\* side-by-side.

---

### 9. Compare three panel policies at the chosen floor ✅ (Aug 18 2026)

| Policy | Longitudinal ρ\* (current / legacy) | Mean $H_{\mathrm{sort}}^{emp}$ (current panel) | Seasons ρ\*=0 |
|--------|-------------------------------------|-----------------------------------------------|---------------|
| **Drop** | **0.0** | 0.0642 | 11/11 |
| **PPM-zero** | 0.570 *(legacy JSON — pre-box-QC)* | 0.0653 | 0/11 *(legacy)* |

**Recommendation: drop at 20.** On the **current box-QC panel**, PPM-zero moves $H_{\mathrm{sort}}$ by only **+0.001** (item 8). The stored PPM-zero bracket JSON (ρ\*≈0.57) was fit to **pre-QC** $H_{\mathrm{sort}}$ targets (~0.17) — not valid for today's panel. Drop ρ\*=0 is on the locked panel.

**Say it aloud:** We considered PPM-zero; on real data it does not change sorting enough to justify ρ\*≈0.5. Drop-at-20 stays locked for PD21.

---

## C. Reconcile ρ\* = 0 vs interval-overlap story

### 10. Single-season interval overlap — ρ\* = 0 year ✅ (Aug 18 2026)

Pick a season where bracket gives ρ\* ≈ 0 (Alex suggested **2012**). Reproduce the **PD17-style interval overlap plot for that season only** (not pooled across all team-seasons).

**Question:** does the “clear linear increase in mean” red line still appear when ρ\* is zero?

**Done.** `python sports/scripts/pd22_interval_overlap_season.py --season 2012` → `PD22_interval_overlap_season_2012.{csv,json,png}`.

| Headline | 2012 |
|----------|------|
| Bracket ρ\* (drop) | **0.0** |
| $H_{\mathrm{sort}}$ | 0.0709 |
| Team-seasons | 345 |
| Max coverage | 345 (full stack at peak) |
| Grid fraction with >1 team | **89.2%** |

**Say it aloud:** ρ\* = 0 does **not** mean rosters look disjoint — 2012 still shows massive interval stacking and the crimson sort-and-chop benchmark sits below actual coverage. Bracket ρ\* answers a sim-calibration question; overlap plots show realized roster geometry.

---

### 11. Single-season interval overlap — ρ\* > 0 year ✅ (Aug 18 2026)

Same plot for a non-zero season (Alex suggested **2013**, ρ\* ≈ 0.07).

**Goal:** answer Alex’s “why did you get zero?” when longitudinal overlap looked meaningful.

**Done.** `python sports/scripts/pd22_interval_overlap_season.py --season 2013` → `PD22_interval_overlap_season_2013.{csv,json,png}`.

**Panel epoch (Alex’s ρ\* ≈ 0.07):** From the **PD21 roster-caps calibration slide** (HAND — “WITH ROSTER CAPS”): min≥20 drop, empirical roster caps, **pre-box-QC** panel. Stored readout: `pd21_rho/PD21_rho_hsort_sensitivity.json` subset `full_min20` — longitudinal ρ\* ≈ **0.067**, 2013 ρ\* ≈ **0.074**, mean $H_{\mathrm{sort}}^{\mathrm{emp}}$ ≈ **0.105** (matches the slide subtitle).

**Locked hero panel (box QC):** `PD21_rho_hsort_calibrate_2011_2021_fit_bracket.json` — **2013 also gives ρ\* = 0** (same as 2012); $H_{\mathrm{sort}}^{\mathrm{emp}}$ ≈ **0.062**. Item 11 overlap plots use this locked panel. The 2012 vs 2013 contrast is **$H_{\mathrm{sort}}$ and overlap intensity**, not bracket ρ\* under the locked estimand.

| | 2012 (item 10) | 2013 (item 11) |
|---|----------------|----------------|
| Bracket ρ\* | 0.0 | 0.0 |
| $H_{\mathrm{sort}}$ | 0.0709 | 0.0620 |
| Team-seasons | 345 | 347 |
| Grid fraction >1 team | 89.2% | **95.0%** |

**Say it aloud:** Both zero-ρ\* seasons still show massive overlap — 2013 if anything *more* stacked than 2012. “Why ρ\* = 0?” → bracket fit on modest $H_{\mathrm{sort}}$ (~0.06–0.07) on the locked panel, not because intervals look disjoint. Alex’s 2013 ρ\* ≈ 0.07 was on the **earlier roster-caps panel** before box QC.

---

### 12. Team-rank dissection — 2012 vs 2013 *(skipped — optional)*

Plot **team ranks** (or H_sort by team) for those two seasons side by side.

**Goal:** “what made 2012 so different from 2013?” — roster depth, star concentration, meaningful minute-players vs bench zeros.

**Status:** Skipped Aug 18 2026. Original motivation was ρ\* contrast (2012 zero vs 2013 ≈ 0.07); resolved by panel-epoch note (item 11). Items 10–11 already show overlap persists at ρ\*=0. Forensic color only — not blocking for item 15 memo.

---

## D. Empirical caps & sensitivity

### 13. Same minutes rule, no empirical caps

Charles’s opening PD22 question: rerun key readouts (empirical H_sort, maybe one-season ρ bracket) with **empirical caps turned off** but the same minutes policy.

**Goal:** separate “minutes filter” from “cap distortion” in the story.

---

### 14. Minutes ladder on ASSIGN ρ\*

Extend `pd21_rho_hsort_sensitivity.py` (currently 0 vs 20) to a ladder aligned with item 1: `{0, draft-safe-min, 10, 15, 20}` × `{drop, ppm-zero}`.

**Deliverable:** one CSV + small plot — H_sort^emp and ρ\* vs threshold.

---

## E. Close the loop

### 15. PD20–22 takeaways memo ✅ (Aug 18 2026)

**Format:** conversational **narrative memo** slides — each slide answers one question with four labeled blocks: *Why we did it → What we did → What we saw → So for us*. Large prose type (not HAND bullet diagnostics).

```bash
python sports/scripts/build_pd20_22_takeaways_memo.py
```

**Output:** `slides/auto/CHAR_PD20_22_takeaways_memo_AUTO.pptx` (7 slides).

| Slide | Question answered |
|-------|-------------------|
| 1 | How to read this memo |
| 2 | Is 20 minutes arbitrary? What PPM do we drop? |
| 3 | Drop vs set sub-20-min PPM to zero? |
| 4 | Why $\rho^*=0$ but overlap looks sorted? |
| 5 | What $\rho$ for PD21 calibration? |
| 6 | Does Gibbs SELECT kill the inverted-U? |
| 7 | Bottom line — what we lock |

**Typography:** `memo_slide_common.py` — narrative blocks at 17 pt body, 14 pt section labels (vs HAND 10 pt diagnostic decks).

**Say it aloud:** Drop at 20 · ρ\*≈0 on locked panel · inverted-U survives SELECT · do not over-interpret assortativity.

---

### 16. Time box

Alex: **~few hours total** on this thread. If item 9 picks a policy and item 15 is draftable, **stop** and resume main ρ / SELECT / story track.

---

## Existing hooks in the repo

| Item | Starting point |
|------|----------------|
| 1, 14 | `sports/scripts/hero_min_minutes_sensitivity_ladder.py` |
| 6, 9, 14 | `sports/scripts/pd21_rho_hsort_calibrate.py` (`--ppm-zero-below-minutes 20`) |
| 14 | `sports/scripts/pd21_rho_hsort_sensitivity.py` |
| 4, panel policy | `3-Master_Plan/Alex_notes/rho_est_options_for_dummies.md` |
| 10–11 | PD17 interval overlap slide / outputs |

---

## PD22 transcript — key Alex quotes (paraphrased)

1. **Draft safety:** “What’s the minimal filter where we at least keep everybody who is drafted?”
2. **Filtered-out PPM:** “What is the distribution of points per minute for the people that we’re filtering out?”
3. **Two distributions:** raw PPM and empirically capped PPM; find the “natural line” for the cut.
4. **Induced homophily:** pushing sub-20-min players to zero may inflate H_sort because “lots of zeros will be with each other.”
5. **Sanity:** no team should be all zeros — double-check.
6. **ρ\* puzzle:** locked panel → all ρ\* = 0; legacy roster-caps panel had non-zero seasons (2013 ρ\* ≈ 0.074). Compare interval plots and team ranks for 2012 vs 2013 on the **locked** panel (overlap intensity, not ρ\* contrast).
7. **Scope:** few hours; model is strong even if assortativity is weak; pick a justified policy and move on.

---

## Figure narratives (appendices)

Plain-English walkthroughs of the three PD22 diagnostic figures (slide PNGs in this folder):

| Appendix | Item(s) | Figure |
|----------|---------|--------|
| **A** (end) | 1 — drafted retention audit | ECDF + retention vs floor |
| **A** (end) | 5 — player-season vs player | *(prose only; no figure)* |
| **B** | 2 — raw panel minutes | ECDF all vs ever-draft + low-minute histogram |
| **C** | 3–4 — PPM tails vs hero ASSIGN | Filtered-out PPM (log *y*) + hero raw PPM + within-season *z* |
| **D** | 6+ — zero-minute policy | *(prose/table only; no figure)* |

---

## Appendix A — Item 1 starting point (drafted-player retention audit)

*Added Aug 17 2026 from COMPASS elaboration on `hero_min_minutes_sensitivity_ladder.py` and panel rebuild mechanics.*

### What you already have (partial answer)

You ran `hero_min_minutes_sensitivity_ladder.py` on Aug 12. The meta file at
`3-Master_Plan/re_entry/HEROs_and_PASSes/grandchild_assign/HERO_min_minutes_sensitivity_2011_2021_meta.json`
already tracks `n_drafted` at each floor:

| `min_minutes` | Player-seasons | `n_drafted` |
|---------------|----------------|-------------|
| 0 | 82,893 | **1,136** |
| 10 | 72,687 | **1,136** |
| 20 | 62,180 | **1,134** |

So under the **drop** policy, **20 min loses exactly 2 drafted player-seasons** relative to 10 min (and 0). That is a useful headline for Alex — the damage at 20 is small in count — but it is not enough on its own. Alex’s question is *who* they are and whether any of them matter for the story (injury season, outlier PPM, etc.).

**Authoritative audit (Aug 17 run):** `pd22_drafted_minutes_audit.py` on the full box panel at `min_minutes=0` finds **1,178** ever-draft player-seasons (521 unique athletes). Under **drop** at min 20: **44 lost** (42 unique; 42 at 0 min, 2 at 17–18 min). The ladder’s “2 lost at 20” used a narrower filtered panel — treat the audit as the draft-safe headline.

### Why the ladder is only a starting point

The ladder script was built for a different job: “does the inverted-U shape change when we raise the minutes floor?” It reports aggregate `n_drafted` per floor, but it does **not**:

1. **Name the lost rows** — athlete, season, team, minutes, PPM
2. **Separate minutes loss from other loss** — `filter_panel()` drops rows missing `poolq_loo` or `Y_draft` *before* applying the minutes cut
3. **Scan fine-grained thresholds** — only 0 / 10 / 20; Alex wants the **minimum floor that retains 100%** of draftees
4. **Distinguish drop vs PPM-zero** — under `--ppm-zero-below-minutes 20`, drafted players with low minutes **stay on the roster** (PPM set to 0); the ladder never exercises that mode
5. **Flag the injury-season narrative** — e.g. a future NBA player who logged 8 minutes in 2014 because of injury

Also worth knowing: **`Y_draft` is an ever-draft flag** (athlete in `athlete_id_draft_lookup.csv`), not “drafted that season.” So you are auditing “do we ever drop a player-season belonging to someone who eventually made the NBA?” — which matches Alex’s concern about injury/low-minute seasons for drafted talent.

### Where the minutes filter actually bites (two stages)

There are two places minutes matter; item 1 should be explicit about which you mean:

**Stage A — panel rebuild** (`panel_rebuild.build_from_box`): if `min_minutes > 0`, rows with `minutes < min_minutes` are removed **before** PPM, within-season z-score, and LOO pool quality are computed. This is what the ladder and PD21 drop policy use.

**Stage B — `filter_panel()`** (`panel_build.filter_panel`): after perf/LOO, again `minutes >= min_minutes` if configured. With rebuild already filtered, this is mostly redundant — but the **poolq_loo dropna** here is not.

For PD21 **PPM-zero**, rebuild uses `min_minutes=0` (everyone stays for LOO), then raw PPM is zeroed below 20 *before* z-scoring — a different policy, and drafted players are never dropped for low minutes.

### The audit logic (what item 1 should actually compute)

Conceptually simple:

1. Build the panel **once** with `min_minutes=0` (same 2011–2021 box rebuild as everything else).
2. Restrict to rows with `Y_draft == 1`.
3. For each candidate threshold `T` (0, 1, 2, 5, 8, 10, 15, 20, …):
   - **Drop policy:** count rows with `minutes < T` → these would be excluded at floor `T`
   - **PPM-zero policy:** count stays 0 lost (everyone kept); optionally flag how many would get PPM=0
4. **Draft-safe maximum floor** = largest `T` such that zero `Y_draft=1` rows have `minutes < T`
   - Equivalently: `T_safe = floor(min(minutes))` among all drafted player-seasons
   - Any policy with `min_minutes <= T_safe` retains every drafted row under **drop**

Deliverables Alex cares about:

- A **CSV of drafted player-seasons** sorted by minutes (the tail is the risk zone)
- A **one-line answer**: “At 20 min we drop 2 of 1,136 drafted player-seasons; draft-safe floor is X min”
- Optional: the 2 rows highlighted with name, season, team, minutes, raw PPM — for the injury/outlier conversation

### Extend the ladder vs small PD22 script?

**Option A — extend the ladder**

Add a `--draft-audit` block to `hero_min_minutes_sensitivity_ladder.py`: build once at min=0, emit `HERO_drafted_minutes_audit_2011_2021.csv` + threshold table. Pros: reuses `_pipeline_config` / `_prepare_panel`. Cons: mixes two diagnostics in one script.

**Option B — dedicated `pd22_drafted_minutes_audit.py`** (recommended)

Thin script in `sports/scripts/`, outputs under `pd22_minutes/`. Same panel build as PD21/ladder, single purpose, easy to cite in the memo. ~80 lines.

Either way, the core is identical: **one rebuild at min=0, then slice on `minutes` — do not re-run the full ladder per threshold.**

### Interpretation hooks for the Alex conversation

**Good news from existing meta:** 10 min and 0 min agree on `n_drafted` (1,136), so the two losses at 20 live in the **10–20 minute band** — not deep bench garbage. That supports the earlier note that “going to 10 gives almost the same.”

**The real question is identity, not magnitude:** Are those 2 rows “Gonzaga star, torn ACL, 15 minutes” or “walk-on who later made a two-way contract”? Alex wants to know we are not silently deleting meaningful outliers.

**Drop vs PPM-zero for item 1:** Item 1 is really about the **drop** policy. PPM-zero sidesteps draft loss entirely; item 9 compares policies *after* you know the drop floor is draft-safe.

**ASSIGN vs SELECT:** Same minutes column and `Y_draft` flag; item 1 is layer-agnostic. If SELECT MLE later uses a different floor, that becomes a separate memo bullet — but the audit table is shared infrastructure.

---

### Item 1 figure narrative (drafted retention audit)

*Added Aug 17 2026. Numbers from `PD22_drafted_minutes_audit_2011_2021.json` (2011–2021 box rebuild, `min_minutes=0`; `Y_draft` = ever-draft flag).*

### Setup (what both panels share)

Both panels restrict to **ever-draft player-seasons only** — athletes who eventually made the NBA (`Y_draft = 1`), about **1,178** rows across 2011–2021. The panel is rebuilt once with **no minutes filter**; we then ask how many of those rows would disappear under a **drop** policy at each candidate floor. Teal dashed = **10 min**; solid red = **20 min** (hero lock).

**Headline:** draft-safe max floor under drop is **0 min** — any positive floor drops at least the **42 zero-minute** ever-draft placeholder seasons. At min 20 we lose **44** player-seasons (**42 unique** athletes): those 42 zeros plus **two** rows at **17–18 minutes** (2017). Under **PPM-zero**, all 1,178 stay on the roster.

---

### Left plot — drafted minutes ECDF

**What this plot is for:** where do *future NBA players* actually log minutes in college? This is the draft-safety view — not the full roster skew from item 2.

**X-axis:** season minutes for one drafted athlete on one team in one season.

**Y-axis:** cumulative fraction — share of ever-draft player-seasons at or below that minute total.

**Blue curve:**

- The curve sits **high and flat near zero** for a long stretch, then **rises steeply** in the rotation band (roughly 600–1,200 minutes). **Median drafted minutes ≈ 979** — these are mostly real playing seasons.
- The flat start is **not** “everyone plays zero”; it means only a **small fraction** of ever-draft rows sit in the very low-minute tail. Zoom the x-axis mentally below 100: the curve barely lifts before it shoots up toward starter minutes.
- The **10- and 20-minute lines** sit in that flat left region. Almost all drafted talent is **to the right** of both lines.

**Say it aloud:** *“Left panel: future NBA players overwhelmingly log heavy minutes. The 20-minute line is far left on their distribution — we are not cutting meaningful rotation seasons, we are mostly deciding what to do with zero-minute roster placeholders and a tiny 17–18 minute tail.”*

---

### Right plot — retention vs floor (drop policy)

**What this plot is for:** how many ever-draft player-seasons survive each **drop** threshold? Red numbers = **lost** at that floor.

**X-axis:** candidate `min_minutes` floor (drop if `minutes < floor`).

**Y-axis:** count of drafted player-seasons **retained** (y-axis zoomed to the narrow band 1,130–1,190 so the steps are visible).

**Blue line (drop policy):**

- **Floor 0:** all **1,178** retained.
- **Floor 1:** sharp drop to **1,136** — **42 lost** immediately. Those are the **zero-minute** ever-draft rows (42 unique athletes). Retention is **flat from 1 through 15** — no additional drafted rows live in the 1–15 minute band.
- **Floor 20 (red line):** **1,134 retained**, **44 lost** — the extra **2** vs floor 15 are the **17–18 minute** seasons in 2017.
- **Floors 25 and 30:** small further losses (**45** and **48**) as more low-minute but sub-20 drafted rows get cut.

**Say it aloud:** *“Right panel: draft loss is a step function. Turn on any positive floor and you lose 42 zero-minute placeholders. Min 20 adds only two more — not forty. PPM-zero keeps everyone if draft retention is the binding constraint.”*

---

### Left + right together (one paragraph for Alex)

Among ever-draft player-seasons, playing time is concentrated in real rotation minutes (median near 980), with a thin left tail of roster placeholders. The ECDF shows that tail is tiny relative to the mass of the curve. The retention ladder shows where policy bites: 42 losses at any floor ≥ 1 (all zero-minute), flat through 15, then two more at 20. Min 20 under drop is draft-*almost*-safe — the honest caveat is those 42 zero-minute NBA guys and two sub-20-minute rows, not a broad strip of meaningful low-minute seasons.

---

### Player-season vs player (item 5 hook)

*Added Aug 17 2026. Extends item 1 audit; names in `PD22_drafted_minutes_audit_2011_2021.csv`.*

Alex’s draft-safe question is defined at **player-season** level: does any row with `Y_draft = 1` get dropped? That is conservative and correct for the audit — but it is easy to misread “44 lost” as “44 future NBA careers deleted.” It is not. The panel is one row per `(athlete_id, season, team_id)`; a minutes floor drops **rows**, not whole athletes unless every row for that athlete is below the floor.

#### Two different “draft-safe” answers

| Question | Answer at min 20 (drop) |
|----------|-------------------------|
| **Player-season audit** (Alex item 1) | **Not draft-safe** — need floor **0** to keep all 1,178 ever-draft rows |
| **Career audit** (substantive) | **Almost fully safe** — **479 / 521** unique ever-draft athletes lose **no** rows; **41** lose only a ghost/zero season; **1** loses everything |

#### What min 20 actually removes

| Level | Count |
|-------|-------|
| Player-seasons lost | **44** |
| Unique athletes with **any** season lost | **42** |
| Athletes who lose **every** row in the panel | **1** — Ricky Ledo (Providence 2014, 0 min; eligibility / never played in box data) |
| Athletes with zero-minute row **plus** other seasons kept | **39** of 40 zero-minute cases |
| Sub-20-minute losses with real minutes | **2** — Desmond Bane (17 min, Washington 2017), Skylar Mays (18 min, Old Dominion 2017) |

**Examples (ghost season dropped, real season kept):**

- **Jaylen Brown:** 2015 California = 0 min (dropped) · **2016 = 907 min** (kept)
- **Mikal Bridges:** 2015 Villanova = 0 · **2016–2018 = 800–1,285 min** (kept)
- **Jordan Clarkson:** 2013 Missouri = 0 (transfer sit-out pattern) · **2014 = 1,228 min** (kept)

For ASSIGN / homophily, these athletes still enter through their rotation seasons. Dropping the zero row removes one node from **one** team-season graph — it does not erase the career.

#### What are the zero-minute ever-draft seasons?

**Redshirt is not coded** in the box panel. `panel_rebuild` sums game minutes from `mbb_df_player_box.csv`; there is no redshirt flag. The 42 zero-minute drafted rows are mostly:

1. **Phantom pre-season row** — roster artifact one year before the player actually logged minutes (e.g. Jaylen Brown 2015, Mikal Bridges 2015, De'Andre Hunter 2017; next season at same school has heavy minutes).
2. **Transfer sit-out** — on roster at new school, 0 box minutes, then real minutes the following year (e.g. Clarkson at Missouri 2013, Rodney Hood at Duke 2013).
3. **Phantom exit-year row** — last row after a full season with no games recorded (e.g. Jaylen Brown 2017 after 2016; Branden Dawson 2016 after 2015).
4. **True no-play season** — Ricky Ledo (Providence 2014; eligibility; only ever-draft athlete fully removed at min 20).

These zeros are **in the data for a reason** (roster presence, transfers, eligibility, labeling quirks) — but they are not “we deleted a star’s only meaningful season.”

#### Career length and the redshirt heuristic (>4 player-seasons)

Charles’s check: if a drafted athlete has **more than 4 player-seasons** in the panel and one is zero, that pattern is *consistent* with a redshirt (four playing years plus one zero year). Count from the audit CSV:

| Career length in panel (among 40 athletes with any zero-minute season) | Athletes |
|-----------------------------------------------------------------------|----------|
| **> 4 player-seasons** | **11** (27.5%) |
| Exactly 4 | 11 |
| 3 seasons | 12 |
| 2 seasons | 5 |
| 1 season (Ricky Ledo only) | 1 |

**>4 seasons does not cleanly identify redshirts.** Most of the 11 look like exit-year phantoms, transfer sit-outs, or pre-season label artifacts — not a coded redshirt year:

| Pattern (11 athletes with >4 seasons) | Examples | Likely redshirt? |
|---------------------------------------|----------|------------------|
| Phantom **exit** year (zero after heavy minutes) | Branden Dawson 2016, Tyrone Wallace 2017, Sandro Mamukelashvili 2021 | No |
| Phantom **pre-season** row (zero, then real minutes next year) | Devon Hall 2014, Grant Riller 2016 | No |
| **Transfer sit-out** (zero at new school) | Abdel Nader 2014 (Iowa State) | No |
| Zero **sandwiched** between playing years | George King 2015, Eric Paschall 2016, Cody Martin 2017, Marial Shayok 2018 | *Maybe* — cannot confirm without eligibility metadata |
| Duplicate-season / data mess | Semi Ojeleye (two 2015 rows, two zeros) | No |

The **12 athletes with only 3 seasons** (Jaylen Brown, Mikal Bridges, De'Andre Hunter, …) show the classic **zero in year *N*, heavy minutes in *N*+1** pattern — usually a phantom first-year row, **not** something the >4-season rule would catch.

**Takeaway:** only **11 of 40** zero-minute ever-draft cases have >4 panel seasons; at most a handful might be true redshirt years, and the box data cannot distinguish them from artifacts. This does not change the item 5 story — **479 of 521** ever-draft careers are still untouched at min 20.

#### Drop vs PPM-zero for drafted rows

Both policies treat zero-minute seasons as “no performance signal”:

- **Drop:** row gone from that team-season.
- **PPM-zero:** row stays, ability set to 0 before z-score — Alex’s induced-homophily concern (bench zeros clustering).

The policy fork matters more for the **~20,663 sub-20-min rows with 1–19 minutes** (item 3 PPM tail) than for these 42 drafted ghosts.

#### Say it aloud (item 5)

*“Draft-safe in Alex’s literal audit means floor zero — any positive floor drops placeholder player-seasons. But we’re not removing NBA guys from the dataset: 479 of 521 ever-draft athletes are untouched at min 20, and the zeros look like roster or transfer artifacts, not redshirt seasons we mishandled. Min 20 is defensible because of PPM noise on the full panel, with a honest footnote about Ledo and two 17–18 minute rows — not because it passes the player-season audit.”*

---

## Appendix B — Item 2 figure narrative (raw panel minutes)

*Added Aug 17 2026. Numbers from `PD22_raw_minutes_distribution_2011_2021.json` (2011–2021 box rebuild, `min_minutes=0`).*

### Setup (what both panels share)

Both panels use the **raw panel**: every player-season rebuilt from box score data with **no minutes filter** (`min_minutes = 0`). That is roughly **104,790 player-season rows** in the Aug 17 run — anyone on a roster, from stars to walk-ons to zero-minute placeholders.

The teal dashed line is **10 minutes**; the solid red line is **20 minutes** (the current hero lock). Those are candidate floors, not facts about the data — they mark where we *might* cut.

---

### Left plot — full-panel empirical cumulative distribution function (ECDF)

**What this plot is for:** the big picture. Where does playing time live across the **entire** NCAA panel, and how does the **ever-draft** subset compare?

**X-axis:** season minutes for one player on one team in one season (0 to about 1,150 on the chart; the axis stops near the 99th percentile so extreme seasons do not squash everything else).

**Y-axis:** cumulative fraction — the share of player-seasons with **that many minutes or fewer**. At y = 0.5, half the panel is at or below that x.

**Blue curve (all player-seasons):** the full roster.

- The curve **jumps up immediately at x = 0** because about **21%** of all rows (**~21,900**) are **zero-minute** — on the roster, no recorded playing time. A big chunk of the raw panel is not “bench with 5 minutes”; it is literally **zero**.
- After that jump, the curve **rises fastest in the low-minute region** (roughly 0–100 min): a lot of cumulative probability piles up while x is still small, so the line climbs noticeably. **Do not expect “steepening” further right** — on a linear minutes axis the slope **flattens** as x grows, because rotation players are spread across hundreds of minutes and each minute band adds only a thin slice of cumulative share.
- **Median minutes for the full panel is only 31** — already half the panel is at or below 31 min (including zeros) — while the **75th percentile is 434** and the **90th is 840**. The upper half of the panel is a **long, gentle climb** on the ECDF toward y = 1, not a steep middle bump. That is the visual signature of a heavy left tail plus a wide right spread.

**Orange curve (ever-draft only, `Y_draft = 1`):** about **1,178** player-seasons belonging to athletes who eventually made the NBA.

- This curve sits **far to the right** of the blue curve almost everywhere. **Median drafted minutes ≈ 979** — these are mostly real seasons, not roster ghosts.
- Only about **3.7%** of ever-draft player-seasons fall **below 20 minutes**. On this full-scale plot that tail is a tiny wiggle near the origin; the orange curve barely separates from the bottom before it shoots up toward regular rotation minutes.

**Say it aloud:** *“Left panel: for the whole panel, playing time is extremely skewed — one in five rows is zero minutes, and the median is only 31 minutes. Future NBA players are different: their curve is shifted way right; they mostly log heavy minutes. The 20-minute floor question affects a thin slice of drafted rows but a much larger share of the full panel.”*

At 20 minutes, about **41%** of **all** player-seasons are below the line — versus **~4%** of ever-draft rows. **Min 20 is a strong scrub on the full roster but a light touch on drafted talent** (mostly zero-minute placeholders, not 15-minute injury seasons).

---

### Right plot — histogram zoom (0–150 minutes)

**What this plot is for:** the **action zone** the left plot hides. Same data, but **magnified to the first 150 minutes** so bin counts are visible instead of a compressed sliver on the ECDF.

**X-axis:** same season minutes, but only **0–150** (where floor policy actually bites).

**Y-axis:** **count** of player-seasons in each bin (not a fraction). Taller bar = more rows in that minute band.

**Blue bars (all player-seasons):**

- The **tallest bar is at 0** — the ~21,900 zero-minute rows dominate visually. Roster padding: managers, injured reserves, DNPs, redshirt tags, etc.
- There is still substantial mass in **1–20 minutes** — garbage-time, end-of-bench, late-game seconds. Together with zeros, **~41%** of the panel falls below 20 minutes.
- Bars shrink quickly after ~30–60 minutes, then trail off.

**Orange outline (ever-draft overlay):**

- Drafted players **barely appear** in the low bins: a small trace at 0 (the **42** zero-minute drafted placeholder seasons from item 1) and almost nothing in 1–19 except **two** rows at 17–18 minutes.
- **The low-minute histogram is overwhelmingly a non-drafted phenomenon.** The floor mainly decides what to do with **bench/placeholder rows**, not stripping meaningful minutes from future pros.

**The 10- and 20-minute lines** mark **policy cutoffs** through the low-minute region:

- **10 min:** about **31%** of the full panel is to the left.
- **20 min:** about **41%** of the full panel is to the left — a strict drop policy removes **well over 40,000** player-seasons before pool-quality filtering.

**Say it aloud:** *“Right panel: zoom in where the left plot squishes everything. The story is the zero-minute spike — one fifth of the panel never played. Ever-draft players barely show up here. The 20-minute line cuts through a huge block of low-minute roster rows that are mostly not future NBA guys. That is why we need an explicit policy — drop them, or keep them with PPM set to zero — not just an arbitrary filter.”*

---

### Left + right together (one paragraph for Alex)

We rebuilt the 2011–2021 panel with no minutes filter. Playing time is wildly skewed: many zero-minute roster rows and a long bench tail, so the full-panel median is only 31 minutes even though rotation players log hundreds. Future draftees look nothing like that — median near 980 minutes, only about 4% of their player-seasons below 20 minutes, mostly zero-minute placeholders. The ECDF shows that contrast on the full scale; the histogram zoom shows where the mass actually lives near zero. A 20-minute drop rule would remove roughly 41% of all player-seasons but only a small, mostly zero-minute slice of ever-draft rows — which is why item 1 names exactly who those 44 player-seasons (42 unique athletes) are before we defend the floor for ρ calibration.

---

## Appendix C — Items 3–4 figure narrative (PPM tails vs hero ASSIGN input)

*Added Aug 17 2026. Numbers from `PD22_ppm_distribution_2011_2021.json` (2011–2021; two panel rebuilds: filtered-out at min=0, hero at min=20).*

### Setup (what the three panels share)

This figure answers Alex’s “what PPM are we throwing away?” and Charles’s paired question: **raw PPM** vs what actually enters **ASSIGN** after the minutes rule. **Left** = rows with **minutes &lt; 20** on the unfiltered panel (**42,559** total; **21,896** at exactly 0 min). **Right column** = **hero panel** after min-20 **drop** (**62,231** player-seasons): raw PPM on top, **PPM z-scored within season** on bottom (PD21 ASSIGN ability input). Empirical roster caps (team-size multiset) are **not** in this figure — they are a separate pipeline step.

---

### Left plot — filtered-out raw PPM (1–19 minutes played)

**What this plot is for:** the **noisy tail** we remove or zero when we impose a minutes floor — Alex’s garbage-time / small-sample PPM concern.

**X-axis:** raw points per minute (PPM) for player-seasons with **1–19 minutes** (zero-minute rows excluded from bars but counted in the inset).

**Y-axis:** player-season count on a **log scale** (so the sparse high-PPM bars are visible, not crushed by the near-zero spike).

**Blue histogram:**

- **Huge mass near PPM ≈ 0** — many sub-20-minute rows are low-scoring end-of-bench or token appearances; median PPM among positive-minute filtered rows is only **~0.13**.
- **Long, sparse right tail** — **327** rows with **PPM &gt; 1.0** (inset); **max raw PPM = 6.0** in the full tail (x-axis truncates near the 99th percentile so the plot is readable). These are the “2 minutes, 20 points” outliers Alex warned about — rare but real.
- **Log y-axis** makes the tail legible: on a linear scale the high-PPM bins vanish next to the left spike.

**Inset box (upper right):** **21,896** zero-minute rows excluded from the histogram; **327** sub-20-min rows with PPM &gt; 1; **max PPM = 6**.

**Say it aloud:** *“Left panel: below 20 minutes, PPM is mostly noise near zero, but a few hundred rows spike above 1.0 — that is why a minutes floor is not arbitrary for ASSIGN. We are not deleting star seasons; we are deleting unstable rate stats from tiny samples.”*

---

### Right top — hero panel raw PPM (min ≥ 20)

**What this plot is for:** what ability **looks like after** the floor, before within-season standardization.

**X-axis:** raw PPM on the min-20 panel.

**Y-axis:** count (linear).

**Blue histogram:**

- **Roughly bell-shaped**, centered near **median PPM ≈ 0.30** — a stable, rotation-player distribution.
- **99th percentile ≈ 0.70** — much tighter than the filtered-out tail; extreme PPM above 1 is rare once minutes are adequate.

**Say it aloud:** *“Top right: after min 20, raw PPM looks like a normal performance cloud — not the weird spike-and-tail mess on the left.”*

---

### Right bottom — ASSIGN ability (PPM z within season)

**What this plot is for:** the **actual numeric input** to homophily calibration after the hero pipeline’s within-season z-score step.

**X-axis:** PPM z within season (mean 0, unit variance by construction within each season).

**Y-axis:** count (linear).

**Orange histogram:**

- **Tight central mass** near 0 (median ≈ **−0.05**); bulk between about **−2 and +3**.
- **Long right tail** out to roughly **+20 z** — a few extreme seasons per year, not a separate population. This is within-season ranking noise compressed by z-scoring, not the empirical cap step.

**Say it aloud:** *“Bottom right: ASSIGN sees standardized within-season ability — mostly near zero, with rare hot seasons in the tail. The minutes floor cleaned up the left-panel garbage; z-scoring puts everyone on a common season scale.”*

---

### All three panels together (one paragraph for Alex)

Below 20 minutes, raw PPM is dominated by near-zero rates plus a thin tail of extreme spikes (327 rows above 1.0, max 6.0) — exactly the small-sample noise a minutes guard is meant to remove. After dropping to min 20, raw PPM is a tight bell near 0.3 PPM, and the ASSIGN input is within-season z-scores centered at zero with a few legitimate star tails. The story for ρ calibration: **floor first** (drop or PPM-zero), **then** z-score; the left panel documents what the floor protects against, the right column documents what homophily actually eats. The overlay figure (`PD22_ppm_full_vs_filtered_2011_2021.png`) gray curve is **full panel with defined PPM** (`minutes > 0` only) — see Appendix D.

---

## Appendix D — Zero-minute handling by layer

*Added Aug 17 2026. Source: `panel_rebuild.py`, `panel_build.py`, `pd21_rho_hsort_calibrate.py`, PD22 diagnostic scripts.*

Zero-minute player-seasons (~21,900 on the raw panel, ~21% of rows) are handled **consistently at the column level** but **differently by plot type and panel policy**. This table is the cheat sheet for “what happens to 0-min rows?”

### Raw column (always)

| Step | Zero-minute behavior |
|------|----------------------|
| **`panel_rebuild`** | `ppm = points / minutes` if `minutes > 0`, else **`NaN`** (not 0). Same since 530 extract. |

### Plots (PD22 and legacy)

| Plot / diagnostic | Zero-minute rows | Notes |
|-------------------|------------------|-------|
| **Item 2** — minutes ECDF / histogram | **Included** | Axis is **minutes**, not PPM — zeros are the big spike at 0. |
| **Items 3–4 / overlay** — PPM histograms | **Excluded from bars** | Only `minutes > 0` (defined PPM). Zeros counted in inset / footnote. |
| **Overlay gray “full panel”** | **Excluded** | Really “full panel with defined PPM” (~82,894 rows), not all 104,790. |
| **Legacy 537 cohort** | **Excluded** | Filter: `minutes > 0`, finite PPM, often `ppm > 0`. |
| **`dataset_coverage`** | **Excluded** | PPM/minutes base uses `minutes > 0`. |

**Plot consistency:** excluding 0-min from PPM histograms matches **`ppm = NaN`** — you cannot histogram undefined values.

### Calculations (panel policy — three forks)

| Policy | Zero-minute rows in raw panel? | `ppm` / `perf` | Enter ASSIGN / ventiles / ρ? |
|--------|-------------------------------|----------------|------------------------------|
| **A. Drop** (`min_minutes = 20`, PD21 default) | No — dropped at **`panel_rebuild`** | N/A | **Never** — row removed before perf / LOO |
| **B. Raw min = 0, no PPM-zero** | Yes — stay on roster | `ppm = NaN` → `perf = NaN` → `poolq_loo = NaN` | **No** — `filter_panel()` drops via `dropna(poolq_loo)` |
| **C. PPM-zero** (`--ppm-zero-below-minutes 20`) | Yes — stay on roster | `ppm` set to **0** for all `minutes < 20` (includes 0-min) → z-scored | **Yes** — enters homophily with zero ability; Alex’s bench-clustering concern |

### Say it aloud

*“Zero minutes means undefined PPM everywhere in the code — we never divide by zero. PPM plots exclude those rows because there’s nothing to plot. Under drop-at-20 they’re gone before the model sees them. Under raw min-zero they sit on the roster but NaN out of pool quality. Under PPM-zero we force ability to zero and they stay in — that’s the policy fork item 6 is about.”*

---

*Generated from PD22 discussion, Aug 17 2026. Print via `./scripts/convert_single_md_to_pdf.sh` if desired.*
