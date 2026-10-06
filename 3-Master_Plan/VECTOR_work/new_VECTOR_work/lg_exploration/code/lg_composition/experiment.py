"""Compare seat opportunities with one opportunity per open team.

The LG seat rule is adapted from the supplied reference snapshot of
sports/541_grandchild_homophily_assign.py. The second rule is an explicitly
different assignment mechanism. Both fill identical prescribed rosters here.
No legacy imports, empirical data, or parent-repository paths are used.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

RULES = ("seat_opportunities", "team_opportunities")
RULE_LABELS = {
    "seat_opportunities": "LG: remaining-seat opportunities",
    "team_opportunities": "Alternative: one opportunity per open team",
}
PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    n_players: int = 2000
    n_teams: int = 100
    roster_size: int = 20
    rhos: tuple[float, ...] = (0., .5, 1., 2., 4.)
    assignment_repetitions: int = 30
    population_seed: int = 6102026
    assignment_seed: int = 6102027
    results_directory: str = "results/composition_first"

    @classmethod
    def from_dict(cls, value):
        value = dict(value)
        value["rhos"] = tuple(value["rhos"])
        result = cls(**value)
        result.validate()
        return result

    def validate(self):
        for name in ("n_players", "n_teams", "roster_size",
                     "assignment_repetitions", "population_seed", "assignment_seed"):
            value = getattr(self, name)
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be an integer")
        if min(self.n_players, self.n_teams, self.roster_size,
               self.assignment_repetitions) <= 0:
            raise ValueError("Population, teams, roster size and repetitions must be positive")
        if min(self.population_seed, self.assignment_seed) < 0:
            raise ValueError("Seeds must be nonnegative")
        if self.n_players != self.n_teams * self.roster_size:
            raise ValueError("This demonstration requires total capacity exactly equal to M")
        if not self.rhos or any(not np.isfinite(r) or r < 0 for r in self.rhos):
            raise ValueError("rho values must be finite and nonnegative")
        if len(set(self.rhos)) != len(self.rhos):
            raise ValueError("rho values must be distinct")
        if 0. not in self.rhos:
            raise ValueError("Include rho=0 as the random-assignment reference")
        relative = Path(self.results_directory)
        if relative.is_absolute() or ".." in relative.parts or relative.parts[:1] != ("results",):
            raise ValueError("Use a project-local path beneath results/")

    @property
    def unit_count(self):
        return len(RULES) * len(self.rhos) * self.assignment_repetitions

    def scientific_dict(self):
        value = asdict(self)
        value.pop("results_directory")
        value.update(distribution="standard_normal", population_repetitions=1,
                     transformation="theoretical_mean_sd", variance_ddof=0,
                     rules=list(RULES), numerical_policy="shifted_log_weights",
                     pairing="same_order_and_uniforms_across_rules_and_rhos")
        return value


def code_digest():
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def run_id(settings):
    payload = json.dumps(settings.scientific_dict(), sort_keys=True, allow_nan=False)
    scientific_hash = hashlib.sha256(payload.encode()).hexdigest()[:12]
    return f"composition-{scientific_hash}-{code_digest()[:12]}"


def run_directory(settings, project_root=PROJECT_ROOT):
    settings.validate()
    root = Path(project_root).resolve()
    destination = (root / settings.results_directory / run_id(settings)).resolve()
    if root not in destination.parents:
        raise ValueError("Output would escape this exploration folder")
    return destination


def assignment_probabilities(ability_i, centroids, remaining, rho, rule):
    """Only homophily is preference. R is remaining-seat multiplicity.

    Shift log weights before exponentiation. This is algebraically equivalent
    to normalizing the declared weights and avoids the legacy all-underflow
    fallback to uniform teams, which would change the scientific rule.
    """
    if rule not in RULES:
        raise ValueError(f"Unknown opportunity rule: {rule}")
    if not np.isfinite(rho) or rho < 0:
        raise ValueError("rho must be finite and nonnegative")
    centroids = np.asarray(centroids, dtype=float)
    remaining = np.asarray(remaining)
    if centroids.shape != remaining.shape or centroids.ndim != 1:
        raise ValueError("Centroids and remaining capacity must be matching vectors")
    open_teams = np.flatnonzero(remaining > 0)
    if not open_teams.size:
        raise ValueError("No open team remains")
    log_weights = -rho * np.abs(float(ability_i) - centroids[open_teams])
    if rule == "seat_opportunities":
        log_weights += np.log(remaining[open_teams])
    if not np.all(np.isfinite(log_weights)):
        raise ValueError("Nonfinite assignment log weights")
    weights = np.exp(log_weights - log_weights.max())
    probabilities = np.zeros(len(remaining), dtype=float)
    probabilities[open_teams] = weights / weights.sum()
    return probabilities


def draw_inputs(settings, repetition):
    # These stream identifiers and repetition IDs do not depend on scheduling,
    # rule, rho, grid position or the number of requested repetitions.
    order_rng = np.random.default_rng(
        np.random.SeedSequence([settings.assignment_seed, 1, repetition]))
    choice_rng = np.random.default_rng(
        np.random.SeedSequence([settings.assignment_seed, 2, repetition]))
    return order_rng.permutation(settings.n_players), choice_rng.random(settings.n_players)


def assign(ability, n_teams, roster_size, rho, rule, order, uniforms):
    ability = np.asarray(ability, dtype=float)
    order = np.asarray(order)
    uniforms = np.asarray(uniforms, dtype=float)
    n = len(ability)
    if ability.ndim != 1 or not np.all(np.isfinite(ability)):
        raise ValueError("Ability must be a finite vector")
    if n != n_teams * roster_size or min(n_teams, roster_size) <= 0:
        raise ValueError("Total capacity must equal the population")
    if order.shape != (n,) or not np.array_equal(np.sort(order), np.arange(n)):
        raise ValueError("Arrival order must be a permutation of player IDs")
    if uniforms.shape != (n,) or not np.all((uniforms >= 0) & (uniforms < 1)):
        raise ValueError("Supply one uniform draw in [0,1) per arrival")
    centroids = np.full(n_teams, ability.mean(), dtype=float)
    counts = np.zeros(n_teams, dtype=np.int64)
    groups = np.full(n, -1, dtype=np.int64)
    for step, player in enumerate(order):
        remaining = roster_size - counts
        probabilities = assignment_probabilities(
            ability[player], centroids, remaining, rho, rule)
        # The same inverse-CDF uniforms couple both rules. Their trajectories
        # may diverge; pairing does not imply identical team compositions.
        cumulative = np.cumsum(probabilities)
        cumulative[-1] = 1.0  # eliminate harmless floating-point end gaps
        team = int(np.searchsorted(cumulative, uniforms[step], side="right"))
        if remaining[team] <= 0:
            raise RuntimeError("Sampled a full team")
        groups[player] = team
        counts[team] += 1
        # With count=1, this replaces the initial population-mean signal.
        centroids[team] += (ability[player] - centroids[team]) / counts[team]
    if not np.all(counts == roster_size):
        raise RuntimeError("Final rosters do not fill their prescribed capacities")
    return groups, centroids


def describe(ability, groups, n_teams):
    ability = np.asarray(ability, dtype=float)
    groups = np.asarray(groups)
    if groups.shape != ability.shape or groups.dtype.kind not in "iu":
        raise ValueError("Group IDs must be an integer vector matching ability")
    if np.any(groups < 0) or np.any(groups >= n_teams):
        raise ValueError("Invalid group IDs")
    counts = np.bincount(groups, minlength=n_teams)
    if np.any(counts == 0):
        raise ValueError("This fixed-roster demonstration has no empty final teams")
    means = np.bincount(groups, weights=ability, minlength=n_teams) / counts
    residual_squared = (ability - means[groups]) ** 2
    variances = np.bincount(groups, weights=residual_squared, minlength=n_teams) / counts
    total_ss = float(np.sum((ability - ability.mean()) ** 2))
    if total_ss <= 0:
        raise ValueError("Sorting is undefined for a constant-talent population")
    h_sort = 1. - float(residual_squared.sum()) / total_ss
    # Population variances (ddof=0). Team variance is zero for a singleton.
    return dict(team_sizes=counts, team_means=means, team_variances=variances,
                h_sort=h_sort, centroid_sd=float(means.std(ddof=0)),
                mean_within_variance=float(np.average(variances, weights=counts)))


def atomic_npz(path, **arrays):
    path = Path(path)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=path.name + ".",
                                     suffix=".partial", delete=False) as handle:
        temporary = Path(handle.name)
        np.savez_compressed(handle, **arrays)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def atomic_text(path, content):
    path = Path(path)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     prefix=path.name + ".", suffix=".partial",
                                     delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def event(directory, **value):
    value["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
    with (directory / "progress.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def unit_path(directory, rho, repetition, rule):
    # float.hex is lossless and independent of rho's position in a sweep.
    rho_token = float(rho).hex().replace(".", "_").replace("+", "p").replace("-", "m")
    return directory / "divisions" / f"{rule}_rho-{rho_token}_rep-{repetition:03d}.npz"


def load_unit(path, settings, rho, repetition, rule, ability):
    with np.load(path, allow_pickle=False) as archive:
        unit = {name: archive[name].copy() for name in archive.files}
    for name, expected in (("run_id", run_id(settings)), ("source_sha256", code_digest()),
                           ("rule", rule), ("rho", rho), ("repetition", repetition)):
        if unit[name].item() != expected:
            raise ValueError(f"Checkpoint metadata mismatch: {path.name}, {name}")
    if not np.array_equal(unit["ability"], ability) or not np.array_equal(
            unit["original_draws"], ability):
        raise ValueError("Checkpoint population differs from configured normal draws")
    if not np.array_equal(unit["player_id"], np.arange(settings.n_players)):
        raise ValueError("Checkpoint player IDs mismatch")
    order, uniforms = draw_inputs(settings, repetition)
    if not np.array_equal(unit["arrival_order"], order) or not np.array_equal(
            unit["choice_uniforms"], uniforms):
        raise ValueError("Checkpoint random inputs mismatch")
    summary = describe(ability, unit["team_id"], settings.n_teams)
    if not np.all(summary["team_sizes"] == settings.roster_size):
        raise ValueError("Checkpoint roster sizes mismatch")
    for key, value in summary.items():
        if not np.allclose(unit[key], value, rtol=1e-12, atol=1e-12):
            raise ValueError(f"Checkpoint statistic mismatch: {key}")
    if not np.array_equal(unit["capacities"], summary["team_sizes"]):
        raise ValueError("Checkpoint capacities mismatch")
    return unit


def population(settings):
    # N(0,1) already has the desired theoretical mean and SD.
    # Keep realized sample moments; never forcibly sample-standardize.
    return np.random.default_rng(settings.population_seed).normal(size=settings.n_players)


def record(unit):
    return {key: unit[key].item() for key in
            ("rule", "rho", "repetition", "h_sort", "centroid_sd", "mean_within_variance")}


def save_summary(directory, records):
    import io
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)
    atomic_text(directory / "division_summary.csv", buffer.getvalue())


def run_experiment(settings, project_root=PROJECT_ROOT, progress=print):
    """Run only the explicitly requested fixed-roster demonstration, resumably."""
    settings.validate()
    directory = run_directory(settings, project_root)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "divisions").mkdir(exist_ok=True)
    started = time.perf_counter()
    ability = population(settings)
    metadata = dict(run_id=run_id(settings), scientific_settings=settings.scientific_dict(),
                    source_sha256=code_digest(), division_count=settings.unit_count,
                    population_mean=float(ability.mean()), population_sd=float(ability.std()),
                    expected_random_h=(settings.n_teams - 1) / (settings.n_players - 1),
                    source="reference_snapshot/sports/541_grandchild_homophily_assign.py",
                    status="running", note="One population; uncertainty across assignments only.")
    atomic_text(directory / "run_metadata.json", json.dumps(metadata, indent=2) + "\n")
    population_file = directory / "population.npz"
    if population_file.exists():
        with np.load(population_file, allow_pickle=False) as saved:
            if not np.array_equal(saved["ability"], ability):
                raise ValueError("Saved population mismatch; checkpoint preserved")
    else:
        atomic_npz(population_file, player_id=np.arange(settings.n_players),
                   original_draws=ability, ability=ability)
    event(directory, status="started", run_id=run_id(settings), total=settings.unit_count)
    records, computed, reused = [], 0, 0
    try:
        for repetition in range(settings.assignment_repetitions):
            order, uniforms = draw_inputs(settings, repetition)
            for rho in settings.rhos:
                for rule in RULES:
                    path = unit_path(directory, rho, repetition, rule)
                    if path.exists():
                        unit = load_unit(path, settings, rho, repetition, rule, ability)
                        reused += 1
                        status = "reused"
                    else:
                        groups, centroids = assign(ability, settings.n_teams,
                            settings.roster_size, rho, rule, order, uniforms)
                        summary = describe(ability, groups, settings.n_teams)
                        np.testing.assert_allclose(centroids, summary["team_means"],
                                                   rtol=1e-12, atol=1e-12)
                        atomic_npz(path, player_id=np.arange(settings.n_players),
                            original_draws=ability, ability=ability, team_id=groups,
                            capacities=np.full(settings.n_teams, settings.roster_size),
                            initial_centroid=ability.mean(), arrival_order=order,
                            choice_uniforms=uniforms, population_seed=settings.population_seed,
                            assignment_seed=settings.assignment_seed, run_id=run_id(settings),
                            source_sha256=code_digest(), rule=rule, rho=rho,
                            repetition=repetition, **summary)
                        unit = load_unit(path, settings, rho, repetition, rule, ability)
                        computed += 1
                        status = "completed"
                    records.append(record(unit))
                    elapsed = time.perf_counter() - started
                    event(directory, status=status, rule=rule, rho=rho,
                          repetition=repetition, completed=len(records),
                          total=settings.unit_count, elapsed_seconds=elapsed, path=str(path))
                    if progress:
                        progress(f"{len(records)}/{settings.unit_count} {status}: "
                                 f"{rule}, rho={rho:g}, repetition={repetition + 1}; "
                                 f"{elapsed:.1f}s")
        save_summary(directory, records)
        metadata.update(status="complete", newly_computed=computed, reused=reused,
                        elapsed_seconds=time.perf_counter() - started)
        atomic_text(directory / "run_metadata.json", json.dumps(metadata, indent=2) + "\n")
        event(directory, status="complete", newly_computed=computed, reused=reused,
              elapsed_seconds=metadata["elapsed_seconds"])
    except BaseException as error:
        metadata.update(status="interrupted" if isinstance(error, KeyboardInterrupt) else "error",
                        completed=len(records), error_type=type(error).__name__, error=str(error))
        atomic_text(directory / "run_metadata.json", json.dumps(metadata, indent=2) + "\n")
        event(directory, status=metadata["status"], error=repr(error), completed=len(records))
        raise
    return directory


def load_complete(settings, project_root=PROJECT_ROOT):
    directory = run_directory(settings, project_root)
    ability = population(settings)
    units = []
    for repetition in range(settings.assignment_repetitions):
        for rho in settings.rhos:
            for rule in RULES:
                path = unit_path(directory, rho, repetition, rule)
                if not path.exists():
                    raise FileNotFoundError(f"Division missing; resume the run first: {path}")
                units.append(load_unit(path, settings, rho, repetition, rule, ability))
    return directory, units


def plot_results(settings, project_root=PROJECT_ROOT):
    """Scientific figures; no independence assumption for pooled team values."""
    # Keep matplotlib's cache within the project when imported by notebook/CLI.
    cache = Path(project_root) / "results" / ".matplotlib"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from matplotlib.colors import Normalize

    directory, units = load_complete(settings, project_root)
    plot_dir = directory / "plots"
    plot_dir.mkdir(exist_ok=True)
    colors = plt.get_cmap("viridis")(np.linspace(.08, .9, len(settings.rhos)))
    figures = {}
    context = (f"M={settings.n_players:,}; J={settings.n_teams}; r={settings.roster_size}; "
               f"one N(0,1) population; {settings.assignment_repetitions} paired assignments")
    for metric, xlabel, title in [
        ("team_means", "Final team mean talent (standard-normal units)",
         "How far do team means differentiate?"),
        ("team_variances", "Within-team population variance (talent units squared)",
         "How similar are teammates within each roster?"),
    ]:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharex=True, sharey=True)
        all_values = np.concatenate([u[metric] for u in units])
        grid = np.linspace(min(0., all_values.min()) if metric == "team_variances"
                           else all_values.min(), all_values.max(), 400)
        for ax, rule in zip(axes, RULES):
            for color, rho in zip(colors, settings.rhos):
                group = [u for u in units if u["rule"].item() == rule and u["rho"] == rho]
                # Each curve is the average of division-level empirical CDFs.
                # Shading is +/- one assignment SD, not a CI from pooled teams.
                curves = np.array([np.searchsorted(np.sort(u[metric]), grid, side="right")
                                   / settings.n_teams for u in group])
                mean = curves.mean(axis=0)
                sd = curves.std(axis=0, ddof=1) if len(group) > 1 else np.zeros_like(mean)
                ax.plot(grid, mean, color=color, label=f"rho={rho:g}", linewidth=2)
                ax.fill_between(grid, np.maximum(0, mean - sd), np.minimum(1, mean + sd),
                                color=color, alpha=.09)
            ax.set(title=RULE_LABELS[rule], xlabel=xlabel, ylim=(0, 1))
            ax.grid(alpha=.18)
            ax.legend(fontsize=9)
        axes[0].set_ylabel("Fraction of teams at or below x")
        fig.suptitle(title)
        fig.text(.5, .015, context + "\nMean empirical CDF; shading: +/-1 SD across assignments.",
                 ha="center", fontsize=9)
        fig.tight_layout(rect=(0, .1, 1, .95))
        figures[metric] = fig

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    metrics = [("h_sort", "Division sorting H_sort", "Explained talent variance (fraction)"),
               ("centroid_sd", "Spread of team means", "SD (talent units)"),
               ("mean_within_variance", "Mean within-team variance", "Talent units squared")]
    for ax, (metric, title, ylabel) in zip(axes, metrics):
        for rule, color, marker in zip(RULES, ("#225ea8", "#bd4f00"), ("o", "s")):
            values = [[float(u[metric]) for u in units
                       if u["rule"].item() == rule and u["rho"] == rho]
                      for rho in settings.rhos]
            means = np.array([np.mean(v) for v in values])
            sds = np.array([np.std(v, ddof=1) if len(v) > 1 else 0 for v in values])
            ax.errorbar(settings.rhos, means, yerr=sds, color=color, marker=marker,
                        linestyle="-" if rule == RULES[0] else "--",
                        label=RULE_LABELS[rule], capsize=3)
        if metric == "h_sort":
            expected = (settings.n_teams - 1) / (settings.n_players - 1)
            ax.axhline(expected, color=".45", linestyle=":",
                       label=f"Random-grouping expectation = {expected:.4f}")
        ax.set(title=title, xlabel="Homophily rho", ylabel=ylabel)
        ax.grid(alpha=.18)
    axes[0].legend(fontsize=7)
    fig.text(.5, .015, context + "\nPoints: assignment means; bars: +/-1 assignment SD. "
             "These three summaries are mathematically related.", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .12, 1, 1))
    figures["division_summaries"] = fig

    fig, ax = plt.subplots(figsize=(8, 4.8))
    delta_means, delta_sds = [], []
    for rho in settings.rhos:
        difference = []
        for rep in range(settings.assignment_repetitions):
            pair = {u["rule"].item(): float(u["h_sort"]) for u in units
                    if u["rho"] == rho and u["repetition"] == rep}
            difference.append(pair[RULES[1]] - pair[RULES[0]])
        delta_means.append(np.mean(difference))
        delta_sds.append(np.std(difference, ddof=1) if len(difference) > 1 else 0.)
    ax.errorbar(settings.rhos, delta_means, yerr=delta_sds, color="#225ea8",
                marker="o", capsize=4)
    ax.axhline(0, color=".4", linestyle=":")
    ax.set(title="Paired change in sorting under one opportunity per team",
           xlabel="Homophily rho", ylabel="H_sort: team rule minus seat rule")
    ax.grid(alpha=.18)
    fig.text(.5, .015, context + "\nBars: +/-1 SD of paired assignment differences; "
             "positive means more sorting under the team rule.", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .12, 1, 1))
    figures["paired_sorting_difference"] = fig

    # Replicate zero is selected in advance, rather than choosing a dramatic run.
    fig, axes = plt.subplots(2, len(settings.rhos), figsize=(3 * len(settings.rhos), 8),
                             squeeze=False, sharex=True, sharey=True)
    norm = Normalize(vmin=population(settings).min(), vmax=population(settings).max())
    for row, rule in enumerate(RULES):
        for col, rho in enumerate(settings.rhos):
            unit = next(u for u in units if u["rule"].item() == rule
                        and u["rho"] == rho and u["repetition"] == 0)
            team_order = np.argsort(unit["team_means"], kind="stable")
            matrix = np.array([np.sort(unit["ability"][unit["team_id"] == team])
                               for team in team_order])
            shown = axes[row, col].imshow(matrix, aspect="auto", origin="lower",
                                         cmap="coolwarm", norm=norm)
            axes[row, col].set_title(f"rho={rho:g}; H_sort={float(unit['h_sort']):.3f}")
            if row == 1:
                axes[row, col].set_xlabel("Player position sorted by talent\nwithin team (zero-based)")
            if col == 0:
                axes[row, col].set_ylabel(
                    ("Seat opportunities" if row == 0 else "Team opportunities")
                    + "\nTeam rank by mean talent (zero-based)")
    fig.suptitle("Actual roster compositions: first paired assignment\n"
                 "Teams ranked separately in every panel; ranks do not match team identities.")
    fig.subplots_adjust(left=.08, right=.86, top=.87, bottom=.13, wspace=.22, hspace=.28)
    color_ax = fig.add_axes((.89, .2, .015, .6))
    fig.colorbar(shown, cax=color_ax, label="Player talent (standard-normal units)")
    fig.text(.5, .025, context + "\nIllustrative repetition 1; summaries above use all repetitions.",
             ha="center", fontsize=9)
    figures["roster_compositions"] = fig
    for name, figure in figures.items():
        figure.savefig(plot_dir / f"{name}.png", dpi=160, bbox_inches="tight")
        figure.savefig(plot_dir / f"{name}.svg", bbox_inches="tight")
    return figures, plot_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path,
                        default=PROJECT_ROOT / "settings/composition_first.json")
    parser.add_argument("--run", action="store_true", help="Execute the reviewed experiment")
    parser.add_argument("--plots", action="store_true", help="Plot a verified complete run")
    args = parser.parse_args()
    settings = Settings.from_dict(json.loads(args.settings.read_text()))
    print(json.dumps(asdict(settings), indent=2))
    print(f"{settings.unit_count} divisions; output: {run_directory(settings)}")
    if args.run:
        run_experiment(settings)
    if args.plots:
        figures, directory = plot_results(settings)
        import matplotlib.pyplot as plt
        for figure in figures.values():
            plt.close(figure)
        print(f"Figures saved: {directory}")
    if not args.run and not args.plots:
        print("Settings preview only. Add --run --plots to execute and plot.")


if __name__ == "__main__":
    main()
