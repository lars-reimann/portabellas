from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from portabellas.containers._cell._cell import Cell

from ._list_operations import ListOperations

if TYPE_CHECKING:
    from portabellas.containers._cell import ConvertibleToIntCell, ConvertibleToStringCell


class ExprListOperations(ListOperations):
    def __init__(self, expression: pl.Expr) -> None:
        self._expression: pl.Expr = expression

    def contains(self, item: ConvertibleToIntCell) -> Cell:
        item_expr = _to_polars_expression(item)
        return _expr_cell(self._expression.list.contains(item_expr))

    def first(self) -> Cell:
        return _expr_cell(self._expression.list.first())

    def get(self, index: ConvertibleToIntCell) -> Cell:
        index_expr = _to_int_expression(index)
        return _expr_cell(self._expression.list.get(index_expr, null_on_oob=True))

    def join(self, separator: ConvertibleToStringCell) -> Cell:
        separator_expr = _to_string_expression(separator)
        return _expr_cell(self._expression.list.join(separator_expr))

    def last(self) -> Cell:
        return _expr_cell(self._expression.list.last())

    def length(self) -> Cell:
        return _expr_cell(self._expression.list.len())

    def max(self) -> Cell:
        return _expr_cell(self._expression.list.max())

    def min(self) -> Cell:
        return _expr_cell(self._expression.list.min())

    def reverse(self) -> Cell:
        return _expr_cell(self._expression.list.reverse())

    def sort(self, *, descending: bool = False) -> Cell:
        return _expr_cell(self._expression.list.sort(descending=descending))

    def sum(self) -> Cell:
        return _expr_cell(self._expression.list.sum())


def _expr_cell(expression: pl.Expr) -> Cell:
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import  # noqa: PLC0415

    return ExprCell(expression)


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
