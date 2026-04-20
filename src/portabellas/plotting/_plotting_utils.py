from __future__ import annotations

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    import polars as pl

    from portabellas.plotting._axis_config import AxisConfig
    from portabellas.plotting._plot_config import PlotConfig

try:
    import plotly.graph_objects as go  # noqa: TC002
except ImportError:
    msg = "Plotting requires the 'plot' extra. Install with: pip install portabellas[plot]"
    raise ImportError(msg) from None


def apply_config(
    figure: go.Figure,
    config: PlotConfig,
) -> go.Figure:
    apply_theme(figure, config.theme)
    apply_title(figure, config.title)
    apply_size(figure, config.width, config.height)
    return figure


def apply_theme(
    figure: go.Figure,
    theme: str,
) -> go.Figure:
    resolved = "plotly" if theme == "auto" else ("plotly_dark" if theme == "dark" else "plotly")
    figure.update_layout(template=resolved)
    figure._portabellas_theme = theme
    return figure


def apply_title(
    figure: go.Figure,
    title: str | None,
) -> go.Figure:
    if title is not None:
        figure.update_layout(title=title)
    return figure


def apply_size(
    figure: go.Figure,
    width: int | None,
    height: int | None,
) -> go.Figure:
    layout_kwargs: dict = {}
    if width is not None:
        layout_kwargs["width"] = width
    if height is not None:
        layout_kwargs["height"] = height
    if layout_kwargs:
        figure.update_layout(**layout_kwargs)
    return figure


def apply_axis_config(
    figure: go.Figure,
    x_axis: AxisConfig | None,
    y_axis: AxisConfig | None,
) -> go.Figure:
    if x_axis is not None and x_axis.log:
        figure.update_xaxes(type="log")
    if y_axis is not None and y_axis.log:
        figure.update_yaxes(type="log")
    return figure


def get_theme(figure: go.Figure) -> str:
    return getattr(figure, "_portabellas_theme", "auto")


def compute_xbins(data: pl.Series, max_bin_count: int) -> dict[str, float] | None:
    if data.is_empty() or not data.dtype.is_numeric():
        return None

    min_val = float(cast("float | None", data.min()) or 0.0)
    max_val = float(cast("float | None", data.max()) or 0.0)
    if min_val == max_val:
        return {"start": min_val, "end": min_val + 1, "size": 1}

    data_range = max_val - min_val
    bin_size = data_range / max_bin_count

    if data.dtype.is_integer():
        bin_size = max(1.0, round(bin_size))

    start = min_val - bin_size * 0.5
    end = max_val + bin_size * 0.5

    return {"start": start, "end": end, "size": bin_size}
