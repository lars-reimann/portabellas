import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError, ColumnTypeError
from portabellas.plotting import PlotConfig
from tests.helpers import assert_plot_has_no_title, assert_plot_has_title, assert_plot_has_traces


@pytest.mark.parametrize(
    ("table", "x_name", "y_names", "title"),
    [
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]}),
            "a",
            ["b"],
            None,
            id="single y, default title",
        ),
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6], "c": [3, 4, 5, 6, 7]}),
            "a",
            ["b", "c"],
            None,
            id="multiple y, default title",
        ),
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]}),
            "a",
            ["b"],
            "Custom",
            id="custom title",
        ),
    ],
)
class TestScatterPlot:
    def test_should_create_scatter_plot(self, table: Table, x_name: str, y_names: list[str], title: str | None) -> None:
        plot = table.plot.scatter_plot(x_name, y_names, config=PlotConfig(title=title))
        assert_plot_has_traces(plot, expected_trace_count=len(y_names), expected_trace_types=["scatter"] * len(y_names))

    def test_should_set_title(self, table: Table, x_name: str, y_names: list[str], title: str | None) -> None:
        plot = table.plot.scatter_plot(x_name, y_names, config=PlotConfig(title=title))
        if title is None:
            assert_plot_has_no_title(plot)
        else:
            assert_plot_has_title(plot, title)


def test_should_raise_if_x_column_does_not_exist() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(ColumnNotFoundError):
        table.plot.scatter_plot("c", ["b"])


def test_should_raise_if_y_column_does_not_exist() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(ColumnNotFoundError):
        table.plot.scatter_plot("a", ["c"])


def test_should_raise_if_y_column_is_not_numeric() -> None:
    table = Table({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    with pytest.raises(ColumnTypeError):
        table.plot.scatter_plot("a", ["b"])
