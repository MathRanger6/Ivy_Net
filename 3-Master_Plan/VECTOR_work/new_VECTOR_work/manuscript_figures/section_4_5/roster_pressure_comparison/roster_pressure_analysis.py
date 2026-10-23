"""Observed NCAA draft outcomes against shared and LOO roster pressure.

This module changes environmental summaries, not scores or observed outcomes.
No simulated selection, fitted parameters, significance tests, or network calls.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.special import expit

HERE = Path(__file__).resolve().parent
REPO = next(p for p in HERE.parents if (p / 'sports/scripts/pass_a_congestion_conditional.py').exists())
for folder in [REPO / 'sports', REPO / 'sports/scripts', HERE.parent]:
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))

KEYS = ['athlete_id', 'team_id', 'season']
GROUPS = ['team_id', 'season']
PANELS = [9, 7, 8]
AXES = ['loo_performance', 'rp_shared', 'rp_loo']
AXIS_LABELS = {
    'loo_performance': 'LOO mean performance\nFocal player EXCLUDED',
    'rp_shared': 'Full-group roster pressure\nFocal player INCLUDED',
    'rp_loo': 'LOO roster pressure\nFocal player EXCLUDED',
}
PANEL_LABELS = {9: 'Panel 9 cohort: all performance levels',
                7: 'Panel 7 cohort: own performance z = 2 to 3',
                8: 'Panel 8 cohort: own performance TOP 7%'}
COLORS = {9: '#356d95', 7: '#735394', 8: '#b45d32'}
SQUID, JACKAL = '#20854b', '#bf660d'
DEFAULT_SETTINGS = dict(theta_quantile=.93, gamma=2., n_bins=16,
                        sensitivity_quantiles=[.80, .90, .93],
                        sensitivity_gammas=[.5, 2., 8.], thin_n=30,
                        show_squid_jackal=True)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def source_fingerprints():
    from sports_pipeline import paths
    files = [paths.player_box_csv(), paths.draft_lookup_csv(), paths.bpm_matched_csv(),
             REPO / 'sports/scripts/pass_a_congestion_conditional.py',
             HERE.parent / 'create_section_4_5_4_figure.py']
    files += sorted((REPO / 'sports/sports_pipeline').glob('*.py'))
    return {str(f.relative_to(REPO)): sha256(f) for f in files if f.is_file()}


def load_sources(refresh=False):
    """Cache only locally reconstructed sources; invalidate on input/code changes."""
    from pass_a_congestion_conditional import CctSpec, _prepare_panel
    from create_section_4_5_4_figure import load_verified_cohort
    cache = HERE / 'cache'
    cache.mkdir(exist_ok=True)
    fingerprints = source_fingerprints()
    manifest = cache / 'source_manifest.json'
    old = json.loads(manifest.read_text()) if manifest.exists() else {}
    names = ['all', 'dft', 'last']
    valid = (not refresh and old.get('inputs') == fingerprints and
             all((cache / f'{name}.pkl').exists() and
                 old.get('cache_sha256', {}).get(name) == sha256(cache / f'{name}.pkl')
                 for name in names))
    if valid:
        sources = {name: pd.read_pickle(cache / f'{name}.pkl') for name in names}
        print('Loaded unchanged, fingerprint-checked local source snapshots.', flush=True)
    else:
        sources = {}
        base = dict(season_min=2009, season_max=2021, min_minutes=20,
                    min_team_season_games=10, winsor_lo=.01, winsor_hi=.99,
                    n_bins=16, ai_lo=None, ai_hi=None)
        for name, dft in [('all', False), ('dft', True)]:
            print(f'Reconstructing full eligible rosters: {name}', flush=True)
            sources[name] = _prepare_panel(CctSpec(**base, dft=dft))
            sources[name].to_pickle(cache / f'{name}.pkl')
        sources['last'], _ = load_verified_cohort()
        sources['last'].to_pickle(cache / 'last.pkl')
        old = dict(inputs=fingerprints, cache_sha256={name: sha256(cache / f'{name}.pkl') for name in names})
        manifest.write_text(json.dumps(old, indent=2))
    verification = verify_sources(sources)
    return sources, dict(**old, verification=verification)


def rank_bins(values, n_bins=16):
    """Historical equal-count convention; ties break by stable source row order."""
    values = pd.Series(values)
    if not np.isfinite(values).all() or len(values) < n_bins:
        raise ValueError('Quantile bins require finite values and at least one row per bin.')
    return np.minimum(np.floor((values.rank(method='first') - 1) * n_bins / len(values)).astype(int), n_bins - 1) + 1


def verify_sources(sources):
    from pass_a_congestion_conditional import _tj_piecewise_tail_edges, _assign_tj_bin_labels
    from create_section_4_5_4_figure import REF_CSV, count_bins
    for name, frame in sources.items():
        if frame[KEYS + ['perf', 'Y_draft']].isna().any().any() or frame.duplicated(KEYS).any():
            raise ValueError(f'Invalid observation identities in {name}.')
        if not frame.Y_draft.isin([0, 1]).all():
            raise ValueError('Expected binary ever-drafted outcomes.')
    last = sources['last']
    assert len(last) == last.athlete_id.nunique() == 22795
    assert int(last.Y_draft.sum()) == 615
    ref = pd.read_csv(REF_CSV)
    checked = count_bins(last, np.r_[ref.edge_lo.iloc[0], ref.edge_hi], 'original')
    assert checked.n.tolist() == ref.n.tolist()
    assert checked.drafted.tolist() == ref.drafts.tolist()
    full = sources['dft']
    cut = float(full.perf.quantile(.93))
    folder = REPO / '3-Master_Plan/re_entry/HEROs_and_PASSes/sports_sandbox/data_story/_compare_0921'
    files = {7: 'CCT_draft_rate_ai_band_poolq_loo_min20_ppm_z2_3_dft.json',
             8: 'ELITE_pond_loo_pw4p7_dft_min20_mg10_top7_ppm_9_21.json'}
    summary = {9: dict(rows=len(last), positive_rows=int(last.Y_draft.sum()))}
    for panel in [7, 8]:
        frame = full.loc[full.perf.between(2, 3) if panel == 7 else full.perf.ge(cut)].copy()
        if panel == 7:
            frame['bin'] = rank_bins(frame.poolq_loo)
        else:
            edges, _ = _tj_piecewise_tail_edges(frame.poolq_loo, n_low=4, n_high=7, split_q=.5)
            frame['bin'] = _assign_tj_bin_labels(frame.poolq_loo, edges).astype(int) + 1
        counts = frame.groupby('bin').Y_draft.agg(['size', 'sum'])
        reference = json.loads((folder / files[panel]).read_text())
        assert counts['size'].tolist() == [v['n'] for v in reference['bins']]
        assert counts['sum'].tolist() == [v['drafts'] for v in reference['bins']]
        summary[panel] = dict(rows=len(frame), positive_rows=int(frame.Y_draft.sum()))
    print('Verified original bin counts and cohorts for panels 9, 7, and 8.', flush=True)
    return dict(panels=summary, panel8_own_performance_cutoff=cut,
                check='All original bin counts and positive counts match saved 2009-2021 sources.')


def add_roster_pressure(roster, theta, gamma):
    """Compute on the FULL roster, then let the caller subset focal observations."""
    if not np.isfinite(theta) or not np.isfinite(gamma) or gamma <= 0:
        raise ValueError('Use finite theta and finite positive gamma.')
    frame = roster.copy()
    if not np.isfinite(frame.perf).all() or frame.duplicated(KEYS).any():
        raise ValueError('Roster needs unique identities and finite performance.')
    frame['competitive_relevance'] = expit(gamma * (frame.perf - theta))
    group = frame.groupby(GROUPS, sort=False)
    frame['roster_n'] = group.perf.transform('size')
    frame['T_j'] = group.perf.transform('mean')
    denominator = (frame.roster_n - 1).replace(0, np.nan)
    frame['loo_performance'] = (group.perf.transform('sum') - frame.perf) / denominator
    frame['rp_shared'] = group.competitive_relevance.transform('mean')
    frame['rp_loo'] = (group.competitive_relevance.transform('sum') - frame.competitive_relevance) / denominator
    frame['rp_difference'] = frame.rp_loo - frame.rp_shared
    eligible = frame.roster_n.gt(1)
    expected = (frame.rp_shared - frame.competitive_relevance) / denominator
    assert np.allclose(frame.loc[eligible, 'rp_difference'], expected[eligible], atol=1e-12)
    assert frame.loc[~eligible, 'rp_loo'].isna().all()
    assert frame.rp_shared.between(0, 1).all()
    assert frame.loc[eligible, 'rp_loo'].between(-1e-14, 1 + 1e-14).all()
    assert group.rp_shared.nunique().eq(1).all()
    return frame


def make_cohorts(sources, theta_quantile=.93, gamma=2.):
    if not 0 < theta_quantile < 1:
        raise ValueError('theta_quantile must lie strictly between zero and one.')
    frames, thresholds = {}, {}
    for name in ['all', 'dft']:
        roster = sources[name]
        theta = float(roster.perf.quantile(theta_quantile))
        thresholds[name] = theta
        frames[name] = add_roster_pressure(roster, theta, gamma)
    # Join the verified final-season keys AFTER computing full team-season means.
    full = frames['all'].set_index(KEYS)
    wanted = pd.MultiIndex.from_frame(sources['last'][KEYS])
    last = full.loc[wanted].reset_index()
    assert np.allclose(last.perf, sources['last'].perf)
    assert np.array_equal(last.Y_draft, sources['last'].Y_draft)
    dft = frames['dft']
    own_cutoff = float(sources['dft'].perf.quantile(.93))
    cohorts = {9: last, 7: dft.loc[dft.perf.between(2, 3)].copy(),
               8: dft.loc[dft.perf.ge(own_cutoff)].copy()}
    for panel, frame in cohorts.items():
        expected = {9: (22795, 615), 7: (534, 175), 8: (1546, 418)}[panel]
        assert (len(frame), int(frame.Y_draft.sum())) == expected
        frame['team_season_key'] = frame.team_id.astype(str) + ':' + frame.season.astype(str)
        frame['theta'] = thresholds['all' if panel == 9 else 'dft']
    return cohorts, dict(theta_quantile=theta_quantile, gamma=gamma,
                         thresholds=thresholds, panel8_own_performance_cutoff=own_cutoff,
                         undefined_loo_rows={p: int(c.rp_loo.isna().sum()) for p, c in cohorts.items()})


def fixed_edges(values, n_bins):
    lo, hi = float(np.nanmin(values)), float(np.nanmax(values))
    if not np.isfinite([lo, hi]).all() or lo >= hi:
        raise ValueError('Equal-width bins require a finite, nonzero range.')
    return np.linspace(lo, hi, n_bins + 1)


def bin_table(frame, axis, method='quantile', n_bins=16, edges=None):
    use = frame.loc[frame[AXES].notna().all(axis=1)].copy()
    use['quantile_bin'] = rank_bins(use[axis], n_bins)
    if method == 'quantile':
        use['bin'] = use.quantile_bin
    elif method == 'EW':
        if edges is None or len(edges) != n_bins + 1:
            raise ValueError('Supply the explicitly shared EW edges.')
        use['bin'] = pd.cut(use[axis], edges, labels=False, include_lowest=True) + 1
        if use.bin.isna().any():
            raise ValueError('An observation falls outside the declared EW range.')
    else:
        raise ValueError('Choose quantile or EW.')
    rows = []
    for k in range(1, n_bins + 1):
        b = use.loc[use.bin == k]
        positives = b.loc[b.Y_draft.eq(1)]
        n, y = len(b), int(b.Y_draft.sum())
        rows.append(dict(bin=k, n=n, positive_rows=y, rate=y / n if n else np.nan,
                         x=float(b[axis].mean()) if method == 'quantile' else (edges[k-1] + edges[k])/2,
                         xmin=float(b[axis].min()), xmax=float(b[axis].max()),
                         edge_left=None if edges is None else edges[k-1],
                         edge_right=None if edges is None else edges[k],
                         distinct_players=b.athlete_id.nunique(),
                         distinct_drafted_players=positives.athlete_id.nunique(),
                         colleges=b.team_id.nunique(), team_seasons=b.team_season_key.nunique(),
                         drafted_colleges=positives.team_id.nunique(),
                         drafted_team_seasons=positives.team_season_key.nunique(),
                         mean_own_performance=float(b.perf.mean())))
    table = pd.DataFrame(rows)
    assert int(table.n.sum()) == len(use)
    assert int(table.positive_rows.sum()) == int(use.Y_draft.sum())
    groups = []
    if n_bins == 16:
        for label, bins in [('Squid', [6, 7, 8]), ('Jackal', [14, 15, 16])]:
            b = use.loc[use.quantile_bin.isin(bins)]
            groups.append(dict(group=label, n=len(b), positive_rows=int(b.Y_draft.sum()),
                               rate=float(b.Y_draft.mean()), xmin=float(b[axis].min()), xmax=float(b[axis].max()),
                               distinct_players=b.athlete_id.nunique(),
                               distinct_drafted_players=b.loc[b.Y_draft.eq(1)].athlete_id.nunique(),
                               team_seasons=b.team_season_key.nunique()))
    return table, pd.DataFrame(groups), use


def make_tables(cohorts, method, n_bins):
    # Physical edges are common between shared and LOO RP AND across cohort rows.
    rp = np.concatenate([c[['rp_shared', 'rp_loo']].to_numpy().ravel() for c in cohorts.values()])
    raw = np.concatenate([c.loo_performance.to_numpy() for c in cohorts.values()])
    edges = {'loo_performance': fixed_edges(raw, n_bins), 'rp_shared': fixed_edges(rp, n_bins)}
    edges['rp_loo'] = edges['rp_shared']
    tables, regions, memberships = {}, [], []
    for panel in PANELS:
        for axis in AXES:
            table, groups, use = bin_table(cohorts[panel], axis, method, n_bins,
                                           edges[axis] if method == 'EW' else None)
            table['panel'], table['axis'], table['method'] = panel, axis, method
            tables[panel, axis] = table
            if not groups.empty:
                groups['panel'], groups['axis'], groups['method'] = panel, axis, method
                regions.append(groups)
            memberships.append(use[KEYS + ['Y_draft', 'bin', 'quantile_bin']].assign(panel=panel, axis=axis, method=method))
    return tables, pd.concat(regions, ignore_index=True) if regions else pd.DataFrame(), edges, pd.concat(memberships, ignore_index=True)


def empirical_counts(frame):
    """Count each player once for empirical K/N; retain plotted row counts separately."""
    labels = frame.groupby('athlete_id').Y_draft
    if labels.nunique().gt(1).any():
        raise ValueError('Ever-drafted status must be consistent across a player\'s rows.')
    players = labels.first()
    return dict(K_emp=int(players.sum()), N_emp=len(players),
                K_over_N=float(players.mean()), D_rows=int(frame.Y_draft.sum()), N_rows=len(frame))


def empirical_count_text(panel, counts):
    c = counts
    return (f'Panel {panel}: unique-player K_emp = {c["K_emp"]:,}; N_emp = {c["N_emp"]:,}; '
            f'K_emp/N_emp = {100*c["K_over_N"]:.2f}% | '
            f'Plotted rows D/N = {c["D_rows"]:,}/{c["N_rows"]:,} ({100*c["D_rows"]/c["N_rows"]:.2f}%).')


def threshold_relation(q):
    return (f'theta = Q_{100*q:g}(full-roster performance); nominal fraction above theta = {100*(1-q):g}%. '
            'Its percentile is chosen independently of empirical K/N.')


def mosaic(cohorts, meta, tables, regions, edges, method, settings, panels=None):
    panels = PANELS if panels is None else panels
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})
    nrows = len(panels)
    fig = plt.figure(figsize=(18, 4.7*nrows + 3.2))
    grid = fig.add_gridspec(nrows*2, 3, height_ratios=[3.1, .9]*nrows,
                           left=.065, right=.985, top=.79 if nrows == 1 else .88,
                           bottom=.32 if nrows == 1 else .19, hspace=.85, wspace=.23)
    q = meta['theta_quantile'] * 100
    fig.suptitle(f'2009–2021 NCAA: changing the measure of the peer environment\n'
                 f'{"QUANTILE" if method == "quantile" else "EQUAL WIDTH (EW)"}: {settings["n_bins"]} bins | '
                 f'theta = performance percentile {q:g} | gamma = {meta["gamma"]:g}',
                 fontsize=16, fontweight='bold', y=.985)
    for row, panel in enumerate(panels):
        frame = cohorts[panel]
        # Matched y scales across all three versions; leave room above 100%.
        upper = max(float(tables[panel, a].rate.max()) for a in AXES) * 100
        ylim = max(10, min(104, np.ceil(upper / 10)*10 + 5))
        for col, axis in enumerate(AXES):
            ax = fig.add_subplot(grid[row*2, col])
            counts_ax = fig.add_subplot(grid[row*2+1, col])
            counts_ax.axis('off')
            t = tables[panel, axis]
            color = COLORS[panel]
            ax.plot(t.x, 100*t.rate, color=color, lw=1.4, zorder=2)
            for thin, markerface in [(False, color), (True, 'white')]:
                selected = (t.n.gt(0) & t.n.lt(settings['thin_n']).eq(thin))
                ax.scatter(t.loc[selected, 'x'], 100*t.loc[selected, 'rate'],
                           facecolors=markerface, edgecolors=color, s=30, zorder=3)
            reg = regions.loc[(regions.panel == panel) & (regions.axis == axis)] if not regions.empty else regions
            if settings['show_squid_jackal'] and not reg.empty:
                for label, bins, paint in [('Squid', [6,7,8], SQUID), ('Jackal', [14,15,16], JACKAL)]:
                    if method == 'quantile':
                        b = t.loc[t.bin.isin(bins)]
                        ax.scatter(b.x, b.rate*100, facecolors=[paint if n >= settings['thin_n'] else 'white' for n in b.n],
                                   edgecolors=paint, s=35, zorder=4)
                    else:
                        r = reg.loc[reg.group == label].iloc[0]
                        ax.axvspan(r.xmin, r.xmax, color=paint, alpha=.10, zorder=0)
                sq, ja = reg.iloc[0], reg.iloc[1]
                counts_ax.text(.5, -.20,
                    f'Squid {int(sq.positive_rows)}/{int(sq.n)} ({100*sq.rate:.1f}%) | '
                    f'Jackal {int(ja.positive_rows)}/{int(ja.n)} ({100*ja.rate:.1f}%)',
                    ha='center', va='top', fontsize=8, transform=counts_ax.transAxes)
            ax.set_title(AXIS_LABELS[axis] + '\n' + PANEL_LABELS[panel], fontsize=10, fontweight='bold', pad=10)
            ax.text(.02, .96, f'N={len(frame):,} | D={int(frame.Y_draft.sum()):,} | '
                    f'theta={frame.theta.iloc[0]:.3f}', transform=ax.transAxes, fontsize=8, va='top',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=.8, pad=1.5))
            ax.set_ylim(0, ylim)
            xedges = edges[axis]
            pad = .035*(xedges[-1]-xedges[0])
            ax.set_xlim(xedges[0]-pad, xedges[-1]+pad)
            ax.set_xlabel('Mean other-player performance (z score)' if axis == 'loo_performance' else 'Mean competitive relevance (0 to 1)', fontsize=9)
            ax.set_ylabel('Ever-drafted players (%)' if panel == 9 else 'Ever-drafted player-season rows (%)', fontsize=9)
            ax.grid(axis='y', alpha=.2)
            ax.spines[['top', 'right']].set_visible(False)
            counts = counts_ax.table(cellText=[t.n.astype(int).astype(str), t.positive_rows.astype(int).astype(str), t.team_seasons.astype(int).astype(str)],
                                     rowLabels=['N', 'D', 'G'], colLabels=t.bin.astype(str),
                                     cellLoc='center', rowLoc='center', bbox=[0, .05, 1, .95])
            counts.auto_set_font_size(False); counts.set_fontsize(6.4 if nrows > 1 else 7)
            for cell in counts.get_celld().values():
                cell.set_linewidth(.25); cell.set_edgecolor('#cccccc')
    footer = ('Performance: PPM, standardized within season\n'
              'N = observations; D = ever-drafted-positive observations; G = distinct college-seasons in each bin. Open circles: N < '
              f'{settings["thin_n"]}. Empty EW bins have no rate.\n'
              'Panel 9: all teams, one final-season row per player. Panels 7–8: all player-seasons at colleges with a draftee in the window.\n'
              'Full eligible rosters define every mean BEFORE focal-player filtering. No x or y clipping; no coarse/fine bin compression; no significance tests.\n')
    footer += '\n'.join(empirical_count_text(p, empirical_counts(cohorts[p])) for p in panels) + '\n'
    footer += threshold_relation(meta['theta_quantile']) + '\n'
    footer += 'K_emp = observed ever-drafted players, not fixed draft slots. Band-specific rates are conditional, not overall selection quotas.\n'
    footer += ('Quantiles are recalculated for each axis and cohort; rank-first ties may split. RP display scales match; membership need not. '
               if method == 'quantile' else 'RP EW edges are identical for shared and LOO pressure across all rows; raw performance has separate units and edges. ')
    if settings['show_squid_jackal'] and settings['n_bins'] == 16:
        footer += '\nGreen = Squid proxy, quantile bins 6–8; orange = Jackal proxy, bins 14–16. EW shading shows their score ranges; totals retain exact quantile membership.'
    fig.text(.5, .018, footer, ha='center', va='bottom', fontsize=8.2, linespacing=1.4)
    return fig


def export_hero_bars(out):
    """Render existing bin counts as traditional HERO bars; no rebinning."""
    out = Path(out)
    bins = pd.read_csv(out / 'all_bin_counts.csv')
    meta = json.loads((out / 'methods_and_provenance.json').read_text())
    summary = pd.read_csv(out / 'paired_comparison_summary.csv').set_index('panel')
    settings = meta['settings']
    paths = {}
    with PdfPages(out / 'HERO_roster_pressure_printable.pdf') as pdf:
        for method in ['quantile', 'EW']:
            for panel in PANELS:
                pair = bins.loc[(bins.panel == panel) & (bins.method == method)
                                & bins.axis.isin(['rp_shared', 'rp_loo'])]
                ymax = max(10, np.ceil(pair.rate.max()*100/5)*5 + 2)
                fig = plt.figure(figsize=(16, 9.5))
                grid = fig.add_gridspec(2, 2, height_ratios=[4, 1], left=.065,
                                       right=.98, bottom=.31, top=.77, hspace=.40, wspace=.17)
                theta = meta['thresholds']['all' if panel == 9 else 'dft']
                label = 'QUANTILE' if method == 'quantile' else 'EQUAL WIDTH (EW)'
                fig.suptitle('Empirical HERO: shared versus LOO roster pressure\n'
                             + PANEL_LABELS[panel] + f' | NCAA 2009–2021 | {label}',
                             fontsize=16, fontweight='bold', y=.98)
                fig.text(.5, .865, f'Threshold theta = performance percentile {100*meta["theta_quantile"]:g}'
                         f' ({theta:.3f} z units) | Sharpness gamma = {meta["gamma"]:g}\n'
                         'Exploratory settings, not fitted to outcomes or calibrated to draft capacity',
                         ha='center', fontsize=10, linespacing=1.5)
                for col, axis in enumerate(['rp_shared', 'rp_loo']):
                    ax = fig.add_subplot(grid[0, col])
                    count_ax = fig.add_subplot(grid[1, col]); count_ax.axis('off')
                    t = pair.loc[pair.axis == axis].sort_values('bin').reset_index(drop=True)
                    assert int(t.n.sum()) == int(summary.loc[panel, 'observations'])
                    assert int(t.positive_rows.sum()) == int(summary.loc[panel, 'positive_rows'])
                    nonempty = t.n.gt(0)
                    bars = ax.bar(t.loc[nonempty, 'bin'], 100*t.loc[nonempty, 'rate'],
                                  width=.80, color='#568ab6', edgecolor='#356d95', linewidth=.5)
                    for bar, n in zip(bars, t.loc[nonempty, 'n']):
                        if n < settings['thin_n']:
                            bar.set_hatch('///')
                    for k in t.loc[~nonempty, 'bin']:
                        ax.text(k, .015*ymax, 'empty', rotation=90, ha='center', va='bottom', fontsize=7)
                    ax.set_title(AXIS_LABELS[axis], fontsize=12, fontweight='bold', pad=10)
                    ax.set_ylim(0, ymax); ax.set_xlim(.3, settings['n_bins']+.7)
                    ax.set_xticks(t.bin)
                    ax.set_xlabel(f'{label} bin (1 = lowest roster pressure)', fontsize=10)
                    ax.set_ylabel('Ever-drafted players (%)' if panel == 9 else 'Ever-drafted player-season rows (%)', fontsize=10)
                    ax.grid(axis='y', alpha=.2); ax.set_axisbelow(True)
                    ax.spines[['top', 'right']].set_visible(False)
                    counts = count_ax.table(cellText=[t.n.astype(int).astype(str),
                        t.positive_rows.astype(int).astype(str), t.team_seasons.astype(int).astype(str)],
                        rowLabels=['N', 'D', 'G'], colLabels=t.bin.astype(int).astype(str),
                        cellLoc='center', rowLoc='center', bbox=[0, 0, 1, 1])
                    counts.auto_set_font_size(False); counts.set_fontsize(8)
                    for cell in counts.get_celld().values():
                        cell.set_edgecolor('#cccccc'); cell.set_linewidth(.35)
                row = summary.loc[panel]
                empirical = dict(K_emp=int(row.distinct_drafted_players), N_emp=int(row.distinct_players),
                                 K_over_N=row.distinct_drafted_players/row.distinct_players,
                                 D_rows=int(row.positive_rows), N_rows=int(row.observations))
                cohort = ('All colleges; one final-season observation per player.' if panel == 9 else
                          'All player-seasons at colleges with a draftee in the window; the same player may recur.')
                bin_note = ('Quantiles are calculated separately for each measure; tied values may split. The same bin number need not contain the same players.'
                            if method == 'quantile' else
                            'Identical physical roster-pressure edges for both charts and all three cohorts. Empty bins have no estimated rate.')
                footer = ('Performance: PPM, standardized within season\n'
                          f'N = observations; D = ever-drafted-positive observations; G = distinct college-seasons in each bin. Bar height = 100 × D/N.\n'
                          + empirical_count_text(panel, empirical) + '\n'
                          + threshold_relation(meta['theta_quantile']) + '\n'
                          'K_emp counts observed ever-drafted players, not fixed draft slots. Band-specific rates are conditional, not overall selection quotas.\n'
                          + cohort + '\n' + bin_note + '\n'
                          f'Hatching: N < {settings["thin_n"]}. Same vertical scale within each pair. No clipping or bin compression. Descriptive outcomes; no significance tests.')
                fig.text(.5, .025, footer, ha='center', va='bottom', fontsize=9, linespacing=1.5)
                path = out / f'HERO_panel{panel}_{method}_shared_vs_LOO.png'
                fig.savefig(path, dpi=200, facecolor='white'); pdf.savefig(fig); plt.close(fig)
                paths[panel, method] = path
    return paths


def paired_diagnostics(cohorts, n_bins=16):
    rows = []
    for panel, frame in cohorts.items():
        c = frame.loc[frame.rp_loo.notna()]
        shared_bins, loo_bins = rank_bins(c.rp_shared, n_bins), rank_bins(c.rp_loo, n_bins)
        positives = c.loc[c.Y_draft.eq(1)]
        rows.append(dict(panel=panel, observations=len(c), distinct_players=c.athlete_id.nunique(),
                         positive_rows=int(c.Y_draft.sum()), distinct_drafted_players=positives.athlete_id.nunique(),
                         colleges=c.team_id.nunique(), college_seasons=c.team_season_key.nunique(),
                         median_shared=float(c.rp_shared.median()), median_loo=float(c.rp_loo.median()),
                         median_paired_change=float(c.rp_difference.median()),
                         loo_lower_percent=100*float(c.rp_difference.lt(-1e-12).mean()),
                         rank_correlation=float(c.rp_shared.corr(c.rp_loo, method='spearman')),
                         changed_quantile_bin_percent=100*float(shared_bins.ne(loo_bins).mean())))
    return pd.DataFrame(rows)


def build_sensitivity(sources, settings, out):
    """Show all predeclared combinations, without searching for a preferred curve."""
    qs, gammas = settings['sensitivity_quantiles'], settings['sensitivity_gammas']
    variants = {(q, g): make_cohorts(sources, q, g)[0] for q in qs for g in gammas}
    all_tables, figures = [], {}
    for panel in PANELS:
        fig, axes = plt.subplots(len(qs), len(gammas), figsize=(14, 12.5), squeeze=False, sharex=True, sharey=True)
        xmax = max(float(c[panel][['rp_shared', 'rp_loo']].max().max()) for c in variants.values())
        ymax = max(float(bin_table(c[panel], a, 'quantile', settings['n_bins'])[0].rate.max())*100
                   for c in variants.values() for a in ['rp_shared', 'rp_loo'])
        ytop = min(104, max(10, np.ceil(ymax/5)*5+2))
        for i, q in enumerate(qs):
            for j, gamma in enumerate(gammas):
                ax = axes[i, j]; frame = variants[q, gamma][panel]
                for axis, color, label in [('rp_shared', '#356d95', 'Full group'), ('rp_loo', '#b45d32', 'LOO')]:
                    table, _, _ = bin_table(frame, axis, 'quantile', settings['n_bins'])
                    table['panel'], table['axis'] = panel, axis
                    table['theta_quantile'], table['gamma'] = q, gamma
                    all_tables.append(table)
                    ax.plot(table.x, table.rate*100, 'o-', color=color, ms=3, lw=1, label=label)
                ax.set_title(f'theta = percentile {100*q:g} ({frame.theta.iloc[0]:.3f}) | gamma = {gamma:g}\n'
                             f'Nominal fraction above theta = {100*(1-q):g}%', fontsize=9)
                ax.set_xlim(-.01, xmax+.01); ax.set_ylim(0, ytop)
                ax.grid(axis='y', alpha=.2); ax.spines[['top', 'right']].set_visible(False)
                ax.set_xlabel('Mean competitive relevance', fontsize=9)
                ax.set_ylabel('Ever-drafted observations (%)', fontsize=9)
        axes[0, 0].legend(fontsize=9)
        fig.suptitle(PANEL_LABELS[panel] + '\nSensitivity to the declared theta and gamma settings', fontsize=15, fontweight='bold')
        fig.text(.5, .025, 'Performance: PPM, standardized within season\n'
                 + empirical_count_text(panel, empirical_counts(frame)) + '\n'
                 'Theta percentiles are chosen independently of empirical K/N; theta uses full-roster performance before focal filtering.\n'
                 'K_emp counts observed ever-drafted players, not fixed draft slots. Band-specific rates are conditional, not overall selection quotas.\n'
                 f'2009–2021 | {settings["n_bins"]} QUANTILE bins per curve, rank-first ties | Blue: focal player included; orange: excluded\n'
                 'Same observations and outcomes in every cell. Separate quantile membership for each curve; common display axes.\n'
                 'All nine settings are shown, not selected for the strongest downturn. Detailed bin support is in sensitivity_bin_counts.csv. No tests.',
                 ha='center', fontsize=9)
        fig.tight_layout(rect=(0, .16, 1, .94))
        path = out / f'panel{panel}_theta_gamma_sensitivity.png'
        fig.savefig(path, dpi=180, facecolor='white'); figures[panel] = path
        plt.close(fig)
    pd.concat(all_tables, ignore_index=True).to_csv(out / 'sensitivity_bin_counts.csv', index=False)
    return figures


def run(settings=None, refresh_sources=False, sensitivity=True):
    settings = {**DEFAULT_SETTINGS, **(settings or {})}
    if not isinstance(settings['n_bins'], int) or settings['n_bins'] < 2:
        raise ValueError('n_bins must be an integer of at least two.')
    if settings['thin_n'] < 1:
        raise ValueError('thin_n must be positive.')
    sources, source_meta = load_sources(refresh=refresh_sources)
    cohorts, meta = make_cohorts(sources, settings['theta_quantile'], settings['gamma'])
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    out = HERE / 'runs' / stamp; out.mkdir(parents=True)
    diagnostics = paired_diagnostics(cohorts, settings['n_bins'])
    diagnostics.to_csv(out / 'paired_comparison_summary.csv', index=False)
    context = pd.DataFrame([dict(panel=p, **empirical_counts(c), theta=meta['thresholds']['all' if p == 9 else 'dft'],
                                 gamma=settings['gamma'], theta_quantile=settings['theta_quantile'],
                                 nominal_above_theta=1-settings['theta_quantile']) for p, c in cohorts.items()])
    context.to_csv(out / 'empirical_selection_context.csv', index=False)
    all_tables, all_regions = [], []
    with PdfPages(out / 'roster_pressure_mosaics_printable.pdf') as pdf:
        for method in ['quantile', 'EW']:
            tables, regions, edges, membership = make_tables(cohorts, method, settings['n_bins'])
            all_tables.extend(tables.values())
            if not regions.empty: all_regions.append(regions)
            membership.to_csv(out / f'{method}_bin_membership.csv.gz', index=False, compression='gzip')
            fig = mosaic(cohorts, meta, tables, regions, edges, method, settings)
            fig.savefig(out / f'roster_pressure_mosaic_{method}.png', dpi=190, facecolor='white')
            pdf.savefig(fig); plt.close(fig)
            for panel in PANELS:
                fig = mosaic(cohorts, meta, tables, regions, edges, method, settings, panels=[panel])
                fig.savefig(out / f'panel{panel}_{method}_comparison.png', dpi=190, facecolor='white')
                plt.close(fig)
            meta[f'{method}_edges'] = {a: e.tolist() for a,e in edges.items()} if method == 'EW' else None
    pd.concat(all_tables, ignore_index=True).to_csv(out / 'all_bin_counts.csv', index=False)
    if all_regions: pd.concat(all_regions, ignore_index=True).to_csv(out / 'squid_jackal_counts.csv', index=False)
    sensitivity_paths = build_sensitivity(sources, settings, out) if sensitivity else {}
    meta.update(settings=settings, source=source_meta, code_sha256=sha256(__file__),
                created_utc=datetime.now(timezone.utc).isoformat(),
                methods={
                    'outcome': 'Observed ever-drafted label. No simulated winners and no annual draft probability.',
                    'cohorts': 'Panel 9: verified all-team final-season cohort. Panels 7/8: verified all-player-season DFT populations. Same cohort within each row.',
                    'rosters': 'Full eligible team-season rosters before performance-band and final-season filtering; min 20 minutes and >10 recorded team-season games.',
                    'performance': 'Original within-season PPM z scores retained. All-team and DFT sources standardize within their respective populations.',
                    'threshold': 'Pooled quantile of ALL full-roster player-season performance values in each source population, before focal filtering. Panels 7/8 share theta; panel 9 uses the all-team scale. Fixed within each shared-versus-LOO pair.',
                    'clipping': 'No clipping of newly computed LOO performance or RP. Historical curves used 1%/99% clipping of LOO performance; exact originals verified before recomputing.',
                    'binning': '16 bins by default for ALL rows: quantile independently by cohort/axis, rank-first ties; EW common physical RP edges across both versions and all cohorts. No mixed-width compression.',
                    'groups': 'G counts distinct team_id/season pairs. Individual players can recur across bins in panels 7/8. Do not add distinct counts across bins.',
                    'squid_jackal': 'Descriptive proxies from displayed quantile bins 6-8 and 14-16, recomputed for each axis/cohort. EW shading min-to-max cannot isolate tied boundary membership.',
                    'inference': 'Descriptive exploration only. No p-values, confidence intervals, fitted models, or causal conclusions.',
                    'sensitivity': 'Predeclared theta percentiles 80,90,93 and gamma .5,2,8 by default; not fitted or chosen to maximize downturn.',
                    'precision': 'Sigmoid evaluated with scipy.special.expit. Extreme finite settings may round to 0 or 1 in floating-point arithmetic.',
                }, sensitivity_files={str(k): str(v) for k,v in sensitivity_paths.items()})
    (out / 'methods_and_provenance.json').write_text(json.dumps(meta, indent=2))
    export_hero_bars(out)
    (HERE / 'latest_run.json').write_text(json.dumps({'run_directory': str(out), 'settings': settings}, indent=2))
    print(diagnostics.to_string(index=False), flush=True)
    print(f'Saved comparison figures and counts in {out}', flush=True)
    return out, diagnostics, meta


if __name__ == '__main__':
    run()
