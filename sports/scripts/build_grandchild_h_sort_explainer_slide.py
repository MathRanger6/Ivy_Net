#!/usr/bin/env python3
"""Build H_sort glossary reference slide (Grandchild / PD17 / Alex brief).

Text explainer with optional inset: GRANDCHILD_rho_vs_assortativity.png (if present).

Run (repo root):
  /opt/anaconda3/envs/sports_net/bin/python sports/scripts/build_grandchild_h_sort_explainer_slide.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import GRANDCHILD_ASSIGN, SLIDES_AUTO, ensure_hero_dirs
from h_sort_readout import h_sort_definition_bullet, h_sort_note_bullet
from pd17_interval_overlap_slide import build_text_reference_slide

OUT_PPTX = SLIDES_AUTO / "CHAR_grandchild_h_sort_explainer_AUTO.pptx"
INSET_FIG = GRANDCHILD_ASSIGN / "GRANDCHILD_rho_vs_assortativity.png"

CLAIM = (
    r"Claim: H_{sort} is realized assortativity on a fixed partition — "
    "generative homophily \\rho is the ASSIGN knob; measure H_{sort} after assign."
)

SUBTITLE = (
    r"Realized sorting index · LG / PD17 · alias \texttt{sorting\_index\_h} in code"
)


def _bullets() -> list[str]:
    return [
        h_sort_definition_bullet(),
        r"Denominator: total Sum of Squares (SS) — spread of \hat{A}_i around \bar{A}.",
        r"Numerator: within-team Sum of Squares (SS) — spread around \mu_{g(i)}.",
        r"H_{sort} = 1 - (within-team SS)/(total SS); explained-variance / Analysis of Variance (ANOVA)-style.",
        r"H_{sort} \approx 0: team label tells you little (random-like partition).",
        r"H_{sort} \approx 1: teams are perfectly separated (point-mass rosters).",
        r"Alex one-liner: knowing roster explains how much ability deviates from \bar{A}.",
        r"Not Newman network assortativity r — partition statistic on abilities.",
        r"Complements interval overlap (geometry) — use both in brief.",
        r"\rho \uparrow \Rightarrow H_{sort} \uparrow in LG sweep (see inset plot).",
        h_sort_note_bullet(),
        r"Memo: grandchild_assign/GRANDCHILD_D_and_H_sort_interpretation.md",
    ]


def main() -> None:
    ensure_hero_dirs()
    fig = INSET_FIG if INSET_FIG.is_file() else None
    if fig is None:
        print(f"Note: inset figure missing ({INSET_FIG.name}); building text-only slide.")

    build_text_reference_slide(
        out_pptx=OUT_PPTX,
        title=r"What is $H_{sort}$? Realized assortativity on rosters",
        subtitle=SUBTITLE,
        bullets=_bullets(),
        claim=CLAIM,
        fig_path=fig,
    )


if __name__ == "__main__":
    main()
