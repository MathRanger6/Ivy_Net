"""Additional absolute H_sort comparison using verified saved divisions.

Kept separate from experiment.py so a presentation change does not change the
scientific implementation digest or invalidate previously generated divisions.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import numpy as np

from .experiment import PROJECT_ROOT, RULES, RULE_LABELS, Settings, load_complete


def plot_sorting_comparison(settings, project_root=PROJECT_ROOT):
    directory, units = load_complete(settings, project_root)
    cache = Path(project_root) / "results" / ".matplotlib"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(9, 6))
    for rule, color, marker, linestyle in zip(
        RULES, ("#225ea8", "#bd4f00"), ("o", "s"), ("-", "--")
    ):
        values = [
            np.array([float(unit["h_sort"]) for unit in units
                      if unit["rule"].item() == rule and float(unit["rho"]) == rho])
            for rho in settings.rhos
        ]
        # Faint dots are the actual division-level H_sort observations.
        # Each connected marker is their mean, conditional on this population.
        for rho, observations in zip(settings.rhos, values):
            ax.scatter(np.full(len(observations), rho), observations, color=color,
                       marker=marker, alpha=.18, s=18, linewidths=0, zorder=2)
        means = [observations.mean() for observations in values]
        sds = [observations.std(ddof=1) if len(observations) > 1 else 0.
               for observations in values]
        ax.errorbar(settings.rhos, means, yerr=sds, color=color, marker=marker,
                    linestyle=linestyle, linewidth=2, markersize=6, capsize=4,
                    label=RULE_LABELS[rule], zorder=3)
    expected = (settings.n_teams - 1) / (settings.n_players - 1)
    ax.axhline(expected, color=".45", linestyle=":", linewidth=1.4,
               label=f"Random-grouping expectation at rho=0: {expected:.4f}")
    ax.set(title="Actual sorting under both opportunity rules",
           xlabel="Homophily rho",
           ylabel="Division H_sort (fraction of talent variance explained)",
           ylim=(0, 1))
    ax.set_xticks(settings.rhos)
    ax.grid(alpha=.18)
    ax.legend(fontsize=9, loc="best")
    fig.text(.5, .055,
             f"M={settings.n_players:,}; J={settings.n_teams}; "
             f"r={settings.roster_size}; one N(0,1) population; "
             f"{settings.assignment_repetitions} paired assignments per rho\n"
             "Dots: individual divisions. Lines: means. Bars: +/-1 assignment SD.",
             ha="center", fontsize=9)
    fig.text(.5, .012, f"Source: verified saved divisions | {directory.name}",
             ha="center", fontsize=8, color=".4")
    fig.tight_layout(rect=(0, .13, 1, 1))
    plot_directory = directory / "plots"
    plot_directory.mkdir(exist_ok=True)
    fig.savefig(plot_directory / "sorting_comparison.png", dpi=160, bbox_inches="tight")
    fig.savefig(plot_directory / "sorting_comparison.svg", bbox_inches="tight")
    return fig, plot_directory


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path,
                        default=PROJECT_ROOT / "settings/composition_first.json")
    args = parser.parse_args()
    settings = Settings.from_dict(json.loads(args.settings.read_text()))
    fig, directory = plot_sorting_comparison(settings)
    import matplotlib.pyplot as plt
    plt.close(fig)
    print(f"Saved absolute sorting comparison: {directory}")


if __name__ == "__main__":
    main()
