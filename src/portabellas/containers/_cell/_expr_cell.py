from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from portabellas._validation import check_type
from portabellas._validation._cell_type_requirements import CellTypeRequirements
from portabellas.query._datetime_operations import ExprDatetimeOperations
from portabellas.query._duration_operations import ExprDurationOperations
from portabellas.query._list_operations import ExprListOperations
from portabellas.query._math_operations import ExprMathOperations
from portabellas.query._string_operations import ExprStringOperations
from portabellas.query._struct_operations import ExprStructOperations
from portabellas.typing import DataType, DataTypes
from portabellas.typing._type_inference import infer_operation_type

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

_BOOLEAN = DataTypes.Boolean()


class ExprCell(Cell):
    """
    A single value in a table.

    This implementation only builds an expression that will be evaluated when needed.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, expression: pl.Expr, *, type: DataType) -> None:  # noqa: A002
        self._expression: pl.Expr = expression
        self.__type: DataType = type

    # "Boolean" operators (actually bitwise) -----------------------------------

    def __invert__(self) -> Cell:
        check_type(self, required=CellTypeRequirements.BOOLEAN)
        return ExprCell(self._expression.cast(pl.Boolean).__invert__(), type=_BOOLEAN)

    def __and__(self, other: ConvertibleToBooleanCell) -> Cell:
        check_type(self, required=CellTypeRequirements.BOOLEAN)
        check_type(other, required=CellTypeRequirements.BOOLEAN)
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__and__(other_expr), type=_BOOLEAN)

    def __rand__(self, other: ConvertibleToBooleanCell) -> Cell:
        check_type(self, required=CellTypeRequirements.BOOLEAN)
        check_type(other, required=CellTypeRequirements.BOOLEAN)
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rand__(other_expr), type=_BOOLEAN)

    def __or__(self, other: ConvertibleToBooleanCell) -> Cell:
        check_type(self, required=CellTypeRequirements.BOOLEAN)
        check_type(other, required=CellTypeRequirements.BOOLEAN)
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__or__(other_expr), type=_BOOLEAN)

    def __ror__(self, other: ConvertibleToBooleanCell) -> Cell:
        check_type(self, required=CellTypeRequirements.BOOLEAN)
        check_type(other, required=CellTypeRequirements.BOOLEAN)
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__ror__(other_expr), type=_BOOLEAN)

    def __xor__(self, other: ConvertibleToBooleanCell) -> Cell:
        check_type(self, required=CellTypeRequirements.BOOLEAN)
        check_type(other, required=CellTypeRequirements.BOOLEAN)
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__xor__(other_expr), type=_BOOLEAN)

    def __rxor__(self, other: ConvertibleToBooleanCell) -> Cell:
        check_type(self, required=CellTypeRequirements.BOOLEAN)
        check_type(other, required=CellTypeRequirements.BOOLEAN)
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__rxor__(other_expr), type=_BOOLEAN)

    # Comparison ---------------------------------------------------------------

    def __eq__(self, other: object) -> Cell:  # type: ignore[override]
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.eq_missing(other_expr), type=_BOOLEAN)

    def __ge__(self, other: object) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__ge__(other_expr), type=_BOOLEAN)

    def __gt__(self, other: object) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__gt__(other_expr), type=_BOOLEAN)

    def __le__(self, other: object) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__le__(other_expr), type=_BOOLEAN)

    def __lt__(self, other: object) -> Cell:
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.__lt__(other_expr), type=_BOOLEAN)

    def __ne__(self, other: object) -> Cell:  # type: ignore[override]
        other_expr = _to_polars_expression(other)
        return ExprCell(self._expression.ne_missing(other_expr), type=_BOOLEAN)

    # Numeric operators --------------------------------------------------------

    def __abs__(self) -> Cell:
        check_type(self, required=CellTypeRequirements.NUMERIC)
        return ExprCell(self._expression.__abs__(), type=self._type)

    def __ceil__(self) -> Cell:
        check_type(self, required=CellTypeRequirements.NUMERIC)
        return ExprCell(self._expression.ceil(), type=self._type)

    def __floor__(self) -> Cell:
        check_type(self, required=CellTypeRequirements.NUMERIC)
        return ExprCell(self._expression.floor(), type=self._type)

    def __neg__(self) -> Cell:
        check_type(self, required=CellTypeRequirements.NUMERIC)
        return ExprCell(self._expression.__neg__(), type=self._type)

    def __pos__(self) -> Cell:
        check_type(self, required=CellTypeRequirements.NUMERIC)
        return ExprCell(self._expression.__pos__(), type=self._type)

    def __add__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__add__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__add__(other_expr), type=result_type)

    def __radd__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__radd__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__radd__(other_expr), type=result_type)

    def __floordiv__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__floordiv__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__floordiv__(other_expr), type=result_type)

    def __rfloordiv__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__rfloordiv__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__rfloordiv__(other_expr), type=result_type)

    def __mod__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__mod__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__mod__(other_expr), type=result_type)

    def __rmod__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__rmod__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__rmod__(other_expr), type=result_type)

    def __mul__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__mul__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__mul__(other_expr), type=result_type)

    def __rmul__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__rmul__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__rmul__(other_expr), type=result_type)

    def __pow__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__pow__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__pow__(other_expr), type=result_type)

    def __rpow__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__rpow__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__rpow__(other_expr), type=result_type)

    def __sub__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__sub__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__sub__(other_expr), type=result_type)

    def __rsub__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__rsub__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__rsub__(other_expr), type=result_type)

    def __truediv__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__truediv__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__truediv__(other_expr), type=result_type)

    def __rtruediv__(self, other: ConvertibleToCell) -> Cell:
        other_expr = _to_polars_expression(other)
        result_type = infer_operation_type(pl.Expr.__rtruediv__, self._type, _type_or_literal_of_other(other))
        return ExprCell(self._expression.__rtruediv__(other_expr), type=result_type)

    # Other --------------------------------------------------------------------

    __hash__ = None

    def __repr__(self) -> str:
        return f"ExprCell({self._expression})"

    def __str__(self) -> str:
        return self._expression.__str__()

    # ------------------------------------------------------------------------------------------------------------------
    # Comparison operations
    # ------------------------------------------------------------------------------------------------------------------

    def eq(self, other: object, *, propagate_nulls: bool = False) -> Cell:
        other_expr = _to_polars_expression(other)

        if propagate_nulls:
            return ExprCell(self._expression.eq(other_expr), type=_BOOLEAN)
        else:
            return ExprCell(self._expression.eq_missing(other_expr), type=_BOOLEAN)

    def neq(self, other: object, *, propagate_nulls: bool = False) -> Cell:
        other_expr = _to_polars_expression(other)

        if propagate_nulls:
            return ExprCell(self._expression.ne(other_expr), type=_BOOLEAN)
        else:
            return ExprCell(self._expression.ne_missing(other_expr), type=_BOOLEAN)

    # ------------------------------------------------------------------------------------------------------------------
    # Properties (namespaces)
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def dt(self) -> DatetimeOperations:
        check_type(self, required=CellTypeRequirements.DT)
        return ExprDatetimeOperations(self._expression, self._type)

    @property
    def dur(self) -> DurationOperations:
        check_type(self, required=CellTypeRequirements.DURATION)
        return ExprDurationOperations(self._expression, self._type)

    @property
    def list(self) -> ListOperations:
        check_type(self, required=CellTypeRequirements.LIST)
        return ExprListOperations(self._expression, self._type)

    @property
    def math(self) -> MathOperations:
        check_type(self._type, required=CellTypeRequirements.NUMERIC)
        return ExprMathOperations(self._expression, self._type)

    @property
    def str(self) -> StringOperations:
        check_type(self, required=CellTypeRequirements.STRING)
        return ExprStringOperations(self._expression, self._type)

    @property
    def struct(self) -> StructOperations:
        check_type(self, required=CellTypeRequirements.STRUCT)
        return ExprStructOperations(self._expression, self._type)

    # ------------------------------------------------------------------------------------------------------------------
    # Other
    # ------------------------------------------------------------------------------------------------------------------

    def cast(self, type: DataType) -> Cell:  # noqa: A002
        return ExprCell(self._expression.cast(type._polars_data_type), type=type)

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def _polars_expression(self) -> pl.Expr:
        return self._expression

    @property
    def _type(self) -> DataType:
        return self.__type


def _type_or_literal_of_other(other: object) -> DataType | object:
    if isinstance(other, Cell):
        return other._type
    return other
