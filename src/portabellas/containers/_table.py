from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from portabellas._config import get_polars_config
from portabellas._utils import safely_collect_lazy_frame
from portabellas._validation import check_columns_dont_exist, check_columns_exist, check_row_counts_are_equal
from portabellas.io import TableReader, TableWriter
from portabellas.plotting import TablePlotter

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

    from portabellas.containers._cell import Cell
    from portabellas.containers._column import Column
    from portabellas.containers._row import Row


class Table:
    """
    A two-dimensional collection of data. It can either be seen as a list of rows or as a list of columns.

    Parameters
    ----------
    data:
        The data of the table.

    Raises
    ------
    LengthMismatchError
        If columns have different lengths.

    Examples
    --------
    >>> from portabellas import Table
    >>> Table({"a": [1, 2, 3], "b": [4, 5, 6]})
    +-----+-----+
    |   a |   b |
    | --- | --- |
    | i64 | i64 |
    +===========+
    |   1 |   4 |
    |   2 |   5 |
    |   3 |   6 |
    +-----+-----+
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------------------------------------------------------

    read: TableReader = TableReader()
    """Create a new table by reading from various sources."""
    # TODO: add examples  # noqa: FIX002

    @staticmethod
    def _from_polars_data_frame(data: pl.DataFrame) -> Table:
        result = object.__new__(Table)
        result.__data_frame_cache = data
        result._lazy_frame = data.lazy()
        return result

    @staticmethod
    def _from_polars_lazy_frame(data: pl.LazyFrame) -> Table:
        result = object.__new__(Table)
        result.__data_frame_cache = None
        result._lazy_frame = data
        return result

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self, data: Mapping[str, Sequence[object]]) -> None:
        # Validation
        check_row_counts_are_equal(data)

        # Fields
        self.__data_frame_cache: pl.DataFrame | None = None  # Scramble the name to prevent access from outside
        self._lazy_frame: pl.LazyFrame = pl.LazyFrame(data, strict=False)

    def __getitem__(self, name: str) -> Column:
        """
        Get the column with the specified name. This is equivalent to `get_column`.

        Parameters
        ----------
        name:
            The name of the column.

        Returns
        -------
        column:
            The column.

        Raises
        ------
        ColumnNotFoundError
            If the column name does not exist.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table["a"]
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   1 |
        |   2 |
        |   3 |
        +-----+
        """
        return self.get_column(name)

    def __repr__(self) -> str:
        with get_polars_config():
            return self._data_frame.__repr__()

    def __str__(self) -> str:
        with get_polars_config():
            return self._data_frame.__str__()

    # ------------------------------------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def _data_frame(self) -> pl.DataFrame:
        if self.__data_frame_cache is None:
            self.__data_frame_cache = safely_collect_lazy_frame(self._lazy_frame)
            # Break chain of polars objects
            self._lazy_frame = self.__data_frame_cache.lazy()

        return self.__data_frame_cache

    @property
    def column_count(self) -> int:
        """
        The number of columns.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.column_count
        2
        """
        return self._data_frame.width

    @property
    def plot(self) -> TablePlotter:
        """Create interactive plots of this table."""
        # TODO: add examples  # noqa: FIX002
        return TablePlotter(self)

    @property
    def row_count(self) -> int:
        """
        The number of rows.

        **Notes:**

        - This operation loads the full data into memory, which can be expensive.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.row_count
        3
        """
        return self._data_frame.height

    @property
    def write(self) -> TableWriter:
        """Write this table to various targets."""
        # TODO: add examples  # noqa: FIX002
        return TableWriter(self)

    # ------------------------------------------------------------------------------------------------------------------
    # Column operations
    # ------------------------------------------------------------------------------------------------------------------

    def add_computed_column(
        self,
        name: str,
        mapper: Callable[[Row], Cell],
    ) -> Table:
        """
        Add a computed column to the table and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        name:
            The name of the new column.
        mapper:
            The function that maps a row to the value of the new column.

        Returns
        -------
        new_table:
            The table with the computed column.

        Raises
        ------
        DuplicateColumnError
            If the column name exists already.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.add_computed_column("c", lambda row: row["a"] + row["b"])
        +-----+-----+-----+
        |   a |   b |   c |
        | --- | --- | --- |
        | i64 | i64 | i64 |
        +=================+
        |   1 |   4 |   5 |
        |   2 |   5 |   7 |
        |   3 |   6 |   9 |
        +-----+-----+-----+
        """
        check_columns_dont_exist(self, name)

        from portabellas.containers._column import Column  # noqa: PLC0415
        from portabellas.containers._row._expr_row import ExprRow  # noqa: PLC0415

        if self.column_count == 0:
            return self._add_columns(Column(name, []))

        computed_column = mapper(ExprRow(self))

        return self._from_polars_lazy_frame(
            self._lazy_frame.with_columns(computed_column._polars_expression.alias(name)),
        )

    def get_column(self, name: str) -> Column:
        """
        Get the column with the specified name. This is equivalent to the `[]` operator.

        Parameters
        ----------
        name:
            The name of the column.

        Returns
        -------
        column:
            The column.

        Raises
        ------
        ColumnNotFoundError
            If the column name does not exist.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.get_column("a")
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   1 |
        |   2 |
        |   3 |
        +-----+
        """
        from portabellas.containers._column import Column  # noqa: PLC0415

        check_columns_exist(self, name)

        return Column._from_polars_lazy_frame(name, self._lazy_frame.select(name))

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    def _add_columns(self, column: Column | list[Column]) -> Table:
        if isinstance(column, list):
            lazy_frame = self._lazy_frame
            for col in column:
                lazy_frame = lazy_frame.with_columns(col._series.rename(col.name))
        else:
            lazy_frame = self._lazy_frame.with_columns(column._series.rename(column.name))

        return self._from_polars_lazy_frame(lazy_frame)
