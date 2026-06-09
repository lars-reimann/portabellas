from __future__ import annotations

import os
from collections.abc import Callable, Iterator, Sequence
from typing import TYPE_CHECKING, Literal, cast, overload

from portabellas._utils import safely_collect_lazy_frame, safely_collect_lazy_frame_schema
from portabellas._validation import (
    check_bounds,
    check_column_has_no_nulls,
    check_column_is_numeric,
    check_indices,
    check_row_counts_are_equal,
)
from portabellas.containers._cell._expr_cell import ExprCell
from portabellas.typing._data_type import DataType, DataTypes, _from_polars_data_type
from portabellas.typing._type_inference import infer_type_from_literal

if TYPE_CHECKING:
    from portabellas import Table
    from portabellas.containers import Cell
    from portabellas.plotting import ColumnPlotter

import polars as pl
from polars.exceptions import InvalidOperationError

_UNKNOWN = DataTypes.Unknown()


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

    >>> from portabellas.typing import DataTypes
    >>> Column("a", [1, 2, 3], type=DataTypes.String())
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
    def from_polars(data: pl.Series) -> Column:
        """
        Create a column from a Polars Series.

        Parameters
        ----------
        data:
            The Polars Series.

        Returns
        -------
        column:
            The created column.

        Examples
        --------
        >>> import polars as pl
        >>> from portabellas import Column
        >>> Column.from_polars(pl.Series("a", [1, 2, 3]))
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
        return Column._from_polars_series(data)

    @staticmethod
    def _from_polars_series(data: pl.Series) -> Column:
        result = object.__new__(Column)
        result._name = data.name
        result.__series_cache = data
        result._lazy_frame = data.to_frame().lazy()
        result.__type_cache = _from_polars_data_type(data.dtype)
        return result

    @staticmethod
    def _from_polars_lazy_frame(name: str, data: pl.LazyFrame, *, type: DataType = _UNKNOWN) -> Column:  # noqa: A002
        result = object.__new__(Column)
        result._name = name
        result.__series_cache = None
        result._lazy_frame = data.select(name)

        if isinstance(type, DataTypes.Unknown):
            result.__type_cache = None
        else:
            result.__type_cache = type
            Column._cross_check_type(result._lazy_frame, type)

        return result

    @staticmethod
    def repeat(name: str, value: object, count: int, *, type: DataType | None = None) -> Column:  # noqa: A002
        check_bounds("count", count, lower_bound=0)

        dtype = type._polars_data_type if type is not None else None
        inferred_type = type if type is not None else infer_type_from_literal(value)
        lazy_frame = pl.LazyFrame().select(pl.repeat(value, count, dtype=dtype).alias(name))
        return Column._from_polars_lazy_frame(name, lazy_frame, type=inferred_type)

    @staticmethod
    def zeros(name: str, count: int, *, type: DataType | None = None) -> Column:  # noqa: A002
        check_bounds("count", count, lower_bound=0)

        inferred_type = type if type is not None else DataTypes.Float64()
        dtype = inferred_type._polars_data_type
        lazy_frame = pl.LazyFrame().select(pl.zeros(count, dtype=dtype).alias(name))
        return Column._from_polars_lazy_frame(name, lazy_frame, type=inferred_type)

    @staticmethod
    def ones(name: str, count: int, *, type: DataType | None = None) -> Column:  # noqa: A002
        check_bounds("count", count, lower_bound=0)

        inferred_type = type if type is not None else DataTypes.Float64()
        dtype = inferred_type._polars_data_type
        lazy_frame = pl.LazyFrame().select(pl.ones(count, dtype=dtype).alias(name))
        return Column._from_polars_lazy_frame(name, lazy_frame, type=inferred_type)

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
        self.__type_cache: DataType | None = _from_polars_data_type(self.__series_cache.dtype)

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
        from portabellas.plotting import ColumnPlotter  # optional dependency  # noqa: PLC0415

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
            self.__type_cache = _from_polars_data_type(schema.dtypes()[0])

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
        ignore_nulls: Literal[True] = ...,
    ) -> Sequence[T_co]: ...

    @overload
    def distinct_values(
        self,
        *,
        ignore_nulls: bool,
    ) -> Sequence[T_co | None]: ...

    def distinct_values(
        self,
        *,
        ignore_nulls: bool = True,
    ) -> Sequence[T_co | None]:
        """
        Return the distinct values in the column.

        Parameters
        ----------
        ignore_nulls:
            Whether to ignore null values.

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
            if ignore_nulls:
                return []
            return [None]

        series = self._series.drop_nulls() if ignore_nulls else self._series
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
        mapper: Callable[[Cell], Cell],
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
        result_cell = mapper(ExprCell(pl.col(self.name), type=self.type))
        expression = result_cell._polars_expression.alias(self.name)
        result = self._lazy_frame.with_columns(expression)

        return self._from_polars_lazy_frame(self.name, result, type=result_cell._type)

    # ------------------------------------------------------------------------------------------------------------------
    # Reductions (quantifiers)
    # ------------------------------------------------------------------------------------------------------------------

    @overload
    def all(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: Literal[True] = ...,
    ) -> bool: ...

    @overload
    def all(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: bool,
    ) -> bool | None: ...

    def all(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: bool = True,
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

        You can instead enable Kleene logic by setting `ignore_nulls=False`. In this case, this method returns

        * True, if the predicate always returns True.
        * False, if the predicate returns False at least once.
        * None, if the predicate never returns False, but at least once None.

        Parameters
        ----------
        predicate:
            The predicate to apply to each value.
        ignore_nulls:
            Whether to ignore cases where the truthiness of the predicate is unknown due to null values.

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

        >>> print(column.all(lambda cell: cell > 0, ignore_nulls=False))
        None

        >>> column.all(lambda cell: cell < 3, ignore_nulls=False)
        False
        """
        expression = predicate(ExprCell(pl.col(self.name), type=self.type))._polars_expression.all(
            ignore_nulls=ignore_nulls
        )
        frame = safely_collect_lazy_frame(self._lazy_frame.select(expression))

        return frame.item()

    @overload
    def any(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: Literal[True] = ...,
    ) -> bool: ...

    @overload
    def any(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: bool,
    ) -> bool | None: ...

    def any(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: bool = True,
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

        You can instead enable Kleene logic by setting `ignore_nulls=False`. In this case, this method returns

        * True, if the predicate returns True at least once.
        * False, if the predicate always returns False.
        * None, if the predicate never returns True, but at least once None.

        Parameters
        ----------
        predicate:
            The predicate to apply to each value.
        ignore_nulls:
            Whether to ignore cases where the truthiness of the predicate is unknown due to null values.

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

        >>> column.any(lambda cell: cell > 2, ignore_nulls=False)
        True

        >>> print(column.any(lambda cell: cell < 0, ignore_nulls=False))
        None
        """
        expression = predicate(ExprCell(pl.col(self.name), type=self.type))._polars_expression.any(
            ignore_nulls=ignore_nulls
        )
        frame = safely_collect_lazy_frame(self._lazy_frame.select(expression))

        return frame.item()

    @overload
    def count_if(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: Literal[True] = ...,
    ) -> int: ...

    @overload
    def count_if(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: bool,
    ) -> int | None: ...

    def count_if(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: bool = True,
    ) -> int | None:
        """
        Count how many values in the column satisfy the predicate.

        The predicate can return one of three results:

        * True, if the value satisfies the predicate.
        * False, if the value does not satisfy the predicate.
        * None, if the truthiness of the predicate is unknown, e.g. due to missing values.

        By default, cases where the truthiness of the predicate is unknown are ignored and this method returns how
        often the predicate returns True.

        You can instead enable Kleene logic by setting `ignore_nulls=False`. In this case, this method returns None if
        the predicate returns None at least once. Otherwise, it still returns how often the predicate returns True.

        Parameters
        ----------
        predicate:
            The predicate to apply to each value.
        ignore_nulls:
            Whether to ignore cases where the truthiness of the predicate is unknown due to null values.

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

        >>> print(column.count_if(lambda cell: cell < 0, ignore_nulls=False))
        None
        """
        expression = predicate(ExprCell(pl.col(self.name), type=self.type))._polars_expression
        frame = safely_collect_lazy_frame(self._lazy_frame.select(expression))
        series = frame.to_series()

        if ignore_nulls or not series.has_nulls():
            return int(series.sum())

        return None

    @overload
    def none(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: Literal[True] = ...,
    ) -> bool: ...

    @overload
    def none(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: bool,
    ) -> bool | None: ...

    def none(
        self,
        predicate: Callable[[Cell], Cell],
        *,
        ignore_nulls: bool = True,
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

        You can instead enable Kleene logic by setting `ignore_nulls=False`. In this case, this method returns

        * True, if the predicate always returns False.
        * False, if the predicate returns True at least once.
        * None, if the predicate never returns True, but at least once None.

        Parameters
        ----------
        predicate:
            The predicate to apply to each value.
        ignore_nulls:
            Whether to ignore cases where the truthiness of the predicate is unknown due to null values.

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

        >>> print(column.none(lambda cell: cell < 0, ignore_nulls=False))
        None

        >>> column.none(lambda cell: cell > 2, ignore_nulls=False)
        False
        """
        expression = (
            predicate(ExprCell(pl.col(self.name), type=self.type))
            ._polars_expression.not_()
            .all(ignore_nulls=ignore_nulls)
        )
        frame = safely_collect_lazy_frame(self._lazy_frame.select(expression))

        return frame.item()

    # ------------------------------------------------------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------------------------------------------------------

    def max(self) -> T_co | None:
        """
        Return the maximum value in the column.

        Returns
        -------
        max:
            The maximum value in the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.max()
        3
        """
        try:
            return cast("T_co | None", self._series.max())
        except InvalidOperationError:
            return None

    def mean(self) -> float:
        """
        Return the mean of the values in the column.

        The mean is the sum of the values divided by the number of values.

        Returns
        -------
        mean:
            The mean of the values in the column.

        Raises
        ------
        ColumnTypeError
            If the column is not numeric.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.mean()
        2.0
        """
        check_column_is_numeric(self, operation="calculate the mean")

        return cast("float", self._series.mean())

    def median(self) -> float:
        """
        Return the median of the values in the column.

        The median is the value in the middle of the sorted list of values. If the number of values is even, the median
        is the mean of the two middle values.

        Returns
        -------
        median:
            The median of the values in the column.

        Raises
        ------
        ColumnTypeError
            If the column is not numeric.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.median()
        2.0

        >>> column = Column("a", [1, 2, 3, 4])
        >>> column.median()
        2.5
        """
        check_column_is_numeric(self, operation="calculate the median")

        return cast("float", self._series.median())

    def min(self) -> T_co | None:
        """
        Return the minimum value in the column.

        Returns
        -------
        min:
            The minimum value in the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.min()
        1
        """
        try:
            return cast("T_co | None", self._series.min())
        except InvalidOperationError:
            return None

    @overload
    def mode(
        self,
        *,
        ignore_nulls: Literal[True] = ...,
    ) -> Sequence[T_co]: ...

    @overload
    def mode(
        self,
        *,
        ignore_nulls: bool,
    ) -> Sequence[T_co | None]: ...

    def mode(
        self,
        *,
        ignore_nulls: bool = True,
    ) -> Sequence[T_co | None]:
        """
        Return the mode of the values in the column.

        The mode is the value that appears most frequently in the column. If multiple values occur equally often, all
        of them are returned. The values are sorted in ascending order.

        Parameters
        ----------
        ignore_nulls:
            Whether to ignore null values.

        Returns
        -------
        mode:
            The mode of the values in the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [3, 1, 2, 1, 3])
        >>> column.mode()
        [1, 3]
        """
        if self.row_count == 0:
            return []
        if self._series.dtype == pl.Null:
            if ignore_nulls:
                return []
            return [None]

        series = self._series.drop_nulls() if ignore_nulls else self._series
        return series.mode().sort().to_list()

    def standard_deviation(self) -> float:
        """
        Return the standard deviation of the values in the column.

        The standard deviation is the square root of the variance.

        Returns
        -------
        standard_deviation:
            The standard deviation of the values in the column.

        Raises
        ------
        ColumnTypeError
            If the column is not numeric.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.standard_deviation()
        1.0
        """
        check_column_is_numeric(self, operation="calculate the standard deviation")

        return cast("float", self._series.std())

    def variance(self) -> float:
        """
        Return the variance of the values in the column.

        The variance is the sum of the squared differences from the mean divided by the number of values minus one.

        Returns
        -------
        variance:
            The variance of the values in the column.

        Raises
        ------
        ColumnTypeError
            If the column is not numeric.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.variance()
        1.0
        """
        check_column_is_numeric(self, operation="calculate the variance")

        return cast("float", self._series.var())

    def correlation_with(self, other: Column) -> float:
        """
        Calculate the Pearson correlation between this column and another column.

        The Pearson correlation is a value between -1 and 1 that indicates how much the two columns are **linearly**
        related:

        - A correlation of -1 indicates a perfect negative linear relationship.
        - A correlation of 0 indicates no linear relationship.
        - A correlation of 1 indicates a perfect positive linear relationship.

        A value of 0 does not necessarily mean that the columns are independent. It only means that there is no linear
        relationship between the columns.

        Parameters
        ----------
        other:
            The other column to calculate the correlation with.

        Returns
        -------
        correlation:
            The Pearson correlation between the two columns.

        Raises
        ------
        ColumnTypeError
            If one of the columns is not numeric.
        LengthMismatchError
            If the columns have different lengths.
        ColumnNullError
            If one of the columns has null values.

        Examples
        --------
        >>> from portabellas import Column
        >>> column1 = Column("a", [1, 2, 3])
        >>> column2 = Column("b", [2, 4, 6])
        >>> column1.correlation_with(column2)
        1.0

        >>> column3 = Column("c", [3, 2, 1])
        >>> column1.correlation_with(column3)
        -1.0
        """
        check_column_is_numeric(self, other_columns=[other], operation="calculate the correlation")
        check_row_counts_are_equal([self, other])
        check_column_has_no_nulls(self, other_columns=[other], operation="calculate the correlation")

        combined_frame = pl.concat(
            [
                self._lazy_frame.select(pl.col(self.name).alias("__left__")),
                other._lazy_frame.select(pl.col(other.name).alias("__right__")),
            ],
            how="horizontal",
        )
        correlation = pl.corr(pl.col("__left__"), pl.col("__right__"))
        result = safely_collect_lazy_frame(combined_frame.select(correlation))
        return cast("float", result.item())

    def distinct_value_count(
        self,
        *,
        ignore_nulls: bool = True,
    ) -> int:
        """
        Return the number of distinct values in the column.

        Parameters
        ----------
        ignore_nulls:
            Whether to ignore null values when counting distinct values.

        Returns
        -------
        distinct_value_count:
            The number of distinct values in the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3, 2, None])
        >>> column.distinct_value_count()
        3

        >>> column.distinct_value_count(ignore_nulls=False)
        4
        """
        if ignore_nulls:
            return self._series.drop_nulls().n_unique()
        return self._series.n_unique()

    def null_count(self) -> int:
        """
        Return the number of null values in the column.

        Returns
        -------
        null_count:
            The number of null values in the column.

        Examples
        --------
        >>> from portabellas import Column
        >>> column1 = Column("a", [1, 2, 3])
        >>> column1.null_count()
        0

        >>> column2 = Column("a", [1, None, 3])
        >>> column2.null_count()
        1
        """
        return self._series.null_count()

    def value_counts(self, *, ignore_nulls: bool = True) -> Table:
        """
        Return a table with the distinct values in this column and their counts.

        The result has two columns: the first has the same name and type as this
        column, and the second is named "count" with type UInt32. Results are
        sorted by count in descending order.

        Parameters
        ----------
        ignore_nulls:
            Whether to exclude null values from the result. Defaults to True.

        Returns
        -------
        table:
            A table with the distinct values and their counts.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 1])
        >>> column.value_counts()
        +-----+-------+
        |   a | count |
        | --- |   --- |
        | i64 |   u32 |
        +=============+
        |   1 |     2 |
        |   2 |     1 |
        +-----+-------+
        """
        from ._table import Table  # circular import  # noqa: PLC0415

        result = self._series.value_counts(sort=True, name="count")
        if ignore_nulls:
            result = result.filter(pl.col(self.name).is_not_null())
        return Table._from_polars_data_frame(result)

    def summarize_statistics(self) -> Table:
        """
        Return a table with important statistics about the column.

        !!! warning "API Stability"

            Do not rely on the exact output of this method. In future versions, we may change the displayed statistics
            without prior notice.

        Returns
        -------
        statistics:
            The table with statistics.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 3])
        >>> column.summarize_statistics()
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
        return self.to_table().summarize_statistics()

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

    def to_polars(self) -> pl.Series:
        """
        Return the internal Polars Series.

        Returns
        -------
        series:
            The Polars Series.

        Examples
        --------
        >>> import polars as pl
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, 3])
        >>> column.to_polars()
        shape: (3,)
        Series: 'a' [i64]
        [
            1
            2
            3
        ]
        """
        return self._series

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
        from ._table import Table  # circular import  # noqa: PLC0415

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

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _cross_check_type(lazy_frame: pl.LazyFrame, type: DataType) -> None:  # noqa: A002
        if "PYTEST_CURRENT_TEST" not in os.environ:
            return  # pragma: no cover

        schema = safely_collect_lazy_frame_schema(lazy_frame)
        polars_type = _from_polars_data_type(schema.dtypes()[0])
        if isinstance(polars_type, (DataTypes.Null, DataTypes.Unknown)):
            return

        assert polars_type == type, (  # noqa: S101
            f"Cached type {type} does not match Polars-inferred type {polars_type}"
        )
