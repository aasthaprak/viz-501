"""Gallery demo: renders one PNG per chart type into examples/output/.

Run from the repo root:

    python examples/demo.py
"""

import math
import os

import matplotlib.pyplot as plt

import simpleviz as sv

OUT = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUT, exist_ok=True)


def main() -> None:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

    sv.bar(
        ["Alpha", "Beta", "Gamma", "Delta"],
        [23, 45, 31, 52],
        title="Bar chart",
        ylabel="Revenue ($k)",
        save=os.path.join(OUT, "bar.png"),
    )

    sv.barh(
        ["North region", "South region", "East region", "West region"],
        [120, 95, 140, 80],
        title="Horizontal bar chart",
        xlabel="Units sold",
        save=os.path.join(OUT, "barh.png"),
    )

    sv.line(
        months,
        [
            [10, 14, 13, 18, 24, 27],
            [8, 9, 12, 11, 15, 19],
        ],
        labels=["Product A", "Product B"],
        title="Line chart",
        ylabel="Sales",
        save=os.path.join(OUT, "line.png"),
    )

    xs = [i / 4 for i in range(40)]
    ys = [math.sin(x) + (x % 1.3) * 0.3 for x in xs]
    sv.scatter(
        xs,
        ys,
        title="Scatter plot",
        xlabel="x",
        ylabel="y",
        save=os.path.join(OUT, "scatter.png"),
    )

    data = [((i * 37) % 100) / 10 for i in range(200)]
    sv.hist(
        data,
        bins=12,
        title="Histogram",
        xlabel="Value",
        save=os.path.join(OUT, "hist.png"),
    )

    sv.pie(
        ["Direct", "Referral", "Organic", "Social"],
        [40, 25, 20, 15],
        title="Pie chart",
        save=os.path.join(OUT, "pie.png"),
    )

    # Charts compose into subplots via the `ax` argument.
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    sv.bar(["Q1", "Q2", "Q3", "Q4"], [12, 19, 15, 22], title="Quarterly", ax=axes[0])
    sv.line(months, [3, 5, 4, 8, 7, 11], title="Trend", ax=axes[1])
    fig.savefig(os.path.join(OUT, "subplots.png"), bbox_inches="tight")

    print(f"Wrote charts to {OUT}")


if __name__ == "__main__":
    main()
