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
        pytest.param([1, 2, 3], 1, id="non-empty list"),
        pytest.param([], None, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_get_first_element(value: list | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.first(),
        expected,
        type_=DataTypes.List(DataTypes.Int64()),
    )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.List(DataTypes.Int64()), lambda cell: cell.list.first(), DataTypes.Int64(), id="int_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.String()), lambda cell: cell.list.first(), DataTypes.String(), id="string_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Float64()), lambda cell: cell.list.first(), DataTypes.Float64(), id="float_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Boolean()), lambda cell: cell.list.first(), DataTypes.Boolean(), id="bool_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Date()), lambda cell: cell.list.first(), DataTypes.Date(), id="date_list"
        ),
        pytest.param(DataTypes.Unknown(), lambda cell: cell.list.first(), DataTypes.Unknown(), id="unknown"),
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
