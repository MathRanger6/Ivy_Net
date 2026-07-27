# 3. Three-day basketball focus

**Audience:** Charles — deadline pressure  
**Goal:** One clear “done” for the simplified model, without scope creep.  
**Status (2026-07-27):** Re-entry bar **reached** — narrative, slide (`Model.pdf`), Alex Pass A bundle on disk. **Pass B (ρ ablation)** in progress via `540_*` — see [`model_OPORD.md`](model_OPORD.md).

---

## What “done” means (72-hour bar)

**Binding check:** You can say in one breath: *Hero = outcome; **environment** = `L_net` (B − D, peers help and hurt); **selection** = `S_i` (Alex score — who gets the slot); sim = test congestion in **selection**, not one giant environment model.* ([`../BINDING_Selection_is_its_own_step.md`](../BINDING_Selection_is_its_own_step.md))

You can stop spiraling when you can honestly say all four:

1. **I can explain the hero** in one minute (doc 01) — including **talent baseline** vs **hero** (two empirical axes).
2. **I can explain three layers** without merging them — unified nest **`S_i = A_i + λ(B−D)`**, Alex v1 **(B−D)=−L_C**, knockout **λ=0** (doc 02).
3. **I have a side-by-side figure**: empirical hero + generative sim, same advancement rate on Y, labeled axes.
4. **I have one limitation sentence** ready for Alex (below — copy when needed).

You do **not** need: bin-for-bin sim match, Rivanna sweeps, **τ** calibrated to 530, tenure figures, manuscript Word inking, or refreshed Army plots in this window.

---

## Minimal model for Alex’s intent (v1 — what he asked for)

| Piece | What it is | Status |
|-------|------------|--------|
| **Empirical phenomenon** | **Naïve:** P(draft \| own **A_i**) ≈ monotone; **Hero:** P(draft \| **PoolQ_LOO**) with tail dip | Done (530; doc 01) |
| **Two-step generative** | **(1)** assign to pools (**ρ**); **(2)** **S_i → top K** | `540_*` + `Model.pdf` |
| **Unified selection** | **`S_i = A_i + λ(B−D)`**; Alex v1: **(B−D)=−L_C** ⇒ **`S_i = A_i − λ·L_C`** | Locked (doc 02) |
| **Headline sim test** | **Knockout λ=0** (**S_i = A_i**) vs congestion in score — same league | **Done** (`hero_model_reset_bundle.py`) |
| **Side-by-side + limits** | Empirical + generative PNG; no bin-for-bin claim | **Done** (export folder) |
| **ρ ablation** | Vary assignment assortativity, **fix** selection rule — “is sorting involved?” | **Pass B** — `540_rho_ablation_bundle.py` |

**One line for Alex:** *Hero is the stylized fact; the minimal generative proof is congestion **in the selection score** (Pass A knockout done); **ρ** ablation tests whether assignment sorting moves the readout with selection held fixed.*

---

## Limitation sentence (v1 — use as-is or lightly edit)

> The empirical stylized fact uses leave-one-out teammate quality among college players; the generative proof-of-concept selects on a score that penalizes leave-one-out viable-peer congestion and plots binned selection rates on a matching quality axis. We do not claim bin-for-bin reproduction of every ventile in v1; we claim that talent-only selection is insufficient and that congestion in the score can bend advancement curves in a disciplined artificial league.

---

## What is already built (do not rebuild from scratch)

| Piece | Status | Where |
|-------|--------|--------|
| Empirical hero (Layer A) | Done | `530`; `sports/datasets/mbb/exports_inverted_u_v0/alex_side_by_side_v0/` |
| Quadratic LPM (β₂ < 0) | Done | `lpm_hero_coefficients.txt` in export folder |
| Generative knockouts (λ=0 vs congestion) | Done | `generative_knockout_*_16quantile.csv`; script `sports/scripts/hero_model_reset_bundle.py` |
| Side-by-side PNG | Done | `inverted_u_side_by_side_empirical_vs_generative.png` |
| Narrative slide | Done | [`Model.pdf`](Model.pdf) / `Model.pptx` |
| Plain readout | Done | `generative_knockout_summary.txt`, `side_by_side_caption.txt` |

Re-run bundle if needed: `python sports/scripts/hero_model_reset_bundle.py`

---

## Five-minute self-test (you’re done when these pass)

1. **Hero (60 s):** Naïve vs Hero; tail dip is **outcome on pool axis**, not “NBA ignores talent.”
2. **Binding (20 s):** doc 03 binding sentence or `Model.pdf` opener.
3. **Knockout (20 s):** same league; **λ=0 → S_i=A_i**; else **S_i=A_i−λL_C** with **(B−D)=−L_C**.
4. **Open side-by-side PNG** — left empirical, right generative; one honest limit.
5. **Read limitation sentence** once without hedging.

---

## Suggested schedule (if still orienting)

### Day 1 — Layer A

- Empirical hero PNG + doc 01; describe tail dip and **talent baseline**.

### Day 2 — Layer C (selection knockout)

- Side-by-side PNG + knockout CSVs; **λ** toggles **`L_C` in selection**, not **ρ**.

### Day 3 — Package for Alex

- **`Model.pdf`** + side-by-side + limitation sentence (email or brief).

---

## Pass B: ρ sims (assignment ablation)

**Question:** Is assortative grouping (**ρ**) involved? **Answer:** Yes in the **full** story (step 1 — who lands where); **not** the minimal proof that congestion in **selection** matters (Pass A — **λ / L_C**, already run).

**Run:** hold **S_i** fixed (**λ**, **L_C** rule); vary **ρ** (low vs high) + sort-and-chop benchmark; same 16-bin readout on **poolq_loo**. Script: `python sports/scripts/540_rho_ablation_bundle.py`. See [`../../sports/540_READ_ME_SIM.md`](../../sports/540_READ_ME_SIM.md).

---

## Explicitly out of scope (park guilt here)

- Bin-for-bin replication of hero ventiles from simulation
- Separate estimation of benefit vs congestion on one axis
- **ρ** calibrated to match hero before minimal story is sent
- Multi-domain Λ sweeps (Army slot capacity)
- Tenure Cox / Setting 3 prose
- Re-reading agent correspondence rounds

---

## If you get pulled into cross-references again

**Rule:** Close the tab. Return to [`00_READ_ME_FIRST.md`](00_READ_ME_FIRST.md).

Agents: when Charles is in re-entry, **do not** point him at `Charles_reading_list.md` items 1–14, Pertinent Thoughts, or nesting note until he finishes re_entry 01–03.

---

## One paragraph to end the reset

You started over because the **reference surface** exceeded your **working memory**. The science for Alex v1 is **on disk** and **in your slide**. Remaining work is **Pass B ρ packaging** (optional with Pass A) and Alex presentation — not re-deriving the model. Everything else waits in [PARKED_FOR_LATER.md](PARKED_FOR_LATER.md).

When you want depth beyond the slide, see `3-Master_Plan/plans/20260721_hero_model_reset.plan.md` — not before doc 02 feels easy.
