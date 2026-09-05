#!/usr/bin/env python3
"""Compose a 3×3 data-story PNG from a manifest of panel images + text cells.

Run (repo root):
  python sports/scripts/build_data_story_mosaic.py \\
    --manifest 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/mbb_reigning_3x3_manifest.json
  python sports/scripts/build_data_story_mosaic.py --manifest ... --no-footer
  python sports/scripts/build_data_story_mosaic.py --manifest ... --page-size letter-landscape --no-footer
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec

REPO = Path(__file__).resolve().parents[2]
if str(REPO / "sports" / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "sports" / "scripts"))

from story_page_layout import MOSAIC_PAGE_SIZE_CHOICES, mosaic_3x3_layout, normalize_mosaic_page_size  # noqa: E402


def _resolve(path_str: str) -> Path:
    p = Path(path_str)
    return p if p.is_absolute() else REPO / p


def _load_image(path: Path):
    if not path.is_file():
        raise FileNotFoundError(path)
    return mpimg.imread(path)


def _text_panel(ax, *, title: str, lines: list[str]) -> None:
    ax.axis("off")
    ax.set_facecolor("#fafafa")
    body = "\n".join(lines)
    ax.text(
        0.04,
        0.96,
        title,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        va="top",
        ha="left",
    )
    ax.text(
        0.04,
        0.88,
        body,
        transform=ax.transAxes,
        fontsize=8,
        va="top",
        ha="left",
        family="monospace",
        linespacing=1.35,
    )


def _image_panel(
    ax,
    img_path: Path,
    *,
    title: str,
    panel_title_fontsize: float,
    show_title: bool = True,
) -> None:
    img = _load_image(img_path)
    ax.imshow(img, aspect="auto")
    ax.axis("off")
    if show_title and title:
        ax.set_title(title, fontsize=panel_title_fontsize, pad=2)


def _placeholder_panel(ax, *, title: str, note: str) -> None:
    ax.axis("off")
    ax.set_facecolor("#f0f0f0")
    ax.text(
        0.5,
        0.55,
        title,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="0.35",
    )
    ax.text(
        0.5,
        0.38,
        note,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=8,
        color="0.45",
        wrap=True,
    )


def build_mosaic(
    manifest: dict[str, Any],
    out_png: Path,
    *,
    show_footer: bool | None = None,
    page_size: str | None = None,
) -> Path:
    grid = manifest["grid"]
    if len(grid) != 9:
        raise ValueError(f"Expected 9 cells, got {len(grid)}")

    if show_footer is None:
        show_footer = bool(manifest.get("show_footer", True))

    page_key = normalize_mosaic_page_size(page_size or manifest.get("page_size"))
    layout = mosaic_3x3_layout(page_key)

    fig_w = float(manifest.get("fig_width_in", layout.fig_width_in))
    fig_h = float(manifest.get("fig_height_in", layout.fig_height_in))
    if page_size or manifest.get("page_size"):
        fig_w = layout.fig_width_in
        fig_h = layout.fig_height_in
    mosaic_dpi = int(manifest.get("mosaic_dpi", layout.mosaic_dpi))
    if page_size or manifest.get("page_size"):
        mosaic_dpi = layout.mosaic_dpi

    pad_inches = float(
        manifest.get(
            "pad_inches",
            layout.pad_inches_with_footer if show_footer else layout.pad_inches_no_footer,
        )
    )

    fig = plt.figure(figsize=(fig_w, fig_h), facecolor="white")
    gs = GridSpec(
        3,
        3,
        figure=fig,
        wspace=layout.wspace,
        hspace=layout.hspace,
        top=layout.grid_top,
        bottom=layout.grid_bottom,
        left=layout.grid_left,
        right=layout.grid_right,
    )

    suptitle = manifest.get("title", "Data story")
    subtitle = manifest.get("subtitle", "")
    fig.suptitle(suptitle, fontsize=layout.suptitle_fontsize, fontweight="bold", y=layout.suptitle_y)
    if subtitle and layout.show_subtitle:
        fig.text(
            0.5,
            layout.subtitle_y,
            subtitle,
            ha="center",
            fontsize=layout.subtitle_fontsize,
            color="0.35",
        )

    for idx, cell in enumerate(grid):
        row, col = divmod(idx, 3)
        ax = fig.add_subplot(gs[row, col])
        title = str(cell.get("title", ""))
        kind = cell.get("type", "image")

        if kind == "text":
            _text_panel(ax, title=title, lines=list(cell.get("lines", [])))
        elif kind == "image":
            img_path = _resolve(str(cell["path"]))
            _image_panel(
                ax,
                img_path,
                title=title,
                panel_title_fontsize=layout.panel_title_fontsize,
                show_title=layout.show_panel_titles,
            )
        elif kind == "placeholder":
            _placeholder_panel(ax, title=title, note=str(cell.get("note", "TBD")))
        else:
            raise ValueError(f"Unknown cell type: {kind}")

    if show_footer:
        footer = manifest.get(
            "footer",
            f"Data story mosaic · {date.today().isoformat()}",
        )
        fig.text(0.01, 0.008, footer, fontsize=7, color="0.45")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    save_kw: dict[str, Any] = {
        "dpi": mosaic_dpi,
        "facecolor": "white",
    }
    if layout.use_tight_bbox:
        save_kw["bbox_inches"] = "tight"
        save_kw["pad_inches"] = pad_inches
    fig.savefig(out_png, **save_kw)
    plt.close(fig)
    return out_png


def main() -> None:
    parser = argparse.ArgumentParser(description="Build 3×3 data-story mosaic PNG")
    parser.add_argument(
        "--manifest",
        type=Path,
        required=True,
        help="JSON manifest (paths relative to repo root unless absolute)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="Override output PNG (default: manifest output_png)",
    )
    parser.add_argument(
        "--no-footer",
        action="store_true",
        help="Omit bottom-left footer (better for Preview/print on letter paper)",
    )
    parser.add_argument(
        "--page-size",
        choices=MOSAIC_PAGE_SIZE_CHOICES,
        default=None,
        help="Print layout: letter-landscape (11×8.5 handout), tabloid-landscape, or screen",
    )
    args = parser.parse_args()

    manifest_path = _resolve(str(args.manifest))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out_png = _resolve(str(args.out or manifest["output_png"]))
    show_footer = False if args.no_footer else None
    built = build_mosaic(
        manifest,
        out_png,
        show_footer=show_footer,
        page_size=args.page_size,
    )
    print(f"Wrote {built.relative_to(REPO)}")


if __name__ == "__main__":
    main()
