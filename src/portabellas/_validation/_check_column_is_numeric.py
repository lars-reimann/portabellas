from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.exceptions import NonNumericColumnError

if TYPE_CHECKING:
    from portabellas.containers import Column


def check_column_is_numeric(
    column: Column,
    *,
    operation: str = "do a numeric operation",
) -> None:
    """
    Check whether a column is numeric, and raise an error if it is not.

    Parameters
    ----------
    column:
        The column to check.
    operation:
        The operation that is performed on the column. This is used in the error message.

    Raises
    ------
    NonNumericColumnError
        If the column is not numeric.
    """
    if not column.type.is_numeric:
        raise NonNumericColumnError([column.name], operation=operation) from None
