from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from portabellas._validation import check_columns_exist

from ._row import Row

if TYPE_CHECKING:
    from portabellas.containers._cell import Cell
    from portabellas.containers._table import Table


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
    # Column operations
    # ------------------------------------------------------------------------------------------------------------------

    def get_cell(self, name: str) -> Cell:
        from portabellas.containers._cell._expr_cell import ExprCell  # noqa: PLC0415

        check_columns_exist(self._table, name)

        return ExprCell(pl.col(name))
