"""Compose perf-metric HERO story PNG(s) — suptitle only, embedded panel titles preserved."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from story_page_layout import perf_story_figsize, perf_story_layout


def build_perf_metric_mosaic(
    rows: list[dict[str, Any]],
    out_png: Path,
    *,
    suptitle: str,
    repo: Path,
    show_footer: bool = True,
    page_size: str = "screen",
    footer_tag: str = "perf metric story",
) -> Path:
    """One page: ``rows`` each need ``q16_png`` and ``ew16_png`` (repo-relative or absolute)."""
    if not rows:
        raise ValueError("rows must be non-empty")
    layout = perf_story_layout(page_size)
    n_rows = len(rows)
    fig_w, fig_h = perf_story_figsize(n_rows, page_size)
    fig = plt.figure(figsize=(fig_w, fig_h), facecolor="white")
    gs = GridSpec(
        n_rows,
        2,
        figure=fig,
        top=layout.grid_top,
        bottom=layout.grid_bottom,
        left=layout.grid_left,
        right=layout.grid_right,
        wspace=layout.wspace,
        hspace=layout.hspace,
    )

    fig.suptitle(
        suptitle,
        fontsize=layout.suptitle_fontsize,
        fontweight="bold",
        y=layout.suptitle_y,
    )

    for i, row in enumerate(rows):
        for j, tag in enumerate(("q16", "ew16")):
            ax = fig.add_subplot(gs[i, j])
            img_path = Path(row[f"{tag}_png"])
            if not img_path.is_absolute():
                img_path = repo / img_path
            img = mpimg.imread(img_path)
            ax.imshow(img, aspect="auto")
            ax.axis("off")

    if show_footer:
        fig.text(
            0.01,
            0.006,
            f"{footer_tag} · {date.today().isoformat()}",
            fontsize=7,
            color="0.45",
        )

    out_png.parent.mkdir(parents=True, exist_ok=True)
    save_kw: dict[str, Any] = {
        "dpi": layout.mosaic_dpi,
        "facecolor": "white",
    }
    if layout.use_tight_bbox:
        save_kw["bbox_inches"] = "tight"
        save_kw["pad_inches"] = (
            layout.pad_inches_with_footer if show_footer else layout.pad_inches_no_footer
        )
    fig.savefig(out_png, **save_kw)
    plt.close(fig)
    return out_png


def build_perf_metric_story_pages(
    rows: list[dict[str, Any]],
    out_dir: Path,
    out_stem: str,
    *,
    suptitle: str,
    repo: Path,
    show_footer: bool = True,
    page_size: str = "screen",
    footer_tag: str = "perf metric story",
    rows_per_page: int | None = None,
) -> list[Path]:
    """Write one or more pages; ``out_stem_p1.png``, ``_p2.png``, … when split."""
    if rows_per_page is None or len(rows) <= rows_per_page:
        single = out_dir / f"{out_stem}.png"
        build_perf_metric_mosaic(
            rows,
            single,
            suptitle=suptitle,
            repo=repo,
            show_footer=show_footer,
            page_size=page_size,
            footer_tag=footer_tag,
        )
        return [single]

    built: list[Path] = []
    n_pages = (len(rows) + rows_per_page - 1) // rows_per_page
    for page_idx in range(n_pages):
        chunk = rows[page_idx * rows_per_page : (page_idx + 1) * rows_per_page]
        page_title = f"{suptitle}  ({page_idx + 1}/{n_pages})"
        out_png = out_dir / f"{out_stem}_p{page_idx + 1}.png"
        build_perf_metric_mosaic(
            chunk,
            out_png,
            suptitle=page_title,
            repo=repo,
            show_footer=show_footer,
            page_size=page_size,
            footer_tag=footer_tag,
        )
        built.append(out_png)
    return built
