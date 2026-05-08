from collections.abc import Callable

import pytest

from portabellas.containers import Cell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
    cell_of_unknown_type,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="zero int"),
        pytest.param(0.0, 0.0, id="zero float"),
        pytest.param(10, 10, id="positive int"),
        pytest.param(10.5, 10.5, id="positive float"),
        pytest.param(-10, 10, id="negative int"),
        pytest.param(-10.5, 10.5, id="negative float"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_absolute_value(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: abs(cell), expected, type_if_none=DataTypes.Float64())


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Boolean(), id="boolean"),
    ],
)
def test_should_raise_for_non_numeric_type(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected numeric type"):
        _ = abs(cell_of_type(cell_type))


def test_should_skip_validation_for_unknown_type() -> None:
    _ = abs(cell_of_unknown_type())


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int32(), lambda cell: abs(cell), DataTypes.Int32(), id="int"),
        pytest.param(DataTypes.Float64(), lambda cell: abs(cell), DataTypes.Float64(), id="float"),
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
