# PD20 — Gibbs SELECT temperature sweep

**Goal (Alex PD20):** Replace deterministic top-K SELECT with **Gibbs rule D**
($w_i \propto \exp(S_i/t)$, then **K draws without replacement**). Sweep
$\log_{10} t$ at fixed $\lambda$ panels and confirm the **inverted-U survives**
before MLE.

**PD17 baseline is untouched:** `grandchild_assign/` still holds rule **C**
(top-K) outputs from `grandchild_lambda_select_sweep.py`.

## Locked settings

| Knob | Value |
|------|-------|
| ASSIGN | LG Grandchild, empirical roster caps, $\rho=0.5$ |
| SCORE | $S_i = \hat{A}_i - \lambda L_{C,g(i)}$ |
| SELECT | Rule **D**, $t$ in denominator |
| $\theta$ | $F^{-1}(1-K/N)$ per season |
| $\lambda$ panels | **1.5** and **2.0** (breakpoint band from PD17 λ sweep) |

## Outputs

| File | Description |
|------|-------------|
| `GRANDCHILD_temperature_select_sweep_2011_2021.png` | 2×2 figure (λ panels × LOO / pool mean) |
| `GRANDCHILD_temperature_cold_limit_2011_2021.png` | Rule C vs D overlay at cold $t$ |
| `*_meta.json` | Curvature labels / cold-limit match flags |

## Slides

| Deck | Path |
|------|------|
| AUTO reference | `slides/auto/CHAR_PD20_HAND_AUTO.pptx` |
| HAND master | `slides/CHAR_PD20_HAND.pptx` |

## Open questions

See `3-Master_Plan/Alex_stuff/PD20_K_draws_and_rho_explainer.md`.
