# Archive — F-HERO bin/layout probes

**Status:** Developmental — one-off comparisons, not population locks.

## Contents

| Pattern | Question |
|---------|----------|
| `FHERO_pw4p4_*` | 4+4 vs 4+7 tail resolution |
| `FHERO_pw4p7_triptych_*` | Three-panel layout experiment |
| `FHERO_pw4p7_dft_*_13_21_last_ps` | +DFT vs ALLT on NEW FIXED window |

## Recreate pw4p4 probe

```bash
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --p2b-single --no-dft \
  --season-min 2013 --season-max 2021 --panel-rows last-ps \
  --min-minutes 20 --ai-top-pct 7 --tj-n-low 4 --tj-n-high 4 \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/_archive/fhero_bin_probes
```

Canonical binning remains **pw4p7** in [`../../fhero/`](../../fhero/).
