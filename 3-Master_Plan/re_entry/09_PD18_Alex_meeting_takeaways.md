# 9. PD18 — Alex meeting takeaways (Aug 7, 2026)

**Last synced:** 2026-08-07

**Audience:** Charles, COMPASS, VECTOR (literature), anyone touching ASSIGN.

**Standalone:** definitions inline; builds on doc [`08`](08_PD16_Alex_meeting_takeaways.md) (team L_C, naive-draft θ) and PD17 empirical deck.

**Source transcript:** `transcripts/20260807_Paper_Directions_18_otter_ai_transcript.docx`

**Working digest:** `transcripts/PD18_notes.md`

**Deck shown:** `HEROs_and_PASSes/slides/CHAR_PD17_HAND.pptx` (empirical MBB); stumble on slide 7, recovered post-call.

---

## Headline — what changed in one paragraph

Alex and Charles agreed **T_j\* (pre-drawn team assignment targets) and ρ (assortativity) do overlapping work** in the current soft-assign rule. **New direction:** explore **ρ-only assignment** by reframing roster formation as an **assortative growth process on a bipartite network** (players ↔ teams). If that works, **eliminate T_j\* from the assignment mechanism** — model gets simpler and opens a defensible **networks** hook. **T_j** (realized mean ability on a roster) **stays** as a **descriptive** quantity for Sketch A, congestion readouts, and empirical **T_jt**. **Do not delete** the existing T_j\* code path; **park** it as fallback. **Time box:** ~weekend; if prototypes cannot produce “reasonably looking teams,” revert to T_j\* + ρ and continue.

---

## What Alex accepted (keep saying this)

| Topic | Status |
|-------|--------|
| PD17 empirical interval-overlap slides (3–6) | ✓ — “love it”; main-paper material |
| **ρ calibration** via coverage / overlap (slide 7 intent) | ✓ — direction right; x-axis explanation needed in briefing |
| **T_j descriptive** (post-assignment roster mean) | ✓ |
| Phase B / PD16 work not thrown away | ✓ (implicit — this is ASSIGN-layer refactor) |
| Sort-and-chop benchmark | ✓ unchanged |

---

## Core model shift — T_j\* parked, ρ-only ASSIGN (exploratory)

### Today (park, do not delete)

1. Draw **A_i** and pre-drawn **T_j\*** per team.  
2. Soft assign: seat player *i* on teams with **T_j\*** near **A_i**, sharpness dialed by **ρ**.  
3. After assign: **T_j** = mean **A_i** on roster (descriptive).

**Problem:** **T_j\*** and **ρ** both control how assortative seating looks — two knobs, one phenomenon.

### PD18 target (if literature + prototype succeed)

1. Draw **A_i** only (or fixed ability draw as now).  
2. **Grow** player–team edges with **one assortativity parameter ρ** (network formation / attachment rule — exact rule from lit).  
3. **Fixed roster size:** every team has the same capacity (Alex flagged this as the main break point vs standard growth models).  
4. **T_j** computed after assign — **never** an input to who sits where.

### Explicit park instruction

| | Action |
|---|--------|
| `draw_target_means` / **T_j\*** in sim | **PARK** — no new features built on it until PD18 fails |
| `soft_assign(..., team_targets=...)` | **KEEP in repo** — fallback |
| Glossary / slide 2 “T_j\* draw” | **Mark legacy** when ρ-only rule is chosen |
| **T_j**, **T_jt** in figures | **KEEP** — descriptive |

---

## Alex research ask — assortative bipartite growth

**Task (Charles + VECTOR):** Find **assortative growth / formation models for bipartite networks**. If sparse, start from **unipartite assortative growth** and assess extension to bipartite (players ↔ teams).

**Scientific question:** Can we generate **realistic overlapping talent windows** on rosters (PD17 slide 3 / 7) with **ρ alone**, without pre-specified team targets?

**Known break point:** Classical growth models often assume **unbounded** or **preferential** degree growth. We need **fixed equal team size** (e.g. 16 players × 350 teams). Alex: bounding **may** break assortativity assumptions — must test, not assume.

**Fallback ladder:**

1. Bipartite assortative growth (preferred)  
2. Unipartite model ported to bipartite  
3. **Urn / combinatorial** assortment (different literature — math-heavy)  
4. **Revert** to T_j\* + ρ soft assign  

**Time box:** ~weekend prototype; “reasonably looking teams” = go/no-go.

**Defense framing (Alex):** Simpler assign layer + networks vocabulary; later extensions (co-authorship, collaboration, relax strict bipartiteness) without rewriting the whole story.

---

## Brief for VECTOR — literature search (copy-paste ready)

**Standalone attachable doc (recommended):** [`20260807_VECTOR_PD18_literature_brief.md`](20260807_VECTOR_PD18_literature_brief.md) — full background for VECTOR cold re-entry + attachment list.

**Short email intro** — paste above the attachable brief:

> VECTOR — picking this back up after the June agent rounds. We’ve been in basketball re-entry (Phase B characterization + empirical PD17 deck). Alex and I met today (PD18): **T_j\*** (pre-drawn team targets) and **ρ** overlap in our assign step. We want a literature path to **ρ-only** bipartite roster formation with **fixed roster size**, or we revert to current code (kept in repo).
>
> **Start here:** `20260807_VECTOR_PD18_literature_brief.md` (self-contained background + attachment list).
>
> **Deliverable:** 3–5 papers + recommended formation rule for our setting. **Time box:** ~weekend.

---

## PD17 slide 7 — what went wrong in the room (fixed narrative)

**Figure:** `empirical_pd17/EMPIRICAL_rho_coverage_overlay.png` — empirical \| sim four ρ \| sim ρ sweep.

**x-axis (correct):** **Individual player ability** (empirical: PPM z; sim: **A_i** on [0,1]) — a point on the talent axis.

**y-axis:** **Coverage** — count of team-seasons (emp) or teams (sim) whose roster talent **interval** [min, max ability on roster] **covers** that x. *Not* team-average **T_j** on the x-axis.

**Story:** Low ρ → many teams span each ability level (broad coverage). High ρ → tighter, more assortative seating → **lower / narrower** coverage peak. Empirical peak is **high**; sort-and-chop benchmark is **~zero** overlap.

Charles initially described x as “overall A_i” in a way Alex read as “the fixed draw shouldn’t move with ρ” — true for the **ability draw**, but the plot is **coverage along the ability axis**, which **does** change with ρ. Post-call explanation aligned with slide 3 interval logic.

---

## Parked vs active (repo hygiene)

| Component | PD18 status |
|-----------|-------------|
| T_j\* assignment attractor | **PARK** (exploratory) |
| T_j\* code | **KEEP** — fallback |
| T_j, T_jt descriptive | **ACTIVE** |
| ρ calibration (PD17 slide 7) | **ACTIVE** — target unchanged until new assign rule |
| PD16 team L_C, naive-draft θ | **ACTIVE** — orthogonal |
| Sort-and-chop | **ACTIVE** — benchmark |

---

## Suggested next steps

| Who | Task |
|-----|------|
| **VECTOR** | Literature scan per § “Brief for VECTOR” |
| **Charles** | Send VECTOR brief; skim top papers over weekend |
| **CODA / COMPASS** | When rule chosen: spec ρ-only assign in `tier1_pool_assignment.py` behind flag (e.g. `GALLERY_ASSIGN_MODE=rho_growth`) — **do not remove** T_j\* path |
| **Charles** | Slide 7 one-liner in HAND17: x = ability axis, y = # teams covering that ability |
| **All** | Go/no-go after weekend: “reasonably looking teams” vs revert |

---

## Related docs

| Doc | Role |
|-----|------|
| [`08_PD16_Alex_meeting_takeaways.md`](08_PD16_Alex_meeting_takeaways.md) | Team L_C, θ(K/N), ρ as L_C spread |
| [`07_Phase_B_Characterization_Slides_Explained.md`](07_Phase_B_Characterization_Slides_Explained.md) | T_j\* glossary (mark legacy when PD18 lands) |
| `HEROs_and_PASSes/slides/README.txt` | HAND17 map |
| `HEROs_and_PASSes/empirical_pd17/REGENERATE.md` | Slide 7 figure regen |
