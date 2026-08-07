# 8. PD16 — Alex meeting takeaways (Aug 4, 2026)

**Last synced:** 2026-08-07

**Audience:** Charles, re-entering after the Phase B characterization briefing.

**Standalone:** definitions inline; no scavenger hunt required.

**Source transcript:** `transcripts/20260804_Paper_Directions_16_otter_ai_transcript.docx`

**Working digest (agents):** `transcripts/PD16_notes.md`

**Deck briefed:** `HEROs_and_PASSes/slides/CHAR_PD16_HAND.pptx` (+ walkthrough doc 07).

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
- **y:** realized team talent **T_j** (mean **A_i** on roster; empirical **T_jt** from **Â_i**)
- **Color:** number of teams in each cell

**Question answered:** Do better teams have more congestion? **Yes** — expect an upward cloud (your wiggly diagonal in the oval).

**Why this matters:** Gives ρ a **model-internal** interpretation Alex can cite, beyond “the selection-by-pool-mean plot moved.”

**Built (Aug 2026):** `sports/scripts/lc_distribution_vs_rho_diagnostic.py` →
`pass_c_rho/LC_distribution_vs_rho_1d_strip{SUFFIX}.png`, `LC_distribution_vs_rho_2d{SUFFIX}.png`.
Included in `./scripts/build_characterization_slides.sh` (and `--pd16`).

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

| | **LOO L_C (parked Aug 2026)** | **Team L_C (default)** |
|---|---------------------|---------------------|
| **Unit** | One value per **player** *i* | One value per **team** *j* |
| **Peers** | Teammates **excluding** *i* | Whole roster (all teammates) |
| **Story** | “My congestion field” | “How crowded is this team?” |
| **Alex** | Fine for hero axis; parked in **score** | Matches “congestion = good players on the team” |

Alex noted early runs that “worked” used **poolq**-style team context, not LOO, for the congestion-in-score story. He thinks team-level L_C will **come out in the wash** for rankings but wants you to **try it and compare**.

---

## Pass C ρ slide — why low-ρ is **not** completely flat (and should not be)

**HAND16 slides 3–4** (Pass C assignment ablation). Old copy said low ρ → “nearly flat” curve. **Corrected Aug 2026** after seed sweep + CSV audit. Briefing deck trimmed to **13 slides** (`CHAR_PD16_HAND.pptx`) Aug 2026 — dropped migration compare slides (old PPT 5, 7, 10, 12).

### What you see (ρ = 0.001, seed 42, current defaults)

| Pool-mean bin | Selection rate (approx.) |
|---------------|--------------------------|
| 1 (weakest) | 0.05 |
| 16 (strongest) | 0.14 |

The blue arm **tilts upward** — it does **not** look horizontal next to ρ = 32 (flat bottom near 0, peak ~0.25 at bin 14, dip at bin 16).

### Is it a seed-42 artifact?

**No.** Re-ran Pass C at ρ = 0.001, λ = 0.55, team L_C, θ(K/N) for seeds {1, 7, 13, 42, 99, 123, 427, 1000}: **every seed** has bin 16 > bin 1 (delta roughly +0.04 to +0.09). Changing `GALLERY_HERO_SEED` reshapes bin noise but **does not remove** the uptilt.

### Why it **should** tilt (plain English for Alex)

1. **Fixed score:** **S_i = A_i − λ L_C** with λ = 0.55; global **top-K** selection (10%).
2. **Low ρ:** rosters mix → **L_C is nearly the same on every team** (Sketch A: one narrow hump ~0.15). Assignment is **not** stratifying peer pressure yet.
3. **X-axis:** 16 **quantile bins of realized team mean ability** (pool mean after assignment).
4. **Selection logic:** take the best scores league-wide. Higher bins contain better players on average → **more selections from those bins**, even when L_C does not vary much.
5. **Contrast with high ρ:** assortativity creates **different L_C worlds** → inverted-U (weak bins near zero selection, interior peak, elite-bin dip). That is the **assignment** story ρ is meant to show.

**One-liner for Alex:**

> At low ρ the curve isn’t flat because global top-K on talent still favors stronger pool-mean bins — what ρ adds at high values is the **inverted-U**, not the baseline slope.

**Not a bug; don’t re-seed hoping ρ = 0.001 goes horizontal.** Slide claim updated to: *low ρ → weak monotone tilt (no inverted-U); high ρ → peer-pressure hump.*

**At λ = 0** the same ρ = 0.001 arm tilts **more** (bin 1 → bin 16 delta ≈ +0.17 at seed 42) — congestion in score actually **moderates** the baseline slope at low ρ.

---

## Stochastic seed — one dial (Aug 2026)

**Canonical:** `sports/hero_seed.py` → reads **`GALLERY_HERO_SEED`** (default **42**).

Wired through: all Phase B gallery diagnostics (`gallery_knobs.HERO_SEED`), `tier1_sim_config.RANDOM_SEED` / `MATCH_539_RANDOM_SEED`, `build_characterization_slides.sh`, `rebuild_hero_gallery.sh`.

```bash
export GALLERY_HERO_SEED=99
./scripts/build_characterization_slides.sh
```

**Exception (unchanged):** `MATCH_539_FULL_RANDOM_SEED = 1` for full-scale 539 reference JSON — separate calibration anchor.

---

## HAND16 deck trim + rename (Aug 2026)

**Renamed:** `CHAR_Phase_B_characterization_HAND.pptx` → **`CHAR_PD16_HAND.pptx`** (pairs with `CHAR_PD17_HAND.pptx`).

**Trimmed to 13 briefing slides** — removed:
- Old PPT **5, 7** — ρ/λ before-after θ migration compares
- Old PPT **10, 12** — duplicate θ×K/N line-only and heatmap

**Canonical map:** `HEROs_and_PASSes/slides/README.txt` · walkthrough doc 07.

---

## Sort-and-chop vs soft assign — λ/γ slides (Aug 2026)

**Keep** sort-and-chop γ × λ grid + λ_crit ≈ 4/γ as a **disjoint benchmark** (HAND deck — do not delete).

**Add** parallel **soft-assign** γ × λ sweep (overlapping rosters, fixed ρ, team L_C, θ(K/N)) — overlaps like PD17 empirical target; **no** 4/γ claim on overlap panels.

**One sentence for Alex:**

> We kept sort-and-chop to show when congestion must enter the score on disjoint rosters; we’re adding the same λ/γ readouts under soft assign because that’s the overlap regime real rosters live in — and that’s where we’ll pin λ on data.

**HAND workflow:** scripts write only `slides/auto/*_AUTO.pptx` and PNGs — **never** overwrite `CHAR_PD16_HAND.pptx` or `CHAR_PD17_HAND.pptx`. Charles edits HAND masters in PowerPoint; Save As backup before substantive changes recommended.

**Figures:** `soft_assign_lambda/GAMMA_sweep_soft_assign_lambda_curves_key_arms.png`  
**AUTO slide:** `slides/auto/CHAR_soft_assign_gamma_sweep_AUTO.pptx`

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

| Variable | Default (Aug 2026) | Legacy / parked |
|----------|-------------------|-----------------|
| `GALLERY_LC_MODE` | `team_smooth` | `loo_smooth` |
| `GALLERY_THETA_MODE` | `k_over_n` (quantile from ability draw + K/N) | `preset` (0.72 from 539) |
| `GALLERY_OUTPUT_SUFFIX` | `` (overwrite baseline names) | `_pd16` (parallel PNGs) |
| `GALLERY_HERO_SEED` | `42` (`sports/hero_seed.py`) | any int — one dial for gallery + tier1 default RNG |

**Default run** (no exports needed):

```bash
./scripts/build_characterization_slides.sh
```

Produces team $L_C$ + $\theta(K/N)$ on all characterization PNGs. For parallel `_pd16` copies only:

```bash
./scripts/build_characterization_slides.sh --pd16
```

Legacy LOO $L_C$ (parked):

```bash
export GALLERY_LC_MODE=loo_smooth
export GALLERY_THETA_MODE=preset
./scripts/build_characterization_slides.sh
```

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
