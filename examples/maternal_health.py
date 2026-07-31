"""A worked women's-health visualization built with simple_viz's theme.

Story: maternal mortality has fallen sharply this century, but the burden is
still wildly unequal across regions. Two panels tell that in one figure.

Data: maternal mortality ratio (MMR) = maternal deaths per 100,000 live births.
Figures are the widely reported WHO / UN MMEIG estimates (rounded); see
"Trends in maternal mortality 2000 to 2020" (WHO, 2023). Values are approximate
and meant to illustrate the library, not to serve as a data source.

Run:  python examples/maternal_health.py
"""

import os

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

import simple_viz as sv  # importing applies the theme (palette + Poppins)

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

INK, MUTED, SURFACE = "#171310", "#9b968e", "#fbfaf7"

# --- Panel A: global MMR, 2000 -> 2020 -------------------------------------
years = [2000, 2005, 2010, 2015, 2020]
global_mmr = [339, 296, 248, 227, 223]

# --- Panel B: MMR by region, 2020 (sorted ascending for a clean bar stack) --
regions = {
    "Sub-Saharan Africa": 545,
    "Central & Southern Asia": 134,
    "Latin America & Caribbean": 88,
    "N. Africa & Western Asia": 84,
    "E. & S.E. Asia": 69,
    "Europe & N. America": 12,
    "Australia & New Zealand": 5,
}
order = sorted(regions, key=regions.get)  # ascending -> largest ends on top
vals = [regions[r] for r in order]


def main() -> None:
    fig, (axL, axR) = plt.subplots(
        1, 2, figsize=(14, 6.2), gridspec_kw={"width_ratios": [1, 1.15]}
    )

    # ---- Panel A: the decline -------------------------------------------
    blue = sv.color(0)
    axL.plot(years, global_mmr, color=blue, lw=2.6, marker="o", markersize=7,
             markerfacecolor=SURFACE, markeredgecolor=blue, markeredgewidth=2, zorder=3)
    # Endpoint value labels.
    for x, y, dy in [(years[0], global_mmr[0], 12), (years[-1], global_mmr[-1], 12)]:
        axL.annotate(f"{y}", (x, y), textcoords="offset points", xytext=(0, dy),
                     ha="center", fontsize=12, fontweight="bold", color=INK)
    # Headline % change.
    drop = round((global_mmr[0] - global_mmr[-1]) / global_mmr[0] * 100)
    axL.annotate(f"{drop}% lower than 2000", (2010.4, 300), fontsize=13,
                 fontweight="bold", color=blue)
    axL.set_title("Global maternal deaths per 100,000 births", fontsize=14,
                  fontweight="bold", loc="left", pad=14, color=INK)
    axL.set_ylim(0, 380)
    axL.set_xticks(years)
    axL.xaxis.set_major_locator(MultipleLocator(5))
    axL.grid(axis="x", visible=False)

    # ---- Panel B: the disparity -----------------------------------------
    ruby = sv.color(4)
    colors = [ruby if r == "Sub-Saharan Africa" else "#c9c3b8" for r in order]
    y = range(len(order))
    axR.barh(list(y), vals, color=colors, height=0.68, zorder=3)
    axR.set_yticks(list(y))
    axR.set_yticklabels(order, fontsize=11, color=INK)
    for i, v in enumerate(vals):
        axR.annotate(f"{v}", (v, i), textcoords="offset points", xytext=(6, 0),
                     va="center", fontsize=11, fontweight="bold",
                     color=ruby if order[i] == "Sub-Saharan Africa" else MUTED)
    axR.set_title("The gap in 2020 — Sub-Saharan Africa carries most of it",
                  fontsize=14, fontweight="bold", loc="left", pad=14, color=INK)
    axR.set_xlim(0, 600)
    axR.grid(axis="y", visible=False)

    fig.suptitle("Maternal mortality: real progress, deeply unequal",
                 fontsize=20, fontweight="bold", x=0.045, ha="left", color=INK)
    fig.text(0.045, 0.005,
             "Source: WHO / UN MMEIG, Trends in Maternal Mortality 2000–2020 "
             "(rounded, illustrative).  Built with simple_viz.",
             fontsize=9, color=MUTED, ha="left")
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])

    path = os.path.join(OUT, "maternal_health.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=SURFACE)
    print("Wrote", path)


if __name__ == "__main__":
    main()
