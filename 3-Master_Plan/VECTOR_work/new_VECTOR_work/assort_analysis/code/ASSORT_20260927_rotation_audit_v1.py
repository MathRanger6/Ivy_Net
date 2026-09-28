#!/usr/bin/env python3
"""Bounded 2015 basketball rotation and peer-pool audit.

This reads the frozen game file, applies the separately sourced six-game
minutes overlay, and writes only inside the VECTOR assortativity workspace.
It neither runs the assignment simulation nor computes a draft-outcome curve.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd


HERE = Path(__file__).resolve()
WORK = HERE.parents[1]
REPO = HERE.parents[5]
OLD_READER = HERE.parent / "ASSORT_20260925_v1.py"
SOURCE = REPO / "datasets/mbb/mbb_df_player_box.csv"
OVERLAY = WORK / "data/source_recovery_2015/minutes_recovery_overlay.csv"
ZERO_OVERLAY = WORK / "data/source_recovery_2015/ASSORT_20260927_zero_minutes_recovery_overlay.csv"
DATA_DIR = WORK / "data/rotation_audit_2015"
OUTPUT_DIR = WORK / "outputs/rotation_audit_2015"
RUN_DIR = WORK / "docs/run_records"
STEM = "ASSORT_20260927_rotation_audit_v1"
THRESHOLD = 5.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_source_reader():
    spec = importlib.util.spec_from_file_location("assort_20260925_source_reader", OLD_READER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load source reader: {OLD_READER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def apply_verified_minutes(box: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    overlay = pd.read_csv(OVERLAY, low_memory=False)
    if len(overlay) != 105 or not overlay["recovery_status"].eq("RECOVERED").all():
        raise ValueError("Six-game overlay differs from the 105 fully recovered rows")
    if overlay["source_data_row"].duplicated().any():
        raise ValueError("Duplicate source row in minutes overlay")
    fields = [
        "source_data_row", "game_id", "athlete_id", "team_id", "points",
        "athlete_display_name", "recovered_minutes",
    ]
    if overlay[fields].isna().any().any():
        raise ValueError("Missing overlay identity, points, name, or recovered minutes")
    checked = box.merge(
        overlay[fields].rename(columns={c: f"overlay_{c}" for c in fields if c != "source_data_row"}),
        on="source_data_row", how="left", validate="one_to_one", indicator=True,
    )
    matched = checked["_merge"].eq("both")
    if int(matched.sum()) != len(overlay):
        raise ValueError("Some overlay rows are absent from the frozen 2015 source")
    for key in ("game_id", "athlete_id", "team_id"):
        left = pd.to_numeric(checked.loc[matched, key], errors="coerce").to_numpy(dtype=float)
        right = pd.to_numeric(checked.loc[matched, f"overlay_{key}"], errors="coerce").to_numpy(dtype=float)
        if not np.array_equal(left, right):
            raise ValueError(f"Overlay mismatch on {key}")
    if not checked.loc[matched, "athlete_display_name"].eq(
        checked.loc[matched, "overlay_athlete_display_name"]
    ).all():
        raise ValueError("Overlay mismatch on athlete display name")
    if not np.array_equal(
        checked.loc[matched, "points"].to_numpy(dtype=float),
        checked.loc[matched, "overlay_points"].to_numpy(dtype=float),
    ):
        raise ValueError("Overlay mismatch on frozen points")
    if not checked.loc[matched, "minutes"].isna().all():
        raise ValueError("An overlay row already has minutes in the frozen source")
    recovered = checked.loc[matched, "overlay_recovered_minutes"].to_numpy(dtype=float)
    if not np.isfinite(recovered).all() or (recovered < 0).any():
        raise ValueError("Recovered minutes must be finite and nonnegative")
    checked.loc[matched, "minutes"] = recovered
    checked = checked[box.columns].copy()
    audit = {
        "overlay_rows_matched": int(matched.sum()),
        "overlay_positive_minute_rows": int((recovered > 0).sum()),
        "overlay_zero_minute_rows": int((recovered == 0).sum()),
        "overlay_recorded_points": float(overlay["points"].sum()),
    }

    zero_overlay = pd.read_csv(ZERO_OVERLAY, low_memory=False)
    if len(zero_overlay) != 37 or zero_overlay["source_data_row"].duplicated().any():
        raise ValueError("Positive-points/zero-minutes overlay must contain 37 unique rows")
    allowed = {"RECOVERED", "UNRESOLVED_MINUTES", "UNRESOLVED_NAME"}
    if set(zero_overlay.recovery_status) - allowed:
        raise ValueError("Unexpected status in positive-points/zero-minutes overlay")
    if int(zero_overlay.recovery_status.eq("RECOVERED").sum()) != 15:
        raise ValueError("Expected 15 independently recovered zero-minute rows")
    zero_fields = [
        "source_data_row", "game_id", "athlete_id", "team_id", "athlete_display_name",
        "minutes", "points", "recovery_status", "recovered_minutes",
    ]
    zero = checked.merge(
        zero_overlay[zero_fields].rename(columns={c: f"zero_{c}" for c in zero_fields if c != "source_data_row"}),
        on="source_data_row", how="left", validate="one_to_one", indicator="_zero_match",
    )
    found = zero["_zero_match"].eq("both")
    if int(found.sum()) != len(zero_overlay):
        raise ValueError("A zero-minute anomaly row is absent from the frozen 2015 source")
    for key in ("game_id", "athlete_id", "team_id"):
        if not np.array_equal(
            pd.to_numeric(zero.loc[found, key], errors="coerce").to_numpy(dtype=float),
            pd.to_numeric(zero.loc[found, f"zero_{key}"], errors="coerce").to_numpy(dtype=float),
        ):
            raise ValueError(f"Zero-minute overlay mismatch on {key}")
    if not zero.loc[found, "athlete_display_name"].eq(
        zero.loc[found, "zero_athlete_display_name"]
    ).all():
        raise ValueError("Zero-minute overlay mismatch on athlete name")
    if not np.array_equal(
        zero.loc[found, "points"].to_numpy(dtype=float),
        zero.loc[found, "zero_points"].to_numpy(dtype=float),
    ) or not zero.loc[found, "minutes"].eq(0).all():
        raise ValueError("Zero-minute overlay does not match the frozen points/zero minutes")
    recovered_zero = found & zero.zero_recovery_status.eq("RECOVERED")
    unresolved_zero = found & ~zero.zero_recovery_status.eq("RECOVERED")
    positive_minutes = zero.loc[recovered_zero, "zero_recovered_minutes"].to_numpy(dtype=float)
    if not np.isfinite(positive_minutes).all() or not (positive_minutes > 0).all():
        raise ValueError("Recovered zero-minute rows require positive verified minutes")
    zero.loc[recovered_zero, "minutes"] = positive_minutes
    zero["excluded_source_points"] = 0.0
    zero["excluded_source_row"] = 0
    zero.loc[unresolved_zero, "excluded_source_points"] = zero.loc[unresolved_zero, "points"]
    zero.loc[unresolved_zero, "excluded_source_row"] = 1
    zero.loc[unresolved_zero, "points"] = 0.0
    audit.update({
        "zero_minute_positive_point_rows_matched": int(found.sum()),
        "zero_minute_positive_point_rows_recovered": int(recovered_zero.sum()),
        "zero_minute_positive_point_rows_fallback": int(unresolved_zero.sum()),
        "zero_minute_positive_point_fallback_points": float(zero.loc[unresolved_zero, "excluded_source_points"].sum()),
    })
    return zero[list(box.columns) + ["excluded_source_points", "excluded_source_row"]].copy(), audit


def select_canonical(candidate: pd.DataFrame, key: str, include_zero: bool) -> pd.DataFrame:
    work = candidate if include_zero else candidate.loc[
        candidate.groupby("athlete_id")["total_minutes"].transform("max").gt(0)
    ]
    ordered = work.sort_values(
        ["athlete_id", key, "total_minutes", "team_id"],
        ascending=[True, False, False, True], kind="stable",
    )
    top = ordered.drop_duplicates("athlete_id", keep="first")
    tied = work.merge(
        top[["athlete_id", key, "total_minutes"]],
        on=["athlete_id", key, "total_minutes"], how="inner",
    )
    tied = tied.loc[tied.duplicated("athlete_id", keep=False)]
    if not tied.empty:
        raise ValueError(
            f"{tied.athlete_id.nunique()} unresolved canonical-team ties under {key}; "
            f"athlete IDs: {sorted(tied.athlete_id.unique().tolist())[:20]}"
        )
    return top[["athlete_id", "team_id"]].rename(columns={"team_id": f"{key}_team_id"})


def quantiles(values: pd.Series) -> dict:
    clean = pd.to_numeric(values, errors="coerce").dropna().to_numpy(dtype=float)
    if len(clean) == 0:
        return {"count": 0}
    return {
        "count": int(len(clean)), "minimum": float(clean.min()),
        "p10": float(np.quantile(clean, 0.10)),
        "median": float(np.median(clean)),
        "p90": float(np.quantile(clean, 0.90)),
        "maximum": float(clean.max()), "mean": float(clean.mean()),
    }


def build() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    reader = load_source_reader()
    box, source_audit = reader.read_2015()
    source_audit["source_rows_2015_recorded_points"] = float(box.points.sum())
    box, overlay_audit = apply_verified_minutes(box)
    source_audit.update(overlay_audit)

    dash = box["athlete_display_name"].astype(str).str.strip().eq("-")
    source_audit["dash_name_rows_removed"] = int(dash.sum())
    box = box.loc[~dash].copy()
    team_games = box.groupby("team_id")["game_id"].nunique()
    source_audit["teams_before_coverage"] = int(len(team_games))
    source_audit["teams_after_coverage"] = int(team_games.ge(11).sum())
    box = box.loc[box["team_id"].isin(team_games.index[team_games.ge(11)])].copy()

    box["positive_minute_game"] = box["game_id"].where(box["minutes"].gt(0))
    candidate = box.groupby(["athlete_id", "team_id"], as_index=False).agg(
        captured_games=("game_id", "nunique"),
        played_games=("positive_minute_game", "nunique"),
        total_minutes=("minutes", "sum"),
        game_rows=("game_id", "size"),
        athlete_display_name=("athlete_display_name", "last"),
        team_short_display_name=("team_short_display_name", "last"),
    )
    old_choice = select_canonical(candidate, "captured_games", include_zero=True)
    new_choice = select_canonical(candidate, "played_games", include_zero=False)
    comparison = old_choice.merge(new_choice, on="athlete_id", how="left", validate="one_to_one")
    comparison["changed"] = comparison["captured_games_team_id"].ne(
        comparison["played_games_team_id"]
    ) & comparison["played_games_team_id"].notna()
    comparison["multi_team"] = comparison["athlete_id"].isin(
        candidate.groupby("athlete_id").size().loc[lambda s: s.gt(1)].index
    )
    candidate = candidate.merge(comparison, on="athlete_id", validate="many_to_one")
    candidate["old_selected"] = candidate["team_id"].eq(candidate["captured_games_team_id"])
    candidate["new_selected"] = candidate["team_id"].eq(candidate["played_games_team_id"])
    chosen_old = candidate.loc[candidate["old_selected"], ["athlete_id", "total_minutes"]].rename(
        columns={"total_minutes": "old_selected_minutes"}
    )
    chosen_new = candidate.loc[candidate["new_selected"], ["athlete_id", "total_minutes"]].rename(
        columns={"total_minutes": "new_selected_minutes"}
    )
    comparison = comparison.merge(chosen_old, on="athlete_id", validate="one_to_one")
    comparison = comparison.merge(chosen_new, on="athlete_id", how="left", validate="one_to_one")
    changed = candidate.loc[candidate["changed"] & candidate["multi_team"]].copy()
    incidence = {
        "all_athletes_after_coverage": int(candidate.athlete_id.nunique()),
        "multi_team_athletes": int(comparison.multi_team.sum()),
        "multi_team_with_any_played_minutes": int(
            (comparison.multi_team & comparison.played_games_team_id.notna()).sum()
        ),
        "multi_team_assignment_changes": int((comparison.multi_team & comparison.changed).sum()),
        "changes_from_zero_minute_to_positive_minute_team": int((
            comparison.multi_team & comparison.changed
            & comparison.old_selected_minutes.eq(0)
            & comparison.new_selected_minutes.gt(0)
        ).sum()),
        "changed_athletes_eligible_under_new_rule": int((
            comparison.multi_team & comparison.changed
            & comparison.new_selected_minutes.ge(20)
        ).sum()),
        "all_zero_minute_athletes_not_assigned": int(
            comparison.played_games_team_id.isna().sum()
        ),
    }

    box = box.merge(new_choice, on="athlete_id", how="inner", validate="many_to_one")
    box = box.loc[box["team_id"].eq(box["played_games_team_id"])].copy()
    duplicate_game = box.duplicated(["athlete_id", "team_id", "game_id"], keep=False)
    if duplicate_game.any():
        raise ValueError(f"{int(duplicate_game.sum())} retained rows duplicate player-team-game keys")
    both_missing = box["minutes"].isna() & box["points"].isna()
    unexpected_both = both_missing & ~box["did_not_play"].eq(True)
    partial = box["minutes"].isna() ^ box["points"].isna()
    if unexpected_both.any() or partial.any():
        raise ValueError(
            f"Unresolved source statistics: {int(unexpected_both.sum())} both-missing; "
            f"{int(partial.sum())} partial"
        )
    if box["minutes"].lt(0).any() or box["points"].lt(0).any():
        raise ValueError("Negative minutes or points in retained source")
    positive_points_zero_minutes = box.loc[
        box["minutes"].eq(0) & box["points"].gt(0),
        ["source_data_row", "game_id", "athlete_id", "athlete_display_name", "team_id", "minutes", "points"],
    ]
    if not positive_points_zero_minutes.empty:
        season_minutes = box.groupby("athlete_id")["minutes"].sum()
        affected_ids = positive_points_zero_minutes["athlete_id"].unique()
        eligible_affected = int(season_minutes.reindex(affected_ids).ge(20).sum())
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        positive_points_zero_minutes.to_csv(
            DATA_DIR / f"{STEM}_zero_minutes_positive_points_stop.csv", index=False
        )
        affected_game_teams = box.loc[
            box.game_id.isin(positive_points_zero_minutes.game_id.unique())
        ].groupby(["game_id", "team_id", "team_short_display_name"], as_index=False).agg(
            recorded_player_minutes=("minutes", "sum"),
            recorded_points=("points", "sum"),
            player_rows=("athlete_id", "size"),
        )
        affected_game_teams.to_csv(
            DATA_DIR / f"{STEM}_zero_minutes_affected_game_teams_stop.csv", index=False
        )
        (DATA_DIR / f"{STEM}_source_check_stop.json").write_text(json.dumps({
            "status": "stopped_before_audit_result",
            "canonical_team_incidence_preliminary": incidence,
            "zero_minute_positive_point_rows": int(len(positive_points_zero_minutes)),
            "affected_games": int(positive_points_zero_minutes.game_id.nunique()),
            "affected_athletes": int(len(affected_ids)),
            "affected_athletes_with_at_least_twenty_other_minutes": eligible_affected,
            "recorded_points_on_these_rows": float(positive_points_zero_minutes.points.sum()),
        }, indent=2, sort_keys=True) + "\n")
        raise ValueError(
            f"Canonical incidence so far: {incidence}. "
            f"{len(positive_points_zero_minutes)} retained rows have positive points and zero minutes "
            f"across {positive_points_zero_minutes.game_id.nunique()} games and "
            f"{positive_points_zero_minutes.athlete_id.nunique()} athletes "
            f"({eligible_affected} at or above twenty other recorded minutes); "
            f"their points sum to {positive_points_zero_minutes.points.sum()}; "
            f"examples: {positive_points_zero_minutes.head(12).to_dict('records')}"
        )
    source_audit["expected_no_play_rows_after_canonical"] = int(both_missing.sum())
    source_audit["retained_game_rows_after_canonical"] = int(len(box))
    source_audit["retained_duplicate_player_team_game_rows"] = 0
    source_audit["fallback_rows_after_canonical"] = int(box.excluded_source_row.sum())
    source_audit["fallback_points_after_canonical"] = float(box.excluded_source_points.sum())

    panel = box.groupby(["athlete_id", "team_id"], as_index=False).agg(
        athlete_display_name=("athlete_display_name", "last"),
        team_short_display_name=("team_short_display_name", "last"),
        points=("points", "sum"), minutes=("minutes", "sum"),
        excluded_source_points=("excluded_source_points", "sum"),
        excluded_source_rows=("excluded_source_row", "sum"),
        captured_game_records=("game_id", "nunique"),
        played_appearances=("positive_minute_game", "nunique"),
    )
    panel = panel.loc[panel.minutes.ge(20)].copy()
    if panel.athlete_id.duplicated().any() or not panel.played_appearances.gt(0).all():
        raise ValueError("Eligible panel contains duplicate athletes or no played appearances")
    panel["minutes_per_played_appearance"] = panel.minutes / panel.played_appearances
    panel["points_per_minute"] = panel.points / panel.minutes
    if not np.isfinite(panel["points_per_minute"]).all():
        raise ValueError("Eligible panel has a nonfinite points-per-minute rate")
    rate = panel["points_per_minute"].to_numpy(dtype=float)
    mean, spread = float(rate.mean()), float(rate.std(ddof=0))
    if not np.isfinite(spread) or spread <= 0:
        raise ValueError("Eligible points-per-minute standard deviation is invalid")
    panel["ability_standardized"] = (rate - mean) / spread
    panel["qualifies_five_minutes"] = panel.minutes_per_played_appearance.ge(THRESHOLD)

    group = panel.groupby("team_id", sort=True)
    team = group.agg(
        team_short_display_name=("team_short_display_name", "last"),
        eligible_players=("athlete_id", "size"),
        eligible_minutes=("minutes", "sum"),
        team_ability_sum=("ability_standardized", "sum"),
    )
    restricted = panel.loc[panel.qualifies_five_minutes].groupby("team_id").agg(
        qualifying_players=("athlete_id", "size"),
        qualifying_minutes=("minutes", "sum"),
        qualifying_ability_sum=("ability_standardized", "sum"),
    )
    team = team.join(restricted, how="left").fillna({
        "qualifying_players": 0, "qualifying_minutes": 0,
        "qualifying_ability_sum": 0,
    })
    team["qualifying_players"] = team.qualifying_players.astype(int)
    team["below_five_players"] = team.eligible_players - team.qualifying_players
    team["qualifying_minute_share"] = team.qualifying_minutes / team.eligible_minutes
    team["below_five_minute_share"] = 1 - team.qualifying_minute_share
    panel = panel.merge(team.reset_index(), on="team_id", validate="many_to_one")
    panel["full_peer_count"] = panel.eligible_players - 1
    panel["restricted_peer_count"] = panel.qualifying_players - panel.qualifies_five_minutes.astype(int)
    full_sum = panel.team_ability_sum - panel.ability_standardized
    restricted_sum = panel.qualifying_ability_sum - np.where(
        panel.qualifies_five_minutes, panel.ability_standardized, 0.0
    )
    panel["full_peer_mean"] = np.where(
        panel.full_peer_count.gt(0), full_sum / panel.full_peer_count.replace(0, np.nan), np.nan
    )
    panel["restricted_peer_mean"] = np.where(
        panel.restricted_peer_count.gt(0),
        restricted_sum / panel.restricted_peer_count.replace(0, np.nan), np.nan,
    )
    panel["restricted_minus_full"] = panel.restricted_peer_mean - panel.full_peer_mean
    panel = panel.sort_values("athlete_id").reset_index(drop=True)
    team = team.reset_index().sort_values("team_id").reset_index(drop=True)
    summary = {
        "status": "executed_unreviewed",
        "year": 2015,
        "team_coverage_minimum_captured_games": 11,
        "player_eligibility_minimum_total_minutes": 20,
        "restricted_peer_minimum_minutes_per_played_appearance": THRESHOLD,
        "ability_rate_mean": mean,
        "ability_rate_population_sd": spread,
        "source_audit": source_audit,
        "canonical_team_incidence": incidence,
        "eligible_athletes": int(len(panel)),
        "eligible_teams": int(len(team)),
        "eligible_athletes_with_fallback_row": int(panel.excluded_source_rows.gt(0).sum()),
        "fallback_points_on_eligible_athletes": float(panel.excluded_source_points.sum()),
        "fallback_row_fraction_of_2015_source": float(
            source_audit["zero_minute_positive_point_rows_fallback"] / source_audit["source_rows_2015"]
        ),
        "fallback_points_fraction_of_2015_recorded_points": float(
            source_audit["zero_minute_positive_point_fallback_points"]
            / source_audit["source_rows_2015_recorded_points"]
        ),
        "fallback_points_fraction_of_eligible_pre_fallback_points": float(
            panel.excluded_source_points.sum()
            / (panel.points.sum() + panel.excluded_source_points.sum())
        ),
        "qualifying_athletes": int(panel.qualifies_five_minutes.sum()),
        "below_five_athletes": int((~panel.qualifies_five_minutes).sum()),
        "total_eligible_minutes": float(panel.minutes.sum()),
        "below_five_minute_share_overall": float(
            panel.loc[~panel.qualifies_five_minutes, "minutes"].sum() / panel.minutes.sum()
        ),
        "full_peer_zero_count": int(panel.full_peer_count.eq(0).sum()),
        "restricted_peer_zero_count": int(panel.restricted_peer_count.eq(0).sum()),
        "restricted_peer_one_count": int(panel.restricted_peer_count.eq(1).sum()),
        "paired_peer_observations": int(panel.restricted_minus_full.notna().sum()),
        "minutes_per_played_appearance": quantiles(panel.minutes_per_played_appearance),
        "played_appearances": quantiles(panel.played_appearances),
        "full_peer_count": quantiles(panel.full_peer_count),
        "restricted_peer_count": quantiles(panel.restricted_peer_count),
        "peer_delta": quantiles(panel.restricted_minus_full),
        "absolute_peer_delta": quantiles(panel.restricted_minus_full.abs()),
        "team_below_five_player_count": quantiles(team.below_five_players),
        "team_below_five_minute_share": quantiles(team.below_five_minute_share),
    }
    return panel, team, candidate, changed, summary


def run() -> None:
    panel, team, candidate, changed, summary = build()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    files = {
        "candidates": DATA_DIR / f"{STEM}_canonical_team_candidates.csv",
        "changed": DATA_DIR / f"{STEM}_canonical_team_changes.csv",
        "players": OUTPUT_DIR / f"{STEM}_players.csv.gz",
        "teams": OUTPUT_DIR / f"{STEM}_teams.csv",
        "summary": OUTPUT_DIR / f"{STEM}_summary.json",
    }
    run_file = RUN_DIR / f"{STEM}_run_record.json"
    if any(path.exists() for path in [*files.values(), run_file]):
        raise FileExistsError("Version-one audit output already exists; preserve it and use a new version")
    candidate.to_csv(files["candidates"], index=False)
    changed.to_csv(files["changed"], index=False)
    panel.to_csv(files["players"], index=False, compression="gzip")
    team.to_csv(files["teams"], index=False)
    files["summary"].write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    record = {
        "status": "executed_unreviewed",
        "timestamp": datetime.now().astimezone().isoformat(),
        "code": str(HERE.relative_to(REPO)), "code_sha256": sha256(HERE),
        "source_reader": str(OLD_READER.relative_to(REPO)),
        "source_reader_sha256": sha256(OLD_READER),
        "frozen_game_file": str(SOURCE.relative_to(REPO)),
        "frozen_game_file_bytes": SOURCE.stat().st_size,
        "frozen_game_file_sha256": sha256(SOURCE),
        "source_recovery_overlay": str(OVERLAY.relative_to(REPO)),
        "source_recovery_overlay_sha256": sha256(OVERLAY),
        "zero_minute_recovery_overlay": str(ZERO_OVERLAY.relative_to(REPO)),
        "zero_minute_recovery_overlay_sha256": sha256(ZERO_OVERLAY),
        "python": sys.version, "numpy": np.__version__, "pandas": pd.__version__,
        "parameters": {
            "season": 2015, "team_minimum_captured_games": 11,
            "athlete_minimum_total_minutes": 20,
            "canonical_team": "most distinct positive-minute games; then total verified minutes",
            "ability": "season points divided by season minutes, standardized with population SD",
            "restricted_peer_minimum_minutes_per_played_appearance": THRESHOLD,
            "focal_player_sample": "same for full and restricted peer means",
            "unresolved_positive_point_zero_minute_rows": "omit the row's points and minutes from constructed rates; retain game identity for coverage",
            "outcome_curve": "not computed",
        },
        "outputs": [
            {"path": str(path.relative_to(REPO)), "bytes": path.stat().st_size, "sha256": sha256(path)}
            for path in files.values()
        ],
    }
    run_file.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "eligible_athletes": summary["eligible_athletes"],
        "eligible_teams": summary["eligible_teams"],
        "canonical_team_incidence": summary["canonical_team_incidence"],
        "below_five_athletes": summary["below_five_athletes"],
        "restricted_peer_zero_count": summary["restricted_peer_zero_count"],
        "restricted_peer_one_count": summary["restricted_peer_one_count"],
        "peer_delta": summary["peer_delta"],
    }, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Run this bounded audit")
    args = parser.parse_args()
    if not args.run:
        parser.error("Pass --run to execute the authorized bounded audit")
    run()
