# F-HERO — canonical outputs only (working aperture)

**Spec:** **09–21** · last-ps · **ALLT** (default) · mg10 min20 · ever-draft · top ~7% Â · pw4p7 · shared T̂_j grid.

**+DFT:** pass `--dft` explicitly when you want draft-ecosystem subsample (not default).

## Files that belong here (current lock)

| Artifact | Role |
|----------|------|
| `BDP_Ai_draft_mass_ecdf_*_09_21_allt_*_last_ps.*` | Draft-mass ECDF (band-picking reference) |
| `FHERO_pw4p7_allt_min20_mg10_top7_ppm_09_21_last_ps.*` | Single-band F-HERO (knee slide) |
| `FHERO_pw4p7_overlay_lines_sharetj_allt_min20_mg10_ppm_09_21_last_ps.*` | P2b overlay — **aligned** T̂_j grid |

*(Older runs may use `_9_21_` or `_13_21_` tags — rerun for `_09_21_` naming.)*

## Recreate

```bash
# ECDF
python sports/scripts/bdp_ai_draft_mass_ecdf.py \
  --season-min 2009 --season-max 2021 \
  --panel-rows last-ps --y-draft-mode ever \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/fhero

# Single-band F-HERO (top 7%)
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --p2b-single \
  --season-min 2009 --season-max 2021 --panel-rows last-ps \
  --min-minutes 20 --ai-top-pct 7 --tj-n-low 4 --tj-n-high 7 \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/fhero

# Overlay (Slide-10 bands)
python sports/scripts/cct_p2b_ai_band_overlay.py \
  --season-min 2009 --season-max 2021 \
  --panel-rows last-ps --y-draft-mode ever \
  --bands "0:7,7:15,15:25,25:40" --hero-top "0:7" \
  --tj-edge-mode shared_panel \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/fhero
```

## Not here

- Band sensitivity matrix → [`../_archive/band_sensitivity_2026-08/`](../_archive/band_sensitivity_2026-08/)
- Old 11–21 +DFT deck → [`../_archive/fhero_old_deck_11_21_dft/`](../_archive/fhero_old_deck_11_21_dft/)
- `localtj` overlay fork → [`../_archive/p2b_localtj_fork/`](../_archive/p2b_localtj_fork/)

Living plan: [`../../_DISPOSABLE_CCT_P2b_workflow_thread.md`](../../_DISPOSABLE_CCT_P2b_workflow_thread.md)
