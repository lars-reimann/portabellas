from __future__ import annotations

from math import ceil
from typing import TYPE_CHECKING

import polars as pl

from portabellas._utils import safely_collect_lazy_frame
from portabellas._validation import check_bounds, check_columns_are_numeric, check_columns_exist
from portabellas.exceptions import ColumnTypeError
from portabellas.plotting._plot import Plot
from portabellas.plotting._plot_config import PlotConfig
from portabellas.plotting._plotting_utils import apply_axis_config, apply_config, compute_xbins

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    msg = "Plotting requires the 'plot' extra. Install with: pip install portabellas[plot]"
    raise ImportError(msg) from None

if TYPE_CHECKING:
    from portabellas import Table
    from portabellas.plotting._axis_config import AxisConfig


class TablePlotter:
    """
    A class that contains plotting methods for a table.

    Parameters
    ----------
    table:
        The table to plot.

    Examples
    --------
    >>> from portabellas import Table
    >>> table = Table({"test": [1, 2, 3]})
    >>> plotter = table.plot
    """

    def __init__(self, table: Table) -> None:
        self._table: Table = table

    # ------------------------------------------------------------------------------------------------------------------
    # Gridded plots for individual columns
    # ------------------------------------------------------------------------------------------------------------------

    def box_plots(
        self,
        *,
        config: PlotConfig | None = None,
        y_axis: AxisConfig | None = None,
    ) -> Plot:
        """
        Create a box plot for every numerical column.

        Parameters
        ----------
        config:
            The configuration of the plot. If None, sensible defaults are used.
        y_axis:
            The configuration of the y-axis. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The box plot(s).

        Raises
        ------
        ColumnTypeError
            If the table contains only non-numerical columns.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2], "b": [3, 42]})
        >>> plot = table.plot.box_plots()
        """
        effective_config = PlotConfig() if config is None else config

        numerical_table = self._table.remove_non_numeric_columns()
        if numerical_table.column_count == 0:
            msg = "Tried to create box plots on a table with only non-numerical columns."
            raise ColumnTypeError(msg) from None

        columns = numerical_table.to_columns()

        max_cols = 3
        n_cols = min(len(columns), max_cols)
        n_rows = ceil(len(columns) / n_cols)

        subplot_titles = [col.name for col in columns]

        fig = make_subplots(
            rows=n_rows,
            cols=n_cols,
            subplot_titles=subplot_titles,
        )

        for i, column in enumerate(columns):
            row = i // n_cols + 1
            col = i % n_cols + 1
            fig.add_trace(
                go.Box(y=column._series.drop_nulls().to_list(), name=column.name),
                row=row,
                col=col,
            )

        apply_config(fig, effective_config)
        apply_axis_config(fig, None, y_axis)

        return Plot(fig)

    def histograms(
        self,
        *,
        max_bin_count: int = 10,
        config: PlotConfig | None = None,
    ) -> Plot:
        """
        Plot a histogram for every column.

        Parameters
        ----------
        max_bin_count:
            The maximum number of bins to use in the histogram.
        config:
            The configuration of the plot. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The histogram(s).

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [2, 3, 5, 1], "b": [54, 74, 90, 2014]})
        >>> plot = table.plot.histograms()
        """
        effective_config = PlotConfig() if config is None else config

        columns = self._table.to_columns()

        max_cols = 3
        n_cols = min(len(columns), max_cols)
        n_rows = ceil(len(columns) / n_cols)

        subplot_titles = [col.name for col in columns]

        fig = make_subplots(
            rows=n_rows,
            cols=n_cols,
            subplot_titles=subplot_titles,
        )

        for i, column in enumerate(columns):
            row = i // n_cols + 1
            col = i % n_cols + 1
            data = column._series.drop_nulls()
            xbins = compute_xbins(data, max_bin_count)
            trace_kwargs: dict = {"x": data.to_list(), "name": column.name}
            if xbins is not None:
                trace_kwargs["xbins"] = xbins
            fig.add_trace(
                go.Histogram(**trace_kwargs),
                row=row,
                col=col,
            )

        fig.update_layout(bargap=0.1)

        apply_config(fig, effective_config)

        return Plot(fig)

    def violin_plots(
        self,
        *,
        config: PlotConfig | None = None,
        y_axis: AxisConfig | None = None,
    ) -> Plot:
        """
        Create a violin plot for every numerical column.

        Parameters
        ----------
        config:
            The configuration of the plot. If None, sensible defaults are used.
        y_axis:
            The configuration of the y-axis. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The violin plot(s).

        Raises
        ------
        ColumnTypeError
            If the table contains only non-numerical columns.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2], "b": [3, 42]})
        >>> plot = table.plot.violin_plots()
        """
        effective_config = PlotConfig() if config is None else config

        numerical_table = self._table.remove_non_numeric_columns()
        if numerical_table.column_count == 0:
            msg = "Tried to create violin plots on a table with only non-numerical columns."
            raise ColumnTypeError(msg) from None

        columns = numerical_table.to_columns()

        max_cols = 3
        n_cols = min(len(columns), max_cols)
        n_rows = ceil(len(columns) / n_cols)

        subplot_titles = [col.name for col in columns]

        fig = make_subplots(
            rows=n_rows,
            cols=n_cols,
            subplot_titles=subplot_titles,
        )

        for i, column in enumerate(columns):
            row = i // n_cols + 1
            col = i % n_cols + 1
            fig.add_trace(
                go.Violin(
                    y=column._series.drop_nulls().to_list(),
                    name=column.name,
                    box_visible=True,
                    meanline_visible=True,
                ),
                row=row,
                col=col,
            )

        apply_config(fig, effective_config)
        apply_axis_config(fig, None, y_axis)

        return Plot(fig)

    # ------------------------------------------------------------------------------------------------------------------
    # Plots for two columns
    # ------------------------------------------------------------------------------------------------------------------

    def line_plot(
        self,
        x_name: str,
        y_names: list[str],
        *,
        show_confidence_interval: bool = True,
        config: PlotConfig | None = None,
        x_axis: AxisConfig | None = None,
        y_axis: AxisConfig | None = None,
    ) -> Plot:
        """
        Create a line plot for two columns in the table.

        Parameters
        ----------
        x_name:
            The name of the column to be plotted on the x-axis.
        y_names:
            The name(s) of the column(s) to be plotted on the y-axis.
        show_confidence_interval:
            If the confidence interval is shown.
        config:
            The configuration of the plot. If None, sensible defaults are used.
        x_axis:
            The configuration of the x-axis. If None, sensible defaults are used.
        y_axis:
            The configuration of the y-axis. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The line plot.

        Raises
        ------
        ColumnNotFoundError
            If a column does not exist.
        ColumnTypeError
            If a y-column is not numeric.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]})
        >>> plot = table.plot.line_plot("a", ["b"])
        """
        _validate_xy_columns(self._table, x_name, y_names)

        effective_config = PlotConfig() if config is None else config

        agg_exprs = []
        for name in y_names:
            agg_exprs.append(pl.col(name).mean().alias(f"{name}_mean"))
            agg_exprs.append(pl.count(name).alias(f"{name}_count"))
            agg_exprs.append(pl.std(name, ddof=0).alias(f"{name}_std"))

        grouped_lazy = self._table._lazy_frame.sort(x_name).group_by(x_name, maintain_order=True).agg(agg_exprs)
        grouped = safely_collect_lazy_frame(grouped_lazy)

        x = grouped.get_column(x_name).to_list()

        fig = go.Figure()

        for name in y_names:
            y_mean_series = grouped.get_column(f"{name}_mean")
            y_mean = y_mean_series.to_list()
            fig.add_trace(go.Scatter(x=x, y=y_mean, mode="lines", name=name))

            if show_confidence_interval:
                y_count = grouped.get_column(f"{name}_count")
                y_std = grouped.get_column(f"{name}_std")
                ci = 1.96 * y_std / y_count.sqrt()
                ci_upper = (y_mean_series + ci).to_list()
                ci_lower = (y_mean_series - ci).to_list()
                fig.add_trace(
                    go.Scatter(
                        x=x + x[::-1],
                        y=ci_upper + ci_lower[::-1],
                        fill="toself",
                        fillcolor="rgba(0,100,255,0.15)",
                        line={"width": 0},
                        name=f"{name} (CI)",
                        showlegend=False,
                    ),
                )

        fig.update_layout(xaxis_title=x_name)

        apply_config(fig, effective_config)
        apply_axis_config(fig, x_axis, y_axis)

        return Plot(fig)

    def histogram_2d(
        self,
        x_name: str,
        y_name: str,
        *,
        x_max_bin_count: int = 10,
        y_max_bin_count: int = 10,
        config: PlotConfig | None = None,
        x_axis: AxisConfig | None = None,
        y_axis: AxisConfig | None = None,
    ) -> Plot:
        """
        Create a 2D histogram for two columns in the table.

        Parameters
        ----------
        x_name:
            The name of the column to be plotted on the x-axis.
        y_name:
            The name of the column to be plotted on the y-axis.
        x_max_bin_count:
            The maximum number of bins to use in the histogram for the x-axis.
        y_max_bin_count:
            The maximum number of bins to use in the histogram for the y-axis.
        config:
            The configuration of the plot. If None, sensible defaults are used.
        x_axis:
            The configuration of the x-axis. If None, sensible defaults are used.
        y_axis:
            The configuration of the y-axis. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The 2D histogram.

        Raises
        ------
        ColumnNotFoundError
            If a column does not exist.
        OutOfBoundsError
            If x_max_bin_count or y_max_bin_count is less than 1.
        ColumnTypeError
            If a column is not numeric.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]})
        >>> plot = table.plot.histogram_2d("a", "b")
        """
        check_bounds("x_max_bin_count", x_max_bin_count, lower_bound=1)
        check_bounds("y_max_bin_count", y_max_bin_count, lower_bound=1)
        check_columns_exist(self._table, [x_name, y_name])

        effective_config = PlotConfig() if config is None else config

        x_data = self._table.get_column(x_name)
        y_data = self._table.get_column(y_name)

        fig = go.Figure(
            go.Histogram2d(
                x=x_data._series.drop_nulls().to_list(),
                y=y_data._series.drop_nulls().to_list(),
                nbinsx=x_max_bin_count,
                nbinsy=y_max_bin_count,
            ),
        )
        fig.update_layout(xaxis_title=x_name, yaxis_title=y_name)

        apply_config(fig, effective_config)
        apply_axis_config(fig, x_axis, y_axis)

        return Plot(fig)

    def scatter_plot(
        self,
        x_name: str,
        y_names: list[str],
        *,
        color_name: str | None = None,
        config: PlotConfig | None = None,
        x_axis: AxisConfig | None = None,
        y_axis: AxisConfig | None = None,
    ) -> Plot:
        """
        Create a scatter plot for two columns in the table.

        Parameters
        ----------
        x_name:
            The name of the column to be plotted on the x-axis.
        y_names:
            The name(s) of the column(s) to be plotted on the y-axis.
        color_name:
            The name of the column whose values are used to color the markers.
            If None, all markers have the same color.
        config:
            The configuration of the plot. If None, sensible defaults are used.
        x_axis:
            The configuration of the x-axis. If None, sensible defaults are used.
        y_axis:
            The configuration of the y-axis. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The scatter plot.

        Raises
        ------
        ColumnNotFoundError
            If a column does not exist.
        ColumnTypeError
            If a column is not numeric.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3, 4, 5], "b": [2, 3, 4, 5, 6]})
        >>> plot = table.plot.scatter_plot("a", ["b"])
        """
        _validate_xy_columns(self._table, x_name, y_names)

        if color_name is not None:
            check_columns_exist(self._table, [color_name])
            check_columns_are_numeric(self._table, [color_name], operation="color scatter plot")

        effective_config = PlotConfig() if config is None else config

        x_data = self._table.get_column(x_name)

        fig = go.Figure()

        for y_name in y_names:
            y_data = self._table.get_column(y_name)
            trace_kwargs: dict = {
                "x": x_data._series.drop_nulls().to_list(),
                "y": y_data._series.drop_nulls().to_list(),
                "mode": "markers",
                "name": y_name,
            }
            if color_name is not None:
                color_data = self._table.get_column(color_name)
                trace_kwargs["marker"] = {
                    "color": color_data._series.to_list(),
                    "colorscale": "Viridis",
                    "colorbar": {"title": color_name},
                }
            fig.add_trace(go.Scatter(**trace_kwargs))

        fig.update_layout(xaxis_title=x_name)

        apply_config(fig, effective_config)
        apply_axis_config(fig, x_axis, y_axis)

        return Plot(fig)

    # ------------------------------------------------------------------------------------------------------------------
    # Plots for all columns
    # ------------------------------------------------------------------------------------------------------------------

    def scatter_matrix(
        self,
        *,
        config: PlotConfig | None = None,
    ) -> Plot:
        """
        Create a scatter plot matrix for all numerical columns.

        Parameters
        ----------
        config:
            The configuration of the plot. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The scatter plot matrix.

        Raises
        ------
        ColumnTypeError
            If the table contains only non-numerical columns.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> plot = table.plot.scatter_matrix()
        """
        effective_config = PlotConfig() if config is None else config

        numerical_table = self._table.remove_non_numeric_columns()
        if numerical_table.column_count == 0:
            msg = "Tried to create a scatter matrix on a table with only non-numerical columns."
            raise ColumnTypeError(msg) from None

        columns = numerical_table.to_columns()

        dimensions = [{"label": col.name, "values": col._series.drop_nulls().to_list()} for col in columns]
        fig = go.Figure(data=go.Splom(dimensions=dimensions))
        fig.update_layout(dragmode="select")

        apply_config(fig, effective_config)

        return Plot(fig)

    def correlation_heatmap(
        self,
        *,
        config: PlotConfig | None = None,
    ) -> Plot:
        """
        Plot a correlation heatmap for all numerical columns of this table.

        Parameters
        ----------
        config:
            The configuration of the plot. If None, sensible defaults are used.

        Returns
        -------
        plot:
            The correlation heatmap.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"temperature": [10, 15, 20, 25, 30], "sales": [54, 74, 90, 206, 210]})
        >>> plot = table.plot.correlation_heatmap()
        """
        effective_config = PlotConfig() if config is None else config

        numerical_table = self._table.remove_non_numeric_columns()
        if numerical_table.column_count == 0:
            fig = go.Figure()
            apply_config(fig, effective_config)
            return Plot(fig)

        corr_df = numerical_table._data_frame.fill_null(0).corr()
        column_names = corr_df.columns
        corr_matrix = corr_df.to_numpy().tolist()

        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix,
                x=column_names,
                y=column_names,
                colorscale="RdBu_r",
                zmin=-1,
                zmax=1,
            ),
        )

        fig.update_layout(xaxis_constrain="domain", yaxis_constrain="domain")

        apply_config(fig, effective_config)

        return Plot(fig)


def _validate_xy_columns(table: Table, x_name: str, y_names: list[str]) -> None:
    all_names = [x_name, *y_names]
    check_columns_exist(table, all_names)
    check_columns_are_numeric(table, y_names, operation="create a plot")

    x_type = table.get_column_type(x_name)
    if not x_type.is_numeric and not x_type.is_temporal:
        msg = f"Tried to create a plot with non-numeric, non-temporal x-column '{x_name}'."
        raise ColumnTypeError(msg) from None
