"""The module name must differ from the function name, so it can be re-exported properly with apipkg."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from portabellas.exceptions import LengthMismatchError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from portabellas import Column, Table


def check_row_counts_are_equal(
    data: Sequence[Column | Table] | Mapping[str, Sequence[Any]],
    *,
    ignore_entries_without_rows: bool = False,
) -> None:
    """
    Check whether all columns or tables have the same row count and raise an error if they do not.

    Parameters
    ----------
    data:
        The columns or tables to check.
    ignore_entries_without_rows:
        Whether to ignore columns or tables that have no rows.

    Raises
    ------
    LengthMismatchError
        If some columns or tables have different row counts.
    """
    # Avoid collecting a single lazy frame
    if len(data) < 2:
        return

    items = _items(data, ignore_entries_without_rows=ignore_entries_without_rows)
    mismatched_items = _mismatched_items(items)
    if mismatched_items:
        message = _build_error_message(items[0], mismatched_items)
        raise LengthMismatchError(message) from None


def _items(
    data: Sequence[Column | Table] | Mapping[str, Sequence[Any]],
    *,
    ignore_entries_without_rows: bool = False,
) -> list[_Item]:
    from portabellas import Column, Table  # circular import

    if isinstance(data, Mapping):
        return [_Item(f"Column '{name}'", len(column)) for name, column in data.items()]

    result = []

    for i, entry in enumerate(data):
        if isinstance(entry, Column) and (not ignore_entries_without_rows or entry.row_count > 0):
            result.append(_Item(f"Column '{entry.name}'", entry.row_count))
        elif isinstance(entry, Table) and (not ignore_entries_without_rows or entry.row_count > 0):
            result.append(_Item(f"Table {i}", entry.row_count))

    return result


def _mismatched_items(items: list[_Item]) -> list[_Item]:
    if len(items) < 2:
        return []

    return [item for item in items[1:] if item.row_count != items[0].row_count]


def _build_error_message(first_entry: _Item, mismatched_entries: list[_Item]) -> str:
    result = f"{first_entry.name} has {first_entry.row_count} rows, which differs from:"

    for entry in mismatched_entries:
        result += f"\n    - {entry.name} ({entry.row_count} rows)"

    return result


@dataclass
class _Item:
    name: str
    row_count: int
