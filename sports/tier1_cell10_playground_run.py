# =============================================================================
# LEGACY — 538 CELL 10 widget playground (NOT the 540 re-entry daily path)
# =============================================================================
# What this file is
#   ipywidgets UI formerly exec()'d from archived 538 / 538D CELL 10. Plot A
#   (interval overlap) + Plot B (selection curve) + knobs for τ-era assignment
#   and score modes. Touched during Jul 2026 ρ work because engines changed —
#   that does NOT mean it is on the CHARLES_CHECKLIST re-entry path.
#
# What to use instead (re-entry)
#   sports/540_READ_ME_SIM.md
#   sports/scripts/hero_model_reset_bundle.py     # Pass A
#   sports/scripts/540_rho_ablation_bundle.py     # Pass B
#   sports/540_three_step_sim.ipynb               # thin display / optional re-run
#   sports/tier1_pool_assignment.py              # engines (shared)
#
# Open this file only if you need the old interactive lab. Do not extend it
# for new Alex deliverables.
# =============================================================================
#
# Executed by 538 notebook CELL 10 via exec(..., globals()).
# Generative pool assignment (Thread A) — not 537 legacy score playground.

from __future__ import annotations

import base64
import importlib.util
import io
import json
import sys
from collections.abc import Callable
from pathlib import Path

import numpy as np

try:
    import ipywidgets as widgets
    from IPython.display import display
except ImportError:
    print(
        "Install ipywidgets (pip install ipywidgets), restart the kernel, then re-run CELL 10."
    )
else:

    def _sports_dir() -> Path:
        """Repo root or sports/ — works when this file is exec()'d (no __file__)."""
        cwd = Path.cwd().resolve()
        for candidate in (cwd / "sports", cwd):
            if (candidate / "tier1_sim_config.py").is_file():
                return candidate
        raise FileNotFoundError(
            "Cannot find tier1_sim_config.py — run notebook from repo root "
            f"(cwd={cwd})"
        )

    _SPORTS = _sports_dir()
    if str(_SPORTS) not in sys.path:
        sys.path.insert(0, str(_SPORTS))

    if globals().get("_CELL10_PLAYGROUND_LIVE") and callable(globals().get("redraw")):
        _live = globals().get("panel")
        if _live is not None:
            display(_live)
            print(
                "CELL 10: re-displayed live panel "
                "(click Run / refresh plot to update figures)"
            )
        else:
            print("CELL 10: panel missing — restart kernel to rebuild")
    else:

        _PLOT_A_DPI = 120
        _PLOT_A_MAX_WIDTH_PX = int(9.0 * _PLOT_A_DPI)
        _PLOT_B_DPI = 120
        _PLOT_B_MAX_WIDTH_PX = int(8.5 * _PLOT_B_DPI)
        _PLOT_C_DPI = 120
        _PLOT_C_MAX_WIDTH_PX = int(8.5 * _PLOT_C_DPI)

        def _make_responsive_plot_widget(
            *,
            max_width_px: int,
            placeholder: str = "(no plot yet)",
        ) -> tuple[widgets.HTML, Callable[[bytes | None], None]]:
            """HTML img wrapper so widening the notebook scales uniformly, not sideways stretch."""

            holder = widgets.HTML(
                value=f"<i>{placeholder}</i>",
                layout=widgets.Layout(align_self="flex-start"),
            )

            def set_png(data: bytes | None) -> None:
                if not data:
                    holder.value = f"<i>{placeholder}</i>"
                    return
                b64 = base64.b64encode(data).decode("ascii")
                holder.value = (
                    f'<img alt="plot" src="data:image/png;base64,{b64}" '
                    f'style="display:block;width:auto;height:auto;'
                    f'max-width:min(100%, {max_width_px}px);" />'
                )

            return holder, set_png

        import tier1_pool_assignment as _tpa
        from tier1_pool_assignment import (
            AssignmentParams,
            assign_selection,
            assign_sort_chop_benchmark,
            build_roster_dataframe,
            draw_abilities,
            draw_target_means,
            pool_l_dropdown_options,
            pool_l_html_label,
            pool_l_short_label,
            roster_team_stats,
            soft_assign,
        )

        _REPO = _SPORTS.parent if _SPORTS.name == "sports" else _SPORTS
        if str(_REPO) not in sys.path:
            sys.path.insert(0, str(_REPO))

        _CFG_PATH = _SPORTS / "tier1_sim_config.py"
        _spec = importlib.util.spec_from_file_location("tier1_sim_config", _CFG_PATH)
        _tier1_cfg = importlib.util.module_from_spec(_spec)
        assert _spec is not None and _spec.loader is not None
        _spec.loader.exec_module(_tier1_cfg)

        PLAYGROUND_STATE_PATH = _SPORTS / "tier1_cell10_playground_state.json"
        # Unicode subscripts — ipywidgets `description` is plain text (no HTML/MathJax)
        _A = "A\u1d62"  # Aᵢ
        _T = "T\u2c7c"  # Tⱼ
        style = {"description_width": "168px"}
        lay = widgets.Layout(width="460px")
        _sym_legend = widgets.HTML(
            value=(
                "<div style='font-size:12px;color:#555;margin:0 0 6px 0'>"
                f"<b>{_A}</b> = latent ability (player <i>i</i>) &nbsp;|&nbsp; "
                f"<b>{_T}</b> = fixed team target mean (team <i>j</i>) &nbsp;|&nbsp; "
                "<b>L<sub>q</sub></b>/<b>L<sub>c</sub></b> = LOO pool (mean / sum)"
                "</div>"
            ),
            layout=widgets.Layout(width="520px"),
        )
        _SCORE_HELP_STYLE = (
            "font-size:14px;color:#222;line-height:1.55;margin:6px 0 8px 0"
        )
        _HINT_STYLE = "font-size:12px;color:#555;line-height:1.45;margin:0 0 4px 0"

        def _state_load() -> dict:
            if not PLAYGROUND_STATE_PATH.is_file():
                return {}
            try:
                return json.loads(PLAYGROUND_STATE_PATH.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return {}

        def _selection_defaults_from_cfg(mod) -> dict:
            n_sel = getattr(mod, "N_SELECTED", None)
            if n_sel is None:
                n_sel = getattr(mod, "N_PROMOTED", 40)
            score = getattr(mod, "SELECTION_SCORE_MODE", None)
            if score is None:
                score = getattr(mod, "PROMOTION_SCORE_MODE", "loo_gap_plus_ability")
            return {
                "n_bins": int(getattr(mod, "GENERATIVE_N_BINS", 12)),
                "bin_mode": str(getattr(mod, "GENERATIVE_POOLQ_BINNING", "quantile")),
                "n_selected": int(n_sel),
                "score_mode": str(score),
                "loo_gap_weight": float(getattr(mod, "LOO_GAP_WEIGHT", 0.5)),
                "winner_selection": str(getattr(mod, "WINNER_SELECTION", "C")),
                "loo_pool_l_mode": str(getattr(mod, "LOO_POOL_L_MODE", "quality")),
            }

        def _defaults() -> dict:
            p = AssignmentParams.from_module(_tier1_cfg)
            sel = _selection_defaults_from_cfg(_tier1_cfg)
            return {
                "n_teams": p.n_teams,
                "roster_size": p.roster_size,
                "tau": p.assignment_temperature,
                "kernel": p.assignment_kernel,
                "target_dist": p.target_mean_dist,
                "t_low": p.target_mean_low,
                "t_high": p.target_mean_high,
                "pref_alpha": p.preferential_alpha,
                "ability_draw": p.ability_draw,
                "seed": int(getattr(_tier1_cfg, "RANDOM_SEED", 42)),
                "show_chop": bool(getattr(_tier1_cfg, "SHOW_CHOP", False)),
                "show_plot_a": bool(getattr(_tier1_cfg, "SHOW_PLOT_A", False)),
                "show_plot_b": bool(getattr(_tier1_cfg, "SHOW_PLOT_B", True)),
                "show_plot_c": bool(getattr(_tier1_cfg, "SHOW_PLOT_C", False)),
                "n_bins": sel["n_bins"],
                "bin_mode": sel["bin_mode"],
                "n_selected": sel["n_selected"],
                "score_mode": sel["score_mode"],
                "loo_gap_weight": sel["loo_gap_weight"],
                "winner_selection": sel["winner_selection"],
                "loo_pool_l_mode": sel["loo_pool_l_mode"],
                "viability_theta": float(getattr(p, "viability_theta", 0.7546158731868137)),
                "viability_sharpness": float(
                    getattr(p, "viability_sharpness", getattr(_tier1_cfg, "VIABILITY_SHARPNESS", 18.0))
                ),
            }

        def _pool_530_defaults() -> dict:
            """530 forensics pool cal: high overlap, median roster SD ~0.8 (NOT 539)."""
            d = _defaults()
            mod = _tier1_cfg
            d.update(
                {
                    "tau": float(
                        getattr(mod, "POOL_530_ASSIGNMENT_TEMPERATURE", 0.65)
                    ),
                    "pref_alpha": float(
                        getattr(mod, "POOL_530_PREFERENTIAL_ALPHA", 0.0)
                    ),
                    "ability_draw": str(
                        getattr(mod, "POOL_530_ABILITY_DRAW", "normal_clipped")
                    ),
                    "target_dist": str(
                        getattr(mod, "POOL_530_TARGET_MEAN_DIST", "uniform")
                    ),
                    "score_mode": str(
                        getattr(mod, "POOL_530_SELECTION_SCORE_MODE", "ability")
                    ),
                    "loo_gap_weight": float(
                        getattr(mod, "POOL_530_LOO_GAP_WEIGHT", 0.0)
                    ),
                    "loo_pool_l_mode": str(
                        getattr(mod, "POOL_530_LOO_POOL_L_MODE", "quality")
                    ),
                    "winner_selection": str(
                        getattr(mod, "POOL_530_WINNER_SELECTION", "C")
                    ),
                }
            )
            return d

        def _minimal_defaults() -> dict:
            """Deprecated alias — same as 530 pool cal."""
            return _pool_530_defaults()

        def _match_539_defaults() -> dict:
            """539 assignment mimicry Layer 0: τ from CELL 10c, ability-only top-K."""
            d = _defaults()
            mod = _tier1_cfg
            d.update(
                {
                    "n_teams": int(getattr(mod, "MATCH_539_N_TEAMS", 1000)),
                    "roster_size": int(getattr(mod, "MATCH_539_ROSTER_SIZE", 15)),
                    "tau": float(getattr(mod, "MATCH_539_ASSIGNMENT_TEMPERATURE", 0.108)),
                    "pref_alpha": float(
                        getattr(mod, "MATCH_539_PREFERENTIAL_ALPHA", 0.0)
                    ),
                    "ability_draw": str(
                        getattr(mod, "MATCH_539_ABILITY_DRAW", "normal_clipped")
                    ),
                    "target_dist": str(
                        getattr(mod, "MATCH_539_TARGET_MEAN_DIST", "uniform")
                    ),
                    "t_low": float(getattr(mod, "MATCH_539_TARGET_MEAN_LOW", -0.5)),
                    "t_high": float(getattr(mod, "MATCH_539_TARGET_MEAN_HIGH", 0.5)),
                    "seed": int(getattr(mod, "MATCH_539_RANDOM_SEED", 42)),
                    "n_selected": int(getattr(mod, "MATCH_539_N_SELECTED", 1500)),
                    "score_mode": str(
                        getattr(mod, "MATCH_539_SELECTION_SCORE_MODE", "ability")
                    ),
                    "loo_gap_weight": float(
                        getattr(mod, "MATCH_539_LOO_GAP_WEIGHT", 0.0)
                    ),
                    "loo_pool_l_mode": str(
                        getattr(mod, "MATCH_539_LOO_POOL_L_MODE", "quality")
                    ),
                    "winner_selection": str(
                        getattr(mod, "MATCH_539_WINNER_SELECTION", "C")
                    ),
                    "viability_theta": float(
                        getattr(mod, "MATCH_539_VIABILITY_THETA", 0.72)
                    ),
                    "viability_sharpness": float(
                        getattr(mod, "MATCH_539_VIABILITY_SHARPNESS", 10.0)
                    ),
                }
            )
            return d

        def _selection_539_defaults() -> dict:
            """539 Layer 2: beta_2_2 on [0,1], crowding_smooth, w=λ; keeps 530 pool τ."""
            d = _pool_530_defaults()
            mod = _tier1_cfg
            lam = float(getattr(mod, "SELECTION_539_LOO_GAP_WEIGHT", 0.55))
            try:
                from tier1_cell10_539_calibration_compare import load_539_reference_settings

                lam = float(load_539_reference_settings(_SPORTS).get("lambda_", lam))
            except Exception:
                pass
            d.update(
                {
                    "ability_draw": str(
                        getattr(mod, "SELECTION_539_ABILITY_DRAW", "beta_2_2")
                    ),
                    "target_dist": "uniform",
                    "t_low": float(getattr(mod, "SELECTION_539_TARGET_MEAN_LOW", 0.0)),
                    "t_high": float(
                        getattr(mod, "SELECTION_539_TARGET_MEAN_HIGH", 1.0)
                    ),
                    "score_mode": str(
                        getattr(
                            mod,
                            "SELECTION_539_SELECTION_SCORE_MODE",
                            "loo_gap_plus_ability",
                        )
                    ),
                    "loo_gap_weight": lam,
                    "loo_pool_l_mode": str(
                        getattr(mod, "SELECTION_539_LOO_POOL_L_MODE", "crowding_smooth")
                    ),
                    "winner_selection": str(
                        getattr(mod, "SELECTION_539_WINNER_SELECTION", "C")
                    ),
                    "viability_theta": float(
                        getattr(mod, "SELECTION_539_VIABILITY_THETA", 0.72)
                    ),
                    "viability_sharpness": float(
                        getattr(mod, "SELECTION_539_VIABILITY_SHARPNESS", 10.0)
                    ),
                }
            )
            return d

        _st = {**_defaults(), **_state_load()}

        def _cell10_plot_flag(
            global_name: str, state_key: str, cfg_name: str, *, default: bool
        ) -> bool:
            if global_name in globals():
                return bool(globals()[global_name])
            return bool(_st.get(state_key, getattr(_tier1_cfg, cfg_name, default)))

        def _show_chop_enabled() -> bool:
            return _cell10_plot_flag(
                "CELL10_SHOW_CHOP", "show_chop", "SHOW_CHOP", default=False
            )

        def _show_plot_a_enabled() -> bool:
            return _cell10_plot_flag(
                "CELL10_SHOW_PLOT_A", "show_plot_a", "SHOW_PLOT_A", default=False
            )

        def _show_plot_b_enabled() -> bool:
            return _cell10_plot_flag(
                "CELL10_SHOW_PLOT_B", "show_plot_b", "SHOW_PLOT_B", default=True
            )

        def _show_plot_c_enabled() -> bool:
            return _cell10_plot_flag(
                "CELL10_SHOW_PLOT_C", "show_plot_c", "SHOW_PLOT_C", default=False
            )

        def _plot_b_team_mean_enabled() -> bool:
            return _cell10_plot_flag(
                "CELL10_PLOT_B_TEAM_MEAN",
                "plot_b_team_mean",
                "SHOW_PLOT_B_TEAM_MEAN",
                default=False,
            )

        _j_max = int(getattr(_tier1_cfg, "N_TEAMS_SLIDER_MAX", 2500))
        w_n_teams = widgets.IntSlider(
            value=min(int(_st["n_teams"]), _j_max),
            min=4,
            max=_j_max,
            step=1,
            description="Teams J",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        w_roster = widgets.IntSlider(
            value=int(_st["roster_size"]),
            min=5,
            max=40,
            step=1,
            description="Roster size",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        w_tau = widgets.FloatSlider(
            value=float(_st["tau"]),
            min=0.05,
            max=2.0,
            step=0.001,
            readout_format=".3f",
            description="tau (temperature)",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        w_kernel = widgets.Dropdown(
            options=["gaussian", "cauchy"],
            value=str(_st["kernel"]),
            description="Kernel",
            style=style,
            layout=lay,
        )
        _TARGET_DIST_OPTIONS = [
            ("Uniform", "uniform"),
            ("Normal clipped", "normal_clipped"),
            ("530 fitted perf (within-season z)", "empirical_530"),
        ]
        _target_val = str(_st.get("target_dist", "uniform")).strip().lower()
        if _target_val not in {v for _, v in _TARGET_DIST_OPTIONS}:
            _target_val = "uniform"
        w_target = widgets.Dropdown(
            options=_TARGET_DIST_OPTIONS,
            value=_target_val,
            description="Target T law",
            style=style,
            layout=widgets.Layout(width="520px"),
        )
        w_t_low = widgets.FloatSlider(
            value=float(_st["t_low"]),
            min=-3.0,
            max=1.0,
            step=0.05,
            description="T low",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        w_t_high = widgets.FloatSlider(
            value=float(_st["t_high"]),
            min=-1.0,
            max=20.0,
            step=0.05,
            description="T high",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        w_pref = widgets.FloatSlider(
            value=float(_st["pref_alpha"]),
            min=0.0,
            max=2.0,
            step=0.05,
            readout_format=".2f",
            description="Pref attach alpha",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        w_ability = widgets.Dropdown(
            options=[
                "normal_clipped",
                "normal_plus_student_t",
                "uniform_01",
                "beta_2_2",
                "empirical_530",
            ],
            value=str(_st["ability_draw"]),
            description="A draw",
            style=style,
            layout=lay,
        )
        w_seed = widgets.IntSlider(
            value=int(_st["seed"]),
            min=0,
            max=99999,
            step=1,
            description="Seed",
            continuous_update=False,
            style=style,
            layout=lay,
        )

        _LOO_L_MODE_OPTIONS = pool_l_dropdown_options()
        _loo_l_val = str(_st.get("loo_pool_l_mode", "quality")).strip().lower()
        if _loo_l_val not in {v for _, v in _LOO_L_MODE_OPTIONS}:
            _loo_l_val = "quality"
        w_loo_l_mode = widgets.Dropdown(
            options=_LOO_L_MODE_OPTIONS,
            value=_loo_l_val,
            description="Pool L in score",
            style=style,
            layout=widgets.Layout(width="520px"),
        )
        _theta_default = float(_st.get("viability_theta", getattr(_tier1_cfg, "VIABILITY_THETA", 0.755)))
        w_viability_theta = widgets.FloatSlider(
            value=_theta_default,
            min=-1.0,
            max=3.5,
            step=0.01,
            readout_format=".3f",
            description="Viability theta",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        _gamma_default = float(
            _st.get("viability_sharpness", getattr(_tier1_cfg, "VIABILITY_SHARPNESS", 18.0))
        )
        w_viability_gamma = widgets.FloatSlider(
            value=_gamma_default,
            min=1.0,
            max=40.0,
            step=0.5,
            readout_format=".1f",
            description="Viability gamma",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        loo_l_hint_html = widgets.HTML(
            layout=widgets.Layout(width="520px", margin="0 0 4px 0")
        )
        w_n_bins = widgets.IntSlider(
            value=int(_st.get("n_bins", 12)),
            min=5,
            max=30,
            step=1,
            description="Plot B: # bins on L_Q",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        _BIN_MODE_OPTIONS = [
            ("Equal count (quantile)", "quantile"),
            ("Equal width on L_Q", "equal_width"),
        ]
        _bin_mode_val = str(_st.get("bin_mode", "quantile")).strip().lower()
        if _bin_mode_val not in {"quantile", "equal_width"}:
            _bin_mode_val = "quantile"
        w_bin_mode = widgets.Dropdown(
            options=_BIN_MODE_OPTIONS,
            value=_bin_mode_val,
            description="Plot B binning",
            style=style,
            layout=widgets.Layout(width="520px"),
        )
        w_n_select = widgets.IntSlider(
            value=int(_st.get("n_selected", _st.get("n_promoted", 200))),
            min=5,
            max=5000,
            step=5,
            description="Selections K",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        _SCORE_MODE_OPTIONS = [
            ("Pool-adjusted ability — w slider below", "loo_gap_plus_ability"),
            ("Ability only (ignores w)", "ability"),
        ]
        _WINNER_OPTIONS = [
            (
                "C: Top-K — K highest scores win (deterministic)",
                "C",
            ),
            (
                "A: Weighted — sample K without replacement by score",
                "A",
            ),
            (
                "B: Bernoulli — each person selected independently",
                "B",
            ),
        ]
        _winner_val = str(_st.get("winner_selection", "C"))
        if _winner_val not in {"A", "B", "C"}:
            _winner_val = "C"

        w_score = widgets.Dropdown(
            options=_SCORE_MODE_OPTIONS,
            value=str(_st.get("score_mode", "loo_gap_plus_ability")),
            description="Selection score",
            style=style,
            layout=widgets.Layout(width="520px"),
        )
        w_loo_w = widgets.FloatSlider(
            value=float(_st.get("loo_gap_weight", 0.5)),
            min=0.0,
            max=1.0,
            step=0.05,
            readout_format=".2f",
            description="Quality-gap weight w",
            continuous_update=False,
            style=style,
            layout=lay,
        )
        score_formula_html = widgets.HTML(
            layout=widgets.Layout(width="520px", margin="0 0 4px 0")
        )
        w_winner = widgets.Dropdown(
            options=_WINNER_OPTIONS,
            value=_winner_val,
            description="Winner draw",
            style=style,
            layout=widgets.Layout(width="520px"),
        )

        def _sync_gamma_slider_visibility(_=None):
            """Hide/show gamma slider — must run AFTER panel display (Step 6 bisect)."""
            mode = str(w_loo_l_mode.value).strip().lower()
            w_viability_gamma.layout.display = (
                "" if mode == "crowding_smooth" else "none"
            )

        def _update_loo_l_hint_html(_=None):
            mode = str(w_loo_l_mode.value).strip().lower()
            l_html = pool_l_html_label(mode)
            th = float(w_viability_theta.value)
            gam = float(w_viability_gamma.value)
            if mode == "crowding_smooth":
                detail = (
                    f"LOO <b>mean viability</b> σ(γ(A−θ)) on teammates "
                    f"(<b>θ={th:.3f}</b>, <b>γ={gam:.1f}</b>; 539 Alex)"
                )
            elif mode == "crowding":
                detail = (
                    f"LOO <b>viable-peer share</b> (count above θ / pool size; "
                    f"<b>θ={th:.3f}</b>; 530 median drafted z)"
                )
            else:
                detail = "LOO <b>mean</b> of teammate ability (quality)"
            loo_l_hint_html.value = (
                f"<div style='{_HINT_STYLE}'>"
                "<b>Selection score only</b> (Plot B x-axis is always L<sub>q</sub>, not this L). "
                f"Active regressor: <b>{l_html}</b> — {detail}"
                "</div>"
            )

        def _on_loo_pool_context_change(_=None):
            _update_loo_l_hint_html()
            _sync_gamma_slider_visibility()

        def _loo_w_slider_label(pool_l_mode: str) -> str:
            """Slider caption: w on (A − L_Q) gap vs w on viable-peer count L_C (not a gap)."""
            if _tpa.is_crowding_l_mode(pool_l_mode):
                return "Crowding weight w"
            return "Quality-gap weight w"

        def _update_score_formula_html(_=None):
            pool_mode = str(w_loo_l_mode.value)
            w_loo_w.description = _loo_w_slider_label(pool_mode)
            w = float(w_loo_w.value)
            l_html = pool_l_html_label(pool_mode)
            if str(w_score.value) == "ability":
                score_formula_html.value = (
                    f"<div style='{_SCORE_HELP_STYLE}'>"
                    "<b>Selection rank</b> = A<sub>i</sub> only (top-K; <i>w</i> unused).<br>"
                    "<span style='color:#444;font-size:11px'>"
                    "Plot B still bins on L<sub>q</sub> — independent of this rank."
                    "</span>"
                    "</div>"
                )
                return
            if _tpa.is_crowding_l_mode(pool_mode):
                if pool_mode == "crowding_smooth":
                    sub = (
                        f"{l_html} is LOO <b>mean σ(γ(A−θ))</b> (smooth viable-peer density; 539)."
                    )
                else:
                    sub = (
                        f"{l_html} is viable-peer <b>share</b> "
                        f"(count above θ / LOO pool size; hard threshold)."
                    )
                a_draw = str(w_ability.value).strip().lower()
                scale_line = ""
                if a_draw not in ("beta_2_2", "uniform_01"):
                    scale_line = (
                        "<br><span style='color:#444;font-size:11px'>"
                        "Z-scored A: L<sub>c</sub> is auto-scaled to A spread (p90−p10) "
                        "so w·L is commensurate with A<sub>i</sub>."
                        "</span>"
                    )
                score_formula_html.value = (
                    f"<div style='{_SCORE_HELP_STYLE}'>"
                    f"<b>Selection rank</b> = A<sub>i</sub> − <i>w</i>·{l_html} &nbsp;&nbsp;|&nbsp;&nbsp; "
                    f"<b><i>w</i> = {w:.2f}</b><br>"
                    f"<span style='color:#444;font-size:12px'>{sub}</span>"
                    f"{scale_line}<br>"
                    "<span style='color:#444;font-size:11px'>"
                    "Plot B x-axis = L<sub>q</sub> bins only (not this L)."
                    "</span><br><br>"
                    f"<b><i>w</i> = 1</b> → ability minus crowding term only.<br>"
                    f"<b><i>w</i> = 0</b> → ability only; crowding ignored."
                    "</div>"
                )
                return
            score_formula_html.value = (
                f"<div style='{_SCORE_HELP_STYLE}'>"
                f"<b>Selection rank</b> = <i>w</i>·(A<sub>i</sub> − {l_html}) + (1−<i>w</i>)·A<sub>i</sub><br>"
                f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= "
                f"A<sub>i</sub> − <i>w</i>·{l_html} &nbsp;&nbsp;|&nbsp;&nbsp; "
                f"<b><i>w</i> = {w:.2f}</b><br>"
                "<span style='color:#444;font-size:11px'>"
                "Plot B x-axis = L<sub>q</sub> bins only (Pool L here is for rank, not bins)."
                "</span><br><br>"
                f"<b><i>w</i> = 1</b> → quality gap only "
                f"(A<sub>i</sub> − {l_html}); own level drops out.<br>"
                f"<b><i>w</i> = 0</b> → ability only; {l_html} ignored."
                "</div>"
            )

        _update_loo_l_hint_html()
        _update_score_formula_html()

        btn_defaults = widgets.Button(
            description="Load defaults from tier1_sim_config.py",
            layout=widgets.Layout(width="360px"),
        )
        btn_pool_530 = widgets.Button(
            description="530 pool cal",
            button_style="info",
            tooltip=(
                "530 forensics track: τ≈0.65, normal_clipped A, ability-only top-K. "
                "High overlap / median roster SD ~0.8 — NOT 539 assignment."
            ),
            layout=widgets.Layout(width="160px"),
        )
        btn_match_539 = widgets.Button(
            description="539 assign cal",
            button_style="warning",
            tooltip=(
                "539 Layer 0: τ from CELL 10c (~0.108), ability-only top-K, w=0. "
                "Re-run 10c after changing A draw, J, or seed."
            ),
            layout=widgets.Layout(width="160px"),
        )
        btn_selection_539 = widgets.Button(
            description="539 selection",
            button_style="success",
            tooltip=(
                "539 Layer 2: beta_2_2 A on [0,1], crowding_smooth, w=λ (~0.55). "
                "530 pool assignment (τ≈0.65). Teaching model for inverted-U."
            ),
            layout=widgets.Layout(width="160px"),
        )
        btn_run = widgets.Button(
            description="Run / refresh plot",
            button_style="primary",
            layout=widgets.Layout(width="200px"),
        )
        btn_seed_change = widgets.Button(
            description="Seed change",
            layout=widgets.Layout(width="140px"),
        )

        plot_a_label = widgets.HTML(
            value="<b>Plot A — interval overlap (530 CELL 8)</b>"
        )
        plot_widget_overlap, set_plot_overlap = _make_responsive_plot_widget(
            max_width_px=_PLOT_A_MAX_WIDTH_PX,
            placeholder="(Plot A hidden)",
        )
        plot_a_box = widgets.VBox(
            [plot_a_label, plot_widget_overlap],
            layout=widgets.Layout(
                align_items="flex-start",
                max_width=f"{_PLOT_A_MAX_WIDTH_PX}px",
            ),
        )
        plot_widget_inverted_u, set_plot_inverted_u = _make_responsive_plot_widget(
            max_width_px=_PLOT_B_MAX_WIDTH_PX,
            placeholder="(Plot B hidden)",
        )
        plot_b_header_html = widgets.HTML(
            value=(
                "<b>Plot B</b> — mean Y<sub>selected</sub> vs <b>L<sub>q</sub></b> bins "
                "(x-axis fixed; not Pool L in score)"
            )
        )
        plot_b_box = widgets.VBox(
            [
                plot_b_header_html,
                plot_widget_inverted_u,
            ],
            layout=widgets.Layout(
                align_items="flex-start",
                max_width=f"{_PLOT_B_MAX_WIDTH_PX}px",
            ),
        )
        plot_widget_ability, set_plot_ability = _make_responsive_plot_widget(
            max_width_px=_PLOT_C_MAX_WIDTH_PX,
            placeholder="(Plot C hidden)",
        )
        plot_c_box = widgets.VBox(
            [
                widgets.HTML(
                    value="<b>Plot C — synthetic $A_i$ vs 530 player-season perf</b>"
                ),
                plot_widget_ability,
            ],
            layout=widgets.Layout(
                align_items="flex-start",
                max_width=f"{_PLOT_C_MAX_WIDTH_PX}px",
            ),
        )
        _summary_col_style = (
            "font-family:ui-monospace,Menlo,monospace;font-size:11px;"
            "line-height:1.55;color:#222;white-space:normal;margin:0"
        )
        _summary_col_layout = widgets.Layout(
            align_items="flex-start",
            min_width="480px",
        )
        summary_pools_html = widgets.HTML(value="", layout=_summary_col_layout)
        summary_sel_html = widgets.HTML(value="", layout=_summary_col_layout)
        summary_footnote_html = widgets.HTML(
            value="",
            layout=widgets.Layout(align_self="flex-start", margin="0 0 8px 0"),
        )
        _summary_row = widgets.HBox(
            [summary_pools_html, summary_sel_html],
            layout=widgets.Layout(
                width="100%",
                flex_flow="row nowrap",
                align_items="flex-start",
            ),
        )
        # Back-compat alias for diagnostics / mirror cells
        summary_html = summary_pools_html
        _pg = {"busy": False, "listeners_on": False, "panel_displayed": False}

        def _params_from_widgets() -> AssignmentParams:
            base = AssignmentParams.from_module(_tier1_cfg)
            return AssignmentParams(
                n_teams=int(w_n_teams.value),
                roster_size=int(w_roster.value),
                target_mean_dist=w_target.value,
                target_mean_low=float(w_t_low.value),
                target_mean_high=float(w_t_high.value),
                target_mean_mu=base.target_mean_mu,
                target_mean_sigma=base.target_mean_sigma,
                assignment_kernel=w_kernel.value,
                assignment_temperature=float(w_tau.value),
                assignment_rho=base.assignment_rho,
                assignment_sigma=base.assignment_sigma,
                use_preferential_attachment=base.use_preferential_attachment,
                preferential_alpha=float(w_pref.value),
                preferential_k=base.preferential_k,
                ability_draw=w_ability.value,
                ability_mean=base.ability_mean,
                ability_sd=base.ability_sd,
                ability_clip_low=base.ability_clip_low,
                ability_clip_high=base.ability_clip_high,
                ability_student_t_df=base.ability_student_t_df,
                ability_student_t_scale=base.ability_student_t_scale,
                sorting_noise_sd=base.sorting_noise_sd,
                viability_theta=float(w_viability_theta.value),
                viability_sharpness=float(w_viability_gamma.value),
            )

        def _selection_from_widgets():
            from tier1_generative_eda import SelectionConfig

            base = SelectionConfig.from_module(_tier1_cfg)
            return SelectionConfig(
                n_bins=int(w_n_bins.value),
                bin_mode=str(w_bin_mode.value),
                n_selected=int(w_n_select.value),
                score_mode=str(w_score.value),
                loo_gap_weight=float(w_loo_w.value),
                winner_selection=str(w_winner.value),
                loo_pool_l_mode=str(w_loo_l_mode.value),
            )

        def _persist():
            try:
                PLAYGROUND_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
                PLAYGROUND_STATE_PATH.write_text(
                    json.dumps(
                        {
                            "n_teams": int(w_n_teams.value),
                            "roster_size": int(w_roster.value),
                            "tau": float(w_tau.value),
                            "kernel": str(w_kernel.value),
                            "target_dist": str(w_target.value),
                            "t_low": float(w_t_low.value),
                            "t_high": float(w_t_high.value),
                            "pref_alpha": float(w_pref.value),
                            "ability_draw": str(w_ability.value),
                            "seed": int(w_seed.value),
                            "show_chop": _show_chop_enabled(),
                        "show_plot_a": _show_plot_a_enabled(),
                        "show_plot_b": _show_plot_b_enabled(),
                        "show_plot_c": _show_plot_c_enabled(),
                            "n_bins": int(w_n_bins.value),
                            "bin_mode": str(w_bin_mode.value),
                            "n_selected": int(w_n_select.value),
                            "score_mode": str(w_score.value),
                            "loo_gap_weight": float(w_loo_w.value),
                            "winner_selection": str(w_winner.value),
                            "loo_pool_l_mode": str(w_loo_l_mode.value),
                            "viability_theta": float(w_viability_theta.value),
                            "viability_sharpness": float(w_viability_gamma.value),
                        },
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n",
                    encoding="utf-8",
                )
            except OSError:
                pass

        def _sync_plot_a_visibility():
            disp = "" if _show_plot_a_enabled() else "none"
            plot_a_box.layout.display = disp

        def _sync_plot_b_visibility():
            disp = "" if _show_plot_b_enabled() else "none"
            plot_b_box.layout.display = disp

        def _sync_plot_c_visibility():
            disp = "" if _show_plot_c_enabled() else "none"
            plot_c_box.layout.display = disp

        def _coverage_curve(teams, grid: np.ndarray) -> np.ndarray:
            lo = teams["min"].to_numpy(dtype=float)
            hi = teams["max"].to_numpy(dtype=float)
            cov = np.zeros(len(grid), dtype=float)
            for a, b in zip(lo, hi):
                cov += (grid >= a) & (grid <= b)
            return cov

        def _figure_ability_distribution(
            ability: np.ndarray,
            ability_draw: str,
            *,
            n_draw: int,
        ) -> object:
            import matplotlib.pyplot as plt

            from sports_pipeline.empirical_perf_fit import overlay_530_reference_on_axis

            a = np.asarray(ability, dtype=float)
            fig, ax = plt.subplots(figsize=(8.5, 4.2))
            n_bins = int(min(60, max(24, round(np.sqrt(a.size)))))
            ax.hist(
                a,
                bins=n_bins,
                density=True,
                color="steelblue",
                edgecolor="white",
                alpha=0.82,
                label=rf"synthetic $A_i$ (N={n_draw:,})",
            )
            xlab, had_hist = overlay_530_reference_on_axis(ax)
            if not had_hist:
                ax.text(
                    0.02,
                    0.97,
                    "Re-run 530 CELL 5b to save 530 histogram overlay",
                    transform=ax.transAxes,
                    fontsize=8,
                    va="top",
                    color="#555",
                )
            ax.set_xlabel(xlab)
            ax.set_ylabel("Density")
            ax.set_title(
                f"538 CELL 10 — $A_i$ distribution vs 530  |  draw={ability_draw!r}"
            )
            ax.legend(fontsize=8, loc="upper right")
            fig.tight_layout()
            return fig

        def redraw(_=None):
            import matplotlib.pyplot as plt

            from tier1_generative_eda import (
                PLOT_B_XAXIS_LABEL,
                PLOT_B_XAXIS_TEAM_MEAN_LABEL,
                figure_inverted_u,
                inverted_u_bin_table,
                inverted_u_bin_table_team_mean,
                plot_b_figure_title,
                selection_rank_formula,
            )
            from sports_pipeline.panel_build import assign_poolq_bin_labels

            if _pg["busy"]:
                return
            _pg["busy"] = True
            was_interactive = plt.isinteractive()
            plt.ioff()
            try:
                summary_pools_html.value = ""
                summary_sel_html.value = ""
                summary_footnote_html.value = ""
                params = _params_from_widgets()
                rng = np.random.default_rng(int(w_seed.value))
                n = params.n_individuals
                ability = draw_abilities(
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
                _sync_plot_c_visibility()
                if _show_plot_c_enabled():
                    fig_c = _figure_ability_distribution(
                        ability,
                        params.ability_draw,
                        n_draw=n,
                    )
                    buf_c = io.BytesIO()
                    fig_c.savefig(buf_c, format="png", dpi=_PLOT_C_DPI, bbox_inches="tight")
                    plt.close(fig_c)
                    set_plot_ability(buf_c.getvalue())
                else:
                    set_plot_ability(None)

                team_targets = draw_target_means(
                    rng,
                    params.n_teams,
                    target_mean_dist=params.target_mean_dist,
                    target_mean_low=params.target_mean_low,
                    target_mean_high=params.target_mean_high,
                    target_mean_mu=params.target_mean_mu,
                    target_mean_sigma=params.target_mean_sigma,
                )
                pool_soft = soft_assign(
                    rng,
                    ability,
                    team_targets,
                    params.roster_size,
                    assignment_kernel=params.assignment_kernel,
                    assignment_temperature=params.assignment_temperature,
                    preferential_alpha=params.preferential_alpha,
                    preferential_k=params.preferential_k,
                )
                players_soft = build_roster_dataframe(ability, pool_soft, team_targets)
                teams_soft = roster_team_stats(players_soft)

                peak_chop = None
                peak_soft = float("nan")
                med_sd = float(teams_soft["pool_sd"].median())
                _sync_plot_a_visibility()
                if _show_plot_a_enabled():
                    grid = np.linspace(-2.0, 2.0, 81)
                    cov_soft = _coverage_curve(teams_soft, grid)
                    peak_soft = float(cov_soft.max())
                    fig, ax = plt.subplots(figsize=(9.0, 4.8))
                    ax.plot(
                        grid, cov_soft, color="C0", lw=2.0, label="soft assign (Thread A)"
                    )
                    if _show_chop_enabled():
                        pool_chop = assign_sort_chop_benchmark(
                            rng,
                            ability,
                            params.n_teams,
                            sorting_noise_sd=params.sorting_noise_sd,
                        )
                        teams_chop = roster_team_stats(
                            build_roster_dataframe(ability, pool_chop, team_targets)
                        )
                        cov_chop = _coverage_curve(teams_chop, grid)
                        peak_chop = float(cov_chop.max())
                        ax.plot(
                            grid,
                            cov_chop,
                            color="C3",
                            ls="--",
                            lw=1.8,
                            label="sort-and-chop (537 B)",
                        )
                    ax.axhline(1.0, color="0.5", ls=":", lw=1.0)
                    ax.set_xlabel("Ability axis (synthetic perf)")
                    ax.set_ylabel("Teams covering grid point")
                    ax.set_title("538 CELL 10 — interval overlap (530 CELL 8 analog)")
                    ax.legend(loc="upper right")
                    ax.set_ylim(bottom=0)
                    fig.tight_layout()
                    buf = io.BytesIO()
                    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight")
                    plt.close(fig)
                    set_plot_overlap(buf.getvalue())
                else:
                    set_plot_overlap(None)

                sel = _selection_from_widgets()
                players_sel = assign_selection(
                    players_soft,
                    rng,
                    n_selected=sel.n_selected,
                    score_mode=sel.score_mode,
                    loo_gap_weight=sel.loo_gap_weight,
                    winner_selection=sel.winner_selection,
                    pool_l_mode=sel.loo_pool_l_mode,
                    viability_theta=params.viability_theta,
                    viability_sharpness=params.viability_sharpness,
                )
                summ_u = inverted_u_bin_table_team_mean(
                    players_sel,
                    sel,
                    assign_poolq_bin_labels=assign_poolq_bin_labels,
                ) if _plot_b_team_mean_enabled() else inverted_u_bin_table(
                    players_sel,
                    sel,
                    assign_poolq_bin_labels=assign_poolq_bin_labels,
                    tpa=_tpa,
                )
                _plot_b_539_axis = _plot_b_team_mean_enabled()
                rank_line = selection_rank_formula(
                    sel.score_mode,
                    loo_gap_weight=sel.loo_gap_weight,
                    pool_l_mode=sel.loo_pool_l_mode,
                    tpa=_tpa,
                )
                if _plot_b_539_axis:
                    plot_b_header_html.value = (
                        "<b>Plot B′</b> — mean Y<sub>selected</sub> vs "
                        "<b>team_mean</b> bins (539-style)<br>"
                        f"<span style='font-size:11px;color:#444'>{rank_line}</span>"
                    )
                else:
                    plot_b_header_html.value = (
                        f"<b>Plot B</b> — mean Y<sub>selected</sub> vs <b>L<sub>q</sub></b> bins "
                        f"(530-style)<br>"
                        f"<span style='font-size:11px;color:#444'>{rank_line}</span>"
                    )
                _sync_plot_b_visibility()
                if _show_plot_b_enabled():
                    fig_u = figure_inverted_u(
                        summ_u,
                        title=plot_b_figure_title(
                            sel, tpa=_tpa, team_mean_axis=_plot_b_539_axis
                        ),
                        n_bins=sel.n_bins,
                        n_teams=params.n_teams,
                        loo_pool_l_mode=sel.loo_pool_l_mode,
                        x_col="mean_team_mean" if _plot_b_539_axis else None,
                        xlabel=(
                            PLOT_B_XAXIS_TEAM_MEAN_LABEL
                            if _plot_b_539_axis
                            else PLOT_B_XAXIS_LABEL
                        ),
                        tpa=_tpa,
                    )
                    buf_u = io.BytesIO()
                    fig_u.savefig(buf_u, format="png", dpi=120, bbox_inches="tight")
                    plt.close(fig_u)
                    set_plot_inverted_u(buf_u.getvalue())
                else:
                    set_plot_inverted_u(None)

                selection_rate = float(players_sel["Y_selected"].mean())
                peak_bin_rate = (
                    float(summ_u["selection_rate"].max()) if len(summ_u) else 0.0
                )

                if _show_plot_a_enabled() and peak_chop is not None:
                    chop_line = f"sort_chop peak={peak_chop:.0f}"
                elif _show_plot_a_enabled():
                    chop_line = "sort_chop overlay off"
                else:
                    chop_line = "Plot A off (overlap not computed)"
                slow_note = (
                    "  |  (J>500: assignment may take 10–60s)"
                    if params.n_teams > 500
                    else ""
                )
                cov_line = (
                    f"soft: coverage_peak={peak_soft:.0f}  median_pool_sd={med_sd:.3f}"
                    if _show_plot_a_enabled()
                    else f"soft: median_pool_sd={med_sd:.3f}  (coverage skipped)"
                )
                target_suffix = (
                    " (530 empirical fit)"
                    if params.target_mean_dist == "empirical_530"
                    else f" [{params.target_mean_low:.2f}, {params.target_mean_high:.2f}]"
                )
                gamma_line = (
                    f"γ={params.viability_sharpness:.1f}<br>"
                    if str(sel.loo_pool_l_mode).strip().lower() == "crowding_smooth"
                    else ""
                )
                summary_pools_html.value = (
                    f"<div style='{_summary_col_style}'>"
                    "<b>Pools</b><br>"
                    f"J={params.n_teams} &nbsp; roster={params.roster_size} &nbsp; "
                    f"N={n:,} &nbsp; τ={params.assignment_temperature:.3f}<br>"
                    f"kernel={params.assignment_kernel!r}<br>"
                    f"{_T}={params.target_mean_dist}{target_suffix}<br>"
                    f"α_pref={params.preferential_alpha:.2f}<br>"
                    f"{cov_line}<br>"
                    f"{chop_line}{slow_note}"
                    "</div>"
                )
                plot_b_axis_line = (
                    "Plot B′ bins: team_mean (539-style)"
                    if _plot_b_539_axis
                    else "Plot B bins: L<sub>q</sub> (530-style)"
                )
                summary_sel_html.value = (
                    f"<div style='{_summary_col_style}'>"
                    "<b>Selection</b><br>"
                    f"{rank_line}<br>"
                    f"K={sel.n_selected} &nbsp; winner={sel.winner_selection!r}<br>"
                    f"{plot_b_axis_line} &nbsp; "
                    f"({sel.n_bins} {sel.bin_mode})<br>"
                    f"Pool L in score={sel.loo_pool_l_mode!r} &nbsp; "
                    f"w={sel.loo_gap_weight:.2f} &nbsp; θ={params.viability_theta:.3f}<br>"
                    f"{gamma_line}"
                    f"overall_rate={selection_rate:.4f} &nbsp; "
                    f"peak_bin_rate={peak_bin_rate:.4f}"
                    "</div>"
                )
                plot_b_footnote = (
                    "Plot B′: y = mean Y_selected; x = pool team_mean (539 notebook style)."
                    if _plot_b_539_axis
                    else "Plot B: y = mean Y_selected; x = L_Q (530 comparability)."
                )
                summary_footnote_html.value = (
                    "<span style='color:#555;font-size:10px;font-family:ui-monospace,Menlo,monospace'>"
                    "Plot A: 530 CELL 8 overlap. "
                    f"{plot_b_footnote} Pool L in score is independent of Plot B x-axis."
                    "</span>"
                )
                _persist()
            finally:
                if was_interactive:
                    plt.ion()
                else:
                    plt.ioff()
                _pg["busy"] = False

        _update_loo_l_hint_html()
        _update_score_formula_html()

        def _seed_change(_=None):
            """New random seed, then redraw (via w_seed value observer)."""
            w_seed.value = int(np.random.default_rng().integers(0, 100_000))

        def _apply_widget_state(d: dict) -> None:
            w_n_teams.value = int(d["n_teams"])
            w_roster.value = int(d["roster_size"])
            w_tau.value = float(d["tau"])
            w_kernel.value = str(d["kernel"])
            w_target.value = str(d["target_dist"])
            w_t_low.value = float(d["t_low"])
            w_t_high.value = float(d["t_high"])
            w_pref.value = float(d["pref_alpha"])
            w_ability.value = str(d["ability_draw"])
            w_seed.value = int(d["seed"])
            w_n_bins.value = int(d["n_bins"])
            w_bin_mode.value = str(d["bin_mode"])
            w_n_select.value = int(d["n_selected"])
            w_score.value = str(d["score_mode"])
            w_loo_w.value = float(d["loo_gap_weight"])
            w_winner.value = str(d["winner_selection"])
            w_loo_l_mode.value = str(d["loo_pool_l_mode"])
            w_viability_theta.value = float(d["viability_theta"])
            w_viability_gamma.value = float(d["viability_sharpness"])

        def _load_defaults(_=None):
            _spec.loader.exec_module(_tier1_cfg)  # type: ignore[union-attr]
            _apply_widget_state(_defaults())
            _update_loo_l_hint_html()
            _update_score_formula_html()
            _sync_gamma_slider_visibility()
            redraw()

        def _load_pool_530(_=None):
            _spec.loader.exec_module(_tier1_cfg)  # type: ignore[union-attr]
            _apply_widget_state(_pool_530_defaults())
            _update_loo_l_hint_html()
            _update_score_formula_html()
            _sync_gamma_slider_visibility()
            redraw()

        def _load_match_539(_=None):
            _spec.loader.exec_module(_tier1_cfg)  # type: ignore[union-attr]
            _apply_widget_state(_match_539_defaults())
            _update_loo_l_hint_html()
            _update_score_formula_html()
            _sync_gamma_slider_visibility()
            redraw()

        def _load_selection_539(_=None):
            _spec.loader.exec_module(_tier1_cfg)  # type: ignore[union-attr]
            _apply_widget_state(_selection_539_defaults())
            _update_loo_l_hint_html()
            _update_score_formula_html()
            _sync_gamma_slider_visibility()
            redraw()

        def _wire_listeners():
            if _pg["listeners_on"]:
                return
            controls = (
                w_n_teams,
                w_roster,
                w_tau,
                w_kernel,
                w_target,
                w_t_low,
                w_t_high,
                w_pref,
                w_ability,
                w_seed,
                w_loo_l_mode,
                w_viability_theta,
                w_viability_gamma,
                w_n_bins,
                w_bin_mode,
                w_n_select,
                w_score,
                w_loo_w,
                w_winner,
            )
            for w in controls:
                w.observe(redraw, names="value")
            w_score.observe(_update_score_formula_html, names="value")
            w_loo_w.observe(_update_score_formula_html, names="value")
            w_loo_l_mode.observe(_update_score_formula_html, names="value")
            w_ability.observe(_update_score_formula_html, names="value")
            w_loo_l_mode.observe(_on_loo_pool_context_change, names="value")
            w_viability_theta.observe(_on_loo_pool_context_change, names="value")
            w_viability_gamma.observe(_on_loo_pool_context_change, names="value")
            btn_run.on_click(redraw)
            btn_seed_change.on_click(_seed_change)
            btn_defaults.on_click(_load_defaults)
            btn_pool_530.on_click(_load_pool_530)
            btn_match_539.on_click(_load_match_539)
            btn_selection_539.on_click(_load_selection_539)
            _pg["listeners_on"] = True

        _CELL10_SLIDER_WIDGETS = (
            w_n_teams,
            w_roster,
            w_tau,
            w_t_low,
            w_t_high,
            w_pref,
            w_seed,
            w_viability_theta,
            w_viability_gamma,
            w_n_bins,
            w_n_select,
            w_loo_w,
        )

        def build_cell10_slider_mirrors():
            """Mirror sliders for Cursor; sync to backend and call redraw.

            Run sliders A→B→C once after the first playground init (kernel restart).
            Do not re-run playground just to refresh plots — it reuses live widgets.
            """
            mirrors = []
            for w in _CELL10_SLIDER_WIDGETS:
                cls = type(w)
                kw = {
                    "value": w.value,
                    "description": w.description,
                    "continuous_update": getattr(w, "continuous_update", False),
                    "layout": widgets.Layout(width="520px", min_height="32px"),
                    "style": {"description_width": "initial"},
                }
                for key in ("min", "max", "step", "readout_format"):
                    if hasattr(w, key):
                        kw[key] = getattr(w, key)
                m = cls(**kw)
                widgets.link((w, "value"), (m, "value"))

                def _mirror_changed(change, backend=w):
                    if backend.value != change["new"]:
                        backend.value = change["new"]
                    redraw()

                m.observe(_mirror_changed, names="value")
                mirrors.append(m)
            return mirrors
        _cell10_header = widgets.HTML(
            "<b>538 CELL 10</b> — generative lab (pools + selection). "
            "Adjust sliders → plots refresh. State → "
            "<code>tier1_cell10_playground_state.json</code>."
        )
        _pools_col = widgets.VBox(
            [
                widgets.HTML("<b>Pools (Thread A)</b>"),
                _sym_legend,
                w_n_teams,
                w_roster,
                w_tau,
                w_kernel,
                w_target,
                w_t_low,
                w_t_high,
                w_pref,
                w_ability,
                w_seed,
            ],
            layout=widgets.Layout(align_items="flex-start", min_width="480px"),
        )
        _sel_col = widgets.VBox(
            [
                widgets.HTML(
                    "<b>Selection</b> — who wins top-K "
                    "(Plot B bins on L<sub>q</sub> separately)"
                ),
                w_loo_l_mode,
                w_viability_theta,
                w_viability_gamma,
                loo_l_hint_html,
                w_n_bins,
                w_bin_mode,
                w_n_select,
                w_score,
                w_loo_w,
                score_formula_html,
                w_winner,
            ],
            layout=widgets.Layout(align_items="flex-start", min_width="480px"),
        )
        _footer_panel = widgets.VBox(
            [
                widgets.HBox(
                    [
                        btn_defaults,
                        btn_pool_530,
                        btn_match_539,
                        btn_selection_539,
                        btn_run,
                        btn_seed_change,
                    ]
                ),
                _summary_row,
                summary_footnote_html,
                plot_c_box,
                plot_a_box,
                plot_b_box,
            ],
            layout=widgets.Layout(align_items="flex-start"),
        )
        _controls_row = widgets.HBox(
            [_pools_col, _sel_col],
            layout=widgets.Layout(
                width="100%",
                flex_flow="row nowrap",
                align_items="flex-start",
            ),
        )
        _layout_panel = widgets.VBox(
            [
                _cell10_header,
                _controls_row,
                _footer_panel,
            ],
            layout=widgets.Layout(align_items="flex-start", width="100%"),
        )
        panel = _layout_panel

        def _schedule_initial_redraw() -> None:
            """First plot + gamma visibility after widget views attach."""

            _delay = float(globals().get("CELL10_DEFER_PLOT_SECONDS", 0.25))

            def _on_panel_first_display(_w=None) -> None:
                _pg["panel_displayed"] = True
                _sync_gamma_slider_visibility()
                if _delay <= 0:
                    return
                if _delay > 0:
                    try:
                        from IPython import get_ipython

                        ip = get_ipython()
                        loop = getattr(ip, "io_loop", None) if ip is not None else None
                        if loop is not None and hasattr(loop, "call_later"):
                            loop.call_later(_delay, redraw)
                            return
                    except Exception:
                        pass
                redraw()

            if hasattr(widgets.Widget, "on_displayed"):
                _layout_panel.on_displayed(_on_panel_first_display, remove=True)
            elif _delay > 0:
                _on_panel_first_display()

        _schedule_initial_redraw()
        display(_layout_panel)
        _wire_listeners()
        globals()["_CELL10_PLAYGROUND_LIVE"] = True
        globals()["w_tau"] = w_tau
        print("CELL 10: panel displayed — plots load shortly (or click Run / refresh plot)")
