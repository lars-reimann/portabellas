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
        pytest.param(0, 0, id="0 deg"),
        pytest.param(math.pi / 8, 22.5, id="22.5 deg"),
        pytest.param(math.pi / 2, 90, id="90 deg"),
        pytest.param(math.pi, 180, id="180 deg"),
        pytest.param(3 * math.pi / 2, 270, id="270 deg"),
        pytest.param(2 * math.pi, 360, id="360 deg"),
        pytest.param(4 * math.pi, 720, id="720 deg"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_convert_radians_to_degrees(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(
        value, lambda cell: cell.math.radians_to_degrees(), expected, type_if_none=DataTypes.Float64()
    )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda cell: cell.math.radians_to_degrees(), DataTypes.Float64(), id="float64"),
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
