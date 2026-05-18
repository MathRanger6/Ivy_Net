"""Generative pool-assignment defaults for Tier 1 (**538**, not **537**).

**537** (`sim_config.py` + Cell 10 widgets) stays the legacy simulation lab (sort-and-chop,
promotion-score experiments). This file holds parameters for the **new** soft-assignment
story calibrated against **`530_sports_pipeline.ipynb` CELLs 5–9**.

Design: `sports/documents/Tier1_Presorting_Design_Note.md`

When 538 grows generative cells, import this module the same way 537 imports `sim_config.py`:

    from pathlib import Path
    import importlib.util
    spec = importlib.util.spec_from_file_location("tier1_sim_config", Path("sports/tier1_sim_config.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
"""

# --- Scope ---------------------------------------------------------------------
# Empirical panel analysis in 538 still uses PipelineConfig (CELL 1) from
# sports_pipeline.config — do not duplicate those knobs here.

# --- Pool count (PD11: J must be >> number of ventile bins) --------------------
N_TEAMS = 50
# 538/530 ventiles often 8–20; keep N_TEAMS several times larger.

ROSTER_SIZE = 15
# Fixed roster size per team-season in synthetic data (tune vs empirical minutes/roster).

N_INDIVIDUALS = N_TEAMS * ROSTER_SIZE

# --- Target team means T_j ------------------------------------------------------
# "uniform" | "normal_clipped"
TARGET_MEAN_DIST = "uniform"
TARGET_MEAN_LOW = -0.5
TARGET_MEAN_HIGH = 0.5
# For normal_clipped:
TARGET_MEAN_MU = 0.0
TARGET_MEAN_SIGMA = 0.35

# --- Soft assignment pi_ij ∝ f(A_i - T_j) --------------------------------------
# "gaussian" | "cauchy"
ASSIGNMENT_KERNEL = "gaussian"
# Temperature tau: larger => more cross-team mixing / overlap
ASSIGNMENT_TEMPERATURE = 0.45

# Optional preferential attachment (0 = off): pi_ij *= (n_j + k)^alpha
PREFERENTIAL_ALPHA = 0.0
PREFERENTIAL_K = 1.0

# --- Ability draw A_i ----------------------------------------------------------
# "uniform_01" | "normal_clipped" | "normal_plus_student_t"
ABILITY_DRAW = "normal_clipped"
ABILITY_MEAN = 0.0
ABILITY_SD = 1.0
ABILITY_CLIP_LOW = -2.5
ABILITY_CLIP_HIGH = 3.5

# Heavy tail on ability (0 = off); used when ABILITY_DRAW includes student-t noise
ABILITY_STUDENT_T_DF = 4
ABILITY_STUDENT_T_SCALE = 0.25

# --- Calibration targets (from 530 forensics; for validation plots) ------------
# Within-season z, PPM-based panel, ~2011–2021, APPLY_ANALYSIS_FILTERS True
CALIBRATION_NOTE = (
    "Match 530 CELL 8: coverage >> 1 at center; CELL 5: median roster SD ~0.8; "
    "CELL 6: weak positive mean–SD correlation, not forced negative."
)
EMPIRIC_MEDIAN_ROSTER_SD_Z = 0.80
EMPIRIC_COVERAGE_PEAK_ORDER = 3000
# Order-of-magnitude; re-read 530 printout after panel refresh

# --- 538 notebook run gates (when generative cells exist) ----------------------
RUN_GENERATIVE_ASSIGNMENT_DEMO = False
RUN_REPLAY_530_STYLE_CHECKS = False
RANDOM_SEED = 42
