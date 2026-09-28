#!/usr/bin/env python3
"""Bounded retrospective ranking diagnostic on the frozen 2015 MBB population."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[6]
WORK = ROOT / "3-Master_Plan/VECTOR_work/new_VECTOR_work/assort_analysis"
SETTINGS_PATH = HERE / "ASSORT_20260927_empirical_selection_replay_v1_settings.json"
OUTPUT = WORK / "outputs/empirical_selection_replay_2015"
STEM = "ASSORT_20260927_empirical_selection_replay_v1"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def relpath(path: Path) -> str:
    return str(path.relative_to(ROOT))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def source_paths(settings: dict) -> list[Path]:
    paths = [
        ROOT / settings["input_population"],
        ROOT / settings["input_population_record"],
        ROOT / settings["draft_lookup"],
        ROOT / settings["fitted_parameters"],
        ROOT / settings["assignment_fit_record"],
        SETTINGS_PATH,
        Path(__file__).resolve(),
    ]
    paths.extend(ROOT / item for item in settings["source_method_files"])
    return paths


def verify_frozen_input(input_path: Path, record_path: Path) -> None:
    record = read_json(record_path)
    rel = relpath(input_path)
    item = next((x for x in record["outputs"] if x["path"] == rel), None)
    if item is None or sha256(input_path) != item["sha256"]:
        raise RuntimeError("Accepted 2015 population does not match its saved execution record.")


def stable_logistic(x: np.ndarray) -> np.ndarray:
    return np.exp(-np.logaddexp(0.0, -np.asarray(x, dtype=float)))


def softmax(logits: np.ndarray) -> np.ndarray:
    z = np.asarray(logits, dtype=float)
    return np.exp(z - np.logaddexp.reduce(z))


def top_k_ids(frame: pd.DataFrame, score_col: str, k: int) -> list[int]:
    ranked = frame.sort_values(
        [score_col, "athlete_id"], ascending=[False, True], kind="mergesort"
    )
    return ranked.head(k)["athlete_id"].astype(int).tolist()


def overlap_metrics(predicted: set[int], actual: set[int], n: int) -> dict:
    tp = len(predicted & actual)
    k = len(predicted)
    actual_n = len(actual)
    return {
        "selected_count": k,
        "actual_count": actual_n,
        "correct_selections": tp,
        "missed_actual_selectees": actual_n - tp,
        "selected_nonselectees": k - tp,
        "precision": tp / k if k else None,
        "recall": tp / actual_n if actual_n else None,
        "intersection_over_union": tp / len(predicted | actual) if predicted | actual else None,
        "expected_overlap_uniform_random_same_k": (k * actual_n / n) if n else None,
    }


def build_rank_bins(frame: pd.DataFrame, column: str, bins: int) -> pd.Series:
    # Sort by the actual numeric peer axis; athlete identifier breaks exact ties.
    # Equal-count bins are then frozen and reused for every observed/model series.
    order = frame.sort_values([column, "athlete_id"], kind="mergesort").index.to_numpy()
    labels = np.empty(len(order), dtype=np.int16)
    for bin_id, indices in enumerate(np.array_split(np.arange(len(order)), bins), start=1):
        labels[indices] = bin_id
    out = pd.Series(index=order, data=labels, dtype="int16")
    return out.reindex(frame.index)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", required=True,
                        help="Required explicit switch; writes only to the named output folder.")
    args = parser.parse_args()
    if not args.run:
        raise SystemExit("--run is required.")

    if OUTPUT.exists() and any(OUTPUT.iterdir()):
        raise RuntimeError(f"Refusing to overwrite existing outputs in {OUTPUT}")
    OUTPUT.mkdir(parents=True, exist_ok=True)

    settings = read_json(SETTINGS_PATH)
    if settings["experiment_id"] != STEM:
        raise RuntimeError("Settings experiment identifier does not match this driver.")
    if not settings.get("no_refitting") or not settings.get("no_reassignment"):
        raise RuntimeError("Settings must keep fitting and assignment outside this comparison.")

    input_path = ROOT / settings["input_population"]
    input_record_path = ROOT / settings["input_population_record"]
    lookup_path = ROOT / settings["draft_lookup"]
    fit_path = ROOT / settings["fitted_parameters"]
    rho_path = ROOT / settings["assignment_fit_record"]
    verify_frozen_input(input_path, input_record_path)

    sources = source_paths(settings)
    before = {relpath(p): sha256(p) for p in sources}

    population = pd.read_csv(input_path)
    expected_n = int(settings["expected_population_players"])
    expected_teams = int(settings["expected_population_teams"])
    if len(population) != expected_n or population["athlete_id"].nunique() != expected_n:
        raise RuntimeError("Frozen player count or unique-identifier check failed.")
    if population["team_id"].nunique() != expected_teams:
        raise RuntimeError("Frozen team count check failed.")
    if population["athlete_id"].isna().any() or population["team_id"].isna().any():
        raise RuntimeError("Missing athlete/team identifiers in frozen input.")
    population["athlete_id"] = pd.to_numeric(population["athlete_id"], errors="raise").astype("int64")
    if population["athlete_id"].duplicated().any():
        raise RuntimeError("Athlete identifiers are not unique in frozen population.")

    ability_col = "ability_standardized"
    if ability_col not in population:
        raise RuntimeError(f"Required frozen ability column is missing: {ability_col}")
    population[ability_col] = pd.to_numeric(population[ability_col], errors="raise")
    if not np.isfinite(population[ability_col].to_numpy()).all():
        raise RuntimeError("Non-finite ability values in frozen population.")

    lookup = pd.read_csv(lookup_path, low_memory=False)
    lookup["athlete_id"] = pd.to_numeric(lookup["athlete_id"], errors="raise")
    if lookup["athlete_id"].isna().any() or lookup["athlete_id"].duplicated().any():
        raise RuntimeError("Draft lookup identifiers must be present and unique.")
    lookup["athlete_id"] = lookup["athlete_id"].astype("int64")
    lookup["draft_year"] = pd.to_numeric(lookup["draft_year"], errors="raise").astype("int64")
    lookup_cols = ["athlete_id", "draft_year", "overall_pick", "draft_name_first",
                   "draft_name_last", "match_tier", "match_score"]
    lookup = lookup[lookup_cols].copy()
    in_population = lookup["athlete_id"].isin(population["athlete_id"])
    lookup = lookup.loc[in_population].copy()
    annual_ids = set(lookup.loc[lookup["draft_year"] == int(settings["season"]), "athlete_id"].astype(int))
    ever_ids = set(lookup["athlete_id"].astype(int))
    if len(annual_ids) != int(settings["expected_annual_drafted"]):
        raise RuntimeError("The accepted 2015 annual draft count differs from the locked expectation.")
    if len(ever_ids) != int(settings["expected_ever_drafted"]):
        raise RuntimeError("The accepted ever-drafted count differs from the locked expectation.")
    if not annual_ids.issubset(set(population["athlete_id"].astype(int))):
        raise RuntimeError("A 2015 draft identity is not present in the accepted population.")

    fit = read_json(fit_path)
    gamma = float(fit["gamma_hat"])
    lam = float(fit["lambda_hat"])
    temperature = float(fit["t_hat"])
    if temperature <= 0:
        raise RuntimeError("Saved fitted temperature must be positive.")
    rho_fit = read_json(rho_path)
    rho_star = float(rho_fit["longitudinal"]["rho_star_longitudinal"])

    # Apply the saved calibration's viable-share threshold convention on this
    # explicitly transported 2015 population.
    ability = population[ability_col].to_numpy(dtype=float)
    theta_quantile = 1.0 - len(ever_ids) / len(population)
    theta = float(np.quantile(ability, theta_quantile, method="linear"))
    viability = stable_logistic(gamma * (ability - theta))
    population["viability"] = viability
    population["team_congestion"] = population.groupby("team_id", sort=False)["viability"].transform("mean")
    counts = population.groupby("team_id", sort=False)[ability_col].transform("size")
    if (counts <= 1).any():
        raise RuntimeError("A team has too few players to compute its leave-one-out peer mean.")
    sums = population.groupby("team_id", sort=False)[ability_col].transform("sum")
    population["peer_mean_loo"] = (sums - population[ability_col]) / (counts - 1)

    population["score_fitted_logit"] = ability / temperature - lam * population["team_congestion"].to_numpy()
    population["score_algebraic_equivalent"] = (
        ability - temperature * lam * population["team_congestion"].to_numpy()
    ) / temperature
    if not np.allclose(population["score_fitted_logit"], population["score_algebraic_equivalent"],
                       rtol=1e-13, atol=1e-13):
        raise RuntimeError("Temperature/lambda algebraic equivalence check failed.")
    population["score_ability_only"] = ability / temperature
    ranked_fit = population.sort_values(
        ["score_fitted_logit", "athlete_id"], ascending=[False, True], kind="mergesort"
    )
    ranked_ability = population.sort_values(
        ["score_ability_only", "athlete_id"], ascending=[False, True], kind="mergesort"
    )
    population["score_rank"] = 0
    population.loc[ranked_fit.index, "score_rank"] = np.arange(1, len(population) + 1)
    population["ability_only_rank"] = 0
    population.loc[ranked_ability.index, "ability_only_rank"] = np.arange(1, len(population) + 1)

    # This is the calibration's season-softmax ranking mass; it sums to one and
    # is not a 45-player inclusion probability.
    population["season_softmax_mass"] = softmax(population["score_fitted_logit"].to_numpy())
    if not np.isclose(population["season_softmax_mass"].sum(), 1.0, atol=1e-12):
        raise RuntimeError("Season-softmax mass does not sum to one.")

    draft_lookup = lookup.set_index("athlete_id")
    population["draft_year"] = population["athlete_id"].map(draft_lookup["draft_year"]).astype("Int64")
    population["overall_pick"] = population["athlete_id"].map(draft_lookup["overall_pick"]).astype("Int64")
    for col in ["draft_name_first", "draft_name_last", "match_tier", "match_score"]:
        population[col] = population["athlete_id"].map(draft_lookup[col])
    population["drafted_2015"] = population["athlete_id"].isin(annual_ids)
    population["ever_drafted_in_lookup"] = population["athlete_id"].isin(ever_ids)

    k_annual = len(annual_ids)
    k_ever = len(ever_ids)
    fitted_annual = set(top_k_ids(population, "score_fitted_logit", k_annual))
    ability_annual = set(top_k_ids(population, "score_ability_only", k_annual))
    fitted_ever = set(top_k_ids(population, "score_fitted_logit", k_ever))
    ability_ever = set(top_k_ids(population, "score_ability_only", k_ever))

    comparison = []
    for name, predicted, actual in [
        ("fitted_score_top_45_vs_2015_draft", fitted_annual, annual_ids),
        ("ability_only_top_45_vs_2015_draft", ability_annual, annual_ids),
        ("fitted_score_top_105_vs_ever_drafted", fitted_ever, ever_ids),
        ("ability_only_top_105_vs_ever_drafted", ability_ever, ever_ids),
    ]:
        result = {"comparison": name, **overlap_metrics(predicted, actual, len(population))}
        result["predicted_id_list"] = ",".join(map(str, sorted(predicted)))
        result["actual_id_list"] = ",".join(map(str, sorted(actual)))
        comparison.append(result)

    def identity_deltas(predicted: set[int], actual: set[int], baseline: set[int]) -> dict:
        return {
            "correct_ids": sorted(predicted & actual),
            "missed_actual_ids": sorted(actual - predicted),
            "selected_nonactual_ids": sorted(predicted - actual),
            "displaced_from_ability_only_ids": sorted(baseline - predicted),
            "added_by_congestion_ids": sorted(predicted - baseline),
        }

    annual_delta = identity_deltas(fitted_annual, annual_ids, ability_annual)
    ever_delta = identity_deltas(fitted_ever, ever_ids, ability_ever)

    peer_bins = int(settings["peer_curve_bins"])
    population["peer_bin"] = build_rank_bins(population, "peer_mean_loo", peer_bins)
    curve_groups = {
        "actual_2015_draft": population["drafted_2015"].to_numpy(dtype=bool),
        "fitted_top_45": population["athlete_id"].isin(fitted_annual).to_numpy(),
        "ability_only_top_45": population["athlete_id"].isin(ability_annual).to_numpy(),
        "actual_ever_drafted": population["ever_drafted_in_lookup"].to_numpy(dtype=bool),
        "fitted_top_105": population["athlete_id"].isin(fitted_ever).to_numpy(),
        "ability_only_top_105": population["athlete_id"].isin(ability_ever).to_numpy(),
    }
    curve_rows = []
    for bin_id, frame in population.groupby("peer_bin", sort=True):
        row = {
            "peer_bin_low_to_high": int(bin_id),
            "peer_axis_min": float(frame["peer_mean_loo"].min()),
            "peer_axis_max": float(frame["peer_mean_loo"].max()),
            "denominator_players": int(len(frame)),
            "mean_peer_axis": float(frame["peer_mean_loo"].mean()),
        }
        for label, flags in curve_groups.items():
            mask = population.index.isin(frame.index)
            successes = int(np.asarray(flags, dtype=bool)[mask].sum())
            row[f"{label}_count"] = successes
            row[f"{label}_rate"] = successes / len(frame)
        curve_rows.append(row)
    curves = pd.DataFrame(curve_rows)
    if len(curves) != peer_bins or int(curves["denominator_players"].sum()) != len(population):
        raise RuntimeError("Peer-bin count or denominator conservation failed.")

    teams = (
        population.groupby(["team_id", "team_short_display_name_x"], as_index=False)
        .agg(players=("athlete_id", "size"),
             mean_ability=(ability_col, "mean"),
             congestion=("team_congestion", "first"),
             actual_2015_draftees=("drafted_2015", "sum"),
             fitted_top_45=("athlete_id", lambda s: int(s.isin(fitted_annual).sum())),
             ability_only_top_45=("athlete_id", lambda s: int(s.isin(ability_annual).sum())),
             actual_ever_drafted=("ever_drafted_in_lookup", "sum"),
             fitted_top_105=("athlete_id", lambda s: int(s.isin(fitted_ever).sum())),
             ability_only_top_105=("athlete_id", lambda s: int(s.isin(ability_ever).sum())))
        .sort_values("team_id")
    )

    selected_union = fitted_annual | ability_annual | fitted_ever | ability_ever | annual_ids | ever_ids
    selected = population.loc[population["athlete_id"].isin(selected_union)].copy()
    selected["selected_by_fitted_top_45"] = selected["athlete_id"].isin(fitted_annual)
    selected["selected_by_ability_only_top_45"] = selected["athlete_id"].isin(ability_annual)
    selected["selected_by_fitted_top_105"] = selected["athlete_id"].isin(fitted_ever)
    selected["selected_by_ability_only_top_105"] = selected["athlete_id"].isin(ability_ever)

    summary = {
        "experiment_id": STEM,
        "status": "executed_pending_review",
        "season": int(settings["season"]),
        "players": int(len(population)),
        "teams": int(population["team_id"].nunique()),
        "annual_draft_count": int(k_annual),
        "ever_drafted_lookup_count": int(k_ever),
        "annual_draft_match_tier_counts": lookup.loc[lookup["draft_year"] == int(settings["season"]), "match_tier"].value_counts(dropna=False).to_dict(),
        "annual_draft_match_score_min": float(lookup.loc[lookup["draft_year"] == int(settings["season"]), "match_score"].min()),
        "annual_draft_match_score_median": float(lookup.loc[lookup["draft_year"] == int(settings["season"]), "match_score"].median()),
        "gamma_star": gamma,
        "lambda_star": lam,
        "temperature_star": temperature,
        "rho_star_from_separate_assignment_fit_not_used": rho_star,
        "theta": theta,
        "theta_quantile": theta_quantile,
        "mean_team_congestion": float(population.groupby("team_id")["team_congestion"].first().mean()),
        "season_softmax_mass_sum": float(population["season_softmax_mass"].sum()),
        "season_softmax_mass_on_actual_2015_draftees": float(population.loc[population["drafted_2015"], "season_softmax_mass"].sum()),
        "annual_fitted_vs_actual": overlap_metrics(fitted_annual, annual_ids, len(population)),
        "annual_ability_only_vs_actual": overlap_metrics(ability_annual, annual_ids, len(population)),
        "annual_congestion_winner_identity_changes": int(len(fitted_annual ^ ability_annual)),
        "annual_congestion_displaced_ability_only_ids": annual_delta["displaced_from_ability_only_ids"],
        "annual_congestion_added_ids": annual_delta["added_by_congestion_ids"],
        "ever_fitted_vs_actual": overlap_metrics(fitted_ever, ever_ids, len(population)),
        "ever_ability_only_vs_actual": overlap_metrics(ability_ever, ever_ids, len(population)),
        "ever_congestion_winner_identity_changes": int(len(fitted_ever ^ ability_ever)),
        "peer_curve_bins": peer_bins,
        "peer_bin_denominators": curves["denominator_players"].astype(int).tolist(),
        "settings_file": relpath(SETTINGS_PATH),
        "parameter_file": relpath(fit_path),
        "interpretation": "Transported-parameter retrospective ranking diagnostic; top-K rankings are not the Bernoulli calibration probabilities or a causal congestion estimate."
    }

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True, sharey=True)
    plotting = [
        (axes[0], "Annual 2015 draft: K=45",
         [("actual_2015_draft_rate", "Actual 2015 draftees"),
          ("fitted_top_45_rate", "Fitted score: top 45"),
          ("ability_only_top_45_rate", "Ability only: top 45")]),
        (axes[1], "Ever drafted in saved lookup: K=105",
         [("actual_ever_drafted_rate", "Actual ever drafted"),
          ("fitted_top_105_rate", "Fitted score: top 105"),
          ("ability_only_top_105_rate", "Ability only: top 105")]),
    ]
    x = curves["mean_peer_axis"].to_numpy()
    for ax, title, series in plotting:
        for col, label in series:
            ax.plot(x, curves[col].to_numpy(), marker="o", linewidth=1.7, label=label)
        ax.set_title(title)
        ax.set_xlabel("Mean leave-one-out teammate ability (within-season standardized points per minute)")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8)
    axes[0].set_ylabel("Share selected/drafted within equal-count peer bin")
    fig.suptitle("2015 actual-roster ranking comparison on the leave-one-out teammate axis")
    figure_path = OUTPUT / f"{STEM}_peer_bin_comparison.png"
    fig.savefig(figure_path, dpi=160)
    plt.close(fig)

    outputs = {
        f"{STEM}_player_scores.csv": population,
        f"{STEM}_selected_and_actual_players.csv": selected,
        f"{STEM}_selection_comparison.csv": pd.DataFrame(comparison),
        f"{STEM}_peer_bin_summary.csv": curves,
        f"{STEM}_team_summary.csv": teams,
        f"{STEM}_summary.json": None,
    }
    for name, frame in outputs.items():
        path = OUTPUT / name
        if name.endswith(".json"):
            path.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        else:
            frame.to_csv(path, index=False)

    after = {relpath(p): sha256(p) for p in sources}
    if before != after:
        raise RuntimeError("An input, code, settings, or source-method file changed during execution.")

    record_path = WORK / f"docs/run_records/{STEM}_run_record.json"
    record_path.parent.mkdir(parents=True, exist_ok=True)
    output_records = []
    for path in sorted(OUTPUT.iterdir()):
        output_records.append({"path": relpath(path), "sha256": sha256(path), "bytes": path.stat().st_size})
    record = {
        "experiment_id": STEM,
        "status": "executed_pending_review",
        "started_or_completed_utc": datetime.now(timezone.utc).isoformat(),
        "driver": relpath(Path(__file__).resolve()),
        "settings": relpath(SETTINGS_PATH),
        "input_and_method_sha256": before,
        "input_and_method_sha256_after": after,
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "matplotlib": matplotlib.__version__,
        },
        "parameters_and_choices": summary,
        "checks": [
            "frozen_population_hash_matches_source_run_record",
            "unique_nonmissing_population_ids",
            "unique_nonmissing_draft_lookup_ids",
            "expected_2015_and_ever_draft_counts",
            "saved_fitted_parameter_values_loaded_without_refitting",
            "temperature_lambda_score_formula_matches_algebraic_equivalent",
            "season_softmax_mass_sums_to_one_and_not_called_topK_probability",
            "exact_topK_counts_with_identifier_tie_break",
            "actual_and_selected_ids_within_frozen_population",
            "peer_bins_frozen_once_equal_count_and_denominators_conserve_population",
            "all_input_settings_driver_and_method_hashes_unchanged",
            "all_output_files_hashed"
        ],
        "outputs": output_records,
        "scope_note": "No assignment, refit, filter change, stochastic selection, random benchmark draw, or sensitivity sweep was performed."
    }
    record_path.write_text(json.dumps(record, indent=2, allow_nan=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": record["status"],
        "output_directory": relpath(OUTPUT),
        "run_record": relpath(record_path),
        "primary": summary["annual_fitted_vs_actual"],
        "ability_only": summary["annual_ability_only_vs_actual"],
        "winner_identity_changes": summary["annual_congestion_winner_identity_changes"],
        "output_count": len(output_records),
    }, indent=2))


if __name__ == "__main__":
    main()
