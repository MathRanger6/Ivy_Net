# PD21 — rho calibration to empirical H_sort

Alex (Aug 14): calibrate homophily knob **rho** so Grandchild assignment (LG) simulated **sorting index ($H_{\mathrm{sort}}$)** matches empirical NCAA on the filtered hero panel. Formal rho maximum likelihood estimation (MLE) parked for later.

## Regenerate (definitive full panel)

```bash
# From repo root — bracket search, 50 seeds, tol=0.001 (defaults)
python sports/scripts/pd21_rho_hsort_calibrate.py --n-seeds 50 --n-jobs 8 --fresh

# Progress + ETA every 30s (default); e.g. every 15s:
python sports/scripts/pd21_rho_hsort_calibrate.py --n-seeds 50 --n-jobs 8 --fresh --progress-interval 15

# Smoke (2015 only, 8 seeds)
python sports/scripts/pd21_rho_hsort_calibrate.py --quick --fresh
```

Use **`--fresh`** when upgrading bracket tolerance or seed count so the detail JSONL checkpoint is rebuilt.

Resume an interrupted run: omit `--fresh` (reuses `*_bracket.jsonl`).

## AUTO slide

```bash
python sports/scripts/build_pd21_rho_hsort_calibrate_slide.py --slides-only
```

Writes `slides/auto/CHAR_PD21_rho_hsort_calibrate_AUTO.pptx` — copy into HAND (Change Picture + bullets).

## Sensitivity (min_minutes + conference subsets)

```bash
python sports/scripts/pd21_rho_hsort_sensitivity.py --n-seeds 20 --n-jobs 8
```

## Bracket search

Assumes $H_{\mathrm{sort}}$ increases in $\rho$. Evaluate $\rho=0$; if sim below empirical, expand upper bound (0.05 → 0.1 → … up to `--rho-max` default 0.5), then **bisect** to `--bracket-tol` (default **0.001**). Rho stored to 12 decimal places.

## Outputs

| File | Content |
|------|---------|
| `PD21_rho_hsort_calibrate_2011_2021_bracket.jsonl` | One row per sim run |
| `PD21_rho_hsort_calibrate_2011_2021_bracket.csv` | Summary by season × rho |
| `PD21_rho_hsort_calibrate_2011_2021_bracket.json` | Per-season $\rho^*$ + longitudinal $\rho^*$ + bracket trace |
| `PD21_rho_hsort_calibrate_2011_2021_bracket.png` | Small multiples (x-axis zoomed to evaluated $\rho$) |

## Parallel

- **`process`** (default): `ProcessPoolExecutor`
- **`ray`**: optional Rivanna / talent-style backend

Modin is not used — inner loop is numpy Grandchild assignment.

## Longitudinal $\rho^*$

Minimizes **mean** across seasons of $|H_{\mathrm{sort}}^{\mathrm{sim}} - H_{\mathrm{sort}}^{\mathrm{emp}}|$ over evaluated $\rho$ values. Legacy $\rho=0.5$ eval included unless `--no-reference-rho`.
