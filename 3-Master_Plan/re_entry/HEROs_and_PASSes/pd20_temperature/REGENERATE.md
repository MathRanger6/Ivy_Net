# PD20 temperature sweep — regenerate

**Run from repo root.** Python env: `/opt/anaconda3/envs/sports_net/bin/python`.

**Outputs folder:** `3-Master_Plan/re_entry/HEROs_and_PASSes/pd20_temperature/`  
**HAND master:** `slides/CHAR_PD20_HAND.pptx` (never overwritten by scripts)

---

## Smoke test (one season, sparse grid)

```bash
PY=/opt/anaconda3/envs/sports_net/bin/python

$PY sports/scripts/grandchild_temperature_select_sweep.py --quick
```

## Full panel (2011–2021, λ = 1.5 & 2.0, log₁₀ t ∈ [−3, 3])

```bash
$PY sports/scripts/grandchild_temperature_select_sweep.py
# or explicitly:
$PY sports/scripts/grandchild_temperature_select_sweep.py --lambda 1.5 2.0
```

## Cold limit check (rule C vs D)

```bash
$PY sports/scripts/grandchild_temperature_cold_limit_diagnostic.py
```

## AUTO slides for CHAR_PD20_HAND

```bash
$PY sports/scripts/build_pd20_hand_slides.py
$PY sports/scripts/build_pd20_hand_slides.py --slides-only   # PNG/meta already fresh
```

Writes `slides/auto/CHAR_PD20_HAND_AUTO.pptx` — copy into `slides/CHAR_PD20_HAND.pptx` by hand.

## Custom grid

```bash
$PY sports/scripts/grandchild_temperature_select_sweep.py \
  --lambda 1.0 1.5 \
  --log10-t -3 -2 -1 0 1 2 3
```

---

## Rollback to PD17 top-K world

PD17 outputs live in `grandchild_assign/` and are **not** modified by PD20 scripts.
To regenerate the λ sweep baseline (rule C):

```bash
$PY sports/scripts/grandchild_lambda_select_sweep.py
```
