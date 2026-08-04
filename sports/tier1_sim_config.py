"""Generative defaults for Tier 1 / **540** soft-assignment + score/select.

==============================================================================
FOR LATER CHARLES — this is the KNOB FILE (like 530 CELL 2)
==============================================================================
Imported by: tier1_pool_assignment.AssignmentParams, Pass A/B bundles,
             tier1_generative_eda.SelectionConfig.
Daily runners: sports/scripts/hero_model_reset_bundle.py
               sports/scripts/540_rho_ablation_bundle.py
Plain English: 3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md
Engine decode: sports/tier1_pool_assignment.py (READ-FIRST GLOSSARY there too).

Do not open tier1_cell10_playground_run.py for re-entry checklist work.

------------------------------------------------------------------------------
READ-FIRST GLOSSARY — every symbol below is defined HERE before knobs use it.
Do not skip this block. Later constants assume you already know these words.
------------------------------------------------------------------------------

WHAT THIS FILE IS
  A list of default numbers/strings for one synthetic league draw + selection.
  Changing a constant here changes the *default* Pass A/B / notebook run
  unless a script overrides that field with replace() / state JSON.

THREE STEPS (same as tier1_pool_assignment)
  (1) ASSIGN  — seat fake players on teams.
  (2) SCORE   — ranking number S_i for each player.
  (3) SELECT  — pick winners (usually top K by S_i).

CORE LETTERS
  A_i   — ability of player i (drawn talent).
  T_j   — team target for team j (soft assignment aims here).
  pool  — team / roster group (pool_id on each player).
  S_i   — selection score (ranking weight only).
  K     — how many get selected (= N_SELECTED below).
  Y_selected — 0/1 after SELECT.

POOL L (enters SCORE)
  LOO   — leave-one-out (exclude self when measuring teammates).
  L_Q   — mean teammate ability (column poolq_loo). Same units as A.
  L_C   — crowding among viable peers, on [0,1] (hard share or smooth).
  θ     — viability cutline (VIABILITY_THETA): A > θ ⇒ “viable peer.”
  γ     — sharpness of soft viability (VIABILITY_SHARPNESS).

SCORE (Pass A toggles these)
  w / LOO_GAP_WEIGHT — weight on L in S = A − w·L. Same role as Alex λ.
  λ (lambda)         — Alex’s name for that weight; in code, w ≈ λ.
  SELECTION_SCORE_MODE — "ability" (S=A) or "loo_gap_plus_ability" (S=A−w·L).
  LOO_POOL_L_MODE      — which L: "quality" / "crowding" / "crowding_smooth".
  CROWDING_L_Z_SCALE   — same idea as l_term_scale in the engine:
                           l = pool L; term = L-piece of S=A−w·L; scale = units.
                           None = auto (p90(A)−p10(A)) when A is z-scored.

ASSIGN (Pass B toggles these)
  ρ / ASSIGNMENT_RHO   — soft assortativity. 0 ≈ mix; larger ≈ sit near T_j.
                         NOT the same as λ/w (those are SCORE weights).
  σ / ASSIGNMENT_SIGMA — length-scale in the soft kernel (~0.65).
  τ / ASSIGNMENT_TEMPERATURE — legacy twin of σ; prefer ρ in 540 work.
  soft vs sort-and-chop — soft = overlapping windows; sort_chop = hard slices.

SELECT
  WINNER_SELECTION "C" — top K by score (Pass A/B default).
  "A"/"B"              — older stochastic rules.

TRACKS / PRESETS BELOW (legacy CELL 10 buttons — optional)
  Track A POOL_530_*     — match 530 empirical pool forensics (overlap / SD).
  Track B MATCH_539_*    — mimic 539 hard-assignment feel (τ from calibration).
  Layer 2 SELECTION_539_* — 539 teaching score (beta A, crowding_smooth, w=λ).
  For daily 540 re-entry, focus on the MAIN knobs (N_TEAMS … WINNER_SELECTION
  and CROWDING_L_Z_SCALE). Preset blocks are for older playground buttons.

SECTION MAP
  1. League size (N_TEAMS, ROSTER_SIZE)
  2. Team targets T_j
  3. Soft assignment (ρ, σ, τ, preferential)
  4. Ability draw A_i
  5. Calibration targets (530 forensics numbers — for plots, not science knobs)
  6. Selection / inverted-U replay (L mode, w, K, winner rule)
  7. CELL 10 presets (530 / 539 tracks) — optional
  8. Notebook run gates / plot flags
==============================================================================
"""

# =============================================================================
# 1. LEAGUE SIZE
# =============================================================================
# Empirical panel analysis in 538 still uses PipelineConfig (CELL 1) from
# sports_pipeline.config — do not duplicate those knobs here.

# N_TEAMS (J): how many synthetic teams (pools) in the fake league.
# PD11: J must be >> number of ventile / Plot B bins so bins are not empty.
N_TEAMS = 1000
# 538/530 ventiles often 8–20; keep N_TEAMS several times larger than K bins.

# N_TEAMS_SLIDER_MAX: CELL 10 widget cap only (not a hard algorithmic limit).
N_TEAMS_SLIDER_MAX = 3000

# ROSTER_SIZE: how many players sit on every team (fixed equal rosters).
ROSTER_SIZE = 15

# N_INDIVIDUALS: total fake players = teams × roster size (derived, do not edit alone).
N_INDIVIDUALS = N_TEAMS * ROSTER_SIZE


# =============================================================================
# 2. TEAM TARGETS T_j
# =============================================================================
# T_j = one number per team; soft assignment tries to seat players with A ≈ T.

# TARGET_MEAN_DIST: which family draws T_j.
#   "uniform" | "normal_clipped" | "empirical_530"
#   empirical_530 = draw from scipy fit saved by 530 CELL 5b (same law as empirical A_i)
TARGET_MEAN_DIST = "uniform"

# TARGET_MEAN_LOW / HIGH: uniform range, or clip bounds for normal_clipped.
TARGET_MEAN_LOW = -0.5
TARGET_MEAN_HIGH = 0.5

# TARGET_MEAN_MU / SIGMA: used only when TARGET_MEAN_DIST == "normal_clipped".
TARGET_MEAN_MU = 0.0
TARGET_MEAN_SIGMA = 0.35


# =============================================================================
# 3. SOFT ASSIGNMENT (Pass B knobs: ρ, σ)
# =============================================================================
# Soft π_ij: probabilistic seating near T_j (overlapping talent windows).

# ASSIGNMENT_KERNEL: shape of soft-match weights. "gaussian" | "cauchy"
ASSIGNMENT_KERNEL = "gaussian"

# ASSIGNMENT_RHO (ρ): assignment assortativity — Pass B’s main knob.
#   0 = max mixing (flat among open seats); ρ↑ = sharper match to T_j.
#   NOT λ / LOO_GAP_WEIGHT (those live in SCORE).
ASSIGNMENT_RHO = 1.0

# ASSIGNMENT_SIGMA (σ): fixed ability–target length-scale in the soft kernel.
#   (ρ=1, σ=0.65 ≡ legacy τ=0.65 on the old parameterization.)
ASSIGNMENT_SIGMA = 0.65

# ASSIGNMENT_TEMPERATURE (τ): legacy alias; keep equal to ASSIGNMENT_SIGMA.
#   Old notebooks / τ prose. Prefer ρ + σ in 540 work.
ASSIGNMENT_TEMPERATURE = 0.65

# USE_PREFERENTIAL_ATTACHMENT: if True, multiply soft weights by (n_j + k)^α
#   (rich-get-richer on seats already filling). Off for 540 defaults.
USE_PREFERENTIAL_ATTACHMENT = False
# PREFERENTIAL_ALPHA (α): exponent when preferential attachment is on.
PREFERENTIAL_ALPHA = 0.35
# PREFERENTIAL_K (k): offset in (n_j + k)^α so empty teams are not weight 0.
PREFERENTIAL_K = 1.0


# =============================================================================
# 4. ABILITY DRAW A_i
# =============================================================================
# A_i = latent talent for each synthetic player.

# ABILITY_DRAW: which distribution invents A_i.
#   "uniform_01" | "beta_2_2" (539 Alex) | "normal_clipped" | "normal_plus_student_t"
#   "empirical_530" = draw from scipy fit saved by 530 CELL 5b (within-season z perf)
#   Scale note: normal_clipped is z-ish → crowding L needs CROWDING_L_Z_SCALE / auto.
ABILITY_DRAW = "normal_clipped"

# ABILITY_MEAN / SD: location and scale for normal_* draws.
ABILITY_MEAN = 0.0
ABILITY_SD = 1.0

# ABILITY_CLIP_LOW / HIGH: hard floor/ceiling after normal_* draws.
ABILITY_CLIP_LOW = -2.5
ABILITY_CLIP_HIGH = 3.5

# ABILITY_STUDENT_T_*: heavy-tail add-on when ABILITY_DRAW includes student-t noise.
#   DF = degrees of freedom; SCALE = 0 means that noise is off.
ABILITY_STUDENT_T_DF = 4
ABILITY_STUDENT_T_SCALE = 0.25


# =============================================================================
# 5. CALIBRATION TARGETS (from 530 forensics — for validation plots)
# =============================================================================
# These are “what good soft assignment should look like,” not Pass A/B science knobs.
# Within-season z, PPM-based panel, ~2011–2021, APPLY_ANALYSIS_FILTERS True.

CALIBRATION_NOTE = (
    "Match 530 CELL 8: coverage >> 1 at center; CELL 5: median roster SD ~0.8; "
    "CELL 6: weak positive mean–SD correlation, not forced negative."
)
# EMPIRIC_MEDIAN_ROSTER_SD_Z: typical within-team ability SD on z scale (~0.8).
EMPIRIC_MEDIAN_ROSTER_SD_Z = 0.80
# EMPIRIC_COVERAGE_PEAK_ORDER: order-of-magnitude overlap peak (re-read 530 after refresh).
EMPIRIC_COVERAGE_PEAK_ORDER = 3000


# =============================================================================
# 6. SELECTION / INVERTED-U REPLAY (Pass A knobs: score mode, L, w, K)
# =============================================================================
# Selection = draft pick, tenure, promotion, etc. Bins are on LOO pool L (not teams).

# LOO_POOL_L_MODE: which L enters the SCORE.
#   "quality"         → L_Q (poolq_loo)
#   "crowding"        → L_C hard share (pool_c_loo)
#   "crowding_smooth" → LOO mean σ(γ(A−θ)) (pool_c_smooth_loo; 539 / Pass A congestion)
LOO_POOL_L_MODE = "quality"

# VIABILITY_THETA (θ): cutline for “viable peer” when building L_C.
#   Default ≈ 530 CELL 5d median drafted within-season z perf (PPM, ever-drafted).
VIABILITY_THETA = 0.7546158731868137

# VIABILITY_SHARPNESS (γ): logistic sharpness in soft viability σ(γ(A−θ)).
#   Higher γ → closer to a hard threshold at θ (539 simulate_viable_peer_congestion).
VIABILITY_SHARPNESS = 18.0

# GENERATIVE_N_BINS: how many bins on the Plot B / inverted-U X-axis.
GENERATIVE_N_BINS = 20

# GENERATIVE_POOLQ_BINNING: how to cut those bins. "quantile" | "equal_width"
GENERATIVE_POOLQ_BINNING = "quantile"

# N_SELECTED (K): how many players get Y_selected=1 (top-K under winner "C").
# Gallery scripts default K/N = 10% via gallery_knobs (characterization baseline).
N_SELECTED = 1500

# SELECTION_SCORE_MODE: how S_i is built.
#   "ability"              → S = A                          (talent-only / λ=0)
#   "loo_gap_plus_ability" → S = A − w·L  (quality: gap vs L_Q; crowding: vs L_C)
SELECTION_SCORE_MODE = "loo_gap_plus_ability"

# LOO_GAP_WEIGHT (w): weight on the L-term in S = A − w·L. Same role as Alex λ.
#   Crowding mode reuses this knob as the “crowding weight.”
LOO_GAP_WEIGHT = 0.5

# WINNER_SELECTION: how scores become winners.
#   "A" = weighted sample without replacement
#   "B" = Bernoulli
#   "C" = top-K deterministic  ← Pass A/B default
WINNER_SELECTION = "C"

# CROWDING_L_Z_SCALE: unit-matching multiplier for crowding L (same as l_term_scale).
#   Name decode: crowding = L_C mode; L = pool L; Z_SCALE = scale when A is z-scored.
#   When using z-scored ability + crowding L, assign_selection multiplies L_C by this
#   (or auto p90(A)−p10(A) when None). Pin a positive float (e.g. 4.0) to freeze it.
CROWDING_L_Z_SCALE = None


# =============================================================================
# 7. CELL 10 PRESETS (two calibration tracks — do not mix casually)
# =============================================================================
#
# Track A — POOL_530_* ("530 pool cal" button): match real MBB forensics (530 CELLs 5–8).
#   τ ≈ 0.65 → median roster SD ~0.8, coverage peak ≫ 1. NOT the 539 Alex assignment story.
#
# Track B — MATCH_539_* ("539 assign cal" button): mimic 539 sort-chop assignment (CELL 10b/10c)
#   before congestion in the selection score. τ from auto_calibrate_tau; re-run 10c after
#   changing ability_draw, J, or seed. Soft assign cannot fully match hard sort-chop — 10b
#   will still show a gap on roster SD / coverage.
#
# Layer 0 (both tracks): ability-only top-K (w=0). Layer 2+: turn on crowding_smooth + w.
#
# Layer 2 — 539 teaching selection (CELL 10 "539 selection" button):
#   beta_2_2 A on [0,1], T_j uniform [0,1], crowding_smooth, w = λ from reference JSON.
#   Keeps 530 pool assignment (τ≈0.65) unless you switch to 539 assign cal separately.

# --- Track A — 530 empirical pool calibration ---------------------------------
POOL_530_ASSIGNMENT_TEMPERATURE = 0.65
POOL_530_ABILITY_DRAW = "normal_clipped"
POOL_530_TARGET_MEAN_DIST = "uniform"
POOL_530_PREFERENTIAL_ALPHA = 0.0
POOL_530_SELECTION_SCORE_MODE = "ability"
POOL_530_LOO_GAP_WEIGHT = 0.0
POOL_530_LOO_POOL_L_MODE = "quality"
POOL_530_WINNER_SELECTION = "C"

# Deprecated aliases (530 track) — old names; same values as POOL_530_* above.
MINIMAL_ABILITY_DRAW = POOL_530_ABILITY_DRAW
MINIMAL_TARGET_MEAN_DIST = POOL_530_TARGET_MEAN_DIST
MINIMAL_PREFERENTIAL_ALPHA = POOL_530_PREFERENTIAL_ALPHA
MINIMAL_SELECTION_SCORE_MODE = POOL_530_SELECTION_SCORE_MODE
MINIMAL_LOO_GAP_WEIGHT = POOL_530_LOO_GAP_WEIGHT
MINIMAL_LOO_POOL_L_MODE = POOL_530_LOO_POOL_L_MODE
MINIMAL_WINNER_SELECTION = POOL_530_WINNER_SELECTION

# --- Track B — 539 assignment mimicry (Layer 0) --------------------------------
# τ from CELL 10c at J=1000, seed=42, rho=0.88
MATCH_539_ASSIGNMENT_TEMPERATURE = 0.108
MATCH_539_N_TEAMS = 1000
MATCH_539_ROSTER_SIZE = 15
MATCH_539_RANDOM_SEED = 42
MATCH_539_ABILITY_DRAW = "normal_clipped"
MATCH_539_TARGET_MEAN_DIST = "uniform"
MATCH_539_TARGET_MEAN_LOW = -0.5
MATCH_539_TARGET_MEAN_HIGH = 0.5
MATCH_539_PREFERENTIAL_ALPHA = 0.0
MATCH_539_N_SELECTED = 1500
MATCH_539_SELECTION_SCORE_MODE = "ability"
MATCH_539_LOO_GAP_WEIGHT = 0.0
MATCH_539_LOO_POOL_L_MODE = "quality"
MATCH_539_WINNER_SELECTION = "C"
MATCH_539_VIABILITY_THETA = 0.72
MATCH_539_VIABILITY_SHARPNESS = 10.0
# Full-scale 539 notebook reference (tier1_539_reference_settings.json): N=30_000, J=2000, seed=1,
# ability=beta_2_2 on [0,1], T_j uniform [0,1], n_selected=3000 (10%). Re-run 10c after switching.
# Sweep hint (J=1000): beta_2_2 → τ≈0.116 (seed 42) or τ≈0.149 (seed 1); 538 SD ~0.21 vs 539 ~0.11.
MATCH_539_FULL_N_TEAMS = 2000
MATCH_539_FULL_ROSTER_SIZE = 15
MATCH_539_FULL_RANDOM_SEED = 1
MATCH_539_FULL_ABILITY_DRAW = "beta_2_2"
MATCH_539_FULL_TARGET_MEAN_LOW = 0.0
MATCH_539_FULL_TARGET_MEAN_HIGH = 1.0
MATCH_539_FULL_N_SELECTED = 3000

# --- Layer 2 — 539 selection score on 530-calibrated pools ----------------------
# Commensurate [0,1] A and L_C (beta draw + crowding_smooth + λ from reference JSON).
SELECTION_539_ABILITY_DRAW = "beta_2_2"
SELECTION_539_TARGET_MEAN_LOW = 0.0
SELECTION_539_TARGET_MEAN_HIGH = 1.0
SELECTION_539_LOO_POOL_L_MODE = "crowding_smooth"
SELECTION_539_LOO_GAP_WEIGHT = 0.55  # λ in tier1_539_reference_settings.json
SELECTION_539_SELECTION_SCORE_MODE = "loo_gap_plus_ability"
SELECTION_539_VIABILITY_THETA = 0.72
SELECTION_539_VIABILITY_SHARPNESS = 10.0
SELECTION_539_WINNER_SELECTION = "C"

# Deprecated aliases (rename only — same values as main N_SELECTED / score mode).
N_PROMOTED = N_SELECTED
PROMOTION_SCORE_MODE = SELECTION_SCORE_MODE


# =============================================================================
# 8. NOTEBOOK RUN GATES / PLOT FLAGS (legacy CELL 10 playground)
# =============================================================================
# These do not change Pass A/B bundle science; they gate optional notebook cells.

# RUN_GENERATIVE_ASSIGNMENT_DEMO: if True, 538-era notebook runs assignment demo cells.
RUN_GENERATIVE_ASSIGNMENT_DEMO = False
# RUN_REPLAY_530_STYLE_CHECKS: if True, run 530-style overlap / SD replay checks.
RUN_REPLAY_530_STYLE_CHECKS = False

# RANDOM_SEED: default RNG seed when a caller does not pass its own Generator.
RANDOM_SEED = 42

# SHOW_PLOT_A: CELL 10 playground — interval-overlap Plot A (530 CELL 8 analog).
SHOW_PLOT_A = True
# SHOW_PLOT_B: CELL 10 playground — inverted-U Plot B (selection rate vs LOO L bins).
SHOW_PLOT_B = True
# SHOW_PLOT_B_TEAM_MEAN: False → Plot B x = L_Q (530 comparability);
#   True → x = pool team_mean (539 notebook style).
SHOW_PLOT_B_TEAM_MEAN = False
# SHOW_PLOT_C: CELL 10 playground — ability histogram Plot C (530 CELL 5b overlay).
SHOW_PLOT_C = True
