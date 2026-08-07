HEROs_and_PASSes — gallery layout
==================================

Subfolders (scripts write here via sports/scripts/hero_gallery_paths.py):

  pass_a/              Empirical MBB hero + PASS_A_* artifacts
  pass_b/              Generative λ knockout + PASS_B_* ablation
  pass_c_rho/          ρ assignment ablation (PASS_C_rho*, PASS_C_generative*)
  sort_chop_lambda/    Sort-and-chop λ diagnostics (see archive/ for old CSVs)
  theta/               θ OAT and θ × K/N sweep outputs
  slides/              PASS_ABC deck, CHAR_* characterization slides, So_Far_.pptx

Regenerate Phase B (figures only — does not touch your hand deck):
  ./scripts/build_characterization_slides.sh

Hand-edited masters: slides/CHAR_PD16_HAND.pptx (sim), slides/CHAR_PD17_HAND.pptx (empirical)
Change-Picture cheat sheet: slides/README.txt (slide # → PNG path)
Disposable auto templates: slides/auto/*_AUTO.pptx  (--auto-slides)

Regenerate (repo root):

  ./scripts/rebuild_hero_gallery.sh
  GALLERY_HERO_BINS=100 python sports/scripts/sort_chop_lambda_diagnostic.py
  GALLERY_HERO_BINS=100 python sports/scripts/sort_chop_lambda_threshold_zoom.py

Memo: 3-Master_Plan/re_entry/06_Lambda_threshold_and_KN_memo.md
