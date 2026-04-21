"""The module name must differ from the function name, so it can be re-exported properly."""

from __future__ import annotations

from typing import TYPE_CHECKING

from portabellas.exceptions import SchemaError

if TYPE_CHECKING:
    from portabellas.containers import Table
    from portabellas.typing import Schema


def check_schema(
    expected: Table | Schema,
    actual: Table | Schema,
) -> None:
    """
    Check whether two schemas match, and raise an error if they do not.

    Parameters
    ----------
    expected:
        The expected schema.
    actual:
        The actual schema.

    Raises
    ------
    SchemaError
        If the schemas do not match.
    """
    from portabellas.containers import Table  # circular import  # noqa: PLC0415

    expected_schema: Schema = expected.schema if isinstance(expected, Table) else expected
    actual_schema: Schema = actual.schema if isinstance(actual, Table) else actual

    expected_column_names = expected_schema.column_names
    actual_column_names = actual_schema.column_names

    missing_columns = set(expected_column_names) - set(actual_column_names)
    if missing_columns:
        message = _build_error_message_for_missing_columns(sorted(missing_columns))
        raise SchemaError(message) from None

    additional_columns = set(actual_column_names) - set(expected_column_names)
    if additional_columns:
        message = _build_error_message_for_additional_columns(sorted(additional_columns))
        raise SchemaError(message) from None

    if expected_column_names != actual_column_names:
        message = _build_error_message_for_columns_in_wrong_order(expected_column_names, actual_column_names)
        raise SchemaError(message) from None

    _check_types(expected_schema, actual_schema)


def _check_types(expected_schema: Schema, actual_schema: Schema) -> None:
    mismatched_types: list[tuple[str, str, str]] = []

    for column_name in expected_schema.column_names:
        expected_type = expected_schema.get_column_type(column_name)
        actual_type = actual_schema.get_column_type(column_name)

        if expected_type != actual_type:
            mismatched_types.append((column_name, str(expected_type), str(actual_type)))

    if mismatched_types:
        message = _build_error_message_for_column_types(mismatched_types)
        raise SchemaError(message) from None


def _build_error_message_for_missing_columns(missing_columns: list[str]) -> str:
    return f"The columns {missing_columns} are missing."


def _build_error_message_for_additional_columns(additional_columns: list[str]) -> str:
    return f"The columns {additional_columns} are not expected."


def _build_error_message_for_columns_in_wrong_order(expected: list[str], actual: list[str]) -> str:
    result = "The columns are in the wrong order:\n"
    result += f"    Expected: {expected}\n"
    result += f"    Actual:   {actual}"
    return result


def _build_error_message_for_column_types(mismatched_types: list[tuple[str, str, str]]) -> str:
    result = "The following columns have the wrong type:"
    for column_name, expected_type, actual_type in mismatched_types:
        result += f"\n    - '{column_name}': Expected '{expected_type}', but got '{actual_type}'."

    return result
