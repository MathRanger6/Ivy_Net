---
name: Hero Model Reset
overview: "Validate the mental reset: three kinds of model, locked hero as fixed target, and the simplest score→select story that can bend a selection curve. Vocabulary locked Jul 2026 — environment ≠ advancement; score ≠ select; assignment uses ρ (not τ)."
todos:
  - id: memo-three-models
    content: "Draft 1-page memo: phenomenological LPM vs L_net theory vs generative sim — what each proves and does not"
    status: completed
  - id: hero-estimand-lock
    content: Confirm hero spec in writing (16 quantile, winsor 0.01–0.99, min_minutes=20, poolq_loo) as fixed target for all model tests
    status: completed
  - id: lpm-layer-a
    content: Run quadratic LPM on hero-filtered panel; record coef signs and overlay vs ventile bins
    status: completed
  - id: pass-a-lambda-knockouts
    content: "Pass A: λ>0 vs λ=0 scoring knockout; same 16-bin readout (hero_model_reset_bundle → alex_side_by_side_v0)"
    status: completed
  - id: alex-side-by-side
    content: Produce side-by-side figure + nesting-note limitation sentence for Alex (empirical hero + generative POC)
    status: completed
  - id: pass-b-rho-ablation
    content: "Pass B: ρ ablation (low/moderate/high + sort-and-chop) via 540_rho_ablation_bundle → alex_rho_ablation_v0"
    status: completed
  - id: defer-stretch
    content: Explicitly park bin-for-bin LOO match and preferential attachment as stretch, not v1 gate
    status: completed
isProject: false
---

# Hero inverted-U: model types, testing, and smart restart

**Synced vocabulary:** 2026-07-28 — matches [`BINDING_Selection_is_its_own_step.md`](../BINDING_Selection_is_its_own_step.md) and [`re_entry/02_Three_Kinds_of_Model.md`](../re_entry/02_Three_Kinds_of_Model.md).  
**Living sim lab:** [`sports/540_READ_ME_SIM.md`](../../sports/540_READ_ME_SIM.md) / `540_three_step_sim.ipynb` (538D archived under `sports/archive/`).

## Short answer: yes, your approach makes sense

You are doing the right thing by stepping back. The project distinguishes **phenomenon → theory → generative POC** ([`05_Model_Nesting_Note_v1.md`](../../5-Manuscript/05_Model_Nesting_Note_v1.md), [`30_Alex_Gates_inform_status_outline.md`](../30_Alex_Gates_inform_status_outline.md)). Confusion is mostly **which layer you are trying to “solve” at once**, plus older docs that said “selection” for the score equation. Splitting layers — and **score ≠ select** — is the smart move.

**Re-entry path if lost:** [`re_entry/00_READ_ME_FIRST.md`](../re_entry/00_READ_ME_FIRST.md) → 01 → 02 → 03.

---

## 1. What “mathematical model” means here (three different objects)

In everyday conversation we say “the model” as if there is one thing. In this project there are **three different objects**, and mixing them up is the main source of confusion. Each answers a different question. None of them, by itself, is the whole dissertation story.

---

### The three layers in plain language

| Layer | Plain-language name | What you are actually doing | What a successful result looks like |
|-------|---------------------|----------------------------|-------------------------------------|
| **A. Phenomenological / reduced form** | **“Describe the curve in the data”** | Fit a simple functional form to real player-season rows — e.g. does draft probability bend downward at the top when you plot it against leave-one-out pool quality? | You can show, on the **locked hero spec**, that draft rate rises and then dips (or is concave) when you smooth or bin the empirical panel. You get coefficients and a picture. |
| **B. Structural / mechanism (theory)** | **“Explain why help and hurt can coexist”** | Write down a story in symbols: net learning has a benefit part and a congestion part; **scoring** may penalize crowding among viable peers, not just reward raw ability; then a **winner rule** picks who advances. | The story is internally consistent, maps to named objects in the code (`A_i`, congestion `L_C`, weight `λ`, winner rule top K), and suggests **ingredient tests that can falsify the claim** (e.g. “if congestion does not enter the **score**, the sim story fails”). |
| **C. Generative / simulation - Data Generating Process (DGP)** | **“Build a fake league and see if the rule produces a bent curve”** | Simulate rosters: draw ability, **assign** players to teams (`ρ`), **score** candidates (`S_i`), **select** top K, then bin and plot **who got selected** vs a pool statistic. | Under a **minimal rule set** (score includes congestion, scarce slots), the **shape** of the simulated selection curve differs from talent-only scoring — e.g. elite bins compress relative to ability-only. |

**Do not use one word (“the model”) for all three.** Layer A is a **statistical summary** of MBB data. Layer B is **economic/statistical narrative** about mechanisms. Layer C is a **computerized thought experiment** that operationalizes part of Layer B.

---

### Layer A — phenomenological (the hero and the quadratic LPM)

**Question it answers:** *Does an inverted-U-shaped (or concave) relationship between pool quality and draft probability show up in the real NCAA→NBA panel on a fixed, pre-specified definition of “quality”?*

**What it is not:** A claim that NBA teams literally maximize a particular formula, or that we have identified *why* the curve bends.

**Concrete objects in the repo:**

- **Hero plot** — binned mean draft rate (`Y_draft`) vs **`poolq_loo`**: each player’s leave-one-out mean teammate performance (teammates’ box-score quality with that player removed so they are not counted twice).
- **Quadratic LPM (linear probability model)** — OLS on the same filtered rows (not linear programming):  
  `Y_draft ~ β₀ + β₁·poolq_loo + β₂·poolq_loo²`  
  wired in [`panel_build.py`](../../sports/sports_pipeline/panel_build.py) (`draft_poolq_quadratic_coeffs`, ventile overlay in 530).

**Why keep the quadratic:** `β₂ < 0` ⇒ fitted curve **concave down**; one turning point `Q* = −β₁/(2β₂)` (local max if `β₂ < 0`). No inflection on a pure quadratic. Claims are about the **fit**; binned hero stays the stylized fact. See also [`re_entry/02`](../re_entry/02_Three_Kinds_of_Model.md) Layer A.

**What “test” means here:** Check sign and magnitude of **`β₂`** (negative ⇒ concave / inverted-U tendency); compare the smooth curve to **ventile bin means** visually; optional out-of-sample checks. You are **fitting the phenomenon**, not simulating a league.

**What Layer A proves:** The stylized fact is **real on the locked estimand** (16 quantile bins, winsorized `poolq_loo`, `min_minutes=20`, etc.).  
**What it does not prove:** Mechanism, causal effects, or that any NBA front office uses this score.

---

### Layer B — structural / mechanism (theory spine)

**Question it answers:** *Why is it plausible that being on a “good” team pool could both help and hurt draft odds?* — and **why describing the environment is not the same as deciding who advances.**

**What it is:** Prose and notation — not one estimated equation in v1. **Keep three separations** (BINDING):

**Part 1 — Environment (`L_net = B(·) − D(·)`):** Peers confer benefit (B) and congestion (D) on net development / value in the environment. This **describes the pool**, not who gets drafted.

**Part 2 — Scoring (Alex score):** **`S_i = A_i − λ·L_C`**. Congestion enters **ranking**, jointly with ability **`A_i`**. **`λ` lives here.** This is **not** the full reduced-form environment and **not** the hero regression.

**Unified nest (Alex v1):** With `(B − D) = −L_C` in the congestion channel used for ranking,

\[
S_i = A_i + \lambda(B - D) = A_i - \lambda \cdot L_C.
\]

Knockout: **`λ = 0`** ⇒ **`S_i = A_i`** (talent-only score).

**Part 3 — Selection (winner rule):** Given scores, **who wins?** v1 default = **top K**. Later can be soft / noisy / stochastic. **Do not call `S_i` “selection.”** Score ≠ select.

**Charles binding (Jul 2026):** [`BINDING_Selection_is_its_own_step.md`](../BINDING_Selection_is_its_own_step.md)

**What “test” means here:** Narrative consistency + sim **scoring knockouts** — e.g. **`λ = 0`** (ability-only score, same top-K) and ask whether the generative story still holds.

**What Layer B proves:** A coherent **mechanism vocabulary** and falsifiable **directional** claims (congestion in the **score** can matter).  
**What it does not prove:** Separate identification of **`B(Q)`** and **`D(Q)`** as functions of one axis in v1, or that the real NBA implements **`S_i`** literally.

---

### Layer C — generative simulation (the DGP)

**Question it answers:** *If we write down an explicit **data-generating process** — artificial players, teams, and a draft rule — does a **minimal** congestion term in the **score** change the **shape** of who gets picked when we bin by pool quality?*

**DGP** = **data-generating process**: the full recipe that **creates** synthetic rosters and draft outcomes, as opposed to fitting a curve to real outcomes after the fact.

**Three-step pipeline (locked):**

1. **Assign** — soft match ability to team types **`T_j`** with user-facing assortativity **`ρ`** (σ fixed ~0.65). Preferential attachment = optional boolean, default **off**. Legacy docs used **`τ`** for temperature (opposite intuition) — treat **`τ` as archived notation only**.
2. **Score** — e.g. **`S_i = A_i − λ·L_C`** (or ability-only when `λ = 0`). Soft crowding inside **`L_C`** (viability sigmoid) is **not** assignment softness and **not** selection noise.
3. **Select** — **top K** draft slots (scarce winners). Later: stochastic draw from scores without renaming the score “selection.”

**Concrete stack in the repo:**

- **Living lab:** [`540_READ_ME_SIM.md`](../../sports/540_READ_ME_SIM.md), `540_three_step_sim.ipynb`, engines under `sports/sports_pipeline/tier1_*.py`.
- **Pass A exports:** `hero_model_reset_bundle.py` → `alex_side_by_side_v0/` (λ knockout).
- **Pass B exports:** `540_rho_ablation_bundle.py` → `alex_rho_ablation_v0/` (ρ levels + sort-and-chop diagnostic).
- **Archived:** 538D and sibling labs under `sports/archive/` — historical source of Pass A lessons; not the open workspace.

**What “test” means here:** Re-run the DGP with knobs toggled; compare **curves**, not regression **`R²`** on real data. Headline knockout (Pass A): **`λ > 0`** (congestion in score) vs **`λ = 0`** (talent-only score), **same top-K** — does the elite tail behave differently?

**What Layer C proves:** A **minimal artificial league** where talent-only **scoring** is **not enough** and a congestion term in the score **can** bend who gets selected — proof-of-concept for Alex’s mechanism.  
**What it does not prove:** Bin-for-bin replication of every hero ventile rate, or that the real draft **is** this sim.

---

### How the three layers relate (read this before the diagram)

```mermaid
flowchart TB
  subgraph rung1 [Rung1_Empirical]
    Hero["Hero plot: mean draft rate vs poolq_loo ventiles"]
    LPM["Quadratic LPM overlay optional"]
  end
  subgraph rung2 [Rung2_Generative]
    Assign["Assign: A_i, T_j, rho"]
    Score["Score: S_i = A_i - lambda L_C"]
    Select["Select: top-K winner rule"]
    SimPlot["Binned P selected vs pool feature"]
  end
  subgraph theory [Theory_spine]
    Lnet["L_net = B minus D"]
  end
  Hero --> LPM
  theory --> Score
  Assign --> Score --> Select --> SimPlot
  Hero -.->|"shape comparison honest axis"| SimPlot
  Lnet -.->|"frames why not only A"| Score
```

**Reading the diagram:**

- **Top path (Rung 1):** Start from **real MBB data** → hero bins + optional quadratic overlay. This is Layer **A**. No simulation required.
- **Middle path (Rung 2):** Start from **rules** → assign → score → select → binned plot. This is Layer **C**. The sim **tests the rule**, not the regression.
- **Theory box:** Layer **B** sits **between** interpretation and design — it explains why **scoring** might use **`A − λL_C`**, not only **`A`**, but it does not by itself produce numbers until wired into Layer C (or decomposed empirically later at Rung 2.5).

**Alex side-by-side (what v1 actually delivers):** Layer **A** hero PNG + Layer **C** sim PNG, same **Y** (advancement / draft rate), **honest X** labels (empirical LOO quality vs sim bins on the best available matching axis), plus an explicit **limitation sentence** — not “derive the hero from a closed-form integral.”

---

### One paragraph to keep in memory

**Layer A** can reproduce an inverted-U **without telling you why** — it is curve-fitting and binning on the real panel (**outcomes only**). **Layer B** splits **environment** (B − D) from **advancement** (score then select). **Layer C** runs **assign → score → select** in code and shows talent-only **scoring** is insufficient under a fixed winner rule. You need **A** for the empirical fact, **B** for the dissertation logic (environment ≠ advancement; score ≠ select), and **C** for the claim that **congestion in the score** can bend curves — three jobs, three objects.

---

## 2. Does simulation test a formula?

**Yes — when the formula is a generative rule**, not when it is only a regression fit.

- **Simulation tests:** “If we **score** with `S_i = A_i − λ·L_C`, **select** top K, and rosters form this way, does **P(selected)** bend non-monotonically when we bin by a pool statistic?”
- **Regression tests:** “Does `P(draft | poolq_loo)` look quadratic in the **real panel**?” (already wired in 530)

Both are legitimate; they answer **different questions**. Simulation is **not** required to *draw* an inverted-U (a quadratic fit can do that). Simulation **is** required for the Wang-style claim: **talent-only scoring is not enough; a congestion term in the score changes who gets selected** (Pass A: λ=0 vs λ>0).

---

## 3. Your two simplification strategies — which to use when

### (a) Top-down: full mechanism → drop until it breaks

**Best for:** Layer B/C — Alex score, assignment, winner rule.

**Procedure:**
1. Start with the **full generative stack** you already built (ability draw, soft assign with `ρ`, congestion in score, top-K).
2. Fix **one empirical anchor** (hero spec below).
3. Remove or zero one ingredient at a time and record **what breaks**:
   - `λ = 0` → talent-only **score** (should flatten / fail congestion story) — **Pass A**
   - change `ρ` (or sort-and-chop diagnostic) → changes pool overlap / tail bins — **Pass B**
   - no `L_C` term, only `A_i` → scoring on ability alone

This is **mechanism identification in the sim**, not coefficient estimation on real draft data.

### (b) Bottom-up: minimal curve → decompose

**Best for:** Layer A — describing the hero.

**Procedure:**
1. Start with **simplest curve**: `E[Y | Q] = β₀ + β₁Q + β₂Q²` with `β₂ < 0` (530 LPM).
2. Decompose **Q** (`poolq_loo`) into interpretable pieces only when moving to Rung 2.5:
   - `poolq_loo` ≈ quality column (B-ish mix)
   - `crowding_smooth` ≈ congestion column (D-ish) — CELL 5d in [`530_sports_pipeline.ipynb`](../../sports/530_sports_pipeline.ipynb)

**Recommendation:** Use **both**, in order: **bottom-up for the hero (A)**, **top-down for the sim (C)**. They are not competing; they are different rungs.

---

## 4. Assortative grouping, ρ, etc. — simulation details or essentials?

**Mostly simulation / DGP details** — not the core mathematical claim.

| Knob | Role | Needed for v1 Alex side-by-side? |
|------|------|----------------------------------|
| **`λ` / congestion in score** | Core mechanism ingredient | **Yes** (Pass A done) |
| **Top-K selection** | Scarcity of draft slots (winner rule) | **Yes** (conceptually) |
| **Soft assignment (`ρ`, `T_j`)** | How players land on teams | **Helpful** for realistic pool overlap; not the headline theorem (Pass B diagnostic done) |
| **Sort-and-chop benchmark** | Hard assortative diagnostic | **Diagnostic only** — **not** `ρ → ∞` |
| **Preferential attachment** | Boolean roster feedback | **Off by default**; stretch |
| **Empirical team distribution on/off** | Faithful historical sweeps | **Stretch / amplitude** — not gate for “minimal POC” |

**Notation trap (archived):** Older plans/labs used **`τ`** for assignment temperature. **User-facing knob is `ρ` (assortativity).** Soft crowding parameters inside `L_C` are a different softness — do not reuse “τ” for both.

Path II (locked in nesting note): generative figure may use **pool mean** on X while empirical hero uses **`poolq_loo`**. Say that aloud; do not over-fit assortativity until the **minimal** scoring story works.

**Stretch goal (parallel, not v1 gate):** match hero on **`poolq_loo`** with same binning ([`alex_side_by_side_v0/`](../../sports/datasets/mbb/exports_inverted_u_v0/alex_side_by_side_v0/) spec: 16 quantile, winsor 0.01–0.99, `min_minutes=20`).

---

## 5. Do you need simulation? Why?

| Goal | Need sim? |
|------|-----------|
| Show inverted-U exists in MBB data | **No** — hero is done |
| Fit a smooth curve through bins | **No** — quadratic LPM |
| Explain *why* help and hurt can coexist | **Partly prose** (`L_net = B − D`) |
| Show **congestion in the score** is a plausible **minimal ingredient** | **Yes** — sim with **λ knockout** (Pass A / 540 stack): congestion in score vs talent-only, **same top-K** |
| Prove **identification of B(Q) and D(Q)** separately on one axis | **No** — explicitly deferred in v1 |

**Why sim exists in your project:** Alex’s score is a **ranking rule for an artificial league**, not a claim that real NBA teams optimize `S_i`. Simulation is how you **operationalize and stress-test** that rule (then apply a winner rule) — including the **knockout** that can falsify the congestion-in-score claim. It is the supplement; the hero is the spine.

---

## 6. What is probably a “keeper” vs what can wait

**Keep (solid foundation):**
- Locked hero triplet + [`530`](../../sports/530_sports_pipeline.ipynb) panel/LOO pipeline
- Nesting note + Alex brief axis honesty + BINDING + re_entry 00–03
- **540** three-step sim + Pass A (`alex_side_by_side_v0/`) + Pass B (`alex_rho_ablation_v0/`)
- Sensitivity lessons in [`Pertinent_Thoughts_Scout.md`](../../sports/documents/Pertinent_Thoughts_Scout.md) (`min_minutes`, quantile vs equal-width)
- Archived 538D lessons (do not reopen as daily workspace)

**Defer / shrink (avoid re-blocking):**
- Bin-for-bin LOO replication as **v1 requirement**
- Large faithful historical sweeps on Rivanna until minimal score→select story stays locked
- HS binning, multiplicative rewrite, full `B(Q)−D(Q)` estimation
- Preferential attachment on; denser assortativity grids beyond Pass B diagnostics

---

## 7. Recommended sequence (status as of Jul 2026 sync)

1. **Write one page “three models” memo** — **done** ([`Hero_Model_Three_Layers_Memo.md`](../../sports/documents/Hero_Model_Three_Layers_Memo.md); re_entry 02 is the Charles-facing version).
2. **Freeze hero estimand** — **done:** 16 quantile, ppm z-scored, winsor (0.01, 0.99), `min_minutes=20`, 2011–2021, `poolq_loo`, draftee filter off.
3. **Layer A check** — **done:** quadratic LPM on same filtered rows.
4. **Pass A (λ knockout)** — **done:** `λ>0` vs `λ=0`, same bin count; side-by-side in `alex_side_by_side_v0/`.
5. **Pass B (ρ ablation)** — **done:** low / moderate / high `ρ` + sort-and-chop diagnostic in `alex_rho_ablation_v0/`.
6. **Alex slide:** side-by-side PNGs + one limitation sentence from nesting note §4 — **ready**.
7. **Only then** revisit preferential attachment / faithful sweeps if LOO match still matters scientifically.

---

## 8. One-sentence answers to your numbered questions

1. **Recreate inverted-U:** Yes — via **quadratic reduced form** (easy) and/or **generative scoring with congestion + top-K select** (mechanism); full `B−D` decomposition is theory, not yet a single estimated formula.
2. **What is a model / how tested:** Three layers (table above); simulation tests **generative rules** (assign → score → select), regression tests **empirical curve**, theory frames **interpretation**.
3. **Top-down vs bottom-up:** Use **both** — bottom-up for hero fit, top-down for sim mechanism stripping.
4. **Assortativity (`ρ`) etc.:** Mostly **simulation plumbing**; not the v1 theorem. Sim is needed for **minimal mechanism POC**, not for proving the hero exists.
5. **Reset smart?** **Yes.** Keep infrastructure; re-order claims around rungs; stop requiring one formula to do all jobs; keep **score ≠ select** in every write-up.
6. **Approach correct?** **Yes**, with one guardrail: **do not make bin-for-bin LOO sim match the gate for “we have a model.”** That is north-star R&D, not the definition of success for the next Alex conversation.
