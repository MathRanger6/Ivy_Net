# BINDING — Selection is its own step (Charles lock, Jul 2026)

**Status:** Binding for agents, re-entry docs, basketball v1, and manuscript framing.  
**Charles #1 confusion resolved:** Do **not** merge “describe the peer environment” with “who wins the scarce slot.”

---

## The two mechanisms (keep separate)

| | **Environment / development** | **Selection (advancement rule)** |
|---|--------------------------------|----------------------------------|
| **Question** | How do peers affect net value, learning, visibility? | **Who gets the draft pick / promotion / slot?** |
| **Symbols (theory)** | `L_net = B(·) − D(·)` — benefit minus congestion in the **environment** | **`S_i = A_i − λ·L_C`** — Alex score: ability minus congestion in **who gets selected** |
| **What it is NOT** | The full story of who gets drafted | The same as fitting the hero curve |
| **Layer A hero** | Shows **outcome** (draft rate vs pool quality) | Does **not** tell you environment vs selection channel |
| **Layer C sim** | Roster assignment (who lands where) | **Explicit step:** rank by selection score → top **K** |

**One sentence:** *The hero describes outcomes; Alex’s equation describes **who gets selected**; the sim tests whether congestion in the **selection rule** changes who gets selected.*

---

## Why Charles (and others) get lost

The project uses **B − D** language for the **environment** and **Alex’s score** for **selection**. If you treat them as one blob (“the model”), you rebuild a complicated world where everything happens at once.

**v1 simplification:**  
- **B − D** = prose frame for help vs hurt among peers (not separately estimated in v1).  
- **Alex score** = **selection only** — congestion enters the **advancement rule**, not “the whole economy.”  
- **538D** = make **selection** a visible step: talent-only vs talent-minus-congestion knockout.

---

## What each layer owns

| Layer | Owns |
|-------|------|
| **A** | Empirical curve — *what* the data look like |
| **B** | Two-part story: (1) B vs D in environment; (2) **D (congestion) may enter selection** via Alex score |
| **C** | Code: assignment → **selection score** → top-K → plot |

---

## Agent rule

When explaining basketball model work to Charles or in manuscript prose:

1. Say **selection** when you mean draft rule / Alex score / top-K.  
2. Say **environment** when you mean B − D / peer effects on development.  
3. Never imply the hero regression **is** the selection equation.  
4. Layer C knockouts are about **selection ingredients**, not reproducing every environmental channel.

**Re-entry pointer:** [`re_entry/02_Three_Kinds_of_Model.md`](re_entry/02_Three_Kinds_of_Model.md) § “Selection is its own step”.
