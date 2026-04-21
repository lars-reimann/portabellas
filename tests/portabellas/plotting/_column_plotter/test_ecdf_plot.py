import pytest

from portabellas import Column
from portabellas.plotting import AxisConfig, PlotConfig
from portabellas.typing import DataType
from tests.helpers import assert_plot_has_title, assert_plot_has_traces


@pytest.mark.parametrize(
    ("column", "config", "expected_title"),
    [
        pytest.param(Column("a", [1, 2, 3]), None, "a", id="default title"),
        pytest.param(Column("a", [1, 2, 3]), PlotConfig(title="Custom"), "Custom", id="custom title"),
    ],
)
class TestEcdfPlot:
    def test_should_create_ecdf_plot(self, column: Column, config: PlotConfig | None, expected_title: str) -> None:
        plot = column.plot.ecdf_plot(config=config)
        assert_plot_has_traces(plot, expected_trace_count=1, expected_trace_types=["scatter"])
        assert isinstance(expected_title, str)

    def test_should_set_title(self, column: Column, config: PlotConfig | None, expected_title: str) -> None:
        plot = column.plot.ecdf_plot(config=config)
        assert_plot_has_title(plot, expected_title)


def test_should_use_lines_mode() -> None:
    column = Column("a", [1, 2, 3])
    plot = column.plot.ecdf_plot()
    assert plot._figure.data[0].mode == "lines"


def test_should_handle_empty_column() -> None:
    column: Column[int] = Column("a", [], type=DataType.Int64())
    plot = column.plot.ecdf_plot()
    assert_plot_has_traces(plot, expected_trace_count=1, expected_trace_types=["scatter"])


def test_should_set_log_axes() -> None:
    column = Column("a", [1, 10, 100, 1000])
    plot = column.plot.ecdf_plot(x_axis=AxisConfig(log=True), y_axis=AxisConfig(log=True))
    fig_dict = plot._figure.to_dict()
    assert fig_dict["layout"]["xaxis"]["type"] == "log"
    assert fig_dict["layout"]["yaxis"]["type"] == "log"
