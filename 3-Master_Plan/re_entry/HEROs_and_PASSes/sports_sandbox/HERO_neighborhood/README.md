# HERO neighborhood — one-knob probes from NEW FIXED HERO

**Base (Alex lock, HAND deck Slide 37 / PNG `Slide38.png`):**

| Field | Value |
|-------|-------|
| Seasons | **2013–2021** |
| Panel | **`last-ps`** (final-season cross-section) |
| X | **`poolq_loo`** · QTL16 · ALLT |
| Y | **ever-draft** |
| Filters | min20 · mg10 · winsor 0.01–0.99 |

**Reference shape (Aug 2026 sweep):** β₂ ≈ **−0.0128** (concave); n ≈ 16,836 PS; drafts ≈ 424.

**Old FIXED HERO** (pre-Alex): 11–21 · **all-ps** · flat elite (β₂ ≈ +0.006). Not the same object.

---

## Base rerun

```bash
python sports/scripts/pass_a_empirical_bundle.py \
  --season-min 2013 --season-max 2021 \
  --y-draft-mode ever --panel-rows last-ps \
  --roster-x poolq_loo --n-bins 16 --poolq-binning quantile \
  --output-tag NEW_FIXED_HERO \
  --output-root 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/HERO_neighborhood
```

---

## Neighborhood grid (one knob each)

Run all:

```bash
zsh 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero_neighborhood_sweep.zsh
```

| Tag | Knob changed | Purpose |
|-----|--------------|---------|
| `NEW_FIXED_HERO` | *(none — base)* | Alex lock reference |
| `probe_allps` | `panel-rows all-ps` | Does concavity disappear on full panel? |
| `probe_ew16` | `poolq-binning equal_width` · `--n-bins 16` | EW16 display |
| `probe_ew20` | `poolq-binning equal_width` · `--n-bins 20` | EW20 display |
| `probe_q20` | `poolq-binning quantile` · `--n-bins 20` | QTL20 display |
| `probe_seasony` | `--y-draft-mode season` | Season-Y label at draft timing |
| `probe_dft` | `--dft` | Power-5 team filter on hero |
| `probe_11_21` | seasons 2011–2021 | Pre-2013 sensitivity |
| `probe_mg0` | `--min-team-season-games 0` | Pre-QC fragment replay |
| `probe_poolq` | `--roster-x poolq` | Team mean (incl. self) vs LOO |

Each run writes tagged PNG + CSV + provenance under this folder.

---

## Paired F-HERO (same season + panel)

See [`../fhero/`](../fhero/) — rerun with `--season-min 2013 --season-max 2021 --panel-rows last-ps`.

**Open choice:** +DFT (Slide 10 tradition) vs ALLT (match NEW HERO population). Run both if unsure.

```bash
# +DFT (Slide 10 parity)
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --p2b-single --dft \
  --season-min 2013 --season-max 2021 --panel-rows last-ps \
  --min-minutes 20 --ai-top-pct 7 --tj-n-low 4 --tj-n-high 7 \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/fhero

# ALLT (match HERO population filter)
python sports/scripts/pass_a_congestion_conditional.py \
  --plot fixed_ai_tj_knbins --p2b-single \
  --season-min 2013 --season-max 2021 --panel-rows last-ps \
  --min-minutes 20 --ai-top-pct 7 --tj-n-low 4 --tj-n-high 7 \
  --out-dir 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/fhero
```

---

*COMPASS · Aug 2026*
