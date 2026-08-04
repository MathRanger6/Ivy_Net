slides/ — Phase B hand deck cheat sheet
========================================

HAND MASTER (never overwritten by scripts):
  CHAR_Phase_B_characterization.pptx

Refresh PNGs only (safe anytime):
  ./scripts/build_characterization_slides.sh

Disposable auto rebuild (compare / copy layout):
  ./scripts/build_characterization_slides.sh --auto-slides

  auto/CHAR_rho_characterization_AUTO.pptx      (2 slides)
  auto/CHAR_lambda_characterization_AUTO.pptx   (1 slide)
  auto/CHAR_theta_characterization_AUTO.pptx    (2 slides)
  auto/CHAR_gamma_characterization_AUTO.pptx    (2 slides)
  auto/CHAR_Phase_B_characterization_AUTO.pptx  (7 slides merged)

  Rule: anything in auto/ ends in _AUTO.pptx — never overwrites hand decks
  in slides/ (no _AUTO suffix).

Plain-English walkthrough (all 7 slides):
  ../07_Phase_B_Characterization_Slides_Explained.md

----------------------------------------------------------------------
CHANGE PICTURE — one row per slide in your hand deck (7 slides)
----------------------------------------------------------------------
PowerPoint: right-click the plot → Change Picture → From File…

Base folder:
  3-Master_Plan/re_entry/HEROs_and_PASSes/

| Slide | Knob | Title (short)                         | PNG to link |
|-------|------|---------------------------------------|-------------|
|   1   |  ρ   | Characterize ρ — sort-and-chop shown  | pass_c_rho/PASS_C_rho_ablation_selection_by_pool_mean_with_sortchop.png |
|   2   |  ρ   | Characterize ρ — sort-and-chop off    | pass_c_rho/PASS_C_rho_ablation_selection_by_pool_mean.png |
|   3   |  λ   | Characterize λ (congestion in score)  | pass_b/PASS_B_lambda_ablation_selection_by_pool_mean.png |
|   4   |  θ   | θ OAT at K/N=10%                      | theta/THETA_OAT_selection_by_pool_mean.png |
|   5   |  θ   | θ × K/N panel (selectivity)           | theta/THETA_KN_sweep_peak_bin.png |
|   6   |  γ   | γ sweep — selection curves            | sort_chop_lambda/GAMMA_sweep_lambda_curves.png |
|   7   |  γ   | λ_crit ≈ 4/γ explainer                | sort_chop_lambda/LAMBDA_threshold_gamma_viability.png |

Slide order matches auto/CHAR_Phase_B_characterization_AUTO.pptx if you need
to compare against a fresh script build.

----------------------------------------------------------------------
L_C box (slides 4–5) — if you re-type in Equation Editor
----------------------------------------------------------------------
  L_C = mean_{j≠i} σ(γ(A_j − θ))

  LOO over teammates j≠i; σ = logistic sigmoid; NOT poolq_loo, NOT A_i.

----------------------------------------------------------------------
Other decks in this folder
----------------------------------------------------------------------
  PASS_ABC_Gallery_Slides.pptx   Pass A/B/C intro (rebuild_hero_gallery.sh)
  So_Far_.pptx                   Your merged Alex deck (slides 1–3 auto-refresh)

  auto/                          Script-generated *_AUTO.pptx only — delete old non-AUTO copies if any

----------------------------------------------------------------------
Regenerate commands (repo root)
----------------------------------------------------------------------
  Figures for Phase B hand deck:
    ./scripts/build_characterization_slides.sh

  Pass A/B/C gallery (slides 1–3 of So_Far_):
    ./scripts/rebuild_hero_gallery.sh
