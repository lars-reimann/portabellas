from __future__ import annotations

from typing import TYPE_CHECKING, overload

import polars as pl

from portabellas._config import get_polars_config
from portabellas._utils import safely_collect_lazy_frame, safely_collect_lazy_frame_schema
from portabellas._validation import (
    check_bounds,
    check_columns_dont_exist,
    check_columns_exist,
    check_row_counts_are_equal,
    check_schema,
)
from portabellas.containers._column import Column
from portabellas.containers._row import ExprRow
from portabellas.exceptions import DuplicateColumnError, LengthMismatchError
from portabellas.io import TableReader, TableWriter
from portabellas.plotting import TablePlotter
from portabellas.typing import Schema

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from typing import Literal

    from polars.interchange.protocol import DataFrame

    from portabellas.containers._cell import Cell
    from portabellas.containers._row import Row
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
    ...     restored == table
    True
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
    def _from_polars_data_frame(data: pl.DataFrame) -> Table:
        result = object.__new__(Table)
        result.__data_frame_cache = data
        result._lazy_frame = data.lazy()
        result.__schema_cache = None
        return result

    @staticmethod
    def _from_polars_lazy_frame(data: pl.LazyFrame) -> Table:
        result = object.__new__(Table)
        result.__data_frame_cache = None
        result._lazy_frame = data
        result.__schema_cache = None
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
        {
            'a': i64,
            'b': i64
        }
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
        ...     restored = Table.read.csv_file(Path(tmp) / "test.csv")
        ...     restored == table
        True
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
        check_columns_exist(self, name)

        return Column._from_polars_lazy_frame(name, self._lazy_frame.select(name))

    def get_column_type(self, name: str) -> DataType:
        """
        Get the type of a column.

        Parameters
        ----------
        name:
            The name of the column.

        Returns
        -------
        type:
            The type of the column.

        Raises
        ------
        ColumnNotFoundError
            If the column does not exist.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.get_column_type("a")
        i64
        """
        return self.schema.get_column_type(name)

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

    # ------------------------------------------------------------------------------------------------------------------
    # Column operations
    # ------------------------------------------------------------------------------------------------------------------

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

    def map_columns(
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
        >>> table.map_columns("a", lambda cell: cell + 1)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   2 |   4 |
        |   3 |   5 |
        |   4 |   6 |
        +-----+-----+

        >>> table.map_columns(["a", "b"], lambda cell: cell + 1)
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

        from portabellas.containers._cell._cell import _expr_cell
        from portabellas.containers._row import ExprRow

        parameter_count = mapper.__code__.co_argcount
        if parameter_count == 1:
            one_arg_mapper: Callable[[Cell], Cell] = mapper  # type: ignore[assignment]
            expressions = [one_arg_mapper(_expr_cell(pl.col(name)))._polars_expression.alias(name) for name in selector]
        else:
            two_arg_mapper: Callable[[Cell, Row], Cell] = mapper  # type: ignore[assignment]
            expressions = [
                two_arg_mapper(_expr_cell(pl.col(name)), ExprRow(self))._polars_expression.alias(name)
                for name in selector
            ]

        return Table._from_polars_lazy_frame(
            self._lazy_frame.with_columns(*expressions),
        )

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

    def remove_columns_with_missing_values(
        self,
        *,
        missing_value_ratio_threshold: float = 0,
    ) -> Table:
        """
        Remove columns with too many missing values and return the result as a new table.

        How many missing values are allowed is determined by the `missing_value_ratio_threshold` parameter. A column is
        removed if its missing value ratio is greater than the threshold. By default, a column is removed if it contains
        any missing values.

        **Notes:**

        - The original table is not modified.
        - This operation must fully load the data into memory, which can be expensive.

        Parameters
        ----------
        missing_value_ratio_threshold:
            The maximum missing value ratio a column can have to be kept (inclusive). Must be between 0 and 1.

        Returns
        -------
        new_table:
            The table without columns that contain too many missing values.

        Raises
        ------
        OutOfBoundsError
            If the `missing_value_ratio_threshold` is not between 0 and 1.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, None]})
        >>> table.remove_columns_with_missing_values()
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
        check_bounds(
            "missing_value_ratio_threshold",
            missing_value_ratio_threshold,
            lower_bound=0,
            upper_bound=1,
        )

        mask = self._data_frame.select(
            (pl.all().null_count() / pl.len() <= missing_value_ratio_threshold),
        )

        if mask.is_empty():
            return Table({})

        return Table._from_polars_data_frame(
            self._data_frame[:, mask.row(0)],
        )

    def remove_non_numeric_columns(self) -> Table:
        """
        Remove non-numeric columns and return the result as a new table.

        **Note:** The original table is not modified.

        Returns
        -------
        new_table:
            The table without non-numeric columns.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": ["4", "5", "6"]})
        >>> table.remove_non_numeric_columns()
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
        import polars.selectors as cs

        return Table._from_polars_lazy_frame(
            self._lazy_frame.select(cs.numeric()),
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
        check_columns_dont_exist(self, new_name, old_name=old_name)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.rename({old_name: new_name}),
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
        check_columns_dont_exist(self, [column.name for column in new_columns], old_name=old_name)
        check_row_counts_are_equal([self, *new_columns])

        if len(new_columns) == 0:
            return self.remove_columns(old_name, ignore_unknown_names=True)

        import polars.selectors as cs

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

    # ------------------------------------------------------------------------------------------------------------------
    # Row operations
    # ------------------------------------------------------------------------------------------------------------------

    @overload
    def count_rows_if(
        self,
        predicate: Callable[[Row], Cell[bool | None]],
        *,
        ignore_unknown: Literal[True] = ...,
    ) -> int: ...

    @overload
    def count_rows_if(
        self,
        predicate: Callable[[Row], Cell[bool | None]],
        *,
        ignore_unknown: bool,
    ) -> int | None: ...

    def count_rows_if(
        self,
        predicate: Callable[[Row], Cell[bool | None]],
        *,
        ignore_unknown: bool = True,
    ) -> int | None:
        """
        Count how many rows in the table satisfy the predicate.

        The predicate can return one of three results:

        * True, if the row satisfies the predicate.
        * False, if the row does not satisfy the predicate.
        * None, if the truthiness of the predicate is unknown, e.g. due to missing values.

        By default, cases where the truthiness of the predicate is unknown are ignored and this method returns how
        often the predicate returns True.

        You can instead enable Kleene logic by setting `ignore_unknown=False`. In this case, this method returns None if
        the predicate returns None at least once. Otherwise, it still returns how often the predicate returns True.

        Parameters
        ----------
        predicate:
            The predicate to apply to each row.
        ignore_unknown:
            Whether to ignore cases where the truthiness of the predicate is unknown.

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

        if ignore_unknown or series.null_count() == 0:
            return int(series.sum())
        else:
            return None

    def filter_rows(
        self,
        predicate: Callable[[Row], Cell[bool | None]],
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

    def filter_rows_by_column(
        self,
        name: str,
        predicate: Callable[[Cell], Cell[bool | None]],
    ) -> Table:
        """
        Keep only rows that satisfy a condition on a specific column and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        name:
            The name of the column.
        predicate:
            The function that determines which rows to keep.

        Returns
        -------
        new_table:
            The table containing only the specified rows.

        Raises
        ------
        ColumnNotFoundError
            If the column does not exist.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.filter_rows_by_column("a", lambda cell: cell == 2)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   2 |   5 |
        +-----+-----+
        """
        check_columns_exist(self, name)

        from portabellas.containers._cell._cell import _expr_cell

        mask = predicate(_expr_cell(pl.col(name)))

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
        predicate: Callable[[Row], Cell[bool | None]],
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

    def remove_rows_by_column(
        self,
        name: str,
        predicate: Callable[[Cell], Cell[bool | None]],
    ) -> Table:
        """
        Remove rows that satisfy a condition on a specific column and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        name:
            The name of the column.
        predicate:
            The function that determines which rows to remove.

        Returns
        -------
        new_table:
            The table without the specified rows.

        Raises
        ------
        ColumnNotFoundError
            If the column does not exist.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3], "b": [4, 5, 6]})
        >>> table.remove_rows_by_column("a", lambda cell: cell == 2)
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   4 |
        |   3 |   6 |
        +-----+-----+
        """
        check_columns_exist(self, name)

        from portabellas.containers._cell._cell import _expr_cell

        mask = predicate(_expr_cell(pl.col(name)))

        return Table._from_polars_lazy_frame(
            self._lazy_frame.remove(mask._polars_expression),
        )

    def remove_rows_with_missing_values(
        self,
        *,
        selector: str | list[str] | None = None,
    ) -> Table:
        """
        Remove rows that contain missing values in the specified columns and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        selector:
            The columns to check. If None, all columns are checked.

        Returns
        -------
        new_table:
            The table without rows that contain missing values in the specified columns.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, None, 3], "b": [4, 5, None]})
        >>> table.remove_rows_with_missing_values()
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

    def remove_rows_with_outliers(
        self,
        *,
        selector: str | list[str] | None = None,
        z_score_threshold: float = 3,
    ) -> Table:
        """
        Remove rows that contain outliers in the specified columns and return the result as a new table.

        Whether a value is an outlier is determined by its z-score. If the z-score is greater than the given threshold,
        the value is considered an outlier. Missing values are ignored during the calculation of the z-score.

        The z-score is only defined for numeric columns. Non-numeric columns are ignored, even if they are specified in
        `selector`.

        **Notes:**

        - The original table is not modified.
        - This operation must fully load the data into memory, which can be expensive.

        Parameters
        ----------
        selector:
            The columns to check. If None, all columns are checked.
        z_score_threshold:
            The z-score threshold for detecting outliers. Must be greater than or equal to 0.

        Returns
        -------
        new_table:
            The table without rows that contain outliers in the specified columns.

        Raises
        ------
        OutOfBoundsError
            If the `z_score_threshold` is less than 0.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table(
        ...     {
        ...         "a": [1, 2, 3, 4, 5, 6, 1000, None],
        ...         "b": [1, 2, 3, 4, 5, 6, 7, 8],
        ...     }
        ... )
        >>> table.remove_rows_with_outliers(z_score_threshold=2)
        +------+-----+
        |    a |   b |
        |  --- | --- |
        |  i64 | i64 |
        +============+
        |    1 |   1 |
        |    2 |   2 |
        |    3 |   3 |
        |    4 |   4 |
        |    5 |   5 |
        |    6 |   6 |
        | null |   8 |
        +------+-----+
        """
        check_bounds("z_score_threshold", z_score_threshold, lower_bound=0)

        if selector is None:
            selector = self.column_names

        import polars.selectors as cs

        selected = self._lazy_frame.select(cs.numeric() & cs.by_name(selector))
        selected_names = safely_collect_lazy_frame_schema(selected).names()
        if not selected_names:
            return self

        non_outlier_mask = pl.all_horizontal(
            safely_collect_lazy_frame(
                selected.select(
                    pl.all().is_null() | ((pl.all() - pl.all().mean()).abs() <= (z_score_threshold * pl.all().std())),
                ),
            ),
        )

        return Table._from_polars_lazy_frame(
            self._lazy_frame.filter(non_outlier_mask),
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
        |   1 |   4 |
        |   3 |   6 |
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
        key_selector: Callable[[Row], Cell],
        *,
        descending: bool = False,
    ) -> Table:
        """
        Sort the rows by a custom function and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        key_selector:
            The function that selects the key to sort by.
        descending:
            Whether to sort in descending order.

        Returns
        -------
        new_table:
            The table with the rows sorted.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [2, 1, 3], "b": [1, 1, 2]})
        >>> table.sort_rows(lambda row: row["a"] - row["b"])
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   1 |
        |   2 |   1 |
        |   3 |   2 |
        +-----+-----+
        """
        key = key_selector(ExprRow(self))

        return Table._from_polars_lazy_frame(
            self._lazy_frame.sort(
                key._polars_expression,
                descending=descending,
                maintain_order=True,
            ),
        )

    def sort_rows_by_column(
        self,
        name: str,
        *,
        descending: bool = False,
    ) -> Table:
        """
        Sort the rows by a specific column and return the result as a new table.

        **Note:** The original table is not modified.

        Parameters
        ----------
        name:
            The name of the column to sort by.
        descending:
            Whether to sort in descending order.

        Returns
        -------
        new_table:
            The table with the rows sorted by the specified column.

        Raises
        ------
        ColumnNotFoundError
            If the column does not exist.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [2, 1, 3], "b": [1, 1, 2]})
        >>> table.sort_rows_by_column("a")
        +-----+-----+
        |   a |   b |
        | --- | --- |
        | i64 | i64 |
        +===========+
        |   1 |   1 |
        |   2 |   1 |
        |   3 |   2 |
        +-----+-----+
        """
        check_columns_exist(self, name)

        return Table._from_polars_lazy_frame(
            self._lazy_frame.sort(
                name,
                descending=descending,
                maintain_order=True,
            ),
        )

    def split_rows(
        self,
        percentage_in_first: float,
        *,
        shuffle: bool = True,
        random_seed: int = 0,
    ) -> tuple[Table, Table]:
        """
        Create two tables by splitting the rows of the current table.

        The first table contains a percentage of the rows specified by `percentage_in_first`, and the second table
        contains the remaining rows. By default, the rows are shuffled before splitting. You can disable this by setting
        `shuffle` to False.

        **Notes:**

        - The original table is not modified.
        - This operation must fully load the data into memory, which can be expensive.

        Parameters
        ----------
        percentage_in_first:
            The percentage of rows to include in the first table. Must be between 0 and 1.
        shuffle:
            Whether to shuffle the rows before splitting.
        random_seed:
            The seed for the pseudorandom number generator used for shuffling.

        Returns
        -------
        first_table:
            The first table.
        second_table:
            The second table.

        Raises
        ------
        OutOfBoundsError
            If `percentage_in_first` is not between 0 and 1.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"a": [1, 2, 3, 4, 5], "b": [6, 7, 8, 9, 10]})
        >>> first_table, second_table = table.split_rows(0.6)
        """
        check_bounds(
            "percentage_in_first",
            percentage_in_first,
            lower_bound=0,
            upper_bound=1,
        )

        input_table = self.shuffle_rows(random_seed=random_seed) if shuffle else self
        row_count_in_first = round(percentage_in_first * input_table.row_count)

        return (
            input_table.slice_rows(length=row_count_in_first),
            input_table.slice_rows(start=row_count_in_first),
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

        from portabellas._utils import compute_duplicates

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

    # ------------------------------------------------------------------------------------------------------------------
    # Dataframe interchange protocol
    # ------------------------------------------------------------------------------------------------------------------

    def __dataframe__(self, *, allow_copy: bool = True) -> DataFrame:
        """
        Return a dataframe object that conforms to the dataframe interchange protocol.

        Generally, there is no reason to call this method directly. The dataframe interchange protocol is designed to
        allow libraries to consume tabular data from different sources, such as `pandas` or `polars`. If you still
        decide to call this method, you should not rely on any capabilities of the returned object beyond the dataframe
        interchange protocol.

        The specification of the dataframe interchange protocol can be found
        [here](https://data-apis.org/dataframe-protocol/latest/index.html).

        **Note:** This operation must fully load the data into memory, which can be expensive.

        Parameters
        ----------
        allow_copy:
            Whether memory may be copied to create the dataframe object.

        Returns
        -------
        dataframe:
            A dataframe object that conforms to the dataframe interchange protocol.
        """
        return self._data_frame.__dataframe__(allow_copy=allow_copy)

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
        import polars.selectors as cs

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
