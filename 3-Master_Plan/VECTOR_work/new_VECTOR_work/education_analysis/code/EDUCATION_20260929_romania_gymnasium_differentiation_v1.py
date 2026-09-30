#!/usr/bin/env python3
"""Alba 2001 originating-gymnasium differentiation gate.

This bounded diagnostic uses national examination performance only. It checks
whether the 168 recovered origin-gymnasium applicant groups are differentiated
relative to size-preserving random groupings. It does not model high-school
placement, estimate congestion, search for an outcome curve, or make a causal
claim.

Names are used by the source parser only while a page is in memory. They are
never saved by this program. Saved analytical outputs are gymnasium-level
aggregates, random-reference summaries, figures, and provenance records.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib
import importlib.util
import json
import math
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


REPO = Path(__file__).resolve().parents[5]
BASE = Path(__file__).resolve().parents[1]
CODE_PATH = Path(__file__).resolve()
STEM = "EDUCATION_20260929_romania_gymnasium_differentiation_v1"
OUT = BASE / "outputs" / "romania_alba_2001_differentiation_v1"
STRUCTURAL_OUT = BASE / "outputs" / "romania_alba_2001_structural_audit_20260929"
DECISION = (
    BASE
    / "docs"
    / "decisions"
    / "EDUCATION_20260929_Romania_gymnasium_differentiation_gate_v1.md"
)
RUN_RECORD = BASE / "docs" / "run_records" / f"{STEM}_run_record.json"

SEED = 20260929
RANDOMIZATIONS = 1000
GRID_POINTS = 401
RETRY_PASSES = 3
RETRY_COOLDOWN_SECONDS = 180.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_structural_module():
    """Load the audited parser without duplicating historical HTML rules."""
    path = CODE_PATH.with_name("EDUCATION_20260929_alba_2001_structural_audit.py")
    spec = importlib.util.spec_from_file_location("alba_structural", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_completed_checkpoint() -> tuple[list[dict], dict[str, dict]]:
    """Require the completed 168-code structural checkpoint before retrieval."""
    directory_path = STRUCTURAL_OUT / "origin_school_directory.json"
    summary_path = STRUCTURAL_OUT / "origin_report_check_summary.json"
    checks_path = STRUCTURAL_OUT / "origin_report_checks.jsonl"
    unresolved_path = STRUCTURAL_OUT / "unresolved_addresses.json"
    for path in [directory_path, summary_path, checks_path, unresolved_path]:
        if not path.exists():
            raise FileNotFoundError(f"Required structural-audit file is missing: {path}")

    directory = json.loads(directory_path.read_text())
    summary = json.loads(summary_path.read_text())
    unresolved = json.loads(unresolved_path.read_text())
    latest = {}
    for line in checks_path.read_text().splitlines():
        if line.strip():
            record = json.loads(line)
            latest[record["source_code"]] = record

    if len(directory) != 168:
        raise ValueError(f"Expected 168 directory codes; found {len(directory)}")
    if summary.get("completed_codes") != 168 or summary.get("unresolved_codes") != 0:
        raise ValueError("Structural audit is not complete")
    if unresolved:
        raise ValueError("Structural unresolved-address queue is not empty")
    if len(latest) != 168:
        raise ValueError(f"Expected 168 latest school checkpoints; found {len(latest)}")
    incomplete = [
        code for code, record in latest.items()
        if record.get("status") != "candidate_report_recovered"
        or record.get("placement_report_unavailable", False)
    ]
    if incomplete:
        raise ValueError(f"Incomplete structural checkpoints: {incomplete[:10]}")
    return directory, latest


def make_event_writer(path: Path):
    """Record every retrieval event while printing only meaningful exceptions."""
    def emit(event: dict) -> None:
        record = {"utc": datetime.now(timezone.utc).isoformat(), **event}
        with path.open("a") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            stream.flush()

        kind = record.get("kind")
        if kind == "adaptive_pace" and record.get("direction") == "slower":
            print(
                f"  ARCHIVE PACE: slowing from {record.get('old_seconds'):.2f}s "
                f"to {record.get('new_seconds'):.2f}s after a failed request.",
                flush=True,
            )
        elif kind == "http_attempt" and record.get("status") not in (200, 302):
            print(
                f"  ARCHIVE RESPONSE: status={record.get('status')} "
                f"error={record.get('error') or 'none'}",
                flush=True,
            )
        elif kind in {
            "fetch_error",
            "parse_error",
            "robots_denied",
            "robots_unavailable",
            "stopped",
        }:
            print(f"  ARCHIVE EVENT: {kind}: {record.get('error') or record.get('reason')}", flush=True)
        elif kind == "retrieval_wait" and float(record.get("seconds", 0)) >= 10:
            print(
                f"  ARCHIVE WAIT: {record['seconds']:.1f}s — {record.get('reason', 'backoff')}",
                flush=True,
            )
    return emit


def retrieve_school_reports(
    structural,
    directory: list[dict],
    expected: dict[str, dict],
    *,
    archive_use_acknowledged: bool,
    initial_interval_seconds: float,
    minimum_interval_seconds: float,
    maximum_interval_seconds: float,
    max_runtime_hours: float,
) -> dict[str, list[dict]]:
    """Retrieve all reports into memory, retrying unresolved addresses by pass."""
    events_path = OUT / "retrieval_events.jsonl"
    structural.OUT = OUT
    structural.emit = make_event_writer(events_path)
    structural.configure_retrieval(
        archive_use_acknowledged,
        initial_interval_seconds=initial_interval_seconds,
        minimum_interval_seconds=minimum_interval_seconds,
        maximum_interval_seconds=maximum_interval_seconds,
        max_runtime_hours=max_runtime_hours,
    )

    recovered: dict[str, list[dict]] = {}
    pending = list(directory)
    try:
        from tqdm.auto import tqdm
    except ImportError:
        tqdm = None

    for pass_number in range(1, RETRY_PASSES + 1):
        if not pending:
            break
        if pass_number > 1:
            structural.CLIENT.wait_between_passes(RETRY_COOLDOWN_SECONDS, pass_number)
        print(
            f"\nRETRIEVAL PASS {pass_number}/{RETRY_PASSES}: "
            f"{len(pending)} school reports remain.",
            flush=True,
        )
        next_pending = []
        pass_started = time.perf_counter()
        bar = (
            tqdm(total=len(pending), desc=f"Alba reports pass {pass_number}", unit="school", dynamic_ncols=True)
            if tqdm is not None else None
        )
        try:
            for position, school in enumerate(pending, 1):
                code = school["code"]
                page = structural.fetch(
                    school["candidate_report"],
                    f"differentiation_origin_{code}",
                )
                if page is None:
                    next_pending.append(school)
                    status = "UNRESOLVED"
                else:
                    rows = page[1]
                    expected_rows = int(expected[code]["candidate_rows"])
                    if len(rows) != expected_rows:
                        raise ValueError(
                            f"School {code}: retrieved {len(rows)} rows; "
                            f"completed audit recorded {expected_rows}"
                        )
                    recovered[code] = rows
                    status = f"recovered {len(rows)} rows"

                elapsed = time.perf_counter() - pass_started
                rate = elapsed / position
                eta = rate * (len(pending) - position)
                if bar is not None:
                    bar.update(1)
                    bar.set_postfix(
                        recovered=f"{len(recovered)}/168",
                        unresolved=len(next_pending),
                        interval=f"{structural.CLIENT.interval:.1f}s",
                        refresh=True,
                    )
                else:
                    print(
                        f"  {position}/{len(pending)} code {code}: {status}; "
                        f"cumulative {len(recovered)}/168; ETA {eta/60:.1f} min; "
                        f"interval {structural.CLIENT.interval:.1f}s",
                        flush=True,
                    )
                if status == "UNRESOLVED" or position % 10 == 0 or position == len(pending):
                    print(
                        f"  CHECKPOINT: {position}/{len(pending)} this pass; code {code} {status}; "
                        f"{len(recovered)}/168 recovered; ETA {eta/60:.1f} min.",
                        flush=True,
                    )
        finally:
            if bar is not None:
                bar.close()
        pending = next_pending

    unresolved = [
        {
            "source_code": school["code"],
            "candidate_report": school["candidate_report"],
        }
        for school in pending
    ]
    (OUT / "unresolved_addresses.json").write_text(
        json.dumps(unresolved, ensure_ascii=False, indent=2) + "\n"
    )
    if unresolved:
        raise RuntimeError(
            f"{len(unresolved)} required reports remain unresolved; no diagnostics calculated"
        )
    return recovered


def truncated_composite(exam: np.ndarray, grades: np.ndarray) -> np.ndarray:
    """Official positive-score rule: retain two decimals without rounding."""
    return np.floor((0.75 * exam + 0.25 * grades + 1e-10) * 100.0) / 100.0


def build_name_free_frame(structural, reports: dict[str, list[dict]]) -> tuple[pd.DataFrame, dict]:
    """Extract only scores and source code; names never enter the returned frame."""
    records = []
    duplicate_names_within_reports = 0
    for code in sorted(reports, key=lambda value: int(value)):
        rows = reports[code]
        names = [row.get("Nume", "") for row in rows]
        duplicate_names_within_reports += sum(
            count - 1 for count in collections.Counter(names).values() if count > 1
        )
        for row in rows:
            exam = structural.numeric(row, "capacitate")
            grades = structural.numeric(row, "absolvire")
            composite = structural.numeric(row, "admitere")
            records.append(
                {
                    "source_code": code,
                    "exam_score": exam,
                    "grades_5_8_average": grades,
                    "admission_composite": composite,
                }
            )

    frame = pd.DataFrame.from_records(records)
    required = ["exam_score", "grades_5_8_average", "admission_composite"]
    missing = frame[required].isna().sum().to_dict()
    if any(missing.values()):
        raise ValueError(f"Missing score components prevent the locked analysis: {missing}")
    values = frame[required].to_numpy(dtype=float)
    if not np.isfinite(values).all():
        raise ValueError("Non-finite score component found")
    if ((values < 0) | (values > 10)).any():
        raise ValueError("Score outside the expected 0–10 range")

    expected_composite = truncated_composite(
        frame["exam_score"].to_numpy(dtype=float),
        frame["grades_5_8_average"].to_numpy(dtype=float),
    )
    formula_disagreements = int(
        (~np.isclose(expected_composite, frame["admission_composite"], atol=1e-10, rtol=0)).sum()
    )
    if formula_disagreements:
        raise ValueError(
            f"Found {formula_disagreements} admission-composite formula disagreements; stopped"
        )

    mean = float(frame["exam_score"].mean())
    population_sd = float(frame["exam_score"].std(ddof=0))
    if population_sd <= 0:
        raise ValueError("National examination score has no variation")
    frame["A_z"] = (frame["exam_score"] - mean) / population_sd
    diagnostics = {
        "rows": int(len(frame)),
        "directory_codes": int(len(reports)),
        "nonempty_gymnasium_codes": int(frame["source_code"].nunique()),
        "zero_applicant_source_codes": sorted(
            [code for code, rows in reports.items() if len(rows) == 0],
            key=int,
        ),
        "duplicate_name_occurrences_within_same_report": int(duplicate_names_within_reports),
        "formula_disagreements": formula_disagreements,
        "exam_mean": mean,
        "exam_population_sd": population_sd,
    }
    return frame, diagnostics


def sorting_index(values: np.ndarray, groups: np.ndarray) -> float:
    """Player-weighted between-group fraction of total variation."""
    count = int(groups.max()) + 1
    counts = np.bincount(groups, minlength=count)
    means = np.bincount(groups, weights=values, minlength=count) / counts
    total = np.square(values - values.mean()).sum()
    within = np.square(values - means[groups]).sum()
    return float(1.0 - within / total)


def group_extrema(values: np.ndarray, groups: np.ndarray, count: int) -> tuple[np.ndarray, np.ndarray]:
    lows = np.full(count, np.inf)
    highs = np.full(count, -np.inf)
    np.minimum.at(lows, groups, values)
    np.maximum.at(highs, groups, values)
    return lows, highs


def coverage_curve(lows: np.ndarray, highs: np.ndarray, grid: np.ndarray) -> np.ndarray:
    return ((grid[None, :] >= lows[:, None]) & (grid[None, :] <= highs[:, None])).sum(axis=0)


def run_diagnostics(
    frame: pd.DataFrame,
    *,
    directory_code_count: int,
    zero_applicant_source_codes: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Calculate observed summaries and the locked size-preserving reference."""
    group_index, labels = pd.factorize(frame["source_code"], sort=True)
    group_index = group_index.astype(np.int64)
    values = frame["A_z"].to_numpy(dtype=float)
    raw = frame["exam_score"].to_numpy(dtype=float)
    group_count = len(labels)
    counts = np.bincount(group_index, minlength=group_count)
    if group_count + len(zero_applicant_source_codes) != directory_code_count:
        raise ValueError(
            "Nonempty and zero-applicant source codes do not reconcile to the directory"
        )
    if np.any(counts == 0):
        raise ValueError("An empty group entered the applicant-level calculation")

    grouped = frame.groupby("source_code", sort=True, observed=True)["A_z"]
    groups = grouped.agg(
        applicant_n="size",
        A_min="min",
        A_q25=lambda s: s.quantile(0.25),
        A_median="median",
        A_mean="mean",
        A_q75=lambda s: s.quantile(0.75),
        A_max="max",
        A_sd_population=lambda s: s.std(ddof=0),
    ).reset_index()
    groups["A_range_width"] = groups["A_max"] - groups["A_min"]
    groups["A_iqr_width"] = groups["A_q75"] - groups["A_q25"]

    observed_h = sorting_index(values, group_index)
    observed_lows, observed_highs = group_extrema(values, group_index, group_count)
    grid = np.linspace(values.min(), values.max(), GRID_POINTS)
    observed_coverage = coverage_curve(observed_lows, observed_highs, grid)

    rng = np.random.default_rng(SEED)
    null_h = np.empty(RANDOMIZATIONS)
    null_means = np.empty((RANDOMIZATIONS, group_count))
    null_widths = np.empty((RANDOMIZATIONS, group_count))
    null_coverage = np.empty((RANDOMIZATIONS, GRID_POINTS), dtype=np.int32)
    print(
        f"\nRANDOM REFERENCE: {RANDOMIZATIONS:,} size-preserving reassignments begin.",
        flush=True,
    )
    started = time.perf_counter()
    for draw in range(RANDOMIZATIONS):
        permuted = rng.permutation(values)
        means = np.bincount(group_index, weights=permuted, minlength=group_count) / counts
        lows, highs = group_extrema(permuted, group_index, group_count)
        null_means[draw] = means
        null_widths[draw] = highs - lows
        null_h[draw] = sorting_index(permuted, group_index)
        null_coverage[draw] = coverage_curve(lows, highs, grid)
        completed = draw + 1
        if completed % 100 == 0 or completed == RANDOMIZATIONS:
            elapsed = time.perf_counter() - started
            eta = elapsed / completed * (RANDOMIZATIONS - completed)
            print(
                f"  Random reference {completed:>4}/{RANDOMIZATIONS}: "
                f"{completed/RANDOMIZATIONS:>5.1%}; elapsed {elapsed:.1f}s; ETA {eta:.1f}s.",
                flush=True,
            )

    # Cross-check the central statistic using the established repository routine.
    sys.path.insert(0, str(REPO / "sports"))
    grandchild = importlib.import_module("541_grandchild_homophily_assign")
    repository_h = float(grandchild.realized_sorting_index_H_sort(values, group_index))
    if not np.isclose(observed_h, repository_h, atol=1e-12, rtol=0):
        raise AssertionError("Repository sorting-index cross-check failed")

    groups["random_mean_p025"] = np.quantile(null_means, 0.025, axis=0)
    groups["random_mean_median"] = np.quantile(null_means, 0.5, axis=0)
    groups["random_mean_p975"] = np.quantile(null_means, 0.975, axis=0)
    groups["mean_outside_random_95"] = (
        (groups["A_mean"] < groups["random_mean_p025"])
        | (groups["A_mean"] > groups["random_mean_p975"])
    )
    groups["random_width_p025"] = np.quantile(null_widths, 0.025, axis=0)
    groups["random_width_median"] = np.quantile(null_widths, 0.5, axis=0)
    groups["random_width_p975"] = np.quantile(null_widths, 0.975, axis=0)

    coverage = pd.DataFrame(
        {
            "A_z": grid,
            "observed_gymnasiums_covering": observed_coverage,
            "random_p025": np.quantile(null_coverage, 0.025, axis=0),
            "random_median": np.quantile(null_coverage, 0.5, axis=0),
            "random_p975": np.quantile(null_coverage, 0.975, axis=0),
        }
    )
    draws = pd.DataFrame({"draw": np.arange(1, RANDOMIZATIONS + 1), "H_sort": null_h})

    n = len(frame)
    thresholds = {}
    for threshold in [1, 2, 5, 10, 20]:
        mask = counts >= threshold
        thresholds[str(threshold)] = {
            "gymnasium_codes": int(mask.sum()),
            "applicants": int(counts[mask].sum()),
            "applicant_fraction": float(counts[mask].sum() / n),
        }

    usable = groups.loc[groups["applicant_n"] >= 5].copy()
    lows = usable["A_min"].to_numpy()
    highs = usable["A_max"].to_numpy()
    pair_total = len(usable) * (len(usable) - 1) // 2
    pair_overlap = sum(
        max(lows[i], lows[j]) <= min(highs[i], highs[j])
        for i in range(len(usable))
        for j in range(i + 1, len(usable))
    )

    summary = {
        "scope": "Alba 2001 pre-placement gymnasium differentiation using national examination score",
        "applicants": n,
        "directory_codes": directory_code_count,
        "nonempty_gymnasium_codes": group_count,
        "zero_applicant_gymnasium_codes": len(zero_applicant_source_codes),
        "zero_applicant_source_codes": zero_applicant_source_codes,
        "group_size": {
            "minimum": int(counts.min()),
            "p25": float(np.quantile(counts, 0.25)),
            "median": float(np.median(counts)),
            "p75": float(np.quantile(counts, 0.75)),
            "maximum": int(counts.max()),
            "threshold_accounting": thresholds,
        },
        "exam_score": {
            "mean": float(raw.mean()),
            "population_sd": float(raw.std(ddof=0)),
            "minimum": float(raw.min()),
            "p25": float(np.quantile(raw, 0.25)),
            "median": float(np.median(raw)),
            "p75": float(np.quantile(raw, 0.75)),
            "maximum": float(raw.max()),
        },
        "sorting": {
            "observed_H_sort": observed_h,
            "repository_crosscheck": repository_h,
            "random_assignment_size_benchmark": float((group_count - 1) / (n - 1)),
            "random_mean": float(null_h.mean()),
            "random_median": float(np.median(null_h)),
            "random_p025": float(np.quantile(null_h, 0.025)),
            "random_p975": float(np.quantile(null_h, 0.975)),
            "fraction_random_at_or_above_observed": float((1 + (null_h >= observed_h).sum()) / (RANDOMIZATIONS + 1)),
        },
        "intervals": {
            "observed_equal_gymnasium_mean_range_width": float(groups["A_range_width"].mean()),
            "random_equal_gymnasium_mean_range_width_mean": float(null_widths.mean(axis=1).mean()),
            "gymnasium_means_outside_own_size_matched_random_95_count": int(groups["mean_outside_random_95"].sum()),
            "gymnasium_means_outside_own_size_matched_random_95_fraction": float(groups["mean_outside_random_95"].mean()),
            "groups_n_at_least_5": int(len(usable)),
            "range_overlap_pairs_n_at_least_5": int(pair_overlap),
            "range_pair_total_n_at_least_5": int(pair_total),
            "range_overlap_fraction_n_at_least_5": float(pair_overlap / pair_total) if pair_total else None,
            "maximum_observed_coverage": int(observed_coverage.max()),
            "maximum_observed_coverage_fraction": float(observed_coverage.max() / group_count),
        },
        "randomization": {
            "draws": RANDOMIZATIONS,
            "seed": SEED,
            "method": "permute observed A_i across fixed source-code slots; preserve every group size",
        },
        "interpretive_limits": [
            "Population is participating applicants associated with source-coded gymnasiums, not every classmate or graduate.",
            "National examination performance is observed after gymnasium exposure, not before it.",
            "Random reassignments are a conditional group-size reference, not national-population uncertainty.",
            "This diagnostic does not estimate placement success, congestion, peer effects, or causality.",
        ],
    }
    return groups, coverage, draws, summary


def make_figures(frame: pd.DataFrame, groups: pd.DataFrame, coverage: pd.DataFrame, draws: pd.DataFrame, summary: dict) -> list[Path]:
    """Create one compact gate figure and one complete interval reference."""
    plt.rcParams.update({
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "figure.titlesize": 16,
    })
    outputs = []

    fig, axes = plt.subplots(2, 2, figsize=(15, 11.5))
    ax = axes[0, 0]
    ax.hist(frame["exam_score"], bins=np.arange(0, 10.05, 0.25), color="#4472C4", edgecolor="white")
    ax.axvline(frame["exam_score"].mean(), color="#B03A48", linewidth=2, label="Mean")
    ax.set_title("A. Overall national-examination performance")
    ax.set_xlabel("National examination score (raw 0–10 scale)")
    ax.set_ylabel("Participating applicants")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.2)

    ax = axes[0, 1]
    sizes = groups["applicant_n"].to_numpy()
    bins = np.arange(0.5, sizes.max() + 1.5, 2)
    ax.hist(sizes, bins=bins, color="#70AD47", edgecolor="white")
    ax.axvline(np.median(sizes), color="#B03A48", linewidth=2, label=f"Median = {np.median(sizes):.0f}")
    ax.set_title("B. Participating applicants per gymnasium code")
    ax.set_xlabel("Applicant count")
    ax.set_ylabel("Gymnasium codes")
    ax.legend(frameon=False)
    ax.grid(axis="y", alpha=0.2)

    ax = axes[1, 0]
    ax.fill_between(
        coverage["A_z"], coverage["random_p025"], coverage["random_p975"],
        color="#AFC6E9", alpha=0.6, label="Random 95% range",
    )
    ax.plot(coverage["A_z"], coverage["random_median"], color="#4472C4", linestyle="--", label="Random median")
    ax.plot(coverage["A_z"], coverage["observed_gymnasiums_covering"], color="#B03A48", linewidth=2.2, label="Observed gymnasiums")
    ax.set_title("C. How many gymnasium intervals cover each performance level?")
    ax.set_xlabel(r"Standardized national examination performance ($A_i$)")
    ax.set_ylabel("Gymnasium min–max intervals covering level")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.2)

    ax = axes[1, 1]
    ax.hist(draws["H_sort"], bins=35, color="#AFC6E9", edgecolor="white", label="Size-preserving random assignments")
    observed = summary["sorting"]["observed_H_sort"]
    benchmark = summary["sorting"]["random_assignment_size_benchmark"]
    ax.axvline(observed, color="#B03A48", linewidth=2.5, label=f"Observed = {observed:.3f}")
    ax.axvline(benchmark, color="black", linestyle=":", linewidth=1.8, label=f"Assignment-size benchmark = {benchmark:.3f}")
    ax.set_title("D. Sorting index relative to fixed-size random groups")
    ax.set_xlabel(r"Sorting index ($H_{sort}$)")
    ax.set_ylabel("Random assignments")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", alpha=0.2)

    fig.suptitle(
        "Alba 2001 — Are originating gymnasiums differentiated in examination performance?\n"
        "Participating applicants; pre-placement diagnostic only",
        fontweight="bold",
    )
    fig.text(
        0.5, 0.015,
        "Random reference preserves all 161 positive gymnasium sizes; seven recovered source codes have zero applicants. Examination scores occur after gymnasium exposure.",
        ha="center", fontsize=10,
    )
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    for suffix in ["png", "pdf"]:
        path = OUT / f"{STEM}_gate_summary.{suffix}"
        fig.savefig(path, dpi=220 if suffix == "png" else None)
        outputs.append(path)
    plt.close(fig)

    ordered = groups.sort_values(["A_mean", "source_code"]).reset_index(drop=True)
    y = np.arange(len(ordered))
    fig, ax = plt.subplots(figsize=(13, 28))
    for position, row in ordered.iterrows():
        color = "#4472C4" if row["applicant_n"] >= 5 else "#B7B7B7"
        ax.plot([row["A_min"], row["A_max"]], [position, position], color=color, linewidth=0.8, alpha=0.85)
        ax.plot([row["A_q25"], row["A_q75"]], [position, position], color=color, linewidth=3.0)
        ax.scatter(row["A_mean"], position, s=14, color="#B03A48", zorder=3)
    ax.axvline(0, color="black", linestyle=":", linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(
        [f"code {row.source_code}  (n={int(row.applicant_n)})" for row in ordered.itertuples()],
        fontsize=6.2,
    )
    ax.set_xlabel(r"Standardized national examination performance ($A_i$)")
    ax.set_ylabel("Origin-gymnasium source code, sorted by mean")
    ax.set_title(
        "Alba 2001 origin-gymnasium intervals\n"
        "thin line = full range; thick line = middle 50%; red point = mean",
        fontweight="bold",
    )
    ax.grid(axis="x", alpha=0.2)
    ax.set_ylim(-1, len(ordered))
    fig.tight_layout()
    for suffix in ["png", "pdf"]:
        path = OUT / f"{STEM}_all_gymnasium_intervals.{suffix}"
        fig.savefig(path, dpi=220 if suffix == "png" else None)
        outputs.append(path)
    plt.close(fig)
    return outputs


def write_run_record(input_paths: list[Path], output_paths: list[Path], started_utc: str, elapsed_seconds: float) -> None:
    RUN_RECORD.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "status": "completed",
        "started_utc": started_utc,
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": elapsed_seconds,
        "scope": "Alba 2001 pre-placement gymnasium differentiation gate",
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "parameters": {
            "ability_measure": "national examination score E_i",
            "group": "source-native originating-gymnasium code",
            "standardization": "global recovered-population mean and population SD",
            "randomizations": RANDOMIZATIONS,
            "seed": SEED,
            "random_reference": "permute observed scores across fixed group slots",
            "student_names_persisted": False,
        },
        "inputs": [
            {"path": str(path.relative_to(REPO)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in input_paths
        ],
        "code": {"path": str(CODE_PATH.relative_to(REPO)), "sha256": sha256(CODE_PATH)},
        "outputs": [
            {"path": str(path.relative_to(REPO)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in output_paths
        ],
    }
    RUN_RECORD.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")


def main(args) -> None:
    started_utc = datetime.now(timezone.utc).isoformat()
    started = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    print("=== ROMANIA 2001 GYMNASIUM DIFFERENTIATION GATE ===", flush=True)
    print("Stage 1/5 — validating the completed structural checkpoint.", flush=True)
    directory, expected = read_completed_checkpoint()
    print("  Confirmed: 168/168 school reports previously recovered; unresolved queue empty.", flush=True)

    print("Stage 2/5 — retrieving the 168 reports into memory; no student names will be saved.", flush=True)
    structural = load_structural_module()
    reports = retrieve_school_reports(
        structural,
        directory,
        expected,
        archive_use_acknowledged=args.archive_use_acknowledged,
        initial_interval_seconds=args.initial_interval,
        minimum_interval_seconds=args.minimum_interval,
        maximum_interval_seconds=args.maximum_interval,
        max_runtime_hours=args.max_hours,
    )

    print("\nStage 3/5 — checking score fields, formula, and gymnasium counts.", flush=True)
    frame, construction = build_name_free_frame(structural, reports)
    print(
        f"  Constructed in memory: {len(frame):,} applicant rows across "
        f"{frame['source_code'].nunique()} source codes.",
        flush=True,
    )
    print("  Admission formula disagreements: 0. Names remain unsaved.", flush=True)

    print("Stage 4/5 — calculating observed intervals and size-preserving random reference.", flush=True)
    groups, coverage, draws, summary = run_diagnostics(
        frame,
        directory_code_count=construction["directory_codes"],
        zero_applicant_source_codes=construction["zero_applicant_source_codes"],
    )
    summary["construction_checks"] = construction

    group_path = OUT / f"{STEM}_gymnasium_aggregate_statistics.csv"
    coverage_path = OUT / f"{STEM}_coverage_reference.csv"
    draws_path = OUT / f"{STEM}_H_sort_random_reference.csv"
    summary_path = OUT / f"{STEM}_summary.json"
    groups.to_csv(group_path, index=False)
    coverage.to_csv(coverage_path, index=False)
    draws.to_csv(draws_path, index=False)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")

    print("Stage 5/5 — creating figures and provenance record.", flush=True)
    figure_paths = make_figures(frame, groups, coverage, draws, summary)
    output_paths = [group_path, coverage_path, draws_path, summary_path, *figure_paths, OUT / "unresolved_addresses.json"]
    input_paths = [
        DECISION,
        STRUCTURAL_OUT / "origin_school_directory.json",
        STRUCTURAL_OUT / "origin_report_check_summary.json",
        STRUCTURAL_OUT / "origin_report_checks.jsonl",
        STRUCTURAL_OUT / "unresolved_addresses.json",
    ]
    elapsed = time.perf_counter() - started
    write_run_record(input_paths, output_paths, started_utc, elapsed)
    print("\nCOMPLETE", flush=True)
    print(f"  Applicants: {summary['applicants']:,}", flush=True)
    print(
        f"  Gymnasium codes: {summary['directory_codes']} directory; "
        f"{summary['nonempty_gymnasium_codes']} with applicants; "
        f"{summary['zero_applicant_gymnasium_codes']} with zero applicants",
        flush=True,
    )
    print(f"  Observed H_sort: {summary['sorting']['observed_H_sort']:.5f}", flush=True)
    print(
        f"  Random 95% range: {summary['sorting']['random_p025']:.5f}–"
        f"{summary['sorting']['random_p975']:.5f}",
        flush=True,
    )
    print(f"  Outputs: {OUT}", flush=True)
    print(f"  Elapsed: {elapsed/60:.1f} minutes", flush=True)


def cli() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--archive-use-acknowledged", action="store_true")
    parser.add_argument("--initial-interval", type=float, default=2.0)
    parser.add_argument("--minimum-interval", type=float, default=1.2)
    parser.add_argument("--maximum-interval", type=float, default=60.0)
    parser.add_argument("--max-hours", type=float, default=6.0)
    args = parser.parse_args()
    if not args.run:
        parser.print_help()
        return
    main(args)


if __name__ == "__main__":
    cli()
