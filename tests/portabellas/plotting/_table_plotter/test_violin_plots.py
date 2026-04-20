import pytest

from portabellas import Table
from portabellas.exceptions import ColumnTypeError
from portabellas.plotting import PlotConfig
from tests.helpers import assert_plot_has_no_title, assert_plot_has_title, assert_plot_has_traces


@pytest.mark.parametrize(
    ("table", "title"),
    [
        pytest.param(Table({"a": [1, 2, 3]}), None, id="single column, default title"),
        pytest.param(Table({"a": [1, 2, 3], "b": [4, 5, 6]}), None, id="two columns, default title"),
        pytest.param(Table({"a": [1, 2, 3]}), "Custom", id="custom title"),
    ],
)
class TestViolinPlots:
    def test_should_create_violin_plots(self, table: Table, title: str | None) -> None:
        plot = table.plot.violin_plots(config=PlotConfig(title=title))
        expected_count = table.remove_non_numeric_columns().column_count
        assert_plot_has_traces(plot, expected_trace_count=expected_count)
        for i in range(expected_count):
            assert plot._figure.data[i].type == "violin"

    def test_should_set_title(self, table: Table, title: str | None) -> None:
        plot = table.plot.violin_plots(config=PlotConfig(title=title))
        if title is None:
            assert_plot_has_no_title(plot)
        else:
            assert_plot_has_title(plot, title)


def test_should_raise_if_all_columns_are_non_numeric() -> None:
    table = Table({"a": ["x", "y", "z"]})
    with pytest.raises(ColumnTypeError):
        table.plot.violin_plots()


def test_should_ignore_non_numeric_columns() -> None:
    table = Table({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    plot = table.plot.violin_plots()
    assert_plot_has_traces(plot, expected_trace_count=1, expected_trace_types=["violin"])
