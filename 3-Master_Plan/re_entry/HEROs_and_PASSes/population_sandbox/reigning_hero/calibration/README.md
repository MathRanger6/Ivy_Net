# Reigning hero — calibration (PD28)

**Alex ask (PD28, Aug 28):** homophily (ρ\*), γ\*, λ\*, and temperature on the **reigning population**.

## Population

| Field | Value |
|-------|--------|
| Seasons | **2009–2021** |
| Panel rows | **all-ps** (roster geometry + MLE — same as PD21 campaign) |
| Filters | min20 · mg10 · winsor 0.01–0.99 · PPM z |

HERO last-ps aperture lives in `basic_data_plots/` and `../hero/` — not repeated here.

## Paper ladder position

| Stage | Folder | Status |
|-------|--------|--------|
| 0 Population lock | `../README.md` | ✓ |
| 1 Porch BDP | `../basic_data_plots/` | ✓ |
| 2 HERO + F-HERO | `../fhero/`, `../hero_star_sweeps/` | ✓ |
| **3 Calibration** | **`calibration/`** | **this folder** |
| 4 Pass B / sim match | `../../../pass_b/` | next |

## Build

```bash
# repo root — full chain (ρ → MLE → temperature)
python sports/scripts/reigning_hero_calibration.py

# smoke
python sports/scripts/reigning_hero_calibration.py --quick

# subset
python sports/scripts/reigning_hero_calibration.py --only rho mle
```

## Outputs

| Step | Subfolder | Script |
|------|-----------|--------|
| ρ\* | `rho/` | `pd21_rho_hsort_calibrate.py` |
| γ\*, λ\*, t\* | `mle/` | `pd21_draft_bernoulli_mle.py` |
| Gibbs SELECT t sweep | `temperature/` | `grandchild_temperature_select_sweep.py` |

- `manifest.json` — step completion flags  
- `CAMPAIGN_COMPARE.md` — reigning vs PD21 campaign baseline  

## Campaign archive (do not overwrite)

Legacy runs remain in:

- `../../../pd21_rho/` (2011–21)
- `../../../pd21_mle/` (2013–21 primary)
- `../../../pd20_temperature/` (2011–21)
