slides/ — HAND deck cheat sheet (HAND16 + HAND17 + HAND20)
==================================================

Naming (Charles shorthand):
  HAND16  = PD16 Phase B sim characterization (fake league, knob sweeps)
  HAND17  = PD17 empirical MBB deck (real rosters, assign → score)

  Pair with HAND17: same *HAND suffix, PD16 vs PD17 prefix.

HAND MASTER files (scripts NEVER overwrite):
  HAND16:  CHAR_PD16_HAND.pptx
  HAND17:  CHAR_PD17_HAND.pptx
  HAND20:  CHAR_PD20_HAND.pptx
  BDP:     Basics_data_plots_HAND.pptx  (back-to-basics data plots, Aug 2026)

  Save As backup before substantive edits, e.g.:
    slides/archive/CHAR_PD16_HAND_backup_YYYYMMDD.pptx
    slides/archive/CHAR_PD17_HAND_backup_YYYYMMDD.pptx
    slides/archive/CHAR_PD20_HAND_backup_YYYYMMDD.pptx

  Scripts write only slides/auto/*_AUTO.pptx and gallery PNGs — never the HAND masters.

  Renamed Aug 2026: CHAR_Phase_B_characterization_HAND.pptx → CHAR_PD16_HAND.pptx
  (archive/ may still hold old filename backups)

----------------------------------------------------------------------
JPEG exports (for agents / visual audit)
----------------------------------------------------------------------
  HAND16:  CHAR_PD16_HAND/Slide1.jpeg … Slide13.jpeg  (re-export after edits)
  HAND17:  CHAR_PD17_HAND/Slide1.png … SlideN.png  (re-export after edits)
  HAND20:  CHAR_PD20_HAND/Slide1.png … Slide21.png  (re-export after edits)
  BDP:     Basics_data_plots_HAND/SlideN.png  (re-export after edits)

  BDP script PNGs (source figures Charles inserts into deck):
    ../basic_data_plots/*.png

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
HAND17 — empirical MBB deck (expanded Aug 2026)
----------------------------------------------------------------------
  Source: CHAR_PD17_HAND.pptx
  PNG audit: CHAR_PD17_HAND/

  Suggested Assign block (after interval pair slides 4–5):
    • global_wss ρ validation (Alex primary) — paste from AUTO below
    • H_sort glossary (Slide 6 in current deck) OR ρ vs H_sort companion
    • Optional appendix: 539 ρ capstone (Slide 21)

  Regenerate λ SELECT sweep (empirical caps held fixed):
    python sports/scripts/grandchild_lambda_select_sweep.py
    python sports/scripts/build_alex_lambda_select_sweep_light_slides.py

  Regenerate ρ validation AUTO decks (global_wss + H_sort companion):
    python sports/scripts/build_pd17_rho_validation_slides.py --slides-only

  Regenerate interval reference slides (full + 2015-2019 window):
    python sports/scripts/rebuild_pd17_interval_reference_slides.py

  Reference outputs → copy into HAND manually:
    Interval: auto/CHAR_empirical_team_interval_overlap_AUTO.pptx (full)
              auto/CHAR_empirical_team_interval_overlap_2015_2019_AUTO.pptx
              auto/CHAR_grandchild_league_interval_overlap_2015_2019_AUTO.pptx
    ρ (Alex): auto/CHAR_grandchild_rho_global_wss_AUTO.pptx  ← primary
              auto/CHAR_grandchild_rho_assortativity_AUTO.pptx  ← H_sort companion
    Glossary: auto/CHAR_grandchild_h_sort_explainer_AUTO.pptx

  Figures: grandchild_assign/GRANDCHILD_rho_vs_global_wss.png
           grandchild_assign/GRANDCHILD_rho_vs_assortativity.png
           grandchild_assign/GRANDCHILD_lambda_select_sweep_2011_2021.png

  HAND master: Change Picture + bullets; keep Office Math you formatted by hand.
  Memo: ../grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md

----------------------------------------------------------------------
HAND20 — Alex deck (PD20 + PD22 + PD21, Aug 2026)
----------------------------------------------------------------------
  Source: CHAR_PD20_HAND.pptx
  PNG audit: CHAR_PD20_HAND/Slide1.png … Slide21.png
  **21 slides** (Aug 18 2026): PD20 → PD22 panel build → PD21 ρ → PD22 policy/overlap

  Story arc (current deck order):
    Act I    PD20 Gibbs SELECT gate (slides 1–4)
    Act II   PD22 why the hero panel exists (slides 5–13)
    Act III  PD21 ρ* on hero + ppm0lt20 contrast (slides 14–16)
    Act IV   PD22 drop vs PPM-zero + overlap reconciliation (slides 17–21)

  Suggested read-aloud order (optional reorder): Acts I → II → IV (17–19) → III (14–16)
  → IV (20–21). Policy evidence (19) before locking ρ (14); overlap (20–21) after ρ.

  Save As backup before substantive edits:
    slides/archive/CHAR_PD20_HAND_backup_YYYYMMDD.pptx

  HAND workflow: AUTO decks in slides/auto/*_AUTO.pptx → **Change Picture** for the
  figure on the right; keep/edit **left sidebar text boxes** (title, subtitle, bullets,
  claim) in HAND. Office Math applied by hand after paste. Slides 14–16 follow this
  layout (editable bullets + figure — not a full-slide flatten).

| PPT | Block | Title (short) | AUTO / PNG |
|-----|-------|---------------|------------|
|  1  | PD20  | Gibbs SELECT intro | auto/CHAR_PD20_HAND_AUTO slide 1 |
|  2  | PD20  | Temperature sweep (rule D) | pd20_temperature/GRANDCHILD_temperature_select_sweep_2011_2021.png |
|  3  | PD20  | Cold limit — rule C vs D | pd20_temperature/GRANDCHILD_temperature_cold_limit_2011_2021.png |
|  4  | PD20  | PD20 takeaways | text (PD20 block in CHAR_PD20_HAND_AUTO) |
|  5  | PD22  | Roster size — raw box (before QC) | pd22_minutes/PD22_raw_roster_size_distribution_before_qc_*.png |
|  6  | PD22  | Games per team-season — before QC | pd22_minutes/PD22_team_season_games_count_*.png |
|  7  | PD22  | Games per team-season — after QC | pd22_minutes/PD22_team_season_games_count_after_qc_*.png |
|  8  | PD22  | Roster size — box-QC panel vs min-20 | pd22_minutes/PD22_raw_roster_size_distribution_after_qc_*.png |
|  9  | PD22  | ESPN coverage 2013→2014 depth break | pd22_minutes/PD22_espn_coverage_by_season_*.png |
| 10  | PD22  | Drafted-player retention vs floor | pd22_minutes/PD22_drafted_minutes_audit_*.png |
| 11  | PD22  | Raw panel season-minutes distribution | pd22_minutes/PD22_raw_minutes_distribution_*.png |
| 12  | PD22  | PPM — filtered tail vs hero ASSIGN input | pd22_minutes/PD22_ppm_distribution_*.png |
| 13  | PD22  | PPM overlay — full vs sub-20 tail | pd22_minutes/PD22_ppm_full_vs_filtered_*.png |
| 14  | PD21  | Calibrate ρ — hero panel (locked) | auto/CHAR_PD21_rho_hsort_calibrate_AUTO.pptx (figure) |
| 15  | PD21  | Calibrate ρ — ppm0lt20 contrast | auto/CHAR_PD21_rho_hsort_calibrate_ppm0lt20_AUTO.pptx |
| 16  | PD21  | Per-season ρ* timeseries (contrast) | auto/CHAR_PD21_rho_hsort_timeseries_ppm0lt20_AUTO.pptx |
| 17  | PD22  | PPM-zero vs drop — ability distribution | auto/CHAR_PD22_ppm_zero_ability_distribution_AUTO.pptx |
| 18  | PD22  | Bench-zero clustering vs H_sort | auto/CHAR_PD22_ppm_zero_hsort_mechanism_AUTO.pptx |
| 19  | PD22  | Panel policy — drop vs PPM-zero at min 20 | auto/CHAR_PD22_panel_policy_compare_AUTO.pptx |
| 20  | PD22  | Interval overlap — season 2012 (ρ*=0) | auto/CHAR_PD22_interval_overlap_season_2012_AUTO.pptx |
| 21  | PD22  | Interval overlap — season 2013 (ρ*=0) | auto/CHAR_PD22_interval_overlap_season_2013_AUTO.pptx |

  Cross-slide pairs for Alex:
    • Slides 9 + 16 — ESPN depth break explains ppm0lt20 2013→2014 jump
    • Slides 12 + 13 — PPM tails (detail vs overlay); slide 13 optional appendix trim
    • Slides 14 vs 15 — locked hero (ρ*=0 all seasons) vs ppm0lt20 contrast (wrong estimand)
    • Slide 14 — box QC lowered H_sort (~0.10→~0.06); pre-QC mixed ρ* archived in
      H_sort_calibration_backups_PD20.pptx — not the locked estimand
    • Slides 17 → 19 — PPM-zero mechanism then policy decision (drop wins)
    • Slides 20 + 21 — overlap persists at ρ*=0; Alex's 2013 ρ*≈0.07 was pre-box-QC panel

  Talking thread for Alex:
    • PD20 cleared → panel choices matter before ρ calibration
    • Raw ESPN box is messy (roster tails, one-game seasons) → box QC fixes it
    • 2013→2014 ESPN lists more bench rows — hero min-20 panel is flat (slide 9)
    • Draft-safe at min=0; hero ASSIGN uses min≥20 for PPM stability
    • Drop at 20 (not PPM-zero): same policy slide 14 already uses — no ρ re-calibration needed
    • Hero panel: ρ*=0, modest H_sort — not “NCAA is random”
    • ppm0lt20 contrast: inflated ρ* + 2014 jump — illustrative only
    • ρ*=0 but overlap plots look sorted — different questions (slides 20–21)

  Regenerate: pd20_temperature/REGENERATE.md, pd21_rho/README.md, pd22_minutes/README.md

  **2013–2021 contrast run (excludes 2011–2012, Alex PD23):**
    ./scripts/regenerate_pd20_22_auto_13_21.sh
    → PNG/JSON tagged *_2013_2021.* ; AUTO decks *_13_21_AUTO.pptx (parallel to full panel)
    SLIDES_ONLY=1 ./scripts/regenerate_pd20_22_auto_13_21.sh   # decks only, if figures exist
    Side-by-side diff checklist: slides/PD20_22_13_21_vs_full_panel_diff.md

  Memo (H_sort): ../grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md
  Takeaways memo (narrative companion): auto/CHAR_PD20_22_takeaways_memo_AUTO.pptx
    ~46 slides — wavetops (Parts 0–2 + bridges) → snag bridge + snag + Q1–Q3 → Act bridges →
    one narrative companion per HAND slide (footer: paste HAND N after) →
    where we stand + what lies ahead (main line, Rung 3, parked, manuscript) → closing
    Regenerate: python sports/scripts/build_pd20_22_takeaways_memo.py
  Big-picture prose (wavetops → now): ../PD20_22_campaign_big_picture.md

  Reorder history:
    • Aug 17 — PD22 backup block (5–13) moved before PD21 ρ (14–16)
    • Aug 18 — PD22 policy/overlap block appended (17–21)
  Pre-box-QC ρ calibration figures: slides/H_sort_calibration_backups_PD20.pptx

----------------------------------------------------------------------
VECTOR ASSIGN decks (Aug 2026 — moved from VECTOR_work/)
----------------------------------------------------------------------
  Source folder: slides/  (same as HAND16/HAND17/HAND20)

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
  CHAR_PD20_HAND.pptx                       HAND20 master (PD20+21+22 Alex deck)
  PASS_ABC_Gallery_Slides.pptx              Pass A/B/C intro
  So_Far_.pptx                              Merged Alex deck (slides 1–3)
  VECTOR_ASSIGN_Dynamic_to_OneShot_Model.pptx
  VECTOR_ASSIGN_Grandchild_Model.pptx
  CHAR_grandchild_league_analysis.pptx       Grandchild sim intervals (legacy 2015)
  auto/CHAR_grandchild_rho_global_wss_AUTO.pptx       ρ vs global_wss (Alex primary)
  auto/CHAR_grandchild_rho_assortativity_AUTO.pptx   ρ vs H_sort (companion)
  auto/CHAR_grandchild_h_sort_explainer_AUTO.pptx    H_sort glossary (Alex brief)
  auto/CHAR_grandchild_empirical_roster_caps_lc_AUTO.pptx  Empirical vs sim team L_C (2011-2021)
  auto/CHAR_grandchild_lambda_select_sweep_AUTO.pptx     λ sweep on SELECT (empirical caps)
  auto/CHAR_grandchild_ncaa_roster_size_compare_AUTO.pptx  NCAA vs LG roster sizes fed in (2011-2021)
  auto/CHAR_hero_min_minutes_sensitivity_compare_AUTO.pptx  min_minutes ladder side-by-side (Alex)
  auto/CHAR_hero_min_minutes_sensitivity_overlay_AUTO.pptx  min_minutes ladder overlay (Alex)
  auto/CHAR_ncaa_roster_size_distribution_AUTO.pptx         NCAA roster sizes at min 20 (Alex)

  Interpret D vs H_sort (Alex brief): ../grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md
  archive/                                  HAND backups
  auto/                                     Script-generated *_AUTO.pptx

  Pass A/B/C gallery: ./scripts/rebuild_hero_gallery.sh
