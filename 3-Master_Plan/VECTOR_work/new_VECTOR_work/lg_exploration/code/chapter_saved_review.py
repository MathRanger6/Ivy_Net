"""Read-only audit of historical assignments and reproducible chapter figures.

This module never generates assignments. It writes derived products to a new
review directory and leaves the source checkpoints and working notebook intact.
"""
from pathlib import Path
from types import SimpleNamespace
import csv
import hashlib
import json
import numpy as np
import matplotlib.pyplot as plt
from lg_composition.experiment import PROJECT_ROOT, draw_inputs

RUN = 'composition-96667ec378b7-d39e35e837ee'
RHOS = (0., .5, 1., 2., 4.)
RULES = {'one': 'team_opportunities', 'seats': 'seat_opportunities'}


def measures(a, ids, j):
    sizes = np.bincount(ids, minlength=j)
    means = np.bincount(ids, weights=a, minlength=j) / sizes
    variances = np.bincount(ids, weights=(a-means[ids])**2, minlength=j)/sizes
    h = np.sum(sizes*(means-a.mean())**2)/np.sum((a-a.mean())**2)
    ranked = np.argsort(means, kind='stable')
    mixes = []
    for lo, hi in zip(ranked[:-1], ranked[1:]):
        x, y = a[ids == lo], np.sort(a[ids == hi])
        left, right = np.searchsorted(y, x, 'left'), np.searchsorted(y, x, 'right')
        mixes.append(np.mean((left+right)/(2*len(y))))
    return sizes, means, variances, float(h), float(np.mean(mixes))


def review(project_root=PROJECT_ROOT):
    root = Path(project_root)
    out = root/'results/chapter_saved_review_20261111'
    out.mkdir(parents=True, exist_ok=True)
    records, ranked_means, checkpoints, sources = [], {}, {}, []
    population = np.random.default_rng(6102026).normal(size=2000)
    settings = SimpleNamespace(n_players=2000, assignment_seed=6102027)
    expected = {(rho, rep) for rho in RHOS for rep in range(100)}
    for label, rule in RULES.items():
        path = root/f'results/composition_scenarios/{label}_J100_r20_reps100'/RUN
        meta = json.loads((path/'run_metadata.json').read_text())
        assert meta['status'] == 'complete' and meta['selected_rule'] == rule
        summary = {(float(x['rho']), int(x['repetition'])): x
                   for x in csv.DictReader((path/'division_summary.csv').open())}
        assert set(summary) == expected
        seen = set()
        for file in sorted((path/'divisions').glob('*.npz')):
            with np.load(file, allow_pickle=False) as z:
                rho, rep = float(z['rho']), int(z['repetition'])
                key = rho, rep
                assert key in expected and key not in seen
                seen.add(key)
                a, ids = z['ability'], z['team_id']
                assert str(z['rule']) == rule and str(z['run_id']) == RUN
                assert str(z['source_sha256']) == meta['source_sha256']
                assert ids.shape == (2000,) and np.issubdtype(ids.dtype, np.integer)
                assert ids.min() >= 0 and ids.max() < 100
                np.testing.assert_array_equal(z['player_id'], np.arange(2000))
                np.testing.assert_array_equal(a, population)
                np.testing.assert_array_equal(z['original_draws'], population)
                np.testing.assert_array_equal(z['capacities'], np.full(100,20))
                np.testing.assert_allclose(z['initial_centroid'], a.mean(), rtol=0, atol=1e-14)
                order, u = draw_inputs(settings, rep)
                np.testing.assert_array_equal(z['arrival_order'], order)
                np.testing.assert_array_equal(z['choice_uniforms'], u)
                sizes, means, variances, h, mixing = measures(a, ids, 100)
                np.testing.assert_array_equal(sizes, np.full(100,20))
                np.testing.assert_array_equal(sizes, z['team_sizes'])
                for name, actual in [('team_means',means), ('team_variances',variances),
                                     ('h_sort',h), ('mean_within_variance',variances.mean())]:
                    np.testing.assert_allclose(actual, z[name], rtol=1e-11, atol=1e-12)
                np.testing.assert_allclose(h,float(summary[key]['h_sort']),rtol=1e-11,atol=1e-12)
                records.append(dict(rule=label,rho=rho,repetition=rep,h_sort=h,
                                    adjacent_inversion=mixing,within_variance=float(variances.mean())))
                ranked_means[label,rho,rep] = np.sort(means)
                if rep == 0: checkpoints[label,rho] = ids.copy()
                sources.append(dict(path=str(file.relative_to(root)),sha256=hashlib.sha256(file.read_bytes()).hexdigest()))
        assert seen == expected
        print(f'Verified {label}: {len(seen)} checkpoints, metrics, population and random streams',flush=True)
    with (out/'division_metrics.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    def values(rule,rho,key):
        return np.array([x[key] for x in sorted(records,key=lambda x:x['repetition'])
                         if x['rule']==rule and x['rho']==rho])
    aggregate=[]
    for rho in RHOS:
        row={'rho':rho}
        for rule in RULES:
            for metric in ['h_sort','adjacent_inversion']:
                v=values(rule,rho,metric)
                row[f'{rule}_{metric}']=float(v.mean())
        d=values('seats',rho,'h_sort')-values('one',rho,'h_sort')
        row.update(paired_h_seats_minus_one=float(d.mean()),paired_h_SE=float(d.std(ddof=1)/10))
        aggregate.append(row)
    def save(fig,name):
        stem=f'{name}__N2000_J100_cap20_normal_Abar_rho0-0p5-1-2-4_reps100'
        for ext in ['png','pdf']: fig.savefig(out/f'{stem}.{ext}',dpi=180)
        plt.close(fig)
    colors=plt.cm.viridis_r(np.linspace(.08,.95,5))
    fig,axes=plt.subplots(1,2,figsize=(15,6),layout='constrained')
    for rho,c in zip(RHOS,colors):
        samples=np.array([ranked_means['one',rho,rep] for rep in range(100)])
        m,sd=samples.mean(0),samples.std(0,ddof=1)
        axes[0].plot(np.arange(1,101),m,color=c,label=f'rho={rho:g}')
        axes[0].fill_between(np.arange(1,101),m-sd,m+sd,color=c,alpha=.09)
        ids=checkpoints['one',rho]
        means=np.bincount(ids,weights=population)/20
        residual=population-means[ids]
        axes[1].hist(residual,bins=np.linspace(-4.5,4.5,55),density=True,histtype='step',color=c,label=f'rho={rho:g}')
    axes[0].set(xlabel='Team rank within each assignment',ylabel='Team mean (talent units)',title='Hierarchy emerging from common A-bar starts')
    axes[1].set(xlabel='Player talent minus own team mean',ylabel='Probability density',title='Within-team spread: prespecified repetition 0')
    for ax in axes: ax.legend();ax.grid(alpha=.2)
    fig.suptitle('Capped baseline: one opportunity per nonfull team | N=2,000; J=100; cap=20\nRanked curves: 100-assignment means; shading: ±1 assignment SD; one fixed normal population',fontsize=12)
    save(fig,'baseline_hierarchy')
    fig,axes=plt.subplots(1,3,figsize=(16,6),layout='constrained')
    for rule,c in [('one','#2166ac'),('seats','#b35806')]:
        for ax,metric,title,ylabel in zip(axes[:2],['h_sort','adjacent_inversion'],['Between-team sorting','Adjacent-team mixing'],['H_sort (between / total variance)','P(lower-mean team player exceeds next team player)']):
            samples=np.array([values(rule,rho,metric) for rho in RHOS])
            m,sd=samples.mean(1),samples.std(1,ddof=1)
            ax.plot(RHOS,m,'o-',color=c,label=rule)
            ax.fill_between(RHOS,m-sd,m+sd,color=c,alpha=.12)
            ax.set(title=title,xlabel='rho',ylabel=ylabel)
    axes[0].axhline(99/1999,color='gray',ls=':',label='Random reference')
    d=np.array([values('seats',rho,'h_sort')-values('one',rho,'h_sort') for rho in RHOS])
    axes[2].errorbar(RHOS,d.mean(1),yerr=1.984*d.std(1,ddof=1)/10,fmt='o-',color='#555555',capsize=4)
    axes[2].axhline(0,color='gray',ls=':')
    axes[2].set(title='Paired sorting difference',xlabel='rho',ylabel='H_sort seats minus one (approx. 95% CI)')
    for ax in axes:ax.grid(alpha=.2)
    for ax in axes[:2]:ax.legend()
    fig.suptitle('One versus remaining-seat opportunities | N=2,000; J=100; cap=20; A-bar starts; mean attractor\n100 paired assignments; one fixed normal population. Shading: ±1 SD; right: conditional mean-difference CI.',fontsize=12)
    save(fig,'opportunity_rules')
    fig,ax=plt.subplots(figsize=(11,5),layout='constrained')
    ax.hist(population,bins=50,density=True,color='#4682b4',edgecolor='white')
    ax.set(title=f'Unique input population: 2,000 normal draws; mean={population.mean():.3f}; SD={population.std():.3f}\nReused across 100 assignments, five rho settings, and both rules',xlabel='A_i (original and assignment units coincide)',ylabel='Probability density')
    save(fig,'input_population')
    inventory=[]
    for path in sorted((root/'results').rglob('run_metadata.json')):
        meta=json.loads(path.read_text());s=meta.get('base_settings',meta.get('scientific_settings',meta.get('settings',{})))
        if s.get('n_players')==2000 and s.get('roster_size') in [10,20,40,80,100]:
            inventory.append(dict(path=str(path.relative_to(root)),status=meta.get('status'),settings=s,selected_rule=meta.get('selected_rule')))
    report=dict(checkpoints_verified=len(sources),checks='Complete grid, labels, IDs, capacity, source declarations, normal population from seed, arrival/choice streams, recomputed sizes/means/variances/H_sort, CSV H_sort',
                limitation='Stored assignments were not replayed through a historical engine; metadata source declarations are not proof of historical execution. No fresh population validation.',
                aggregate=aggregate,roster_candidate_inventory=inventory,source_files=sources,
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/'audit_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(aggregate,indent=2),flush=True)
    print(f'OUTPUT: {out}',flush=True)
    return out


if __name__=='__main__':
    review()
