from collections.abc import Callable
from typing import Any

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
    ("value", "type_", "expected"),
    [
        pytest.param(1, DataTypes.String(), "1", id="int64 to string"),
        pytest.param("1", DataTypes.Int64(), 1, id="string to int64"),
        pytest.param(None, DataTypes.Int64(), None, id="None to int64"),
    ],
)
def test_should_cast_values_to_requested_type(value: Any, type_: DataType, expected: Any) -> None:
    assert_cell_operation_works(value, lambda cell: cell.cast(type_), expected)


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Int32(), lambda cell: cell.cast(DataTypes.String()), DataTypes.String(), id="int to string"
        ),
        pytest.param(
            DataTypes.String(), lambda cell: cell.cast(DataTypes.Int64()), DataTypes.Int64(), id="string to int64"
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
