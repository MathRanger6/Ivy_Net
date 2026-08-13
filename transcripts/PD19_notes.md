# Paper Directions 19 — my read (Aug 13, 2026)

**Source:** `transcripts/20260813_Paper_Directions_19_otter_ai_transcript.docx`  
**Follow-up:** [`PD20_notes.md`](PD20_notes.md) (same day — locks **$t$ in denominator**, inverted-U before MLE)

**Related artifacts:**

| Artifact | Path |
|----------|------|
| Formula synopsis | `3-Master_Plan/Alex_stuff/MLE_prob.docx` |
| Whiteboard | `3-Master_Plan/Alex_stuff/PD19_board.jpeg` |
| LG briefing (HAND17 walk-through) | `3-Master_Plan/re_entry/HEROs_and_PASSes/Alex_LG_three_step_briefing.md` |

---

## Headline

**Briefing landed.** Alex loved **$H_{\text{sort}}$** (paper material). Next modeling step: replace deterministic **top-K SELECT** with **probabilistic selection** from $S_i$, then **MLE** for **$\rho^*, \lambda^*, \gamma^*$** — superseded in part by PD20 (see below).

---

## What was on the table (PD19)

### Pipeline (unchanged ASSIGN + SCORE)

- **ASSIGN:** LG — $\tilde{w}_{ij} = R_j e^{-\rho|\hat{A}_i - \hat{\mu}_j|}$, $P(j|i) = \tilde{w}_{ij}/\sum_{j'}\tilde{w}_{ij'}$
- **SCORE:** $S_i = \hat{A}_i - \lambda L_{C,g(i)}$; team $L_C$ via soft viability $\sigma(\gamma(\hat{A}-\theta))$
- **SELECT (old):** top **K** by $S_i$

### PD19 SELECT proposal (synopsis doc — **superseded by PD20 on $t$**)

`MLE_prob.docx` wrote:

\[
P(Y_i=1) \propto \frac{\exp\bigl(t(\hat{A}_i - \lambda L_C)\bigr)}{\sum_k \exp\bigl(t(\hat{A}_k - \lambda L_C)\bigr)}
\]

**$t$ in the numerator** — non–physics convention. **PD20 locks** Gibbs form with **$t$ in the denominator:** $\exp(S_i/t)/\sum \exp(S_k/t)$.

### MLE ambition (still on roadmap — after PD20 gate)

Fit **$\rho^*, \lambda^*, \gamma^*$** (and $t$) to empirical draft $Y_i$ once probabilistic SELECT is validated.

### Other PD19 locks

- **$H_{\text{sort}}$** — Alex wants in the paper (realized sorting after ASSIGN)
- **$\theta$ from CDF:** $\theta_t = F_t^{-1}(1 - K_t/N_t)$
- **Robustness:** extreme $t$ and $R_j$ must not break numerics

---

## PD20 overrides (read next)

See [`PD20_notes.md`](PD20_notes.md) for:

- **$t$ in denominator** (Gibbs / statistical physics)
- **Priority:** $t$ sweep + **inverted-U survival** before MLE
- Charles test plan: $\lambda=1$ and breakpoint $\lambda$, each with log-$t$ sweep
