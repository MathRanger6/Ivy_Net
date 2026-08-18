# Paper Directions 23 — my read (Aug 18, 2026)

**Source:** `transcripts/20260918_Paper_directions_23_otter_ai_transcript.docx` (~40 min)  
**Context:** Charles walked Alex through the PD20–22 memo / HAND backup slides (box QC, minutes floor, ρ bracket, ppm0lt20 contrast). First live read-aloud of the full campaign arc.  
**Prior:** [`PD21_notes.md`](PD21_notes.md) · [`PD20_notes.md`](PD20_notes.md) · [`../3-Master_Plan/re_entry/HEROs_and_PASSes/PD20_22_campaign_big_picture.md`](../3-Master_Plan/re_entry/HEROs_and_PASSes/PD20_22_campaign_big_picture.md)

---

## Headline

Alex is **thrilled with the hero and the panel story** — defensive PD22 work did not break the main result. **Next mission is MLE:** write the likelihood, then fit **λ*, γ*, t*** on fixed empirical rosters. ρ bracket / H_sort forensics and the ppm-zero std-dev plot are **parked** (≤ one day) — not blocking the paper.

---

## What Charles covered (briefing arc)

Charles walked the full ladder: Army inverted-U → MBB hero → Wang-style minimal model (congestion in score) → LG pipeline (ASSIGN → SCORE → SELECT) → Gibbs gate cleared (PD20) → ρ calibration via H_sort bracket → box QC + minutes policy (PD22) → ppm0lt20 contrast slides.

Alex said the articulation practice was valuable; for his book the scientific state is unchanged from “a little while ago” except that panel assumptions are now defended.

---

## Alex reactions — what landed

| Topic | Alex |
|-------|------|
| Box QC (dash rows, ≥11 games) | “This looks great.” |
| Roster-size before/after | Happy — tails gone |
| ESPN 2013→2014 depth jump | OK — Charles has a finger on it |
| Drafted-player minutes CDF | Misread once (44 = drafted player-seasons lost at min 20, not total players); cleared |
| ρ* = 0 on hero panel | Not worried — modest H_sort fit, not “NCAA is random” |
| Interval overlap / visual sorting | Accepts geometry vs bracket ρ* are different questions |
| ppm0lt20 ρ* “strong” | “Where’s the problem?” — if hero + intervals + Gibbs still work, fine |
| ρ ≈ 0 as must-have | **No** — “edge calculation”; hero inverted-U is the main result |
| Drop 2011–2012 seasons | **Yes** — treat as data-quality; analysis from **2013+** is defensible |
| End state | Same as before defensive push: fit **λ, γ, t** by MLE |

---

## ρ, H_sort, ppm-zero — clarify for next briefing

**Hero panel (slide 14, locked):** drop sub-20 + box QC + roster caps → bracket **ρ* = 0** all seasons, H_sort ≈ 0.06. Model–measurement fit, not “no sorting in NCAA.”

**ppm0lt20 contrast (slide 15):** same box-QC ingestion as hero; mean H_sort ≈ drop (Δ ≈ 0.001); longitudinal ρ* ≈ **0.05** (hero = 0) with mid-decade per-season spike 2014→2015. Illustrative wrong estimand — not production policy.

**Re-cal done Aug 18:** `python sports/scripts/pd21_rho_hsort_calibrate.py --ppm-zero-below-minutes 20 --fresh` → refreshed bracket JSON + AUTO slides 15–16.

**Locked production policy (do not confuse with Otter end):** **drop sub-20**, not ppm-zero. Otter garbled the closing (“you’re out” / “it’s zero”). Alex’s operational lock at end of call mixed drop + ppm-zero + drop 2011–2012 — **write down explicitly:** drop-at-20 for ASSIGN input; ppm-zero stays **contrast only**; consider **2013–2021** as primary window.

---

## “Where’s the problem?” — Charles vs Alex

Charles was still carrying PD22 worry: all-zero ρ* on drop panel felt scary vs interval-overlap pictures.

Alex’s frame:

- Hero inverted-U + high visual sorting + Gibbs survival = **main line intact**
- ρ* small or zero after cleaning assumptions is **not fatal**
- Revisiting cleaning assumptions was the **point** of PD22 — no blame for moving fast earlier
- If hero survives, **move on to MLE**

Charles corrected Alex once: **ρ is not a dial that turns up congestion** — congestion needs viable competition (γ-sharp peers); weak leagues don’t get “more congestion” from ρ alone.

---

## Std-dev vs zero-fraction plot (slide 18 area)

Alex pushed on the **positive slope**: more ppm-zero’d players per team → **higher** within-team perf std — opposite naive “everyone at zero → lower dispersion → higher homophily.”

Alex intuition: identical zeros should **lower** team dispersion → **raise** H_sort, not the direction shown.

**Alex priority:** worth **≤ one day** — inspect H_sort **numerators** (team-level SS decomposition), verify perf column uses z-scored ability under ppm-zero policy, not raw PPM bleed-through.

**Not blocking MLE** — Alex said so explicitly twice.

---

## Locked / agreed actions

| Item | Decision |
|------|----------|
| **Hero outcome** | Inverted-U survives — primary scientific object |
| **Gibbs SELECT** | Gate cleared (PD20) |
| **Box QC** | Keep (dash + min 11 games) |
| **Minutes floor** | **Drop sub-20** for locked panel |
| **ppm-zero** | Contrast / investigation only — not production policy |
| **Season window** | OK to drop **2011–2012** (ESPN depth); primary **2013+** |
| **ρ*** | Have bracket value on hero panel (~0); optional edge — not gating paper |
| **Next fit** | **MLE → λ*, γ*, t*** |

---

## MLE — Alex lock (repeated)

1. **Write down the likelihood** (Charles says he already has a functional draft — simplify if overbuilt).
2. **Then** use a solver (scipy / statsmodels / etc.) — only **three** parameters; should be smooth.
3. **Do not** let H_sort forensics or ChatGPT code sprawl **block** this.

Alex also pushed: code will need a **condense pass** after MLE — too much volume from AI-assisted scripts; expect a future sit-down to shrink to a succinct package for the paper.

### Likelihood form — Alex lock (Aug 18 follow-up)

Frame draft outcomes **Bernoulli-style** on the fixed empirical roster each season:

- **K successes:** drafted players ($Y_i = 1$)
- **N − K failures:** not drafted ($Y_i = 0$)
- **Independent** across players (within season), with $p_i$ from the board softmax

Board probabilities (PD21 whiteboard factorization):

\[
\text{logits}_i = \frac{A_i}{t} - \lambda L^C_i, \qquad
p_i = \frac{\exp(\text{logits}_i)}{\sum_j \exp(\text{logits}_j)}
\]

**Log-likelihood** — maximize draft probability on successes, minimize it on failures:

\[
\ell(\lambda, t, \gamma) = \sum_i \Big[ Y_i \log p_i + (1 - Y_i) \log(1 - p_i) \Big]
\]

Plain English (what Alex was gesturing at):

- **Successes (K drafted):** push $p_i$ **up** on drafted players ($\log p_i$ term).
- **Failures (N − K not drafted):** push $p_i$ **down** on everyone else ($\log(1-p_i)$ term).

That is the standard Bernoulli coin-flip story — one term rewards getting the **K** right, the other penalizes giving high draft chance to the **N − K** who were not drafted.

**Sim vs MLE note:** Gibbs SELECT in sim still uses **K draws without replacement** for the readout. MLE uses **independent Bernoullis from softmax** — Alex explicitly chose this for estimation. Softmax sums to 1 per season, so $\sum_i p_i = 1$ (expected ~1 draft if taken literally); treat as a **relative** draft-probability model for fitting $(\lambda, t, \gamma)$, not a literal count constraint. K is observed in the data but does not enter the formula as a separate parameter.

**Related code:** `sports/scripts/pd21_draft_bernoulli_mle.py` — implements the above; extend to joint $\gamma$ if not already wired.

**Explainer stack:** [`../3-Master_Plan/Alex_stuff/PD20_softmax_K_winners_explainer.md`](../3-Master_Plan/Alex_stuff/PD20_softmax_K_winners_explainer.md) · [`../3-Master_Plan/Alex_stuff/PD20_K_draws_and_rho_explainer.md`](../3-Master_Plan/Alex_stuff/PD20_K_draws_and_rho_explainer.md)

---

## Army parallel track

Alex wants **anonymized Army export** so MBB work is not blocked forever — swap talent proxy (e.g. top-block ratio vs PPM) and reproduce the arc for the three-setting paper. Charles ~2–3 days on Army access last week; export “completely anonymized crap” for local + paper sharing when access returns (~1 month horizon mentioned).

**Not blocking MBB MLE now.**

---

## Charles homework

- [x] **Finish H_sort re-calibration run** (Aug 18) — hero drop + ppm0lt20 on current box-QC pipeline; AUTO slides 15–16 + memo companions refreshed
- [ ] **Write / simplify likelihood** for λ, γ, t (Bernoulli-softmax form — Alex lock above)
- [ ] **Run MLE** — grid + BFGS; season batches on locked drop panel
- [ ] **Lock written policy one-pager:** drop sub-20 (not ppm-zero); 2013+ window; slide 14 vs 15 roles
- [ ] **Optional ≤1 day:** H_sort numerator diagnostics + ppm-zero std-dev plot (Alex curiosity, not gate)
- [ ] **Optional:** `PD23_notes` → mirror under `3-Master_Plan/re_entry/` when stable
- [ ] **Army:** export script for anonymized panel when back on Rivanna/AWS

---

## One-liners for next Alex touchpoint

**Where we are:** “Hero and Gibbs gate cleared; box QC and drop-at-20 locked; ρ* ≈ 0 on hero panel is modest H_sort fit — we’re fitting λ, γ, and t by MLE next.”

**ppm-zero slide:** “Slide 15 is contrast on the ppm0lt20 estimand — modest ρ* (~0.05) with a mid-decade spike, vs flat zero on slide 14. Wrong policy, illustrative only; locked calibration is drop + slide 14.”

**If ρ comes up:** “ρ is ASSIGN homophily, not a congestion dial; we can keep ρ at the bracket value or treat it as edge — hero doesn’t require ρ > 0.”

---

## Artifacts

| Item | Path |
|------|------|
| Transcript | `transcripts/20260918_Paper_directions_23_otter_ai_transcript.docx` |
| Campaign narrative | `3-Master_Plan/re_entry/HEROs_and_PASSes/PD20_22_campaign_big_picture.md` |
| Memo deck (read-aloud) | `3-Master_Plan/re_entry/HEROs_and_PASSes/slides/CHAR_PD20_22_takeaways_memo_HAND.pptx` |
| Hero ρ AUTO | `slides/auto/CHAR_PD21_rho_hsort_calibrate_AUTO.pptx` |
| ppm0 contrast AUTO | `slides/auto/CHAR_PD21_rho_hsort_calibrate_ppm0lt20_AUTO.pptx` |
| PD22 investigation | `3-Master_Plan/re_entry/HEROs_and_PASSes/pd22_minutes/PD22_minutes_panel_investigation_todo.md` |
