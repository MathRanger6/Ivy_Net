basic_data_plots/ — BDP (Basic Data Plots) analysis outputs
============================================================

Charles (Aug 2026): all **new PNGs** created during the back-to-basics /
BDP plot recreation workflow go **here**, not pass_a/ root or sensitivity/.

HAND deck (Charles edits; scripts do NOT overwrite):
  slides/Basics_data_plots_HAND.pptx

Slide audit exports (Charles exports after deck edits):
  slides/Basics_data_plots_HAND/SlideN.png
  First slide = titled index (same convention as HAND16/17/20).

Agent / script PNG outputs for BDP:
  3-Master_Plan/re_entry/HEROs_and_PASSes/basic_data_plots/

Naming: descriptive prefix + filter ladder tag, e.g.
  BDP_pass_a_side_by_side_all_seasons_no_qc.png
  BDP_pass_a_side_by_side_mg10_min20_2011_2021.png

Related CSV/JSON (if any) may live alongside PNGs in this folder.

Filter shorthand (Basics_data_plots_HAND slide 3 — parameterized):
  QC           MINIMUM DATA SET — ALWAYS ON for BDP. Only ESPN "-" placeholder
               name rows removed. NEVER assume mg10 (or min20) unless Charles
               names mgN / minN in the request.
  FP           full population within QC (no mgN / minN unless listed)
  NN_NN        season window (e.g. 11_21 = 2011–2021)
  mgN          drop team-seasons with <= N ESPN games (mg10 = POST-QC hero cut)
  minN         drop player-seasons with < N total minutes (min20 = usual hero cut)
  CPR          player-rows cut by an mgN filter

  Default for every BDP request: start from QC panel, then apply named filters
  left-to-right, then season tag (e.g. min5 mg10 11_21).

  Code note (binding): min_team_season_games=0 by default for BDP — NOT 10.
  drop_dash_placeholder_names=True only. mg10 only when "mg10" is in the spec.

Do NOT clobber:
  pass_a/PASS_A_empirical_talent_vs_roster_side_by_side.png  (PPM canonical)
  pass_a/sensitivity/*                                     (Track C robustness)
