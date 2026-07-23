"""Chart functions for simpleviz.

Each function follows the same contract:

* The data comes first, positionally.
* ``title``, ``xlabel``, ``ylabel`` are optional keyword labels.
* ``ax`` lets you draw into an existing Axes (for subplots); if omitted a new
  figure and Axes are created.
* ``save`` writes the figure to the given path.
* The function returns the Axes it drew on, so you can keep customizing.
"""

from __future__ import annotations

from typing import Optional, Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from .theme import color


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
        wedgeprops={"edgecolor": "#fcfcfb", "linewidth": 2},
        textprops={"color": "#0b0b0b"},
    )
    ax.set_aspect("equal")
    ax.grid(visible=False)
    return _finish(ax, title, None, None, save)
