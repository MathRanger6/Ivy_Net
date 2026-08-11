"""Output paths for PD17 team interval overlap diagnostics (full panel vs season window)."""

from __future__ import annotations

from hero_gallery_paths import EMPIRICAL_PD17, GRANDCHILD_ASSIGN, SLIDES, SLIDES_AUTO

# Default apples-to-apples compare window (HAND17 slides 4 & 5 reference).
DEFAULT_WINDOW_SEASON_MIN = 2015
DEFAULT_WINDOW_SEASON_MAX = 2019


def window_tag(season_min: int, season_max: int) -> str:
    return f"{season_min}_{season_max}"


def seasons_label(season_min: int, season_max: int) -> str:
    if season_min == season_max:
        return str(season_min)
    return f"{season_min}-{season_max}"


def empirical_overlap_paths(*, season_min: int | None = None, season_max: int | None = None) -> dict:
    """Full panel (2011-2021) when season_min and season_max are both None."""
    if season_min is None and season_max is None:
        stem = "EMPIRICAL_team_interval_overlap"
        deck = SLIDES_AUTO / "CHAR_empirical_team_interval_overlap_AUTO.pptx"
    else:
        if season_min is None or season_max is None:
            raise ValueError("season_min and season_max must both be set for a window run")
        tag = window_tag(season_min, season_max)
        stem = f"EMPIRICAL_team_interval_overlap_{tag}"
        deck = SLIDES_AUTO / f"CHAR_empirical_team_interval_overlap_{tag}_AUTO.pptx"
    return {
        "png": EMPIRICAL_PD17 / f"{stem}.png",
        "csv": EMPIRICAL_PD17 / f"{stem}_team_season.csv",
        "meta": EMPIRICAL_PD17 / f"{stem}_meta.json",
        "deck": deck,
        "season_min": season_min,
        "season_max": season_max,
        "seasons": seasons_label(season_min, season_max) if season_min is not None else "2011-2021",
    }


def grandchild_overlap_paths(
    *,
    season_min: int,
    season_max: int,
    single_season_legacy: bool = False,
) -> dict:
    """Legacy names for default single-season 2015; tagged files for all other runs."""
    if single_season_legacy:
        return {
            "png": GRANDCHILD_ASSIGN / "GRANDCHILD_league_interval_overlap.png",
            "csv": GRANDCHILD_ASSIGN / "GRANDCHILD_league_interval_team.csv",
            "meta": GRANDCHILD_ASSIGN / "GRANDCHILD_league_interval_meta.json",
            "deck": SLIDES / "CHAR_grandchild_league_analysis.pptx",
            "season_min": season_min,
            "season_max": season_max,
            "seasons": str(season_min),
            "legacy": True,
        }
    tag = window_tag(season_min, season_max)
    stem = f"GRANDCHILD_league_interval_overlap_{tag}"
    return {
        "png": GRANDCHILD_ASSIGN / f"{stem}.png",
        "csv": GRANDCHILD_ASSIGN / f"{stem}_team_season.csv",
        "meta": GRANDCHILD_ASSIGN / f"{stem}_meta.json",
        "deck": SLIDES_AUTO / f"CHAR_grandchild_league_interval_overlap_{tag}_AUTO.pptx",
        "season_min": season_min,
        "season_max": season_max,
        "seasons": seasons_label(season_min, season_max),
        "legacy": False,
    }
