# DISPOSABLE — Alex hero / F-HERO population thread (2026-08-25)

**Purpose:** One place after Alex meeting — population lock, plot provenance, CLI sweep order.  
**Companion:** [`_DISPOSABLE_CCT_P2b_workflow_thread.md`](_DISPOSABLE_CCT_P2b_workflow_thread.md) (band overlay / knees).  
**Say `anchor`** in chat to paste **YOU ARE HERE**.

---

## YOU ARE HERE

| Step | Task | Status |
|------|------|--------|
| **0** | Alex meeting captured (this doc) | ✓ |
| **1** | **Plot provenance strip** on HERO + F-HERO | ✓ code + sandbox |
| **2** | Sandbox **HERO baseline** (q16 mg10 + ew20 + mg0 audit) | ✓ Charles (Aug 25) |
| **3** | Lock **ever-draft** for Alex sweep | ✓ default (no season-Y in sandbox) |
| **4** | Sweep **QTL vs EW** (display only) | ✓ HERO ew20 side note in sandbox; q16 = primary |
| **5** | Sweep **2013–2021** vs 2011–2021 (HERO + F-HERO pair) | **→ NEXT** |
| **6** | **Div I / II** filter | **SCOUT active** (Charles, Aug 25) |
| **7** | Sweep **ALLT vs DFT** (Alex: DFT ok for distributions, suspect for hero) | Pending |

**Canonical deck pair (locked for now):** HERO `q16 · mg10 · min20 · 11_21 · ALLT · poolq_loo` + F-HERO `pw4p7 · mg10 · min20 · 11_21 · +DFT · top7% Â · T̂_j`.  
**Sandbox artifacts:** [`population_sandbox/hero/`](HEROs_and_PASSes/population_sandbox/hero/) · [`population_sandbox/fhero/`](HEROs_and_PASSes/population_sandbox/fhero/).

**Side notes (not locked population):** mg=0 audit only; ew20 modest elite dip on LOO (display); full-panel **T̂_j** (`pool_mean`) = monotone rise, no downturn — see `pass_a/sensitivity/PASS_A_sensitivity_poolmean_mg10_2011_2021_b16q_w0199.png` (≠ F-HERO).

**Prime directive (Alex + Charles):** Before changing any knob, ask *why would I change x→y, and is that change worth looking at?*

---

## A — Two plots (do not conflate)

| Name | Script | X-axis | Y-axis | Deck ref |
|------|--------|--------|--------|----------|
| **HERO** | `pass_a_empirical_bundle.py` | **`poolq_loo`** (LOO teammate perf) | mean `Y_draft` · 16 bins | OLD_vs_NEW slides 2–3 top-right |
| **F-HERO** | `pass_a_congestion_conditional.py` `--plot fixed_ai_tj_knbins` | **`T_j_hat`** (team mean perf, **incl. self**) | mean `Y_draft` · piecewise T̂_j bins | `Fixed_Ai_Comparisons` Slide 10 |

**Not the same axis.** HERO = LOO pond. F-HERO = team mean T̂_j.

---

## A2 — mg confusion lock (Aug 25 — do not re-litigate)

| Object | mg | Elite downturn? | Lock for Alex? |
|--------|-----|-----------------|----------------|
| HERO `poolq_loo` q16 | **10** | **No** (flat ~3.2%) | **Yes** — canonical POST-QC |
| HERO `poolq_loo` q16 | **0** | **Yes** (~1.2% bin 15) | **No** — pre-QC / fragment replay only |
| F-HERO `T̂_j` pw4p7 | **10** | **Yes** | **Yes** — Slide 10 (different x) |

**Memory correction:** After PD22 box QC, **mg=10 removed** quantile HERO inverted-U; it did **not** produce it. F-HERO downturn is a **separate plot** (T̂_j, +DFT, top 7% Â).

Evidence: mg0 `n=62,180` β₂=−0.025 vs mg10 `n=46,306` β₂=+0.0064. See [`population_sandbox/README.md`](HEROs_and_PASSes/population_sandbox/README.md).

**Alex one-liner:** *“LOO hero: middle rise, flat elite on cleaned panel. Team-mean F-HERO at fixed Â: downturn on T̂_j — different object.”*

---

## B — Alex meeting notes (consensus)

1. **Band overlay / lower-band knees moving right** — Alex’s first read: **Wilson intervals huge** on those knees → low n / thin bins; don’t over-interpret point estimates.
2. **LOO vs mean** — HERO is already `poolq_loo`; F-HERO is T̂_j (team mean). Label explicitly on figures.
3. **Binning** — pick QTL vs EW with justification; can run both for display; Alex ok either way if labeled.
4. **+DFT** — good for **distributions**; may **bias hero** curves → report **ALLT vs DFT** side by side for hero/F-HERO, not DFT-only as default.
5. **Division I / II** — Charles: consider restricting; check how many D-II draftees; may drop D-II too. **Panel has no `division` column today** — needs lookup or external list.
6. **Season window** — Alex **asked about** 2011–2012 / 2013–2021 (did **not** suggest switching). **2013–2021 = sweep only**, not primary until paired run says otherwise. See §B2.
7. **Season-Y (`--y-draft-mode season`)** — **park for Alex sweep**; orthogonal to **`--panel-rows`** (see sandbox README § Y vs panel). Default sweep = **ever + all-ps**.
8. **Provenance on plot** — all switches visible on figure; filenames stay short.

---

## B2 — 2013–2021: primary or not?

**Code already knows both windows** (`pd20_22_campaign_window.py`: full 2011–2021; primary 2013–2021 tagged `_13_21` for AUTO decks).

### What “funky” refers to (honest sourcing)

| Claim | Source | Detail |
|-------|--------|--------|
| “2011–2012 funky” | **Alex meeting (Charles memory, Aug 25)** | Not a formal 2011–2012-only audit in repo |
| **2013→2014 ESPN break** | **Documented (PD22, Aug 17)** | Raw player-season count +83% (5,801→10,633); games only +3%; ESPN listed **deeper box scores** (~+2 rows/game/team). Breaks **ppm0lt20** ρ panels; **min-20 hero** barely moves (+2.7% player-seasons 2013→2014) |
| Early scrape / fragments | BOX QC memos | Dash placeholders, D-II one-game cameos — worse in raw early years but **QC + mg10** already scrubs most |

### Should 2013–2021 be primary?

| For | Against |
|-----|---------|
| Alex asked (exploratory, not a recommendation) | All locked hero decks / `alex_side_by_side_v0` use **2011–2021** |
| Avoids pre/post **2014 box-depth** regime mix in longitudinal work | HERO at **min20 + QC** is **stable** across 2013→2014 |
| Cleaner ρ / H_sort story if you keep ppm0 panels | Dropping 2011–2012 loses 2 seasons of draft rows (~small at hero n) |
| Already wired as `PRIMARY_SEASON_MIN` in campaign window | Need **paired 11_21 vs 13_21** hero + F-HERO before locking |

**COMPASS read:** **13–21 = sweep only** (Alex asked; did not suggest). Default stays **11–21** until paired HERO+F-HERO shows material shape change. Sweep #3 in §E.

---

## C — Plot provenance strip (target)

Footer or subtitle block (8–10 pt), e.g.:

```
HERO · poolq_loo (LOO) · bins=QTL16 · PPM z · 2011–2021 · min0 mg10 · ALLT · Y=ever · winsor 1–99%
```

```
F-HERO · T̂_j (team mean, incl. self) · piecewise 4+7 · top7% Â · +DFT · min20 · 2011–2021 · Y=ever
```

**Always write matching JSON** with same keys (already partial on F-HERO / season-Y).

---

## D — Filename policy (Charles 2026-08-25)

**Always in filename** (even when = default — Charles can't remember defaults):

- Plot family (`HERO` / `CCT_FHERO`)
- **Binning + count:** `q16` / `ew16` / F-HERO `pw4p7` (piecewise 4+7)
- Seasons (`11_21` / `13_21`)
- Population (`allt` / `dft` / later `div1`)
- `min{N}` · `mg{N}`

**Plot footer + JSON only:** Y mode, `last_ps`, winsor, perf metric spelled out, axis (LOO vs T̂_j), n/drafts.

**Locked defaults (reference):** HERO `q16` quantile · min20 · mg10 · winsor 1–99% · 2011–2021 · ever · ALLT · ppm.

---

## E — CLI sweep order (Charles runs)

**Defaults for sweep:** `--y-draft-mode ever` · no season-Y · provenance after step 1.

| # | Change | HERO command sketch | F-HERO command sketch |
|---|--------|---------------------|------------------------|
| 1 | **Baseline lock** | `pass_a_empirical_bundle.py` (locked or explicit min20 mg10) | `pass_a_congestion_conditional.py --plot fixed_ai_tj_knbins --dft --p2b-single --min-minutes 20 --ai-top-pct 7 --tj-n-low 4 --tj-n-high 7` |
| 2 | **EW vs QTL** | add `--poolq-binning equal_width` (second PNG) | F-HERO binning already piecewise; note in doc |
| 3 | **13–21** | `--season-min 2013 --season-max 2021` | same season flags |
| 4 | **ALLT vs DFT** | omit vs `--dft` | omit `--dft` vs `--dft` |
| 5 | **Div filter** | blocked until division map exists | same |

**Season-Y experiment folder** (`pass_a/season_y_experiment/`) — do not overwrite canonical Alex sweep artifacts.

---

## F — Division (SCOUT active)

**Owner:** SCOUT thread (Aug 25) — Charles delegated; not blocked on COMPASS/this thread.

**Prior repo context (pre-SCOUT):** June 2026 Div-I thread; SCOUT BOX QC memos. Panel has **no `division` column** today; prior quant ~0 D-II/D-III draftees in matched lookup.

**When SCOUT lands:** wire `--div1` / `--div12` (or equivalent) → sweep #5 in §E. Until then, skip div rows in sandbox matrix.

---

## H — Population sandbox (live)

**Root:** `3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/` — see [`README.md`](HEROs_and_PASSes/population_sandbox/README.md).

```text
population_sandbox/
  README.md              ← sweep matrix + rerun commands
  hero/                  ← pass_a_empirical_bundle.py (--output-root)
  fhero/                 ← pass_a_congestion_conditional.py (--out-dir)
```

**In sandbox (Aug 25):** `HERO_q16_allt_min20_mg10_11_21.png` (canonical), `HERO_ew20_…`, `HERO_q16_…_mg0_…` (audit), `FHERO_pw4p7_…_11_21.png`.

---

## I — Parked after population lock (Charles: don't forget)

**SI descriptive slides** — distributions (ability, poolq_loo, T̂_j, minutes, draft rate by subgroup, etc.) on the **locked** population. Not Alex-deck blocking; paper SI pass.

---

## G — Parked (not Alex-blocking)

- Season-Y hero (`y-draft-mode season`, `last_ps`) — built; use when estimand discussion matures.
- Overlay knee automation / formal θ̂.
- [`_DISPOSABLE_CCT_P2b_workflow_thread.md`](_DISPOSABLE_CCT_P2b_workflow_thread.md) §I null knee migration.

---

## Thread log

### 2026-08-25 — Y vs panel-rows CLI split (Charles)

- **Problem:** `--y-draft-mode season` implicitly defaulted to `last_ps`, conflating season-Y **labeling** with final-season **cross-section**.
- **Fix:** orthogonal flags — `--y-draft-mode {ever,season}` + `--panel-rows {all-ps,last-ps}` (default `all-ps`).
- Charles #2 = `--y-draft-mode season --panel-rows all-ps`. Cross-section = `--panel-rows last-ps`.
- Retired `--last-season-only` / `--all-seasons` (hidden aliases + deprecation warning).

### 2026-08-25 — T̂_j vs LOO on full panel (Charles question)

- **`pass_a_empirical_bundle.py`** bins LOO only; no T̂_j switch in sandbox runner.
- **Full-panel T̂_j analog:** `pool_mean` in `pass_a_hero_sensitivity_plots.py` — same n=46,306, q16 mg10 11–21.
- **Shape:** monotone rise to **5.22%** top bin; LPM β₂=+0.0153 (not concave). **No elite downturn.**
- LOO canonical: flat/wobbly ~3.2% elite; β₂=+0.0064.
- **F-HERO downturn** remains separate object (top 7% Â, +DFT, piecewise T̂_j).

### 2026-08-25 — Sandbox baseline complete (Charles)

- Cleared/reran `population_sandbox/hero/`: q16 mg10 canonical, ew20 display, mg0 audit.
- F-HERO baseline already in `fhero/` (11–21).
- **Next:** paired **13–21** HERO + F-HERO (§E sweep #3).

### 2026-08-25 — mg=0 vs mg=10 HERO (Charles rerun)

- mg=0 reproduces inverted-U on **poolq_loo** (β₂<0, n≈62k) — **sensitivity artifact**, not canonical.
- mg=10 flat elite (β₂>0, n≈46k) — matches locked `pass_a/`. **Not the same plot.**
- F-HERO mg=10 **does** show downturn — on **T̂_j**, not LOO. Memory was cross-wired.
- Sandbox README § mg table; caption boilerplate fixed in `pass_a_empirical_bundle.py`.

### 2026-08-25 — Alex meeting debrief + Charles corrections

- Wilson CIs on lower-band knees; LOO vs T̂_j; QTL vs EW; DFT bias on hero; provenance on plots; variable discipline.
- **13–21:** Alex asked about early seasons; **did not suggest** switching — sweep only.
- **Division:** SCOUT working separately (Charles).

---

*COMPASS · living log · say **anchor** in chat*
