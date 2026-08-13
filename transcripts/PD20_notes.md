# Paper Directions 20 — my read (Aug 13, 2026)

**Source:** `transcripts/20260813_Paper_Directions_20_otter_ai_transcript.docx` (~5 min follow-up, same day as PD19).  
**Context:** Charles briefed Alex well on the LG three-step pipeline (ASSIGN → SCORE → SELECT). PD19 opened **probabilistic SELECT + MLE**; PD20 **locks temperature convention** and **reorders priorities** (inverted-U survival before MLE).  
**PD19 digest:** [`transcripts/PD19_notes.md`](PD19_notes.md)  
**Open questions (K draws, $\rho^*$):** [`../3-Master_Plan/Alex_stuff/PD20_K_draws_and_rho_explainer.md`](../3-Master_Plan/Alex_stuff/PD20_K_draws_and_rho_explainer.md)

**Related PD19 artifacts (same day):**

| Artifact | Path |
|----------|------|
| Transcript (PD19) | `transcripts/20260813_Paper_Directions_19_otter_ai_transcript.docx` |
| Formula synopsis | `3-Master_Plan/Alex_stuff/MLE_prob.docx` |
| Whiteboard | `3-Master_Plan/Alex_stuff/PD19_board.jpeg` |
| Briefing doc | `3-Master_Plan/re_entry/HEROs_and_PASSes/Alex_LG_three_step_briefing.md` |

---

## Headline

**Replace deterministic top-K SELECT with a Gibbs (softmax) rule at temperature $t$**, with **$t$ in the denominator** (statistical-physics convention). **First job:** prove the **inverted-U still emerges** at some $t$ when everything else is held at the PD17/LG settings that worked. **MLE for $\rho^*, \lambda^*, \gamma^*$ is step two** — not blocked, but not first.

---

## Arc — PD19 → PD20

### PD19 (morning meeting + board)

- **SCORE unchanged:** $S_i = \hat{A}_i - \lambda L_{C,g(i)}$ (team smooth congestion).
- **SELECT change:** instead of top-K by $S_i$, define **$P(Y_i=1)$** from the selection score.
- **MLE ambition:** fit **$\rho^*, \lambda^*, \gamma^*$** (and likely $t$) to real draft outcomes.
- **Synopsis doc** wrote $P(Y=1|i) \propto \exp\bigl(t(\hat{A}_i - \lambda L_C)\bigr) / \sum_i \exp(\cdots)$ — **$t$ in the numerator** (non–physics convention).
- **Board (bottom left)** looked like **$t$ in the denominator** — PD20 confirms that is the lock.

### PD20 (follow-up call)

- Alex’s **first-order worry:** softening the hard top-K cut may **smooth away the breakpoint** that produces the inverted-U (“lose a phase transition”).
- **Hope:** in the **right $t$ regime**, Gibbs SELECT ≈ hard cut, but **$t$ adds a knob** on U shape.
- **Lock:** **$t$ in denominator** — Gibbs / statistical-physics temperature.
- **Immediate work:** sim + **log-spaced $t$ sweep**; reaffirm U; **then** MLE / full parameter story.

---

## Locked formula — Gibbs SELECT

**Selection score (unchanged — SCORE step):**

\[
S_i = \hat{A}_i - \lambda L_{C,g(i)}
\]

**Team congestion (unchanged):**

\[
L_{C,j} = \frac{1}{|j|}\sum_{k \in j} \sigma\!\bigl(\gamma(\hat{A}_k - \theta)\bigr),
\qquad
\sigma(x) = \frac{1}{1+e^{-x}}
\]

**Selection probability (SELECT step — PD20 lock):**

\[
P(Y_i=1) = \frac{\exp(S_i / t)}{\sum_{k=1}^{N} \exp(S_k / t)}
\]

**Alex framing:** **Gibbs probabilities** — $S_i$ plays the role of a **Hamiltonian** (objective / energy-like score); $t$ is **temperature**. Same family as stat-phys / transfer-matrix intuition (Laplace transform link came up in passing).

### Temperature behavior ($t$ in denominator)

| Regime | Effect on SELECT | Link to old rule |
|--------|------------------|------------------|
| **$t \to 0^+$** (cold) | Weight concentrates on highest $S_i$ → **≈ deterministic top-ranked** | Recovers hard cut |
| **$t$ moderate** | Soft ranking; tunable sharpness | **Target operating band** for inverted-U |
| **$t$ large** (hot) | **≈ uniform** over pool | Noise dominates; U may flatten |

**Sweep $t$ logarithmically** — Alex: orders of magnitude in the exponent matter; don’t only linspace small values.

---

## What stays the same (BINDING)

Per [`BINDING_Selection_is_its_own_step.md`](../3-Master_Plan/BINDING_Selection_is_its_own_step.md):

| Separation | PD20 status |
|------------|-------------|
| **ASSIGN vs SCORE vs SELECT** | Still three steps |
| **Score ≠ select** | $S_i$ built in SCORE; **only SELECT rule changes** |
| **λ lives in SCORE** | Unchanged |
| **ρ lives in ASSIGN** | Unchanged (LG Grandchild) |
| **Hero** | Layer A outcome — not the scoring equation |

**MLE does not merge layers** — it estimates parameters **inside** the generative story once the SELECT rule is validated.

---

## Alex priority order (explicit)

1. **Build a SELECT rule** from Gibbs probabilities that is **equivalent to top-K** in the cold-$t$ limit.
2. **Simulate** — hold ASSIGN + SCORE at the **PD17/LG settings that produced the inverted-U** (empirical caps, $\rho$, $\lambda$ band, etc.).
3. **Sweep $t$** (log scale) — plot selection rate vs LOO pool quality (Hero axis).
4. **Success criterion:** inverted-U **re-emerges** at some $t$; hard-cut behavior at small $t$.
5. **Then** — MLE for $\rho^*, \lambda^*, \gamma^*$ (and $t$); “rest of” PD19 agenda.

**Not first:** full MLE pipeline before U is reaffirmed.

---

## Charles test plan (from call — Alex said “sure”)

| Panel | Fix | Sweep |
|-------|-----|-------|
| **A** | $\lambda \approx 1$ (congestion in score) | $t$ log-spaced |
| **B** | $\lambda$ at **breakpoint** (where λ sweep first moved SELECT vs talent-only) | $t$ log-spaced |

**Question both panels answer:** Does **$t$ kill the inverted-U** that λ created, or is there a **$t$ window** where the hump survives?

---

## Implementation notes (code — PD20 scaffold built Aug 2026)

### Bridging Gibbs to **K** draft slots

PD20 did **not** re-litigate the “softmax sums to 1” vs “**K** winners per season” issue. Practical bridge for **sim readouts** (consistent with “equivalent to top-K at cold $t$”):

- Compute weights $w_i \propto \exp(S_i / t)$ with **log-sum-exp** for stability.
- **Draw $K$ players without replacement** proportional to $w_i$ (Plackett-Luce / rule `"A"` skeleton in `tier1_pool_assignment.choose_selected`).
- Bin **realized** `Y_selected` vs `poolq_loo` — same Hero comparison as `grandchild_lambda_select_sweep.py`.

**Flag for Alex (one line email):** “Sim uses K draws without replacement from Gibbs weights — OK?”

### MLE (PD19 — parked until step 5)

When ready, likelihood on player-seasons:

\[
\mathcal{L} = \prod_i P(Y_i=1 \mid S_i(t,\lambda,\gamma,\ldots))^{Y_i}
\bigl(1 - P(Y_i=1 \mid \cdots)\bigr)^{1-Y_i}
\]

**$\rho$ in MLE:** only enters if rosters are **re-simulated** (LG assign). On **fixed empirical rosters**, $\rho$ does not move $L_C$ — match $\rho$ via **$H_{\text{sort}}$** separately (Alex loved $H_{\text{sort}}$ for the paper).

---

## ASSIGN recap (unchanged — for PD20 reader)

LG weight (unnormalized): $\tilde{w}_{ij} = R_j \exp(-\rho|\hat{A}_i - \hat{\mu}_j|)$.

Seat probability: $P(j|i) = \tilde{w}_{ij} / \sum_{j'} \tilde{w}_{ij'}$.

Each player **draws** a team (weighted random seat). Final $\hat{T}_j = \mu_j$.

---

## Open questions (carry forward)

| # | Question | Owner |
|---|----------|-------|
| 1 | K draws without replacement vs independent Bernoulli scaled to $K$? | Confirm with Alex (one line) |
| 2 | Is **expected** selection curve (analytical $P$) enough, or only **simulated** draws? | Charles / first plots |
| 3 | $\theta$ still $F^{-1}(1-K/N)$ per season when sweeping $t$? | Default yes unless MLE pass |
| 4 | Exact **log-$t$ grid** (e.g. $10^{-3}$ to $10^{3}$?) | Empirical after first run |

---

## Code touchpoints (when Charles says go)

| Piece | File / pattern |
|-------|----------------|
| SELECT rule `"D"` (Gibbs + K draws) | `sports/tier1_pool_assignment.py` → `choose_selected`, `gibbs_select_weights` |
| $t$ sweep diagnostic | `sports/scripts/grandchild_temperature_select_sweep.py` |
| PD20 outputs (isolated) | `HEROs_and_PASSes/pd20_temperature/` — see `REGENERATE.md` |
| Baseline λ sweep (rule C, PD17) | `sports/scripts/grandchild_lambda_select_sweep.py` → `grandchild_assign/` |
| HAND deck path | `slides/CHAR_PD20_HAND.pptx` via `HAND_PD20_DECK` in `hero_gallery_paths.py` |
| LG ASSIGN | `sports/541_grandchild_homophily_assign.py` |
| Briefing / notation | `3-Master_Plan/re_entry/HEROs_and_PASSes/Alex_LG_three_step_briefing.md` |

---

## One-liners for the paper / defense

**Gibbs SELECT:** “Advancement probability follows a Gibbs rule on the selection score $S_i$, with temperature $t$; the deterministic top-K limit is the cold-$t$ regime.”

**Why PD20 before MLE:** “We first verify that the phenomenological inverted-U is not an artifact of the hard cut alone — it must survive a soft Gibbs SELECT in a finite $t$ window before we estimate parameters by likelihood.”

**$H_{\text{sort}}$ (PD19 carryover):** Realized sorting diagnostic for ASSIGN — Alex wants it in the paper; separate from SELECT temperature.

---

## Next doc (optional)

Mirror to re_entry when stable: `3-Master_Plan/re_entry/10_PD20_Alex_meeting_takeaways.md` (COMPASS-style, like `09_PD18`).
