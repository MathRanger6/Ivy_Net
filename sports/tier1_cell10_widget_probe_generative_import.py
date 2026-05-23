# Test 11 — import tier1_generative_eda (pulls matplotlib) BEFORE ipywidgets display.
# Expected: sliders missing if matplotlib-before-widgets is the root cause.

from tier1_generative_eda import SelectionConfig  # noqa: F401 — imports matplotlib.pyplot

import ipywidgets as widgets
from IPython.display import display

print("=== Test 11: generative_eda import before widgets ===")
_sl = [widgets.IntSlider(value=i, min=0, max=10, description=f"s{i}") for i in range(6)]
display(widgets.VBox(_sl))
print("Test 11 done — sliders visible?")
