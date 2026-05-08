import math
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
        pytest.param(0, 0, id="0"),
        pytest.param(-1, -0.5 * (math.e - 1 / math.e), id="-1"),
        pytest.param(1, 0.5 * (math.e - 1 / math.e), id="1"),
        pytest.param(math.log((1 + math.sqrt(5)) / 2), 0.5, id="ln of golden ratio"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_hyperbolic_sine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.sinh(), expected, type_if_none=DataTypes.Float64())


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda cell: cell.math.sinh(), DataTypes.Float64(), id="float64"),
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
