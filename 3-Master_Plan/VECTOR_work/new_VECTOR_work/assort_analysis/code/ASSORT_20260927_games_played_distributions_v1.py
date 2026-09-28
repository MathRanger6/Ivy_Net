#!/usr/bin/env python3
"""Plot 2015 eligible players' played games and share of captured team games."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
WORK = HERE.parents[1]
REPO = HERE.parents[5]
STEM = "ASSORT_20260927_games_played_distributions_v1"
SOURCE_REL = "datasets/mbb/mbb_df_player_box.csv"
AUDIT_INPUT_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/"
    "rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
)
AUDIT_RECORD_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/run_records/"
    "ASSORT_20260927_rotation_audit_v1_run_record.json"
)
READER_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/"
    "ASSORT_20260925_v1.py"
)
CODE_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/"
    + STEM + ".py"
)
OUT_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/"
    "games_played_2015/"
)
RECORD_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/run_records/"
    + STEM + "_run_record.json"
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def describe(values: pd.Series) -> dict:
    data = values.to_numpy(dtype=float)
    return {
        "minimum": float(data.min()),
        "p10": float(np.percentile(data, 10)),
        "p25": float(np.percentile(data, 25)),
        "median": float(np.median(data)),
        "mean": float(data.mean()),
        "p75": float(np.percentile(data, 75)),
        "p90": float(np.percentile(data, 90)),
        "maximum": float(data.max()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="run the frozen-input plot build")
    args = parser.parse_args()
    if not args.run:
        parser.error("pass --run to execute")

    record = json.loads((REPO / AUDIT_RECORD_REL).read_text())
    recorded_player = [item for item in record["outputs"] if item["path"] == AUDIT_INPUT_REL]
    if len(recorded_player) != 1:
        raise ValueError("audit record lacks the exact player input")
    if sha256(REPO / AUDIT_INPUT_REL) != recorded_player[0]["sha256"]:
        raise ValueError("audit player input checksum changed")
    if sha256(REPO / SOURCE_REL) != record["frozen_game_file_sha256"]:
        raise ValueError("frozen game source checksum changed")
    if sha256(REPO / READER_REL) != record["source_reader_sha256"]:
        raise ValueError("source reader checksum changed")

    players = pd.read_csv(REPO / AUDIT_INPUT_REL)
    if len(players) != 4267 or players.athlete_id.nunique() != 4267:
        raise ValueError("unexpected audit player count or duplicate athlete")

    spec = importlib.util.spec_from_file_location("assort_frozen_source_reader", REPO / READER_REL)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not import frozen source reader")
    reader = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reader)
    box, read_audit = reader.read_2015()
    box = box.loc[~box["athlete_display_name"].astype(str).str.strip().eq("-")]
    team_games = box.groupby("team_id", sort=True)["game_id"].nunique()
    team_games = team_games.loc[team_games.ge(11)].rename("captured_team_games")
    if len(team_games) != 351 or set(players.team_id) != set(team_games.index):
        raise ValueError("captured team-games population differs from player audit")

    output = players[["athlete_id", "team_id", "played_appearances", "captured_game_records"]].copy()
    output = output.merge(team_games, left_on="team_id", right_index=True, validate="many_to_one")
    output = output.rename(columns={"played_appearances": "games_with_positive_minutes"})
    if not (
        (output.games_with_positive_minutes >= 1)
        & (output.games_with_positive_minutes <= output.captured_game_records)
        & (output.captured_game_records <= output.captured_team_games)
    ).all():
        raise ValueError("invalid player/team game count ordering")
    output["percentage_of_captured_team_games"] = (
        100 * output.games_with_positive_minutes / output.captured_team_games
    )
    if not output.percentage_of_captured_team_games.between(0, 100).all():
        raise ValueError("invalid percentage")

    # Matplotlib is used only for two fixed descriptive figures, not model fitting.
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    output_dir = REPO / OUT_REL
    output_dir.mkdir(parents=True, exist_ok=False)
    data_rel = OUT_REL + STEM + "_player_values.csv"
    summary_rel = OUT_REL + STEM + "_summary.json"
    games_rel = OUT_REL + STEM + "_games_count.png"
    percentage_rel = OUT_REL + STEM + "_percentage_captured_team_games.png"
    output.to_csv(REPO / data_rel, index=False)

    n = len(output)
    games = output.games_with_positive_minutes
    fig, ax = plt.subplots(figsize=(9, 5.4))
    counts = games.value_counts().sort_index()
    ax.bar(counts.index, counts.values, width=0.86, color="#285A83", edgecolor="white", linewidth=0.3)
    ax.axvline(float(games.median()), color="#A3472B", linestyle="--", linewidth=1.7,
               label=f"Median: {games.median():.0f} games")
    ax.set(xlabel="Games with verified positive player minutes in 2015",
           ylabel="Eligible players",
           title=f"2015 men's basketball: games played per eligible player (n={n:,})")
    ax.set_xlim(0.5, max(counts.index) + 0.5)
    ax.set_xticks(np.arange(1, max(counts.index) + 1, 2))
    ax.grid(axis="y", alpha=0.22)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    fig.text(0.5, 0.015, "Played = positive verified minutes; incomplete game capture can shorten observed seasons.",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(REPO / games_rel, dpi=200, facecolor="white")
    plt.close(fig)

    pct = output.percentage_of_captured_team_games
    fig, ax = plt.subplots(figsize=(9, 5.4))
    edges = np.arange(0, 105, 5)
    ax.hist(pct, bins=edges, color="#23796F", edgecolor="white", linewidth=0.5)
    ax.axvline(float(pct.median()), color="#A3472B", linestyle="--", linewidth=1.7,
               label=f"Median: {pct.median():.1f}%")
    ax.set(xlabel="Percentage of team's captured 2015 games with positive player minutes",
           ylabel="Eligible players",
           title=f"2015 men's basketball: share of captured team games played (n={n:,})")
    ax.set_xlim(0, 100)
    ax.set_xticks(np.arange(0, 101, 10))
    ax.grid(axis="y", alpha=0.22)
    ax.set_axisbelow(True)
    ax.legend(frameon=False)
    fig.text(0.5, 0.015, "Denominator = team games in the frozen file, not the complete NCAA schedule.",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(REPO / percentage_rel, dpi=200, facecolor="white")
    plt.close(fig)

    summary = {
        "season": 2015,
        "eligible_players": n,
        "teams": len(team_games),
        "games_with_positive_minutes": describe(games),
        "percentage_of_captured_team_games": describe(pct),
        "captured_team_games": describe(team_games),
        "player_source": AUDIT_INPUT_REL,
        "team_denominator_source": SOURCE_REL,
        "source_rows_2015": read_audit["source_rows_2015"],
        "percentage_denominator_limitation": "captured team games, not a verified complete season schedule",
    }
    (REPO / summary_rel).write_text(json.dumps(summary, indent=2) + "\n")
    run_record = {
        "status": "executed_unreviewed",
        "timestamp": datetime.now().astimezone().isoformat(),
        "code": CODE_REL,
        "code_sha256": sha256(REPO / CODE_REL),
        "audit_input": AUDIT_INPUT_REL,
        "audit_input_sha256": sha256(REPO / AUDIT_INPUT_REL),
        "audit_run_record": AUDIT_RECORD_REL,
        "audit_run_record_sha256": sha256(REPO / AUDIT_RECORD_REL),
        "frozen_game_file": SOURCE_REL,
        "frozen_game_file_sha256": record["frozen_game_file_sha256"],
        "source_reader": READER_REL,
        "source_reader_sha256": sha256(REPO / READER_REL),
        "definition": "positive-minute player appearances / distinct captured team games; 2015 eligible audit players",
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "outputs": [
            {"path": rel, "sha256": sha256(REPO / rel), "bytes": (REPO / rel).stat().st_size}
            for rel in (data_rel, summary_rel, games_rel, percentage_rel)
        ],
    }
    (REPO / RECORD_REL).write_text(json.dumps(run_record, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
