# Archive — P2b localtj fork (DEAD)

**Status:** **Fork — do not use for deck.** Alex rejected: per-tier median 4+7 splits put overlay lines on **different T̂_j x positions**.

## Superseded by

`FHERO_pw4p7_overlay_lines_sharetj_*` in [`../../fhero/`](../../fhero/) — panel-wide shared T̂_j grid (`--tj-edge-mode shared_panel`).

## Recreate (for audit only)

```bash
python sports/scripts/cct_p2b_ai_band_overlay.py \
  --season-min 2013 --season-max 2021 \
  --panel-rows last-ps --y-draft-mode ever --no-dft \
  --tj-edge-mode within_band \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/_archive/p2b_localtj_fork
```

Filename stem contains **`localtj`** (legacy) vs **`sharetj`** (current).

## Date

2026-08-27 — fixed same day after Alex debrief.
