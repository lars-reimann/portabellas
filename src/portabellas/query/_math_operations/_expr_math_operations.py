from __future__ import annotations

from typing import TYPE_CHECKING

from ._math_operations import MathOperations

if TYPE_CHECKING:
    import polars as pl


class ExprMathOperations(MathOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression
