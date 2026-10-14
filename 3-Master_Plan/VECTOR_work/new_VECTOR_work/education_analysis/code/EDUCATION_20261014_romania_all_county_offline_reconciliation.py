"""All-county offline reconciliation for Romania 2001 Ministry checkpoints.

Reads saved pages only. It does not contact the archive, rank programs, or
draw outcome curves. Printed name plus admission score is a provisional
comparison because the archived personal identifier is masked.

Repository files receive county counts and plain-language findings. Rows that
still carry printed names stay in a private ledger under ~/Desktop/VECTOR_temp
so a later cross-county check can resume without copying names into the
repository.

One county's bad checkpoint is recorded and the next county continues.
"""

from __future__ import annotations

import hashlib
import json
import os
from collections import Counter
from datetime import datetime
from pathlib import Path

import pandas as pd

import EDUCATION_20261006_romania_school_results_incoming_acquisition as views
from EDUCATION_20260930_romania_2001_national_acquisition import CACHE
from EDUCATION_20261001_romania_four_county_school_report_check import PAGES as APPLICANT_PAGES
from EDUCATION_20261001_romania_four_county_school_sample import school_directory
from EDUCATION_20261001_romania_offline_county_source_readiness import (
    counters,
    family_status,
    number as source_number,
    placement_status,
    saved_rows,
    verified_program_rows,
)
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    ALBA_PAGES,
    all_gymnasium_rows,
    components,
    name_score,
)
from EDUCATION_20261003_romania_four_county_program_identity_gate import source_programs
from EDUCATION_20261007_romania_seven_county_new_views_offline_audit import (
    count,
    county_suffix,
    marked_unassigned,
    multiset,
    school_code,
)

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "outputs/romania_2001_all_county_offline_reconciliation"
LEDGER_ROOT = Path.home() / "Desktop/VECTOR_temp/romania_2001_all_county_reconciliation_ledgers"
NEW_FAMILIES = (
    "school_results",
    "resident_candidates",
    "incoming_candidates",
    "incoming_admitted",
    "incoming_rejected",
)
BASE_FAMILIES = (
    "origin_school_directory",
    "candidate_roster",
    "admitted_placements",
    "unassigned_applicants",
    "program_directory",
    "program_occupancy",
)
FAMILY_LABELS = {
    "school_results": "School Result View",
    "resident_candidates": "resident applicant list",
    "incoming_candidates": "incoming applicant list",
    "incoming_admitted": "incoming admitted list",
    "incoming_rejected": "incoming unassigned list",
    "origin_school_directory": "origin school directory",
    "candidate_roster": "general county applicant list",
    "admitted_placements": "county admitted list",
    "unassigned_applicants": "county unassigned list",
    "program_directory": "program directory",
    "program_occupancy": "program occupancy table",
}
SUMMARY_FIELDS = (
    "county",
    "county_name",
    "checked_at",
    "origin_directory_schools",
    "school_applicant_pages_saved",
    "school_applicant_pages_expected",
    "school_result_pages_verified",
    "school_result_directory_pages",
    "school_result_pages_expected",
    "school_result_unresolved_urls",
    "school_result_malformed_pages",
    "school_result_rows",
    "school_result_pages_complete",
    "resident_pages_saved",
    "resident_pages_projected",
    "resident_list_complete",
    "resident_rows_saved",
    "resident_rows_with_result_match",
    "resident_rows_without_result_match",
    "result_rows_without_saved_resident_match",
    "incoming_candidate_rows",
    "incoming_admitted_rows",
    "incoming_rejected_rows",
    "incoming_candidate_rows_without_outcome",
    "incoming_outcome_rows_without_candidate",
    "outgoing_rows_with_other_county_suffix",
    "occupancy_admitted_total",
    "original_placement_rows",
    "original_placement_shortfall",
    "remaining_placement_shortfall",
    "program_identity",
    "applicant_result_matches",
    "applicant_rows_without_result",
    "result_rows_without_applicant",
    "applicant_component_disagreements",
    "next_source_question",
    "plain_summary",
)


def say(message):
    print(f"{datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} | {message}", flush=True)


def county_directory():
    payload = json.loads((CACHE / "county_directory.json").read_text(encoding="utf-8"))
    return [(row["county_code"], row["county_name"]) for row in payload["counties"]]


def _stat_token(path):
    if not path.exists():
        return f"{path}|MISSING"
    stat = path.stat()
    return f"{path}|{stat.st_size}|{stat.st_mtime_ns}"


def _placement_line(county):
    path = ROOT / "outputs/romania_2001_national_source_recovery/placement_county_status.csv"
    if not path.exists():
        return "placement-status-missing"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(county + ","):
            return line
    return "placement-status-no-row"


def fingerprint_county(county, status):
    """Size and modification time of this county's checkpoints, plus status text.

    A replaced file that keeps both size and modification time will not force
    another pass. The pass itself still checks saved hashes when it runs.
    """
    parts = [_placement_line(county)]
    state = status.get("counties", {}).get(county, {})
    parts.append(json.dumps(state, sort_keys=True, ensure_ascii=False))
    parts.append(_stat_token(CACHE / "county_manifests" / f"{county}.json"))
    for family in NEW_FAMILIES:
        folder = views.PAGES / county / family
        if not folder.exists():
            parts.append(f"{family}|NO FOLDER")
            continue
        for path in sorted(folder.glob("*.json")):
            parts.append(_stat_token(path))
    for folder in (
        CACHE / "alternate_report_pilot" / county,
        CACHE / "supplemental_program_reports" / county,
    ):
        if not folder.exists():
            parts.append(f"{folder.name}|NO FOLDER")
            continue
        for path in sorted(folder.iterdir()):
            if path.is_file():
                parts.append(_stat_token(path))
    if county == "AB":
        applicant_files = sorted(ALBA_PAGES.glob("school_*.json")) if ALBA_PAGES.exists() else []
    else:
        applicant_files = sorted(APPLICANT_PAGES.glob(f"{county}_*.json")) if APPLICANT_PAGES.exists() else []
    parts.append(f"applicant-files|{len(applicant_files)}")
    for path in applicant_files:
        parts.append(_stat_token(path))
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def _atomic_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def open_run(output_root, resume):
    output_root = Path(output_root or DEFAULT_OUTPUT)
    output_root.mkdir(parents=True, exist_ok=True)
    if resume:
        runs = sorted(path for path in output_root.glob("run_*") if path.is_dir())
        if runs:
            say(f"Resuming saved run folder: {runs[-1].name}")
            return runs[-1]
    stamp = datetime.now().astimezone().strftime("%Y%m%dT%H%M%S%z")
    folder = output_root / f"run_{stamp}"
    folder.mkdir()
    say(f"Started a new run folder: {folder.name}")
    return folder


def latest_run(output_root=None):
    output_root = Path(output_root or DEFAULT_OUTPUT)
    runs = sorted(path for path in output_root.glob("run_*") if path.is_dir())
    if not runs:
        raise FileNotFoundError(f"No reconciliation run folder in {output_root}")
    return runs[-1]


def _blank(record):
    for field in SUMMARY_FIELDS:
        record.setdefault(field, "")
    return record


def _verified_family(county, family, state):
    pages = []
    problems = []
    discovered = list(state.get("discovered") or [])
    for relative in discovered:
        try:
            page = views.checked_page(county, family, relative)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            problems.append(f"{relative}: {exc}")
            continue
        if page is None:
            problems.append(f"{relative}: discovered URL address has no saved file")
            continue
        pages.append((relative, page))
    unresolved = dict(state.get("unresolved") or {})
    folder = views.PAGES / county / family
    on_disk = list(folder.glob("*.json")) if folder.exists() else []
    expected_names = {views.page_path(county, family, relative).name for relative in discovered}
    extra = [path.name for path in on_disk if path.name not in expected_names]
    projected = state.get("projected_pages")
    target = max(len(discovered), int(projected)) if projected is not None else len(discovered)
    saved_pages = state.get("saved_pages")
    complete = (
        not problems
        and not unresolved
        and not extra
        and bool(pages)
        and len(pages) == target
        and saved_pages == len(pages)
    )
    return {
        "pages": pages,
        "problems": problems,
        "unresolved": unresolved,
        "extra_files": extra,
        "projected_pages": projected,
        "target_pages": target,
        "complete": complete,
        "saved_rows_status": state.get("saved_rows"),
        "projection_basis": state.get("projection_basis", ""),
    }


def _family_rows(loaded):
    return [row for _relative, page in loaded["pages"] for row in page["rows"]]


def _school_result_pages(loaded):
    directory = []
    schools = []
    for relative, page in loaded["pages"]:
        if relative.lower().startswith("raport_scoli_din_judet_tot"):
            directory.append((relative, page))
        else:
            schools.append((relative, page))
    return directory, schools


def _multiset_report(left_name, right_name, left, right):
    return {
        "matches": count(left & right),
        "left_only": count(left - right),
        "right_only": count(right - left),
        "left_name": left_name,
        "right_name": right_name,
    }


def _applicant_paths(county, directory):
    missing = []
    present = 0
    for code in directory:
        if county == "AB":
            path = ALBA_PAGES / f"school_{int(code):03d}.json"
        else:
            path = APPLICANT_PAGES / f"{county}_{code}.json"
        if path.exists():
            present += 1
        else:
            missing.append(code)
    return present, missing


def _compare_applicants(county, manifest, school_pages):
    """Same-school comparison. Skipped when School Applicant View pages are missing."""
    result = {
        "expected_pages": "",
        "saved_pages": "",
        "matches": "",
        "applicant_without_result": "",
        "result_without_applicant": "",
        "repeated_applicant_keys": "",
        "rows_without_name_or_score": "",
        "component_disagreements": "",
        "note": "",
    }
    try:
        complete, unresolved = family_status(manifest, "origin_school_directory")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        result["note"] = f"Origin school directory could not be read: {exc}"
        return result
    if not complete or unresolved:
        result["note"] = (
            "The origin school directory is incomplete, so School Applicant View "
            "pages cannot be checked against a full school list."
        )
        return result
    try:
        directory = school_directory(county)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        result["note"] = f"Origin school directory could not be read: {exc}"
        return result
    result["expected_pages"] = len(directory)
    try:
        present, missing = _applicant_paths(county, directory)
    except (OSError, ValueError) as exc:
        result["note"] = f"School Applicant View filenames could not be checked: {exc}"
        return result
    result["saved_pages"] = present
    if missing:
        result["note"] = (
            f"School Applicant View pages saved: {present} of {len(directory)}. "
            f"{len(missing)} listed schools have no saved page. "
            "Person comparison with the School Result View waits until those pages exist. "
            "Missing pages stay unresolved. They are not treated as empty schools."
        )
        return result
    gymnasiums, _counts = all_gymnasium_rows([county])
    by_school = {}
    repeated = 0
    no_key = 0
    for code, key, _comp in gymnasiums[county]:
        bucket = by_school.setdefault(code, Counter())
        if key is None:
            no_key += 1
        else:
            bucket[key] += 1
    repeated = sum(1 for counter in by_school.values() for n in counter.values() if n > 1)
    result_by_school = {}
    result_codes = []
    for relative, page in school_pages:
        code = school_code(relative)
        result_codes.append(code)
        result_by_school.setdefault(code, Counter()).update(multiset(page["rows"]))
    matches = applicant_only = result_only = 0
    for code in set(by_school) | set(result_by_school):
        left = by_school.get(code, Counter())
        right = result_by_school.get(code, Counter())
        matches += count(left & right)
        applicant_only += count(left - right)
        result_only += count(right - left)
    result.update(
        matches=matches,
        applicant_without_result=applicant_only,
        result_without_applicant=result_only,
        repeated_applicant_keys=repeated,
        rows_without_name_or_score=no_key,
    )
    notes = []
    if None in result_codes or len(result_codes) != len(set(result_codes)):
        notes.append(
            "Some School Result View pages lack a school code or repeat one, "
            "so the same-school comparison is incomplete."
        )
    component_note, disagreements = _component_disagreements(county, manifest, gymnasiums[county])
    result["component_disagreements"] = disagreements
    if component_note:
        notes.append(component_note)
    result["note"] = " ".join(notes)
    return result


def _component_disagreements(county, manifest, applicant_rows):
    """Compare exam and school-grade components on unique name-and-score keys."""
    complete, gaps = family_status(manifest, "candidate_roster")
    saved = saved_rows(manifest, "candidate_roster")
    roster = Counter()
    roster_components = {}
    for row in saved:
        key = name_score(row)
        if key is None:
            continue
        roster[key] += 1
        roster_components.setdefault(key, components(row))
    disagreements = 0
    comparable = 0
    for _code, key, comp in applicant_rows:
        if key is None or roster[key] != 1:
            continue
        other = roster_components.get(key)
        if comp is None or other is None:
            continue
        comparable += 1
        if comp != other:
            disagreements += 1
    scope = (
        "The general county applicant list is complete."
        if complete and not gaps
        else "The general county applicant list is incomplete, so this comparison uses only its saved pages."
    )
    note = (
        f"{scope} Among {comparable} School Applicant View rows with a unique "
        "name-and-score key and both exam and school-grade components on both views, "
        f"{disagreements} disagree."
    )
    return note, disagreements


def _program_block(county, manifest, progress):
    result = {
        "occupancy_admitted_total": "",
        "original_placement_rows": "",
        "original_placement_shortfall": "",
        "remaining_placement_shortfall": "",
        "program_identity": "",
        "note": "",
    }
    notes = []
    occupancy_complete, occupancy_gaps = family_status(manifest, "program_occupancy")
    directory_complete, directory_gaps = family_status(manifest, "program_directory")
    placement_complete, placement_gaps = family_status(manifest, "admitted_placements")
    occupancy_rows = saved_rows(manifest, "program_occupancy") if occupancy_complete else []
    placement_rows = saved_rows(manifest, "admitted_placements")
    result["original_placement_rows"] = len(placement_rows)
    if occupancy_complete and not occupancy_gaps:
        admitted_total = sum(source_number(row["Candidaţi admişi"]) for row in occupancy_rows)
        result["occupancy_admitted_total"] = admitted_total
        result["original_placement_shortfall"] = admitted_total - len(placement_rows)
    else:
        notes.append(
            "The program occupancy table is incomplete, so the original placement "
            "shortfall is not established."
        )
    state = progress.get(county, {}).get("state", "")
    if result["occupancy_admitted_total"] == "":
        result["remaining_placement_shortfall"] = ""
    elif placement_complete and not placement_gaps and state != "placement_views_reconciled":
        result["remaining_placement_shortfall"] = result["original_placement_shortfall"]
        if result["original_placement_shortfall"] == 0:
            notes.append("The county admitted list matches the occupancy admitted total.")
        else:
            notes.append(
                "The county admitted list does not match the occupancy admitted total, "
                "and no recovered program-view reconciliation is recorded."
            )
    elif state == "placement_views_reconciled":
        expected = int(progress[county]["verified_programs"])
        program_rows = verified_program_rows(county, expected)
        original_keys, original_blank = counters(placement_rows)
        program_keys, program_blank = counters(program_rows)
        if original_blank or program_blank:
            notes.append(
                "Some placement or program-report rows lack a name or admission score, "
                "so the remaining shortfall is not established."
            )
        else:
            combined = original_keys + (program_keys - original_keys)
            result["remaining_placement_shortfall"] = result["occupancy_admitted_total"] - sum(combined.values())
            notes.append(
                f"Program recovery records {expected} verified program reports. "
                f"The original shortfall is {result['original_placement_shortfall']}. "
                f"The remaining unreconciled shortfall is {result['remaining_placement_shortfall']}."
            )
    else:
        notes.append(
            "Placement pages are still unresolved. The original shortfall is the gap "
            "in the saved county admitted list. It is not a count of unsuccessful students."
        )
        result["remaining_placement_shortfall"] = ""
    if directory_complete and occupancy_complete and not directory_gaps and not occupancy_gaps:
        try:
            programs = source_programs(manifest, county)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            result["program_identity"] = f"disagreement: {exc}"
            notes.append(f"Program directory and occupancy disagree: {exc}")
        else:
            result["program_identity"] = (
                f"{len(programs)} programs; capacity balances and directory labels agree"
            )
    else:
        result["program_identity"] = "not checked; program directory or occupancy pages are incomplete"
    result["note"] = " ".join(notes)
    return result


def _flow_from_pages(county, school_pages, admitted_pages):
    outgoing_keys = Counter()
    incoming_keys = Counter()
    outgoing_rows = Counter()
    incoming_rows = Counter()
    stats = Counter()
    missing_origin_columns = None
    origin_fields = ("Scoală provenienţă", "Şcoală provenienţă")
    for _relative, page in school_pages:
        for row in page["rows"]:
            destination = county_suffix(row.get("Liceu"))
            if not destination:
                stats["outgoing_rows_no_suffix"] += 1
                continue
            if destination == county:
                stats["outgoing_rows_own_county_suffix"] += 1
                continue
            stats["outgoing_rows_with_other_county_suffix"] += 1
            outgoing_rows[destination] += 1
            key = name_score(row)
            if key is None:
                stats["outgoing_rows_without_key"] += 1
                continue
            outgoing_keys[(destination, _key_text(key))] += 1
    for _relative, page in admitted_pages:
        for row in page["rows"]:
            if not any(field in row for field in origin_fields):
                stats["incoming_rows_no_or_unparsed_origin"] += 1
                missing_origin_columns = list(row.keys())
                continue
            origin = _origin_county(row, origin_fields)
            if not origin:
                stats["incoming_rows_no_or_unparsed_origin"] += 1
                continue
            if origin == county:
                stats["incoming_rows_own_county_suffix"] += 1
                continue
            stats["incoming_rows_with_other_county_suffix"] += 1
            incoming_rows[origin] += 1
            key = name_score(row)
            if key is None:
                stats["incoming_rows_without_key"] += 1
                continue
            incoming_keys[(origin, _key_text(key))] += 1
    return outgoing_keys, incoming_keys, outgoing_rows, incoming_rows, stats, missing_origin_columns


def _key_text(key):
    name, score = key
    return f"{name}\t{score}"


def _origin_county(row, fields):
    for field in fields:
        if field in row:
            return county_suffix(row.get(field)) or ""
    return None


def _write_ledger(county, fingerprint, payload):
    LEDGER_ROOT.mkdir(parents=True, exist_ok=True)
    os.chmod(LEDGER_ROOT, 0o700)
    path = LEDGER_ROOT / f"{county}.json"
    body = {"fingerprint": fingerprint, **payload}
    _atomic_text(path, json.dumps(body, ensure_ascii=False))
    os.chmod(path, 0o600)
    return path


def _read_ledger(county, fingerprint):
    path = LEDGER_ROOT / f"{county}.json"
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("fingerprint") != fingerprint:
        return None
    return payload


def reconcile_county(county, county_name, status, progress, fingerprint):
    say(f"{county_name} ({county}): reading saved checkpoints. No archive requests.")
    record = _blank({
        "county": county,
        "county_name": county_name,
        "checked_at": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
        "source_notes": [],
        "unresolved_school_result_urls": [],
    })
    manifest_path = CACHE / "county_manifests" / f"{county}.json"
    manifest = None
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            record["source_notes"].append(f"County manifest could not be read: {exc}")
    else:
        record["source_notes"].append("No saved county manifest for the original report families.")

    if manifest is not None:
        for family in BASE_FAMILIES:
            try:
                complete, unresolved = family_status(manifest, family)
                listed = len(manifest["families"][family].get("pages") or [])
                record["source_notes"].append(
                    f"{FAMILY_LABELS[family]}: {listed} saved pages listed in the manifest, "
                    f"{unresolved} unresolved URL addresses, "
                    f"{'complete flag is true' if complete else 'complete flag is false'}."
                )
            except (KeyError, TypeError, ValueError) as exc:
                record["source_notes"].append(f"{FAMILY_LABELS.get(family, family)}: {exc}")

    loaded = {}
    county_state = status.get("counties", {}).get(county, {})
    for family in NEW_FAMILIES:
        label = FAMILY_LABELS[family]
        state = county_state.get(family)
        if not state:
            record["source_notes"].append(f"{label}: not in the saved acquisition status.")
            loaded[family] = None
            continue
        say(f"{county_name} ({county}): checking {label}.")
        loaded[family] = _verified_family(county, family, state)
        info = loaded[family]
        record["source_notes"].append(
            f"{label}: {len(info['pages'])} verified pages, "
            f"target {info['target_pages']}, "
            f"{len(info['unresolved'])} unresolved URL addresses, "
            f"{len(info['problems'])} malformed or missing checkpoints, "
            f"{len(info['extra_files'])} files on disk that are not in the status list."
        )
        if info["projection_basis"]:
            record["source_notes"].append(f"{label} target basis: {info['projection_basis']}.")

    results = loaded.get("school_results")
    directory_pages, school_pages = _school_result_pages(results) if results else ([], [])
    record["school_result_pages_verified"] = len(school_pages)
    record["school_result_directory_pages"] = len(directory_pages)
    record["school_result_pages_expected"] = "" if not results else results["target_pages"]
    record["school_result_unresolved_urls"] = 0 if not results else len(results["unresolved"])
    record["school_result_malformed_pages"] = 0 if not results else len(results["problems"])
    record["unresolved_school_result_urls"] = [] if not results else sorted(results["unresolved"])
    record["school_result_rows"] = sum(len(page["rows"]) for _relative, page in school_pages)
    record["school_result_pages_complete"] = bool(results and results["complete"] and len(directory_pages) == 1)
    if results and len(directory_pages) != 1:
        record["source_notes"].append(
            f"School Result View directories verified: {len(directory_pages)}. "
            "Expected one directory page."
        )
    elif directory_pages:
        listed_schools = directory_pages[0][1].get("row_count")
        record["source_notes"].append(
            f"School Result View directory lists {listed_schools} schools and "
            f"{len(school_pages)} school pages were verified."
        )
        if listed_schools != len(school_pages):
            record["school_result_pages_complete"] = False
            record["source_notes"].append(
                "The verified school pages do not match the directory's school count."
            )

    residents = loaded.get("resident_candidates")
    if residents is not None:
        record["resident_pages_saved"] = len(residents["pages"])
        record["resident_pages_projected"] = (
            "" if residents["projected_pages"] is None else residents["projected_pages"]
        )
        record["resident_list_complete"] = bool(residents["complete"])
        resident_counter = multiset(_family_rows(residents))
        record["resident_rows_saved"] = count(resident_counter)
        if school_pages:
            result_counter = multiset(row for _relative, page in school_pages for row in page["rows"])
            compared = _multiset_report(
                "resident applicant list", "School Result View", resident_counter, result_counter
            )
            record["resident_rows_with_result_match"] = compared["matches"]
            record["resident_rows_without_result_match"] = compared["left_only"]
            record["result_rows_without_saved_resident_match"] = compared["right_only"]
            if not residents["complete"]:
                record["source_notes"].append(
                    "The resident applicant list is incomplete. Counts of rows without a "
                    "School Result View match describe the saved pages only. People on "
                    "missing pages are unresolved, not rejected."
                )
    else:
        record["resident_list_complete"] = False

    incoming = {}
    for family in ("incoming_candidates", "incoming_admitted", "incoming_rejected"):
        loaded_family = loaded.get(family)
        if loaded_family is None:
            incoming[family] = Counter()
            continue
        incoming[family] = multiset(_family_rows(loaded_family))
        if not loaded_family["complete"]:
            record["source_notes"].append(
                f"The {FAMILY_LABELS[family]} is incomplete, so its row counts use verified pages only."
            )
    outcomes = incoming["incoming_admitted"] + incoming["incoming_rejected"]
    record["incoming_candidate_rows"] = count(incoming["incoming_candidates"])
    record["incoming_admitted_rows"] = count(incoming["incoming_admitted"])
    record["incoming_rejected_rows"] = count(incoming["incoming_rejected"])
    record["incoming_candidate_rows_without_outcome"] = count(incoming["incoming_candidates"] - outcomes)
    record["incoming_outcome_rows_without_candidate"] = count(outcomes - incoming["incoming_candidates"])

    admitted_pages = [] if loaded.get("incoming_admitted") is None else loaded["incoming_admitted"]["pages"]
    outgoing_keys, incoming_keys, outgoing_rows, incoming_rows, flow_stats, missing_origin_columns = (
        _flow_from_pages(county, school_pages, admitted_pages)
    )
    record["outgoing_rows_with_other_county_suffix"] = flow_stats["outgoing_rows_with_other_county_suffix"]
    record["flow_stats"] = dict(flow_stats)
    if missing_origin_columns is not None:
        record["source_notes"].append(
            "Incoming admitted origin column was not found. Page columns: "
            + ", ".join(missing_origin_columns)
        )
    if flow_stats["outgoing_rows_own_county_suffix"]:
        record["source_notes"].append(
            f"{flow_stats['outgoing_rows_own_county_suffix']} School Result View rows "
            "have a destination suffix naming this same county. They are not counted as outgoing."
        )

    if manifest is not None:
        try:
            programs = _program_block(county, manifest, progress)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            programs = {
                "occupancy_admitted_total": "",
                "original_placement_rows": "",
                "original_placement_shortfall": "",
                "remaining_placement_shortfall": "",
                "program_identity": f"check stopped: {exc}",
                "note": str(exc),
            }
            say(f"{county_name} ({county}): program check stopped: {exc}")
        for key in (
            "occupancy_admitted_total",
            "original_placement_rows",
            "original_placement_shortfall",
            "remaining_placement_shortfall",
            "program_identity",
        ):
            record[key] = programs[key]
        if programs["note"]:
            record["source_notes"].append(programs["note"])
        try:
            applicants = _compare_applicants(county, manifest, school_pages)
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            applicants = {
                "expected_pages": "",
                "saved_pages": "",
                "matches": "",
                "applicant_without_result": "",
                "result_without_applicant": "",
                "component_disagreements": "",
                "note": f"School Applicant View comparison stopped: {exc}",
            }
            say(f"{county_name} ({county}): School Applicant View comparison stopped: {exc}")
        record["school_applicant_pages_expected"] = applicants["expected_pages"]
        record["school_applicant_pages_saved"] = applicants["saved_pages"]
        record["applicant_result_matches"] = applicants["matches"]
        record["applicant_rows_without_result"] = applicants["applicant_without_result"]
        record["result_rows_without_applicant"] = applicants["result_without_applicant"]
        record["applicant_component_disagreements"] = applicants["component_disagreements"]
        if applicants["note"]:
            record["source_notes"].append(applicants["note"])
        if manifest and family_status(manifest, "origin_school_directory")[0]:
            try:
                record["origin_directory_schools"] = len(school_directory(county))
            except (OSError, ValueError, KeyError, json.JSONDecodeError):
                record["origin_directory_schools"] = ""
    else:
        record["source_notes"].append(
            "School Applicant View and program checks need the county manifest, which is missing."
        )

    record["next_source_question"] = _next_question(record)
    record["plain_summary"] = _plain_summary(record)
    _write_ledger(county, fingerprint, {
        "school_results_complete": bool(record["school_result_pages_complete"]),
        "incoming_admitted_complete": bool(
            loaded.get("incoming_admitted") and loaded["incoming_admitted"]["complete"]
        ),
        "outgoing_keys": _grouped(outgoing_keys),
        "incoming_admitted_keys": _grouped(incoming_keys),
        "outgoing_rows": dict(outgoing_rows),
        "incoming_rows": dict(incoming_rows),
        "flow_stats": record["flow_stats"],
    })
    say(f"{county_name} ({county}): {record['plain_summary']}")
    say(f"{county_name} ({county}): next source question: {record['next_source_question']}")
    return record


def _grouped(pairs):
    grouped = {}
    for (other, key), n in pairs.items():
        grouped.setdefault(other, {})[key] = n
    return grouped


def _next_question(record):
    if record["school_result_malformed_pages"] not in ("", 0):
        return (
            f"{record['school_result_malformed_pages']} School Result View checkpoints "
            "are malformed or missing a file that the status list expects. "
            "Inspect those URL addresses before treating the county's results as covered."
        )
    if record["school_result_unresolved_urls"] not in ("", 0):
        return (
            f"{record['school_result_unresolved_urls']} School Result View URL "
            f"{'address remains' if record['school_result_unresolved_urls'] == 1 else 'addresses remain'} "
            "unresolved. Keep them open. Do not treat the missing school as having no applicants."
        )
    saved = record["school_applicant_pages_saved"]
    expected = record["school_applicant_pages_expected"]
    if expected != "" and saved != "" and saved < expected:
        return (
            f"School Applicant View pages saved: {saved} of {expected}. "
            "A gymnasium peer pool cannot be built until the missing pages are saved "
            "or explicitly left unresolved."
        )
    if record["resident_list_complete"] is False and record["resident_pages_projected"] != "":
        return (
            f"Resident applicant list pages saved: {record['resident_pages_saved']} of "
            f"{record['resident_pages_projected']}. Other views may still corroborate people. "
            "The short list is not a reason to drop the county."
        )
    if record["remaining_placement_shortfall"] not in ("", 0):
        return (
            f"Occupancy says {record['occupancy_admitted_total']} admitted places. "
            f"The original county admitted list is short by {record['original_placement_shortfall']}. "
            f"The remaining unreconciled shortfall is {record['remaining_placement_shortfall']}."
        )
    if record["applicant_rows_without_result"] not in ("", 0):
        return (
            f"{record['applicant_rows_without_result']} School Applicant View rows have no "
            "matching School Result View row at the same school, using printed name and admission score."
        )
    if str(record["program_identity"]).startswith("disagreement") or str(record["program_identity"]).startswith("check stopped"):
        return f"Program identity is unresolved: {record['program_identity']}"
    return (
        "Saved page checks finished without a new missing-file gap. "
        "Read the remaining ambiguous name-and-score counts before using the county in an outcome plot."
    )


def _plain_summary(record):
    parts = [
        f"{record['county_name']} ({record['county']}).",
        (
            f"School Result View: {record['school_result_pages_verified']} verified school pages"
            f" plus {record['school_result_directory_pages']} directory page"
            f" (page target {record['school_result_pages_expected']}, which includes the directory), "
            f"{record['school_result_rows']} printed rows, "
            f"{record['school_result_unresolved_urls']} unresolved URL addresses, "
            f"{record['school_result_malformed_pages']} malformed or missing checkpoints."
        ),
    ]
    if record["school_applicant_pages_expected"] == "":
        parts.append("School Applicant View was not compared because the origin school directory is not available.")
    else:
        parts.append(
            f"School Applicant View: {record['school_applicant_pages_saved']} saved pages "
            f"of {record['school_applicant_pages_expected']} listed schools."
        )
    if record["applicant_result_matches"] != "":
        parts.append(
            f"Provisional same-school name-and-score matches: {record['applicant_result_matches']}. "
            f"Applicant rows without a result row: {record['applicant_rows_without_result']}. "
            f"Result rows without an applicant row: {record['result_rows_without_applicant']}."
        )
    if record["resident_pages_projected"] != "":
        parts.append(
            f"Resident applicant list: {record['resident_pages_saved']} of "
            f"{record['resident_pages_projected']} projected pages."
        )
    parts.append(
        f"Incoming lists, verified rows: {record['incoming_candidate_rows']} applicants, "
        f"{record['incoming_admitted_rows']} admitted, {record['incoming_rejected_rows']} unassigned. "
        f"Applicant rows without an incoming outcome row: {record['incoming_candidate_rows_without_outcome']}. "
        f"Outcome rows without an incoming applicant row: {record['incoming_outcome_rows_without_candidate']}."
    )
    parts.append(
        f"School Result View rows with another county's destination suffix: "
        f"{record['outgoing_rows_with_other_county_suffix']}."
    )
    if record["original_placement_shortfall"] != "":
        remaining = record["remaining_placement_shortfall"]
        remaining_text = "not established" if remaining == "" else remaining
        parts.append(
            f"Original placement shortfall against occupancy: {record['original_placement_shortfall']}. "
            f"Remaining unreconciled shortfall: {remaining_text}."
        )
    parts.append(
        "These counts do not certify the county for a national outcome analysis."
    )
    return " ".join(str(part) for part in parts if part)


def _publish(run_folder, record):
    county_dir = run_folder / "counties"
    county_dir.mkdir(parents=True, exist_ok=True)
    path = county_dir / f"{record['county']}.json"
    public = {key: value for key, value in record.items() if key not in {"outgoing_keys", "incoming_keys"}}
    _atomic_text(path, json.dumps(public, ensure_ascii=False, indent=2))
    _rewrite_tables(run_folder)
    log_path = run_folder / "progress.jsonl"
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "checked_at": record["checked_at"],
            "county": record["county"],
            "county_name": record["county_name"],
            "next_source_question": record["next_source_question"],
        }, ensure_ascii=False) + "\n")
        stream.flush()
    say(f"Saved name-free county record: {path}")


def _rewrite_tables(run_folder):
    records = []
    for path in sorted((run_folder / "counties").glob("*.json")):
        records.append(json.loads(path.read_text(encoding="utf-8")))
    frame = pd.DataFrame(records)
    for field in SUMMARY_FIELDS:
        if field not in frame.columns:
            frame[field] = ""
    csv_path = run_folder / "county_summaries.csv"
    frame[list(SUMMARY_FIELDS)].to_csv(csv_path, index=False)
    lines = [
        "# Romania 2001 all-county offline reconciliation",
        "",
        "Name-free county findings. A printed name and admission score can corroborate "
        "two saved rows. It does not prove a unique person. This file does not authorize "
        "a national outcome analysis.",
        "",
        f"Counties with a saved check: {len(records)}.",
        "",
    ]
    for record in records:
        lines.append(f"## {record['county_name']} ({record['county']})")
        lines.append("")
        lines.append(record.get("plain_summary", ""))
        lines.append("")
        lines.append(f"Next source question: {record.get('next_source_question', '')}")
        lines.append("")
        for note in record.get("source_notes") or []:
            lines.append(f"- {note}")
        lines.append("")
    _atomic_text(run_folder / "report.md", "\n".join(lines))


def run_counties(counties=None, output_root=None, *, resume=True, force=()):
    """Check each county, write aggregates, and continue after a county error."""
    status = views.load_status()
    progress = placement_status()
    directory = county_directory()
    names = dict(directory)
    selected = list(counties) if counties else [code for code, _name in directory]
    unknown = [code for code in selected if code not in names]
    if unknown:
        raise ValueError(f"Unknown county code(s): {', '.join(unknown)}")
    run_folder = open_run(output_root, resume=resume)
    fingerprints = _load_json(run_folder / "fingerprints.json", {})
    force = {code.upper() for code in force}
    say(
        f"Counties in this pass: {len(selected)}. "
        "Each saved page is hash-checked. Nothing is downloaded."
    )
    for index, county in enumerate(selected, 1):
        current = fingerprint_county(county, status)
        saved = run_folder / "counties" / f"{county}.json"
        ledger = _read_ledger(county, current)
        if resume and county not in force and fingerprints.get(county) == current and saved.exists() and ledger:
            say(
                f"{index}/{len(selected)} {names[county]} ({county}): "
                "saved check matches current source files. Skipping."
            )
            continue
        say(f"{index}/{len(selected)} {names[county]} ({county}): starting.")
        try:
            record = reconcile_county(county, names[county], status, progress, current)
        except Exception as exc:
            say(f"{names[county]} ({county}): stopped with {type(exc).__name__}: {exc}")
            record = _blank({
                "county": county,
                "county_name": names[county],
                "checked_at": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z"),
                "plain_summary": (
                    f"{names[county]} ({county}) stopped before a full set of counts: "
                    f"{type(exc).__name__}: {exc}. Other counties continue."
                ),
                "next_source_question": f"Rerun {county} after reading the error above. This county was not marked done.",
                "source_notes": [f"{type(exc).__name__}: {exc}"],
            })
            _publish(run_folder, record)
            continue
        _publish(run_folder, record)
        fingerprints[county] = current
        _atomic_text(
            run_folder / "fingerprints.json",
            json.dumps(fingerprints, indent=2),
        )
    say(f"County pass finished. Run folder: {run_folder}")
    return run_folder


def cross_county_routes(run_folder):
    """Compare outgoing School Result View rows with incoming admitted lists.

    Aggregate equality is reported separately from uniquely supported name-and-score
    keys. Names stay in the private ledger.
    """
    run_folder = Path(run_folder)
    fingerprints = _load_json(run_folder / "fingerprints.json", {})
    county_paths = sorted((run_folder / "counties").glob("*.json"))
    if not county_paths:
        raise FileNotFoundError(f"No county records in {run_folder}")
    known = {code for code, _name in county_directory()}
    outgoing_counts = Counter()
    incoming_counts = Counter()
    pair_keys_out = {}
    pair_keys_in = {}
    coverage = {}
    say(f"Cross-county routes: {len(county_paths)} counties in {run_folder.name}. No archive requests.")
    for path in county_paths:
        record = json.loads(path.read_text(encoding="utf-8"))
        county = record["county"]
        ledger = _read_ledger(county, fingerprints.get(county))
        if ledger is None:
            raise FileNotFoundError(
                f"Private flow ledger for {county} is missing or does not match the saved fingerprint. "
                "Rerun that county in the county-pass cell."
            )
        coverage[county] = {
            "school_results_complete": ledger.get("school_results_complete", False),
            "incoming_admitted_complete": ledger.get("incoming_admitted_complete", False),
            "county_name": record.get("county_name", county),
        }
        for destination, n in ledger.get("outgoing_rows", {}).items():
            outgoing_counts[(county, destination)] += n
        for origin, n in ledger.get("incoming_rows", {}).items():
            incoming_counts[(origin, county)] += n
        for destination, keys in ledger.get("outgoing_keys", {}).items():
            for key, n in keys.items():
                pair_keys_out.setdefault((county, destination), Counter())[key] += n
        for origin, keys in ledger.get("incoming_admitted_keys", {}).items():
            for key, n in keys.items():
                pair_keys_in.setdefault((origin, county), Counter())[key] += n
        say(
            f"{record.get('county_name', county)} ({county}): "
            f"outgoing suffix rows {sum(ledger.get('outgoing_rows', {}).values())}, "
            f"incoming admitted suffix rows {sum(ledger.get('incoming_rows', {}).values())}."
        )
    pairs = sorted(set(outgoing_counts) | set(incoming_counts))
    rows = []
    for origin, destination in pairs:
        out_n = outgoing_counts[(origin, destination)]
        in_n = incoming_counts[(origin, destination)]
        left = pair_keys_out.get((origin, destination), Counter())
        right = pair_keys_in.get((origin, destination), Counter())
        unique = only_out = only_in = ambiguous = 0
        for key in set(left) | set(right):
            a, b = left[key], right[key]
            if a > 1 or b > 1:
                ambiguous += 1
            elif a == 1 and b == 1:
                unique += 1
            elif a == 1:
                only_out += 1
            elif b == 1:
                only_in += 1
        both_in_run = origin in coverage and destination in coverage
        both_complete = (
            both_in_run
            and coverage[origin]["school_results_complete"]
            and coverage[destination]["incoming_admitted_complete"]
        )
        if destination not in known:
            scope = "destination suffix is outside the 41 county units"
        elif origin not in known:
            scope = "origin suffix is outside the 41 county units"
        elif not both_in_run:
            scope = "one county was not in this run"
        elif not both_complete:
            scope = "one side still has unresolved, malformed, or incomplete pages"
        else:
            scope = "both sides verified for known pages"
        rows.append({
            "origin_county": origin,
            "destination_county": destination,
            "school_result_outgoing_rows": out_n,
            "incoming_admitted_rows": in_n,
            "aggregate_counts_agree": out_n == in_n,
            "unique_name_score_keys_on_both_sides": unique,
            "keys_only_on_school_result": only_out,
            "keys_only_on_incoming_admitted": only_in,
            "ambiguous_keys": ambiguous,
            "comparison_scope": scope,
        })
    frame = pd.DataFrame(rows)
    csv_path = run_folder / "cross_county_flow_counts.csv"
    frame.to_csv(csv_path, index=False)
    agree = int(frame["aggregate_counts_agree"].sum()) if len(frame) else 0
    complete_pairs = frame[frame["comparison_scope"] == "both sides verified for known pages"] if len(frame) else frame
    complete_agree = int(complete_pairs["aggregate_counts_agree"].sum()) if len(complete_pairs) else 0
    lines = [
        "# Cross-county routes",
        "",
        f"Counties included: {len(coverage)} of {len(known)} inventory units. "
        "A pair count uses School Result View rows whose destination label ends in another "
        "county code, and incoming admitted rows whose origin-school label ends in another county code.",
        "",
        "Equal aggregate counts do not prove that the same people appear on both sides. "
        "Aggregate row counts include rows that lack a printable name or admission score. "
        "Those rows are absent from the key comparison. "
        "A unique name-and-score key is one printed name and admission score that occurs once "
        "on each side. The archived personal identifier is masked, so even a unique key is provisional.",
        "",
        f"Pairs with any saved count: {len(frame)}. Aggregate counts agree: {agree}.",
        f"Pairs where both sides have complete known pages: {len(complete_pairs)}. "
        f"Those aggregate counts agree: {complete_agree}.",
        "",
        "This comparison does not authorize a national outcome analysis.",
        "",
    ]
    _atomic_text(run_folder / "cross_county_routes.md", "\n".join(lines))
    say(f"Saved cross-county counts: {csv_path}")
    say(lines[6])
    say(lines[7])
    return frame


def summary_frame(run_folder):
    run_folder = Path(run_folder)
    records = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((run_folder / "counties").glob("*.json"))
    ]
    frame = pd.DataFrame(records)
    for field in SUMMARY_FIELDS:
        if field not in frame.columns:
            frame[field] = ""
    return frame[list(SUMMARY_FIELDS)]
