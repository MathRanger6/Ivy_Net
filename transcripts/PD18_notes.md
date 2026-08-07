# Paper Directions 18 — my read (Aug 7, 2026)

**Source:** `transcripts/20260807_Paper_Directions_18_otter_ai_transcript.docx` (~17 min).  
**Context:** Follow-up after PD17 empirical deck (`CHAR_PD17_HAND.pptx`). Charles stumbled on slide 7 x-axis; recovered after call (coverage plot — see below).

---

## Headline

**Assignment simplification:** Alex and Charles agree **T_j\* and ρ overlap** — explore **ρ-only** assignment via **assortative growth models on bipartite networks**. **Park T_j\*** (do not delete code). **T_j** stays as **descriptive** realized roster mean (Sketch A, calibration readouts).

**Time box:** Today + weekend literature + prototype. If no “reasonably looking teams” → **revert** to T_j\* soft assign and keep running.

---

## Alex ask (priority 1)

1. Literature search: **assortative growth / formation models for bipartite networks** (if thin → unipartite assortative growth, then extend).
2. Reframe ASSIGN as: **one assortativity parameter ρ** seats players on teams without pre-drawn **T_j\*** targets.
3. **Breakpoint to watch:** standard network growth often **unbounded degree**; we need **fixed equal roster size** (every team fills to capacity). Bounding may break assortativity mechanism — test empirically.
4. **Plan B:** urn / combinatorial assortment (math-heavy, different lit) if network framing fails.

**Defense upside (Alex):** cleaner model + legitimate “networks” chapter hook; later relax bipartiteness → co-authorship, collaboration units, etc.

---

## What we keep vs park

| Object | PD18 status |
|--------|-------------|
| **T_j\*** (pre-drawn team target) | **PARK** for assignment — redundant with ρ if growth model works |
| **T_j** (realized mean A_i on roster) | **KEEP** — descriptive; Sketch A y-axis; empirical **T_jt** |
| **ρ** | **KEEP** — sole ASSIGN knob (target formulation TBD from lit) |
| **Sort-and-chop** | **KEEP** — benchmark (already ignores T_j\*) |
| **T_j\* code path** | **DO NOT DELETE** — fallback if PD18 exploration fails |

---

## PD17 deck — meeting moment (slide 7)

Charles showed slides 3–7. Alex **loved** interval overlap (slide 3), L_C distributions (4–6).

**Slide 7 stumble:** Alex asked what x-axis is. Charles first said “player A_i overall” (fixed draw — shouldn’t move with ρ). Wrong.

**Correct readout (Charles, post-call):** x = **individual ability** on the talent axis; y = **how many team-seasons (empirical) or teams (sim) have a roster member at that ability** — i.e. **interval coverage** from slide 3, not team-average T_j. Low ρ → broad coverage (many teams span each x); high ρ → narrow overlap peak.

**Action:** Fix slide 7 speaker notes / x-axis one-liner; keep figure logic (already in `empirical_rho_coverage_overlay.py`).

---

## VECTOR handoff

Charles → VECTOR: bipartite **assortative attachment / growth** literature scan. See **`09_PD18_Alex_meeting_takeaways.md`** § “Brief for VECTOR.”

---

## Fallback chain (Alex)

1. Bipartite assortative growth (preferred)  
2. Unipartite assortative growth → adapt  
3. Bounded urn / combinatorial assortment  
4. **Revert** to current T_j\* + ρ soft assign  

---

## Next code touchpoints (when lit lands — not yet)

- `sports/tier1_pool_assignment.py` — `soft_assign`, `draw_target_means` (park, don’t delete)
- `empirical_rho_coverage_overlay.py` — calibration target unchanged until assign rule changes
- Deck glossary: slide 2 sim inputs may drop T_j\* draw if ρ-only wins
