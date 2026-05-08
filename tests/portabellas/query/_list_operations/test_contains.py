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
    ("value", "item", "expected"),
    [
        pytest.param([1, 2, 3], 2, True, id="item in list"),
        pytest.param([1, 2, 3], 4, False, id="item not in list"),
        pytest.param([], 1, False, id="empty list"),
        pytest.param(None, 1, None, id="None list"),
    ],
)
class TestShouldCheckIfListContainsItem:
    def test_plain_arguments(self, value: list | None, item: int, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.contains(item),
            expected,
            type_=DataTypes.List(DataTypes.Int64()),
        )

    def test_arguments_wrapped_in_cell(self, value: list | None, item: int, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.contains(Cell.constant(item)),
            expected,
            type_=DataTypes.List(DataTypes.Int64()),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.List(DataTypes.Int64()), lambda cell: cell.list.contains(1), DataTypes.Boolean(), id="int_list"
        ),
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
