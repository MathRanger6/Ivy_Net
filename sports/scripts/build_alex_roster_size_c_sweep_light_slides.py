#!/usr/bin/env python3
"""Light AUTO slides for Alex — LG roster capacity C sweep (10, 11, 15).

Slides-only (uses existing PNGs in grandchild_assign/). No diagnostic rerun.

Run (repo root):
  python sports/scripts/build_alex_roster_size_c_sweep_light_slides.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, SLIDES_AUTO, ensure_hero_dirs
from pd17_interval_overlap_slide import build_interval_overlap_slide, load_meta

ASSIGN = GRANDCHILD_ASSIGN
META = ASSIGN / "GRANDCHILD_roster_size_c_sweep_2011_2021_meta.json"

FIG_LC = ASSIGN / "GRANDCHILD_roster_size_c_sweep_lc_2011_2021.png"
FIG_SEL = ASSIGN / "GRANDCHILD_roster_size_c_sweep_selection_2011_2021.png"

OUT_LC = SLIDES_AUTO / "CHAR_grandchild_roster_size_c_sweep_lc_AUTO.pptx"
OUT_SEL = SLIDES_AUTO / "CHAR_grandchild_roster_size_c_sweep_selection_AUTO.pptx"


def _run_row(meta: dict, c: int) -> dict | None:
    for row in meta.get("runs", []):
        if int(row.get("roster_size", -1)) == int(c):
            return row
    return None


def _lc_bullets(meta: dict) -> list[str]:
    emp = meta.get("empirical", {})
    emp_lc = emp.get("L_C", {})
    seasons = meta.get("seasons", "2011-2021")
    rho = meta.get("rho", 0.5)
    gamma = meta.get("gamma", 0.5)
    bullets = [
        rf"Team $L_C$ after ASSIGN — same $\sigma(\gamma(\hat{{A}}_j-\theta))$ as NCAA.",
        rf"MBB {seasons} · min 20 min panel · $\rho={rho:g}$, $\gamma={gamma:g}$.",
        rf"NCAA: $n={emp_lc.get('n', 0):,}$ team-seasons · "
        rf"mean={emp_lc.get('mean', 0):.3f} · sd={emp_lc.get('std', 0):.3f}.",
    ]
    for c in meta.get("roster_sizes", []):
        row = _run_row(meta, c)
        if not row:
            continue
        lc = row.get("L_C", {})
        bullets.append(
            rf"$C={c}$: $n={lc.get('n', 0):,}$ teams · "
            rf"mean={lc.get('mean', 0):.3f} · sd={lc.get('std', 0):.3f}."
        )
    bullets.extend(
        [
            r"$C=10$ closest to NCAA team count (~6.2k vs 6.5k); $C=15$ = gallery default.",
            r"L\_C first moment stable across capacity — score-side calibration OK.",
            r"Capacity is a labeled sensitivity, not a silent swap for $C=15$.",
        ]
    )
    return bullets


def _selection_bullets(meta: dict) -> list[str]:
    emp = meta.get("empirical", {})
    curv_emp = emp.get("curvature_loo", {})
    seasons = meta.get("seasons", "2011-2021")
    rho = meta.get("rho", 0.5)
    bullets = [
        r"SELECT: draft rate vs LOO peer quality (left) and pool mean (right).",
        rf"MBB {seasons} · fixed $\rho={rho:g}$ · empirical dashed blue.",
        rf"Empirical LOO: {curv_emp.get('shape', '?').replace('_', ' ')} "
        rf"(peak bin {curv_emp.get('peak_bin', '?')}, "
        rf"{100 * curv_emp.get('peak_rate', 0):.2f}\%).",
    ]
    for c in meta.get("roster_sizes", []):
        row = _run_row(meta, c)
        if not row:
            continue
        curv = row.get("curvature_loo", {})
        bullets.append(
            rf"LG $C={c}$: {curv.get('shape', '?').replace('_', ' ')} on LOO."
        )
    bullets.extend(
        [
            r"Lowering $C$ toward rotation-cohort scale does not recover inverted-U.",
            r"$\rho$ shapes ASSIGN sorting; selection curvature lives in SCORE ($\lambda$).",
            r"Next lever: $\lambda$ sweep on SELECT — not $\rho$ or $C$ alone.",
        ]
    )
    return bullets


def main() -> None:
    ensure_hero_dirs()
    meta = load_meta(META)
    seasons = meta.get("seasons", "2011-2021")
    emp_lc = meta.get("empirical", {}).get("L_C", {})
    row10 = _run_row(meta, 10) or {}
    lc10 = row10.get("L_C", {})

    build_interval_overlap_slide(
        fig_path=FIG_LC,
        out_pptx=OUT_LC,
        title=r"LG capacity sweep — team $L_C$ vs NCAA",
        subtitle=rf"MBB {seasons} · $C \in {{10,11,15}}$ · NCAA mean={emp_lc.get('mean', 0):.3f}",
        bullets=_lc_bullets(meta),
        claim=(
            "Talking point: C=10 aligns team counts; L_C mean ~0.251 at every C — "
            "capacity mismatch is interpretive, not a broken L_C calibration."
        ),
    )
    print(f"Wrote {OUT_LC}")

    build_interval_overlap_slide(
        fig_path=FIG_SEL,
        out_pptx=OUT_SEL,
        title=r"LG capacity sweep — SELECT vs empirical Hero",
        subtitle=rf"MBB {seasons} · LOO + pool mean · all LG curves monotone",
        bullets=_selection_bullets(meta),
        claim=(
            "Talking point: C fixes headcount, not selection shape — "
            "empirical inverted-U survives; λ is the promising SCORE knob."
        ),
    )
    print(f"Wrote {OUT_SEL}")


if __name__ == "__main__":
    main()
