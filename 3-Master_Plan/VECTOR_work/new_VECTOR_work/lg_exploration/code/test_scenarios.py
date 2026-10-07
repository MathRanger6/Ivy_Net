"""Small tuple-routing, checkpoint compatibility and plot-export checks."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from lg_composition.experiment import PROJECT_ROOT, run_experiment, run_directory
from lg_composition.scenarios import Batch, Scenario, load_scenario, ready_scenarios, run_batch
from lg_composition.scenario_plots import figure_stem, plot_comparisons, plot_scenario, plot_player_distribution, unique_population_scenarios


def fixture(scenarios, chance="both", distribution="normal", scale="theoretical_mean_sd"):
    values=json.loads((PROJECT_ROOT/"settings/composition_scenarios.json").read_text())
    values["scenarios"]=scenarios
    values.update(chance_rule=chance, talent_distribution=distribution, talent_scale=scale)
    values["results_directory"]="results/scenario_validation"
    return Batch.from_dict(values)


class ScenarioChecks(unittest.TestCase):
    def temporary_root(self):
        parent=PROJECT_ROOT/"results/validation"
        parent.mkdir(parents=True,exist_ok=True)
        return tempfile.TemporaryDirectory(dir=parent)

    def test_distribution_scaling_and_resume(self):
        from dataclasses import replace
        from lg_composition.talent import draw_population, theoretical_moments
        for law in ("normal", "uniform", "beta", "weibull"):
            batch=fixture([(4,3,1)],distribution=law)
            settings=batch.settings(batch.scenarios[0])
            raw,ability=draw_population(settings)
            mean,sd=theoretical_moments(settings)
            np.testing.assert_array_equal(ability,(raw-mean)/sd)
            raw_again,unscaled=draw_population(replace(settings,talent_scale="original"))
            np.testing.assert_array_equal(raw,raw_again)
            np.testing.assert_array_equal(raw,unscaled)
            with self.temporary_root() as temporary:
                run_batch(batch,Path(temporary),progress=None)
                ready=ready_scenarios(batch,Path(temporary),progress=None)
                for key in ("original_draws","ability","arrival_order","choice_uniforms"):
                    np.testing.assert_array_equal(ready[0]["units"][0][key],ready[1]["units"][0][key])
                with patch("lg_composition.scenarios.assign",side_effect=AssertionError("Recomputed")):
                    run_batch(batch,Path(temporary),progress=None)
                self.assertIn(batch.talent_slug,figure_stem("team_means",batch,batch.scenarios))
        with self.assertRaises(ValueError):
            fixture([(4,3,1)],chance="bad")
        from lg_composition.experiment import run_id
        beta=fixture([(4,3,1)],distribution="beta")
        normal=fixture([(4,3,1)])
        self.assertNotEqual(run_id(beta.settings(beta.scenarios[0])),
                            run_id(normal.settings(normal.scenarios[0])))

    def test_player_distribution_preview_without_assignments(self):
        import matplotlib.pyplot as plt
        from lg_composition.talent import draw_population
        batch=fixture([(4,3,2)],chance="one",distribution="beta")
        scenario=batch.scenarios[0]
        raw,ability=draw_population(batch.settings(scenario))
        with self.temporary_root() as temporary:
            root=Path(temporary)
            with patch("lg_composition.scenarios.assign",side_effect=AssertionError("Assigned")):
                figure=plot_player_distribution(batch,scenario,root,bins=5)
            for ax,values in zip(figure.axes,(raw,ability)):
                # Pooling repeated populations leaves normalized density unchanged.
                density,edges=np.histogram(np.tile(values,scenario.repetitions),bins=5,density=True)
                np.testing.assert_allclose([p.get_height() for p in ax.patches],density)
                np.testing.assert_allclose([p.get_x() for p in ax.patches],edges[:-1])
                self.assertAlmostEqual(sum(p.get_height()*p.get_width() for p in ax.patches),1.)
            self.assertIn("All 24 player appearances",figure.texts[-1].get_text())
            directory=run_directory(batch.settings(scenario),root)
            self.assertFalse((directory/"run_metadata.json").exists())
            stem=figure_stem("player_talent_distribution_bins5",batch,[scenario])
            for suffix in (".png",".svg",".json"):
                self.assertTrue((directory/"plots"/(stem+suffix)).exists())
            (PROJECT_ROOT/"results/validation/QA_player_distribution.png").write_bytes(
                (directory/"plots"/(stem+".png")).read_bytes())
            plt.close(figure)
        notebook=json.loads((PROJECT_ROOT/"notebooks/01_composition_opportunity_rules.ipynb").read_text())
        ids=[c.get("id") for c in notebook["cells"]]
        self.assertLess(ids.index("lg-player-distribution"),ids.index("lg-batch-run"))

    def test_unique_population_previews(self):
        # Two scenarios with both rules produce four assignment cases, two previews.
        batch=fixture([(4,3,2),(5,3,2)])
        self.assertEqual(len(batch.scenarios),4)
        self.assertEqual(len(unique_population_scenarios(batch)),2)
        # Team dimensions and opportunity rules do not change the population.
        batch=fixture([(4,3,2),(3,4,2),(4,3,3)])
        unique=unique_population_scenarios(batch)
        self.assertEqual([(s.n_players,s.repetitions) for s in unique],[(12,2),(12,3)])
        for chance in ("one","seats","both"):
            self.assertEqual(len(unique_population_scenarios(fixture([(4,3,2)],chance=chance))),1)

    def test_validation_cell_loads_its_own_imports(self):
        # No imports cell or assignments: only controls + validation in a fresh namespace.
        import os
        notebook=json.loads((PROJECT_ROOT/"notebooks/01_composition_opportunity_rules.ipynb").read_text())
        cells={c.get("id"):"".join(c["source"]) for c in notebook["cells"]}
        previous=os.getcwd()
        try:
            os.chdir(PROJECT_ROOT)
            namespace={}
            exec(cells["lg-batch-scenarios"],namespace)
            exec(cells["lg-batch-controls"],namespace)
            with patch("lg_composition.experiment.atomic_text"):
                exec(cells["lg-batch-validate"],namespace)
            self.assertIsInstance(namespace["batch"],namespace["Batch"])
            self.assertIn("unique_population_scenarios",namespace)
            import importlib
            import lg_composition.scenarios as refreshed
            importlib.reload(refreshed)
        finally:
            os.chdir(previous)

    def test_population_switch_pairing_resume_and_preview(self):
        from dataclasses import replace
        from lg_composition.talent import draw_population
        from lg_composition.experiment import run_id
        import matplotlib.pyplot as plt
        for law in ("normal","beta","weibull"):
            same=fixture([(4,3,2)],distribution=law)
            fresh=replace(same,population_mode="fresh")
            scenario=fresh.scenarios[0]
            same_settings=same.settings(same.scenarios[0])
            settings=fresh.settings(scenario)
            np.testing.assert_array_equal(draw_population(same_settings,0)[1],
                                          draw_population(same_settings,1)[1])
            self.assertFalse(np.array_equal(draw_population(settings,0)[1],
                                            draw_population(settings,1)[1]))
            self.assertNotEqual(run_id(same_settings),run_id(settings))
            self.assertEqual(Batch.from_dict(fresh.as_dict()).population_mode,"fresh")
            with self.temporary_root() as temporary:
                root=Path(temporary)
                run_batch(fresh,root,progress=None)
                ready=ready_scenarios(fresh,root,progress=None)
                for rep in range(2):
                    expected=draw_population(settings,rep)[1]
                    for item in ready:
                        for unit in item["units"]:
                            if int(unit["repetition"])==rep:
                                np.testing.assert_array_equal(unit["ability"],expected)
                    one=next(u for u in ready[0]["units"] if int(u["repetition"])==rep)
                    seats=next(u for u in ready[1]["units"] if int(u["repetition"])==rep)
                    for key in ("ability","original_draws","arrival_order","choice_uniforms"):
                        np.testing.assert_array_equal(one[key],seats[key])
                with patch("lg_composition.scenarios.assign",side_effect=AssertionError("Recomputed")):
                    run_batch(fresh,root,progress=None)
                # The histogram must pool the very same per-repetition vectors.
                figure=plot_player_distribution(fresh,scenario,root,bins=5)
                expected=np.concatenate([draw_population(settings,rep)[1] for rep in range(2)])
                density,_=np.histogram(expected,bins=5,density=True)
                np.testing.assert_allclose([p.get_height() for p in figure.axes[1].patches],density)
                self.assertIn("24 independently generated",figure.texts[-1].get_text())
                plt.close(figure)
                if law=="beta":
                    # Verify contenders use their own population in every division.
                    figures=plot_scenario(fresh,ready[0],root)
                    self.assertIn("theta recomputed per population",
                                  figures["team_contender_counts"].axes[0].get_title())
                    for fig in figures.values():
                        plt.close(fig)
                    for fig in plot_comparisons(fresh,ready,root).values():
                        plt.close(fig)
        with self.assertRaises(ValueError):
            replace(same,population_mode="bad").settings(same.scenarios[0]).validate()

    def test_tuple_validation(self):
        self.assertEqual(Scenario.parse(("one",100,20,30)).n_players,2000)
        for value in [("bad",6,10,2),("one",6,10),("one",6,10.,2),("one",0,10,2)]:
            with self.assertRaises(ValueError):
                Scenario.parse(value)
        with self.assertRaises(ValueError):
            fixture([(6,10,2),(6,10,2)])

    def test_selected_rules_resume_pairing_and_parameter_names(self):
        # This is a tiny validation population. Rhos still come from the notebook.
        batch=fixture([(6,10,2)])
        with self.temporary_root() as temporary:
            root=Path(temporary)
            run_batch(batch,root,progress=None)
            ready=ready_scenarios(batch,root,progress=None)
            self.assertEqual(len(ready),2)
            for item in ready:
                self.assertEqual(len(item["units"]),2*len(batch.rhos))
                self.assertEqual({u["rule"].item() for u in item["units"]},{item["scenario"].rule})
                self.assertEqual(len(list((item["directory"]/"divisions").glob("*.npz"))),
                                 2*len(batch.rhos))
            for one,seats in zip(ready[0]["units"],ready[1]["units"]):
                for key in ("ability","arrival_order","choice_uniforms"):
                    np.testing.assert_array_equal(one[key],seats[key])
            with patch("lg_composition.scenarios.assign",side_effect=AssertionError("Recomputed")):
                run_batch(batch,root,progress=None)
            for item in ready:
                metadata=json.loads((item["directory"]/"run_metadata.json").read_text())
                self.assertEqual(metadata["newly_computed"],0)
                self.assertEqual(metadata["reused"],2*len(batch.rhos))
            parent=PROJECT_ROOT/"results/validation"
            import matplotlib.pyplot as plt
            for item in ready:
                figures=plot_scenario(batch,item,root)
                self.assertEqual(len(figures),6)
                for metric,figure in figures.items():
                    stem=figure_stem(metric,batch,[item["scenario"]])
                    self.assertIn(item["scenario"].slug,stem)
                    for suffix in (".png",".svg",".json"):
                        self.assertTrue((item["directory"]/"plots"/(stem+suffix)).is_file())
                    if item["scenario"].chance=="one":
                        (parent/f"QA_scenario_{metric}.png").write_bytes(
                            (item["directory"]/"plots"/(stem+".png")).read_bytes())
                    plt.close(figure)
            figures=plot_comparisons(batch,ready,root)
            self.assertEqual(len(figures),2)
            folder=root/batch.results_directory/"comparisons"
            stem=figure_stem("sorting_comparison",batch,list(batch.scenarios))
            (parent/"QA_scenario_comparison.png").write_bytes((folder/(stem+".png")).read_bytes())
            for figure in figures.values():
                plt.close(figure)
            # A one-only selection has no paired difference and no seats checkpoint.
            one_only=fixture([(6,10,2)], chance="one")
            self.assertEqual(one_only.unit_count,2*len(batch.rhos))
            selected=ready_scenarios(one_only,root,progress=None)
            self.assertEqual(len(selected),1)
            figures=plot_comparisons(one_only,selected,root)
            self.assertEqual(set(figures),{"sorting_comparison"})
            for figure in figures.values():
                plt.close(figure)

    def test_reuse_original_checkpoints_without_mutating_them(self):
        batch=fixture([(6,10,2)], chance="one")
        scenario=batch.scenarios[0]
        from dataclasses import replace
        old_settings=replace(batch.settings(scenario),results_directory="results/composition_first")
        with self.temporary_root() as temporary:
            root=Path(temporary)
            old_directory=run_experiment(old_settings,root,progress=None)
            previous=(old_directory/"run_metadata.json").read_bytes()
            with patch("lg_composition.scenarios.assign",side_effect=AssertionError("Recomputed")):
                run_batch(batch,root,progress=None)
            self.assertEqual((old_directory/"run_metadata.json").read_bytes(),previous)
            item=load_scenario(batch,scenario,root)
            metadata=json.loads((item["directory"]/"run_metadata.json").read_text())
            self.assertEqual(metadata["imported_original"],2*len(batch.rhos))
            self.assertEqual(metadata["newly_computed"],0)


if __name__=="__main__":
    unittest.main()
