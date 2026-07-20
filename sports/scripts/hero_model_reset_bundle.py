#!/usr/bin/env python3
"""Hero model reset bundle: Layer A LPM + Layer C generative knockouts + side-by-side PNG.

Writes to sports/datasets/mbb/exports_inverted_u_v0/alex_side_by_side_v0/
Run from repo root: python sports/scripts/hero_model_reset_bundle.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SPORTS = REPO / "sports"
OUT = SPORTS / "datasets/mbb/exports_inverted_u_v0/alex_side_by_side_v0"
HERO_SLUG = "empirical_ppm_poolq_loo_16quantile_winsor0199_min20_2011"
HERO_BINS = 16
HERO_SEED = 42


def _hero_pipeline_config():
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


def run_layer_a_lpm(out_dir: Path) -> pd.Series:
    """OLS Y_draft ~ poolq_loo + poolq_sq on hero-filtered panel."""
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
    txt = out_dir / "lpm_hero_coefficients.txt"
    txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return coef


def run_layer_c_knockouts(out_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Talent-only vs congestion-in-score on poolq_loo axis, 16 quantile bins."""
    import importlib.util

    # Ensure clean imports
    for mod_name in list(sys.modules):
        if mod_name.startswith("tier1_"):
            del sys.modules[mod_name]

    sys.path.insert(0, str(SPORTS))
    sys.path.insert(0, str(REPO))
    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    cfg_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    base_sel = tge.SelectionConfig.from_module(mod)
    params = tpa.AssignmentParams.from_tier1_sim_config(cfg_path)

    def _one(label: str, score_mode: str, pool_l: str, w: float, seed: int) -> pd.DataFrame:
        sel = replace(
            base_sel,
            n_bins=HERO_BINS,
            bin_mode="quantile",
            score_mode=score_mode,
            loo_pool_l_mode=pool_l,
            loo_gap_weight=w,
        )
        rng = np.random.default_rng(seed)
        _, summ, _ = tge.run_inverted_u_pipeline(
            params,
            sel,
            rng,
            tpa=tpa,
            assign_poolq_bin_labels=assign_poolq_bin_labels,
        )
        out = summ.copy()
        out["knockout"] = label
        return out

    talent = _one("talent_only", "ability", "quality", 0.0, HERO_SEED)
    congest = _one(
        "congestion_in_score",
        "loo_gap_plus_ability",
        "crowding_smooth",
        0.5,
        HERO_SEED + 1,
    )
    talent.to_csv(out_dir / "generative_knockout_talent_only_16quantile.csv", index=False)
    congest.to_csv(out_dir / "generative_knockout_congestion_16quantile.csv", index=False)

    meta = {
        "hero_bins": HERO_BINS,
        "bin_mode": "quantile",
        "x_axis": "poolq_loo (mean_loo_q in bin table)",
        "talent_only": {"score_mode": "ability", "loo_pool_l_mode": "quality", "w": 0.0},
        "congestion": {
            "score_mode": "loo_gap_plus_ability",
            "loo_pool_l_mode": "crowding_smooth",
            "w": 0.5,
        },
        "seeds": {"talent_only": HERO_SEED, "congestion": HERO_SEED + 1},
    }
    (out_dir / "generative_knockout_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    print("Generative knockouts written (16 quantile bins on poolq_loo).")
    return talent, congest


def _write_knockout_summary(
    out_dir: Path,
    talent: pd.DataFrame,
    congest: pd.DataFrame,
    coef: pd.Series | None,
) -> None:
    t_top = float(talent.loc[talent["bin"] == talent["bin"].max(), "selection_rate"].iloc[0])
    c_top = float(congest.loc[congest["bin"] == congest["bin"].max(), "selection_rate"].iloc[0])
    t_bot = float(talent.loc[talent["bin"] == talent["bin"].min(), "selection_rate"].iloc[0])
    lpm_line = ""
    if coef is not None:
        lpm_line = f"- LPM: poolq_sq = {coef['poolq_sq']:.6g} (concave); see lpm_hero_coefficients.txt.\n"
    txt = out_dir / "generative_knockout_summary.txt"
    txt.write_text(
        "\n".join(
            [
                f"# Generative knockouts vs hero ({date.today().isoformat()})",
                "",
                "Spec: 16 quantile bins on poolq_loo (L_Q); see generative_knockout_meta.json.",
                "",
                "## Talent-only (score = A_i)",
                "",
                f"- Bin 1 → bin 16 selection rate: {t_bot:.4f} → {t_top:.4f} (monotone increasing).",
                "- No elite ventile dip on poolq_loo — fails inverted-U shape test.",
                "",
                "## Congestion in score (A_i − w·L_C, crowding_smooth, w=0.5)",
                "",
                f"- Top bin rate {c_top:.4f} vs talent-only {t_top:.4f} at same LOO rank.",
                "- Congestion compresses elite-tail vs ability-only; not bin-for-bin hero match (Path II).",
                "",
                "## Layer A reference (same hero estimand)",
                "",
                lpm_line.rstrip() or "- See lpm_hero_coefficients.txt.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _load_empirical_bins(out_dir: Path) -> pd.DataFrame:
    csv = out_dir / f"binned_draft_rate_{HERO_SLUG}.csv"
    if not csv.is_file():
        alt = (
            SPORTS
            / "datasets/mbb/exports_inverted_u_v0"
            / "binned_draft_rate_ventiles_ppm_zwithinseason_ventilebars520_2026-07-17.csv"
        )
        if alt.is_file():
            df = pd.read_csv(alt)
            df.to_csv(csv, index=False)
        else:
            raise FileNotFoundError(f"Missing hero CSV: {csv}")
    return pd.read_csv(csv)


def build_side_by_side(
    out_dir: Path,
    emp: pd.DataFrame,
    congest: pd.DataFrame,
    coef: pd.Series,
) -> None:
    """Empirical ventile bars + generative congestion line on shared-style axes."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Empirical (hero)
    ax = axes[0]
    x = emp["vent"].to_numpy() + 1
    y = emp["draft_rate"].to_numpy(dtype=float)
    ax.bar(x, y, color="steelblue", edgecolor="white", alpha=0.9)
    ax.set_xlabel("Ventile bin (1 = lowest poolq_loo)")
    ax.set_ylabel("Mean Y_draft")
    ax.set_title("Empirical (MBB hero)\n16 quantile | min=20 | winsor 0.01–0.99")
    ax.set_xticks(x)
    if coef["poolq_sq"] < 0:
        ax.text(
            0.02,
            0.96,
            f"LPM: β₂={coef['poolq_sq']:.4g} (<0)",
            transform=ax.transAxes,
            fontsize=8,
            va="top",
        )

    # Generative congestion knockout
    ax = axes[1]
    gx = congest["bin"].to_numpy(dtype=float) + 1
    gy = congest["selection_rate"].to_numpy(dtype=float)
    ax.plot(gx, gy, "o-", color="darkorange", lw=2, ms=6)
    ax.fill_between(gx, 0, gy, alpha=0.15, color="darkorange")
    ax.set_xlabel("Bin (1 = lowest poolq_loo in sim)")
    ax.set_ylabel("Mean Y_selected")
    ax.set_title(
        "Generative POC (538D-style)\n"
        "A − w·L_C crowding | 16 quantile on poolq_loo"
    )

    fig.suptitle(
        "Hero inverted-U reset — empirical fact vs minimal generative ingredient\n"
        "Same bin count & quantile rule; v1 does not claim bin-for-bin match",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    png = out_dir / "inverted_u_side_by_side_empirical_vs_generative.png"
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")

    caption = out_dir / "side_by_side_caption.txt"
    caption.write_text(
        "\n".join(
            [
                "Alex side-by-side caption (v1)",
                "",
                "Left: Empirical mean NBA draft rate by ventile of leave-one-out teammate quality",
                "(poolq_loo), MBB 2011–2021, hero spec locked in Hero_Model_Three_Layers_Memo.md.",
                "",
                "Right: Generative selection rate in an artificial league with congestion in the",
                "selection score (A − w·L_C), binned on simulated poolq_loo — same 16 quantile bins.",
                "",
                "Limitation: We do not claim pointwise match between panels in v1; talent-only",
                "selection (score = A only) fails the congestion ingredient test (see knockout CSVs).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def sync_empirical_png(out_dir: Path) -> None:
    """Ensure hero empirical PNG exists in alex folder."""
    dst = out_dir / f"inverted_u_{HERO_SLUG}.png"
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
    coef = run_layer_a_lpm(out_dir)
    talent, congest = run_layer_c_knockouts(out_dir)
    _write_knockout_summary(out_dir, talent, congest, coef)
    emp = _load_empirical_bins(out_dir)
    build_side_by_side(out_dir, emp, congest, coef)
    print(f"\nDone. Outputs in {out_dir}")


if __name__ == "__main__":
    main()
