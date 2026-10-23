"""Two descriptive checks beside the existing Romania placement plots.

Test 1 counts, for each applicant, how many other applicants on the same
gymnasium page have a strictly higher national exam score. Test 2 records how
many filled cutoffs in the destination category sit strictly above the program
the student entered. Neither test changes the saved top-program outcome.

Student-level rows stay in memory. The run writes name-free aggregate tables
and two figures only when called with run=True. Importing this module does not
read source pages and does not make web requests.
"""

from collections import defaultdict
from datetime import datetime
import json
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import EDUCATION_20261004_romania_four_county_pilot as base
import EDUCATION_20261009_romania_ct_ph_tm_cj_descriptive_pilot as pilot
from EDUCATION_20261001_romania_four_county_school_sample import school_directory
from EDUCATION_20261001_romania_offline_county_source_readiness import placement_status
from EDUCATION_20261002_romania_full_gymnasium_offline_reconciliation import (
    all_gymnasium_rows, components, name_score,
)
from EDUCATION_20261002_romania_three_county_gymnasium_acquisition import saved_school
from EDUCATION_20261003_romania_four_county_program_identity_gate import (
    clean, local_placement_rows,
)
from EDUCATION_20261007_romania_seven_county_new_views_offline_audit import (
    county_suffix, marked_unassigned, rows, school_code,
)

ROOT = pilot.ROOT
OUTPUTS = ROOT / "outputs/romania_2001_competitor_count_and_cutoff_step"
WITHIN_TOWN_OUTPUTS = ROOT / "outputs/romania_2001_within_town_same_score"
# The 22 counties whose live builder already clears both cutoff tiers.
PLOTTED_COUNTIES = (
    "AB", "CS", "GL", "TL", "AR", "SB", "B", "CT", "PH", "TM", "CJ",
    "AG", "BR", "BT", "BV", "DB", "DJ", "GJ", "IL", "OT", "VL", "VN",
)
COMPETITOR_EDGES = (0, 1, 5, 10, 20, np.inf)
COMPETITOR_LABELS = ("0", "1-4", "5-9", "10-19", "20 or more")


def _better_counts(exams):
    """Count other scores in this gymnasium that are strictly higher."""
    values = np.asarray(exams, dtype=float)
    n = len(values)
    order = np.argsort(values, kind="mergesort")
    ordered = values[order]
    above = np.empty(n, dtype=int)
    i = n - 1
    while i >= 0:
        j = i
        while j >= 0 and ordered[j] == ordered[i]:
            j -= 1
        above[j + 1:i + 1] = n - 1 - i
        i = j
    counts = np.empty(n, dtype=int)
    counts[order] = above
    return counts


def _category(program, settings):
    return base._ranking_category(program, settings)


def _filled_ladders(catalog, settings):
    """Distinct filled cutoffs in each category, highest first."""
    by_category = defaultdict(set)
    for program in catalog.values():
        if (program["places"] <= 0 or program["admitted"] <= 0
                or program["cutoff"] is None
                or (settings.require_full_programs and program["vacancies"] != 0)):
            continue
        category = _category(program, settings)
        if category is None:
            continue
        by_category[category].add(program["cutoff"])
    return {category: sorted(cutoffs, reverse=True)
            for category, cutoffs in by_category.items()}


def _step_from_options(options, catalog, ladders, settings):
    """Return (state, steps). Steps count filled cutoffs strictly above.

    The entered program does not itself have to be filled. A town college
    with vacancies still has a countable distance below the filled cutoffs
    in its category. A destination with no recorded cutoff, or labels that
    point at different steps, stays unresolved and out of the step average.
    """
    if not options:
        return "no_local_program", None
    steps = []
    for code in options:
        program = catalog[code]
        category = _category(program, settings)
        if category is None:
            return "other_subject", None
        if program["cutoff"] is None:
            return "cutoff_absent", None
        ladder = ladders.get(category, [])
        steps.append(sum(cutoff > program["cutoff"] for cutoff in ladder))
    if len(set(steps)) != 1:
        return "mixed_step", None
    return "placed", int(steps[0])


def _earlier_order(county, settings):
    """Program options in the same student order as the earlier-county plot."""
    gymnasiums, _directories = all_gymnasium_rows((county,))
    manifest, programs, catalog = base._program_catalog(county)
    reports = local_placement_rows(manifest, county, placement_status(), programs)
    local = defaultdict(list)
    for report in reports:
        key = name_score(report)
        if key is None:
            raise ValueError(f"{county}: blank name or score in a placement report")
        local[key].append(report)
    by_identity = defaultdict(list)
    for code, source, *_rest in programs:
        identity = tuple(clean(source[field]) for field in ("Liceu", "Profil", "Specializare"))
        by_identity[identity].append(code)
    ordered = []
    for gymnasium, key, score in gymnasiums[county]:
        found = local.get(key, [])
        options = ()
        if len(found) == 1:
            options = tuple(base._destination_options(found[0], county, catalog, by_identity))
        ordered.append({"county": county, "gymnasium": str(gymnasium),
                        "exam": float(score[0]), "options": options})
    return ordered, catalog


def _later_order(county, settings):
    """Program options in the same student order as the later-county plot."""
    schools = school_directory(county)
    state = pilot.views.load_status()["counties"][county]["school_results"]
    saved, missing = rows(county, "school_results", state)
    if missing or state["unresolved"] or len(saved) != state["saved_pages"]:
        raise ValueError(f"{county}: school-result pages are incomplete")
    results_by_school = {}
    for relative, page in saved:
        if relative.lower().startswith("raport_scoli_din_judet_tot.asp"):
            continue
        code = school_code(relative)
        if code is None or code in results_by_school:
            raise ValueError(f"{county}: duplicate or unidentified result school")
        results_by_school[code] = page["rows"]
    manifest, programs, catalog = base._program_catalog(county)
    placements = local_placement_rows(manifest, county, placement_status(), programs)
    exact_codes = {}
    for row in placements:
        code = row.get("__source_program_code")
        if code is None:
            continue
        key = name_score(row)
        if key is None or key in exact_codes:
            raise ValueError(f"{county}: duplicate exact-code source key")
        exact_codes[key] = code
    by_identity = defaultdict(list)
    for code, program, *_rest in programs:
        identity = tuple(clean(program[field]) for field in ("Liceu", "Profil", "Specializare"))
        by_identity[identity].append(code)
    ordered = []
    for gymnasium, (_name, relative) in schools.items():
        page = saved_school(county, gymnasium, relative)
        if page is None:
            raise ValueError(f"{county} gymnasium {gymnasium}: score report absent")
        result_keys = defaultdict(list)
        for row in results_by_school[gymnasium]:
            result_keys[name_score(row)].append(row)
        for student in page["rows"]:
            key = name_score(student)
            matches = result_keys.get(key, [])
            if key is None or len(matches) != 1:
                raise ValueError(f"{county} gymnasium {gymnasium}: result match is not unique")
            result = matches[0]
            options = ()
            if not marked_unassigned(result) and (county_suffix(result.get("Liceu")) or county) == county:
                options = tuple(base._destination_options(result, county, catalog, by_identity))
                exact = exact_codes.get(key)
                if exact is not None:
                    if exact not in options:
                        raise ValueError(f"{county}: exact code contradicts school-result label")
                    options = (exact,)
            ordered.append({"county": county, "gymnasium": str(gymnasium),
                            "exam": float(components(student)[0]), "options": options})
    return ordered, catalog


def _attach(students, settings):
    """Add competitor counts and cutoff steps, aligned to the plot's rows."""
    first = settings.top_tiers[0]
    base_rows = students.loc[students["tier"] == first].copy()
    base_rows["gymnasium"] = base_rows["gymnasium"].astype(str)
    attached = []
    for county, part in base_rows.groupby("county", sort=False):
        print(f"Cutoff step {county}...", flush=True)
        if county in pilot.LATER_COUNTIES:
            ordered, catalog = _later_order(county, settings)
        elif county in base.COUNTY_NAMES:
            ordered, catalog = _earlier_order(county, settings)
        else:
            raise ValueError(f"{county}: not in either source pipeline")
        part = part.reset_index(drop=True)
        if len(part) != len(ordered):
            raise ValueError(f"{county}: student count differs from the placement plot")
        walked_exam = np.array([row["exam"] for row in ordered], dtype=float)
        walked_gym = [row["gymnasium"] for row in ordered]
        if not np.array_equal(part["exam"].to_numpy(dtype=float), walked_exam):
            raise ValueError(f"{county}: exam order differs from the placement plot")
        if part["gymnasium"].tolist() != walked_gym:
            raise ValueError(f"{county}: gymnasium order differs from the placement plot")
        ladders = _filled_ladders(catalog, settings)
        states, steps = [], []
        for row, source in zip(part.itertuples(index=False), ordered):
            state, step = _step_from_options(source["options"], catalog, ladders, settings)
            local = str(row.status).startswith("local_")
            if local and state == "no_local_program":
                raise ValueError(f"{county}: local placement did not resolve to a program")
            if not local and source["options"]:
                raise ValueError(f"{county}: non-local row still resolved to a program")
            if state == "placed" and int(row.success) == 1 and step != 0:
                raise ValueError(f"{county}: top-tier placement is not at the top filled cutoff")
            if row.status == "placed_other_county":
                state = "outside_county"
            elif row.status == "confirmed_unassigned":
                state = "unassigned"
            states.append(state)
            steps.append(step if state == "placed" else np.nan)
        part = part.copy()
        part["ladder_state"] = states
        part["cutoffs_above"] = steps
        part["n_better_peers"] = part.groupby("gymnasium", sort=False)["exam"].transform(
            lambda exams: _better_counts(exams.to_numpy()))
        attached.append(part)
    return pd.concat(attached, ignore_index=True)


def _competitor_bin(counts):
    return pd.cut(counts, COMPETITOR_EDGES, right=False, labels=COMPETITOR_LABELS,
                  include_lowest=True)


def _cell_record(cell, county, band, competitor_bin):
    placed = cell.loc[cell["ladder_state"] == "placed", "cutoffs_above"]
    gymnasiums = (len(cell.drop_duplicates(["county", "gymnasium"])) if county == "ALL"
                  else cell["gymnasium"].nunique())
    return {
        "county": county,
        "band": band,
        "competitor_bin": str(competitor_bin),
        "applicants": len(cell),
        "gymnasiums": int(gymnasiums),
        "mean_better_peers": cell["n_better_peers"].mean(),
        "top_tier_successes": int(cell["success"].sum()),
        "top_tier_rate": cell["success"].mean(),
        "placed_with_cutoff_step": int(len(placed)),
        "mean_cutoffs_above": placed.mean() if len(placed) else np.nan,
        "median_cutoffs_above": placed.median() if len(placed) else np.nan,
        "share_at_top_cutoff": float((placed == 0).mean()) if len(placed) else np.nan,
        "unassigned": int((cell["ladder_state"] == "unassigned").sum()),
        "cutoff_absent": int((cell["ladder_state"] == "cutoff_absent").sum()),
    }


def _aggregate(measured, settings):
    work = measured.copy()
    work["tier"] = settings.top_tiers[0]
    work, _boundaries = base._add_bands(work, settings)
    eligible = base._eligible(work, settings, exclude_vocational=False, exclude_ambiguous=False)
    eligible = eligible.loc[eligible["exclusion"] == "included"].copy()
    eligible["competitor_bin"] = _competitor_bin(eligible["n_better_peers"])
    records = []
    for (county, band, competitor_bin), cell in eligible.groupby(
            ["county", "county_band", "competitor_bin"], sort=False, observed=True):
        records.append(_cell_record(cell, county, band, competitor_bin))
    for (band, competitor_bin), cell in eligible.groupby(
            ["county_band", "competitor_bin"], sort=False, observed=True):
        records.append(_cell_record(cell, "ALL", band, competitor_bin))
    table = pd.DataFrame(records)
    order = {label: i for i, label in enumerate(COMPETITOR_LABELS)}
    table["bin_order"] = table["competitor_bin"].map(order)
    table.sort_values(["county", "band", "bin_order"], inplace=True, kind="stable", ignore_index=True)
    return table.drop(columns="bin_order"), eligible


def _plot(table, settings, folder):
    labels = base._band_labels(settings)
    high_bands = labels[2:]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    pooled = table.loc[table["county"] == "ALL"]
    for axis, band in zip(axes, high_bands):
        data = pooled.loc[pooled["band"] == band].sort_values("competitor_bin",
            key=lambda s: s.map({label: i for i, label in enumerate(COMPETITOR_LABELS)}))
        axis.plot(np.arange(len(data)), 100 * data["top_tier_rate"], marker="o", color="#a43d4c")
        for position, row in enumerate(data.itertuples()):
            axis.annotate(f"{row.top_tier_successes}/{row.applicants}\n{row.gymnasiums} gyms",
                          (position, 100 * row.top_tier_rate), fontsize=7, ha="center",
                          xytext=(0, 6), textcoords="offset points")
        axis.set_xticks(np.arange(len(data)), data["competitor_bin"], rotation=30)
        axis.set_title(band)
        axis.set_xlabel("Classmates with a higher exam score")
        axis.grid(axis="y", alpha=.25)
    axes[0].set_ylabel("Placed in top filled program (%)")
    fig.suptitle("Test 1. Top-program placement by number of higher-scoring classmates\n"
                 f"Applicant-weighted across {len(settings.counties)} counties. Descriptive.")
    fig.tight_layout()
    fig.savefig(folder / "competitor_count_top_tier.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for axis, band in zip(axes, high_bands):
        data = pooled.loc[pooled["band"] == band].sort_values("competitor_bin",
            key=lambda s: s.map({label: i for i, label in enumerate(COMPETITOR_LABELS)}))
        axis.plot(np.arange(len(data)), data["mean_cutoffs_above"], marker="o", color="#356c9b")
        for position, row in enumerate(data.itertuples()):
            axis.annotate(f"{row.placed_with_cutoff_step} placed\n{row.gymnasiums} gyms",
                          (position, row.mean_cutoffs_above), fontsize=7, ha="center",
                          xytext=(0, 6), textcoords="offset points")
        axis.set_xticks(np.arange(len(data)), data["competitor_bin"], rotation=30)
        axis.set_title(band)
        axis.set_xlabel("Classmates with a higher exam score")
        axis.grid(axis="y", alpha=.25)
    axes[0].set_ylabel("Filled cutoffs above the program entered")
    fig.suptitle("Test 2. Cutoff steps by number of higher-scoring classmates\n"
                 f"Applicant-weighted across {len(settings.counties)} counties. "
                 "Outside-county and mixed-step placements are omitted from the mean.")
    fig.tight_layout()
    fig.savefig(folder / "competitor_count_cutoff_steps.png", dpi=160)
    plt.close(fig)


def run(settings: pilot.Settings | None = None, *, run: bool = False):
    """Build both checks only after the caller sets run=True."""
    if settings is None:
        settings = pilot.Settings(counties=PLOTTED_COUNTIES, ai_percentile_cuts=(90, 80, 50))
    settings.validate()
    if not run:
        print("Analysis is off. Call run(settings, run=True) to build the two checks.", flush=True)
        return None
    print("Building the placement rows used by the existing plots...", flush=True)
    frame, _chosen, _overview = pilot._source_frames(settings)
    measured = _attach(frame, settings)
    table, _eligible_rows = _aggregate(measured, settings)
    stamp = datetime.now().astimezone().strftime("run_%Y%m%dT%H%M%S%z")
    folder = OUTPUTS / stamp
    folder.mkdir(parents=True, exist_ok=False)
    table.to_csv(folder / "competitor_count_and_cutoff_step.csv", index=False)
    _plot(table, settings, folder)
    (folder / "run_manifest.json").write_text(json.dumps({
        "run_at_local": stamp,
        "counties": list(settings.counties),
        "ai_percentile_cuts": list(settings.ai_percentile_cuts),
        "top_tier": settings.top_tiers[0],
        "require_full_programs": settings.require_full_programs,
        "combine_program_categories": settings.combine_program_categories,
        "math_cs_only": settings.math_cs_only,
        "competitor_definition": "other applicants on the same gymnasium page with a strictly higher exam score",
        "step_definition": "count of filled category cutoffs strictly above the entered program",
        "privacy": "aggregate output only",
    }, indent=2) + "\n")
    pooled = table.loc[(table["county"] == "ALL") & (table["band"].isin(base._band_labels(settings)[2:]))]
    print(pooled[["band", "competitor_bin", "applicants", "top_tier_successes", "top_tier_rate",
                  "mean_cutoffs_above", "share_at_top_cutoff"]].to_string(index=False), flush=True)
    print(f"Saved {folder}", flush=True)
    return folder


# Ilfov localities that appear at the end of a Bucharest and Ilfov school name.
# Every other school in county B is treated as the Bucharest market.
_ILFOV_LOCALITIES = frozenset({
    "AFUMATI", "BALOTESTI", "BERCENI", "BRAGADIRU", "BRANESTI", "BUFTEA",
    "CERNICA", "CHIAJNA", "CHITILA", "CIOLPANI", "CIOROGIRLA", "CLINCENI",
    "CORBEANCA", "CORNETU", "DARASTI", "DASCALU", "DOBROESTI", "DOMNESTI",
    "DRAGOMIRESTI-DEAL", "DRAGOMIRESTI-VALE", "GANEASA", "GLINA", "GRADISTEA",
    "GRUIU", "JILAVA", "MAGURELE", "MOGOSOAIA", "NUCI", "PANTELIMON", "PERIS",
    "PETRACHIOAIA", "POPESTI-LEORDENI", "SNAGOV", "TUNARI", "VIDRA", "VOLUNTARI",
    "DECEMBRIE", "VLASIEI",
})
_DIACRITICS = str.maketrans({
    "Ă": "A", "Â": "A", "Î": "I", "Ș": "S", "Ş": "S", "Ț": "T", "Ţ": "T",
    "ă": "A", "â": "A", "î": "I", "ș": "S", "ş": "S", "ț": "T", "ţ": "T",
})


def _place_token(name):
    """Return (token, truncated). Truncated names are 50 characters on the page."""
    original = name.strip()
    text = original.upper().translate(_DIACRITICS)
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s*\([^)]*\)\s*$", "", text).strip()
    raw = text.split(",")[-1].strip() if "," in text else (text.split()[-1] if text.split() else "")
    place = re.sub(r"^(COMUNA|COM\.|ORASUL|ORAS|MUNICIPIUL|MUN\.|SATUL|SAT)\s+", "", raw)
    place = place.replace("TG-", "TIRGU-").replace("TARGU", "TIRGU")
    place = re.sub(r"\bTG\b", "TIRGU", place)
    place = re.sub(r"\s+", "-", place.strip(" .,"))
    if not re.fullmatch(r"[A-Z][A-Z-]{3,}", place or ""):
        return None, len(original) >= 50
    return place, len(original) >= 50


def _towns_for_county(county):
    """Map a gymnasium code to a town. Names that do not yield a town map to None.

    Bucharest schools rarely print the city. They share one market. A printed
    Ilfov locality stays its own town. A 50-character name is kept only when
    its visible ending is a unique prefix, at least 6 letters, of one complete
    town token in that county.
    """
    parsed = {}
    complete = set()
    for code, (name, _relative) in school_directory(county).items():
        place, truncated = _place_token(name)
        parsed[code] = (place, truncated, name)
        if place and not truncated:
            complete.add(place)
    towns = {}
    for code, (place, truncated, _name) in parsed.items():
        if county == "B":
            towns[code] = place if place in _ILFOV_LOCALITIES else "BUCURESTI"
            continue
        if place and not truncated:
            towns[code] = place
            continue
        if place and truncated and len(place) >= 6:
            matches = [item for item in complete if item.startswith(place)]
            towns[code] = matches[0] if len(matches) == 1 else None
            continue
        towns[code] = None
    return towns


def _within_town_tables(measured, settings, *, slice_low=90, slice_high=95, min_side=15):
    """Compare gymnasiums that share a town, inside a narrow own-score slice.

    The peer measure is a property of the gymnasium: how many of its applicants
    sit at or above the county top-tenth cutoff. Personal rank is not used.
    Towns with one gymnasium in the slice are omitted.
    """
    if not 50 <= slice_low < slice_high <= 100:
        raise ValueError("the score slice must sit inside 50 to 100, low before high")
    work = measured.loc[measured["tier"] == settings.top_tiers[0]].copy()
    work["gymnasium"] = work["gymnasium"].astype(str)
    work["town"] = pd.NA
    for county in settings.counties:
        towns = {str(code): town for code, town in _towns_for_county(county).items()}
        mask = work["county"] == county
        work.loc[mask, "town"] = work.loc[mask, "gymnasium"].map(towns)
    named = work["town"].ne("") & work["town"].notna()
    low_q, high_q = slice_low / 100, slice_high / 100
    edges = {}
    for county, scores in work.groupby("county")["exam"]:
        edges[county] = (
            float(scores.quantile(low_q)),
            float(scores.quantile(high_q)),
        )
    work["top_tenth"] = [
        exam >= edges[county][0]
        for county, exam in zip(work["county"], work["exam"])
    ]
    crowding = (work.loc[work["top_tenth"]]
                .groupby(["county", "gymnasium"]).size()
                .rename("top_tenth_applicants"))
    work = work.join(crowding, on=["county", "gymnasium"])
    work["top_tenth_applicants"] = work["top_tenth_applicants"].fillna(0).astype(int)
    in_slice = [
        edges[county][0] <= exam < edges[county][1]
        for county, exam in zip(work["county"], work["exam"])
    ]
    slice_rows = work.loc[named & np.array(in_slice)].copy()
    slice_rows = slice_rows.loc[slice_rows["success"].notna()].copy()
    gym_rows = []
    for (county, town, gymnasium), cell in slice_rows.groupby(
            ["county", "town", "gymnasium"], sort=False):
        placed = cell.loc[cell["ladder_state"] == "placed", "cutoffs_above"]
        gym_rows.append({
            "county": county,
            "town": town,
            "gymnasium": gymnasium,
            "slice_applicants": len(cell),
            "top_tenth_applicants": int(cell["top_tenth_applicants"].iloc[0]),
            "mean_exam": cell["exam"].mean(),
            "top_tier_successes": int(cell["success"].sum()),
            "top_tier_rate": cell["success"].mean(),
            "mean_cutoffs_above": placed.mean() if len(placed) else np.nan,
        })
    gyms = pd.DataFrame(gym_rows)
    if gyms.empty:
        raise ValueError("the score slice has no within-county placements")
    town_sizes = gyms.groupby(["county", "town"])["gymnasium"].nunique()
    multi = town_sizes[town_sizes >= 2].reset_index()[["county", "town"]]
    gyms = gyms.merge(multi, on=["county", "town"], how="inner")
    town_rows = []
    for (county, town), cell in gyms.groupby(["county", "town"], sort=False):
        median_crowd = cell["top_tenth_applicants"].median()
        thin = cell.loc[cell["top_tenth_applicants"] < median_crowd]
        crowded = cell.loc[cell["top_tenth_applicants"] > median_crowd]
        if thin.empty or crowded.empty:
            continue
        thin_n = int(thin["slice_applicants"].sum())
        crowded_n = int(crowded["slice_applicants"].sum())
        thin_rate = np.average(thin["top_tier_rate"], weights=thin["slice_applicants"])
        crowded_rate = np.average(crowded["top_tier_rate"], weights=crowded["slice_applicants"])
        thin_exam = np.average(thin["mean_exam"], weights=thin["slice_applicants"])
        crowded_exam = np.average(crowded["mean_exam"], weights=crowded["slice_applicants"])
        town_rows.append({
            "county": county,
            "town": town,
            "gymnasiums": int(len(cell)),
            "thin_gymnasiums": int(len(thin)),
            "crowded_gymnasiums": int(len(crowded)),
            "thin_top_tenth_applicants": int(thin["top_tenth_applicants"].median()),
            "crowded_top_tenth_applicants": int(crowded["top_tenth_applicants"].median()),
            "thin_slice_applicants": thin_n,
            "crowded_slice_applicants": crowded_n,
            "thin_mean_exam": thin_exam,
            "crowded_mean_exam": crowded_exam,
            "thin_top_tier_rate": thin_rate,
            "crowded_top_tier_rate": crowded_rate,
            "rate_difference_crowded_minus_thin": crowded_rate - thin_rate,
            "slice_low_exam": edges[county][0],
            "slice_high_exam": edges[county][1],
            "enough_students": thin_n >= min_side and crowded_n >= min_side,
        })
    towns = pd.DataFrame(town_rows)
    if towns.empty:
        raise ValueError("no town had both a thinner and a more crowded gymnasium")
    towns.sort_values(["enough_students", "county", "town"],
                      ascending=[False, True, True], inplace=True, kind="stable",
                      ignore_index=True)
    return gyms.sort_values(["county", "town", "top_tenth_applicants"],
                            kind="stable", ignore_index=True), towns


def _plot_within_town(towns, folder):
    kept = towns.loc[towns["enough_students"]].sort_values(
        "rate_difference_crowded_minus_thin", kind="stable")
    if kept.empty:
        return
    labels = [f"{row.town} ({row.county})" for row in kept.itertuples()]
    y = np.arange(len(kept))
    fig, axis = plt.subplots(figsize=(10, max(4, 0.38 * len(kept) + 1.5)))
    axis.hlines(y, 100 * kept["thin_top_tier_rate"], 100 * kept["crowded_top_tier_rate"],
                color="#9aa0a6", linewidth=1)
    axis.scatter(100 * kept["thin_top_tier_rate"], y, color="#356c9b",
                 label="Thinner gymnasiums", zorder=3)
    axis.scatter(100 * kept["crowded_top_tier_rate"], y, color="#a43d4c",
                 label="More crowded gymnasiums", zorder=3)
    axis.set_yticks(y, labels, fontsize=8)
    axis.set_xlabel("Placed in the top filled program (%)")
    axis.set_title("Same town, same narrow score slice\n"
                   "Crowding is the gymnasium's count of county top-tenth applicants")
    axis.grid(axis="x", alpha=.25)
    axis.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(folder / "within_town_top_tier.png", dpi=160)
    plt.close(fig)


def within_town(settings: pilot.Settings | None = None, *, run: bool = False,
                slice_low: int = 90, slice_high: int = 95, min_side: int = 15):
    """Build the within-town comparison only after the caller sets run=True."""
    if settings is None:
        settings = pilot.Settings(counties=PLOTTED_COUNTIES, ai_percentile_cuts=(90, 80, 50))
    settings.validate()
    if not run:
        print("Analysis is off. Call within_town(settings, run=True) to compare "
              "gymnasiums in the same town.", flush=True)
        return None
    print("Building the placement rows used by the existing plots...", flush=True)
    frame, _chosen, _overview = pilot._source_frames(settings)
    measured = _attach(frame, settings)
    gyms, towns = _within_town_tables(
        measured, settings, slice_low=slice_low, slice_high=slice_high, min_side=min_side)
    stamp = datetime.now().astimezone().strftime("run_%Y%m%dT%H%M%S%z")
    folder = WITHIN_TOWN_OUTPUTS / stamp
    folder.mkdir(parents=True, exist_ok=False)
    gyms.to_csv(folder / "within_town_gymnasiums.csv", index=False)
    towns.to_csv(folder / "within_town_contrasts.csv", index=False)
    _plot_within_town(towns, folder)
    kept = towns.loc[towns["enough_students"]]
    if kept.empty:
        equal_town = np.nan
        weighted = np.nan
    else:
        equal_town = float(kept["rate_difference_crowded_minus_thin"].mean())
        weighted = float(np.average(
            kept["crowded_top_tier_rate"], weights=kept["crowded_slice_applicants"])
            - np.average(kept["thin_top_tier_rate"], weights=kept["thin_slice_applicants"]))
    (folder / "run_manifest.json").write_text(json.dumps({
        "run_at_local": stamp,
        "counties": list(settings.counties),
        "top_tier": settings.top_tiers[0],
        "math_cs_only": settings.math_cs_only,
        "slice": f"county exam percentile {slice_low} inclusive to {slice_high} exclusive",
        "crowding": "gymnasium count of applicants at or above the county top-tenth cutoff",
        "town_rule": "locality printed at the end of the gymnasium name; Bucharest is one market; one-gymnasium towns omitted",
        "min_side": min_side,
        "towns_compared": int(len(towns)),
        "towns_with_enough_students": int(len(kept)),
        "equal_town_mean_rate_difference": equal_town,
        "applicant_weighted_rate_difference": weighted,
        "privacy": "aggregate output only; gymnasium codes, not applicant names",
    }, indent=2) + "\n")
    print(f"Towns with both sides: {len(towns)}. "
          f"Towns with at least {min_side} students on each side: {len(kept)}.", flush=True)
    if len(kept):
        print(f"Equal-town mean rate difference (crowded minus thin): {equal_town:+.3f}", flush=True)
        print(f"Applicant-weighted rate difference (crowded minus thin): {weighted:+.3f}", flush=True)
        show = kept[[
            "county", "town", "thin_slice_applicants", "crowded_slice_applicants",
            "thin_top_tenth_applicants", "crowded_top_tenth_applicants",
            "thin_mean_exam", "crowded_mean_exam",
            "thin_top_tier_rate", "crowded_top_tier_rate",
            "rate_difference_crowded_minus_thin",
        ]]
        print(show.to_string(index=False, float_format=lambda value: f"{value:.3f}"), flush=True)
    print(f"Saved {folder}", flush=True)
    return folder


if __name__ == "__main__":
    run(run=False)
