"""Bounded HS&B construction audit to prepare a combined source query."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys
import numpy as np
import pandas as pd

SCRIPT = Path(__file__).resolve()
BASE = SCRIPT.parents[1]
ROOT = SCRIPT.parents[5]
SOURCE = ROOT / 'datasets/hsb80/hsb80_big_fish_panel.csv'
OUT = BASE / 'outputs/hsb_source_audit_20260928'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check(a, b):
    ok = a.notna() & b.notna()
    delta = (a[ok].astype(float)-b[ok].astype(float)).abs()
    return {'comparable': int(ok.sum()), 'missingness_disagreements': int((a.isna()!=b.isna()).sum()),
            'differences_over_1e_5': int((delta>1e-5).sum()),
            'max_absolute_difference': float(delta.max()) if len(delta) else None}

def main():
    before = sha(SOURCE)
    d = pd.read_csv(SOURCE)
    OUT.mkdir(parents=True, exist_ok=True)
    outcomes = ['high_school_or_higher_by_1986', 'any_postsecondary_by_1986',
                'two_year_or_higher_by_1986', 'bachelors_or_higher_by_1986']
    result = {'rows': len(d), 'columns': len(d.columns), 'source': str(SOURCE.relative_to(ROOT)),
              'source_sha256': before, 'cohorts': {}}
    for cohort, s in d.groupby('cohort'):
        print('Auditing '+cohort+': '+str(len(s))+' rows.', flush=True)
        g = s.groupby('school_id').own_performance_raw
        n, total = g.transform('count'), g.transform('sum')
        ztotal = s.groupby('school_id').own_performance_z.transform('sum')
        checks = {}
        for name,a,b in [
            ('school_size',s.unit_n,n), ('peer_count',s.peer_n,n-1),
            ('peer_mean',s.peer_mean_loo,(total-s.own_performance_raw)/(n-1)),
            ('peer_z_mean',s.peer_mean_z_loo,(ztotal-s.own_performance_z)/(n-1)),
            ('rank',s.within_unit_percentile_loo,(g.rank(method='average')-1)/(n-1)),
            ('outcome_observed',s.outcome_observed,s.bachelors_or_higher_by_1986.notna().astype(int)),
            ('weighted_flag',s.analytic_sample_min5_weighted,(s.analytic_sample_min5.eq(1)&s.followup_weight_1986.gt(0)).astype(int))
        ]:
            checks[name]=check(a,b)
        for floor in [5,10]:
            expected=(s.unit_n.ge(floor)&s.own_performance_raw.notna()&s.peer_mean_loo.notna()&s.outcome_observed.eq(1)).astype(int)
            checks['min'+str(floor)+'_candidate_recipe']=check(s['analytic_sample_min'+str(floor)],expected)
        work=s[s.analytic_sample_min5.eq(1)]
        v=s[['own_performance_raw','own_performance_z']].dropna()
        slope,intercept=np.polyfit(v.own_performance_raw,v.own_performance_z,1)
        r={'rows':len(s),'schools':int(s.school_id.nunique()),
           'duplicate_student_ids':int(s.student_id.duplicated().sum()),'missing_student_ids':int(s.student_id.isna().sum()),
           'analytic_rows':len(work),'analytic_schools':int(work.school_id.nunique()),
           'analytic_nonpositive_weights':int(work.followup_weight_1986.le(0).sum()),
           'analytic_missing_weights':int(work.followup_weight_1986.isna().sum()),
           'weighted_flag_rows':int(s.analytic_sample_min5_weighted.eq(1).sum()),
           'checks':checks,
           'standardization':{'implied_mean':float(-intercept/slope),'implied_sd':float(1/slope),
               'max_residual':float((v.own_performance_z-(slope*v.own_performance_raw+intercept)).abs().max())},
           'ba_without_entry':int((s.bachelors_or_higher_by_1986.eq(1)&s.any_postsecondary_by_1986.eq(0)).sum()),
           'analytic_outcomes':{c:{'n_observed':int(work[c].notna().sum()),'n_positive':int(work[c].eq(1).sum())} for c in outcomes},
           'analytic_missing_by_column':work.isna().sum().astype(int).to_dict(),
           'analytic_code_counts':{c:{str(k):int(v) for k,v in work[c].value_counts(dropna=False).items()} for c in ['attainment_code_1986','sex_code','race_code','questionnaire_respondent']}}
        result['cohorts'][cohort]=r
        s.groupby(['attainment_code_1986',*outcomes,'outcome_observed'],dropna=False).size().rename('n').reset_index().to_csv(OUT/(cohort.lower()+'_outcome_crosswalk.csv'),index=False)
    result['source_unchanged']=sha(SOURCE)==before
    assert result['source_unchanged']
    result['run']={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.executable,'pandas':pd.__version__,
                   'numpy':np.__version__,'script_sha256':sha(SCRIPT),'scope':'internal checks only; no model fits'}
    (OUT/'audit_summary.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    for name,r in result['cohorts'].items():
        print(name,json.dumps({k:v for k,v in r.items() if k not in ['analytic_missing_by_column','analytic_code_counts','analytic_outcomes']}),flush=True)
    print('Done; source fingerprint unchanged.',flush=True)

if __name__=='__main__':
    main()
