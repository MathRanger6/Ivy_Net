"""Shared labels for Cell 10 (537 notebook) and faithful sweep candidate plots.

Option tuples are (display label, internal value) and match ipywidgets.Dropdown options
in sports/cell10_playground_run.py. Import this module from the sweep plotter so PNG
titles use the same wording as the widgets (no A/B/C translation table).
"""

from __future__ import annotations

from typing import Any, Sequence

# --- Dropdown option lists: (label shown in widget, value stored in sim / CSV) ---

POOL_ASSIGNMENT_OPTIONS: list[tuple[str, str]] = [
    ("Random equal pools", "A"),
    ("Assortative", "B"),
    ("Disassortative", "C"),
]

SCORE_MODE_OPTIONS: list[tuple[str, str]] = [
    ("Local rank only", "local_rank"),
    ("w·local rank + (1-w)·A_i", "local_rank_plus_ability"),
    ("w·(A_i−LOO pool q)+(1-w)·A_i", "loo_gap_plus_ability"),
]

BINNING_MODE_OPTIONS: list[tuple[str, str]] = [
    ("Individuals: bins on plot x", "individual_qcut"),
    (
        "Pools: equal pool count (x = mean LOO peer A in bin)",
        "pool_equal_count",
    ),
    (
        "Pools: equal width on mean A (x = mean LOO peer A in bin)",
        "pool_equal_width",
    ),
]

VIEW_MODE_OPTIONS: list[tuple[str, str]] = [
    ("With pools · local rank", "pool_local"),
    ("With pools · global rank", "pool_global"),
    ("With pools · ability A_i", "pool_A"),
    ("No pools · global rank (reference)", "nopool_global"),
]

ABILITY_OPTIONS: list[tuple[str, str]] = [
    ("A — Uniform(0,1)", "A"),
    ("B — clipped Normal(0.5, 0.18)", "B"),
    ("C — scaled Beta(2,5)", "C"),
]

WINNER_OPTIONS: list[tuple[str, str]] = [
    ("A — weighted K w/o replacement", "A"),
    ("B — independent Bernoulli", "B"),
    ("C — deterministic top-K", "C"),
]

PERSON_X_BINNING_OPTIONS: list[tuple[str, str]] = [
    ("Person x: equal count (quantile)", "equal_count"),
    ("Person x: equal width", "equal_width"),
]


def _label(options: Sequence[tuple[str, str]], value: str) -> str:
    for label, val in options:
        if val == value:
            return label
    return str(value)


def format_faithful_sweep_plot_metadata_lines(rank: int, row: dict[str, Any]) -> list[str]:
    """Human-readable lines: same Cell 10 wording as the playground widgets.

    Used below the axis in ``faithful_537_sweep.plot_top`` so long settings stay legible.
    """
    pool_l = _label(POOL_ASSIGNMENT_OPTIONS, str(row["pool_assignment"]))
    score_l = _label(SCORE_MODE_OPTIONS, str(row["score_mode"]))
    abil_l = _label(ABILITY_OPTIONS, str(row["ability_choice"]))
    win_l = _label(WINNER_OPTIONS, str(row["winner_choice"]))
    lines: list[str] = [
        f"Candidate #{int(rank)} — settings (Cell 10 labels)",
        f"Pool assignment: {pool_l}",
        f"Promotion score: {score_l}",
    ]
    smode = str(row["score_mode"])
    if smode == "local_rank_plus_ability":
        lines.append(
            f"ADDITIVE w (local-rank share): {float(row['local_rank_weight']):.2f}"
        )
    elif smode == "loo_gap_plus_ability":
        lines.append(
            f"ADDITIVE w (LOO-gap share): {float(row['local_rank_weight']):.2f}"
        )
    lines.extend(
        [
            f"Winner draw: {win_l}",
            f"A_i distribution: {abil_l}",
            f"Sorting noise sd: {float(row['sorting_noise_sd']):g}",
            f"Min A to promote: {float(row['min_ability_for_promotion']):g}",
            f"N individuals: {int(row['n'])}",
            f"Promotions per run (K): {int(row['k'])}",
            f"Pools (#): {int(row['n_pools'])}",
            f"Runs (playground): {int(row['n_runs'])}",
            f"Pool–talent bins (#): {int(row['n_pool_bins'])}",
        ]
    )
    return lines


def format_faithful_sweep_plot_title(rank: int, row: dict[str, Any]) -> str:
    """Compact chart title only; full settings live in :func:`format_faithful_sweep_plot_metadata_lines`."""
    return f"#{int(rank)} — mean promotion vs pool-quality bin (shaded = seed range)"
