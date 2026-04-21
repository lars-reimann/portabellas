from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portabellas.containers import Cell


class StructOperations(ABC):
    """
    Namespace for operations on structs.

    This class cannot be instantiated directly. It can only be accessed using the `struct` attribute of a cell.

    Examples
    --------
    >>> from portabellas import Column
    >>> column = Column("a", [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}])
    >>> column.map(lambda cell: cell.struct.field("name"))
    +-------+
    | a     |
    | ---   |
    | str   |
    +=======+
    | Alice |
    | Bob   |
    +-------+
    """

    @abstractmethod
    def field(self, name: str) -> Cell:
        """
        Get a field of the struct by name.

        Parameters
        ----------
        name:
            The name of the field.

        Returns
        -------
        cell:
            The field value.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}])
        >>> column.map(lambda cell: cell.struct.field("name"))
        +-------+
        | a     |
        | ---   |
        | str   |
        +=======+
        | Alice |
        | Bob   |
        +-------+
        """

    @abstractmethod
    def rename(self, old_name: str, new_name: str) -> Cell:
        """
        Rename a field of the struct.

        Parameters
        ----------
        old_name:
            The current name of the field.
        new_name:
            The new name of the field.

        Returns
        -------
        cell:
            The struct with the renamed field.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}])
        >>> column.map(lambda cell: cell.struct.rename("name", "first_name"))
        +--------------+
        | a            |
        | ---          |
        | struct[2]    |
        +==============+
        | {"Alice",25} |
        | {"Bob",30}   |
        +--------------+
        """

    @abstractmethod
    def to_json(self) -> Cell[str | None]:
        """
        Convert the struct to a JSON string.

        Returns
        -------
        cell:
            The JSON string representation of the struct.

        Examples
        --------
        >>> from portabellas import Column
        >>> column = Column("a", [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}])
        >>> column.map(lambda cell: cell.struct.to_json())
        +---------------------------+
        | a                         |
        | ---                       |
        | str                       |
        +===========================+
        | {"name":"Alice","age":25} |
        | {"name":"Bob","age":30}   |
        +---------------------------+
        """
