import pytest

from portabellas import Table
from portabellas.plotting import PlotConfig
from tests.helpers import assert_plot_has_no_title, assert_plot_has_title, assert_plot_has_traces


@pytest.mark.parametrize(
    ("table", "title"),
    [
        pytest.param(
            Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            None,
            id="default title",
        ),
        pytest.param(
            Table({"a": [1, 2, 3], "b": [4, 5, 6]}),
            "Custom",
            id="custom title",
        ),
    ],
)
class TestCorrelationHeatmap:
    def test_should_create_correlation_heatmap(self, table: Table, title: str | None) -> None:
        plot = table.plot.correlation_heatmap(config=PlotConfig(title=title))
        assert_plot_has_traces(plot, expected_trace_count=1)

    def test_should_set_title(self, table: Table, title: str | None) -> None:
        plot = table.plot.correlation_heatmap(config=PlotConfig(title=title))
        if title is None:
            assert_plot_has_no_title(plot)
        else:
            assert_plot_has_title(plot, title)


def test_should_handle_only_non_numeric_columns() -> None:
    table = Table({"a": ["x", "y", "z"]})
    plot = table.plot.correlation_heatmap()
    assert_plot_has_traces(plot, expected_trace_count=0)
