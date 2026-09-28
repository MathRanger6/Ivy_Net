#!/usr/bin/env python3
"""2015 high-minute rotation interval diagnostic (SCOUT mission Sep 27, 2026).

Reads the accepted rotation-audit player file only. Does not rebuild panel,
re-standardize, or touch shared sports/ entry points.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[5]
BASE = Path(__file__).resolve().parents[1]
STEM = "ASSORT_20260927_rotation_core_intervals_v1"
INPUT_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/"
    "rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
)
AUDIT_RECORD_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/"
    "run_records/ASSORT_20260927_rotation_audit_v1_run_record.json"
)
CODE_REL = f"3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/{STEM}.py"
OUT_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/"
    "rotation_core_intervals_2015/"
)
RECORD_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/"
    f"run_records/{STEM}_run_record.json"
)
REPORT_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/"
    f"results/{STEM}_report.md"
)

ROTATION_K = 10
N_RANDOM_DRAWS = 100
MASTER_SEED = 20260927
COVERAGE_GRID_POINTS = 400
TEAM_MIN_PLAYERS = 2

# Preselected before analysis: 12 team_ids at evenly spaced ranks (all-player mean order).
PRESELECT_RANKS = [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 350]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_and_validate(input_path: Path, audit_record_path: Path) -> pd.DataFrame:
    audit_record = json.loads(audit_record_path.read_text())
    matching = [e for e in audit_record["outputs"] if e["path"] == INPUT_REL]
    if len(matching) != 1 or sha256(input_path) != matching[0]["sha256"]:
        raise ValueError("player input SHA-256 does not match rotation audit run record")

    frame = pd.read_csv(input_path, compression="gzip")
    required = ["athlete_id", "team_id", "minutes", "points_per_minute", "ability_standardized"]
    if not set(required).issubset(frame.columns):
        raise ValueError(f"missing columns; need {required}")
    if len(frame) != 4267 or frame["athlete_id"].nunique() != 4267:
        raise ValueError("expected 4267 unique athletes")
    if frame["team_id"].nunique() != 351:
        raise ValueError("expected 351 teams")
    for col in ("minutes", "points_per_minute", "ability_standardized"):
        if not np.isfinite(frame[col].to_numpy(dtype=float)).all():
            raise ValueError(f"non-finite values in {col}")
    if (frame["minutes"] < 0).any():
        raise ValueError("negative minutes")
    return frame


def interval_stats(sub: pd.DataFrame) -> dict:
    a = sub["ability_standardized"].to_numpy(dtype=float)
    m = sub["minutes"].to_numpy(dtype=float)
    lo, hi = float(a.min()), float(a.max())
    return {
        "n": int(len(sub)),
        "a_min": lo,
        "a_max": hi,
        "a_mean": float(a.mean()),
        "width": hi - lo,
        "minutes_sum": float(m.sum()),
    }


def select_high_minute(team: pd.DataFrame, k: int) -> pd.DataFrame:
    kj = min(k, len(team))
    sort = team.sort_values(
        ["minutes", "athlete_id"],
        ascending=[False, True],
        kind="mergesort",
    )
    return sort.head(kj).copy()


def coverage_curve(lo: np.ndarray, hi: np.ndarray, grid: np.ndarray) -> np.ndarray:
    cover = np.zeros(grid.size, dtype=np.int64)
    for a, b in zip(lo, hi):
        cover += (grid >= a) & (grid <= b)
    return cover


def build_team_table(frame: pd.DataFrame, rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
    teams = []
    selections = []
    random_widths = np.full((N_RANDOM_DRAWS, 351), np.nan)
    team_ids_ordered = []

    for tid, grp in frame.groupby("team_id", sort=True):
        grp = grp.copy()
        n_elig = len(grp)
        kj = min(ROTATION_K, n_elig)
        all_stats = interval_stats(grp)
        high = select_high_minute(grp, ROTATION_K)
        high_stats = interval_stats(high)
        high_ids = set(high["athlete_id"].tolist())
        omitted = grp.loc[~grp["athlete_id"].isin(high_ids)]

        team_elig_minutes = float(grp["minutes"].sum())
        high_min_share = high_stats["minutes_sum"] / team_elig_minutes if team_elig_minutes > 0 else np.nan

        for _, row in high.iterrows():
            selections.append(
                {
                    "team_id": tid,
                    "athlete_id": int(row["athlete_id"]),
                    "case": "high_minute",
                    "minutes": float(row["minutes"]),
                    "ability_standardized": float(row["ability_standardized"]),
                }
            )
        for _, row in omitted.iterrows():
            selections.append(
                {
                    "team_id": tid,
                    "athlete_id": int(row["athlete_id"]),
                    "case": "omitted_from_high_minute",
                    "minutes": float(row["minutes"]),
                    "ability_standardized": float(row["ability_standardized"]),
                }
            )

        min_player = grp.loc[grp["ability_standardized"].idxmin()]
        max_player = grp.loc[grp["ability_standardized"].idxmax()]
        omit_min = int(min_player["athlete_id"]) not in high_ids
        omit_max = int(max_player["athlete_id"]) not in high_ids

        draw_widths = []
        for d in range(N_RANDOM_DRAWS):
            if kj >= n_elig:
                w = all_stats["width"]
            else:
                idx = rng.choice(n_elig, size=kj, replace=False)
                sub = grp.iloc[idx]
                w = interval_stats(sub)["width"]
            draw_widths.append(w)
        draw_widths_arr = np.array(draw_widths, dtype=float)
        team_idx = len(team_ids_ordered)
        random_widths[:, team_idx] = draw_widths_arr
        team_ids_ordered.append(int(tid))

        teams.append(
            {
                "team_id": int(tid),
                "eligible_n": n_elig,
                "k_j": kj,
                "omitted_n": n_elig - kj,
                "all_a_min": all_stats["a_min"],
                "all_a_max": all_stats["a_max"],
                "all_a_mean": all_stats["a_mean"],
                "all_width": all_stats["width"],
                "high_a_min": high_stats["a_min"],
                "high_a_max": high_stats["a_max"],
                "high_a_mean": high_stats["a_mean"],
                "high_width": high_stats["width"],
                "high_minutes_sum": high_stats["minutes_sum"],
                "eligible_minutes_sum": team_elig_minutes,
                "high_minute_share_of_team_minutes": high_min_share,
                "width_change_high_minus_all": high_stats["width"] - all_stats["width"],
                "random_width_mean": float(draw_widths_arr.mean()),
                "random_width_median": float(np.median(draw_widths_arr)),
                "random_width_p025": float(np.percentile(draw_widths_arr, 2.5)),
                "random_width_p975": float(np.percentile(draw_widths_arr, 97.5)),
                "omit_original_min_player": omit_min,
                "omit_original_max_player": omit_max,
                "high_equals_all": kj >= n_elig,
            }
        )

    team_df = pd.DataFrame(teams)
    if len(team_df) != 351:
        raise ValueError("team table length mismatch")
    sel_df = pd.DataFrame(selections)
    return team_df, sel_df, random_widths


def integrity_checks(team_df: pd.DataFrame, grid: np.ndarray, cover_all: np.ndarray, cover_high: np.ndarray, cover_rand_median: np.ndarray):
    if not (team_df["high_width"] <= team_df["all_width"] + 1e-12).all():
        raise AssertionError("high-minute width exceeds all-player width")
    if not (team_df["high_a_min"] >= team_df["all_a_min"] - 1e-12).all():
        raise AssertionError("high-minute min below all-player min")
    if not (team_df["high_a_max"] <= team_df["all_a_max"] + 1e-12).all():
        raise AssertionError("high-minute max above all-player max")
    if (cover_high > cover_all).any():
        raise AssertionError("high-minute coverage exceeds all-player on grid")
    if (cover_rand_median > cover_all).any():
        raise AssertionError("random median coverage exceeds all-player on grid")


def write_figure(
    team_df: pd.DataFrame,
    grid: np.ndarray,
    cover_all: np.ndarray,
    cover_high: np.ndarray,
    cover_rand_median: np.ndarray,
    cover_rand_p10: np.ndarray,
    cover_rand_p90: np.ndarray,
    preselect_ids: list[int],
    png_path: Path,
) -> None:
    xlab = "Standardized observed season points per minute"
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1.0])

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.fill_between(grid, cover_all, step="mid", alpha=0.25, color="steelblue", label="All eligible")
    ax0.plot(grid, cover_high, color="darkorange", lw=2, label="Top 10 by minutes")
    ax0.plot(grid, cover_rand_median, color="gray", lw=1.5, ls="--", label="Random 10 (median of 100 draws)")
    ax0.fill_between(
        grid,
        cover_rand_p10,
        cover_rand_p90,
        color="gray",
        alpha=0.15,
        label="Random 10 (10th–90th pct across draws)",
    )
    ax0.set_xlabel(xlab, fontsize=10)
    ax0.set_ylabel("Team-seasons covering this level", fontsize=10)
    ax0.set_title("Interval overlap — three cases (common grid)", fontsize=11)
    ax0.legend(fontsize=8, loc="upper right")
    ax0.axhline(1, color="0.5", ls=":", lw=1)

    ax1 = fig.add_subplot(gs[0, 1])
    w = team_df["all_width"].to_numpy()
    ax1.hist(w, bins=35, color="steelblue", alpha=0.5, label="All eligible")
    ax1.hist(team_df["high_width"], bins=35, color="darkorange", alpha=0.5, label="Top 10 minutes")
    ax1.axvline(team_df["random_width_median"].median(), color="gray", ls="--", label="Random 10 median width (team-level medians)")
    ax1.set_xlabel("Interval width (max − min ability)", fontsize=10)
    ax1.set_ylabel("Team count", fontsize=10)
    ax1.set_title("Width distributions", fontsize=11)
    ax1.legend(fontsize=8)

    ax2 = fig.add_subplot(gs[1, 0])
    sub = team_df.sort_values("all_a_mean").reset_index(drop=True)
    x = sub["all_width"].to_numpy()
    y = sub["high_width"].to_numpy()
    rm = sub["random_width_median"].to_numpy()
    ax2.scatter(x, y, c="darkorange", s=18, alpha=0.7, label="High-minute width")
    ax2.scatter(x, rm, c="gray", s=12, alpha=0.5, label="Random-10 median width")
    lim = max(x.max(), y.max(), rm.max()) * 1.05
    ax2.plot([0, lim], [0, lim], "k:", lw=1)
    ax2.set_xlabel("All-player width", fontsize=10)
    ax2.set_ylabel("Subset width", fontsize=10)
    ax2.set_title("Paired widths (351 teams)", fontsize=11)
    ax2.legend(fontsize=8)

    ax3 = fig.add_subplot(gs[1, 1])
    plot_teams = team_df.loc[team_df["team_id"].isin(preselect_ids)].copy()
    plot_teams = plot_teams.sort_values("all_a_mean")
    ypos = np.arange(len(plot_teams))
    for i, row in enumerate(plot_teams.itertuples()):
        ax3.hlines(i, row.all_a_min, row.all_a_max, colors="steelblue", lw=3, alpha=0.85)
        ax3.scatter(row.all_a_mean, i, color="steelblue", s=40, zorder=3)
        if not row.high_equals_all:
            ax3.hlines(i, row.high_a_min, row.high_a_max, colors="darkorange", lw=2, alpha=0.9)
            ax3.scatter(row.high_a_mean, i, color="crimson", s=36, zorder=4)
        else:
            ax3.scatter(row.high_a_mean, i, color="crimson", s=36, zorder=4)
    ax3.set_yticks(ypos)
    ax3.set_yticklabels([str(int(t)) for t in plot_teams["team_id"]], fontsize=7)
    ax3.set_xlabel(xlab, fontsize=10)
    ax3.set_ylabel("Preselected team_id (sorted by all-player mean)", fontsize=9)
    ax3.set_title("Interval bars: blue=all eligible; orange=top-10 minutes; dot=subset mean", fontsize=10)

    fig.suptitle(
        "2015 men's basketball — high-minute rotation interval diagnostic (SCOUT mission)",
        fontsize=12,
        y=0.98,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not args.run:
        parser.error("pass --run to execute")

    input_path = REPO / INPUT_REL
    audit_path = REPO / AUDIT_RECORD_REL
    frame = load_and_validate(input_path, audit_path)

    # Direct groupby cross-check (all-player case).
    direct = (
        frame.groupby("team_id")["ability_standardized"]
        .agg(["min", "max", "mean", "count"])
        .reset_index()
    )
    direct = direct.loc[direct["count"] >= TEAM_MIN_PLAYERS]

    rng = np.random.default_rng(MASTER_SEED)
    team_df, sel_df, random_widths = build_team_table(frame, rng)

    merged = team_df.merge(
        direct.rename(columns={"min": "chk_min", "max": "chk_max", "mean": "chk_mean"}),
        on="team_id",
    )
    if not np.allclose(merged["all_a_min"], merged["chk_min"], atol=1e-9):
        raise AssertionError("all_a_min mismatch vs direct groupby")
    if not np.allclose(merged["all_a_max"], merged["chk_max"], atol=1e-9):
        raise AssertionError("all_a_max mismatch vs direct groupby")

    grid = np.linspace(team_df["all_a_min"].min(), team_df["all_a_max"].max(), COVERAGE_GRID_POINTS)
    lo_all = team_df["all_a_min"].to_numpy()
    hi_all = team_df["all_a_max"].to_numpy()
    lo_high = team_df["high_a_min"].to_numpy()
    hi_high = team_df["high_a_max"].to_numpy()
    cover_all = coverage_curve(lo_all, hi_all, grid)
    cover_high = coverage_curve(lo_high, hi_high, grid)

    # Random draws: coverage per draw then summarize.
    cover_rand_stack = []
    team_groups = {tid: g for tid, g in frame.groupby("team_id", sort=True)}
    team_order = team_df["team_id"].tolist()
    for d in range(N_RANDOM_DRAWS):
        lo_d = []
        hi_d = []
        for tid in team_order:
            grp = team_groups[tid]
            n_elig = len(grp)
            kj = min(ROTATION_K, n_elig)
            if kj >= n_elig:
                st = interval_stats(grp)
            else:
                idx = rng.choice(n_elig, size=kj, replace=False)
                st = interval_stats(grp.iloc[idx])
            lo_d.append(st["a_min"])
            hi_d.append(st["a_max"])
        cover_rand_stack.append(coverage_curve(np.array(lo_d), np.array(hi_d), grid))
    cover_rand_stack = np.stack(cover_rand_stack, axis=0)
    cover_rand_median = np.median(cover_rand_stack, axis=0).astype(int)
    cover_rand_p10 = np.percentile(cover_rand_stack, 10, axis=0)
    cover_rand_p90 = np.percentile(cover_rand_stack, 90, axis=0)

    integrity_checks(team_df, grid, cover_all, cover_high, cover_rand_median)

    n_gt10 = int((team_df["eligible_n"] > ROTATION_K).sum())
    n_eq10 = int((team_df["eligible_n"] == ROTATION_K).sum())
    n_lt10 = int((team_df["eligible_n"] < ROTATION_K).sum())

    sorted_teams = team_df.sort_values("all_a_mean").reset_index(drop=True)
    preselect_ids = sorted_teams.iloc[PRESELECT_RANKS]["team_id"].astype(int).tolist()

    out_dir = REPO / OUT_REL
    out_dir.mkdir(parents=True, exist_ok=True)
    team_rel = OUT_REL + f"{STEM}_teams.csv"
    sel_rel = OUT_REL + f"{STEM}_player_selections.csv"
    rand_rel = OUT_REL + f"{STEM}_random_draw_team_widths.csv"
    grid_rel = OUT_REL + f"{STEM}_coverage_grid.csv"
    png_rel = OUT_REL + f"{STEM}_comparison.png"
    summary_rel = OUT_REL + f"{STEM}_summary.json"

    team_df.to_csv(REPO / team_rel, index=False)
    sel_df.to_csv(REPO / sel_rel, index=False)
    pd.DataFrame(
        random_widths,
        columns=[f"team_{tid}" for tid in team_order],
    ).to_csv(REPO / rand_rel, index=False)
    pd.DataFrame(
        {
            "grid": grid,
            "coverage_all": cover_all,
            "coverage_high_minute": cover_high,
            "coverage_random_median": cover_rand_median,
            "coverage_random_p10": cover_rand_p10,
            "coverage_random_p90": cover_rand_p90,
        }
    ).to_csv(REPO / grid_rel, index=False)

    write_figure(
        team_df,
        grid,
        cover_all,
        cover_high,
        cover_rand_median,
        cover_rand_p10,
        cover_rand_p90,
        preselect_ids,
        REPO / png_rel,
    )

    summary = {
        "design": {
            "season": 2015,
            "rotation_k": ROTATION_K,
            "random_draws": N_RANDOM_DRAWS,
            "master_seed": MASTER_SEED,
            "rng": "numpy.random.default_rng",
            "preselect_team_ranks": PRESELECT_RANKS,
            "preselected_team_ids": preselect_ids,
            "input": INPUT_REL,
            "input_sha256": sha256(input_path),
            "ability_column": "ability_standardized (frozen audit; not recomputed)",
        },
        "denominators": {
            "players": 4267,
            "teams": 351,
            "teams_with_more_than_10_eligible": n_gt10,
            "teams_with_exactly_10_eligible": n_eq10,
            "teams_with_fewer_than_10_eligible": n_lt10,
            "teams_unchanged_high_vs_all": int(team_df["high_equals_all"].sum()),
        },
        "omit_extremes": {
            "teams_omit_original_min_player": int(team_df["omit_original_min_player"].sum()),
            "teams_omit_original_max_player": int(team_df["omit_original_max_player"].sum()),
        },
        "width_all": {
            "mean": float(team_df["all_width"].mean()),
            "median": float(team_df["all_width"].median()),
            "max": float(team_df["all_width"].max()),
        },
        "width_high_minute": {
            "mean": float(team_df["high_width"].mean()),
            "median": float(team_df["high_width"].median()),
            "max": float(team_df["high_width"].max()),
        },
        "width_random_median_of_draws_per_team": {
            "mean": float(team_df["random_width_median"].mean()),
            "median": float(team_df["random_width_median"].median()),
        },
        "width_change_high_minus_all": {
            "mean": float(team_df["width_change_high_minus_all"].mean()),
            "median": float(team_df["width_change_high_minus_all"].median()),
        },
        "coverage_on_shared_grid": {
            "max_all": int(cover_all.max()),
            "mean_all": float(cover_all.mean()),
            "max_high": int(cover_high.max()),
            "mean_high": float(cover_high.mean()),
            "max_random_median": int(cover_rand_median.max()),
            "mean_random_median": float(cover_rand_median.mean()),
        },
        "high_minute_minute_share": {
            "mean_share_of_eligible_minutes": float(team_df["high_minute_share_of_team_minutes"].mean()),
            "median_share": float(team_df["high_minute_share_of_team_minutes"].median()),
        },
        "interpretation_guide": (
            "Compare high-minute narrowing to random-10 narrowing; "
            "subset intervals are nested in all-player intervals by construction."
        ),
    }
    (REPO / summary_rel).write_text(json.dumps(summary, indent=2) + "\n")

    outputs = [team_rel, sel_rel, rand_rel, grid_rel, png_rel, summary_rel]
    record = {
        "status": "executed_unreviewed",
        "timestamp": datetime.now().astimezone().isoformat(),
        "mission": (
            "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/scientific_questions/"
            "ASSORT_20260927_SCOUT_mission_high_minute_rotation_intervals.md"
        ),
        "code": CODE_REL,
        "code_sha256": sha256(REPO / CODE_REL),
        "input": INPUT_REL,
        "input_sha256": sha256(input_path),
        "audit_run_record": AUDIT_RECORD_REL,
        "parameters": summary["design"],
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "matplotlib": plt.matplotlib.__version__,
        "checks": [
            "input_sha256_vs_audit_record",
            "4267_players_351_teams",
            "all_player_intervals_match_groupby",
            "high_interval_subset_of_all",
            "coverage_high_le_all_on_grid",
            "deterministic_high_minute_ties_athlete_id",
        ],
        "outputs": [
            {"path": rel, "sha256": sha256(REPO / rel), "bytes": (REPO / rel).stat().st_size}
            for rel in outputs
        ],
    }
    (REPO / RECORD_REL).write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
