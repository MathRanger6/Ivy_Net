#!/usr/bin/env python3
"""One bounded, reproducible 2015 basketball sorting-sensitivity comparison.

This reads the verified rotation-audit player file. It neither rebuilds the
source population nor runs the assignment or selection simulations.
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

import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[5]
BASE = Path(__file__).resolve().parents[1]
STEM = "ASSORT_20260927_sorting_sensitivity_v1"
INPUT_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/"
    "rotation_audit_2015/ASSORT_20260927_rotation_audit_v1_players.csv.gz"
)
AUDIT_RECORD_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/"
    "run_records/ASSORT_20260927_rotation_audit_v1_run_record.json"
)
CODE_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/code/"
    + STEM + ".py"
)
OUT_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/outputs/"
    "sorting_sensitivity_2015/"
)
RECORD_REL = (
    "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis/docs/"
    "run_records/" + STEM + "_run_record.json"
)
SEED = 20260927
SHUFFLES = 1000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sorting_index(values: np.ndarray, teams: np.ndarray) -> float:
    """Player-weighted between-team share of total PPM variation."""
    n_team = int(teams.max()) + 1
    counts = np.bincount(teams, minlength=n_team)
    sums = np.bincount(teams, weights=values, minlength=n_team)
    means = sums / counts
    grand_mean = values.mean()
    total = np.square(values - grand_mean).sum()
    within = np.square(values - means[teams]).sum()
    return float(1.0 - within / total)


def inspect_population(frame: pd.DataFrame, name: str) -> dict:
    values = frame["points_per_minute"].to_numpy(dtype=float)
    teams, labels = pd.factorize(frame["team_id"], sort=True)
    teams = teams.astype(np.int64)
    counts = np.bincount(teams, minlength=len(labels))
    if np.any(counts == 0) or not np.all(np.isfinite(values)):
        raise ValueError(f"{name}: missing team or non-finite PPM")
    if float(np.var(values)) <= 0:
        raise ValueError(f"{name}: no PPM variation")
    observed = sorting_index(values, teams)

    # First cross-check: the repository's Grandchild ASSIGN reporting function.
    sys.path.insert(0, str(REPO / "sports"))
    grandchild = importlib.import_module("541_grandchild_homophily_assign")
    grandchild_value = grandchild.realized_sorting_index_H_sort(values, teams)
    if not np.isclose(observed, grandchild_value, atol=1e-12, rtol=0):
        raise AssertionError(f"{name}: Grandchild sorting-index mismatch")

    # Second cross-check: the PD21 empirical wrapper, including its team coding.
    sys.path.insert(0, str(REPO / "sports" / "scripts"))
    pd21 = importlib.import_module("pd21_rho_hsort_calibrate")
    pd21_frame = frame[["team_id", "points_per_minute"]].rename(
        columns={"points_per_minute": "perf"}
    )
    pd21_value = pd21.empirical_h_sort(pd21_frame)
    if not np.isclose(observed, pd21_value, atol=1e-12, rtol=0):
        raise AssertionError(f"{name}: PD21 empirical sorting-index mismatch")

    return {
        "name": name,
        "values": values,
        "teams": teams,
        "players": len(frame),
        "teams_count": len(labels),
        "min_team_size": int(counts.min()),
        "max_team_size": int(counts.max()),
        "observed_h_sort": observed,
        "grandchild_crosscheck": grandchild_value,
        "pd21_crosscheck": pd21_value,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="execute the locked comparison")
    args = parser.parse_args()
    if not args.run:
        parser.error("pass --run to execute")

    input_path = REPO / INPUT_REL
    audit_record_path = REPO / AUDIT_RECORD_REL
    audit_record = json.loads(audit_record_path.read_text())
    matching = [entry for entry in audit_record["outputs"] if entry["path"] == INPUT_REL]
    if len(matching) != 1 or sha256(input_path) != matching[0]["sha256"]:
        raise ValueError("rotation-audit player input does not match its run record")

    frame = pd.read_csv(input_path)
    required = [
        "athlete_id", "team_id", "points", "minutes", "played_appearances",
        "minutes_per_played_appearance", "points_per_minute", "qualifies_five_minutes",
    ]
    if not set(required).issubset(frame.columns):
        raise ValueError("rotation-audit player input lacks required columns")
    if len(frame) != 4267 or frame["athlete_id"].nunique() != 4267:
        raise ValueError("unexpected full-population size or duplicate athlete")
    if frame[required].isna().any().any():
        raise ValueError("missing required player values")
    if not frame["qualifies_five_minutes"].isin([True, False]).all():
        raise ValueError("invalid five-minute flag")
    if not (frame["played_appearances"] > 0).all():
        raise ValueError("nonpositive appearance count")
    minutes_per = frame["minutes"] / frame["played_appearances"]
    if not np.allclose(minutes_per, frame["minutes_per_played_appearance"], atol=1e-10):
        raise ValueError("stored minutes-per-appearance mismatch")
    if not np.all(frame["qualifies_five_minutes"] == (minutes_per >= 5)):
        raise ValueError("five-minute flag mismatch")
    if not np.allclose(frame["points"] / frame["minutes"], frame["points_per_minute"], atol=1e-10):
        raise ValueError("stored PPM mismatch")

    regular_frame = frame.loc[frame["qualifies_five_minutes"]].copy()
    if len(regular_frame) != 3928 or regular_frame["team_id"].nunique() != 351:
        raise ValueError("unexpected regular-playing population")
    populations = [
        inspect_population(frame, "full"),
        inspect_population(regular_frame, "regular_playing"),
    ]

    streams = np.random.SeedSequence(SEED).spawn(2)
    draws = []
    summary = {}
    for population, stream in zip(populations, streams):
        rng = np.random.default_rng(stream)
        values, teams = population["values"], population["teams"]
        sample = np.empty(SHUFFLES, dtype=float)
        for iteration in range(SHUFFLES):
            sample[iteration] = sorting_index(rng.permutation(values), teams)
            draws.append((population["name"], iteration + 1, sample[iteration]))
        expected = (population["teams_count"] - 1) / (population["players"] - 1)
        null_mean = float(sample.mean())
        if abs(null_mean - expected) >= 0.005:
            raise AssertionError(f"{population['name']}: shuffle mean far from analytic expectation")
        summary[population["name"]] = {
            key: value for key, value in population.items() if key not in ("values", "teams")
        }
        summary[population["name"]].update({
            "analytic_random_expectation": expected,
            "random_mean": null_mean,
            "random_p025": float(np.percentile(sample, 2.5)),
            "random_p975": float(np.percentile(sample, 97.5)),
            "observed_minus_random_mean": population["observed_h_sort"] - null_mean,
        })

    full, regular = summary["full"], summary["regular_playing"]
    summary["comparison"] = {
        "players_removed": full["players"] - regular["players"],
        "regular_minus_full_observed_h_sort": regular["observed_h_sort"] - full["observed_h_sort"],
        "regular_minus_full_reference_adjusted": (
            regular["observed_minus_random_mean"] - full["observed_minus_random_mean"]
        ),
    }
    summary["design"] = {
        "season": 2015,
        "metric": "raw season points per minute",
        "regular_playing_rule": "at least 5 minutes per positive-minute appearance",
        "random_reference": "fixed values and team sizes; uniform permutation among player slots",
        "shuffles_per_population": SHUFFLES,
        "master_seed": SEED,
        "input": INPUT_REL,
        "input_sha256": sha256(input_path),
        "interpretation": "descriptive nested-sample comparison; not a causal or formal sampling test",
    }

    output_dir = REPO / OUT_REL
    output_dir.mkdir(parents=True, exist_ok=False)
    summary_rel = OUT_REL + STEM + "_summary.json"
    draws_rel = OUT_REL + STEM + "_random_draws.csv"
    (REPO / summary_rel).write_text(json.dumps(summary, indent=2) + "\n")
    pd.DataFrame(draws, columns=["population", "shuffle", "h_sort"]).to_csv(REPO / draws_rel, index=False)

    record = {
        "status": "executed_unreviewed",
        "timestamp": datetime.now().astimezone().isoformat(),
        "code": CODE_REL,
        "code_sha256": sha256(REPO / CODE_REL),
        "input": INPUT_REL,
        "input_sha256": sha256(input_path),
        "audit_run_record": AUDIT_RECORD_REL,
        "audit_run_record_sha256": sha256(audit_record_path),
        "repository_sorting_sources": [
            {"path": "sports/541_grandchild_homophily_assign.py", "sha256": sha256(REPO / "sports/541_grandchild_homophily_assign.py")},
            {"path": "sports/scripts/pd21_rho_hsort_calibrate.py", "sha256": sha256(REPO / "sports/scripts/pd21_rho_hsort_calibrate.py")},
        ],
        "parameters": summary["design"],
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "outputs": [
            {"path": rel, "sha256": sha256(REPO / rel), "bytes": (REPO / rel).stat().st_size}
            for rel in (summary_rel, draws_rel)
        ],
    }
    (REPO / RECORD_REL).write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
