#!/usr/bin/env python3
"""2015 rotation interval diagnostic v2 — unified random draws + H_sort (SCOUT mission).

Version two: one random membership per draw drives width, coverage, and sorting index.
Does not overwrite v1 outputs.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import platform
import sys
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[5]
STEM = "ASSORT_20260927_rotation_core_intervals_v2"
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
ACCEPTED_FULL_H_SORT = 0.06194
H_SORT_TOL = 1e-4

ROTATION_K = 10
N_RANDOM_DRAWS = 100
MASTER_SEED = 20260927
COVERAGE_GRID_POINTS = 400
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
    for col in required[2:]:
        if not np.isfinite(frame[col].to_numpy(dtype=float)).all():
            raise ValueError(f"non-finite values in {col}")
    return frame


def h_sort_explicit(values: np.ndarray, team_idx: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    team_idx = np.asarray(team_idx, dtype=int)
    grand = values.mean()
    denom = np.square(values - grand).sum()
    if denom <= 0 or not np.isfinite(denom):
        raise ValueError("non-positive or non-finite H_sort denominator")
    n_team = int(team_idx.max()) + 1
    counts = np.bincount(team_idx, minlength=n_team)
    sums = np.bincount(team_idx, weights=values, minlength=n_team)
    means = sums / counts
    numer = np.square(values - means[team_idx]).sum()
    return float(1.0 - numer / denom)


def h_sort_repository(frame: pd.DataFrame, value_col: str) -> float:
    sys.path.insert(0, str(REPO / "sports"))
    grandchild = importlib.import_module("541_grandchild_homophily_assign")
    teams, _ = pd.factorize(frame["team_id"], sort=True)
    values = frame[value_col].to_numpy(dtype=float)
    return float(grandchild.realized_sorting_index_H_sort(values, teams.astype(np.int64)))


def select_high_minute_ids(grp: pd.DataFrame, k: int) -> list[int]:
    kj = min(k, len(grp))
    sort = grp.sort_values(["minutes", "athlete_id"], ascending=[False, True], kind="mergesort")
    return sort.head(kj)["athlete_id"].astype(int).tolist()


def random_team_ids(grp: pd.DataFrame, k: int, rng: np.random.Generator) -> list[int]:
    n = len(grp)
    kj = min(k, n)
    if kj >= n:
        return grp["athlete_id"].astype(int).tolist()
    pos = rng.choice(n, size=kj, replace=False)
    return grp.iloc[pos]["athlete_id"].astype(int).tolist()


def subset_frame(frame: pd.DataFrame, team_to_ids: dict[int, list[int]]) -> pd.DataFrame:
    parts = []
    for tid in sorted(team_to_ids.keys()):
        ids = set(team_to_ids[tid])
        part = frame.loc[(frame["team_id"] == tid) & (frame["athlete_id"].isin(ids))]
        if len(part) != len(ids):
            raise ValueError(f"team {tid}: selection size mismatch")
        parts.append(part)
    out = pd.concat(parts, ignore_index=True)
    return out


def team_interval_table(sub: pd.DataFrame) -> pd.DataFrame:
    iv = (
        sub.groupby("team_id", sort=True)["ability_standardized"]
        .agg(a_min="min", a_max="max", a_mean="mean", n="count")
        .reset_index()
    )
    iv["width"] = iv["a_max"] - iv["a_min"]
    return iv


def coverage_curve(lo: np.ndarray, hi: np.ndarray, grid: np.ndarray) -> np.ndarray:
    cover = np.zeros(grid.size, dtype=np.int64)
    for a, b in zip(lo, hi):
        cover += (grid >= a) & (grid <= b)
    return cover


def analytic_random_expectation(n_teams: int, n_players: int) -> float:
    if n_players <= 1:
        raise ValueError("invalid N for analytic expectation")
    return (n_teams - 1) / (n_players - 1)


def write_figure_v2_fixed(
    team_all: pd.DataFrame,
    team_high: pd.DataFrame,
    grid: np.ndarray,
    cover_all: np.ndarray,
    cover_high: np.ndarray,
    cover_rand_median: np.ndarray,
    cover_rand_p10: np.ndarray,
    cover_rand_p90: np.ndarray,
    width_all_mean: float,
    width_high_mean: float,
    width_rand_draw_mean: float,
    width_rand_team_median_secondary: float,
    preselect_ids: list[int],
    png_path: Path,
) -> None:
    xlab = "Standardized observed season points per minute"
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax0 = axes[0, 0]
    ax0.fill_between(grid, cover_all, step="mid", alpha=0.25, color="steelblue", label="All eligible")
    ax0.plot(grid, cover_high, color="darkorange", lw=2, label="Top 10 by minutes")
    ax0.plot(grid, cover_rand_median, color="gray", lw=1.5, ls="--", label="Random 10 (median curve)")
    ax0.fill_between(grid, cover_rand_p10, cover_rand_p90, color="gray", alpha=0.15)
    ax0.set_xlabel(xlab, fontsize=10)
    ax0.set_ylabel("Team-seasons covering this level", fontsize=10)
    ax0.set_title("Coverage on fixed grid", fontsize=11)
    ax0.legend(fontsize=7)

    ax1 = axes[0, 1]
    ax1.bar(
        [0, 1, 2],
        [width_all_mean, width_high_mean, width_rand_draw_mean],
        color=["steelblue", "darkorange", "gray"],
    )
    ax1.set_xticks([0, 1, 2])
    ax1.set_xticklabels(["All", "Top 10 min", "Random 10\n(draw-mean avg)"], fontsize=8)
    ax1.set_ylabel("Mean team interval width", fontsize=10)
    ax1.set_title("Headline widths (v2)", fontsize=11)

    ax2 = axes[1, 0]
    merged = team_all.merge(
        team_high[["team_id", "width"]].rename(columns={"width": "width_high"}),
        on="team_id",
    )
    ax2.scatter(merged["all_width"], merged["width_high"], c="darkorange", s=20, alpha=0.7)
    lim = max(merged["all_width"].max(), merged["width_high"].max()) * 1.05
    ax2.plot([0, lim], [0, lim], "k:", lw=1)
    ax2.set_xlabel("All-player width", fontsize=10)
    ax2.set_ylabel("Top-10-minute width", fontsize=10)

    ax3 = axes[1, 1]
    th_map = team_high.set_index("team_id")
    ta_map = team_all.set_index("team_id")
    plot_ids = [t for t in preselect_ids if t in ta_map.index]
    plot_ids = sorted(plot_ids, key=lambda t: ta_map.loc[t, "all_a_mean"])
    ypos = np.arange(len(plot_ids))
    for i, tid in enumerate(plot_ids):
        ra, rb = ta_map.loc[tid, "all_a_min"], ta_map.loc[tid, "all_a_max"]
        ax3.hlines(i, ra, rb, colors="steelblue", lw=3)
        ax3.scatter(ta_map.loc[tid, "all_a_mean"], i, color="steelblue", s=40, zorder=3)
        ha, hb = th_map.loc[tid, "a_min"], th_map.loc[tid, "a_max"]
        ax3.hlines(i, ha, hb, colors="darkorange", lw=2)
        ax3.scatter(th_map.loc[tid, "a_mean"], i, color="crimson", s=36, zorder=4)
    ax3.set_yticks(ypos)
    ax3.set_yticklabels([str(t) for t in plot_ids], fontsize=7)
    ax3.set_xlabel(xlab, fontsize=10)

    fig.suptitle("Rotation core intervals 2015 — v2", fontsize=12)
    fig.tight_layout()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(png_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def build_all_case_team_table(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[int, list[int]]]:
    """All-player and high-minute team intervals + player selection log."""
    teams_all = []
    selections = []
    high_map: dict[int, list[int]] = {}

    for tid, grp in frame.groupby("team_id", sort=True):
        n_elig = len(grp)
        kj = min(ROTATION_K, n_elig)
        st_all = team_interval_table(grp).iloc[0]
        high_ids = select_high_minute_ids(grp, ROTATION_K)
        high_map[tid] = high_ids
        high_sub = grp.loc[grp["athlete_id"].isin(high_ids)]
        st_high = team_interval_table(high_sub).iloc[0]

        min_id = int(grp.loc[grp["ability_standardized"].idxmin(), "athlete_id"])
        max_id = int(grp.loc[grp["ability_standardized"].idxmax(), "athlete_id"])
        high_set = set(high_ids)

        teams_all.append(
            {
                "team_id": int(tid),
                "eligible_n": n_elig,
                "k_j": kj,
                "all_a_min": st_all["a_min"],
                "all_a_max": st_all["a_max"],
                "all_a_mean": st_all["a_mean"],
                "all_width": st_all["width"],
                "high_a_min": st_high["a_min"],
                "high_a_max": st_high["a_max"],
                "high_a_mean": st_high["a_mean"],
                "high_width": st_high["width"],
                "omit_original_min": min_id not in high_set,
                "omit_original_max": max_id not in high_set,
                "high_equals_all": kj >= n_elig,
            }
        )
        for aid in high_ids:
            selections.append({"team_id": tid, "athlete_id": aid, "case": "high_minute"})
        for aid in grp["athlete_id"]:
            if int(aid) not in high_set:
                selections.append({"team_id": tid, "athlete_id": int(aid), "case": "omitted_high_minute"})

    team_all = pd.DataFrame(teams_all)
    if len(team_all) != 351:
        raise ValueError("expected 351 teams")
    return team_all, pd.DataFrame(selections), high_map


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not args.run:
        parser.error("pass --run to execute")

    input_path = REPO / INPUT_REL
    frame = load_and_validate(input_path, REPO / AUDIT_RECORD_REL)

    team_all, sel_high, high_map = build_all_case_team_table(frame)
    high_sub = subset_frame(frame, high_map)
    if len(high_sub) != 3501:
        raise ValueError(f"expected 3501 high-minute players, got {len(high_sub)}")

    teams_code, _ = pd.factorize(frame["team_id"], sort=True)
    h_full_a = h_sort_explicit(frame["ability_standardized"].to_numpy(), teams_code)
    h_full_ppm = h_sort_explicit(frame["points_per_minute"].to_numpy(), teams_code)
    h_full_gc_a = h_sort_repository(frame, "ability_standardized")
    h_full_gc_ppm = h_sort_repository(frame, "points_per_minute")
    if not np.isclose(h_full_a, h_full_ppm, atol=1e-10):
        raise AssertionError("H_sort mismatch ability vs ppm on full sample")
    if not np.isclose(h_full_a, h_full_gc_a, atol=1e-10):
        raise AssertionError("H_sort grandchild mismatch full ability")
    if abs(h_full_a - ACCEPTED_FULL_H_SORT) > H_SORT_TOL:
        raise ValueError(
            f"full H_sort {h_full_a} differs from accepted {ACCEPTED_FULL_H_SORT} beyond tolerance"
        )

    th_code, _ = pd.factorize(high_sub["team_id"], sort=True)
    h_high = h_sort_explicit(high_sub["ability_standardized"].to_numpy(), th_code)
    h_high_gc = h_sort_repository(high_sub, "ability_standardized")

    grid = np.linspace(team_all["all_a_min"].min(), team_all["all_a_max"].max(), COVERAGE_GRID_POINTS)
    team_high_iv = team_interval_table(high_sub)
    cover_all = coverage_curve(team_all["all_a_min"].to_numpy(), team_all["all_a_max"].to_numpy(), grid)
    cover_high = coverage_curve(team_high_iv["a_min"].to_numpy(), team_high_iv["a_max"].to_numpy(), grid)
    mean_cov_all = float(cover_all.mean())

    team_groups = {int(t): g for t, g in frame.groupby("team_id", sort=True)}
    team_order = sorted(team_groups.keys())
    kj_map = {tid: min(ROTATION_K, len(team_groups[tid])) for tid in team_order}

    rng = np.random.default_rng(MASTER_SEED)
    rep_rows = []
    membership_rows = []
    cover_stack = []
    random_team_widths = np.full((N_RANDOM_DRAWS, len(team_order)), np.nan)

    for draw in range(1, N_RANDOM_DRAWS + 1):
        team_to_ids = {
            tid: random_team_ids(team_groups[tid], ROTATION_K, rng) for tid in team_order
        }
        sub = subset_frame(frame, team_to_ids)
        if len(sub) != 3501:
            raise ValueError(f"draw {draw}: expected 3501 players, got {len(sub)}")
        for tid in team_order:
            for aid in team_to_ids[tid]:
                membership_rows.append({"draw": draw, "team_id": tid, "athlete_id": aid})

        iv = team_interval_table(sub)
        iv = iv.set_index("team_id").loc[team_order].reset_index()
        widths = iv["width"].to_numpy()
        random_team_widths[draw - 1, :] = widths
        mean_width = float(widths.mean())
        lo, hi = iv["a_min"].to_numpy(), iv["a_max"].to_numpy()
        cover = coverage_curve(lo, hi, grid)
        if (cover > cover_all).any():
            raise AssertionError(f"draw {draw}: coverage exceeds all-player")
        mean_cov = float(cover.mean())
        tc, _ = pd.factorize(sub["team_id"], sort=True)
        h = h_sort_explicit(sub["ability_standardized"].to_numpy(), tc)
        if draw <= 3:
            h_gc = h_sort_repository(sub, "ability_standardized")
            if not np.isclose(h, h_gc, atol=1e-10):
                raise AssertionError(f"draw {draw}: H_sort cross-check failed")

        rep_rows.append(
            {
                "draw": draw,
                "n_players": len(sub),
                "mean_team_width": mean_width,
                "mean_coverage_over_grid": mean_cov,
                "h_sort": h,
                "coverage_max": int(cover.max()),
            }
        )
        cover_stack.append(cover)

    rep_df = pd.DataFrame(rep_rows)
    cover_stack = np.stack(cover_stack, axis=0)
    cover_rand_median = np.median(cover_stack, axis=0)
    cover_rand_p10 = np.percentile(cover_stack, 10, axis=0)
    cover_rand_p90 = np.percentile(cover_stack, 90, axis=0)

    width_all_mean = float(team_all["all_width"].mean())
    width_high_mean = float(team_all["high_width"].mean())
    width_rand_draw_mean = float(rep_df["mean_team_width"].mean())
    width_rand_team_median_secondary = float(np.median(random_team_widths, axis=0).mean())

    mean_cov_high = float(cover_high.mean())
    mean_cov_rand_draw_level = float(rep_df["mean_coverage_over_grid"].mean())
    mean_cov_pointwise_median_curve = float(cover_rand_median.mean())

    sorted_teams = team_all.sort_values("all_a_mean").reset_index(drop=True)
    preselect_ids = sorted_teams.iloc[PRESELECT_RANKS]["team_id"].astype(int).tolist()

    out_dir = REPO / OUT_REL
    out_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "teams": OUT_REL + f"{STEM}_teams.csv",
        "selections": OUT_REL + f"{STEM}_player_selections_high_minute.csv",
        "membership": OUT_REL + f"{STEM}_random_membership.csv",
        "rep": OUT_REL + f"{STEM}_random_repetitions.csv",
        "team_widths": OUT_REL + f"{STEM}_random_team_widths.csv",
        "grid": OUT_REL + f"{STEM}_coverage_grid.csv",
        "h_sort": OUT_REL + f"{STEM}_sorting_index_summary.json",
        "png": OUT_REL + f"{STEM}_comparison.png",
        "summary": OUT_REL + f"{STEM}_summary.json",
    }

    team_all.to_csv(REPO / paths["teams"], index=False)
    sel_high.to_csv(REPO / paths["selections"], index=False)
    pd.DataFrame(membership_rows).to_csv(REPO / paths["membership"], index=False)
    rep_df.to_csv(REPO / paths["rep"], index=False)
    pd.DataFrame(random_team_widths, columns=[f"team_{t}" for t in team_order]).to_csv(
        REPO / paths["team_widths"], index=False
    )
    pd.DataFrame(
        {
            "grid": grid,
            "coverage_all": cover_all,
            "coverage_high_minute": cover_high,
            "coverage_random_median_curve": cover_rand_median,
            "coverage_random_p10": cover_rand_p10,
            "coverage_random_p90": cover_rand_p90,
        }
    ).to_csv(REPO / paths["grid"], index=False)

    write_figure_v2_fixed(
        team_all,
        team_high_iv,
        grid,
        cover_all,
        cover_high,
        cover_rand_median,
        cover_rand_p10,
        cover_rand_p90,
        width_all_mean,
        width_high_mean,
        width_rand_draw_mean,
        width_rand_team_median_secondary,
        preselect_ids,
        REPO / paths["png"],
    )

    exp_full = analytic_random_expectation(351, 4267)
    exp_sub = analytic_random_expectation(351, 3501)

    h_sort_summary = {
        "full_population": {
            "n_players": 4267,
            "n_teams": 351,
            "h_sort_ability_standardized": h_full_a,
            "h_sort_points_per_minute": h_full_ppm,
            "grandchild_crosscheck": h_full_gc_a,
            "accepted_reference": ACCEPTED_FULL_H_SORT,
            "analytic_assignment_expectation_if_reallocated": exp_full,
            "observed_minus_expectation": h_full_a - exp_full,
        },
        "fixed_top_ten_minutes": {
            "n_players": 3501,
            "h_sort": h_high,
            "grandchild_crosscheck": h_high_gc,
            "analytic_assignment_expectation_if_reallocated": exp_sub,
            "observed_minus_expectation": h_high - exp_sub,
        },
        "random_ten_within_team": {
            "n_draws": N_RANDOM_DRAWS,
            "h_sort_mean": float(rep_df["h_sort"].mean()),
            "h_sort_median": float(rep_df["h_sort"].median()),
            "h_sort_min": float(rep_df["h_sort"].min()),
            "h_sort_max": float(rep_df["h_sort"].max()),
            "h_sort_p025": float(rep_df["h_sort"].quantile(0.025)),
            "h_sort_p975": float(rep_df["h_sort"].quantile(0.975)),
            "note": "within-team subset draws; not random-assignment null",
        },
        "cross_checks": {
            "tolerance": H_SORT_TOL,
            "draws_grandchild_checked": [1, 2, 3],
        },
    }
    (REPO / paths["h_sort"]).write_text(json.dumps(h_sort_summary, indent=2) + "\n")

    summary = {
        "version": 2,
        "corrections_vs_v1": [
            "single random membership per draw for width, coverage, and H_sort",
            "headline random width = mean of draw-level mean team widths",
            "headline random coverage = mean of draw-level grid means",
        ],
        "design": {
            "master_seed": MASTER_SEED,
            "random_draws": N_RANDOM_DRAWS,
            "rotation_k": ROTATION_K,
            "input_sha256": sha256(input_path),
        },
        "width_headline": {
            "all_eligible_mean_team_width": width_all_mean,
            "top_ten_minutes_mean_team_width": width_high_mean,
            "random_ten_mean_of_draw_mean_widths": width_rand_draw_mean,
            "secondary_mean_of_team_median_widths_v1_style": width_rand_team_median_secondary,
        },
        "coverage_headline": {
            "all_mean_over_grid": mean_cov_all,
            "top_ten_mean_over_grid": mean_cov_high,
            "random_mean_of_draw_level_grid_means": mean_cov_rand_draw_level,
            "secondary_mean_of_pointwise_median_curve": mean_cov_pointwise_median_curve,
            "max_all": int(cover_all.max()),
            "max_high": int(cover_high.max()),
        },
        "h_sort_summary_path": paths["h_sort"],
        "membership_rows": len(membership_rows),
    }
    (REPO / paths["summary"]).write_text(json.dumps(summary, indent=2) + "\n")

    output_rels = list(paths.values())
    record = {
        "status": "executed_unreviewed",
        "timestamp": datetime.now().astimezone().isoformat(),
        "version": 2,
        "supersedes_statistics_only": "ASSORT_20260927_rotation_core_intervals_v1",
        "mission": (
            "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/scientific_questions/"
            "ASSORT_20260927_SCOUT_mission_high_minute_rotation_intervals.md"
        ),
        "code": CODE_REL,
        "code_sha256": sha256(REPO / CODE_REL),
        "input": INPUT_REL,
        "parameters": summary["design"],
        "checks_passed": [
            "input_hash",
            "4267_and_3501_counts",
            "full_h_sort_matches_accepted",
            "grandchild_h_sort_crosscheck",
            "unified_random_membership",
            "subset_coverage_le_all",
        ],
        "outputs": [
            {"path": rel, "sha256": sha256(REPO / rel), "bytes": (REPO / rel).stat().st_size}
            for rel in output_rels
        ],
    }
    (REPO / RECORD_REL).write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
