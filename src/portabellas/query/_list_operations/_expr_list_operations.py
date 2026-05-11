from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from portabellas._validation import check_type
from portabellas._validation._cell_type_requirements import CellTypeRequirements
from portabellas.containers._cell._cell import Cell
from portabellas.typing import DataType, DataTypes
from portabellas.typing._type_inference import infer_operation_type

from ._list_operations import ListOperations

if TYPE_CHECKING:
    from portabellas.containers._cell import ConvertibleToCell, ConvertibleToIntCell, ConvertibleToStringCell

_UNKNOWN = DataTypes.Unknown()
_BOOLEAN = DataTypes.Boolean()
_STRING = DataTypes.String()
_UINT32 = DataTypes.UInt32()


class ExprListOperations(ListOperations):
    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, expression: pl.Expr, type: DataType) -> None:  # noqa: A002
        self._expression: pl.Expr = expression
        self._type: DataType = type

    def __getitem__(self, index: ConvertibleToIntCell) -> Cell:
        return self.get(index)

    # ------------------------------------------------------------------------------------------------------------------
    # Named methods
    # ------------------------------------------------------------------------------------------------------------------

    def contains(self, item: ConvertibleToCell) -> Cell:
        item_expr = _to_polars_expression(item)
        return _expr_cell(self._expression.list.contains(item_expr), type=_BOOLEAN)

    def first(self) -> Cell:
        return _expr_cell(self._expression.list.first(), type=_inner_type_if_list(self._type))

    def get(self, index: ConvertibleToIntCell) -> Cell:
        index_expr = _to_int_expression(index)
        return _expr_cell(self._expression.list.get(index_expr, null_on_oob=True), type=_inner_type_if_list(self._type))

    def join(self, separator: ConvertibleToStringCell) -> Cell:
        check_type(_inner_type_if_list(self._type), required=CellTypeRequirements.STRING)
        separator_expr = _to_string_expression(separator)
        return _expr_cell(self._expression.list.join(separator_expr), type=_STRING)

    def last(self) -> Cell:
        return _expr_cell(self._expression.list.last(), type=_inner_type_if_list(self._type))

    def length(self) -> Cell:
        return _expr_cell(self._expression.list.len(), type=_UINT32)

    def max(self) -> Cell:
        return _expr_cell(self._expression.list.max(), type=_inner_type_if_list(self._type))

    def min(self) -> Cell:
        return _expr_cell(self._expression.list.min(), type=_inner_type_if_list(self._type))

    def reverse(self) -> Cell:
        return _expr_cell(self._expression.list.reverse(), type=self._type)

    def sort(self, *, descending: bool = False) -> Cell:
        return _expr_cell(self._expression.list.sort(descending=descending), type=self._type)

    def sum(self) -> Cell:
        check_type(_inner_type_if_list(self._type), required=CellTypeRequirements.NUMERIC_OR_BOOLEAN)
        result_type = infer_operation_type(lambda a: a.list.sum(), self._type)
        return _expr_cell(self._expression.list.sum(), type=result_type)


def _expr_cell(expression: pl.Expr, *, type: DataType) -> Cell:  # noqa: A002
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import  # noqa: PLC0415

    return ExprCell(expression, type=type)


def _to_polars_expression(cell_proxy: object) -> pl.Expr:
    if isinstance(cell_proxy, Cell):
        return cell_proxy._polars_expression
    return pl.lit(cell_proxy)


def _to_int_expression(value: ConvertibleToIntCell) -> pl.Expr:
    if isinstance(value, Cell):
        return value._polars_expression
    if value is None:
        return pl.lit(value, dtype=pl.Int64)
    return pl.lit(value)


def _to_string_expression(value: ConvertibleToStringCell) -> pl.Expr:
    if isinstance(value, Cell):
        return value._polars_expression
    if value is None:
        return pl.lit(value, dtype=pl.Utf8)
    return pl.lit(value)


def _inner_type_if_list(type: DataType) -> DataType:  # noqa: A002
    if isinstance(type, DataTypes.List):
        return type.inner
    return _UNKNOWN
