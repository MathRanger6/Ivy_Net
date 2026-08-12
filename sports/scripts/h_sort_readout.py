"""Shared readout lines for H_sort (realized sorting index) on PD17 / LG slides."""

from __future__ import annotations


def h_sort_definition_bullet() -> str:
    return (
        r"H_{sort} = 1 - \sum_i(\hat{A}_i - \hat{\mu}_{g(i)})^2 "
        r"/ \sum_i(\hat{A}_i - \bar{A})^2 — realized sorting on a fixed partition."
    )


def h_sort_value_bullet(h_sort: float | None, *, label: str = "This partition") -> str | None:
    if h_sort is None:
        return None
    try:
        val = float(h_sort)
    except (TypeError, ValueError):
        return None
    if not (val == val):  # NaN
        return None
    return rf"{label}: H_{{sort}} = {val:.3f} (0 = none, 1 = full team sorting)."


def h_sort_note_bullet() -> str:
    return (
        r"VECTOR lock: H_{sort} is realized sorting — not the generative homophily knob \rho."
    )
