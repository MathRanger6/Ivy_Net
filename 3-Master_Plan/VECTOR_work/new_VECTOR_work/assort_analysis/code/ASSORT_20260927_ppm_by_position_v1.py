#!/usr/bin/env python3
"""One descriptive 2015 points-per-minute distribution by source position."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
REPO = HERE.parents[5]
BASE = "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/"
STEM = "ASSORT_20260927_ppm_by_position_v1"
SOURCE_REL = "datasets/mbb/mbb_df_player_box.csv"
PLAYERS_REL = BASE + "outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
AUDIT_RECORD_REL = BASE + "docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json"
CODE_REL = BASE + "code/" + STEM + ".py"
OUT_REL = BASE + "outputs/ppm_by_position_2015/"
RECORD_REL = BASE + "docs/run_records/" + STEM + "_run_record.json"
MAIN_POSITIONS = ("guard", "forward", "center")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarize(values: pd.Series) -> dict:
    a = values.to_numpy(dtype=float)
    return {
        "players": len(a),
        "mean": float(np.mean(a)),
        "median": float(np.median(a)),
        "p10": float(np.percentile(a, 10)),
        "p90": float(np.percentile(a, 90)),
        "p99": float(np.percentile(a, 99)),
        "maximum": float(np.max(a)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="execute the one descriptive plot")
    args = parser.parse_args()
    if not args.run:
        parser.error("pass --run to execute")

    audit = json.loads((REPO / AUDIT_RECORD_REL).read_text())
    entries = [item for item in audit["outputs"] if item["path"] == PLAYERS_REL]
    if len(entries) != 1 or sha256(REPO / PLAYERS_REL) != entries[0]["sha256"]:
        raise ValueError("accepted player file differs from its run record")
    if sha256(REPO / SOURCE_REL) != audit["frozen_game_file_sha256"]:
        raise ValueError("frozen game source differs from accepted audit input")
    players = pd.read_csv(REPO / PLAYERS_REL, usecols=[
        "athlete_id", "team_id", "points_per_minute", "minutes", "played_appearances",
    ])
    if len(players) != 4267 or players.athlete_id.nunique() != 4267:
        raise ValueError("unexpected accepted player population")

    columns = ["season", "athlete_id", "team_id", "athlete_position_name"]
    parts = []
    for chunk in pd.read_csv(REPO / SOURCE_REL, usecols=columns, chunksize=200_000, low_memory=False):
        season = pd.to_numeric(chunk["season"], errors="coerce")
        parts.append(chunk.loc[season.eq(2015), columns[1:]].copy())
    box = pd.concat(parts, ignore_index=True)
    rows = box.merge(players[["athlete_id", "team_id"]], on=["athlete_id", "team_id"],
                     how="inner", validate="many_to_one")
    rows["source_position"] = rows.athlete_position_name.astype("string").str.strip().str.lower()
    categories = rows.groupby(["athlete_id", "team_id"])["source_position"].nunique(dropna=True)
    if len(categories) != len(players) or not categories.eq(1).all():
        raise ValueError("missing or inconsistent source position for an accepted player")
    positions = rows.drop_duplicates(["athlete_id", "team_id"])[
        ["athlete_id", "team_id", "source_position"]
    ]
    work = players.merge(positions, on=["athlete_id", "team_id"], validate="one_to_one")
    if len(work) != 4267 or not np.isfinite(work.points_per_minute).all():
        raise ValueError("invalid merged player/position values")
    counts = work.source_position.value_counts().to_dict()
    if not set(MAIN_POSITIONS).issubset(counts):
        raise ValueError("one of the expected main source positions is missing")
    summary = {
        "season": 2015,
        "accepted_players": len(work),
        "position_source": "athlete_position_name in frozen ESPN-derived game box",
        "label_rule": "exact consistent source position per accepted athlete and team; no hybrid reassignment",
        "main_plot_categories": list(MAIN_POSITIONS),
        "all_source_position_counts": {str(k): int(v) for k, v in counts.items()},
        "main_position_ppm": {
            position: summarize(work.loc[work.source_position.eq(position), "points_per_minute"])
            for position in MAIN_POSITIONS
        },
        "hybrid_and_unavailable_excluded_from_three_panel_plot": int(
            (~work.source_position.isin(MAIN_POSITIONS)).sum()
        ),
        "unit": "raw season total points divided by total verified season minutes",
        "interpretation_limit": "observed scoring rate, not position-adjusted talent",
    }

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir = REPO / OUT_REL
    out_dir.mkdir(parents=True, exist_ok=False)
    values_rel = OUT_REL + STEM + "_player_values.csv"
    summary_rel = OUT_REL + STEM + "_summary.json"
    image_rel = OUT_REL + STEM + "_distribution.png"
    work.to_csv(REPO / values_rel, index=False)
    (REPO / summary_rel).write_text(json.dumps(summary, indent=2) + "\n")

    maximum = float(work.points_per_minute.max())
    bin_width = 0.025
    bins = np.arange(0, maximum + 2 * bin_width, bin_width)
    palette = {"guard": "#285A83", "forward": "#23796F", "center": "#A65437"}
    fig, axes = plt.subplots(3, 1, figsize=(9.2, 9.1), sharex=True, sharey=True)
    for ax, position in zip(axes, MAIN_POSITIONS):
        group = work.loc[work.source_position.eq(position), "points_per_minute"]
        ax.hist(group, bins=bins, weights=np.full(len(group), 100 / len(group)),
                color=palette[position], edgecolor="white", linewidth=0.25)
        median = float(group.median())
        ax.axvline(median, color="#292929", linestyle="--", linewidth=1.4)
        ax.text(0.98, 0.88, f"{position.title()} · n={len(group):,} · median={median:.3f}",
                transform=ax.transAxes, ha="right", va="top", fontsize=11,
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85})
        ax.grid(axis="y", alpha=0.2)
        ax.set_axisbelow(True)
    axes[1].set_ylabel("Percentage of players in position per 0.025 PPM bin")
    axes[-1].set_xlabel("Season points per minute (PPM)")
    axes[-1].set_xlim(0, bins[-1])
    fig.suptitle("2015 men's basketball: observed scoring rate by source position", fontsize=16)
    excluded = summary["hybrid_and_unavailable_excluded_from_three_panel_plot"]
    fig.text(0.5, 0.01,
             f"Accepted player pool; {excluded} hybrid/unavailable labels shown in summary, not reassigned. Each panel sums to 100%.",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.035, 1, 0.96))
    fig.savefig(REPO / image_rel, dpi=200, facecolor="white")
    plt.close(fig)

    run_record = {
        "status": "executed_unreviewed",
        "timestamp": datetime.now().astimezone().isoformat(),
        "code": CODE_REL,
        "code_sha256": sha256(REPO / CODE_REL),
        "inputs": [
            {"path": PLAYERS_REL, "sha256": sha256(REPO / PLAYERS_REL), "run_record": AUDIT_RECORD_REL},
            {"path": SOURCE_REL, "sha256": audit["frozen_game_file_sha256"]},
        ],
        "position_rule": summary["label_rule"],
        "ppm_rule": summary["unit"],
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "outputs": [
            {"path": rel, "sha256": sha256(REPO / rel), "bytes": (REPO / rel).stat().st_size}
            for rel in (values_rel, summary_rel, image_rel)
        ],
    }
    (REPO / RECORD_REL).write_text(json.dumps(run_record, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
