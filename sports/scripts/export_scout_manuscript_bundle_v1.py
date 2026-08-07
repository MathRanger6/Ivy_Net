#!/usr/bin/env python3
"""SCOUT D10 — freeze manuscript export bundle for VECTOR §3 (Path II).

Output: datasets/mbb/exports_inverted_u_v0/scout_manuscript_v1/

Charles lock Q-SCOUT-9 / Q-D10 = go (2026-06-24).
Packaging only — no new science.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

REPO = Path(__file__).resolve().parents[2]
SPORTS = REPO / "sports"
SRC_EXPORTS = REPO / "datasets" / "mbb" / "exports_inverted_u_v0"
OUT = SRC_EXPORTS / "scout_manuscript_v1"
DATE_SLUG = datetime.now(timezone.utc).strftime("%Y-%m-%d")

EMPIRICAL_PNG_SRC = SRC_EXPORTS / "inverted_u_ventiles_ppm_zwithinseason_2026-04-06.png"
EMPIRICAL_CSV_SRC = SRC_EXPORTS / "binned_draft_rate_ventiles_ppm_zwithinseason_2026-04-06.csv"
HET_PNG = SRC_EXPORTS / "heterogeneity_ventiles_top_tail.png"
HET_CSV = SRC_EXPORTS / "heterogeneity_ventiles_top_tail.csv"
STATE_PATH = SPORTS / "tier1_cell10_playground_state.json"


def _git_head() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=REPO,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def _load_cfg():
    spec = importlib.util.spec_from_file_location(
        "tier1_sim_config", SPORTS / "tier1_sim_config.py"
    )
    cfg = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(cfg)
    return cfg


def _import_generative_stack():
    if str(SPORTS) not in sys.path:
        sys.path.insert(0, str(SPORTS))
    if str(REPO) not in sys.path:
        sys.path.insert(0, str(REPO))
    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    return tge, tpa, assign_poolq_bin_labels


def _run_generative_figure(
    *,
    label: str,
    score_mode: str,
    loo_gap_weight: float,
    loo_pool_l_mode: str,
    team_mean_axis: bool,
    state: dict,
    out_png: Path,
    out_csv: Path,
) -> dict:
    import numpy as np
    import matplotlib.pyplot as plt

    tge, tpa, assign_poolq_bin_labels = _import_generative_stack()
    from hero_seed import HERO_SEED
    cfg = _load_cfg()
    base_sel = tge.SelectionConfig.from_module(cfg)
    sel = tge.SelectionConfig.from_state(state, base_sel)
    sel = tge.SelectionConfig(
        n_bins=sel.n_bins,
        bin_mode=sel.bin_mode,
        n_selected=sel.n_selected,
        score_mode=score_mode,
        loo_gap_weight=loo_gap_weight,
        winner_selection=sel.winner_selection,
        loo_pool_l_mode=loo_pool_l_mode,
    )
    params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
    rng = np.random.default_rng(int(state.get("seed", HERO_SEED)))
    players, _, _ = tpa.simulate_generative_rosters(params, rng=rng, method="soft")
    players = tpa.assign_selection(
        players,
        rng,
        n_selected=sel.n_selected,
        score_mode=sel.score_mode,
        loo_gap_weight=sel.loo_gap_weight,
        winner_selection=sel.winner_selection,
        pool_l_mode=sel.loo_pool_l_mode,
        viability_theta=params.viability_theta,
        viability_sharpness=params.viability_sharpness,
    )
    if team_mean_axis:
        summ = tge.inverted_u_bin_table_team_mean(
            players, sel, assign_poolq_bin_labels=assign_poolq_bin_labels
        )
        x_col = "mean_team_mean"
        xlabel = tge.PLOT_B_XAXIS_TEAM_MEAN_LABEL
    else:
        summ = tge.inverted_u_bin_table(
            players, sel, assign_poolq_bin_labels=assign_poolq_bin_labels, tpa=tpa
        )
        x_col = "mean_loo_q"
        xlabel = tge.PLOT_B_XAXIS_LABEL

    fig = tge.figure_inverted_u(
        summ,
        title=tge.plot_b_figure_title(
            sel,
            header=f"D10 generative — {label}",
            team_mean_axis=team_mean_axis,
            tpa=tpa,
        ),
        n_bins=sel.n_bins,
        n_teams=params.n_teams,
        loo_pool_l_mode=sel.loo_pool_l_mode,
        x_col=x_col,
        xlabel=xlabel,
        tpa=tpa,
    )
    fig.savefig(out_png, dpi=120, bbox_inches="tight")
    plt.close(fig)
    summ.to_csv(out_csv, index=False)
    return {
        "label": label,
        "score_mode": score_mode,
        "loo_gap_weight": loo_gap_weight,
        "loo_pool_l_mode": loo_pool_l_mode,
        "team_mean_axis": team_mean_axis,
        "png": out_png.name,
        "csv": out_csv.name,
        "max_selection_rate": float(summ["selection_rate"].max()),
        "min_selection_rate": float(summ["selection_rate"].min()),
    }


def _write_axis_table(out: Path) -> None:
    md = """# Axis table — generative readouts vs empirical quantities (v1)

**Bundle:** SCOUT D10 · Path II · Charles Tier 1 locks 2026-06-24

| Setting | Rung | Model / empirical quantity | Column / object | Axis or outcome | v1 claim |
|---------|------|--------------------------|-----------------|-----------------|----------|
| Basketball | 1 | Empirical LOO pool quality | `poolq_loo` | Binned draft rate vs LOO mean teammate perf | Inverted-U stylized fact |
| Basketball | 2.5 | Team quality vs congestion | `poolq_loo` vs `crowding_smooth` | Separate measurement columns | PD12 P3 model-guided features |
| Basketball | 2 | Generative selection score | S = A - lambda L_C_LOO | Pool **mean** axis (539 preset) | Qualitative peak-and-decline POC |
| Basketball | 2 | Ability-only null | score_mode=ability, w=0 | Pool mean axis | Monotone — fails without congestion |
| Basketball | 2 | Same score, LOO quality readout | poolq_loo bins | LOO pool quality axis | Mostly decreasing — honest limitation |
| Basketball | 3 | Near-threshold heterogeneity | CELL 4D ventiles | Own-perf slice x pool quality | Prediction #1 readout |
| Army | 1 | LOO pool minus mean | pool_minus_mean | CIF / Cox panels | Empirical inverted-U anchor |
| Army | 3 | Peak shift with Lambda | pool size | Promotion hazard | Prediction #2 prose hook |
| Tenure | 1 | LOO dept peer quality | poolq_loo_mean | Stage 9 binned tenure rate | Preliminary Setting 3 |

**Do not claim:** generative bin-for-bin LOO match; full B(Q)-D(Q) estimation; 3-domain parametric identifiability.
"""
    out.write_text(md, encoding="utf-8")
    csv_lines = [
        "setting,rung,quantity,column,axis,v1_claim",
        "basketball,1,empirical_loo_pool_quality,poolq_loo,binned_draft_rate,inverted_u",
        "basketball,2.5,quality_vs_congestion,poolq_loo;crowding_smooth,columns,pd12_p3",
        "basketball,2,generative_score,S=A-lambda*L_C,pool_mean,poc",
        "basketball,2,ability_only,score_mode=ability,pool_mean,null_fail",
        "basketball,3,near_threshold,cell_4d,heterogeneity,prediction_1",
        "army,1,loo_pool_minus_mean,pool_minus_mean,cif,anchor",
        "tenure,1,loo_dept_quality,poolq_loo_mean,stage9,preliminary",
    ]
    (out.parent / "axis_table_generative_readouts.csv").write_text(
        "\n".join(csv_lines) + "\n", encoding="utf-8"
    )


def _write_score_one_pager(out: Path, state: dict) -> None:
    cfg = _load_cfg()
    lam = state.get("loo_gap_weight", getattr(cfg, "SELECTION_539_LOO_GAP_WEIGHT", 0.55))
    theta = state.get("viability_theta", getattr(cfg, "SELECTION_539_VIABILITY_THETA", 0.72))
    gamma = state.get(
        "viability_sharpness", getattr(cfg, "SELECTION_539_VIABILITY_SHARPNESS", 10.0)
    )
    text = f"""# Selection score one-pager (v1 frozen preset)

**Date frozen:** {DATE_SLUG}
**Source state:** sports/tier1_cell10_playground_state.json
**Config:** sports/tier1_sim_config.py (SELECTION_539_*)

## Score (constraint leg D in selection)

S_i = A_i - lambda * L_C,LOO,i

- A_i — latent ability (539 preset: Beta(2,2) on [0,1])
- L_C,LOO — LOO viable-peer congestion (crowding_smooth)
- lambda = {lam}
- Viability theta = {theta}; sharpness gamma = {gamma}

## Selection rule

- Soft assignment (tau ~ {state.get('tau', 0.65)})
- Top-K by score (winner_selection = {state.get('winner_selection', 'C')})
- Ability-only null: score_mode=ability, w=0

## Ontology

Alex score = D-leg in L_net = B - D. Not a second model.

## Honest limitation

POC on pool mean; empirical fact on LOO pool quality. No bin-for-bin LOO claim.

See 5-Manuscript/Model_Nesting_Note_v1.md.
"""
    out.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

    emp_png = OUT / f"inverted_u_ventiles_ppm_zwithinseason_{DATE_SLUG}.png"
    emp_csv = OUT / f"binned_draft_rate_ventiles_ppm_zwithinseason_{DATE_SLUG}.csv"
    if EMPIRICAL_PNG_SRC.is_file():
        shutil.copy2(EMPIRICAL_PNG_SRC, emp_png)
    if EMPIRICAL_CSV_SRC.is_file():
        shutil.copy2(EMPIRICAL_CSV_SRC, emp_csv)
    if HET_PNG.is_file():
        shutil.copy2(HET_PNG, OUT / "heterogeneity_ventiles_top_tail.png")
    if HET_CSV.is_file():
        shutil.copy2(HET_CSV, OUT / "heterogeneity_ventiles_top_tail.csv")

    gen_runs = [
        _run_generative_figure(
            label="ability_only_null",
            score_mode="ability",
            loo_gap_weight=0.0,
            loo_pool_l_mode="quality",
            team_mean_axis=True,
            state=state,
            out_png=OUT / "generative_ability_only_pool_mean.png",
            out_csv=OUT / "generative_ability_only_pool_mean.csv",
        ),
        _run_generative_figure(
            label="congestion_539_pool_mean",
            score_mode=str(state.get("score_mode", "loo_gap_plus_ability")),
            loo_gap_weight=float(state.get("loo_gap_weight", 0.55)),
            loo_pool_l_mode=str(state.get("loo_pool_l_mode", "crowding_smooth")),
            team_mean_axis=True,
            state=state,
            out_png=OUT / "generative_congestion_539_pool_mean.png",
            out_csv=OUT / "generative_congestion_539_pool_mean.csv",
        ),
        _run_generative_figure(
            label="congestion_539_loo_quality",
            score_mode=str(state.get("score_mode", "loo_gap_plus_ability")),
            loo_gap_weight=float(state.get("loo_gap_weight", 0.55)),
            loo_pool_l_mode=str(state.get("loo_pool_l_mode", "crowding_smooth")),
            team_mean_axis=False,
            state=state,
            out_png=OUT / "generative_congestion_539_loo_quality.png",
            out_csv=OUT / "generative_congestion_539_loo_quality.csv",
        ),
    ]

    _write_axis_table(OUT / "axis_table_generative_readouts.md")
    _write_score_one_pager(OUT / "score_equation_one_pager.md", state)

    manifest = {
        "bundle": "scout_manuscript_v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "date_slug": DATE_SLUG,
        "git_head": _git_head(),
        "charles_locks": "20260611_Charles_Tier1_locks.md",
        "playground_state": "sports/tier1_cell10_playground_state.json",
        "empirical_figure_2": {"png": emp_png.name, "csv": emp_csv.name},
        "generative_runs": gen_runs,
        "tier_2_5": {
            "quality_column": "poolq_loo",
            "congestion_column": "crowding_smooth",
            "heterogeneity": "heterogeneity_ventiles_top_tail.png",
        },
    }
    (OUT / "MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"D10 bundle written to {OUT}")


if __name__ == "__main__":
    main()
