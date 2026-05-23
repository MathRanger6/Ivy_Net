"""538 vs 539 assignment calibration — median roster SD + Plot A coverage overlap.

539: sort-and-chop on ``assortativity * A + (1-rho) * N(0,1)`` (Alex notebook).
538: soft assign to drawn team targets T_j with kernel temperature tau.

Uses the **same ability vector** for both paths so differences reflect assignment only.
Reads pool knobs from ``tier1_cell10_playground_state.json`` when present.
539 assignment ρ from ``tier1_539_reference_settings.json`` when present (saved by
``539_alex_model.ipynb``).

Run from 538D:
    from tier1_cell10_539_calibration_compare import display_calibration_panel
    display_calibration_panel(link_tau_widget=globals().get("w_tau"))

    # Automated τ search (538 soft assign → match 539 median SD + coverage peak):
    from tier1_cell10_539_calibration_compare import auto_calibrate_tau
    auto_calibrate_tau(
        apply_tau_widget=globals().get("w_tau"),
        persist_state=True,
    )
"""

from __future__ import annotations

import io
import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import tier1_pool_assignment as tpa
from tier1_generative_eda import assignment_params_from_state, load_playground_state


def _sports_dir() -> Path:
    here = Path(__file__).resolve().parent
    return here if (here / "tier1_sim_config.py").is_file() else here / "sports"


REFERENCE_539_SETTINGS_NAME = "tier1_539_reference_settings.json"
DEFAULT_ASSORTATIVITY = 0.88


def reference_539_settings_path(sports: Path | None = None) -> Path:
    sports = sports or _sports_dir()
    return sports / REFERENCE_539_SETTINGS_NAME


def load_539_reference_settings(sports: Path | None = None) -> dict:
    """Load settings written by ``539_alex_model.ipynb`` (or ``save_539_reference_settings``)."""
    path = reference_539_settings_path(sports)
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_539_reference_settings(
    *,
    sports: Path | None = None,
    assortativity: float,
    N: int | None = None,
    team_size: int | None = None,
    seed: int | None = None,
    **extra,
) -> Path:
    """Persist 539 run knobs for CELL 10b / ``auto_calibrate_tau``."""
    sports = sports or _sports_dir()
    payload: dict = {"assortativity": float(assortativity)}
    if N is not None:
        payload["N"] = int(N)
    if team_size is not None:
        payload["team_size"] = int(team_size)
        if N is not None:
            payload["n_teams"] = int(N) // int(team_size)
    if seed is not None:
        payload["seed"] = int(seed)
    for key, val in extra.items():
        if val is not None:
            payload[key] = val
    path = reference_539_settings_path(sports)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def resolve_assortativity(
    sports: Path | None = None,
    assortativity: float | None = None,
) -> float:
    """Explicit arg → ``tier1_539_reference_settings.json`` → default 0.88."""
    if assortativity is not None:
        return float(assortativity)
    ref = load_539_reference_settings(sports)
    if "assortativity" in ref:
        return float(ref["assortativity"])
    return float(DEFAULT_ASSORTATIVITY)


def assign_539_sort_chop(
    rng: np.random.Generator,
    ability: np.ndarray,
    n_teams: int,
    roster_size: int,
    *,
    assortativity: float,
) -> np.ndarray:
    """539-style: sort by noisy ability signal, equal-count team slices."""
    ability = np.asarray(ability, dtype=float)
    n = len(ability)
    expected = n_teams * roster_size
    if n != expected:
        raise ValueError(f"len(ability)={n} != n_teams*roster_size={expected}")
    rho = float(assortativity)
    signal = rho * ability + (1.0 - rho) * rng.normal(size=n)
    order = np.argsort(signal, kind="mergesort")
    base = np.repeat(np.arange(n_teams), roster_size)
    pool_id = np.empty(n, dtype=np.int64)
    pool_id[order] = base
    return pool_id


def roster_team_stats_from_players(players: pd.DataFrame) -> pd.DataFrame:
    return tpa.roster_team_stats(players)


def coverage_curve(teams: pd.DataFrame, grid: np.ndarray) -> np.ndarray:
    """Plot A metric: count of rosters whose ability span covers each grid point."""
    lo = teams["min"].to_numpy(dtype=float)
    hi = teams["max"].to_numpy(dtype=float)
    grid = np.asarray(grid, dtype=float)
    cov = np.zeros(len(grid), dtype=float)
    for a, b in zip(lo, hi):
        cov += (grid >= a) & (grid <= b)
    return cov


def ability_support_grid(ability: np.ndarray, *, n_points: int = 81) -> np.ndarray:
    a = np.asarray(ability, dtype=float)
    lo = float(np.nanmin(a))
    hi = float(np.nanmax(a))
    pad = max((hi - lo) * 0.05, 1e-6)
    return np.linspace(lo - pad, hi + pad, int(n_points))


def summarize_assignment(
    label: str,
    players: pd.DataFrame,
    grid: np.ndarray,
) -> dict:
    teams = roster_team_stats_from_players(players)
    cov = coverage_curve(teams, grid)
    return {
        "label": label,
        "median_pool_sd": float(teams["pool_sd"].median()),
        "mean_pool_sd": float(teams["pool_sd"].mean()),
        "coverage_peak": float(cov.max()),
        "coverage_at_median_pool_mean": float(
            cov[np.argmin(np.abs(grid - teams["pool_mean"].median()))]
        ),
        "teams": teams,
        "coverage": cov,
    }


@dataclass
class CalibrationCache:
    ability: np.ndarray
    team_targets: np.ndarray
    params: tpa.AssignmentParams
    grid: np.ndarray
    s539: dict
    seed: int
    assortativity: float
    n: int


def build_calibration_cache(
    *,
    sports: Path | None = None,
    seed: int | None = None,
    assortativity: float | None = None,
    ability_draw: str | None = None,
) -> CalibrationCache:
    sports = sports or _sports_dir()
    rho = resolve_assortativity(sports, assortativity)
    state = load_playground_state(sports)
    params = assignment_params_from_state(sports, state, tpa=tpa)
    if seed is None:
        seed = int(state.get("seed", 1))
    if ability_draw is not None:
        params = tpa.AssignmentParams(
            **{
                **params.__dict__,
                "ability_draw": ability_draw,
            }
        )

    rng = np.random.default_rng(int(seed))
    n = params.n_individuals
    ability = tpa.draw_abilities(
        rng,
        n,
        ability_draw=params.ability_draw,
        ability_mean=params.ability_mean,
        ability_sd=params.ability_sd,
        ability_clip_low=params.ability_clip_low,
        ability_clip_high=params.ability_clip_high,
        ability_student_t_df=params.ability_student_t_df,
        ability_student_t_scale=params.ability_student_t_scale,
    )
    team_targets = tpa.draw_target_means(
        rng,
        params.n_teams,
        target_mean_dist=params.target_mean_dist,
        target_mean_low=params.target_mean_low,
        target_mean_high=params.target_mean_high,
        target_mean_mu=params.target_mean_mu,
        target_mean_sigma=params.target_mean_sigma,
    )
    pool_539 = assign_539_sort_chop(
        rng,
        ability,
        params.n_teams,
        params.roster_size,
        assortativity=rho,
    )
    players_539 = tpa.build_roster_dataframe(ability, pool_539, team_targets)
    grid = ability_support_grid(ability)
    s539 = summarize_assignment(
        f"539 sort-chop (rho={rho:.2f})", players_539, grid
    )
    return CalibrationCache(
        ability=ability,
        team_targets=team_targets,
        params=params,
        grid=grid,
        s539=s539,
        seed=int(seed),
        assortativity=float(rho),
        n=int(n),
    )


def soft_assign_at_tau(cache: CalibrationCache, tau: float) -> dict:
    """538 soft assign for one τ; 539 path fixed in cache."""
    rng = np.random.default_rng(int(cache.seed))
    pool_538 = tpa.soft_assign(
        rng,
        cache.ability,
        cache.team_targets,
        cache.params.roster_size,
        assignment_kernel=cache.params.assignment_kernel,
        assignment_temperature=float(tau),
        preferential_alpha=cache.params.preferential_alpha,
        preferential_k=cache.params.preferential_k,
    )
    players_538 = tpa.build_roster_dataframe(
        cache.ability, pool_538, cache.team_targets
    )
    return summarize_assignment("538 soft assign", players_538, cache.grid)


def calibration_table(s538: dict, s539: dict) -> pd.DataFrame:
    rows = []
    for s in (s538, s539):
        rows.append(
            {
                "assignment": s["label"],
                "median_roster_sd": s["median_pool_sd"],
                "mean_roster_sd": s["mean_pool_sd"],
                "coverage_peak": s["coverage_peak"],
            }
        )
    return pd.DataFrame(rows)


def plot_calibration_figure(
    cache: CalibrationCache,
    s538: dict,
    *,
    tau: float,
) -> plt.Figure:
    grid = cache.grid
    s539 = cache.s539
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.2))

    ax = axes[0]
    ax.plot(
        grid,
        s538["coverage"],
        color="C0",
        lw=2.0,
        label=f"538 soft (tau={tau:.3f})",
    )
    ax.plot(
        grid,
        s539["coverage"],
        color="C3",
        ls="--",
        lw=1.8,
        label=s539["label"],
    )
    ax.axhline(1.0, color="0.5", ls=":", lw=1.0)
    ax.set_xlabel("Ability grid (data support)")
    ax.set_ylabel("Teams covering grid point")
    ax.set_title("Plot A overlap — coverage curve")
    ax.legend(fontsize=8)

    ax = axes[1]
    ax.hist(
        s538["teams"]["pool_sd"],
        bins=30,
        alpha=0.55,
        color="C0",
        label="538 soft",
        density=True,
    )
    ax.hist(
        s539["teams"]["pool_sd"],
        bins=30,
        alpha=0.45,
        color="C3",
        label="539 sort-chop",
        density=True,
    )
    ax.axvline(
        s538["median_pool_sd"],
        color="C0",
        ls="-",
        lw=1.5,
        label=f"538 median={s538['median_pool_sd']:.3f}",
    )
    ax.axvline(
        s539["median_pool_sd"],
        color="C3",
        ls="--",
        lw=1.5,
        label=f"539 median={s539['median_pool_sd']:.3f}",
    )
    ax.set_xlabel("Roster SD (ability within team)")
    ax.set_ylabel("Density")
    ax.set_title("Roster SD distribution")
    ax.legend(fontsize=7)
    fig.suptitle(
        f"CELL 10b — N={cache.n:,}  J={cache.params.n_teams}  "
        f"seed={cache.seed}  rho={cache.assortativity:.2f}",
        fontsize=10,
        y=1.02,
    )
    fig.tight_layout()
    return fig


def _metrics_html(
    cache: CalibrationCache,
    table: pd.DataFrame,
    tau: float,
    *,
    linked: bool,
) -> str:
    p = cache.params
    link_note = (
        "τ mirror is <b>linked</b> to CELL 10 tau slider."
        if linked
        else "Run CELL 10 first to link τ mirror to the playground slider."
    )
    rows = ""
    for _, row in table.iterrows():
        rows += (
            f"<tr><td>{row['assignment']}</td>"
            f"<td>{row['median_roster_sd']:.4f}</td>"
            f"<td>{row['coverage_peak']:.1f}</td></tr>"
        )
    return (
        f"<div style='font-size:12px;line-height:1.45'>"
        f"<b>538</b> tau={tau:.3f}  kernel={p.assignment_kernel!r}  "
        f"T={p.target_mean_dist!r} [{p.target_mean_low:.2f}, {p.target_mean_high:.2f}]  "
        f"A={p.ability_draw!r}<br>"
        f"{link_note}<br>"
        f"<table border='1' cellpadding='4' cellspacing='0' "
        f"style='border-collapse:collapse;margin-top:6px'>"
        f"<tr><th>assignment</th><th>median roster SD</th>"
        f"<th>coverage peak</th></tr>{rows}</table></div>"
    )


def display_calibration_panel(
    *,
    sports: Path | None = None,
    assortativity: float | None = None,
    link_tau_widget=None,
    seed: int | None = None,
):
    """Interactive CELL 10b: plots + τ mirror slider (optionally linked to CELL 10)."""
    import ipywidgets as widgets
    from IPython.display import display

    sports = sports or _sports_dir()
    rho = resolve_assortativity(sports, assortativity)
    state = load_playground_state(sports)
    cache = build_calibration_cache(
        sports=sports,
        seed=seed,
        assortativity=rho,
    )
    tau0 = float(
        getattr(link_tau_widget, "value", None)
        if link_tau_widget is not None
        else state.get("tau", cache.params.assignment_temperature)
    )

    w_tau_mirror = widgets.FloatSlider(
        value=tau0,
        min=0.05,
        max=2.0,
        step=0.001,
        readout_format=".3f",
        description="tau (10b mirror)",
        continuous_update=False,
        style={"description_width": "initial"},
        layout=widgets.Layout(width="520px"),
    )
    plot_out = widgets.Output()
    metrics_html = widgets.HTML()
    _state = {"busy": False, "listeners_wired": False}

    def redraw(tau: float) -> None:
        from IPython.display import Image, clear_output, display

        if _state["busy"]:
            return
        _state["busy"] = True
        was_interactive = plt.isinteractive()
        plt.ioff()
        try:
            s538 = soft_assign_at_tau(cache, float(tau))
            table = calibration_table(s538, cache.s539)
            metrics_html.value = _metrics_html(
                cache, table, float(tau), linked=link_tau_widget is not None
            )
            fig = plot_calibration_figure(cache, s538, tau=float(tau))
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
            plt.close(fig)
            png = buf.getvalue()
            with plot_out:
                clear_output(wait=True)
                display(Image(png))
        finally:
            if was_interactive:
                plt.ion()
            _state["busy"] = False

    def _on_tau(change) -> None:
        if change.get("name") != "value":
            return
        if change.get("new") == change.get("old"):
            return
        redraw(float(change["new"]))

    def _wire_tau_listeners() -> None:
        if _state["listeners_wired"]:
            return
        _state["listeners_wired"] = True
        w_tau_mirror.observe(_on_tau, names="value")
        if link_tau_widget is not None:
            widgets.link((w_tau_mirror, "value"), (link_tau_widget, "value"))

    panel = widgets.VBox(
        [
            widgets.HTML(
                "<b>CELL 10b</b> — 538 vs 539 assignment calibration "
                "(same A_i draw; drag τ below plot)"
            ),
            plot_out,
            w_tau_mirror,
            metrics_html,
        ],
        layout=widgets.Layout(align_items="flex-start"),
    )
    display(panel)

    def _schedule_initial_draw(_=None) -> None:
        """First draw after the Output widget is on screen (CELL 10 pattern)."""
        delay = 0.25

        def _go() -> None:
            redraw(float(w_tau_mirror.value))
            _wire_tau_listeners()

        if delay > 0:
            try:
                from IPython import get_ipython

                ip = get_ipython()
                loop = getattr(ip, "io_loop", None) if ip is not None else None
                if loop is not None and hasattr(loop, "call_later"):
                    loop.call_later(delay, _go)
                    return
            except Exception:
                pass
        _go()

    if hasattr(panel, "on_displayed"):
        panel.on_displayed(_schedule_initial_draw, remove=True)
    else:
        _schedule_initial_draw()

    # Do not return panel — Jupyter would display it again as the cell result.
    return None


def compare_538_vs_539(
    *,
    sports: Path | None = None,
    seed: int | None = None,
    assortativity: float | None = None,
    ability_draw: str | None = None,
    tau: float | None = None,
    show_plot: bool = True,
) -> pd.DataFrame:
    """One-shot compare (non-interactive)."""
    sports = sports or _sports_dir()
    rho = resolve_assortativity(sports, assortativity)
    cache = build_calibration_cache(
        sports=sports,
        seed=seed,
        assortativity=rho,
        ability_draw=ability_draw,
    )
    use_tau = float(tau if tau is not None else cache.params.assignment_temperature)
    s538 = soft_assign_at_tau(cache, use_tau)
    table = calibration_table(s538, cache.s539)

    print("=== 538 vs 539 assignment calibration (same A_i draw) ===")
    print(
        f"N={cache.n:,}  J={cache.params.n_teams}  "
        f"roster={cache.params.roster_size}  seed={cache.seed}"
    )
    print(
        f"538 knobs: tau={use_tau:.3f}  "
        f"kernel={cache.params.assignment_kernel!r}  "
        f"T={cache.params.target_mean_dist!r} "
        f"[{cache.params.target_mean_low:.2f}, {cache.params.target_mean_high:.2f}]  "
        f"A draw={cache.params.ability_draw!r}  "
        f"pref_alpha={cache.params.preferential_alpha:.2f}"
    )
    print(f"539 knob: assortativity rho={cache.assortativity:.3f}")
    print()
    print(table.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    print()
    print(
        "Interpretation:\n"
        "  • median_roster_sd — spread of ability within teams.\n"
        "  • coverage_peak — Plot A soft-line peak (team span overlap).\n"
        "  • Tune τ until 538 row matches 539; use display_calibration_panel() "
        "for live mirror slider."
    )

    if show_plot:
        fig = plot_calibration_figure(cache, s538, tau=use_tau)
        plt.show()

    return table


@dataclass
class TauCalibrationResult:
    """Best τ from ``auto_calibrate_tau``."""

    tau: float
    median_roster_sd: float
    coverage_peak: float
    target_median_roster_sd: float
    target_coverage_peak: float
    delta_median_roster_sd: float
    delta_coverage_peak: float
    loss: float
    cache: CalibrationCache
    sweep: pd.DataFrame


def calibration_loss(
    s538: dict,
    s539: dict,
    *,
    weight_sd: float = 1.0,
    weight_cov: float = 1.0,
) -> float:
    """Weighted relative squared error vs 539 on median roster SD and coverage peak."""
    t_sd = float(s539["median_pool_sd"])
    t_cov = float(s539["coverage_peak"])
    d_sd = (float(s538["median_pool_sd"]) - t_sd) / max(abs(t_sd), 1e-9)
    d_cov = (float(s538["coverage_peak"]) - t_cov) / max(abs(t_cov), 1e-9)
    return float(weight_sd * d_sd**2 + weight_cov * d_cov**2)


def _tau_sweep_rows(
    cache: CalibrationCache,
    tau_values: np.ndarray,
    *,
    weight_sd: float,
    weight_cov: float,
) -> list[dict]:
    target = cache.s539
    rows = []
    for tau in tau_values:
        s538 = soft_assign_at_tau(cache, float(tau))
        loss = calibration_loss(s538, target, weight_sd=weight_sd, weight_cov=weight_cov)
        rows.append(
            {
                "tau": float(tau),
                "loss": loss,
                "median_roster_sd": s538["median_pool_sd"],
                "coverage_peak": s538["coverage_peak"],
                "delta_sd_vs_539": s538["median_pool_sd"] - target["median_pool_sd"],
                "delta_cov_peak_vs_539": s538["coverage_peak"] - target["coverage_peak"],
            }
        )
    return rows


def auto_calibrate_tau(
    *,
    sports: Path | None = None,
    seed: int | None = None,
    assortativity: float | None = None,
    ability_draw: str | None = None,
    tau_min: float = 0.05,
    tau_max: float = 0.45,
    coarse_step: float = 0.01,
    refine_step: float = 0.001,
    refine_window: float = 0.02,
    weight_sd: float = 1.0,
    weight_cov: float = 1.0,
    apply_tau_widget=None,
    persist_state: bool = False,
    verbose: bool = True,
    cache: CalibrationCache | None = None,
) -> TauCalibrationResult:
    """Find τ minimizing distance to 539 on median roster SD + coverage peak.

    Two-pass search: coarse grid, then ±``refine_window`` at ``refine_step`` (default
    0.001). Optionally push τ to a linked CELL 10 slider and/or
    ``tier1_cell10_playground_state.json``.
    """
    sports = sports or _sports_dir()
    rho = resolve_assortativity(sports, assortativity)
    if cache is None:
        cache = build_calibration_cache(
            sports=sports,
            seed=seed,
            assortativity=rho,
            ability_draw=ability_draw,
        )
    target = cache.s539

    coarse_taus = np.arange(tau_min, tau_max + coarse_step * 0.5, coarse_step)
    if verbose:
        ref_path = reference_539_settings_path(sports)
        ref_note = (
            f" (from {ref_path.name})"
            if assortativity is None and ref_path.is_file()
            else ""
        )
        print("=== auto_calibrate_tau (538 soft → 539 sort-chop) ===")
        print(
            f"N={cache.n:,}  J={cache.params.n_teams}  roster={cache.params.roster_size}  "
            f"seed={cache.seed}  rho={cache.assortativity:.3f}{ref_note}"
        )
        print(
            f"539 target: median_sd={target['median_pool_sd']:.4f}  "
            f"coverage_peak={target['coverage_peak']:.1f}"
        )
        print(
            f"Coarse grid: tau in [{tau_min:.3f}, {tau_max:.3f}] step={coarse_step:.3f} "
            f"({len(coarse_taus)} evals)…"
        )

    coarse_rows = _tau_sweep_rows(
        cache, coarse_taus, weight_sd=weight_sd, weight_cov=weight_cov
    )
    coarse_df = pd.DataFrame(coarse_rows)
    best_coarse = coarse_df.loc[coarse_df["loss"].idxmin()]

    lo = max(tau_min, float(best_coarse["tau"]) - refine_window)
    hi = min(tau_max, float(best_coarse["tau"]) + refine_window)
    refine_taus = np.arange(lo, hi + refine_step * 0.5, refine_step)
    if verbose:
        print(
            f"Refine: tau in [{lo:.3f}, {hi:.3f}] step={refine_step:.3f} "
            f"({len(refine_taus)} evals)…"
        )

    refine_rows = _tau_sweep_rows(
        cache, refine_taus, weight_sd=weight_sd, weight_cov=weight_cov
    )
    refine_df = pd.DataFrame(refine_rows)
    best = refine_df.loc[refine_df["loss"].idxmin()]

    tau_best = round(float(best["tau"]), 3)
    s538 = soft_assign_at_tau(cache, tau_best)
    loss_best = calibration_loss(s538, target, weight_sd=weight_sd, weight_cov=weight_cov)

    sweep = pd.concat(
        [
            coarse_df.assign(stage="coarse"),
            refine_df.assign(stage="refine"),
        ],
        ignore_index=True,
    )

    if apply_tau_widget is not None:
        apply_tau_widget.value = tau_best

    if persist_state:
        state_path = sports / "tier1_cell10_playground_state.json"
        state = load_playground_state(sports)
        state["tau"] = tau_best
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        if verbose:
            print(f"Wrote tau={tau_best:.3f} → {state_path.name}")

    result = TauCalibrationResult(
        tau=tau_best,
        median_roster_sd=float(s538["median_pool_sd"]),
        coverage_peak=float(s538["coverage_peak"]),
        target_median_roster_sd=float(target["median_pool_sd"]),
        target_coverage_peak=float(target["coverage_peak"]),
        delta_median_roster_sd=float(s538["median_pool_sd"] - target["median_pool_sd"]),
        delta_coverage_peak=float(s538["coverage_peak"] - target["coverage_peak"]),
        loss=float(loss_best),
        cache=cache,
        sweep=sweep,
    )

    if verbose:
        print()
        print(f"Best tau = {result.tau:.3f}  (loss={result.loss:.6f})")
        print(
            f"  538: median_sd={result.median_roster_sd:.4f}  "
            f"coverage_peak={result.coverage_peak:.1f}"
        )
        print(
            f"  539: median_sd={result.target_median_roster_sd:.4f}  "
            f"coverage_peak={result.target_coverage_peak:.1f}"
        )
        print(
            f"  delta: median_sd={result.delta_median_roster_sd:+.4f}  "
            f"coverage_peak={result.delta_coverage_peak:+.1f}"
        )
        if apply_tau_widget is not None:
            print("  Applied to linked tau slider (run CELL 10 refresh if plots stale).")

    return result


def tau_sweep_hint(
    *,
    sports: Path | None = None,
    seed: int = 1,
    assortativity: float | None = None,
    tau_values: tuple[float, ...] = (0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.30, 0.45),
) -> pd.DataFrame:
    """Quick grid: median SD and coverage peak vs tau (538 only), fixed 539 target."""
    sports = sports or _sports_dir()
    rho = resolve_assortativity(sports, assortativity)
    cache = build_calibration_cache(
        sports=sports,
        seed=seed,
        assortativity=rho,
    )
    target = cache.s539

    rows = []
    for tau in tau_values:
        s = soft_assign_at_tau(cache, float(tau))
        rows.append(
            {
                "tau": float(tau),
                "median_roster_sd": s["median_pool_sd"],
                "coverage_peak": s["coverage_peak"],
                "delta_sd_vs_539": s["median_pool_sd"] - target["median_pool_sd"],
                "delta_cov_peak_vs_539": s["coverage_peak"] - target["coverage_peak"],
            }
        )
    df = pd.DataFrame(rows)
    print(
        f"539 target: median_sd={target['median_pool_sd']:.4f}  "
        f"coverage_peak={target['coverage_peak']:.1f}"
    )
    print(df.to_string(index=False, float_format=lambda x: f"{x:.4f}"))
    return df


if __name__ == "__main__":
    import matplotlib

    matplotlib.use("Agg")
    compare_538_vs_539(show_plot=False)
    print("\n--- auto_calibrate_tau ---")
    auto_calibrate_tau(verbose=True, persist_state=False)
