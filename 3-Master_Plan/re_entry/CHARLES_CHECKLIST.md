# Charles checklist — PD15 characterization (manual checkoff)

**Last synced:** 2026-08-03

**Source:** Paper Directions **15** (Jul 31, 2026) — [`../../transcripts/PD15_notes.md`](../../transcripts/PD15_notes.md)

**Purpose:** The **one** place you mark **what you personally did** for Alex’s current ask: **characterize the model** (sensitivity slides), then (later) fit to data — not re-entry onboarding.

**Supersedes:** [`CHARLES_CHECKLIST_archive_20260803.md`](CHARLES_CHECKLIST_archive_20260803.md) (re-entry + PD14 path).

**How to use**

1. Work **top to bottom** (Phase A → B → C).  
2. Change `[ ]` → `[x]` only when **you** finished that row.  
3. Fill **Proof** with a path, date, or one-line note.  
4. **Gallery slide labels:** Pass **A** = empirical; Pass **B** = **λ** in score; Pass **C** = **ρ** in assignment (`So_Far_.pptx` slides 1–3).  
5. **Score on Model slide:** \(S_i = A_i - \lambda L_C\) (\(\lambda > 0\)).

**Mission (one line):** Vary **one knob at a time** at the **539 baseline**; show how **both curves** move (binned by **A_i** and by **poolq_loo / L_C**). Not curve-fitting to the empirical Hero yet.

**Not this file:** Agent status in `model_OPORD.md`, doc 03, COMPASS stubs.

---

## Locked — gallery already on disk (do not redo unless asked)

| Slide | Pass | Status |
|-------|------|--------|
| 1 | Pass A — empirical talent vs poolq_loo | Use `PASS_A_empirical_*` in `HEROs_and_PASSes/` |
| 2 | Pass B — λ knockout | Use `PASS_B_generative_lambda_knockout_*` |
| 3 | Pass C — ρ ablation | Use `PASS_C_rho_ablation_*` |
| 4 | Model (hand-edited) | You maintain `re_entry/Model.pptx`; script refreshes slides 1–3 only |

Refresh deck: `./scripts/rebuild_hero_gallery.sh` (passes-only merge; slide 4 untouched).

---

## Phase A — Gallery honesty (~1–2 days)

Alex “puzzle pieces” before the full characterization deck.

| Done | Step | What to do | Proof |
|------|------|------------|-------|
| [ ] | **λ ablation panel** | Fix ρ; vary λ (four λ values at one fixed ρ — mirror Pass C layout) | PNG path |
| [ ] | **Sim double-plot** | One run (λ≈0.55, ρ fixed): **left** = 16 bins on **A_i**; **right** = 16 bins on **poolq_loo** | PNG path |
| [ ] | **λ overlay** | On **A_i-binned** side: overlay λ=0 vs λ>0 | PNG path |
| [ ] | **Sort-and-chop** | Put sort-and-chop arm back on Pass C ρ figure | PNG path |
| [ ] | **Fitted inputs** | On slides: report **t_j** distribution, σ²; mark data-fitted (t̃) vs sim-drawn | slide / note |
| [ ] | **Refresh So_Far_** | `./scripts/rebuild_hero_gallery.sh`; open in **PowerPoint** (not Cursor preview) | date |

**Phase A done when:** `So_Far_.pptx` slides 1–3 reflect the above; you can walk Alex through them.

---

## Phase B — Characterization deck (~4 days; ~2 knobs/day)

**Slide template (each knob):** three core equations at top → **bold the knob** → figure(s) with **both curves**.

**OAT caveat:** One knob alone may not produce the Hero curve; ρ and λ may need each other. If a marginal sweep looks flat, check baseline; consider a **ρ × λ** panel at checkpoint.

| Done | Knob | What to deliver | Proof |
|------|------|-----------------|-------|
| [ ] | **ρ** | OAT sweep; Pass C is the start — “matters a lot” | slide + 1-sentence claim |
| [ ] | **λ** | OAT sweep; extend Pass B to full panel | slide + 1-sentence claim |
| [ ] | **Checkpoint Alex** | After ρ + λ: review slides; ask about ρ × λ if needed | date / notes |
| [ ] | **θ** (sigmoid center) | Sweep; note tie to **K/N** (success rate), not “median of selected” | slide |
| [ ] | **γ** (sigmoid slope) | Sweep | slide |
| [ ] | **A_i distribution** | Robustness: default + 1–2 alternatives (SI note) | slide or SI list |
| [ ] | **t_j distribution** | Fix from empirical ballpark; brief sensitivity | slide |
| [ ] | **K/N** | System feature: high vs low selectivity regimes | slide |

**Done with each knob when:** you can state (1) what was fixed, (2) what varied, (3) what happened to **both curves**, (4) whether it matters for the story.

**Phase B done when:** characterization deck is ready; Alex agrees you characterized the model (not fit to data yet).

---

## Phase C — Parked until after Phase B

Do **not** start until Phase B checkpoint clears.

| Done | Step | Pointer | Proof |
|------|------|---------|-------|
| [ ] | **PD14 magnitude** | [`05_Alex_Magnitude_Spec.md`](05_Alex_Magnitude_Spec.md) — Model A vs B predictive importance | |
| [ ] | **Statistical ρ̂, λ̂** | Estimators from **data statistics** — not Hero curve matching | |
| [ ] | **Notation cleanup** | Fix σ used twice (team σ_j vs sigmoid); separate if needed | Model.pptx |

---

## Explicitly not on this checklist

- Rebuild empirical hero from `530`
- Bin-for-bin LOO match as a gate
- B vs D decomposition (use **L_C** only for now)
- Army / tenure figures
- Old 14-doc reading stack

Park list: [`PARKED_FOR_LATER.md`](PARKED_FOR_LATER.md).

---

## Next action right now

Start **Phase A** row 1 (**λ ablation panel**) unless `So_Far_.pptx` already needs a quick look in PowerPoint first.

When stuck: read [`PD15_notes.md`](../../transcripts/PD15_notes.md), then return here.
