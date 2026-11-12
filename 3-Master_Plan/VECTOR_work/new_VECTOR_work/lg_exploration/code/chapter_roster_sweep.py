"""Paired fixed-population roster-size experiment; resumable and notebook-led."""
from pathlib import Path
from types import SimpleNamespace
import csv
import hashlib
import json
import numpy as np
import matplotlib.pyplot as plt
from lg_composition.experiment import PROJECT_ROOT, assign, draw_inputs, atomic_npz
from chapter_saved_review import measures, RUN


def run(roster_sizes=(10,20,40,80,100), rhos=(0,.5,1,2,4), repetitions=30,
        population_seed=6102026, assignment_seed=6102027, project_root=PROJECT_ROOT):
    root=Path(project_root)
    roster_sizes=tuple(int(r) for r in roster_sizes)
    rhos=tuple(float(x) for x in rhos)
    if not roster_sizes or any(r<=0 or 2000%r or r>=2000 for r in roster_sizes):
        raise ValueError('Roster sizes must divide 2000 and leave at least two teams')
    if repetitions<2 or not rhos or any(not np.isfinite(x) or x<0 for x in rhos):
        raise ValueError('Use >=2 repetitions and finite nonnegative rho')
    if len(set(roster_sizes))!=len(roster_sizes) or len(set(rhos))!=len(rhos):
        raise ValueError('Use unique roster sizes and rho values')
    kernel=hashlib.sha256((root/'code/lg_composition/experiment.py').read_bytes()).hexdigest()
    spec=dict(n_players=2000,roster_sizes=roster_sizes,rhos=rhos,repetitions=repetitions,
              population_seed=population_seed,assignment_seed=assignment_seed,
              distribution='standard_normal',population_mode='same',initialization='population_mean',
              attractor='actual_member_mean',rule='team_opportunities',kernel_sha256=kernel)
    digest=hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()[:12]
    out=root/'results/chapter_roster_sweep'/digest
    (out/'divisions').mkdir(parents=True,exist_ok=True)
    (out/'specification.json').write_text(json.dumps(spec,indent=2)+'\n')
    a=np.random.default_rng(population_seed).normal(size=2000)
    streams=SimpleNamespace(n_players=2000,assignment_seed=assignment_seed)
    rows=[]; ranked={}; provenance=[]; new=reused=imported=0
    old=root/f'results/composition_scenarios/one_J100_r20_reps100/{RUN}/divisions'
    oldfiles={}
    if population_seed==6102026 and assignment_seed==6102027:
        for f in old.glob('*.npz'):
            with np.load(f,allow_pickle=False) as z: oldfiles[float(z['rho']),int(z['repetition'])]=f
    for r in roster_sizes:
        j=2000//r
        for rep in range(repetitions):
            order,u=draw_inputs(streams,rep)
            for rho in rhos:
                f=out/'divisions'/f'r{r}_rho{rho.hex().replace(".","_")}_rep{rep:03}.npz'
                source=None
                if f.exists():
                    source=f;reused+=1
                elif r==20 and (rho,rep) in oldfiles:
                    source=oldfiles[rho,rep];imported+=1
                if source is not None:
                    with np.load(source,allow_pickle=False) as z:
                        for key,value in [('ability',a),('arrival_order',order),('choice_uniforms',u),('capacities',np.full(j,r))]:
                            np.testing.assert_array_equal(z[key],value)
                        assert float(z['rho'])==rho and int(z['repetition'])==rep
                        assert str(z['rule'])=='team_opportunities'
                        np.testing.assert_allclose(z['initial_centroid'],a.mean(),atol=1e-14)
                        # Old size-20 assignments are reused only under the identical kernel.
                        assert str(z['source_sha256'])==kernel
                        ids=z['team_id'].copy()
                else:
                    ids,centroids=assign(a,j,r,rho,'team_opportunities',order,u)
                    new+=1
                assert ids.shape==a.shape and ids.dtype.kind in 'iu' and ids.min()>=0 and ids.max()<j
                sizes,means,variances,h,mix=measures(a,ids,j)
                np.testing.assert_array_equal(sizes,np.full(j,r))
                if source is None: np.testing.assert_allclose(means,centroids,atol=1e-12)
                if not f.exists():
                    atomic_npz(f,ability=a,original_draws=a,player_id=np.arange(2000),team_id=ids,
                               arrival_order=order,choice_uniforms=u,capacities=np.full(j,r),
                               initial_centroid=a.mean(),rho=rho,repetition=rep,
                               rule='team_opportunities',source_sha256=kernel,
                               imported_from='' if source is None else str(source.relative_to(root)))
                ref=(j-1)/1999
                rows.append(dict(roster_size=r,n_teams=j,rho=rho,repetition=rep,h_sort=h,
                                 random_reference=ref,excess_h=h-ref,adjacent_inversion=mix,
                                 within_variance=float(variances.mean())))
                ranked[r,rho,rep]=np.sort(means)
                provenance.append(dict(path=str(f.relative_to(root)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
        print(f'Completed r={r}, J={j}: {repetitions} repetitions x {len(rhos)} rho',flush=True)
    with (out/'division_metrics.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    colors=plt.cm.viridis_r(np.linspace(.12,.95,len(roster_sizes)))
    title=f'N=2,000; normal population; A-bar starts; mean attractor; one opportunity per nonfull team\n{repetitions} paired assignments per setting; fixed population; shading = ±1 assignment SD'
    suffix=f'N2000_r'+ '-'.join(map(str,roster_sizes))+'_rho'+'-'.join(f'{x:g}' for x in rhos)+f'_reps{repetitions}_{digest}'
    def save(fig,name):
        for ext in ['png','pdf']:fig.savefig(out/f'{name}__{suffix}.{ext}',dpi=170)
        plt.close(fig)
    aggregate=[]
    fig,axes=plt.subplots(2,2,figsize=(15,11),layout='constrained')
    for r,color in zip(roster_sizes,colors):
        for ax,key,heading,ylabel in zip(axes.flat,['h_sort','excess_h','within_variance','adjacent_inversion'],
                ['Overall sorting','Sorting above random reference','Within-team variation','Overlap between adjacent ranked teams'],
                ['H_sort','H_sort minus (J−1)/(N−1)','Mean within-team variance (talent units squared)','P(lower-mean team player exceeds next team player)']):
            v=np.array([[x[key] for x in rows if x['roster_size']==r and x['rho']==rho] for rho in rhos])
            m,sd=v.mean(1),v.std(1,ddof=1)
            ax.plot(rhos,m,'o-',color=color,label=f'r={r}; J={2000//r}')
            ax.fill_between(rhos,m-sd,m+sd,color=color,alpha=.1)
            ax.set(title=heading,xlabel='rho',ylabel=ylabel);ax.grid(alpha=.2)
        axes[0,0].axhline((2000//r-1)/1999,color=color,ls=':',alpha=.5)
        for rho in rhos:
            selected=[x for x in rows if x['roster_size']==r and x['rho']==rho]
            aggregate.append(dict(roster_size=r,n_teams=2000//r,rho=rho,
                **{k:float(np.mean([x[k] for x in selected])) for k in ['h_sort','excess_h','within_variance','adjacent_inversion']}))
    axes[0,0].legend(fontsize=9)
    axes[0,0].set_title('Overall sorting; dotted lines = random references')
    axes[1,1].set_title('Adjacent-team overlap (rank spacing changes with J)')
    fig.suptitle(title,fontsize=12);save(fig,'roster_size_comparison')
    fig,axes=plt.subplots(1,len(rhos),figsize=(4*len(rhos),5.5),squeeze=False,layout='constrained')
    for ax,rho in zip(axes[0],rhos):
        for r,color in zip(roster_sizes,colors):
            v=np.array([ranked[r,rho,rep] for rep in range(repetitions)])
            ax.plot((np.arange(2000//r)+.5)/(2000//r),v.mean(0),color=color,label=f'r={r}; J={2000//r}')
        ax.set(title=f'rho={rho:g}',xlabel='Relative team rank',ylabel='Team mean (talent units)',ylim=(-2.6,2.9));ax.grid(alpha=.2)
    axes[0,0].legend(fontsize=8);fig.suptitle(title.replace('; shading = ±1 assignment SD','')+'\nTeams ranked separately within each assignment; curves are mean ranked values',fontsize=11)
    save(fig,'ranked_team_means')
    fig,ax=plt.subplots(figsize=(10,5),layout='constrained')
    ax.hist(a,bins=50,density=True,color='#4682b4',edgecolor='white')
    ax.set(title=f'One shared input population: 2,000 normal draws\nMean={a.mean():.3f}; SD={a.std():.3f}; no population redraws across settings',xlabel='A_i',ylabel='Probability density')
    save(fig,'input_population')
    (out/'summary.json').write_text(json.dumps(dict(new_assignments=new,reused=reused,imported=imported,
        aggregate=aggregate,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        limitation='Conditional on one population. N fixed implies J changes with r. Adjacent-team overlap compares different rank spacings across J.',
        checkpoints=provenance),indent=2)+'\n')
    print(f'New: {new}; imported: {imported}; resumed: {reused}\nOUTPUT: {out}',flush=True)
    return out


if __name__=='__main__':run()
