# BINDING — Environment ≠ advancement; score ≠ select (Charles lock, Jul 2026)

**Status:** Binding for agents, re-entry docs, basketball v1, and manuscript framing.  
**Last sharpened:** 2026-07-28 — **scoring** and **selection** (winner rule) are separate pipeline steps.  
**Charles #1 confusion resolved:** Do **not** merge “describe the peer environment” with “who wins the scarce slot.”

**Filename note:** File kept as `BINDING_Selection_is_its_own_step.md` for stable links. “Selection is its own step” still means: advancement is **not** environment. Inside advancement, **score ≠ select**.

---

## Three separations (keep all of them)

| Separation | Keep apart | Objects |
|------------|------------|---------|
| **1. Environment vs advancement** | Peer help/hurt vs who gets the scarce slot | **`L_net = B − D`** vs score + winner rule |
| **2. Scoring vs selection** | How we **rank** vs how we **pick winners** | **`S_i`** (λ) vs **top K** (later: stochastic draw) |
| **3. Hero vs equations** | Empirical outcome plot vs generative rules | Layer A curve ≠ Alex score |

### Environment vs advancement

| | **Environment / development** | **Advancement (who gets the slot)** |
|---|--------------------------------|--------------------------------------|
| **Question** | How do peers affect net value, learning, visibility? | **Who gets the draft pick / promotion / slot?** |
| **Symbols (theory)** | `L_net = B(·) − D(·)` | Score **`S_i`**, then a **winner rule** |
| **What it is NOT** | The full story of who gets drafted | The same as fitting the hero curve |
| **Layer A hero** | Shows **outcome** (draft rate vs pool quality) | Does **not** separate environment vs advancement channel |

### Scoring vs selection (inside advancement)

| | **Scoring** | **Selection (winner rule)** |
|---|-------------|------------------------------|
| **Question** | How do we **rank** candidates? | Given ranks, **who wins**? |
| **Symbols / knobs** | **`S_i = A_i − λ·L_C`** (Alex v1); **λ** lives here | **Top K** (v1 default); later soft / noisy / stochastic draw |
| **Pass A knockout** | Toggle congestion **in the score** (λ=0 vs λ>0) | Same winner rule held fixed |
| **Future noise** | Leave **S_i** fixed | Change only this step |

**One sentence:** *The hero describes outcomes; **`L_net`** is the peer environment; advancement = **score** then **select**; the sim tests whether congestion **in the score** changes who gets selected under a fixed winner rule.*

---

## Why Charles (and others) get lost

The project uses **B − D** for the **environment** and Alex’s **`S_i`** for **ranking**. If you treat environment + score + top-K as one blob (“the model”), you rebuild a complicated world where everything happens at once. If you call **`S_i`** “selection,” you cannot cleanly add stochastic draft later.

**v1 simplification:**  
- **B − D** = prose frame for help vs hurt among peers (not separately estimated in v1).  
- **Alex score** = **scoring only** — congestion enters the **ranking**, not “the whole economy.”  
- **Winner rule** = **top K** for now (explicit, separate step).  
- Generative code = make **score → select** visible: talent-only score vs congestion-in-score, same top-K.

---

## What each layer owns

| Layer | Owns |
|-------|------|
| **A** | Empirical curve — *what* the data look like |
| **B** | Two-part story: (1) B vs D in environment; (2) **D (congestion) may enter the score** via Alex **`S_i`**, then a winner rule |
| **C** | Code: **assign → score → select (top K) → plot** |

---

## Agent rule

When explaining basketball model work to Charles or in manuscript prose:

1. Say **environment** when you mean B − D / peer effects on development.  
2. Say **scoring** / **Alex score** / **`S_i`** when you mean the ranking equation (**λ** lives here).  
3. Say **selection** / **winner rule** / **draft** when you mean top-K or a later stochastic pick from scores.  
4. Never imply the hero regression **is** the scoring equation.  
5. Layer C knockouts (Pass A) change **scoring ingredients**, not the winner rule and not every environmental channel.

**Re-entry pointer:** [`re_entry/02_Three_Kinds_of_Model.md`](re_entry/02_Three_Kinds_of_Model.md) — BINDING + scoring vs selection.
