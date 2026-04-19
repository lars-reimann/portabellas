from __future__ import annotations

from typing import TYPE_CHECKING

from ._string_operations import StringOperations

if TYPE_CHECKING:
    import polars as pl


class ExprStringOperations(StringOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression
