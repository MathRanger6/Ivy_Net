# HERO — canonical outputs only

**Do not** dump permutation sweeps or sensitivity grids here — use [`../_archive/`](../_archive/).

## NEW FIXED lock (2013–21 · last-ps · ALLT · mg10 · q16 · poolq_loo)

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --season-min 2013 --season-max 2021 \
  --y-draft-mode ever --panel-rows last-ps \
  --roster-x poolq_loo --n-bins 16 --poolq-binning quantile \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero
```

Expected stem: `HERO_q16_allt_min20_mg10_13_21_last_ps.*`

## Sensitivity (archive separately)

- **mg=0:** same command + `--min-team-season-games 0` → [`../_archive/`](../_archive/) when done
- **Permutation deck:** [`../_archive/hero_permutation_sweep/`](../_archive/hero_permutation_sweep/)

Living plan: [`../../_DISPOSABLE_Alex_hero_population_thread.md`](../../_DISPOSABLE_Alex_hero_population_thread.md)
