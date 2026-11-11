"""Audit saved runs and optionally run a paired initialization comparison.

This separate review does not modify the working notebook or historical results.
New experiments require --run-paired. Caps are equal and sum to M; each nonfull
team gets one opportunity. Initial signals disappear at the first real arrival.
"""
from pathlib import Path
from dataclasses import fields
import argparse
import csv
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lg_composition.experiment import PROJECT_ROOT, assignment_probabilities, assign, draw_inputs
from lg_composition.talent import draw_population
from lg_composition.uncapped import UncappedSettings, describe_uncapped


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False)+'\n')


def audit(output):
    """Read metadata and check the first saved population against its stated law."""
    rows = []
    names = {f.name for f in fields(UncappedSettings)}
    for path in sorted((PROJECT_ROOT/'results').rglob('run_metadata.json')):
        if 'validation' in path.parts or output in path.parents:
            continue
        meta = json.loads(path.read_text())
        settings = meta.get('settings', meta.get('base_settings', {}))
        row = dict(path=str(path.relative_to(PROJECT_ROOT)), status=meta.get('status'), settings=settings)
        divisions = sorted((path.parent/'divisions').glob('*rep-000.npz'))
        if divisions and 'uncapped_rosters' in path.parts:
            with np.load(divisions[0], allow_pickle=False) as unit:
                raw, expected = draw_population(UncappedSettings(**{k:v for k,v in settings.items() if k in names}), 0)
                row['first_population_matches_declared_law'] = bool(np.array_equal(unit['ability'], expected))
                row['first_population_range'] = [float(unit['ability'].min()), float(unit['ability'].max())]
                row['first_population_file'] = str(divisions[0].relative_to(PROJECT_ROOT))
        summary = path.parent/'division_summary.csv'
        if summary.exists():
            records = list(csv.DictReader(summary.open()))
            row['saved_h_sort_means'] = {str(rho): float(np.mean([float(r['h_sort']) for r in records
                if float(r['rho']) == rho])) for rho in sorted({float(r['rho']) for r in records})}
        rows.append(row)
    write_json(output/'historical_inventory.json', rows)
    return rows


def capped_assignment(ability, capacities, initial, rho, order, uniforms):
    """Use the existing stable probability kernel with configurable initial signals."""
    counts = np.zeros(len(capacities), dtype=int)
    means = initial.copy()
    ids = np.full(len(ability), -1, dtype=int)
    for step, player in enumerate(order):
        p = assignment_probabilities(ability[player], means, capacities-counts, rho, 'team_opportunities')
        cdf = np.cumsum(p); cdf[-1] = 1.
        team = int(np.searchsorted(cdf, uniforms[step], side='right'))
        ids[player] = team
        counts[team] += 1
        if counts[team] == 1:
            means[team] = ability[player]
        else:
            means[team] += (ability[player]-means[team])/counts[team]
    np.testing.assert_array_equal(counts, capacities)
    return ids


def metrics(ability, ids, n_teams):
    result = describe_uncapped(ability, ids, n_teams)
    ranked = np.argsort(result['team_means'])
    inversions = []
    for low, high in zip(ranked[:-1], ranked[1:]):
        a, b = ability[ids == low], np.sort(ability[ids == high])
        left = np.searchsorted(b, a, side='left')
        right = np.searchsorted(b, a, side='right')
        inversions.append(float(np.mean((left+.5*(right-left))/len(b))))
    result['adjacent_inversion'] = float(np.mean(inversions))
    return result


def run_paired(output, repetitions, n_players, n_teams):
    if n_players % n_teams or n_teams < 2:
        raise ValueError('Use at least two teams and M divisible by J for this equal-cap review')
    rhos = (0., .5, 1., 2., 4.)
    spec = dict(n_players=n_players, n_teams=n_teams, repetitions=repetitions,
                laws=['normal', 'beta'], rhos=rhos, population_seed=6102026,
                assignment_seed=6102027, population_mode='same', talent_scale='theoretical_mean_sd',
                capacities='equal; total=M', opportunities='one_per_nonfull_team',
                initializations=['population_mean','linear_realized_min_to_max'],
                first_member_replaces_initial=True,
                interpretation='Controlled synthetic check; not empirical league validation',
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                kernel_sha256=hashlib.sha256((PROJECT_ROOT/'code/lg_composition/experiment.py').read_bytes()).hexdigest(),
                talent_sha256=hashlib.sha256((PROJECT_ROOT/'code/lg_composition/talent.py').read_bytes()).hexdigest())
    digest = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:12]
    destination = output/f'paired-{digest}'
    (destination/'divisions').mkdir(parents=True, exist_ok=True)
    write_json(destination/'specification.json', spec)
    capacities = np.full(n_teams, n_players//n_teams, dtype=int)
    records, arrays = [], {}
    for law in spec['laws']:
        settings = UncappedSettings(n_players=n_players, n_teams=n_teams,
                                    assignment_repetitions=repetitions, talent_distribution=law, rhos=rhos)
        raw, ability = draw_population(settings, 0)
        starts = {'population_mean': np.full(n_teams, ability.mean()),
                  'linear_realized_min_to_max': np.linspace(ability.min(), ability.max(), n_teams)}
        for rep in range(repetitions):
            order, uniforms = draw_inputs(settings, rep)
            for rho in rhos:
                ids_by_start = {}
                for label, initial in starts.items():
                    file = destination/'divisions'/f'{law}_{label}_rho{rho:g}_rep{rep:03d}.npz'
                    if file.exists():
                        with np.load(file, allow_pickle=False) as saved:
                            for key, val in [('ability',ability), ('arrival_order',order), ('choice_uniforms',uniforms),
                                             ('initial_centroids',initial), ('capacities',capacities)]:
                                np.testing.assert_array_equal(saved[key], val)
                            ids = saved['team_id'].copy()
                    else:
                        ids = capped_assignment(ability, capacities, initial, rho, order, uniforms)
                        # Independently compare the Abar branch to the existing fixed-roster engine.
                        if rep == 0 and label == 'population_mean':
                            baseline, _ = assign(ability, n_teams, n_players//n_teams, rho,
                                                 'team_opportunities', order, uniforms)
                            np.testing.assert_array_equal(ids, baseline)
                        np.savez_compressed(file, ability=ability, original_draws=raw, team_id=ids,
                            arrival_order=order, choice_uniforms=uniforms, initial_centroids=initial,
                            capacities=capacities, rho=rho, repetition=rep, initialization=label)
                    ids_by_start[label] = ids
                    summary = metrics(ability, ids, n_teams)
                    np.testing.assert_array_equal(summary['team_sizes'], capacities)
                    records.append(dict(law=law, initialization=label, rho=rho, repetition=rep,
                        h_sort=float(summary['h_sort']), adjacent_inversion=summary['adjacent_inversion'],
                        mean_range=float(np.ptp(summary['team_means'])),
                        within_variance=float(summary['mean_within_variance'])))
                    arrays[(law,label,rho,rep)] = (ability, ids, summary['team_means'])
                if rho == 0:
                    np.testing.assert_array_equal(*ids_by_start.values())
            if (rep+1) % 5 == 0:
                print(f'{law}: {rep+1}/{repetitions} paired repetitions saved', flush=True)
    with (destination/'division_metrics.csv').open('w') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0])); writer.writeheader(); writer.writerows(records)
    aggregate = []
    for law in spec['laws']:
        for rho in rhos:
            rows = {}
            for label in starts:
                rows[label] = [r for r in records if r['law']==law and r['rho']==rho and r['initialization']==label]
                aggregate.append(dict(law=law, rho=rho, initialization=label,
                    h_sort_mean=float(np.mean([r['h_sort'] for r in rows[label]])),
                    adjacent_inversion_mean=float(np.mean([r['adjacent_inversion'] for r in rows[label]]))))
            delta = np.array([r['h_sort'] for r in rows['linear_realized_min_to_max']])-np.array([r['h_sort'] for r in rows['population_mean']])
            se = float(delta.std(ddof=1)/np.sqrt(repetitions)) if repetitions>1 else 0.
            aggregate.append(dict(law=law, rho=rho, initialization='paired_linear_minus_Abar',
                                  h_sort_difference=float(delta.mean()), conditional_SE=se))
    write_json(destination/'aggregate.json', aggregate)
    colors = {'population_mean':'#2166ac','linear_realized_min_to_max':'#b35806'}
    labels = {'population_mean':'All start at Abar','linear_realized_min_to_max':'Equally spaced: min(A) to max(A)'}
    fig, axes = plt.subplots(2,3,figsize=(16,9))
    for row, law in enumerate(spec['laws']):
        for label in starts:
            for col, key in enumerate(['h_sort','adjacent_inversion']):
                samples = np.array([[r[key] for r in records if r['law']==law and r['rho']==rho and r['initialization']==label] for rho in rhos])
                mean, sd = samples.mean(axis=1), samples.std(axis=1,ddof=1)
                axes[row,col].plot(rhos, mean, marker='o',color=colors[label],label=labels[label])
                axes[row,col].fill_between(rhos, mean-sd, mean+sd, color=colors[label],alpha=.12)
            ranked = np.array([np.sort(arrays[law,label,4.,rep][2]) for rep in range(repetitions)])
            axes[row,2].plot(np.arange(1,n_teams+1), ranked.mean(axis=0), marker='o',color=colors[label],label=labels[label])
            axes[row,2].fill_between(np.arange(1,n_teams+1),ranked.mean(axis=0)-ranked.std(axis=0,ddof=1),
                                     ranked.mean(axis=0)+ranked.std(axis=0,ddof=1),color=colors[label],alpha=.12)
        for col, title in enumerate(['Between-team sorting: H_sort','Adjacent-team mixing probability','Ranked team means at rho=4']):
            axes[row,col].set_title(f'{law.capitalize()}: {title}')
            axes[row,col].grid(alpha=.2)
            axes[row,col].set_xlabel('rho' if col<2 else 'Team rank within each repetition')
        axes[row,0].set_ylim(0,1);axes[row,1].set_ylim(0,.55)
        axes[row,0].legend(fontsize=8)
    fig.suptitle(f'NEW matched capped experiment: M={n_players:,}; J={n_teams}; cap={n_players//n_teams}; {repetitions} repetitions\n'
                 'One opportunity per nonfull team; mean attractor; same players/order/uniforms within each paired comparison')
    fig.text(.5,.01,'Shading: ±1 assignment SD, conditional on one fixed population per law. Adjacent mixing = P(player from lower-mean team exceeds player from next-higher-mean team).\n'
             'Sorted ranks are recomputed within each repetition; curves do not assert stable rankings of named teams. Equal capacities are illustrative, not empirical league sizes.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.065,1,.92))
    fig.savefig(destination/'initialization_comparison.png',dpi=150);fig.savefig(destination/'initialization_comparison.pdf');plt.close(fig)
    print(json.dumps(aggregate, indent=2), flush=True)
    print(f'OUTPUT: {destination}', flush=True)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-paired', action='store_true')
    parser.add_argument('--players', type=int, default=2000)
    parser.add_argument('--teams', type=int, default=10)
    parser.add_argument('--repetitions', type=int, default=30)
    args = parser.parse_args()
    output = PROJECT_ROOT/'results/initialization_review_20261110'
    output.mkdir(parents=True, exist_ok=True)
    inventory = audit(output)
    print(f'Audited {len(inventory)} historical runs; inventory: {output}',flush=True)
    if args.run_paired:
        run_paired(output,args.repetitions,args.players,args.teams)
