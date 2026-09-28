#!/usr/bin/env python3
"""Read-only source preflight for the authorized three-season mechanism comparison.
Writes audit artifacts only inside this experiment's isolated data/run directories.
Does not construct final populations or run assignment/selection.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
WORK = HERE.parents[2]
REPO = WORK.parents[3]
STEM = "ASSORT_20260927_three_season_mechanism_v1"
SOURCE = REPO / "datasets/mbb/mbb_df_player_box.csv"
OUT = WORK / "data/three_season_mechanism_v1/preflight"
RECORD = WORK / "docs/run_records" / (STEM + "_preflight.json")

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(2**20), b""):
            h.update(b)
    return h.hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    if not parser.parse_args().run:
        parser.error("--run required")
    if OUT.exists() or RECORD.exists():
        raise RuntimeError("Refusing to overwrite preflight artifacts")
    OUT.mkdir(parents=True)
    before = sha(SOURCE)
    pieces = []
    offset = 0
    cols = ["season", "game_id", "athlete_id", "team_id", "athlete_display_name",
            "minutes", "points", "did_not_play"]
    for chunk in pd.read_csv(SOURCE, usecols=cols, chunksize=200000, low_memory=False):
        keep = pd.to_numeric(chunk.season, errors="coerce").isin([2014, 2016])
        part = chunk.loc[keep].copy()
        part["source_data_row"] = np.flatnonzero(keep.to_numpy()) + offset + 1
        pieces.append(part)
        offset += len(chunk)
    raw = pd.concat(pieces, ignore_index=True)
    summaries = []
    for season in [2014, 2016]:
        b = raw.loc[pd.to_numeric(raw.season).eq(season)].copy()
        nraw = len(b)
        for col in ["game_id", "athlete_id", "team_id", "minutes", "points"]:
            b[col] = pd.to_numeric(b[col], errors="coerce")
        bad_id = b[["game_id", "athlete_id", "team_id"]].isna().any(axis=1)
        bad_id |= (b[["game_id", "athlete_id", "team_id"]].mod(1).fillna(0) != 0).any(axis=1)
        blank = b.athlete_id.isna() & b.athlete_display_name.isna()
        malformed = bad_id & ~blank
        b.loc[bad_id].to_csv(OUT / f"{season}_identity_rows.csv", index=False)
        b = b.loc[~bad_id & b.athlete_display_name.astype(str).str.strip().ne("-")].copy()
        coverage = b.groupby("team_id").game_id.nunique()
        teams = coverage.index[coverage.ge(11)]
        b = b.loc[b.team_id.isin(teams)].copy()
        both = b.minutes.isna() & b.points.isna()
        dnp = b.did_not_play.astype(str).str.lower().eq("true")
        partial = b.minutes.isna() ^ b.points.isna()
        zero_points = b.minutes.eq(0) & b.points.gt(0)
        negative = b.minutes.lt(0) | b.points.lt(0)
        nonfinite = (~np.isfinite(b.minutes) & b.minutes.notna()) | (~np.isfinite(b.points) & b.points.notna())
        unexpected_blank = both & ~dnp
        duplicate = b.duplicated(["game_id", "athlete_id", "team_id"], keep=False)
        cross = b.groupby(["game_id", "athlete_id"]).team_id.transform("nunique").gt(1)
        b["partial_stats"] = partial
        b["positive_points_zero_minutes"] = zero_points
        b["unexpected_blank_stats"] = unexpected_blank
        b["negative_or_nonfinite"] = negative | nonfinite
        b["duplicate_same_team_game"] = duplicate
        b["cross_team_same_game"] = cross
        bad = partial | zero_points | unexpected_blank | negative | nonfinite | duplicate | cross
        b.loc[bad].to_csv(OUT / f"{season}_flagged_rows.csv", index=False)
        # Totals below screen impact only. They are NOT accepted PPM construction.
        totals = b.groupby(["athlete_id","team_id"], as_index=False).agg(
            recorded_minutes=("minutes","sum"), rows=("game_id","size"),
            captured_games=("game_id","nunique"))
        positives = b.loc[b.minutes.gt(0)].groupby(["athlete_id","team_id"]).game_id.nunique().rename("positive_minute_games")
        totals = totals.merge(positives, on=["athlete_id","team_id"], how="left")
        totals["positive_minute_games"] = totals.positive_minute_games.fillna(0)
        multi = totals.groupby("athlete_id").team_id.transform("size").gt(1)
        totals.loc[multi].to_csv(OUT / f"{season}_multi_team_candidates.csv", index=False)
        positive_multi = totals.loc[totals.positive_minute_games.gt(0)].groupby("athlete_id").team_id.nunique().gt(1)
        eligible_pairs = totals.loc[totals.recorded_minutes.ge(20), ["athlete_id","team_id"]]
        impact = b.loc[bad].merge(eligible_pairs, on=["athlete_id","team_id"], how="inner")
        summary = {
            "season": season, "source_rows": nraw, "teams_at_least_11_games": len(teams),
            "coverage_retained_rows": len(b), "blank_identity_rows": int(blank.sum()),
            "malformed_identity_rows": int(malformed.sum()),
            "partial_stat_rows": int(partial.sum()),
            "positive_points_zero_minute_rows": int(zero_points.sum()),
            "unexpected_blank_stat_rows": int(unexpected_blank.sum()),
            "negative_or_nonfinite_rows": int((negative | nonfinite).sum()),
            "duplicate_same_team_game_rows": int(duplicate.sum()),
            "cross_team_same_game_rows": int(cross.sum()),
            "multi_team_athletes": int(totals.loc[multi].athlete_id.nunique()),
            "athletes_positive_minutes_on_multiple_teams": int(positive_multi.sum()),
            "provisional_player_team_pairs_at_least_20_recorded_minutes": len(eligible_pairs),
            "flagged_rows_on_provisionally_eligible_pairs": len(impact),
            "provisionally_eligible_athletes_with_flags": int(impact.athlete_id.nunique()),
            "status": "requires_source_review" if bad.any() or malformed.any() or positive_multi.any() else "source_screen_passed"
        }
        summaries.append(summary)
        print(json.dumps(summary), flush=True)
    after = sha(SOURCE)
    if before != after:
        raise RuntimeError("Source changed during audit")
    record = {"experiment": STEM, "stage": "preflight_only", "time_utc": datetime.now(timezone.utc).isoformat(),
              "source": str(SOURCE.relative_to(REPO)), "source_sha256_before": before,
              "source_sha256_after": after, "driver_sha256": sha(HERE),
              "software": {"numpy": np.__version__, "pandas": pd.__version__},
              "seasons": summaries, "simulation_executed": False,
              "outputs": {str(p.relative_to(WORK)): sha(p) for p in sorted(OUT.glob("*.csv"))}}
    RECORD.write_text(json.dumps(record, indent=2) + "\n")
    print("PREFLIGHT COMPLETE; no simulations executed.", flush=True)

if __name__ == "__main__":
    main()

