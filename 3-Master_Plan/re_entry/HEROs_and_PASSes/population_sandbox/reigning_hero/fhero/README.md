# Reigning hero — paired F-HERO

**Population:** same aperture as [`../README.md`](../README.md) lock and [`../basic_data_plots/`](../basic_data_plots/).

| Field | Value |
|-------|--------|
| Seasons | **2009–2021** |
| **panel-rows** | **last-ps** |
| **y-draft-mode** | **ever** |
| Population | **ALLT** (default) |
| Filters | min20 · mg10 · winsor 1–99 · PPM z |
| F-HERO x-axis | **T̂_j** (team mean, incl. self) — **not** poolq_LOO |
| Â band | top **7%** |
| T̂_j bins | **pw4p7** (4 coarse + 7 fine tail) |

## Pairing with reigning HERO

| Plot | X-axis | Elite shape (09–21) |
|------|--------|---------------------|
| **HERO** (EW16 lock) | poolq_LOO | **Flat** (β₂ ≈ +0.00172) |
| **F-HERO** (this folder) | T̂_j | **Downturn visible** (`alex_downturn_visible`) |

Same rows, different congestion measure — do not merge into one curve.

## Build

```bash
python sports/scripts/reigning_hero_fhero.py
# or
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/reigning_hero_fhero.zsh

# +DFT overlay sensitivity:
python sports/scripts/reigning_hero_fhero.py --with-dft-overlay
```

Subset: `--only ecdf single overlay overlay_dft`

## Artifacts

| Key | File stem | Role |
|-----|-----------|------|
| `ecdf` | `BDP_Ai_draft_mass_ecdf_mg10_min20_9_21_allt_ppm_last_ps` | Band-picking ECDF |
| `single` | `FHERO_pw4p7_allt_min20_mg10_top7_ppm_9_21_last_ps` | Single-band knee |
| `overlay` | `FHERO_pw4p7_overlay_lines_sharetj_allt_min20_mg10_ppm_9_21_last_ps` | Slide-10 multi-band |
| `overlay_dft` | `…_dft_…` | Optional +DFT sensitivity |

Manifest: [`manifest.json`](manifest.json) — readouts + pairing note.

Legacy copies of the same 09–21 runs may also live in [`../../fhero/`](../../fhero/); **this folder** is the reigning-hero canonical path.
