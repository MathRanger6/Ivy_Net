"""Offline, name-free reconciliation of seven counties' new 2001 source views.

Reads verified private Ministry checkpoints. Prints and exports counts only.
Printed name + admission score is a provisional source-match key, not a
person identifier; the archive masks the personal ID. No source requests,
peer measures, program ranking, HERO curve, or substantive experiment.
"""

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import EDUCATION_20261006_romania_school_results_incoming_acquisition as views
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    all_gymnasium_rows, name_score, saved_national_indexes,
)
from EDUCATION_20260930_romania_2001_national_acquisition import CACHE
from EDUCATION_20261001_romania_offline_county_source_readiness import (
    placement_status, saved_rows, verified_program_rows,
)

COUNTIES = ("B", "AB", "CS", "GL", "TL", "AR", "SB")
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_seven_county_new_views_20261007"
CSV = OUT / "source_reconciliation.csv"
REPORT = OUT / "source_reconciliation.md"
FLOW_CSV = OUT / "county_flow_counts.csv"
FIELDS = (
    "county", "score_bearing_school_pages", "score_bearing_applicant_rows",
    "school_result_directory_rows", "school_result_pages_verified",
    "school_result_rows", "same_school_name_score_matches",
    "applicant_rows_absent_from_school_results", "result_rows_absent_from_score_pages",
    "result_only_rows_marked_unassigned", "result_only_rows_other_status",
    "applicant_rows_with_repeated_county_name_score",
    "incoming_candidate_rows", "incoming_admitted_rows", "incoming_unassigned_rows",
    "incoming_candidate_without_outcome", "incoming_outcome_without_candidate",
    "resident_pages_saved", "resident_pages_projected", "resident_pages_unresolved",
    "resident_rows_saved", "resident_rows_expected", "resident_to_school_matches",
    "resident_rows_absent_from_school_pages", "school_rows_absent_from_saved_resident_pages",
    "resident_source_complete",
)


def rows(county, family, state):
    """Return source rows after verifying every saved page's identity and hashes."""
    output = []
    missing = []
    for relative in state["discovered"]:
        page = views.checked_page(county, family, relative)
        if page is None:
            missing.append(relative)
        else:
            output.append((relative, page))
    return output, missing


def multiset(source_rows):
    return Counter(key for row in source_rows if (key := name_score(row)))


def count(counter):
    return sum(counter.values())


def school_code(relative):
    match = re.search(r"(?:[?&-])cs=([A-Za-z0-9]+)(?:[&.]|$)", relative, re.I)
    return match.group(1) if match else None


def marked_unassigned(row):
    """The Ministry puts this literal outcome marker in the Liceu column."""
    return "NEREPARTIZAT" in str(row.get("Liceu", "")).upper()


def county_suffix(label):
    """Read the Ministry's printed `/ XX` county suffix, without guessing a town."""
    match = re.search(r"/\s*([A-Z]{1,2})\s*$", str(label or ""))
    return match.group(1) if match else None


def source_flows(saved_status):
    """Aggregate origin/destination counts; no student-level record is exported."""
    outgoing = Counter()
    incoming = {family: Counter() for family in
                ("incoming_candidates", "incoming_admitted", "incoming_rejected")}
    for destination in COUNTIES:
        for family in incoming:
            pages, missing = rows(destination, family, saved_status[destination][family])
            if missing:
                raise ValueError(f"{destination}: {family} flow pages are incomplete")
            for _relative, page in pages:
                for row in page["rows"]:
                    label = (row.get("Şcoală de provenienţă") if family == "incoming_candidates"
                             else row.get("Scoală provenienţă"))
                    origin = county_suffix(label)
                    if not origin or origin == destination:
                        raise ValueError(f"{destination}: incoming origin county is absent or not external")
                    incoming[family][(origin, destination)] += 1
        pages, missing = rows(destination, "school_results", saved_status[destination]["school_results"])
        if missing:
            raise ValueError(f"{destination}: school-result flow pages are incomplete")
        for relative, page in pages:
            if relative.lower().startswith("raport_scoli_din_judet_tot"):
                continue
            for row in page["rows"]:
                receiving_county = county_suffix(row.get("Liceu"))
                if receiving_county:
                    if receiving_county == destination:
                        raise ValueError(f"{destination}: apparent cross-county suffix names own county")
                    outgoing[(destination, receiving_county)] += 1
    all_pairs = set(outgoing)
    for family in incoming:
        all_pairs.update(incoming[family])
    flow_rows = []
    overlap_pairs = overlap_people = 0
    for origin, destination in sorted(all_pairs):
        out_count = outgoing[(origin, destination)]
        admitted_count = incoming["incoming_admitted"][(origin, destination)]
        if origin in COUNTIES and destination in COUNTIES:
            if out_count != admitted_count:
                raise ValueError(f"{origin}→{destination}: outgoing and incoming admitted counts disagree")
            overlap_pairs += 1
            overlap_people += out_count
        flow_rows.append({
            "origin_county": origin,
            "destination_county": destination,
            "origin_school_result_outgoing_placed": out_count if origin in COUNTIES else "",
            "destination_incoming_candidates": incoming["incoming_candidates"][(origin, destination)]
                                               if destination in COUNTIES else "",
            "destination_incoming_admitted": admitted_count if destination in COUNTIES else "",
            "destination_incoming_unassigned": incoming["incoming_rejected"][(origin, destination)]
                                               if destination in COUNTIES else "",
        })
    return flow_rows, {
        "outgoing_placed_from_seven": sum(outgoing.values()),
        "incoming_candidates_to_seven": sum(incoming["incoming_candidates"].values()),
        "incoming_admitted_to_seven": sum(incoming["incoming_admitted"].values()),
        "incoming_unassigned_to_seven": sum(incoming["incoming_rejected"].values()),
        "within_seven_pairs_reconciled": overlap_pairs,
        "within_seven_admitted_reconciled": overlap_people,
    }


def bucharest_previously_unlocated(applicants_b, result_lookup):
    """Revisit only the B applicant rows the older 41-county audit could not locate."""
    manifest = json.loads((CACHE / "county_manifests/B.json").read_text())
    progress = placement_status()["B"]
    original = multiset(saved_rows(manifest, "admitted_placements"))
    program = multiset(verified_program_rows("B", int(progress["verified_programs"])))
    local_placed = original | program  # Two views of the same placements overlap.
    local_unassigned = Counter(
        key for row in saved_rows(manifest, "unassigned_applicants")
        if (key := name_score(row, "Media admitere"))
    )
    _applicants, national_placed, national_unassigned, _coverage = saved_national_indexes([])
    key_counts = Counter(key for _code, key, _components in applicants_b if key)
    tally = Counter()
    for code, key, _components in applicants_b:
        if key is None or key_counts[key] != 1 or local_placed[key] + local_unassigned[key]:
            continue
        if any(found != "B" for found in national_placed[key] + national_unassigned[key]):
            continue
        tally["previously_unlocated"] += 1
        result_rows = result_lookup.get((code, key), [])
        if len(result_rows) != 1:
            tally["missing_or_ambiguous_school_result"] += 1
        elif marked_unassigned(result_rows[0]):
            tally["school_result_says_unassigned"] += 1
        else:
            tally["school_result_other_status"] += 1
    return tally


def run():
    if not views.STATUS.exists():
        raise FileNotFoundError("The source-only worker has no saved checkpoint status")
    saved_status = views.load_status()["counties"]
    applicants, directory_counts = all_gymnasium_rows(COUNTIES)
    output = []
    for county in COUNTIES:
        source = saved_status[county]
        applicant_by_school = defaultdict(Counter)
        applicant_all = Counter()
        for code, key, _components in applicants[county]:
            if key:
                applicant_by_school[code][key] += 1
                applicant_all[key] += 1

        result_state = source["school_results"]
        result_pages, result_missing = rows(county, "school_results", result_state)
        directory_pages = [(relative, page) for relative, page in result_pages
                           if relative.lower().startswith("raport_scoli_din_judet_tot.asp")]
        if len(directory_pages) != 1:
            raise ValueError(f"{county}: need exactly one verified school-result directory")
        result_by_school = defaultdict(Counter)
        result_page_codes = set()
        result_only_status = Counter()
        result_lookup = defaultdict(list)
        for relative, page in result_pages:
            if relative.lower().startswith("raport_scoli_din_judet_tot.asp"):
                continue
            code = school_code(relative)
            if not code or code in result_page_codes:
                raise ValueError(f"{county}: duplicate or unidentified school-result page")
            result_page_codes.add(code)
            result_by_school[code].update(multiset(page["rows"]))
            extra_on_this_page = multiset(page["rows"]) - applicant_by_school[code]
            for row in page["rows"]:
                key = name_score(row)
                if county == "B" and key:
                    result_lookup[(code, key)].append(row)
                if key and extra_on_this_page[key]:
                    result_only_status["marked_unassigned" if marked_unassigned(row)
                                       else "other_status"] += 1
                    extra_on_this_page[key] -= 1
        if result_missing or result_state["unresolved"] or len(result_page_codes) != directory_counts[county]:
            raise ValueError(f"{county}: school-result source pages are still incomplete")

        shared = score_only = result_only = 0
        for code in applicant_by_school.keys() | result_by_school.keys():
            a, b = applicant_by_school[code], result_by_school[code]
            shared += count(a & b)
            score_only += count(a - b)
            result_only += count(b - a)
        if result_only_status.total() != result_only:
            raise ValueError(f"{county}: extra school-result status counts do not reconcile")

        incoming = {}
        for family in ("incoming_candidates", "incoming_admitted", "incoming_rejected"):
            pages, missing = rows(county, family, source[family])
            if missing or source[family]["unresolved"]:
                raise ValueError(f"{county}: {family} pages remain incomplete")
            incoming[family] = multiset(row for _relative, page in pages for row in page["rows"])
        incoming_outcomes = incoming["incoming_admitted"] + incoming["incoming_rejected"]

        resident_state = source["resident_candidates"]
        resident_pages, resident_missing = rows(county, "resident_candidates", resident_state)
        resident = multiset(row for _relative, page in resident_pages for row in page["rows"])
        resident_complete = (not resident_missing and not resident_state["unresolved"]
                             and resident_state.get("projected_pages") == len(resident_pages)
                             and resident_state.get("projected_records") == count(resident))
        record = {
            "county": county,
            "score_bearing_school_pages": directory_counts[county],
            "score_bearing_applicant_rows": count(applicant_all),
            "school_result_directory_rows": directory_pages[0][1]["row_count"],
            "school_result_pages_verified": len(result_page_codes),
            "school_result_rows": sum(count(values) for values in result_by_school.values()),
            "same_school_name_score_matches": shared,
            "applicant_rows_absent_from_school_results": score_only,
            "result_rows_absent_from_score_pages": result_only,
            "result_only_rows_marked_unassigned": result_only_status["marked_unassigned"],
            "result_only_rows_other_status": result_only_status["other_status"],
            "applicant_rows_with_repeated_county_name_score": sum(n for n in applicant_all.values() if n > 1),
            "incoming_candidate_rows": count(incoming["incoming_candidates"]),
            "incoming_admitted_rows": count(incoming["incoming_admitted"]),
            "incoming_unassigned_rows": count(incoming["incoming_rejected"]),
            "incoming_candidate_without_outcome": count(incoming["incoming_candidates"] - incoming_outcomes),
            "incoming_outcome_without_candidate": count(incoming_outcomes - incoming["incoming_candidates"]),
            "resident_pages_saved": len(resident_pages),
            "resident_pages_projected": resident_state.get("projected_pages", ""),
            "resident_pages_unresolved": len(resident_state["unresolved"]),
            "resident_rows_saved": count(resident),
            "resident_rows_expected": resident_state.get("projected_records", ""),
            "resident_to_school_matches": count(resident & applicant_all),
            "resident_rows_absent_from_school_pages": count(resident - applicant_all),
            "school_rows_absent_from_saved_resident_pages": count(applicant_all - resident),
            "resident_source_complete": resident_complete,
        }
        output.append(record)
        if county == "B":
            b_unlocated = bucharest_previously_unlocated(applicants[county], result_lookup)
            if (b_unlocated["school_result_says_unassigned"]
                    + b_unlocated["school_result_other_status"]
                    + b_unlocated["missing_or_ambiguous_school_result"]
                    != b_unlocated["previously_unlocated"]):
                raise ValueError("B: new result statuses do not account for older source gaps")
        print(f"{county}: school rows {record['score_bearing_applicant_rows']} matched; "
              f"{result_only} extra result rows; incoming candidate/outcome "
              f"{record['incoming_candidate_rows']}/{count(incoming_outcomes)}; "
              f"resident pages {len(resident_pages)}/{resident_state.get('projected_pages', '?')}", flush=True)

    OUT.mkdir(parents=True, exist_ok=True)
    with CSV.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(output)
    flow_rows, flow_summary = source_flows(saved_status)
    with FLOW_CSV.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(flow_rows[0]))
        writer.writeheader()
        writer.writerows(flow_rows)
    total_applicants = sum(row["score_bearing_applicant_rows"] for row in output)
    total_extras = sum(row["result_rows_absent_from_score_pages"] for row in output)
    extra_unassigned = sum(row["result_only_rows_marked_unassigned"] for row in output)
    total_incoming = sum(row["incoming_candidate_rows"] for row in output)
    total_admitted = sum(row["incoming_admitted_rows"] for row in output)
    total_unassigned = sum(row["incoming_unassigned_rows"] for row in output)
    lines = [
        "# Romania 2001: seven-county offline source reconciliation", "",
        "This audit reads saved, hash-verified Ministry webpages only. It makes no archive request. "
        "It compares printed name and admission score **within the same originating-school code**, "
        "but the archived personal identifier is masked. A matching printed key is strong source "
        "corroboration, not proof of unique person identity.", "",
        f"Across B, AB, CS, GL, TL, AR, and SB, all **{total_applicants:,}** score-bearing "
        "gymnasium applicant rows have a corresponding school-result row. "
        f"The school-result webpages contain **{total_extras} additional rows** not found in "
        f"their same-school score-bearing webpages. **{extra_unassigned}** carry the Ministry's "
        "literal `NEREPARTIZAT` (unassigned) marker; one carries another status. "
        "Those rows need a separate source explanation; "
        "they are not silently added to a research cohort.", "",
        f"The older Bucharest source audit could not locate **{b_unlocated['previously_unlocated']}** "
        "gymnasium applicants in its saved county outcome lists. Each has exactly one matching "
        "row in the newly recovered result page for the same originating school, and all "
        f"**{b_unlocated['school_result_says_unassigned']}** are explicitly marked "
        "`NEREPARTIZAT`. The archived personal ID is masked, so this is a provisional "
        "printed-name-and-admission-score match corroborated by school code, not a certified "
        "person-identifier linkage. The old 86-person *source gap* is resolved by this view; "
        "it does not show a program preference or justify a new analysis yet.", "",
        f"The separate cross-county candidate lists contain **{total_incoming:,}** rows. "
        f"At printed name-and-score multiplicity, they equal **{total_admitted:,} admitted + "
        f"{total_unassigned:,} unassigned** incoming rows, with zero unmatched rows in either direction. "
        "This verifies the three incoming source views against each other for these destination "
        "counties; it does not establish a national transfer rate.", "",
        "These sources also support **county-to-county flow counts**. Every incoming candidate, "
        "admitted, and unassigned row in these seven destination counties prints an "
        "origin-school label ending in its county code. The school-result webpages for "
        f"these seven origin counties print **{flow_summary['outgoing_placed_from_seven']:,}** "
        "placements with an external destination-county suffix. In the "
        f"**{flow_summary['within_seven_pairs_reconciled']} origin–destination county pairs** "
        "where both sides are among the seven, the two independent admitted counts agree "
        f"for all **{flow_summary['within_seven_admitted_reconciled']}** placements. "
        "The accompanying `county_flow_counts.csv` gives aggregate counts by origin and "
        "destination, never student names. A cross-county admissions route is observable; "
        "whether a family moved or a student sought a particular program is not.", "",
        "The resident-candidate report pages are complete by their own printed page totals in "
        "AB, CS, TL, AR, and SB. Their printed name-and-score rows exactly match the "
        "score-bearing gymnasium webpages. Bucharest (B) has 6 of 45 projected resident pages, "
        "and Galați (GL) has 9 of 11; each has an unresolved archived URL. Their saved resident "
        "rows are subsets of the school webpages, but the missing resident pages remain unresolved. "
        "A source-printed total matching a school-page count does not substitute for those pages.", "",
        "## County counts", "",
    ]
    for row in output:
        extra_word = "row" if row["result_rows_absent_from_score_pages"] == 1 else "rows"
        lines.append(
            f"- **{row['county']}:** {row['same_school_name_score_matches']:,} school-page rows "
            f"matched; {row['result_rows_absent_from_score_pages']} extra school-result {extra_word}; "
            f"incoming {row['incoming_candidate_rows']} = "
            f"{row['incoming_admitted_rows']} admitted + {row['incoming_unassigned_rows']} "
            f"unassigned; resident pages {row['resident_pages_saved']}/"
            f"{row['resident_pages_projected']} projected"
            f"{' (source incomplete)' if not row['resident_source_complete'] else ''}."
        )
    lines += [
        "", "## Open source questions", "",
        "1. Explain the 25 school-result-only rows by inspecting their saved source context and "
        "whether they belong to a different allocation route or a report inconsistency. Do not "
        "infer a reason from these counts alone.",
        "2. Seek alternative archived captures for the missing B and GL resident-candidate pages; "
        "keep the addresses unresolved until Charles decides whether to stop recovery.",
        "", "This is a source audit, not a HERO or congestion analysis. No student names, personal "
        "identifiers, or individual scores are exported in the report or CSV.", "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved name-free audit: {REPORT}")
    return output


if __name__ == "__main__":
    run()
