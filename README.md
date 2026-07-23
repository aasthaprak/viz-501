# simple_viz

A small, opinionated visualization library built on [matplotlib](https://matplotlib.org/).

The idea: get a good-looking, readable chart in one line, without touching
matplotlib's rcParams or fiddling with colors, spines, and gridlines. simple_viz
ships a validated, colorblind-aware palette and recessive chrome by default, and
gets out of your way when you need to customize.

## Install

```bash
pip install -e .        # from a clone of this repo
```

Requires Python 3.8+ and matplotlib 3.5+.

## Quick start

```python
import simple_viz as sv

sv.bar(["A", "B", "C"], [3, 7, 5], title="Scores", save="scores.png")
```

That's it — the theme is applied automatically on import.

## Chart types

| Function | What it draws |
|----------|---------------|
| `bar(labels, values)`      | Vertical bar chart |
| `barh(labels, values)`     | Horizontal bar chart (good for long labels) |
| `line(x, y, labels=...)`   | Line chart, single or multiple series |
| `scatter(x, y)`            | Scatter plot |
| `hist(values, bins=...)`   | Histogram |
| `pie(labels, values)`      | Pie chart |

### Shared conventions

Every chart function accepts the same optional keywords:

- `title`, `xlabel`, `ylabel` — labels.
- `ax` — draw into an existing matplotlib `Axes` (for subplots). If omitted, a
  new figure is created.
- `save` — a path to write the figure to (e.g. `"chart.png"`).

Each function **returns the `Axes`** it drew on, so you can keep customizing with
plain matplotlib afterwards:

```python
ax = sv.bar(["A", "B"], [1, 2])
ax.set_ylim(0, 5)
ax.figure.savefig("out.png")
```

### Multiple line series

Pass a list of series as `y` and name them with `labels`; a legend appears
automatically:

```python
sv.line(
    ["Jan", "Feb", "Mar"],
    [[10, 14, 13], [8, 9, 12]],
    labels=["Product A", "Product B"],
    ylabel="Sales",
)
```

### Composing into subplots

```python
import matplotlib.pyplot as plt
import simple_viz as sv

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
sv.bar(["Q1", "Q2", "Q3", "Q4"], [12, 19, 15, 22], title="Quarterly", ax=axes[0])
sv.line(["Jan", "Feb", "Mar"], [3, 5, 4], title="Trend", ax=axes[1])
```

## The palette

`simple_viz.PALETTE` is a fixed list of eight hues, ordered so that adjacent
colors stay distinguishable under common forms of color vision deficiency.
Colors are assigned in order (series 0 → slot 0, series 1 → slot 1, …) and never
cycled arbitrarily. Use `simple_viz.color(i)` to pull slot `i` yourself.

If you have more than eight series, group the smallest into an "Other" category
rather than relying on hue to distinguish nine-plus lines.

## Theme

The theme is applied on import via `simple_viz.use_theme()`. If another library
overrides matplotlib's rcParams, call `use_theme()` again to restore it.

## Examples & tests

```bash
python examples/demo.py    # renders one PNG per chart type into examples/output/
python -m pytest           # run the test suite
```

## License

MIT
