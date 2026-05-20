"""Shared generative EDA: inverted-U bins, params from CELL 10 state JSON."""

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


def _outcome_col(players: pd.DataFrame) -> str:
    if "Y_selected" in players.columns:
        return "Y_selected"
    if "Y_promoted" in players.columns:
        return "Y_promoted"
    raise KeyError("players need Y_selected or Y_promoted")


@dataclass(frozen=True)
class SelectionConfig:
    n_bins: int
    bin_mode: str
    n_selected: int
    score_mode: str
    loo_gap_weight: float
    winner_selection: str
    loo_pool_l_mode: str = "quality"

    @classmethod
    def from_module(cls, mod) -> SelectionConfig:
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


# Deprecated alias
PromotionConfig = SelectionConfig


def assignment_params_from_state(
    sports: Path,
    state: dict | None,
    *,
    tpa,
) -> AssignmentParams:
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
    )


def load_playground_state(sports: Path) -> dict:
    path = sports / "tier1_cell10_playground_state.json"
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def inverted_u_bin_table(
    players: pd.DataFrame,
    sel: SelectionConfig,
    *,
    assign_poolq_bin_labels,
    tpa=None,
) -> pd.DataFrame:
    """Binned inverted-U table: x-axis always L_Q (``poolq_loo``), not crowding.

    ``sel.loo_pool_l_mode`` affects the selection score only (via ``assign_selection``);
    bins are always on LOO mean teammate ability so Plot B stays comparable across
    quality vs crowding score modes.
    """
    if tpa is None:
        import tier1_pool_assignment as tpa  # noqa: PLC0415

    ycol = _outcome_col(players)
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


def figure_inverted_u(
    summ: pd.DataFrame,
    *,
    title: str,
    n_bins: int,
    n_teams: int,
    show_bin_n: bool = True,
    loo_pool_l_mode: str = "quality",
    tpa=None,
) -> plt.Figure:
    if tpa is None:
        import tier1_pool_assignment as tpa  # noqa: PLC0415

    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    if "mean_loo_q" in summ.columns:
        xcol = "mean_loo_q"
    elif "mean_loo_l" in summ.columns:
        xcol = "mean_loo_l"
    else:
        raise KeyError("summ needs mean_loo_q (or legacy mean_loo_l)")
    x = summ[xcol].to_numpy(dtype=float)
    rate_col = (
        "selection_rate"
        if "selection_rate" in summ.columns
        else "promo_rate"
    )
    y = summ[rate_col].to_numpy(dtype=float)
    ax.plot(x, y, "o-", color="C0", lw=2.0, ms=7)
    ax.fill_between(x, 0, y, alpha=0.12, color="C0")
    ax.set_xlabel(f"Bin mean {tpa.pool_l_short_label('quality')}")
    ax.set_ylabel("Mean selection rate")
    ax.set_title(title)
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


def run_inverted_u_pipeline(
    params: AssignmentParams,
    sel: SelectionConfig,
    rng,
    *,
    tpa,
    assign_poolq_bin_labels,
) -> tuple[pd.DataFrame, pd.DataFrame, plt.Figure]:
    """Soft assign → select K → bin table → figure."""
    players, _, _ = tpa.simulate_generative_rosters(params, rng=rng, method="soft")
    players = tpa.assign_selection(
        players,
        rng,
        n_selected=sel.n_selected,
        score_mode=sel.score_mode,
        loo_gap_weight=sel.loo_gap_weight,
        winner_selection=sel.winner_selection,
        pool_l_mode=sel.loo_pool_l_mode,
        viability_theta=params.viability_theta,
    )
    summ = inverted_u_bin_table(
        players, sel, assign_poolq_bin_labels=assign_poolq_bin_labels, tpa=tpa
    )
    fig = figure_inverted_u(
        summ,
        title=f"Inverted-U preview ({sel.n_bins} bins, J={params.n_teams})",
        n_bins=sel.n_bins,
        n_teams=params.n_teams,
        loo_pool_l_mode=sel.loo_pool_l_mode,
        tpa=tpa,
    )
    return players, summ, fig
