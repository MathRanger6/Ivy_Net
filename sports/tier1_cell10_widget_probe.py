# Exec target for 538D_widget_render_test.ipynb Test 5.
# Same widget mix as Test 4 but created inside exec().

import ipywidgets as widgets
from IPython.display import display

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


kids = [
    widgets.HTML("<b>Pools</b>"),
    _slider("Teams J", 100, wtype="int", min=4, max=2500),
    _slider("Roster", 15, wtype="int", min=5, max=40),
    _slider("tau", 0.05, wtype="float", min=0.05, max=2.0),
    _dd("Kernel", ["gaussian", "cauchy"]),
    _dd("Target T", ["uniform", "empirical_530"]),
    _slider("T low", -1.85, wtype="float"),
    _slider("T high", 7.4, wtype="float"),
    _slider("pref", 0.0, wtype="float"),
    _dd("A draw", ["normal", "empirical_530"]),
    _slider("Seed", 42, wtype="int", min=0, max=99999),
    widgets.HTML("<b>Selection</b>"),
    _dd("Pool L", ["quality", "crowding"]),
    _slider("theta", 0.71, wtype="float"),
    _slider("gamma", 18.0, wtype="float"),
    _slider("bins", 20, wtype="int", min=5, max=30),
    _dd("bin mode", ["quantile", "equal_width"]),
    _slider("K", 200, wtype="int", min=5, max=2000),
    _dd("score", ["loo_gap_plus_ability"]),
    _slider("w", 0.1, wtype="float", min=0, max=1),
    _dd("winner", ["A", "C"]),
]
display(widgets.VBox(kids, layout=widgets.Layout(align_items="flex-start")))
print(f"probe exec: {len(kids)} children")
