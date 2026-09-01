# Disposable perf-metric × ρ / H_sort EDA

**Safe to delete.** Nothing in `reigning_hero/` or canonical `pd21_rho/` reads from here.

## Phase 1 — H_sort ladder (done)

Compare **sorting index (H_sort)** across perf metrics: **09–21 · mg10 · min20 · all-ps · z-within-season**.

→ `H_SORT_LADDER_REPORT.md`, `h_sort/`

## Phase 2 — LOO-shape batch (done)

**COMPASS promotion gate** on reigning porch (mg10 · min20 · 09_21 · last-ps · EW16 · winsor 1–99):

```bash
export PYTHONPATH="sports"
python3 sports/scripts/perf_metric_loo_shape_batch.py
python3 sports/scripts/perf_metric_loo_shape_batch.py --no-plots   # CSV only (~2 min)
python3 sports/scripts/perf_metric_loo_shape_batch.py --metrics ppm bpm minutes
```

→ `loo_shape/LOO_SHAPE_REPORT.md`, `loo_shape/loo_shape_summary_2009_2021.csv`, per-metric PNGs

**Headline (Aug 2026 run):** No alternate metric beats PPM for hero promotion. PPM = **marginal** (flat β₂). BPM / PER / WS = **fail** (convex β₂). Minutes = concave **pass** but not a substantive ability axis.

## Layout

| Path | Contents |
|------|----------|
| `h_sort/` | Per-metric empirical H_sort |
| `loo_shape/` | Draft rate vs poolq_LOO + LPM β₂ batch |
| `rho_calibration/{metric}/` | PD21 ρ outputs when `--run-rho` (parked) |
| `H_SORT_LADDER_REPORT.md` | Ladder + COMPASS gate narrative |
| `_DISPOSABLE_perf_metric_rho_eda_thread.md` | Thread anchor |

## Discard

```bash
rm -rf 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/_DISPOSABLE_perf_metric_rho_eda
```
