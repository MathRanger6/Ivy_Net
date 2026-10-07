"""Plots for the separate uncapped model. Plotting never calls assignment."""
from dataclasses import asdict
from pathlib import Path
import csv
import hashlib
import io
import json
import math
import textwrap
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.patches import Circle
import numpy as np
from .experiment import PROJECT_ROOT, atomic_text
from .talent import draw_population
from .contender_plot import contender_counts
from .uncapped import load_complete, run_directory, random_reference, resolve_initial_centroids



def _centroid_token(settings):
    spec = settings.initial_centroids
    if isinstance(spec, str):
        return 'Abar'
    if np.ndim(spec) == 0:
        return f'{float(spec):g}'
    return 'perteam'


def _title(settings):
    law = {'normal': 'N(0,1)', 'uniform': 'Uniform(0,1)', 'beta': 'Beta(2,2)',
           'weibull': f'Weibull(shape={settings.weibull_shape:g}, scale=1)'}[settings.talent_distribution]
    return (f'Uncapped rosters: M={settings.n_players:,}; J={settings.n_teams:,}; '
            f'{settings.assignment_repetitions} repetitions\n'
            f'{law}; {settings.talent_scale}; population={settings.population_mode}; '
            f'attractor={settings.team_attractor}; opportunities='
            f'{"1+members" if settings.seats_option else "one/team"}')



def _centroid_details(settings, units):
    """Deduplicate rho copies, retaining the exact starting T_j for every team."""
    by_repetition = {}
    for unit in units:
        rep = int(unit['repetition'])
        initial = resolve_initial_centroids(unit['ability'], settings.n_teams, settings.initial_centroids)
        if 'initial_centroids' in unit and not np.array_equal(unit['initial_centroids'], initial):
            raise ValueError('Plot inputs have inconsistent starting centroids')
        if rep in by_repetition and not np.array_equal(by_repetition[rep], initial):
            raise ValueError('Starting centroids must be shared across rho within each repetition')
        by_repetition[rep] = initial
    return by_repetition


def _centroid_caption(settings, details):
    """Fresh mode displays the chosen target; exact realized values stay saved."""
    if settings.population_mode == 'fresh' and isinstance(settings.initial_centroids, str):
        return (r'Initial centroid target: $T_j(0)=\bar{A}$'
                f' for all {settings.n_teams} teams')
    vectors = list(details.values())
    if all(np.array_equal(vectors[0], v) for v in vectors[1:]):
        values = vectors[0]
        entries = []
        start = 0
        while start < len(values):
            end = start+1
            while end < len(values) and values[end] == values[start]:
                end += 1
            team = f'T_{start+1}(0)' if end == start+1 else f'T_{{{start+1}..{end}}}(0)'
            entries.append(f'{team}={values[start]:.8g}')
            start = end
        prefix = ('Initial centroid targets (assignment units; all teams): '
                  if settings.population_mode == 'fresh' else
                  'Initial centroids (Abar; all teams): ' if isinstance(settings.initial_centroids, str)
                  else 'Initial centroids (assignment units; all teams): ')
        # Tuple specifications compare safely to the default string; ndarray
        # specifications are only supported by the internal assignment helper.
        return '\n'.join(textwrap.wrap(prefix+'; '.join(entries), width=130, break_long_words=False))
    raise ValueError('Starting centroids changed unexpectedly across repetitions')


def _annotate_centroids(fig, settings, details):
    caption = _centroid_caption(settings, details)
    width, height = fig.get_size_inches()
    # Preserve the taller plot area when a long per-team caption needs more lines.
    extra_height = .19 * max(0, len(caption.splitlines())-1)
    fig.set_size_inches(width, height+extra_height)
    title = fig._suptitle.get_text() if fig._suptitle is not None else _title(settings)
    header = fig.suptitle(title+'\n'+caption, fontsize=10,
                         y=1-.10/(height+extra_height), va='top')
    # Measure the actual header instead of reserving a large fixed top margin.
    # Exclude it from tight_layout so its height is not reserved a second time.
    header.set_in_layout(False)
    fig.canvas.draw()
    header_bottom = header.get_window_extent(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted()).y0
    top = header_bottom-.04/(height+extra_height)
    fig.tight_layout(rect=(0, .045, 1, top), pad=.6)
    # Include the header in notebook PNGs and tight-bounding-box exports.
    header.set_in_layout(True)


def _save(fig, metric, settings, folder, extra=None):
    """Human-readable parameters plus a digest and exact JSON sidecar."""
    parameters = dict(settings=asdict(settings), metric=metric,
                      plot_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      **(extra or {}))
    digest = hashlib.sha256(json.dumps(parameters, sort_keys=True).encode()).hexdigest()[:12]
    rho_text = '-'.join(f'{r:g}' for r in settings.rhos)
    if len(rho_text) > 35:
        rho_text = f'{len(settings.rhos)}values'
    law = settings.talent_distribution
    if law == 'weibull':
        law += f'{settings.weibull_shape:g}'
    scale = 'std' if settings.talent_scale == 'theoretical_mean_sd' else 'raw'
    name = (f'{metric}_uncapped_M{settings.n_players}_J{settings.n_teams}'
            f'_reps{settings.assignment_repetitions}_{law}_{scale}_{settings.population_mode}'
            f'_{settings.team_attractor}_{"1pmembers" if settings.seats_option else "oneperteam"}'
            f'_rho{rho_text}_ps{settings.population_seed}_as{settings.assignment_seed}'
            f'_q{settings.theta_quantile:g}_T0{_centroid_token(settings)}_{digest}')
    if extra and 'displayed_repetition' in extra:
        name += f"_rep{extra['displayed_repetition']}"
    # Arbitrarily large seed integers must not exceed filesystem name limits.
    if len(name) > 220:
        name = f'{metric}_uncapped_M{settings.n_players}_J{settings.n_teams}_{digest}'
    folder.mkdir(parents=True, exist_ok=True)
    for extension in ('png', 'svg'):
        fig.savefig(folder / f'{name}.{extension}', dpi=150, bbox_inches='tight')
    atomic_text(folder / f'{name}.json', json.dumps(parameters, indent=2) + '\n')


def _band(ax, x, rows, color, label):
    """Each repetition contributes one equally weighted distribution/summary."""
    rows = np.asarray(rows)
    mean = rows.mean(axis=0)
    sd = rows.std(axis=0, ddof=1) if len(rows) > 1 else np.zeros_like(mean)
    ax.plot(x, mean, color=color, label=label)
    ax.fill_between(x, np.maximum(0, mean-sd), np.minimum(1, mean+sd), color=color, alpha=.12)


def _pmf(values, maximum):
    return np.bincount(np.asarray(values, dtype=int), minlength=maximum+1) / len(values)


def _binomial_pmf(n_players, n_teams, support):
    """Exact marginal roster distribution at rho=0; no simulated reference."""
    if n_teams == 1:
        return (support == n_players).astype(float)
    p = 1/n_teams
    return np.array([math.exp(math.lgamma(n_players+1)-math.lgamma(k+1)
                    -math.lgamma(n_players-k+1)+k*math.log(p)
                    +(n_players-k)*math.log1p(-p)) for k in support])


def _polya_pmf(n_players, n_teams, support):
    """Marginal Beta-binomial roster distribution for rho=0 and n_j+1 chances."""
    if n_teams == 1:
        return (support == n_players).astype(float)
    log_beta_denominator = (math.lgamma(1)+math.lgamma(n_teams-1)-math.lgamma(n_teams))
    values = []
    for k in support:
        log_combination = (math.lgamma(n_players+1)-math.lgamma(k+1)
                           -math.lgamma(n_players-k+1))
        log_beta_numerator = (math.lgamma(k+1)+math.lgamma(n_players-k+n_teams-1)
                              -math.lgamma(n_players+n_teams))
        values.append(math.exp(log_combination+log_beta_numerator-log_beta_denominator))
    return np.asarray(values)


def _build_figures(settings, units, *, roster_only=False):
    """Pure plotting of supplied divisions; also accepts hand-built test fixtures."""
    groups = [[u for u in units if float(u['rho']) == rho] for rho in settings.rhos]
    if any(len(g) != settings.assignment_repetitions for g in groups):
        raise ValueError('Require every selected repetition for every rho')
    # Lower rho is lighter; rank by value even if the notebook list is reordered.
    rho_ranks = np.argsort(np.argsort(np.asarray(settings.rhos)))
    colors = plt.get_cmap("viridis")(np.linspace(.9, .08, len(settings.rhos))[rho_ranks])
    figures = {}
    note = ('Curves are repetition means; shading is ±1 repetition SD. '
            + ('Variation conditional on one population.' if settings.population_mode == 'same'
               else 'Variation includes fresh populations and assignments.'))
    maximum = max(int(np.max(u['team_sizes'])) for u in units)
    support = np.arange(maximum+1)
    figures['roster_size_distribution'], axes = plt.subplots(1, 2, figsize=(13, 7))
    for rho, group, color in zip(settings.rhos, groups, colors):
        rows = [_pmf(u['team_sizes'], maximum) for u in group]
        _band(axes[0], support, rows, color, f'rho={rho:g}')
        _band(axes[1], support, np.cumsum(rows, axis=1), color, f'rho={rho:g}')
    reference = (_polya_pmf(settings.n_players, settings.n_teams, support)
                 if settings.seats_option else
                 _binomial_pmf(settings.n_players, settings.n_teams, support))
    reference_label = ('rho=0 theory: Pólya/Beta-binomial' if settings.seats_option
                       else 'rho=0 theory: binomial')
    axes[0].plot(support, reference, 'k--', lw=1, label=reference_label)
    axes[0].set(title='Team-size probability distribution', ylabel='Fraction of ALL teams')
    axes[1].set(title='Cumulative team-size distribution', ylabel='Fraction of teams with size ≤ x')
    for ax in axes:
        ax.axvline(settings.n_players/settings.n_teams, color='gray', ls=':', label='M/J (fixed mean)')
        ax.set(xlabel='Realized roster size (zero included)', xlim=(-.5, maximum+.5))
        ax.legend(fontsize=8); ax.grid(alpha=.2)
    fig = figures['roster_size_distribution']
    fig.suptitle(_title(settings)); fig.text(.5, .01, note, ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .06, 1, .89))

    if roster_only:
        # Return before constructing the other figures or contender diagnostics.
        # This is a plotting choice; it does not change assignment/checkpoint IDs.
        _annotate_centroids(fig, settings, _centroid_details(settings, units))
        return figures

    figures['roster_size_summary'], axes = plt.subplots(1, 3, figsize=(14, 7))
    for ax, key, label in zip(axes, ['empty_teams', 'largest_roster', 'roster_sd'],
                             ['Empty teams', 'Largest roster', 'SD of roster sizes across all teams']):
        rows = np.array([[float(u[key]) for u in group] for group in groups])
        sd = rows.std(axis=1, ddof=1) if rows.shape[1] > 1 else np.zeros(len(groups))
        ax.errorbar(settings.rhos, rows.mean(axis=1), yerr=sd, marker='o', capsize=3)
        ax.set(xlabel='rho', ylabel=label); ax.grid(alpha=.2)
    axes[0].scatter([0], [random_reference(settings)['expected_empty_teams']],
                    color='black', marker='x', label='rho=0 theoretical expectation')
    axes[0].legend(fontsize=8)
    fig = figures['roster_size_summary']; fig.suptitle(_title(settings))
    fig.text(.5, .01, note + f' Mean roster size is always M/J={settings.n_players/settings.n_teams:g}.',
             ha='center', fontsize=8); fig.tight_layout(rect=(0, .07, 1, .89))

    figures['weighted_sorting'], axes = plt.subplots(1, 3, figsize=(14, 7))
    for ax, key, label in zip(axes, ['h_sort', 'between_variance', 'mean_within_variance'],
                             ['Division H_sort', 'Between-team variance (player weighted)',
                              'Within-team variance (player weighted)']):
        rows = np.array([[float(u[key]) for u in group] for group in groups])
        sd = rows.std(axis=1, ddof=1) if rows.shape[1] > 1 else np.zeros(len(groups))
        ax.errorbar(settings.rhos, rows.mean(axis=1), yerr=sd, marker='o', capsize=3)
        ax.set(xlabel='rho', ylabel=label); ax.grid(alpha=.2)
    axes[0].scatter([0], [random_reference(settings)['expected_h_sort']], color='black', marker='x',
                    label='rho=0 theoretical expectation'); axes[0].legend(fontsize=8)
    fig = figures['weighted_sorting']; fig.suptitle(_title(settings))
    fig.text(.5, .01, note, ha='center', fontsize=9); fig.tight_layout(rect=(0, .06, 1, .89))

    figures['occupied_team_composition'], axes = plt.subplots(1, 2, figsize=(13, 7))
    for ax, key, label in zip(axes, ['team_means', 'team_variances'], ['Team mean talent', 'Team talent variance']):
        pooled = np.concatenate([u[key][np.isfinite(u[key])] for u in units])
        low, high = float(pooled.min()), float(pooled.max())
        margin = max((high-low)*.02, 1e-8)
        grid = np.linspace(low-margin, high+margin, 400)
        for rho, group, color in zip(settings.rhos, groups, colors):
            rows = [np.searchsorted(np.sort(u[key][np.isfinite(u[key])]), grid, side='right')
                    / np.count_nonzero(np.isfinite(u[key])) for u in group]
            _band(ax, grid, rows, color, f'rho={rho:g}')
        ax.set(xlabel=label, ylabel='Fraction of occupied teams ≤ x'); ax.legend(); ax.grid(alpha=.2)
    fig = figures['occupied_team_composition']; fig.suptitle(_title(settings))
    fig.text(.5, .01, 'Empty teams have undefined means/variances and are excluded here. '
             'Singleton variance is zero. ' + note, ha='center', fontsize=8)
    fig.tight_layout(rect=(0, .07, 1, .89))

    derived = []
    for group in groups:
        records = []
        for u in group:
            theta = float(np.quantile(u['ability'], settings.theta_quantile, method='linear'))
            flag, counts, peers = contender_counts(u['ability'], u['team_id'], settings.n_teams, theta)
            if not np.any(flag) or np.all(flag):
                raise ValueError('Contender diagnostic requires contenders and other players')
            # With unequal rosters this is NOT total contenders times a common r-1.
            if peers.sum() != np.sum(counts*(u['team_sizes']-1)):
                raise ValueError('Variable-roster contender conservation failed')
            records.append((counts, peers[flag], peers[~flag]))
        derived.append(records)
    figures['contender_distributions'], axes = plt.subplots(1, 3, figsize=(15, 7))
    labels = ['Contenders per team (empty teams included)', 'Contender teammates: contender players',
              'Contender teammates: other players']
    for panel, (ax, label) in enumerate(zip(axes, labels)):
        largest = max(int(record[panel].max()) for group in derived for record in group)
        x = np.arange(largest+1)
        for rho, group, color in zip(settings.rhos, derived, colors):
            _band(ax, x, [_pmf(record[panel], largest) for record in group], color, f'rho={rho:g}')
        ax.set(xlabel='Count', ylabel='Fraction of teams' if panel == 0 else 'Fraction of specified players',
               title=label); ax.legend(fontsize=8); ax.grid(alpha=.2)
    fig = figures['contender_distributions']; fig.suptitle(_title(settings))
    fig.text(.5, .01, f'Contender: A > population quantile {settings.theta_quantile:g}. '
             'Focal players exclude themselves. ' + note, ha='center', fontsize=8)
    fig.tight_layout(rect=(0, .08, 1, .89))
    details = _centroid_details(settings, units)
    for fig in figures.values():
        _annotate_centroids(fig, settings, details)
    return figures



def _roster_snapshot(settings, units, repetition):
    if isinstance(repetition, bool) or not isinstance(repetition, int) or not 0 <= repetition < settings.assignment_repetitions:
        raise ValueError('Choose an existing repetition for the individual roster display')
    selected = []
    for rho in settings.rhos:
        matches = [u for u in units if int(u['repetition']) == repetition and float(u['rho']) == rho]
        if len(matches) != 1:
            raise ValueError('Need exactly one division per rho for the chosen repetition')
        unit = matches[0]
        sizes = np.asarray(unit['team_sizes'])
        if sizes.shape != (settings.n_teams,) or sizes.dtype.kind not in 'iu' or np.any(sizes < 0) or sizes.sum() != settings.n_players:
            raise ValueError('Roster sizes must conserve the chosen player and team counts')
        selected.append(unit)
    return selected


def _ranked_roster_text(settings, units, repetition):
    selected = _roster_snapshot(settings, units, repetition)
    lines = [f'Descending (team size, team mean) — repetition {repetition+1} '
             '(one actual division per rho; means in assignment units, to 3 decimals; '
             'empty-team means are undefined):']
    for rho, unit in zip(settings.rhos, selected):
        sizes = np.asarray(unit['team_sizes'])
        means = np.asarray(unit['team_means'])
        if means.shape != sizes.shape:
            raise ValueError('Each roster must have its corresponding team mean')
        order = np.argsort(-sizes, kind='stable')
        entries = [f'({int(sizes[j])}, {means[j]:.3f})' if sizes[j] > 0 else '(0, undefined)'
                   for j in order]
        lines.append(f'\nrho={rho:g}; largest={int(sizes.max())}; empty teams={np.count_nonzero(sizes==0)}')
        lines.extend(textwrap.wrap('['+', '.join(entries)+']', width=110, break_long_words=False))
    return '\n'.join(lines)+'\n'


def _team_mean_history(settings, unit):
    """Reconstruct observed team means after every arrival from one saved division."""
    ability = np.asarray(unit['ability'], dtype=float)
    team_ids = np.asarray(unit['team_id'])
    order = np.asarray(unit['arrival_order'])
    if (ability.shape != (settings.n_players,) or team_ids.shape != ability.shape
            or team_ids.dtype.kind not in 'iu' or np.any(team_ids < 0)
            or np.any(team_ids >= settings.n_teams)
            or order.shape != ability.shape or order.dtype.kind not in 'iu'
            or not np.array_equal(np.sort(order), np.arange(settings.n_players))):
        raise ValueError('Mean histories require valid saved talents, memberships and arrival order')
    counts = np.zeros(settings.n_teams, dtype=int)
    sums = np.zeros(settings.n_teams, dtype=float)
    current = np.full(settings.n_teams, np.nan)
    history = np.full((settings.n_teams, settings.n_players), np.nan)
    chosen = team_ids[order]
    for step, player in enumerate(order):
        team = int(team_ids[player])
        counts[team] += 1
        sums[team] += ability[player]
        current[team] = sums[team]/counts[team]
        history[:, step] = current
    if not np.array_equal(counts, unit['team_sizes']):
        raise ValueError('Mean-history roster counts do not match the saved division')
    if not np.allclose(current, unit['team_means'], equal_nan=True, rtol=1e-12, atol=1e-12):
        raise ValueError('Mean-history endpoint does not match saved team means')
    return history, chosen


def _build_team_mean_evolution(settings, units, repetition=0):
    """Wide small-multiple plot, enabled only for at most fifteen teams."""
    if settings.n_teams > 15:
        raise ValueError('Team-mean evolution plot is limited to fifteen teams')
    selected = _roster_snapshot(settings, units, repetition)
    fig, axes = plt.subplots(len(selected), 1, sharex=True, sharey=True,
                             figsize=(20, max(6, 3.2*len(selected)+1)), squeeze=False)
    axes = axes[:, 0]
    rounds = np.arange(1, settings.n_players+1)
    colors = plt.get_cmap('tab20')(np.linspace(0, 1, settings.n_teams, endpoint=False))
    for ax, rho, unit in zip(axes, settings.rhos, selected):
        history, chosen = _team_mean_history(settings, unit)
        for team, color in enumerate(colors):
            ax.plot(rounds, history[team], color=color, linewidth=1.7,
                    drawstyle='steps-post', label=f'Team {team+1}')
            updates = np.flatnonzero(chosen == team)
            ax.scatter(rounds[updates], history[team, updates], color=color,
                       s=12, zorder=3, edgecolors='none')
        ax.set_ylabel('Team mean')
        ax.set_title(f'rho={rho:g}')
        ax.grid(alpha=.18)
    axes[-1].set_xlabel('Assignment round (round 1 = first arriving player)')
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=min(settings.n_teams, 8),
               bbox_to_anchor=(.5, .955), frameon=False)
    fig.suptitle(_title(settings)+f'\nObserved team-mean evolution: repetition {repetition+1}')
    fig.text(.5, .01, 'A team line begins when its first real player arrives; dots mark rounds '
             'when that team receives a player. Between arrivals its observed mean is unchanged.',
             ha='center', fontsize=9)
    _annotate_centroids(fig, settings, _centroid_details(settings, selected))
    return fig


def _build_roster_bubbles(settings, units, repetition=0):
    """Filled circle AREA is proportional to actual members; no random layout."""
    selected = _roster_snapshot(settings, units, repetition)
    panel_columns = min(3, len(selected))
    panel_rows = math.ceil(len(selected)/panel_columns)
    fig, axes = plt.subplots(panel_rows, panel_columns,
                             figsize=(6*panel_columns, 6*panel_rows+1), squeeze=False)
    # Same scale and display grid for every rho, so circles are comparable.
    maximum = max(int(np.max(u['team_sizes'])) for u in selected)
    columns = math.ceil(math.sqrt(settings.n_teams))
    rows = math.ceil(settings.n_teams/columns)
    ranks = np.argsort(np.argsort(np.asarray(settings.rhos)))
    colors = plt.get_cmap('viridis')(np.linspace(.9, .08, len(selected))[ranks])
    for ax, rho, unit, color in zip(axes.flat, settings.rhos, selected, colors):
        sizes = np.sort(unit['team_sizes'])[::-1]
        for rank, members in enumerate(sizes):
            if members == 0:
                continue  # Zero membership has zero area; reported in the panel label.
            radius = .46*math.sqrt(int(members)/maximum)
            ax.add_patch(Circle((rank % columns, rank // columns), radius,
                                facecolor=color, edgecolor='none', alpha=1.))
        ax.set(xlim=(-.6, columns-.4), ylim=(rows-.4, -.6), aspect='equal')
        ax.set_title(f'rho={rho:g} • largest={sizes[0]} • empty teams={np.count_nonzero(sizes==0)}')
        ax.set_axis_off()
    for ax in list(axes.flat)[len(selected):]:
        ax.set_axis_off()
    fig.suptitle(_title(settings)+f'\nIndividual rosters: repetition {repetition+1}')
    fig.text(.5, .01, 'One filled circle per occupied team. Area ∝ members; same scale across rho. '
             'Largest to smallest on a display grid; positions have no model meaning.',
             ha='center', fontsize=9)
    _annotate_centroids(fig, settings, _centroid_details(settings, selected))
    return fig


def _build_mean_bubbles(settings, units, repetition=0):
    """Match the roster-circle layout, with area proportional to |team mean|."""
    selected = _roster_snapshot(settings, units, repetition)
    panel_columns = min(3, len(selected))
    panel_rows = math.ceil(len(selected)/panel_columns)
    fig, axes = plt.subplots(panel_rows, panel_columns,
                             figsize=(6*panel_columns, 6*panel_rows+1), squeeze=False)
    occupied_means = []
    for unit in selected:
        sizes = np.asarray(unit['team_sizes'])
        means = np.asarray(unit['team_means'], dtype=float)
        if means.shape != sizes.shape or np.any(~np.isfinite(means[sizes > 0])):
            raise ValueError('Occupied teams must have finite team means')
        occupied_means.extend(means[sizes > 0])
    maximum = max((abs(float(value)) for value in occupied_means), default=0.)
    columns = math.ceil(math.sqrt(settings.n_teams))
    rows = math.ceil(settings.n_teams/columns)
    for ax, rho, unit in zip(axes.flat, settings.rhos, selected):
        sizes = np.asarray(unit['team_sizes'])
        means = np.asarray(unit['team_means'], dtype=float)
        values = means[sizes > 0]
        values = values[np.argsort(-np.abs(values), kind='stable')]
        for rank, mean in enumerate(values):
            # Area is proportional to magnitude, so radius is proportional to sqrt(|mean|).
            radius = 0. if maximum == 0 else .46*math.sqrt(abs(float(mean))/maximum)
            color = '#b2182b' if mean > 0 else '#2166ac' if mean < 0 else '#808080'
            ax.add_patch(Circle((rank % columns, rank // columns), radius,
                                facecolor=color, edgecolor='none', alpha=1.))
        ax.set(xlim=(-.6, columns-.4), ylim=(rows-.4, -.6), aspect='equal')
        ax.set_title(f'rho={rho:g} • max |mean|={np.max(np.abs(values)):.3f} '
                     f'• empty teams={np.count_nonzero(sizes==0)}')
        ax.set_axis_off()
    for ax in list(axes.flat)[len(selected):]:
        ax.set_axis_off()
    fig.suptitle(_title(settings)+f'\nTeam means: repetition {repetition+1}')
    fig.text(.5, .01, 'One filled circle per occupied team. Area ∝ |team mean|; '
             'red = positive, blue = negative, gray = zero; same scale across rho. '
             'Largest |mean| to smallest on a display grid; positions have no model meaning.',
             ha='center', fontsize=9)
    _annotate_centroids(fig, settings, _centroid_details(settings, selected))
    return fig


def _build_high_rho_combined_bubbles(settings, units, repetition=0):
    """Highest rho only: area shows membership and diverging color shows mean."""
    selected = _roster_snapshot(settings, units, repetition)
    highest_rho = max(settings.rhos)
    unit = next(u for rho, u in zip(settings.rhos, selected) if rho == highest_rho)
    sizes = np.asarray(unit['team_sizes'])
    means = np.asarray(unit['team_means'], dtype=float)
    if means.shape != sizes.shape or np.any(~np.isfinite(means[sizes > 0])):
        raise ValueError('Occupied teams must have finite team means')
    order = np.argsort(-sizes, kind='stable')
    order = order[sizes[order] > 0]
    maximum_size = int(sizes.max())
    maximum_absolute_mean = max((float(np.max(np.abs(means[order]))) if len(order) else 0.), 1e-12)
    norm = Normalize(vmin=-maximum_absolute_mean, vmax=maximum_absolute_mean)
    cmap = plt.get_cmap('RdBu_r')
    columns = math.ceil(math.sqrt(settings.n_teams))
    rows = math.ceil(settings.n_teams/columns)
    fig, ax = plt.subplots(figsize=(12, 11))
    for rank, team in enumerate(order):
        radius = .46*math.sqrt(int(sizes[team])/maximum_size)
        ax.add_patch(Circle((rank % columns, rank // columns), radius,
                            facecolor=cmap(norm(means[team])), edgecolor='none', alpha=1.))
    ax.set(xlim=(-.6, columns-.4), ylim=(rows-.4, -.6), aspect='equal')
    ax.set_title(f'Highest rho={highest_rho:g} • largest roster={maximum_size} '
                 f'• empty teams={np.count_nonzero(sizes==0)}')
    ax.set_axis_off()
    colorbar = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax,
                            fraction=.035, pad=.02)
    colorbar.set_label('Team mean (assignment-talent units)')
    fig.suptitle(_title(settings)+f'\nTeam size and mean: repetition {repetition+1}')
    fig.text(.5, .01, 'Highest rho only. Circle area ∝ team size; darker red = higher positive mean; '
             'darker blue = more negative mean; near-white = near zero. '
             'Largest to smallest on a display grid; positions have no model meaning.',
             ha='center', fontsize=9)
    _annotate_centroids(fig, settings, _centroid_details(settings, [unit]))
    return fig


def plot_uncapped(settings, project_root=PROJECT_ROOT, *, roster_only=False, roster_repetition=0):
    """Read completed checkpoints, draw charts and export; never run assignment."""
    folder, units = load_complete(settings, project_root)
    # Validate the chosen snapshot before constructing or exporting figures.
    _roster_snapshot(settings, units, roster_repetition)
    figures = _build_figures(settings, units, roster_only=roster_only)
    bubbles = _build_roster_bubbles(settings, units, roster_repetition)
    mean_bubbles = _build_mean_bubbles(settings, units, roster_repetition)
    combined_bubbles = _build_high_rho_combined_bubbles(settings, units, roster_repetition)
    mean_evolution = (_build_team_mean_evolution(settings, units, roster_repetition)
                      if settings.n_teams <= 15 else None)
    distribution = figures.pop('roster_size_distribution')
    figures = dict(roster_size_distribution=distribution,
                   **({'team_mean_evolution': mean_evolution} if mean_evolution is not None else {}),
                   roster_size_bubbles=bubbles,
                   team_mean_bubbles=mean_bubbles,
                   high_rho_size_mean_bubbles=combined_bubbles,
                   **figures)
    atomic_text(folder/f'ranked_team_sizes_rep-{roster_repetition+1:03d}.txt',
                _ranked_roster_text(settings, units, roster_repetition))
    details = {str(rep): values.tolist() for rep, values in _centroid_details(settings, units).items()}
    for metric, fig in figures.items():
        extra = {'initial_centroids_by_repetition': details}
        if metric == 'roster_size_bubbles':
            extra.update(displayed_repetition=roster_repetition+1, circle_area='proportional_to_member_count')
        elif metric == 'team_mean_bubbles':
            extra.update(displayed_repetition=roster_repetition+1,
                         circle_area='proportional_to_absolute_team_mean',
                         circle_color='red_positive_blue_negative_gray_zero')
        elif metric == 'high_rho_size_mean_bubbles':
            extra.update(displayed_repetition=roster_repetition+1,
                         displayed_rho=max(settings.rhos),
                         circle_area='proportional_to_member_count',
                         circle_color='symmetric_zero_centered_RdBu_r_team_mean')
        elif metric == 'team_mean_evolution':
            extra.update(displayed_repetition=roster_repetition+1,
                         x_axis='assignment_round_starting_at_one',
                         quantity='actual_member_team_mean',
                         empty_teams='undefined_until_first_real_member')
        _save(fig, metric, settings, folder/'plots', extra)
    # Exact distributions alongside curves: every repetition includes all J teams.
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(['rho', 'repetition', 'roster_size', 'team_count', 'fraction_of_all_teams'])
    maximum = max(int(u['team_sizes'].max()) for u in units)
    for u in units:
        counts = np.bincount(u['team_sizes'], minlength=maximum+1)
        for size, count in enumerate(counts):
            writer.writerow([float(u['rho']), int(u['repetition']), size, int(count), count/settings.n_teams])
    atomic_text(folder/'roster_size_distributions.csv', stream.getvalue())
    return figures, folder


def plot_population_preview(settings, project_root=PROJECT_ROOT, bins=40):
    """Notebook-only preview before assignment; no extra copies for rho values."""
    if isinstance(bins, bool) or not isinstance(bins, int) or bins < 1:
        raise ValueError('Histogram bins must be a positive integer')
    populations = [draw_population(settings, rep) for rep in range(settings.assignment_repetitions)]
    raw, used = (np.concatenate([p[i] for p in populations]) for i in (0, 1))
    fig, axes = plt.subplots(1, 2, figsize=(13, 7))
    for ax, values, label, color in zip(axes, [raw, used], ['Original draws', 'Talent used for assignment'],
                                       ['seagreen', 'steelblue']):
        ax.hist(values, bins=bins, density=True, color=color, edgecolor='white')
        ax.set(title=f'{label}\nEmpirical mean={values.mean():.3f}; SD={values.std():.3f}',
               xlabel='Original units' if label == 'Original draws' else 'Assignment units',
               ylabel='Empirical probability density'); ax.grid(alpha=.2)
    distinct = settings.n_players*(settings.assignment_repetitions if settings.population_mode == 'fresh' else 1)
    fig.suptitle(_title(settings))
    fig.text(.5, .01, f'{len(raw):,} player appearances; {distinct:,} distinct simulated players. '
             'Same mode repeats one population; no extra copies across rho.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .06, 1, .89))
    units = [dict(repetition=rep, ability=population[1]) for rep, population in enumerate(populations)]
    details = _centroid_details(settings, units)
    _annotate_centroids(fig, settings, details)
    _save(fig, 'player_distribution', settings, run_directory(settings, project_root)/'plots',
          {'bins': bins, 'initial_centroids_by_repetition': {str(rep): v.tolist() for rep, v in details.items()}})
    return fig
