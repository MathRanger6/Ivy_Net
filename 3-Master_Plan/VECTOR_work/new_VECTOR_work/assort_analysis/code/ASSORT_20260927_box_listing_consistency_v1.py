#!/usr/bin/env python3
"""Audit whether 2015 game-box listing is a stable roster-presence proxy."""

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
WORK = HERE.parents[1]
BASE = "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/"
STEM = "ASSORT_20260927_box_listing_consistency_v1"
SOURCE_REL = "datasets/mbb/mbb_df_player_box.csv"
PLAYERS_REL = BASE + "outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
AUDIT_RECORD_REL = BASE + "docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json"
CODE_REL = BASE + "code/" + STEM + ".py"
OUT_REL = BASE + "outputs/box_listing_consistency_2015/"
RECORD_REL = BASE + "docs/run_records/" + STEM + "_run_record.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def quantiles(values: pd.Series) -> dict:
    a = pd.to_numeric(values, errors="coerce").dropna().to_numpy(dtype=float)
    if len(a) == 0:
        return {"count": 0}
    return {
        "count": len(a), "minimum": float(np.min(a)),
        "p10": float(np.percentile(a, 10)),
        "p25": float(np.percentile(a, 25)),
        "median": float(np.median(a)),
        "p75": float(np.percentile(a, 75)),
        "p90": float(np.percentile(a, 90)),
        "maximum": float(np.max(a)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="run the bounded source audit")
    args = parser.parse_args()
    if not args.run:
        parser.error("pass --run to execute")

    audit = json.loads((REPO / AUDIT_RECORD_REL).read_text())
    expected = {item["path"]: item["sha256"] for item in audit["outputs"]}
    if sha256(REPO / SOURCE_REL) != audit["frozen_game_file_sha256"]:
        raise ValueError("frozen game source differs from prior audit")
    if sha256(REPO / PLAYERS_REL) != expected[PLAYERS_REL]:
        raise ValueError("accepted player file differs from prior audit")
    for relative, key in (
        (audit["source_reader"], "source_reader_sha256"),
        (audit["source_recovery_overlay"], "source_recovery_overlay_sha256"),
        (audit["zero_minute_recovery_overlay"], "zero_minute_recovery_overlay_sha256"),
    ):
        if sha256(REPO / relative) != audit[key]:
            raise ValueError(f"source-recovery input changed: {relative}")

    import importlib.util

    source_code = WORK / "code/ASSORT_20260927_rotation_audit_v1.py"
    spec = importlib.util.spec_from_file_location("assort_rotation_source", source_code)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import verified rotation source routines")
    rotation = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rotation)
    reader = rotation.load_source_reader()
    box, read_audit = reader.read_2015()
    box, overlay_audit = rotation.apply_verified_minutes(box)
    box = box.loc[~box.athlete_display_name.astype(str).str.strip().eq("-")].copy()
    team_games = box.groupby("team_id")["game_id"].nunique()
    box = box.loc[box.team_id.isin(team_games.index[team_games.ge(11)])].copy()
    if box.team_id.nunique() != 351:
        raise ValueError("accepted team coverage differs from prior audit")
    duplicate = box.duplicated(["team_id", "game_id", "athlete_id"])
    if duplicate.any():
        raise ValueError(f"{int(duplicate.sum())} duplicated team-game-athlete rows")

    box["dnp_flag"] = box.did_not_play.eq(True)
    box["positive_minutes"] = box.minutes.gt(0)
    box["missing_minutes"] = box.minutes.isna()
    box["zero_minutes"] = box.minutes.eq(0)
    box["both_stats_missing"] = box.minutes.isna() & box.points.isna()
    box["active_true"] = box.active.eq(True)

    game = box.groupby(["team_id", "game_id"], as_index=False).agg(
        team_name=("team_short_display_name", "last"),
        listed_players=("athlete_id", "size"),
        positive_minute_players=("positive_minutes", "sum"),
        did_not_play_flags=("dnp_flag", "sum"),
        zero_minute_rows=("zero_minutes", "sum"),
        missing_minute_rows=("missing_minutes", "sum"),
        active_true_rows=("active_true", "sum"),
    )
    game["dnp_present"] = game.did_not_play_flags.gt(0)
    game["participant_only"] = game.did_not_play_flags.eq(0) & game.positive_minute_players.eq(game.listed_players)
    game["no_dnp_but_unplayed"] = game.did_not_play_flags.eq(0) & game.positive_minute_players.lt(game.listed_players)
    game["unplayed_listings"] = game.listed_players - game.positive_minute_players
    if not (game.listed_players >= game.positive_minute_players).all():
        raise ValueError("more positive-minute players than listings")

    team = game.groupby("team_id").agg(
        team_name=("team_name", "last"),
        captured_games=("game_id", "size"),
        median_listed=("listed_players", "median"),
        min_listed=("listed_players", "min"),
        max_listed=("listed_players", "max"),
        median_positive_minute_players=("positive_minute_players", "median"),
        games_with_dnp=("dnp_present", "sum"),
        participant_only_games=("participant_only", "sum"),
        no_dnp_but_unplayed_games=("no_dnp_but_unplayed", "sum"),
    ).reset_index()
    team["share_games_with_dnp"] = team.games_with_dnp / team.captured_games
    team["listing_range"] = team.max_listed - team.min_listed
    dnp_median = game.loc[game.dnp_present].groupby("team_id").listed_players.median()
    no_dnp_median = game.loc[~game.dnp_present].groupby("team_id").listed_players.median()
    team["median_listed_when_dnp_present"] = team.team_id.map(dnp_median)
    team["median_listed_when_no_dnp"] = team.team_id.map(no_dnp_median)
    team["mixed_game_listing_gap"] = (
        team.median_listed_when_dnp_present - team.median_listed_when_no_dnp
    )
    team["mixed_dnp_status"] = team.games_with_dnp.gt(0) & team.games_with_dnp.lt(team.captured_games)

    players = pd.read_csv(REPO / PLAYERS_REL)
    players = players[[
        "athlete_id", "team_id", "captured_game_records", "played_appearances",
        "minutes", "minutes_per_played_appearance",
    ]].merge(team[["team_id", "captured_games"]], on="team_id", validate="many_to_one")
    players["listed_game_share"] = players.captured_game_records / players.captured_games
    players["played_game_share"] = players.played_appearances / players.captured_games
    players["listing_minus_playing_share"] = players.listed_game_share - players.played_game_share
    if not (
        players.captured_game_records.ge(players.played_appearances)
        & players.captured_games.ge(players.captured_game_records)
    ).all():
        raise ValueError("accepted-player listed/played/team game counts are inconsistent")
    short = players.minutes_per_played_appearance.lt(5)

    flag = box.groupby(["dnp_flag", "active_true", "both_stats_missing", "positive_minutes"],
                       dropna=False).size().rename("rows").reset_index()
    summary = {
        "season": 2015,
        "team_count": len(team),
        "team_game_count": len(game),
        "source_rows_after_dash_and_team_coverage": len(box),
        "source_rows_2015": read_audit["source_rows_2015"],
        "verified_minutes_overlay": overlay_audit,
        "source_flag_counts": {
            "did_not_play_true_rows": int(box.dnp_flag.sum()),
            "active_true_rows": int(box.active_true.sum()),
            "both_stats_missing_rows": int(box.both_stats_missing.sum()),
            "dnp_true_with_positive_minutes": int((box.dnp_flag & box.positive_minutes).sum()),
            "dnp_true_with_nonmissing_minutes": int((box.dnp_flag & ~box.missing_minutes).sum()),
            "both_stats_missing_without_dnp_flag": int((box.both_stats_missing & ~box.dnp_flag).sum()),
        },
        "game_listing": {
            "listed_players": quantiles(game.listed_players),
            "positive_minute_players": quantiles(game.positive_minute_players),
            "unplayed_listings": quantiles(game.unplayed_listings),
            "games_with_any_dnp": int(game.dnp_present.sum()),
            "participant_only_games": int(game.participant_only.sum()),
            "no_dnp_but_unplayed_games": int(game.no_dnp_but_unplayed.sum()),
        },
        "team_listing": {
            "share_games_with_dnp": quantiles(team.share_games_with_dnp),
            "listing_range": quantiles(team.listing_range),
            "teams_dnp_every_game": int(team.games_with_dnp.eq(team.captured_games).sum()),
            "teams_dnp_no_games": int(team.games_with_dnp.eq(0).sum()),
            "teams_mixed_dnp_presence": int(team.mixed_dnp_status.sum()),
            "mixed_teams_dnp_game_median_listing_at_least_three_higher": int(
                (team.mixed_dnp_status & team.mixed_game_listing_gap.ge(3)).sum()
            ),
            "mixed_game_listing_gap": quantiles(team.mixed_game_listing_gap),
        },
        "accepted_players": {
            "count": len(players),
            "listed_game_share": quantiles(players.listed_game_share),
            "played_game_share": quantiles(players.played_game_share),
            "listed_at_least_half_team_games": int(players.listed_game_share.ge(0.5).sum()),
            "listed_at_least_half_and_played_under_half": int(
                (players.listed_game_share.ge(0.5) & players.played_game_share.lt(0.5)).sum()
            ),
            "under_five_minutes_per_played_appearance": int(short.sum()),
            "under_five_and_listed_at_least_half_team_games": int(
                (short & players.listed_game_share.ge(0.5)).sum()
            ),
        },
        "interpretation_limit": "internal box-listing consistency cannot establish complete true rosters",
    }

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir = REPO / OUT_REL
    out_dir.mkdir(parents=True, exist_ok=False)
    game_rel = OUT_REL + STEM + "_team_game.csv"
    team_rel = OUT_REL + STEM + "_team_summary.csv"
    player_rel = OUT_REL + STEM + "_accepted_players.csv"
    flag_rel = OUT_REL + STEM + "_source_flags.csv"
    summary_rel = OUT_REL + STEM + "_summary.json"
    plot_rel = OUT_REL + STEM + "_team_dnp_share.png"
    game.to_csv(REPO / game_rel, index=False)
    team.to_csv(REPO / team_rel, index=False)
    players.to_csv(REPO / player_rel, index=False)
    flag.to_csv(REPO / flag_rel, index=False)
    (REPO / summary_rel).write_text(json.dumps(summary, indent=2) + "\n")

    fig, ax = plt.subplots(figsize=(9, 5.4))
    ax.hist(100 * team.share_games_with_dnp, bins=np.arange(0, 110, 10),
            color="#285A83", edgecolor="white", linewidth=0.5)
    ax.set(xlabel="Percentage of captured games with at least one 'did not play' listing",
           ylabel="Teams",
           title="2015 men's basketball: consistency of no-play game-box listings")
    ax.set_xticks(np.arange(0, 101, 10))
    ax.set_xlim(0, 100)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)
    fig.text(0.5, 0.015, "351 accepted teams; a no-play listing is evidence in the box, not proof of a complete roster.",
             ha="center", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(REPO / plot_rel, dpi=200, facecolor="white")
    plt.close(fig)

    record = {
        "status": "executed_unreviewed",
        "timestamp": datetime.now().astimezone().isoformat(),
        "code": CODE_REL,
        "code_sha256": sha256(REPO / CODE_REL),
        "audit_run_record": AUDIT_RECORD_REL,
        "audit_run_record_sha256": sha256(REPO / AUDIT_RECORD_REL),
        "inputs": [
            {"path": SOURCE_REL, "sha256": audit["frozen_game_file_sha256"]},
            {"path": PLAYERS_REL, "sha256": expected[PLAYERS_REL]},
            {"path": audit["source_reader"], "sha256": audit["source_reader_sha256"]},
            {"path": audit["source_recovery_overlay"], "sha256": audit["source_recovery_overlay_sha256"]},
            {"path": audit["zero_minute_recovery_overlay"], "sha256": audit["zero_minute_recovery_overlay_sha256"]},
        ],
        "scope": "2015 accepted teams; all named source game-box rows; no eligibility change",
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
        "outputs": [
            {"path": rel, "sha256": sha256(REPO / rel), "bytes": (REPO / rel).stat().st_size}
            for rel in (game_rel, team_rel, player_rel, flag_rel, summary_rel, plot_rel)
        ],
    }
    (REPO / RECORD_REL).write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
