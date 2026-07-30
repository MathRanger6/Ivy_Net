"""Shared generative EDA: inverted-U bins + the Assign→Score→Select pipeline runner.

==============================================================================
FOR LATER CHARLES — read this like a notebook CELL map
==============================================================================
Daily path: 540_READ_ME_SIM.md + hero_model_reset_bundle / 540_rho_ablation_bundle.
Plain English: 3-Master_Plan/re_entry/04_Pass_A_and_Pass_B_in_Plain_English.md

This file sits *above* the engine (tier1_pool_assignment.py):
  • knobs come from tier1_sim_config.py (or CELL 10 state JSON)
  • ASSIGN / SCORE / SELECT math lives in tier1_pool_assignment
  • HERE we bundle selection knobs, build the binned inverted-U table,
    draw Plot B, and run one full preview pipeline

------------------------------------------------------------------------------
READ-FIRST GLOSSARY — defined HERE before any code uses these words.
(Same letters as tier1_pool_assignment / tier1_sim_config — repeated so you
do not have to jump files mid-read.)
------------------------------------------------------------------------------

WHAT THIS FILE DOES
  Takes a synthetic roster (or builds one), scores/selects players, then
  summarizes selection *rate* by bins of pool quality — the sim “inverted-U”
  table and figure Pass A/B bundles look at.

THREE STEPS (engine does 1–3; this file orchestrates + bins/plots)
  (1) ASSIGN  — seat players (simulate_generative_rosters).
  (2) SCORE   — S_i from ability ± pool L (assign_selection → selection_weights).
  (3) SELECT  — winners Y_selected (usually top K, choice "C").
  Then: BIN + PLOT — mean Y_selected vs bin of L_Q (or team mean).

CORE LETTERS
  A_i, T_j, pool, S_i, K, Y_selected — same as the engine glossary.
  L / LOO / L_Q / L_C / θ / γ / w / λ / ρ — same as the engine glossary.
  l_term_scale / CROWDING_L_Z_SCALE — unit matcher for crowding L; decode in
      tier1_pool_assignment READ-FIRST GLOSSARY (l = L; term = L-piece of score).

IMPORTANT AXIS RULE (easy to miss)
  Plot B / inverted_u_bin_table X-axis is ALWAYS L_Q (poolq_loo) by default —
  mean teammate ability — so curves stay comparable when you change which L
  enters the *score*. Changing loo_pool_l_mode changes SCORE, not the bin axis
  (unless you deliberately use the team_mean Plot B′ helper).

SELECTIONCONFIG vs ASSIGNMENTPARAMS
  AssignmentParams — league geometry + assign knobs (from tier1_sim_config).
  SelectionConfig  — bins, K, score mode, w, winner rule, which L in score.
  Pass A mostly varies SelectionConfig (and L mode / w).
  Pass B mostly varies AssignmentParams.assignment_rho / method.

SECTION MAP
  0. Outcome column helper (Y_selected vs legacy Y_promoted)
  1. SelectionConfig — SCORE/SELECT + binning knobs
  2. Plot B axis label strings
  3. Formula / title helpers (what the figure claims)
  4. Load knobs from CELL 10 state JSON (legacy playground)
  5. inverted_u_bin_table — binned selection rates (main Plot B data)
  6. inverted_u_bin_table_team_mean — optional 539-style X-axis
  7. figure_inverted_u — draw Plot B
  8. run_inverted_u_pipeline — one-shot Assign→Select→bin→figure
==============================================================================
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from tier1_pool_assignment import AssignmentParams


# =============================================================================
# 0. OUTCOME COLUMN HELPER
# =============================================================================
# Early drafts called the 0/1 column Y_promoted; current name is Y_selected.
# Same meaning: 1 = got the slot after SELECT.


def _outcome_col(players: pd.DataFrame) -> str:
    """Return the 0/1 outcome column name on a scored roster table.

    Prefers Y_selected; falls back to legacy Y_promoted.
    """
    if "Y_selected" in players.columns:
        return "Y_selected"
    if "Y_promoted" in players.columns:
        return "Y_promoted"
    raise KeyError("players need Y_selected or Y_promoted")


# =============================================================================
# 1. SelectionConfig — SCORE / SELECT / BINNING KNOBS
# =============================================================================
# AssignmentParams (engine) = how the fake league is built and who sits where.
# SelectionConfig (this class) = how we score, how many we pick, how we bin Plot B.


@dataclass(frozen=True)
class SelectionConfig:
    """Knobs for SCORE + SELECT + inverted-U binning (mirror tier1_sim_config).

    Field-by-field (530 CELL 2 style)
      n_bins           — how many bins on the Plot B X-axis.
      bin_mode         — "quantile" or "equal_width" cuts on that axis.
      n_selected (K)   — how many players get Y_selected=1.
      score_mode       — "ability" or "loo_gap_plus_ability" (Pass A toggle).
      loo_gap_weight   — w in S = A − w·L (same role as Alex λ).
      winner_selection — "A"/"B"/"C"; Pass A/B default "C" = top K by score.
      loo_pool_l_mode  — which L enters the SCORE (quality / crowding / …).
                         Does NOT change the default Plot B bin axis (still L_Q).
    """

    n_bins: int
    # n_bins: number of X-axis bins for the inverted-U / Plot B summary.
    bin_mode: str
    # bin_mode: "quantile" (~equal n per bin) or "equal_width" (equal L spacing).
    n_selected: int
    # n_selected (K): how many winners under the winner rule.
    score_mode: str
    # score_mode: "ability" (S=A) or "loo_gap_plus_ability" (S=A−w·L).
    loo_gap_weight: float
    # loo_gap_weight (w): weight on the L-term; ≈ Alex λ in the nesting.
    winner_selection: str
    # winner_selection: "C" = top K (default); "A"/"B" = stochastic (legacy).
    loo_pool_l_mode: str = "quality"
    # loo_pool_l_mode: which pool L enters SCORE — not the default Plot B X-axis.

    @classmethod
    def from_module(cls, mod) -> SelectionConfig:
        """Build from an imported tier1_sim_config (or compatible) module.

        Reads N_SELECTED / SELECTION_SCORE_MODE with legacy N_PROMOTED /
        PROMOTION_SCORE_MODE fallbacks so old configs still load.
        """
        n_sel = getattr(mod, "N_SELECTED", None)
        if n_sel is None:
            n_sel = getattr(mod, "N_PROMOTED", 40)
        score = getattr(mod, "SELECTION_SCORE_MODE", None)
        if score is None:
            score = getattr(mod, "PROMOTION_SCORE_MODE", "loo_gap_plus_ability")
        return cls(
            n_bins=int(getattr(mod, "GENERATIVE_N_BINS", 12)),
            bin_mode=str(getattr(mod, "GENERATIVE_POOLQ_BINNING", "quantile")),
            n_selected=int(n_sel),
            score_mode=str(score),
            loo_gap_weight=float(getattr(mod, "LOO_GAP_WEIGHT", 0.5)),
            winner_selection=str(getattr(mod, "WINNER_SELECTION", "C")),
            loo_pool_l_mode=str(getattr(mod, "LOO_POOL_L_MODE", "quality")),
        )

    @classmethod
    def from_state(cls, state: dict, base: SelectionConfig) -> SelectionConfig:
        """Overlay CELL 10 playground JSON knobs onto a base SelectionConfig.

        state keys use short names (n_selected, score_mode, …) from the widget UI.
        Missing keys keep the base value.
        """
        n_sel = state.get("n_selected", state.get("n_promoted", base.n_selected))
        return cls(
            n_bins=int(state.get("n_bins", base.n_bins)),
            bin_mode=str(state.get("bin_mode", base.bin_mode)),
            n_selected=int(n_sel),
            score_mode=str(state.get("score_mode", base.score_mode)),
            loo_gap_weight=float(state.get("loo_gap_weight", base.loo_gap_weight)),
            winner_selection=str(state.get("winner_selection", base.winner_selection)),
            loo_pool_l_mode=str(
                state.get("loo_pool_l_mode", base.loo_pool_l_mode)
            ),
        )


# Deprecated alias — early drafts said "PromotionConfig"; same class.
PromotionConfig = SelectionConfig


# =============================================================================
# 2. PLOT B AXIS LABEL STRINGS
# =============================================================================
# Default X = L_Q bins (530-comparable). Optional team_mean axis = 539-style.

# PLOT_B_XAXIS_LABEL: default X — bin mean of L_Q (LOO mean teammate ability).
PLOT_B_XAXIS_LABEL = (
    "Bin mean L_Q (LOO mean teammate ability)\n"
    "[x-axis fixed — Pool L dropdown affects selection score only]"
)
# PLOT_B_XAXIS_TEAM_MEAN_LABEL: optional 539-style X — realized team mean ability.
PLOT_B_XAXIS_TEAM_MEAN_LABEL = (
    "Bin mean team ability (pool mean; 539-style)\n"
    "[Pool L dropdown affects selection score only]"
)
# PLOT_B_YAXIS_LABEL: Y — mean of Y_selected inside each bin (selection rate).
PLOT_B_YAXIS_LABEL = "Mean selection rate (Y_selected) per bin"


# =============================================================================
# 3. FORMULA / TITLE HELPERS (what the figure claims in plain text)
# =============================================================================


def selection_rank_formula(
    score_mode: str,
    *,
    loo_gap_weight: float,
    pool_l_mode: str,
    tpa=None,
) -> str:
    """Plain-text formula for who wins top-K (not the Plot B bin axis).

    Args
      score_mode      — "ability" or "loo_gap_plus_ability".
      loo_gap_weight  — w / λ in S = A − w·L.
      pool_l_mode     — which L enters the score (quality / crowding_smooth…).
      tpa             — optional tier1_pool_assignment module (imported if None).

    Returns a one-line string suitable for a figure title subtitle.
    """
    if tpa is None:
        import tier1_pool_assignment as tpa  # noqa: PLC0415

    mode = str(score_mode).strip().lower()
    if mode == "ability":
        return "Selection rank = A_i only (top-K; w unused)"
    w = float(loo_gap_weight)
    l_short = tpa.pool_l_short_label(pool_l_mode)
    if tpa.is_crowding_l_mode(pool_l_mode):
        return (
            f"Selection rank = A_i − w·{l_short} "
            f"(w={w:.2f}; Pool L in score={pool_l_mode!r})"
        )
    return f"Selection rank = w·(A_i−L_Q)+(1−w)·A_i (w={w:.2f})"


def plot_b_figure_title(
    sel: SelectionConfig,
    *,
    header: str = "538 CELL 10 — Plot B",
    team_mean_axis: bool = False,
    tpa=None,
) -> str:
    """Two-line matplotlib title: y vs Plot B bins + selection-rank recipe.

    Args
      sel             — SelectionConfig (K, bins, score mode, L mode, w).
      header          — first-line prefix (Pass A/B bundles customize this).
      team_mean_axis  — True if X is team_mean bins (539-style), else L_Q bins.
      tpa             — optional tier1_pool_assignment module.
    """
    rank = selection_rank_formula(
        sel.score_mode,
        loo_gap_weight=sel.loo_gap_weight,
        pool_l_mode=sel.loo_pool_l_mode,
        tpa=tpa,
    )
    x_label = "team_mean bins (539-style)" if team_mean_axis else "L_Q bins"
    return (
        f"{header}: mean Y_selected vs {x_label}\n"
        f"{rank} | K={sel.n_selected} | {sel.n_bins} bins ({sel.bin_mode})"
    )


# =============================================================================
# 4. LOAD KNOBS FROM CELL 10 STATE JSON (legacy playground)
# =============================================================================
# Daily 540 re-entry prefers scripts + tier1_sim_config defaults.
# These helpers still support the old CELL 10 widget state file.


def assignment_params_from_state(
    sports: Path,
    state: dict | None,
    *,
    tpa,
) -> AssignmentParams:
    """Build AssignmentParams from tier1_sim_config, then overlay playground state.

    Args
      sports — path to the sports/ directory (holds tier1_sim_config.py).
      state  — dict from load_playground_state (or None / {} → config defaults).
      tpa    — tier1_pool_assignment module (caller imports it).

    State key map (widget short name → AssignmentParams field)
      n_teams, roster_size, target_dist, t_low, t_high, kernel, tau, rho, sigma,
      use_preferential_attachment, pref_alpha, ability_draw,
      viability_theta, viability_sharpness
    """
    base = tpa.AssignmentParams.from_tier1_sim_config(sports / "tier1_sim_config.py")
    if not state:
        return base
    return tpa.AssignmentParams(
        n_teams=int(state.get("n_teams", base.n_teams)),
        roster_size=int(state.get("roster_size", base.roster_size)),
        target_mean_dist=state.get("target_dist", base.target_mean_dist),
        target_mean_low=float(state.get("t_low", base.target_mean_low)),
        target_mean_high=float(state.get("t_high", base.target_mean_high)),
        target_mean_mu=base.target_mean_mu,
        target_mean_sigma=base.target_mean_sigma,
        assignment_kernel=state.get("kernel", base.assignment_kernel),
        assignment_temperature=float(state.get("tau", base.assignment_temperature)),
        assignment_rho=float(state.get("rho", base.assignment_rho)),
        assignment_sigma=float(state.get("sigma", base.assignment_sigma)),
        use_preferential_attachment=bool(
            state.get("use_preferential_attachment", base.use_preferential_attachment)
        ),
        preferential_alpha=float(state.get("pref_alpha", base.preferential_alpha)),
        preferential_k=base.preferential_k,
        ability_draw=state.get("ability_draw", base.ability_draw),
        ability_mean=base.ability_mean,
        ability_sd=base.ability_sd,
        ability_clip_low=base.ability_clip_low,
        ability_clip_high=base.ability_clip_high,
        ability_student_t_df=base.ability_student_t_df,
        ability_student_t_scale=base.ability_student_t_scale,
        sorting_noise_sd=base.sorting_noise_sd,
        viability_theta=float(
            state.get("viability_theta", base.viability_theta)
        ),
        viability_sharpness=float(
            state.get("viability_sharpness", base.viability_sharpness)
        ),
    )


def load_playground_state(sports: Path) -> dict:
    """Load sports/tier1_cell10_playground_state.json if present; else {}.

    Missing or corrupt file → empty dict (callers fall back to config defaults).
    Not on the daily 540 checklist path — legacy CELL 10 UI state only.
    """
    path = sports / "tier1_cell10_playground_state.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


# =============================================================================
# 5. inverted_u_bin_table — MAIN PLOT B DATA (X = L_Q always)
# =============================================================================


def inverted_u_bin_table(
    players: pd.DataFrame,
    sel: SelectionConfig,
    *,
    assign_poolq_bin_labels,
    tpa=None,
) -> pd.DataFrame:
    """Binned inverted-U table: X-axis always L_Q (``poolq_loo``), not crowding.

    What each output column *is*
      bin              — bin label from assign_poolq_bin_labels
      n                — how many players in the bin
      selection_rate   — mean Y_selected (or Y_promoted) in the bin
      mean_loo_q       — mean L_Q inside the bin (Plot B X)

    Args
      players — roster table that already has LOO columns + Y_selected
                (after assign_selection), or at least poolq_loo + outcome.
      sel     — SelectionConfig (n_bins, bin_mode; L mode does NOT move X).
      assign_poolq_bin_labels — callable(series, n_bins, bin_mode) → bin labels
                (usually from sports_pipeline / notebook helper).
      tpa     — optional tier1_pool_assignment module.

    Reminder: sel.loo_pool_l_mode affects the selection *score* only (upstream).
    Bins stay on LOO mean teammate ability so Plot B stays comparable across
    quality vs crowding score modes.
    """
    if tpa is None:
        import tier1_pool_assignment as tpa  # noqa: PLC0415

    ycol = _outcome_col(players)
    # bin_lcol: always L_Q column name — fixed X-axis by design.
    bin_lcol = tpa.POOL_L_QUALITY_COL
    use = players.dropna(subset=[bin_lcol, ycol]).copy()
    use["bin"] = assign_poolq_bin_labels(use[bin_lcol], sel.n_bins, sel.bin_mode)
    return (
        use.dropna(subset=["bin"])
        .groupby("bin", observed=True)
        .agg(
            n=(ycol, "size"),
            selection_rate=(ycol, "mean"),
            mean_loo_q=(bin_lcol, "mean"),
        )
        .reset_index()
        .sort_values("mean_loo_q")
    )


# =============================================================================
# 6. inverted_u_bin_table_team_mean — OPTIONAL 539-STYLE X-AXIS
# =============================================================================


def inverted_u_bin_table_team_mean(
    players: pd.DataFrame,
    sel: SelectionConfig,
    *,
    assign_poolq_bin_labels,
) -> pd.DataFrame:
    """539-style Plot B′: binned selection rate vs realized pool (team) mean ability.

    Differs from inverted_u_bin_table: X is each team’s mean A (including self),
    not LOO L_Q. Use only when you deliberately want the 539 notebook axis.
    """
    ycol = _outcome_col(players)
    use = players.copy()
    # pool_mean: average ability on this player's team (realized roster mean).
    use["pool_mean"] = use.groupby("pool_id", observed=True)["ability"].transform("mean")
    use = use.dropna(subset=["pool_mean", ycol])
    use["bin"] = assign_poolq_bin_labels(use["pool_mean"], sel.n_bins, sel.bin_mode)
    return (
        use.dropna(subset=["bin"])
        .groupby("bin", observed=True)
        .agg(
            n=(ycol, "size"),
            selection_rate=(ycol, "mean"),
            mean_team_mean=("pool_mean", "mean"),
        )
        .reset_index()
        .sort_values("mean_team_mean")
    )


# =============================================================================
# 7. figure_inverted_u — DRAW PLOT B
# =============================================================================


def figure_inverted_u(
    summ: pd.DataFrame,
    *,
    title: str,
    n_bins: int,
    n_teams: int,
    show_bin_n: bool = True,
    loo_pool_l_mode: str = "quality",
    x_col: str | None = None,
    xlabel: str | None = None,
    tpa=None,
) -> plt.Figure:
    """Draw the inverted-U / Plot B line from a bin summary table.

    Args
      summ            — output of inverted_u_bin_table(_team_mean).
      title           — full matplotlib title (often from plot_b_figure_title).
      n_bins / n_teams— kept for call-site clarity / future annotations
                        (not all are drawn on the axes today).
      show_bin_n      — if True, print n=… above each point.
      loo_pool_l_mode — unused for X; kept so callers can pass sel fields.
      x_col           — force which summ column is X; else auto-detect
                        mean_team_mean / mean_loo_q / legacy mean_loo_l.
      xlabel          — X axis label string; default PLOT_B_XAXIS_LABEL.
      tpa             — optional tier1_pool_assignment (imported if needed later).
    """
    if tpa is None:
        import tier1_pool_assignment as tpa  # noqa: PLC0415

    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    # Pick X column: explicit override, else team_mean, else L_Q, else legacy name.
    if x_col is not None:
        xcol = x_col
    elif "mean_team_mean" in summ.columns:
        xcol = "mean_team_mean"
    elif "mean_loo_q" in summ.columns:
        xcol = "mean_loo_q"
    elif "mean_loo_l" in summ.columns:
        xcol = "mean_loo_l"
    else:
        raise KeyError("summ needs mean_loo_q, mean_team_mean, or legacy mean_loo_l")
    x = summ[xcol].to_numpy(dtype=float)
    # rate_col: selection_rate (current) or promo_rate (legacy column name).
    rate_col = (
        "selection_rate"
        if "selection_rate" in summ.columns
        else "promo_rate"
    )
    y = summ[rate_col].to_numpy(dtype=float)
    ax.plot(x, y, "o-", color="C0", lw=2.0, ms=7)
    ax.fill_between(x, 0, y, alpha=0.12, color="C0")
    ax.set_xlabel(xlabel or PLOT_B_XAXIS_LABEL)
    ax.set_ylabel(PLOT_B_YAXIS_LABEL)
    ax.set_title(title, fontsize=10)
    ymax = float(y.max()) if len(y) else 0.0
    ymin = float(y.min()) if len(y) else 0.0
    if ymax <= 0:
        ax.set_ylim(0, 0.01)
    else:
        span = ymax - max(ymin, 0.0)
        pad = max(span * 0.12, ymax * 0.08, 1e-4)
        ax.set_ylim(0, min(1.0, ymax + pad))

    if show_bin_n and "n" in summ.columns and len(summ):
        y_top = ax.get_ylim()[1]
        for xi, yi, ni in zip(x, y, summ["n"].to_numpy(dtype=int), strict=True):
            label_y = min(float(yi) + y_top * 0.04, y_top * 0.98)
            ax.text(
                xi,
                label_y,
                f"n={int(ni):,}",
                ha="center",
                va="bottom",
                fontsize=7,
                color="0.35",
                clip_on=True,
            )

    fig.tight_layout()
    return fig


# =============================================================================
# 8. run_inverted_u_pipeline — ONE-SHOT ASSIGN → SELECT → BIN → FIGURE
# =============================================================================


def run_inverted_u_pipeline(
    params: AssignmentParams,
    sel: SelectionConfig,
    rng,
    *,
    tpa,
    assign_poolq_bin_labels,
    method: str = "soft",
    ability: np.ndarray | None = None,
    team_targets: np.ndarray | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, plt.Figure]:
    """Full preview: ASSIGN → SCORE/SELECT → L_Q bin table → Plot B figure.

    This is the thin “conductor” Pass A/B-style previews call. Heavy math is in
    tier1_pool_assignment; this function only sequences the steps.

    Args
      params   — AssignmentParams (league + assign knobs; Pass B varies ρ here).
      sel      — SelectionConfig (K, score mode, w, L mode; Pass A varies these).
      rng      — NumPy Generator (caller owns the seed).
      tpa      — tier1_pool_assignment module.
      assign_poolq_bin_labels — binning helper (same as inverted_u_bin_table).
      method   — "soft" or "sort_chop" (Pass B extreme arm).
      ability / team_targets — optional pre-drawn A_i / T_j so Pass B reuses
                               the same talent deck across ρ arms.

    Returns
      players — roster with LOO columns, selection_weight, Y_selected
      summ    — inverted_u_bin_table (n, selection_rate, mean_loo_q per bin)
      fig     — matplotlib Figure for Plot B
    """
    # Step 1 — ASSIGN: build fake rosters (no Y_selected yet).
    players, _, _ = tpa.simulate_generative_rosters(
        params,
        rng=rng,
        method=method,
        ability=ability,
        team_targets=team_targets,
    )
    # Steps 2–3 — SCORE then SELECT (adds L columns, S_i, Y_selected).
    players = tpa.assign_selection(
        players,
        rng,
        n_selected=sel.n_selected,
        score_mode=sel.score_mode,
        loo_gap_weight=sel.loo_gap_weight,
        winner_selection=sel.winner_selection,
        pool_l_mode=sel.loo_pool_l_mode,
        viability_theta=params.viability_theta,
        viability_sharpness=params.viability_sharpness,
    )
    # Bin on L_Q and draw Plot B.
    summ = inverted_u_bin_table(
        players, sel, assign_poolq_bin_labels=assign_poolq_bin_labels, tpa=tpa
    )
    fig = figure_inverted_u(
        summ,
        title=plot_b_figure_title(
            sel,
            header=f"Inverted-U preview (J={params.n_teams})",
            tpa=tpa,
        ),
        n_bins=sel.n_bins,
        n_teams=params.n_teams,
        loo_pool_l_mode=sel.loo_pool_l_mode,
        tpa=tpa,
    )
    return players, summ, fig
