"""Read-only county progress inventory. No acquisition imports, network or source writes.

Counts describe saved checkpoints and recorded audits, not fresh verification of
student links or eligibility for analysis. Only county aggregates are returned.
"""
from pathlib import Path
from datetime import datetime
import csv
import json
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FAMILIES = {
    "school_results": "School results (admitted + rejected, including directory)",
    "resident_candidates": "County resident applicant list",
    "incoming_candidates": "Applicants from other counties",
    "incoming_admitted": "Admitted applicants from other counties",
    "incoming_rejected": "Rejected applicants from other counties",
}
BASE_FAMILIES = {
    "origin_school_directory": "Origin school directory",
    "candidate_roster": "Original general applicant list",
    "admitted_placements": "Original county admitted list",
    "unassigned_applicants": "Original county unassigned list",
    "program_directory": "Program directory",
    "program_occupancy": "Program occupancy totals",
}


def stamp(epoch):
    return datetime.fromtimestamp(epoch).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z") if epoch else "Not recorded"


def integer(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def load_json(path, warnings, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {} if default is None else default
    except (OSError, ValueError):
        warnings.append(f"Could not read {path.name}; it may be changing. Rerun the refresh cell.")
        return {} if default is None else default


def file_stats(folder, pattern="*.json"):
    # Stat only: never print or export source rows, names or scores.
    files = {}
    for p in folder.glob(pattern):
        try:
            s = p.stat()
            files[p] = (s.st_size, s.st_mtime)
        except FileNotFoundError:
            pass  # A worker may have just atomically replaced a checkpoint.
    return files


def records(path, warnings):
    try:
        with path.open(encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []
    except (OSError, csv.Error, UnicodeError):
        warnings.append(f"Could not read {path.name}; rerun after its writer finishes.")
        return []


def saved_audits(outputs, warnings):
    # Keep different questions separate. The newest file for a county/question wins.
    patterns = {
        "School applicants linked to outcomes": "full_gymnasium_reconciliation.csv",
        "Applicants compared with school results": "source_reconciliation.csv",
        "New source views compared": "county_source_counts.csv",
        "Placement labels checked for plots": "plot_source_gate_counts.csv",
        "Original county source inventory": "EDUCATION_20261001_county_source_readiness.csv",
    }
    latest = {}
    for kind, filename in patterns.items():
        for p in outputs.rglob(filename):
            modified = p.stat().st_mtime
            for row in records(p, warnings):
                county = row.get("county")
                if not county:
                    continue
                key = (county, kind)
                if key not in latest or modified > latest[key][0]:
                    latest[key] = (modified, p, row)
    return latest


def describe_audit(kind, row):
    def n(key):
        return row.get(key, "not recorded")
    if kind == "Placement labels checked for plots":
        return (f"{n('matched_result_rows')}/{n('applicant_rows')} applicant rows matched; "
                f"{n('ambiguous_or_missing_result_rows')} ambiguous/missing results; "
                f"{n('top1_label_unresolved')} top-one labels unresolved; "
                f"{n('top2_label_unresolved')} top-two labels unresolved; "
                f"occupancy difference {n('occupancy_difference')}")
    if kind == "Applicants compared with school results":
        return (f"{n('same_school_name_score_matches')} same-school name/score matches; "
                f"{n('applicant_rows_absent_from_school_results')} applicant rows absent from results; "
                f"{n('result_rows_absent_from_score_pages')} result rows absent from score pages")
    if kind == "New source views compared":
        return (f"{n('school_result_pages')}/{n('school_result_directory_schools')} school reports; "
                f"{n('resident_rows_absent_from_school_results')} resident rows absent from school results; "
                f"{n('incoming_candidate_rows_without_outcome')} incoming applicants without an outcome")
    if kind == "School applicants linked to outcomes":
        return (f"{n('verified_gymnasium_pages')}/{n('directory_gymnasiums')} school pages checked; "
                f"{n('outcome_not_found_in_saved_reports')} outcomes not found; "
                f"{n('outcome_name_score_ambiguous')} ambiguous name/score outcomes")
    return (f"County applicant list complete: {n('candidate_pages_complete')}; "
            f"{n('candidate_without_unique_local_outcome')} without a unique local outcome. "
            "This early inventory does not include all later school-result recovery.")


def collect_progress(private_root=None, outputs=None):
    private_root = Path(private_root or Path.home()/"Desktop/VECTOR_temp").expanduser()
    outputs = Path(outputs or ROOT/"outputs").expanduser()
    cache = private_root/"romania_2001_national_main_allocation_v1"
    new = private_root/"romania_2001_school_results_incoming_v1"
    warnings = []
    directory = load_json(cache/"county_directory.json", warnings).get("counties", [])
    if not directory:
        raise FileNotFoundError(f"County inventory missing or unreadable: {cache/'county_directory.json'}")
    state_path = new/"status.json"
    state = load_json(state_path, warnings).get("counties", {})
    state_time = state_path.stat().st_mtime if state_path.exists() else 0
    placement_path = outputs/"romania_2001_national_source_recovery/placement_county_status.csv"
    placements = {r['county']: r for r in records(placement_path, warnings)}
    placement_time = placement_path.stat().st_mtime if placement_path.exists() else 0
    audits = saved_audits(outputs, warnings)
    gym_files = file_stats(private_root/"romania_2001_four_county_school_source_pilot/school_reports")
    overview, sources, audit_rows = [], [], []
    for county_info in directory:
        c, name = county_info['county_code'], county_info['county_name']
        manifest_path = cache/"county_manifests"/f"{c}.json"
        manifest = load_json(manifest_path, warnings)
        mf = manifest.get('families', {})
        county_files = file_stats(cache/"pages"/c, "**/*.json")
        county_files.update(file_stats(cache/"alternate_report_pilot"/c, "destination_program_*.html"))
        local_gym = {p: v for p, v in gym_files.items() if p.name.startswith(c+'_')}
        if c == 'AB':
            local_gym.update(file_stats(private_root/"romania_alba_2001_differentiation_v1/school_reports", 'school_*.json'))
        county_files.update(local_gym)
        expected_gyms = mf.get('origin_school_directory', {}).get('row_count')
        base_complete = 0
        for family, label in BASE_FAMILIES.items():
            f = mf.get(family, {})
            listed = f.get('pages', [])
            existing = sum((cache/p['file']).exists() for p in listed)
            complete = bool(f.get('complete')) and existing == len(listed) and bool(listed)
            base_complete += complete
            sources.append({'County': c, 'Source': label,
                'Saved pages': existing, 'Expected / known pages': len(listed)+len(f.get('unresolved', [])) if f else None,
                'Scope of target': 'Manifest-listed pages + unresolved URLs; not a guaranteed total',
                'Unresolved URLs': len(f.get('unresolved', [])) if f else None,
                'Recorded source rows': f.get('row_count'),
                'Progress': 'Complete in original manifest' if complete else ('Still open in original manifest' if f else 'Not inventoried'),
                'Record last saved': manifest.get('saved_utc', 'Not recorded')})
        family_summaries = {}
        incoming_covered = 0
        for family, label in FAMILIES.items():
            f = state.get(c, {}).get(family, {})
            files = file_stats(new/'pages'/c/family)
            county_files.update(files)
            known = len(f.get('discovered', []))
            saved = integer(f.get('saved_pages'))
            projected = f.get('projected_pages')
            target = max(known, integer(projected)) if known or projected is not None else None
            unresolved = len(f.get('unresolved', {}))
            # No complete claim from a fraction alone; projections can be lower bounds.
            covered = bool(f) and target is not None and saved >= target and saved > 0 and unresolved == 0 and len(files) == saved
            progress = ('All known pages saved' if covered else 'Pending pages or unresolved URLs') if f else 'Not yet inventoried'
            if f and len(files) != saved:
                progress = 'Checkpoint count changed; status needs refresh'
            if family.startswith('incoming_'):
                incoming_covered += covered
            sources.append({'County': c, 'Source': label, 'Saved pages': len(files),
                'Expected / known pages': target, 'Scope of target': f.get('projection_basis', 'Known links only; full total not established'),
                'Unresolved URLs': unresolved if f else None,
                'Recorded source rows': f.get('saved_rows'), 'Progress': progress,
                'Record last saved': stamp(state_time) if f else 'Not recorded'})
            fraction = f"{len(files)}/{target if target is not None else '?'}"
            family_summaries[family] = (fraction, covered, unresolved, bool(f))
        newest_download = max((v[1] for v in county_files.values()), default=0)
        meaningful = []
        for (ac, kind), (modified, path, row) in audits.items():
            if ac != c:
                continue
            outdated = newest_download > modified
            audit_rows.append({'County': c, 'Check': kind, 'Recorded finding': describe_audit(kind, row),
                'Report file last saved': stamp(modified),
                'Downloads newer than report': 'Yes — review or rerun that audit' if outdated else 'No newer tracked download found; not a fresh audit',
                'Report file': str(path)})
            if kind != 'Original county source inventory':
                meaningful.append((modified, kind, outdated))
        if meaningful:
            modified, kind, outdated = max(meaningful)
            reconciliation = 'Saved checks; newer downloads need review' if outdated else 'Saved checks available (see details)'
            audit_date = stamp(modified)
        else:
            reconciliation = 'No later school/result reconciliation found'
            audit_date = 'Not recorded'
        placement = placements.get(c, {})
        program_text = (f"{placement.get('verified_programs','?')}/{placement.get('target_programs','?')}" if placement else 'No recovery record')
        result_fraction, results_covered, result_errors, results_started = family_summaries['school_results']
        if not results_started:
            action = 'Inventory and acquire school-result pages.'
        elif not results_covered:
            action = 'Finish or retry school-result pages; keep unresolved items open.'
        elif incoming_covered < 3:
            action = 'Finish or inventory the three incoming-student lists.'
        elif not meaningful:
            action = 'School results saved; run offline applicant/outcome reconciliation.'
        elif max(meaningful)[2]:
            action = 'Review downloads added since the saved reconciliation.'
        else:
            action = 'Read saved check details and remaining ambiguities before expanding analysis.'
        overview.append({'County': c, 'County name': name,
            'School applicant pages saved / listed schools': f"{len(local_gym)}/{expected_gyms if expected_gyms is not None else '?'}",
            'School result pages saved / target': result_fraction,
            'School result URLs unresolved': result_errors if results_started else None,
            'Incoming lists with all known pages saved': f'{incoming_covered}/3',
            'Resident list pages saved / target': family_summaries['resident_candidates'][0],
            'Original report families complete': f'{base_complete}/{len(BASE_FAMILIES)}',
            'Program recovery reports verified / target': program_text,
            'Placement recovery recorded state': placement.get('state', 'No recovery record'),
            'Placement recovery record saved': stamp(placement_time) if placement else 'Not recorded',
            'Reconciliation': reconciliation, 'Latest school/result audit saved': audit_date,
            'Last tracked source file saved': stamp(newest_download),
            'Tracked source files MB': round(sum(v[0] for v in county_files.values())/1_000_000, 1),
            'Next step': action})
    return {'counties': pd.DataFrame(overview), 'sources': pd.DataFrame(sources),
            'audits': pd.DataFrame(audit_rows), 'warnings': warnings,
            'refreshed': stamp(datetime.now().timestamp()), 'private_root': str(private_root)}


def show_progress(result, counties=None):
    from IPython.display import display, Markdown, HTML
    selected = {c.upper() for c in counties} if counties else set(result['counties']['County'])
    df = result['counties'][result['counties']['County'].isin(selected)].copy()
    display(Markdown(f"### Romania progress — {result['refreshed']}\n"
                     f"**{len(df)} county reporting units shown.** Read-only snapshot; no internet requests."))
    # A scrollable table keeps every county visible without pandas truncating rows.
    primary = ['County', 'County name', 'School applicant pages saved / listed schools',
               'School result pages saved / target', 'School result URLs unresolved',
               'Incoming lists with all known pages saved', 'Resident list pages saved / target',
               'Reconciliation', 'Next step']
    display(HTML('<div style="overflow:auto;max-height:850px">'+df[primary].to_html(index=False, na_rep='Unknown', escape=True)+'</div>'))
    display(Markdown("**How to read it:** A fraction is saved pages / known or projected target. "
        "School-result pages include the directory itself. Targets can grow as links are discovered. "
        "Incoming lists means applicants, admitted, and rejected from other counties. "
        "All known pages saved does not prove every historical applicant is represented. "
        "Reconciliation findings are from saved reports, not newly rerun checks. "
        "The detailed tables below separate the original county lists, recovered program reports, and school results."))
    for message in result['warnings']:
        display(Markdown('**Read warning:** '+message))
    return df


def show_details(result, county='B'):
    from IPython.display import display, Markdown, HTML
    county = county.upper()
    if county not in set(result['counties']['County']):
        raise ValueError(f'Unknown county code: {county}')
    display(Markdown(f'### {county} — source and reconciliation details'))
    for label, key in [('County summary', 'counties'), ('Download families', 'sources'), ('Recorded reconciliation checks', 'audits')]:
        df = result[key]
        display(Markdown('**'+label+'**'))
        if df.empty or not (df['County'] == county).any():
            display(Markdown('No saved record found. This is unresolved, not a failed county.'))
            continue
        data = df.loc[df['County'] == county]
        if key == 'counties':
            data = data.set_index('County').T.reset_index().rename(columns={'index': 'Item', county: 'Value'})
        display(HTML('<div style="overflow:auto">'+data.to_html(index=False, na_rep='Unknown', escape=True)+'</div>'))


def save_snapshot(result, folder):
    """Optional new aggregate files only; never alter worker or audit checkpoints."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    tag = datetime.now().astimezone().strftime('%Y%m%dT%H%M%S%f%z')
    paths = []
    for key in ('counties', 'sources', 'audits'):
        p = folder/f'{tag}_{key}.csv'
        result[key].to_csv(p, index=False)
        paths.append(p)
    return paths
