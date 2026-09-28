#!/usr/bin/env python3
"""Bounded saved-source identity and same-player metric audit; no source mutation."""
from __future__ import annotations

import hashlib
import json
import platform
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[5]
WORK = REPO / "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis"
STEM = "ASSORT_20260927_performance_metric_audit_v1"
OUT = WORK / "outputs/performance_metric_audit_2015"
INPUT = WORK / "outputs/rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
AUDIT_RECORD = WORK / "docs/run_records/ASSORT_20260927_rotation_audit_v1_run_record.json"
MATCHED = REPO / "datasets/mbb/DO_NOT_ERASE/bpm_player_season_matched.csv"
RAW = REPO / "datasets/mbb/DO_NOT_ERASE/bpm_player_season_raw.csv"
CROSSWALK = REPO / "datasets/mbb/DO_NOT_ERASE/sr_school_slug_crosswalk.csv"
SAMPLE_SIZE = 24
SAMPLE_SALT = "metric-identity-2015-20260927"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized_name(value):
    name = re.sub(r"[^a-z0-9\s]", "", str(value).lower())
    name = re.sub(r"\s+(jr|sr|ii|iii|iv|v)\s*$", "", name)
    return re.sub(r"\s+", " ", name).strip()


def h_sort(frame, column):
    values = frame[column].to_numpy(dtype=float)
    grand = values.mean()
    total = np.square(values - grand).sum()
    group = frame.groupby("team_id")[column]
    means = group.transform("mean").to_numpy()
    within = np.square(values - means).sum()
    agg = group.agg(["size", "mean"])
    between = (agg["size"] * np.square(agg["mean"] - grand)).sum()
    assert np.isclose(between + within, total, rtol=1e-12, atol=1e-10)
    assert np.isclose(between / total, 1 - within / total, atol=1e-12)
    return float(between / total)


def main():
    if list(OUT.glob(f"{STEM}*")):
        raise RuntimeError("Refusing to overwrite existing audit outputs")
    source_paths = [INPUT, AUDIT_RECORD, MATCHED, RAW, CROSSWALK, Path(__file__)]
    before = {str(p.relative_to(REPO)): sha(p) for p in source_paths}
    original_record = json.loads(AUDIT_RECORD.read_text())
    expected = next(x["sha256"] for x in original_record["outputs"] if x["path"] == str(INPUT.relative_to(REPO)))
    assert sha(INPUT) == expected
    players = pd.read_csv(INPUT)
    assert len(players) == players.athlete_id.nunique() == 4267
    assert players.team_id.nunique() == 351
    players["season"] = 2015  # Fixed input's documented season; not inferred from names.
    matched_all = pd.read_csv(MATCHED, low_memory=False)
    matched = matched_all.loc[matched_all.season == 2015].copy()
    assert not matched.duplicated(["athlete_id", "season", "team_id"]).any()
    joined = players.merge(matched, on=["athlete_id", "season", "team_id"], how="left", validate="one_to_one", indicator=True)
    for col in ["BPM", "PER", "points_per_minute"]:
        joined[col] = pd.to_numeric(joined[col], errors="coerce")
    common = joined.loc[np.isfinite(joined.BPM) & np.isfinite(joined.PER)].copy()
    assert len(common) == 4161

    # Sample selected solely by identifier hash; one player per team.
    common["sample_hash"] = common.athlete_id.map(lambda value: hashlib.sha256(f"{SAMPLE_SALT}|{int(value)}".encode()).hexdigest())
    sample = common.sort_values("sample_hash").drop_duplicates("team_id").head(SAMPLE_SIZE).copy()
    assert len(sample) == sample.team_id.nunique() == SAMPLE_SIZE
    cw = pd.read_csv(CROSSWALK)
    assert not cw.team_id.duplicated().any()
    sample = sample.merge(cw[["team_id", "school_slug"]], on="team_id", how="left", validate="many_to_one")
    raw = pd.read_csv(RAW, low_memory=False)
    raw = raw.loc[raw.sr_year == 2015].copy()
    raw["player_key"] = raw.Player.map(normalized_name)
    raw["MP"] = pd.to_numeric(raw.MP, errors="coerce")
    keys = ["school_slug", "sr_year", "player_key"]
    raw_counts = raw.groupby(keys).size()
    raw_selected = raw.sort_values(keys + ["MP"], ascending=[True, True, True, False], kind="stable").drop_duplicates(keys)
    identities = []
    for row in sample.itertuples(index=False):
        key = (row.school_slug, 2015, normalized_name(row.athlete_display_name))
        found = raw_selected.loc[(raw_selected.school_slug == key[0]) & (raw_selected.sr_year == key[1]) & (raw_selected.player_key == key[2])]
        entry = {"athlete_id": int(row.athlete_id), "team_id": int(row.team_id), "accepted_name": row.athlete_display_name, "accepted_team": row.team_short_display_name_x, "school_slug": row.school_slug, "sample_hash": row.sample_hash, "raw_candidates": int(raw_counts.get(key, 0)), "accepted_minutes": float(row.minutes)}
        entry["status"] = "no_raw_key"
        if len(found) == 1:
            sr = found.iloc[0]
            entry.update({"sr_name": sr.Player, "source_url": sr.get("source_url", ""), "scrape_date": sr.get("scrape_date", ""), "sr_minutes": sr.MP, "saved_BPM": row.BPM, "raw_BPM": sr.BPM, "saved_PER": row.PER, "raw_PER": sr.PER})
            agreement = all(np.isfinite(float(sr[col])) and np.isclose(float(sr[col]), getattr(row, col), rtol=0, atol=1e-10) for col in ["BPM", "PER"])
            entry["status"] = "key_and_values_agree" if agreement else "value_disagreement"
        identities.append(entry)
    identity = pd.DataFrame(identities)
    OUT.mkdir(parents=True, exist_ok=True)
    identity_path = OUT / f"{STEM}_identity_sample.csv"
    identity.to_csv(identity_path, index=False)
    if not identity.status.eq("key_and_values_agree").all():
        raise RuntimeError(f"Identity/value check failed; see {identity_path}. No metric comparison performed.")

    summaries, widths = [], []
    for column, label in [("points_per_minute", "Points per minute"), ("PER", "Player Efficiency Rating"), ("BPM", "Box Plus/Minus")]:
        values = common[column].to_numpy(dtype=float)
        z_col = column + "_z_common"
        common[z_col] = (values - values.mean()) / values.std(ddof=0)
        index = h_sort(common, column)
        assert np.isclose(index, h_sort(common, z_col), atol=1e-12)
        team = common.groupby("team_id")[z_col].agg(["size", "min", "max", "mean", "std"]).reset_index()
        team["width"] = team["max"] - team["min"]
        team["metric"] = label
        widths.append(team)
        q = np.quantile(values, [0, .05, .25, .5, .75, .95, 1])
        summaries.append({"metric": label, "column": column, "players": len(common), "teams": common.team_id.nunique(), "mean_raw": float(values.mean()), "sd_raw_population": float(values.std(ddof=0)), "min_raw": float(q[0]), "p05_raw": float(q[1]), "p25_raw": float(q[2]), "median_raw": float(q[3]), "p75_raw": float(q[4]), "p95_raw": float(q[5]), "max_raw": float(q[6]), "H_sort": index, "mean_team_interval_width_z_equal_team": float(team.width.mean()), "median_team_interval_width_z_equal_team": float(team.width.median())})
    summary_frame = pd.DataFrame(summaries)
    joined["has_both_metrics"] = np.isfinite(joined.BPM) & np.isfinite(joined.PER)
    excluded = joined.loc[~joined.has_both_metrics]
    correlations = common[["points_per_minute", "PER", "BPM"]].corr(method="spearman")
    summary = {
        "season": 2015,
        "accepted_players": len(players), "accepted_teams": int(players.team_id.nunique()),
        "key_matches": int(joined._merge.eq("both").sum()),
        "finite_BPM": int(np.isfinite(joined.BPM).sum()), "finite_PER": int(np.isfinite(joined.PER).sum()),
        "common_players": len(common), "common_teams": int(common.team_id.nunique()),
        "excluded_from_common": len(excluded), "excluded_fraction": len(excluded) / len(players),
        "common_min_team_size": int(common.groupby("team_id").size().min()),
        "full_PPM_H_sort": h_sort(players, "points_per_minute"),
        "common_PPM_H_sort": h_sort(common, "points_per_minute"),
        "identity_sample_size": SAMPLE_SIZE, "identity_sample_status_counts": identity.status.value_counts().to_dict(),
        "identity_raw_duplicate_keys": int(identity.raw_candidates.gt(1).sum()),
        "raw_file_seasons": [int(pd.read_csv(RAW, usecols=["sr_year"]).sr_year.min()), int(pd.read_csv(RAW, usecols=["sr_year"]).sr_year.max())],
        "matched_file_seasons": [int(matched_all.season.min()), int(matched_all.season.max())],
        "sample_scrape_dates": sorted(identity.scrape_date.dropna().astype(str).unique().tolist()),
        "spearman_rank_correlations": correlations.to_dict(),
        "metrics": summaries,
        "limitations": ["Saved-source name/school/year and value consistency only; no independent website validation or measured linkage error rate.", "Predetermined 24-player sample covers 24 teams, not every record or collision.", "Common-sample exclusion avoids differing people across measures but does not establish missingness is ignorable.", "Global 2015 population standardization does not remove role, pace, opponent, or team effects.", "BPM contains a team-performance adjustment; its sorting cannot be treated as independent evidence of latent talent sorting.", "No random-assignment reference, draft outcome, model calibration, causal analysis, or experiment computed."]
    }
    outputs = {
        "common_players.csv": common[["athlete_id", "team_id", "season", "athlete_display_name", "team_short_display_name_x", "minutes", "points_per_minute", "PER", "BPM", "mp_sr", "points_per_minute_z_common", "PER_z_common", "BPM_z_common"]],
        "metric_summary.csv": summary_frame,
        "team_intervals.csv": pd.concat(widths, ignore_index=True),
        "excluded_players.csv": excluded[["athlete_id", "team_id", "athlete_display_name", "team_short_display_name_x", "minutes", "points_per_minute", "BPM", "PER", "_merge"]],
        "rank_correlations.csv": correlations.reset_index(names="metric"),
    }
    for suffix, frame in outputs.items():
        frame.to_csv(OUT / f"{STEM}_{suffix}", index=False)
    (OUT / f"{STEM}_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    after = {str(p.relative_to(REPO)): sha(p) for p in source_paths}
    assert before == after, "Source hash changed during audit"
    result_paths = sorted(OUT.glob(f"{STEM}*"))
    record = {"status": "executed_pending_review", "timestamp_utc": datetime.now(timezone.utc).isoformat(), "code": str(Path(__file__).relative_to(REPO)), "inputs_and_code_sha256": before, "parameters": {"season": 2015, "sample_size": SAMPLE_SIZE, "sample_salt": SAMPLE_SALT, "sample_selection": "ascending SHA256(salt|athlete_id), first player from each distinct team", "population": "accepted 4267-player audit; compare finite-BPM-and-PER intersection", "standardization": "per-metric mean and population SD on common 2015 sample", "weighting": "equal player for H_sort; equal team for mean interval widths", "random_assignment_reference": "not run"}, "python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__, "outputs": [{"path": str(p.relative_to(REPO)), "sha256": sha(p), "bytes": p.stat().st_size} for p in result_paths]}
    (WORK / f"docs/run_records/{STEM}_run_record.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(summary, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
