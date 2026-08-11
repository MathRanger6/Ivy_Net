# PD17 empirical figures & AUTO slides — regenerate cheat sheet

**Run from repo root** unless noted. Python env: `/opt/anaconda3/envs/sports_net/bin/python` (needs `python-pptx` for slide builders).

**Outputs folder:** `3-Master_Plan/re_entry/HEROs_and_PASSes/empirical_pd17/`  
**AUTO decks:** `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/auto/`  
**HAND master (never overwritten):** `slides/CHAR_PD17_HAND.pptx`

Close PowerPoint before regenerating `.pptx` files.

**HAND workflow:** Scripts write **reference** decks (`slides/auto/*_AUTO.pptx` and standalone `.pptx`). You update HAND by hand: **Change Picture** for plots, copy updated bullet numbers, keep **Insert → Equation → LaTeX** formatting you already applied. python-pptx cannot create real Office Math objects.

---

## Regenerate everything (figures + AUTO slides)

```bash
PY=/opt/anaconda3/envs/sports_net/bin/python

$PY sports/scripts/build_empirical_pd17_intro_slide.py
$PY sports/scripts/build_empirical_ai_tj_distributions_slide.py
$PY sports/scripts/build_empirical_team_interval_overlap_slide.py
$PY sports/scripts/build_empirical_lc_distributions_slide.py
$PY sports/scripts/build_empirical_gamma_lc_slide.py
$PY sports/scripts/build_empirical_rho_coverage_slide.py
$PY sports/scripts/build_grandchild_league_analysis_slide.py
```

Slide builders call their diagnostic scripts by default (full refresh). Use `--slides-only` when PNGs are already correct and you only changed slide text/layout.

**HAND17 interval slides 3–5** (full panel + paired 2015–2019 window):

```bash
$PY sports/scripts/rebuild_pd17_interval_reference_slides.py
$PY sports/scripts/rebuild_pd17_interval_reference_slides.py --slides-only
$PY sports/scripts/rebuild_pd17_interval_reference_slides.py --skip-full-panel   # slides 4–5 only
```

Writes reference decks only — **not** `CHAR_PD17_HAND.pptx`:

| HAND # | Reference deck |
|--------|----------------|
| 3 | `auto/CHAR_empirical_team_interval_overlap_AUTO.pptx` (2011–2021 full panel) |
| 4 | `auto/CHAR_empirical_team_interval_overlap_2015_2019_AUTO.pptx` (NCAA window) |
| 5 | `auto/CHAR_grandchild_league_interval_overlap_2015_2019_AUTO.pptx` (sim window) |

Legacy alias: `sync_pd17_hand_slides_3_4.py` → same orchestrator.

---

## Per slide — diagnostic (PNG) vs builder (AUTO .pptx)

| HAND # | Task | Diagnostic (PNG/CSV) | Options | Slide builder | Reference output |
|--------|------|----------------------|---------|---------------|------------------|
| 1 | Glossary | *(text only)* | — | `build_empirical_pd17_intro_slide.py` | `auto/CHAR_empirical_pd17_intro_AUTO.pptx` |
| 2 | `\hat{A}_i`, `\hat{T}_j` | `empirical_ai_tj_distributions.py` | — | `build_empirical_ai_tj_distributions_slide.py` | `auto/CHAR_empirical_ai_tj_distributions_AUTO.pptx` |
| 3 | Interval overlap (full panel) | `empirical_team_interval_overlap.py` | — | `build_empirical_team_interval_overlap_slide.py` | `auto/CHAR_empirical_team_interval_overlap_AUTO.pptx` |
| 4 | Interval overlap (NCAA window) | `empirical_team_interval_overlap.py` | `--season-min 2015 --season-max 2019` | same + window flags | `auto/CHAR_empirical_team_interval_overlap_2015_2019_AUTO.pptx` |
| 5 | Grandchild interval (sim window) | `grandchild_league_interval_diagnostic.py` | `--season-min 2015 --season-max 2019` | `build_grandchild_league_analysis_slide.py` | `auto/CHAR_grandchild_league_interval_overlap_2015_2019_AUTO.pptx` |
| 6 | Team `L_C` 1D | `empirical_lc_distributions.py` | `--gamma G` | `build_empirical_lc_distributions_slide.py` | `auto/CHAR_empirical_lc_distributions_AUTO.pptx` (slide 1) |
| 7 | `\hat{T}_j` vs `L_C` | *(same as row 6)* | `--gamma G` | *(same deck, slide 2)* | same AUTO deck |
| 8 | Empirical vs sim `\rho` | `empirical_rho_coverage_overlay.py` | see below | `build_empirical_rho_coverage_slide.py` | `auto/CHAR_empirical_rho_coverage_overlay_AUTO.pptx` |

Slide builders support `--slides-only`. **`rebuild_pd17_interval_reference_slides.py`** rebuilds HAND rows 3–5 in one command (never HAND).

### HAND choices not in script defaults

- Slide 5 (L_C): Charles uses **`\gamma = 0.5`** (interior `L_C`); scripts default **`\gamma = 10`** from `tier1_sim_config.py` unless you pass `--gamma 0.5`.
- Slide 4 (Grandchild): default **`\rho = 0.5`**, seed **5412015**.
- Slide 1 glossary: **`\hat{A}_i` = PPM z**, not Beta(2,2) sim draw.

---

## Script reference (flags & outputs)

### `empirical_ai_tj_distributions.py`

```bash
python sports/scripts/empirical_ai_tj_distributions.py
```

**Writes:** `EMPIRICAL_Ai_Tj_distributions.png`, `EMPIRICAL_Ai_Tj_team_season.csv`, `EMPIRICAL_Ai_Tj_meta.json`

---

### `empirical_team_interval_overlap.py`

```bash
python sports/scripts/empirical_team_interval_overlap.py
python sports/scripts/empirical_team_interval_overlap.py --season-min 2015 --season-max 2019
```

**Writes:** `EMPIRICAL_team_interval_overlap.png` (full) or `EMPIRICAL_team_interval_overlap_2015_2019.png` (window), team-season CSV, meta JSON

**Tip:** Link PNG in PowerPoint instead of embedding if Dropbox Save fails.

---

### `grandchild_league_interval_diagnostic.py`

```bash
python sports/scripts/grandchild_league_interval_diagnostic.py
python sports/scripts/grandchild_league_interval_diagnostic.py --season-min 2015 --season-max 2019 --rho 0.5
```

**Writes:** legacy `GRANDCHILD_league_interval_overlap.png` (default 2015) or tagged window PNG/meta; one Grandchild run **per season** in window, stacked team-seasons

---

### `empirical_lc_distributions.py`

```bash
python sports/scripts/empirical_lc_distributions.py
python sports/scripts/empirical_lc_distributions.py --gamma 0.5
python sports/scripts/empirical_lc_distributions.py --gamma 3
```

| Flag | Meaning |
|------|---------|
| `--gamma G` | Override viability sharpness in `\sigma(\gamma(\hat{A}-\theta))`. Default: `SELECTION_539_VIABILITY_SHARPNESS` (10). |

**Writes:** `EMPIRICAL_L_C_distribution.png`, `EMPIRICAL_L_C_vs_Tj_2d.png`, team CSV, meta JSON

---

### `empirical_gamma_lc_sweep.py`

```bash
python sports/scripts/empirical_gamma_lc_sweep.py
```

**Writes:** `EMPIRICAL_L_C_gamma_sweep_strip.png`, `EMPIRICAL_L_C_gamma_sweep_summary.csv`, meta JSON  
**Arms:** `\gamma \in \{10, 5, 1, 0.5, 0.001\}`; fixed `\theta` from K/N on panel.

---

### `empirical_rho_coverage_overlay.py`

```bash
# Default — 1×3: empirical | four ρ arms | ρ=1→32 sweep (Oranges ramp)
python sports/scripts/empirical_rho_coverage_overlay.py

python sports/scripts/empirical_rho_coverage_overlay.py --cmap Greens
python sports/scripts/empirical_rho_coverage_overlay.py --cmap YlOrRd
python sports/scripts/empirical_rho_coverage_overlay.py --two-panel
```

| Flag | Meaning |
|------|---------|
| `--cmap NAME` | Hue ramp for ρ=1→32 lines (right panel). `Oranges` (default), `Greens`, `YlOrRd`, `YlGn`. |
| `--two-panel` | Old 1×2: empirical \| sweep only (drops center four-arm panel). |

**Writes:**

| File | Use |
|------|-----|
| `EMPIRICAL_rho_coverage_overlay.png` | Full **1×3** default — slide 7 |
| `EMPIRICAL_rho_coverage_sim_rho_1_32_sweep.png` | Right-panel sweep only |
| `EMPIRICAL_rho_coverage_overlay_meta.json` | Peaks per arm (`sim_legacy_arms`, `sim_sweep_arms`) |

**ρ sweep values (default):** log-spaced 1, 1.64, 2.69, 4.42, 7.25, 11.9, 19.5, 32.

---

## Slide builders — common flag

All `build_empirical_*_slide.py` scripts support:

```bash
python sports/scripts/build_empirical_<name>_slide.py --slides-only
```

Skips PNG regeneration; rebuilds `.pptx` from existing figures + meta JSON.

**`build_empirical_lc_distributions_slide.py`** also passes through `--gamma G` to the diagnostic script when not using `--slides-only`.

---

## Reference `.pptx` output names

| Script | Output |
|--------|--------|
| `build_empirical_pd17_intro_slide.py` | `auto/CHAR_empirical_pd17_intro_AUTO.pptx` |
| `build_empirical_ai_tj_distributions_slide.py` | `auto/CHAR_empirical_ai_tj_distributions_AUTO.pptx` |
| `build_empirical_team_interval_overlap_slide.py` | `auto/CHAR_empirical_team_interval_overlap_AUTO.pptx` |
| `build_empirical_lc_distributions_slide.py` | `auto/CHAR_empirical_lc_distributions_AUTO.pptx` (2 slides) |
| `build_empirical_gamma_lc_slide.py` | `auto/CHAR_empirical_gamma_lc_sweep_AUTO.pptx` |
| `build_empirical_rho_coverage_slide.py` | `auto/CHAR_empirical_rho_coverage_overlay_AUTO.pptx` |
| `build_grandchild_league_analysis_slide.py` | legacy 2015 → `slides/CHAR_grandchild_league_analysis.pptx`; window → `auto/CHAR_grandchild_league_interval_overlap_*_AUTO.pptx` |
| `build_grandchild_empirical_lc_compare_slide.py` | `auto/CHAR_grandchild_empirical_lc_compare_AUTO.pptx` |
| `build_grandchild_ncaa_roster_size_slide.py` | `auto/CHAR_grandchild_ncaa_roster_size_compare_AUTO.pptx` |
| `rebuild_pd17_interval_reference_slides.py` | orchestrates HAND rows 3–5 (never HAND) |

**Optional:** gamma sweep AUTO is not in the current 7-slide HAND17 deck.

---

## Related docs

- Slide order & HAND JPEG exports: [`../slides/README.txt`](../slides/README.txt)
- Phase B sim deck (separate): `./scripts/build_characterization_slides.sh`
- Slide typography / LaTeX workflow: `sports/scripts/gallery_mathtext.py` (PD17 bullets: no `$...$`, line spacing 1.5)
