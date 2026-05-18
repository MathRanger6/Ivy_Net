"""Configuration for **537_Sports_Simulation.ipynb** only.

**Do not add Tier 1 generative pool-assignment knobs here.** Those live in
``sports/tier1_sim_config.py`` and will be used from **538** when soft-assignment
cells are implemented. See ``sports/documents/Tier1_Presorting_Design_Note.md``.

Operator guide: ``sports/documents/537_Manual.md``

**Workflow**
- Edit this file for **537** defaults.
- Run **Cell 0** → ``reload_sim_config()`` refreshes the kernel.
- **Cell 10 widgets are authoritative** for plots; click **Load defaults from sim_config.py**
  to copy these values into sliders.
- Widget labels / sweep PNG wording: ``cell10_knob_catalog.py``.
"""

# --- Run gates -----------------------------------------------------------------
RUN_CELL1 = True
RUN_CELL_PLAYGROUND = True
RUN_CELL11 = True

# --- Batch simulation size -----------------------------------------------------
RANDOM_SEED = 27876507
N_INDIVIDUALS = 1_000
N_WINNERS = 50
N_POOLS = 50
N_RUNS = 500
N_BINS = 20
N_POOL_AGG_BINS = 8

# --- Figure output -------------------------------------------------------------
SAVE_FIGURES = False
SHOW_CONVERGENCE_PLOTS = False
RUN_CHECKPOINTS = [5, 10, 25, 50, 100, 250, 500, 1_000]

# --- Legacy assignment & promotion (sort-and-chop family) ----------------------
ABILITY_DISTRIBUTION_CHOICE = "B"

PROMOTION_WEIGHT_RULE_CHOICE_SIM1 = "A"
PROMOTION_WEIGHT_RULE_CHOICE_SIM2 = "B"
PROMOTION_WEIGHT_RULE_CHOICE_SIM3 = "B"

WINNER_SELECTION_CHOICE = "A"

LOCAL_POOL_ASSIGNMENT_CHOICES_SIM3 = ("A", "B")

# Sorting noise for assign_pool_ids only (does not change true A_i)
SORTING_NOISE_SD = 0.01

# Promotion score blend when score mode uses local rank (Cell 10 dropdown)
ADDITIVE_LOCAL_RANK_WEIGHT = 0.0

MIN_ABILITY_FOR_PROMOTION = 0.0

# --- Cell 10 playground (starting defaults; widgets override until reload) -----
FIG_PLAYGROUND_EDA_INCHES = (8.0, 7.2)

INTERACTIVE_N_INDIVIDUALS = 500
INTERACTIVE_N_RUNS = 120
INTERACTIVE_N_BINS = 20
INTERACTIVE_N_POOL_AGG_BINS = 8
INTERACTIVE_SORTING_NOISE_MAX = 0.5
