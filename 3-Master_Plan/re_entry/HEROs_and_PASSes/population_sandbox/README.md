# Population sandbox — HERO + F-HERO paired sweeps

**Purpose:** Explore population knobs without clobbering canonical `pass_a/` or `basic_data_plots/` artifacts.

**Living plan:** [`../../_DISPOSABLE_Alex_hero_population_thread.md`](../../_DISPOSABLE_Alex_hero_population_thread.md)  
**CLI cheat sheet:** [`CLI_CHEAT_SHEET.md`](CLI_CHEAT_SHEET.md) · raw `--help` dump: `cli_help_dump.txt` (regen: `./scripts/dump_hero_cli_help.sh`)

---

## Layout

```text
population_sandbox/
  README.md          ← this file
  hero/              ← pass_a_empirical_bundle.py outputs
  fhero/             ← pass_a_congestion_conditional.py F-HERO outputs
```

Each PNG has a matching `*_provenance.json` (HERO) or embedded `provenance` block (F-HERO JSON). **Full spec is on the plot footer.**

---

## Filename convention (always in name)

| Token | Meaning |
|-------|---------|
| `q16` / `ew16` | HERO poolq_loo binning (quantile / equal-width) |
| `pw4p7` / `ew24` | F-HERO T̂_j binning (piecewise 4+7 / equal-width) |
| `allt` / `dft` | Full panel vs +DFT |
| `min20` | Minutes floor |
| `mg10` | Min team-season games (box QC) |
| `11_21` / `13_21` | Season window |
| `top7` | F-HERO Â band (top 7%) |

**Example HERO:** `HERO_q16_allt_min20_mg10_11_21.png`  
**Example F-HERO:** `FHERO_pw4p7_dft_min20_mg10_top7_ppm_11_21.png`

---

## Y labeling vs panel rows (orthogonal — Aug 25)

Two **independent** CLI flags. Do not conflate.

| Flag | Values | Meaning |
|------|--------|---------|
| **`--y-draft-mode`** | `ever` (default) · `season` | **How Y is assigned.** `season`: draftees get `Y=1` on **last college PS only**; earlier PS rows stay with `Y=0`. |
| **`--panel-rows`** | `all-ps` (default) · `last-ps` | **Which rows enter the plot.** `last-ps`: one row per athlete at max(season) — cross-section. |

| panel-rows | y-draft-mode | Use case |
|------------|--------------|----------|
| `all-ps` | `ever` | **Canonical HERO** (deck) |
| `all-ps` | `season` | Full panel; season-Y label only (Charles #2) |
| `last-ps` | `ever` | Final-season cross-section; ever-draft |
| `last-ps` | `season` | Final-season cross-section; season-Y (old implicit default) |

**Retired:** `--last-season-only` / `--all-seasons` → use `--panel-rows`. Hidden aliases still work with deprecation warning.

**Example — Charles #2 (full panel, season-Y label):**

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --y-draft-mode season \
  --panel-rows all-ps \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero
```

**Example — final-season cross-section only:**

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --y-draft-mode season --panel-rows last-ps \
  --output-root ...
```

Filename slugs: `_season_y` = season-Y labeling; `_last_ps` = last-ps panel (both can appear).

---

## LOO vs team `poolq` (roster-pressure x-axis)

| `--roster-x` | Meaning | Deck? |
|--------------|---------|-------|
| **`poolq_loo`** (default) | LOO teammate mean — self excluded | **Canonical HERO** |
| **`poolq`** | Team-season mean perf z — **includes self** | Sensitivity / compare to LOO |

Not F-HERO (no Â band, no +DFT requirement, full-panel bins).

```bash
# LOO (canonical)
python sports/scripts/pass_a_empirical_bundle.py \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero

# Team poolq (includes star in team mean)
python sports/scripts/pass_a_empirical_bundle.py \
  --roster-x poolq \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero
```

Output: `HERO_poolq_q16_allt_min20_mg10_11_21.png` vs `HERO_q16_…` for LOO.

---

| # | Change | HERO | F-HERO |
|---|--------|------|--------|
| **0** | Baseline lock | ✓ `hero/` + `fhero/` 11_21 | ✓ |
| **1** | EW vs QTL | ✓ `HERO_ew20_…` in `hero/` (display) | (F-HERO already piecewise) |
| **2** | 13–21 window | **→ NEXT** — add season flags below | **→ NEXT** |
| **3** | ALLT vs DFT | omit `--dft` / add `--dft` | omit `--dft` / add `--dft` |
| **4** | Division | blocked — SCOUT | SCOUT |

---

## ⚠️ HERO mg=0 vs mg=10 vs F-HERO — read before Alex (Aug 25)

**Three different objects. Do not merge memories.**

| Plot | x-axis | mg | Downturn at elite? | Defensible? |
|------|--------|-----|-------------------|-------------|
| **HERO mg=10** q16 | `poolq_loo` | 10 | **No** — flat elite (~3.2%) | **Canonical POST-QC** (`n≈46k`, β₂>0) |
| **HERO mg=0** q16 | `poolq_loo` | 0 | **Yes** — bin 15 dip ~1.2% | **Sensitivity only** — fragment/cameo replay (`n≈62k`, β₂<0) |
| **F-HERO** pw4p7 | `T̂_j` (team mean) | 10 | **Yes** (Alex Slide 10) | Different estimand; +DFT, top 7% Â |

**Charles memory fix:** Box QC + **mg=10 did not restore** quantile HERO inverted-U — it **removed** it. The poolq_loo downturn replays on **mg=0** (pre-QC). **F-HERO** downturn is real but on **T̂_j**, not LOO.

Source: [`../PD20_22_campaign_big_picture.md`](../PD20_22_campaign_big_picture.md) § hero POST-QC.

**For Alex deck:** pair **HERO mg=10** (middle rise, flat tail) with **F-HERO mg=10** (T̂_j downturn). Mention mg=0 only as “what pollution looked like.”

---

## Rerun sandbox (Charles — wipe `hero/` OK)

Clear `population_sandbox/hero/*` then run **both** canonical + sensitivity:

```bash
# 1 — Canonical HERO (mg=10 default)
python sports/scripts/pass_a_empirical_bundle.py \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero

# 2 — mg=0 sensitivity (do NOT lock as population)
python sports/scripts/pass_a_empirical_bundle.py \
  --min-team-season-games 0 \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero

# 3 — ventile diff table
python sports/scripts/compare_hero_mg_sandbox.py
```

(`compare_hero_mg_sandbox.py` re-runs mg=0 if missing; skip step 2 if you already have mg0 files.)

F-HERO in `fhero/` — **leave as-is** unless re-running F-HERO sweep.

### F-HERO optional rerun

```bash
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --p2b-single --dft \
  --min-minutes 20 --ai-top-pct 7 --tj-n-low 4 --tj-n-high 7 \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/fhero
```

### EW display (HERO only)

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --poolq-binning equal_width \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/hero
```

### 13–21 sweep (both)

Add `--season-min 2013 --season-max 2021` to either command.

---

## LOCKED POPULATION

*(Fill when HERO + F-HERO agree on one row in the matrix.)*

| Field | Value |
|-------|-------|
| Seasons | 2011–2021 |
| HERO | q16 · min20 · **mg10** · ALLT · poolq_loo |
| F-HERO | pw4p7 · min20 · mg10 · +DFT · top7% Â · T̂_j |
| Y mode | ever |

**Then:** SI descriptive slides (distributions on locked sample) — see disposable thread §I.

---

*COMPASS · Aug 2026*
