#!/usr/bin/env python3
"""Pass B — Generative λ knockout: talent-only score (left) vs congestion in score (right).

==============================================================================
FOR LATER CHARLES — read this block first
==============================================================================
What this file is
  One-shot script that runs two generative leagues differing ONLY in SCORE:
    Left  — S_i = A_i (λ = 0; roster pressure out of score)
    Right — S_i = A_i − w·L_C (congestion in score)
  Same assign → score → select pipeline; step 4 VISUALIZE uses **pool mean**
  (team mean ability, including self — NOT poolq_loo).

Four steps (generative passes B/C)
  (1) ASSIGN  (2) SCORE  (3) SELECT  (4) VISUALIZE — bin + plot readout.

Presets (PRESET knob below)
  "539" — Beta(2,2) A on [0,1], w=0.55, θ/γ from SELECTION_539_* (SCOUT D10).
          Stronger inverted-U on pool-mean readout.
  "540" — tier1_sim_config defaults (normal_clipped A, w=0.5).

What this file is NOT
  - Not empirical MBB (Pass A) — see pass_a_empirical_bundle.py
  - Not ρ ablation (Pass C) — see pass_c_rho_ablation_bundle.py

Run (repo root)
  python sports/scripts/pass_b_generative_knockout_bundle.py

Outputs
  3-Master_Plan/re_entry/HEROs_and_PASSes/pass_b/PASS_B_*
  (+ PASS_B_D10_* reference copies from scout_manuscript_v1 when present)

Spec
  sports/540_READ_ME_SIM.md
==============================================================================
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SCRIPTS))
from gallery_knobs import HERO_BINS, HERO_SEED, PRESET
from hero_gallery_paths import PASS_B, ensure_hero_dirs

OUT = PASS_B
D10_DIR = REPO / "datasets" / "mbb" / "exports_inverted_u_v0" / "scout_manuscript_v1"
D10_EXPORT_SCRIPT = SPORTS / "scripts" / "export_scout_manuscript_bundle_v1.py"
PASS_B_PNG_NAME = "PASS_B_generative_lambda_knockout_side_by_side.png"
PASS_B_D10_PNG_NAME = "PASS_B_D10_reference_lambda_knockout_pool_mean.png"
BIN_AXIS = "pool_mean"


def _load_cfg_module():
    import importlib.util

    cfg_path = SPORTS / "tier1_sim_config.py"
    spec = importlib.util.spec_from_file_location("tier1_sim_config", cfg_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod, cfg_path


def _539_playground_state(mod) -> dict:
    """539 selection layer on [0,1] scales — matches SELECTION_539_* / D10 bundle."""
    return {
        "ability_draw": str(getattr(mod, "SELECTION_539_ABILITY_DRAW", "beta_2_2")),
        "target_dist": "uniform",
        "t_low": float(getattr(mod, "SELECTION_539_TARGET_MEAN_LOW", 0.0)),
        "t_high": float(getattr(mod, "SELECTION_539_TARGET_MEAN_HIGH", 1.0)),
        "viability_theta": float(getattr(mod, "SELECTION_539_VIABILITY_THETA", 0.72)),
        "viability_sharpness": float(
            getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0)
        ),
        "n_bins": HERO_BINS,
        "n_selected": int(getattr(mod, "N_SELECTED", 1500)),
        "winner_selection": str(getattr(mod, "SELECTION_539_WINNER_SELECTION", "C")),
    }


def _congestion_w(mod) -> float:
    if PRESET == "539":
        return float(getattr(mod, "SELECTION_539_LOO_GAP_WEIGHT", 0.55))
    return 0.5


def _load_engines():
    for mod_name in list(sys.modules):
        if mod_name.startswith("tier1_"):
            del sys.modules[mod_name]
    sys.path.insert(0, str(SPORTS))
    sys.path.insert(0, str(REPO))
    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    return tge, tpa, assign_poolq_bin_labels


def run_knockouts(out_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Two score modes; bin readout on team pool mean (not poolq_loo)."""
    mod, cfg_path = _load_cfg_module()
    tge, tpa, assign_poolq_bin_labels = _load_engines()
    base_sel = tge.SelectionConfig.from_module(mod)
    w_congest = _congestion_w(mod)

    if PRESET == "539":
        state = _539_playground_state(mod)
        params = tge.assignment_params_from_state(SPORTS, state, tpa=tpa)
        base_sel = replace(
            base_sel,
            n_bins=HERO_BINS,
            n_selected=int(state.get("n_selected", base_sel.n_selected)),
            winner_selection=str(state.get("winner_selection", base_sel.winner_selection)),
        )
    else:
        params = tpa.AssignmentParams.from_tier1_sim_config(cfg_path)
        state = {}

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
        summ = tge.inverted_u_bin_table_team_mean(
            players, sel, assign_poolq_bin_labels=assign_poolq_bin_labels
        )
        out = summ.copy()
        out["knockout"] = label
        return out

    talent = _one("talent_only", "ability", "quality", 0.0, HERO_SEED)
    congest = _one(
        "congestion_in_score",
        "loo_gap_plus_ability",
        "crowding_smooth",
        w_congest,
        HERO_SEED + 1,
    )
    talent.to_csv(
        out_dir / "PASS_B_generative_knockout_talent_only_16quantile_poolmean.csv",
        index=False,
    )
    congest.to_csv(
        out_dir / "PASS_B_generative_knockout_congestion_16quantile_poolmean.csv",
        index=False,
    )

    meta = {
        "pass": "B",
        "preset": PRESET,
        "hero_bins": HERO_BINS,
        "bin_mode": "quantile",
        "x_axis": BIN_AXIS,
        "x_axis_note": "team mean ability on realized roster (includes self; not LOO)",
        "talent_only": {"score_mode": "ability", "loo_pool_l_mode": "quality", "w": 0.0},
        "congestion": {
            "score_mode": "loo_gap_plus_ability",
            "loo_pool_l_mode": "crowding_smooth",
            "w": w_congest,
        },
        "assignment": {
            "ability_draw": params.ability_draw,
            "viability_theta": params.viability_theta,
            "viability_sharpness": params.viability_sharpness,
            "target_mean_low": params.target_mean_low,
            "target_mean_high": params.target_mean_high,
        },
        "seeds": {"talent_only": HERO_SEED, "congestion": HERO_SEED + 1},
        "playground_state_overlay": state if PRESET == "539" else None,
    }
    (out_dir / "PASS_B_generative_knockout_meta.json").write_text(
        json.dumps(meta, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Generative knockouts written ({PRESET} preset, 16 quantile bins on pool mean).")
    return talent, congest, meta


def _write_summary(
    out_dir: Path,
    talent: pd.DataFrame,
    congest: pd.DataFrame,
    meta: dict,
) -> None:
    w = meta["congestion"]["w"]
    t_top = float(talent.loc[talent["bin"] == talent["bin"].max(), "selection_rate"].iloc[0])
    c_top = float(congest.loc[congest["bin"] == congest["bin"].max(), "selection_rate"].iloc[0])
    c_peak = float(congest["selection_rate"].max())
    t_bot = float(talent.loc[talent["bin"] == talent["bin"].min(), "selection_rate"].iloc[0])
    txt = out_dir / "PASS_B_generative_knockout_summary.txt"
    txt.write_text(
        "\n".join(
            [
                f"# Pass B — generative λ knockout ({date.today().isoformat()})",
                "",
                f"Preset: {PRESET}. 16 quantile bins on pool mean (not poolq_loo).",
                "See PASS_B_generative_knockout_meta.json.",
                "",
                "## Left arm — talent-only (score $= A_i$, λ = 0)",
                "",
                f"- Bin 1 → bin {HERO_BINS} selection rate: {t_bot:.4f} → {t_top:.4f}.",
                "- Expected: roughly monotone on pool mean (no elite dip).",
                "",
                f"## Right arm — congestion in score ($A_i − w·L_C$, w={w:g})",
                "",
                f"- Peak bin rate {c_peak:.4f}; top-bin rate {c_top:.4f} "
                f"(talent-only top {t_top:.4f}).",
                "- Expected: inverted-U-ish on pool mean vs monotone left.",
                "",
                "## Limitation",
                "",
                "- Qualitative POC only; Pass A hero bins poolq_loo, not pool mean.",
                "- PASS_B_D10_* files = frozen SCOUT reference (20-bin playground state).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def build_side_by_side(
    out_dir: Path,
    talent: pd.DataFrame,
    congest: pd.DataFrame,
    meta: dict,
) -> None:
    w = meta["congestion"]["w"]
    sys.path.insert(0, str(SCRIPTS))
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    ax = axes[0]
    gx = talent["bin"].to_numpy(dtype=float) + 1
    gy = talent["selection_rate"].to_numpy(dtype=float)
    ax.plot(gx, gy, "o-", color="seagreen", lw=2, ms=6)
    ax.fill_between(gx, 0, gy, alpha=0.15, color="seagreen")
    ax.set_xlabel(r"Bin ($1$ = lowest pool mean in sim)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{selected}}$")
    ax.set_title(
        rf"Generative — $\lambda = 0$ ({PRESET})"
        "\n"
        rf"$S_i = A_i$ | ${HERO_BINS}$ quantile on pool mean"
    )

    ax = axes[1]
    gx = congest["bin"].to_numpy(dtype=float) + 1
    gy = congest["selection_rate"].to_numpy(dtype=float)
    ax.plot(gx, gy, "o-", color="darkorange", lw=2, ms=6)
    ax.fill_between(gx, 0, gy, alpha=0.15, color="darkorange")
    ax.set_xlabel(r"Bin ($1$ = lowest pool mean in sim)")
    ax.set_ylabel(r"Mean $Y_{\mathrm{selected}}$")
    ax.set_title(
        rf"Generative — roster pressure in score ({PRESET})"
        "\n"
        rf"$S_i = A_i - {w:g}\,L_C$ | ${HERO_BINS}$ quantile on pool mean"
    )

    fig.suptitle(
        r"Pass B — Generative league: $\lambda$ off vs $\lambda$ on in SCORE"
        "\n"
        r"Readout binned on pool mean (not $\mathrm{poolq\_loo}$); qualitative POC",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    png = out_dir / PASS_B_PNG_NAME
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")

    caption = out_dir / "PASS_B_side_by_side_caption.txt"
    caption.write_text(
        "\n".join(
            [
                "Pass B caption — generative λ knockout pair",
                "",
                f"Preset: {PRESET}. Steps 1–3: ASSIGN → SCORE → SELECT.",
                f"Step 4 VISUALIZE: bin on pool mean (not poolq_loo).",
                "",
                "Left: S_i = A_i only (λ = 0), top-K select, binned on pool mean.",
                f"Right: S_i = A_i − {w:g}·L_C (crowding_smooth), same bins.",
                "",
                "Pool mean includes self; poolq_loo excludes self (Pass A hero axis).",
                "See PASS_B_D10_* for SCOUT reference figures (playground / 20 bins).",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _ensure_d10_bundle() -> Path:
    """Run SCOUT D10 export if reference PNGs missing."""
    need = [
        D10_DIR / "generative_congestion_539_pool_mean.png",
        D10_DIR / "generative_ability_only_pool_mean.png",
    ]
    if all(p.is_file() for p in need):
        return D10_DIR
    print("Building SCOUT D10 reference bundle …")
    subprocess.run(
        [sys.executable, str(D10_EXPORT_SCRIPT)],
        cwd=str(REPO),
        check=True,
    )
    return D10_DIR


def _build_d10_side_by_side(out_dir: Path, d10: Path) -> None:
    """Two-panel reference from D10 pool-mean CSVs (539 playground, 20 bins)."""
    sys.path.insert(0, str(SCRIPTS))
    from gallery_mathtext import configure_matplotlib_mathtext

    configure_matplotlib_mathtext()
    talent_csv = d10 / "generative_ability_only_pool_mean.csv"
    congest_csv = d10 / "generative_congestion_539_pool_mean.csv"
    if not talent_csv.is_file() or not congest_csv.is_file():
        print("D10 reference CSVs missing — skip PASS_B_D10 side-by-side.")
        return

    talent = pd.read_csv(talent_csv)
    congest = pd.read_csv(congest_csv)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    for ax, df, color, title in (
        (
            axes[0],
            talent,
            "seagreen",
            r"D10 reference — $\lambda = 0$" "\n" r"$539$ preset | pool mean | $20$ bins",
        ),
        (
            axes[1],
            congest,
            "darkorange",
            r"D10 reference — congestion in score"
            "\n"
            r"$539$ preset | pool mean | $20$ bins",
        ),
    ):
        gx = df["bin"].to_numpy(dtype=float) + 1
        gy = df["selection_rate"].to_numpy(dtype=float)
        ax.plot(gx, gy, "o-", color=color, lw=2, ms=5)
        ax.fill_between(gx, 0, gy, alpha=0.15, color=color)
        ax.set_xlabel(r"Bin ($1$ = lowest pool mean)")
        ax.set_ylabel(r"Mean $Y_{\mathrm{selected}}$")
        ax.set_title(title)

    fig.suptitle(
        r"SCOUT D10 reference — inverted-U on pool mean (not Pass A $\mathrm{poolq\_loo}$ axis)",
        fontsize=11,
        y=1.02,
    )
    fig.tight_layout()
    png = out_dir / PASS_B_D10_PNG_NAME
    fig.savefig(png, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {png}")


def sync_d10_reference_files(out_dir: Path) -> None:
    """Copy D10 PNGs/CSVs into gallery + build pool-mean side-by-side."""
    d10 = _ensure_d10_bundle()
    copies = [
        ("generative_ability_only_pool_mean.png", "PASS_B_D10_talent_only_pool_mean.png"),
        ("generative_congestion_539_pool_mean.png", "PASS_B_D10_congestion_pool_mean.png"),
        (
            "generative_congestion_539_loo_quality.png",
            "PASS_B_D10_congestion_poolq_loo_readout.png",
        ),
        ("axis_table_generative_readouts.md", "PASS_B_D10_axis_table.md"),
    ]
    for src_name, dst_name in copies:
        src = d10 / src_name
        if src.is_file():
            shutil.copy2(src, out_dir / dst_name)
            print(f"Copied D10 → {dst_name}")
    _build_d10_side_by_side(out_dir, d10)


def main() -> None:
    out_dir = OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    talent, congest, meta = run_knockouts(out_dir)
    _write_summary(out_dir, talent, congest, meta)
    build_side_by_side(out_dir, talent, congest, meta)
    sync_d10_reference_files(out_dir)
    print(f"\nDone. Outputs in {out_dir}")


if __name__ == "__main__":
    main()
