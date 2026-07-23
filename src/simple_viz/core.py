"""Core of simple_viz — theme, palette, and chart functions.

Everything the library does lives here:

* A validated, colorblind-aware categorical palette (:data:`PALETTE`) that is
  applied to matplotlib automatically via :func:`use_theme`.
* Chart functions (:func:`bar`, :func:`barh`, :func:`line`, :func:`scatter`,
  :func:`hist`, :func:`pie`) that share one contract — data first, optional
  ``title`` / ``xlabel`` / ``ylabel`` / ``ax`` / ``save`` keywords, and each
  returns the :class:`~matplotlib.axes.Axes` it drew on.
"""

from __future__ import annotations

from typing import Optional, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# ---------------------------------------------------------------------------
# Palette & theme
# ---------------------------------------------------------------------------

#: Fixed categorical color order. Do not reorder casually — the sequence is
#: chosen so that adjacent slots stay distinguishable under common forms of
#: color vision deficiency. Colors are assigned in order, never cycled
#: arbitrarily: the Nth series always gets slot N.
PALETTE = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

# Chrome / ink colors (light surface).
_INK_PRIMARY = "#0b0b0b"
_INK_SECONDARY = "#52514e"
_MUTED = "#898781"
_GRID = "#e1e0d9"
_SURFACE = "#fcfcfb"


def color(i: int) -> str:
    """Return the categorical color for slot ``i`` (0-based).

    Slots wrap around the palette if ``i`` exceeds its length, but relying on
    more than eight distinct series is discouraged — group the tail instead.
    """
    return PALETTE[i % len(PALETTE)]


def use_theme() -> None:
    """Apply the simple_viz look to matplotlib's global rcParams.

    Called automatically when :mod:`simple_viz` is imported. Call it again to
    restore the theme after another library has changed the rcParams.
    """
    mpl.rcParams.update(
        {
            # Color cycle drives the default series colors.
            "axes.prop_cycle": mpl.cycler(color=PALETTE),
            # Surface.
            "figure.facecolor": _SURFACE,
            "axes.facecolor": _SURFACE,
            "savefig.facecolor": _SURFACE,
            # Recessive chrome: drop the top/right spines, soften the rest.
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": _MUTED,
            "axes.linewidth": 0.8,
            # Light, behind-the-data gridlines.
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": _GRID,
            "grid.linewidth": 0.8,
            # Typography.
            "font.family": "sans-serif",
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.titleweight": "bold",
            "axes.titlecolor": _INK_PRIMARY,
            "axes.titlelocation": "left",
            "axes.titlepad": 12,
            "axes.labelcolor": _INK_SECONDARY,
            "axes.labelsize": 11,
            "text.color": _INK_PRIMARY,
            "xtick.color": _MUTED,
            "ytick.color": _MUTED,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            # Marks.
            "lines.linewidth": 2.0,
            "lines.markersize": 6,
            # Legend.
            "legend.frameon": False,
            "legend.fontsize": 10,
            # Output.
            "figure.figsize": (8, 5),
            "figure.dpi": 110,
            "savefig.dpi": 150,
            "savefig.bbox": "tight",
        }
    )


# ---------------------------------------------------------------------------
# Chart helpers
# ---------------------------------------------------------------------------


def _prepare(ax: Optional[Axes]) -> Axes:
    """Return the Axes to draw on, creating a figure if none was given."""
    if ax is None:
        _, ax = plt.subplots()
    return ax


def _finish(
    ax: Axes,
    title: Optional[str],
    xlabel: Optional[str],
    ylabel: Optional[str],
    save: Optional[str],
) -> Axes:
    """Apply shared labels and optionally save, then return the Axes."""
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if save:
        ax.figure.savefig(save)
    return ax


# ---------------------------------------------------------------------------
# Chart functions
# ---------------------------------------------------------------------------


def bar(
    labels: Sequence,
    values: Sequence[float],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    ax: Optional[Axes] = None,
    save: Optional[str] = None,
) -> Axes:
    """Vertical bar chart of ``values`` labeled by ``labels``."""
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    ax = _prepare(ax)
    ax.bar(range(len(values)), values, color=color(0), width=0.68, zorder=3)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels([str(x) for x in labels])
    ax.grid(axis="x", visible=False)
    return _finish(ax, title, xlabel, ylabel, save)


def barh(
    labels: Sequence,
    values: Sequence[float],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    ax: Optional[Axes] = None,
    save: Optional[str] = None,
) -> Axes:
    """Horizontal bar chart — good for long or many category labels."""
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    ax = _prepare(ax)
    ax.barh(range(len(values)), values, color=color(0), height=0.68, zorder=3)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels([str(x) for x in labels])
    ax.invert_yaxis()  # first label on top, reads top-to-bottom
    ax.grid(axis="y", visible=False)
    return _finish(ax, title, xlabel, ylabel, save)


def line(
    x: Sequence,
    y,
    *,
    labels: Optional[Sequence[str]] = None,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    ax: Optional[Axes] = None,
    save: Optional[str] = None,
) -> Axes:
    """Line chart.

    ``y`` may be a single sequence, or a sequence of sequences for multiple
    series. When there are multiple series, pass ``labels`` to name them and a
    legend is drawn automatically.
    """
    ax = _prepare(ax)

    # Normalize to a list of series.
    first = y[0] if len(y) else None
    is_multi = isinstance(first, (list, tuple)) or hasattr(first, "__len__")
    series = list(y) if is_multi else [y]

    for i, ys in enumerate(series):
        if len(ys) != len(x):
            raise ValueError("each y series must be the same length as x")
        label = labels[i] if labels and i < len(labels) else None
        ax.plot(x, ys, color=color(i), label=label, marker="o", markersize=4)

    if labels and len(series) > 1:
        ax.legend()
    return _finish(ax, title, xlabel, ylabel, save)


def scatter(
    x: Sequence[float],
    y: Sequence[float],
    *,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    ax: Optional[Axes] = None,
    save: Optional[str] = None,
) -> Axes:
    """Scatter plot of paired ``x`` / ``y`` values."""
    if len(x) != len(y):
        raise ValueError("x and y must be the same length")
    ax = _prepare(ax)
    ax.scatter(x, y, color=color(0), s=48, alpha=0.85, edgecolor=None, zorder=3)
    return _finish(ax, title, xlabel, ylabel, save)


def hist(
    values: Sequence[float],
    *,
    bins: int = 10,
    title: Optional[str] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = "Count",
    ax: Optional[Axes] = None,
    save: Optional[str] = None,
) -> Axes:
    """Histogram of ``values`` into ``bins`` bins."""
    ax = _prepare(ax)
    ax.hist(values, bins=bins, color=color(0), zorder=3)
    ax.grid(axis="x", visible=False)
    return _finish(ax, title, xlabel, ylabel, save)


def pie(
    labels: Sequence[str],
    values: Sequence[float],
    *,
    title: Optional[str] = None,
    ax: Optional[Axes] = None,
    save: Optional[str] = None,
) -> Axes:
    """Pie chart. Best kept to a handful of slices; prefer :func:`bar` when
    comparing precise magnitudes."""
    if len(labels) != len(values):
        raise ValueError("labels and values must be the same length")
    ax = _prepare(ax)
    colors = [color(i) for i in range(len(values))]
    ax.pie(
        values,
        labels=[str(x) for x in labels],
        colors=colors,
        autopct="%1.0f%%",
        wedgeprops={"edgecolor": _SURFACE, "linewidth": 2},
        textprops={"color": _INK_PRIMARY},
    )
    ax.set_aspect("equal")
    ax.grid(visible=False)
    return _finish(ax, title, None, None, save)
