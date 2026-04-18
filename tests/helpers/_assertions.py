import math
from collections.abc import Callable
from typing import Any, SupportsFloat

from polars.testing import assert_frame_equal

from portabellas import Column, Table
from portabellas.containers import Cell
from portabellas.typing import DataType


def assert_cell_operation_works(
    value: Any,
    transformer: Callable[[Cell], Cell],
    expected: Any,
    *,
    type_if_none: DataType | None = None,
    ignore_float_imprecision: bool = True,
) -> None:
    """
    Assert that a cell operation works as expected.

    Parameters
    ----------
    value:
        The value in the input cell.
    transformer:
        The transformer to apply to the cells.
    expected:
        The expected value of the transformed cell.
    type_if_none:
        The type of the column if the value is `None`.
    ignore_float_imprecision:
        If False, check if floating point values match EXACTLY.
    """
    type_ = type_if_none if value is None else None
    column = Column("a", [value], type=type_)
    transformed_column = column.transform(transformer)
    actual = transformed_column[0]

    message = f"Expected {expected}, but got {actual}."

    if expected is None:
        assert actual is None, message
    elif isinstance(expected, SupportsFloat) and math.isnan(expected):
        assert math.isnan(actual), message
    elif isinstance(expected, SupportsFloat) and ignore_float_imprecision:
        assert math.isclose(actual, expected, abs_tol=1e-15), message
    else:
        assert actual == expected, message


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
