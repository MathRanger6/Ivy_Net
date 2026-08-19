"""Season window + AUTO deck suffix for PD20–22 campaign regeneration.

Default (full panel): 2011–2021, no suffix on AUTO decks.
Primary window (Alex PD23): 2013–2021, AUTO decks get ``_13_21`` suffix.

Scripts read CLI flags first, then env vars ``PD20_22_SEASON_MIN`` /
``PD20_22_SEASON_MAX`` / ``PD20_22_AUTO_SUFFIX``, then defaults.

Shell driver: ``scripts/regenerate_pd20_22_auto_13_21.sh``
"""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from pathlib import Path

from interval_overlap_paths import seasons_label

FULL_PANEL_SEASON_MIN = 2011
FULL_PANEL_SEASON_MAX = 2021
PRIMARY_SEASON_MIN = 2013
PRIMARY_SEASON_MAX = 2021
PRIMARY_AUTO_SUFFIX = "_13_21"

_current: "CampaignWindow | None" = None


@dataclass(frozen=True)
class CampaignWindow:
    season_min: int
    season_max: int
    auto_suffix: str = ""

    @property
    def tag(self) -> str:
        return f"{self.season_min}_{self.season_max}"

    @property
    def label(self) -> str:
        return seasons_label(self.season_min, self.season_max)

    @property
    def is_full_panel(self) -> bool:
        return self.season_min == FULL_PANEL_SEASON_MIN and self.season_max == FULL_PANEL_SEASON_MAX

    @classmethod
    def full_panel(cls) -> CampaignWindow:
        return cls(FULL_PANEL_SEASON_MIN, FULL_PANEL_SEASON_MAX, auto_suffix="")

    @classmethod
    def primary(cls) -> CampaignWindow:
        return cls(
            PRIMARY_SEASON_MIN,
            PRIMARY_SEASON_MAX,
            auto_suffix=PRIMARY_AUTO_SUFFIX,
        )


def default_auto_suffix(season_min: int, season_max: int) -> str:
    if season_min == PRIMARY_SEASON_MIN and season_max == PRIMARY_SEASON_MAX:
        return PRIMARY_AUTO_SUFFIX
    if season_min == FULL_PANEL_SEASON_MIN and season_max == FULL_PANEL_SEASON_MAX:
        return ""
    return f"_{season_min}_{season_max}"


def resolve_window(
    *,
    season_min: int | None = None,
    season_max: int | None = None,
    auto_suffix: str | None = None,
) -> CampaignWindow:
    smin = (
        int(season_min)
        if season_min is not None
        else int(os.environ.get("PD20_22_SEASON_MIN", FULL_PANEL_SEASON_MIN))
    )
    smax = (
        int(season_max)
        if season_max is not None
        else int(os.environ.get("PD20_22_SEASON_MAX", FULL_PANEL_SEASON_MAX))
    )
    suffix = auto_suffix
    if suffix is None:
        suffix = os.environ.get("PD20_22_AUTO_SUFFIX")
    if suffix is None:
        suffix = default_auto_suffix(smin, smax)
    return CampaignWindow(smin, smax, auto_suffix=str(suffix))


def resolve_window_from_args(args: argparse.Namespace) -> CampaignWindow:
    return resolve_window(
        season_min=getattr(args, "season_min", None),
        season_max=getattr(args, "season_max", None),
        auto_suffix=getattr(args, "auto_suffix", None),
    )


def set_current_window(window: CampaignWindow) -> None:
    global _current
    _current = window


def current_window() -> CampaignWindow:
    global _current
    if _current is None:
        _current = resolve_window()
    return _current


def add_window_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--season-min",
        type=int,
        default=None,
        help=f"Panel season min (default: env PD20_22_SEASON_MIN or {FULL_PANEL_SEASON_MIN}).",
    )
    parser.add_argument(
        "--season-max",
        type=int,
        default=None,
        help=f"Panel season max (default: env PD20_22_SEASON_MAX or {FULL_PANEL_SEASON_MAX}).",
    )
    parser.add_argument(
        "--auto-suffix",
        type=str,
        default=None,
        help=(
            "Suffix on AUTO .pptx names before _AUTO (default: _13_21 for 2013–2021, "
            "empty for 2011–2021)."
        ),
    )


def window_cli_flags(window: CampaignWindow | None = None) -> list[str]:
    """Subprocess argv fragment for child scripts."""
    w = window or current_window()
    out = ["--season-min", str(w.season_min), "--season-max", str(w.season_max)]
    if w.auto_suffix:
        out.extend(["--auto-suffix", w.auto_suffix])
    return out


def auto_deck_path(base: Path, window: CampaignWindow | None = None) -> Path:
    """``CHAR_foo_AUTO.pptx`` → ``CHAR_foo_13_21_AUTO.pptx`` when suffix set."""
    w = window or current_window()
    if not w.auto_suffix:
        return base
    stem = base.stem
    if stem.endswith("_AUTO"):
        stem = stem[: -len("_AUTO")] + f"{w.auto_suffix}_AUTO"
    else:
        stem = f"{stem}{w.auto_suffix}"
    return base.with_name(stem + base.suffix)


def activate_from_args(args: argparse.Namespace) -> CampaignWindow:
    window = resolve_window_from_args(args)
    set_current_window(window)
    return window
