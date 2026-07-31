"""Core of simple_viz — theme, palette, and chart functions.

Every chart shares one contract: data first, optional ``title`` / ``xlabel`` /
``ylabel`` / ``ax`` / ``save`` keywords, and each returns the Axes it drew on.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager as _fm
from matplotlib.axes import Axes

# Poppins is bundled with the package so charts look identical everywhere.
_FONT_DIR = Path(__file__).parent / "fonts"
_FONT = "Poppins"


def _register_fonts() -> str:
    """Register the bundled Poppins weights; return the family name to use.

    Falls back to the default sans-serif family if the files are missing.
    """
    if not _FONT_DIR.is_dir():
        return "sans-serif"
    for ttf in _FONT_DIR.glob("*.ttf"):
        try:
            _fm.fontManager.addfont(str(ttf))
        except Exception:  # pragma: no cover - never break import over a font
            pass
    return _FONT if any(f.name == _FONT for f in _fm.fontManager.ttflist) else "sans-serif"

#: Deep jewel-tone categorical order — rich, saturated hues that stay elegant
#: on a light surface. Ordered so adjacent slots remain distinguishable under
#: common forms of color vision deficiency (validated: worst adjacent CVD
#: ΔE 17, normal-vision ΔE 18.9, all >= 3:1 contrast). Assigned in order, never
#: cycled arbitrarily: the Nth series always gets slot N.
PALETTE = [
    "#1e4fa3",  # sapphire blue
    "#0f7a55",  # emerald green
    "#5c3a8e",  # amethyst violet
    "#0a97a8",  # deep teal
    "#a31d3f",  # ruby red
    "#b57e08",  # amber gold
    "#8e2c62",  # plum
    "#c25a20",  # burnt orange
]

# Chrome / ink colors (light surface). Warm near-black ink + a soft ivory
# surface give the jewel tones a more elevated, gallery-like setting.
_INK, _INK2, _MUTED, _GRID, _SURFACE = "#171310", "#5a544e", "#9b968e", "#eae7e0", "#fbfaf7"


def color(i: int) -> str:
    """Categorical color for slot ``i`` (0-based); wraps past the palette end."""
    return PALETTE[i % len(PALETTE)]


def use_theme() -> None:
    """Apply the simple_viz look to matplotlib's rcParams (done on import)."""
    family = _register_fonts()
    mpl.rcParams.update({
        "axes.prop_cycle": mpl.cycler(color=PALETTE),
        "figure.facecolor": _SURFACE, "axes.facecolor": _SURFACE, "savefig.facecolor": _SURFACE,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": _MUTED, "axes.linewidth": 0.8,
        "axes.grid": True, "axes.axisbelow": True, "grid.color": _GRID, "grid.linewidth": 0.6,
        # Bundled Poppins (geometric sans) with graceful fallback.
        "font.family": family,
        "font.sans-serif": [_FONT, "Helvetica Neue", "Arial",
                            "Liberation Sans", "DejaVu Sans"],
        "font.size": 11,
        "axes.titlesize": 14, "axes.titleweight": "bold", "axes.titlecolor": _INK,
        "axes.titlelocation": "left", "axes.titlepad": 16,
        "axes.labelcolor": _INK2, "axes.labelsize": 11, "text.color": _INK,
        "xtick.color": _MUTED, "ytick.color": _MUTED, "xtick.labelsize": 10, "ytick.labelsize": 10,
        "lines.linewidth": 2.0, "lines.markersize": 6,
        "legend.frameon": False, "legend.fontsize": 10,
        "figure.figsize": (8, 5), "figure.dpi": 110, "savefig.dpi": 150, "savefig.bbox": "tight",
    })


def _finish(ax, title, xlabel, ylabel, save) -> Axes:
    """Apply shared labels, optionally save, and return the Axes."""
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if save:
        ax.figure.savefig(save)
    return ax


def _axes(ax) -> Axes:
    return ax if ax is not None else plt.subplots()[1]


def bar(labels, values, *, title=None, xlabel=None, ylabel=None, ax=None, save=None) -> Axes:
    """Vertical bar chart of ``values`` labeled by ``labels``."""
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    ax = _axes(ax)
    ax.bar(range(len(values)), values, color=color(0), width=0.68, zorder=3)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels([str(x) for x in labels])
    ax.grid(axis="x", visible=False)
    return _finish(ax, title, xlabel, ylabel, save)


def barh(labels, values, *, title=None, xlabel=None, ylabel=None, ax=None, save=None) -> Axes:
    """Horizontal bar chart — good for long or many category labels."""
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    ax = _axes(ax)
    ax.barh(range(len(values)), values, color=color(0), height=0.68, zorder=3)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels([str(x) for x in labels])
    ax.invert_yaxis()  # first label on top, reads top-to-bottom
    ax.grid(axis="y", visible=False)
    return _finish(ax, title, xlabel, ylabel, save)


def line(x, y, *, labels=None, title=None, xlabel=None, ylabel=None, ax=None, save=None) -> Axes:
    """Line chart. ``y`` is one sequence, or a list of sequences for multiple
    series; pass ``labels`` to name them and a legend is drawn automatically."""
    ax = _axes(ax)
    first = y[0] if len(y) else None
    series = list(y) if hasattr(first, "__len__") else [y]
    for i, ys in enumerate(series):
        if len(ys) != len(x):
            raise ValueError("each y series must be the same length as x")
        ax.plot(x, ys, color=color(i), marker="o", markersize=4,
                label=labels[i] if labels and i < len(labels) else None)
    if labels and len(series) > 1:
        ax.legend()
    return _finish(ax, title, xlabel, ylabel, save)


def scatter(x, y, *, title=None, xlabel=None, ylabel=None, ax=None, save=None) -> Axes:
    """Scatter plot of paired ``x`` / ``y`` values."""
    if len(x) != len(y):
        raise ValueError("x and y must be the same length")
    ax = _axes(ax)
    ax.scatter(x, y, color=color(0), s=48, alpha=0.85, edgecolor=None, zorder=3)
    return _finish(ax, title, xlabel, ylabel, save)


def hist(values, *, bins=10, title=None, xlabel=None, ylabel="Count", ax=None, save=None) -> Axes:
    """Histogram of ``values`` into ``bins`` bins."""
    ax = _axes(ax)
    ax.hist(values, bins=bins, color=color(0), zorder=3)
    ax.grid(axis="x", visible=False)
    return _finish(ax, title, xlabel, ylabel, save)


def pie(labels, values, *, title=None, ax=None, save=None) -> Axes:
    """Pie chart. Best kept to a few slices; prefer :func:`bar` for precise
    magnitude comparison."""
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    ax = _axes(ax)
    ax.pie(values, labels=[str(x) for x in labels], colors=[color(i) for i in range(len(values))],
           autopct="%1.0f%%", wedgeprops={"edgecolor": _SURFACE, "linewidth": 2},
           textprops={"color": _INK})
    ax.set_aspect("equal")
    ax.grid(visible=False)
    return _finish(ax, title, None, None, save)
