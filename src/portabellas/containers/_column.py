from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, overload

from portabellas._utils import safely_collect_lazy_frame, safely_collect_lazy_frame_schema
from portabellas._validation import check_indices
from portabellas.typing._polars_data_type import PolarsDataType

if TYPE_CHECKING:
    from portabellas import Table
    from portabellas.typing import DataType

import polars as pl

from portabellas.plotting import ColumnPlotter


class Column[T](Sequence[T]):
    """
    A named, one-dimensional collection of homogeneous values.

    Parameters
    ----------
    name:
        The name of the column.
    data:
        The data of the column.
    type:
        The type of the column. If `None` (default), the type is inferred from the data.

    Examples
    --------
    >>> from portabellas import Column
    >>> Column("a", [1, 2, 3])
    +-----+
    |   a |
    | --- |
    | i64 |
    +=====+
    |   1 |
    |   2 |
    |   3 |
    +-----+

    >>> from portabellas.typing import DataType
    >>> Column("a", [1, 2, 3], type=DataType.String())
    +-----+
    | a   |
    | --- |
    | str |
    +=====+
    | 1   |
    | 2   |
    | 3   |
    +-----+
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Import
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _from_polars_series(data: pl.Series) -> Column:
        result = object.__new__(Column)
        result._name = data.name
        result.__series_cache = data
        result._lazy_frame = data.to_frame().lazy()
        result.__type_cache = PolarsDataType(data.dtype)
        return result

    @staticmethod
    def _from_polars_lazy_frame(name: str, data: pl.LazyFrame) -> Column:
        result = object.__new__(Column)
        result._name = name
        result.__series_cache = None
        result._lazy_frame = data.select(name)
        result.__type_cache = None
        return result

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __init__(
        self,
        name: str,
        data: Sequence[T],
        *,
        type: DataType | None = None,  # noqa: A002
    ) -> None:
        # Preprocessing
        dtype = None if type is None else type._polars_data_type

        # Fields
        self._name: str = name
        self.__series_cache: pl.Series | None = pl.Series(name, data, dtype=dtype, strict=False)
        self._lazy_frame: pl.LazyFrame = self.__series_cache.to_frame().lazy()
        self.__type_cache: DataType | None = PolarsDataType(self.__series_cache.dtype)

    def __contains__(self, value: object) -> bool:
        try:
            return self._series.__contains__(value)
        except pl.exceptions.InvalidOperationError:
            # Happens if types are incompatible
            return False

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> Column[T]: ...

    def __getitem__(self, index: int | slice) -> T | Column[T]:
        if isinstance(index, int):
            return self.get_value(index)

        try:
            return self._from_polars_lazy_frame(self.name, self._lazy_frame[index])
        except ValueError:
            return self._from_polars_series(self._series[index])

    def __iter__(self) -> Iterator[T]:
        return self._series.__iter__()

    def __len__(self) -> int:
        return self.row_count

    def __repr__(self) -> str:
        return self.to_table().__repr__()

    def __str__(self) -> str:
        return self.to_table().__str__()

    # ------------------------------------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def _series(self) -> pl.Series:
        if self.__series_cache is None:
            self.__series_cache = safely_collect_lazy_frame(self._lazy_frame).to_series()
            # Break chain of polars objects
            self._lazy_frame = self.__series_cache.to_frame().lazy()

        return self.__series_cache

    @property
    def name(self) -> str:
        """
        The name of the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.name
        'a'
        """
        return self._name

    @property
    def row_count(self) -> int:
        """
        The number of rows.

        **Notes:**

        - This operation loads the full data into memory, which can be expensive.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.row_count
        3
        """
        return self._series.len()

    @property
    def plot(self) -> ColumnPlotter:
        """Create interactive plots of this column."""
        # TODO: examples # noqa: FIX002
        return ColumnPlotter(self)

    @property
    def type(self) -> DataType:
        """
        The type of the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.type
        i64
        """
        if self.__type_cache is None:
            schema = safely_collect_lazy_frame_schema(self._lazy_frame)
            self.__type_cache = PolarsDataType(schema.dtypes()[0])

        return self.__type_cache

    # ------------------------------------------------------------------------------------------------------------------
    # Value operations
    # ------------------------------------------------------------------------------------------------------------------

    def get_value(self, index: int) -> T:
        """
        Return the column value at the specified index. This is equivalent to the `[]` operator (indexed access).

        Nonnegative indices are counted from the beginning (starting at 0), negative indices from the end (starting at
        -1).

        Parameters
        ----------
        index:
            The index of the requested value.

        Returns
        -------
        value:
            The value at the index.

        Raises
        ------
        IndexOutOfBoundsError
            If the index is out of bounds.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.get_value(0)
        1

        >>> column[0]
        1

        >>> column.get_value(-1)
        3

        >>> column[-1]
        3
        """
        check_indices(self, index)

        # Lazy containers do not allow indexed accesses
        return self._series[index]

    # ------------------------------------------------------------------------------------------------------------------
    # Transformations
    # ------------------------------------------------------------------------------------------------------------------

    def rename(self, new_name: str) -> Column[T]:
        """
        Rename the column and return the result as a new column.

        **Note:** The original column is not modified.

        Parameters
        ----------
        new_name:
            The new name of the column.

        Returns
        -------
        new_column:
            A column with the new name.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.rename("b")
        +-----+
        |   b |
        | --- |
        | i64 |
        +=====+
        |   1 |
        |   2 |
        |   3 |
        +-----+
        """
        result = self._lazy_frame.rename({self.name: new_name})
        return self._from_polars_lazy_frame(new_name, result)

    # ------------------------------------------------------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------------------------------------------------------

    def to_table(self) -> Table:
        """
        Create a table that contains only this column.

        Returns
        -------
        table:
            The table with this column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.to_table()
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
        from ._table import Table  # noqa: PLC0415

        return Table._from_polars_lazy_frame(self._lazy_frame)
