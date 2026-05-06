from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from portabellas._validation import check_cell_type
from portabellas._validation._cell_type_requirements import CellTypeRequirements
from portabellas.query._datetime_operations import ExprDatetimeOperations
from portabellas.query._duration_operations import ExprDurationOperations
from portabellas.query._list_operations import ExprListOperations
from portabellas.query._math_operations import ExprMathOperations
from portabellas.query._string_operations import ExprStringOperations
from portabellas.query._struct_operations import ExprStructOperations
from portabellas.typing import DataType, DataTypes

from ._cell import Cell, ConvertibleToBooleanCell, ConvertibleToCell, _to_polars_expression

if TYPE_CHECKING:
    from portabellas.query import (
        DatetimeOperations,
        DurationOperations,
        ListOperations,
        MathOperations,
        StringOperations,
        StructOperations,
    )

_UNKNOWN = DataTypes.Unknown()


class ExprCell[T](Cell[T]):
    """
    A single value in a table.

    This implementation only builds an expression that will be evaluated when needed.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, expression: pl.Expr, *, type: DataType = _UNKNOWN) -> None:  # noqa: A002
        self._expression: pl.Expr = expression
        self._type: DataType = type

    # "Boolean" operators (actually bitwise) -----------------------------------

    def __invert__(self) -> Cell[bool | None]:
        return ExprCell(self._expression.cast(pl.Boolean).__invert__())

    def __and__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__and__(other_expr))

    def __rand__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rand__(other_expr))

    def __or__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__or__(other_expr))

    def __ror__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__ror__(other_expr))

    def __xor__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__xor__(other_expr))

    def __rxor__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rxor__(other_expr))

    # Comparison ---------------------------------------------------------------

    def __eq__(self, other: object) -> Cell[bool | None]:  # type: ignore[override]
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.eq_missing(other_expr))

    def __ge__(self, other: object) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__ge__(other_expr))

    def __gt__(self, other: object) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__gt__(other_expr))

    def __le__(self, other: object) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__le__(other_expr))

    def __lt__(self, other: object) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__lt__(other_expr))

    def __ne__(self, other: object) -> Cell[bool | None]:  # type: ignore[override]
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.ne_missing(other_expr))

    # Numeric operators --------------------------------------------------------

    def __abs__(self) -> Cell:
        return ExprCell(self._expression.__abs__())

    def __ceil__(self) -> Cell:
        return ExprCell(self._expression.ceil())

    def __floor__(self) -> Cell:
        return ExprCell(self._expression.floor())

    def __neg__(self) -> Cell:
        return ExprCell(self._expression.__neg__())

    def __pos__(self) -> Cell:
        return ExprCell(self._expression.__pos__())

    def __add__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__add__(other_expr))

    def __radd__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__radd__(other_expr))

    def __floordiv__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__floordiv__(other_expr))

    def __rfloordiv__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rfloordiv__(other_expr))

    def __mod__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__mod__(other_expr))

    def __rmod__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rmod__(other_expr))

    def __mul__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__mul__(other_expr))

    def __rmul__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rmul__(other_expr))

    def __pow__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__pow__(other_expr))

    def __rpow__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rpow__(other_expr))

    def __sub__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__sub__(other_expr))

    def __rsub__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rsub__(other_expr))

    def __truediv__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__truediv__(other_expr))

    def __rtruediv__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rtruediv__(other_expr))

    # Other --------------------------------------------------------------------

    __hash__ = None

    def __repr__(self) -> str:
        return f"ExprCell({self._expression})"

    def __str__(self) -> str:
        return self._expression.__str__()

    # ------------------------------------------------------------------------------------------------------------------
    # Comparison operations
    # ------------------------------------------------------------------------------------------------------------------

    def eq(self, other: object, *, propagate_nulls: bool = False) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)

        if propagate_nulls:
            return ExprCell(self._expression.eq(other_expr))
        else:
            return ExprCell(self._expression.eq_missing(other_expr))

    def neq(self, other: object, *, propagate_nulls: bool = False) -> Cell[bool | None]:
        other_expr = _to_polars_expression(other)

        if propagate_nulls:
            return ExprCell(self._expression.ne(other_expr))
        else:
            return ExprCell(self._expression.ne_missing(other_expr))

    # ------------------------------------------------------------------------------------------------------------------
    # Properties (namespaces)
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def dt(self) -> DatetimeOperations:
        check_cell_type(self._type, required=CellTypeRequirements.DT)
        return ExprDatetimeOperations(self._expression, self._type)

    @property
    def dur(self) -> DurationOperations:
        check_cell_type(self._type, required=CellTypeRequirements.DURATION)
        return ExprDurationOperations(self._expression, self._type)

    @property
    def list(self) -> ListOperations:
        check_cell_type(self._type, required=CellTypeRequirements.LIST)
        return ExprListOperations(self._expression, self._type)

    @property
    def math(self) -> MathOperations:
        check_cell_type(self._type, required=CellTypeRequirements.NUMERIC)
        return ExprMathOperations(self._expression, self._type)

    @property
    def str(self) -> StringOperations:
        check_cell_type(self._type, required=CellTypeRequirements.STRING)
        return ExprStringOperations(self._expression, self._type)

    @property
    def struct(self) -> StructOperations:
        check_cell_type(self._type, required=CellTypeRequirements.STRUCT)
        return ExprStructOperations(self._expression, self._type)

    # ------------------------------------------------------------------------------------------------------------------
    # Other
    # ------------------------------------------------------------------------------------------------------------------

    def cast(self, type: DataType) -> Cell:  # noqa: A002
        return ExprCell(self._expression.cast(type._polars_data_type))

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def _polars_expression(self) -> pl.Expr:
        return self._expression
