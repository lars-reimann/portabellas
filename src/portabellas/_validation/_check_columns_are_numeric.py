"""The module name must differ from the function name, so it can be re-exported properly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.exceptions import ColumnTypeError

if TYPE_CHECKING:
    from collections.abc import Container

    from portabellas.containers import Table
    from portabellas.typing import Schema


def check_columns_are_numeric(
    table_or_schema: Table | Schema,
    selector: str | list[str],
    *,
    operation: str = "do a numeric operation",
) -> None:
    """
    Check whether the specified columns are numeric, and raise an error if any are not. Missing columns are ignored.

    Parameters
    ----------
    table_or_schema:
        The table or schema to check.
    selector:
        The columns to check.
    operation:
        The operation that is performed on the columns. This is used in the error message.

    Raises
    ------
    ColumnTypeError
        If a column exists but is not numeric.
    """
    from portabellas.containers import Table  # circular import  # noqa: PLC0415

    if isinstance(table_or_schema, Table):
        table_or_schema = table_or_schema.schema
    if isinstance(selector, str):
        selector = [selector]

    if len(selector) > 1:
        known_names: Container = set(table_or_schema.column_names)
    else:
        known_names = table_or_schema.column_names

    non_numeric_names = [
        name for name in selector if name in known_names and not table_or_schema.get_column_type(name).is_numeric
    ]
    if non_numeric_names:
        message = _build_error_message(non_numeric_names, operation)
        raise ColumnTypeError(message) from None


def _build_error_message(non_numeric_names: list[str], operation: str) -> str:
    return f"Tried to {operation} on non-numeric columns {non_numeric_names}."
