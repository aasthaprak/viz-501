"""simpleviz — a small, opinionated visualization library built on matplotlib.

The goal is to make good-looking, readable charts with almost no boilerplate.
Every chart function shares the same conventions:

* A validated, colorblind-aware categorical palette is applied automatically.
* Chrome is recessive (thin axes, light gridlines, no top/right spines).
* Functions accept an optional ``ax`` so charts compose into subplots, and
  return the :class:`~matplotlib.axes.Axes` they drew on.
* Passing ``save="name.png"`` writes the figure to disk.

Example
-------
>>> import simpleviz as sv
>>> sv.bar(["A", "B", "C"], [3, 7, 5], title="Scores", save="scores.png")

See ``examples/demo.py`` for a gallery of every chart type.
"""

from .theme import PALETTE, use_theme, color
from .charts import bar, barh, line, scatter, hist, pie

__version__ = "0.1.0"

__all__ = [
    "PALETTE",
    "use_theme",
    "color",
    "bar",
    "barh",
    "line",
    "scatter",
    "hist",
    "pie",
    "__version__",
]

# Apply the theme on import so charts look consistent out of the box.
use_theme()
