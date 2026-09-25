#!/usr/bin/env python3
"""2015 paired assortativity experiment; all products stay in assort_analysis."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import sys
import time

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
WORK = HERE.parents[1]
REPO = HERE.parents[5]
SOURCE = REPO / "datasets/mbb/mbb_df_player_box.csv"
DATA = WORK / "data"
OUTPUTS = WORK / "outputs"
RECORDS = WORK / "docs/run_records"
PREFIX = "ASSORT_20260925_v1"
MASTER_SEED = 20260925
REPETITIONS = 100
RHO_VALUES = (0.0, 1.0)
SELECTION_FRACTIONS = (0.01, 0.10)
GAMMA = 10.0
BINS = 16


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def json_write(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def finite_number(value: object, field: str) -> int:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number) or not np.isfinite(number) or float(number) != int(number):
        raise ValueError(f"{field} must be a nonmissing integer, got {value!r}")
    return int(number)


def read_2015() -> tuple[pd.DataFrame, dict]:
    """Read only needed columns, retaining source CSV data-row numbers."""
    columns = [
        "game_id", "season", "athlete_id", "team_id",
        "athlete_display_name", "team_short_display_name", "minutes", "points",
        "did_not_play", "active",
    ]
    pieces: list[pd.DataFrame] = []
    offset = 0
    selected = 0
    for chunk in pd.read_csv(SOURCE, usecols=columns, chunksize=200_000, low_memory=False):
        season = pd.to_numeric(chunk["season"], errors="coerce")
        keep = season.eq(2015)
        part = chunk.loc[keep].copy()
        part["source_data_row"] = np.flatnonzero(keep.to_numpy()) + offset + 1
        pieces.append(part)
        selected += len(part)
        offset += len(chunk)
    if not pieces:
        raise ValueError("No 2015 source rows")
    work = pd.concat(pieces, ignore_index=True)
    for col in ("athlete_id", "team_id", "minutes", "points"):
        work[col] = pd.to_numeric(work[col], errors="coerce")
    # The source contains seven entirely blank 2015 athlete records. The
    # established panel builder drops rows without athlete/team identifiers
    # before coverage counting; keep the same rule and record its impact.
    blank_identity = work["athlete_id"].isna() & work["athlete_display_name"].isna()
    audit = dict(
        source_rows_total=offset,
        source_rows_2015=selected,
        blank_identity_rows_removed=int(blank_identity.sum()),
    )
    work = work.loc[~blank_identity].copy()
    for col in ("athlete_id", "team_id"):
        val = work[col].to_numpy(dtype=float)
        if not np.all(np.isfinite(val) & (val == np.floor(val))):
            raise ValueError(f"Invalid {col} in 2015 source; stop for inspection")
        work[col] = work[col].astype(np.int64)
    if work["game_id"].isna().any():
        raise ValueError("Missing game identifier in 2015 source")
    if work["athlete_display_name"].isna().any():
        raise ValueError("Missing athlete name in 2015 source")
    return work, audit


def build_population() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    box, audit = read_2015()
    dash = box["athlete_display_name"].astype(str).str.strip().eq("-")
    audit["dash_rows_removed"] = int(dash.sum())
    box = box.loc[~dash].copy()

    games = box.groupby("team_id", sort=True)["game_id"].nunique()
    keep_teams = games.index[games.ge(11)]
    audit["teams_before_coverage"] = int(len(games))
    audit["teams_after_coverage"] = int(len(keep_teams))
    audit["rows_removed_coverage"] = int((~box["team_id"].isin(keep_teams)).sum())
    box = box.loc[box["team_id"].isin(keep_teams)].copy()

    # Canonical team is decided before player-season aggregation.
    candidate = box.groupby(["athlete_id", "team_id"], as_index=False).agg(
        distinct_games=("game_id", "nunique"),
        total_minutes=("minutes", "sum"),
        game_rows=("game_id", "size"),
    )
    candidate = candidate.sort_values(
        ["athlete_id", "distinct_games", "total_minutes"],
        ascending=[True, False, False],
        kind="stable",
    )
    top = candidate.drop_duplicates("athlete_id", keep="first")
    checks = candidate.merge(
        top[["athlete_id", "distinct_games", "total_minutes"]],
        on=["athlete_id", "distinct_games", "total_minutes"],
    )
    tied = checks.loc[checks.duplicated("athlete_id", keep=False)]
    if not tied.empty:
        tied.to_csv(DATA / f"{PREFIX}_unresolved_team_ties.csv", index=False)
        raise ValueError(f"{tied.athlete_id.nunique()} unresolved canonical-team ties")
    chosen = top[["athlete_id", "team_id"]].rename(columns={"team_id": "canonical_team_id"})
    candidate = candidate.merge(chosen, on="athlete_id", validate="many_to_one")
    candidate["kept"] = candidate["team_id"].eq(candidate["canonical_team_id"])
    candidate.to_csv(DATA / f"{PREFIX}_canonical_team_audit.csv", index=False)
    audit["multi_team_athletes_after_coverage"] = int(
        candidate.groupby("athlete_id").size().gt(1).sum()
    )
    audit["removed_athlete_team_records"] = int((~candidate["kept"]).sum())
    box = box.merge(chosen, on="athlete_id", validate="many_to_one")
    audit["rows_removed_wrong_team"] = int(
        box["team_id"].ne(box["canonical_team_id"]).sum()
    )
    box = box.loc[box["team_id"].eq(box["canonical_team_id"])].copy()

    # A blank no-play row is expected. A partial row with points but no
    # minutes changes the scoring-rate numerator without its denominator.
    both_missing = box["minutes"].isna() & box["points"].isna()
    expected_no_play = both_missing & box["did_not_play"].eq(True)
    unexpected_both = both_missing & ~box["did_not_play"].eq(True)
    partial = box["minutes"].isna() ^ box["points"].isna()
    audit["expected_no_play_rows"] = int(expected_no_play.sum())
    audit["unexpected_both_missing_rows"] = int(unexpected_both.sum())
    audit["partial_missing_stat_rows"] = int(partial.sum())
    anomaly = box.loc[unexpected_both | partial, [
        "source_data_row", "game_id", "athlete_id", "athlete_display_name",
        "team_id", "team_short_display_name", "minutes", "points",
        "did_not_play", "active",
    ]].copy()
    anomaly.to_csv(DATA / f"{PREFIX}_partial_stat_rows.csv", index=False)
    box["missing_minutes_row"] = box["minutes"].isna()
    box["missing_points_row"] = box["points"].isna()
    panel = box.groupby(["athlete_id", "team_id"], as_index=False).agg(
        points=("points", "sum"),
        minutes=("minutes", "sum"),
        missing_minutes_rows=("missing_minutes_row", "sum"),
        missing_points_rows=("missing_points_row", "sum"),
        distinct_games=("game_id", "nunique"),
        game_rows=("game_id", "size"),
    )
    panel["ppm"] = np.where(panel["minutes"] > 0, panel["points"] / panel["minutes"], np.nan)
    audit["player_team_rows_before_minutes"] = int(len(panel))
    eligible = panel.loc[panel["minutes"].ge(20)].copy()
    audit["player_team_rows_after_minutes"] = int(len(eligible))
    affected = eligible.loc[
        eligible["athlete_id"].isin(anomaly["athlete_id"])
    ]
    audit["eligible_with_partial_or_unexpected_missing_stats"] = int(len(affected))
    if not affected.empty:
        affected.to_csv(DATA / f"{PREFIX}_eligible_partial_stat_athletes.csv", index=False)
        json_write(DATA / f"{PREFIX}_population_audit_needs_review.json", audit)
        raise ValueError("Partial or unexpected missing statistics touch eligible athletes; inspect audit")
    if eligible["athlete_id"].isna().any() or eligible["athlete_id"].duplicated().any():
        raise ValueError("Eligible athlete identifiers are missing or duplicated")
    if not np.isfinite(eligible["ppm"]).all():
        raise ValueError("Eligible points-per-minute values must all be finite")
    eligible = eligible.sort_values("athlete_id").reset_index(drop=True)
    raw = eligible["ppm"].to_numpy(dtype=float)
    mean = float(raw.mean())
    spread = float(raw.std(ddof=0))
    if not np.isfinite(spread) or spread <= 0:
        raise ValueError(f"Invalid ability population spread: {spread}")
    eligible["ability"] = (raw - mean) / spread
    caps = eligible.groupby("team_id", sort=True).size().rename("capacity").reset_index()
    caps["pool_id"] = np.arange(len(caps), dtype=np.int64)
    if caps["capacity"].sum() != len(eligible):
        raise AssertionError("Roster capacities do not sum to population")
    audit.update(
        n_athletes=int(len(eligible)), n_teams=int(len(caps)),
        roster_min=int(caps.capacity.min()), roster_max=int(caps.capacity.max()),
        roster_mean=float(caps.capacity.mean()),
        ppm_mean=mean, ppm_population_sd=spread,
        ability_mean=float(eligible.ability.mean()),
        ability_population_sd=float(eligible.ability.std(ddof=0)),
    )
    audit["arkansas_pine_bluff_eligible_count"] = int(
        caps.loc[caps.team_id.eq(2029), "capacity"].sum()
    )
    return eligible, caps, candidate, audit


class PairedChoices:
    """One fixed player order and one fixed uniform draw per player."""

    def __init__(self, order: np.ndarray, uniforms: np.ndarray):
        self.order = order
        self.uniforms = uniforms
        self.cursor = 0

    def permutation(self, size: int) -> np.ndarray:
        if size != len(self.order):
            raise ValueError("Assignment player count changed")
        return self.order.copy()

    def choice(self, size: int, p: np.ndarray) -> int:
        if self.cursor >= len(self.uniforms) or size != len(p):
            raise ValueError("Paired choice stream exhausted or team count changed")
        cdf = np.cumsum(np.asarray(p, dtype=float))
        j = int(np.searchsorted(cdf, self.uniforms[self.cursor], side="right"))
        self.cursor += 1
        return min(j, size - 1)


def rank_scores(score: np.ndarray, athlete_id: np.ndarray) -> np.ndarray:
    # lexsort uses the final key as primary; equal scores favor lower athlete_id.
    order = np.lexsort((athlete_id, -score))
    ranks = np.empty(len(score), dtype=np.int16)
    ranks[order] = np.arange(1, len(score) + 1, dtype=np.int16)
    return ranks


def bin_labels(peer_quality: np.ndarray, athlete_id: np.ndarray) -> np.ndarray:
    if not np.isfinite(peer_quality).all():
        raise ValueError("A singleton roster or nonfinite peer quality prevents 16-bin display")
    order = np.lexsort((athlete_id, peer_quality))
    labels = np.empty(len(order), dtype=np.int8)
    labels[order] = (np.arange(len(order)) * BINS // len(order)).astype(np.int8)
    return labels


def summarize(values: pd.Series) -> dict:
    array = values.to_numpy(dtype=float)
    return dict(
        mean=float(array.mean()), median=float(np.median(array)),
        minimum=float(array.min()), maximum=float(array.max()),
        simulation_p025=float(np.quantile(array, 0.025, method="linear")),
        simulation_p975=float(np.quantile(array, 0.975, method="linear")),
    )


def run_experiment() -> None:
    start = time.monotonic()
    for folder in (DATA, OUTPUTS, RECORDS):
        folder.mkdir(parents=True, exist_ok=True)
    panel, caps, _, audit = build_population()
    n = len(panel)
    if n != 4266 or audit["arkansas_pine_bluff_eligible_count"] != 14:
        json_write(DATA / f"{PREFIX}_population_audit_needs_review.json", audit)
        raise ValueError("Population differs from prior 4,266-athlete / 14-player audit")
    panel.to_csv(DATA / f"{PREFIX}_eligible_players.csv.gz", index=False)
    caps.to_csv(DATA / f"{PREFIX}_team_capacities.csv", index=False)
    json_write(DATA / f"{PREFIX}_population_audit.json", audit)
    print(f"Population verified: N={n}, teams={len(caps)}, capacities {audit['roster_min']}–{audit['roster_max']}", flush=True)

    ability = panel["ability"].to_numpy(dtype=float)
    athlete_id = panel["athlete_id"].to_numpy(dtype=np.int64)
    cap_values = caps["capacity"].to_numpy(dtype=np.int64)
    observed_pool = pd.Categorical(panel["team_id"], categories=caps["team_id"]).codes
    if np.any(observed_pool < 0):
        raise AssertionError("Observed team mapping failed")
    theta = float(np.quantile(ability, 0.99, method="linear"))
    viability = 1.0 / (1.0 + np.exp(-np.clip(GAMMA * (ability - theta), -500, 500)))
    observed_c = np.bincount(observed_pool, weights=viability, minlength=len(caps)) / cap_values
    observed_exposure = observed_c[observed_pool]
    c_mean = float(observed_exposure.mean())
    c_sd = float(observed_exposure.std(ddof=0))
    if not np.isfinite(c_sd) or c_sd <= 1e-8:
        json_write(DATA / f"{PREFIX}_invalid_reference_spread.json", dict(
            congestion_mean=c_mean, congestion_population_sd=c_sd, threshold=1e-8
        ))
        raise ValueError("Reference congestion spread is zero or too small")

    slots = [math.floor(q * n + 0.5) for q in SELECTION_FRACTIONS]
    if any(k <= 0 or k > n for k in slots):
        raise ValueError("Invalid slot count")
    gc_path = REPO / "sports/541_grandchild_homophily_assign.py"
    sys.path.insert(0, str(gc_path.parent))
    gc = importlib.import_module("541_grandchild_homophily_assign")

    children = np.random.SeedSequence(MASTER_SEED).spawn(REPETITIONS)
    seeds = np.array([int(child.generate_state(1, dtype=np.uint64)[0]) for child in children], dtype=np.uint64)
    if len(set(map(int, seeds))) != REPETITIONS:
        raise AssertionError("Repetition seeds are not unique")

    pool_all = np.empty((REPETITIONS, 2, n), dtype=np.int16)
    peer_all = np.empty((REPETITIONS, 2, n), dtype=np.float64)
    congestion_all = np.empty((REPETITIONS, 2, n), dtype=np.float64)
    score_all = np.empty((REPETITIONS, 2, 3, n), dtype=np.float64)
    ranks_all = np.empty((REPETITIONS, 2, 3, n), dtype=np.int16)
    bins_all = np.empty((REPETITIONS, 2, n), dtype=np.int8)
    displacement_rows: list[dict] = []
    curve_rows: list[dict] = []
    sorting_rows: list[dict] = []
    baseline_rank = rank_scores(ability, athlete_id)
    for rep, seed in enumerate(seeds, start=1):
        generator = np.random.default_rng(int(seed))
        order = generator.permutation(n)
        uniforms = generator.random(n)
        for rho_idx, rho in enumerate(RHO_VALUES):
            paired = PairedChoices(order, uniforms)
            pool, centroid = gc.grandchild_assign(
                paired, ability, roster_caps=cap_values, rho=rho
            )
            if paired.cursor != n:
                raise AssertionError("Paired random stream not fully consumed")
            counts = np.bincount(pool, minlength=len(caps))
            if not np.array_equal(counts, cap_values):
                raise AssertionError("A labeled team did not receive its exact capacity")
            team_c = np.bincount(pool, weights=viability, minlength=len(caps)) / counts
            c_player = team_c[pool]
            sum_ability = np.bincount(pool, weights=ability, minlength=len(caps))
            peer = (sum_ability[pool] - ability) / (counts[pool] - 1)
            labels = bin_labels(peer, athlete_id)
            scores = (
                ability,
                ability - c_player,
                ability - (c_player - c_mean) / c_sd,
            )
            ranks = [rank_scores(value, athlete_id) for value in scores]
            if not np.array_equal(ranks[0], baseline_rank):
                raise AssertionError("Ability-only rank changed with assignment")
            # A common team penalty cannot reverse within-team ability order.
            for score in scores[1:]:
                residual = score - ability
                if any(np.ptp(residual[pool == j]) > 1e-12 for j in range(len(caps))):
                    raise AssertionError("Congestion penalty differs within a team")
            pool_all[rep - 1, rho_idx] = pool
            peer_all[rep - 1, rho_idx] = peer
            congestion_all[rep - 1, rho_idx] = c_player
            bins_all[rep - 1, rho_idx] = labels
            for mode_idx, (score, rank) in enumerate(zip(scores, ranks)):
                score_all[rep - 1, rho_idx, mode_idx] = score
                ranks_all[rep - 1, rho_idx, mode_idx] = rank
            sorting_rows.append(dict(
                repetition=rep, seed=int(seed), rho=rho,
                realized_h_sort=float(gc.sorting_index_h(ability, pool, centroid)),
            ))
            for k_idx, (fraction, k) in enumerate(zip(SELECTION_FRACTIONS, slots)):
                baseline = ranks[0] <= k
                if int(baseline.sum()) != k:
                    raise AssertionError("Ability-only selection did not fill all slots")
                for mode_idx, mode in ((1, "raw"), (2, "fixed_reference_standardized")):
                    winners = ranks[mode_idx] <= k
                    if int(winners.sum()) != k:
                        raise AssertionError("Congestion selection did not fill all slots")
                    displacement = int(np.count_nonzero(baseline & ~winners))
                    displacement_rows.append(dict(
                        repetition=rep, seed=int(seed), rho=rho,
                        congestion_representation=mode,
                        target_fraction=fraction, k=k, achieved_fraction=k / n,
                        displaced_winners=displacement,
                        displacement_fraction=displacement / k,
                    ))
                for mode_idx, mode in ((0, "ability_only"), (1, "raw"), (2, "fixed_reference_standardized")):
                    selected = ranks[mode_idx] <= k
                    for b in range(BINS):
                        members = labels == b
                        curve_rows.append(dict(
                            repetition=rep, seed=int(seed), rho=rho,
                            score_representation=mode,
                            target_fraction=fraction, k=k, bin=b + 1,
                            n_players=int(members.sum()),
                            mean_peer_quality=float(peer[members].mean()),
                            selection_rate=float(selected[members].mean()),
                        ))
        if rep % 10 == 0 or rep == 1:
            print(f"Completed paired repetitions: {rep}/{REPETITIONS}", flush=True)

    displacement = pd.DataFrame(displacement_rows)
    curves = pd.DataFrame(curve_rows)
    sorting = pd.DataFrame(sorting_rows)
    displacement.to_csv(OUTPUTS / f"{PREFIX}_displacement_by_repetition.csv", index=False)
    curves.to_csv(OUTPUTS / f"{PREFIX}_curve_bins_by_repetition.csv", index=False)
    sorting.to_csv(OUTPUTS / f"{PREFIX}_sorting_by_repetition.csv", index=False)

    grouped = []
    for keys, part in displacement.groupby(
        ["rho", "congestion_representation", "target_fraction", "k"], sort=True
    ):
        row = dict(zip(["rho", "congestion_representation", "target_fraction", "k"], keys))
        row.update({f"count_{key}": value for key, value in summarize(part["displaced_winners"]).items()})
        row.update({f"fraction_{key}": value for key, value in summarize(part["displacement_fraction"]).items()})
        row["fraction_repetitions_with_any_displacement"] = float(
            part["displaced_winners"].gt(0).mean()
        )
        grouped.append(row)
    pd.DataFrame(grouped).to_csv(OUTPUTS / f"{PREFIX}_displacement_summary.csv", index=False)

    paired = displacement.pivot(
        index=["repetition", "seed", "congestion_representation", "target_fraction", "k"],
        columns="rho", values=["displaced_winners", "displacement_fraction"]
    )
    pair_rows = []
    for index, row in paired.iterrows():
        rep, seed, mode, fraction, k = index
        pair_rows.append(dict(
            repetition=rep, seed=seed, congestion_representation=mode,
            target_fraction=fraction, k=k,
            count_difference_rho1_minus_rho0=int(row[("displaced_winners", 1.0)] - row[("displaced_winners", 0.0)]),
            fraction_difference_rho1_minus_rho0=float(row[("displacement_fraction", 1.0)] - row[("displacement_fraction", 0.0)]),
        ))
    paired_df = pd.DataFrame(pair_rows)
    paired_df.to_csv(OUTPUTS / f"{PREFIX}_paired_differences_by_repetition.csv", index=False)
    paired_summary = []
    for keys, part in paired_df.groupby(["congestion_representation", "target_fraction", "k"]):
        row = dict(zip(["congestion_representation", "target_fraction", "k"], keys))
        row.update({f"count_difference_{key}": value for key, value in summarize(part["count_difference_rho1_minus_rho0"]).items()})
        row.update({f"fraction_difference_{key}": value for key, value in summarize(part["fraction_difference_rho1_minus_rho0"]).items()})
        paired_summary.append(row)
    pd.DataFrame(paired_summary).to_csv(OUTPUTS / f"{PREFIX}_paired_difference_summary.csv", index=False)

    curve_summary = []
    for keys, part in curves.groupby(
        ["rho", "score_representation", "target_fraction", "k", "bin"], sort=True
    ):
        row = dict(zip(["rho", "score_representation", "target_fraction", "k", "bin"], keys))
        row["mean_peer_quality"] = float(part.mean_peer_quality.mean())
        row["mean_bin_players"] = float(part.n_players.mean())
        row.update({f"rate_{key}": value for key, value in summarize(part["selection_rate"]).items()})
        curve_summary.append(row)
    pd.DataFrame(curve_summary).to_csv(OUTPUTS / f"{PREFIX}_curve_summary.csv", index=False)

    np.savez_compressed(
        OUTPUTS / f"{PREFIX}_individual_arrays.npz",
        athlete_id=athlete_id, repetition_seeds=seeds,
        rho_values=np.array(RHO_VALUES), capacity=cap_values,
        ability=ability, pool_id=pool_all, peer_quality=peer_all,
        congestion=congestion_all, peer_bin=bins_all,
        scores=score_all, ranks=ranks_all,
    )
    outputs = sorted(OUTPUTS.glob(f"{PREFIX}_*"))
    manifest = dict(
        status="executed", prefix=PREFIX, date="2026-09-25",
        source_repo_path=str(SOURCE.relative_to(REPO)),
        source_sha256=sha256(SOURCE), source_bytes=SOURCE.stat().st_size,
        code_repo_path=str(HERE.relative_to(REPO)), code_sha256=sha256(HERE),
        grandchild_code_repo_path=str(gc_path.relative_to(REPO)),
        grandchild_code_sha256=sha256(gc_path),
        python=sys.version, numpy=np.__version__, pandas=pd.__version__,
        master_seed=MASTER_SEED, seed_derivation="numpy SeedSequence(master).spawn(100); each child generate_state(1,uint64)[0]",
        generator="numpy.random.default_rng (PCG64); paired permutation plus uniform inverse-CDF choices",
        repetition_seeds=[int(value) for value in seeds],
        n=n, team_count=len(caps), theta=theta, gamma=GAMMA,
        congestion_reference_mean=c_mean, congestion_reference_population_sd=c_sd,
        implied_raw_scale_multiplier=1 / c_sd,
        selection_fractions=list(SELECTION_FRACTIONS), slot_counts=slots,
        rho_values=list(RHO_VALUES), lambda_values=[0.0, 1.0],
        bins=BINS, elapsed_seconds=time.monotonic() - start,
        outputs=[dict(path=str(path.relative_to(REPO)), bytes=path.stat().st_size, sha256=sha256(path)) for path in outputs],
        population_audit=audit,
    )
    json_write(RECORDS / f"{PREFIX}_run_record.json", manifest)
    print(f"Run complete in {manifest['elapsed_seconds']:.1f}s; reference sd={c_sd:.6g}; K={slots}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Execute the documented 100 paired repetitions")
    args = parser.parse_args()
    if not args.run:
        parser.error("Pass --run to execute the experiment")
    run_experiment()
