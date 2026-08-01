"""A sports visualization built with simple_viz's theme: a dumbbell chart.

Story: average match attendance in women's professional football/basketball
leagues has jumped in just five years. A dumbbell (before/after) chart shows
each league's 2019 and 2024 figures and the distance travelled between them.

Data: approximate average per-match attendance (thousands), rounded from
publicly reported league figures. Illustrative — meant to exercise the
library, not to serve as a data source.

Run:  python examples/womens_sports.py
"""

import os

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import simple_viz as sv  # importing applies the theme (palette + Poppins)

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)

INK, MUTED, SURFACE = "#171310", "#9b968e", "#fbfaf7"

# league -> (2019, 2024) average attendance, in thousands
leagues = {
    "NWSL (USA)": (7.4, 11.2),
    "WNBA (USA)": (6.5, 9.8),
    "WSL (England)": (3.9, 7.0),
    "Liga F (Spain)": (1.4, 5.6),
    "Frauen-Bundesliga (Ger.)": (2.6, 4.2),
}
order = sorted(leagues, key=lambda k: leagues[k][1])  # largest ends on top

PAST = MUTED
NOW = sv.color(1)   # emerald green — "growth"
LINK = "#d7d2c7"


def main() -> None:
    fig, ax = plt.subplots(figsize=(11, 6.2))

    for i, name in enumerate(order):
        a, b = leagues[name]
        ax.plot([a, b], [i, i], color=LINK, lw=3.2, zorder=1, solid_capstyle="round")
        ax.scatter(a, i, s=150, color=PAST, zorder=3)
        ax.scatter(b, i, s=170, color=NOW, zorder=3)
        # Value labels: 2019 to the left, 2024 to the right.
        ax.annotate(f"{a:.1f}k", (a, i), xytext=(-10, 0), textcoords="offset points",
                    va="center", ha="right", fontsize=10.5, color=MUTED)
        ax.annotate(f"{b:.1f}k", (b, i), xytext=(11, 0), textcoords="offset points",
                    va="center", ha="left", fontsize=11, fontweight="bold", color=NOW)
        # Growth badge.
        growth = round((b - a) / a * 100)
        ax.annotate(f"+{growth}%", (13.0, i), va="center", ha="left",
                    fontsize=11, fontweight="bold", color=INK)

    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(order, fontsize=12, color=INK)
    ax.set_xlim(0, 15.2)
    ax.set_ylim(-0.6, len(order) - 0.4)
    ax.set_xlabel("Average attendance per match (thousands)", fontsize=11, color="#5a544e")
    ax.grid(axis="y", visible=False)
    ax.margins(y=0.08)

    # Column header for the growth badges.
    ax.annotate("5-yr\ngrowth", (13.0, len(order) - 0.35), va="bottom", ha="left",
                fontsize=9.5, fontweight="bold", color=MUTED)

    # Manual legend for the two endpoints.
    handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=PAST,
               markersize=11, label="2019"),
        Line2D([0], [0], marker="o", color="none", markerfacecolor=NOW,
               markersize=12, label="2024"),
    ]
    ax.legend(handles=handles, loc="lower right", ncol=2, fontsize=11,
              handletextpad=0.2, columnspacing=1.2, bbox_to_anchor=(1.0, -0.02))

    fig.suptitle("Women's leagues are filling more seats",
                 fontsize=20, fontweight="bold", x=0.045, ha="left", color=INK)
    fig.text(0.045, 0.9, "Average match attendance, 2019 vs 2024",
             fontsize=13, color="#5a544e", ha="left")
    fig.text(0.045, 0.005,
             "Source: publicly reported league attendance (rounded, illustrative).  "
             "Built with simple_viz.",
             fontsize=9, color=MUTED, ha="left")
    fig.tight_layout(rect=[0, 0.03, 1, 0.88])

    path = os.path.join(OUT, "womens_sports.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=SURFACE)
    print("Wrote", path)


if __name__ == "__main__":
    main()
