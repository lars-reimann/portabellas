from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from portabellas.containers._cell import Cell
    from portabellas.typing import DataType, Schema


class Row(ABC):
    """
    A one-dimensional collection of named, heterogeneous values.

    You only need to interact with this class in callbacks passed to higher-order functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __contains__(self, key: object, /) -> bool:
        if not isinstance(key, str):
            return False
        return self.has_column(key)

    def __getitem__(self, name: str) -> Cell:
        return self.get_cell(name)

    def __iter__(self) -> Iterator[str]:
        return iter(self.column_names)

    def __len__(self) -> int:
        return self.column_count

    # ------------------------------------------------------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------------------------------------------------------

    @property
    @abstractmethod
    def column_count(self) -> int:
        """The number of columns."""

    @property
    @abstractmethod
    def column_names(self) -> list[str]:
        """The names of the columns."""

    @property
    @abstractmethod
    def schema(self) -> Schema:
        """The schema of the row, which is a mapping from column names to their types."""

    # ------------------------------------------------------------------------------------------------------------------
    # Column operations
    # ------------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def get_cell(self, name: str) -> Cell:
        """
        Get the cell in the specified column. This is equivalent to the `[]` operator (indexed access).

        Parameters
        ----------
        name:
            The name of the column.

        Returns
        -------
        cell:
            The cell in the specified column.

        Raises
        ------
        ColumnNotFoundError
            If the column name does not exist.

        Examples
        --------
        >>> from portabellas import Table
        >>> table = Table({"col1": [1, 2], "col2": [3, 4]})
        >>> table.add_computed_column("col3", lambda row: row.get_cell("col1") + 1)
        +------+------+------+
        | col1 | col2 | col3 |
        | ---  | ---  | ---  |
        | i64  | i64  | i64  |
        +=====================+
        |    1 |    3 |    2 |
        |    2 |    4 |    3 |
        +------+------+------+

        >>> table.add_computed_column("col3", lambda row: row["col1"] + 1)
        +------+------+------+
        | col1 | col2 | col3 |
        | ---  | ---  | ---  |
        | i64  | i64  | i64  |
        +=====================+
        |    1 |    3 |    2 |
        |    2 |    4 |    3 |
        +------+------+------+
        """

    @abstractmethod
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
        """

    @abstractmethod
    def has_column(self, name: str) -> bool:
        """
        Check if the row has a column with a specific name. This is equivalent to the `in` operator.

        Parameters
        ----------
        name:
            The name of the column.

        Returns
        -------
        has_column:
            Whether the row has a column with the specified name.
        """
