#!/usr/bin/env python3
"""Compose a 3×3 data-story PNG from a manifest of panel images + text cells.

Run (repo root):
  python sports/scripts/build_data_story_mosaic.py \\
    --manifest 3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/mbb_reigning_3x3_manifest.json
"""

from __future__ import annotations

import argparse
import json
import textwrap
from datetime import date
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.gridspec import GridSpec

REPO = Path(__file__).resolve().parents[2]


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


def _image_panel(ax, img_path: Path, *, title: str, panel_dpi: int = 200) -> None:
    img = _load_image(img_path)
    ax.imshow(img, aspect="auto")
    ax.axis("off")
    ax.set_title(title, fontsize=10, pad=6)


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


def build_mosaic(manifest: dict[str, Any], out_png: Path) -> Path:
    grid = manifest["grid"]
    if len(grid) != 9:
        raise ValueError(f"Expected 9 cells, got {len(grid)}")

    fig_w = float(manifest.get("fig_width_in", 24))
    fig_h = float(manifest.get("fig_height_in", 18))
    panel_dpi = int(manifest.get("panel_dpi", 200))
    mosaic_dpi = int(manifest.get("mosaic_dpi", 300))
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor="white")
    gs = GridSpec(3, 3, figure=fig, wspace=0.06, hspace=0.22)

    suptitle = manifest.get("title", "Data story")
    subtitle = manifest.get("subtitle", "")
    fig.suptitle(suptitle, fontsize=14, fontweight="bold", y=0.98)
    if subtitle:
        fig.text(0.5, 0.955, subtitle, ha="center", fontsize=9, color="0.35")

    for idx, cell in enumerate(grid):
        row, col = divmod(idx, 3)
        ax = fig.add_subplot(gs[row, col])
        title = str(cell.get("title", ""))
        kind = cell.get("type", "image")

        if kind == "text":
            _text_panel(ax, title=title, lines=list(cell.get("lines", [])))
        elif kind == "image":
            img_path = _resolve(str(cell["path"]))
            _image_panel(ax, img_path, title=title, panel_dpi=panel_dpi)
        elif kind == "placeholder":
            _placeholder_panel(ax, title=title, note=str(cell.get("note", "TBD")))
        else:
            raise ValueError(f"Unknown cell type: {kind}")

    footer = manifest.get(
        "footer",
        f"Data story mosaic · {date.today().isoformat()}",
    )
    fig.text(0.01, 0.008, footer, fontsize=7, color="0.45")
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=mosaic_dpi, bbox_inches="tight", facecolor="white")
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
    args = parser.parse_args()

    manifest_path = _resolve(str(args.manifest))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    out_png = _resolve(str(args.out or manifest["output_png"]))
    built = build_mosaic(manifest, out_png)
    print(f"Wrote {built.relative_to(REPO)}")


if __name__ == "__main__":
    main()
