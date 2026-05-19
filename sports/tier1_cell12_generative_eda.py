# Executed by 538 notebook CELL 12 via exec(..., globals()).
# Alex §6 step 1 on simulated rosters: binned selection rate vs LOO poolq_loo (inverted-U target).

from __future__ import annotations

import importlib
import importlib.util
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _sports_dir() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in (cwd / "sports", cwd):
        if (candidate / "tier1_sim_config.py").is_file():
            return candidate
    raise FileNotFoundError(f"Cannot find sports/ from cwd={cwd}")


def _load_tier1_cfg(sports: Path) -> object:
    spec = importlib.util.spec_from_file_location(
        "tier1_sim_config", sports / "tier1_sim_config.py"
    )
    if spec is None or spec.loader is None:
        raise ImportError("tier1_sim_config")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_cell12(*, seed: int | None = None) -> pd.DataFrame:
    sports = _sports_dir()
    if str(sports) not in sys.path:
        sys.path.insert(0, str(sports))

    import tier1_generative_eda as tge
    import tier1_pool_assignment as tpa

    importlib.reload(tpa)
    importlib.reload(tge)

    cfg = _load_tier1_cfg(sports)
    state = tge.load_playground_state(sports)
    base_sel = tge.SelectionConfig.from_module(cfg)
    sel = tge.SelectionConfig.from_state(state, base_sel)
    params = tge.assignment_params_from_state(sports, state or None, tpa=tpa)

    if seed is None:
        try:
            seed = int(state.get("seed", getattr(cfg, "RANDOM_SEED", 42)))
        except (TypeError, ValueError):
            seed = int(getattr(cfg, "RANDOM_SEED", 42))

    repo = sports.parent if sports.name == "sports" else sports
    if str(repo) not in sys.path:
        sys.path.insert(0, str(repo))
    from sports_pipeline.panel_build import assign_poolq_bin_labels

    print(
        f"CELL 12: soft assign J={params.n_teams} N={params.n_individuals} "
        f"bins={sel.n_bins} K={sel.n_selected} score={sel.score_mode!r} "
        f"winner={sel.winner_selection!r} seed={seed}"
    )
    if state:
        print("  (pool + selection knobs from tier1_cell10_playground_state.json)")

    rng = np.random.default_rng(seed)
    _, summ, fig = tge.run_inverted_u_pipeline(
        params,
        sel,
        rng,
        tpa=tpa,
        assign_poolq_bin_labels=assign_poolq_bin_labels,
    )
    print(summ.to_string(index=False))
    fig.axes[0].set_title(
        f"538 CELL 12 — generative inverted-U check ({sel.n_bins} bins, J={params.n_teams})"
    )
    plt.show()
    plt.close(fig)
    return summ


if __name__ == "__main__":
    import matplotlib

    matplotlib.use("Agg")
    run_cell12()
