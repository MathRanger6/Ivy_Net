# Reigning hero — star sweep (EW bins × season windows)

**Base lock:** slide 12 — see [`../README.md`](../README.md).

## Grid (20 runs) — **complete Aug 2026**

Hold: `poolq_loo` · `ever` · `last-ps` · `ALLT` · `equal_width` · min20 · mg10 · winsor 0.01–0.99.

| n_bins | 09_21 | 11_21 | 13_21 | 09_19 |
|--------|-------|-------|-------|-------|
| 8 | ✓ | ✓ | ✓ | ✓ |
| 10 | ✓ | ✓ | ✓ | ✓ |
| 12 | ✓ | ✓ | ✓ | ✓ |
| 20 | ✓ | ✓ | ✓ | ✓ |
| 24 | ✓ | ✓ | ✓ | ✓ |

`09_19` = seasons **2009–2019** (drops 2020–21).

## Build

```bash
python sports/scripts/reigning_hero_star_sweep.py
# or
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_star_sweep.zsh
```

`--dry-run` · `--force` (re-run existing PNGs)

## Output tags

`star_ew{N}_{season_window}` — e.g. `star_ew12_09_21`, `star_ew20_13_21`.

Artifacts: `HERO_ew{N}_allt_min20_mg10_{season}_last_ps_star_ew{N}_{window}.png` + CSV + LPM.

Manifest: [`manifest.json`](manifest.json) (`n_runs=20`, `complete=true`).

## Slides (auto deck)

After the sweep completes:

```bash
python sports/scripts/build_reigning_hero_star_sweep_slides.py
# or
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_star_sweep_slides.zsh
```

Outputs in this folder:

- `HERO_star_sweep_slides_AUTO.pptx` — intro + lock reference + 20 runs (Δ vs EW16 · 09–21)
- `HERO_star_sweep_slides_summary.md` — table of diffs and β₂

Each run slide: subtitle + prose bullets (bin count / season window vs lock), PNG, CLI, shape readout.

## Not in v1

- Quantile binning (stay EW family)
- Winsor sweep (hold 0.01–0.99 unless lower-bin forensics demand it)
- +DFT population (reigning hero is ALLT)

Driver: `sports/scripts/reigning_hero_star_sweep.py`
