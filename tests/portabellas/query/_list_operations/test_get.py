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
    ("value", "index", "expected"),
    [
        pytest.param([1, 2, 3], 0, 1, id="first element"),
        pytest.param([1, 2, 3], 2, 3, id="last element"),
        pytest.param([1, 2, 3], 5, None, id="positive out of bounds"),
        pytest.param([], 0, None, id="empty list"),
        pytest.param(None, 0, None, id="None list"),
        pytest.param([1, 2, 3], -1, 3, id="negative index last element"),
        pytest.param([1, 2, 3], -2, 2, id="negative index second to last element"),
        pytest.param([1, 2, 3], -4, None, id="negative out of bounds"),
    ],
)
class TestShouldGetElementAtIndex:
    def test_plain_arguments(self, value: list | None, index: int, expected: int | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.get(index),
            expected,
            type_=DataTypes.List(DataTypes.Int64()),
        )

    def test_arguments_wrapped_in_cell(self, value: list | None, index: int, expected: int | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.get(Cell.constant(index)),
            expected,
            type_=DataTypes.List(DataTypes.Int64()),
        )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.List(DataTypes.Int64()), lambda cell: cell.list.get(0), DataTypes.Int64(), id="int_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.String()), lambda cell: cell.list.get(0), DataTypes.String(), id="string_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Float64()), lambda cell: cell.list.get(0), DataTypes.Float64(), id="float_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Boolean()), lambda cell: cell.list.get(0), DataTypes.Boolean(), id="bool_list"
        ),
        pytest.param(DataTypes.List(DataTypes.Date()), lambda cell: cell.list.get(0), DataTypes.Date(), id="date_list"),
        pytest.param(DataTypes.Unknown(), lambda cell: cell.list.get(0), DataTypes.Unknown(), id="unknown"),
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
