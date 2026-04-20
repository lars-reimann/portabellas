from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AxisConfig:
    """
    Configuration for a plot axis.

    Parameters
    ----------
    log:
        Whether to use a logarithmic scale.

    Examples
    --------
    >>> from portabellas.plotting import AxisConfig
    >>> AxisConfig(log=True)
    AxisConfig(log=True)
    """

    log: bool = False
