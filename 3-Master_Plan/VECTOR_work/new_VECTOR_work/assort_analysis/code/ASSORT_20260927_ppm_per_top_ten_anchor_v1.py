#!/usr/bin/env python3
"""Fixed original top-ten-minute anchors for PPM/PER, with paired size references."""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[5]
WORK = REPO / "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis"
STEM = "ASSORT_20260927_ppm_per_top_ten_anchor_v1"
OUT = WORK / "outputs/ppm_per_top_ten_anchor_2015"
INPUT = WORK / "outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
INPUT_RECORD = WORK / "docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json"
MATCHED = REPO / "datasets/mbb/DO_NOT_ERASE/bpm_player_season_matched.csv"
OLD_ANCHORS = WORK / "outputs/rotation_core_intervals_2015/ASSORT_20260927_rotation_core_intervals_v2_player_selections_high_minute.csv"
OLD_RECORD = WORK / "docs/run_records/ASSORT_20260927_rotation_core_intervals_v2_run_record.json"
SEED = 20260927
DRAWS = 100
METRICS = [("points_per_minute", "PPM", "Points per minute"), ("PER", "PER", "Player Efficiency Rating")]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_recorded_input(path, record_path):
    record = json.loads(record_path.read_text())
    item = next(x for x in record["outputs"] if x["path"] == str(path.relative_to(REPO)))
    assert sha(path) == item["sha256"], f"Input hash mismatch: {path}"


def interval_table(frame, col):
    result = frame.groupby("team_id")[col].agg(n="size", low="min", high="max", mean="mean").reset_index()
    result["width_z"] = result.high - result.low
    return result


def h_sort(frame, col):
    values = frame[col].to_numpy()
    center = values.mean()
    total = np.square(values - center).sum()
    groups = frame.groupby("team_id")[col]
    group_means = groups.transform("mean").to_numpy()
    within = np.square(values - group_means).sum()
    ag = groups.agg(["size", "mean"])
    between = (ag["size"] * np.square(ag["mean"] - center)).sum()
    assert total > 0 and np.isclose(total, within + between, atol=1e-9, rtol=1e-12)
    assert np.isclose(between / total, 1 - within / total, atol=1e-12)
    return float(between / total)


def coverage(table, grid):
    return ((grid[None, :] >= table.low.to_numpy()[:, None]) & (grid[None, :] <= table.high.to_numpy()[:, None])).sum(axis=0)


def stats(frame, metric, case, grid):
    table = interval_table(frame, metric + "_z")
    cov = coverage(table, grid)
    result = {"metric": metric, "case": case, "players": len(frame), "teams": len(table), "H_sort": h_sort(frame, metric), "mean_width_z": float(table.width_z.mean()), "median_width_z": float(table.width_z.median()), "maximum_grid_coverage": int(cov.max()), "mean_grid_coverage": float(cov.mean())}
    assert np.isclose(result["H_sort"], h_sort(frame, metric + "_z"), atol=1e-12)
    return result, table, cov


def write_figure(summary, coverage_frame):
    grid = coverage_frame.standardized_value.to_numpy()
    metric_results = summary["metrics"]
    plt.rcParams.update({"font.size": 10})
    fig, axes = plt.subplots(3, 2, figsize=(13, 12), constrained_layout=True)
    width_limit = 1.25 * max(max(x["full"]["mean_width_z"], x["anchors"]["mean_width_z"], x["random"]["mean_width_z"]) for x in metric_results)
    sorting_limit = 1.25 * max(max(x["full"]["H_sort"], x["anchors"]["H_sort"], x["random"]["H_sort_mean"]) for x in metric_results)
    for column_index, (col, short, long_name) in enumerate(METRICS):
        ax = axes[0, column_index]
        ax.plot(grid, coverage_frame[f"{short}_all_coverage"], color="#245a81", label="All matched players")
        ax.plot(grid, coverage_frame[f"{short}_anchor_coverage"], color="#b55a23", label="Fixed minute anchors")
        ax.plot(grid, coverage_frame[f"{short}_random_median_coverage"], color="#666666", ls="--", label="Random subsets: median")
        ax.fill_between(grid, coverage_frame[f"{short}_random_p10_coverage"], coverage_frame[f"{short}_random_p90_coverage"], color="#666666", alpha=.15, label="Random subsets: central 80%")
        ax.set(title=long_name, xlabel=f"{short}: standard deviations from full matched-population mean", ylabel="Team intervals covering this value", ylim=(0, summary["common_teams"] + 10))
        ax.legend(fontsize=8)
        data = metric_results[column_index]
        labels = ["All matched", "Minute anchors", "Random mean"]
        for row_index, key, ylabel, limit in [(1, "mean_width_z", "Equal-team mean interval width (standard deviations)", width_limit), (2, "H_sort", "Overall sorting index (equal-player weighting)", sorting_limit)]:
            values = [data["full"][key], data["anchors"][key], data["random"][key + "_mean"] if key == "H_sort" else data["random"][key]]
            ax = axes[row_index, column_index]
            bars = ax.bar(labels, values, color=["#245a81", "#b55a23", "#777777"])
            ax.bar_label(bars, labels=[f"{x:.4f}" if key == "H_sort" else f"{x:.3f}" for x in values], padding=3)
            ax.set(ylabel=ylabel, ylim=(0, limit))
    fig.suptitle(f"2015 fixed top-ten-minute anchors: PPM and PER\n{summary['common_players']:,} matched players; {summary['available_anchors']:,} available original anchors; {summary['common_teams']} teams", fontsize=14)
    fig.savefig(OUT / f"{STEM}_comparison.png", dpi=160)
    plt.close(fig)


def main():
    if "--render-only" in sys.argv:
        summary = json.loads((OUT / f"{STEM}_summary.json").read_text())
        coverage_frame = pd.read_csv(OUT / f"{STEM}_coverage_grid.csv")
        record_path = WORK / f"docs/run_records/{STEM}_run_record.json"
        record = json.loads(record_path.read_text())
        for item in record["outputs"]:
            assert sha(REPO / item["path"]) == item["sha256"]
        figure_path = OUT / f"{STEM}_comparison.png"
        old_figure_sha = sha(figure_path)
        write_figure(summary, coverage_frame)
        for item in record["outputs"]:
            if item["path"] == str(figure_path.relative_to(REPO)):
                item.update(sha256=sha(figure_path), bytes=figure_path.stat().st_size)
        record["visual_amendment"] = {"reason": "Use identical width and sorting vertical scales across PPM and PER; numerical outputs unchanged.", "figure_sha256_before": old_figure_sha, "figure_sha256_after": sha(figure_path), "current_code_sha256": sha(Path(__file__)), "timestamp_utc": datetime.now(timezone.utc).isoformat()}
        record_path.write_text(json.dumps(record, indent=2) + "\n")
        print("Figure redrawn on common vertical scales; numerical output hashes unchanged.")
        return
    if list(OUT.glob(f"{STEM}*")):
        raise RuntimeError("Refusing to overwrite previous outputs")
    sources = [INPUT, INPUT_RECORD, MATCHED, OLD_ANCHORS, OLD_RECORD, Path(__file__)]
    source_hashes = {str(p.relative_to(REPO)): sha(p) for p in sources}
    verify_recorded_input(INPUT, INPUT_RECORD)
    verify_recorded_input(OLD_ANCHORS, OLD_RECORD)
    full = pd.read_csv(INPUT)
    assert len(full) == full.athlete_id.nunique() == 4267 and full.team_id.nunique() == 351
    ordered = full.sort_values(["team_id", "minutes", "athlete_id"], ascending=[True, False, True], kind="stable")
    original = ordered.groupby("team_id", sort=True).head(10)
    old = pd.read_csv(OLD_ANCHORS)
    old = old.loc[old["case"] == "high_minute"]
    assert set(zip(original.team_id, original.athlete_id)) == set(zip(old.team_id, old.athlete_id))
    assert len(original) == 3501
    anchor_ids = set(original.athlete_id)
    full["original_anchor"] = full.athlete_id.isin(anchor_ids)
    full["season"] = 2015
    matched = pd.read_csv(MATCHED, low_memory=False)
    matched = matched.loc[matched.season == 2015, ["athlete_id", "season", "team_id", "PER"]]
    assert not matched.duplicated(["athlete_id", "season", "team_id"]).any()
    joined = full.merge(matched, on=["athlete_id", "season", "team_id"], how="left", validate="one_to_one")
    joined["PER"] = pd.to_numeric(joined.PER, errors="coerce")
    joined["comparison_eligible"] = np.isfinite(joined.PER) & np.isfinite(joined.points_per_minute)
    common = joined.loc[joined.comparison_eligible].sort_values(["team_id", "athlete_id"]).reset_index(drop=True)
    assert len(common) == 4163 and common.team_id.nunique() == 350
    for col, _, _ in METRICS:
        common[col + "_z"] = (common[col] - common[col].mean()) / common[col].std(ddof=0)
    high = common.loc[common.original_anchor].copy()
    target_counts = high.groupby("team_id").size()
    assert set(target_counts.index) == set(common.team_id) and target_counts.min() > 0
    count_table = joined.groupby("team_id").agg(team_name=("team_short_display_name_x", "first"), full_players=("athlete_id", "size"), original_anchors=("original_anchor", "sum"), available_players=("comparison_eligible", "sum"))
    count_table["available_anchors"] = target_counts.reindex(count_table.index).fillna(0).astype(int)
    count_table["unavailable_anchors"] = count_table.original_anchors - count_table.available_anchors
    grid = np.linspace(min(common[col + "_z"].min() for col, _, _ in METRICS), max(common[col + "_z"].max() for col, _, _ in METRICS), 801)
    fixed_results, fixed_tables, fixed_cov = [], [], {}
    for col, _, _ in METRICS:
        for case, frame in [("All matched players", common), ("Fixed minute anchors", high)]:
            result, table, cov = stats(frame, col, case, grid)
            table["metric"], table["case"] = col, case
            fixed_results.append(result)
            fixed_tables.append(table)
            fixed_cov[col, case] = cov
        assert np.all(fixed_cov[col, "Fixed minute anchors"] <= fixed_cov[col, "All matched players"])
    all_tables = {col: interval_table(common, col + "_z").set_index("team_id") for col, _, _ in METRICS}
    rng = np.random.default_rng(SEED)
    team_rows = [(tid, grp.index.to_numpy(), int(target_counts.loc[tid])) for tid, grp in common.groupby("team_id", sort=True)]
    random_results, memberships = [], []
    random_cov = {col: [] for col, _, _ in METRICS}
    for draw in range(1, DRAWS + 1):
        indices = np.concatenate([rng.choice(rows, size=count, replace=False) for _, rows, count in team_rows])
        sub = common.loc[indices]
        assert len(sub) == len(high) and sub.athlete_id.is_unique
        assert sub.groupby("team_id").size().equals(target_counts)
        member = sub[["team_id", "athlete_id"]].copy()
        member["draw"] = draw
        memberships.append(member)
        for col, _, _ in METRICS:
            result, table, cov = stats(sub, col, "Random matched-size subset", grid)
            assert np.all(cov <= fixed_cov[col, "All matched players"])
            check = table.set_index("team_id").join(all_tables[col][["low", "high"]], rsuffix="_all")
            assert (check.low >= check.low_all).all() and (check.high <= check.high_all).all()
            result["draw"] = draw
            random_results.append(result)
            random_cov[col].append(cov)
    random_frame = pd.DataFrame(random_results)
    summary_metrics = []
    coverage_frame = pd.DataFrame({"standardized_value": grid})
    for col, short, long_name in METRICS:
        fixed_all = next(x for x in fixed_results if x["metric"] == col and x["case"] == "All matched players")
        fixed_high = next(x for x in fixed_results if x["metric"] == col and x["case"] == "Fixed minute anchors")
        draws = random_frame.loc[random_frame.metric == col]
        curve = np.asarray(random_cov[col])
        for case, key in [("All matched players", "all"), ("Fixed minute anchors", "anchor")]:
            coverage_frame[f"{short}_{key}_coverage"] = fixed_cov[col, case]
        for q, key in [(0.1, "p10"), (0.5, "median"), (0.9, "p90")]:
            coverage_frame[f"{short}_random_{key}_coverage"] = np.quantile(curve, q, axis=0)
        summary_metrics.append({"metric": long_name, "column": col, "full": fixed_all, "anchors": fixed_high, "random": {"draws": DRAWS, "H_sort_mean": float(draws.H_sort.mean()), "H_sort_median": float(draws.H_sort.median()), "H_sort_min": float(draws.H_sort.min()), "H_sort_max": float(draws.H_sort.max()), "draws_H_sort_at_or_above_anchor": int((draws.H_sort >= fixed_high["H_sort"]).sum()), "mean_width_z": float(draws.mean_width_z.mean()), "mean_width_min": float(draws.mean_width_z.min()), "mean_width_max": float(draws.mean_width_z.max()), "draws_width_at_or_below_anchor": int((draws.mean_width_z <= fixed_high["mean_width_z"]).sum()), "maximum_grid_coverage_median": float(draws.maximum_grid_coverage.median())}})
    lost = joined.loc[joined.original_anchor & ~joined.comparison_eligible]
    summary = {"season": 2015, "original_players": len(full), "original_teams": int(full.team_id.nunique()), "original_anchors": len(original), "common_players": len(common), "common_teams": int(common.team_id.nunique()), "comparison_excluded_players": int((~joined.comparison_eligible).sum()), "available_anchors": len(high), "unavailable_original_anchors": len(lost), "minimum_available_anchors_per_comparison_team": int(target_counts.min()), "maximum_available_anchors_per_comparison_team": int(target_counts.max()), "comparison_teams_below_ten_available_anchors": int((target_counts < 10).sum()), "teams_unavailable_for_comparison": count_table.loc[count_table.available_players == 0].reset_index().to_dict("records"), "anchor_minus_full_H_sort_PER_minus_PPM": (summary_metrics[1]["anchors"]["H_sort"] - summary_metrics[1]["full"]["H_sort"]) - (summary_metrics[0]["anchors"]["H_sort"] - summary_metrics[0]["full"]["H_sort"]), "metrics": summary_metrics}
    OUT.mkdir(parents=True, exist_ok=True)
    export = {"player_membership.csv": joined, "common_players.csv": common, "unavailable_anchors.csv": lost, "team_counts.csv": count_table.reset_index(), "fixed_team_intervals.csv": pd.concat(fixed_tables), "fixed_summary.csv": pd.DataFrame(fixed_results), "random_repetitions.csv": random_frame, "random_membership.csv": pd.concat(memberships), "coverage_grid.csv": coverage_frame}
    for suffix, frame in export.items():
        frame.to_csv(OUT / f"{STEM}_{suffix}", index=False)
    (OUT / f"{STEM}_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    write_figure(summary, coverage_frame)
    assert source_hashes == {str(p.relative_to(REPO)): sha(p) for p in sources}
    record = {"status": "executed_pending_review", "timestamp_utc": datetime.now(timezone.utc).isoformat(), "inputs_and_code_sha256": source_hashes, "parameters": {"anchor_definition": "original full-audit top ten total minutes per team, ties by athlete_id, no replacement for missing PER", "comparison_population": "finite PER and PPM; BPM not required", "master_seed": SEED, "draws": DRAWS, "rng": type(rng.bit_generator).__name__, "subset_counts": "per-team available original anchor counts", "standardization": "fixed per metric on common full matched population, population SD", "grid_points": len(grid), "grid_min": float(grid.min()), "grid_max": float(grid.max())}, "python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "matplotlib": matplotlib.__version__, "checks": ["accepted_input_hash", "anchor_input_hash", "original_anchor_identity_agreement", "paired_metric_identity_and_random_membership", "exact_per_team_counts", "subset_interval_and_grid_coverage_containment", "sorting_variance_decomposition", "sorting_scale_invariance", "unchanged_source_hashes"], "outputs": [{"path": str(p.relative_to(REPO)), "sha256": sha(p), "bytes": p.stat().st_size} for p in sorted(OUT.glob(f"{STEM}*"))]}
    (WORK / f"docs/run_records/{STEM}_run_record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(summary, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
