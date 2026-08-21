#!/usr/bin/env python3
"""Pass A — Empirical MBB: talent-only read (left) vs roster-pressure hero (right).

==============================================================================
FOR LATER CHARLES — read this block first
==============================================================================
What this file is
  One-shot script that builds the empirical pair for Alex:
    Left  — mean draft rate by quantile bins of player ability (perf / ppm z)
    Right — mean draft rate by poolq_loo bins (locked hero spec by default)

What this file is NOT
  - Not generative sim (Pass B) — see pass_b_generative_knockout_bundle.py
  - Not ρ ablation (Pass C) — see pass_c_rho_ablation_bundle.py
  - Not the full 530 pipeline UI — this reuses panel_build on the locked estimand

Pass A claim
  Empirical contrast: talent alone tends monotone; peer/roster context (poolq_loo)
  shows inverted-U. No λ language on the empirical side.

Pipeline (real data — no sim ASSIGN/SCORE/SELECT)
  VISUALIZE only: bin MBB panel → plot mean Y_draft (ability ventiles | poolq_loo).

Run (repo root)
  python sports/scripts/pass_a_empirical_bundle.py
  python sports/scripts/pass_a_empirical_bundle.py --season-min 2013 --season-max 2021

  # Sensitivity / exploration (parallel filenames — does not clobber locked PNGs)
  python sports/scripts/pass_a_empirical_bundle.py --season-min 2013 --season-max 2021 \\
    --n-bins 20 --poolq-binning equal_width --output-tag ew20

Outputs (pass_a/)
  Full panel + locked defaults: legacy names without season tag.
  Other windows / non-default spec: tagged PNG/CSV/txt (parallel to PD20–22 campaign).

Spec
  sports/540_READ_ME_SIM.md
==============================================================================
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(SPORTS))

from gallery_knobs import HERO_BINS
from hero_gallery_paths import PASS_A, ensure_hero_dirs
from interval_overlap_paths import seasons_label, window_tag
from pd20_22_campaign_window import (
    FULL_PANEL_SEASON_MAX,
    FULL_PANEL_SEASON_MIN,
    activate_from_args,
    add_window_args,
    current_window,
)

DEFAULT_MIN_MINUTES = 20.0
DEFAULT_WINSOR_LO = 0.01
DEFAULT_WINSOR_HI = 0.99
DEFAULT_N_BINS = HERO_BINS
DEFAULT_POOLQ_BINNING = "quantile"

OUT = PASS_A

_spec: PassAHeroSpec | None = None


@dataclass(frozen=True)
class PassAHeroSpec:
    """Tunable Pass A hero / side-by-side figure spec."""

    n_bins: int = DEFAULT_N_BINS
    poolq_binning: str = DEFAULT_POOLQ_BINNING
    min_minutes: float = DEFAULT_MIN_MINUTES
    winsor_lo: float = DEFAULT_WINSOR_LO
    winsor_hi: float = DEFAULT_WINSOR_HI
    output_tag: str | None = None
    perf_metric: str = "ppm"

    @property
    def winsor_quantiles(self) -> tuple[float, float]:
        return (float(self.winsor_lo), float(self.winsor_hi))

    @property
    def bin_mode_slug(self) -> str:
        mode = "quantile" if self.poolq_binning == "quantile" else "equalwidth"
        return f"{int(self.n_bins)}{mode}"

    @property
    def winsor_slug(self) -> str:
        lo = int(round(self.winsor_lo * 100))
        hi = int(round(self.winsor_hi * 100))
        return f"winsor{lo:02d}{hi:02d}"

    @property
    def plot_spec_line(self) -> str:
        mode_label = "quantile" if self.poolq_binning == "quantile" else "equal width"
        return (
            rf"${self.n_bins}$ {mode_label} | min$={self.min_minutes:g}$ | "
            rf"winsor ${self.winsor_lo:g}$–${self.winsor_hi:g}$"
        )

    def is_locked_default(self) -> bool:
        return (
            int(self.n_bins) == DEFAULT_N_BINS
            and self.poolq_binning == DEFAULT_POOLQ_BINNING
            and float(self.min_minutes) == DEFAULT_MIN_MINUTES
            and float(self.winsor_lo) == DEFAULT_WINSOR_LO
            and float(self.winsor_hi) == DEFAULT_WINSOR_HI
            and not self.output_tag
            and str(self.perf_metric).strip().lower() == "ppm"
        )


def _hero_spec() -> PassAHeroSpec:
    if _spec is None:
        raise RuntimeError("PassAHeroSpec not initialized — call activate_hero_spec() first")
    return _spec


def activate_hero_spec(spec: PassAHeroSpec) -> None:
    global _spec
    _spec = spec


def _w():
    return current_window()


def _uses_legacy_names() -> bool:
    w = _w()
    return (
        w.season_min == FULL_PANEL_SEASON_MIN
        and w.season_max == FULL_PANEL_SEASON_MAX
        and _hero_spec().is_locked_default()
    )


def _name_parts() -> list[str]:
    """Suffix segments after PASS_A_* stem (excluding .png/.csv)."""
    spec = _hero_spec()
    parts: list[str] = []
    perf = str(spec.perf_metric).strip().lower()
    if perf != "ppm":
        parts.append(perf)
    if not spec.is_locked_default():
        parts.append(spec.bin_mode_slug)
        parts.append(spec.winsor_slug)
        parts.append(f"min{int(spec.min_minutes)}")
    w = _w()
    if w.season_min != FULL_PANEL_SEASON_MIN or w.season_max != FULL_PANEL_SEASON_MAX:
        parts.append(w.tag.lstrip("_"))
    if spec.output_tag:
        parts.append(spec.output_tag)
    return parts


def _tag_suffix() -> str:
    parts = _name_parts()
    return f"_{'_'.join(parts)}" if parts else ""


def _hero_slug() -> str:
    tag = window_tag(_w().season_min, _w().season_max)
    spec = _hero_spec()
    perf = str(spec.perf_metric).strip().lower()
    perf_part = f"{perf}_" if perf != "ppm" else "ppm_"
    return (
        f"empirical_{perf_part}poolq_loo_{spec.bin_mode_slug}_{spec.winsor_slug}_"
        f"min{int(spec.min_minutes)}_{tag.lstrip('_')}"
        f"{f'_{spec.output_tag}' if spec.output_tag else ''}"
    )


def _pass_a_png_name() -> str:
    if _uses_legacy_names():
        return "PASS_A_empirical_talent_vs_roster_side_by_side.png"
    return f"PASS_A_empirical_talent_vs_roster_side_by_side{_tag_suffix()}.png"


def _hero_png_name() -> str:
    return f"HERO_inverted_u_{_hero_slug()}.png"


def _roster_csv_name() -> str:
    return f"PASS_A_binned_draft_rate_{_hero_slug()}.csv"


def _ability_csv_name() -> str:
    if _uses_legacy_names():
        return "PASS_A_binned_draft_rate_ability_16quantile.csv"
    spec = _hero_spec()
    return f"PASS_A_binned_draft_rate_ability_{spec.n_bins}quantile{_tag_suffix()}.csv"


def _lpm_txt_name() -> str:
    if _uses_legacy_names():
        return "PASS_A_lpm_hero_coefficients.txt"
    return f"PASS_A_lpm_hero_coefficients{_tag_suffix()}.txt"


def _caption_txt_name() -> str:
    if _uses_legacy_names():
        return "PASS_A_side_by_side_caption.txt"
    return f"PASS_A_side_by_side_caption{_tag_suffix()}.txt"


def _hero_pipeline_config():
    """Layer A estimand from active PassAHeroSpec + campaign window."""
    from sports_pipeline.config import PipelineConfig

    w = _w()
    spec = _hero_spec()
    perf = str(spec.perf_metric).strip().lower()
    return PipelineConfig(
        perf_metric=[perf],
        perf_zscore_within_season=True,
        ventiles=int(spec.n_bins),
        poolq_binning=str(spec.poolq_binning),
        poolq_winsor_quantiles=spec.winsor_quantiles,
        min_minutes=float(spec.min_minutes),
        min_team_season_games=10,
        drop_dash_placeholder_names=True,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=int(w.season_min),
        panel_season_max=int(w.season_max),
        analysis_season_min=int(w.season_min),
        analysis_season_max=int(w.season_max),
    )


def _prepare_hero_panel():
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _hero_pipeline_config()
    panel = conductor.prepare_panel(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    use = panel_build.filter_panel(panel, cfg)
    return cfg, use


def ability_ventile_table(df: pd.DataFrame, n_bins: int) -> pd.DataFrame:
    """Bin ``perf`` (ability); within each bin, mean ``Y_draft`` (always quantile)."""
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    work = df.dropna(subset=["perf", "Y_draft"]).copy()
    work["vent"] = assign_poolq_bin_labels(work["perf"], n_bins, "quantile")
    return (
        work.dropna(subset=["vent"])
        .groupby("vent", observed=True)
        .agg(
            n=("Y_draft", "size"),
            draft_rate=("Y_draft", "mean"),
            perf_mean=("perf", "mean"),
            perf_median=("perf", "median"),
        )
        .reset_index()
        .sort_values("vent")
    )


def run_layer_a_lpm(out_dir: Path, use: pd.DataFrame) -> pd.Series:
    """Layer A: OLS Y_draft ~ poolq_loo + poolq_sq on hero-filtered panel."""
    from sports_pipeline import panel_build

    spec = _hero_spec()
    coef = panel_build.draft_poolq_quadratic_coeffs(use)
    seasons = seasons_label(_w().season_min, _w().season_max)
    lines = [
        f"# Hero Layer A — quadratic LPM ({date.today().isoformat()})",
        f"seasons={seasons} ({_w().season_min}–{_w().season_max})",
        f"n={len(use):,} player-seasons after hero filters",
        f"Y_draft=1 count: {int(use['Y_draft'].sum()):,}",
        f"n_bins={spec.n_bins} poolq_binning={spec.poolq_binning} perf_metric={spec.perf_metric}",
        f"min_minutes={spec.min_minutes} winsor={spec.winsor_lo}–{spec.winsor_hi}",
        *( [f"output_tag={spec.output_tag}"] if spec.output_tag else [] ),
        "",
        "Model: Y_draft ~ const + poolq_loo + poolq_sq",
        "",
        coef.to_string(),
        "",
        f"Interpretation: beta_poolq_sq = {coef['poolq_sq']:.6g} "
        f"({'concave / inverted-U consistent' if coef['poolq_sq'] < 0 else 'not concave — flat elite tail on POST-QC panel'})",
    ]
    txt = out_dir / _lpm_txt_name()
    txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return coef


def build_empirical_tables(out_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Ability ventiles (left) + poolq_loo ventiles (right) on the same filtered panel."""
    from sports_pipeline import panel_build

    spec = _hero_spec()
    cfg, use = _prepare_hero_panel()
    ability = ability_ventile_table(use, spec.n_bins)
    roster = panel_build.ventile_table(use, cfg)
    ability_path = out_dir / _ability_csv_name()
    roster_path = out_dir / _roster_csv_name()
    ability.to_csv(ability_path, index=False)
    roster.to_csv(roster_path, index=False)
    print(f"Wrote {ability_path.name} and {roster_path.name}")
    coef = run_layer_a_lpm(out_dir, use)
    return ability, roster, coef


def _lpm_annotation(coef: pd.Series) -> str | None:
    """On-figure LPM readout for roster-pressure panel."""
    b2 = float(coef["poolq_sq"])
    if b2 < 0:
        return rf"LPM: $\beta_2={b2:.4g}$ ($<0$, concave)"
    return rf"LPM: $\beta_2={b2:+.4g}$ (flat / not concave on this panel)"


def build_hero_single_panel(out_dir: Path, roster: pd.DataFrame, coef: pd.Series) -> None:
    """Standalone hero PNG (poolq_loo ventiles only)."""
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    spec = _hero_spec()
    seasons = seasons_label(_w().season_min, _w().season_max)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="steelblue", edgecolor="white", alpha=0.9)
    ax.set_xlabel(r"Ventile bin ($1$ = lowest $\mathrm{poolq\_loo}$)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(
        rf"Empirical hero — roster context · MBB {seasons}\n"
        rf"{spec.plot_spec_line} · POST-QC panel",
        fontsize=10,
    )
    ax.set_xticks(x)
    ax.grid(axis="y", alpha=0.25, linewidth=0.5)
    note = _lpm_annotation(coef)
    if note:
        ax.text(0.02, 0.96, note, transform=ax.transAxes, fontsize=8, va="top")
    fig.tight_layout()
    png = out_dir / _hero_png_name()
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")


def build_side_by_side(
    out_dir: Path,
    ability: pd.DataFrame,
    roster: pd.DataFrame,
    coef: pd.Series,
) -> None:
    """Left = talent (ability ventiles); right = roster pressure (poolq_loo hero)."""
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    spec = _hero_spec()
    perf = str(spec.perf_metric).strip().upper()
    seasons = seasons_label(_w().season_min, _w().season_max)
    left_spec = (
        rf"${spec.n_bins}$ quantile | min$={spec.min_minutes:g}$ | "
        rf"winsor ${spec.winsor_lo:g}$–${spec.winsor_hi:g}$ | perf={perf}"
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    ax = axes[0]
    x = ability["vent"].to_numpy(dtype=float) + 1
    y = ability["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="seagreen", edgecolor="white", alpha=0.9)
    ax.set_xlabel(rf"Ability ventile ($1$ = lowest perf, {perf} $z$ within season)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(f"Empirical — talent alone\n{left_spec}")
    ax.set_xticks(x)

    ax = axes[1]
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="steelblue", edgecolor="white", alpha=0.9)
    ax.set_xlabel(r"Ventile bin ($1$ = lowest $\mathrm{poolq\_loo}$)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(
        f"Empirical — roster context (hero)\n"
        f"{spec.plot_spec_line} · middle rise; flat elite tail"
    )
    ax.set_xticks(x)
    note = _lpm_annotation(coef)
    if note:
        ax.text(0.02, 0.96, note, transform=ax.transAxes, fontsize=8, va="top")

    fig.suptitle(
        f"Pass A — Empirical MBB: talent vs roster context · {seasons} · POST-QC panel\n"
        r"Qualitative shapes only; generative inverted-U is Pass B/C (not bin-for-bin match)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    png = out_dir / _pass_a_png_name()
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")

    caption = out_dir / _caption_txt_name()
    caption.write_text(
        "\n".join(
            [
                "Pass A caption — empirical pair",
                "",
                f"Spec: n_bins={spec.n_bins} poolq_binning={spec.poolq_binning} "
                f"min_minutes={spec.min_minutes} winsor={spec.winsor_lo}–{spec.winsor_hi} "
                f"perf_metric={spec.perf_metric}",
                *( [f"output_tag={spec.output_tag}"] if spec.output_tag else [] ),
                "",
                "Left: Mean NBA draft rate by ventile of player ability (perf z-scored",
                "within season). Monotone-up is the talent-only stylized read.",
                "",
                "Right: Mean NBA draft rate by ventile of leave-one-out teammate quality",
                f"(poolq_loo), MBB {seasons}, POST-QC panel (mg>=10, drop sub-20).",
                "Middle rise is the stylized fact; elite tail is flat on this panel.",
                "July pre-QC inverted-U tail: pass_a/sensitivity/ (not canonical).",
                "",
                "We do not use λ language on the empirical side; λ is a generative score knob (Pass B).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _sanitize_output_tag(raw: str | None) -> str | None:
    if raw is None or raw == "":
        return None
    tag = re.sub(r"[^A-Za-z0-9_-]+", "_", raw.strip()).strip("_")
    if not tag:
        raise ValueError(f"Invalid --output-tag {raw!r} (empty after sanitization)")
    return tag


def add_hero_spec_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--n-bins",
        type=int,
        default=None,
        help=f"Poolq_loo + ability bin count (default: GALLERY_HERO_BINS or {DEFAULT_N_BINS}).",
    )
    parser.add_argument(
        "--poolq-binning",
        choices=("quantile", "equal_width"),
        default=DEFAULT_POOLQ_BINNING,
        help="Right-panel poolq_loo binning (left ability panel always quantile).",
    )
    parser.add_argument(
        "--min-minutes",
        type=float,
        default=DEFAULT_MIN_MINUTES,
        help=f"Playing-time floor (default: {DEFAULT_MIN_MINUTES:g}).",
    )
    parser.add_argument(
        "--winsor-lo",
        type=float,
        default=DEFAULT_WINSOR_LO,
        help=f"Lower poolq winsor quantile (default: {DEFAULT_WINSOR_LO}).",
    )
    parser.add_argument(
        "--winsor-hi",
        type=float,
        default=DEFAULT_WINSOR_HI,
        help=f"Upper poolq winsor quantile (default: {DEFAULT_WINSOR_HI}).",
    )
    parser.add_argument(
        "--output-tag",
        type=str,
        default=None,
        help=(
            "Extra filename tag for exploration runs (e.g. ew20). "
            "Non-default spec also embeds bin mode in filenames."
        ),
    )
    parser.add_argument(
        "--perf-metric",
        type=str,
        default="ppm",
        choices=("ppm", "obpm", "opm", "bpm", "dbpm", "dpm"),
        help="Own-ability + LOO teammate perf source (default ppm). SR merge required for obpm/bpm.",
    )


def hero_spec_from_args(args: argparse.Namespace) -> PassAHeroSpec:
    n_bins = DEFAULT_N_BINS if args.n_bins is None else int(args.n_bins)
    if n_bins < 2:
        raise SystemExit("--n-bins must be >= 2")
    winsor_lo = float(args.winsor_lo)
    winsor_hi = float(args.winsor_hi)
    if not (0.0 <= winsor_lo < winsor_hi <= 1.0):
        raise SystemExit("--winsor-lo and --winsor-hi must satisfy 0 <= lo < hi <= 1")
    return PassAHeroSpec(
        n_bins=n_bins,
        poolq_binning=str(args.poolq_binning),
        min_minutes=float(args.min_minutes),
        winsor_lo=winsor_lo,
        winsor_hi=winsor_hi,
        output_tag=_sanitize_output_tag(args.output_tag),
        perf_metric=str(args.perf_metric).strip().lower(),
    )


def _resolve_out_dir() -> Path:
    """Non-PPM robustness runs go under pass_a/sensitivity/ (Track C)."""
    spec = _hero_spec()
    if str(spec.perf_metric).strip().lower() == "ppm" and spec.is_locked_default():
        return OUT
    sens = OUT / "sensitivity"
    sens.mkdir(parents=True, exist_ok=True)
    return sens


def main() -> None:
    parser = argparse.ArgumentParser(description="Pass A empirical hero + side-by-side PNGs.")
    add_window_args(parser)
    add_hero_spec_args(parser)
    args = parser.parse_args()
    activate_from_args(args)
    spec = hero_spec_from_args(args)
    activate_hero_spec(spec)

    out_dir = _resolve_out_dir()
    ensure_hero_dirs()
    out_dir.mkdir(parents=True, exist_ok=True)
    seasons = seasons_label(_w().season_min, _w().season_max)
    print(
        f"Pass A · seasons {seasons} ({_w().season_min}–{_w().season_max}) · "
        f"perf={spec.perf_metric} · "
        f"{spec.n_bins} {spec.poolq_binning} min={spec.min_minutes:g} "
        f"winsor={spec.winsor_lo}–{spec.winsor_hi}"
        + (f" tag={spec.output_tag}" if spec.output_tag else "")
        + (f" · out={out_dir.relative_to(REPO)}" if out_dir != OUT else ""),
        flush=True,
    )
    ability, roster, coef = build_empirical_tables(out_dir)
    build_hero_single_panel(out_dir, roster, coef)
    build_side_by_side(out_dir, ability, roster, coef)
    print(f"\nDone. Side-by-side: {out_dir / _pass_a_png_name()}")


if __name__ == "__main__":
    main()
