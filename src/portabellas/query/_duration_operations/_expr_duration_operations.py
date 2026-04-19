from __future__ import annotations

from typing import TYPE_CHECKING

from ._duration_operations import DurationOperations

if TYPE_CHECKING:
    import polars as pl


class ExprDurationOperations(DurationOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression
