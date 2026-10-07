"""Small validation checks; the rho grid comes from the notebook's saved settings.

Edit rho only in the notebook and run its settings cell to refresh the generated
settings/composition_scenarios.json snapshot. These checks use that same grid with
a tiny population; this file is not an experiment-settings interface.
"""
import itertools
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
from lg_composition.sorting_plot import plot_sorting_comparison
from lg_composition.experiment import (
    PROJECT_ROOT, RULES, Settings, assign, assignment_probabilities, describe,
    draw_inputs, load_complete, plot_results, run_experiment, unit_path,
)


def notebook_fixture_settings(**overrides):
    """Inherit the notebook's exported grid; shrink only validation run sizes."""
    batch = json.loads((PROJECT_ROOT / "settings/composition_scenarios.json").read_text())
    teams, roster, repetitions = batch["scenarios"][0]
    values = dict(n_players=teams * roster, n_teams=teams, roster_size=roster,
                  assignment_repetitions=repetitions, rhos=batch["rhos"],
                  population_seed=batch["population_seed"], assignment_seed=batch["assignment_seed"],
                  results_directory="results/composition_first")
    values.update(overrides)
    values["rhos"] = tuple(values["rhos"])
    return Settings(**values)


class CompositionChecks(unittest.TestCase):
    def test_opportunity_odds_and_full_teams(self):
        for rule, expected in [(RULES[0], [.2, .8, 0]), (RULES[1], [.5, .5, 0])]:
            np.testing.assert_allclose(
                assignment_probabilities(0, [0, 0, 0], [2, 8, 0], 0, rule), expected)
        # Fourfold preference for team 0 offsets its fourfold seat disadvantage.
        centroids = [0, np.log(4)]
        np.testing.assert_allclose(
            assignment_probabilities(0, centroids, [2, 8], 1, RULES[0]), [.5, .5])
        np.testing.assert_allclose(
            assignment_probabilities(0, centroids, [2, 8], 1, RULES[1]), [.8, .2])
        # Direct exponentials would all underflow in this case.
        np.testing.assert_allclose(
            assignment_probabilities(0, [1000, 1000], [2, 8], 1000, RULES[0]), [.2, .8])

    def test_filled_rosters_centroids_and_variance_identity(self):
        ability = np.array([-2., -1., 1., 2., -.5, .5])
        for rule in RULES:
            groups, centroids = assign(ability, 3, 2, 4, rule,
                                      np.array([4, 2, 1, 5, 3, 0]), np.linspace(.01, .99, 6))
            summary = describe(ability, groups, 3)
            np.testing.assert_array_equal(summary["team_sizes"], [2, 2, 2])
            np.testing.assert_allclose(centroids, summary["team_means"])
            within = summary["mean_within_variance"]
            between = summary["centroid_sd"] ** 2
            self.assertAlmostEqual(within + between, ability.var())
            self.assertAlmostEqual(summary["h_sort"], between / ability.var())
        # Singleton centroids must be actual players, not population-mean seeds.
        groups, centroids = assign(ability, 6, 1, 2, RULES[0],
                                  np.arange(6), np.linspace(.01, .99, 6))
        np.testing.assert_allclose(centroids[groups], ability)
        np.testing.assert_allclose(describe(ability, groups, 6)["team_variances"], 0)

    def test_random_grouping_expectation_by_exact_enumeration(self):
        # Enumerate every arrival order and every possible weighted team path.
        # This establishes both rho=0 baselines without a Monte Carlo tolerance.
        ability = np.array([-2., -1., 1., 2.])
        for rule in RULES:
            total = 0.
            for permutation in itertools.permutations(range(4)):
                def visit(step, counts, groups, probability):
                    if step == 4:
                        return probability * describe(ability, groups, 2)["h_sort"]
                    probabilities = assignment_probabilities(
                        0, np.zeros(2), 2 - counts, 0, rule)
                    value = 0.
                    for team in np.flatnonzero(probabilities):
                        next_counts, next_groups = counts.copy(), groups.copy()
                        next_counts[team] += 1
                        next_groups[permutation[step]] = team
                        value += visit(step + 1, next_counts, next_groups,
                                       probability * probabilities[team])
                    return value
                total += visit(0, np.zeros(2, dtype=int), np.zeros(4, dtype=int), 1.)
            self.assertAlmostEqual(total / 24, (2 - 1) / (4 - 1), places=12)

    def test_pairing_reproducibility(self):
        settings = notebook_fixture_settings(n_players=40, n_teams=8, roster_size=5)
        first = draw_inputs(settings, 2)
        repeated = draw_inputs(settings, 2)
        np.testing.assert_array_equal(first[0], repeated[0])
        np.testing.assert_array_equal(first[1], repeated[1])
        self.assertFalse(np.array_equal(first[0], draw_inputs(settings, 3)[0]))

    def test_settings_reject_scope_or_capacity_errors(self):
        grid_without_baseline = tuple(rho for rho in notebook_fixture_settings().rhos if rho != 0.)
        wrong_population = notebook_fixture_settings().n_players + 1
        for settings in [notebook_fixture_settings(n_players=wrong_population),
                         notebook_fixture_settings(results_directory="../other"),
                         notebook_fixture_settings(results_directory="reference_snapshot/results"),
                         notebook_fixture_settings(rhos=grid_without_baseline)]:
            with self.assertRaises(ValueError):
                settings.validate()

    def test_resume_corruption_and_plotting(self):
        parent = PROJECT_ROOT / "results" / "validation"
        parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as temporary:
            root = Path(temporary)
            settings = notebook_fixture_settings(n_players=60, n_teams=6, roster_size=10,
                                                 assignment_repetitions=2)
            directory = run_experiment(settings, root, progress=None)
            metadata = json.loads((directory / "run_metadata.json").read_text())
            self.assertEqual(metadata["newly_computed"], settings.unit_count)
            # A verified complete resume must perform no fresh assignments.
            with patch("lg_composition.experiment.assign", side_effect=AssertionError("Recomputed")):
                self.assertEqual(run_experiment(settings, root, progress=None), directory)
            metadata = json.loads((directory / "run_metadata.json").read_text())
            self.assertEqual(metadata["reused"], settings.unit_count)
            directory, units = load_complete(settings, root)
            self.assertEqual(len(units), settings.unit_count)
            figures, plots = plot_results(settings, root)
            sorting_figure, _ = plot_sorting_comparison(settings, root)
            figures["sorting_comparison"] = sorting_figure
            self.assertEqual(len(figures), 6)
            self.assertTrue(all((plots / (name + ".png")).is_file() for name in figures))
            import matplotlib.pyplot as plt
            for fig in figures.values():
                plt.close(fig)
            # Keep one QA image within the project, explicitly a tiny test run.
            for name in figures:
                qa = parent / f"QA_small_test_{name}.png"
                qa.write_bytes((plots / f"{name}.png").read_bytes())
            path = unit_path(directory, 0., 0, RULES[0])
            path.write_bytes(b"intentionally corrupt test checkpoint")
            with self.assertRaises(ValueError):
                run_experiment(settings, root, progress=None)
            self.assertEqual(json.loads((directory / "run_metadata.json").read_text())["status"],
                             "error")
            self.assertEqual(path.read_bytes(), b"intentionally corrupt test checkpoint")


if __name__ == "__main__":
    unittest.main()
