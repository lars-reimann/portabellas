from __future__ import annotations

import math
from typing import TYPE_CHECKING

from portabellas._validation import check_bounds
from portabellas.typing import DataType, DataTypes

from ._math_operations import MathOperations, RoundingMode

if TYPE_CHECKING:
    import polars as pl

    from portabellas.containers import Cell
    from portabellas.containers._cell import ConvertibleToNumericCell

_FLOAT64 = DataTypes.Float64()


class ExprMathOperations(MathOperations):
    def __init__(self, expression: pl.Expr, type: DataType) -> None:  # noqa: A002
        self._expression: pl.Expr = expression
        self._type: DataType = type

    def abs(self) -> Cell:
        return _expr_cell(self._expression.__abs__(), type=self._type)

    def acos(self) -> Cell:
        return _expr_cell(self._expression.arccos(), type=_FLOAT64)

    def acosh(self) -> Cell:
        return _expr_cell(self._expression.arccosh(), type=_FLOAT64)

    def asin(self) -> Cell:
        return _expr_cell(self._expression.arcsin(), type=_FLOAT64)

    def asinh(self) -> Cell:
        return _expr_cell(self._expression.arcsinh(), type=_FLOAT64)

    def atan(self) -> Cell:
        return _expr_cell(self._expression.arctan(), type=_FLOAT64)

    def atanh(self) -> Cell:
        return _expr_cell(self._expression.arctanh(), type=_FLOAT64)

    def cbrt(self) -> Cell:
        return _expr_cell(self._expression.cbrt(), type=_FLOAT64)

    def ceil(self) -> Cell:
        return _expr_cell(self._expression.ceil(), type=self._type)

    def clip(
        self,
        *,
        lower_bound: ConvertibleToNumericCell = None,
        upper_bound: ConvertibleToNumericCell = None,
    ) -> Cell:
        from portabellas.containers._cell._cell import _to_polars_expression  # circular import  # noqa: PLC0415

        lower_expr = _to_polars_expression(lower_bound) if lower_bound is not None else None
        upper_expr = _to_polars_expression(upper_bound) if upper_bound is not None else None

        return _expr_cell(self._expression.clip(lower_expr, upper_expr), type=self._type)

    def cos(self) -> Cell:
        return _expr_cell(self._expression.cos(), type=_FLOAT64)

    def cosh(self) -> Cell:
        return _expr_cell(self._expression.cosh(), type=_FLOAT64)

    def cot(self) -> Cell:
        return _expr_cell(self._expression.cot(), type=_FLOAT64)

    def degrees_to_radians(self) -> Cell:
        return _expr_cell(self._expression.radians(), type=_FLOAT64)

    def exp(self) -> Cell:
        return _expr_cell(self._expression.exp(), type=_FLOAT64)

    def floor(self) -> Cell:
        return _expr_cell(self._expression.floor(), type=self._type)

    def log(self, *, base: float = math.e) -> Cell:
        check_bounds("base", base, lower_bound=0, lower_bound_mode="open")
        if base == 1:
            msg = "The base of the logarithm must not be 1."
            raise ValueError(msg)

        return _expr_cell(self._expression.log(base), type=_FLOAT64)

    def log1p(self) -> Cell:
        return _expr_cell(self._expression.log1p(), type=_FLOAT64)

    def log10(self) -> Cell:
        return _expr_cell(self._expression.log10(), type=_FLOAT64)

    def radians_to_degrees(self) -> Cell:
        return _expr_cell(self._expression.degrees(), type=_FLOAT64)

    def round_to_decimal_places(self, decimal_places: int, *, mode: RoundingMode = "half_away_from_zero") -> Cell:
        check_bounds("decimal_places", decimal_places, lower_bound=0, lower_bound_mode="closed")

        match mode:
            case "half_away_from_zero":
                return _expr_cell(self._expression.round(decimal_places, mode="half_away_from_zero"), type=self._type)
            case "half_to_even":
                return _expr_cell(self._expression.round(decimal_places, mode="half_to_even"), type=self._type)
            case "truncate":
                return _expr_cell(self._expression.truncate(decimal_places), type=self._type)
            case _:
                valid_modes = {"half_away_from_zero", "half_to_even", "truncate"}
                msg = f"Invalid rounding mode: {mode!r}. Must be one of {sorted(valid_modes)}."
                raise ValueError(msg)

    def round_to_significant_figures(self, significant_figures: int) -> Cell:
        check_bounds("significant_figures", significant_figures, lower_bound=1, lower_bound_mode="closed")

        return _expr_cell(self._expression.round_sig_figs(significant_figures), type=self._type)

    def sign(self) -> Cell:
        return _expr_cell(self._expression.sign(), type=self._type)

    def sin(self) -> Cell:
        return _expr_cell(self._expression.sin(), type=_FLOAT64)

    def sinh(self) -> Cell:
        return _expr_cell(self._expression.sinh(), type=_FLOAT64)

    def sqrt(self) -> Cell:
        return _expr_cell(self._expression.sqrt(), type=_FLOAT64)

    def tan(self) -> Cell:
        return _expr_cell(self._expression.tan(), type=_FLOAT64)

    def tanh(self) -> Cell:
        return _expr_cell(self._expression.tanh(), type=_FLOAT64)


def _expr_cell(expression: pl.Expr, *, type: DataType) -> Cell:  # noqa: A002
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import  # noqa: PLC0415

    return ExprCell(expression, type=type)
