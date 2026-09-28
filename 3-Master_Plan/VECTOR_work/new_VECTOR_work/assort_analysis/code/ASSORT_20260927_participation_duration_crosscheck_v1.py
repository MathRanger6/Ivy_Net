#!/usr/bin/env python3
"""Describe 2015 appearance frequency jointly with minutes per appearance."""

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
STEM = "ASSORT_20260927_participation_duration_crosscheck_v1"
BASE = "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/"
PLAYERS_REL = BASE + "outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
PLAYERS_RECORD_REL = BASE + "docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json"
GAMES_REL = BASE + "outputs/games_played_2015/ASSORT_20260927_games_played_distributions_v1_player_values.csv"
GAMES_RECORD_REL = BASE + "docs/run_records/ASSORT_20260927_games_played_distributions_v1_run_record.json"
CODE_REL = BASE + "code/" + STEM + ".py"
OUT_REL = BASE + "outputs/participation_duration_2015/"
RECORD_REL = BASE + "docs/run_records/" + STEM + "_run_record.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verified_output(path_rel: str, record_rel: str) -> None:
    record = json.loads((REPO / record_rel).read_text())
    entries = [item for item in record["outputs"] if item["path"] == path_rel]
    if len(entries) != 1 or sha256(REPO / path_rel) != entries[0]["sha256"]:
        raise ValueError(f"saved input differs from run record: {path_rel}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="run the bounded descriptive comparison")
    args = parser.parse_args()
    if not args.run:
        parser.error("pass --run to execute")
    verified_output(PLAYERS_REL, PLAYERS_RECORD_REL)
    verified_output(GAMES_REL, GAMES_RECORD_REL)

    players = pd.read_csv(REPO / PLAYERS_REL)
    games = pd.read_csv(REPO / GAMES_REL)
    if len(players) != 4267 or len(games) != 4267:
        raise ValueError("unexpected saved-player population")
    if players.athlete_id.duplicated().any() or games.athlete_id.duplicated().any():
        raise ValueError("duplicate athlete")
    work = players[[
        "athlete_id", "team_id", "minutes", "played_appearances",
        "minutes_per_played_appearance", "qualifies_five_minutes",
    ]].merge(
        games[["athlete_id", "team_id", "captured_team_games", "percentage_of_captured_team_games"]],
        on=["athlete_id", "team_id"], how="inner", validate="one_to_one",
    )
    if len(work) != 4267:
        raise ValueError("population mismatch after merge")
    if not np.allclose(work.minutes / work.played_appearances, work.minutes_per_played_appearance):
        raise ValueError("minutes-per-appearance mismatch")
    if not np.all(work.qualifies_five_minutes == work.minutes_per_played_appearance.ge(5)):
        raise ValueError("five-minute flag mismatch")
    if not np.allclose(
        100 * work.played_appearances / work.captured_team_games,
        work.percentage_of_captured_team_games,
    ):
        raise ValueError("captured-game percentage mismatch")

    frequency_edges = [0, 25, 50, 75, 90, 101]
    frequency_labels = ["<25%", "25–<50%", "50–<75%", "75–<90%", "90–100%"]
    duration_edges = [0, 5, 10, 20, np.inf]
    duration_labels = ["<5 min", "5–<10 min", "10–<20 min", "≥20 min"]
    work["frequency_band"] = pd.cut(
        work.percentage_of_captured_team_games,
        bins=frequency_edges, labels=frequency_labels, right=False,
    )
    work["duration_band"] = pd.cut(
        work.minutes_per_played_appearance,
        bins=duration_edges, labels=duration_labels, right=False,
    )
    if work[["frequency_band", "duration_band"]].isna().any().any():
        raise ValueError("unbinned values")
    count_table = pd.crosstab(work.duration_band, work.frequency_band, dropna=False)
    if int(count_table.to_numpy().sum()) != 4267:
        raise ValueError("cross-tab does not include every player")
    percent_table = count_table / 4267 * 100

    # Illustrative extremes only: these are descriptions, not proposed filters.
    short = work.minutes_per_played_appearance.lt(5)
    perennial = work.percentage_of_captured_team_games.ge(90)
    occasional = work.percentage_of_captured_team_games.lt(25)
    long = work.minutes_per_played_appearance.ge(20)
    summary = {
        "season": 2015,
        "eligible_players": len(work),
        "short_stint_under_five_minutes_per_played_appearance": int(short.sum()),
        "short_stint_and_90_percent_or_more_captured_games": int((short & perennial).sum()),
        "short_stint_and_under_25_percent_captured_games": int((short & occasional).sum()),
        "long_stint_20_minutes_or_more_and_under_25_percent_captured_games": int((long & occasional).sum()),
        "under_25_percent_captured_games_all_durations": int(occasional.sum()),
        "90_percent_or_more_captured_games_all_durations": int(perennial.sum()),
        "descriptive_only": "display bands and illustrative extremes are not new eligibility rules",
        "minutes_denominator": "positive-minute player appearances",
        "games_denominator": "captured team games, not verified complete official schedule",
    }
    summary["short_stint_fraction_perennial"] = (
        summary["short_stint_and_90_percent_or_more_captured_games"] / int(short.sum())
    )
    summary["short_stint_fraction_occasional"] = (
        summary["short_stint_and_under_25_percent_captured_games"] / int(short.sum())
    )

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir = REPO / OUT_REL
    out_dir.mkdir(parents=True, exist_ok=False)
    values_rel = OUT_REL + STEM + "_player_values.csv"
    counts_rel = OUT_REL + STEM + "_cross_tab_counts.csv"
    summary_rel = OUT_REL + STEM + "_summary.json"
    heatmap_rel = OUT_REL + STEM + "_heatmap.png"
    short_rel = OUT_REL + STEM + "_short_vs_other_frequency.png"
    work.to_csv(REPO / values_rel, index=False)
    count_table.to_csv(REPO / counts_rel)
    (REPO / summary_rel).write_text(json.dumps(summary, indent=2) + "\n")

    fig, ax = plt.subplots(figsize=(10, 6))
    image = ax.imshow(count_table.to_numpy(), cmap="Blues", aspect="auto")
    ax.set_xticks(range(len(frequency_labels)), labels=frequency_labels)
    ax.set_yticks(range(len(duration_labels)), labels=duration_labels)
    ax.set(xlabel="Share of team's captured games with positive minutes",
           ylabel="Average minutes per positive-minute appearance",
           title="2015 men's basketball: participation frequency and duration (n=4,267)")
    for row in range(len(duration_labels)):
        for col in range(len(frequency_labels)):
            count = int(count_table.iloc[row, col])
            color = "white" if count > count_table.to_numpy().max() * 0.55 else "#152335"
            ax.text(col, row, f"{count:,}", ha="center", va="center", color=color, fontsize=12)
    fig.colorbar(image, ax=ax, label="Eligible players", shrink=0.8)
    fig.text(0.5, 0.015, "Display bands only; they are not eligibility cutoffs. Games denominator is captured team games.",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(REPO / heatmap_rel, dpi=200, facecolor="white")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.4))
    x = np.arange(len(frequency_labels))
    short_counts = count_table.loc["<5 min"].to_numpy(dtype=float)
    other_counts = count_table.loc[duration_labels[1:]].sum(axis=0).to_numpy(dtype=float)
    width = 0.4
    ax.bar(x - width / 2, 100 * short_counts / short_counts.sum(), width=width,
           color="#A65437", label=f"Under 5 minutes (n={int(short.sum()):,})")
    ax.bar(x + width / 2, 100 * other_counts / other_counts.sum(), width=width,
           color="#285A83", label=f"At least 5 minutes (n={int((~short).sum()):,})")
    ax.set_xticks(x, labels=frequency_labels)
    ax.set(xlabel="Share of team's captured games with positive minutes",
           ylabel="Percentage within each minutes-per-appearance group",
           title="2015 men's basketball: how often did short-stint players appear?")
    ax.grid(axis="y", alpha=0.22)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    fig.text(0.5, 0.015, "The 5-minute line is the earlier audit boundary; percentage bands are descriptive only.",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(REPO / short_rel, dpi=200, facecolor="white")
    plt.close(fig)

    run_record = {
        "status": "executed_unreviewed",
        "timestamp": datetime.now().astimezone().isoformat(),
        "code": CODE_REL,
        "code_sha256": sha256(REPO / CODE_REL),
        "inputs": [
            {"path": PLAYERS_REL, "sha256": sha256(REPO / PLAYERS_REL), "run_record": PLAYERS_RECORD_REL},
            {"path": GAMES_REL, "sha256": sha256(REPO / GAMES_REL), "run_record": GAMES_RECORD_REL},
        ],
        "parameters": {
            "frequency_bands_percent": frequency_edges,
            "minutes_per_appearance_bands": ["<5", "5–<10", "10–<20", "≥20"],
            "extreme_examples": ["<25% captured games", "≥90% captured games"],
            "new_filter_applied": False,
        },
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "outputs": [
            {"path": rel, "sha256": sha256(REPO / rel), "bytes": (REPO / rel).stat().st_size}
            for rel in (values_rel, counts_rel, summary_rel, heatmap_rel, short_rel)
        ],
    }
    (REPO / RECORD_REL).write_text(json.dumps(run_record, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print("\nCross-tabulation (player counts):")
    print(count_table.to_string())
    print("\nCross-tabulation (percent of all eligible players):")
    print(percent_table.round(2).to_string())


if __name__ == "__main__":
    main()
