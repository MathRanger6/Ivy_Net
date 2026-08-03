# ARCHIVED — superseded 2026-08-03

**Replaced by:** [`CHARLES_CHECKLIST.md`](CHARLES_CHECKLIST.md) (Paper Directions 15 — characterization mission).

**Why archived:** Re-entry + Pass A/B redo + PD14 magnitude scaffold did its job. Alex PD15 (Jul 31, 2026) reframed the mission as **directed sensitivity characterization** (~4 days), then statistical fitting — not the old onboarding path.

**Source notes:** [`../../transcripts/PD15_notes.md`](../../transcripts/PD15_notes.md)

---

# Charles checklist — re-entry (manual checkoff)

**Last synced:** 2026-07-30

**Created:** 2026-07-28 16:58  
**Purpose:** The **one** place you walk beginning → end and mark **what you personally did**.  
**Not this file:** Agent “already done” tables in `model_OPORD.md`, doc 03, COMPASS stub, or the hero reset plan. Those are **project/agent status**. This file is **your** progress.

**How to use**

1. Work **top to bottom**.  
2. Change `[ ]` → `[x]` only when **you** finished that row.  
3. Fill **Proof** with a path, date, or one-line note.  
4. **Do not rebuild** the empirical hero (Layer A panel) unless you choose to later.  
5. **Do re-run** generative Pass A and Pass B yourself so you own the sim story.

**Companion reads (check when true):** docs `00`–`03`, then **`04_Pass_A_and_Pass_B_in_Plain_English.md` before any sim redo**. Optional depth: hero reset plan, Three Layers memo, `Model.pdf`. After doc 04, optional shorthand: `540_READ_ME_SIM.md`.

---

## 0. Orientation (reading)

| Done | Step | Proof (you fill) |
|------|------|------------------|
| [ ] | Read `00_READ_ME_FIRST.md` | |
| [ ] | Read `01_The_Problem_in_Plain_English.md` | |
| [ ] | Read `02_Three_Kinds_of_Model.md` | |
| [ ] | Read `03_Three_Day_Basketball_Focus.md` | |
| [ ] | Read hero reset plan (optional depth) | |
| [ ] | Read Three Layers memo (optional card) | |
| [ ] | Skim `Model.pdf` (your slide) | |

---

## 1. Self-test (no code) — you’re oriented when all pass

Say each out loud. Check only when you can, without hedging.

| Done | Step | Proof |
|------|------|-------|
| [ ] | **Hero:** talent baseline (own A) vs hero (poolq_loo); cliff at elite end is **outcome**, not “NBA ignores talent” | |
| [ ] | **Binding:** environment `L_net = B−D` ≠ advancement; advancement = **score** (`S_i`, λ) then **select** (top K) | |
| [ ] | **Nest:** `S_i = A_i + λ(B−D)` with Alex v1 `(B−D)=−L_C` ⇒ `S_i = A_i − λ·L_C`; knockout λ=0 ⇒ `S_i = A_i` | |
| [ ] | **Hero shape honesty:** peak ~bin 12, high/wobble 13–15, **cliff at bin 16** (not “only bin 16 ever falls”) | |
| [ ] | Read limitation sentence in doc 03 once, cold | |

---

## 2. Skip — empirical hero (Layer A)

You are **not** rebuilding these. Treat as locked inputs.

| Status | Artifact | Path |
|--------|----------|------|
| Use as-is | Hero PNG | `re_entry/HEROs_and_PASSes/HERO_inverted_u_empirical_ppm_poolq_loo_16quantile_winsor0199_min20_2011.png` |
| Use as-is | Hero CSV | `re_entry/HEROs_and_PASSes/PASS_A_binned_draft_rate_empirical_ppm_poolq_loo_16quantile_winsor0199_min20_2011.csv` |
| Optional open | LPM coefs | `re_entry/HEROs_and_PASSes/PASS_A_lpm_hero_coefficients.txt` |

| Done | Optional (only if you want) | Proof |
|------|------------------------------|-------|
| [ ] | Open hero PNG + CSV; confirm peak ~12 / cliff at 16 yourself | |

---

## 2b. Bridge — read before any sim redo (required)

**Stop.** Do not open the 540 notebook expecting it to teach Pass A/B. Read the plain-English bridge first.

| Done | Step | Proof |
|------|------|-------|
| [ ] | Read [`04_Pass_A_and_Pass_B_in_Plain_English.md`](04_Pass_A_and_Pass_B_in_Plain_English.md) | |
| [ ] | Can say in your own words: hero = empirical; Pass A/B = simulated league | |
| [ ] | Can say what Pass A changes vs what Pass B changes | |
| [ ] | Optional after 04: skim `sports/540_READ_ME_SIM.md` (shorthand OK now) | |

---

## 3. Sim redo — Pass A — **you run this**

**Full explanation:** doc **04**. Short reminder: same fake league setup and same top-K; one arm scores on ability only; the other puts congestion in the score.

**What you run:** `python sports/scripts/hero_model_reset_bundle.py` (from repo root).  
**Notebook:** `sports/540_three_step_sim.ipynb` is optional display / can call the scripts — it is **not** the full simulator by itself.

| Done | Step | What to do | Proof |
|------|------|------------|-------|
| [ ] | Run Pass A bundle | From **repo root:** `python sports/scripts/hero_model_reset_bundle.py` | date + exit 0 |
| [ ] | Inspect talent-only CSV | `HEROs_and_PASSes/PASS_A_generative_knockout_talent_only_16quantile.csv` — monotone rise? | |
| [ ] | Inspect congestion CSV | `HEROs_and_PASSes/PASS_A_generative_knockout_congestion_16quantile.csv` — elite compression vs talent-only? | |
| [ ] | Inspect side-by-side PNG | `HEROs_and_PASSes/PASS_A_inverted_u_side_by_side_empirical_vs_generative.png` | |
| [ ] | Read summary + caption | `PASS_A_generative_knockout_summary.txt`, `PASS_A_side_by_side_caption.txt` | |
| [ ] | One-sentence claim (yours) | Write: what Pass A proves / does **not** prove | |

**Pass A done for you when:** you ran the script, looked at both knockout arms + PNG, and can state the claim without reading notes.

---

## 4. Sim redo — Pass B — **you run this**

**Full explanation:** doc **04**. Short reminder: score + top-K fixed; only assignment assortativity (ρ) / sort-and-chop changes.

| Done | Step | What to do | Proof |
|------|------|------------|-------|
| [ ] | Run Pass B bundle | From **repo root:** `python sports/scripts/540_rho_ablation_bundle.py` | date + exit 0 |
| [ ] | Inspect arms | `HEROs_and_PASSes/PASS_B_generative_*_16quantile.csv` (low / moderate / high / very_high / sort_chop) | |
| [ ] | Inspect PNG | `HEROs_and_PASSes/PASS_B_rho_ablation_selection_by_poolq_loo.png` | |
| [ ] | Read summary + caption + README | `PASS_B_rho_ablation_summary.txt`, `PASS_B_rho_ablation_caption.txt`, `PASS_B_README.txt` | |
| [ ] | One-sentence claim (yours) | Sorting can matter for pools; **not** the minimal congestion-in-score proof; not hero bin-for-bin | |

**Pass B done for you when:** you ran it and can separate Pass A vs Pass B in one breath.

---

## 5. Alex magnitude — predictive importance (Paper Directions 14)

**Full spec:** [`05_Alex_Magnitude_Spec.md`](05_Alex_Magnitude_Spec.md)  
**Transcript:** `transcripts/20260730_Paper_Directions_14_otter_ai_transcript.docx`  
**Reminder:** Hero ventile plot ≠ this task. Fit **Model A** (ability + poolq_loo + poolq_loo²) vs **Model B** (ability only); compare predicted draft probabilities and overall predictive gain.

| Done | Step | What to do | Proof |
|------|------|------------|-------|
| [ ] | Read spec + transcript skim | Doc **05**; confirm counterfactual = λ off in **prediction**, not rewound career | |
| [ ] | Run magnitude script (when exists) | From repo root: `python sports/scripts/hero_magnitude_predictive_comparison.py` (TBD) | date + exit 0 |
| [ ] | Inspect model comparison | `HEROs_and_PASSes/MAGNITUDE_model_comparison.txt` (when written) | |
| [ ] | Inspect per-person gaps | CSV: \(\hat{p}_i^{\text{full}}\), \(\hat{p}_i^{\text{ability}}\), \|Δ\| by ability ventile | |
| [ ] | One-sentence claim (yours) | “Roster in the model improves prediction by ___; largest at top ability / few slots because ___” | |

**Done for you when:** you can answer Alex’s “how much better is prediction with roster?” with numbers, not only the Hero curve shape.

---

## 6. Optional — see the pipeline in the notebook

| Done | Step | What to do | Proof |
|------|------|------------|-------|
| [ ] | Open `sports/540_three_step_sim.ipynb` | Paths + display of exports; set `RUN=True` only if you want re-run from cells | |
| [ ] | Skim `tier1_pool_assignment.py` | Find: `soft_assign` / `assignment_rho`, `assign_selection`, `choose_selected` | |
| [ ] | Skim `tier1_sim_config.py` | Find: `ASSIGNMENT_RHO`, score mode, `N_SELECTED`, viability θ/γ | |

---

## 7. Package for Alex (when sims feel like *yours*)

| Done | Step | What to do | Proof |
|------|------|------------|-------|
| [ ] | Assemble packet | `Model.pdf` + Pass A side-by-side PNG + Pass B PNG (optional) + limitation sentence (doc 03) | |
| [ ] | Dry-run the talk | 2–3 min: layers → Pass A knockout → (optional) Pass B → limits | |
| [ ] | Send / meet | Email or calendar | date |

---

## 8. Explicitly **not** on this checklist (park guilt)

Do **not** check these off here; they are out of scope until you decide otherwise:

- Rebuild empirical hero from `530`
- Bin-for-bin LOO match as a gate
- Rivanna / faithful historical sweeps
- Preferential attachment on
- Army / tenure figures
- Nesting note / Pertinent Thoughts / old 14-doc stack
- Fixing every “bin 16 only” prose line (nice polish; not blocking)

Park list: [`PARKED_FOR_LATER.md`](PARKED_FOR_LATER.md).

---

## Where other “done” lists live (ignore for checkoff)

| File | What it is |
|------|------------|
| `model_OPORD.md` | Ops order / agent phases (archive, ρ wiring, exports) |
| `03_Three_Day_Basketball_Focus.md` | “72-hour bar” + project status |
| `20260727_COMPASS_sim_reentry_status.md` | COMPASS stub |
| Hero reset plan §7 | Plan sequence status |

**Rule:** If a box here is unchecked, **you** still have work — even if another doc says “Done.”

---

## Next action right now

If sections **0–2** are checked: read **§2b / doc 04**, then start **§3** (Pass A script).

When stuck: return to [`00_READ_ME_FIRST.md`](00_READ_ME_FIRST.md), then come back **here**.
