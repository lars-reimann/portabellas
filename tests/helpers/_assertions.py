import math
from collections.abc import Callable
from typing import Any, SupportsFloat

import polars as pl
from polars.testing import assert_frame_equal

from portabellas import Column, Table
from portabellas.containers import Cell, Row
from portabellas.typing import DataType


def assert_cell_has_type(cell: Cell, expected_type: DataType) -> None:
    """
    Assert that a cell has the expected type.

    Parameters
    ----------
    cell:
        The cell to check.
    expected_type:
        The expected type of the cell.
    """
    assert cell._type == expected_type, f"Expected type {expected_type}, got {cell._type}"


def assert_cell_operation_works(
    value: Any,
    mapper: Callable[[Cell], Cell],
    expected: Any,
    *,
    type_: DataType | None = None,
    type_if_none: DataType | None = None,
    ignore_float_imprecision: bool = True,
) -> None:
    """
    Assert that a cell operation works as expected.

    Parameters
    ----------
    value:
        The value in the input cell.
    mapper:
        The function that maps a cell to a new value.
    expected:
        The expected value of the transformed cell.
    type_:
        The type of the column. Overrides `type_if_none` if provided.
    type_if_none:
        The type of the column if the value is `None`. Ignored if `type_` is provided.
    ignore_float_imprecision:
        If False, check if floating point values match EXACTLY.
    """
    column_type: DataType | None = None
    if type_ is not None:
        column_type = type_
    elif value is None:
        column_type = type_if_none

    column = Column("a", [value], type=column_type)
    transformed_column = column.map(mapper)
    actual = transformed_column[0]
    if isinstance(actual, pl.Series):
        actual = actual.to_list()

    message = f"Expected {expected}, but got {actual}."

    if expected is None:
        assert actual is None, message
    elif isinstance(expected, SupportsFloat) and math.isnan(expected):
        assert math.isnan(actual), message
    elif isinstance(expected, SupportsFloat) and ignore_float_imprecision:
        assert math.isclose(actual, expected, abs_tol=1e-15), message
    else:
        assert actual == expected, message


def assert_row_operation_works(
    table: Table,
    mapper: Callable[[Row], Cell],
    expected: list[Any],
) -> None:
    """
    Assert that a row operation works as expected.

    Parameters
    ----------
    table:
        The input table.
    mapper:
        The function that maps a row to the value of the new column.
    expected:
        The expected values of the computed column.
    """
    column_name = _find_free_column_name(table, "computed")

    new_table = table.add_computed_column(column_name, mapper)
    actual = list(new_table.get_column(column_name))
    assert actual == expected


def _find_free_column_name(table: Table, prefix: str) -> str:
    column_name = prefix

    while table.has_column(column_name):
        column_name += "_"

    return column_name


def assert_tables_are_equal(
    actual: Table,
    expected: Table,
    *,
    ignore_column_order: bool = False,
    ignore_row_order: bool = False,
    ignore_types: bool = False,
    ignore_float_imprecision: bool = True,
) -> None:
    """
    Assert that two tables are equal.

    Parameters
    ----------
    actual:
        The actual table.
    expected:
        The expected table.
    ignore_column_order:
        Ignore differences in column order.
    ignore_row_order:
        Ignore differences in row order.
    ignore_types:
        Ignore differences between types.
    ignore_float_imprecision:
        Ignore minor differences between floats.
    """
    assert_frame_equal(
        actual._data_frame,
        expected._data_frame,
        check_column_order=not ignore_column_order,
        check_row_order=not ignore_row_order,
        check_dtypes=not ignore_types,
        check_exact=not ignore_float_imprecision,
    )
