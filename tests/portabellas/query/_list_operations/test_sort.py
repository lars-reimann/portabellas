from collections.abc import Callable

import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "descending", "expected"),
    [
        pytest.param([3, 1, 2], False, [1, 2, 3], id="ascending"),
        pytest.param([3, 1, 2], True, [3, 2, 1], id="descending"),
        pytest.param([], False, [], id="empty list ascending"),
        pytest.param([], True, [], id="empty list descending"),
        pytest.param(None, False, None, id="None list"),
    ],
)
def test_should_sort_list(value: list | None, descending: bool, expected: list | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.sort(descending=descending),
        expected,
        type_=DataTypes.List(DataTypes.Int64()),
    )


_INT64_LIST = DataTypes.List(DataTypes.Int64())
_STRING_LIST = DataTypes.List(DataTypes.String())


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(_INT64_LIST, lambda cell: cell.list.sort(), _INT64_LIST, id="int list"),
        pytest.param(_STRING_LIST, lambda cell: cell.list.sort(), _STRING_LIST, id="string list"),
    ],
)
def test_should_infer_type(given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType) -> None:
    result = operation(cell_of_type(given_type))
    assert_cell_has_type(result, expected_type)
