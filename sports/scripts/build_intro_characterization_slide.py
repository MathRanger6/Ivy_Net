#!/usr/bin/env python3
"""Build Phase B intro slide (text-only deck opener).

Run (repo root):
  python sports/scripts/build_intro_characterization_slide.py

Outputs:
  HEROs_and_PASSes/slides/auto/CHAR_intro_characterization_AUTO.pptx
"""

from __future__ import annotations

import sys
from pathlib import Path

from pptx import Presentation
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
from gallery_knobs import (
    HERO_K_OVER_N,
    HERO_N_SELECTED,
    HERO_SEED,
    LAMBDA_FIXED_RHO,
    LAMBDA_MODERATE,
    PRESET,
    hero_league_n,
)
from hero_gallery_paths import AUTO_INTRO_DECK, ensure_hero_dirs

from gallery_mathtext import fill_bullets_latex, populate_paragraph_with_latex

OUT_PPTX = AUTO_INTRO_DECK

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN = Inches(0.42)
CONTENT_W = SLIDE_W - 2 * MARGIN
COL_GAP = Inches(0.28)
LEFT_W = Inches(6.35)
RIGHT_W = CONTENT_W - LEFT_W - COL_GAP

TITLE = r"Phase B — Fake-league characterization (not curve fitting)"

GLOSSARY_HEAD = r"Knobs (mini glossary)"
# (symbol, plain name, what it controls) — matches walkthrough SLIDE 0 table
GLOSSARY_ROWS = [
    (r"$A_i$", "Player ability", r"Innate talent draw — Beta(2,2) on [0,1] (539 preset)"),
    (
        r"$T_{j^*}$",
        "Sim assignment target",
        r"Synthetic iid Uniform[0,1] per team (`draw_target_means`); soft-assign attractor — not realized roster talent",
    ),
    (
        r"$T_j$",
        "Realized team talent",
        r"Mean $A_i$ on team $j$'s roster after ASSIGN; empirical $T_{jt}$ from $\hat{A}_i$",
    ),
    (
        r"$\rho$",
        "Assignment assortativity",
        r"Soft match strength: players $\to$ teams with $T_{j^*} \approx A_i$",
    ),
    (
        r"$L_C$",
        "Congestion measure",
        r"LOO peer viability — deck uses smooth $\sigma$; code also has hard share ($A_j>\theta$)",
    ),
    (
        r"$\lambda$",
        "Congestion weight in score",
        r"How hard $L_C$ penalizes ranking — not congestion itself",
    ),
    (r"$\theta$", "Viability cutline", "Center of the sigmoid"),
    (r"$\gamma$", "Sigmoid sharpness", r"Steepness of viability step around $\theta$"),
    (r"$K/N$", "Selectivity", r"Fraction of league selected ($K \div N$)"),
]
GLOSSARY_HEADERS = ("Symbol", "Plain name", "What it controls")

NOTES_HEAD = r"How to read this deck"
NOTES = [
    r"Not curve fitting: which rules \emph{bend} synthetic selection curves — not NCAA fit yet.",
    rf"Three steps: ASSIGN ($\rho$) $\to$ SCORE ($S_i = A_i - \lambda L_C$) $\to$ SELECT (top-$K$); then VISUALIZE by pool-mean bin.",
    r"$L_C$ in this deck: \texttt{crowding\_smooth} (mean $\sigma$). Code also builds hard $L_C$ = LOO share with $A_j > \theta$ — not shown here.",
    r"One-at-a-time (OAT): each slide moves one knob; other settings stay at benchmark values.",
    rf"Seed {HERO_SEED} on stochastic steps: draw $A_i$, $T_{{j^*}}$; soft-$\rho$ assignment. Score, top-$K$, bins are deterministic.",
    rf"League: $N={hero_league_n()}$, $K={HERO_N_SELECTED}$, $K/N={HERO_K_OVER_N:.0%}$ ({PRESET} preset).",
]

BENCHMARK_HEAD = r"Benchmark values (while sweeping other knobs)"
BENCHMARK_BULLETS = [
    rf"$A_i$: Beta(2,2) on [0,1] — \texttt{{SELECTION\_539\_ABILITY\_DRAW}}",
    r"$T_{j^*}$: Uniform[0,1] iid per team — \texttt{draw\_target\_means}; synthetic assignment targets, not NCAA roster data",
    r"$T_j$: realized roster mean after ASSIGN — not drawn; Sketch A 2D $y$-axis",
    rf"$\lambda={LAMBDA_MODERATE:g}$ — \texttt{{tier1\_539\_reference\_settings.json}} / playground default",
    r"$\theta=0.72$, $\gamma=10$ — same 539 reference JSON",
    rf"$\rho={LAMBDA_FIXED_RHO:g}$ — gallery fixed assign for $\lambda$ / $\theta$ slides (moderate-high mixing; not a 539 JSON field)",
    rf"$K/N={HERO_K_OVER_N:.0%}$ — characterization default (MBB draft $\approx$ 1% is a separate calibration point)",
]

EMPIRICAL_HEAD = r"Empirical data (Layer A) vs this deck (Layer C)"
EMPIRICAL_BULLETS = [
    r"Real hero: draft rate vs \textbf{poolq\_loo} (teammate quality, leave-one-out) — a \textbf{bend} at the top bins.",
    r"This deck: fraction selected vs \textbf{pool mean} in a fake league — same \emph{kind} of question, different axis and league.",
    r"Benchmarks anchor to the Alex 539 playground track so sim slides stay comparable; we have \textbf{not} re-fit those numbers to NCAA data in Phase B.",
]


def _set_cell_text(
    cell,
    text: str,
    *,
    font_size: int = 9,
    bold: bool = False,
) -> None:
    cell.text = ""
    tf = cell.text_frame
    tf.word_wrap = True
    tf.margin_left = Pt(4)
    tf.margin_right = Pt(4)
    tf.margin_top = Pt(2)
    tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]
    if "$" in text or "\\" in text:
        populate_paragraph_with_latex(p, text, font_size=font_size)
    else:
        p.text = text
        p.font.size = Pt(font_size)
        p.font.name = "Calibri"
    if bold:
        p.font.bold = True
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE


def _add_glossary_table(slide, *, left, top, width, height) -> None:
    head_box = slide.shapes.add_textbox(left, top, width, Inches(0.28))
    populate_paragraph_with_latex(
        head_box.text_frame.paragraphs[0], GLOSSARY_HEAD, font_size=12
    )
    head_box.text_frame.paragraphs[0].font.bold = True

    table_top = top + Inches(0.3)
    table_h = height - Inches(0.3)
    n_rows = 1 + len(GLOSSARY_ROWS)
    n_cols = 3
    shape = slide.shapes.add_table(n_rows, n_cols, left, table_top, width, table_h)
    table = shape.table

    col_fracs = (0.14, 0.28, 0.58)
    for i, frac in enumerate(col_fracs):
        table.columns[i].width = int(width * frac)

    for j, header in enumerate(GLOSSARY_HEADERS):
        _set_cell_text(table.cell(0, j), header, font_size=9, bold=True)

    for i, (sym, plain, controls) in enumerate(GLOSSARY_ROWS, start=1):
        _set_cell_text(table.cell(i, 0), sym, font_size=9)
        _set_cell_text(table.cell(i, 1), plain, font_size=9)
        _set_cell_text(table.cell(i, 2), controls, font_size=8)

    # Light header shading via solid fill on first row (optional subtle gray)
    from pptx.dml.color import RGBColor

    for j in range(n_cols):
        cell = table.cell(0, j)
        fill = cell.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(0xEE, 0xEE, 0xEE)


def _add_section(
    slide,
    *,
    left,
    top,
    width,
    height,
    head_text: str,
    bullets: list[str],
    head_size: int = 11,
    bullet_size: int = 9,
) -> None:
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.clear()

    head = tf.paragraphs[0]
    populate_paragraph_with_latex(head, head_text, font_size=head_size)
    head.font.bold = True
    head.space_after = 3

    fill_bullets_latex(tf, bullets, font_size=bullet_size)


def main() -> None:
    ensure_hero_dirs()

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    slide = prs.slides.add_slide(prs.slide_layouts[6])

    title_top = Inches(0.24)
    title_h = Inches(0.5)
    title_box = slide.shapes.add_textbox(MARGIN, title_top, CONTENT_W, title_h)
    populate_paragraph_with_latex(
        title_box.text_frame.paragraphs[0], TITLE, font_size=20
    )
    title_box.text_frame.paragraphs[0].font.bold = True

    body_top = title_top + title_h + Inches(0.08)
    footer_h = Inches(0.38)
    body_h = SLIDE_H - MARGIN - footer_h - body_top

    left_x = MARGIN
    right_x = MARGIN + LEFT_W + COL_GAP

    _add_glossary_table(
        slide, left=left_x, top=body_top, width=LEFT_W, height=body_h
    )

    notes_h = Inches(2.05)
    bench_h = Inches(1.55)
    emp_h = body_h - notes_h - bench_h - Inches(0.12)

    _add_section(
        slide,
        left=right_x,
        top=body_top,
        width=RIGHT_W,
        height=notes_h,
        head_text=NOTES_HEAD,
        bullets=NOTES,
        bullet_size=9,
    )
    _add_section(
        slide,
        left=right_x,
        top=body_top + notes_h + Inches(0.04),
        width=RIGHT_W,
        height=bench_h,
        head_text=BENCHMARK_HEAD,
        bullets=BENCHMARK_BULLETS,
        bullet_size=9,
    )
    _add_section(
        slide,
        left=right_x,
        top=body_top + notes_h + bench_h + Inches(0.08),
        width=RIGHT_W,
        height=emp_h,
        head_text=EMPIRICAL_HEAD,
        bullets=EMPIRICAL_BULLETS,
        bullet_size=9,
    )

    foot = slide.shapes.add_textbox(
        MARGIN, SLIDE_H - MARGIN - footer_h, CONTENT_W, footer_h
    )
    populate_paragraph_with_latex(
        foot.text_frame.paragraphs[0],
        r"Claim: Phase B maps which generative knobs move \emph{who gets selected} — prerequisite before Phase C calibration to the hero.",
        font_size=11,
    )
    foot.text_frame.paragraphs[0].font.bold = True

    prs.save(str(OUT_PPTX))
    print(f"Wrote {OUT_PPTX}")


if __name__ == "__main__":
    main()
