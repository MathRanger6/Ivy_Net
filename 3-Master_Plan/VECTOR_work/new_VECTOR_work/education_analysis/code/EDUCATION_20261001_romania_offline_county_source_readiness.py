"""Offline Romania 2001 source-readiness audit; no network and no outcome analysis.

Run from the notebook, or with:
    python EDUCATION_20261001_romania_offline_county_source_readiness.py --run

The private Desktop cache is read only. This script publishes county aggregates, never
student names, individual scores, or raw archived pages. A match by printed name and
admission score is provisional and does not establish a unique national identifier.
"""

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from EDUCATION_20260930_romania_2001_national_acquisition import CACHE, _extract_rows

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "outputs/romania_2001_national_source_recovery/placement_county_status.csv"
OUT = ROOT / "outputs/romania_2001_source_readiness"
FIELDS = [
    "county", "candidate_pages_complete", "candidate_unresolved_addresses",
    "candidate_rows_saved", "candidate_unique_signatures", "candidate_duplicate_signatures",
    "candidate_exam_score_rows", "candidate_school_label_rows", "candidate_distinct_school_labels",
    "unassigned_pages_complete", "unassigned_unresolved_addresses", "unassigned_rows_saved",
    "origin_directory_complete", "origin_directory_school_codes",
    "county_placement_pages_complete", "placement_source_status", "admitted_total_reference",
    "placement_rows_available", "recovered_program_reports_verified",
    "candidate_to_placement_unique_matches", "candidate_to_unassigned_unique_matches",
    "candidate_without_unique_local_outcome", "ambiguous_candidate_signatures",
    "candidate_to_outcome_link_status", "origin_school_code_link_status", "source_followup_group",
]


def say(message):
    print(f"{datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z} | {message}", flush=True)


def normalized_text(value):
    return " ".join(str(value or "").split())


def signature(row, score_field="Medie Admitere"):
    name = normalized_text(row.get("Nume"))
    score = normalized_text(row.get(score_field)).replace(",", ".")
    return (name, score) if name and score else None


def saved_rows(manifest, family):
    """Read only saved, manifest-listed source pages; never request a URL."""
    result = []
    for page in manifest["families"][family]["pages"]:
        payload = json.loads((CACHE / page["file"]).read_text())
        rows = payload["rows"]
        if payload["row_count"] != len(rows):
            raise ValueError(f"Saved page row count changed: {page['file']}")
        result.extend(rows)
    return result


def family_status(manifest, family):
    report = manifest["families"][family]
    return bool(report["complete"]), len(report["unresolved"])


def number(value):
    return int(str(value).replace(".", "").replace(" ", ""))


def placement_status():
    if not STATUS.exists():
        return {}
    with STATUS.open(newline="") as stream:
        return {row["county"]: row for row in csv.DictReader(stream)}


def verified_program_rows(county, expected_count):
    """Open only checked program reports in the private recovery cache."""
    folder = CACHE / "alternate_report_pilot" / county
    reports = sorted(folder.glob("destination_program_*.html"))
    if len(reports) != expected_count:
        raise ValueError(f"{county}: {len(reports)} saved program reports, expected {expected_count}")
    legacy_path = folder / "initial_pilot_sources.json"
    legacy = json.loads(legacy_path.read_text()) if legacy_path.exists() else {}
    rows = []
    for raw_path in reports:
        meta_path = raw_path.with_suffix(".json")
        if meta_path.exists():
            meta = json.loads(meta_path.read_text())
        else:
            meta = legacy.get(raw_path.stem)
            code = raw_path.stem.removeprefix("destination_program_")
            if (county != "VS" or not meta or meta.get("file") != raw_path.name
                    or f"cs={code}&" not in meta.get("effective_url", "")):
                raise ValueError(f"{county}: unverified legacy report {raw_path.name}")
        raw = raw_path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != meta["sha256"]:
            raise ValueError(f"{county}: checkpoint hash mismatch at {raw_path.name}")
        headings, report_rows = _extract_rows(raw)
        if not {"Nume", "Medie Admitere"}.issubset(headings):
            raise ValueError(f"{county}: unexpected report columns at {raw_path.name}")
        if "row_count" in meta and len(report_rows) != meta["row_count"]:
            raise ValueError(f"{county}: checkpoint row count mismatch at {raw_path.name}")
        rows.extend(report_rows)
    return rows


def counters(rows, score_field="Medie Admitere"):
    found = Counter()
    blank = 0
    for row in rows:
        key = signature(row, score_field)
        if key is None:
            blank += 1
        else:
            found[key] += 1
    return found, blank


def county_audit(county, placement_progress):
    manifest_path = CACHE / "county_manifests" / f"{county}.json"
    if not manifest_path.exists():
        raise ValueError(f"No saved county manifest for {county}; audit stops rather than guessing")
    manifest = json.loads(manifest_path.read_text())
    candidate = saved_rows(manifest, "candidate_roster")
    unassigned = saved_rows(manifest, "unassigned_applicants")
    admitted = saved_rows(manifest, "admitted_placements")
    origin_directory = saved_rows(manifest, "origin_school_directory")
    occupancy = saved_rows(manifest, "program_occupancy")
    candidate_complete, candidate_gaps = family_status(manifest, "candidate_roster")
    unassigned_complete, unassigned_gaps = family_status(manifest, "unassigned_applicants")
    placement_complete, _ = family_status(manifest, "admitted_placements")
    directory_complete, _ = family_status(manifest, "origin_school_directory")
    expected_admitted = sum(number(row["Candidaţi admişi"]) for row in occupancy)
    admitted_keys, admitted_blank = counters(admitted)
    verified_programs = 0
    progress = placement_progress.get(county, {})
    if placement_complete:
        if len(admitted) != expected_admitted:
            raise ValueError(f"{county}: complete county placement count disagrees with occupancy")
        source_status = "original_county_pages_complete"
    elif progress.get("state") == "placement_views_reconciled":
        verified_programs = int(progress["verified_programs"])
        program_rows = verified_program_rows(county, verified_programs)
        program_keys, program_blank = counters(program_rows)
        if program_blank or admitted_blank:
            raise ValueError(f"{county}: blank name or score in placement comparison")
        if sum(program_keys.values()) != len(program_keys):
            raise ValueError(f"{county}: duplicate program-report signatures")
        admitted_keys += (program_keys - admitted_keys)
        if sum(admitted_keys.values()) != expected_admitted:
            raise ValueError(f"{county}: combined placement count disagrees with occupancy")
        source_status = "recovered_program_views_reconciled"
    else:
        source_status = "placement_pages_unresolved"
    candidate_keys, candidate_blank = counters(candidate)
    unassigned_keys, unassigned_blank = counters(unassigned, "Media admitere")
    # Count only one-to-one links within this county. Cross-county placements,
    # duplicate names/scores, and missing pages remain separate uncertainty.
    placed = sum(1 for key, n in candidate_keys.items()
                 if n == 1 and admitted_keys[key] == 1 and unassigned_keys[key] == 0)
    not_placed = sum(1 for key, n in candidate_keys.items()
                     if n == 1 and unassigned_keys[key] == 1 and admitted_keys[key] == 0)
    ambiguous = sum(1 for key, n in candidate_keys.items()
                    if n > 1 or admitted_keys[key] > 1 or unassigned_keys[key] > 1
                    or (admitted_keys[key] and unassigned_keys[key]))
    school_labels = [normalized_text(row.get("Şcoală")) for row in candidate]
    exam_rows = sum(bool(normalized_text(row.get("Medie Capacitate"))) for row in candidate)
    if not candidate_complete:
        followup = "candidate_pages_first"
    elif not unassigned_complete:
        followup = "unassigned_pages_first"
    elif source_status == "placement_pages_unresolved":
        followup = "placement_pages_first"
    else:
        followup = "origin_school_code_and_person_link_review"
    return {
        "county": county, "candidate_pages_complete": candidate_complete,
        "candidate_unresolved_addresses": candidate_gaps,
        "candidate_rows_saved": len(candidate),
        "candidate_unique_signatures": len(candidate_keys),
        "candidate_duplicate_signatures": sum(n-1 for n in candidate_keys.values() if n > 1),
        "candidate_exam_score_rows": exam_rows,
        "candidate_school_label_rows": sum(bool(x) for x in school_labels),
        "candidate_distinct_school_labels": len(set(x for x in school_labels if x)),
        "unassigned_pages_complete": unassigned_complete,
        "unassigned_unresolved_addresses": unassigned_gaps,
        "unassigned_rows_saved": len(unassigned),
        "origin_directory_complete": directory_complete,
        "origin_directory_school_codes": len(origin_directory),
        "county_placement_pages_complete": placement_complete,
        "placement_source_status": source_status,
        "admitted_total_reference": expected_admitted,
        "placement_rows_available": sum(admitted_keys.values()),
        "recovered_program_reports_verified": verified_programs,
        "candidate_to_placement_unique_matches": placed,
        "candidate_to_unassigned_unique_matches": not_placed,
        "candidate_without_unique_local_outcome": len(candidate)-placed-not_placed,
        "ambiguous_candidate_signatures": ambiguous,
        "candidate_to_outcome_link_status": "provisional_name_and_admission_score_within_county",
        "origin_school_code_link_status": "unverified_name_to_directory_code",
        "source_followup_group": followup,
    }


def write_outputs(rows):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "EDUCATION_20261001_county_source_readiness.csv"
    temporary = path.with_suffix(".part")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)
    summary = OUT / "EDUCATION_20261001_source_readiness_summary.md"
    missing_applicants = [row["county"] for row in rows if not row["candidate_pages_complete"]]
    missing_unassigned = [row["county"] for row in rows if not row["unassigned_pages_complete"]]
    missing_placements = [row["county"] for row in rows
                          if row["placement_source_status"] == "placement_pages_unresolved"]
    report_sets_present = [row["county"] for row in rows
                           if row["candidate_pages_complete"] and row["unassigned_pages_complete"]
                           and row["placement_source_status"] != "placement_pages_unresolved"]
    text = [
        "# Romania 2001 offline county source readiness",
        "",
        "This is a source inventory, not a national outcome analysis or a list of counties approved for HERO curves. It reads only saved private checkpoints. No student names or individual scores are exported.",
        "",
        f"Counties inspected: **{len(rows)}**. Placement views available to occupancy total: **{sum(row['placement_source_status'] != 'placement_pages_unresolved' for row in rows)}**. Candidate page families complete: **{sum(row['candidate_pages_complete'] for row in rows)}**. Unassigned page families complete: **{sum(row['unassigned_pages_complete'] for row in rows)}**.",
        "",
        "## What we have, and what is still missing",
        "",
        "Each county has three lists to compare: (1) people who applied, (2) people placed in a program, and (3) people left without a placement. A school directory is a fourth list used to identify each applicant's originating gymnasium. Here, a 'complete' list means its expected archived report pages were saved; it does not yet establish that the list includes every child who attended a gymnasium. The two-letter labels below are county abbreviations (for example, AB means Alba and B means Bucharest).",
        "",
        f"- **All three applicant/placement report sets are present in {len(report_sets_present)} counties:** {', '.join(report_sets_present) or 'none'}. The next check for these counties is whether the gymnasium name printed beside each applicant can be matched reliably to one school in the directory. We must also review the provisional person match between the applicant and outcome lists. Having all three lists does not yet make a county ready for a HERO curve.",
        f"- **The applicant list still has missing archived pages in {len(missing_applicants)} counties:** {', '.join(missing_applicants) or 'none'}. We can read the applicant pages already saved, but cannot yet say we have the full participating applicant list for those counties. The immediate source task is to recover or account for those pages.",
        f"- **The unassigned-applicant list still has missing pages in {len(missing_unassigned)} counties:** {', '.join(missing_unassigned) or 'none'}. A person absent from the placement list is not automatically an unsuccessful applicant; the missing list must be checked too.",
        f"- **The placement reports are still unresolved in {len(missing_placements)} counties:** {', '.join(missing_placements) or 'none'}. Until those reports are accounted for, some applicants' destinations may be absent.",
        "",
        "These are overlapping descriptions, not four separate sets of counties. A county can appear in more than one missing-page line. The four-way 'next task' field in the detailed CSV records only the first issue the script encountered, so use the separate completeness columns to see every open issue.",
        "",
        "## What this check means for the study",
        "",
        "For counties with all three report sets, the saved applicant names and admission scores could be matched one-to-one to a saved placement or unassigned record within that county. This is an encouraging consistency check, not proof of a unique national student identifier or complete gymnasium peer groups. Next, verify school-name-to-directory-code mapping and the meaning of the applicant population before producing outcome curves.",
        "", "## Interpretation limits", "",
        "- A complete archived applicant report covers that report's participating applicants; it does not prove that every eighth grader at each gymnasium participated.",
        "- The candidate roster contains school labels, while the directory contains school codes. This audit does not equate them or certify complete origin-school groups.",
        "- Name plus admission score is only a provisional within-county comparison. An unmatched candidate may have a cross-county outcome or a missing report. Never count it as unsuccessful by default.",
        "- Recovered placement reports are used only when the existing placement worker marked the county reconciled and saved report hashes and row counts still verify.",
        "- The CSV contains name-free aggregates. The private source pages remain on the Desktop. A researcher must review the source gates and authorize any national outcome analysis.",
        "", "Detailed name-free counts are in `EDUCATION_20261001_county_source_readiness.csv`.", "",
    ]
    summary.write_text("\n".join(text), encoding="utf-8")
    say(f"SAVED name-free county audit: {path}")
    say(f"SAVED interpretation: {summary}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="run the offline audit and save name-free results")
    parser.add_argument("--counties", nargs="*", help="optional county codes; default all 41")
    args = parser.parse_args(argv)
    directory = json.loads((CACHE / "county_directory.json").read_text())
    all_codes = [row["county_code"] for row in directory["counties"]]
    wanted = set(args.counties or all_codes)
    unknown = wanted - set(all_codes)
    if unknown:
        parser.error(f"Unknown county code(s): {sorted(unknown)}")
    codes = [code for code in all_codes if code in wanted]
    say(f"OFFLINE SOURCE AUDIT: {len(codes)} county units queued; no network requests")
    if not args.run:
        say("PREVIEW ONLY. Pass --run or enable the notebook run switch to audit saved pages.")
        return
    progress = placement_status()
    results = []
    for i, county in enumerate(codes, 1):
        say(f"READING SAVED SOURCES {i}/{len(codes)}: {county}")
        row = county_audit(county, progress)
        results.append(row)
        say(f"CHECKED {county}: candidates {row['candidate_rows_saved']}; "
            f"placement {row['placement_source_status']}; next {row['source_followup_group']}")
    write_outputs(results)
    say("OFFLINE AUDIT COMPLETE. Source gates remain separate from analysis authorization.")


if __name__ == "__main__":
    main()
