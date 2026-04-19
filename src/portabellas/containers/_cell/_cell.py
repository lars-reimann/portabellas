from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime, time, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING

import polars as pl

if TYPE_CHECKING:
    from portabellas.typing import DataType

type _ConvertibleToCell = int | float | Decimal | date | time | datetime | timedelta | bool | str | bytes | Cell | None
type _ConvertibleToBooleanCell = bool | Cell | None


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
        >>> column.transform(lambda cell: cell < 2)
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
        from ._expr_cell import ExprCell  # noqa: PLC0415

        dtype = type._polars_data_type if type is not None else None

        return ExprCell(pl.lit(value, dtype=dtype))

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    # "Boolean" operators (actually bitwise) -----------------------------------

    @abstractmethod
    def __invert__(self) -> Cell[bool | None]: ...

    @abstractmethod
    def __and__(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __rand__(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __or__(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __ror__(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __xor__(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]: ...

    @abstractmethod
    def __rxor__(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]: ...

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
    def __add__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __radd__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __floordiv__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rfloordiv__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __mod__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rmod__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __mul__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rmul__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __pow__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rpow__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __sub__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rsub__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __truediv__(self, other: _ConvertibleToCell) -> Cell: ...

    @abstractmethod
    def __rtruediv__(self, other: _ConvertibleToCell) -> Cell: ...

    # Other --------------------------------------------------------------------

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
        >>> column.transform(lambda cell: cell.not_())
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.transform(lambda cell: ~cell)
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

    def and_(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]:
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
        >>> column.transform(lambda cell: cell.and_(True))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell & True)
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

    def or_(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]:
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
        >>> column.transform(lambda cell: cell.or_(False))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell | False)
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

    def xor(self, other: _ConvertibleToBooleanCell) -> Cell[bool | None]:
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
        >>> column.transform(lambda cell: cell.xor(True))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell ^ True)
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
        >>> column.transform(lambda cell: cell.neg())
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |   -1 |
        |    2 |
        | null |
        +------+

        >>> column.transform(lambda cell: -cell)
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

    def add(self, other: _ConvertibleToCell) -> Cell:
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
        >>> column.transform(lambda cell: cell.add(3))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    4 |
        |    5 |
        | null |
        +------+

        >>> column.transform(lambda cell: cell + 3)
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

    def div(self, other: _ConvertibleToCell) -> Cell:
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
        >>> column.transform(lambda cell: cell.div(2))
        +---------+
        |       a |
        |     --- |
        |     f64 |
        +=========+
        | 3.00000 |
        | 4.00000 |
        |    null |
        +---------+

        >>> column.transform(lambda cell: cell / 2)
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

    def mod(self, other: _ConvertibleToCell) -> Cell:
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
        >>> column.transform(lambda cell: cell.mod(3))
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

        >>> column.transform(lambda cell: cell % 3)
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

    def mul(self, other: _ConvertibleToCell) -> Cell:
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
        >>> column.transform(lambda cell: cell.mul(4))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    8 |
        |   12 |
        | null |
        +------+

        >>> column.transform(lambda cell: cell * 4)
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

    def pow(self, other: _ConvertibleToCell) -> Cell:
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
        >>> column.transform(lambda cell: cell.pow(3))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    8 |
        |   27 |
        | null |
        +------+

        >>> column.transform(lambda cell: cell ** 3)
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

    def sub(self, other: _ConvertibleToCell) -> Cell:
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
        >>> column.transform(lambda cell: cell.sub(3))
        +------+
        |    a |
        |  --- |
        |  i64 |
        +======+
        |    2 |
        |    3 |
        | null |
        +------+

        >>> column.transform(lambda cell: cell - 3)
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
        >>> column.transform(lambda cell: cell.eq(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell == 2)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell.eq(2, propagate_missing_values=False))
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
        >>> column.transform(lambda cell: cell.neq(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell != 2)
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell.neq(2, propagate_missing_values=False))
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
        >>> column.transform(lambda cell: cell.ge(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | true  |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell >= 2)
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
        >>> column.transform(lambda cell: cell.gt(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | false |
        | false |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell > 2)
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
        >>> column.transform(lambda cell: cell.le(2))
        +------+
        | a    |
        | ---  |
        | bool |
        +======+
        | true |
        | true |
        | null |
        +------+

        >>> column.transform(lambda cell: cell <= 2)
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
        >>> column.transform(lambda cell: cell.lt(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        | null  |
        +-------+

        >>> column.transform(lambda cell: cell < 2)
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
        >>> column.transform(lambda cell: cell.cast(DataType.String()))
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
