# Incremental CELL 10 playground rebuild — bisect slider rendering.
# Re-run the BISECT cell in 538D_widget_render_test.ipynb after each step change.
#
# Roadmap (one step added per iteration):
#   Step 1  Nested layout + full 12-slider / 7-dropdown probe mix
#   Step 2  + tier1_pool_assignment import + tier1_sim_config load
#   Step 3  + real tuple dropdown options (pool_l_dropdown_options, …)
#   Step 4  + _sym_legend HTML block
#   Step 5  + loo_l_hint_html + score_formula_html + pre-display updates
#   Step 6  + gamma layout.display toggle (DEFERRED until after display)  [CURRENT]
#           Pre-display layout.display="none" on sliders breaks ALL slider views.
#   Step 7  + full footer (3 plot boxes, 3 buttons, summary HTML)
#   Step 8  + redraw() stub (updates summary text only, no matplotlib)
#   Step 9  + matplotlib redraw (plot PNG into HTML holders)
#   Step 10 + full simulation body from tier1_cell10_playground_run.py

BISECT_STEP = 6

import importlib.util
import sys
from pathlib import Path

import ipywidgets as widgets
from IPython.display import display


def _sports_dir() -> Path:
    cwd = Path.cwd().resolve()
    for candidate in (cwd / "sports", cwd):
        if (candidate / "tier1_sim_config.py").is_file():
            return candidate
    raise FileNotFoundError(
        f"Cannot find tier1_sim_config.py — run from repo root (cwd={cwd})"
    )


_SPORTS = _sports_dir()
if str(_SPORTS) not in sys.path:
    sys.path.insert(0, str(_SPORTS))

# --- Step 2: tier1 imports BEFORE widget creation (same as playground_run.py) ---
import tier1_pool_assignment as _tpa  # noqa: F401
from tier1_pool_assignment import (
    AssignmentParams,
    pool_l_dropdown_options,
    pool_l_html_label,
)

_CFG_PATH = _SPORTS / "tier1_sim_config.py"
_spec = importlib.util.spec_from_file_location("tier1_sim_config", _CFG_PATH)
_tier1_cfg = importlib.util.module_from_spec(_spec)
assert _spec is not None and _spec.loader is not None
_spec.loader.exec_module(_tier1_cfg)
_bisect_params = AssignmentParams.from_module(_tier1_cfg)
print(
    f"Step {BISECT_STEP}: tier1 loaded — default n_teams={_bisect_params.n_teams}, "
    f"roster={_bisect_params.roster_size}"
)

_MIN_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)

style = {"description_width": "168px"}
lay = widgets.Layout(width="460px")

# --- Step 4: symbol legend (unicode subscripts in HTML, not slider descriptions) ---
_A = "A\u1d62"  # Aᵢ
_T = "T\u2c7c"  # Tⱼ
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


def _slider(desc, val, wtype="int", **kw):
    cls = widgets.IntSlider if wtype == "int" else widgets.FloatSlider
    return cls(
        value=val,
        description=desc,
        style=style,
        layout=lay,
        continuous_update=False,
        **kw,
    )


lay_wide = widgets.Layout(width="520px")


def _dd(desc, opts):
    return widgets.Dropdown(
        options=opts, value=opts[0], description=desc, style=style, layout=lay
    )


def _dd_tuple(desc, options, value, *, wide=False):
    valid = {v for _, v in options}
    val = str(value).strip()
    if val not in valid:
        val = options[0][1]
    return widgets.Dropdown(
        options=options,
        value=val,
        description=desc,
        style=style,
        layout=lay_wide if wide else lay,
    )


# --- Steps 1–2: sliders + probe labels; Step 3: real tuple dropdown options ---
_TARGET_DIST_OPTIONS = [
    ("Uniform", "uniform"),
    ("Normal clipped", "normal_clipped"),
    ("530 fitted perf (within-season z)", "empirical_530"),
]
_BIN_MODE_OPTIONS = [
    ("Equal count (quantile)", "quantile"),
    ("Equal width on LOO L", "equal_width"),
]
_SCORE_MODE_OPTIONS = [
    ("Pool-adjusted ability — w slider below", "loo_gap_plus_ability"),
    ("Ability only (ignores w)", "ability"),
]
_WINNER_OPTIONS = [
    ("C: Top-K — K highest scores win (deterministic)", "C"),
    ("A: Weighted — sample K without replacement by score", "A"),
    ("B: Bernoulli — each person selected independently", "B"),
]
_LOO_L_MODE_OPTIONS = pool_l_dropdown_options()

w_n_teams = _slider("Teams J", _bisect_params.n_teams, wtype="int", min=4, max=2500)
w_roster = _slider("Roster", _bisect_params.roster_size, wtype="int", min=5, max=40)
w_tau = _slider("tau", _bisect_params.assignment_temperature, wtype="float", min=0.05, max=2.0)
w_kernel = _dd("Kernel", ["gaussian", "cauchy"])
w_target = _dd_tuple(
    "Target T", _TARGET_DIST_OPTIONS, _bisect_params.target_mean_dist, wide=True
)
w_t_low = _slider("T low", _bisect_params.target_mean_low, wtype="float")
w_t_high = _slider("T high", _bisect_params.target_mean_high, wtype="float")
w_pref = _slider("pref", _bisect_params.preferential_alpha, wtype="float")
w_ability = _dd(
    "A draw",
    ["normal_clipped", "normal_plus_student_t", "uniform_01", "empirical_530"],
)
w_ability.value = str(_bisect_params.ability_draw)
w_seed = _slider("Seed", int(getattr(_tier1_cfg, "RANDOM_SEED", 42)), wtype="int", min=0, max=99999)
w_loo_l_mode = _dd_tuple(
    "Pool L", _LOO_L_MODE_OPTIONS, getattr(_tier1_cfg, "LOO_POOL_L_MODE", "quality"), wide=True
)
w_theta = _slider("theta", float(getattr(_tier1_cfg, "VIABILITY_THETA", 0.71)), wtype="float")
w_gamma = _slider("gamma", float(getattr(_tier1_cfg, "VIABILITY_SHARPNESS", 18.0)), wtype="float")
loo_l_hint_html = widgets.HTML(layout=widgets.Layout(width="520px", margin="0 0 4px 0"))
w_n_bins = _slider("bins", int(getattr(_tier1_cfg, "GENERATIVE_N_BINS", 20)), wtype="int", min=5, max=30)
w_bin_mode = _dd_tuple(
    "bin mode", _BIN_MODE_OPTIONS, getattr(_tier1_cfg, "GENERATIVE_POOLQ_BINNING", "quantile"), wide=True
)
w_n_select = _slider("K", int(getattr(_tier1_cfg, "N_SELECTED", 200)), wtype="int", min=5, max=2000)
w_score = _dd_tuple(
    "score",
    _SCORE_MODE_OPTIONS,
    getattr(_tier1_cfg, "SELECTION_SCORE_MODE", "loo_gap_plus_ability"),
    wide=True,
)
w_loo_w = _slider("w", float(getattr(_tier1_cfg, "LOO_GAP_WEIGHT", 0.1)), wtype="float", min=0, max=1)
score_formula_html = widgets.HTML(layout=widgets.Layout(width="520px", margin="0 0 4px 0"))
w_winner = _dd_tuple(
    "winner", _WINNER_OPTIONS, getattr(_tier1_cfg, "WINNER_SELECTION", "C"), wide=True
)


# --- Step 5–6: dynamic HTML hints; gamma visibility AFTER display only ---
def _sync_gamma_slider_visibility(_=None):
    mode = str(w_loo_l_mode.value).strip().lower()
    w_gamma.layout.display = "" if mode == "crowding_smooth" else "none"


def _loo_w_slider_label(pool_l_mode: str) -> str:
    if _tpa.is_crowding_l_mode(pool_l_mode):
        return "Crowding weight w"
    return "Quality-gap weight w"


def _update_loo_l_hint_html(_=None):
    mode = str(w_loo_l_mode.value).strip().lower()
    l_html = pool_l_html_label(mode)
    th = float(w_theta.value)
    gam = float(w_gamma.value)
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
        f"Active regressor: <b>{l_html}</b> — {detail}"
        "</div>"
    )


def _update_score_formula_html(_=None):
    pool_mode = str(w_loo_l_mode.value)
    w_loo_w.description = _loo_w_slider_label(pool_mode)
    w = float(w_loo_w.value)
    l_html = pool_l_html_label(pool_mode)
    if str(w_score.value) == "ability":
        score_formula_html.value = (
            f"<div style='{_SCORE_HELP_STYLE}'>"
            "<b>Score</b> = A<sub>i</sub> (ability only; <i>w</i> unused)."
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
        score_formula_html.value = (
            f"<div style='{_SCORE_HELP_STYLE}'>"
            f"<b>Score</b> = A<sub>i</sub> − <i>w</i>·{l_html} &nbsp;&nbsp;|&nbsp;&nbsp; "
            f"<b><i>w</i> = {w:.2f}</b><br>"
            f"<span style='color:#444;font-size:12px'>{sub}</span><br><br>"
            f"<b><i>w</i> = 1</b> → ability minus crowding term only.<br>"
            f"<b><i>w</i> = 0</b> → ability only; crowding ignored."
            "</div>"
        )
        return
    score_formula_html.value = (
        f"<div style='{_SCORE_HELP_STYLE}'>"
        f"<b>Score</b> = <i>w</i>·(A<sub>i</sub> − {l_html}) + (1−<i>w</i>)·A<sub>i</sub><br>"
        f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;= "
        f"A<sub>i</sub> − <i>w</i>·{l_html} &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b><i>w</i> = {w:.2f}</b><br><br>"
        f"<b><i>w</i> = 1</b> → quality gap only "
        f"(A<sub>i</sub> − {l_html}); own level drops out.<br>"
        f"<b><i>w</i> = 0</b> → ability only; {l_html} ignored."
        "</div>"
    )


_update_loo_l_hint_html()
_update_score_formula_html()

btn_run = widgets.Button(description="Run / refresh plot", button_style="primary")
plot_html = widgets.HTML(
    value=(
        f'<img alt="plot" src="data:image/png;base64,{_MIN_PNG_B64}" '
        'style="display:block;max-width:400px;" />'
    )
)
summary_html = widgets.HTML(value="<i>(summary placeholder)</i>")

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
        widgets.HTML("<b>Selection (inverted-U preview)</b>"),
        w_loo_l_mode,
        w_theta,
        w_gamma,
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
_footer = widgets.VBox(
    [widgets.HBox([btn_run]), summary_html, plot_html],
    layout=widgets.Layout(align_items="flex-start"),
)
panel = widgets.VBox(
    [
        widgets.HTML(f"<b>BISECT Step {BISECT_STEP}</b> — incremental playground rebuild"),
        widgets.HBox(
            [
                _pools_col,
                widgets.VBox(
                    [_sel_col, _footer],
                    layout=widgets.Layout(align_items="flex-start"),
                ),
            ],
            layout=widgets.Layout(
                width="100%", flex_flow="row wrap", align_items="flex-start"
            ),
        ),
    ],
    layout=widgets.Layout(align_items="flex-start", width="100%"),
)

if hasattr(widgets.Widget, "on_displayed"):
    panel.on_displayed(lambda _: _sync_gamma_slider_visibility(), remove=True)

display(panel)
print(f"BISECT Step {BISECT_STEP}: displayed — sliders visible? (gamma hide deferred)")
