# COMPASS — sim re-entry status (2026-07-27)

**Audience:** Charles, future agents  
**Scope:** Basketball generative sim only — not tenure/Army.

---

## What changed

1. **Document re-entry** (01–03 + `Model.pdf`) — unchanged intent; **ρ** replaces **τ** in assignment prose.
2. **Sim re-entry:** old lab notebooks → `sports/archive/`; active surface = **`540_*`** + scripts.
3. **Assignment knob:** user-facing **ρ (assortativity)**; **ρ=0** = max mixing; **ρ↑** = sharper soft match. Legacy **τ** in archived docs only.
4. **Preferential attachment:** `USE_PREFERENTIAL_ATTACHMENT` boolean (default off).

---

## Experiments

| Pass | Question | Status | Export |
|------|----------|--------|--------|
| **A** | Congestion in **S_i**? (λ=0 vs λ>0) | **Done** | `alex_side_by_side_v0/` |
| **B** | Assignment sorting moves readout? (ρ low/high/chop) | **Done** | `alex_rho_ablation_v0/` |

**Claims guard (v1):**

- Pass A proves congestion **in selection** can bend curves — not hero bin-for-bin match.
- Pass B shows assignment sensitivity with selection fixed — not proof NBA uses ρ.
- Sort-and-chop is a **benchmark**, not ρ→∞.

---

## Execution order

See [`re_entry/model_OPORD.md`](re_entry/model_OPORD.md).

---

## Agents

- **Charles + Cursor agent** own archive + 540 implementation.
- **SCOUT:** archived notebooks = reference only; no handoff required.
- **COMPASS:** this stub + claims guard; no domain coding.
