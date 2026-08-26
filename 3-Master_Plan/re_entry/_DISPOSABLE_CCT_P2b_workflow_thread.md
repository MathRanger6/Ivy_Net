# DISPOSABLE — CCT P2b workflow thread (living log)

**Purpose:** One place for **where we are** when Alex drive-bys pull you off the campaign plan.  
**Companion (science):** [`_DISPOSABLE_PD25_Alex_board_for_dummies.md`](_DISPOSABLE_PD25_Alex_board_for_dummies.md) — read that for *what* P2b is; **this file** is *what to do now*.  
**Protocol:** Document-first (Option A). COMPASS updates **YOU ARE HERE** after each substantive turn. Say **anchor** in chat if lost — I'll paste this block.  
**Delete when:** P2b binning settled + Alex briefed + campaign plan triage merged.

---

## YOU ARE HERE (2026-08-24, evening)

| Step | Task | Status |
|------|------|--------|
| **A** | Back-of-envelope binning math | ✓ In this doc |
| **B** | P2b sweeps; top-band; F-HERO lock | ✓ Charles deck `slides/Fixed_Ai_Comparisons/` |
| **C** | Campaign plan triage | ✓ Below |
| **D** | **θ knee sweep** — overlay lower Â bands on F-HERO | **Next** — run `cct_p2b_ai_band_overlay.py` |
| **E** | Season-specific `Y_draft` (vs ever-draft) | **Active (#4)** — preservation protocol §J |

**F-HERO (locked candidate for Alex board):** `mg10 min20 11_21` · +DFT · PPM · **top 7%** Â · piecewise **4+7** T̂_j bins.  
Plot: `CCT_draft_rate_fixedAi_Tj_knbins_min20_ppm_top7_dft_low4_high7.png` (330 drafts in band).  
Deck exports: [`HEROs_and_PASSes/slides/Fixed_Ai_Comparisons/`](HEROs_and_PASSes/slides/Fixed_Ai_Comparisons/) (14 slides).  
**Canonical Y label:** ever-draft (no suffix on filenames). Season-`Y` = experiment only (§J).

**Drive-by rule:** Alex questions **do not automatically supersede** the campaign plan. Fast honest answer + optional **one** replot → return here unless Alex reprioritizes.

**One sentence for Alex (binning):** “We did the power half of the back-of-envelope — 20 tail bins gave ~10 people per bin; we’re re-running with **10 tail bins** (~20 per bin) so the downturn isn’t over-fit noise.”

**One sentence for Alex (F-HERO):** “Hold the **top 7%** of player talent at **min 20** minutes; draft rate is flat then falls as **team talent** rises — that’s the congestion read.”

---

## A — Back-of-envelope math (minimal)

**Question:** How many T̂_j bins can this band support?

**Inputs (primary run):**

- $N_{\mathrm{band}} = 392$ player-seasons (PPM $z \in [2,3]$, +DFT, min10)
- Split at within-band **median** $\hat{T}_j$ → $n_{\mathrm{above}} \approx N_{\mathrm{band}}/2 \approx 196$

**Power (exploratory bar level):**

$$\bar{n}_{\mathrm{tail}} = \frac{n_{\mathrm{above}}}{B_{\mathrm{tail}}}$$

Target $\bar{n}_{\mathrm{tail}} \gtrsim 15$–20 →

$$B_{\mathrm{tail}} \lesssim \frac{196}{20} \approx 10$$

**Choice:**

$$B_{\mathrm{left}} = 4,\quad B_{\mathrm{tail}} = 10 \quad\Rightarrow\quad 14 \text{ bins total}$$

(v0 was $4+20=24$ → $\bar{n}_{\mathrm{tail}} \approx 196/20 \approx 10$ — too thin for bar-to-bar reads.)

**Read rule (not per-bar hypothesis tests):**

- **Plateau rate** $\bar{p}_{\mathrm{plat}}$ = mean draft rate over coarse / mid bins (pool if needed)
- **Tail rate** $\bar{p}_{\mathrm{tail}}$ = mean over **last 2–3** fine bins (pool)
- **Downturn** if $\bar{p}_{\mathrm{tail}} < \bar{p}_{\mathrm{plat}}$ (directional; Wilson CI on pooled groups if reporting)

**Not done yet:** Model cutpoint from $K/N$, $\theta$, $\gamma$ → split on $\hat{T}_j$ (formal memo). v0 uses **median split** as zoom line.

**$n \geq 30$ flag:** Warning for **adjacent-bar** comparison only — not a requirement that every elite bin hit 30. Elite $\hat{T}_j$ is sparse by geography, not because $K$ is tiny inside this band.

**Alex’s “~20 bins”:** Meant **uniform** binning on $X$ to prune bad grids — **not** “20 fine bins after piecewise.” Piecewise spends bins where congestion lives; **10 tail bins ≈ adequate resolution**.

---

## B — Re-run spec

```bash
# Single cell only (recommended when you specify band + minutes):
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --dft --p2b-single \
  --ai-lo 2.0 --ai-hi 3.0 --min-minutes 20 \
  --tj-n-low 4 --tj-n-high 10
# → …/CCT_draft_rate_fixedAi_Tj_knbins_min20_ppm_z2_3_dft.png

# Default bundle (no --p2b-single): primary z[2,3] at YOUR min-minutes + sensitivity z[1.5,2] min20
```

**Inspect:** downturn still visible? fewer red thin cells? plateau vs tail box sensible?

**Adjust knobs if needed:** `--tj-n-high 8` (more power) or `12` (more resolution); `--tj-tail-split-q 0.75` (tail-only zoom).

---

## C — Campaign plan triage (2026-08-24)

### OBE / moot (do not resume unless Alex re-opens)

| Item | Why OBE |
|------|---------|
| **P2 heatmap** | Parked; Alex PD25 = P2b, not smearing diagnosis |
| **P2 before P2b sequencing** | P2b shipped; order obsolete |
| **16-ventile T̂_j panel** | Wrong binning; superseded by P2b |
| **Hunting bin-16 marginal hero dip** | Explicit do-not-do |
| **OBPM as canonical** | Appendix only — settled |
| **Act II “green-light SCOUT for P1”** | Done |
| **Formal K/N → $\theta$ cutpoint memo** | Open but **not blocking** Alex drive-by answer |

### Active now (task at hand)

| Item | Owner |
|------|-------|
| **P2b bin refinement** (4+10 run, inspect) | Charles + COMPASS/SCOUT |
| **Articulate binning to Alex** | Charles (use §A + one sentence above) |

### After task at hand (campaign plan still true)

| Item | When |
|------|------|
| **Act III** — HAND deck (triptych + P2b + P3 Q4) | Alex: after next week |
| **Paper outline / framing** | Same window |
| **§8 Alex read-aloud paragraph** | HAND assembly |
| **K/N formal memo** | Before claiming model-aligned knee |
| **P4 interval overlap** | Optional HAND enrich |
| **PD24 BPM hero rerun** | Appendix when bandwidth |

### Drive-by vs supersede (how to tell)

| Alex says… | Treat as… |
|------------|-----------|
| “Did we do the back-of-envelope?” / “Is 20 bins too many?” | **Clarify + maybe one replot** — does **not** cancel Act III or triptych deck |
| “Stop everything and rewrite the paper” | **Supersedes** — update campaign plan Status |
| “Looks good, let's frame the story” | **Confirms** Act III next — park binning after B satisfied |

---

## D — Alex deck talking points (`slides/Fixed_Ai_Comparisons/`)

**Arc:** sensitivity (knobs) → mechanism (min0) → improve candidate → simplify (%) → **F-HERO** → θ knee sweep → labeling appendix.

### Slides 1–2 — minX at fixed z [2,3]

- Anchor **min20, z [2,3]** (blue border); sweep min0 / min5 / min25 / min30.
- **Talk:** min20 is the sweet spot — enough drafts, stable bins; min0/min5 sparse/noisy; min25≈min20.
- **Do not say:** “min0 opens the aperture so we get more draftees in the band.” It **doesn’t** — z [2,3] is recomputed on a noisier pool (see §E).

### Slides 3–5 — top % vs z (min fixed)

- Top **20%** dilutes; top **5%** is clean but thin; percentages easier for Alex than z cuts.
- **Talk:** “Top 7% of the +DFT panel at min20” ≈ widening z band without reopening min0.

### Slide 6 — min0 vs min20 paradox

- **Talk:** “Same label z [2,3], **different players** — min0 rebuilds the z curve with low-minute noise; real stars’ z compress; band fills with non-draftees.”
- Numbers: 52 vs 143 drafts; band median minutes ~37 vs ~962.

### Slides 7–8 — widen Â + compress tail bins

- z [1.5,3] + **4+7** bins → more power per tail bin, same downturn story. Right panel = **CANDIDATE** before F-HERO.

### Slide 9–10 — F-HERO

- **Lock:** min20 · **top 7%** · +DFT · 4+7 · ~330 drafts.
- **Talk:** “Elite seventh of the panel; flat draft rate at moderate T̂_j, then downturn when team is **too loaded**.”
- **Next (Alex ask):** Does the **T̂_j knee move left or right** on **lower, disjoint** Â intervals — e.g. $(85\%,93\%]$, $(75\%,85\%]$ — **not** by widening F-HERO cumulatively?

### Slides 11–13 — ever-draft `Y=1` at min0 (appendix)

- Zero-minute spike among “drafted” rows = **ever-draft flag**, not “drafted this season.”
- **Talk:** “F-HERO uses min20 so this doesn’t drive the board; it’s an **outcome-label** honesty slide.”

### Slide 14 — +DFT teams vs drafted-only Â (min20)

- +DFT: Â ~ N(0,1); drafted-only: Â mean ~0.86 on +DFT panel (ever-draft `Y=1`).
- **Fixed (2026-08-25):** right-hand **T̂_j must repeat +DFT roster mean** — not mean among drafted players only.
- **Â on right:** ever-draft `Y=1` with **full-panel** within-season PPM z (mean ≈ **1.08**). Left Â uses **+DFT** pool (mean ≈ 0.09). Different z-reference pools — intentional.
- **Plot:** `BDP_Ai_Tj_mg10_min20_11_21_ppm_slide14_compare.png` (four panels) or `--drafted-only --panel-tj-dft` for 1×2 pair.
- **Talk:** “Who draftees **are** (Â) vs **ecosystem** team loading (shared T̂_j).”

---

## E — min0 vs min20 (mechanism, for slides)

`min_minutes` runs **before** within-season PPM z-scoring, not as a post-filter on the same z’s.

1. At **min0**, low-minute rows enter the z reference pool → inflates SD, small-sample high-PPM noise lands in z [2,3].
2. True high-minute stars’ z **compress** — many miss [2,3] at min0, qualify at min20.
3. Result: **fewer** draftees in the band at min0 despite “wider” minutes gate.

Diagnostic (+DFT, z [2,3]): only **38** drafted PS overlap both bands; **105** enter at min20 only.

---

## F — Line plot overlay + draft-mass ECDF (band picking)

**Overlay:** `sports/scripts/cct_p2b_ai_band_overlay.py` — percentile Â slices, shared T̂_j x-axis.

```bash
python sports/scripts/cct_p2b_ai_band_overlay.py
python sports/scripts/cct_p2b_ai_band_overlay.py --bands "0:7,7:15,15:25,25:40"
python sports/scripts/cct_p2b_ai_band_overlay.py --suggest-width 8 --min-band-n 120
```

Outputs: `CCT_P2b_ai_band_overlay_lines.png`, `_sweep.csv`, `.json` in `basic_data_plots/`.  
Use sweep CSV to pick band boundaries (`knee_tj_mean`, `band_n`, `downturn_visible`) before final Alex figure.

**Draft-mass ECDF:** `sports/scripts/bdp_ai_draft_mass_ecdf.py` — same +DFT panel as overlay; orange = drafted-only Â; blue = panel pool; red dots = 5% draft-mass quantiles; purple = panel top-% cuts.

```bash
python sports/scripts/bdp_ai_draft_mass_ecdf.py
python sports/scripts/bdp_ai_draft_mass_ecdf.py --draft-mass-step 10
```

Outputs: `BDP_Ai_draft_mass_ecdf_mg10_min20_11_21_dft_ppm.png`, `_cuts.csv`, `.json`.  
**Draft-mass 30% tiers (Slide 15 read)** — three overlay lines, bottom 10% of draftees dropped:

```bash
python sports/scripts/cct_p2b_ai_band_overlay.py --bands "0:7.4,7.4:22,22:53.7" --hero-top "0:7.4"
```

| Tier | Panel band | Draft mass | Drafts | knee T̂_j (peak) |
|------|------------|------------|--------|------------------|
| 1 (F-HERO) | top 7.4% | ~30% | 340 | **~0.33** |
| 2 | top 7.4–22% | ~30% | 342 | **~0.59** |
| 3 | top 22–53.7% | ~30% | 338 | **~0.58** |

Red dots on overlay = **visual knee** (rightmost plateau peak); legend `knee≈` matches.

Cuts calibrated from orange ECDF at y=70/40/10% (draft-mass grid), not default purple 7/15/25/40 lines.

---

## G — Can we compute the knee? **Partially — enough for Alex now**

**What we have today** (`knee_summary` in P2b JSON):

- **Plateau rate** = mean draft rate over coarse (first `n_low`) bins.
- **Tail rate** = mean over **last 3** bins.
- **Downturn visible** = tail (or last bin) < plateau.
- Bin CSV has `T_j_mean`, `edge_lo`, `edge_hi` per bin.

**What we do *not* have:** a single scalar **θ̂** = “T̂_j value where the curve bends” exported per run, nor K/N-linked cutpoint (formal memo still parked).

**Practical plan for Alex (descriptive geometry first):**

1. Overlay draft-rate vs **T̂_j mean** lines for F-HERO and lower Â bands (same 4+7 recipe, same min20, +DFT).
2. Read off knee **visually**: where rate stops rising / starts falling.
3. If lower **disjoint** Â bands’ downturn sits at **lower T̂_j**, say: *“The knee moves left as we **move the fixed slice down** the Â ladder — consistent with congestion.”*
4. Optional later: automate knee = first bin where rate drops >δ below rolling plateau, or argmax then first decline — **after** overlays look convincing.

**Do not** claim fitted θ or (K/N − θ)/γ alignment until the formal memo.

---

## H — `Y_draft`: ever-draft vs drafted **that season** (plain English)

### What we do now (ever-draft)

Draft lookup gives a set of **athlete IDs** who were ever drafted. Panel merge sets **`Y_draft = 1` on every college season row** for that athlete — freshman, redshirt, zero-minute years included.

### What “season-specific” would mean (locked 2026-08-25)

Lookup says **who** was ever drafted (`athlete_id` + `draft_year`). **`Y_draft = 1` on exactly one row per draftee:** their **last college player-season** in the panel (`max(season)` for that athlete). All earlier seasons: `Y=0`.

**Do not** match `panel.season == draft_year` — many players are drafted a year or more after they leave college (G-League, overseas, etc.). The outcome attaches to **final college season**, not NBA draft calendar.

**Example A — drafted same spring they finish (2019 draft, last season 2019):**

| Season row | Ever-draft (now) | Season-specific |
|------------|------------------|-----------------|
| 2015–16, 0 min | Y=1 | Y=0 |
| 2018–19, starter | Y=1 | Y=1 ← last season |

**Example B — drafted 2019, last college season 2017 (gap years):**

| Season row | Ever-draft (now) | Season-specific |
|------------|------------------|-----------------|
| 2015–16 | Y=1 | Y=0 |
| 2016–17, starter | Y=1 | Y=1 ← last season (draft_year=2019 ignored for row pick) |

### Why Army used ever-draft

Survival / time-to-promotion needs **one risk set per officer** — “ever promoted by year T” with censoring. Same flag on all rows = correct for **time-to-event**.

### Why MBB board may switch later

P2b estimand: **P(drafted | this season’s Â, T̂_j)** — a **cross-section**, not “will this freshman eventually draft?” Ever-draft on a freshman row answers a **different question** and creates artifacts (zero-minute “drafted” rows in slides 11–13).

### Does F-HERO need relabeling first?

**No for this Alex meeting** — min20 + top 7% + +DFT is coherent. Slides 11–14 flag the **future** refactor. When season-`Y` ships: rerun F-HERO grid once, note draft-count delta in this doc.

---

## I — Overlay null result: knee does **not** drift left (2026-08-24)

**Tested:** draft-mass 30% tiers → panel bands `0:7.4`, `7.4:22`, `22:53.7` (min20 · +DFT · 4+7).  
**Alex ask (Slide 10):** on **disjoint lower Â intervals** (not widening F-HERO), does T̂_j knee move left/right?

**What Slide 10 literally says:** (1) θ at $\hat{A}_i \in (93\%,\infty)$; (2) **look at lower intervals** $(85\%,93\%]$, $(75\%,85\%]$, …; (3) see if knee moves. Each band is a **separate fixed slice** — move down the ladder, not expand the elite pool.

**What we ran:** overlay bands **are** disjoint (`top_lo:top_hi` slices). Draft-mass tiers `0:7.4`, `7.4:22`, `22:53.7` recalibrated cutpoints but same logic. Earlier run `0:7,7:15,15:25,25:40` matches Slide 10 prose more literally.

**Answer:** **No knee migration** in descriptive geometry — knees ~0.71–0.73 on all disjoint tiers. **Levels** fall as Â slice moves down.

### Say to Alex (honest, not apologetic)

> “We overlaid **disjoint** Â slices on a shared T̂_j axis — F-HERO plus lower intervals — not one widening elite band. The downturn location doesn’t migrate; knees sit at roughly the same team-loading. What changes is **curve height**: lower Â slices convert at much lower draft rates. Did you expect the **threshold** to shift with Â, or is stable knee + tier-dependent level the story?”

### Do **not** treat as failure

Null on knee migration is a **result**. F-HERO + ECDF + overlay = enough for one board conversation.

### Next steps (priority)

| Priority | Action | Why |
|----------|--------|-----|
| **Now** | Deck: F-HERO bar + ECDF (Slide 15) + 3-line overlay | Shows question asked + answer |
| **Now** | Ask Alex to interpret stable knee vs level shift | His call whether to pursue θ formalism |
| **Later** | Season-specific `Y_draft` | Cross-section estimand; not blocking |
| **Later** | Formal θ̂ / (K/N − θ) memo | Parked until Alex cares |
| **Skip for now** | More band grids / automated knee | Diminishing returns unless Alex redirects |

---

- Charles built `slides/Fixed_Ai_Comparisons/` (14 slides); locked **F-HERO** = min20 · top 7% · 4+7 · +DFT.
- §D–H added: Alex talking points, line-overlay plan, knee scope, Y_draft plain English.
- Next: θ sweep via **line overlays** on shared T̂_j axis; formal θ̂/K/N memo still parked.

### 2026-08-24 — Charles: lost; wants A/B/C workflow

- Chose **document-first (A)** for thread tracking.
- This file created. Back-of-envelope math compressed to §A.
- Drive-by protocol: answer Alex first, then return to YOU ARE HERE.

### 2026-08-24 — Color bug fixed; all knbins artifacts deleted

**Bug:** Orange/blue used top-25% of T̂_j **range**, not piecewise split → with 5+10 bins, orange started at bin 4 instead of bin 6.

**Fix:** `high_tj_tail` = fine region (bin index ≥ `n_low`). Legend: "Coarse" / "Fine tail". Plateau box uses first `n_low` bins.

**Deleted:** all `CCT_draft_rate_fixedAi_Tj_knbins*` — **you rerun** after pulling latest script.

**Top band (alternative to z slice):** `--ai-top-pct 10` keeps pooled top 10% of perf z in panel (JSON records `ai_perf_cut`).

```bash
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --dft --p2b-single \
  --min-minutes 20 --ai-top-pct 10 \
  --tj-n-low 5 --tj-n-high 10
# → …_min20_ppm_top10_dft_low5_high10.png
```

Z-band example:

---

## PARKED — viable / draftee counts on team (Charles 2026-08-25)

**Idea (not built):** distributions of (a) # viable players per team-season, (b) # drafted players per team-season; among **drafted PS only** — # fellow viable teammates and # fellow draftees. “Viable” TBD (moving target; may tie to Â band or min minutes).

**When:** after Alex meeting / season-`Y` panel decision.

---

## J — Season-`Y` experiment: **don't clobber ever-draft** (2026-08-25)

**Goal:** cross-section estimand — `Y=1` only on each draftee’s **last college player-season** (§H). **Ever-draft stays canonical** for Alex deck until we explicitly switch.

### Layer 1 — Defaults unchanged

| What | Ever-draft (canonical) | Season-`Y` (experiment) |
|------|------------------------|-------------------------|
| `panel_rebuild.py` | unchanged default | **do not change rebuild yet** |
| Script default | no flag → ever | `--y-draft-mode season` opt-in |
| `CctSpec` / cache key | `y_draft_mode="ever"` | include mode in cache key |

**Phase 1 (first):** post-hoc relabel helper after a **pre-min / pre-games** panel load (`min_minutes=0`, `min_team_season_games=0`); then apply analysis filters. No rewrite of `player_season_panel_530.csv`.

**Phase 2 (only if Alex cares):** optional `PipelineConfig.y_draft_mode` in rebuild + separate export CSV.

### Layer 2 — Output isolation (hard rule)

- **Ever-draft outputs:** keep current paths under `basic_data_plots/` (no suffix).
- **Season-`Y` outputs:** subfolder `basic_data_plots/season_y_experiment/` **and** filename suffix `_season_y`.
- **Safety assert:** scripts refuse to write season-`Y` PNG/JSON unless path contains `season_y`.
- **JSON provenance:** every artifact records `"y_draft_mode": "ever"|"season"`, `n_drafts`, season↔draft_year rule version.
- **Deck:** do **not** touch `slides/Fixed_Ai_Comparisons/`; new deck folder only if we promote the experiment.

### Layer 3 — Git / snapshot

- Work on branch `experiment/season-y-draft` (or commit ever-draft state on current branch before code changes).
- Optional one-time copy: `basic_data_plots/_canonical_ever_y_2026-08-25/` — tarball of F-HERO + overlay + ECDF + Slide 14 PNGs/JSONs.

### Layer 4 — First smoke test (minimal)

One rerun only before any sweep:

```bash
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --dft --p2b-single \
  --min-minutes 20 --ai-top-pct 7 --tj-n-low 4 --tj-n-high 7 \
  --y-draft-mode season
# → basic_data_plots/season_y_experiment/CCT_..._season_y.png
```

Compare to canonical F-HERO: band n, draft count (~330 ever vs ? season), knee location. Log delta in this section. **Stop if nonsense** — delete `season_y_experiment/` only; ever-draft untouched.

**Smoke (2026-08-25, mg10 · min20 · top 7% · 4+7 · +DFT · season-Y):**

| | Ever-draft (canonical) | Season-Y (`season_y_experiment/`) |
|--|------------------------|-----------------------------------|
| `band_n` | 1,237 PS | 1,154 PS |
| Drafts in band | 330 | 216 |
| Plateau rate | ~20.7% | ~15.9% |
| Tail rate | ~19.7% | ~12.8% |
| Alarms | — | 7 draftees lost to min20 (521→514 labeled) |

PNG: `…/CCT_draft_rate_fixedAi_Tj_knbins_min20_ppm_top7_dft_low4_high7_season_y.png`

### Last-season assignment rule (locked in helper)

1. **Draftee set:** `athlete_id` present in `athlete_id_draft_lookup.csv` (has `draft_year`; used for membership only).
2. **Panel for labeling — pre-minutes, pre-min-games (hard rule, 2026-08-25):** build (or load) the panel with **`min_minutes=0`** and **`min_team_season_games=0`**. Last season `s* = max(season)` is computed on **this** frame only — never on a min20 / mg10-trimmed panel.
3. **Exactly one Y=1 row per draftee:** row with `(athlete_id, season=s*)`; transfer tie → **max minutes** (log ties).
4. **All other rows:** `Y_draft = 0`.
5. **Then analysis filters:** apply spec `min_minutes`, `min_team_season_games`, +DFT, Â band, etc. **after** relabel. Zero-minute last seasons are expected to vanish under min20; **alarms** fire when min-games / min-minutes / +DFT drop a labeled draftee (stdout `ALARM · …`, `UserWarning`, JSON `y_draft_survival_audit`).

**Alarms (2026-08-25):** `sports/sports_pipeline/y_draft_mode.py` — after each filter step, compare draftee `athlete_id` sets with `Y=1` before vs after. Log `n_draftees_lost` + sample IDs. Helper: `audit_y1_survival()`, `emit_survival_summary()`.

`draft_year` is **not** used to pick the row — only to know they were eventually drafted.

**Pipeline order (season-`Y` mode):**

```
build panel (min_minutes=0, min_team_season_games=0, season window)
  → perf / LOO / z on full panel
  → apply_y_draft_last_season()
  → drop team-seasons with games ≤ min_team_season_games (post-hoc)
  → filter_panel min_minutes (+ +DFT / bands as today)
```

**Helper sketch:** `apply_y_draft_last_season(panel, lookup)` · provenance `"y_draft_rule": "last_college_season_v1_premin"`.

### Not the same knob

`draftee_restriction=season` in `PipelineConfig` = **+DFT team filter** (team-seasons with ≥1 draftee that year). **Different** from season-specific **Y labeling**. Season-`Y` may eventually pair with season-level +DFT; wire separately.

---

*COMPASS · 2026-08-24 · living log*
