slides/ — HAND deck cheat sheet (HAND16 + HAND17)
==================================================

Naming (Charles shorthand):
  HAND16  = PD16 Phase B sim characterization (fake league, knob sweeps)
  HAND17  = PD17 empirical MBB deck (real rosters, assign → score)

  Pair with HAND17: same *HAND suffix, PD16 vs PD17 prefix.

HAND MASTER files (scripts NEVER overwrite):
  HAND16:  CHAR_PD16_HAND.pptx
  HAND17:  CHAR_PD17_HAND.pptx

  Save As backup before substantive edits, e.g.:
    slides/archive/CHAR_PD16_HAND_backup_YYYYMMDD.pptx
    slides/archive/CHAR_PD17_HAND_backup_YYYYMMDD.pptx

  Scripts write only slides/auto/*_AUTO.pptx and gallery PNGs — never the HAND masters.

  Renamed Aug 2026: CHAR_Phase_B_characterization_HAND.pptx → CHAR_PD16_HAND.pptx
  (archive/ may still hold old filename backups)

----------------------------------------------------------------------
JPEG exports (for agents / visual audit)
----------------------------------------------------------------------
  HAND16:  CHAR_PD16_HAND/Slide1.jpeg … Slide13.jpeg  (re-export after edits)
  HAND17:  CHAR_PD17_HAND/Slide1.jpeg … Slide7.jpeg

  Legacy (pre-trim): HAND_slides_images/ (16 slides), old CHAR_PD16_HAND/Slide17.jpeg

  Charles exports JPEGs (File → Export → images, or Save as Pictures).
  Overwrite SlideN.jpeg names so paths stay stable.

----------------------------------------------------------------------
Regenerate gallery figures (repo root)
----------------------------------------------------------------------
  Phase B PNGs only (safe anytime):
    ./scripts/build_characterization_slides.sh

  Stochastic seed (one dial): export GALLERY_HERO_SEED=42  (default)
  Canonical module: sports/hero_seed.py

  PD16 parallel PNGs (legacy side-by-side; optional):
    ./scripts/build_characterization_slides.sh --pd16

  Disposable AUTO rebuild:
    ./scripts/build_characterization_slides.sh --auto-slides

  auto/CHAR_intro_characterization_AUTO.pptx
  auto/CHAR_sim_input_distributions_AUTO.pptx
  auto/CHAR_rho_characterization_AUTO.pptx         (2 slides)
  auto/CHAR_lc_congestion_characterization_AUTO.pptx (2 slides — Sketch A)
  auto/CHAR_lambda_characterization_AUTO.pptx
  auto/CHAR_theta_characterization_AUTO.pptx       (2 slides)
  auto/CHAR_gamma_characterization_AUTO.pptx       (2 slides)
  auto/CHAR_soft_assign_gamma_sweep_AUTO.pptx
  auto/CHAR_Phase_B_characterization_AUTO.pptx     (merged — not 1:1 HAND16)

Plain-English walkthrough (HAND16):
  ../07_Phase_B_Characterization_Slides_Explained.md

Alex meeting notes:
  ../08_PD16_Alex_meeting_takeaways.md

----------------------------------------------------------------------
L_C box — HAND16 + HAND17 (team smooth; LOO parked Aug 2026)
----------------------------------------------------------------------
  L_C = mean_{j} σ(γ(A_j − θ))  on each roster (team smooth)

  PARKED: LOO L_C — GALLERY_LC_MODE=loo_smooth for legacy runs only.

----------------------------------------------------------------------
HAND16 — canonical slide map (13 slides, Aug 2026 trim)
----------------------------------------------------------------------
  Source: CHAR_PD16_HAND.pptx
  JPEG audit: CHAR_PD16_HAND/

  Dropped from briefing deck (Aug 2026): old PPT 5, 7, 10, 12 — see PARKED below.

| PPT | Knob | Title (short)                              | Primary PNG / AUTO |
|-----|------|----------------------------------------------|--------------------|
|  1  |  —   | Phase B glossary + deck map                  | auto/CHAR_intro_characterization_AUTO.pptx |
|  2  |  —   | Simulated league inputs (A_i, T_j* draws)    | sim_inputs/SIM_league_Ai_Tj_distributions.png |
|  3  |  ρ   | Characterize ρ — sort-and-chop shown         | pass_c_rho/PASS_C_rho_ablation_selection_by_pool_mean_with_sortchop.png |
|  4  |  ρ   | Characterize ρ — sort-and-chop suppressed    | pass_c_rho/PASS_C_rho_ablation_selection_by_pool_mean.png |
|  5  |  λ   | Characterize λ (Pass B)                      | pass_b/PASS_B_lambda_ablation_selection_by_pool_mean.png |
|  6  |  θ   | θ OAT at K/N=10%                             | theta/THETA_OAT_selection_by_pool_mean.png |
|  7  |  θ   | θ compare with computed θ (PD16)             | theta/*_pd16 or computed-θ arm PNG |
|  8  |  θ   | θ × K/N — lines + naive-draft θ vs K/N       | theta/THETA_KN_sweep_peak_bin_lines.png + theta/THETA_KN_sweep_peak_bin_vs_kn.png (or *_pd16) |
|  9  |  γ   | γ sweep — sort-and-chop selection curves     | sort_chop_lambda/GAMMA_sweep_lambda_curves_key_arms.png |
| 10  |  γ   | λ_crit ≈ 4/γ explainer (sort-and-chop only)  | sort_chop_lambda/LAMBDA_threshold_gamma_viability.png |
| 11  | γ,λ  | γ × λ soft assign (overlap rosters)          | soft_assign_lambda/GAMMA_sweep_soft_assign_lambda_curves_key_arms.png |
| 12  |  ρ   | PD16 Sketch A — team L_C vs ρ (strip)        | pass_c_rho/LC_distribution_vs_rho_1d_strip_pd16.png |
| 13  |  ρ   | PD16 Sketch A — T_j vs L_C (2D heatmap)      | pass_c_rho/LC_distribution_vs_rho_2d_pd16.png |

  Change Picture: right-click plot → Change Picture → From File…
  Base folder: 3-Master_Plan/re_entry/HEROs_and_PASSes/

----------------------------------------------------------------------
PARKED — removed from CHAR_PD16_HAND (Aug 2026)
----------------------------------------------------------------------
  Old PPT 5  — ρ before/after θ standardization (migration compare)
  Old PPT 7  — λ before/after θ standardization (migration compare)
  Old PPT 10 — θ×K/N line plot only (duplicate of left panel of old 11)
  Old PPT 12 — θ×K/N heatmap (duplicate of old 10 data)

  PNGs still regenerate; reuse from archive if needed for appendix.

----------------------------------------------------------------------
HAND17 — empirical MBB deck (7 slides)
----------------------------------------------------------------------
  Source: CHAR_PD17_HAND.pptx
  JPEG audit: CHAR_PD17_HAND/

  | # | Block   | Content                              |
  |---|---------|--------------------------------------|
  | 1 | Frame   | PD17 glossary + deck map             |
  | 2 | Assign  | Â_i, T_j inputs                      |
  | 3 | Assign  | Team interval overlap (ρ) + **H_sort** empirical |
  | 4 | Assign  | Grandchild sim interval overlap + **H_sort** (ρ=0.5) |
  | 5 | Score   | Team L_C distribution                |
  | 6 | Score   | Sketch A: T_j vs L_C                 |
  | 7 | Assign  | Sim ρ calibration capstone (1×3)     |

  Regenerate all interval reference slides (3 full + 4/5 window 2015-2019):
    /opt/anaconda3/envs/sports_net/bin/python sports/scripts/rebuild_pd17_interval_reference_slides.py

  Reference outputs → copy into HAND manually:
    Slide 3 (full 2011-2021): auto/CHAR_empirical_team_interval_overlap_AUTO.pptx
    Slide 4 (NCAA 2015-2019): auto/CHAR_empirical_team_interval_overlap_2015_2019_AUTO.pptx
    Slide 5 (sim 2015-2019):  auto/CHAR_grandchild_league_interval_overlap_2015_2019_AUTO.pptx

  HAND master: Change Picture + bullet numbers; keep Office Math you formatted by hand.
  Full PD17 regen cheat sheet: ../empirical_pd17/REGENERATE.md
  Planned: slide 8 — empirical Pass B λ on real MBB.

----------------------------------------------------------------------
VECTOR ASSIGN decks (Aug 2026 — moved from VECTOR_work/)
----------------------------------------------------------------------
  Source folder: slides/  (same as HAND16/HAND17)

  VECTOR_ASSIGN_Dynamic_to_OneShot_Model.pptx
    Parent → Child briefing (3 slides).
    JPEG audit: VECTOR_ASSIGN_Dynamic_to_OneShot_Model/Slide1.jpeg … Slide3.jpeg

  VECTOR_ASSIGN_Grandchild_Model.pptx
    Grandchild endogenous-centroid prototype (ASSIGN-only).
    JPEG audit: VECTOR_ASSIGN_Grandchild_Model/SlideN.jpeg  (export after edits)

  CHAR_grandchild_league_analysis.pptx
    Grandchild sim league — 2×2 interval overlap (HAND17 slide 3 analog).
    Regenerate: /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_league_analysis_slide.py
    Figures: ../grandchild_assign/GRANDCHILD_league_interval_overlap.png

  Markdown/PDF specs remain in 3-Master_Plan/VECTOR_work/ (not duplicated here).

----------------------------------------------------------------------
Other files in slides/
----------------------------------------------------------------------
  CHAR_PD16_HAND.pptx                       HAND16 master
  CHAR_PD17_HAND.pptx                       HAND17 master
  PASS_ABC_Gallery_Slides.pptx              Pass A/B/C intro
  So_Far_.pptx                              Merged Alex deck (slides 1–3)
  VECTOR_ASSIGN_Dynamic_to_OneShot_Model.pptx
  VECTOR_ASSIGN_Grandchild_Model.pptx
  CHAR_grandchild_league_analysis.pptx       Grandchild sim intervals (legacy 2015)
  auto/CHAR_grandchild_rho_assortativity_AUTO.pptx   ρ vs H_sort (Alex validation)
  auto/CHAR_grandchild_h_sort_explainer_AUTO.pptx    H_sort glossary (Alex brief)
  auto/CHAR_grandchild_empirical_lc_compare_AUTO.pptx  Empirical vs sim team L_C (2011-2021)
  auto/CHAR_grandchild_ncaa_roster_size_compare_AUTO.pptx  NCAA vs LG roster sizes fed in (2011-2021)

  Interpret D vs H_sort (Alex brief): ../grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md
  archive/                                  HAND backups
  auto/                                     Script-generated *_AUTO.pptx

  Pass A/B/C gallery: ./scripts/rebuild_hero_gallery.sh
