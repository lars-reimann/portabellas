import pytest

from portabellas import Table
from portabellas.exceptions import ColumnNotFoundError, ColumnTypeError
from portabellas.plotting import PlotConfig
from tests.helpers import assert_plot_has_no_title, assert_plot_has_title, assert_plot_has_traces


@pytest.mark.parametrize(
    ("table", "x_name", "y_names", "show_confidence_interval", "title"),
    [
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]}),
            "a",
            ["b"],
            True,
            None,
            id="single y, with CI, default title",
        ),
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]}),
            "a",
            ["b"],
            False,
            None,
            id="single y, no CI",
        ),
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6], "c": [3, 4, 5, 6, 7]}),
            "a",
            ["b", "c"],
            True,
            None,
            id="multiple y, with CI",
        ),
        pytest.param(
            Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]}),
            "a",
            ["b"],
            True,
            "Custom",
            id="custom title",
        ),
    ],
)
class TestLinePlot:
    def test_should_create_line_plot(
        self,
        table: Table,
        x_name: str,
        y_names: list[str],
        show_confidence_interval: bool,
        title: str | None,
    ) -> None:
        plot = table.plot.line_plot(
            x_name, y_names, show_confidence_interval=show_confidence_interval, config=PlotConfig(title=title)
        )
        expected_count = len(y_names) * (2 if show_confidence_interval else 1)
        assert_plot_has_traces(plot, expected_trace_count=expected_count)

    def test_should_set_title(
        self,
        table: Table,
        x_name: str,
        y_names: list[str],
        show_confidence_interval: bool,
        title: str | None,
    ) -> None:
        plot = table.plot.line_plot(
            x_name, y_names, show_confidence_interval=show_confidence_interval, config=PlotConfig(title=title)
        )
        if title is None:
            assert_plot_has_no_title(plot)
        else:
            assert_plot_has_title(plot, title)


def test_should_raise_if_x_column_does_not_exist() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(ColumnNotFoundError):
        table.plot.line_plot("c", ["b"])


def test_should_raise_if_y_column_does_not_exist() -> None:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    with pytest.raises(ColumnNotFoundError):
        table.plot.line_plot("a", ["c"])


def test_should_raise_if_y_column_is_not_numeric() -> None:
    table = Table({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    with pytest.raises(ColumnTypeError):
        table.plot.line_plot("a", ["b"])
