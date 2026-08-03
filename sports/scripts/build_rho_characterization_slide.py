#!/usr/bin/env python3
"""Build two-slide ρ characterization deck (with / without sort-and-chop on figure).

Run (repo root):
  python sports/scripts/build_rho_characterization_slide.py

Regenerates Pass C PNG variants, then writes:
  3-Master_Plan/re_entry/HEROs_and_PASSes/CHAR_rho_characterization.pptx
    slide 1 — sort-and-chop visible
    slide 2 — sort-and-chop suppressed (soft ρ arms only)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
GALLERY = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"
META = GALLERY / "PASS_C_rho_ablation_meta.json"
OUT_PPTX = GALLERY / "CHAR_rho_characterization.pptx"
PASS_C_SCRIPT = SCRIPTS / "pass_c_rho_ablation_bundle.py"

FIG_WITH = GALLERY / "PASS_C_rho_ablation_selection_by_pool_mean_with_sortchop.png"
FIG_WITHOUT = GALLERY / "PASS_C_rho_ablation_selection_by_pool_mean_no_sortchop.png"

sys.path.insert(0, str(SCRIPTS))
from gallery_mathtext import fill_bullets_latex, populate_paragraph_with_latex

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.45)
CONTENT_W = SLIDE_W - 2 * MARGIN
COL_GAP = Inches(0.22)
LEFT_W = Inches(4.55)
RIGHT_W = CONTENT_W - LEFT_W - COL_GAP

CLAIM = (
    "Claim: at fixed score and top-$K$, $\\rho$ in assignment matters — "
    "low-$\\rho$ mixing yields a nearly flat curve; high-$\\rho$ assortativity "
    "delivers the peer-pressure inverted-$U$ readout."
)

SLIDE_VARIANTS = [
    {
        "subtitle": "sort-and-chop shown",
        "figure": FIG_WITH,
        "show_sortchop_on_figure": True,
    },
    {
        "subtitle": "sort-and-chop suppressed",
        "figure": FIG_WITHOUT,
        "show_sortchop_on_figure": False,
    },
]


def _load_meta() -> dict:
    if META.is_file():
        return json.loads(META.read_text(encoding="utf-8"))
    return {"selection": {"w": 0.55}, "assignment_sigma": 0.65, "preset": "539"}


def _run_pass_c(*, show_sort_chop: bool, png_suffix: str) -> None:
    env = os.environ.copy()
    env["GALLERY_SHOW_SORT_CHOP"] = "1" if show_sort_chop else "0"
    env["GALLERY_PASS_C_PNG_SUFFIX"] = png_suffix
    subprocess.run(
        [sys.executable, str(PASS_C_SCRIPT)],
        cwd=str(REPO),
        env=env,
        check=True,
    )


def _regenerate_figures() -> None:
    print("Regenerating Pass C figure (with sort-and-chop) ...")
    _run_pass_c(show_sort_chop=True, png_suffix="_with_sortchop")
    print("Regenerating Pass C figure (no sort-and-chop on plot) ...")
    _run_pass_c(show_sort_chop=False, png_suffix="_no_sortchop")


def _add_picture_fitted(slide, img_path: Path, left, top, max_width, max_height):
    if not img_path.is_file():
        box = slide.shapes.add_textbox(left, top, max_width, Inches(0.4))
        box.text_frame.text = f"[Missing figure: {img_path.name}]"
        return

    pic = slide.shapes.add_picture(str(img_path), left, top, width=max_width)
    if pic.height > max_height:
        scale = max_height / pic.height
        pic.height = int(pic.height * scale)
        pic.width = int(pic.width * scale)
    pic.left = left + (max_width - pic.width) // 2


def _add_params_column(
    slide,
    meta: dict,
    *,
    left,
    top,
    width,
    height,
    show_sortchop_on_figure: bool,
) -> None:
    w = float(meta.get("selection", {}).get("w", 0.55))
    sigma = float(meta.get("assignment_sigma", 0.65))
    preset = meta.get("preset", "539")

    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.clear()

    head = tf.paragraphs[0]
    populate_paragraph_with_latex(
        head,
        rf"Characterize $\rho$ — one-at-a-time at {preset} baseline "
        r"(score + top-$K$ fixed)",
        font_size=11,
    )
    head.font.bold = True
    head.space_after = 6

    eq = tf.add_paragraph()
    eq.text = ""
    eq.space_after = 4
    populate_paragraph_with_latex(
        eq,
        r"$\pi_{ij} \propto \exp\!\left(-\rho\,\frac{(A_i-T_j)^2}{2\sigma^2}\right)$",
        font_size=12,
    )

    arms_line = (
        rf"$\sigma={sigma:g}$ fixed"
        "\n"
        rf"arms: $\rho \in {{0.1, 1, 8, 32}}$"
    )
    if show_sortchop_on_figure:
        arms_line += " + sort-and-chop"
    bullets = [
        arms_line,
        rf"$S_i = A_i - {w:g}\,L_C$ (crowding in score held constant across arms)",
        r"top-$K$ by $S_i$",
        r"VISUALIZE = mean $Y_{\mathrm{selected}}$ vs pool mean ($16$ bins)",
    ]
    for line in bullets:
        para = tf.add_paragraph()
        para.text = ""
        populate_paragraph_with_latex(para, line, font_size=10)
        para.space_after = 2
        para.level = 0


def _add_oat_notes(
    slide,
    *,
    left,
    top,
    width,
    height,
    show_sortchop_on_figure: bool,
) -> None:
    bullets = [
        r"OAT: one draw of $A_i$, $T_j$ (seed $42$); only ASSIGN changes across arms.",
        r"Low $\rho$: players mix across teams — selection vs pool mean stays nearly flat.",
        r"High $\rho$: assortative matching — peer environments concentrate; inverted-$U$ emerges.",
    ]
    if show_sortchop_on_figure:
        bullets.append(
            r"Sort-and-chop benchmark: hard rank match (same score rule as soft arms)."
        )
    else:
        bullets.append(
            r"Sort-and-chop arm omitted from plot (still in CSV bundle; toggle restores it)."
        )

    box = slide.shapes.add_textbox(left, top, width, height)
    fill_bullets_latex(box.text_frame, bullets, font_size=9)


def _add_slide(prs: Presentation, meta: dict, variant: dict) -> None:
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title_top = Inches(0.28)
    title_h = Inches(0.46)
    title_box = slide.shapes.add_textbox(MARGIN, title_top, CONTENT_W, title_h)
    populate_paragraph_with_latex(
        title_box.text_frame.paragraphs[0],
        rf"Phase B — Characterize $\rho$ (assignment assortativity) — {variant['subtitle']}",
        font_size=20,
    )
    title_box.text_frame.paragraphs[0].font.bold = True

    body_top = title_top + title_h + Inches(0.1)
    footer_h = Inches(0.52)
    footer_top = SLIDE_H - MARGIN - footer_h
    notes_h = Inches(1.35)
    params_h = footer_top - body_top - notes_h - Inches(0.08)

    left_x = MARGIN
    right_x = MARGIN + LEFT_W + COL_GAP

    _add_params_column(
        slide,
        meta,
        left=left_x,
        top=body_top,
        width=LEFT_W,
        height=params_h,
        show_sortchop_on_figure=variant["show_sortchop_on_figure"],
    )

    _add_picture_fitted(
        slide,
        variant["figure"],
        right_x,
        body_top,
        RIGHT_W,
        params_h,
    )

    _add_oat_notes(
        slide,
        left=left_x,
        top=footer_top - notes_h - Inches(0.06),
        width=LEFT_W + RIGHT_W + COL_GAP,
        height=notes_h,
        show_sortchop_on_figure=variant["show_sortchop_on_figure"],
    )

    foot = slide.shapes.add_textbox(MARGIN, footer_top, CONTENT_W, footer_h)
    populate_paragraph_with_latex(foot.text_frame.paragraphs[0], CLAIM, font_size=11)
    foot.text_frame.paragraphs[0].font.bold = True
    foot.text_frame.paragraphs[0].alignment = PP_ALIGN.LEFT


def main() -> None:
    GALLERY.mkdir(parents=True, exist_ok=True)
    _regenerate_figures()
    meta = _load_meta()

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    for variant in SLIDE_VARIANTS:
        _add_slide(prs, meta, variant)

    prs.save(str(OUT_PPTX))
    print(f"Wrote {OUT_PPTX} ({len(SLIDE_VARIANTS)} slides)")


if __name__ == "__main__":
    main()
