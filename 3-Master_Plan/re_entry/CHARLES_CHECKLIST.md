# Charles checklist — post-PD16 (manual checkoff)

**Last synced:** 2026-08-05

**Source:** Paper Directions **16** (Aug 4, 2026) — [`../../transcripts/PD16_notes.md`](../../transcripts/PD16_notes.md); narrative [`08_PD16_Alex_meeting_takeaways.md`](08_PD16_Alex_meeting_takeaways.md)

**Supersedes:** [`archive/checklists/CHARLES_CHECKLIST_archive_20260804_pd15.md`](archive/checklists/CHARLES_CHECKLIST_archive_20260804_pd15.md) (PD15 characterization deck arc).

**Where we are:** Phase B **characterization deck is built** (intro + ρ, λ, θ, θ×K/N, γ, λ_crit) and you **briefed Alex (PD16)**. Alex accepted the deck structure and sort-and-chop story. **Near-term mission shifted:** implement **team-level L_C**, **θ from K/N**, and **L_C-vs-ρ distribution diagnostics** — then move toward **data-linked ρ, θ** and principled **γ, λ** (not “match the hero curve” as the definition).

**How to use**

1. Work **top to bottom**.  
2. Change `[ ]` → `[x]` only when **you** finished that row.  
3. Fill **Proof** with a path, date, or one-line note.  
4. **Two decks:** `So_Far_.pptx` (Pass A/B/C gallery, slides 1–3) ≠ `CHAR_Phase_B_characterization.pptx` (OAT sensitivity deck).  
5. **Score:** \(S_i = A_i - \lambda L_C\); **λ** = weight on congestion; **L_C** = congestion (smooth sigmoid in current deck).

**Notation:** [`02_Three_Kinds_of_Model.md`](02_Three_Kinds_of_Model.md) § Notation addendum — **K** = slots, **λ** = weight on **L_C**, default **K/N = 10%**.

**Not this file:** Agent status in `model_OPORD.md`, doc 03, COMPASS stubs.

---

## Locked — already on disk (do not redo unless asked)

| Artifact | Location | Notes |
|----------|----------|-------|
| Phase B hand deck | `HEROs_and_PASSes/slides/CHAR_Phase_B_characterization.pptx` | Scripts never overwrite — you format in PowerPoint |
| Auto compare deck | `HEROs_and_PASSes/slides/auto/CHAR_intro_characterization_AUTO.pptx` | `./scripts/build_characterization_slides.sh --auto-slides` |
| Slide walkthrough | [`07_Phase_B_Characterization_Slides_Explained.md`](07_Phase_B_Characterization_Slides_Explained.md) | Seed 42, T_j, hard vs smooth L_C, sort-and-chop |
| PD16 takeaways | [`08_PD16_Alex_meeting_takeaways.md`](08_PD16_Alex_meeting_takeaways.md) | Whiteboard sketches, calibration roadmap |
| λ_crit memo | [`06_Lambda_threshold_and_KN_memo.md`](06_Lambda_threshold_and_KN_memo.md) | Sort-and-chop; λ_crit ≈ 4/γ |
| θ×K/N sweep | `HEROs_and_PASSes/theta/THETA_KN_sweep_*` | Run with **preset θ** — revisit after θ(K/N) |
| γ readable plots | `HEROs_and_PASSes/sort_chop_lambda/GAMMA_sweep_lambda_curves_key_arms.png` | Full grid: `GAMMA_sweep_lambda_curves.png` |
| Pass A/B/C gallery PNGs | `HEROs_and_PASSes/pass_a/`, `pass_b/`, `pass_c_rho/` | Refresh: `./scripts/rebuild_hero_gallery.sh` |
| Regenerate char PNGs | `./scripts/build_characterization_slides.sh` | Then **Change Picture** in hand deck if plots changed |

---

## Phase B — Characterization deck (built — your sign-off)

**Agent/build status:** scripts and PNGs exist for all rows below except **A_i** and **t_j** robustness. **Your job:** approve each claim in the hand deck and mark `[x]` when you can defend it to Alex.

| Done | Item | What “done” means | Proof |
|------|------|-------------------|-------|
| [x] | **Intro / glossary** | You can walk equations, benchmarks (A_i, T_j), seed 42, “not curve-fitting” | PD16 Aug 4; hand deck slide 0; doc 07 SLIDE 0 |
| [x] | **ρ OAT** | Both curves move; “assortativity matters” | PD16 Aug 4; hand deck slides 1–2; `pass_c_rho/` |
| [x] | **λ OAT** | Talent-only vs λ>0 bend on A_i-binned curve | PD16 Aug 4; hand deck slide 3; `pass_b/PASS_B_lambda_ablation_*.png` |
| [x] | **θ OAT (preset v1)** | Sigmoid center sweep at **preset θ** (539 / 0.72 arms) | Slides 4–5; PD16 Aug 4. **Definition refresh** → PD16 row 2 below |
| [x] | **θ × K/N panel** | Co-movement before fixing θ rule | `theta/THETA_KN_sweep_*` |
| [ ] | **γ + λ_crit** | Sort-and-chop; readable γ sweep; λ_crit ≈ 4/γ story | Hand deck slides 6–7; doc 07 |
| [x] | **Walkthrough PDF** | Plain-English deck guide for you / Alex | doc 07 (+ your PDF if printed) |
| [x] | **PD16 briefing** | Alex saw deck; direction captured | Aug 4 meeting; doc 08 |
| [ ] | **A_i distribution** | Robustness: default + 1–2 alternatives (SI note) | *Not built* |
| [ ] | **t_j distribution** | Empirical ballpark + brief sensitivity | *Not built* |

**Phase B “characterized” when:** you mark the rows above `[x]` (except A_i/t_j if deferred) **and** Alex agrees the OAT deck answered “what moves when I turn this knob?” — **not** “we fit to data.”

---

## PD16 follow-ups — Alex’s new direction (priority order)

Implement via **shell env vars** in `gallery_knobs.py` (`GALLERY_LC_MODE`, `GALLERY_THETA_MODE`) — **not** a new conda environment. Defaults unchanged = current deck PNGs.

| Done | Priority | What to do | Proof |
|------|----------|------------|-------|
| [x] | **1. Team-level L_C** | Congestion = property of **team j** (same for all roster players); compare Pass B curves to LOO default | `tier1_pool_assignment.add_team_pool_columns`; `*_pd16.png` |
| [x] | **2. θ from K/N** | Naive-draft quantile: θ = F_A⁻¹(1 − K/N) on ability draw (Beta in sim); re-run θ OAT + θ×K/N | `gallery_knobs.resolve_viability_theta`; `theta/*_pd16.png` |
| [ ] | **3. L_C distribution vs ρ** | Whiteboard Sketch A: histogram # teams vs L_C per ρ arm; 2D heatmap team ability vs L_C | new script + slide gap filled |
| [ ] | **4. ρ low arm + intuition** | Try **ρ → 0.001**; one clean sentence why ρ matters in *this* construction | PNG + footer note on ρ slide |
| [ ] | **5. Update intro / doc 07** | When θ provenance shifts (539 preset → K/N quantile), refresh intro slide + walkthrough | slide + doc 07 § θ |
| [ ] | **6. Env-var walkthrough** | You can `export GALLERY_…` or `./scripts/build_characterization_slides.sh --pd16` | run yourself in PowerPoint compare |

**PD16 implementation done when:** team L_C + θ(K/N) modes run side-by-side with current deck; L_C-vs-ρ figures exist; you and Alex agree ρ/θ are **data-identifiable** in principle.

---

## Lingering from PD15 — still open (lower priority unless Alex asks)

**Phase A gallery (`So_Far_.pptx` slides 1–3)** — separate from Phase B deck; never fully checked off.

| Done | Step | What to do | Proof |
|------|------|------------|-------|
| [ ] | **λ ablation panel** | Fix ρ; vary λ (four values — mirror Pass C layout) | PNG path |
| [ ] | **Sim double-plot** | One run: 16 bins on **A_i** (left) and **poolq_loo** (right) | PNG path |
| [ ] | **λ overlay** | A_i-binned: λ=0 vs λ>0 overlay | PNG path |
| [ ] | **Sort-and-chop on Pass C ρ** | Sort-and-chop arm on gallery ρ figure | PNG path |
| [ ] | **Fitted inputs on gallery** | Report **t_j**, σ²; data-fitted vs sim-drawn | slide note |
| [ ] | **Refresh So_Far_** | `./scripts/rebuild_hero_gallery.sh`; open in **PowerPoint** | date |

**Optional checkpoint (pre-PD16):** ρ × λ interaction panel if a marginal sweep looked flat — ask Alex if still needed after team L_C work.

---

## Phase C — Calibration & fit (parked until PD16 rows 1–4 clear)

Alex PD16 roadmap: **A_i, K/N, θ, ρ** from data; only **γ, λ** remain free — fit via **data properties**, not “make sim curve match hero.”

| Done | Step | Pointer | Proof |
|------|------|---------|-------|
| [ ] | **ρ from data** | Match assignment assortativity in empirical data | estimator + note |
| [ ] | **θ from data** | Quantile at 1 − K/N on empirical or declared A distribution | ties to PD16 row 2 |
| [ ] | **γ, λ estimators** | Principled fit — **not** hero-curve matching as definition | memo / Alex sign-off |
| [ ] | **PD14 magnitude** | [`05_Alex_Magnitude_Spec.md`](05_Alex_Magnitude_Spec.md) — predictive importance A vs B | |
| [ ] | **Notation cleanup** | σ used twice (team σ_j vs sigmoid) | Model.pptx |

---

## Parked (good ideas, wrong moment)

| Item | Pointer |
|------|---------|
| Menger multiplicative congestion | Alex OK to park; 4-sentence memo if he asks |
| Preferential attachment sweep | After boolean default validated |
| Old 14-doc reading stack | [`PARKED_FOR_LATER.md`](PARKED_FOR_LATER.md) |
| Rebuild empirical hero from `530` | Not a gate |
| Army / tenure figures | Out of scope |

---

## Explicitly not on this checklist

- Bin-for-bin LOO match as a gate  
- B vs D decomposition (use **L_C** only for now)  
- Agent “Done” tables in OPORD / doc 03  

---

## Next action right now

1. **Sign off remaining Phase B rows** — **γ + λ_crit** (slides 6–7); defer **A_i / t_j** unless Alex asks.  
2. **Start PD16 row 1** — team-level L_C in code (`GALLERY_LC_MODE=team_smooth` when ready).  
3. **Read doc 08** if you need the whiteboard / calibration story in one sitting: [`08_PD16_Alex_meeting_takeaways.md`](08_PD16_Alex_meeting_takeaways.md).  
4. **Defer Phase A gallery** unless Alex asks for `So_Far_.pptx` refresh before team L_C lands.
