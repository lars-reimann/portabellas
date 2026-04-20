from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from typing import TYPE_CHECKING, Literal, overload

from portabellas._utils import safely_collect_lazy_frame, safely_collect_lazy_frame_schema
from portabellas._validation import check_indices
from portabellas.containers._cell._expr_cell import ExprCell
from portabellas.typing._polars_data_type import PolarsDataType

if TYPE_CHECKING:
    from portabellas import Table
    from portabellas.containers import Cell
    from portabellas.typing import DataType

import polars as pl

from portabellas.plotting import ColumnPlotter


class Column[T_co](Sequence[T_co]):
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
        data: Sequence[T_co],
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Column):
            return NotImplemented
        if self is other:
            return True
        return self.name == other.name and self._series.equals(other._series)

    @overload
    def __getitem__(self, index: int) -> T_co: ...

    @overload
    def __getitem__(self, index: slice) -> Column[T_co]: ...

    def __getitem__(self, index: int | slice) -> T_co | Column[T_co]:
        if isinstance(index, int):
            return self.get_value(index)

        try:
            return self._from_polars_lazy_frame(self.name, self._lazy_frame[index])
        except ValueError:
            return self._from_polars_series(self._series[index])

    def __hash__(self) -> int:
        return hash((self.name, repr(self.type), self.row_count))

    def __iter__(self) -> Iterator[T_co]:
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

    def get_value(self, index: int) -> T_co:
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

    @overload
    def distinct_values(
        self,
        *,
        ignore_missing_values: Literal[True] = ...,
    ) -> Sequence[T_co]: ...

    @overload
    def distinct_values(
        self,
        *,
        ignore_missing_values: bool,
    ) -> Sequence[T_co | None]: ...

    def distinct_values(
        self,
        *,
        ignore_missing_values: bool = True,
    ) -> Sequence[T_co | None]:
        """
        Return the distinct values in the column.

        Parameters
        ----------
        ignore_missing_values:
            Whether to ignore missing values.

        Returns
        -------
        distinct_values:
            The distinct values in the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3, 2])
        >>> column.distinct_values()
        [1, 2, 3]
        """
        if self.row_count == 0:
            return []
        if self._series.dtype == pl.Null:
            if ignore_missing_values:
                return []
            return [None]

        series = self._series.drop_nulls() if ignore_missing_values else self._series
        return series.unique(maintain_order=True).to_list()

    # ------------------------------------------------------------------------------------------------------------------
    # Transformations
    # ------------------------------------------------------------------------------------------------------------------

    def rename(self, new_name: str) -> Column[T_co]:
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

    def map(
        self,
        mapper: Callable[[Cell[T_co]], Cell],
    ) -> Column:
        """
        Transform the values in the column and return the result as a new column.

        **Note:** The original column is not modified.

        Parameters
        ----------
        mapper:
            The function that maps a cell to a new value.

        Returns
        -------
        new_column:
            A column with the transformed values.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell < 2)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+
        """
        expression = mapper(ExprCell(pl.col(self.name)))._polars_expression.alias(self.name)
        result = self._lazy_frame.with_columns(expression)

        return self._from_polars_lazy_frame(self.name, result)

    # ------------------------------------------------------------------------------------------------------------------
    # Reductions (quantifiers)
    # ------------------------------------------------------------------------------------------------------------------

    @overload
    def all(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: Literal[True] = ...,
    ) -> bool: ...

    @overload
    def all(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: bool,
    ) -> bool | None: ...

    def all(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: bool = True,
    ) -> bool | None:
        """
        Check whether all values in the column satisfy the predicate.

        The predicate can return one of three values:

        * True, if the value satisfies the predicate.
        * False, if the value does not satisfy the predicate.
        * None, if the truthiness of the predicate is unknown, e.g. due to missing values.

        By default, cases where the truthiness of the predicate is unknown are ignored and this method returns

        * True, if the predicate always returns True or None.
        * False, if the predicate returns False at least once.

        You can instead enable Kleene logic by setting `ignore_unknown=False`. In this case, this method returns

        * True, if the predicate always returns True.
        * False, if the predicate returns False at least once.
        * None, if the predicate never returns False, but at least once None.

        Parameters
        ----------
        predicate:
            The predicate to apply to each value.
        ignore_unknown:
            Whether to ignore cases where the truthiness of the predicate is unknown.

        Returns
        -------
        all_satisfy_predicate:
            Whether all values in the column satisfy the predicate.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3, None])
        >>> column.all(lambda cell: cell > 0)
        True

        >>> column.all(lambda cell: cell < 3)
        False

        >>> print(column.all(lambda cell: cell > 0, ignore_unknown=False))
        None

        >>> column.all(lambda cell: cell < 3, ignore_unknown=False)
        False
        """
        expression = predicate(ExprCell(pl.col(self.name)))._polars_expression.all(ignore_nulls=ignore_unknown)
        frame = safely_collect_lazy_frame(self._lazy_frame.select(expression))

        return frame.item()

    @overload
    def any(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: Literal[True] = ...,
    ) -> bool: ...

    @overload
    def any(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: bool,
    ) -> bool | None: ...

    def any(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: bool = True,
    ) -> bool | None:
        """
        Check whether any value in the column satisfies the predicate.

        The predicate can return one of three values:

        * True, if the value satisfies the predicate.
        * False, if the value does not satisfy the predicate.
        * None, if the truthiness of the predicate is unknown, e.g. due to missing values.

        By default, cases where the truthiness of the predicate is unknown are ignored and this method returns

        * True, if the predicate returns True at least once.
        * False, if the predicate always returns False or None.

        You can instead enable Kleene logic by setting `ignore_unknown=False`. In this case, this method returns

        * True, if the predicate returns True at least once.
        * False, if the predicate always returns False.
        * None, if the predicate never returns True, but at least once None.

        Parameters
        ----------
        predicate:
            The predicate to apply to each value.
        ignore_unknown:
            Whether to ignore cases where the truthiness of the predicate is unknown.

        Returns
        -------
        any_satisfy_predicate:
            Whether any value in the column satisfies the predicate.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3, None])
        >>> column.any(lambda cell: cell > 2)
        True

        >>> column.any(lambda cell: cell < 0)
        False

        >>> column.any(lambda cell: cell > 2, ignore_unknown=False)
        True

        >>> print(column.any(lambda cell: cell < 0, ignore_unknown=False))
        None
        """
        expression = predicate(ExprCell(pl.col(self.name)))._polars_expression.any(ignore_nulls=ignore_unknown)
        frame = safely_collect_lazy_frame(self._lazy_frame.select(expression))

        return frame.item()

    @overload
    def count_if(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: Literal[True] = ...,
    ) -> int: ...

    @overload
    def count_if(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: bool,
    ) -> int | None: ...

    def count_if(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: bool = True,
    ) -> int | None:
        """
        Count how many values in the column satisfy the predicate.

        The predicate can return one of three results:

        * True, if the value satisfies the predicate.
        * False, if the value does not satisfy the predicate.
        * None, if the truthiness of the predicate is unknown, e.g. due to missing values.

        By default, cases where the truthiness of the predicate is unknown are ignored and this method returns how
        often the predicate returns True.

        You can instead enable Kleene logic by setting `ignore_unknown=False`. In this case, this method returns None if
        the predicate returns None at least once. Otherwise, it still returns how often the predicate returns True.

        Parameters
        ----------
        predicate:
            The predicate to apply to each value.
        ignore_unknown:
            Whether to ignore cases where the truthiness of the predicate is unknown.

        Returns
        -------
        count:
            The number of values in the column that satisfy the predicate.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3, None])
        >>> column.count_if(lambda cell: cell > 1)
        2

        >>> print(column.count_if(lambda cell: cell < 0, ignore_unknown=False))
        None
        """
        expression = predicate(ExprCell(pl.col(self.name)))._polars_expression
        frame = safely_collect_lazy_frame(self._lazy_frame.select(expression))
        series = frame.to_series()

        if ignore_unknown or not series.has_nulls():
            return int(series.sum())

        return None

    @overload
    def none(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: Literal[True] = ...,
    ) -> bool: ...

    @overload
    def none(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: bool,
    ) -> bool | None: ...

    def none(
        self,
        predicate: Callable[[Cell[T_co]], Cell[bool | None]],
        *,
        ignore_unknown: bool = True,
    ) -> bool | None:
        """
        Check whether no value in the column satisfies the predicate.

        The predicate can return one of three values:

        * True, if the value satisfies the predicate.
        * False, if the value does not satisfy the predicate.
        * None, if the truthiness of the predicate is unknown, e.g. due to missing values.

        By default, cases where the truthiness of the predicate is unknown are ignored and this method returns

        * True, if the predicate always returns False or None.
        * False, if the predicate returns True at least once.

        You can instead enable Kleene logic by setting `ignore_unknown=False`. In this case, this method returns

        * True, if the predicate always returns False.
        * False, if the predicate returns True at least once.
        * None, if the predicate never returns True, but at least once None.

        Parameters
        ----------
        predicate:
            The predicate to apply to each value.
        ignore_unknown:
            Whether to ignore cases where the truthiness of the predicate is unknown.

        Returns
        -------
        none_satisfy_predicate:
            Whether no value in the column satisfies the predicate.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3, None])
        >>> column.none(lambda cell: cell < 0)
        True

        >>> column.none(lambda cell: cell > 2)
        False

        >>> print(column.none(lambda cell: cell < 0, ignore_unknown=False))
        None

        >>> column.none(lambda cell: cell > 2, ignore_unknown=False)
        False
        """
        expression = predicate(ExprCell(pl.col(self.name)))._polars_expression.not_().all(ignore_nulls=ignore_unknown)
        frame = safely_collect_lazy_frame(self._lazy_frame.select(expression))

        return frame.item()

    # ------------------------------------------------------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------------------------------------------------------

    def to_list(self) -> list[T_co]:
        """
        Return the values of the column in a list.

        Returns
        -------
        values:
            The values of the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.to_list()
        [1, 2, 3]
        """
        return self._series.to_list()

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
        from ._table import Table  # circular import

        return Table._from_polars_lazy_frame(self._lazy_frame)

    # ------------------------------------------------------------------------------------------------------------------
    # IPython integration
    # ------------------------------------------------------------------------------------------------------------------

    def _repr_html_(self) -> str:
        """
        Return a compact HTML representation of the column for IPython.

        Returns
        -------
        html:
            The generated HTML.
        """
        return self._series._repr_html_()
