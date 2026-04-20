from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal


@dataclass(frozen=True)
class PlotConfig:
    """
    Configuration for a plot.

    Parameters
    ----------
    title:
        The title of the plot. If None, a sensible default is used.
    theme:
        The color theme of the plot.
    width:
        The width of the plot in pixels. If None, the default width is used.
    height:
        The height of the plot in pixels. If None, the default height is used.

    Examples
    --------
    >>> from portabellas.plotting import PlotConfig
    >>> PlotConfig(title="My Plot", theme="dark")
    PlotConfig(title='My Plot', theme='dark', width=None, height=None)
    """

    title: str | None = None
    theme: Literal["auto", "dark", "light"] = "auto"
    width: int | None = None
    height: int | None = None
