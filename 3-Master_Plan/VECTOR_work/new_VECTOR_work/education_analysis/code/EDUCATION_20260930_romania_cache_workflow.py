"""Two-stage Alba 2001 workflow: resumable local acquisition, then offline analysis.

Complete source rows, including names, are confined to the user-designated
Desktop cache. Importing this module makes no network requests. The analysis
stage writes only name-free research outputs into the VECTOR workspace.
"""

from __future__ import annotations

import hashlib
import base64
import json
import os
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from EDUCATION_20260929_romania_gymnasium_differentiation_v1 import (
    BASE, CODE_PATH, DECISION, OUT, RANDOMIZATIONS, REPO, RUN_RECORD, SEED,
    STEM, STRUCTURAL_OUT, build_name_free_frame, load_structural_module,
    make_figures, read_completed_checkpoint, run_diagnostics, sha256,
)

CACHE = Path.home() / "Desktop" / "VECTOR_temp" / "romania_alba_2001_differentiation_v1"
CACHE_FILES = CACHE / "school_reports"
SCHEMA_VERSION = 1
MAX_CONSECUTIVE_NETWORK_FAILURES = 4


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def atomic_json(path: Path, value: object) -> None:
    """Finish each school file before naming it as a complete checkpoint."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".part-{os.getpid()}")
    try:
        with temporary.open("x", encoding="utf-8") as stream:
            os.chmod(temporary, 0o600)
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def prepare_cache() -> None:
    """Keep directly identifying source tables in the chosen Desktop folder."""
    CACHE.mkdir(parents=True, exist_ok=True)
    CACHE_FILES.mkdir(parents=True, exist_ok=True)
    os.chmod(CACHE, 0o700)
    os.chmod(CACHE_FILES, 0o700)


def report_path(code: str) -> Path:
    if not code.isdigit():
        raise ValueError(f"Non-numeric source code: {code!r}")
    return CACHE_FILES / f"school_{int(code):03d}.json"


def verified_cache_record(school: dict, checkpoint: dict) -> dict | None:
    """Return one trustworthy checkpoint, or None if it has not been saved."""
    path = report_path(school["code"])
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    required = {"schema_version", "source_code", "candidate_report", "row_count", "rows", "rows_sha256", "source_page", "raw_html_base64", "raw_html_sha256"}
    if not isinstance(payload, dict) or not required.issubset(payload):
        raise ValueError(f"Incomplete cache file: {path}")
    if payload["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"Cache schema mismatch: {path}")
    if payload["source_code"] != school["code"] or payload["candidate_report"] != school["candidate_report"]:
        raise ValueError(f"Source identity mismatch: {path}")
    rows = payload["rows"]
    expected_rows = int(checkpoint["candidate_rows"])
    if not isinstance(rows, list) or payload["row_count"] != len(rows) or len(rows) != expected_rows:
        raise ValueError(f"Cached row count differs from completed structural audit: {path}")
    if hashlib.sha256(canonical_bytes(rows)).hexdigest() != payload["rows_sha256"]:
        raise ValueError(f"Cached row digest mismatch: {path}")
    raw = base64.b64decode(payload["raw_html_base64"], validate=True)
    if hashlib.sha256(raw).hexdigest() != payload["raw_html_sha256"]:
        raise ValueError(f"Cached raw page digest mismatch: {path}")
    return payload


def cache_status() -> dict:
    """Read-only overview. It does not fetch pages or display student records."""
    directory, checkpoints = read_completed_checkpoint()
    complete, missing = [], []
    for school in directory:
        record = verified_cache_record(school, checkpoints[school["code"]])
        (complete if record is not None else missing).append(school["code"])
    return {
        "directory_codes": len(directory),
        "cached_and_verified_codes": len(complete),
        "remaining_codes": len(missing),
        "remaining_source_codes": missing,
        "cache_folder": str(CACHE),
    }


def _event_writer(event: dict) -> None:
    """Preserve technical retrieval details locally while printing plain updates."""
    record = {"utc": now_utc(), **event}
    with (CACHE / "retrieval_events.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        stream.flush()
    kind = event.get("kind")
    if kind == "adaptive_pace" and event.get("direction") == "slower":
        print(f"  Archive slowed after a failed request: {event['new_seconds']:.1f} seconds between requests.", flush=True)
    elif kind == "retrieval_wait" and event.get("seconds", 0) >= 10:
        print(f"  Archive wait: {event['seconds']:.1f} seconds ({event.get('reason', 'backoff')}).", flush=True)
    elif kind == "http_attempt" and event.get("status") not in (200, 302):
        print(f"  Request unresolved: HTTP {event.get('status')}, {event.get('error') or 'no further detail'}. Retrying later.", flush=True)


def acquire(
    *,
    live: bool = False,
    initial_interval_seconds: float = 2.0,
    minimum_interval_seconds: float = 1.2,
    maximum_interval_seconds: float = 60.0,
    max_runtime_hours: float = 6.0,
    retry_passes: int = 3,
    retry_cooldown_seconds: float = 180.0,
) -> dict:
    """Acquire all 168 reports, checkpointing every success outside Dropbox.

    ``live=False`` makes this a safe status check. With ``live=True``, every
    network request is sequential and paced by the existing ArchiveClient.
    A repeated network outage ends the run so it does not churn overnight.
    """
    if not live:
        print("Preview only: no network requests.", flush=True)
        return cache_status()
    if retry_passes < 1 or retry_cooldown_seconds < 0:
        raise ValueError("Retry passes must be positive and cooldown nonnegative")
    prepare_cache()
    directory, checkpoints = read_completed_checkpoint()
    structural = load_structural_module()
    structural.OUT = CACHE
    structural.emit = _event_writer
    structural.configure_retrieval(
        True,
        initial_interval_seconds=initial_interval_seconds,
        minimum_interval_seconds=minimum_interval_seconds,
        maximum_interval_seconds=maximum_interval_seconds,
        max_runtime_hours=max_runtime_hours,
    )
    print("Stage 1/2: checking local school checkpoints.", flush=True)
    initial = cache_status()
    print(f"  {initial['cached_and_verified_codes']}/{len(directory)} already saved; {initial['remaining_codes']} to fetch.", flush=True)
    started = time.monotonic()
    failures_in_a_row = 0
    for pass_number in range(1, retry_passes + 1):
        pending = [s for s in directory if not report_path(s["code"]).exists()]
        if not pending:
            break
        if pass_number > 1:
            structural.CLIENT.wait_between_passes(retry_cooldown_seconds, pass_number)
        print(f"Stage 2/2: pass {pass_number}/{retry_passes}, {len(pending)} reports to attempt.", flush=True)
        pass_started = time.monotonic()
        try:
            from tqdm.auto import tqdm
        except ImportError:
            tqdm = None
        bar = tqdm(total=len(pending), desc=f"Alba acquisition pass {pass_number}", unit="school", dynamic_ncols=True) if tqdm else None
        try:
            for position, school in enumerate(pending, 1):
                code = school["code"]
                page = structural.fetch(
                    school["candidate_report"],
                    f"acquisition_origin_{code}",
                    include_raw=True,
                )
                if page is None:
                    failures_in_a_row += 1
                    label = "unresolved; queued for later"
                else:
                    rows = page[1]
                    expected_rows = int(checkpoints[code]["candidate_rows"])
                    if len(rows) != expected_rows:
                        raise ValueError(f"School {code}: {len(rows)} rows now versus {expected_rows} in the structural audit")
                    raw_html = page[4]
                    payload = {
                        "schema_version": SCHEMA_VERSION,
                        "source_code": code,
                        "candidate_report": school["candidate_report"],
                        "saved_utc": now_utc(),
                        "row_count": len(rows),
                        "rows_sha256": hashlib.sha256(canonical_bytes(rows)).hexdigest(),
                        "source_page": page[3],
                        "raw_html_sha256": hashlib.sha256(raw_html).hexdigest(),
                        "raw_html_base64": base64.b64encode(raw_html).decode("ascii"),
                        "rows": rows,
                    }
                    atomic_json(report_path(code), payload)
                    verified_cache_record(school, checkpoints[code])
                    failures_in_a_row = 0
                    label = f"saved {len(rows)} rows"
                elapsed = time.monotonic() - pass_started
                eta = elapsed / position * (len(pending) - position)
                # Count *all* completed school files, including successful
                # schools from an earlier pass of this same invocation.
                complete = sum(report_path(s["code"]).exists() for s in directory)
                if bar:
                    bar.update(1)
                    bar.set_postfix(saved=f"{complete}/{len(directory)}", interval=f"{structural.CLIENT.interval:.1f}s", refresh=True)
                if position % 10 == 0 or page is None or position == len(pending):
                    print(f"  {position}/{len(pending)} this pass; code {code}: {label}; total saved {complete}/{len(directory)}; estimated pass time left {eta/60:.1f} min.", flush=True)
                if failures_in_a_row >= MAX_CONSECUTIVE_NETWORK_FAILURES:
                    print("  Four consecutive requests failed. Stopping for a later resume.", flush=True)
                    return cache_status()
        finally:
            if bar:
                bar.close()
    result = cache_status()
    if result["remaining_codes"] == 0:
        manifest = {
            "completed_utc": now_utc(),
            "directory_codes": result["directory_codes"],
            "complete_codes": result["cached_and_verified_codes"],
            "school_files": [
                {"source_code": school["code"], "file": report_path(school["code"]).name,
                 "sha256": sha256(report_path(school["code"]))}
                for school in directory
            ],
        }
        atomic_json(CACHE / "completed_manifest.json", manifest)
        print(f"All {result['directory_codes']} school reports are saved and verified. Acquisition complete.", flush=True)
    else:
        print(f"Acquisition paused with {result['remaining_codes']} reports remaining. Re-run to resume.", flush=True)
    print(f"Elapsed this invocation: {(time.monotonic()-started)/60:.1f} minutes.", flush=True)
    return result


def _read_all_cached_reports() -> tuple[dict[str, list[dict]], dict]:
    """Read every local school file, verifying its identity and completeness."""
    directory, checkpoints = read_completed_checkpoint()
    status = cache_status()
    if status["remaining_codes"]:
        raise RuntimeError(f"Acquisition incomplete: {status['remaining_codes']} school reports remain")
    manifest_path = CACHE / "completed_manifest.json"
    if not manifest_path.exists():
        raise RuntimeError("Completed cache manifest is missing; finish acquisition first")
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("complete_codes") != len(directory):
        raise ValueError("Completed cache manifest does not cover the directory")
    expected_hashes = {item["source_code"]: item["sha256"] for item in manifest["school_files"]}
    if set(expected_hashes) != {school["code"] for school in directory}:
        raise ValueError("Manifest source codes differ from the structural directory")
    reports = {}
    for school in directory:
        code = school["code"]
        path = report_path(code)
        if sha256(path) != expected_hashes[code]:
            raise ValueError(f"Cache file changed after acquisition: code {code}")
        reports[code] = verified_cache_record(school, checkpoints[code])["rows"]
    return reports, manifest


def count_cross_code_exact_duplicates(structural, reports: dict[str, list[dict]]) -> int:
    """Flag apparent repeated people without storing names or making a fuzzy join.

    A printed name plus all three identical scores in two source-code reports
    is a conservative warning that the same applicant may have been counted
    twice. We stop rather than silently assign that record to one gymnasium.
    """
    signatures: dict[tuple, set[str]] = {}
    for code, rows in reports.items():
        for row in rows:
            signature = (
                row.get("Nume", ""),
                structural.col(row, "capacitate"),
                structural.col(row, "absolvire"),
                structural.col(row, "admitere"),
            )
            signatures.setdefault(signature, set()).add(code)
    return sum(len(codes) - 1 for codes in signatures.values() if len(codes) > 1)


def analyze(*, run: bool = False) -> dict:
    """Offline differentiation analysis. No archive client is created here."""
    status = cache_status()
    if not run:
        print("Preview only: no analysis or network requests.", flush=True)
        return status
    if status["remaining_codes"]:
        raise RuntimeError(f"Need {status['remaining_codes']} more reports before analysis")
    print("Stage 1/4: verifying the complete Desktop cache.", flush=True)
    reports, manifest = _read_all_cached_reports()
    structural = load_structural_module()
    cross_code_duplicates = count_cross_code_exact_duplicates(structural, reports)
    if cross_code_duplicates:
        raise ValueError(
            f"Found {cross_code_duplicates} exact name-and-score signatures in multiple "
            "source codes. Source-code membership needs reconciliation before analysis."
        )
    print("Stage 2/4: extracting scores and checking the admission formula.", flush=True)
    frame, construction = build_name_free_frame(structural, reports)
    construction["cross_code_exact_name_and_score_duplicates"] = cross_code_duplicates
    del reports
    # The row number is a generated analytic identifier within a source code;
    # it is not derived from a student's name or historical personal ID.
    frame.insert(1, "analytic_row", frame.groupby("source_code", sort=False).cumcount() + 1)
    print(f"  {len(frame):,} applicant rows; {construction['nonempty_gymnasium_codes']} nonempty codes; {len(construction['zero_applicant_source_codes'])} empty codes; zero formula disagreements.", flush=True)
    print("Stage 3/4: gymnasium intervals and 1,000 size-preserving random assignments.", flush=True)
    groups, coverage, draws, summary = run_diagnostics(
        frame,
        directory_code_count=construction["directory_codes"],
        zero_applicant_source_codes=construction["zero_applicant_source_codes"],
    )
    summary["construction_checks"] = construction
    OUT.mkdir(parents=True, exist_ok=True)
    name_free = OUT / f"{STEM}_name_free_applicant_scores.csv.gz"
    group_path = OUT / f"{STEM}_gymnasium_aggregate_statistics.csv"
    coverage_path = OUT / f"{STEM}_coverage_reference.csv"
    draws_path = OUT / f"{STEM}_H_sort_random_reference.csv"
    summary_path = OUT / f"{STEM}_summary.json"
    frame.to_csv(name_free, index=False, compression="gzip")
    groups.to_csv(group_path, index=False)
    coverage.to_csv(coverage_path, index=False)
    draws.to_csv(draws_path, index=False)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print("Stage 4/4: drawing figures and recording provenance.", flush=True)
    figures = make_figures(frame, groups, coverage, draws, summary)
    outputs = [name_free, group_path, coverage_path, draws_path, summary_path, *figures]
    provenance = {
        "completed_utc": now_utc(),
        "status": "complete",
        "scope": "Alba 2001 pre-placement gymnasium differentiation",
        "analysis_code": str(CODE_PATH.relative_to(REPO)),
        "analysis_code_sha256": sha256(CODE_PATH),
        "workflow_code": str(Path(__file__).resolve().relative_to(REPO)),
        "workflow_code_sha256": sha256(Path(__file__).resolve()),
        "decision_sha256": sha256(DECISION),
        "temporary_cache_manifest_sha256": sha256(CACHE / "completed_manifest.json"),
        "temporary_cache_school_hashes": manifest["school_files"],
        "randomizations": RANDOMIZATIONS,
        "seed": SEED,
        "permanent_outputs": [
            {"path": str(path.relative_to(REPO)), "sha256": sha256(path), "bytes": path.stat().st_size}
            for path in outputs
        ],
        "student_names_persisted_in_research_workspace": False,
    }
    RUN_RECORD.parent.mkdir(parents=True, exist_ok=True)
    RUN_RECORD.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n")
    print(f"Completed: {summary['applicants']:,} applicants, {summary['nonempty_gymnasium_codes']} nonempty gymnasiums.", flush=True)
    print(f"Observed sorting index: {summary['sorting']['observed_H_sort']:.5f}; random 95% range: {summary['sorting']['random_p025']:.5f}–{summary['sorting']['random_p975']:.5f}.", flush=True)
    print(f"Figures and name-free data: {OUT}", flush=True)
    return summary
