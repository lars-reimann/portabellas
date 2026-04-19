"""The module name must differ from the function name, so it can be re-exported properly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.exceptions import ColumnNotFoundError

if TYPE_CHECKING:
    from portabellas.containers._table import Table


def check_columns_exist(table: Table, selector: str | list[str]) -> None:
    """
    Check whether the specified columns exist, and raise an error if they do not.

    Parameters
    ----------
    table:
        The table to check.
    selector:
        The columns to check.

    Raises
    ------
    ColumnNotFoundError
        If a column name does not exist.
    """
    if isinstance(selector, str):
        selector = [selector]

    known_names = set(table._data_frame.columns)
    unknown_names = [name for name in selector if name not in known_names]
    if unknown_names:
        message = _build_error_message(known_names, unknown_names)
        raise ColumnNotFoundError(message) from None


def _build_error_message(known_names: set[str], unknown_names: list[str]) -> str:
    from portabellas._utils import get_similar_strings  # noqa: PLC0415

    result = "Could not find column(s):"

    for unknown_name in unknown_names:
        similar_columns = get_similar_strings(unknown_name, known_names)
        result += f"\n    - '{unknown_name}'"
        if similar_columns:
            result += f": Did you mean one of {similar_columns}?"

    return result
