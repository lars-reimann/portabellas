from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.exceptions import MissingValuesColumnError

if TYPE_CHECKING:
    from portabellas.containers import Column


def check_column_has_no_missing_values(
    column: Column,
    *,
    other_columns: list[Column] | None = None,
    operation: str = "do an operation",
) -> None:
    """
    Check whether columns have no missing values, and raise an error if any do.

    Parameters
    ----------
    column:
        The column to check.
    other_columns:
        Other columns to check. This provides better error messages than checking each column individually.
    operation:
        The operation that is performed on the column. This is used in the error message.

    Raises
    ------
    MissingValuesColumnError
        If a column has missing values.
    """
    if other_columns is None:
        other_columns = []

    columns = [column, *other_columns]
    missing_values_names = [col.name for col in columns if col._series.has_nulls()]

    if missing_values_names:
        msg = f"Tried to {operation} on columns with missing values {missing_values_names}."
        raise MissingValuesColumnError(msg) from None
