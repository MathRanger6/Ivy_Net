#!/usr/bin/env python3
"""PD21 — H_sort sensitivity: min_minutes floor and conference subsets.

Compares empirical sorting index (H_sort) and optional bracket rho* under:
  1. min_minutes = 0 vs 20 (hero default)
  2. Full panel vs within-ESPN-conference subsets

Conference IDs come from ``datasets/mbb/mbb_df_sched.csv`` (home/away conference_id).

Run (repo root):
  python sports/scripts/pd21_rho_hsort_sensitivity.py
  python sports/scripts/pd21_rho_hsort_sensitivity.py --n-seeds 20 --n-jobs 8
  python sports/scripts/pd21_rho_hsort_sensitivity.py --skip-conference-bracket

Outputs (HEROs_and_PASSes/pd21_rho/):
  PD21_rho_hsort_sensitivity_minutes.csv
  PD21_rho_hsort_sensitivity_conference_hsort.csv
  PD21_rho_hsort_sensitivity.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
SPORTS = REPO / "sports"
sys.path.insert(0, str(SPORTS))
sys.path.insert(0, str(SCRIPTS))

from hero_gallery_paths import PD21_RHO, ensure_hero_dirs

import grandchild_selection_inverted_u_diagnostic as gsel
import pd21_rho_hsort_calibrate as prc

OUT = PD21_RHO
SEASON_MIN = gsel.FULL_PANEL_SEASON_MIN
SEASON_MAX = gsel.FULL_PANEL_SEASON_MAX
MIN_TEAMS_PER_CONF = 8
MIN_PLAYERS_PER_CONF_SEASON = 80


def _hero_pipeline_config(*, min_minutes: float):
    from sports_pipeline.config import PipelineConfig

    return PipelineConfig(
        perf_metric=["ppm"],
        perf_zscore_within_season=True,
        ventiles=16,
        poolq_binning="quantile",
        poolq_winsor_quantiles=(0.01, 0.99),
        min_minutes=float(min_minutes),
        restrict_teams_by_draftees=False,
        use_prebuilt_panel_csv=False,
        panel_season_min=SEASON_MIN,
        panel_season_max=SEASON_MAX,
        analysis_season_min=SEASON_MIN,
        analysis_season_max=SEASON_MAX,
    )


def prepare_panel(*, min_minutes: float) -> pd.DataFrame:
    from sports_pipeline import conductor, panel_build
    from sports_pipeline.perf_metric import perf_metric_active

    cfg = _hero_pipeline_config(min_minutes=min_minutes)
    panel = conductor.prepare_panel(cfg)
    panel = panel_build.apply_perf_metric_for_analysis(
        panel,
        perf_metric_active(cfg),
        poolq_winsor_quantiles=cfg.poolq_winsor_quantiles,
        zscore_perf_within_season=True,
    )
    return panel_build.filter_panel(panel, cfg)


def load_team_conference_map() -> pd.DataFrame:
    """team_id × season → ESPN conference_id from schedule file."""
    sched_path = REPO / "datasets" / "mbb" / "mbb_df_sched.csv"
    sched = pd.read_csv(
        sched_path,
        usecols=["season", "home_id", "home_conference_id", "away_id", "away_conference_id"],
    )
    sched = sched.loc[sched["season"].between(SEASON_MIN, SEASON_MAX)]
    home = sched.rename(
        columns={"home_id": "team_id", "home_conference_id": "conference_id"}
    )[["season", "team_id", "conference_id"]]
    away = sched.rename(
        columns={"away_id": "team_id", "away_conference_id": "conference_id"}
    )[["season", "team_id", "conference_id"]]
    tm = pd.concat([home, away], ignore_index=True)
    tm = tm.dropna(subset=["team_id", "conference_id", "season"])
    tm["team_id"] = tm["team_id"].astype(np.int64)
    tm["season"] = tm["season"].astype(int)
    tm["conference_id"] = tm["conference_id"].astype(float)
    return tm.drop_duplicates(["season", "team_id"])


def attach_conference(panel: pd.DataFrame, team_conf: pd.DataFrame) -> pd.DataFrame:
    return panel.merge(team_conf, on=["team_id", "season"], how="left")


def season_data_from_panel(
    panel: pd.DataFrame,
    season: int,
    *,
    conference_id: float | None = None,
) -> prc.SeasonData | None:
    gc = prc._load_gc()
    sub = panel.loc[panel["season"] == int(season)].copy()
    if conference_id is not None:
        sub = sub.loc[sub["conference_id"] == float(conference_id)]
    sub = sub.dropna(subset=["perf", "team_id"])
    if sub.empty:
        return None
    caps = (
        sub.groupby("team_id", observed=True)
        .size()
        .to_numpy(dtype=np.int64)
    )
    ability = sub["perf"].to_numpy(dtype=float)
    if int(caps.sum()) != len(ability):
        return None
    pool_id = sub.groupby("team_id", observed=True).ngroup().to_numpy(dtype=np.int64)
    h_emp = float(gc.realized_sorting_index_H_sort(ability, pool_id))
    return prc.SeasonData(
        season=int(season),
        ability=np.asarray(ability, dtype=float),
        roster_caps=np.asarray(caps, dtype=np.int64),
        h_sort_empirical=h_emp,
        n_players=int(len(ability)),
        n_teams=int(caps.size),
    )


def empirical_hsort_by_minutes() -> pd.DataFrame:
    rows: list[dict] = []
    for mm in (0.0, 20.0):
        print(f"  Building panel min_minutes={mm:g} ...", flush=True)
        panel = prepare_panel(min_minutes=mm)
        for season in range(SEASON_MIN, SEASON_MAX + 1):
            sd = season_data_from_panel(panel, season)
            if sd is None:
                continue
            rows.append(
                {
                    "min_minutes": mm,
                    "season": season,
                    "h_sort_empirical": sd.h_sort_empirical,
                    "n_players": sd.n_players,
                    "n_teams": sd.n_teams,
                }
            )
    return pd.DataFrame(rows)


def empirical_hsort_by_conference(panel: pd.DataFrame, team_conf: pd.DataFrame) -> pd.DataFrame:
    panel = attach_conference(panel, team_conf)
    rows: list[dict] = []
    for season in range(SEASON_MIN, SEASON_MAX + 1):
        sub = panel.loc[panel["season"] == int(season)]
        for conf_id, g in sub.groupby("conference_id", observed=True):
            if pd.isna(conf_id):
                continue
            n_teams = int(g["team_id"].nunique())
            n_players = int(len(g))
            if n_teams < MIN_TEAMS_PER_CONF or n_players < MIN_PLAYERS_PER_CONF_SEASON:
                continue
            sd = season_data_from_panel(panel, season, conference_id=float(conf_id))
            if sd is None:
                continue
            rows.append(
                {
                    "season": int(season),
                    "conference_id": float(conf_id),
                    "h_sort_empirical": sd.h_sort_empirical,
                    "n_players": sd.n_players,
                    "n_teams": sd.n_teams,
                }
            )
    return pd.DataFrame(conf_rows if (conf_rows := rows) else [])


def top_conferences(conf_df: pd.DataFrame, *, n: int = 5) -> list[float]:
    """Conferences with largest median team count across seasons."""
    med = (
        conf_df.groupby("conference_id")["n_teams"]
        .median()
        .sort_values(ascending=False)
    )
    return [float(x) for x in med.head(int(n)).index.tolist()]


def bracket_for_panel_subset(
    panel: pd.DataFrame,
    *,
    label: str,
    conference_id: float | None,
    n_seeds: int,
    n_jobs: int,
    parallel: str,
    bracket_tol: float,
) -> dict:
    seasons: list[prc.SeasonData] = []
    for season in range(SEASON_MIN, SEASON_MAX + 1):
        sd = season_data_from_panel(panel, season, conference_id=conference_id)
        if sd is not None:
            seasons.append(sd)
    if not seasons:
        return {"label": label, "error": "no seasons"}

    detail_path = OUT / f"PD21_rho_hsort_sensitivity_{label}_detail.jsonl"
    if detail_path.exists():
        detail_path.unlink()

    per_season, trace = prc.run_bracket_search(
        seasons,
        n_seeds=n_seeds,
        base_seed=prc.BASE_SEED + (int(conference_id) if conference_id else 0),
        parallel=parallel,
        n_jobs=n_jobs,
        detail_path=detail_path,
        rho_max=prc.BRACKET_RHO_MAX_DEFAULT,
        rho_tol=bracket_tol,
        max_expansions=8,
        max_bisect=12,
        eval_reference_rho=True,
    )
    per_df = pd.DataFrame(per_season)
    summary = prc.attach_empirical(
        prc.summarize_detail(detail_path),
        seasons,
    )
    longitudinal = prc.pick_rho_longitudinal(summary)
    return {
        "label": label,
        "conference_id": conference_id,
        "n_seasons": len(seasons),
        "longitudinal_rho_star": prc.normalize_rho(longitudinal["rho_star_longitudinal"]),
        "mean_abs_err_at_star": longitudinal["mean_abs_err_at_star"],
        "reference_rho_0p5_mean_abs_err": longitudinal["mean_abs_err_at_reference_rho"],
        "per_season": per_df.to_dict(orient="records"),
        "bracket_trace_n": len(trace),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="PD21 H_sort sensitivity diagnostics.")
    parser.add_argument("--n-seeds", type=int, default=20)
    parser.add_argument("--n-jobs", type=int, default=4)
    parser.add_argument("--parallel", choices=("process", "ray"), default="process")
    parser.add_argument("--bracket-tol", type=float, default=0.001)
    parser.add_argument("--skip-conference-bracket", action="store_true")
    parser.add_argument("--top-conferences", type=int, default=3)
    args = parser.parse_args()

    ensure_hero_dirs()

    print("Empirical H_sort: min_minutes 0 vs 20 ...", flush=True)
    minutes_df = empirical_hsort_by_minutes()
    minutes_csv = OUT / "PD21_rho_hsort_sensitivity_minutes.csv"
    minutes_df.to_csv(minutes_csv, index=False, float_format="%.12g")

    pivot = minutes_df.pivot_table(
        index="season",
        columns="min_minutes",
        values="h_sort_empirical",
    )
    if 0.0 in pivot.columns and 20.0 in pivot.columns:
        pivot["delta_mm20_minus_mm0"] = pivot[20.0] - pivot[0.0]
    print("\nMinutes comparison (H_sort empirical):")
    print(pivot.to_string(float_format=lambda x: f"{x:.6f}"))

    print("\nLoading conference map + min_minutes=20 panel ...", flush=True)
    team_conf = load_team_conference_map()
    panel20 = prepare_panel(min_minutes=20.0)
    conf_df = empirical_hsort_by_conference(panel20, team_conf)
    conf_csv = OUT / "PD21_rho_hsort_sensitivity_conference_hsort.csv"
    conf_df.to_csv(conf_csv, index=False, float_format="%.12g")

    if not conf_df.empty:
        conf_summary = (
            conf_df.groupby("conference_id")["h_sort_empirical"]
            .agg(["mean", "median", "std", "count"])
            .sort_values("mean", ascending=False)
        )
        print("\nTop conferences by mean empirical H_sort (min 20 min panel):")
        print(conf_summary.head(10).to_string(float_format=lambda x: f"{x:.6f}"))
    else:
        conf_summary = pd.DataFrame()
        print("\nNo conference subsets passed size filters.")

    full_panel_mean = float(
        minutes_df.loc[minutes_df["min_minutes"] == 20.0, "h_sort_empirical"].mean()
    )
    conf_pooled = (
        conf_df.groupby("conference_id")["h_sort_empirical"].mean().sort_values(ascending=False)
        if not conf_df.empty
        else pd.Series(dtype=float)
    )

    bracket_results: list[dict] = []
    if not args.skip_conference_bracket:
        print("\nBracket rho* — full panel (min 20) ...", flush=True)
        bracket_results.append(
            bracket_for_panel_subset(
                panel20,
                label="full_min20",
                conference_id=None,
                n_seeds=args.n_seeds,
                n_jobs=args.n_jobs,
                parallel=args.parallel,
                bracket_tol=args.bracket_tol,
            )
        )
        panel20_conf = attach_conference(panel20, team_conf)
        for conf_id in top_conferences(conf_df, n=args.top_conferences):
            print(f"\nBracket rho* — conference_id={conf_id:g} ...", flush=True)
            bracket_results.append(
                bracket_for_panel_subset(
                    panel20_conf,
                    label=f"conf_{int(conf_id)}",
                    conference_id=conf_id,
                    n_seeds=args.n_seeds,
                    n_jobs=args.n_jobs,
                    parallel=args.parallel,
                    bracket_tol=args.bracket_tol,
                )
            )

    meta = {
        "generated": date.today().isoformat(),
        "script": "sports/scripts/pd21_rho_hsort_sensitivity.py",
        "seasons": f"{SEASON_MIN}-{SEASON_MAX}",
        "rho_match_decimals": prc.RHO_MATCH_DECIMALS,
        "bracket_tol": float(args.bracket_tol),
        "minutes_comparison": {
            "mean_h_sort_min0": float(
                minutes_df.loc[minutes_df["min_minutes"] == 0.0, "h_sort_empirical"].mean()
            ),
            "mean_h_sort_min20": float(full_panel_mean),
            "mean_delta_mm20_minus_mm0": float(
                minutes_df.loc[minutes_df["min_minutes"] == 20.0, "h_sort_empirical"].mean()
                - minutes_df.loc[minutes_df["min_minutes"] == 0.0, "h_sort_empirical"].mean()
            ),
            "per_season": pivot.reset_index().to_dict(orient="records"),
        },
        "conference_empirical": {
            "top_by_mean_h_sort": [
                {"conference_id": float(k), "mean_h_sort": float(v)}
                for k, v in conf_pooled.head(10).items()
            ],
            "full_panel_mean_h_sort_min20": full_panel_mean,
        },
        "bracket_subsets": bracket_results,
        "outputs": {
            "minutes_csv": str(minutes_csv.relative_to(REPO)),
            "conference_csv": str(conf_csv.relative_to(REPO)),
        },
    }
    meta_path = OUT / "PD21_rho_hsort_sensitivity.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"\nWrote {minutes_csv}")
    print(f"Wrote {conf_csv}")
    print(f"Wrote {meta_path}")


if __name__ == "__main__":
    main()
