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

E = math.e


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 1, id="0"),
        pytest.param(-1, 0.5 * (E + 1 / E), id="-1"),
        pytest.param(1, 0.5 * (E + 1 / E), id="1"),
        pytest.param(math.log((1 + math.sqrt(5)) / 2), 0.5 * math.sqrt(5), id="ln of golden ratio"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_hyperbolic_cosine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.cosh(), expected, type_if_none=DataTypes.Float64())


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda cell: cell.math.cosh(), DataTypes.Float64(), id="float64"),
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
