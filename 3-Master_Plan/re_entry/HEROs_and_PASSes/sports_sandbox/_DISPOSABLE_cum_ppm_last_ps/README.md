# Disposable — career cumulative PPM HERO probe

**Safe to delete.** Does not write to `pass_a/` or `sports_sandbox/hero/`.

## Spec

- **2009–2021** · **last-ps** · ever-Y · mg10 · min20 · poolq_loo · quantile
- **Career PPM** = cum college points ÷ cum college minutes (through each season)
- **Option A z:** mean/std from last-PS cross-section applied before LOO on full panel

## Regenerate

```bash
export PYTHONPATH="sports"
python3 sports/scripts/pass_a_cum_ppm_hero_probe.py --n-bins 8 10 16
```

## Outputs (2026-09-03)

| Bins | PNG |
|------|-----|
| Q8 | `HERO_q8_cum_ppm_z_lastps_2009_2021.png` |
| Q10 | `HERO_q10_cum_ppm_z_lastps_2009_2021.png` |
| Q16 | `HERO_q16_cum_ppm_z_lastps_2009_2021.png` |

Aug 2026 run: LPM β₂ ≈ **+0.011** (not concave on this panel — compare season-PPM reigning hero).
