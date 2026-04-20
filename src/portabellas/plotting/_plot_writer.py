from __future__ import annotations

import importlib.util
from typing import TYPE_CHECKING

from portabellas._validation import normalize_and_check_file_path

if TYPE_CHECKING:
    from pathlib import Path

    from portabellas.plotting._plot import Plot


class PlotWriter:
    """
    Write a plot to various file formats.

    This class cannot be instantiated directly. Access it via `plot.write` instead.

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

    def __init__(self, plot: Plot) -> None:
        self._plot = plot

    def html_file(self, path: str | Path) -> None:
        """
        Write the plot to a standalone HTML file.

        If the file and/or the parent directories do not exist, they will be created. If the file exists already, it
        will be overwritten.

        Parameters
        ----------
        path:
            The path to the HTML file. If the file extension is omitted, it is assumed to be ".html".

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".html".

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
        path = normalize_and_check_file_path(path, ".html", [".html"])
        path.parent.mkdir(parents=True, exist_ok=True)

        self._plot._figure.write_html(path, include_plotlyjs="cdn", full_html=True)

    def png_file(self, path: str | Path) -> None:
        """
        Write the plot to a PNG file.

        If the file and/or the parent directories do not exist, they will be created. If the file exists already, it
        will be overwritten.

        **Note:** This requires the `plot` extra to be installed (`pip install portabellas[plot]`).

        Parameters
        ----------
        path:
            The path to the PNG file. If the file extension is omitted, it is assumed to be ".png".

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".png".
        ImportError
            If the `plot` extra (kaleido) is not installed.

        Examples
        --------
        >>> from portabellas import Table
        >>> import tempfile
        >>> from pathlib import Path
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> plot = table.plot.scatter_plot("a", ["b"])
        >>> with tempfile.TemporaryDirectory() as tmp:
        ...     plot.write.png_file(Path(tmp) / "plot.png")  # doctest: +SKIP
        """
        _check_kaleido_installed()

        path = normalize_and_check_file_path(path, ".png", [".png"])
        path.parent.mkdir(parents=True, exist_ok=True)

        self._plot._figure.write_image(path, format="png")

    def svg_file(self, path: str | Path) -> None:
        """
        Write the plot to an SVG file.

        If the file and/or the parent directories do not exist, they will be created. If the file exists already, it
        will be overwritten.

        **Note:** This requires the `plot` extra to be installed (`pip install portabellas[plot]`).

        Parameters
        ----------
        path:
            The path to the SVG file. If the file extension is omitted, it is assumed to be ".svg".

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".svg".
        ImportError
            If the `plot` extra (kaleido) is not installed.
        """
        _check_kaleido_installed()

        path = normalize_and_check_file_path(path, ".svg", [".svg"])
        path.parent.mkdir(parents=True, exist_ok=True)

        self._plot._figure.write_image(path, format="svg")

    def pdf_file(self, path: str | Path) -> None:
        """
        Write the plot to a PDF file.

        If the file and/or the parent directories do not exist, they will be created. If the file exists already, it
        will be overwritten.

        **Note:** This requires the `plot` extra to be installed (`pip install portabellas[plot]`).

        Parameters
        ----------
        path:
            The path to the PDF file. If the file extension is omitted, it is assumed to be ".pdf".

        Raises
        ------
        FileExtensionError
            If the path has an extension that is not ".pdf".
        ImportError
            If the `plot` extra (kaleido) is not installed.
        """
        _check_kaleido_installed()

        path = normalize_and_check_file_path(path, ".pdf", [".pdf"])
        path.parent.mkdir(parents=True, exist_ok=True)

        self._plot._figure.write_image(path, format="pdf")


def _check_kaleido_installed() -> None:
    if importlib.util.find_spec("kaleido") is None:
        msg = "Static image export requires the 'plot' extra. Install it with: pip install portabellas[plot]"
        raise ImportError(msg) from None
