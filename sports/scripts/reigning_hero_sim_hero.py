#!/usr/bin/env python3
"""Reigning hero — empirical roster → SCORE → SELECT → sim HERO vs empirical.

Frozen NCAA rosters (no LG ASSIGN). Fit params from reigning PD21 MLE JSON.
v1 default SELECT: Gibbs rule D, K draws without replacement per season.

Population lock (HERO readout):
  2009–2021 · last-ps · ever-Y · ALLT · min20 · mg10 · winsor 1–99 · PPM z · EW16 LOO

SELECT pool (matches MLE attachment):
  2009–2021 · all-ps · min20 · PPM z · team L_C at γ*

Run (repo root):
  python sports/scripts/reigning_hero_sim_hero.py
  python sports/scripts/reigning_hero_sim_hero.py --select gibbs --gibbs-t 1.0
  python sports/scripts/reigning_hero_sim_hero.py --select all
  python sports/scripts/reigning_hero_sim_hero.py --gibbs-t-sweep
  python sports/scripts/reigning_hero_sim_hero.py --gibbs-t-sweep 0.75 1 1.5 2 5 12

Outputs:
  ``sports_sandbox/reigning_hero/sim_hero/``
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from bdp_ai_tj_distributions import BdpSpec, parse_bdp_spec  # noqa: E402
from bdp_reigning_loo_plots import (  # noqa: E402
    N_BINS_EW,
    WINSOR,
    _loo_ventile_table,
    _paint_draft_rate_panel,
    _prepare_last_ps,
    _quadratic_lpm_coef,
)
from gallery_mathtext import configure_matplotlib_mathtext  # noqa: E402
from grandchild_selection_inverted_u_diagnostic import _curvature_label  # noqa: E402
from hero_gallery_paths import (  # noqa: E402
    REIGNING_HERO_CALIBRATION_MLE,
    REIGNING_HERO_SIM_HERO,
    ensure_hero_dirs,
)
from pd21_draft_bernoulli_mle import (  # noqa: E402
    LC_COL,
    attach_player_level_lc,
    board_logits,
    softmax_probs,
)
from pd21_rho_hsort_calibrate import PanelPrepConfig, prepare_calibration_panel  # noqa: E402

import tier1_pool_assignment as tpa  # noqa: E402

SEASON_MIN = 2009
SEASON_MAX = 2021
SLUG = "mg10_min20_09_21"
DEFAULT_MLE_JSON = (
    REIGNING_HERO_CALIBRATION_MLE
    / f"REIGNING_PD21_draft_bernoulli_mle_{SEASON_MIN}_{SEASON_MAX}_{SLUG}.json"
)
HERO_SPEC = "mg10 min20 09_21"
DEFAULT_SEED = 5412015
DEFAULT_GIBBS_T = 1.0
# Mid-t band only (cold t ≈ top-K pathology; omitted from default sweep).
DEFAULT_GIBBS_T_SWEEP = (0.75, 1.0, 1.5, 2.0, 5.0, 12.0)
EMP_COLOR = "#4a6fa5"
SELECT_CHOICES = ("gibbs", "topk", "bernoulli")


def _load_mle_params(path: Path) -> dict[str, float]:
    fit = json.loads(path.read_text(encoding="utf-8"))
    return {
        "gamma_hat": float(fit["gamma_hat"]),
        "lambda_hat": float(fit["lambda_hat"]),
        "t_mle_hat": float(fit["t_hat"]),
    }


def _prepare_select_panel(season_min: int, season_max: int) -> pd.DataFrame:
    cfg = PanelPrepConfig(
        min_minutes=20.0,
        season_min=int(season_min),
        season_max=int(season_max),
    )
    return prepare_calibration_panel(cfg, perf_metric="ppm")


def _alex_scores(ability: np.ndarray, lc: np.ndarray, *, lam: float) -> np.ndarray:
    return np.asarray(ability, dtype=float) - float(lam) * np.asarray(lc, dtype=float)


def _load_draft_k_by_season(season_min: int, season_max: int) -> dict[int, int]:
    """NBA picks per college season: ``draft_year == panel season`` (617 over 2009–2021)."""
    from sports_pipeline.y_draft_mode import load_draft_lookup

    lu = load_draft_lookup()
    dy = pd.to_numeric(lu["draft_year"], errors="coerce")
    out: dict[int, int] = {}
    for season in range(int(season_min), int(season_max) + 1):
        out[int(season)] = int((dy == int(season)).sum())
    return out


def _apply_select_rule(
    work: pd.DataFrame,
    *,
    rule: str,
    lam: float,
    t_mle: float,
    gibbs_t: float,
    seed: int,
    k_by_season: dict[int, int],
) -> pd.DataFrame:
    out = work.copy()
    out["Y_sim"] = 0
    if "athlete_id" not in out.columns:
        raise KeyError("SELECT panel missing athlete_id")
    out["_athlete_id"] = pd.to_numeric(out["athlete_id"], errors="coerce").astype("Int64")
    rng = np.random.default_rng(int(seed))
    rule = str(rule).strip().lower()
    drafted_ever: set[int] = set()

    for season, sub in out.groupby("season", observed=True):
        sub = sub.loc[~sub["_athlete_id"].isin(list(drafted_ever))].copy()
        if sub.empty:
            continue
        idx = sub.index.to_numpy()
        ability = sub["ability"].to_numpy(dtype=float)
        lc = sub[LC_COL].to_numpy(dtype=float)
        k = int(k_by_season.get(int(season), 0))
        if k <= 0 or sub.empty:
            continue
        k = min(k, len(sub))
        scores = _alex_scores(ability, lc, lam=lam)

        if rule == "gibbs":
            mask = tpa.choose_selected(
                rng,
                scores,
                k,
                "D",
                temperature=float(gibbs_t),
            )
        elif rule == "topk":
            mask = tpa.choose_selected(rng, scores, k, "C")
        elif rule == "bernoulli":
            logits = board_logits(ability, lc, lam=lam, t=t_mle)
            p = softmax_probs(logits)
            mask = rng.uniform(size=len(p)) < np.clip(p, 0.0, 1.0)
        else:
            raise ValueError(f"unknown select rule {rule!r}")

        out.loc[idx, "Y_sim"] = mask.astype(int)
        picked = sub.loc[mask, "_athlete_id"].dropna().astype(int)
        drafted_ever.update(int(a) for a in picked.tolist())

    out = out.drop(columns=["_athlete_id"])
    return out


def _y_sim_ever_by_athlete(work: pd.DataFrame) -> pd.Series:
    if "athlete_id" not in work.columns:
        raise KeyError("SELECT panel missing athlete_id")
    ids = pd.to_numeric(work["athlete_id"], errors="coerce")
    y = pd.to_numeric(work["Y_sim"], errors="coerce").fillna(0).astype(int)
    tbl = pd.DataFrame({"athlete_id": ids, "Y_sim": y}).dropna(subset=["athlete_id"])
    tbl["athlete_id"] = tbl["athlete_id"].astype(int)
    return tbl.groupby("athlete_id", observed=True)["Y_sim"].max()


def _hero_panel_with_sim(
    spec: BdpSpec,
    y_sim_ever: pd.Series,
) -> pd.DataFrame:
    panel = _prepare_last_ps(spec, poolq_winsor_quantiles=WINSOR)
    panel = panel.copy()
    panel["athlete_id"] = pd.to_numeric(panel["athlete_id"], errors="coerce").astype("Int64")
    panel["Y_sim"] = (
        panel["athlete_id"].map(y_sim_ever).fillna(0).astype(int)
    )
    return panel


def _ventile_for_y(panel: pd.DataFrame, y_col: str) -> pd.DataFrame:
    cols = ["poolq_loo", y_col]
    tmp = panel.loc[:, cols].dropna().copy()
    tmp = tmp.rename(columns={y_col: "Y_draft"})
    tbl = _loo_ventile_table(tmp, n_bins=N_BINS_EW, poolq_binning="equal_width")
    return tbl.rename(columns={"draft_rate": "rate"})


def _lpm_on_y(panel: pd.DataFrame, y_col: str) -> dict:
    tmp = panel.loc[:, ["poolq_loo", y_col]].dropna().copy()
    tmp = tmp.rename(columns={y_col: "Y_draft"})
    return _quadratic_lpm_coef(tmp)


def _gibbs_t_palette(t_values: list[float]) -> dict[float, str]:
    sorted_t = sorted(set(float(t) for t in t_values))
    n = len(sorted_t)
    cmap = plt.cm.plasma if n > 2 else plt.cm.viridis
    return {t: cmap(i / max(n - 1, 1)) for i, t in enumerate(sorted_t)}


def _prepare_shared_select_work(
    *,
    mle_path: Path,
    season_min: int,
    season_max: int,
    hero_spec: BdpSpec,
) -> dict:
    """Load panel once; empirical HERO table; SELECT work without Y_sim."""
    params = _load_mle_params(mle_path)
    print(f"Loading SELECT pool {season_min}–{season_max} (all-ps, min20) ...", flush=True)
    panel = _prepare_select_panel(season_min, season_max)
    print(
        f"Attaching $L^C$ at $\\gamma^*={params['gamma_hat']:.3g}$ ...",
        flush=True,
    )
    work = attach_player_level_lc(
        panel,
        gamma=params["gamma_hat"],
        season_min=season_min,
        season_max=season_max,
    )
    work = work.rename(columns={"perf": "ability"})
    if "ability" not in work.columns:
        work["ability"] = work.get("perf")

    hero_panel = _prepare_last_ps(hero_spec, poolq_winsor_quantiles=WINSOR)
    emp_tbl = _ventile_for_y(hero_panel, "Y_draft")
    emp_coef = _lpm_on_y(hero_panel, "Y_draft")

    try:
        mle_rel = str(mle_path.relative_to(REPO))
    except ValueError:
        mle_rel = str(mle_path)

    return {
        "params": params,
        "mle_json": mle_rel,
        "work": work,
        "hero_panel_base": hero_panel,
        "emp_tbl": emp_tbl,
        "emp_coef": emp_coef,
        "k_by_season": _load_draft_k_by_season(season_min, season_max),
    }


def _simulate_gibbs_hero(
    shared: dict,
    *,
    gibbs_t: float,
    seed: int,
    hero_spec: BdpSpec,
) -> tuple[pd.DataFrame, pd.DataFrame, dict, pd.DataFrame, int]:
    """Return (sim_tbl, sim_coef, sim_curvature, hero_panel, n_sim_picks)."""
    params = shared["params"]
    work = _apply_select_rule(
        shared["work"],
        rule="gibbs",
        lam=params["lambda_hat"],
        t_mle=params["t_mle_hat"],
        gibbs_t=float(gibbs_t),
        seed=int(seed),
        k_by_season=shared["k_by_season"],
    )
    y_sim_ever = _y_sim_ever_by_athlete(work)
    hero_panel = shared["hero_panel_base"].copy()
    hero_panel["athlete_id"] = pd.to_numeric(hero_panel["athlete_id"], errors="coerce").astype("Int64")
    hero_panel["Y_sim"] = hero_panel["athlete_id"].map(y_sim_ever).fillna(0).astype(int)
    sim_tbl = _ventile_for_y(hero_panel, "Y_sim")
    sim_coef = _lpm_on_y(hero_panel, "Y_sim")
    curv = _curvature_label(sim_tbl.rename(columns={"rate": "selection_rate"}))
    return sim_tbl, sim_coef, curv, hero_panel, int(work["Y_sim"].sum())


def _plot_gibbs_t_sweep_overlay(
    emp_tbl: pd.DataFrame,
    emp_coef: dict,
    sweep_frames: dict[float, pd.DataFrame],
    sweep_meta: list[dict],
    *,
    spec: BdpSpec,
    mle_params: dict[str, float],
    out_png: Path,
) -> None:
    configure_matplotlib_mathtext()
    # Tall figure + y-zoom to data range (not 0–1) so mid-t curves separate visually.
    fig = plt.figure(figsize=(14.0, 10.5))
    gs = fig.add_gridspec(2, 1, height_ratios=[3.2, 1.0], hspace=0.32)
    ax = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[1, 0])
    colors = _gibbs_t_palette(list(sweep_frames))

    x_emp = emp_tbl["x_center"].to_numpy(dtype=float)
    y_emp = emp_tbl["rate"].to_numpy(dtype=float)
    ax.plot(
        x_emp,
        y_emp,
        "s--",
        color=EMP_COLOR,
        lw=2.4,
        ms=6,
        label=rf"Empirical ($\beta_2={emp_coef['beta_poolq_loo_sq']:+.4g}$)",
        zorder=1,
    )

    for row in sweep_meta:
        t_val = float(row["gibbs_t"])
        summ = sweep_frames[t_val]
        x = summ["x_center"].to_numpy(dtype=float)
        y = summ["rate"].to_numpy(dtype=float)
        b2 = float(row["lpm_sim"]["beta_poolq_loo_sq"])
        shape = str(row["curvature_sim"]["shape"]).replace("_", " ")
        ax.plot(
            x,
            y,
            "o-",
            lw=2.2,
            ms=5,
            color=colors[t_val],
            label=rf"$t={t_val:g}$ · $\beta_2={b2:+.4g}$ · {shape}",
            zorder=2,
        )

    all_y = [y_emp, *([s["rate"].to_numpy(dtype=float) for s in sweep_frames.values()])]
    pooled = np.concatenate([np.asarray(a, dtype=float) for a in all_y])
    pooled = pooled[np.isfinite(pooled)]
    y_lo = float(pooled.min())
    y_hi = float(pooled.max())
    span = max(y_hi - y_lo, 0.005)
    pad = span * 0.12
    ax.set_ylim(y_lo - pad, y_hi + pad)
    ax.set_xlabel(r"Player poolq$_{\mathrm{LOO}}$ (EW16 midpoint)", fontsize=11)
    ax.set_ylabel(r"$\hat{P}(Y{=}1)$ per bin", fontsize=11)
    ax.set_title(
        rf"Gibbs $t$ sweep vs empirical HERO · MBB {spec.season_min}–{spec.season_max}"
        rf" (y-zoomed: {y_lo - pad:.3f}–{y_hi + pad:.3f})",
        fontsize=11,
    )
    ax.legend(fontsize=7.5, loc="upper left", framealpha=0.95, ncol=1)
    ax.grid(alpha=0.25)

    t_arr = np.array([float(r["gibbs_t"]) for r in sweep_meta], dtype=float)
    b2_arr = np.array([float(r["lpm_sim"]["beta_poolq_loo_sq"]) for r in sweep_meta], dtype=float)
    emp_b2 = float(emp_coef["beta_poolq_loo_sq"])
    log_t = np.log10(np.maximum(t_arr, 1e-12))
    ax2.axhline(emp_b2, color=EMP_COLOR, ls="--", lw=1.8, label=rf"Empirical $\beta_2$")
    ax2.plot(log_t, b2_arr, "o-", color="#9467bd", lw=2.0, ms=6)
    for t_val, lt, b2 in zip(t_arr, log_t, b2_arr, strict=True):
        ax2.annotate(f"{t_val:g}", (lt, b2), textcoords="offset points", xytext=(4, 4), fontsize=7)
    b2_lo = float(min(b2_arr.min(), emp_b2))
    b2_hi = float(max(b2_arr.max(), emp_b2))
    b2_span = max(b2_hi - b2_lo, 0.003)
    b2_pad = b2_span * 0.2
    ax2.set_ylim(b2_lo - b2_pad, b2_hi + b2_pad)
    ax2.set_xlabel(r"$\log_{10} t_{\mathrm{Gibbs}}$", fontsize=10)
    ax2.set_ylabel(r"LPM $\beta_2$ on poolq$_{\mathrm{LOO}}$", fontsize=10)
    ax2.set_title("Curvature tag vs temperature", fontsize=10)
    ax2.legend(fontsize=8, loc="best")
    ax2.grid(alpha=0.25)

    fig.suptitle(
        r"Reigning sim HERO — Gibbs SELECT temperature dial (rule D, frozen rosters)",
        fontsize=12,
        y=0.98,
    )
    fig.text(
        0.5,
        0.01,
        (
            f"SCORE $S=A-\\lambda^* L^C$ ({LC_COL}) · HERO axis poolq$_{{LOO}}$ · "
            rf"$\gamma^*={mle_params['gamma_hat']:.2f}$ · $\lambda^*={mle_params['lambda_hat']:.2f}$ · "
            f"last-ps · EW{N_BINS_EW} · mg{spec.min_team_season_games} min{spec.min_minutes:g}"
        ),
        ha="center",
        va="bottom",
        fontsize=8,
        color="0.35",
    )
    fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.07)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=160, bbox_inches="tight")
    plt.close(fig)


def run_gibbs_t_sweep(
    *,
    t_values: tuple[float, ...],
    mle_path: Path,
    seed: int,
    season_min: int,
    season_max: int,
    hero_spec: BdpSpec,
    out_dir: Path,
) -> dict:
    shared = _prepare_shared_select_work(
        mle_path=mle_path,
        season_min=season_min,
        season_max=season_max,
        hero_spec=hero_spec,
    )
    sweep_frames: dict[float, pd.DataFrame] = {}
    sweep_meta: list[dict] = []

    for i, t_val in enumerate(t_values):
        print(f"Gibbs sweep t={t_val:g} ({i + 1}/{len(t_values)}) ...", flush=True)
        sim_tbl, sim_coef, curv, _hero, _n_picks = _simulate_gibbs_hero(
            shared,
            gibbs_t=float(t_val),
            seed=int(seed) + 100 * i,
            hero_spec=hero_spec,
        )
        sweep_frames[float(t_val)] = sim_tbl
        sweep_meta.append(
            {
                "gibbs_t": float(t_val),
                "log10_t": float(np.log10(max(float(t_val), 1e-12))),
                "lpm_sim": sim_coef,
                "curvature_sim": curv,
            }
        )

    stem = f"REIGNING_SIM_HERO_gibbs_t_sweep_{SLUG}_last_ps"
    out_png = out_dir / f"{stem}.png"
    out_json = out_dir / f"{stem}.json"
    out_csv = out_dir / f"{stem}_beta2.csv"

    _plot_gibbs_t_sweep_overlay(
        shared["emp_tbl"],
        shared["emp_coef"],
        sweep_frames,
        sweep_meta,
        spec=hero_spec,
        mle_params=shared["params"],
        out_png=out_png,
    )

    beta_df = pd.DataFrame(
        [
            {
                "gibbs_t": row["gibbs_t"],
                "log10_t": row["log10_t"],
                "beta_poolq_loo_sq": row["lpm_sim"]["beta_poolq_loo_sq"],
                "curvature_shape": row["curvature_sim"]["shape"],
            }
            for row in sweep_meta
        ]
    )
    beta_df.to_csv(out_csv, index=False)

    meta = {
        "diagnostic": "reigning_hero_sim_hero_gibbs_t_sweep",
        "date": date.today().isoformat(),
        "season_min": season_min,
        "season_max": season_max,
        "hero_spec": hero_spec.slug,
        "gibbs_t_values": [float(t) for t in t_values],
        "seed": int(seed),
        "mle_json": shared["mle_json"],
        "mle_params": shared["params"],
        "score_lc_col": LC_COL,
        "hero_axis": "poolq_loo",
        "axis_mismatch_note": (
            "SCORE uses team L_C; HERO bins LOO — cold t nests top-K on S, "
            "which can over-draft low-LOO big fish."
        ),
        "lpm_empirical": shared["emp_coef"],
        "curvature_empirical": _curvature_label(
            shared["emp_tbl"].rename(columns={"rate": "selection_rate"})
        ),
        "runs": sweep_meta,
        "artifacts": {
            "png": out_png.name,
            "json": out_json.name,
            "beta2_csv": out_csv.name,
        },
    }
    out_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {out_png}")
    print(f"Wrote {out_json}")
    print(f"Wrote {out_csv}")
    return meta


def _plot_emp_vs_sim(
    emp_tbl: pd.DataFrame,
    sim_tbl: pd.DataFrame,
    *,
    emp_coef: dict,
    sim_coef: dict,
    spec: BdpSpec,
    select_rule: str,
    gibbs_t: float | None,
    mle_params: dict[str, float],
    out_png: Path,
) -> None:
    configure_matplotlib_mathtext()
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.0))
    fig.subplots_adjust(wspace=0.22, top=0.84, bottom=0.16)

    panels = [
        (axes[0], emp_tbl, emp_coef, "Empirical $Y$", "#4a6fa5"),
        (axes[1], sim_tbl, sim_coef, r"Sim $Y^{\mathrm{sim}}$", "#c44e52"),
    ]
    for ax, tbl, coef, title, color in panels:
        plot_tbl = tbl.rename(columns={"rate": "draft_rate"})
        _paint_draft_rate_panel(
            ax,
            plot_tbl,
            title=title,
            xlabel=r"Player poolq$_{\mathrm{LOO}}$ (EW16 midpoint)",
            lpm_b2=coef["beta_poolq_loo_sq"],
            poolq_binning="equal_width",
        )
        for patch in ax.patches:
            patch.set_facecolor(color)
            patch.set_alpha(0.88)

    if select_rule == "gibbs":
        rule_note = rf"Gibbs rule D · $t_{{\mathrm{{Gibbs}}}}={float(gibbs_t):g}$"
    elif select_rule == "topk":
        rule_note = r"Deterministic top-$K$ (rule C)"
    else:
        rule_note = r"Bernoulli replay from MLE $p_i$"

    fig.suptitle(
        rf"HERO replay — empirical vs sim SELECT · MBB {spec.season_min}–{spec.season_max}",
        fontsize=11,
    )
    fig.text(
        0.5,
        0.02,
        (
            f"last-ps · ever-$Y$ · ALLT · min{spec.min_minutes:g} · mg{spec.min_team_season_games} · "
            f"EW{N_BINS_EW} · frozen rosters · "
            rf"$\gamma^*={mle_params['gamma_hat']:.2f}$ · "
            rf"$\lambda^*={mle_params['lambda_hat']:.2f}$ · "
            rf"$t^*_{{\mathrm{{MLE}}}}={mle_params['t_mle_hat']:.3f}$ · {rule_note}"
        ),
        ha="center",
        va="bottom",
        fontsize=8,
        color="0.35",
    )
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=160, bbox_inches="tight")
    plt.close(fig)


def _output_stem(select_rule: str, *, gibbs_t: float | None) -> str:
    if select_rule == "gibbs":
        t_tag = f"t{gibbs_t:g}".replace(".", "p")
        return f"REIGNING_SIM_HERO_{select_rule}_{t_tag}_{SLUG}_last_ps"
    return f"REIGNING_SIM_HERO_{select_rule}_{SLUG}_last_ps"


def run_one(
    *,
    select_rule: str,
    mle_path: Path,
    gibbs_t: float,
    seed: int,
    season_min: int,
    season_max: int,
    hero_spec: BdpSpec,
    out_dir: Path,
    shared: dict | None = None,
) -> dict:
    if shared is None:
        shared = _prepare_shared_select_work(
            mle_path=mle_path,
            season_min=season_min,
            season_max=season_max,
            hero_spec=hero_spec,
        )
    params = shared["params"]

    if select_rule == "gibbs":
        print(f"SELECT rule=gibbs t={gibbs_t:g} seed={seed} ...", flush=True)
        sim_tbl, sim_coef, curv, hero_panel, n_sim_picks = _simulate_gibbs_hero(
            shared,
            gibbs_t=float(gibbs_t),
            seed=int(seed),
            hero_spec=hero_spec,
        )
    else:
        print(f"SELECT rule={select_rule!r} seed={seed} ...", flush=True)
        work = _apply_select_rule(
            shared["work"],
            rule=select_rule,
            lam=params["lambda_hat"],
            t_mle=params["t_mle_hat"],
            gibbs_t=float(gibbs_t),
            seed=seed,
            k_by_season=shared["k_by_season"],
        )
        y_sim_ever = _y_sim_ever_by_athlete(work)
        hero_panel = _hero_panel_with_sim(hero_spec, y_sim_ever)
        sim_tbl = _ventile_for_y(hero_panel, "Y_sim")
        sim_coef = _lpm_on_y(hero_panel, "Y_sim")
        curv = _curvature_label(sim_tbl.rename(columns={"rate": "selection_rate"}))
        n_sim_picks = int(work["Y_sim"].sum())

    emp_tbl = shared["emp_tbl"]
    emp_coef = shared["emp_coef"]

    stem = _output_stem(select_rule, gibbs_t=gibbs_t if select_rule == "gibbs" else None)
    out_png = out_dir / f"{stem}.png"
    out_json = out_dir / f"{stem}.json"
    out_csv = out_dir / f"{stem}_last_ps_panel.csv"

    _plot_emp_vs_sim(
        emp_tbl,
        sim_tbl,
        emp_coef=emp_coef,
        sim_coef=sim_coef,
        spec=hero_spec,
        select_rule=select_rule,
        gibbs_t=gibbs_t if select_rule == "gibbs" else None,
        mle_params=params,
        out_png=out_png,
    )

    hero_panel.to_csv(out_csv, index=False)

    n_sim_drafted = int(hero_panel["Y_sim"].sum())
    n_emp_drafted = int(hero_panel["Y_draft"].sum())
    meta = {
        "diagnostic": "reigning_hero_sim_hero",
        "date": date.today().isoformat(),
        "season_min": season_min,
        "season_max": season_max,
        "hero_spec": hero_spec.slug,
        "select_rule": select_rule,
        "gibbs_t": float(gibbs_t) if select_rule == "gibbs" else None,
        "seed": int(seed),
        "mle_json": shared["mle_json"],
        "mle_params": params,
        "score_form_select": f"S_i = A_i - lambda^* L^C ({LC_COL})",
        "hero_axis": "poolq_loo",
        "select_pool": "all-ps · min20 · matches PD21 L_C attachment",
        "k_source": "NBA draft lookup: K_s = count(draft_year == season)",
        "k_by_season": shared["k_by_season"],
        "n_sim_picks_total": n_sim_picks,
        "hero_readout": (
            "last-ps · ever-Y empirical · Y_sim_ever = max_t Y_sim · "
            "at-most-once career sim draft · EW16 LOO · mg10"
        ),
        "n_hero_rows": int(len(hero_panel)),
        "n_emp_drafted_last_ps": n_emp_drafted,
        "n_sim_drafted_last_ps_ever": n_sim_drafted,
        "lpm_empirical": emp_coef,
        "lpm_sim": sim_coef,
        "curvature_empirical": _curvature_label(emp_tbl.rename(columns={"rate": "selection_rate"})),
        "curvature_sim": curv,
        "artifacts": {
            "png": out_png.name,
            "json": out_json.name,
            "panel_csv": out_csv.name,
        },
    }
    out_json.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {out_png}")
    print(f"Wrote {out_json}")
    print(f"Wrote {out_csv}")
    print(
        f"  drafted (last-ps): emp={n_emp_drafted} sim_ever={n_sim_drafted} · "
        f"LPM β₂ emp={emp_coef['beta_poolq_loo_sq']:+.5f} sim={sim_coef['beta_poolq_loo_sq']:+.5f}",
        flush=True,
    )
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Reigning hero — empirical roster sim HERO replay")
    parser.add_argument("--season-min", type=int, default=SEASON_MIN)
    parser.add_argument("--season-max", type=int, default=SEASON_MAX)
    parser.add_argument("--mle-json", type=Path, default=DEFAULT_MLE_JSON)
    parser.add_argument(
        "--select",
        nargs="+",
        choices=[*SELECT_CHOICES, "all"],
        default=["gibbs"],
        help="SELECT rule(s); 'all' runs gibbs, topk, bernoulli",
    )
    parser.add_argument("--gibbs-t", type=float, default=DEFAULT_GIBBS_T)
    parser.add_argument(
        "--gibbs-t-sweep",
        nargs="*",
        type=float,
        metavar="T",
        default=None,
        help=(
            "Overlay PNG + β₂ table for Gibbs t grid "
            f"(default grid: {', '.join(str(t) for t in DEFAULT_GIBBS_T_SWEEP)}). "
            "Pass values to override, e.g. --gibbs-t-sweep 0.1 1 5"
        ),
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--hero-spec", default=HERO_SPEC, help=f"BdpSpec (default: {HERO_SPEC!r})")
    parser.add_argument("--out-dir", type=Path, default=REIGNING_HERO_SIM_HERO)
    args = parser.parse_args()

    ensure_hero_dirs()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    if not args.mle_json.is_file():
        raise SystemExit(
            f"Missing MLE JSON {args.mle_json} — run reigning_hero_calibration.py --only mle first."
        )

    hero_spec = parse_bdp_spec(args.hero_spec)
    results: list[dict] = []

    if args.gibbs_t_sweep is not None:
        t_values = tuple(args.gibbs_t_sweep) if args.gibbs_t_sweep else DEFAULT_GIBBS_T_SWEEP
        results.append(
            run_gibbs_t_sweep(
                t_values=t_values,
                mle_path=args.mle_json,
                seed=int(args.seed),
                season_min=int(args.season_min),
                season_max=int(args.season_max),
                hero_spec=hero_spec,
                out_dir=args.out_dir,
            )
        )

    want_singles = args.gibbs_t_sweep is None
    if "all" in args.select:
        rules = list(SELECT_CHOICES)
    else:
        rules = list(dict.fromkeys(args.select))
    if args.gibbs_t_sweep is not None and rules == ["gibbs"]:
        want_singles = False

    if want_singles:
        shared = None
        if len(rules) > 1:
            shared = _prepare_shared_select_work(
                mle_path=args.mle_json,
                season_min=int(args.season_min),
                season_max=int(args.season_max),
                hero_spec=hero_spec,
            )
        for i, rule in enumerate(rules):
            seed = int(args.seed) + 1000 * i
            results.append(
                run_one(
                    select_rule=rule,
                    mle_path=args.mle_json,
                    gibbs_t=float(args.gibbs_t),
                    seed=seed,
                    season_min=int(args.season_min),
                    season_max=int(args.season_max),
                    hero_spec=hero_spec,
                    out_dir=args.out_dir,
                    shared=shared,
                )
            )

    if not results:
        raise SystemExit("Nothing to run — use --select and/or --gibbs-t-sweep.")

    manifest = {
        "diagnostic": "reigning_hero_sim_hero",
        "date": date.today().isoformat(),
        "runs": results,
    }
    manifest_path = args.out_dir / f"REIGNING_SIM_HERO_manifest_{SLUG}.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nWrote {manifest_path}")


if __name__ == "__main__":
    main()
