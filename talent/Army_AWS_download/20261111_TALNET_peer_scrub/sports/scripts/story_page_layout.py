"""Print-oriented layout presets for STORY mosaic PNGs (3×3 and perf-metric decks)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PageSize = Literal["screen", "letter", "tabloid"]
MosaicPageSize = Literal[
    "screen", "letter", "letter-landscape", "tabloid", "tabloid-landscape"
]
# 3×3 data-story mosaics (landscape variants are print-friendly for wide panels).
MOSAIC_PAGE_SIZE_CHOICES: tuple[str, ...] = (
    "screen",
    "letter",
    "letter-landscape",
    "tabloid",
    "tabloid-landscape",
)
# Perf-metric storyboards — portrait only (tall row stacks).
PERF_PAGE_SIZE_CHOICES: tuple[str, ...] = ("screen", "letter", "tabloid")
PAGE_SIZE_CHOICES: tuple[str, ...] = MOSAIC_PAGE_SIZE_CHOICES


@dataclass(frozen=True)
class Mosaic3x3Layout:
    fig_width_in: float
    fig_height_in: float
    mosaic_dpi: int
    suptitle_fontsize: float
    subtitle_fontsize: float
    suptitle_y: float
    subtitle_y: float
    grid_top: float
    grid_bottom: float
    grid_left: float
    grid_right: float
    wspace: float
    hspace: float
    panel_title_fontsize: float
    pad_inches_with_footer: float
    pad_inches_no_footer: float
    show_subtitle: bool = True
    show_panel_titles: bool = True
    use_tight_bbox: bool = True


@dataclass(frozen=True)
class PerfStoryLayout:
    fig_width_in: float
    max_height_in: float
    mosaic_dpi: int
    title_band_in: float
    suptitle_fontsize: float
    suptitle_y: float
    grid_top: float
    grid_bottom: float
    grid_left: float
    grid_right: float
    hspace: float
    wspace: float
    pad_inches_with_footer: float
    pad_inches_no_footer: float
    use_tight_bbox: bool = True


MOSAIC_3X3: dict[str, Mosaic3x3Layout] = {
    "screen": Mosaic3x3Layout(
        fig_width_in=24.0,
        fig_height_in=18.0,
        mosaic_dpi=400,
        suptitle_fontsize=17.0,
        subtitle_fontsize=11.5,
        suptitle_y=0.985,
        subtitle_y=0.968,
        grid_top=0.925,
        grid_bottom=0.03,
        grid_left=0.04,
        grid_right=0.98,
        wspace=0.06,
        hspace=0.20,
        panel_title_fontsize=10.0,
        pad_inches_with_footer=0.06,
        pad_inches_no_footer=0.015,
        show_subtitle=True,
        show_panel_titles=True,
        use_tight_bbox=True,
    ),
    "letter": Mosaic3x3Layout(
        fig_width_in=8.5,
        fig_height_in=11.0,
        mosaic_dpi=520,
        suptitle_fontsize=14.0,
        subtitle_fontsize=9.0,
        suptitle_y=0.975,
        subtitle_y=0.955,
        grid_top=0.945,
        grid_bottom=0.008,
        grid_left=0.04,
        grid_right=0.98,
        wspace=0.02,
        hspace=0.06,
        panel_title_fontsize=7.5,
        pad_inches_with_footer=0.02,
        pad_inches_no_footer=0.0,
        show_subtitle=False,
        show_panel_titles=True,
        use_tight_bbox=False,
    ),
    # US letter landscape 11×8.5 — recommended handout for 3×3 (wider cells).
    "letter-landscape": Mosaic3x3Layout(
        fig_width_in=11.0,
        fig_height_in=8.5,
        mosaic_dpi=520,
        suptitle_fontsize=14.5,
        subtitle_fontsize=9.0,
        suptitle_y=0.972,
        subtitle_y=0.952,
        grid_top=0.938,
        grid_bottom=0.01,
        grid_left=0.035,
        grid_right=0.985,
        wspace=0.025,
        hspace=0.045,
        panel_title_fontsize=8.0,
        pad_inches_with_footer=0.02,
        pad_inches_no_footer=0.0,
        show_subtitle=False,
        show_panel_titles=True,
        use_tight_bbox=False,
    ),
    "tabloid": Mosaic3x3Layout(
        fig_width_in=11.0,
        fig_height_in=17.0,
        mosaic_dpi=420,
        suptitle_fontsize=16.0,
        subtitle_fontsize=10.0,
        suptitle_y=0.982,
        subtitle_y=0.965,
        grid_top=0.935,
        grid_bottom=0.012,
        grid_left=0.04,
        grid_right=0.98,
        wspace=0.03,
        hspace=0.10,
        panel_title_fontsize=9.0,
        pad_inches_with_footer=0.03,
        pad_inches_no_footer=0.0,
        show_subtitle=False,
        show_panel_titles=True,
        use_tight_bbox=False,
    ),
    # US tabloid landscape 17×11.
    "tabloid-landscape": Mosaic3x3Layout(
        fig_width_in=17.0,
        fig_height_in=11.0,
        mosaic_dpi=420,
        suptitle_fontsize=16.5,
        subtitle_fontsize=10.0,
        suptitle_y=0.978,
        subtitle_y=0.962,
        grid_top=0.928,
        grid_bottom=0.012,
        grid_left=0.035,
        grid_right=0.985,
        wspace=0.03,
        hspace=0.06,
        panel_title_fontsize=9.5,
        pad_inches_with_footer=0.03,
        pad_inches_no_footer=0.0,
        show_subtitle=False,
        show_panel_titles=True,
        use_tight_bbox=False,
    ),
}


PERF_STORY: dict[str, PerfStoryLayout] = {
    "screen": PerfStoryLayout(
        fig_width_in=17.5,
        max_height_in=28.0,
        mosaic_dpi=350,
        title_band_in=0.45,
        suptitle_fontsize=18.0,
        suptitle_y=0.98,
        grid_top=0.94,
        grid_bottom=0.03,
        grid_left=0.04,
        grid_right=0.98,
        hspace=0.12,
        wspace=0.06,
        pad_inches_with_footer=0.04,
        pad_inches_no_footer=0.01,
        use_tight_bbox=True,
    ),
    "letter": PerfStoryLayout(
        fig_width_in=8.5,
        max_height_in=11.0,
        mosaic_dpi=480,
        title_band_in=0.35,
        suptitle_fontsize=15.0,
        suptitle_y=0.985,
        grid_top=0.955,
        grid_bottom=0.02,
        grid_left=0.03,
        grid_right=0.98,
        hspace=0.08,
        wspace=0.04,
        pad_inches_with_footer=0.0,
        pad_inches_no_footer=0.0,
        use_tight_bbox=False,
    ),
    "tabloid": PerfStoryLayout(
        fig_width_in=11.0,
        max_height_in=17.0,
        mosaic_dpi=400,
        title_band_in=0.40,
        suptitle_fontsize=17.0,
        suptitle_y=0.985,
        grid_top=0.955,
        grid_bottom=0.025,
        grid_left=0.03,
        grid_right=0.98,
        hspace=0.10,
        wspace=0.05,
        pad_inches_with_footer=0.0,
        pad_inches_no_footer=0.0,
        use_tight_bbox=False,
    ),
}


_PERF_FROM_MOSAIC: dict[str, str] = {
    "letter-landscape": "letter",
    "tabloid-landscape": "tabloid",
}


def normalize_mosaic_page_size(page_size: str | None) -> str:
    key = (page_size or "screen").strip().lower()
    if key not in MOSAIC_PAGE_SIZE_CHOICES:
        raise ValueError(
            f"page_size must be one of {MOSAIC_PAGE_SIZE_CHOICES}, got {page_size!r}"
        )
    return key


def normalize_perf_page_size(page_size: str | None) -> str:
    key = (page_size or "screen").strip().lower()
    key = _PERF_FROM_MOSAIC.get(key, key)
    if key not in PERF_PAGE_SIZE_CHOICES:
        raise ValueError(
            f"page_size must be one of {PERF_PAGE_SIZE_CHOICES} "
            f"(mosaic landscape aliases map to portrait), got {page_size!r}"
        )
    return key


def normalize_page_size(page_size: str | None) -> PageSize:
    """Backward-compatible alias — mosaic sizes; use normalize_* helpers in new code."""
    key = normalize_mosaic_page_size(page_size)
    if key in PERF_PAGE_SIZE_CHOICES:
        return key  # type: ignore[return-value]
    return "letter"  # type: ignore[return-value]


def mosaic_3x3_layout(page_size: str | None = None) -> Mosaic3x3Layout:
    return MOSAIC_3X3[normalize_mosaic_page_size(page_size)]


def perf_story_layout(page_size: str | None = None) -> PerfStoryLayout:
    return PERF_STORY[normalize_perf_page_size(page_size)]


def perf_story_figsize(n_rows: int, page_size: str | None = None) -> tuple[float, float]:
    """Full page height on letter/tabloid; row area split evenly (no vertical squish)."""
    layout = perf_story_layout(page_size)
    n_rows = max(int(n_rows), 1)
    if not layout.use_tight_bbox:
        return layout.fig_width_in, layout.max_height_in
    row_band = max(1.85, (layout.max_height_in - layout.title_band_in) / n_rows)
    fig_h = min(layout.max_height_in, layout.title_band_in + row_band * n_rows)
    return layout.fig_width_in, fig_h
