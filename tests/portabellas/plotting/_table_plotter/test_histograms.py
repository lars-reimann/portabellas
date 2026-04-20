import pytest

from portabellas import Table
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
class TestHistograms:
    def test_should_create_histograms(self, table: Table, title: str | None) -> None:
        plot = table.plot.histograms(config=PlotConfig(title=title))
        assert_plot_has_traces(plot, expected_trace_count=table.column_count)
        for i in range(table.column_count):
            assert plot._figure.data[i].type == "histogram"

    def test_should_set_title(self, table: Table, title: str | None) -> None:
        plot = table.plot.histograms(config=PlotConfig(title=title))
        if title is None:
            assert_plot_has_no_title(plot)
        else:
            assert_plot_has_title(plot, title)


def test_should_work_with_string_columns() -> None:
    table = Table({"a": ["x", "y", "z", "x"], "b": [1, 2, 3, 4]})
    plot = table.plot.histograms()
    assert_plot_has_traces(plot, expected_trace_count=2)
