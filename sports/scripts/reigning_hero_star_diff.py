"""Diff text: reigning hero star-sweep runs vs slide-12 lock."""

from __future__ import annotations

from typing import Any

REIGNING_LOCK_TAG = "perm_loo_ever_lastps_ew16"
LOCK_BETA_SQ_09_21 = 0.00172

SEASON_WINDOW_LABELS: dict[str, str] = {
    "09_21": "2009–2021",
    "11_21": "2011–2021",
    "13_21": "2013–2021",
    "09_19": "2009–2019",
}

SEASON_WINDOW_NOTES: dict[str, str] = {
    "09_21": "Same season window as reigning lock (2009–2021).",
    "11_21": "Drops 2009–10 vs lock — full ESPN panel start (2011–21).",
    "13_21": "Drops 2009–12 vs lock — primary campaign window (2013–21).",
    "09_19": "Drops 2020–21 vs lock — pre-COVID end state (2009–19).",
}


def _n_bins_note(lock_bins: int, run_bins: int) -> str:
    if run_bins == lock_bins:
        return f"EW ventiles: {run_bins} (same as lock)."
    direction = "coarser" if run_bins < lock_bins else "finer"
    return (
        f"EW ventiles: {lock_bins} → {run_bins} ({direction} equal-width bins on poolq_LOO). "
        "Bar heights and ventile labels change; LPM fits continuous poolq_LOO so β₂ should "
        "match lock within the same season window."
    )


def diff_from_reigning_lock(run: dict[str, Any], lock: dict[str, Any]) -> dict[str, Any]:
    """Return terse deltas, subtitle, and prose for one manifest run vs reigning lock."""
    lock_bins = int(lock.get("n_bins", 16))
    lock_win = str(lock.get("season_window", "09_21"))
    run_bins = int(run.get("n_bins", run.get("spec", {}).get("n_bins", 0)))
    run_win = str(run.get("season_window", run.get("spec", {}).get("season_window", "")))

    terse: list[str] = []
    if run_bins != lock_bins:
        terse.append(f"n_bins: {lock_bins} → {run_bins}")
    if run_win != lock_win:
        terse.append(f"season_window: {lock_win} → {run_win}")

    held = [
        "poolq_loo",
        "y-draft-mode ever",
        "panel-rows last-ps",
        "ALLT",
        "equal_width",
        "min20 · mg10 · winsor 0.01–0.99",
    ]

    prose_lines = [
        _n_bins_note(lock_bins, run_bins),
        SEASON_WINDOW_NOTES.get(run_win, f"Season window {run_win}."),
    ]

    shape = run.get("shape") or {}
    beta = shape.get("beta_sq")
    if run_win == lock_win and beta is not None:
        if abs(float(beta) - LOCK_BETA_SQ_09_21) < 5e-4:
            prose_lines.append(
                f"LPM β₂ = {beta:+.5g} — matches lock ({LOCK_BETA_SQ_09_21:+.5g}); "
                "bin count is a display choice only."
            )
        else:
            prose_lines.append(
                f"LPM β₂ = {beta:+.5g} (lock {LOCK_BETA_SQ_09_21:+.5g} at EW16)."
            )
    elif beta is not None:
        prose_lines.append(
            f"LPM β₂ = {beta:+.5g} — era shift vs lock; concave/negative β₂ common off 09–21."
        )

    subtitle = (
        f"Δ vs reigning lock (EW{lock_bins} · {lock_win.replace('_', '–')}): "
        + ("; ".join(terse) if terse else "same axes (not in sweep grid)")
    )

    return {
        "terse": terse,
        "held_constant": held,
        "prose_lines": prose_lines,
        "subtitle": subtitle,
        "lock_tag": REIGNING_LOCK_TAG,
        "lock_label": f"Reigning hero · EW{lock_bins} · {SEASON_WINDOW_LABELS.get(lock_win, lock_win)}",
    }
