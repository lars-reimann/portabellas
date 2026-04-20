from __future__ import annotations

from typing import TYPE_CHECKING

import polars as pl

from portabellas._config import get_polars_config
from portabellas._utils import safely_collect_lazy_frame, safely_collect_lazy_frame_schema
from portabellas._validation import check_columns_dont_exist, check_columns_exist, check_row_counts_are_equal
from portabellas.containers._column import Column
from portabellas.containers._row import ExprRow
from portabellas.io import TableReader, TableWriter
from portabellas.plotting import TablePlotter
from portabellas.typing import Schema

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

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
    """Create a new table by reading from various sources."""
    # TODO: add examples  # noqa: FIX002

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
        """Write this table to various targets."""
        # TODO: add examples  # noqa: FIX002
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
