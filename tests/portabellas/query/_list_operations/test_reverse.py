from collections.abc import Callable

import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], [3, 2, 1], id="non-empty list"),
        pytest.param([], [], id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_reverse_list(value: list | None, expected: list | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.reverse(),
        expected,
        type_=DataTypes.List(DataTypes.Int64()),
    )


_INT64_LIST = DataTypes.List(DataTypes.Int64())
_STRING_LIST = DataTypes.List(DataTypes.String())


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(_INT64_LIST, lambda cell: cell.list.reverse(), _INT64_LIST, id="int list"),
        pytest.param(_STRING_LIST, lambda cell: cell.list.reverse(), _STRING_LIST, id="string list"),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        assert_cell_type_matches_polars(given_type, operation, expected_type)
