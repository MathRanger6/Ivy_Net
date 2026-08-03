"""Mathtext for Pass A/B/C gallery PNGs (matplotlib) and slides (python-pptx runs).

Matplotlib: wrap math in $...$ in titles/labels.
Slides: same $...$ convention; math segments render as Cambria Math + sub/superscripts.
"""

from __future__ import annotations

import re

_GREEK = {
    r"\lambda": "λ",
    r"\rho": "ρ",
    r"\sigma": "σ",
    r"\pi": "π",
    r"\beta": "β",
    r"\propto": "∝",
    r"\exp": "exp",
    r"\cdot": "·",
    r"\Rightarrow": "⇒",
    r"\rightarrow": "→",
    r"\uparrow": "↑",
    r"\!": "",
}


def configure_matplotlib_mathtext() -> None:
    import matplotlib as mpl

    mpl.rcParams.update(
        {
            "mathtext.fontset": "cm",
            "axes.unicode_minus": False,
        }
    )


def _strip_math_commands(s: str) -> str:
    s = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\texttt\{([^}]*)\}", r"\1", s)
    for tok, ch in _GREEK.items():
        s = s.replace(tok, ch)
    return s


def _add_run(paragraph, text: str, *, size: int, italic: bool = False, sub: bool = False) -> None:
    from pptx.util import Pt

    if not text:
        return
    run = paragraph.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.name = "Cambria Math"
    run.font.italic = italic
    run.font.subscript = sub


def _populate_math_runs(paragraph, math: str, *, size: int) -> None:
    """Render a single $...$ math segment into pptx runs."""
    math = _strip_math_commands(math)
    i = 0
    buf: list[str] = []
    italic = True

    def flush() -> None:
        nonlocal buf, italic
        if buf:
            _add_run(paragraph, "".join(buf), size=size, italic=italic)
            buf = []

    while i < len(math):
        ch = math[i]
        if ch == "_":
            flush()
            i += 1
            if i < len(math) and math[i] == "{":
                j = math.index("}", i)
                sub = math[i + 1 : j]
                i = j + 1
            elif i < len(math):
                sub = math[i]
                i += 1
            else:
                sub = ""
            _add_run(paragraph, sub, size=size, italic=True, sub=True)
            continue
        if ch == "^":
            flush()
            i += 1
            if i < len(math) and math[i] == "{":
                j = math.index("}", i)
                sup = math[i + 1 : j]
                i = j + 1
            elif i < len(math):
                sup = math[i]
                i += 1
            else:
                sup = ""
            from pptx.util import Pt

            run = paragraph.add_run()
            run.text = sup
            run.font.size = Pt(max(size - 2, 8))
            run.font.name = "Cambria Math"
            run.font.superscript = True
            continue
        if ch.isalpha() and ch.isupper() and len(buf) == 0:
            italic = True
        buf.append(ch)
        i += 1
    flush()


def populate_paragraph_with_latex(paragraph, text: str, *, font_size: int = 11) -> None:
    """Parse plain text with $...$ math into a python-pptx paragraph."""
    from pptx.util import Pt

    paragraph.text = ""
    parts = text.split("$")
    for idx, part in enumerate(parts):
        if not part:
            continue
        if idx % 2 == 1:
            _populate_math_runs(paragraph, part, size=font_size)
        else:
            run = paragraph.add_run()
            run.text = part
            run.font.size = Pt(font_size)


def fill_bullets_latex(text_frame, lines: list[str], *, font_size: int = 11) -> None:
    text_frame.clear()
    text_frame.word_wrap = True
    for i, line in enumerate(lines):
        para = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        populate_paragraph_with_latex(para, line, font_size=font_size)
        para.level = 0
        para.space_after = 3
        para.space_before = 0
