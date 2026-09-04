# Disposable — normalized weighted cumulative PER HERO probe

**Safe to delete.** Separate from raw-sum folder `_DISPOSABLE_cum_per_weighted_last_ps/`.

## PER_cum (normalized)

At college year k, using only seasons with non-null PER:

$$\text{PER}_{\mathrm{cum},k} = \frac{\sum_{i=1}^{k} i \cdot \text{PER}_i}{\sum_{i=1}^{k} i} = \frac{\sum_{i=1}^{k} i \cdot \text{PER}_i}{k(k+1)/2}$$

when all PER through k exist. Weights **1, 2, …, k** on each season’s PER — a **weighted average**, not a raw sum.

Same HERO spec: 2009–21 · last-ps · mg10 · min20 · poolq_loo · Option A z.

## Regenerate

```bash
export PYTHONPATH="sports"
python3 sports/scripts/pass_a_cum_per_hero_probe.py --normalized --n-bins 8 10 16
```

## Outputs

| Bins | PNG |
|------|-----|
| Q8 | `HERO_q8_cum_per_wt_norm_z_lastps_2009_2021.png` |
| Q10 | `HERO_q10_cum_per_wt_norm_z_lastps_2009_2021.png` |
| Q16 | `HERO_q16_cum_per_wt_norm_z_lastps_2009_2021.png` |
