# Paper Directions 16 — my read (Aug 4, 2026)

**Source:** `transcripts/20260804_Paper_Directions_16_otter_ai_transcript.docx` (~31 min).  
**Context:** Charles briefed Alex on Phase B characterization deck (intro + ρ, λ, θ, θ×K/N, γ, λ_crit).  
**Whiteboard:** two sketches saved under `.cursor/.../assets/` (L_C vs ρ distributions; naive-draft θ from K/N).

---

## Headline

**Strong meeting.** Alex liked the deck structure, sigmoid understanding, and sort-and-chop rationale for γ / λ_crit. The big pivot is **principled θ from K/N** (naive draft) and **reframing ρ + L_C** via **team-level congestion distributions** — not just selection-curve OAT plots.

Closing energy: move from “539 preset knobs” toward **data-identified** ρ, θ, (then principled γ, λ) — only γ and λ remain free after θ is fixed from ability draw + K/N.

---

## What landed well

- **Intro / glossary / benchmarks** — A_i, T_j, smooth L_C, seed 42, not curve-fitting.
- **ρ slides** — “Assortativity matters” accepted; Alex wants **deeper intuition** (see gaps).
- **λ slide** — talent-only vs λ>0 bend; same story as before.
- **θ × K/N** — co-movement readout; Alex said continue, revisit θ interpretation.
- **γ / sort-and-chop / λ_crit ≈ 4/γ** — Charles’s “no ambiguity, deterministic” explanation accepted; Alex not demanding full derivation now.

---

## Whiteboard ↔ transcript (capture for slides / memo)

### Sketch A — distribution of **L_C** over teams vs **ρ**

| Panel | Axes | Low **ρ** | High **ρ** |
|-------|------|-----------|------------|
| **1D (top/middle)** | x = **L_C**, y = **# teams** | Single **narrow hump** (Alex: nearly a **delta**, not even uniform) | **Spread** / bimodal — weak teams **L_C ≈ 0**, strong teams **L_C** high |
| **2D (bottom)** | x = **L_C**, y = **team ability** (mean A on team or T_j) | — | Heatmap: **# teams**; expect **upward** cloud — **better teams → more congestion** |

**Alex lock:** **ρ dials the spread of the L_C distribution across teams** — practical interpretation of assortativity in *this* model, not only “selection curve bends.”

Charles linked this to sort-and-chop picture (elite vs weak team L_C) — Alex: “not coincidence.”

### Sketch B — **naive draft** → principled **θ**

- Draw **A_i** from ability distribution (Beta on [0,1] in sim).
- **No teams** — everyone competes on ability alone; top **K/N** advance.
- Find cutoff **A\*** such that **P(A > A\*) = K/N** (area under PDF to the right of cutoff).
- **That cutoff defines θ** (viability / ability threshold).

**Meaning (Alex):** θ is the ability level where, **if there were no roster ambiguity**, everyone above would advance and everyone below would not. The sigmoid then adds **ambiguity around that threshold** (peer viability graded, not cliff).

**Not the same as today’s code default:** fixed **θ = 0.72** from `tier1_539_reference_settings.json`. PD16 direction = **compute θ from K/N + ability draw** each league/domain.

---

## Model changes Alex asked to try (priority order)

1. **L_C per team (not LOO per player)**  
   - Congestion = property of **team j**, same for all players on roster.  
   - Alex: earlier hero-style runs used **poolq** (not LOO) and worked; LOO may be unnecessary for L_C in score.  
   - **Action:** implement team-level L_C; verify Pass B curve + Army path unchanged “in the wash.”

2. **θ from K/N + ability CDF**  
   - Replace free θ preset with **quantile**: θ = F_A⁻¹(1 − K/N) on the draw used for A_i (Beta or empirical).  
   - **Action:** helper + re-run θ/OAT and θ×K/N with computed θ; document shift from 0.72.

3. **ρ ↔ L_C distribution diagnostic (new figure / slide gap)**  
   - For each ρ arm: histogram of **team L_C** (# teams vs L_C).  
   - 2D heatmap: team mean ability (or T_j) vs L_C.  
   - **Action:** new script or Pass C extension; fills whiteboard Sketch A.

4. **ρ low arm still not flat enough**  
   - Try **ρ → 0.001**; check bin count / stochastic assignment.  
   - Build **one clean sentence** + empirical/analytic intuition for why ρ matters in *this* construction.

5. **γ and λ — principled fit (later)**  
   - After ρ, θ data-linked: only **γ, λ** free.  
   - Alex: avoid “make sim curve match hero” as the *definition*; find **data properties** that pin γ, λ.

**Parked:** Menger **multiplicative** congestion (Charles → 4-sentence memo); additive mean vs product.

---

## Empirical calibration roadmap (Alex, end of meeting)

| Knob | From data? | How |
|------|------------|-----|
| **A_i** distribution | Yes | Empirical perf or declared draw (Beta) |
| **K/N** | Yes | Domain (MBB ~1%, etc.) |
| **θ** | Yes (PD16) | Quantile from A distribution at 1 − K/N |
| **ρ** | Yes | Match assignment assortativity in data |
| **γ, λ** | **Open** | Need principled estimators — not preset-only |

---

## Sort-and-chop (what Charles told Alex)

Used for **γ / λ_crit** slides only: removes assignment ambiguity → clean **λ_crit ≈ 4/γ** story. Alex OK’d; wanted congestion unpacked separately (team L_C, θ from K/N) — not a rejection of sort-and-chop.

---

## Quotes to keep

- **ρ:** “Assortativity is this dialing measure of what’s the spread of the L_Cs.”
- **θ:** “In a world where there was no team congestion, the cutoff for ability would have been … pick θ so that area = K/N.”
- **L_C:** “Congestion should be how many good players are on the team.”
- **Fit:** “Try to find γ and λ without saying the way to do it is just make the two curves as close as possible.”

---

## Suggested next COMPASS / Charles actions

**Live checklist:** [`CHARLES_CHECKLIST.md`](../3-Master_Plan/re_entry/CHARLES_CHECKLIST.md) (post-PD16). Archived: [`archive/checklists/`](../3-Master_Plan/re_entry/archive/checklists/README.txt).

- [x] Draft PD16 one-pager for `re_entry/` → [`08_PD16_Alex_meeting_takeaways.md`](../3-Master_Plan/re_entry/08_PD16_Alex_meeting_takeaways.md)
- [x] Refresh Charles checklist for PD16 priorities
- [ ] Implement **team L_C** + **θ(K/N)** via **shell env vars** (`GALLERY_LC_MODE`, `GALLERY_THETA_MODE` in `gallery_knobs.py`) — **not** a new conda env; compare PNGs to current deck
- [ ] Build **L_C distribution vs ρ** figures (whiteboard Sketch A)  
- [ ] ρ → 0.001 arm + assortativity intuition paragraph for slide footer  
- [ ] Menger multiplicative — 4 sentences (parked)  
- [ ] Update intro slide when θ provenance changes (539 preset → K/N quantile)

**Related:** Phase B walkthrough `07_Phase_B_Characterization_Slides_Explained.md`; memo 06 (λ_crit); PD15 (characterization vs fitting).
