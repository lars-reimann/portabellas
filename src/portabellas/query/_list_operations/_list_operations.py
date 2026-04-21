from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portabellas.containers import Cell
    from portabellas.containers._cell import ConvertibleToIntCell, ConvertibleToStringCell


class ListOperations(ABC):
    """
    Namespace for operations on lists.

    This class cannot be instantiated directly. It can only be accessed using the `list` attribute of a cell.
    """

    @abstractmethod
    def contains(self, item: ConvertibleToIntCell) -> Cell[bool | None]:
        """
        Check if the list contains the given item.

        Parameters
        ----------
        item:
            The item to search for.

        Returns
        -------
        cell:
            Whether the list contains the item.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5, 6]])
        >>> column.map(lambda cell: cell.list.contains(2))
        +-------+
        | a     |
        | ---   |
        | bool  |
        +=======+
        | true  |
        | false |
        +-------+
        """

    @abstractmethod
    def first(self) -> Cell:
        """
        Get the first value of the list.

        Returns
        -------
        cell:
            The first value of the list.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5, 6]])
        >>> column.map(lambda cell: cell.list.first())
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   1 |
        |   4 |
        +-----+
        """

    @abstractmethod
    def get(self, index: ConvertibleToIntCell) -> Cell:
        """
        Get the value at the specified index in the list.

        Parameters
        ----------
        index:
            The index of the value to get. If the index is out of bounds, the result is null.

        Returns
        -------
        cell:
            The value at the given index.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5, 6]])
        >>> column.map(lambda cell: cell.list.get(1))
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   2 |
        |   5 |
        +-----+
        """

    @abstractmethod
    def join(self, separator: ConvertibleToStringCell) -> Cell[str | None]:
        """
        Join all elements in the list into a string, separated by the given separator.

        Parameters
        ----------
        separator:
            The separator to place between elements.

        Returns
        -------
        cell:
            The joined string.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [["a", "b", "c"], ["x", "y"]])
        >>> column.map(lambda cell: cell.list.join("-"))
        +-------+
        | a     |
        | ---   |
        | str   |
        +=======+
        | a-b-c |
        | x-y   |
        +-------+
        """

    @abstractmethod
    def last(self) -> Cell:
        """
        Get the last value of the list.

        Returns
        -------
        cell:
            The last value of the list.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5, 6]])
        >>> column.map(lambda cell: cell.list.last())
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   3 |
        |   6 |
        +-----+
        """

    @abstractmethod
    def length(self) -> Cell[int | None]:
        """
        Get the number of elements in the list.

        Returns
        -------
        cell:
            The number of elements in the list.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5]])
        >>> column.map(lambda cell: cell.list.length())
        +-----+
        |   a |
        | --- |
        | u32 |
        +=====+
        |   3 |
        |   2 |
        +-----+
        """

    @abstractmethod
    def max(self) -> Cell:
        """
        Get the maximum value in the list.

        Returns
        -------
        cell:
            The maximum value in the list.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5, 6]])
        >>> column.map(lambda cell: cell.list.max())
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   3 |
        |   6 |
        +-----+
        """

    @abstractmethod
    def min(self) -> Cell:
        """
        Get the minimum value in the list.

        Returns
        -------
        cell:
            The minimum value in the list.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5, 6]])
        >>> column.map(lambda cell: cell.list.min())
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   1 |
        |   4 |
        +-----+
        """

    @abstractmethod
    def reverse(self) -> Cell:
        """
        Reverse the list.

        Returns
        -------
        cell:
            The reversed list.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5, 6]])
        >>> column.map(lambda cell: cell.list.reverse())
        +-----------+
        | a         |
        | ---       |
        | list[i64] |
        +===========+
        | [3, 2, 1] |
        | [6, 5, 4] |
        +-----------+
        """

    @abstractmethod
    def sort(self, *, descending: bool = False) -> Cell:
        """
        Sort the list.

        Parameters
        ----------
        descending:
            Whether to sort in descending order.

        Returns
        -------
        cell:
            The sorted list.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[3, 1, 2], [6, 4, 5]])
        >>> column.map(lambda cell: cell.list.sort())
        +-----------+
        | a         |
        | ---       |
        | list[i64] |
        +===========+
        | [1, 2, 3] |
        | [4, 5, 6] |
        +-----------+
        """

    @abstractmethod
    def sum(self) -> Cell:
        """
        Sum all values in the list.

        Returns
        -------
        cell:
            The sum of all values in the list.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [[1, 2, 3], [4, 5, 6]])
        >>> column.map(lambda cell: cell.list.sum())
        +-----+
        |   a |
        | --- |
        | i64 |
        +=====+
        |   6 |
        |  15 |
        +-----+
        """
