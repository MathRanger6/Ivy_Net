# Exec target for 538D_widget_render_test.ipynb Test 8.
# Probe widget mix in the real CELL 10 nested layout (no matplotlib / redraw).

import ipywidgets as widgets
from IPython.display import display

# Valid 1×1 red PNG (same pattern as playground plot holders)
_MIN_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)

style = {"description_width": "168px"}
lay = widgets.Layout(width="460px")


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


def _dd(desc, opts):
    return widgets.Dropdown(
        options=opts, value=opts[0], description=desc, style=style, layout=lay
    )


w_n_teams = _slider("Teams J", 100, wtype="int", min=4, max=2500)
w_roster = _slider("Roster", 15, wtype="int", min=5, max=40)
w_tau = _slider("tau", 0.05, wtype="float", min=0.05, max=2.0)
w_kernel = _dd("Kernel", ["gaussian", "cauchy"])
w_target = _dd("Target T", ["uniform", "empirical_530"])
w_t_low = _slider("T low", -1.85, wtype="float")
w_t_high = _slider("T high", 7.4, wtype="float")
w_pref = _slider("pref", 0.0, wtype="float")
w_ability = _dd("A draw", ["normal", "empirical_530"])
w_seed = _slider("Seed", 42, wtype="int", min=0, max=99999)
w_loo_l_mode = _dd("Pool L", ["quality", "crowding"])
w_theta = _slider("theta", 0.71, wtype="float")
w_gamma = _slider("gamma", 18.0, wtype="float")
w_n_bins = _slider("bins", 20, wtype="int", min=5, max=30)
w_bin_mode = _dd("bin mode", ["quantile", "equal_width"])
w_n_select = _slider("K", 200, wtype="int", min=5, max=2000)
w_score = _dd("score", ["loo_gap_plus_ability"])
w_loo_w = _slider("w", 0.1, wtype="float", min=0, max=1)
w_winner = _dd("winner", ["A", "C"])

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
        w_n_bins,
        w_bin_mode,
        w_n_select,
        w_score,
        w_loo_w,
        w_winner,
    ],
    layout=widgets.Layout(align_items="flex-start", min_width="480px"),
)
_footer = widgets.VBox(
    [widgets.HBox([btn_run]), summary_html, plot_html],
    layout=widgets.Layout(align_items="flex-start"),
)
_layout = widgets.VBox(
    [
        widgets.HTML("<b>538 CELL 10 layout probe</b>"),
        widgets.HBox(
            [
                _pools_col,
                widgets.VBox([_sel_col, _footer], layout=widgets.Layout(align_items="flex-start")),
            ],
            layout=widgets.Layout(width="100%", flex_flow="row wrap", align_items="flex-start"),
        ),
    ],
    layout=widgets.Layout(align_items="flex-start", width="100%"),
)
display(_layout)
print("layout probe: nested HBox + footer (no matplotlib)")
