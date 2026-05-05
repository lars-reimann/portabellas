"""The module name must differ from the function name, so it can be re-exported properly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas._utils import compute_duplicates
from portabellas._validation._check_columns_exist import check_columns_exist
from portabellas.exceptions import DuplicateColumnError

if TYPE_CHECKING:
    from portabellas.containers import Table
    from portabellas.typing import Schema


def check_columns_are_permutation(
    table_or_schema: Table | Schema,
    column_names: list[str],
) -> None:
    """
    Check whether the given column names are a permutation of the table's column names, and raise an error if not.

    This checks three conditions:

    1. No duplicate column names.
    2. No unknown column names (names not in the table).
    3. No missing column names (columns in the table but not in the list).

    Parameters
    ----------
    table_or_schema:
        The table or schema to check against.
    column_names:
        The column names to validate.

    Raises
    ------
    ColumnNotFoundError
        If a column name does not exist in the table.
    DuplicateColumnError
        If a column name appears more than once.
    ValueError
        If a table column is missing from the list.
    """
    from portabellas.containers import Table  # circular import  # noqa: PLC0415

    if isinstance(table_or_schema, Table):
        table_or_schema = table_or_schema.schema

    duplicate_names = compute_duplicates(column_names)
    if duplicate_names:
        message = _build_duplicate_error_message(duplicate_names)
        raise DuplicateColumnError(message) from None

    check_columns_exist(table_or_schema, column_names)

    column_name_set = set(column_names)
    missing_names = [name for name in table_or_schema.column_names if name not in column_name_set]
    if missing_names:
        message = _build_missing_error_message(missing_names)
        raise ValueError(message) from None


def _build_duplicate_error_message(duplicate_names: list[str]) -> str:
    return f"The column names {duplicate_names} appear more than once."


def _build_missing_error_message(missing_names: list[str]) -> str:
    return f"The following column(s) exist in the table but were not listed: {missing_names}"
