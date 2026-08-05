# 8. PD16 — Alex meeting takeaways (Aug 4, 2026)

**Last synced:** 2026-08-05

**Audience:** Charles, re-entering after the Phase B characterization briefing.

**Standalone:** definitions inline; no scavenger hunt required.

**Source transcript:** `transcripts/20260804_Paper_Directions_16_otter_ai_transcript.docx`

**Working digest (agents):** `transcripts/PD16_notes.md`

**Deck briefed:** `HEROs_and_PASSes/slides/CHAR_Phase_B_characterization.pptx` (+ walkthrough doc 07).

---

## Headline — what changed in one paragraph

Alex liked the **characterization deck** (intro, ρ, λ, θ, θ×K/N, γ, λ_crit). The meeting did **not** ask you to throw away Phase B. It **re-aimed two definitions** and opened a **calibration path**:

1. **L_C** should be a **team** congestion measure (how many viable peers on the roster), not a leave-one-out per-player variant — at least for the score story Alex wants next.
2. **θ** should come from **K/N and the ability draw** (naive draft / no teams): the ability cutoff where the top **K/N** tail of the talent distribution lives — not a free 539 preset like 0.72.
3. **ρ** gets a sharper interpretation: it **dials how spread out team L_C values are** across the league (your whiteboard histograms), not only “the selection curve bends.”

Only **γ** and **λ** remain as knobs to fit from data once ρ and θ are pinned — and Alex wants that fit to use **properties of the data**, not “slide the sim curve until it matches the hero.”

---

## What Alex accepted (keep saying this)

| Topic | Status |
|-------|--------|
| Phase B = **characterization**, not NCAA curve fitting | ✓ |
| Pipeline: ASSIGN → SCORE (**S_i = A_i − λ L_C**) → SELECT (top-K) → VISUALIZE | ✓ |
| **Smooth L_C** in deck; hard share still in code | ✓ |
| **λ** in score bends selection vs talent-only | ✓ |
| **θ × K/N** grid worth keeping; revisit after θ redefinition | ✓ |
| **Sort-and-chop** for γ / **λ_crit ≈ 4/γ** — deterministic testbed | ✓ (not rejected) |

---

## Whiteboard A — ρ dials the **distribution of team L_C**

You drew three panels; Alex confirmed the story.

### 1D: # teams vs L_C

| **ρ** | Shape of histogram |
|-------|-------------------|
| **Low** (little assortativity) | One **narrow** hump — almost a **spike** (Alex: not even uniform; teams look similar) |
| **High** (strong assortativity) | **Spread** — weak teams pile up near **L_C ≈ 0**, strong teams at **high L_C** |

**Plain English:** ρ controls **how much team congestion varies** across the league. Low ρ → everyone faces similar peer pressure; high ρ → elite rosters are crowded, weak rosters are not.

### 2D heatmap: team ability vs L_C

- **x:** team **L_C**
- **y:** team ability (mean **A** on roster, or target **T_j**)
- **Color:** number of teams in each cell

**Question answered:** Do better teams have more congestion? **Yes** — expect an upward cloud (your wiggly diagonal in the oval).

**Why this matters:** Gives ρ a **model-internal** interpretation Alex can cite, beyond “the selection-by-pool-mean plot moved.”

**Not built yet:** scripts/figures for this diagnostic (checklist item in PD16_notes).

---

## Whiteboard B — **naive draft** defines **θ**

**Setup:** Draw **A_i** from an ability distribution (Beta(2,2) on [0,1] in the sim; empirical in real data).

**Thought experiment:** No teams — everyone competes on talent alone. Exactly fraction **K/N** of the league advances (naive draft).

**Definition:**

Find ability cutoff **A\*** such that

\[
P(A_i > A^*) = K/N
\]

(i.e. the **right-tail area** under the ability PDF equals **K/N**).

**Set θ = A\*.**

**Meaning:** θ is the talent threshold where, **if roster ambiguity did not exist**, everyone above would advance and everyone below would not. The **sigmoid** σ(γ(A_j − θ)) then adds **graded** peer viability around that threshold — ambiguity at the margin, not a hard cliff.

**Today vs PD16:**

| | **Today (Phase B deck)** | **PD16 direction** |
|---|--------------------------|-------------------|
| θ at K/N = 10% | Fixed **0.72** (539 preset) | **Computed** from Beta + K/N (≈ **0.68** for Beta(2,2) at 10%) |
| θ when K/N changes | Grid varies K/N but θ arms were {0.50, 0.72, 0.90} | θ **tracks** K/N by construction when using naive-draft mode |

**Not implemented yet** in gallery scripts — planned as an opt-in switch (see below).

---

## L_C: team-level vs LOO (Alex ask)

| | **LOO L_C (today)** | **Team L_C (PD16)** |
|---|---------------------|---------------------|
| **Unit** | One value per **player** *i* | One value per **team** *j* |
| **Peers** | Teammates **excluding** *i* | Whole roster (all teammates) |
| **Story** | “My congestion field” | “How crowded is this team?” |
| **Alex** | Fine for hero axis; maybe over-customized in **score** | Matches “congestion = good players on the team” |

Alex noted early runs that “worked” used **poolq**-style team context, not LOO, for the congestion-in-score story. He thinks team-level L_C will **come out in the wash** for rankings but wants you to **try it and compare**.

---

## Empirical calibration roadmap (end of meeting)

| Knob | From data? | How (PD16) |
|------|------------|------------|
| **A_i** distribution | Yes | Empirical perf or declared draw |
| **K/N** | Yes | Domain (MBB ~1%, gallery 10%, etc.) |
| **θ** | Yes | Quantile: **θ = F_A⁻¹(1 − K/N)** |
| **ρ** | Yes | Match assignment assortativity in panel |
| **γ, λ** | **Open** | Need principled estimators — **not** “match the hero curve” as the definition |

---

## “Behind an environment flag” — what that literally means

**Not** a new **Anaconda / conda environment.** Same Python, same `conda activate` you use now.

**Yes** — a **shell environment variable** (toggle) read by `sports/scripts/gallery_knobs.py`, the same way the repo already does:

```bash
export GALLERY_PRESET=539
export GALLERY_HERO_SEED=42
export GALLERY_K_OVER_N=0.10
./scripts/build_characterization_slides.sh
```

**PD16 toggles** (implemented in `sports/scripts/gallery_knobs.py`):

| Variable | Default (unchanged deck) | PD16 experimental |
|----------|--------------------------|-------------------|
| `GALLERY_LC_MODE` | `loo_smooth` | `team_smooth` |
| `GALLERY_THETA_MODE` | `preset` (0.72 from 539) | `k_over_n` (quantile from ability draw + K/N) |
| `GALLERY_OUTPUT_SUFFIX` | `` (overwrite baseline names) | `_pd16` (parallel PNGs) |

**Why flags:** Running `./scripts/build_characterization_slides.sh` with **no** exports keeps producing **today’s PNGs** for your hand deck. Opt in when ready:

```bash
./scripts/build_characterization_slides.sh --pd16
```

Or manually:

```bash
export GALLERY_LC_MODE=team_smooth
export GALLERY_THETA_MODE=k_over_n
export GALLERY_OUTPUT_SUFFIX=_pd16
./scripts/build_characterization_slides.sh
```

Then **compare** peak bins, curve shapes, and θ×K/N cells to the current deck — evidence before you change slide footers or benchmarks.

---

## Open work (priority)

1. **Code:** team L_C + θ(K/N) toggles in `gallery_knobs.py` + pool assignment path; compare figures.
2. **Figures:** L_C distribution vs ρ (whiteboard A) — histogram + 2D heatmap.
3. **ρ slide:** try ρ → 0.001; one clean sentence on why ρ matters in this model.
4. **Intro / doc 07:** update θ provenance when naive-draft θ becomes default.
5. **Later:** principled **γ, λ** from data; Menger multiplicative congestion (parked).

---

## Sort-and-chop (unchanged role)

Still the **γ / λ_crit** testbed: extreme assignment removes overlap so **λ_crit ≈ 4/γ** is readable. PD16 congestion changes are **orthogonal** — Alex wants both.

---

## Quotes worth keeping

- **ρ:** “Assortativity is this dialing measure of what’s the spread of the L_Cs.”
- **θ:** “In a world where there was no team congestion, the cutoff … pick θ so that area = K/N.”
- **L_C:** “Congestion should be how many good players are on the team.”
- **Fit:** “Try to find γ and λ without … just make the two curves as close as possible.”

---

## Related files

| Doc | Role |
|-----|------|
| [`07_Phase_B_Characterization_Slides_Explained.md`](07_Phase_B_Characterization_Slides_Explained.md) | Deck walkthrough (pre-PD16 θ/L_C) |
| [`06_Lambda_threshold_and_KN_memo.md`](06_Lambda_threshold_and_KN_memo.md) | λ_crit, sort-and-chop |
| [`CHARLES_CHECKLIST.md`](CHARLES_CHECKLIST.md) | Near-term tasks |
| [`transcripts/PD16_notes.md`](../../transcripts/PD16_notes.md) | Agent-oriented digest + checklist |
