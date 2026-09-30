"""Resumable Alba 2001 origin-school completeness audit.

This is a structural source audit, not a sorting or outcome analysis. It:
1. uses the source directory's 168 explicit school links;
2. connects each recovered school roster to the county candidate report;
3. retrieves a companion placement roster only when needed;
4. flushes one aggregate, name-free checkpoint after every school;
5. revisits unresolved addresses in later passes;
6. resumes without re-requesting successfully completed schools.

Student names are used in memory for exact within-school correspondence and are
never written to these audit outputs. A failed request remains "unresolved"; it
is never silently interpreted as an absent school or student.
"""
import argparse
import collections
import importlib.util
import json
import time
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "alba",
    Path(__file__).with_name("EDUCATION_20260929_alba_2001_structural_audit.py"),
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

OUT = m.OUT
LOG = OUT / "origin_report_checks.jsonl"
UNRESOLVED = OUT / "unresolved_addresses.json"
SUMMARY = OUT / "origin_report_check_summary.json"
LIVE_PROGRESS = OUT / "live_progress.json"


def archive_url(relative_path):
    """Create the exact Wayback request URL from a source-provided relative link."""
    return f"https://web.archive.org/web/{m.STAMP}id_/{m.SOURCE}{relative_path}"


def save(record):
    """Append and flush after every school so an interrupted run loses no progress."""
    with LOG.open("a") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
        file.flush()

    # Readable real-time feedback without printing student names.
    visible = {
        key: record[key]
        for key in [
            "pass_number",
            "source_code",
            "status",
            "candidate_rows",
            "county_label_rows",
            "candidate_extra_to_county",
            "county_missing_from_school",
            "placement_exact_matches",
        ]
        if key in record
    }
    print(json.dumps(visible, ensure_ascii=False), flush=True)
    return record


def write_live_progress(
    *,
    pass_number,
    passes_planned,
    attempted_this_pass,
    pending_at_pass_start,
    total_school_codes,
    pass_started,
):
    """Persist the same progress information shown in the notebook."""
    latest = latest_records()
    completed = sum(is_complete(record) for record in latest.values())
    elapsed = time.perf_counter() - pass_started
    remaining_this_pass = max(0, pending_at_pass_start - attempted_this_pass)
    seconds_per_school = elapsed / attempted_this_pass if attempted_this_pass else None
    eta = seconds_per_school * remaining_this_pass if seconds_per_school is not None else None
    snapshot = {
        "updated_utc": m.datetime.datetime.now(m.datetime.timezone.utc).isoformat(),
        "pass_number": pass_number,
        "passes_planned": passes_planned,
        "attempted_this_pass": attempted_this_pass,
        "pending_at_pass_start": pending_at_pass_start,
        "pass_percent": (
            100.0 * attempted_this_pass / pending_at_pass_start
            if pending_at_pass_start else 100.0
        ),
        "completed_school_codes": completed,
        "total_school_codes": total_school_codes,
        "currently_unresolved_or_unattempted": total_school_codes - completed,
        "elapsed_seconds_this_pass": elapsed,
        "estimated_seconds_remaining_this_pass": eta,
        "current_request_interval_seconds": m.CLIENT.interval,
    }
    LIVE_PROGRESS.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    return snapshot


def latest_records():
    """Return the most recent checkpoint for each source-native school code."""
    latest = {}
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            if line.strip():
                record = json.loads(line)
                latest[record["source_code"]] = record
    return latest


def is_complete(record):
    """Candidate roster plus any required companion placement check succeeded."""
    return (
        record.get("status") == "candidate_report_recovered"
        and not record.get("placement_report_unavailable", False)
    )


def write_summary(directory, *, stopped_reason=None, pass_number=None):
    """Write a current snapshot and an explicit unresolved-address queue."""
    latest = latest_records()
    results = list(latest.values())
    completed_codes = {code for code, record in latest.items() if is_complete(record)}
    unresolved = []

    for school in directory:
        if school["code"] in completed_codes:
            continue
        prior = latest.get(school["code"], {})
        candidate_relative = school["candidate_report"]
        placement_relative = candidate_relative.replace(
            "raport_candidati_per_scoala", "raport_total_per_scoala", 1
        )
        unresolved.append({
            "source_code": school["code"],
            "school_name": school["name"],
            "candidate_url": archive_url(candidate_relative),
            "placement_url_if_needed": archive_url(placement_relative),
            "last_status": prior.get("status", "not_yet_attempted"),
            "last_pass_number": prior.get("pass_number"),
            "placement_report_unavailable": prior.get("placement_report_unavailable", False),
        })

    summary = {
        "directory_codes": len(directory),
        "completed_codes": len(completed_codes),
        "unresolved_codes": len(unresolved),
        "directory_pass_finished": not unresolved,
        "last_pass_number": pass_number,
        "stopped_reason": stopped_reason,
        "candidate_rows_across_completed_reports_not_deduplicated": sum(
            record.get("candidate_rows", 0)
            for record in results
            if is_complete(record)
        ),
        "codes_with_added_names_vs_county_label": sum(
            is_complete(record) and record.get("candidate_extra_to_county", 0) > 0
            for record in results
        ),
        "added_name_occurrences_not_unique_students": sum(
            record.get("candidate_extra_to_county", 0)
            for record in results
            if is_complete(record)
        ),
        "codes_with_component_disagreements": sum(
            is_complete(record)
            and any(record.get("shared_component_disagreements", {}).values())
            for record in results
        ),
        "codes_with_county_names_missing_from_school": sum(
            is_complete(record) and record.get("county_missing_from_school", 0) > 0
            for record in results
        ),
        "cautions": [
            "Unresolved means retrieval incomplete, not source record absent.",
            "Counts across school reports are not assumed disjoint.",
            "A full graduating-cohort denominator remains unavailable.",
        ],
    }
    SUMMARY.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    UNRESOLVED.write_text(json.dumps(unresolved, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)
    return summary


def process_school(school, county_rows, same_name_code_counts, pass_number):
    """Retrieve and compare one source-coded gymnasium, retaining no personal rows."""
    reference = [
        row for row in county_rows
        if m.origin_parts(m.school_label(row)) == (school["name"], "AB")
    ]
    candidate_relative = school["candidate_report"]
    candidate_page = m.fetch(
        candidate_relative,
        "origin_candidates_" + school["code"],
    )

    if candidate_page is None:
        return save({
            "pass_number": pass_number,
            "source_code": school["code"],
            "status": "candidate_report_unresolved",
            "candidate_url": archive_url(candidate_relative),
            "county_label_rows": len(reference),
        })

    rows = candidate_page[1]
    county_by_name = collections.defaultdict(list)
    school_by_name = collections.defaultdict(list)
    for row in reference:
        county_by_name[row["Nume"]].append(row)
    for row in rows:
        school_by_name[row["Nume"]].append(row)

    shared = {
        name for name in county_by_name.keys() & school_by_name.keys()
        if len(county_by_name[name]) == len(school_by_name[name]) == 1
    }
    component_terms = ["admitere", "capacitate", "absolvire"]
    component_disagreements = {
        term: sum(
            m.col(county_by_name[name][0], term)
            != m.col(school_by_name[name][0], term)
            for name in shared
        )
        for term in component_terms
    }

    record = {
        "pass_number": pass_number,
        "source_code": school["code"],
        "school_name": school["name"],
        "status": "candidate_report_recovered",
        "candidate_rows": len(rows),
        "candidate_unique_names": len(school_by_name),
        "county_label_rows": len(reference),
        "directory_same_name_codes": same_name_code_counts[school["name"]],
        "exact_unique_names_shared": len(shared),
        "candidate_extra_to_county": len(school_by_name.keys() - county_by_name.keys()),
        "county_missing_from_school": len(county_by_name.keys() - school_by_name.keys()),
        "shared_component_disagreements": component_disagreements,
        "source_page": candidate_page[3],
        "applicant_county_column_counts": dict(
            collections.Counter(m.col(row, "Judeţ") for row in rows)
        ),
        "full_graduating_cohort_denominator": "unavailable",
    }

    companion_needed = (
        record["candidate_extra_to_county"] > 0
        or same_name_code_counts[school["name"]] > 1
        or school["code"] == "101"
    )
    if companion_needed:
        placement_relative = candidate_relative.replace(
            "raport_candidati_per_scoala", "raport_total_per_scoala", 1
        )
        placement_page = m.fetch(
            placement_relative,
            "origin_placement_" + school["code"],
        )
        if placement_page is None:
            record["placement_report_unavailable"] = True
            record["placement_url"] = archive_url(placement_relative)
        else:
            placement_by_name = collections.defaultdict(list)
            for row in placement_page[1]:
                placement_by_name[row["Nume"]].append(row)
            common = {
                name for name in school_by_name.keys() & placement_by_name.keys()
                if len(school_by_name[name]) == len(placement_by_name[name]) == 1
            }
            extras = (school_by_name.keys() - county_by_name.keys()) & common
            record.update({
                "placement_rows": len(placement_page[1]),
                "placement_exact_matches": len(common),
                "placement_unmatched_candidate_names": len(school_by_name.keys() - common),
                "placement_composite_disagreements": sum(
                    m.col(school_by_name[name][0], "admitere")
                    != m.col(placement_by_name[name][0], "admitere")
                    for name in common
                ),
                "extra_names_with_placement_rows": len(extras),
                "extra_placement_descriptions": dict(collections.Counter(
                    m.col(placement_by_name[name][0], "Liceu")
                    + " | "
                    + m.col(placement_by_name[name][0], "Specializare")
                    for name in extras
                )),
                "placement_page": placement_page[3],
            })

    return save(record)


def main(
    *,
    archive_use_acknowledged=False,
    initial_interval_seconds=2.0,
    minimum_interval_seconds=1.2,
    maximum_interval_seconds=60.0,
    max_runtime_hours=6.0,
    retry_passes=3,
    retry_pass_cooldown_seconds=180.0,
):
    """Run or resume the bounded audit, then revisit unresolved addresses."""
    if retry_passes < 1:
        raise ValueError("retry_passes must be at least 1")
    if retry_pass_cooldown_seconds < 0:
        raise ValueError("retry_pass_cooldown_seconds cannot be negative")

    OUT.mkdir(parents=True, exist_ok=True)
    directory = json.loads((OUT / "origin_school_directory.json").read_text())
    m.configure_retrieval(
        archive_use_acknowledged,
        initial_interval_seconds=initial_interval_seconds,
        minimum_interval_seconds=minimum_interval_seconds,
        maximum_interval_seconds=maximum_interval_seconds,
        max_runtime_hours=max_runtime_hours,
    )

    # These six pages are the in-memory reference used for exact comparisons.
    # They are refetched once per invocation because identifiable rows are not cached.
    county_rows = []
    for index in [1, 501, 1001, 1501, 2001, 2501]:
        page = m.fetch(
            f"raport_candidati_total.asp-cj=AB&nj=ALBA&idx={index}.htm",
            "school_check_county_reference",
        )
        if page is None:
            raise m.RetrievalStopped(
                "A county reference page is unresolved; school comparisons paused."
            )
        county_rows.extend(page[1])

    same_name_code_counts = collections.Counter(
        school["name"] for school in directory
    )

    initial_latest = latest_records()
    initial_completed = sum(is_complete(record) for record in initial_latest.values())
    print("\n=== Alba 2001 originating-gymnasium structural audit ===", flush=True)
    print(
        f"Resume state: {initial_completed}/{len(directory)} school codes complete; "
        f"{len(directory) - initial_completed} unresolved or not yet attempted.",
        flush=True,
    )
    print(
        f"Adaptive interval: {m.CLIENT.interval:.2f}s now; allowed range "
        f"{m.CLIENT.minimum_interval:.2f}–{m.CLIENT.maximum_interval:.2f}s.",
        flush=True,
    )

    try:
        from tqdm.auto import tqdm
    except ImportError:
        tqdm = None
        print("tqdm is unavailable; using one-line progress reports instead.", flush=True)

    for pass_number in range(1, retry_passes + 1):
        completed_codes = {
            code for code, record in latest_records().items()
            if is_complete(record)
        }
        pending = [
            school for school in directory
            if school["code"] not in completed_codes
        ]
        if not pending:
            write_summary(directory, pass_number=pass_number)
            print("All source-directory school codes are complete.", flush=True)
            return

        if pass_number > 1:
            m.CLIENT.wait_between_passes(
                retry_pass_cooldown_seconds,
                pass_number,
            )

        print(
            f"Starting pass {pass_number}/{retry_passes}: "
            f"{len(pending)} unresolved school codes.",
            flush=True,
        )
        pass_started = time.perf_counter()
        progress_bar = None
        if tqdm is not None:
            progress_bar = tqdm(
                total=len(pending),
                desc=f"Alba archive pass {pass_number}/{retry_passes}",
                unit="school",
                dynamic_ncols=True,
                mininterval=0.5,
            )
        try:
            for position, school in enumerate(pending, 1):
                print(
                    f"Pass {pass_number}: school {position}/{len(pending)}, "
                    f"source code {school['code']}; current interval "
                    f"{m.CLIENT.interval:.2f} seconds.",
                    flush=True,
                )
                process_school(
                    school,
                    county_rows,
                    same_name_code_counts,
                    pass_number,
                )

                snapshot = write_live_progress(
                    pass_number=pass_number,
                    passes_planned=retry_passes,
                    attempted_this_pass=position,
                    pending_at_pass_start=len(pending),
                    total_school_codes=len(directory),
                    pass_started=pass_started,
                )
                if progress_bar is not None:
                    progress_bar.update(1)
                    progress_bar.set_postfix(
                        complete=f"{snapshot['completed_school_codes']}/{len(directory)}",
                        unresolved=snapshot["currently_unresolved_or_unattempted"],
                        interval=f"{snapshot['current_request_interval_seconds']:.1f}s",
                        refresh=True,
                    )
                else:
                    eta = snapshot["estimated_seconds_remaining_this_pass"]
                    eta_text = (
                        f"{eta / 60:.1f} min" if eta is not None else "calculating"
                    )
                    print(
                        f"  Progress {position}/{len(pending)} "
                        f"({snapshot['pass_percent']:.1f}%); cumulative complete "
                        f"{snapshot['completed_school_codes']}/{len(directory)}; "
                        f"ETA this pass {eta_text}; interval "
                        f"{snapshot['current_request_interval_seconds']:.1f}s.",
                        flush=True,
                    )
        finally:
            # A clean close matters in notebooks: an archive stop or a manual
            # interrupt should return the cell promptly instead of leaving a
            # visually active progress bar behind.
            if progress_bar is not None:
                progress_bar.close()
        pass_elapsed = time.perf_counter() - pass_started
        print(
            f"Pass {pass_number} finished in {pass_elapsed / 60:.1f} minutes.",
            flush=True,
        )

        summary = write_summary(directory, pass_number=pass_number)
        if summary["directory_pass_finished"]:
            return

    print(
        f"Completed {retry_passes} passes. "
        f"See {UNRESOLVED} for addresses still unresolved.",
        flush=True,
    )


def cli():
    parser = argparse.ArgumentParser(
        description="Run or resume the Alba 2001 structural archive audit."
    )
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--archive-use-acknowledged", action="store_true")
    parser.add_argument("--initial-interval", type=float, default=2.0)
    parser.add_argument("--minimum-interval", type=float, default=1.2)
    parser.add_argument("--maximum-interval", type=float, default=60.0)
    parser.add_argument("--max-hours", type=float, default=6.0)
    parser.add_argument("--retry-passes", type=int, default=3)
    parser.add_argument("--retry-cooldown", type=float, default=180.0)
    args = parser.parse_args()

    if not args.run:
        parser.print_help()
        return
    try:
        main(
            archive_use_acknowledged=args.archive_use_acknowledged,
            initial_interval_seconds=args.initial_interval,
            minimum_interval_seconds=args.minimum_interval,
            maximum_interval_seconds=args.maximum_interval,
            max_runtime_hours=args.max_hours,
            retry_passes=args.retry_passes,
            retry_pass_cooldown_seconds=args.retry_cooldown,
        )
    except (m.RetrievalStopped, KeyboardInterrupt) as error:
        reason = str(error) or "Interrupted by user"
        m.emit({"kind": "stopped", "reason": reason})
        directory = json.loads((OUT / "origin_school_directory.json").read_text())
        write_summary(directory, stopped_reason=reason)
        raise SystemExit(2)


if __name__ == "__main__":
    cli()
