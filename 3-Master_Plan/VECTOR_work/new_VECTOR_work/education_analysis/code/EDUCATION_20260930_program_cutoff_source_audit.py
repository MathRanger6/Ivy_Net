"""Parse saved public program tables; no student data or HERO calculation.

The directory and occupancy table come from the same Alba 2001 main-allocation
report family. Join on their literal specialization codes, including the source's
`x` prefixes. Preserve language and attendance form rather than merging programs
that merely share a school and specialization name.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / 'outputs/romania_alba_2001_program_cutoffs_20260930'


def table_rows(path):
    soup = BeautifulSoup(path.read_bytes().decode('cp1250'), 'html.parser')
    table = next(t for t in soup.find_all('table') if t.find('th'))
    headings = [h.get_text(' ', strip=True) for h in table.find_all('th')]
    rows = []
    for tr in table.find_all('tr'):
        cells = [td.get_text(' ', strip=True) for td in tr.find_all('td', recursive=False)]
        if len(cells) == len(headings) and cells[0].isdigit():
            rows.append(dict(zip(headings, cells)))
    return rows


def main(source_dir):
    programs = table_rows(source_dir / 'programs.html')
    occupancy = table_rows(source_dir / 'occupancy.html')
    directory = {r['Cod specializare']: r for r in programs}
    assert len(directory) == len(programs) == len(occupancy) == 85
    assert {r['Liceu'].split(' ', 1)[0] for r in occupancy} == set(directory)
    combined = []
    for row in occupancy:
        code, description = row['Liceu'].split(' ', 1)
        program = directory[code]
        assert row['Profil'] == program['Profil']
        assert row['Specializare'] == program['Specializare']
        # The occupancy display adds a route suffix to the directory school name.
        # Require the complete directory name, not a fuzzy school-name match.
        assert description.startswith(program['Liceu'] + ' /')
        places = int(row['Nr. de locuri'])
        admitted = int(row['Candidaţi admişi'])
        vacancies = int(row['Nr. de locuri libere'])
        assert places == int(program['Nr. de locuri']) == admitted + vacancies
        low = float(row['Ultima notă'].replace(',', '.'))
        high = float(row['Prima notă'].replace(',', '.'))
        assert (0 < low <= high <= 10) if admitted else (low == high == 0)
        combined.append({
            'program_code': code, 'school_name': program['Liceu'],
            'profile': program['Profil'], 'specialization': program['Specializare'],
            'level': program['Nivel'], 'attendance_form': program['Formă de învăţământ'],
            'language': program['Limbă'], 'places': places, 'admitted': admitted,
            'vacancies': vacancies, 'filled': vacancies == 0,
            # Zero-admission entries have no observed cutoff. Keep their original
            # zero only in the source field, so it cannot become a ranking score.
            'lowest_admitted_score': low if admitted else None,
            'highest_admitted_score': high if admitted else None,
            'source_ultima_nota': row['Ultima notă'],
            'source_occupancy_description': row['Liceu'],
        })
    assert sum(r['admitted'] for r in combined) == 2977
    # This is a source ordering only: no top-program success threshold, outcome
    # label, eligibility filter, or HERO denominator is chosen here.
    combined.sort(key=lambda r: (r['specialization'],
                                 -(r['lowest_admitted_score'] or -1), r['program_code']))
    summary = {
        'cohort': 2001, 'county': 'Alba', 'report_family': 'main allocation; not rep2',
        'programs': len(combined), 'places': sum(r['places'] for r in combined),
        'admitted': sum(r['admitted'] for r in combined),
        'vacancies': sum(r['vacancies'] for r in combined),
        'filled_programs': sum(r['filled'] for r in combined),
        'partially_filled_programs': sum(0 < r['admitted'] < r['places'] for r in combined),
        'empty_programs': sum(r['admitted'] == 0 for r in combined),
        'specialization_counts': dict(collections.Counter(r['specialization'] for r in combined)),
        'level_counts': dict(collections.Counter(r['level'] for r in combined)),
        'language_counts': dict(collections.Counter(r['language'] for r in combined)),
        'attendance_counts': dict(collections.Counter(r['attendance_form'] for r in combined)),
        'highest_cutoff_by_specialization': {},
        'source_metadata': {},
        'checks': '85 unique exact program-code joins; school/profile/specialization/capacity agree; all capacity balances pass; 2977 admitted matches earlier county audit',
        'limit': 'No student placement merge; no outcome threshold; reported last-admitted scores are not preannounced eligibility thresholds or teaching-quality measures.',
    }
    for spec in summary['specialization_counts']:
        group = [r for r in combined if r['specialization'] == spec and r['admitted']]
        maximum = max(r['lowest_admitted_score'] for r in group)
        summary['highest_cutoff_by_specialization'][spec] = [r for r in group if r['lowest_admitted_score'] == maximum]
    OUT.mkdir(parents=True, exist_ok=True)
    for label in ['root', 'map', 'alba_index', 'programs', 'occupancy']:
        path = source_dir / (label + '.html')
        if path.exists():
            raw = path.read_bytes()
            (OUT / path.name).write_bytes(raw)
            meta_path = source_dir / (label + '.json')
            metadata = json.loads(meta_path.read_text()) if meta_path.exists() else {}
            metadata['sha256'] = hashlib.sha256(raw).hexdigest()
            summary['source_metadata'][label] = metadata
    summary['parser_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT / 'program_cutoffs.json').write_text(json.dumps(combined, ensure_ascii=False, indent=2) + '\n')
    (OUT / 'source_audit_summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in summary.items() if k not in ['source_metadata', 'highest_cutoff_by_specialization']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', required=True, type=Path)
    main(parser.parse_args().source_dir)
