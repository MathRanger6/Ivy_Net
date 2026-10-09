"""Offline source gate for CT/PH/TM/CJ program-label plot eligibility.

Reads hash-verified private pages, exports county counts only. No network,
success-rate plots, or peer-effect test. Masked IDs make row links provisional.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

import EDUCATION_20261004_romania_four_county_pilot as pilot
import EDUCATION_20261006_romania_school_results_incoming_acquisition as views
from EDUCATION_20261001_romania_four_county_school_sample import school_directory
from EDUCATION_20261002_romania_three_county_gymnasium_acquisition import saved_school
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import name_score
from EDUCATION_20261003_romania_four_county_program_identity_gate import (
    clean, local_placement_rows,
)
from EDUCATION_20261001_romania_offline_county_source_readiness import placement_status
from EDUCATION_20261007_romania_seven_county_new_views_offline_audit import (
    county_suffix, marked_unassigned, rows, school_code,
)

COUNTIES = ("CT", "PH", "TM", "CJ")
OUT = Path(__file__).resolve().parents[1] / "outputs/romania_2001_four_new_county_source_reconciliation_20261008"
FIELDS = (
    "county", "applicant_rows", "matched_result_rows", "ambiguous_or_missing_result_rows",
    "home_placements", "away_placements", "unassigned",
    "one_program", "multiple_programs", "no_program_match",
    "exact_program_code_corroborated",
    "top1_label_unresolved", "top2_label_unresolved",
    "program_admitted_total", "home_plus_incoming_admitted", "occupancy_difference",
    "single_applicant_gymnasiums",
)


def run():
    state = views.load_status()["counties"]
    settings = pilot.Settings()
    progress = placement_status()
    output = []
    for county in COUNTIES:
        schools = school_directory(county)
        saved, missing = rows(county, "school_results", state[county]["school_results"])
        if missing or state[county]["school_results"]["unresolved"]:
            raise ValueError(f"{county}: school-result pages incomplete")
        result_by_school = {}
        for relative, page in saved:
            if relative.lower().startswith("raport_scoli_din_judet_tot.asp"):
                continue
            code = school_code(relative)
            if code in result_by_school or code is None:
                raise ValueError(f"{county}: duplicate or unidentified school-result page")
            result_by_school[code] = page["rows"]
        if set(schools) != set(result_by_school):
            raise ValueError(f"{county}: gymnasium/result directories disagree")

        _manifest, programs, catalog = pilot._program_catalog(county)
        by_identity = defaultdict(list)
        for code, program, *_ in programs:
            by_identity[tuple(clean(program[field]) for field in
                              ("Liceu", "Profil", "Specializare"))].append(code)
        winners = {tier: pilot._winner_codes(catalog, tier, settings) for tier in (1, 2)}
        incoming, missing = rows(county, "incoming_admitted", state[county]["incoming_admitted"])
        if missing or state[county]["incoming_admitted"]["unresolved"]:
            raise ValueError(f"{county}: incoming-admitted pages incomplete")
        incoming_count = sum(page["row_count"] for _url, page in incoming)

        # Reuse independently verified destination-program webpages where
        # available. A code is trusted only for a county-unique printed key
        # whose school/profile/specialization also agrees with this result.
        coded_placements = {}
        for placed_row in local_placement_rows(_manifest, county, progress, programs):
            if "__source_program_code" in placed_row:
                key = name_score(placed_row)
                if key in coded_placements:
                    raise ValueError(f"{county}: duplicate coded placement key")
                coded_placements[key] = placed_row["__source_program_code"]
        school_pages = {}
        county_keys = Counter()
        for code, (_school_name, relative) in schools.items():
            school_pages[code] = saved_school(county, code, relative)
            if school_pages[code] is None:
                raise ValueError(f"{county} gymnasium {code}: score page missing")
            county_keys.update(name_score(row) for row in school_pages[code]["rows"])

        tally = Counter()
        for code, (_school_name, relative) in schools.items():
            score_page = school_pages[code]
            applicant_keys = Counter(name_score(row) for row in score_page["rows"])
            result_keys = defaultdict(list)
            for row in result_by_school[code]:
                result_keys[name_score(row)].append(row)
            tally["applicant_rows"] += score_page["row_count"]
            tally["single_applicant_gymnasiums"] += score_page["row_count"] == 1
            for key, n in applicant_keys.items():
                found = result_keys.get(key, [])
                tally["matched_result_rows"] += min(n, len(found))
                if key is None or n != 1 or len(found) != 1:
                    tally["ambiguous_or_missing_result_rows"] += n
                    continue
                result = found[0]
                if marked_unassigned(result):
                    tally["unassigned"] += 1
                    continue
                destination = county_suffix(result.get("Liceu")) or county
                if destination != county:
                    tally["away_placements"] += 1
                    continue
                tally["home_placements"] += 1
                options = pilot._destination_options(result, county, catalog, by_identity)
                coded = coded_placements.get(key)
                if coded is not None and county_keys[key] == 1:
                    school = clean(result.get("Liceu"))
                    suffix = f" / {county}"
                    if school.endswith(suffix):
                        school = school[:-len(suffix)]
                    identity = (school, clean(result.get("Profil")),
                                clean(result.get("Specializare")))
                    if (coded not in options
                            or coded not in catalog
                            or (catalog[coded]["school"],
                                clean(result.get("Profil")),
                                catalog[coded]["category"]) != identity):
                        raise ValueError(f"{county}: coded program contradicts result label")
                    options = [coded]
                    tally["exact_program_code_corroborated"] += 1
                tally["one_program" if len(options) == 1 else
                      "multiple_programs" if options else "no_program_match"] += 1
                for tier in (1, 2):
                    if not options or len({option in winners[tier] for option in options}) != 1:
                        tally[f"top{tier}_label_unresolved"] += 1
        tally["program_admitted_total"] = sum(program[3] for program in programs)
        tally["home_plus_incoming_admitted"] = tally["home_placements"] + incoming_count
        tally["occupancy_difference"] = (tally["program_admitted_total"]
                                          - tally["home_plus_incoming_admitted"])
        record = {"county": county, **{field: tally[field] for field in FIELDS if field != "county"}}
        output.append(record)
        print(f"{county}: {tally['applicant_rows']:,} applicants; "
              f"{tally['home_placements']:,} home placements; "
              f"top-one/top-two labels unresolved "
              f"{tally['top1_label_unresolved']}/{tally['top2_label_unresolved']}; "
              f"occupancy difference {tally['occupancy_difference']:+}", flush=True)

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "plot_source_gate_counts.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, FIELDS)
        writer.writeheader()
        writer.writerows(output)
    total = lambda field: sum(row[field] for row in output)
    lines = [
        "# Romania 2001: four-county program-label source gate", "",
        "This offline check uses saved, hash-verified Ministry pages only. It exports "
        "county counts, not names or scores. It applies the previously chosen six "
        "program categories, full-occupancy rule, and top-one/top-two cutoff tiers "
        "only to test source-label certainty. It does not calculate success rates.", "",
        f"Applicants: **{total('applicant_rows'):,}**. Corresponding school-result "
        f"rows: **{total('matched_result_rows'):,}**. Rows with a missing or nonunique "
        f"school-specific printed name-and-score key: "
        f"**{total('ambiguous_or_missing_result_rows')}**. The archived personal "
        "identifier is masked, so all matches remain provisional.", "",
        f"Among uniquely matched rows: **{total('home_placements'):,}** home "
        f"placements, **{total('away_placements'):,}** away placements, and "
        f"**{total('unassigned'):,}** unassigned. Home placement labels identify "
        f"one directory program for **{total('one_program'):,}** rows and multiple "
        f"programs for **{total('multiple_programs'):,}** rows; "
        f"**{total('no_program_match')}** have no directory match. "
        f"Already-saved program-specific reports corroborate exact codes for "
        f"**{total('exact_program_code_corroborated'):,}** home placements. "
        f"Top-one labels are unresolved for **{total('top1_label_unresolved')}** "
        f"home placements; top-two for **{total('top2_label_unresolved')}**. "
        "An unresolved label is never coded as a failure by default.", "",
        "## County detail", "",
    ]
    for row in output:
        lines.append(
            f"- **{row['county']}:** {row['applicant_rows']:,} applicants; "
            f"{row['home_placements']:,} home placements; "
            f"{row['away_placements']:,} away placements; {row['unassigned']:,} "
            f"unassigned; {row['multiple_programs']:,} multiple-program labels; "
            f"top-one/top-two unresolved {row['top1_label_unresolved']}/"
            f"{row['top2_label_unresolved']}; occupancy difference "
            f"{row['occupancy_difference']:+}."
        )
    lines += [
        "", "Occupancy difference equals the program tables' admitted total minus "
        "home-origin placements plus admitted arrivals from other counties. "
        "A nonzero difference requires source review; a zero difference is an "
        "aggregate check, not person-level proof.", "",
        "This is a source gate, not a HERO plot, program preference measure, "
        "or national outcome analysis.", "",
    ]
    path = OUT / "plot_source_gate.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print("Saved name-free source gate:", path, flush=True)
    return output


if __name__ == "__main__":
    run()
