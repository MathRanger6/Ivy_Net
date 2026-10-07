"""Parameter-named figures for completed notebook-selected scenarios."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import numpy as np
from .experiment import PROJECT_ROOT, RULE_LABELS, atomic_text, code_digest, run_directory
from .contender_plot import contender_counts
from .talent import draw_population


def _number(value):
    return format(float(value), ".12g").replace("-", "m").replace(".", "p").replace("+", "")


def figure_stem(metric, batch, scenarios):
    """Human-readable parameters plus a digest; no anonymous plot filenames."""
    tags = "-vs-".join(s.slug for s in scenarios)
    if metric.startswith("player_talent_distribution"):
        tags = "-vs-".join(f"M{s.n_players}_reps{s.repetitions}" for s in scenarios)
    if len(tags) > 75:
        tags = f"{len(scenarios)}scenarios"
    grid = "-".join(_number(r) for r in batch.rhos)
    if len(grid) > 60:
        grid = f"{len(batch.rhos)}values-{_number(min(batch.rhos))}-to-{_number(max(batch.rhos))}"
    context = dict(batch=batch.as_dict(), plotted_scenarios=[s.as_tuple() for s in scenarios],
                   metric=metric, kernel_sha256=code_digest(),
                   plotting_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    digest = hashlib.sha256(json.dumps(context, sort_keys=True).encode()).hexdigest()[:10]
    return (f"{metric}__{tags}__{batch.talent_slug}__rho{grid}__ps{batch.population_seed}"
            f"_as{batch.assignment_seed}_q{_number(batch.theta_quantile)}__{digest}")


def _save(figure, metric, batch, scenarios, folder):
    folder.mkdir(parents=True, exist_ok=True)
    stem = figure_stem(metric, batch, scenarios)
    figure.savefig(folder / f"{stem}.png", dpi=160, bbox_inches="tight")
    figure.savefig(folder / f"{stem}.svg", bbox_inches="tight")
    atomic_text(folder / f"{stem}.json", json.dumps(
        dict(plot=metric, scenarios=[s.as_tuple() for s in scenarios], parameters=batch.as_dict(),
             kernel_sha256=code_digest()), indent=2) + "\n")
    return stem


def _pyplot(root):
    cache = Path(root) / "results" / ".matplotlib"
    cache.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("MPLCONFIGDIR", str(cache))
    import matplotlib.pyplot as plt
    return plt


def _caption(fig, text):
    fig.text(.5, .025, text, ha="center", fontsize=9)


def unique_population_scenarios(batch):
    """One preview per population size/repetition count, independent of team rule.

    Talent law, scale, shape and population seed are shared across a batch.
    Equal M and repetition count therefore give identical pooled talent values,
    even when team dimensions or opportunity rules differ.
    """
    seen = set()
    selected = []
    for scenario in batch.scenarios:
        key = (scenario.n_players, scenario.repetitions)
        if key not in seen:
            seen.add(key)
            selected.append(scenario)
    return selected


def plot_player_distribution(batch, scenario, project_root=PROJECT_ROOT, bins=40):
    """Preview all player appearances over repetitions before any assignments.

    Population mode chooses fixed or fresh draws. Count each player once per
    repetition, without multiplying by the rho grid or opportunity-rule choice.
    The preview uses exactly the same deterministic draws as the runner.
    """
    if isinstance(bins, bool) or not isinstance(bins, int) or bins < 1:
        raise ValueError("Talent histogram bins must be a positive integer")
    settings = batch.settings(scenario)
    directory = run_directory(settings, project_root)
    populations = [draw_population(settings, rep) for rep in range(scenario.repetitions)]
    pooled_raw = np.concatenate([raw for raw, _ in populations])
    pooled_ability = np.concatenate([ability for _, ability in populations])
    plt = _pyplot(project_root)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.8))
    for ax, values, label, color in zip(
            axes, (pooled_raw, pooled_ability),
            ("Original draws", "Talent used for assignment"), ("#238b45", "#225ea8")):
        ax.hist(values, bins=bins, density=True, color=color, alpha=.75,
                edgecolor="white", linewidth=.5)
        ax.set(title=f"{label}\nEmpirical mean={values.mean():.3f}; SD={values.std(ddof=0):.3f}",
               xlabel="Original talent units" if label == "Original draws" else "Assignment talent units",
               ylabel="Empirical probability density")
        ax.grid(axis="y", alpha=.18)
    fig.suptitle(f"Player talent distribution: M={scenario.n_players:,}; "
                 f"{scenario.repetitions} repetitions\n{batch.talent_label}")
    population_note = (f"{scenario.n_players:,} distinct players; one fixed population is reused."
                       if batch.population_mode == "same" else
                       f"{len(pooled_ability):,} independently generated player draws; fresh population each repetition.")
    _caption(fig, f"All {len(pooled_ability):,} player appearances across {scenario.repetitions} repetitions;\n"
             + population_note + " No extra copies across rho; density integrates to 1.")
    fig.tight_layout(rect=(0, .14, 1, .89))
    metric = f"player_talent_distribution_bins{bins}"
    _save(fig, metric, batch, [scenario], directory / "plots")
    return fig


def plot_scenario(batch, item, project_root=PROJECT_ROOT):
    """All individual-scenario diagnostics; never generates new assignments."""
    plt = _pyplot(project_root)
    scenario, units = item["scenario"], item["units"]
    directory = item["directory"]
    title = f"{scenario.chance}: {RULE_LABELS[scenario.rule]}"
    context = (f"J={scenario.n_teams}; r={scenario.roster_size}; M={scenario.n_players:,}; "
               f"{scenario.repetitions} repetitions per rho; {batch.talent_label}\n{batch.population_label}")
    # Lower rho is lighter; rank by value even if the notebook list is reordered.
    rho_ranks = np.argsort(np.argsort(np.asarray(batch.rhos)))
    colors = plt.get_cmap("viridis")(np.linspace(.9, .08, len(batch.rhos))[rho_ranks])
    figures = {}
    for metric, xlabel in [
        ("team_means", "Final team mean talent (talent units)"),
        ("team_variances", "Within-team population variance (talent units squared)"),
    ]:
        all_values = np.concatenate([u[metric] for u in units])
        low, high = float(all_values.min()), float(all_values.max())
        if low == high:
            low, high = low - .1, high + .1
        grid = np.linspace(low, high, 400)
        fig, ax = plt.subplots(figsize=(9, 5.5))
        for rho, color in zip(batch.rhos, colors):
            group = [u for u in units if float(u["rho"]) == rho]
            curves = np.array([np.searchsorted(np.sort(u[metric]), grid, side="right")
                               / scenario.n_teams for u in group])
            mean = curves.mean(axis=0)
            sd = curves.std(axis=0, ddof=1) if len(group) > 1 else np.zeros_like(mean)
            ax.plot(grid, mean, color=color, label=f"rho={rho:g}", linewidth=2)
            ax.fill_between(grid, np.maximum(0, mean-sd), np.minimum(1, mean+sd),
                            color=color, alpha=.08)
        ax.set(title=title, xlabel=xlabel, ylabel="Fraction of teams at or below x", ylim=(0,1))
        ax.grid(alpha=.18)
        ax.legend()
        _caption(fig, context + "\nMean division-level empirical CDF; shading: +/-1 repetition SD.")
        fig.tight_layout(rect=(0,.13,1,1))
        figures[metric] = fig

    fig, axes = plt.subplots(1,3,figsize=(14,4.8))
    scalar_metrics = [
        ("h_sort","Division H_sort","Explained talent variance (fraction)"),
        ("centroid_sd","Spread of team means","SD (talent units)"),
        ("mean_within_variance","Mean within-team variance","Talent units squared"),
    ]
    rhos = sorted(batch.rhos)
    for ax,(metric,label,ylabel) in zip(axes,scalar_metrics):
        values = [[float(u[metric]) for u in units if float(u["rho"])==r] for r in rhos]
        ax.errorbar(rhos, [np.mean(v) for v in values],
                    yerr=[np.std(v,ddof=1) if len(v)>1 else 0 for v in values],
                    color="#225ea8",marker="o",capsize=4)
        if metric=="h_sort":
            ax.axhline((scenario.n_teams-1)/(scenario.n_players-1),
                       color=".4",linestyle=":",label="rho=0 expectation")
            ax.legend(fontsize=8)
        ax.set(title=label,xlabel="Homophily rho",ylabel=ylabel)
        ax.grid(alpha=.18)
    fig.suptitle(title)
    _caption(fig,context+"\nMeans +/-1 repetition SD; these summaries share a variance decomposition.")
    fig.tight_layout(rect=(0,.15,1,.93))
    figures["division_summaries"]=fig

    from matplotlib.colors import Normalize
    ability=next(u["ability"] for u in units if int(u["repetition"])==0)
    fig,axes=plt.subplots(1,len(batch.rhos),figsize=(3*len(batch.rhos)+1,5.5),squeeze=False)
    norm=Normalize(float(ability.min()),float(ability.max()))
    for ax,rho in zip(axes[0],batch.rhos):
        unit=next(u for u in units if float(u["rho"])==rho and int(u["repetition"])==0)
        order=np.argsort(unit["team_means"],kind="stable")
        matrix=np.array([np.sort(ability[unit["team_id"]==team]) for team in order])
        image=ax.imshow(matrix,aspect="auto",origin="lower",cmap="coolwarm",norm=norm)
        ax.set(title=f"rho={rho:g}; H_sort={float(unit['h_sort']):.3f}",
               xlabel="Player position within team\n(sorted by talent, zero-based)")
    axes[0,0].set_ylabel("Team rank by mean talent (zero-based)")
    fig.suptitle(title+"\nActual rosters: first assignment, selected in advance")
    fig.subplots_adjust(left=.09,right=.86,bottom=.24,top=.81,wspace=.25)
    color_ax=fig.add_axes((.9,.29,.015,.46))
    fig.colorbar(image,cax=color_ax,label="Player talent (talent units)")
    _caption(fig,context+"\nEach panel sorts teams independently; row ranks are not matched identities.")
    figures["roster_compositions"]=fig

    derived=[]
    for unit in units:
        # Freeze each population's quantile across its rules and rho values.
        current_ability=unit["ability"]
        theta=float(np.quantile(current_ability,batch.theta_quantile,method="linear"))
        total=int(np.sum(current_ability>theta))
        if not 0<total<scenario.n_players:
            raise ValueError("Contender diagnostic requires contenders and other players")
        flag,counts,peers=contender_counts(current_ability,unit["team_id"],scenario.n_teams,theta)
        if counts.sum()!=total or peers.sum()!=total*(scenario.roster_size-1):
            raise ValueError("Contender conservation failed")
        derived.append(dict(rho=float(unit["rho"]),counts=counts,theta=theta,total=total,
                            contenders=peers[flag],others=peers[~flag]))
    totals={d["total"] for d in derived}
    if len(totals)!=1:
        raise ValueError("Contender totals differ across continuous-law populations")
    total=next(iter(totals))

    def count_lines(ax,key,maximum):
        x=np.arange(maximum+1)
        for rho,color in zip(batch.rhos,colors):
            curves=np.array([np.bincount(d[key],minlength=maximum+1)/len(d[key])
                             for d in derived if d["rho"]==rho])
            mean=curves.mean(axis=0)
            sd=curves.std(axis=0,ddof=1) if len(curves)>1 else np.zeros_like(mean)
            ax.plot(x,mean,color=color,marker="o",markersize=3,label=f"rho={rho:g}")
            ax.fill_between(x,np.maximum(0,mean-sd),np.minimum(1,mean+sd),color=color,alpha=.08)
        ax.set_ylim(0,1)
        ax.set_xticks(np.unique(np.r_[np.arange(0,maximum+1,2),maximum]))
        ax.grid(alpha=.18)
        ax.legend(fontsize=8)

    theta_note=(f"theta={derived[0]['theta']:.3f}" if batch.population_mode=="same"
                else "theta recomputed per population, shared across rules/rho")
    threshold=f"theta quantile={batch.theta_quantile:g}; {theta_note}; {total} contenders (A > theta)"
    fig,ax=plt.subplots(figsize=(9,5.6))
    count_lines(ax,"counts",scenario.roster_size)
    ax.set(title=title+"\n"+threshold,xlabel="Contenders per team (players)",
           ylabel="Fraction of teams with exactly this count")
    _caption(fig,context+f"\nMean contenders/team is fixed at {total/scenario.n_teams:g}; "
             "shading: +/-1 repetition SD.")
    fig.tight_layout(rect=(0,.15,1,1))
    figures["team_contender_counts"]=fig
    fig,axes=plt.subplots(2,1,figsize=(9,8.5),sharex=True)
    for ax,key,label,denominator in zip(axes,("contenders","others"),
                                       ("Contender players (A > theta)","Other players (A <= theta)"),
                                       (total,scenario.n_players-total)):
        count_lines(ax,key,scenario.roster_size-1)
        ax.set(title=label,xlabel="Contender teammates (self excluded)",
               ylabel=f"Fraction of {denominator:,} players\nwith exactly this count")
    fig.suptitle(title+"\n"+threshold)
    _caption(fig,context+"\nDiscrete division-level fractions; shading: +/-1 repetition SD. "
             "No SCORE or SELECT.")
    fig.tight_layout(rect=(0,.12,1,.92))
    figures["contender_teammate_counts"]=fig

    for metric,figure in figures.items():
        _save(figure,metric,batch,[scenario],directory/"plots")
    return figures


def plot_comparisons(batch,ready,project_root=PROJECT_ROOT):
    """Absolute sorting for selected complete scenarios, plus eligible paired differences."""
    if not ready:
        return {}
    plt=_pyplot(project_root)
    rhos=sorted(batch.rhos)
    fig,ax=plt.subplots(figsize=(10,6))
    for index,item in enumerate(ready):
        scenario,units=item["scenario"],item["units"]
        color=plt.get_cmap("tab10")(index%10)
        values=[[float(u["h_sort"]) for u in units if float(u["rho"])==rho] for rho in rhos]
        ax.errorbar(rhos,[np.mean(v) for v in values],
                    yerr=[np.std(v,ddof=1) if len(v)>1 else 0 for v in values],
                    color=color,marker="o" if scenario.chance=="seats" else "s",
                    linestyle="-" if scenario.chance=="seats" else "--",capsize=4,
                    label=f"{scenario.chance}; J={scenario.n_teams}, r={scenario.roster_size}, "
                          f"M={scenario.n_players}, reps={scenario.repetitions}")
    ax.set(title="Actual H_sort across completed selected scenarios",xlabel="Homophily rho",
           ylabel="Division H_sort (explained talent variance fraction)",ylim=(0,1))
    ax.set_xticks(rhos)
    ax.grid(alpha=.18)
    ax.legend(fontsize=8)
    _caption(fig,f"Means +/-1 repetition SD; {batch.talent_label}.\n{batch.population_label}.\n"
             "Compare identical dimensions to isolate opportunity rules.")
    fig.tight_layout(rect=(0,.14,1,1))
    specs=[item["scenario"] for item in ready]
    folder=Path(project_root)/batch.results_directory/"comparisons"
    # Resolve through a validated scenario path to guard a symlink escape.
    if Path(project_root).resolve() not in folder.resolve().parents:
        raise ValueError("Comparison output would escape the project")
    _save(fig,"sorting_comparison",batch,specs,folder)
    figures={"sorting_comparison":fig}
    pairs={}
    for item in ready:
        s=item["scenario"]
        pairs.setdefault((s.n_teams,s.roster_size,s.repetitions),{})[s.chance]=item
    for dimensions,pair in pairs.items():
        if set(pair)!={"one","seats"}:
            continue
        fig,ax=plt.subplots(figsize=(9,5.5))
        means,sds=[],[]
        for rho in rhos:
            by_rule={name:{int(u["repetition"]):u for u in item["units"] if float(u["rho"])==rho}
                     for name,item in pair.items()}
            differences=[]
            for rep,one in by_rule["one"].items():
                seats=by_rule["seats"][rep]
                for key in ("ability","arrival_order","choice_uniforms"):
                    if not np.array_equal(one[key],seats[key]):
                        raise ValueError(f"Unpaired scenario inputs: {key}")
                differences.append(float(one["h_sort"])-float(seats["h_sort"]))
            means.append(np.mean(differences))
            sds.append(np.std(differences,ddof=1) if len(differences)>1 else 0.)
        ax.errorbar(rhos,means,yerr=sds,color="#225ea8",marker="o",capsize=4)
        ax.axhline(0,color=".4",linestyle=":")
        ax.set(title=f"Paired sorting difference: J={dimensions[0]}, r={dimensions[1]}, "
               f"reps={dimensions[2]}",xlabel="Homophily rho",ylabel="H_sort: one minus seats")
        ax.grid(alpha=.18)
        _caption(fig,"Mean difference +/-1 paired repetition SD; shared talent, arrival order and draws.")
        fig.tight_layout(rect=(0,.12,1,1))
        metric=f"paired_sorting_difference_J{dimensions[0]}_r{dimensions[1]}_reps{dimensions[2]}"
        _save(fig,metric,batch,[pair["one"]["scenario"],pair["seats"]["scenario"]],folder)
        figures[metric]=fig
    return figures
