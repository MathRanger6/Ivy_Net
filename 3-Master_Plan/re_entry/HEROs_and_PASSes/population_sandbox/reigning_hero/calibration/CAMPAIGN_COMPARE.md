# Reigning hero calibration vs PD21 campaign

**Generated:** 2026-08-28  
**Reigning lock:** 2009–2021 · all-ps · min20 · mg10 · PPM z

## Headline numbers (Alex PD28)

| Parameter | Reigning 09–21 | Campaign baseline | Notes |
|-----------|----------------|-------------------|-------|
| **ρ\*** (H_sort bracket) | 0 | 0 | Campaign: 2011–21 [`pd21_rho/`](../../../../pd21_rho/) |
| **γ\*** | 19.5723 | 18 | Campaign MLE: 2013–21 |
| **λ\*** | 1.30243 | 2.5715 | Bernoulli softmax MLE |
| **t\*** (temperature in score) | 1.0699 | 1.06556 | Not Gibbs SELECT t |
| **log L** | -8865.7 | -6919.11 | |
| **n player-seasons** | 46306 | 38123 | |

## Gibbs SELECT temperature sweep

| λ | log10(t) | LOO shape | pool-mean shape |
|---|----------|-----------|-----------------|
| 1.5 | -3.0 | inverted_u_like | monotone_increasing |
| 1.5 | -2.5 | inverted_u_like | monotone_increasing |
| 1.5 | -2.0 | inverted_u_like | monotone_increasing |
| 1.5 | -1.5 | monotone_decreasing | monotone_increasing |
| 1.5 | -1.0 | inverted_u_like | monotone_increasing |
| 1.5 | -0.5 | monotone_decreasing | monotone_increasing |
| 1.5 | 0.0 | inverted_u_like | monotone_increasing |
| 1.5 | 0.5 | inverted_u_like | inverted_u_like |
| 1.5 | 1.0 | inverted_u_like | monotone_increasing |
| 1.5 | 1.5 | inverted_u_like | inverted_u_like |
| 1.5 | 2.0 | monotone_decreasing | monotone_decreasing |
| 1.5 | 2.5 | inverted_u_like | inverted_u_like |
| 1.5 | 3.0 | inverted_u_like | inverted_u_like |
| 2.0 | -3.0 | monotone_decreasing | monotone_increasing |
| 2.0 | -2.5 | monotone_decreasing | monotone_increasing |
| 2.0 | -2.0 | monotone_decreasing | monotone_increasing |
| 2.0 | -1.5 | inverted_u_like | inverted_u_like |
| 2.0 | -1.0 | monotone_decreasing | monotone_increasing |
| 2.0 | -0.5 | inverted_u_like | monotone_increasing |
| 2.0 | 0.0 | inverted_u_like | inverted_u_like |
| … | … | *(26 total runs)* | |

## Artifacts

- ρ: `3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/calibration/rho/REIGNING_PD21_rho_hsort_calibrate_2009_2021_mg10_min20_09_21_fit_bracket.json`
- MLE: `3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/calibration/mle/REIGNING_PD21_draft_bernoulli_mle_2009_2021_mg10_min20_09_21.json`
- Temperature: `3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/reigning_hero/calibration/temperature/REIGNING_GRANDCHILD_temperature_select_sweep_2009_2021_mg10_min20_09_21_meta.json`

## Read for Alex

Re-run the **same PD21 calibration chain** on the **09–21 reigning panel**. ρ* answers ASSIGN (homophily vs empirical H_sort); γ*/λ*/t* answer SCORE on fixed rosters; temperature sweep confirms inverted-U survives Gibbs SELECT at reigning ρ*.

