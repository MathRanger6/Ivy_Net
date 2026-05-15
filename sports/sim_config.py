"""Configuration choices for ``537_Sports_Simulation.ipynb``.

See **`sports/documents/537_Manual.md`** for a full operator guide (variables, binning modes, widget map).

Edit **`sports/sim_config.py`**, then reload (**Cell 0**) so ``reload_sim_config()`` picks up changes. **Cell 10** widgets are *authoritative* for plots; use **“Load defaults from sim_config.py”** there to copy these values into sliders. Shared knob labels for sweep PNG titles live in ``cell10_knob_catalog.py``.
"""

# --- Run gates -----------------------------------------------------------------
# Old batch-driven cells **2–9** were removed from the live notebook on 2026-05-08.
# Full snapshot lives at:
# ``obsolete_files/sports_gameplan_old/537_Sports_Simulation_pre_archive_8MAy.ipynb``
RUN_CELL1 = True  # Imports and simulation helpers (required for Cell 10)
RUN_CELL_PLAYGROUND = True  # Cell 10 — interactive EDA widgets
RUN_CELL11 = True  # Cell 11 — optional PPM histogram / draft overlay from panel_530 CSV

# --- Simulation size -----------------------------------------------------------
RANDOM_SEED = 27876507
N_INDIVIDUALS = 1_000
N_WINNERS = 50
N_POOLS = 50
N_RUNS = 500
N_BINS = 20
# Pool-mean-A aggregation bins (Cell 10): independent of N_POOLS. Example: 100 pools,
# 20 bins → ~5 pools per bin after sorting pools by mean A_i within each run.
N_POOL_AGG_BINS = 8

# --- Figure output -------------------------------------------------------------
# Set True when you want notebook figures written to disk with fig.savefig(...).
# Set False for fast exploratory reruns with inline display only.
SAVE_FIGURES = False

# --- Convergence plots ---------------------------------------------------------
# True overlays curves from small-to-large run counts, showing noisy early
# estimates settling toward the high-run equilibrium. False keeps only the main
# diagnostic plots.
SHOW_CONVERGENCE_PLOTS = False
RUN_CHECKPOINTS = [5, 10, 25, 50, 100, 250, 500, 1_000]

# --- A/B/C choices -------------------------------------------------------------
# Ability distribution:
#   A. uniform_0_1      — Alex's first-pass suggestion.
#   B. normal_clipped   — bell-shaped ability with clipping to [0, 1].
#   C. empirical_like   — distribution shaped from an observed metric.
ABILITY_DISTRIBUTION_CHOICE = "B"

# Promotion weight rule:
#   A. normalized ability weights      — Simulation 1.
#   B. normalized global-rank weights  — Simulation 2.
#   C. softmax/Gibbs weights           — later; e^{score} / sum(e^{score}).
PROMOTION_WEIGHT_RULE_CHOICE_SIM1 = "A"
PROMOTION_WEIGHT_RULE_CHOICE_SIM2 = "B"
PROMOTION_WEIGHT_RULE_CHOICE_SIM3 = "B"  # local pools + local rank weights

# Winner selection rule:
#   A. weighted sampling without replacement of K winners per run.
#   B. independent Bernoulli threshold.
#   C. top-K deterministic.
WINNER_SELECTION_CHOICE = "A"

# Local pool sorting / assignment for Simulation 3:
#   A. random equal-sized pools.
#   B. pure/noisy assortative pools; sort similar A_i together.
#   C. pure/noisy disassortative pools; mix high and low A_i together.
LOCAL_POOL_ASSIGNMENT_CHOICES_SIM3 = ("A", "B")

# Sorting noise is only used to assign people to pools. It does not change true A_i.
# sorting_signal_i = A_i + epsilon_i, epsilon_i ~ Normal(0, SORTING_NOISE_SD)
SORTING_NOISE_SD = 0.01

# Additive blend: score = w * local_rank_score + (1 - w) * A_i.
ADDITIVE_LOCAL_RANK_WEIGHT = 0.0

# Individuals with true A_i below this value cannot be promoted: their weights
# are zeroed before the winner draw (fewer than K promotions if not enough pass).
MIN_ABILITY_FOR_PROMOTION = 0.0

# --- Interactive playground (Cell 10) -----------------------------------------
# Single-panel figure size (width, height) in inches — nearly square so the plot
# is not “squashed” like the old 3-across strip (14×4.7 in). Adjust here only.
FIG_PLAYGROUND_EDA_INCHES = (8.0, 7.2)

# Smaller N and fewer runs keep slider updates responsive. Full-batch cells still
# use N_INDIVIDUALS and N_RUNS above.
INTERACTIVE_N_INDIVIDUALS = 500
INTERACTIVE_N_RUNS = 120
# Person-level qcut bin count for the playground (often matches N_BINS).
INTERACTIVE_N_BINS = 20
# Pool-talent bins default for playground sliders; batch lock uses N_POOL_AGG_BINS.
INTERACTIVE_N_POOL_AGG_BINS = 8
INTERACTIVE_SORTING_NOISE_MAX = 0.5  # upper end of the sorting-noise slider
# When True, older Cell 10 builds exposed a “batch lock” tied to this flag.
# Current Cell 10 ignores this; use “Load defaults from sim_config.py” in the notebook instead.
INTERACTIVE_USE_MAIN_SCALES = False

