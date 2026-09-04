# Disposable — weighted cumulative PER HERO probe

**Safe to delete.** Does not write to `pass_a/` or `sports_sandbox/hero/`.

## PER_cum definition

At college year index `i` (1 = first season, 2 = second, …):

$$\text{PER}_{\mathrm{cum},k} = \sum_{i=1}^{k} i \cdot \text{PER}_i$$

Example (four years): `1×PER_fr + 2×PER_so + 3×PER_jr + 4×PER_sr`.

Missing PER in a season → that term skipped; earlier terms kept.

## Spec

- 2009–2021 · last-ps · ever-Y · mg10 · min20 · poolq_loo · quantile
- Option A z: reference = last-PS cross-section before LOO

## Regenerate

```bash
export PYTHONPATH="sports"
python3 sports/scripts/pass_a_cum_per_hero_probe.py --n-bins 8 10 16
```

## Outputs

| Bins | PNG |
|------|-----|
| Q8 | `HERO_q8_cum_per_wt_z_lastps_2009_2021.png` |
| Q10 | `HERO_q10_cum_per_wt_z_lastps_2009_2021.png` |
| Q16 | `HERO_q16_cum_per_wt_z_lastps_2009_2021.png` |

2026-09-03 run: N=20,705 · drafts=560 · LPM β₂ ≈ **+0.020** (not concave).
