from __future__ import annotations

import os
from typing import TYPE_CHECKING, overload

import polars as pl
import polars.selectors as cs

from portabellas._config import get_polars_config
from portabellas._utils import compute_duplicates, safely_collect_lazy_frame, safely_collect_lazy_frame_schema
from portabellas._validation import (
    check_bounds,
    check_columns_are_permutation,
    check_columns_dont_exist,
    check_columns_exist,
    check_row_counts_are_equal,
    check_schema,
)
from portabellas.containers._cell._cell import _expr_cell
from portabellas.containers._column import Column
from portabellas.containers._row import ExprRow
from portabellas.exceptions import DuplicateColumnError, LengthMismatchError
from portabellas.io import TableReader, TableWriter
from portabellas.typing import Schema
from portabellas.typing._data_type import DataTypes, _from_polars_data_type

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from typing import Literal

    from portabellas.containers import Cell, Row
    from portabellas.plotting import TablePlotter
    from portabellas.typing import DataType


from portabellas.typing import DataType


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
    """
    Create a new table by reading from various sources.

    Examples
    --------
    >>> from portabellas import Table
    >>> import tempfile
    >>> from pathlib import Path
    >>> table = Table({"a": [1, 2], "b": [3, 4]})
    >>> with tempfile.TemporaryDirectory() as tmp:
    ...     table.write.csv_file(Path(tmp) / "test.csv")
    ...     restored = Table.read.csv_file(Path(tmp) / "test.csv")
    """

    @staticmethod
    def from_columns(columns: Column | list[Column]) -> Table:
        """
        Create a table from columns.

        Parameters
        ----------
        columns:
            The columns.

        Returns
        -------
        table:
            The created table.

        Raises
        ------
        DuplicateColumnError
            If multiple columns have the same name.
        LengthMismatchError
            If some columns have different lengths.

        Examples
        --------
        >>> from portabellas import Column, Table
        >>> a = Column("a", [1, 2, 3])
        >>> b = Column("b", [4, 5, 6])
        >>> Table.from_columns([a, b])
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
        if isinstance(columns, Column):
            columns = [columns]
        if len(columns) == 0:
            return Table({})

        check_columns_dont_exist(Table({}), [column.name for column in columns])
        check_row_counts_are_equal(columns)

        return Table._from_polars_lazy_frame(
            pl.concat(
                [column._lazy_frame for column in columns],
                how="horizontal",
            ),
        )

    @staticmethod
    def from_dict(data: dict[str, list[object]]) -> Table:
        """
        Create a table from a dictionary that maps column names to column values.

        Parameters
        ----------
        data:
            The data.

        Returns
        -------
        table:
            The created table.

        Raises
        ------
        LengthMismatchError
            If columns have different row counts.

        Examples
        --------
        >>> from portabellas import Table
        >>> data = {"a": [1, 2, 3], "b": [4, 5, 6]}
        >>> Table.from_dict(data)
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
        return Table(data)

    @staticmethod
    def from_polars(data: pl.LazyFrame | pl.DataFrame) -> Table:
        """
        Create a table from a Polars LazyFrame or DataFrame.

        Parameters
        ----------
        data:
            The Polars LazyFrame or DataFrame.

        Returns
        -------
        table:
            The created table.

        Examples
        --------
        >>> import polars as pl
        >>> from portabellas import Table
        >>> Table.from_polars(pl.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        |   2 |   5 |
        |   3 |   6 |
        +-----+-----+
        >>> Table.from_polars(pl.LazyFrame({"a": [1, 2, 3], "b": [4, 5, 6]}))
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
        if isinstance(data, pl.DataFrame):
            return Table._from_polars_data_frame(data)
        return Table._from_polars_lazy_frame(data)

    @staticmethod
    def _from_polars_data_frame(data: pl.DataFrame) -> Table:
        result = object.__new__(Table)
        result.__data_frame_cache = data
        result._lazy_frame = data.lazy()
        result.__schema_cache = None
        return result

    @staticmethod
    def _from_polars_lazy_frame(data: pl.LazyFrame, *, schema: Schema | None = None) -> Table:
        result = object.__new__(Table)
        result.__data_frame_cache = None
        result._lazy_frame = data

        if schema is None or any(isinstance(t, DataTypes.Unknown) for t in schema.values()):
            result.__schema_cache = None
        else:
            result.__schema_cache = schema
            Table._cross_check_schema(result._lazy_frame, result.__schema_cache)

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
        self.__schema_cache: Schema | None = None

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Table):
            return NotImplemented
        if self is other:
            return True
        return self._data_frame.equals(other._data_frame)

    def __hash__(self) -> int:
        return hash((self.schema, self.row_count))

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

        **Notes:**

        - This operation computes the schema of the table, which can be expensive.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.column_count
        2
        """
        return self.schema.column_count

    @property
    def column_names(self) -> list[str]:
        """
        The names of the columns in the table.

        **Notes:**

        - This operation computes the schema of the table, which can be expensive.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.column_names
        ['a', 'b']
        """
        return self.schema.column_names

    @property
    def plot(self) -> TablePlotter:
        """Create interactive plots of this table."""
        from portabellas.plotting import TablePlotter  # optional dependency  # noqa: PLC0415

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
    def schema(self) -> Schema:
        """
        The schema of the table.

        **Notes:**

        - This operation computes the schema of the table, which can be expensive.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.schema
        Schema({
            'a': i64,
            'b': i64
        })
        """
        if self.__schema_cache is None:
            self.__schema_cache = Schema._from_polars_schema(
                safely_collect_lazy_frame_schema(self._lazy_frame),
            )
        return self.__schema_cache

    @property
    def write(self) -> TableWriter:
        """
        Write this table to various targets.

        Examples
        --------
        >>> from portabellas import Table
        >>> import tempfile
        >>> from pathlib import Path
        >>> table = Table({"a": [1, 2], "b": [3, 4]})
        >>> with tempfile.TemporaryDirectory() as tmp:
        ...     table.write.csv_file(Path(tmp) / "test.csv")
        """
        return TableWriter(self)

    # ------------------------------------------------------------------------------------------------------------------
    # Column operations
    # ------------------------------------------------------------------------------------------------------------------

    def add_columns(
        self,
        columns: Column | list[Column],
    ) -> Table:
        """
        Add columns to the table and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        columns:
            The columns to add.

        Returns
        -------
        new_table:
            The table with the additional columns.

        Raises
        ------
        DuplicateColumnError
            If a column name exists already. This can also happen if the new columns have duplicate names.
        LengthMismatchError
            If the columns have different row counts.

        Examples
        --------
        >>> from portabellas import Column, Table
        >>> table = Table({"a": [1, 2, 3]})
        >>> new_column = Column("b", [4, 5, 6])
        >>> table.add_columns(new_column)
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
        if isinstance(columns, Column):
            columns = [columns]
        if len(columns) == 0:
            return self

        check_columns_dont_exist(self, [column.name for column in columns])
        check_row_counts_are_equal([self, *columns], ignore_entries_without_rows=True)

        return self._from_polars_lazy_frame(
            pl.concat(
                [
                    self._lazy_frame,
                    *[column._lazy_frame for column in columns],
                ],
                how="horizontal",
            ),
        )

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

        if self.column_count == 0:
            return self.add_columns(Column(name, []))

        computed_column = mapper(ExprRow(self))

        result_schema = _build_schema_with_new_column(self.schema, name, computed_column._type)

        return self._from_polars_lazy_frame(
            self._lazy_frame.with_columns(computed_column._polars_expression.alias(name)),
            schema=result_schema,
        )

    def add_computed_columns(
        self,
        mappers: dict[str, Callable[[Row], Cell]],
    ) -> Table:
        """
        Add multiple computed columns to the table and return the result as a new table.

        Each mapper receives the same row and is evaluated independently — a mapper cannot
        reference columns added by another mapper in the same call. Chain `add_computed_column` or
        `add_computed_columns` calls if later mappers depend on earlier results.

        **Note:** The original table is not modified.

        Parameters
        ----------
        mappers:
            A dictionary mapping new column names to mapper callbacks.

        Returns
        -------
        new_table:
            The table with the computed columns.

        Raises
        ------
        DuplicateColumnError
            If a column name exists already.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.add_computed_columns(
        ...     {"c": lambda row: row["a"] + row["b"], "d": lambda row: row["a"] * row["b"]},
        ... )
        +-----+-----+-----+-----+
        |   a |   b |   c |   d |
        | --- | --- | --- | --- |
        | i64 | i64 | i64 | i64 |
        +=======================+
        |   1 |   4 |   5 |   4 |
        |   2 |   5 |   7 |  10 |
        |   3 |   6 |   9 |  18 |
        +-----+-----+-----+-----+
        """
        if len(mappers) == 0:
            return self

        check_columns_dont_exist(self, list(mappers.keys()))

        if self.column_count == 0:
            return self.add_columns([Column(name, []) for name in mappers])

        expr_row = ExprRow(self)
        result_cells = {name: mapper(expr_row) for name, mapper in mappers.items()}
        expressions = [cell._polars_expression.alias(name) for name, cell in result_cells.items()]

        new_column_types = {name: cell._type for name, cell in result_cells.items()}
        result_schema = _build_schema_with_new_columns(self.schema, new_column_types)

        return self._from_polars_lazy_frame(
            self._lazy_frame.with_columns(expressions),
            schema=result_schema,
        )

    def add_index_column(self, name: str, *, first_index: int = 0) -> Table:
        """
        Add an index column to the table and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        name:
            The name of the new column.
        first_index:
            The index to assign to the first row. Must be greater or equal to 0.

        Returns
        -------
        new_table:
            The table with the index column.

        Raises
        ------
        DuplicateColumnError
            If the column name exists already.
        OutOfBoundsError
            If `first_index` is negative.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.add_index_column("id")
        +-----+-----+-----+
        |  id |   a |   b |
        | --- | --- | --- |
        | u32 | i64 | i64 |
        +=================+
        |   0 |   1 |   4 |
        |   1 |   2 |   5 |
        |   2 |   3 |   6 |
        +-----+-----+-----+
        """
        check_columns_dont_exist(self, name)
        check_bounds("first_index", first_index, lower_bound=0)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.with_row_index(name, offset=first_index),
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
        check_columns_exist(self, name)

        return Column._from_polars_lazy_frame(name, self._lazy_frame.select(name))

    def has_column(self, name: str) -> bool:
        """
        Check if the table has a column with a specific name.

        Parameters
        ----------
        name:
            The name of the column.

        Returns
        -------
        has_column:
            Whether the table has a column with the specified name.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.has_column("a")
        True

        >>> table.has_column("c")
        False
        """
        return self.schema.has_column(name)

    def remove_columns(
        self,
        selector: str | list[str],
        *,
        ignore_unknown_names: bool = False,
    ) -> Table:
        """
        Remove the specified columns from the table and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        selector:
            The columns to remove.
        ignore_unknown_names:
            If set to True, columns that are not present in the table will be ignored.
            If set to False, an error will be raised if any of the specified columns do not exist.

        Returns
        -------
        new_table:
            The table with the columns removed.

        Raises
        ------
        ColumnNotFoundError
            If a column does not exist and unknown names are not ignored.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.remove_columns("a")
        +-----+
        |   b |
        | --- |
        | i64 |
        +=====+
        |   4 |
        |   5 |
        |   6 |
        +-----+
        """
        if isinstance(selector, str):
            selector = [selector]

        if not ignore_unknown_names:
            check_columns_exist(self, selector)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.drop(selector, strict=not ignore_unknown_names),
        )

    def rename_column(self, old_name: str, new_name: str) -> Table:
        """
        Rename a column and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        old_name:
            The name of the column to rename.
        new_name:
            The new name of the column.

        Returns
        -------
        new_table:
            The table with the column renamed.

        Raises
        ------
        ColumnNotFoundError
            If no column with the old name exists.
        DuplicateColumnError
            If a column with the new name exists already.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.rename_column("a", "c")
        +-----+-----+
        |   c |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        |   2 |   5 |
        |   3 |   6 |
        +-----+-----+
        """
        check_columns_exist(self, old_name)
        check_columns_dont_exist(self, new_name, old_names=old_name)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.rename({old_name: new_name}),
        )

    def rename_columns(self, mapper: dict[str, str] | Callable[[str], str]) -> Table:
        """
        Rename columns and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        mapper:
            Either a dict that maps old column names to new column names, or a callable that takes
            an old column name and returns the new name. When a callable is given, it is applied to
            every column.

        Returns
        -------
        new_table:
            The table with the columns renamed.

        Raises
        ------
        ColumnNotFoundError
            If a column name in the mapping does not exist.
        DuplicateColumnError
            If the new column names are not unique.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.rename_columns({"a": "c", "b": "d"})
        +-----+-----+
        |   c |   d |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        |   2 |   5 |
        |   3 |   6 |
        +-----+-----+
        >>> table.rename_columns(lambda name: name.upper())
        +-----+-----+
        |   A |   B |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        |   2 |   5 |
        |   3 |   6 |
        +-----+-----+
        """
        if isinstance(mapper, dict):
            check_columns_exist(self, list(mapper.keys()))
            check_columns_dont_exist(self, list(mapper.values()), old_names=list(mapper.keys()))
        else:
            new_names = [mapper(name) for name in self.column_names]
            check_columns_dont_exist(self, new_names, old_names=self.column_names)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.rename(mapper),
        )

    def reorder_columns(self, column_names: list[str]) -> Table:
        """
        Reorder the columns and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        column_names:
            The column names in the desired order. Must contain every column in the table exactly once.

        Returns
        -------
        new_table:
            The table with the columns reordered.

        Raises
        ------
        ColumnNotFoundError
            If a column name does not exist in the table.
        DuplicateColumnError
            If a column name appears more than once.
        ValueError
            If a table column is missing from the list.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.reorder_columns(["b", "a"])
        +-----+-----+
        |   b |   a |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   4 |   1 |
        |   5 |   2 |
        |   6 |   3 |
        +-----+-----+
        """
        check_columns_are_permutation(self, column_names)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.select(column_names),
        )

    def replace_column(
        self,
        old_name: str,
        new_columns: Column | list[Column] | Table,
    ) -> Table:
        """
        Replace a column with zero or more columns and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        old_name:
            The name of the column to replace.
        new_columns:
            The new columns.

        Returns
        -------
        new_table:
            The table with the column replaced.

        Raises
        ------
        ColumnNotFoundError
            If no column with the old name exists.
        DuplicateColumnError
            If a column name exists already. This can also happen if the new columns have duplicate names.
        LengthMismatchError
            If the columns have different row counts.

        Examples
        --------
        >>> from portabellas import Column, Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.replace_column("a", [])
        +-----+
        |   b |
        | --- |
        | i64 |
        +=====+
        |   4 |
        |   5 |
        |   6 |
        +-----+
        """
        if isinstance(new_columns, Column):
            new_columns = [new_columns]
        elif isinstance(new_columns, Table):
            new_columns = new_columns.to_columns()

        check_columns_exist(self, old_name)
        check_columns_dont_exist(self, [column.name for column in new_columns], old_names=old_name)
        check_row_counts_are_equal([self, *new_columns])

        if len(new_columns) == 0:
            return self.remove_columns(old_name, ignore_unknown_names=True)

        if len(new_columns) == 1:
            new_column = new_columns[0]
            return Table._from_polars_lazy_frame(
                self._lazy_frame.with_columns(new_column._series.alias(old_name)).rename({old_name: new_column.name}),
            )

        column_names = self.column_names
        index = column_names.index(old_name)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.select(
                cs.by_name(column_names[:index]),
                *[column._series for column in new_columns],
                cs.by_name(column_names[index + 1 :]),
            ),
        )

    def select_columns(
        self,
        selector: str | list[str],
    ) -> Table:
        """
        Select a subset of the columns and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        selector:
            The columns to keep.

        Returns
        -------
        new_table:
            The table with only a subset of the columns.

        Raises
        ------
        ColumnNotFoundError
            If a column does not exist.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.select_columns("a")
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
        check_columns_exist(self, selector)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.select(selector),
        )

    def select_computed_columns(
        self,
        mappers: dict[str, Callable[[Row], Cell]],
    ) -> Table:
        """
        Compute new columns and return a table containing only those columns.

        Unlike `add_computed_columns`, which keeps the original columns, this method drops all original columns and
        returns only the mapper-defined columns.

        Each mapper receives the same row and is evaluated independently — a mapper cannot reference columns added by
        another mapper in the same call. Chain `add_computed_column` or `add_computed_columns` calls if later mappers
        depend on earlier results.

        **Note:** The original table is not modified.

        Parameters
        ----------
        mappers:
            A dictionary mapping column names to mapper callbacks. Each callback
            receives a `Row` and returns a `Cell`. Column names may overlap
            with existing column names — the computed columns replace the originals.

        Returns
        -------
        new_table:
            A table containing only the computed columns. Original columns are dropped.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.select_computed_columns(
        ...     {"c": lambda row: row["a"] + row["b"], "d": lambda row: row["a"] * row["b"]},
        ... )
        +-----+-----+
        |   c |   d |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   5 |   4 |
        |   7 |  10 |
        |   9 |  18 |
        +-----+-----+
        """
        if len(mappers) == 0:
            return Table._from_polars_lazy_frame(self._lazy_frame.select([]))

        if self.column_count == 0:
            return Table({name: [] for name in mappers})

        expr_row = ExprRow(self)
        result_cells = {name: mapper(expr_row) for name, mapper in mappers.items()}
        expressions = [cell._polars_expression.alias(name) for name, cell in result_cells.items()]

        result_schema = Schema({name: cell._type for name, cell in result_cells.items()})

        return self._from_polars_lazy_frame(
            self._lazy_frame.with_columns(expressions).select(list(mappers.keys())),
            schema=result_schema,
        )

    def transform_columns(
        self,
        selector: str | list[str],
        mapper: Callable[[Cell], Cell] | Callable[[Cell, Row], Cell],
    ) -> Table:
        """
        Transform columns with a custom function and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        selector:
            The names of the columns to transform.
        mapper:
            The function that computes the new values. It may take either a single cell or a cell and the entire row as
            arguments.

        Returns
        -------
        new_table:
            The table with the transformed columns.

        Raises
        ------
        ColumnNotFoundError
            If no column with the specified name exists.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.transform_columns("a", lambda cell: cell + 1)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   2 |   4 |
        |   3 |   5 |
        |   4 |   6 |
        +-----+-----+

        >>> table.transform_columns(["a", "b"], lambda cell: cell + 1)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   2 |   5 |
        |   3 |   6 |
        |   4 |   7 |
        +-----+-----+
        """
        check_columns_exist(self, selector)

        if isinstance(selector, str):
            selector = [selector]

        parameter_count = mapper.__code__.co_argcount
        if parameter_count == 1:
            one_arg_mapper: Callable[[Cell], Cell] = mapper  # type: ignore[assignment]
            expressions = [
                one_arg_mapper(
                    _expr_cell(pl.col(name), type=self.schema.get_column_type(name))
                )._polars_expression.alias(name)
                for name in selector
            ]
        else:
            two_arg_mapper: Callable[[Cell, Row], Cell] = mapper  # type: ignore[assignment]
            expressions = [
                two_arg_mapper(
                    _expr_cell(pl.col(name), type=self.schema.get_column_type(name)), ExprRow(self)
                )._polars_expression.alias(name)
                for name in selector
            ]

        return Table._from_polars_lazy_frame(
            self._lazy_frame.with_columns(*expressions),
        )

    # ------------------------------------------------------------------------------------------------------------------
    # Row operations
    # ------------------------------------------------------------------------------------------------------------------

    @overload
    def count_rows_if(
        self,
        predicate: Callable[[Row], Cell],
        *,
        ignore_nulls: Literal[True] = ...,
    ) -> int: ...

    @overload
    def count_rows_if(
        self,
        predicate: Callable[[Row], Cell],
        *,
        ignore_nulls: bool,
    ) -> int | None: ...

    def count_rows_if(
        self,
        predicate: Callable[[Row], Cell],
        *,
        ignore_nulls: bool = True,
    ) -> int | None:
        """
        Count how many rows in the table satisfy the predicate.

        The predicate can return one of three results:

        * True, if the row satisfies the predicate.
        * False, if the row does not satisfy the predicate.
        * None, if the truthiness of the predicate is unknown, e.g. due to missing values.

        By default, cases where the truthiness of the predicate is unknown are ignored and this method returns how
        often the predicate returns True.

        You can instead enable Kleene logic by setting `ignore_nulls=False`. In this case, this method returns None if
        the predicate returns None at least once. Otherwise, it still returns how often the predicate returns True.

        Parameters
        ----------
        predicate:
            The predicate to apply to each row.
        ignore_nulls:
            Whether to ignore cases where the truthiness of the predicate is unknown due to null values.

        Returns
        -------
        count:
            The number of rows in the table that satisfy the predicate.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"col1": [1, 2, 3], "col2": [1, 3, None]})
        >>> table.count_rows_if(lambda row: row["col1"] < row["col2"])
        1
        """
        expression = predicate(ExprRow(self))._polars_expression
        series = safely_collect_lazy_frame(self._lazy_frame.select(expression.alias("count"))).get_column("count")

        if ignore_nulls or series.null_count() == 0:
            return int(series.sum())
        else:
            return None

    def filter_rows(
        self,
        predicate: Callable[[Row], Cell],
    ) -> Table:
        """
        Keep only rows that satisfy a condition and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        predicate:
            The function that determines which rows to keep.

        Returns
        -------
        new_table:
            The table containing only the specified rows.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.filter_rows(lambda row: row["a"] == 2)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   2 |   5 |
        +-----+-----+
        """
        mask = predicate(ExprRow(self))

        return Table._from_polars_lazy_frame(
            self._lazy_frame.filter(mask._polars_expression),
        )

    def remove_duplicate_rows(self) -> Table:
        """
        Remove duplicate rows and return the result as a new table.

        **Note:** The original table is not modified.

        Returns
        -------
        new_table:
            The table without duplicate rows.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 2], "b": [4, 5, 5]})
        >>> table.remove_duplicate_rows()
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        |   2 |   5 |
        +-----+-----+
        """
        return Table._from_polars_lazy_frame(
            self._lazy_frame.unique(maintain_order=True),
        )

    def remove_rows(
        self,
        predicate: Callable[[Row], Cell],
    ) -> Table:
        """
        Remove rows that satisfy a condition and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        predicate:
            The function that determines which rows to remove.

        Returns
        -------
        new_table:
            The table without the specified rows.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.remove_rows(lambda row: row["a"] == 2)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        |   3 |   6 |
        +-----+-----+
        """
        mask = predicate(ExprRow(self))

        return Table._from_polars_lazy_frame(
            self._lazy_frame.remove(mask._polars_expression),
        )

    def remove_rows_with_nulls(
        self,
        *,
        selector: str | list[str] | None = None,
    ) -> Table:
        """
        Remove rows that contain null values in the specified columns and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        selector:
            The columns to check. If None, all columns are checked.

        Returns
        -------
        new_table:
            The table without rows that contain null values in the specified columns.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, None, 3], "b": [4, 5, None]})
        >>> table.remove_rows_with_nulls()
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        +-----+-----+
        """
        if isinstance(selector, list) and not selector:
            return self

        return Table._from_polars_lazy_frame(
            self._lazy_frame.drop_nulls(subset=selector),
        )

    def shuffle_rows(self, *, random_seed: int = 0) -> Table:
        """
        Shuffle the rows and return the result as a new table.

        **Notes:**

        - The original table is not modified.
        - This operation must fully load the data into memory, which can be expensive.

        Parameters
        ----------
        random_seed:
            The seed for the pseudorandom number generator.

        Returns
        -------
        new_table:
            The table with the rows shuffled.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.shuffle_rows()
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   3 |   6 |
        |   1 |   4 |
        |   2 |   5 |
        +-----+-----+
        """
        return Table._from_polars_data_frame(
            self._data_frame.sample(
                fraction=1,
                shuffle=True,
                seed=random_seed,
            ),
        )

    def sample_rows_by_count(self, count: int, *, with_replacement: bool = False, random_seed: int | None = 0) -> Table:
        """
        Sample a fixed number of rows from the table.

        **Notes:**

        - The original table is not modified.
        - This operation must fully load the data into memory, which can be expensive.

        Parameters
        ----------
        count:
            The number of rows to sample. Must be at least 0.
        with_replacement:
            Whether to allow the same row to be sampled more than once.
        random_seed:
            The seed for the pseudorandom number generator. Use None for non-deterministic sampling.

        Returns
        -------
        new_table:
            The table with the sampled rows.

        Raises
        ------
        OutOfBoundsError
            If count is less than 0, or if count exceeds the number of rows without replacement.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.sample_rows_by_count(2)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        |   2 |   5 |
        +-----+-----+
        """
        check_bounds("count", count, lower_bound=0)

        if not with_replacement:
            check_bounds("count", count, upper_bound=self.row_count)

        return Table._from_polars_data_frame(
            self._data_frame.sample(
                n=count,
                with_replacement=with_replacement,
                seed=random_seed,
            ),
        )

    def sample_rows_by_fraction(
        self,
        fraction: float,
        *,
        with_replacement: bool = False,
        random_seed: int | None = 0,
    ) -> Table:
        """
        Sample a fraction of rows from the table.

        **Notes:**

        - The original table is not modified.
        - This operation must fully load the data into memory, which can be expensive.

        Parameters
        ----------
        fraction:
            The fraction of rows to sample. Must be at least 0. Must be at most 1.0 when
            `with_replacement` is False. Values greater than 1.0 are allowed when `with_replacement`
            is True (for oversampling).
        with_replacement:
            Whether to allow the same row to be sampled more than once.
        random_seed:
            The seed for the pseudorandom number generator. Use None for non-deterministic sampling.

        Returns
        -------
        new_table:
            The table with the sampled rows.

        Raises
        ------
        OutOfBoundsError
            If fraction is less than 0, or if fraction is greater than 1.0 without
            replacement.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3, 4], "b": [5, 6, 7, 8]})
        >>> table.sample_rows_by_fraction(0.5)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   5 |
        |   2 |   6 |
        +-----+-----+
        """
        check_bounds("fraction", fraction, lower_bound=0, lower_bound_mode="closed")

        if not with_replacement:
            check_bounds("fraction", fraction, upper_bound=1.0)

        return Table._from_polars_data_frame(
            self._data_frame.sample(
                fraction=fraction,
                with_replacement=with_replacement,
                seed=random_seed,
            ),
        )

    def slice_rows(self, *, start: int = 0, length: int | None = None) -> Table:
        """
        Slice the rows and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        start:
            The start index of the slice. Nonnegative indices are counted from the beginning (starting at 0), negative
            indices from the end (starting at -1).
        length:
            The length of the slice. If None, the slice contains all rows starting from `start`. Must be greater than or
            equal to 0.

        Returns
        -------
        new_table:
            The table with the slice of rows.

        Raises
        ------
        OutOfBoundsError
            If length is less than 0.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.slice_rows(start=1)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   2 |   5 |
        |   3 |   6 |
        +-----+-----+
        """
        check_bounds("length", length, lower_bound=0)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.slice(start, length),
        )

    def sort_rows(
        self,
        by: str | list[str] | Callable[[Row], Cell],
        *,
        descending: bool = False,
    ) -> Table:
        """
        Sort the rows and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        by:
            What to sort by. Can be:

            - A column name to sort by a single column.
            - A list of column names to sort by multiple columns in priority order.
            - A function that selects the sort key.

        descending:
            Whether to sort in descending order.

        Returns
        -------
        new_table:
            The table with the rows sorted.

        Raises
        ------
        ColumnNotFoundError
            If a column name does not exist.

        Examples
        --------
        >>> from portabellas import Table

        Sort by a single column:

        >>> table = Table({"a": [2, 1, 3], "b": [1, 1, 2]})
        >>> table.sort_rows("a")
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   1 |
        |   2 |   1 |
        |   3 |   2 |
        +-----+-----+

        Sort by multiple columns:

        >>> table2 = Table({"a": [2, 1, 1], "b": [1, 1, 2]})
        >>> table2.sort_rows(["a", "b"])
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   1 |
        |   1 |   2 |
        |   2 |   1 |
        +-----+-----+

        Sort by a computed key:

        >>> table3 = Table({"a": [2, 1, 3], "b": [0, 1, 2]})
        >>> table3.sort_rows(lambda row: row["a"] - row["b"])
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   1 |
        |   3 |   2 |
        |   2 |   0 |
        +-----+-----+
        """
        if isinstance(by, str | list):
            check_columns_exist(self, by)
            polars_by: str | list[str] | pl.Expr = by
        else:
            polars_by = by(ExprRow(self))._polars_expression

        return Table._from_polars_lazy_frame(
            self._lazy_frame.sort(
                polars_by,
                descending=descending,
                maintain_order=True,
            ),
        )

    # ------------------------------------------------------------------------------------------------------------------
    # Table operations
    # ------------------------------------------------------------------------------------------------------------------

    def add_tables_as_columns(self, others: Table | list[Table]) -> Table:
        """
        Add the columns of other tables and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        others:
            The tables to add as columns.

        Returns
        -------
        new_table:
            The table with the columns added.

        Raises
        ------
        DuplicateColumnError
            If a column name exists already.
        LengthMismatchError
            If the tables have different row counts.

        Examples
        --------
        >>> from portabellas import Table
        >>> table1 = Table({"a": [1, 2, 3]})
        >>> table2 = Table({"b": [4, 5, 6]})
        >>> table1.add_tables_as_columns(table2)
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
        if isinstance(others, Table):
            others = [others]

        check_columns_dont_exist(self, [name for other in others for name in other.column_names])
        check_row_counts_are_equal([self, *others], ignore_entries_without_rows=True)

        return Table._from_polars_lazy_frame(
            pl.concat(
                [
                    self._lazy_frame,
                    *[other._lazy_frame for other in others],
                ],
                how="horizontal",
            ),
        )

    def add_tables_as_rows(self, others: Table | list[Table]) -> Table:
        """
        Add the rows of other tables and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        others:
            The tables to add as rows.

        Returns
        -------
        new_table:
            The table with the rows added.

        Raises
        ------
        SchemaError
            If the schemas of the tables do not match.

        Examples
        --------
        >>> from portabellas import Table
        >>> table1 = Table({"a": [1, 2, 3]})
        >>> table2 = Table({"a": [4, 5, 6]})
        >>> table1.add_tables_as_rows(table2)
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   1 |
        |   2 |
        |   3 |
        |   4 |
        |   5 |
        |   6 |
        +-----+
        """
        if isinstance(others, Table):
            others = [others]

        for other in others:
            check_schema(self, other)

        return Table._from_polars_lazy_frame(
            pl.concat(
                [
                    self._lazy_frame,
                    *[other._lazy_frame for other in others],
                ],
                how="vertical",
            ),
        )

    def join(
        self,
        right_table: Table,
        left_names: str | list[str],
        right_names: str | list[str],
        *,
        mode: Literal["inner", "left", "right", "full"] = "inner",
    ) -> Table:
        """
        Join the current table (left table) with another table (right table) and return the result as a new table.

        Rows are matched if the values in the specified columns are equal. The parameter `left_names` controls which
        columns are used for the left table, and `right_names` does the same for the right table.

        There are various types of joins, specified by the `mode` parameter:

        - `"inner"`:
            Keep only rows that have matching values in both tables.
        - `"left"`:
            Keep all rows from the left table and the matching rows from the right table. Cells with no match are
            marked as missing values.
        - `"right"`:
            Keep all rows from the right table and the matching rows from the left table. Cells with no match are
            marked as missing values.
        - `"full"`:
            Keep all rows from both tables. Cells with no match are marked as missing values.

        **Note:** The original tables are not modified.

        Parameters
        ----------
        right_table:
            The table to join with the left table.
        left_names:
            Names of columns to join on in the left table.
        right_names:
            Names of columns to join on in the right table.
        mode:
            Specify which type of join you want to use.

        Returns
        -------
        new_table:
            The table with the joined table.

        Raises
        ------
        ColumnNotFoundError
            If a column does not exist in one of the tables.
        DuplicateColumnError
            If a column is used multiple times in the join.
        LengthMismatchError
            If the number of columns to join on is different in the two tables.
        ValueError
            If `left_names` or `right_names` are an empty list.

        Examples
        --------
        >>> from portabellas import Table
        >>> table1 = Table({"a": [1, 2], "b": [True, False]})
        >>> table2 = Table({"c": [1, 3], "d": ["a", "b"]})
        >>> table1.join(table2, "a", "c", mode="inner")
        +-----+------+-----+
        |   a | b    | d   |
        | --- | ---  | --- |
        | i64 | bool | str |
        +==================+
        |   1 | true | a   |
        +-----+------+-----+
        """
        if isinstance(left_names, str):
            left_names = [left_names]
        if isinstance(right_names, str):
            right_names = [right_names]

        check_columns_exist(self, left_names)
        check_columns_exist(right_table, right_names)

        duplicate_left_names = compute_duplicates(left_names)
        if duplicate_left_names:
            message = f"Columns to join on must be unique, but left names {duplicate_left_names} are duplicated."
            raise DuplicateColumnError(message) from None

        duplicate_right_names = compute_duplicates(right_names)
        if duplicate_right_names:
            message = f"Columns to join on must be unique, but right names {duplicate_right_names} are duplicated."
            raise DuplicateColumnError(message) from None

        if len(left_names) != len(right_names):
            message = "The number of columns to join on must be the same in both tables."
            raise LengthMismatchError(message) from None

        if not left_names:
            message = "The columns to join on must not be empty."
            raise ValueError(message) from None

        result = self._lazy_frame.join(
            right_table._lazy_frame,
            left_on=left_names,
            right_on=right_names,
            how=mode,
            maintain_order="left_right",
            coalesce=True,
        )

        return Table._from_polars_lazy_frame(result)

    def sql(self, query: str) -> Table:
        """
        Execute an SQL query against this table and return the result as a new table.

        The table is registered as `"self"` in the SQL context, so you can reference it in your query using
        `FROM self`.

        **Note:** The original table is not modified.

        Parameters
        ----------
        query:
            The SQL query to execute.

        Returns
        -------
        result:
            The table with the query results.

        Raises
        ------
        SQLQueryError
            If the query fails during query planning (e.g. syntax errors, missing column references).

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.sql("SELECT * FROM self WHERE a > 1")
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   2 |   5 |
        |   3 |   6 |
        +-----+-----+
        """
        from portabellas.query._sql_context import SQLContext  # circular import  # noqa: PLC0415

        ctx = SQLContext(tables={"self": self})
        return ctx.execute(query)

    # ------------------------------------------------------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------------------------------------------------------

    def summarize_statistics(self) -> Table:
        """
        Return a table with important statistics about this table.

        !!! warning "API Stability"

            Do not rely on the exact output of this method. In future versions, we may change the displayed statistics
            without prior notice.

        Returns
        -------
        statistics:
            The table with statistics.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 3]})
        >>> table.summarize_statistics()
        +---------------------+---------+
        | statistic           |       a |
        | ---                 |     --- |
        | str                 |     f64 |
        +===============================+
        | min                 | 1.00000 |
        | max                 | 3.00000 |
        | mean                | 2.00000 |
        | median              | 2.00000 |
        | standard deviation  | 1.41421 |
        | missing value count | 0.00000 |
        +---------------------+---------+
        """
        if self.column_count == 0:
            return Table({})

        statistic_column_name = "statistic"
        while statistic_column_name in self.column_names:
            statistic_column_name += "_"

        non_null_columns = cs.exclude(cs.by_dtype(pl.Null))

        named_statistics: dict[str, list[pl.Expr]] = {
            "min": [non_null_columns.min()],
            "max": [non_null_columns.max()],
            "mean": [cs.numeric().mean()],
            "median": [cs.numeric().median()],
            "standard deviation": [cs.numeric().std()],
            "missing value count": [cs.all().null_count()],
        }

        frame = self._lazy_frame
        schema = safely_collect_lazy_frame_schema(frame)
        for name, type_ in schema.items():
            if not type_.is_numeric() and not type_.is_(pl.Null):
                schema[name] = pl.String

        return Table._from_polars_lazy_frame(
            pl.concat(
                [
                    pl.LazyFrame({statistic_column_name: []}),
                    schema.to_frame(eager=False),
                    *[
                        frame.select(
                            pl.lit(name).alias(statistic_column_name),
                            *expressions,
                        )
                        for name, expressions in named_statistics.items()
                    ],
                ],
                how="diagonal_relaxed",
            ),
        )

    # ------------------------------------------------------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------------------------------------------------------

    def to_columns(self) -> list[Column]:
        """
        Return the data of the table as a list of columns.

        Returns
        -------
        columns:
            The columns of the table.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> columns = table.to_columns()
        """
        return [Column._from_polars_lazy_frame(name, self._lazy_frame) for name in self.column_names]

    def to_dict(self) -> dict[str, list[object]]:
        """
        Return a dictionary that maps column names to column values.

        **Note:** This operation must fully load the data into memory, which can be expensive.

        Returns
        -------
        dict:
            The dictionary representation of the table.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.to_dict()
        {'a': [1, 2, 3], 'b': [4, 5, 6]}
        """
        return self._data_frame.to_dict(as_series=False)

    def to_polars(self) -> pl.LazyFrame:
        """
        Return the internal Polars LazyFrame.

        Returns
        -------
        lazy_frame:
            The Polars LazyFrame.

        Examples
        --------
        >>> import polars as pl
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.to_polars().collect()
        shape: (3, 2)
        ┌─────┬─────┐
        │ a   ┆ b   │
        │ --- ┆ --- │
        │ i64 ┆ i64 │
        ╞═════╪═════╡
        │ 1   ┆ 4   │
        │ 2   ┆ 5   │
        │ 3   ┆ 6   │
        └─────┴─────┘
        """
        return self._lazy_frame

    # ------------------------------------------------------------------------------------------------------------------
    # IPython integration
    # ------------------------------------------------------------------------------------------------------------------

    def _repr_html_(self) -> str:
        """
        Return a compact HTML representation of the table for IPython.

        **Note:** This operation must fully load the data into memory, which can be expensive.

        Returns
        -------
        html:
            The generated HTML.
        """
        return self._data_frame._repr_html_()

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _cross_check_schema(lazy_frame: pl.LazyFrame, schema: Schema | None) -> None:
        if schema is None or "PYTEST_CURRENT_TEST" not in os.environ:
            return  # pragma: no cover

        polars_schema = safely_collect_lazy_frame_schema(lazy_frame)
        for name, cached_type in schema.items():
            if isinstance(cached_type, (DataTypes.Null, DataTypes.Unknown)):
                continue
            polars_type = _from_polars_data_type(polars_schema[name])
            assert polars_type == cached_type, (  # noqa: S101
                f"Cached type {cached_type} for column '{name}' does not match Polars-inferred type {polars_type}"
            )


def _build_schema_with_new_column(schema: Schema, name: str, type: DataType) -> Schema:  # noqa: A002
    new_entries = dict(schema.to_dict())
    new_entries[name] = type
    return Schema(new_entries)


def _build_schema_with_new_columns(schema: Schema, new_columns: dict[str, DataType]) -> Schema:
    new_entries = dict(schema.to_dict())
    new_entries.update(new_columns)
    return Schema(new_entries)
