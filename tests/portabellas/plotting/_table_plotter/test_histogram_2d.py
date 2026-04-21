import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError, OutOfBoundsError
from portabellas.plotting import AxisConfig, PlotConfig
from tests.helpers import assert_plot_has_no_title, assert_plot_has_title, assert_plot_has_traces


@pytest.mark.parametrize(
    ("table", "x_name", "y_name", "title"),
    [
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]}),
            "a",
            "b",
            None,
            id="default title",
        ),
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]}),
            "a",
            "b",
            "Custom",
            id="custom title",
        ),
    ],
)
class TestHistogram2d:
    def test_should_create_2d_histogram(self, table: Table, x_name: str, y_name: str, title: str | None) -> None:
        plot = table.plot.histogram_2d(x_name, y_name, config=PlotConfig(title=title))
        assert_plot_has_traces(plot, expected_trace_count=1)

    def test_should_set_title(self, table: Table, x_name: str, y_name: str, title: str | None) -> None:
        plot = table.plot.histogram_2d(x_name, y_name, config=PlotConfig(title=title))
        if title is None:
            assert_plot_has_no_title(plot)
        else:
            assert_plot_has_title(plot, title)


def test_should_raise_if_column_does_not_exist() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(ColumnNotFoundError):
        table.plot.histogram_2d("a", "c")


def test_should_raise_if_x_max_bin_count_is_less_than_1() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(OutOfBoundsError):
        table.plot.histogram_2d("a", "b", x_max_bin_count=0)


def test_should_raise_if_y_max_bin_count_is_less_than_1() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(OutOfBoundsError):
        table.plot.histogram_2d("a", "b", y_max_bin_count=0)


def test_should_set_log_axes() -> None:
    table = Table({"a": [1, 10, 100, 1000], "b": [2, 20, 200, 2000]})
    plot = table.plot.histogram_2d("a", "b", x_axis=AxisConfig(log=True), y_axis=AxisConfig(log=True))
    fig_dict = plot._figure.to_dict()
    assert fig_dict["layout"]["xaxis"]["type"] == "log"
    assert fig_dict["layout"]["yaxis"]["type"] == "log"
