"""The module name must differ from the function name, so it can be re-exported properly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas._utils import compute_duplicates
from portabellas.exceptions import DuplicateColumnError

if TYPE_CHECKING:
    from portabellas.containers import Table
    from portabellas.typing import Schema


def check_columns_dont_exist(
    table_or_schema: Table | Schema,
    new_names: str | list[str],
    *,
    old_names: str | list[str] | None = None,
) -> None:
    """
    Check whether the specified new column names do not exist yet and are unique, and raise an error if they do.

    Parameters
    ----------
    table_or_schema:
        The table or schema to check.
    new_names:
        The column names to check.
    old_names:
        The old column name(s) to exclude from the check. Set this to None if you don't want to exclude any columns.

    Raises
    ------
    DuplicateColumnError
        If a column name exists already.
    """
    from portabellas.containers import Table  # circular import  # noqa: PLC0415

    if isinstance(table_or_schema, Table):
        table_or_schema = table_or_schema.schema
    if isinstance(new_names, str):
        new_names = [new_names]
    if isinstance(old_names, str):
        old_names = [old_names]

    excluded = set(old_names) if old_names is not None else set()
    known_names = set(table_or_schema.column_names) - excluded
    duplicate_names = compute_duplicates(new_names, forbidden_values=known_names)

    if duplicate_names:
        message = _build_error_message(duplicate_names)
        raise DuplicateColumnError(message) from None


def _build_error_message(duplicate_names: list[str]) -> str:
    return f"The columns {duplicate_names} exist already."
