from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import polars as pl

if TYPE_CHECKING:
    from portabellas.typing import DataType


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

    # Other --------------------------------------------------------------------

    __hash__ = None  # type: ignore[assignment]

    @abstractmethod
    def __repr__(self) -> str: ...

    @abstractmethod
    def __str__(self) -> str: ...

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
