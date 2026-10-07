"""Uncapped variable-roster extension; distinct from fixed-roster LG.

All teams remain eligible. Only exp(-rho*abs(A_i-T_j)) controls preference.
There is no remaining-seat multiplier and no minimum or maximum team size.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
from .experiment import (PROJECT_ROOT, assignment_probabilities, atomic_npz,
                         atomic_text, draw_inputs, event, unit_path, save_summary)
from .talent import draw_population, theoretical_moments

RULE = "uncapped_team_opportunities"
MEMBER_OPPORTUNITY_RULE = "uncapped_one_plus_members_opportunities"


@dataclass(frozen=True)
class UncappedSettings:
    n_players: int = 2000
    n_teams: int = 100
    assignment_repetitions: int = 30
    rhos: tuple[float, ...] = (0., .5, 1., 2., 4.)
    talent_distribution: str = "normal"
    weibull_shape: float = 2.0
    talent_scale: str = "theoretical_mean_sd"
    population_mode: str = "same"
    team_attractor: str = "mean"
    seats_option: bool = False
    initial_centroids: str | float | tuple[float, ...] = "population_mean"
    population_seed: int = 6102026
    assignment_seed: int = 6102027
    theta_quantile: float = .9
    results_directory: str = "results/uncapped_rosters"

    @classmethod
    def from_dict(cls, values):
        values = dict(values)
        values["rhos"] = tuple(float(r) for r in values["rhos"])
        if isinstance(values.get("initial_centroids"), list):
            values["initial_centroids"] = tuple(values["initial_centroids"])
        settings = cls(**values)
        settings.validate()
        return settings

    def validate(self):
        for name in ("n_players", "n_teams", "assignment_repetitions", "population_seed", "assignment_seed"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
        if self.n_players < 2 or self.n_teams < 1 or self.assignment_repetitions < 1:
            raise ValueError("Require at least two players, one team and one repetition")
        if min(self.population_seed, self.assignment_seed) < 0:
            raise ValueError("Seeds must be nonnegative")
        if (not self.rhos or 0. not in self.rhos or len(set(self.rhos)) != len(self.rhos)
                or any(not np.isfinite(r) or r < 0 for r in self.rhos)):
            raise ValueError("Use distinct finite nonnegative rhos including zero")
        if self.talent_distribution not in ("normal", "uniform", "beta", "weibull"):
            raise ValueError("Talent distribution must be normal, uniform, beta or weibull")
        if self.population_mode not in ("same", "fresh"):
            raise ValueError("Population mode must be same or fresh")
        if self.team_attractor not in ("mean", "sum"):
            raise ValueError("Team attractor must be mean or sum")
        if not isinstance(self.seats_option, bool):
            raise ValueError("Uncapped seats option must be True or False")
        if self.talent_scale not in ("original", "theoretical_mean_sd"):
            raise ValueError("Talent scale must be original or theoretical_mean_sd")
        if not np.isfinite(self.weibull_shape) or self.weibull_shape <= 0:
            raise ValueError("Weibull shape must be finite and positive")
        theoretical_moments(self)
        validate_initial_centroids(self.initial_centroids, self.n_teams)
        if not np.isfinite(self.theta_quantile) or not 0 < self.theta_quantile < 1:
            raise ValueError("Contender quantile must lie strictly between zero and one")
        path = Path(self.results_directory)
        if path.is_absolute() or '..' in path.parts or path.parts[:1] != ('results',):
            raise ValueError("Outputs must stay beneath project results/")

    def scientific_dict(self):
        values = asdict(self)
        values.pop("results_directory")
        values.update(model="uncapped_variable_rosters", rule=rule_name(self),
                      opportunity_multiplicity=("one_plus_actual_members"
                                                if self.seats_option else "one_per_team"),
                      initial_signal_update=("first_member_replaces_then_actual_member_mean"
                                             if self.team_attractor == "mean" else
                                             "first_member_replaces_then_actual_member_sum"),
                      variance_ddof=0,
                      pairing="shared_population_order_uniforms_across_rhos",
                      talent_source_sha256=hashlib.sha256(Path(__file__).with_name("talent.py").read_bytes()).hexdigest(),
                      core_source_sha256=hashlib.sha256(Path(__file__).with_name("experiment.py").read_bytes()).hexdigest())
        return values

    @property
    def unit_count(self):
        return self.assignment_repetitions * len(self.rhos)


def rule_name(settings):
    return MEMBER_OPPORTUNITY_RULE if settings.seats_option else RULE



def validate_initial_centroids(specification, n_teams):
    """Accept the population mean, one common value, or one value per team."""
    if isinstance(specification, str):
        if specification != "population_mean":
            raise ValueError('Initial centroids must be "population_mean", a finite number, or a list per team')
        return
    if isinstance(specification, (bool, np.bool_)):
        raise ValueError("Initial centroids must be numerical values, not booleans")
    if isinstance(specification, (list, tuple)) and any(isinstance(v, (bool, np.bool_)) for v in specification):
        raise ValueError("Initial centroids must be numerical values, not booleans")
    try:
        values = np.asarray(specification, dtype=float)
    except (TypeError, ValueError) as error:
        raise ValueError("Initial centroids must be finite numerical values") from error
    if values.ndim > 1 or (values.ndim == 1 and values.shape != (n_teams,)) or not np.all(np.isfinite(values)):
        raise ValueError("Supply one finite common centroid or exactly one finite centroid per team")


def resolve_initial_centroids(ability, n_teams, specification="population_mean"):
    """Initial attachment signals only: no seeded members, counts or prior weight."""
    validate_initial_centroids(specification, n_teams)
    if isinstance(specification, str):
        return np.full(n_teams, np.asarray(ability, dtype=float).mean())
    values = np.asarray(specification, dtype=float)
    return np.full(n_teams, values.item()) if values.ndim == 0 else values.copy()


def update_attractor(current, incoming_ability, new_team_size, team_attractor):
    """Update one team signal; its first real member replaces the imaginary signal."""
    if team_attractor not in ("mean", "sum"):
        raise ValueError("Team attractor must be mean or sum")
    if new_team_size < 1:
        raise ValueError("New team size must be positive")
    if new_team_size == 1:
        return float(incoming_ability)
    if team_attractor == "sum":
        return float(current + incoming_ability)
    return float(current + (incoming_ability-current)/new_team_size)


def expected_final_attractors(ability, team_ids, n_teams, initial, team_attractor):
    """Reconstruct final attachment signals from saved memberships."""
    sizes = np.bincount(team_ids, minlength=n_teams)
    sums = np.bincount(team_ids, weights=ability, minlength=n_teams)
    occupied = sizes > 0
    final = np.asarray(initial, dtype=float).copy()
    final[occupied] = (sums[occupied] if team_attractor == "sum"
                       else sums[occupied]/sizes[occupied])
    return final


def uncapped_assignment_probabilities(ability_i, attractors, team_sizes, rho,
                                      seats_option=False):
    """One base chance per team; optional extra chance per actual member."""
    attractors = np.asarray(attractors, dtype=float)
    sizes = np.asarray(team_sizes)
    if (sizes.shape != attractors.shape or sizes.ndim != 1 or sizes.dtype.kind not in 'iu'
            or np.any(sizes < 0)):
        raise ValueError("Team sizes must be matching nonnegative integers")
    if not isinstance(seats_option, (bool, np.bool_)):
        raise ValueError("Uncapped seats option must be True or False")
    opportunities = sizes + 1 if seats_option else np.ones_like(sizes)
    kernel = "seat_opportunities" if seats_option else "team_opportunities"
    return assignment_probabilities(ability_i, attractors, opportunities, rho, kernel)


def source_digest():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def run_id(settings):
    payload = json.dumps(settings.scientific_dict(), sort_keys=True, allow_nan=False)
    return "uncapped-" + hashlib.sha256(payload.encode()).hexdigest()[:12] + '-' + source_digest()[:12]


def run_directory(settings, project_root=PROJECT_ROOT):
    settings.validate()
    root = Path(project_root).resolve()
    folder = (root / settings.results_directory / run_id(settings)).resolve()
    if root not in folder.parents:
        raise ValueError("Output would escape the LG exploration folder")
    return folder


def export_settings(settings, project_root=PROJECT_ROOT):
    run_directory(settings, project_root)
    root = Path(project_root).resolve()
    folder = root / "settings"
    if root not in folder.resolve().parents:
        raise ValueError("Settings would escape the project")
    folder.mkdir(exist_ok=True)
    path = folder / "uncapped_rosters.json"
    atomic_text(path, json.dumps(asdict(settings), indent=2) + '\n')
    return path


def assign_uncapped(ability, n_teams, rho, order, uniforms,
                    initial_centroids="population_mean", team_attractor="mean",
                    seats_option=False):
    ability = np.asarray(ability, dtype=float)
    order, uniforms = np.asarray(order), np.asarray(uniforms, dtype=float)
    if ability.ndim != 1 or ability.size < 2 or not np.all(np.isfinite(ability)):
        raise ValueError("Talent must be a finite vector with at least two players")
    n = len(ability)
    if isinstance(n_teams, bool) or not isinstance(n_teams, int) or n_teams < 1:
        raise ValueError("Team count must be a positive integer")
    if order.dtype.kind not in 'iu' or order.shape != (n,) or not np.array_equal(np.sort(order), np.arange(n)):
        raise ValueError("Arrival order must be a permutation of player IDs")
    if uniforms.shape != (n,) or not np.all((uniforms >= 0) & (uniforms < 1)):
        raise ValueError("Supply one uniform in [0,1) per arrival")
    attractors = resolve_initial_centroids(ability, n_teams, initial_centroids)
    sizes = np.zeros(n_teams, dtype=np.int64)
    team_ids = np.full(n, -1, dtype=np.int64)
    for step, player in enumerate(order):
        # The n_j+1 copies, when enabled, all use this team's one current attractor.
        probabilities = uncapped_assignment_probabilities(
            ability[player], attractors, sizes, rho, seats_option)
        cdf = np.cumsum(probabilities)
        cdf[-1] = 1.
        team = int(np.searchsorted(cdf, uniforms[step], side='right'))
        team_ids[player] = team
        sizes[team] += 1
        # The imaginary starting value has no permanent weight. The first real
        # member replaces it; subsequent signals follow the selected rule.
        attractors[team] = update_attractor(
            attractors[team], ability[player], sizes[team], team_attractor)
    return team_ids, attractors


def describe_uncapped(ability, team_ids, n_teams):
    ability, ids = np.asarray(ability, dtype=float), np.asarray(team_ids)
    if isinstance(n_teams, bool) or not isinstance(n_teams, int) or n_teams < 1:
        raise ValueError("Team count must be a positive integer")
    if (ability.ndim != 1 or len(ability) < 2 or not np.all(np.isfinite(ability))
            or ids.shape != ability.shape or ids.dtype.kind not in 'iu'
            or np.any(ids < 0) or np.any(ids >= n_teams)):
        raise ValueError("Supply finite talents and valid integer team IDs")
    sizes = np.bincount(ids, minlength=n_teams)
    occupied = sizes > 0
    means = np.full(n_teams, np.nan)
    means[occupied] = np.bincount(ids, weights=ability, minlength=n_teams)[occupied] / sizes[occupied]
    residuals = (ability - means[ids]) ** 2
    variances = np.full(n_teams, np.nan)
    variances[occupied] = np.bincount(ids, weights=residuals, minlength=n_teams)[occupied] / sizes[occupied]
    total_variance = float(ability.var(ddof=0))
    if total_variance <= 0:
        raise ValueError("Sorting is undefined for constant talent")
    within = float(residuals.mean())
    between = float(np.sum(sizes[occupied] * (means[occupied]-ability.mean())**2) / len(ability))
    np.testing.assert_allclose(within+between, total_variance, rtol=1e-11, atol=1e-12)
    return dict(team_sizes=sizes, team_means=means, team_variances=variances,
                h_sort=between/total_variance, between_variance=between,
                mean_within_variance=within, centroid_sd=np.sqrt(between),
                empty_teams=int(np.sum(~occupied)), occupied_teams=int(occupied.sum()),
                largest_roster=int(sizes.max()), roster_sd=float(sizes.std(ddof=0)))


def random_reference(settings):
    # At rho=0 the baseline is uniform when seats_option=False and a symmetric
    # Polya urn with one initial opportunity per team when seats_option=True.
    if settings.seats_option:
        empty = (0. if settings.n_teams == 1 else
                 settings.n_teams*(settings.n_teams-1)
                 /(settings.n_teams+settings.n_players-1))
    else:
        empty = settings.n_teams * (1-1/settings.n_teams)**settings.n_players
    occupied = settings.n_teams-empty
    return dict(expected_empty_teams=empty, expected_h_sort=(occupied-1)/(settings.n_players-1),
                mean_roster=settings.n_players/settings.n_teams)


def load_unit(path, settings, rho, repetition):
    with np.load(path, allow_pickle=False) as archive:
        unit = {k: archive[k].copy() for k in archive.files}
    for key, value in [('run_id', run_id(settings)), ('source_sha256', source_digest()),
                       ('rho', rho), ('repetition', repetition), ('rule', rule_name(settings))]:
        if unit[key].item() != value:
            raise ValueError(f"Checkpoint mismatch: {key}")
    raw, ability = draw_population(settings, repetition)
    order, uniforms = draw_inputs(settings, repetition)
    for key, value in [('original_draws',raw),('ability',ability),('arrival_order',order),
                       ('choice_uniforms',uniforms),('player_id',np.arange(settings.n_players))]:
        if not np.array_equal(unit[key], value):
            raise ValueError(f"Checkpoint inputs mismatch: {key}")
    if unit['population_seed'].item()!=settings.population_seed or unit['assignment_seed'].item()!=settings.assignment_seed:
        raise ValueError("Checkpoint seeds mismatch")
    summary = describe_uncapped(ability, unit['team_id'], settings.n_teams)
    for key, value in summary.items():
        if not np.allclose(unit[key],value,rtol=1e-12,atol=1e-12,equal_nan=True):
            raise ValueError(f"Checkpoint statistics mismatch: {key}")
    initial = resolve_initial_centroids(ability, settings.n_teams, settings.initial_centroids)
    if not np.array_equal(unit['initial_centroids'], initial):
        raise ValueError("Checkpoint initial team centroids mismatch")
    signals = expected_final_attractors(
        ability, unit['team_id'], settings.n_teams, initial, settings.team_attractor)
    if (unit['final_attractors'].shape != signals.shape
            or not np.allclose(unit['final_attractors'], signals, rtol=1e-12, atol=1e-12)):
        raise ValueError("Checkpoint final attractor signals mismatch")
    return unit


def run_uncapped(settings, project_root=PROJECT_ROOT, progress=print):
    """Only call when Charles turns on the notebook execution switch."""
    folder = run_directory(settings, project_root)
    (folder/'divisions').mkdir(parents=True, exist_ok=True)
    metadata = dict(run_id=run_id(settings),settings=settings.scientific_dict(),
                    division_count=settings.unit_count,status='running',**random_reference(settings))
    atomic_text(folder/'run_metadata.json',json.dumps(metadata,indent=2)+'\n')
    event(folder,status='started',total=settings.unit_count)
    records=[]; computed=reused=0; start=time.perf_counter()
    try:
        for rep in range(settings.assignment_repetitions):
            raw, ability=draw_population(settings,rep)
            order, uniforms=draw_inputs(settings,rep)
            initial = resolve_initial_centroids(ability, settings.n_teams, settings.initial_centroids)
            for rho in settings.rhos:
                path=unit_path(folder,rho,rep,rule_name(settings))
                if path.exists():
                    unit=load_unit(path,settings,rho,rep);reused+=1
                else:
                    ids,attractors=assign_uncapped(
                        ability, settings.n_teams, rho, order, uniforms,
                        initial_centroids=initial, team_attractor=settings.team_attractor,
                        seats_option=settings.seats_option)
                    summary=describe_uncapped(ability,ids,settings.n_teams)
                    expected = expected_final_attractors(
                        ability, ids, settings.n_teams, initial, settings.team_attractor)
                    np.testing.assert_allclose(attractors, expected, rtol=1e-12, atol=1e-12)
                    atomic_npz(path,player_id=np.arange(settings.n_players),original_draws=raw,ability=ability,
                               team_id=ids,final_attractors=attractors,initial_centroids=initial,
                               arrival_order=order,choice_uniforms=uniforms,run_id=run_id(settings),
                               source_sha256=source_digest(),rule=rule_name(settings),rho=rho,repetition=rep,
                               population_seed=settings.population_seed,assignment_seed=settings.assignment_seed,
                               **summary)
                    unit=load_unit(path,settings,rho,rep);computed+=1
                records.append({k:unit[k].item() for k in ['rho','repetition','h_sort','empty_teams',
                                'occupied_teams','largest_roster','roster_sd','centroid_sd','mean_within_variance']})
                event(folder,status='division_ready',completed=len(records),total=settings.unit_count,rho=rho,repetition=rep)
                if progress:progress(f"Uncapped {len(records)}/{settings.unit_count}; rho={rho:g}, repetition={rep+1}; "
                                     f"{computed} new, {reused} reused; {time.perf_counter()-start:.1f}s")
        save_summary(folder,records)
        metadata.update(status='complete',newly_computed=computed,reused=reused,elapsed_seconds=time.perf_counter()-start)
        atomic_text(folder/'run_metadata.json',json.dumps(metadata,indent=2)+'\n')
        event(folder,status='complete',newly_computed=computed,reused=reused)
    except BaseException as error:
        metadata.update(status='interrupted' if isinstance(error,KeyboardInterrupt) else 'error',
                        completed=len(records),error=repr(error))
        atomic_text(folder/'run_metadata.json',json.dumps(metadata,indent=2)+'\n')
        event(folder,status=metadata['status'],completed=len(records),error=repr(error))
        raise
    return folder


def load_complete(settings, project_root=PROJECT_ROOT):
    folder=run_directory(settings,project_root)
    metadata=folder/'run_metadata.json'
    if not metadata.exists() or json.loads(metadata.read_text()).get('status')!='complete':
        raise FileNotFoundError("Uncapped run is not complete. Use its notebook switch to run/resume first.")
    units=[load_unit(unit_path(folder,rho,rep,rule_name(settings)),settings,rho,rep)
           for rep in range(settings.assignment_repetitions) for rho in settings.rhos]
    return folder,units


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--settings',type=Path,default=PROJECT_ROOT/'settings/uncapped_rosters.json')
    parser.add_argument('--run',action='store_true')
    parser.add_argument('--plots',action='store_true')
    args=parser.parse_args()
    settings=UncappedSettings.from_dict(json.loads(args.settings.read_text()))
    print(json.dumps(asdict(settings),indent=2));print(f"Divisions: {settings.unit_count}")
    if args.run:run_uncapped(settings)
    if args.plots:
        from .uncapped_plots import plot_uncapped
        import matplotlib.pyplot as plt
        figures,_=plot_uncapped(settings)
        for fig in figures.values():plt.close(fig)
    if not args.run and not args.plots:print('Configuration preview only; no experiment executed.')


if __name__=='__main__':main()
