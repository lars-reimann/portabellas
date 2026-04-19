from __future__ import annotations

from typing import TYPE_CHECKING

from ._datetime_operations import DatetimeOperations

if TYPE_CHECKING:
    import polars as pl


class ExprDatetimeOperations(DatetimeOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression
