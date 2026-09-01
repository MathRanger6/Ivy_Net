# LOO-shape batch — perf-metric promotion gate (disposable EDA)

**Generated:** 2026-08-28
**Porch:** reigning hero lock · `mg10 min20 09_21` · last-ps · EW16 · winsor 1–99 on poolq_LOO

**COMPASS rule:** do not promote on sorting index (H_sort) alone. **Pass** = concave LPM β₂ (< 0). **Fail** = strictly monotone ↑ or convex β₂. **Marginal** = flat β₂ (includes reigning PPM baseline).

## Summary

| Rank | Key | LPM β₂ | LPM | Bin shape | Monotone ↑? | Â–LOO r | H_sort | Verdict |
|------|-----|--------|-----|-----------|-------------|---------|--------|---------|
| 1 | `minutes` | -0.00972 | concave | inverted_u_like | no | -0.089 | 0.0534 | **pass** |
| 2 | `ppm` | +0.00172 | flat | inverted_u_like | no | -0.063 | 0.0644 | **marginal** |
| 3 | `ts_pct_box` | +0.02103 | convex | other | no | 0.134 | 0.1243 | **fail** |
| 4 | `tspct` | +0.02318 | convex | other | no | 0.127 | 0.1247 | **fail** |
| 5 | `efg_pct` | +0.02651 | convex | other | no | 0.129 | 0.1215 | **fail** |
| 6 | `per` | +0.03807 | convex | other | no | 0.116 | 0.1113 | **fail** |
| 7 | `fg_pct` | +0.03895 | convex | other | no | 0.060 | 0.0948 | **fail** |
| 8 | `ws` | +0.04823 | convex | other | no | 0.264 | 0.1627 | **fail** |
| 9 | `bpm` | +0.06880 | convex | other | no | 0.473 | 0.3366 | **fail** |

## Verdict key

- **pass** — concave LPM β₂ (< 0); candidate to inspect (not auto-promote)
- **marginal** — flat LPM β₂ ≈ 0 (reigning PPM lives here)
- **fail** — strictly monotone ↑ and/or convex LPM β₂ (> 0)

## Points per minute (PPM) baseline

- LPM β₂ = +0.00172 (flat); bin shape = inverted_u_like; verdict = **marginal** (flat LPM β₂ (+0.00172); bin=inverted_u_like (non-monotone but not concave)).
- Reigning lock reference: β₂ ≈ +0.00172, shape tags “robust tail drop.”

## Per-metric artifacts

PNG + bin CSV under `loo_shape/{metric}/`.

