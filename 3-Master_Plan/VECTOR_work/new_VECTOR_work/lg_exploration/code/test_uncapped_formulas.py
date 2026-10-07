"""Hand-built formula/plot checks ONLY: no population draws or assignments."""
import itertools
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from lg_composition.uncapped import (UncappedSettings, describe_uncapped, random_reference,
    resolve_initial_centroids, update_attractor, expected_final_attractors,
    uncapped_assignment_probabilities, load_unit, run_id, source_digest, RULE)
from lg_composition.uncapped_plots import (_build_figures, _binomial_pmf, _polya_pmf, _pmf,
    _centroid_details, _centroid_caption, plot_population_preview,
    _build_roster_bubbles, _build_mean_bubbles, _build_high_rho_combined_bubbles,
    _team_mean_history, _build_team_mean_evolution, _ranked_roster_text)
from lg_composition.talent import theoretical_moments


class UncappedFormulaChecks(unittest.TestCase):
    def test_uniform_theoretical_moments_and_settings(self):
        settings = UncappedSettings(n_players=4, n_teams=2, rhos=(0.,),
                                    talent_distribution='uniform')
        mean, sd = theoretical_moments(settings)
        self.assertEqual(mean, .5)
        self.assertAlmostEqual(sd, np.sqrt(1/12))
        settings.validate()

    def test_empty_singleton_and_weighted_decomposition(self):
        result = describe_uncapped([0., 2., 4.], np.array([0, 0, 2]), 4)
        np.testing.assert_array_equal(result['team_sizes'], [2, 0, 1, 0])
        np.testing.assert_allclose(result['team_means'], [1, np.nan, 4, np.nan], equal_nan=True)
        np.testing.assert_allclose(result['team_variances'], [1, np.nan, 0, np.nan], equal_nan=True)
        self.assertAlmostEqual(result['h_sort'], .75)
        self.assertAlmostEqual(result['between_variance'], 2.)
        self.assertAlmostEqual(result['mean_within_variance'], 2/3)
        self.assertEqual(result['empty_teams'], 2)
        self.assertEqual(result['largest_roster'], 2)
        np.testing.assert_allclose(_pmf(result['team_sizes'], 2), [.5, .25, .25])

    def test_sorting_extremes(self):
        a = np.array([-2., 0., 1., 3.])
        self.assertEqual(describe_uncapped(a, np.array([0, 0, 0, 0]), 4)['h_sort'], 0.)
        self.assertAlmostEqual(describe_uncapped(a, np.arange(4), 4)['h_sort'], 1.)

    def test_exact_random_reference_by_enumerating_partitions(self):
        # Enumerate every possible partition of three fixed talents into three
        # labeled teams. This is an exact finite sum, not a simulated experiment.
        settings = UncappedSettings(n_players=3, n_teams=3, rhos=(0.,))
        summaries = [describe_uncapped([-1., 0., 2.], np.array(ids), 3)
                     for ids in itertools.product(range(3), repeat=3)]
        expected = random_reference(settings)
        self.assertAlmostEqual(np.mean([s['h_sort'] for s in summaries]), expected['expected_h_sort'])
        self.assertAlmostEqual(np.mean([s['empty_teams'] for s in summaries]), expected['expected_empty_teams'])
        pmf = _binomial_pmf(3, 3, np.arange(4))
        np.testing.assert_allclose(pmf, [8/27, 12/27, 6/27, 1/27])

    def test_plots_from_handmade_partitions_no_random_or_assignment(self):
        settings = UncappedSettings(n_players=4, n_teams=4, assignment_repetitions=2,
                                    rhos=(0., 2.))
        ability = np.array([-2., 0., 1., 3.])
        patterns = {(0., 0): [0, 0, 2, 3], (0., 1): [0, 1, 2, 3],
                    (2., 0): [0, 0, 1, 1], (2., 1): [0, 0, 0, 0]}
        units = [dict(ability=ability, team_id=np.array(ids), rho=rho, repetition=rep,
                      **describe_uncapped(ability, np.array(ids), 4))
                 for (rho, rep), ids in patterns.items()]
        # Guard against any accidental scientific execution during plot checks.
        with patch('numpy.random.default_rng', side_effect=AssertionError('No random draws allowed')), \
             patch('lg_composition.uncapped.assign_uncapped', side_effect=AssertionError('No assignment allowed')):
            figures = _build_figures(settings, units)
            self.assertEqual(len(figures), 5)
            ax = figures['roster_size_distribution'].axes[0]
            np.testing.assert_allclose(ax.lines[0].get_ydata(), [.125, .75, .125, 0., 0.])
            for fig in figures.values():
                fig.canvas.draw()  # Render deterministic fixture plots, no saved research output.
                plt.close(fig)

    def test_initial_centroids_are_signals_not_members(self):
        ability = np.array([-2., 0., 1., 3.])
        np.testing.assert_array_equal(resolve_initial_centroids(ability, 3), [.5, .5, .5])
        np.testing.assert_array_equal(resolve_initial_centroids(ability, 3, 7.), [7., 7., 7.])
        np.testing.assert_array_equal(resolve_initial_centroids(ability, 3, [-1., 0., 1.]), [-1., 0., 1.])
        for spec in [True, float('nan'), float('inf'), [0., 1.], [[0., 1., 2.]], 'other']:
            with self.assertRaises(ValueError):
                resolve_initial_centroids(ability, 3, spec)
        first = UncappedSettings(n_players=4, n_teams=3, rhos=(0.,))
        second = UncappedSettings(n_players=4, n_teams=3, rhos=(0.,), initial_centroids=7.)
        self.assertNotEqual(run_id(first), run_id(second))
        summed = UncappedSettings(n_players=4, n_teams=3, rhos=(0.,), team_attractor='sum')
        self.assertNotEqual(run_id(first), run_id(summed))

    def test_mean_and_sum_updates_replace_the_imaginary_value(self):
        # Pure hand-calculated updates: no assignment or random inputs.
        self.assertEqual(update_attractor(99., 2., 1, 'mean'), 2.)
        self.assertEqual(update_attractor(99., 2., 1, 'sum'), 2.)
        self.assertEqual(update_attractor(2., 4., 2, 'mean'), 3.)
        self.assertEqual(update_attractor(2., 4., 2, 'sum'), 6.)
        ability = np.array([2., 4., -1.])
        ids = np.array([0, 0, 2])
        initial = np.array([99., 88., 77., 66.])
        np.testing.assert_array_equal(
            expected_final_attractors(ability, ids, 4, initial, 'mean'),
            [3., 88., -1., 66.])
        np.testing.assert_array_equal(
            expected_final_attractors(ability, ids, 4, initial, 'sum'),
            [6., 88., -1., 66.])

    def test_uncapped_member_opportunities_share_one_team_attractor(self):
        attractors = np.array([.25, .25, .25])
        sizes = np.array([0, 2, 5])
        np.testing.assert_allclose(
            uncapped_assignment_probabilities(.25, attractors, sizes, 4., False),
            [1/3, 1/3, 1/3])
        np.testing.assert_allclose(
            uncapped_assignment_probabilities(.25, attractors, sizes, 4., True),
            [1/10, 3/10, 6/10])
        probabilities = uncapped_assignment_probabilities(
            0., np.array([0., 1.]), np.array([2, 2]), 1., True)
        self.assertAlmostEqual(probabilities[0]/probabilities[1], np.e)
        base = UncappedSettings(n_players=4, n_teams=2, rhos=(0.,))
        seats = UncappedSettings(n_players=4, n_teams=2, rhos=(0.,), seats_option=True)
        self.assertNotEqual(run_id(base), run_id(seats))
        np.testing.assert_allclose(_polya_pmf(2, 2, np.arange(3)), [1/3, 1/3, 1/3])
        self.assertAlmostEqual(random_reference(seats)['expected_empty_teams'], 2/5)

    def test_checkpoint_initial_and_empty_signals_handbuilt(self):
        # Manually specified division; mock input providers so nothing is drawn
        # or assigned. Check that an empty team retains its own chosen T_j(0).
        settings = UncappedSettings(n_players=3, n_teams=4, rhos=(0.,),
                                    initial_centroids=(-1., 0., 1., 2.))
        ability = np.array([0., 2., 4.]); ids = np.array([0, 0, 2])
        order = np.arange(3); uniforms = np.array([.1, .2, .3])
        unit = dict(ability=ability, original_draws=ability, team_id=ids,
                    player_id=np.arange(3), arrival_order=order, choice_uniforms=uniforms,
                    initial_centroids=np.array(settings.initial_centroids),
                    final_attractors=np.array([1., 0., 4., 2.]),
                    run_id=run_id(settings), source_sha256=source_digest(), rule=RULE,
                    rho=0., repetition=0, population_seed=settings.population_seed,
                    assignment_seed=settings.assignment_seed,
                    **describe_uncapped(ability, ids, 4))
        with tempfile.TemporaryDirectory() as temporary, \
             patch('lg_composition.uncapped.draw_population', return_value=(ability, ability)), \
             patch('lg_composition.uncapped.draw_inputs', return_value=(order, uniforms)), \
             patch('lg_composition.uncapped.assign_uncapped', side_effect=AssertionError('No assignments')):
            path = Path(temporary)/'handbuilt.npz'
            np.savez(path, **unit)
            loaded = load_unit(path, settings, 0., 0)
            np.testing.assert_array_equal(loaded['team_sizes'], [2, 0, 1, 0])
            unit['initial_centroids'] = np.zeros(4)
            np.savez(path, **unit)
            with self.assertRaisesRegex(ValueError, 'initial team centroids'):
                load_unit(path, settings, 0., 0)

    def test_all_plot_annotations_and_preview_without_population_draws(self):
        ability = np.array([-2., 0., 1., 3.]); ids = np.array([0, 0, 2, 3])
        with patch('numpy.random.default_rng', side_effect=AssertionError('No random draws')), \
             patch('lg_composition.uncapped.assign_uncapped', side_effect=AssertionError('No assignments')):
            for spec in ['population_mean', 1.5, (-1., 0., 1., 2.)]:
                settings = UncappedSettings(n_players=4, n_teams=4, rhos=(0.,),
                                            assignment_repetitions=1, initial_centroids=spec)
                unit = dict(ability=ability, team_id=ids, rho=0., repetition=0,
                            **describe_uncapped(ability, ids, 4))
                caption = _centroid_caption(settings, _centroid_details(settings, [unit]))
                figures = _build_figures(settings, [unit])
                for fig in figures.values():
                    self.assertIn(caption, fig._suptitle.get_text())
                    fig.canvas.draw(); plt.close(fig)
                with patch('lg_composition.uncapped_plots.draw_population', return_value=(ability, ability)), \
                     patch('lg_composition.uncapped_plots._save') as save:
                    fig = plot_population_preview(settings, bins=4)
                    self.assertIn(caption, fig._suptitle.get_text())
                    self.assertIn('initial_centroids_by_repetition', save.call_args.args[4])
                    plt.close(fig)
            fresh = UncappedSettings(n_players=4, n_teams=4, rhos=(0.,), population_mode='fresh',
                                     assignment_repetitions=2)
            details = _centroid_details(fresh, [dict(ability=ability, repetition=0),
                                              dict(ability=ability+1., repetition=1)])
            caption = _centroid_caption(fresh, details)
            self.assertIn('all 4 teams', caption)
            self.assertIn(r'T_j(0)=\bar{A}', caption)
            self.assertNotIn('rep 1', caption); self.assertNotIn('0.5', caption)
            self.assertNotIn('rep 2', caption); self.assertNotIn('1.5', caption)
            # A single fresh repetition must also show the target, not realization.
            one = _centroid_caption(fresh, {0: details[0]})
            self.assertEqual(one, caption)
            # Custom targets remain numerical and cover all teams.
            custom = UncappedSettings(n_players=4, n_teams=4, rhos=(0.,),
                                      population_mode='fresh', initial_centroids=7.)
            caption = _centroid_caption(custom, {0: np.full(4, 7.), 1: np.full(4, 7.)})
            self.assertIn('targets', caption); self.assertIn('=7', caption)
            self.assertNotIn('rep ', caption)

    def test_roster_only_skips_other_figures_and_diagnostics(self):
        settings = UncappedSettings(n_players=4, n_teams=4, assignment_repetitions=1, rhos=(0.,))
        ability = np.array([-2., 0., 1., 3.])
        # Only fields needed for the roster plot, not sorting or contenders.
        unit = dict(ability=ability, rho=0., repetition=0, team_sizes=np.array([2, 0, 1, 1]))
        with patch('numpy.random.default_rng', side_effect=AssertionError('No draws')), \
             patch('lg_composition.uncapped_plots.contender_counts', side_effect=AssertionError('Disabled diagnostic')):
            figures = _build_figures(settings, [unit], roster_only=True)
            self.assertEqual(list(figures), ['roster_size_distribution'])
            fig = figures['roster_size_distribution']
            np.testing.assert_allclose(fig.axes[0].lines[0].get_ydata(), [.25, .5, .25])
            self.assertIn('Initial centroids', fig._suptitle.get_text())
            fig.canvas.draw(); plt.close(fig)

    def test_circle_areas_and_descending_list_from_handbuilt_sizes(self):
        settings = UncappedSettings(n_players=6, n_teams=4, rhos=(2., 0.),
                                    assignment_repetitions=2, population_mode='fresh')
        ability = np.array([-2., -1., 0., 1., 2., 3.])
        units = [dict(ability=ability, rho=rho, repetition=rep, team_sizes=np.array(sizes),
                      team_means=np.array([-2., np.nan, .5, 3.] if rho==2. else [-1.5, 0., 1.5, 3.]))
                 for rep in [0, 1] for rho, sizes in [(2., [1, 0, 4, 1]), (0., [2, 1, 2, 1])]]
        with patch('numpy.random.default_rng', side_effect=AssertionError('No draws')), \
             patch('lg_composition.uncapped.assign_uncapped', side_effect=AssertionError('No assignments')):
            text = _ranked_roster_text(settings, units, 1)
            self.assertIn('repetition 2', text)
            self.assertIn('[(4, 0.500), (1, -2.000), (1, 3.000), (0, undefined)]', text)
            self.assertIn('[(2, -1.500), (2, 1.500), (1, 0.000), (1, 3.000)]', text)
            fig = _build_roster_bubbles(settings, units, 1)
            first, second = fig.axes
            self.assertEqual(len(first.patches), 3)
            self.assertEqual(len(second.patches), 4)
            self.assertAlmostEqual((first.patches[0].radius/first.patches[1].radius)**2, 4.)
            self.assertAlmostEqual((first.patches[0].radius/second.patches[0].radius)**2, 2.)
            self.assertTrue(all(c.get_fill() and c.get_alpha()==1. for ax in fig.axes for c in ax.patches))
            self.assertIn('empty teams=1', first.get_title())
            self.assertNotIn('rep 1:', fig._suptitle.get_text())
            fig.canvas.draw(); plt.close(fig)
            mean_fig = _build_mean_bubbles(settings, units, 1)
            mean_first, mean_second = mean_fig.axes
            self.assertEqual(len(mean_first.patches), 3)
            self.assertEqual(len(mean_second.patches), 4)
            # Areas follow |mean|, using one common scale across rho panels.
            self.assertAlmostEqual(
                (mean_first.patches[0].radius/mean_first.patches[1].radius)**2, 1.5)
            self.assertAlmostEqual(
                (mean_first.patches[0].radius/mean_first.patches[2].radius)**2, 6.)
            self.assertEqual(mean_first.patches[0].get_facecolor()[:3],
                             matplotlib.colors.to_rgba('#b2182b')[:3])
            self.assertEqual(mean_first.patches[1].get_facecolor()[:3],
                             matplotlib.colors.to_rgba('#2166ac')[:3])
            self.assertEqual(mean_second.patches[-1].get_facecolor()[:3],
                             matplotlib.colors.to_rgba('#808080')[:3])
            self.assertIn('Area ∝ |team mean|', mean_fig.texts[-1].get_text())
            mean_fig.canvas.draw(); plt.close(mean_fig)
            combined = _build_high_rho_combined_bubbles(settings, units, 1)
            combined_ax = combined.axes[0]
            # rho=2 is numerically highest even though settings order is (2, 0).
            self.assertIn('Highest rho=2', combined_ax.get_title())
            self.assertEqual(len(combined_ax.patches), 3)
            self.assertAlmostEqual(
                (combined_ax.patches[0].radius/combined_ax.patches[1].radius)**2, 4.)
            # The largest team has mean +0.5 (red); the next has mean -2 (blue).
            self.assertGreater(combined_ax.patches[0].get_facecolor()[0],
                               combined_ax.patches[0].get_facecolor()[2])
            self.assertGreater(combined_ax.patches[1].get_facecolor()[2],
                               combined_ax.patches[1].get_facecolor()[0])
            self.assertIn('Circle area ∝ team size', combined.texts[-1].get_text())
            combined.canvas.draw(); plt.close(combined)
            with self.assertRaises(ValueError):
                _ranked_roster_text(settings, units, 2)

    def test_team_mean_history_and_wide_figure_from_handbuilt_arrivals(self):
        settings = UncappedSettings(n_players=4, n_teams=2, rhos=(0., 2.),
                                    assignment_repetitions=1)
        ability = np.array([2., 4., -1., 3.])
        order = np.array([2, 0, 3, 1])
        ids = np.array([0, 0, 1, 0])
        summary = describe_uncapped(ability, ids, 2)
        units = [dict(ability=ability, team_id=ids, arrival_order=order,
                      rho=rho, repetition=0, **summary) for rho in settings.rhos]
        history, chosen = _team_mean_history(settings, units[0])
        np.testing.assert_allclose(history[0], [np.nan, 2., 2.5, 3.], equal_nan=True)
        np.testing.assert_allclose(history[1], [-1., -1., -1., -1.])
        np.testing.assert_array_equal(chosen, [1, 0, 0, 0])
        with patch('numpy.random.default_rng', side_effect=AssertionError('No draws')), \
             patch('lg_composition.uncapped.assign_uncapped', side_effect=AssertionError('No assignments')):
            fig = _build_team_mean_evolution(settings, units, 0)
            self.assertEqual(len(fig.axes), 2)
            self.assertGreaterEqual(fig.get_size_inches()[0], 20)
            self.assertEqual(fig.axes[-1].get_xlabel(),
                             'Assignment round (round 1 = first arriving player)')
            self.assertEqual(len(fig.axes[0].lines), 2)
            self.assertEqual(fig.axes[0].lines[0].get_label(), 'Team 1')
            fig.canvas.draw(); plt.close(fig)
        too_many = UncappedSettings(n_players=16, n_teams=16, rhos=(0.,),
                                    assignment_repetitions=1)
        with self.assertRaisesRegex(ValueError, 'fifteen'):
            _build_team_mean_evolution(too_many, [], 0)

    def test_single_team_analytic_reference(self):
        settings = UncappedSettings(n_players=4, n_teams=1, rhos=(0.,))
        self.assertEqual(random_reference(settings)['expected_h_sort'], 0.)
        np.testing.assert_array_equal(_binomial_pmf(4, 1, np.arange(5)), [0, 0, 0, 0, 1])


if __name__ == '__main__':
    unittest.main()
