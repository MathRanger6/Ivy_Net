"""Hard-threshold contender counts from already saved fixed-roster divisions.

This is a descriptive competition diagnostic, separate from SCORE and SELECT.
It does not replace the legacy smooth, self-included mean congestion equation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path

import numpy as np

from .experiment import (
    PROJECT_ROOT, RULES, RULE_LABELS, Settings, atomic_text, load_complete,
)


def contender_counts(ability, team_ids, n_teams, theta):
    """A strict A > theta cut; competitors exclude the focal player."""
    ability = np.asarray(ability, dtype=float)
    team_ids = np.asarray(team_ids)
    if not np.isfinite(theta) or not np.all(np.isfinite(ability)):
        raise ValueError("Talent and theta must be finite")
    if ability.ndim != 1 or team_ids.shape != ability.shape or team_ids.dtype.kind not in "iu":
        raise ValueError("Supply matching talent and integer team-ID vectors")
    if n_teams < 1 or np.any(team_ids < 0) or np.any(team_ids >= n_teams):
        raise ValueError("Invalid team IDs")
    is_contender = ability > theta
    team_counts = np.bincount(team_ids[is_contender], minlength=n_teams)
    teammate_counts = team_counts[team_ids] - is_contender.astype(np.int64)
    return is_contender, team_counts, teammate_counts


def _pmf(values, maximum):
    """Fraction of the specified teams or players at each integer count."""
    if len(values) == 0:
        raise ValueError("The requested diagnostic group is empty")
    if np.any(values < 0) or np.any(values > maximum):
        raise ValueError("Count outside its roster-size support")
    return np.bincount(values, minlength=maximum + 1) / len(values)


def _csv_text(records):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)
    return stream.getvalue()


def plot_contender_diagnostic(settings, project_root=PROJECT_ROOT, theta_quantile=.9):
    if not np.isfinite(theta_quantile) or not 0 < theta_quantile < 1:
        raise ValueError("Use a theta quantile strictly between 0 and 1")
    directory, units = load_complete(settings, project_root)
    ability = units[0]["ability"]
    # One realized population threshold, frozen across rules, rho and repetitions.
    theta = float(np.quantile(ability, theta_quantile, method="linear"))
    contender_total = int(np.sum(ability > theta))
    if not 0 < contender_total < settings.n_players:
        raise ValueError("This diagnostic requires both contenders and other players")
    spec = dict(theta_quantile=float(theta_quantile), quantile_method="linear",
                comparison="ability > theta", focal_exclusion=True,
                source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    diagnostic_id = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()[:12]
    destination = directory / "diagnostics" / f"contenders-{diagnostic_id}"
    destination.mkdir(parents=True, exist_ok=True)
    metadata = dict(**spec, theta=theta, contender_count=contender_total,
                    contender_fraction=contender_total / settings.n_players,
                    source_run_id=directory.name,
                    mean_contenders_per_team=contender_total / settings.n_teams,
                    mean_contender_teammates_all_players=
                        contender_total * (settings.roster_size - 1) / settings.n_players,
                    note="Descriptive hard-threshold counts; no SCORE or SELECT.")
    records, histograms, derived = [], [], []
    for unit in units:
        flag, team_counts, peer_counts = contender_counts(
            unit["ability"], unit["team_id"], settings.n_teams, theta)
        # Same contender population in every saved assignment.
        if int(flag.sum()) != contender_total:
            raise ValueError("Population contender count changed")
        if team_counts.sum() != contender_total:
            raise ValueError("Team contender counts do not conserve contenders")
        expected_peer_sum = contender_total * (settings.roster_size - 1)
        if int(peer_counts.sum()) != expected_peer_sum:
            raise ValueError("Teammate-count conservation failed")
        identifier = dict(rule=unit["rule"].item(), rho=float(unit["rho"]),
                          repetition=int(unit["repetition"]))
        records.append(dict(**identifier, theta=theta, contender_count=contender_total,
                            mean_contenders_per_team=float(team_counts.mean()),
                            mean_peers_all_players=float(peer_counts.mean()),
                            mean_peers_contenders=float(peer_counts[flag].mean()),
                            mean_peers_other_players=float(peer_counts[~flag].mean()),
                            fraction_teams_without_contenders=float(np.mean(team_counts == 0)),
                            fraction_contenders_without_contender_peers=
                                float(np.mean(peer_counts[flag] == 0)),
                            fraction_other_players_without_contender_peers=
                                float(np.mean(peer_counts[~flag] == 0))))
        groups = [
            ("teams", team_counts, settings.roster_size),
            ("contender_players", peer_counts[flag], settings.roster_size - 1),
            ("other_players", peer_counts[~flag], settings.roster_size - 1),
        ]
        item = dict(**identifier)
        for group, counts, maximum in groups:
            pmf = _pmf(counts, maximum)
            item[group] = pmf
            for count, fraction in enumerate(pmf):
                histograms.append(dict(**identifier, group=group, count=count,
                                       denominator=len(counts), fraction=float(fraction)))
        derived.append(item)
    atomic_text(destination / "diagnostic_metadata.json", json.dumps(metadata, indent=2) + "\n")
    atomic_text(destination / "division_contender_summary.csv", _csv_text(records))
    atomic_text(destination / "count_distributions.csv", _csv_text(histograms))

    cache = Path(project_root) / "results" / ".matplotlib"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib.pyplot as plt

    # Lower rho is lighter; rank by value even if the notebook list is reordered.
    rho_ranks = np.argsort(np.argsort(np.asarray(settings.rhos)))
    colors = plt.get_cmap("viridis")(np.linspace(.9, .08, len(settings.rhos))[rho_ranks])
    context = (f"M={settings.n_players:,}; J={settings.n_teams}; r={settings.roster_size}; "
               f"{settings.assignment_repetitions} paired assignments per rho")
    threshold_caption = (f"theta = population {100 * theta_quantile:g}th percentile "
                         f"= {theta:.3f} talent units; A > theta; {contender_total} contenders")
    figures = {}

    def draw(ax, rule, group, maximum):
        x = np.arange(maximum + 1)
        for rho, color in zip(settings.rhos, colors):
            curves = np.array([item[group] for item in derived
                               if item["rule"] == rule and item["rho"] == rho])
            mean = curves.mean(axis=0)
            sd = curves.std(axis=0, ddof=1) if len(curves) > 1 else np.zeros_like(mean)
            ax.plot(x, mean, color=color, linewidth=2, marker="o", markersize=3,
                    label=f"rho={rho:g}")
            ax.fill_between(x, np.maximum(0, mean - sd), np.minimum(1, mean + sd),
                            color=color, alpha=.08)
        ax.set_xlim(-.3, maximum + .3)
        # These are discrete counts; connected lines guide the eye, not a density fit.
        ax.set_xticks(np.arange(0, maximum + 1, 2))
        ax.set_ylim(0, 1)
        ax.grid(alpha=.18)
        ax.legend(fontsize=8)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.6), sharex=True, sharey=True)
    for ax, rule in zip(axes, RULES):
        draw(ax, rule, "teams", settings.roster_size)
        ax.set(title=RULE_LABELS[rule], xlabel="Number of contenders on a team (players)")
    axes[0].set_ylabel("Fraction of teams with exactly this count")
    fig.suptitle("Are draft contenders spread out or concentrated together?\n"
                 + threshold_caption)
    fig.text(.5, .04, context + "\nMean contenders per team is fixed at "
             f"{contender_total / settings.n_teams:g}; concentration can change. "
             "Shading: +/-1 assignment SD.", ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .13, 1, .91))
    figures["team_contender_counts"] = fig

    fig, axes = plt.subplots(2, 2, figsize=(12, 9.2), sharex=True, sharey=True)
    for row, (group, label, size) in enumerate([
        ("contender_players", "Contender players (A > theta)", contender_total),
        ("other_players", "Other players (A <= theta)", settings.n_players - contender_total),
    ]):
        for col, rule in enumerate(RULES):
            ax = axes[row, col]
            draw(ax, rule, group, settings.roster_size - 1)
            ax.set_title(RULE_LABELS[rule] + "\n" + label)
            ax.set_xlabel("Number of contender teammates (self excluded)")
            if col == 0:
                ax.set_ylabel(f"Fraction of {size:,} players\nwith exactly this count")
    fig.suptitle("How many contender teammates does a player face?\n" + threshold_caption)
    fig.text(.5, .028, context + "\nCurves average division-level fractions; "
             "shading: +/-1 assignment SD. Each contender is excluded from their own count.\n"
             "Hard-threshold diagnostic only; no scoring or draft selections.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .12, 1, .93), h_pad=2.5)
    figures["contender_teammate_counts"] = fig
    for name, figure in figures.items():
        figure.savefig(destination / f"{name}.png", dpi=160, bbox_inches="tight")
        figure.savefig(destination / f"{name}.svg", bbox_inches="tight")
    return figures, destination, metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path,
                        default=PROJECT_ROOT / "settings/composition_first.json")
    parser.add_argument("--diagnostic-settings", type=Path,
                        default=PROJECT_ROOT / "settings/contender_diagnostic.json")
    args = parser.parse_args()
    settings = Settings.from_dict(json.loads(args.settings.read_text()))
    diagnostic = json.loads(args.diagnostic_settings.read_text())
    figures, destination, metadata = plot_contender_diagnostic(
        settings, theta_quantile=diagnostic["theta_quantile"])
    import matplotlib.pyplot as plt
    for figure in figures.values():
        plt.close(figure)
    print(json.dumps(metadata, indent=2))
    print(f"Contender figures and data saved: {destination}")


if __name__ == "__main__":
    main()
