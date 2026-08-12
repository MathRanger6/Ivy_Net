#!/usr/bin/env python3
"""Light AUTO slide for Alex — LG λ SELECT sweep (empirical roster caps).

Slides-only (uses existing PNG in grandchild_assign/). No diagnostic rerun.

Run (repo root):
  python sports/scripts/build_alex_lambda_select_sweep_light_slides.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, SLIDES_AUTO, ensure_hero_dirs
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

ASSIGN = GRANDCHILD_ASSIGN
META = ASSIGN / "GRANDCHILD_lambda_select_sweep_2011_2021_meta.json"
FIG = ASSIGN / "GRANDCHILD_lambda_select_sweep_2011_2021.png"
OUT = SLIDES_AUTO / "CHAR_grandchild_lambda_select_sweep_AUTO.pptx"


def _run_row(meta: dict, lam: float) -> dict | None:
    for row in meta.get("runs", []):
        if abs(float(row.get("lambda", -1)) - float(lam)) < 1e-9:
            return row
    return None


def _selection_bullets(meta: dict) -> list[str]:
    emp = meta.get("empirical", {})
    curv_emp = emp.get("curvature_loo", {})
    seasons = meta.get("seasons", "2011-2021")
    rho = meta.get("rho", 0.5)
    bullets = [
        r"SELECT: draft rate vs LOO peer quality (left) and pool mean (right).",
        rf"MBB {seasons} · empirical roster caps · fixed $\rho={rho:g}$ · sweep $\lambda$ in $S=A-\lambda L_C$.",
        rf"Empirical LOO: {curv_emp.get('shape', '?').replace('_', ' ')} "
        rf"(peak bin {curv_emp.get('peak_bin', '?')}, "
        rf"{100 * curv_emp.get('peak_rate', 0):.2f}\%).",
    ]
    for row in meta.get("runs", []):
        lam = float(row.get("lambda", 0))
        curv = row.get("curvature_loo", {})
        bullets.append(
            rf"LG $\lambda={lam:g}$: {curv.get('shape', '?').replace('_', ' ')} on LOO."
        )
    bullets.extend(
        [
            r"Input geometry fixed (Alex caps) — only SCORE congestion weight moves.",
            r"$\rho$ = ASSIGN; $\lambda$ = SCORE — test whether inverted-U lives in selection.",
            r"Compare curvature labels across $\lambda$ arms, not just level shifts.",
        ]
    )
    return bullets


def _claim(meta: dict) -> str:
    runs = meta.get("runs", [])
    shapes = [r.get("curvature_loo", {}).get("shape", "?") for r in runs]
    if any(s == "inverted_u_like" for s in shapes):
        return (
            "Talking point: at least one λ arm shows inverted-U-like LOO curvature — "
            "SCORE knob can move selection shape after input comparability."
        )
    return (
        "Talking point: λ sweep under empirical caps — if all arms stay monotone, "
        "inverted-U may need a different L definition or SELECT rule, not λ alone."
    )


def main() -> None:
    ensure_hero_dirs()
    meta = load_meta(META)
    seasons = meta.get("seasons", "2011-2021")
    rho = meta.get("rho", 0.5)
    lam_str = ", ".join(f"{x:g}" for x in meta.get("lambda_values", []))

    build_interval_overlap_slide(
        fig_path=FIG,
        out_pptx=OUT,
        title=r"Empirical caps — $\lambda$ sweep on SELECT",
        subtitle=rf"MBB {seasons} · $\rho={rho:g}$ · $\lambda \in \{{{lam_str}\}}$ · empirical caps held fixed",
        bullets=_selection_bullets(meta),
        claim=_claim(meta),
    )
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
