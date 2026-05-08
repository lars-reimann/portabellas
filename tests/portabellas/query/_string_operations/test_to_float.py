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
        pytest.param("", None, id="empty"),
        pytest.param("abc", None, id="invalid"),
        pytest.param("1", 1.0, id="int"),
        pytest.param("1.5", 1.5, id="positive float"),
        pytest.param("-1.5", -1.5, id="negative float"),
        pytest.param("1e3", 1000, id="exponential"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_convert_string_to_float(value: str | None, expected: float | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.str.to_float(),
        expected,
        type_if_none=DataTypes.String(),
    )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.String(), lambda cell: cell.str.to_float(), DataTypes.Float64(), id="string"),
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
