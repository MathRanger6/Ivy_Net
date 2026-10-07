"""Notebook-led batches with shared rule and talent-distribution controls.

This orchestrator calls the unchanged fixed-roster assignment kernel. A tuple
runs only its selected rule. Population size is J*r; variable rosters are later.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import time
from dataclasses import dataclass
from pathlib import Path
import numpy as np
from .talent import TalentSettings, draw_population, load_talent_unit
from .experiment import (
    PROJECT_ROOT, Settings, assign, atomic_npz, atomic_text, code_digest, describe,
    draw_inputs, event, load_unit, population, record, run_directory, run_id,
    save_summary, unit_path,
)

RULE_NAMES = {"one": "team_opportunities", "seats": "seat_opportunities"}


@dataclass(frozen=True)
class Scenario:
    chance: str
    n_teams: int
    roster_size: int
    repetitions: int

    @classmethod
    def parse(cls, value):
        if not isinstance(value, (list, tuple)) or len(value) != 4:
            raise ValueError("Each scenario must be (one-or-seats, teams, players/team, repetitions)")
        scenario = cls(*value)
        if not isinstance(scenario.chance, str) or scenario.chance not in RULE_NAMES:
            raise ValueError("Scenario rule must be 'one' or 'seats'")
        if any(isinstance(v, bool) or not isinstance(v, int) or v <= 0
               for v in (scenario.n_teams, scenario.roster_size, scenario.repetitions)):
            raise ValueError("Teams, players/team and repetitions must be positive integers")
        if scenario.n_players < 2:
            raise ValueError("Sorting requires at least two players")
        return scenario

    @property
    def rule(self):
        return RULE_NAMES[self.chance]

    @property
    def n_players(self):
        return self.n_teams * self.roster_size

    @property
    def slug(self):
        return f"{self.chance}_J{self.n_teams}_r{self.roster_size}_reps{self.repetitions}"

    def as_tuple(self):
        return (self.chance, self.n_teams, self.roster_size, self.repetitions)


@dataclass(frozen=True)
class Batch:
    scenarios: tuple[Scenario, ...]
    rhos: tuple[float, ...]
    population_seed: int
    assignment_seed: int
    theta_quantile: float
    results_directory: str
    chance_rule: str = "both"
    talent_distribution: str = "normal"
    weibull_shape: float = 2.0
    talent_scale: str = "theoretical_mean_sd"
    population_mode: str = "same"

    @classmethod
    def from_dict(cls, values):
        chance = values.get("chance_rule", "both")
        if chance not in ("one", "seats", "both"):
            raise ValueError("CHANCE_RULE must be one, seats or both")
        dimensions = values["scenarios"]
        if any(not isinstance(s, (list, tuple)) or len(s) != 3 for s in dimensions):
            raise ValueError("Each scenario must be (teams, players/team, repetitions)")
        if len({tuple(s) for s in dimensions}) != len(dimensions):
            raise ValueError("Supply distinct scenario tuples")
        choices = ("one", "seats") if chance == "both" else (chance,)
        scenarios = tuple(Scenario.parse((rule, *s)) for s in dimensions for rule in choices)
        if not scenarios or len(set(scenarios)) != len(scenarios):
            raise ValueError("Supply a nonempty list of distinct scenario tuples")
        batch = cls(scenarios, tuple(float(r) for r in values["rhos"]),
                    values["population_seed"], values["assignment_seed"],
                    float(values["theta_quantile"]), values["results_directory"],
                    chance, values.get("talent_distribution", "normal"),
                    float(values.get("weibull_shape", 2.0)),
                    values.get("talent_scale", "theoretical_mean_sd"),
                    values.get("population_mode", "same"))
        if not np.isfinite(batch.theta_quantile) or not 0 < batch.theta_quantile < 1:
            raise ValueError("Theta quantile must lie strictly between zero and one")
        for scenario in scenarios:
            batch.settings(scenario).validate()
        return batch

    def as_dict(self):
        dimensions = list(dict.fromkeys((s.n_teams, s.roster_size, s.repetitions) for s in self.scenarios))
        return dict(scenarios=[list(s) for s in dimensions], chance_rule=self.chance_rule,
                    talent_distribution=self.talent_distribution, weibull_shape=self.weibull_shape,
                    talent_scale=self.talent_scale, population_mode=self.population_mode,
                    rhos=list(self.rhos), population_seed=self.population_seed,
                    assignment_seed=self.assignment_seed, theta_quantile=self.theta_quantile,
                    results_directory=self.results_directory)

    def settings(self, scenario):
        return TalentSettings(n_players=scenario.n_players, n_teams=scenario.n_teams,
                        roster_size=scenario.roster_size, rhos=self.rhos,
                        assignment_repetitions=scenario.repetitions,
                        population_seed=self.population_seed,
                        assignment_seed=self.assignment_seed,
                        results_directory=f"{self.results_directory}/{scenario.slug}",
                        talent_distribution=self.talent_distribution, weibull_shape=self.weibull_shape,
                        talent_scale=self.talent_scale, population_mode=self.population_mode)

    @property
    def talent_label(self):
        law = {"normal": "N(0,1)", "uniform": "Uniform(0,1)", "beta": "Beta(2,2)",
               "weibull": f"Weibull(shape={self.weibull_shape:g}, scale=1)"}[self.talent_distribution]
        return law + ("; theoretical mean/SD scaling" if self.talent_scale == "theoretical_mean_sd"
                      else "; original scale")

    @property
    def population_label(self):
        return ("one fixed population; SD reflects assignment variability" if self.population_mode == "same"
                else "fresh population per repetition; SD reflects population and assignment variability")

    @property
    def talent_slug(self):
        shape = format(self.weibull_shape, ".6g").replace(".", "p")
        law = f"weibull_k{shape}" if self.talent_distribution == "weibull" else self.talent_distribution
        return law + ("_std" if self.talent_scale == "theoretical_mean_sd" else "_raw") + f"_{self.population_mode}"

    @property
    def unit_count(self):
        return sum(s.repetitions * len(self.rhos) for s in self.scenarios)


def export_batch(batch, project_root=PROJECT_ROOT):
    root = Path(project_root).resolve()
    folder = root / "settings"
    if folder.resolve().parent != root:
        raise ValueError("Settings folder must stay within the project")
    folder.mkdir(exist_ok=True)
    destination = folder / "composition_scenarios.json"
    atomic_text(destination, json.dumps(batch.as_dict(), indent=2) + "\n")
    return destination


def load_scenario(batch, scenario, project_root=PROJECT_ROOT):
    settings = batch.settings(scenario)
    directory = run_directory(settings, project_root)
    units = []
    for rep in range(scenario.repetitions):
        original_draws, ability = draw_population(settings, rep)
        for rho in batch.rhos:
            path = unit_path(directory, rho, rep, scenario.rule)
            if not path.exists():
                raise FileNotFoundError(f"Missing division for {scenario.slug}; run/resume first: {path}")
            units.append(load_talent_unit(path, settings, rho, rep, scenario.rule, ability))
    return dict(scenario=scenario, settings=settings, directory=directory, units=units)


def ready_scenarios(batch, project_root=PROJECT_ROOT, progress=print):
    """Show only verified complete scenarios, preserving incomplete/error state."""
    ready = []
    for scenario in batch.scenarios:
        directory = run_directory(batch.settings(scenario), project_root)
        metadata_file = directory / "run_metadata.json"
        if not metadata_file.exists():
            if progress:
                progress(f"{scenario.slug}: not yet run")
            continue
        metadata = json.loads(metadata_file.read_text())
        if metadata.get("status") != "complete":
            if progress:
                progress(f"{scenario.slug}: {metadata.get('status')}; run/resume before plotting")
            continue
        item = load_scenario(batch, scenario, project_root)
        ready.append(item)
        if progress:
            progress(f"{scenario.slug}: verified {len(item['units'])} divisions")
    return ready


def run_batch(batch, project_root=PROJECT_ROOT, progress=print):
    """Execute only tuples selected in the notebook. One checkpoint per division."""
    for scenario in batch.scenarios:
        settings = batch.settings(scenario)
        directory = run_directory(settings, project_root)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "divisions").mkdir(exist_ok=True)
        total = scenario.repetitions * len(batch.rhos)
        metadata = dict(scenario=list(scenario.as_tuple()), source_sha256=code_digest(),
                        orchestrator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                        base_settings=settings.scientific_dict(), selected_rule=scenario.rule,
                        division_count=total, status="running", run_id=run_id(settings))
        started = time.perf_counter()
        records, computed, reused, imported = [], 0, 0, 0
        atomic_text(directory / "run_metadata.json", json.dumps(metadata, indent=2) + "\n")
        event(directory, status="started", scenario=list(scenario.as_tuple()), total=total)
        try:
            for rep in range(scenario.repetitions):
                original_draws, ability = draw_population(settings, rep)
                order, uniforms = draw_inputs(settings, rep)
                for rho in batch.rhos:
                    path = unit_path(directory, rho, rep, scenario.rule)
                    if path.exists():
                        unit = load_talent_unit(path, settings, rho, rep, scenario.rule, ability)
                        reused += 1
                        status = "reused"
                    else:
                        # Read-only compatibility with the original saved paired experiment.
                        # Only an exact scientific-settings match can be reused.
                        old_values = dict(n_players=settings.n_players, n_teams=settings.n_teams,
                                          roster_size=settings.roster_size, rhos=settings.rhos,
                                          assignment_repetitions=settings.assignment_repetitions,
                                          population_seed=settings.population_seed,
                                          assignment_seed=settings.assignment_seed,
                                          results_directory="results/composition_first")
                        old_settings = Settings(**old_values)
                        old_path = unit_path(run_directory(old_settings, project_root),
                                             rho, rep, scenario.rule)
                        if settings.legacy_compatible and old_path.exists():
                            unit = load_unit(old_path, old_settings, rho, rep, scenario.rule, ability)
                            atomic_npz(path, **unit)
                            imported += 1
                            status = "reused original checkpoint"
                        else:
                            teams, centroids = assign(ability, scenario.n_teams,
                                scenario.roster_size, rho, scenario.rule, order, uniforms)
                            summary = describe(ability, teams, scenario.n_teams)
                            np.testing.assert_allclose(centroids, summary["team_means"],
                                                       rtol=1e-12, atol=1e-12)
                            atomic_npz(path, player_id=np.arange(scenario.n_players),
                                original_draws=original_draws, ability=ability, team_id=teams,
                                capacities=np.full(scenario.n_teams, scenario.roster_size),
                                initial_centroid=ability.mean(), arrival_order=order,
                                choice_uniforms=uniforms, population_seed=batch.population_seed,
                                assignment_seed=batch.assignment_seed, run_id=run_id(settings),
                                source_sha256=code_digest(), rule=scenario.rule, rho=rho,
                                repetition=rep, **summary)
                            computed += 1
                            status = "completed"
                        unit = load_talent_unit(path, settings, rho, rep, scenario.rule, ability)
                    records.append(record(unit))
                    elapsed = time.perf_counter() - started
                    event(directory, status=status, rho=rho, repetition=rep,
                          completed=len(records), total=total, elapsed_seconds=elapsed)
                    if progress:
                        progress(f"{scenario.slug}: {len(records)}/{total} {status}, "
                                 f"rho={rho:g}, repetition={rep + 1}; {elapsed:.1f}s")
            save_summary(directory, records)
            metadata.update(status="complete", newly_computed=computed, reused=reused,
                            imported_original=imported, elapsed_seconds=time.perf_counter()-started)
            atomic_text(directory / "run_metadata.json", json.dumps(metadata, indent=2) + "\n")
            event(directory, status="complete", newly_computed=computed, reused=reused,
                  imported_original=imported)
        except BaseException as error:
            metadata.update(status="interrupted" if isinstance(error, KeyboardInterrupt) else "error",
                            completed=len(records), error=repr(error))
            atomic_text(directory / "run_metadata.json", json.dumps(metadata, indent=2) + "\n")
            event(directory, status=metadata["status"], completed=len(records), error=repr(error))
            raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path,
                        default=PROJECT_ROOT / "settings/composition_scenarios.json")
    parser.add_argument("--run", action="store_true")
    parser.add_argument("--plots", action="store_true")
    args = parser.parse_args()
    batch = Batch.from_dict(json.loads(args.settings.read_text()))
    print(json.dumps(batch.as_dict(), indent=2))
    print(f"Selected divisions: {batch.unit_count}")
    if args.run:
        run_batch(batch)
    if args.plots:
        from .scenario_plots import plot_scenario, plot_comparisons, plot_player_distribution, unique_population_scenarios
        ready = ready_scenarios(batch)
        import matplotlib.pyplot as plt
        for scenario in unique_population_scenarios(batch):
            plt.close(plot_player_distribution(batch, scenario))
        for item in ready:
            for fig in plot_scenario(batch, item).values():
                plt.close(fig)
        for fig in plot_comparisons(batch, ready).values():
            plt.close(fig)
    if not args.run and not args.plots:
        print("Configuration preview only. Scientific execution is controlled by Charles.")


if __name__ == "__main__":
    main()
