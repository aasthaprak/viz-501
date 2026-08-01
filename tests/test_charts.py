"""Tests for simpleviz. Uses the non-interactive Agg backend so charts render
without a display."""

import os
import tempfile

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest
from matplotlib.axes import Axes

import simple_viz as sv


def teardown_function() -> None:
    plt.close("all")


def test_palette_is_fixed_and_unique() -> None:
    assert len(sv.PALETTE) == 8
    assert len(set(sv.PALETTE)) == 8  # no duplicates
    assert all(c.startswith("#") and len(c) == 7 for c in sv.PALETTE)


def test_color_wraps_around() -> None:
    assert sv.color(0) == sv.PALETTE[0]
    assert sv.color(8) == sv.PALETTE[0]
    assert sv.color(9) == sv.PALETTE[1]


def test_bar_returns_axes() -> None:
    ax = sv.bar(["A", "B", "C"], [1, 2, 3], title="t")
    assert isinstance(ax, Axes)
    assert ax.get_title(loc="left") == "t"  # theme sets titles left-aligned
    assert len(ax.patches) == 3


def test_barh_returns_axes() -> None:
    ax = sv.barh(["A", "B"], [4, 5])
    assert isinstance(ax, Axes)
    assert len(ax.patches) == 2


def test_line_single_series() -> None:
    ax = sv.line([0, 1, 2], [3, 4, 5])
    assert len(ax.lines) == 1


def test_line_multi_series_with_legend() -> None:
    ax = sv.line([0, 1, 2], [[1, 2, 3], [3, 2, 1]], labels=["a", "b"])
    assert len(ax.lines) == 2
    assert ax.get_legend() is not None


def test_scatter() -> None:
    ax = sv.scatter([1, 2, 3], [4, 5, 6])
    assert len(ax.collections) == 1


def test_hist() -> None:
    ax = sv.hist([1, 1, 2, 3, 3, 3, 4], bins=4)
    assert len(ax.patches) == 4


def test_pie() -> None:
    ax = sv.pie(["a", "b", "c"], [1, 2, 3])
    assert len(ax.patches) == 3


def test_mismatched_lengths_raise() -> None:
    with pytest.raises(ValueError):
        sv.bar(["A", "B"], [1])
    with pytest.raises(ValueError):
        sv.scatter([1, 2], [1])
    with pytest.raises(ValueError):
        sv.line([0, 1, 2], [1, 2])


def test_save_writes_file() -> None:
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "out.png")
        sv.bar(["A"], [1], save=path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0


def test_draws_into_existing_axes() -> None:
    fig, ax = plt.subplots()
    returned = sv.bar(["A", "B"], [1, 2], ax=ax)
    assert returned is ax
