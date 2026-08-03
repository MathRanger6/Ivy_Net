# 5. Alex magnitude spec — predictive importance of roster pressure

**Last synced:** 2026-07-30

**Source:** Paper Directions **14** (2026-07-30 transcript with Alex Gates)  
**Status:** Spec only — **not yet run**  
**Panel:** Locked hero sample (530): ppm z within season, 16 quantile, winsor (0.01, 0.99), `min_minutes=20`, 2011–2021  
**Full Alex context:** [`../sports/documents/Pertinent_Thoughts_Scout.md`](../../sports/documents/Pertinent_Thoughts_Scout.md) (Alex Follow-Up §3)

---

## The question (in sentences)

Ability alone gets you **most of the way** predicting who gets drafted or promoted. Alex wants to know:

**How much better is prediction if the model includes roster pressure (congestion in the selection score), compared to ability only?**

If the gain is tiny, roster pressure is a nice curve but **does not matter for the prediction people care about** (“Will I get promoted / drafted?”). If the gain is large — especially for **top ability** players under **few slots** — it matters.

This is **not** the same as overlaying the Hero ventile plot on a Naïve ability plot. The Hero plot is **E[Y | poolq_loo]** in a world where roster pressure **already exists**. Alex wants a **fitted counterfactual**: same players, same careers, but the **assessment model** ignores roster congestion (λ = 0 in the **prediction** score).

**Not:** “What if you never played on that team?” (development / ppm endogeneity)  
**Yes:** “What if selectors had unlimited scout capacity and scored you on **ability only**?” (fabricated assessment world — articulate this in prose)

---

## Two models (micro rows, same sample)

| Model | Formula (v1) | Meaning |
|-------|----------------|---------|
| **A — Full** | `Y_draft ~ ability + poolq_loo + poolq_loo²` | Selection with roster / congestion channel |
| **B — Ability-only** | `Y_draft ~ ability` | Alex counterfactual: no roster in the score |

- **ability:** same as hero lock — e.g. `perf` = ppm z-scored within season on the panel row.  
- **poolq_loo:** leave-one-out teammate quality (hero estimand).  
- Use **logit or LPM** consistently; Alex asked for **predicted probabilities**, not only coefficients.

Optional v2: explicit interaction `ability × poolq_loo` if Alex wants ability-dependent roster effects in one equation.

---

## Deliverables (what to give Alex)

### 1. Fit both models

Alex explicitly: **“You have to give me a fit.”** Ventile bars alone are not enough.

- Report coefficients + N + hero filter flags in a small text export (e.g. `HEROs_and_PASSes/MAGNITUDE_model_comparison.txt` when run).

### 2. Per-person counterfactual gap

For each player-season *i*:

- \(\hat{p}_i^{\text{full}}\) = predicted P(draft) from Model A  
- \(\hat{p}_i^{\text{ability}}\) = predicted P(draft) from Model B  
- **Gap:** \(\Delta_i = \hat{p}_i^{\text{full}} - \hat{p}_i^{\text{ability}}\)

Summarize: mean |Δ|, distribution, and **by ability ventile** (Alex suspects error **largest at the top**).

### 3. Overall predictive gain

Compare Model A vs B on the **same holdout or in-sample** (state which):

- ΔAUC (or pseudo-R² for LPM)  
- ΔBrier / log-loss if feasible  
- Alex framing: “~10% greater predictive capacity?” — define denominator (e.g. relative improvement in log-loss)

### 4. Ability-stratified story

| Ability tier | Hypothesis (Alex) |
|--------------|-------------------|
| Low / mid | Roster adds little; ability dominates |
| **Top** | Knowing roster effects **substantially** improves prediction; \|Δ\| largest here |

Optional figure: boxplot of \(\Delta_i\) by ability ventile, or line of mean |Δ| by ability bin.

### 5. Carrying capacity (K / λ) prose

NBA draft ≈ **~60 slots** for the whole NCAA — few winners. Alex + Charles: under **small K**, roster pressure may **crush** top-tier predictions; under many slots, effect may be a **rounding error**. Report basketball numbers; note Army/tenure for cross-domain later.

---

## What the Hero plot does and does not do

| Hero ventile plot | This spec |
|-------------------|-----------|
| Shows **shape** of outcome vs `poolq_loo` | Shows **prediction gain** from including roster in the model |
| World **with** roster pressure in selection | Compares **with** vs **without** roster in the **fitted** prediction |
| Descriptive bins | Requires **Model A vs B** on micro rows |

Pass A generative (λ = 0 vs λ > 0) is the **sim** analogue; this spec is the **empirical** analogue on the 530 panel.

---

## Limitations (say out loud)

1. **ppm / ability may reflect roster context** — Alex accepts a **fabricated assessment** counterfactual; do not claim we rewound development.  
2. **Draft is rare (~1–2%)** — metrics can be noisy; always report **n** by stratum.  
3. **In-sample vs out-of-sample** — prefer a simple train/test or season split if time allows; if not, label in-sample clearly.

---

## Implementation sketch (when you run it)

1. Load hero-filtered panel via `530` / `sports_pipeline` (same config as hero PNG).  
2. Fit Model A and Model B (statsmodels or sklearn).  
3. Write `MAGNITUDE_model_comparison.txt` + CSV of \(\hat{p}_i^{\text{full}}\), \(\hat{p}_i^{\text{ability}}\), \(\Delta_i\), ability ventile, poolq ventile.  
4. Optional PNG: \|Δ\| by ability ventile → `HEROs_and_PASSes/MAGNITUDE_prediction_gap_by_ability.png`.

**Script home (TBD):** e.g. `sports/scripts/hero_magnitude_predictive_comparison.py` — create when Charles runs this checklist section.

---

## One-sentence claim template (yours, after run)

> “Including roster pressure in the draft prediction model [improves / does not materially improve] overall accuracy by [X]; the gain is [largest / not largest] for top-ability players, consistent with congestion mattering most when [few slots / elite peer pools].”

---

## Checklist pointer

[`CHARLES_CHECKLIST.md`](CHARLES_CHECKLIST.md) **Phase C** — after PD15 characterization (Phase B) is done.
