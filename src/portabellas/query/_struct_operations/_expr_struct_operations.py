from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.typing import DataType, DataTypes

from ._struct_operations import StructOperations

if TYPE_CHECKING:
    import polars as pl

    from portabellas.containers import Cell

_UNKNOWN = DataTypes.Unknown()
_STRING = DataTypes.String()


class ExprStructOperations(StructOperations):
    def __init__(self, expression: pl.Expr, type: DataType) -> None:  # noqa: A002
        self._expression: pl.Expr = expression
        self._type: DataType = type

    def get(self, name: str) -> Cell:
        return _expr_cell(self._expression.struct.field(name))

    def rename(self, old_name: str, new_name: str) -> Cell:
        return _expr_cell(self._expression.name.map_fields(lambda name: new_name if name == old_name else name))

    def prefix_names(self, prefix: str) -> Cell:
        return _expr_cell(self._expression.name.prefix_fields(prefix))

    def suffix_names(self, suffix: str) -> Cell:
        return _expr_cell(self._expression.name.suffix_fields(suffix))

    def to_json(self) -> Cell:
        return _expr_cell(self._expression.struct.json_encode(), type=_STRING)


def _expr_cell(expression: pl.Expr, *, type: DataType = _UNKNOWN) -> Cell:  # noqa: A002
    from portabellas.containers._cell._expr_cell import ExprCell  # circular import  # noqa: PLC0415

    return ExprCell(expression, type=type)
