from pathlib import Path
from typing import Literal
from unittest.mock import patch

import pytest

from portabellas import Table
from portabellas.plotting import Plot, PlotConfig


@pytest.fixture
def plot() -> Plot:
    table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    return table.plot.scatter_plot("a", ["b"])


class TestReprHtml:
    def test_should_return_html_string(self, plot: Plot) -> None:
        html = plot._repr_html_()
        assert isinstance(html, str)
        assert "plotly" in html

    @pytest.mark.parametrize(
        "theme",
        [
            pytest.param("light", id="light theme"),
            pytest.param("dark", id="dark theme"),
        ],
    )
    def test_should_return_html_without_dark_mode_script_for_non_auto_theme(
        self, theme: Literal["auto", "dark", "light"]
    ) -> None:
        table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        plot = table.plot.scatter_plot("a", ["b"], config=PlotConfig(theme=theme))
        html = plot._repr_html_()
        assert isinstance(html, str)
        assert "matchMedia" not in html


class TestWriteHtmlFile:
    def test_should_write_html_file(self, plot: Plot, tmp_path: Path) -> None:
        plot.write.html_file(tmp_path / "test.html")
        assert (tmp_path / "test.html").exists()
        content = (tmp_path / "test.html").read_text()
        assert "plotly" in content

    def test_should_create_parent_directories(self, plot: Plot, tmp_path: Path) -> None:
        plot.write.html_file(tmp_path / "subdir" / "test.html")
        assert (tmp_path / "subdir" / "test.html").exists()


class TestWritePngFile:
    def test_should_raise_import_error_if_kaleido_not_installed(self, plot: Plot, tmp_path: Path) -> None:
        with patch.dict("sys.modules", {"kaleido": None}), pytest.raises(ImportError, match="plot"):
            plot.write.png_file(tmp_path / "test.png")


class TestFigureProperty:
    def test_should_return_plotly_figure(self, plot: Plot) -> None:
        figure = plot._figure
        assert hasattr(figure, "to_dict")
        assert hasattr(figure, "update_layout")


class TestPlotConfigSize:
    @pytest.mark.parametrize(
        ("width", "height"),
        [
            pytest.param(800, None, id="width only"),
            pytest.param(None, 600, id="height only"),
            pytest.param(800, 600, id="width and height"),
        ],
    )
    def test_should_set_size(self, width: int | None, height: int | None) -> None:
        table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        plot = table.plot.scatter_plot("a", ["b"], config=PlotConfig(width=width, height=height))
        layout = plot._figure.to_dict()["layout"]
        if width is not None:
            assert layout["width"] == width
        if height is not None:
            assert layout["height"] == height
