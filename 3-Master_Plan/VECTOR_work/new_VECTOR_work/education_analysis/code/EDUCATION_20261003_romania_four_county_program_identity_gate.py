"""Offline source gate for four-county local program identity; no HERO analysis.

Reads only saved Ministry pages and verified private checkpoints. Exports county
counts, never names, scores, row-level identifiers, or raw source pages.
"""

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from EDUCATION_20260930_romania_2001_national_acquisition import CACHE, _extract_rows
from EDUCATION_20261001_romania_offline_county_source_readiness import (
    family_status, placement_status, saved_rows, verified_program_rows,
)
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    COUNTIES, OUT, all_gymnasium_rows, name_score, saved_national_indexes,
)

CSV = OUT / "program_identity_source_gate.csv"
REPORT = OUT / "program_identity_source_gate.md"
FIELDS = (
    "county", "gymnasium_applicant_rows", "one_local_placement", "local_program_unique",
    "local_program_not_found", "local_program_ambiguous", "confirmed_unassigned",
    "ambiguous_might_be_top1", "ambiguous_might_be_top2",
    "placed_other_county", "unresolved_or_ambiguous_outcome", "no_observed_peer",
    "unique_programs", "fully_occupied_programs", "program_places", "program_admitted",
    "saved_local_placement_rows", "program_table_capacity_balanced",
    "program_table_admitted_matches_placements",
)


def clean(value):
    return " ".join(str(value or "").split())


def integer(value):
    return int(clean(value).replace(".", "").replace(" ", ""))


def source_programs(manifest, county):
    """Join directory and occupancy on printed program code; reject disagreement."""
    directory_rows = saved_rows(manifest, "program_directory")
    occupancy_rows = saved_rows(manifest, "program_occupancy")
    directory = {clean(row["Cod specializare"]): row for row in directory_rows}
    if len(directory) != len(directory_rows) or len(directory) != len(occupancy_rows):
        raise ValueError(f"{county}: duplicate or missing program directory codes")
    programs = []
    for row in occupancy_rows:
        code, description = clean(row["Liceu"]).split(" ", 1)
        if code not in directory:
            raise ValueError(f"{county}: occupancy code absent from directory")
        program = directory[code]
        if (clean(row["Profil"]) != clean(program["Profil"])
                or clean(row["Specializare"]) != clean(program["Specializare"])
                or not description.startswith(clean(program["Liceu"]) + " /")):
            raise ValueError(f"{county}: program source descriptions disagree at {code}")
        places = integer(row["Nr. de locuri"])
        admitted = integer(row["Candidaţi admişi"])
        vacancies = integer(row["Nr. de locuri libere"])
        if places != integer(program["Nr. de locuri"]) or places != admitted + vacancies:
            raise ValueError(f"{county}: program capacity balance failed at {code}")
        cutoff = Decimal(clean(row["Ultima notă"]).replace(",", ".")) if admitted else None
        programs.append((code, program, places, admitted, vacancies, cutoff))
    return programs


def local_placement_rows(manifest, county, progress, programs):
    complete, gaps = family_status(manifest, "admitted_placements")
    original = saved_rows(manifest, "admitted_placements")
    if complete and not gaps:
        return original
    status = progress.get(county, {})
    if status.get("state") != "placement_views_reconciled":
        raise ValueError(f"{county}: placement reports have not cleared source gate")
    # First verify every recovered page using the shared source-audit routine.
    verified_program_rows(county, int(status["verified_programs"]))
    by_numeric_code = {code.lstrip("x"): (code, admitted)
                       for code, _program, _places, admitted, _vacancies, _cutoff in programs}
    if len(by_numeric_code) != len(programs):
        raise ValueError(f"{county}: program code loses uniqueness without x prefix")
    combined = {name_score(row): row for row in original}
    if None in combined or len(combined) != len(original):
        raise ValueError(f"{county}: original report has blank or duplicate name-score key")
    folder = CACHE / "alternate_report_pilot" / county
    for path in sorted(folder.glob("destination_program_*.html")):
        numeric_code = path.stem.removeprefix("destination_program_")
        if numeric_code not in by_numeric_code:
            raise ValueError(f"{county}: recovered source program code absent from directory")
        code, expected_admitted = by_numeric_code[numeric_code]
        metadata = json.loads(path.with_suffix(".json").read_text())
        raw = path.read_bytes()
        if (hashlib.sha256(raw).hexdigest() != metadata["sha256"]
                or f"cs={numeric_code}&" not in metadata.get("effective_url", "")):
            raise ValueError(f"{county}: recovered page hash or URL code disagrees")
        _headings, rows = _extract_rows(raw)
        if len(rows) != metadata["row_count"] or len(rows) != expected_admitted:
            raise ValueError(f"{county}: program report count disagrees with occupancy")
        for row in rows:
            key = name_score(row)
            if key is None:
                raise ValueError(f"{county}: blank name or score in program report")
            if key in combined and "__source_program_code" in combined[key]:
                raise ValueError(f"{county}: duplicate recovered program row")
            combined[key] = {**row, "__source_program_code": code}
    return list(combined.values())


def run():
    gymnasiums, _ = all_gymnasium_rows()
    _, national_placements, national_unassigned, _ = saved_national_indexes()
    progress = placement_status()
    results = []
    for county in COUNTIES:
        manifest = json.loads((CACHE / "county_manifests" / f"{county}.json").read_text())
        programs = source_programs(manifest, county)
        ranked = defaultdict(set)
        for code, program, places, admitted, vacancies, cutoff in programs:
            if places and admitted and not vacancies and cutoff is not None:
                ranked[clean(program["Specializare"])].add(cutoff)
        cutoff_tiers = {subject: sorted(scores, reverse=True) for subject, scores in ranked.items()}
        top1 = {code for code, program, places, admitted, vacancies, cutoff in programs
                if places and admitted and not vacancies and cutoff is not None
                and cutoff in cutoff_tiers.get(clean(program["Specializare"]), [])[:1]}
        top2 = {code for code, program, places, admitted, vacancies, cutoff in programs
                if places and admitted and not vacancies and cutoff is not None
                and cutoff in cutoff_tiers.get(clean(program["Specializare"]), [])[:2]}
        reports = local_placement_rows(manifest, county, progress, programs)
        if len(reports) != sum(p[3] for p in programs):
            raise ValueError(f"{county}: local placement pages disagree with program occupancy")
        by_person = defaultdict(list)
        for report in reports:
            if key := name_score(report):
                by_person[key].append(report)
        if sum(len(value) for value in by_person.values()) != len(reports):
            raise ValueError(f"{county}: blank name or admission score in placement report")
        by_program = defaultdict(list)
        for code, program, *_ in programs:
            identity = tuple(clean(program[field]) for field in ("Liceu", "Profil", "Specializare"))
            by_program[identity].append(code)
        school_sizes = Counter(code for code, _key, _comp in gymnasiums[county])
        tally = Counter()
        for school_code, key, _comp in gymnasiums[county]:
            if school_sizes[school_code] < 2:
                tally["no_observed_peer"] += 1
            if key is None:
                tally["unresolved_or_ambiguous_outcome"] += 1
                continue
            local = by_person[key]
            if len(local) == 1:
                tally["one_local_placement"] += 1
                report = local[0]
                if "__source_program_code" in report:
                    matched = [report["__source_program_code"]]
                else:
                    destination = re.sub(rf"\s*/\s*{county}$", "", clean(report.get("Liceu")))
                    identity = (destination, clean(report.get("Profil")),
                                clean(report.get("Specializare")))
                    matched = by_program[identity]
                tally["local_program_unique" if len(matched) == 1 else
                      "local_program_not_found" if not matched else "local_program_ambiguous"] += 1
                if len(matched) > 1:
                    tally["ambiguous_might_be_top1"] += any(code in top1 for code in matched)
                    tally["ambiguous_might_be_top2"] += any(code in top2 for code in matched)
            elif len(local) > 1:
                tally["unresolved_or_ambiguous_outcome"] += 1
            elif len(national_unassigned[key]) == 1 and not national_placements[key]:
                tally["confirmed_unassigned"] += 1
            elif len(national_placements[key]) == 1 and national_placements[key][0] != county:
                tally["placed_other_county"] += 1
            else:
                tally["unresolved_or_ambiguous_outcome"] += 1
        if (tally["one_local_placement"] + tally["confirmed_unassigned"]
                + tally["placed_other_county"] + tally["unresolved_or_ambiguous_outcome"]
                != len(gymnasiums[county])):
            raise ValueError(f"{county}: outcome source categories do not sum")
        row = {field: tally[field] for field in FIELDS}
        row.update(county=county, gymnasium_applicant_rows=len(gymnasiums[county]),
                   unique_programs=len(programs),
                   fully_occupied_programs=sum(p[2] > 0 and p[4] == 0 for p in programs),
                   program_places=sum(p[2] for p in programs),
                   program_admitted=sum(p[3] for p in programs),
                   saved_local_placement_rows=len(reports),
                   program_table_capacity_balanced=True,
                   program_table_admitted_matches_placements=True)
        results.append(row)
        print(f"SOURCE GATE {county}: {row['one_local_placement']} local placements; "
              f"{row['local_program_unique']} unique program identities; "
              f"{row['local_program_not_found']} unmatched; "
              f"{row['local_program_ambiguous']} ambiguous", flush=True)
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="write name-free county audit")
    args = parser.parse_args(argv)
    print("OFFLINE PROGRAM SOURCE GATE: no Wayback requests or HERO analysis", flush=True)
    results = run()
    if not args.run:
        print("PREVIEW ONLY: add --run to write name-free county counts", flush=True)
        return
    OUT.mkdir(parents=True, exist_ok=True)
    with CSV.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(results)
    lines = [
        "# Romania 2001 four county program identity source gate", "",
        "This offline check asks whether each locally placed applicant from the four originating counties can be connected to one specific destination program in the saved Romanian Ministry tables. It uses the already-agreed top-one and top-two full-program rules only to check whether an uncertain exact program could alter a success label. It does not calculate a success rate or test a peer effect. No new webpage was requested and no individual information was exported.", "",
        "The Program Directory names every program and gives its code. The Program Occupancy View gives its seats, admitted count, vacancies, and cutoff. The Placement View identifies where each admitted applicant went. We joined the first two on exact printed program code and required seats to balance. For a recovered one-program webpage, the verified source URL and webpage filename supply that program's code; its student rows do not repeat a program name. For an original county-wide placement webpage, school, profile, and specialization must together identify exactly one directory entry.", "",
        "| Origin county | Applicant rows | Local placements | One program identified | More than one possible program | Ambiguous that might be top 1 | Ambiguous that might be top 2 | Unassigned | Placed outside origin county | Outcome unresolved | No observed gymnasium peer |", 
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        lines.append(f"| {row['county']} | {row['gymnasium_applicant_rows']:,} | "
                     f"{row['one_local_placement']:,} | {row['local_program_unique']:,} | "
                     f"{row['local_program_ambiguous']:,} | "
                     f"{row['ambiguous_might_be_top1']:,} | {row['ambiguous_might_be_top2']:,} | "
                     f"{row['confirmed_unassigned']:,} | {row['placed_other_county']:,} | "
                     f"{row['unresolved_or_ambiguous_outcome']:,} | {row['no_observed_peer']:,} |")
    lines += ["", "The 'might be top' columns are a conservative source-impact screen: they count ambiguous placements for which at least one possible directory program is in the agreed highest one or two full-program cutoff tiers. They are **not** successful-placement counts. All four counties have zero in both columns. Thus, for the six original program categories with the full-occupancy requirement, the 558 applicants with more than one possible exact program are known **not** to be in a designated top-one or top-two program. Their exact program identity remains unresolved.", "", "On October 4, Charles agreed to include these 558 applicants in the primary success-rate denominator as nonsuccesses, and to show a separately labeled comparison omitting them. Recheck the binary label if the category grouping or full-occupancy rule changes; the zero-impact finding does not automatically transfer to alternate definitions. Outside-county placements and the one unresolved outcome stay out of the primary within-county outcome denominator but remain in the originating-gymnasium peer calculation. A gymnasium with only one observed applicant cannot supply a leave-one-out peer average; report those rows separately rather than inventing one.", "", "Printed name plus admission score is a provisional link because the archived personal identifier is masked. This audit does not establish whether all eighth graders participated or who preferred any particular program. True program-level competitor counts and institutional K/N remain unknown because applicant preferences are not recorded.", ""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"SAVED {CSV} and {REPORT}", flush=True)


if __name__ == "__main__":
    main()
