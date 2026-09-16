#!/usr/bin/env python3
"""Build 1×3 composite: Army G1 CIF + MBB reigning HERO + tenure HERO (flipbook 3.3)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "3-Master_Plan/re_entry/HEROs_and_PASSes/composites"
OUT_PNG = OUT_DIR / "THREE_LEG_HERO_composite.png"

PANELS: list[tuple[str, Path]] = [
    (
        "Army · promotion CIF vs pool-minus-mean (G1)",
        REPO
        / "3-Master_Plan/re_entry/HEROs_and_PASSes/army_sandbox/ARMY_G1_pool_minus_mean_fwd_cif_b8.png",
    ),
    (
        "MBB · draft rate vs poolq LOO (reigning EW16)",
        REPO
        / "3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/hero/HERO_ew16_allt_min20_mg10_09_21_last_ps_perm_loo_ever_lastps_ew16.png",
    ),
    (
        "Tenure · rate vs dept LOO career rate (PD29 Q16)",
        REPO
        / "3-Master_Plan/re_entry/HEROs_and_PASSes/tenure_sandbox/hero/HERO_tenure_q16_decision_dept_loo_infHM_slide.png",
    ),
]


def _load_rgb(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGB")


def main() -> None:
    images = [_load_rgb(p) for _, p in PANELS]
    target_h = 720
    scaled: list[Image.Image] = []
    for img in images:
        w = int(img.width * target_h / img.height)
        scaled.append(img.resize((w, target_h), Image.Resampling.LANCZOS))

    header_h = 48
    gap = 16
    margin = 24
    total_w = margin * 2 + sum(im.width for im in scaled) + gap * (len(scaled) - 1)
    total_h = margin * 2 + header_h + target_h

    canvas = Image.new("RGB", (total_w, total_h), "white")
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 14)
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
        title_font = font

    draw.text(
        (margin, margin),
        "Three-leg hero porch — same LOO logic, graded signal (flipbook 3.3)",
        fill="black",
        font=title_font,
    )

    x = margin
    y = margin + header_h
    for (label, _), im in zip(PANELS, scaled, strict=True):
        canvas.paste(im, (x, y))
        draw.text((x, y + target_h + 4), label, fill="#333333", font=font)
        x += im.width + gap

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT_PNG, dpi=(150, 150))
    print(f"Wrote {OUT_PNG}")


if __name__ == "__main__":
    main()
