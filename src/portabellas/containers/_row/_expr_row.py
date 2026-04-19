from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from portabellas._validation import check_columns_exist

from ._row import Row

if TYPE_CHECKING:
    from portabellas.containers._cell import Cell
    from portabellas.containers._table import Table
    from portabellas.typing import DataType, Schema


class ExprRow(Row):
    """
    A one-dimensional collection of named, heterogeneous values.

    This implementation treats an entire table as a row, where each column is a "cell" in the row. Accessing a column
    only builds an expression that will be evaluated when needed.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, table: Table) -> None:
        self._table: Table = table

    # ------------------------------------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def column_count(self) -> int:
        return self._table.column_count

    @property
    def column_names(self) -> list[str]:
        return self._table.column_names

    @property
    def schema(self) -> Schema:
        return self._table.schema

    # ------------------------------------------------------------------------------------------------------------------
    # Column operations
    # ------------------------------------------------------------------------------------------------------------------

    def get_cell(self, name: str) -> Cell:
        from portabellas.containers._cell import ExprCell  # noqa: PLC0415

        check_columns_exist(self._table, name)

        return ExprCell(pl.col(name))

    def get_column_type(self, name: str) -> DataType:
        return self._table.get_column_type(name)

    def has_column(self, name: str) -> bool:
        return self._table.has_column(name)
