"""Audit supplied NELS fields; never rewrite source or fit an outcome model."""
from pathlib import Path
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve()
BASE = HERE.parents[1]
ROOT = HERE.parents[5]
SOURCE = ROOT / 'datasets/nels88/nels88_big_fish_panel.csv'
OUT = BASE / 'outputs/source_audit_20260928'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def compare(actual, expected):
    valid = actual.notna() & expected.notna()
    delta = (actual[valid].astype(float) - expected[valid].astype(float)).abs()
    return {'comparable': int(valid.sum()), 'mismatches_1e_7': int((delta > 1e-7).sum()),
            'mismatches_1e_5': int((delta > 1e-5).sum()),
            'max_absolute_error': float(delta.max()) if len(delta) else None,
            'missingness_disagreements': int((actual.isna() != expected.isna()).sum())}

def main():
    print('Reading supplied NELS panel; source remains read-only.', flush=True)
    before = sha(SOURCE)
    d = pd.read_csv(SOURCE)
    OUT.mkdir(parents=True, exist_ok=True)
    outcomes = ['high_school_diploma_by_2000', 'any_postsecondary_by_2000',
                'associate_or_higher_by_2000', 'bachelors_or_higher_by_2000']
    result = {'source': str(SOURCE.relative_to(ROOT)), 'source_sha256': before,
              'rows': len(d), 'columns': len(d.columns),
              'duplicate_student_ids': int(d.student_id.duplicated().sum()),
              'missing_student_ids': int(d.student_id.isna().sum()),
              'schools': int(d.school_id.nunique()), 'checks': {}, 'samples': {}}
    print('Checking outcome recodes and school-peer identities.', flush=True)
    for code in ['degree_code_2000', 'hs_completion_code_2000']:
        cols = [code, *outcomes, 'outcome_observed']
        d.groupby(cols, dropna=False).size().rename('n').reset_index().to_csv(OUT / (code + '_crosswalk.csv'), index=False)
    sizes = d.groupby('school_id').own_performance_raw.transform('count')
    sums = d.groupby('school_id').own_performance_raw.transform('sum')
    zsum = d.groupby('school_id').own_performance_z.transform('sum')
    for label, actual, expected in [
        ('unit_n_from_recorded_school', d.unit_n, sizes),
        ('peer_n_from_recorded_school', d.peer_n, sizes - 1),
        ('raw_peer_mean', d.peer_mean_loo, (sums-d.own_performance_raw)/(sizes-1)),
        ('z_peer_mean', d.peer_mean_z_loo, (zsum-d.own_performance_z)/(sizes-1)),
        ('raw_relative_performance', d.relative_performance_raw, d.own_performance_raw-d.peer_mean_loo),
        ('outcome_observed_from_ba', d.outcome_observed, d.bachelors_or_higher_by_2000.notna().astype(int)),
    ]:
        result['checks'][label] = compare(actual, expected)
    for floor in [5, 10, 15]:
        result['checks'][f'cell_at_least_{floor}_unit_n'] = compare(d[f'cell_at_least_{floor}'], (d.unit_n >= floor).astype(int))
    for floor in [5, 10]:
        expected = ((d.unit_n >= floor) & d.own_performance_raw.notna() & d.peer_mean_loo.notna() & d.outcome_observed.eq(1)).astype(int)
        result['checks'][f'analytic_min{floor}_candidate_recipe'] = compare(d[f'analytic_sample_min{floor}'], expected)
    for low, high in zip(outcomes, outcomes[1:]):
        result['checks'][f'{high}_without_{low}'] = int((d[high].eq(1) & d[low].eq(0)).sum())
    result['checks']['min10_students_with_exactly_nine_peers'] = int((d.analytic_sample_min10.eq(1) & d.peer_n.eq(9)).sum())
    # Stored rank definitions are checked without changing the supplied fields.
    g = d.groupby('school_id').own_performance_raw
    above = sizes - g.rank(method='max')
    equal = g.transform(lambda x: x.map(x.value_counts())) - 1
    for label, actual, expected in [
        ('n_peers_above', d.n_peers_above, above),
        ('n_peers_equal', d.n_peers_equal, equal),
        ('share_peers_above', d.share_peers_above, above/(sizes-1)),
        ('percentile_midrank_candidate', d.within_unit_percentile_loo, ((sizes-1)-above-0.5*equal)/(sizes-1))
    ]:
        result['checks'][label] = compare(actual, expected)
    for name, sub in [('all', d), ('analytic_min10', d[d.analytic_sample_min10.eq(1)])]:
        w = sub.followup_weight_2000
        stats = {'n': len(sub), 'schools': int(sub.school_id.nunique()),
                 'weight_missing': int(w.isna().sum()), 'weight_nonpositive': int(w.le(0).sum()),
                 'weight_positive_range': [float(w[w.gt(0)].min()), float(w[w.gt(0)].max())],
                 'own_z_mean': float(sub.own_performance_z.mean()),
                 'own_z_sd_population': float(sub.own_performance_z.std(ddof=0)),
                 'raw_mean': float(sub.own_performance_raw.mean()),
                 'raw_sd_population': float(sub.own_performance_raw.std(ddof=0)),
                 'ses_range': [float(sub.base_year_ses.min()), float(sub.base_year_ses.max())],
                 'race_codes': {str(k): int(v) for k,v in sub.race_code.value_counts(dropna=False).items()},
                 'sex_codes': {str(k): int(v) for k,v in sub.sex_code.value_counts(dropna=False).items()},
                 'missing_by_field': sub.isna().sum().astype(int).to_dict(),
                 'degree_codes': {str(k): int(v) for k,v in sub.degree_code_2000.value_counts(dropna=False).items()},
                 'outcomes': {c: {'observed': int(sub[c].notna().sum()), 'positive': int(sub[c].eq(1).sum()), 'unweighted_mean': float(sub[c].mean())} for c in outcomes}}
        e = sub.any_postsecondary_by_2000.eq(1)
        stats['ba_among_recorded_entrants'] = float(sub.loc[e, 'bachelors_or_higher_by_2000'].mean())
        result['samples'][name] = stats
    valid = d[['own_performance_raw', 'own_performance_z']].dropna()
    slope, intercept = np.polyfit(valid.own_performance_raw, valid.own_performance_z, 1)
    result['standardization'] = {'slope': float(slope), 'intercept': float(intercept),
        'implied_reference_mean': float(-intercept/slope), 'implied_reference_sd': float(1/slope),
        'max_residual': float(np.max(np.abs(valid.own_performance_z-(slope*valid.own_performance_raw+intercept))))}
    for c in ['base_reading_std_score', 'base_history_std_score']:
        result['checks']['raw_equals_'+c] = compare(d.own_performance_raw, d[c])
    result['checks']['raw_equals_reading_history_average'] = compare(d.own_performance_raw, (d.base_reading_std_score+d.base_history_std_score)/2)
    result['source_unchanged'] = sha(SOURCE) == before
    assert result['source_unchanged']
    result['run'] = {'utc': datetime.now(timezone.utc).isoformat(), 'python': sys.executable,
                     'version': platform.python_version(), 'pandas': pd.__version__, 'numpy': np.__version__,
                     'script_sha256': sha(HERE), 'kind': 'internal audit; no substantive models'}
    (OUT/'audit_summary.json').write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ['rows','schools','checks','standardization','source_unchanged']}, indent=2), flush=True)
    print('Audit complete. Outputs: '+str(OUT), flush=True)

if __name__ == '__main__':
    main()
