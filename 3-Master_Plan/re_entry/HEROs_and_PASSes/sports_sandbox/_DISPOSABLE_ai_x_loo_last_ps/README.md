# Disposable — Â × poolq_loo product HERO probe

**Safe to delete.** Does not write to `pass_a/` or `sports_sandbox/hero/`.

## X-axis

$$\text{ai\_x\_loo} = \hat{A}_i \times \mathrm{poolq}_{\mathrm{LOO}}$$

Both are z-scored ppm (within season) and winsorized LOO teammate quality from the locked rebuild path. Quantile bins on the **product**.

## Spec

2009–2021 · last-ps · ever-Y · mg10 · min20 · ppm · winsor (0.01, 0.99)

## Regenerate

```bash
export PYTHONPATH="sports"
python3 sports/scripts/pass_a_ai_x_loo_hero_probe.py --n-bins 8 10 16
```

## Outputs

| Bins | PNG |
|------|-----|
| Q8 | `HERO_q8_ai_x_loo_lastps_2009_2021.png` |
| Q10 | `HERO_q10_ai_x_loo_lastps_2009_2021.png` |
| Q16 | `HERO_q16_ai_x_loo_lastps_2009_2021.png` |

CSV ventile tables + `HERO_ai_x_loo_meta_2009_2021.json` (includes LOO-only and perf-only β₂ on same rows).
