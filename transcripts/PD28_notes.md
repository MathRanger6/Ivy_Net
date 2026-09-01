# Paper Directions 28 — my read (Aug 28, 2026)

**Source:** `transcripts/20260828_Paper_Directions_28_otter_ai_transcript.docx` (~3:21)  
**Context:** Short check-in after porch work — Charles showed **no-winsor poolq_LOO** distribution and confirmed **Â** talent distribution on reigning deck.  
**Prior:** [`PD27_notes.md`](PD27_notes.md) · [`../3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md`](../3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/README.md)

---

## Headline

Alex approved the cleaned distributions (“this cleaned up a good bit of stuff for me”). **Next deliverable:** rerun the **PD20–21 calibration chain** on the **reigning hero population** (09–21 · min20 · mg10) and report **ρ\*** (homophily), **γ\***, **λ\***, and **temperature** sweep status.

> **Alex one-liner:** “Give me those numbers.”

---

## Transcript arc (~3:21)

1. **No-winsor LOO (00:00–00:12)** — Charles shows poolq_LOO dist without winsor clip; Alex: “Great. That looks good.”
2. **Â distribution (00:22–01:16)** — Charles pulls Â_i histogram from slide deck; “very slightly skewed.” Alex happy — winsor confusion resolved.
3. **Calibration ask (01:34–02:01)** — Alex: next step = **homophily calculation on the new data**, then **gamma star, lambda star**, and **temperature**. Charles: “Right up.”

---

## Alex ask — locked task list

| # | Parameter | PD21 script | Reigning output |
|---|-----------|-------------|-----------------|
| **1** | **ρ\*** (homophily / H_sort match) | `pd21_rho_hsort_calibrate.py` | `reigning_hero/calibration/rho/` |
| **2** | **γ\***, **λ\***, **t\*** | `pd21_draft_bernoulli_mle.py` | `reigning_hero/calibration/mle/` |
| **3** | **Temperature** (Gibbs SELECT) | `grandchild_temperature_select_sweep.py` | `reigning_hero/calibration/temperature/` |

**Population lock (same as reigning hero):**

| Field | Value |
|-------|--------|
| Seasons | **2009–2021** |
| Panel for ρ / MLE | **all-ps** (player-season rosters; same as PD21 campaign) |
| Filters | min20 · mg10 (default pipeline) · winsor 0.01–0.99 on poolq |
| HERO aperture | last-ps (separate — already built in porch) |

**Not on screen:** F-HERO, draft-rate LOO vs T̂_j, star sweeps — those are porch/SI; this call is **calibration numbers only**.

---

## Campaign comparison (baseline)

| Run | Seasons | ρ\* (longitudinal) | γ\* | λ\* | t\* |
|-----|---------|-------------------|-----|-----|-----|
| PD21 campaign | 2011–2021 | **0.0** | — | — | — |
| PD21 MLE (primary) | 2013–2021 | — | **18.0** | **2.57** | **1.07** |
| **Reigning (PD28)** | **2009–2021** | **0.0** | **19.57** | **1.30** | **1.07** |

See [`../3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/CAMPAIGN_COMPARE.md`](../3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/reigning_hero/calibration/CAMPAIGN_COMPARE.md) after runs complete.

---

## Build

```bash
# repo root — all three steps
python sports/scripts/reigning_hero_calibration.py

# or subset
python sports/scripts/reigning_hero_calibration.py --only rho mle temperature
```

---

## Thread log

| Date | Entry |
|------|--------|
| 2026-08-28 | PD28 ingested; calibration scaffold + driver wired; runs started on 09–21 reigning panel. |
