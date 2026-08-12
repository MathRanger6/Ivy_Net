#!/usr/bin/env python3
"""Light AUTO slides for Alex — LG empirical roster caps (Aug 2026).

Slides-only (uses existing PNGs in grandchild_assign/). No diagnostic rerun.

Run (repo root):
  python sports/scripts/build_alex_empirical_roster_caps_light_slides.py
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
META = ASSIGN / "GRANDCHILD_empirical_roster_caps_2011_2021_meta.json"

FIG_ROSTER = ASSIGN / "GRANDCHILD_empirical_roster_caps_roster_compare_2011_2021.png"
FIG_LC = ASSIGN / "GRANDCHILD_empirical_roster_caps_lc_2011_2021.png"
FIG_SEL = ASSIGN / "GRANDCHILD_empirical_roster_caps_selection_2011_2021.png"

OUT_ROSTER = SLIDES_AUTO / "CHAR_grandchild_empirical_roster_caps_roster_AUTO.pptx"
OUT_LC = SLIDES_AUTO / "CHAR_grandchild_empirical_roster_caps_lc_AUTO.pptx"
OUT_SEL = SLIDES_AUTO / "CHAR_grandchild_empirical_roster_caps_selection_AUTO.pptx"


def _roster_bullets(meta: dict) -> list[str]:
    emp = meta.get("empirical", {}).get("roster_sizes", {})
    sim = meta.get("sim", {}).get("roster_sizes", {})
    seasons = meta.get("seasons", "2011-2021")
    bullets = [
        r"Alex ask: LG stub capacities = exact NCAA filtered roster-size multiset.",
        rf"MBB {seasons} · min 20 min · one capacity per real team-season per year.",
        rf"NCAA / LG: $n={emp.get('n', 0):,}$ team-seasons · "
        rf"mean={emp.get('mean', 0):.1f} · median={emp.get('median', 0):.0f} · "
        rf"sd={emp.get('std', 0):.1f}.",
        rf"Range {int(emp.get('min', 0))}–{int(emp.get('max', 0))} qualifying players per team.",
        r"Replaces fixed $C=15$ repack ($J=N/15$, every roster exactly 15).",
        r"Same player pool (~62k); ASSIGN homophily unchanged — only input geometry.",
    ]
    if sim and sim.get("mean") == emp.get("mean"):
        bullets.append(r"LG realized roster sizes match NCAA by construction (overlay).")
    return bullets


def _lc_bullets(meta: dict) -> list[str]:
    emp = meta.get("empirical", {})
    sim = meta.get("sim", {})
    emp_lc = emp.get("L_C", {})
    sim_lc = sim.get("L_C", {})
    seasons = meta.get("seasons", "2011-2021")
    rho = meta.get("rho", 0.5)
    gamma = meta.get("gamma", 0.5)
    return [
        r"Team $L_C$ after empirical-cap ASSIGN vs real NCAA rosters.",
        rf"MBB {seasons} · $\rho={rho:g}$, $\gamma={gamma:g}$.",
        rf"NCAA: $n={emp_lc.get('n', 0):,}$ · mean={emp_lc.get('mean', 0):.3f} · "
        rf"sd={emp_lc.get('std', 0):.3f}.",
        rf"LG empirical caps: $n={sim_lc.get('n', 0):,}$ · mean={sim_lc.get('mean', 0):.3f} · "
        rf"sd={sim_lc.get('std', 0):.3f}.",
        r"Team count now aligned (6,492) — fixed $C=15$ had only 4,140 teams.",
        r"L\_C first moment still matches; slightly wider LG tail (assign noise).",
        r"Input comparability fixed; SCORE/SELECT shape is a separate question.",
    ]


def _selection_bullets(meta: dict) -> list[str]:
    emp = meta.get("empirical", {})
    sim = meta.get("sim", {})
    curv_emp = emp.get("curvature_loo", {})
    curv_sim = sim.get("curvature_loo", {})
    seasons = meta.get("seasons", "2011-2021")
    rho = meta.get("rho", 0.5)
    return [
        r"SELECT: draft rate vs LOO peer quality (left) and pool mean (right).",
        rf"MBB {seasons} · empirical caps · $\rho={rho:g}$ · default $\lambda$.",
        rf"Empirical LOO: {curv_emp.get('shape', '?').replace('_', ' ')} "
        rf"(peak bin {curv_emp.get('peak_bin', '?')}, "
        rf"{100 * curv_emp.get('peak_rate', 0):.2f}\%).",
        rf"LG empirical caps: {curv_sim.get('shape', '?').replace('_', ' ')} on LOO.",
        r"Roster-size alignment does not recover Hero inverted-U alone.",
        r"$\rho$ = ASSIGN sorting; $\lambda$ = SCORE congestion penalty — next sweep.",
        r"C sweep and exact caps both monotone — shape gap is not headcount.",
    ]


def main() -> None:
    ensure_hero_dirs()
    meta = load_meta(META)
    seasons = meta.get("seasons", "2011-2021")
    emp_rs = meta.get("empirical", {}).get("roster_sizes", {})
    emp_lc = meta.get("empirical", {}).get("L_C", {})

    build_interval_overlap_slide(
        fig_path=FIG_ROSTER,
        out_pptx=OUT_ROSTER,
        title=r"LG input — empirical roster-size multiset",
        subtitle=rf"MBB {seasons} · mean={emp_rs.get('mean', 0):.1f} vs old fixed $C=15$",
        bullets=_roster_bullets(meta),
        claim=(
            "Talking point: Alex's fix — LG teams get the exact filtered NCAA "
            "roster-size distribution, not a synthetic 15-man league."
        ),
    )
    print(f"Wrote {OUT_ROSTER}")

    build_interval_overlap_slide(
        fig_path=FIG_LC,
        out_pptx=OUT_LC,
        title=r"Empirical caps — team $L_C$ vs NCAA",
        subtitle=rf"MBB {seasons} · 6,492 team-seasons · NCAA mean={emp_lc.get('mean', 0):.3f}",
        bullets=_lc_bullets(meta),
        claim=(
            "Talking point: comparability achieved — same team count and L_C mean; "
            "assignment layer is now apples-to-apples on roster geometry."
        ),
    )
    print(f"Wrote {OUT_LC}")

    build_interval_overlap_slide(
        fig_path=FIG_SEL,
        out_pptx=OUT_SEL,
        title=r"Empirical caps — SELECT vs Hero",
        subtitle=rf"MBB {seasons} · LOO still monotone · empirical inverted-U",
        bullets=_selection_bullets(meta),
        claim=(
            "Talking point: input fix necessary but not sufficient — "
            "λ sweep on SELECT is the next experiment."
        ),
    )
    print(f"Wrote {OUT_SEL}")


if __name__ == "__main__":
    main()
