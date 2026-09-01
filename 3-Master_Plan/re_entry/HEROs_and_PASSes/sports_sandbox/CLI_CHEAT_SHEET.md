# HERO / F-HERO — CLI cheat sheet (Aug 2026)

**Regenerate raw `--help` dumps:**

```bash
# From repo root — writes sports_sandbox/cli_help_dump.txt
./scripts/dump_hero_cli_help.sh
```

**Paste into Word:** open `cli_help_dump.txt`, or copy sections from this file.

---

## Three orthogonal knobs (do not conflate)

| Knob | Flag | Default | Meaning |
|------|------|---------|---------|
| **Y labeling** | `--y-draft-mode` | `ever` | `ever`: every PS row of a draftee gets Y=1. `season`: Y=1 **only** on last college PS; earlier PS kept with Y=0. |
| **Panel rows** | `--panel-rows` | `all-ps` | `all-ps`: all player-seasons (fr/so/jr/sr). `last-ps`: one row per athlete (max season). |
| **Roster x-axis** (HERO only) | `--roster-x` | `poolq_loo` | `poolq_loo`: LOO teammate mean (self out). `poolq`: team-season mean (self in). |

### 2×2: Y × panel (HERO + F-HERO)

| | **`panel-rows all-ps`** | **`panel-rows last-ps`** |
|---|---|---|
| **`y-draft-mode ever`** | **Canonical deck HERO** | Final-season cross-section |
| **`y-draft-mode season`** | Full panel; Y=1 last PS only | Final-season + season-Y |

**Retired (hidden):** `--last-season-only` → use `--panel-rows last-ps`. `--all-seasons` → use `--panel-rows all-ps`.

---

## Script 1 — `pass_a_empirical_bundle.py` (HERO)

**What it does:** Left = ability ventiles; right = roster-pressure hero; standalone HERO PNG + CSVs + provenance JSON.

**Usage:**

```text
python sports/scripts/pass_a_empirical_bundle.py [options]
```

| Flag | Choices / default | Notes |
|------|-------------------|--------|
| `--season-min` / `--season-max` | 2011 / 2021 | Season window |
| `--n-bins` | 16 | Hero + ability bin count |
| `--poolq-binning` | `quantile` · `equal_width` | Right panel only |
| `--roster-x` | `poolq_loo` · `poolq` | LOO vs team mean |
| `--min-minutes` | 20 | Playing-time floor |
| `--min-team-season-games` | 10 (`mg10`) | Box QC; use `0` for mg0 audit only |
| `--winsor-lo` / `--winsor-hi` | 0.01 / 0.99 | On roster-x column |
| `--y-draft-mode` | `ever` · `season` | Y labeling |
| `--panel-rows` | `all-ps` · `last-ps` | Which rows |
| `--dft` | off | +DFT team filter |
| `--output-root` | `pass_a/` or sandbox | Sandbox: `…/sports_sandbox/hero` |
| `--output-tag` | optional | Extra filename slug |
| `--side-by-side` | off (default) | Add talent\|roster pair PNG + caption |
| `--perf-metric` | `ppm` (+ obpm/bpm/…) | Ability + pool source |

**Canonical (deck):**

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero
```

**Season-Y + full panel + LOO:**

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --y-draft-mode season --panel-rows all-ps \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero
```

**Team poolq (not LOO):**

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --roster-x poolq \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero
```

**Filename tokens:** `HERO_[poolq_]q16_allt_min20_mg10_11_21[_season_y][_last_ps].png`

---

## Script 2 — `pass_a_congestion_conditional.py` (F-HERO / CCT)

**What it does:** Conditional draft-rate plots. Alex Slide 10 = `--plot fixed_ai_tj_knbins`.

**Usage:**

```text
python sports/scripts/pass_a_congestion_conditional.py --plot fixed_ai_tj_knbins [options]
```

| Flag | Choices / default | Notes |
|------|-------------------|--------|
| `--plot` | `fixed_ai_tj_knbins` (F-HERO) | Also: `matched_pond`, `p1_grid`, … |
| `--season-min` / `--season-max` | 2011 / 2021 | |
| `--min-minutes` | 20 | |
| `--min-team-season-games` | 10 | |
| `--ai-top-pct` | 7 (typical) | Top X% Â band; vs `--ai-lo`/`--ai-hi` |
| `--dft` | off | Slide 10 uses +DFT |
| `--y-draft-mode` | `ever` · `season` | Same semantics as HERO |
| `--panel-rows` | `all-ps` · `last-ps` | Same semantics as HERO |
| `--tj-binning` | `piecewise_tail` | F-HERO `pw4p7` |
| `--tj-n-low` / `--tj-n-high` | 4 / 7 | Piecewise T̂_j bins |
| `--p2b-single` | off | One spec only (no bundle) |
| `--out-dir` | `basic_data_plots/` | Sandbox: `…/sports_sandbox/fhero` |

**Canonical F-HERO:**

```bash
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --p2b-single --dft \
  --min-minutes 20 --ai-top-pct 7 --tj-n-low 4 --tj-n-high 7 \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/fhero
```

**13–21 sweep:** add `--season-min 2013 --season-max 2021`.

---

## Script 3 — `pass_a_hero_sensitivity_plots.py`

**What it does:** Gallery of labeled sensitivity PNGs under `pass_a/sensitivity/` (includes LOO vs `pool_mean` grid).

```bash
python sports/scripts/pass_a_hero_sensitivity_plots.py --quick
python sports/scripts/pass_a_hero_sensitivity_plots.py --perf-metric obpm
```

| Flag | Notes |
|------|--------|
| `--quick` | Smoke subset (~8 specs) |
| `--perf-metric` | Default `ppm` |

---

## Script 4 — `compare_hero_mg_sandbox.py`

**What it does:** Ventile diff table mg0 vs mg10 in sandbox (runs mg0 if missing).

```bash
python sports/scripts/compare_hero_mg_sandbox.py
```

No CLI flags — paths fixed to `sports_sandbox/hero/`.

---

## Output roots (sandbox)

| Folder | Script | `--output-root` / `--out-dir` |
|--------|--------|-------------------------------|
| `sports_sandbox/hero/` | `pass_a_empirical_bundle.py` | `--output-root …/hero` |
| `sports_sandbox/fhero/` | `pass_a_congestion_conditional.py` | `--out-dir …/fhero` |

Every HERO PNG has `*_provenance.json` with full footer spec.

---

## Permutation sweep + PowerPoint deck

**Run all 2×2×2 core combos** (roster-x × y-mode × panel-rows) and build a deck like your manual `Slide_scripts.zsh`:

```bash
# Core 8 specs, 2011–2021 (default)
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero_permutation_sweep.zsh core

# 2013–2021 only
zsh …/hero_permutation_sweep.zsh core 13_21

# Both windows (16 specs for core)
zsh …/hero_permutation_sweep.zsh core both

# extended (+DFT):  … hero_permutation_sweep.zsh extended 11_21
# full (+EW20):     … hero_permutation_sweep.zsh full both
# real_full:        … hero_permutation_sweep.zsh real_full   # full × both seasons (64)
# force re-run:     … hero_permutation_sweep.zsh core 11_21 force
```

Or stepwise:

```bash
python sports/scripts/hero_permutation_sweep.py --tier core --season-window 11_21
python sports/scripts/hero_permutation_sweep.py --tier core --season-window 13_21
python sports/scripts/hero_permutation_sweep.py --tier core --season-window both
python sports/scripts/hero_permutation_sweep.py --tier real_full   # full + both seasons (64)
python sports/scripts/build_hero_permutation_slides.py
```

**Outputs:**

| File | Purpose |
|------|---------|
| `hero_permutation_slides/manifest.json` | All specs, CLI commands, shape summaries (`n_planned` / `n_runs` / `complete`) |
| `hero_permutation_slides/HERO_permutation_slides_AUTO.pptx` | Intro + one slide per run (PNG + command box) |
| `hero/HERO_*_{tag}.png` | Tagged PNGs (`FIXED_HERO`, `perm_loo_seasony_allps_q16`, …) |

`--dry-run` writes manifest without running. Existing PNGs are skipped unless `--force`.

**Repair manifest** (fix wrong `roster_csv` / shape summaries without re-running pass_a):

```bash
python sports/scripts/hero_permutation_sweep.py --tier real_full --repair-manifest
python sports/scripts/build_hero_permutation_slides.py
```

Manifest fields: `n_planned` (grid size), `n_runs` (= `n_specs`, completed entries), `complete`.

Legacy one-at-a-time script: `Slide_scripts.zsh` (use straight quotes `"`, not curly `"`).

---
