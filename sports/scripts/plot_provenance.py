"""Shared plot provenance — HERO / F-HERO population sweeps (Aug 2026).

Filenames use short slugs (q16, pw4p7, allt, 11_21). Full spec lives on the figure
footer and in JSON sidecars.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


def hero_bin_slug(*, poolq_binning: str, n_bins: int) -> str:
    prefix = "q" if str(poolq_binning).strip().lower() == "quantile" else "ew"
    return f"{prefix}{int(n_bins)}"


def hero_bin_label(*, poolq_binning: str, n_bins: int) -> str:
    kind = "QTL" if str(poolq_binning).strip().lower() == "quantile" else "EW"
    return f"{kind}{int(n_bins)}"


def fhero_bin_slug(
    *,
    tj_binning: str = "piecewise_tail",
    tj_n_low: int = 4,
    tj_n_high: int = 7,
    tj_n_bins: int = 24,
) -> str:
    if str(tj_binning).strip().lower() == "piecewise_tail":
        return f"pw{int(tj_n_low)}p{int(tj_n_high)}"
    return f"ew{int(tj_n_bins)}"


def fhero_bin_label(
    *,
    tj_binning: str = "piecewise_tail",
    tj_n_low: int = 4,
    tj_n_high: int = 7,
    tj_n_bins: int = 24,
) -> str:
    if str(tj_binning).strip().lower() == "piecewise_tail":
        return f"piecewise {int(tj_n_low)}+{int(tj_n_high)} T̂_j bins"
    return f"EW{int(tj_n_bins)} T̂_j bins"


def population_slug(*, dft: bool) -> str:
    return "dft" if dft else "allt"


def population_label(*, dft: bool) -> str:
    return "+DFT" if dft else "ALLT"


def season_slug(season_min: int, season_max: int) -> str:
    return f"{int(season_min) % 100}_{int(season_max) % 100}"


def y_draft_short(mode: str) -> str:
    return "season" if str(mode).strip().lower() == "season" else "ever"


def y_draft_label(mode: str) -> str:
    if y_draft_short(mode) == "season":
        return "season-Y (Y=1 on last PS only)"
    return "ever-draft"


ROSTER_X_LOO = "poolq_loo"
ROSTER_X_TEAM = "poolq"
ROSTER_X_MODES = frozenset({ROSTER_X_LOO, ROSTER_X_TEAM})


def normalize_roster_x(mode: str) -> str:
    m = str(mode).strip().lower().replace("-", "_")
    aliases = {
        "loo": ROSTER_X_LOO,
        "poolq_loo": ROSTER_X_LOO,
        "team": ROSTER_X_TEAM,
        "poolq": ROSTER_X_TEAM,
        "pool_mean": ROSTER_X_TEAM,
        "tj": ROSTER_X_TEAM,
        "t_j": ROSTER_X_TEAM,
    }
    m = aliases.get(m, m)
    if m not in ROSTER_X_MODES:
        raise ValueError(
            f"roster_x must be one of {sorted(ROSTER_X_MODES)!r} (aliases: loo, poolq, pool_mean), got {mode!r}"
        )
    return m


def roster_x_slug(mode: str) -> str:
    return normalize_roster_x(mode)


def roster_x_label(mode: str) -> str:
    if normalize_roster_x(mode) == ROSTER_X_TEAM:
        return "poolq (team-season mean perf z; includes self)"
    return "poolq_loo (LOO teammate mean perf z; self excluded)"


def roster_x_mathtext(mode: str) -> str:
    if normalize_roster_x(mode) == ROSTER_X_TEAM:
        return r"$\mathrm{poolq}$"
    return r"$\mathrm{poolq\_loo}$"


def panel_rows_label(panel_rows: str) -> str:
    from sports_pipeline.y_draft_mode import normalize_panel_rows, PANEL_ROWS_LAST

    if normalize_panel_rows(panel_rows) == PANEL_ROWS_LAST:
        return "panel: final-season PS only"
    return "panel: all PS rows"


@dataclass(frozen=True)
class HeroProvenance:
    bin_slug: str
    bin_label: str
    perf_metric: str
    season_min: int
    season_max: int
    min_minutes: float
    min_team_season_games: int
    population: str
    y_draft_mode: str
    winsor_lo: float
    winsor_hi: float
    panel_rows: str = "all-ps"
    n_rows: int | None = None
    n_drafts: int | None = None
    plot_family: str = "HERO"
    axis: str = "poolq_loo (LOO teammate mean perf z; self excluded)"

    def footer_text(self) -> str:
        seasons = f"{self.season_min}–{self.season_max}"
        pop = population_label(dft=self.population == "dft")
        y = y_draft_label(self.y_draft_mode)
        line = (
            f"{self.plot_family} · {self.axis} · {self.bin_label} · "
            f"{self.perf_metric.upper()} z · {seasons} · "
            f"min{self.min_minutes:g} mg{self.min_team_season_games} · {pop} · "
            f"Y={y} · {panel_rows_label(self.panel_rows)} · "
            f"winsor {self.winsor_lo:g}–{self.winsor_hi:g}"
        )
        if self.n_rows is not None and self.n_drafts is not None:
            line += f" · n={self.n_rows:,} PS · drafts={self.n_drafts:,}"
        return line

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FHeroProvenance:
    bin_slug: str
    bin_label: str
    perf_metric: str
    season_min: int
    season_max: int
    min_minutes: float
    min_team_season_games: int
    population: str
    y_draft_mode: str
    winsor_lo: float
    winsor_hi: float
    ai_band_label: str
    panel_rows: str = "all-ps"
    n_rows: int | None = None
    n_drafts: int | None = None
    plot_family: str = "F-HERO"
    axis: str = "T̂_j (team mean perf z; includes self — not poolq_loo)"

    def footer_text(self) -> str:
        seasons = f"{self.season_min}–{self.season_max}"
        pop = population_label(dft=self.population == "dft")
        y = y_draft_label(self.y_draft_mode)
        line = (
            f"{self.plot_family} · {self.axis} · {self.bin_label} · "
            f"Â band {self.ai_band_label} · {self.perf_metric.upper()} z · {seasons} · "
            f"min{self.min_minutes:g} mg{self.min_team_season_games} · {pop} · "
            f"Y={y} · {panel_rows_label(self.panel_rows)} · "
            f"winsor {self.winsor_lo:g}–{self.winsor_hi:g}"
        )
        if self.n_rows is not None and self.n_drafts is not None:
            line += f" · band n={self.n_rows:,} · drafts={self.n_drafts:,}"
        return line

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def stamp_figure_footer(fig, text: str, *, y: float = 0.008, fontsize: float = 7.5) -> None:
    fig.text(0.5, y, text, ha="center", va="bottom", fontsize=fontsize, color="0.35")


def write_provenance_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
