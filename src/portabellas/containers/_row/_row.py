from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from portabellas.containers._cell import Cell


class Row(ABC):
    """
    A one-dimensional collection of named, heterogeneous values.

    You only need to interact with this class in callbacks passed to higher-order functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------------------------------------------------------

    def __getitem__(self, name: str) -> Cell:
        return self.get_cell(name)

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
