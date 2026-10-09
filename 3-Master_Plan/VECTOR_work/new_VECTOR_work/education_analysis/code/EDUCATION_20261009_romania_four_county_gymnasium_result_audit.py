"""Offline source match: four counties' gymnasium score and school-result pages.

Read hash-verified private webpages, export county/school-count aggregates only.
Never print or save student names, scores, or raw source rows in Dropbox.
"""

import csv
from collections import Counter
from pathlib import Path

from EDUCATION_20261001_romania_four_county_school_sample import school_directory
from EDUCATION_20261002_romania_three_county_gymnasium_acquisition import saved_school
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import components, name_score
from EDUCATION_20261007_romania_seven_county_new_views_offline_audit import (
    count, marked_unassigned, multiset, rows, school_code,
)
import EDUCATION_20261006_romania_school_results_incoming_acquisition as views


COUNTIES = ("CT", "PH", "TM", "CJ")
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_four_new_county_source_reconciliation_20261008"
FIELDS = (
    "county", "directory_schools", "gymnasium_score_reports_verified",
    "gymnasium_score_reports_unresolved", "score_bearing_applicant_rows",
    "applicant_rows_with_both_score_components",
    "score_rows_without_name_admission_score", "same_school_name_score_matches",
    "score_rows_absent_from_school_results", "result_rows_absent_from_verified_score_reports",
    "result_only_rows_marked_unassigned", "result_only_rows_other_status",
    "result_rows_at_unresolved_gymnasiums",
)


def run():
    status = views.load_status()["counties"]
    records = []
    unresolved = []
    for county in COUNTIES:
        directory = school_directory(county)
        state = status[county]["school_results"]
        result_pages, missing = rows(county, "school_results", state)
        if missing or state["unresolved"] or len(result_pages) != state["projected_pages"]:
            raise ValueError(f"{county}: school-result source pages incomplete")
        result_by_code = {}
        for relative, page in result_pages:
            if relative.lower().startswith("raport_scoli_din_judet_tot.asp"):
                continue
            code = school_code(relative)
            if not code or code in result_by_code:
                raise ValueError(f"{county}: repeated or unidentified school-result code")
            result_by_code[code] = page["rows"]
        if set(result_by_code) != set(directory):
            raise ValueError(f"{county}: school-result and gymnasium directories differ")

        matched = score_only = result_only = result_unresolved = 0
        score_total = component_total = no_key = verified = 0
        extra_status = Counter()
        for code, (_label, relative) in directory.items():
            page = saved_school(county, code, relative)
            result_rows = result_by_code[code]
            if page is None:
                unresolved.append((county, code))
                result_unresolved += len(result_rows)
                continue
            verified += 1
            score_rows = page["rows"]
            score_total += len(score_rows)
            component_total += sum(components(row) is not None for row in score_rows)
            applicants = multiset(score_rows)
            no_key += len(score_rows) - count(applicants)
            results = multiset(result_rows)
            matched += count(applicants & results)
            score_only += count(applicants - results)
            result_only += count(results - applicants)
            extras = results - applicants
            for row in result_rows:
                key = name_score(row)
                if key and extras[key]:
                    extra_status["unassigned" if marked_unassigned(row) else "other"] += 1
                    extras[key] -= 1
        if result_only != extra_status.total():
            raise ValueError(f"{county}: extra result-row status count disagrees")
        record = {
            "county": county,
            "directory_schools": len(directory),
            "gymnasium_score_reports_verified": verified,
            "gymnasium_score_reports_unresolved": len(directory) - verified,
            "score_bearing_applicant_rows": score_total,
            "applicant_rows_with_both_score_components": component_total,
            "score_rows_without_name_admission_score": no_key,
            "same_school_name_score_matches": matched,
            "score_rows_absent_from_school_results": score_only,
            "result_rows_absent_from_verified_score_reports": result_only,
            "result_only_rows_marked_unassigned": extra_status["unassigned"],
            "result_only_rows_other_status": extra_status["other"],
            "result_rows_at_unresolved_gymnasiums": result_unresolved,
        }
        records.append(record)
        print(f"{county}: {verified}/{len(directory)} gymnasium reports; "
              f"{matched:,} applicant rows matched; {score_only} applicant rows absent from "
              f"school results; {result_only} extra result rows", flush=True)

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "gymnasium_result_match_counts.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, FIELDS)
        writer.writeheader()
        writer.writerows(records)
    total = lambda field: sum(row[field] for row in records)
    lines = [
        "# Romania 2001: four-county gymnasium-to-result source audit", "",
        "This is an offline comparison of saved, hash-verified Ministry webpages. "
        "It made no archive request and exports only counts. Matching printed name and admission "
        "score within the same originating-school code corroborates source rows but does not "
        "establish unique person identity; the archived personal identifier is masked.", "",
        f"Verified gymnasium reports: **{total('gymnasium_score_reports_verified')}/"
        f"{total('directory_schools')}**. The remaining school codes are **unresolved**, "
        "not assumed to have zero applicants.", "",
        f"The verified reports contain **{total('score_bearing_applicant_rows'):,}** "
        f"applicant rows; **{total('applicant_rows_with_both_score_components'):,}** have both "
        "the examination score and school-grade average. "
        f"**{total('same_school_name_score_matches'):,}** have a matching "
        f"row in the corresponding school-result report; **{total('score_rows_absent_from_school_results')}** "
        "do not. Across verified schools, the school-result reports have "
        f"**{total('result_rows_absent_from_verified_score_reports')}** additional rows, "
        f"including **{total('result_only_rows_marked_unassigned')}** explicitly marked "
        f"unassigned and **{total('result_only_rows_other_status')}** with another status. "
        "These extra rows are not silently added to a research cohort.", "",
        "## County details", "",
    ]
    for row in records:
        lines.append(
            f"- **{row['county']}:** {row['gymnasium_score_reports_verified']}/"
            f"{row['directory_schools']} gymnasium reports; "
            f"{row['same_school_name_score_matches']:,} matching applicant rows; "
            f"{row['score_rows_absent_from_school_results']} applicant rows absent from results; "
            f"{row['result_rows_absent_from_verified_score_reports']} result-only rows "
            f"({row['result_only_rows_marked_unassigned']} marked unassigned, "
            f"{row['result_only_rows_other_status']} other); "
            f"{row['result_rows_at_unresolved_gymnasiums']} result rows belong to unresolved schools."
        )
    lines += ["", "## Open source questions", ""]
    if unresolved:
        lines.append("1. Retry the following gymnasium report URL addresses, then rerun this audit: "
                     + ", ".join(f"{county} school code {code}" for county, code in unresolved) + ".")
    else:
        lines.append("All directory-listed gymnasium reports were verified.")
    if total("result_only_rows_other_status"):
        lines.append("2. Inspect the source context of result-only rows with statuses other than "
                     "unassigned before assigning them to any research cohort.")
    lines += ["", "This is a source reconciliation, not a HERO, peer-strength, program-ranking, "
              "or national outcome analysis.", ""]
    (OUT / "gymnasium_result_reconciliation.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved name-free audit: {OUT / 'gymnasium_result_reconciliation.md'}", flush=True)
    return records


if __name__ == "__main__":
    run()
