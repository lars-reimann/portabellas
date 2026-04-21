import pytest

from portabellas import Table
from portabellas.exceptions import ColumnTypeError
from portabellas.plotting import PlotConfig
from tests.helpers import assert_plot_has_no_title, assert_plot_has_title, assert_plot_has_traces


@pytest.mark.parametrize(
    ("table", "title"),
    [
        pytest.param(Table({"a": [1, 2, 3], "b": [4, 5, 6]}), None, id="default title"),
        pytest.param(Table({"a": [1, 2, 3], "b": [4, 5, 6]}), "Custom", id="custom title"),
    ],
)
class TestScatterMatrix:
    def test_should_create_scatter_matrix(self, table: Table, title: str | None) -> None:
        plot = table.plot.scatter_matrix(config=PlotConfig(title=title))
        assert_plot_has_traces(plot, expected_trace_count=1)
        assert plot._figure.data[0].type == "splom"

    def test_should_set_title(self, table: Table, title: str | None) -> None:
        plot = table.plot.scatter_matrix(config=PlotConfig(title=title))
        if title is None:
            assert_plot_has_no_title(plot)
        else:
            assert_plot_has_title(plot, title)


def test_should_raise_if_all_columns_are_non_numeric() -> None:
    table = Table({"a": ["x", "y", "z"]})
    with pytest.raises(ColumnTypeError):
        table.plot.scatter_matrix()


def test_should_work_with_single_numeric_column() -> None:
    table = Table({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    plot = table.plot.scatter_matrix()
    assert_plot_has_traces(plot, expected_trace_count=1)
    assert plot._figure.data[0].type == "splom"
