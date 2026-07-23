"""Theme and color palette for simpleviz.

The categorical palette is a fixed, validated hue order (colorblind-aware, with
adjacent pairs kept perceptually distinct). Colors are assigned in order and
never cycled arbitrarily — the Nth series always gets slot N. Past eight series,
consider grouping the tail into an "Other" category rather than inventing hues.
"""

from __future__ import annotations

import matplotlib as mpl

#: Fixed categorical color order. Do not reorder casually — the sequence is
#: chosen so that adjacent slots stay distinguishable under common forms of
#: color vision deficiency.
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
    """Apply the simpleviz look to matplotlib's global rcParams.

    Called automatically when :mod:`simpleviz` is imported. Call it again to
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
