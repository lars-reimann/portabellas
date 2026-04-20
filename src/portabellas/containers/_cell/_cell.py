from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

import polars as pl

from portabellas._validation import check_time_zone

if TYPE_CHECKING:
    from portabellas.query import DatetimeOperations, DurationOperations, MathOperations, StringOperations
    from portabellas.typing import DataType

type ConvertibleToCell = int | float | Decimal | date | time | datetime | timedelta | bool | str | bytes | Cell | None
type ConvertibleToBooleanCell = bool | Cell | None
type ConvertibleToIntCell = int | Cell | None
type ConvertibleToStringCell = str | Cell | None


class Cell[T_co](ABC):
    """
    A single value in a table.

    You only need to interact with this class in callbacks passed to higher-order functions. Most operations are grouped
    into namespaces, which are accessed through the following attributes:

    - `dt`: Operations on datetime/date/time values
    - `dur`: Operations on durations
    - `math`: Mathematical operations on numbers
    - `str`: Operations on strings

    This class only has methods that are not specific to a data type (e.g. `cast`), methods with corresponding
    operators (e.g. `add` for `+`), and static methods to create new cells.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Static methods
    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def constant(value: object, *, type: DataType | None = None) -> Cell:  # noqa: A002
        """
        Create a cell with a constant value.

        Parameters
        ----------
        value:
            The value to create the cell from.
        type:
            The type of the cell. If None, the type is inferred from the value.

        Returns
        -------
        cell:
            The created cell.

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
        dtype = type._polars_data_type if type is not None else None

        return _expr_cell(pl.lit(value, dtype=dtype))

    @staticmethod
    def date(
        year: ConvertibleToIntCell,
        month: ConvertibleToIntCell,
        day: ConvertibleToIntCell,
    ) -> Cell[date | None]:
        """
        Create a cell with a date.

        Invalid dates are converted to missing values (`None`).

        Parameters
        ----------
        year:
            The year.
        month:
            The month. Must be between 1 and 12.
        day:
            The day. Must be between 1 and 31.

        Returns
        -------
        cell:
            The created cell.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda _: Cell.date(2025, 1, 15))
        +------------+
        | a          |
        | ---        |
        | date       |
        +============+
        | 2025-01-15 |
        | 2025-01-15 |
        | 2025-01-15 |
        +------------+

        >>> column.map(lambda cell: Cell.date(2025, cell, 15))
        +------------+
        | a          |
        | ---        |
        | date       |
        +============+
        | 2025-01-15 |
        | 2025-02-15 |
        | null       |
        +------------+
        """
        return _expr_cell(
            pl.date(
                year=_to_polars_expression(year),
                month=_to_polars_expression(month),
                day=_to_polars_expression(day),
            ),
        )

    @staticmethod
    def datetime(
        year: ConvertibleToIntCell,
        month: ConvertibleToIntCell,
        day: ConvertibleToIntCell,
        hour: ConvertibleToIntCell,
        minute: ConvertibleToIntCell,
        second: ConvertibleToIntCell,
        *,
        microsecond: ConvertibleToIntCell = 0,
        time_zone: str | None = None,
    ) -> Cell[datetime | None]:
        """
        Create a cell with a datetime.

        Invalid datetimes are converted to missing values (`None`).

        Parameters
        ----------
        year:
            The year.
        month:
            The month. Must be between 1 and 12.
        day:
            The day. Must be between 1 and 31.
        hour:
            The hour. Must be between 0 and 23.
        minute:
            The minute. Must be between 0 and 59.
        second:
            The second. Must be between 0 and 59.
        microsecond:
            The microsecond. Must be between 0 and 999,999.
        time_zone:
            The time zone. If None, values are assumed to be in local time. This is different from setting the time zone
            to `"UTC"`. Any TZ identifier defined in the
            [tz database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) is valid.

        Returns
        -------
        cell:
            The created cell.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda _: Cell.datetime(2025, 1, 15, 12, 0, 0))
        +---------------------+
        | a                   |
        | ---                 |
        | datetime[μs]        |
        +=====================+
        | 2025-01-15 12:00:00 |
        | 2025-01-15 12:00:00 |
        | 2025-01-15 12:00:00 |
        +---------------------+

        >>> column.map(lambda cell: Cell.datetime(2025, 1, 15, cell, 0, 0))
        +---------------------+
        | a                   |
        | ---                 |
        | datetime[μs]        |
        +=====================+
        | 2025-01-15 01:00:00 |
        | 2025-01-15 02:00:00 |
        | null                |
        +---------------------+
        """
        check_time_zone(time_zone)

        pl_year = _to_polars_expression(year)
        pl_month = _to_polars_expression(month)
        pl_day = _to_polars_expression(day)
        pl_hour = _to_polars_expression(hour)
        pl_minute = _to_polars_expression(minute)
        pl_second = _to_polars_expression(second)
        pl_microsecond = _to_polars_expression(microsecond)

        # https://github.com/pola-rs/polars/issues/21664
        return _expr_cell(
            pl.when(pl_microsecond <= 999_999)
            .then(
                pl.datetime(
                    pl_year,
                    pl_month,
                    pl_day,
                    pl_hour,
                    pl_minute,
                    pl_second,
                    pl_microsecond,
                    time_zone=time_zone,
                ),
            )
            .otherwise(None),
        )

    @staticmethod
    def duration(
        *,
        weeks: ConvertibleToIntCell = 0,
        days: ConvertibleToIntCell = 0,
        hours: ConvertibleToIntCell = 0,
        minutes: ConvertibleToIntCell = 0,
        seconds: ConvertibleToIntCell = 0,
        milliseconds: ConvertibleToIntCell = 0,
        microseconds: ConvertibleToIntCell = 0,
    ) -> Cell[timedelta | None]:
        """
        Create a cell with a duration.

        Invalid durations are converted to missing values (`None`).

        Parameters
        ----------
        weeks:
            The number of weeks.
        days:
            The number of days.
        hours:
            The number of hours.
        minutes:
            The number of minutes.
        seconds:
            The number of seconds.
        milliseconds:
            The number of milliseconds.
        microseconds:
            The number of microseconds.

        Returns
        -------
        cell:
            The created cell.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda _: Cell.duration(hours=1))
        +--------------+
        | a            |
        | ---          |
        | duration[μs] |
        +==============+
        | 1h           |
        | 1h           |
        | 1h           |
        +--------------+

        >>> column.map(lambda cell: Cell.duration(hours=cell))
        +--------------+
        | a            |
        | ---          |
        | duration[μs] |
        +==============+
        | 1h           |
        | 2h           |
        | null         |
        +--------------+
        """

        # pl.duration raises for null-typed expressions
        def _to_int_expression(value: ConvertibleToIntCell) -> pl.Expr:
            expr = _to_polars_expression(value)
            if value is None:
                expr = expr.cast(pl.Int32)
            return expr

        return _expr_cell(
            pl.duration(
                weeks=_to_int_expression(weeks),
                days=_to_int_expression(days),
                hours=_to_int_expression(hours),
                minutes=_to_int_expression(minutes),
                seconds=_to_int_expression(seconds),
                milliseconds=_to_int_expression(milliseconds),
                microseconds=_to_int_expression(microseconds),
            ),
        )

    @staticmethod
    def time(
        hour: ConvertibleToIntCell,
        minute: ConvertibleToIntCell,
        second: ConvertibleToIntCell,
        *,
        microsecond: ConvertibleToIntCell = 0,
    ) -> Cell[time | None]:
        """
        Create a cell with a time.

        Invalid times are converted to missing values (`None`).

        Parameters
        ----------
        hour:
            The hour. Must be between 0 and 23.
        minute:
            The minute. Must be between 0 and 59.
        second:
            The second. Must be between 0 and 59.
        microsecond:
            The microsecond. Must be between 0 and 999,999.

        Returns
        -------
        cell:
            The created cell.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda _: Cell.time(12, 0, 0))
        +----------+
        | a        |
        | ---      |
        | time     |
        +==========+
        | 12:00:00 |
        | 12:00:00 |
        | 12:00:00 |
        +----------+

        >>> column.map(lambda cell: Cell.time(12, cell, 0, microsecond=1))
        +-----------------+
        | a               |
        | ---             |
        | time            |
        +=================+
        | 12:01:00.000001 |
        | 12:02:00.000001 |
        | null            |
        +-----------------+
        """
        pl_hour = _to_polars_expression(hour)
        pl_minute = _to_polars_expression(minute)
        pl_second = _to_polars_expression(second)
        pl_microsecond = _to_polars_expression(microsecond)

        # https://github.com/pola-rs/polars/issues/21664
        return _expr_cell(
            pl.when(pl_microsecond <= 999_999)
            .then(pl.time(pl_hour, pl_minute, pl_second, pl_microsecond))
            .otherwise(None),
        )

    @staticmethod
    def first_not_none[P](cells: list[Cell[P]]) -> Cell[P | None]:
        """
        Return the first cell that is not None or None if all cells are None.

        Parameters
        ----------
        cells:
            The list of cells to be checked.

        Returns
        -------
        cell:
            The first cell that is not None or None if all cells are None.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda _: Cell.first_not_none([Cell.constant(None), Cell.constant(1)]))
        +-----+
        |   a |
        | --- |
        | i32 |
        +=====+
        |   1 |
        |   1 |
        |   1 |
        +-----+
        """
        if not cells:
            return Cell.constant(None)

        return _expr_cell(pl.coalesce([_to_polars_expression(cell) for cell in cells]))

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    # "Boolean" operators (actually bitwise) -----------------------------------

    @abstractmethod
    def __invert__(self) -> Cell[bool | None]: ...

    @abstractmethod
    def __and__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __rand__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __or__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __ror__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __xor__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __rxor__(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    # Comparison ---------------------------------------------------------------

    @abstractmethod
    def __eq__(self, other: object) -> Cell[bool | None]:  # type: ignore[override]
        ...

    @abstractmethod
    def __ne__(self, other: object) -> Cell[bool | None]:  # type: ignore[override]
        ...

    @abstractmethod
    def __ge__(self, other: object) -> Cell[bool | None]: ...

    @abstractmethod
    def __gt__(self, other: object) -> Cell[bool | None]: ...

    @abstractmethod
    def __le__(self, other: object) -> Cell[bool | None]: ...

    @abstractmethod
    def __lt__(self, other: object) -> Cell[bool | None]: ...

    # Numeric operators --------------------------------------------------------

    @abstractmethod
    def __abs__(self) -> Cell: ...

    @abstractmethod
    def __ceil__(self) -> Cell: ...

    @abstractmethod
    def __floor__(self) -> Cell: ...

    @abstractmethod
    def __neg__(self) -> Cell: ...

    @abstractmethod
    def __pos__(self) -> Cell: ...

    @abstractmethod
    def __add__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __radd__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __floordiv__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rfloordiv__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __mod__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rmod__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __mul__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rmul__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __pow__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rpow__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __sub__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rsub__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __truediv__(self, other: ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rtruediv__(self, other: ConvertibleToCell) -> Cell: ...

    # Other --------------------------------------------------------------------

    # __eq__ does not follow the standard contract, so hashing must be disabled
    __hash__ = None  # type: ignore[assignment]

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...

    # ------------------------------------------------------------------------------------------------------------------
    # Boolean operations
    # ------------------------------------------------------------------------------------------------------------------

    def not_(self) -> Cell[bool | None]:
        """
        Negate a Boolean. This is equivalent to the `~` operator.

        Do **not** use the `not` operator. Its behavior cannot be overwritten in Python, so it will not work as
        expected.

        Returns
        -------
        cell:
            The result of the Boolean negation.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [True, False, None])
        >>> column.map(lambda cell: cell.not_())
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.map(lambda cell: ~cell)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+
        """
        return self.__invert__()

    def and_(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        """
        Perform a Boolean AND operation. This is equivalent to the `&` operator.

        Do **not** use the `and` operator. Its behavior cannot be overwritten in Python, so it will not work as
        expected.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the conjunction.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [True, False, None])
        >>> column.map(lambda cell: cell.and_(True))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell & True)
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
        return self.__and__(other)

    def or_(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        """
        Perform a Boolean OR operation. This is equivalent to the `|` operator.

        Do **not** use the `or` operator. Its behavior cannot be overwritten in Python, so it will not work as expected.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the disjunction.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [True, False, None])
        >>> column.map(lambda cell: cell.or_(False))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell | False)
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
        return self.__or__(other)

    def xor(self, other: ConvertibleToBooleanCell) -> Cell[bool | None]:
        """
        Perform a Boolean XOR operation. This is equivalent to the `^` operator.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the exclusive or.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [True, False, None])
        >>> column.map(lambda cell: cell.xor(True))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell ^ True)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+
        """
        return self.__xor__(other)

    # ------------------------------------------------------------------------------------------------------------------
    # Numeric operations
    # ------------------------------------------------------------------------------------------------------------------

    def neg(self) -> Cell:
        """
        Negate the value. This is equivalent to the unary `-` operator.

        Returns
        -------
        cell:
            The negated value.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, -2, None])
        >>> column.map(lambda cell: cell.neg())
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |   -1 |
        |    2 |
        | null |
        +------+

        >>> column.map(lambda cell: -cell)
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |   -1 |
        |    2 |
        | null |
        +------+
        """
        return self.__neg__()

    def add(self, other: ConvertibleToCell) -> Cell:
        """
        Add a value. This is equivalent to the `+` operator.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the addition.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell.add(3))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    4 |
        |    5 |
        | null |
        +------+

        >>> column.map(lambda cell: cell + 3)
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    4 |
        |    5 |
        | null |
        +------+
        """
        return self.__add__(other)

    def div(self, other: ConvertibleToCell) -> Cell:
        """
        Divide by a value. This is equivalent to the `/` operator.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the division.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [6, 8, None])
        >>> column.map(lambda cell: cell.div(2))
        +---------+
        |       a |
        |     --- |
        |     f64 |
        +=========+
        | 3.00000 |
        | 4.00000 |
        |    null |
        +---------+

        >>> column.map(lambda cell: cell / 2)
        +---------+
        |       a |
        |     --- |
        |     f64 |
        +=========+
        | 3.00000 |
        | 4.00000 |
        |    null |
        +---------+
        """
        return self.__truediv__(other)

    def mod(self, other: ConvertibleToCell) -> Cell:
        """
        Perform a modulo operation. This is equivalent to the `%` operator.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the modulo operation.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [5, 6, -1, None])
        >>> column.map(lambda cell: cell.mod(3))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    2 |
        |    0 |
        |    2 |
        | null |
        +------+

        >>> column.map(lambda cell: cell % 3)
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    2 |
        |    0 |
        |    2 |
        | null |
        +------+
        """
        return self.__mod__(other)

    def mul(self, other: ConvertibleToCell) -> Cell:
        """
        Multiply by a value. This is equivalent to the `*` operator.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the multiplication.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [2, 3, None])
        >>> column.map(lambda cell: cell.mul(4))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    8 |
        |   12 |
        | null |
        +------+

        >>> column.map(lambda cell: cell * 4)
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    8 |
        |   12 |
        | null |
        +------+
        """
        return self.__mul__(other)

    def pow(self, other: ConvertibleToCell) -> Cell:
        """
        Raise to a power. This is equivalent to the `**` operator.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the exponentiation.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [2, 3, None])
        >>> column.map(lambda cell: cell.pow(3))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    8 |
        |   27 |
        | null |
        +------+

        >>> column.map(lambda cell: cell ** 3)
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    8 |
        |   27 |
        | null |
        +------+
        """
        return self.__pow__(other)

    def sub(self, other: ConvertibleToCell) -> Cell:
        """
        Subtract a value. This is equivalent to the binary `-` operator.

        Parameters
        ----------
        other:
            The right operand.

        Returns
        -------
        cell:
            The result of the subtraction.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [5, 6, None])
        >>> column.map(lambda cell: cell.sub(3))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    2 |
        |    3 |
        | null |
        +------+

        >>> column.map(lambda cell: cell - 3)
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    2 |
        |    3 |
        | null |
        +------+
        """
        return self.__sub__(other)

    # ------------------------------------------------------------------------------------------------------------------
    # Comparison operations
    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def eq(
        self,
        other: object,
        *,
        propagate_missing_values: bool = True,
    ) -> Cell[bool | None]:
        """
        Check if equal to a value. The default behavior is equivalent to the `==` operator.

        Missing values (indicated by `None`) are handled as follows:

        - If `propagate_missing_values` is `True` (default), the result will be a missing value if either the cell or
          the other value is a missing value. Here, `None == None` is `None`. The intuition is that we do not know the
          result of the comparison if we do not know the values, which is consistent with the other cell operations.
        - If `propagate_missing_values` is `False`, `None` will be treated as a regular value. Here, `None == None`
          is `True`. This behavior is useful, if you want to work with missing values, e.g. to filter them out.

        Parameters
        ----------
        other:
            The value to compare to.
        propagate_missing_values:
            Whether to propagate missing values.

        Returns
        -------
        cell:
            The result of the comparison.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell.eq(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell == 2)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell.eq(2, propagate_missing_values=False))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | false |
        +-------+
        """

    @abstractmethod
    def neq(
        self,
        other: object,
        *,
        propagate_missing_values: bool = True,
    ) -> Cell[bool | None]:
        """
        Check if not equal to a value. The default behavior is equivalent to the `!=` operator.

        Missing values (indicated by `None`) are handled as follows:

        - If `propagate_missing_values` is `True` (default), the result will be a missing value if either the cell or
          the other value is a missing value. Here, `None != None` is `None`. The intuition is that we do not know the
          result of the comparison if we do not know the values, which is consistent with the other cell operations.
        - If `propagate_missing_values` is `False`, `None` will be treated as a regular value. Here, `None != None`
          is `False`. This behavior is useful, if you want to work with missing values, e.g. to filter them out.

        Parameters
        ----------
        other:
            The value to compare to.
        propagate_missing_values:
            Whether to propagate missing values.

        Returns
        -------
        cell:
            The result of the comparison.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell.neq(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell != 2)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell.neq(2, propagate_missing_values=False))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | true  |
        +-------+
        """

    def ge(self, other: object) -> Cell[bool | None]:
        """
        Check if greater than or equal to a value. This is equivalent to the `>=` operator.

        Parameters
        ----------
        other:
            The value to compare to.

        Returns
        -------
        cell:
            The result of the comparison.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell.ge(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell >= 2)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+
        """
        return self.__ge__(other)

    def gt(self, other: object) -> Cell[bool | None]:
        """
        Check if greater than a value. This is equivalent to the `>` operator.

        Parameters
        ----------
        other:
            The value to compare to.

        Returns
        -------
        cell:
            The result of the comparison.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell.gt(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | false |
        | null  |
        +-------+

        >>> column.map(lambda cell: cell > 2)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | false |
        | null  |
        +-------+
        """
        return self.__gt__(other)

    def le(self, other: object) -> Cell[bool | None]:
        """
        Check if less than or equal to a value. This is equivalent to the `<=` operator.

        Parameters
        ----------
        other:
            The value to compare to.

        Returns
        -------
        cell:
            The result of the comparison.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell.le(2))
        +------+
        | a    |
        | ---  |
        | bool |
        +======+
        | true |
        | true |
        | null |
        +------+

        >>> column.map(lambda cell: cell <= 2)
        +------+
        | a    |
        | ---  |
        | bool |
        +======+
        | true |
        | true |
        | null |
        +------+
        """
        return self.__le__(other)

    def lt(self, other: object) -> Cell[bool | None]:
        """
        Check if less than a value. This is equivalent to the `<` operator.

        Parameters
        ----------
        other:
            The value to compare to.

        Returns
        -------
        cell:
            The result of the comparison.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell.lt(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

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
        return self.__lt__(other)

    # ------------------------------------------------------------------------------------------------------------------
    # Properties (namespaces)
    # ------------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def dt(self) -> DatetimeOperations:
        """
        Namespace for operations on datetime/date/time values.

        Examples
        --------
        >>> from datetime import datetime
        >>> from portabellas import Column
        >>> column = Column("a", [datetime(2025, 1, 1), datetime(2024, 1, 1)])
        >>> column.map(lambda cell: cell.dt.year())
        +------+
        |    a |
        |  --- |
        |  i32 |
        +======+
        | 2025 |
        | 2024 |
        +------+
        """

    @property
    @abstractmethod
    def dur(self) -> DurationOperations:
        """
        Namespace for operations on durations.

        Examples
        --------
        >>> from datetime import timedelta
        >>> from portabellas import Column
        >>> column = Column("a", [timedelta(hours=1), timedelta(hours=2)])
        >>> column.map(lambda cell: cell.dur.full_hours())
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   1 |
        |   2 |
        +-----+
        """

    @property
    @abstractmethod
    def math(self) -> MathOperations:
        """
        Namespace for mathematical operations.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [1, -2])
        >>> column.map(lambda cell: cell.math.abs())
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   1 |
        |   2 |
        +-----+
        """

    @property
    @abstractmethod
    def str(self) -> StringOperations:
        """
        Namespace for operations on strings.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", ["hi", "hello"])
        >>> column.map(lambda cell: cell.str.length())
        +-----+
        |   a |
        | --- |
        | u32 |
        +=====+
        |   2 |
        |   5 |
        +-----+
        """

    # ------------------------------------------------------------------------------------------------------------------
    # Other
    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def cast(self, type: DataType) -> Cell:  # noqa: A002
        """
        Cast the cell to a different type.

        Parameters
        ----------
        type:
            The type to cast to.

        Returns
        -------
        cell:
            The cast cell.

        Examples
        --------
        >>> from portabellas import Column
        >>> from portabellas.typing import DataType
        >>> column = Column("a", [1, 2, None])
        >>> column.map(lambda cell: cell.cast(DataType.String()))
        +------+
        | a    |
        | ---  |
        | str  |
        +======+
        | 1    |
        | 2    |
        | null |
        +------+
        """

    # ------------------------------------------------------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def _polars_expression(self) -> pl.Expr:
        """The polars expression that corresponds to this cell."""


def _to_polars_expression(cell_proxy: object) -> pl.Expr:
    """
    Convert a cell proxy to a polars expression.

    Parameters
    ----------
    cell_proxy:
        The cell proxy to convert.

    Returns
    -------
    expression:
        The polars expression.
    """
    if isinstance(cell_proxy, Cell):
        return cell_proxy._polars_expression

    return pl.lit(cell_proxy)


def _expr_cell(expression: pl.Expr) -> Cell:
    from ._expr_cell import ExprCell  # circular import

    return ExprCell(expression)
