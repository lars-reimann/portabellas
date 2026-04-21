from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas._validation import check_bounds

from ._math_operations import MathOperations

if TYPE_CHECKING:
    import polars as pl

    from portabellas.containers import Cell


class ExprMathOperations(MathOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression

    def abs(self) -> Cell:
        return _expr_cell(self._expression.__abs__())

    def acos(self) -> Cell:
        return _expr_cell(self._expression.arccos())

    def acosh(self) -> Cell:
        return _expr_cell(self._expression.arccosh())

    def asin(self) -> Cell:
        return _expr_cell(self._expression.arcsin())

    def asinh(self) -> Cell:
        return _expr_cell(self._expression.arcsinh())

    def atan(self) -> Cell:
        return _expr_cell(self._expression.arctan())

    def atanh(self) -> Cell:
        return _expr_cell(self._expression.arctanh())

    def cbrt(self) -> Cell:
        return _expr_cell(self._expression.cbrt())

    def ceil(self) -> Cell:
        return _expr_cell(self._expression.ceil())

    def cos(self) -> Cell:
        return _expr_cell(self._expression.cos())

    def cosh(self) -> Cell:
        return _expr_cell(self._expression.cosh())

    def degrees_to_radians(self) -> Cell:
        return _expr_cell(self._expression.radians())

    def exp(self) -> Cell:
        return _expr_cell(self._expression.exp())

    def floor(self) -> Cell:
        return _expr_cell(self._expression.floor())

    def ln(self) -> Cell:
        return _expr_cell(self._expression.log())

    def log(self, base: float) -> Cell:
        check_bounds("base", base, lower_bound=0, lower_bound_mode="open")
        if base == 1:
            msg = "The base of the logarithm must not be 1."
            raise ValueError(msg)

        return _expr_cell(self._expression.log(base))

    def log10(self) -> Cell:
        return _expr_cell(self._expression.log10())

    def radians_to_degrees(self) -> Cell:
        return _expr_cell(self._expression.degrees())

    def round_to_decimal_places(self, decimal_places: int) -> Cell:
        check_bounds("decimal_places", decimal_places, lower_bound=0, lower_bound_mode="closed")

        return _expr_cell(self._expression.round(decimal_places, mode="half_away_from_zero"))

    def round_to_significant_figures(self, significant_figures: int) -> Cell:
        check_bounds("significant_figures", significant_figures, lower_bound=1, lower_bound_mode="closed")

        return _expr_cell(self._expression.round_sig_figs(significant_figures))

    def sign(self) -> Cell:
        return _expr_cell(self._expression.sign())

    def sin(self) -> Cell:
        return _expr_cell(self._expression.sin())

    def sinh(self) -> Cell:
        return _expr_cell(self._expression.sinh())

    def sqrt(self) -> Cell:
        return _expr_cell(self._expression.sqrt())

    def tan(self) -> Cell:
        return _expr_cell(self._expression.tan())

    def tanh(self) -> Cell:
        return _expr_cell(self._expression.tanh())


def _expr_cell(expression: pl.Expr) -> Cell:
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import  # noqa: PLC0415

    return ExprCell(expression)
