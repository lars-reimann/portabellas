from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.plotting._plotting_utils import get_theme

try:
    import plotly.graph_objects as go  # noqa: TC002
except ImportError:
    msg = "Plotting requires the 'plot' extra. Install with: pip install portabellas[plot]"
    raise ImportError(msg) from None

if TYPE_CHECKING:
    from portabellas.plotting._plot_writer import PlotWriter


class Plot:
    """
    An interactive plot backed by a Plotly figure.

    This class cannot be instantiated directly. Access it via the plot methods on `Table.plot` or `Column.plot`.

    Examples
    --------
    >>> from portabellas import Table
    >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    >>> plot = table.plot.scatter_plot("a", ["b"])
    """

    def __init__(self, figure: go.Figure) -> None:
        self._figure = figure

    def _repr_html_(self) -> str:
        theme = get_theme(self._figure)

        if theme == "auto":
            html = self._figure.to_html(include_plotlyjs="cdn", full_html=False)
            script = (
                "<script>"
                "(function(){"
                "var scripts=document.querySelectorAll('script');"
                "var s=scripts[scripts.length-1];"
                "var div=s.previousElementSibling;"
                "if(!div)return;"
                "var isDark=window.matchMedia&&window.matchMedia('(prefers-color-scheme:dark)').matches;"
                "if(!isDark){"
                "var el=document.documentElement;"
                "isDark=el.classList.contains('dark')||el.classList.contains('vscode-dark')||el.dataset.theme==='dark';"
                "}"
                "if(isDark){Plotly.relayout(div,{'template':'plotly_dark'});}"
                "})();"
                "</script>"
            )
            return html + script

        return self._figure.to_html(include_plotlyjs="cdn", full_html=False)

    @property
    def write(self) -> PlotWriter:
        """
        Write this plot to various file formats.

        Examples
        --------
        >>> from portabellas import Table
        >>> import tempfile
        >>> from pathlib import Path
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> plot = table.plot.scatter_plot("a", ["b"])
        >>> with tempfile.TemporaryDirectory() as tmp:
        ...     plot.write.html_file(Path(tmp) / "plot.html")
        """
        from portabellas.plotting._plot_writer import PlotWriter  # circular import  # noqa: PLC0415

        return PlotWriter(self)

    def show(self) -> None:
        """Open the plot in a web browser."""
        self._figure.show()
