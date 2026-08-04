slides/ — Phase B hand deck cheat sheet
========================================

HAND MASTER (never overwritten by scripts):
  CHAR_Phase_B_characterization.pptx

Refresh PNGs only (safe anytime):
  ./scripts/build_characterization_slides.sh

Disposable auto rebuild (compare / copy layout):
  ./scripts/build_characterization_slides.sh --auto-slides

  auto/CHAR_intro_characterization_AUTO.pptx    (1 slide — text intro)
  auto/CHAR_rho_characterization_AUTO.pptx      (2 slides)
  auto/CHAR_lambda_characterization_AUTO.pptx   (1 slide)
  auto/CHAR_theta_characterization_AUTO.pptx    (2 slides)
  auto/CHAR_gamma_characterization_AUTO.pptx    (2 slides)
  auto/CHAR_Phase_B_characterization_AUTO.pptx  (8 slides merged)

  Rule: anything in auto/ ends in _AUTO.pptx — never overwrites hand decks
  in slides/ (no _AUTO suffix).

Plain-English walkthrough (all slides):
  ../07_Phase_B_Characterization_Slides_Explained.md

Intro slide only:
  python sports/scripts/build_intro_characterization_slide.py

----------------------------------------------------------------------
CHANGE PICTURE — one row per slide in your hand deck (8 slides + optional)
----------------------------------------------------------------------
PowerPoint: right-click the plot → Change Picture → From File…

Base folder:
  3-Master_Plan/re_entry/HEROs_and_PASSes/

| Slide | Knob | Title (short)                         | PNG / asset |
|-------|------|---------------------------------------|-------------|
|   0   |  —   | Phase B intro (text)                  | Copy from auto/CHAR_intro_characterization_AUTO.pptx |
|   1   |  ρ   | Characterize ρ — sort-and-chop shown  | pass_c_rho/PASS_C_rho_ablation_selection_by_pool_mean_with_sortchop.png |
|   2   |  ρ   | Characterize ρ — sort-and-chop off    | pass_c_rho/PASS_C_rho_ablation_selection_by_pool_mean.png |
|   3   |  λ   | Characterize λ (weight on L_C)        | pass_b/PASS_B_lambda_ablation_selection_by_pool_mean.png |
|   4   |  θ   | θ OAT at K/N=10%                      | theta/THETA_OAT_selection_by_pool_mean.png |
| 5heat |  θ   | θ × K/N — heatmap (hand ~slide 5)     | theta/THETA_KN_sweep_peak_bin.png |
| 5line |  θ   | θ × K/N — line plot (hand ~slide 6)     | theta/THETA_KN_sweep_peak_bin_lines.png |
|   6   |  γ   | γ sweep — selection curves            | sort_chop_lambda/GAMMA_sweep_lambda_curves_key_arms.png |
|   7   |  γ   | λ_crit ≈ 4/γ explainer                | sort_chop_lambda/LAMBDA_threshold_gamma_viability.png |

γ sweep: use *_key_arms.png for slides (3 λ curves × 3 panels).
Full 5-λ grid (dashed intermediates): GAMMA_sweep_lambda_curves.png
Hard vs smooth L_C explainer (optional appendix):
  sort_chop_lambda/VIABILITY_hard_vs_smooth.png

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
