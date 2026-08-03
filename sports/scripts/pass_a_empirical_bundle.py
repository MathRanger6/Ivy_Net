#!/usr/bin/env python3
"""Pass A — Empirical MBB: talent-only read (left) vs roster-pressure hero (right).

==============================================================================
FOR LATER CHARLES — read this block first
==============================================================================
What this file is
  One-shot script that builds the empirical pair for Alex:
    Left  — mean draft rate by 16 quantile bins of player ability (perf / ppm z)
    Right — mean draft rate by 16 quantile bins of poolq_loo (locked hero spec)

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

Outputs (only)
  3-Master_Plan/re_entry/HEROs_and_PASSes/PASS_A_*  (+ HERO_* PNG if synced)

Spec
  sports/540_READ_ME_SIM.md
==============================================================================
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
from gallery_knobs import HERO_BINS
OUT = REPO / "3-Master_Plan" / "re_entry" / "HEROs_and_PASSes"
PASS_A_PNG_NAME = "PASS_A_empirical_talent_vs_roster_side_by_side.png"
HERO_SLUG = "empirical_ppm_poolq_loo_16quantile_winsor0199_min20_2011"
HERO_PNG_NAME = f"HERO_inverted_u_{HERO_SLUG}.png"
PASS_A_ROSTER_CSV = f"PASS_A_binned_draft_rate_{HERO_SLUG}.csv"
PASS_A_ABILITY_CSV = "PASS_A_binned_draft_rate_ability_16quantile.csv"


def _hero_pipeline_config():
    """Locked Layer A estimand (same filters as the hero PNG / memo)."""
    sys.path.insert(0, str(SPORTS))
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=HERO_BINS,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=20,
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=2011,
        panel_season_max=2021,
        analysis_season_min=2011,
        analysis_season_max=2021,
    )


def _prepare_hero_panel():
    sys.path.insert(0, str(SPORTS))
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
    """Bin ``perf`` (ability); within each bin, mean ``Y_draft``."""
    sys.path.insert(0, str(SPORTS))
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
    sys.path.insert(0, str(SPORTS))
    from sports_pipeline import panel_build

    coef = panel_build.draft_poolq_quadratic_coeffs(use)
    lines = [
        f"# Hero Layer A — quadratic LPM ({date.today().isoformat()})",
        f"n={len(use):,} player-seasons after hero filters",
        f"Y_draft=1 count: {int(use['Y_draft'].sum()):,}",
        "",
        "Model: Y_draft ~ const + poolq_loo + poolq_sq",
        "",
        coef.to_string(),
        "",
        f"Interpretation: beta_poolq_sq = {coef['poolq_sq']:.6g} "
        f"({'concave / inverted-U consistent' if coef['poolq_sq'] < 0 else 'NOT concave — investigate'})",
    ]
    txt = out_dir / "PASS_A_lpm_hero_coefficients.txt"
    txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return coef


def build_empirical_tables(out_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    """Ability ventiles (left) + poolq_loo ventiles (right) on the same filtered panel."""
    sys.path.insert(0, str(SPORTS))
    from sports_pipeline import panel_build

    cfg, use = _prepare_hero_panel()
    ability = ability_ventile_table(use, HERO_BINS)
    roster = panel_build.ventile_table(use, cfg)
    ability.to_csv(out_dir / PASS_A_ABILITY_CSV, index=False)
    roster.to_csv(out_dir / PASS_A_ROSTER_CSV, index=False)
    print(f"Wrote {PASS_A_ABILITY_CSV} and {PASS_A_ROSTER_CSV}")
    coef = run_layer_a_lpm(out_dir, use)
    return ability, roster, coef


def _load_roster_bins(out_dir: Path) -> pd.DataFrame:
    """Load roster ventiles; rebuild from panel if missing."""
    csv = out_dir / PASS_A_ROSTER_CSV
    if csv.is_file():
        return pd.read_csv(csv)
    alt = (
        SPORTS
        / "datasets/mbb/exports_inverted_u_v0"
        / "binned_draft_rate_ventiles_ppm_zwithinseason_ventilebars520_2026-07-17.csv"
    )
    if alt.is_file():
        df = pd.read_csv(alt)
        df.to_csv(csv, index=False)
        return df
    raise FileNotFoundError(f"Missing roster CSV: {csv}")


def build_side_by_side(
    out_dir: Path,
    ability: pd.DataFrame,
    roster: pd.DataFrame,
    coef: pd.Series,
) -> None:
    """Left = talent (ability ventiles); right = roster pressure (poolq_loo hero)."""
    sys.path.insert(0, str(SCRIPTS))
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    ax = axes[0]
    x = ability["vent"].to_numpy(dtype=float) + 1
    y = ability["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="seagreen", edgecolor="white", alpha=0.9)
    ax.set_xlabel(r"Ability ventile ($1$ = lowest perf, ppm $z$ within season)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(
        "Empirical — talent alone\n"
        r"$16$ quantile | min$=20$ | winsor $0.01$–$0.99$"
    )
    ax.set_xticks(x)

    ax = axes[1]
    x = roster["vent"].to_numpy(dtype=float) + 1
    y = roster["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="steelblue", edgecolor="white", alpha=0.9)
    ax.set_xlabel(r"Ventile bin ($1$ = lowest $\mathrm{poolq\_loo}$)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{draft}}$")
    ax.set_title(
        "Empirical — roster pressure (hero)\n"
        r"$16$ quantile | min$=20$ | winsor $0.01$–$0.99$"
    )
    ax.set_xticks(x)
    if coef["poolq_sq"] < 0:
        ax.text(
            0.02,
            0.96,
            rf"LPM: $\beta_2={coef['poolq_sq']:.4g}$ ($<0$)",
            transform=ax.transAxes,
            fontsize=8,
            va="top",
        )

    fig.suptitle(
        "Pass A — Empirical MBB: talent read vs roster-pressure read\n"
        r"Qualitative shapes only; no bin-for-bin claim to generative sim",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    png = out_dir / PASS_A_PNG_NAME
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")

    caption = out_dir / "PASS_A_side_by_side_caption.txt"
    caption.write_text(
        "\n".join(
            [
                "Pass A caption — empirical pair",
                "",
                "Left: Mean NBA draft rate by ventile of player ability (ppm z-scored",
                "within season). Monotone-up is the talent-only stylized read.",
                "",
                "Right: Mean NBA draft rate by ventile of leave-one-out teammate quality",
                "(poolq_loo), MBB 2011–2021, hero spec locked in Hero_Model_Three_Layers_Memo.md.",
                "",
                "We do not use λ language on the empirical side; λ is a generative score knob (Pass B).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def sync_empirical_png(out_dir: Path) -> None:
    """Ensure standalone HERO_* PNG exists in the gallery (copy if missing)."""
    dst = out_dir / HERO_PNG_NAME
    if dst.is_file():
        return
    src = (
        SPORTS
        / "datasets/mbb/exports_inverted_u_v0"
        / "inverted_u_ventiles_ppm_zwithinseason_ventilebars520_2026-07-17.png"
    )
    if src.is_file():
        dst.write_bytes(src.read_bytes())
        print(f"Copied empirical hero PNG → {dst}")


def main() -> None:
    out_dir = OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    sync_empirical_png(out_dir)
    ability, roster, coef = build_empirical_tables(out_dir)
    build_side_by_side(out_dir, ability, roster, coef)
    print(f"\nDone. Outputs in {out_dir}")


if __name__ == "__main__":
    main()
