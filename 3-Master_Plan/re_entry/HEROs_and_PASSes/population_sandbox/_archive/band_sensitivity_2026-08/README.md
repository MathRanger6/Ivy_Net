# Archive — P2b band sensitivity (2026-08-27)

**Status:** Developmental — retained to tell “which Â bands?” story for Alex.

## Summary figure

Open **`BAND_SENSITIVITY_summary.png`** first — 2×2 overlays + elite-tier power bars.

Readout: `BAND_SENSITIVITY_readout.md`

## Recreate everything

```bash
python sports/scripts/cct_p2b_band_sensitivity.py \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/population_sandbox/_archive/band_sensitivity_2026-08

# Skip panel rebuild if artifacts exist:
python sports/scripts/cct_p2b_band_sensitivity.py --skip-rerun --out-dir ...
```

## Schemes (subfolders)

| Slug | Bands | Notes |
|------|-------|-------|
| `dm30` | 30% draft-mass tiers | Old default — top band too narrow (~5%) |
| `slide10` | 0:7,7:15,15:25,25:40 | Matches Alex Slide 10 prose |
| `two_band` | 0:7,7:20 | Simpler overlay |
| `suggest10` | Auto 10% steps | Top 10% has most drafts (K=206) |

**Conclusion:** Knee T̂_j ≈ 1.35 stable on elite band across schemes; prefer Slide-10 or top 7–10% for deck.

## Script

`sports/scripts/cct_p2b_band_sensitivity.py`

## Related

- SCOUT memo: [`../../SCOUT_and_COMPASS/20260827_COMPASS_to_SCOUT_P2b_data_aperture_last_ps.md`](../../SCOUT_and_COMPASS/20260827_COMPASS_to_SCOUT_P2b_data_aperture_last_ps.md)
- Disposable: [`../../_DISPOSABLE_CCT_P2b_workflow_thread.md`](../../_DISPOSABLE_CCT_P2b_workflow_thread.md)
