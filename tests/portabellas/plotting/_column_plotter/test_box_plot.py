import pytest

from portabellas import Column
from portabellas.exceptions import ColumnTypeError
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
class TestBoxPlot:
    def test_should_create_box_plot(self, column: Column, config: PlotConfig | None, expected_title: str) -> None:
        plot = column.plot.box_plot(config=config)
        assert_plot_has_traces(plot, expected_trace_count=1, expected_trace_types=["box"])
        assert isinstance(expected_title, str)

    def test_should_set_title(self, column: Column, config: PlotConfig | None, expected_title: str) -> None:
        plot = column.plot.box_plot(config=config)
        assert_plot_has_title(plot, expected_title)


def test_should_raise_if_column_is_not_numeric() -> None:
    column = Column("a", ["x", "y", "z"])
    with pytest.raises(ColumnTypeError):
        column.plot.box_plot()


def test_should_handle_empty_column() -> None:
    column: Column[int] = Column("a", [], type=DataType.Int64())
    plot = column.plot.box_plot()
    assert_plot_has_traces(plot, expected_trace_count=1, expected_trace_types=["box"])


def test_should_set_y_axis_to_log() -> None:
    column = Column("a", [1, 10, 100, 1000])
    plot = column.plot.box_plot(y_axis=AxisConfig(log=True))
    fig_dict = plot._figure.to_dict()
    assert fig_dict["layout"]["yaxis"]["type"] == "log"
