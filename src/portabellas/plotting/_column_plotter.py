from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas._validation import check_column_is_numeric
from portabellas.plotting._plot import Plot
from portabellas.plotting._plot_config import PlotConfig
from portabellas.plotting._plotting_utils import apply_axis_config, apply_config, compute_xbins

try:
    import plotly.graph_objects as go
except ImportError:
    msg = "Plotting requires the 'plot' extra. Install with: pip install portabellas[plot]"
    raise ImportError(msg) from None

if TYPE_CHECKING:
    from portabellas import Column
    from portabellas.plotting._axis_config import AxisConfig


class ColumnPlotter:
    """
    A class that contains plotting methods for a column.

    Parameters
    ----------
    column:
        The column to plot.

    Examples
    --------
    >>> from portabellas import Column
    >>> column = Column("test", [1, 2, 3])
    >>> plotter = column.plot
    """

    def __init__(self, column: Column) -> None:
        self._column: Column = column

    def box_plot(
        self,
        *,
        y_axis: AxisConfig | None = None,
        config: PlotConfig | None = None,
    ) -> Plot:
        """
        Create a box plot for the values in the column.

        Parameters
        ----------
        y_axis:
            The configuration of the y-axis. If None, sensible defaults are used.
        config:
            The configuration of the plot. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The box plot.

        Raises
        ------
        ColumnTypeError
            If the column is not numeric.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("test", [1, 2, 3])
        >>> plot = column.plot.box_plot()
        """
        check_column_is_numeric(self._column, operation="create a box plot")

        effective_config = PlotConfig(title=self._column.name) if config is None else config

        fig = go.Figure()
        fig.add_trace(
            go.Box(
                y=self._column._series.drop_nulls().to_list(),
                name=self._column.name,
            ),
        )
        fig.update_layout(yaxis_title=self._column.name)

        apply_config(fig, effective_config)
        apply_axis_config(fig, None, y_axis)

        return Plot(fig)

    def histogram(
        self,
        *,
        max_bin_count: int = 10,
        x_axis: AxisConfig | None = None,
        config: PlotConfig | None = None,
    ) -> Plot:
        """
        Create a histogram for the values in the column.

        Parameters
        ----------
        max_bin_count:
            The maximum number of bins to use in the histogram.
        x_axis:
            The configuration of the x-axis. If None, sensible defaults are used.
        config:
            The configuration of the plot. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The histogram.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("test", [1, 2, 3])
        >>> plot = column.plot.histogram()
        """
        effective_config = PlotConfig(title=self._column.name) if config is None else config

        data = self._column._series.drop_nulls()
        xbins = compute_xbins(data, max_bin_count)
        fig = go.Figure()
        trace_kwargs: dict = {"x": data.to_list(), "name": self._column.name}
        if xbins is not None:
            trace_kwargs["xbins"] = xbins
        fig.add_trace(go.Histogram(**trace_kwargs))
        fig.update_layout(bargap=0.1, xaxis_title=self._column.name)

        apply_config(fig, effective_config)
        apply_axis_config(fig, x_axis, None)

        return Plot(fig)

    def violin_plot(
        self,
        *,
        y_axis: AxisConfig | None = None,
        config: PlotConfig | None = None,
    ) -> Plot:
        """
        Create a violin plot for the values in the column.

        Parameters
        ----------
        y_axis:
            The configuration of the y-axis. If None, sensible defaults are used.
        config:
            The configuration of the plot. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The violin plot.

        Raises
        ------
        ColumnTypeError
            If the column is not numeric.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("test", [1, 2, 3])
        >>> plot = column.plot.violin_plot()
        """
        check_column_is_numeric(self._column, operation="create a violin plot")

        effective_config = PlotConfig(title=self._column.name) if config is None else config

        fig = go.Figure()
        fig.add_trace(
            go.Violin(
                y=self._column._series.drop_nulls().to_list(),
                name=self._column.name,
                box_visible=True,
                meanline_visible=True,
            ),
        )
        fig.update_layout(yaxis_title=self._column.name)

        apply_config(fig, effective_config)
        apply_axis_config(fig, None, y_axis)

        return Plot(fig)

    def ecdf_plot(
        self,
        *,
        x_axis: AxisConfig | None = None,
        y_axis: AxisConfig | None = None,
        config: PlotConfig | None = None,
    ) -> Plot:
        """
        Create an empirical cumulative distribution function plot.

        Parameters
        ----------
        x_axis:
            The configuration of the x-axis. If None, sensible defaults are used.
        y_axis:
            The configuration of the y-axis. If None, sensible defaults are used.
        config:
            The configuration of the plot. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The ECDF plot.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("test", [1, 2, 3])
        >>> plot = column.plot.ecdf_plot()
        """
        effective_config = PlotConfig(title=self._column.name) if config is None else config

        data = self._column._series.drop_nulls().sort()
        n = len(data)
        x = data.to_list()
        y = [(i + 1) / n for i in range(n)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=self._column.name))
        fig.update_layout(xaxis_title=self._column.name, yaxis_title="Cumulative Probability")

        apply_config(fig, effective_config)
        apply_axis_config(fig, x_axis, y_axis)

        return Plot(fig)
