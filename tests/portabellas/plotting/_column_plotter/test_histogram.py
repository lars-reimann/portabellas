import pytest

from portabellas import Column
from portabellas.plotting import AxisConfig, PlotConfig
from portabellas.typing import DataType
from tests.helpers import assert_plot_has_title, assert_plot_has_traces


@pytest.mark.parametrize(
    ("column", "config", "expected_title"),
    [
        pytest.param(Column("a", [1, 2, 3, 4, 5]), None, "a", id="default title"),
        pytest.param(Column("a", [1, 2, 3, 4, 5]), PlotConfig(title="Custom"), "Custom", id="custom title"),
    ],
)
class TestHistogram:
    def test_should_create_histogram(self, column: Column, config: PlotConfig | None, expected_title: str) -> None:
        plot = column.plot.histogram(config=config)
        assert_plot_has_traces(plot, expected_trace_count=1, expected_trace_types=["histogram"])
        assert isinstance(expected_title, str)

    def test_should_set_title(self, column: Column, config: PlotConfig | None, expected_title: str) -> None:
        plot = column.plot.histogram(config=config)
        assert_plot_has_title(plot, expected_title)


def test_should_work_with_string_column() -> None:
    column = Column("a", ["x", "y", "z", "x", "y"])
    plot = column.plot.histogram()
    assert_plot_has_traces(plot, expected_trace_count=1, expected_trace_types=["histogram"])


def test_should_handle_empty_column() -> None:
    column: Column[int] = Column("a", [], type=DataType.Int64())
    plot = column.plot.histogram()
    assert_plot_has_traces(plot, expected_trace_count=1, expected_trace_types=["histogram"])


def test_should_set_x_axis_to_log() -> None:
    column = Column("a", [1, 10, 100, 1000])
    plot = column.plot.histogram(x_axis=AxisConfig(log=True))
    fig_dict = plot._figure.to_dict()
    assert fig_dict["layout"]["xaxis"]["type"] == "log"
