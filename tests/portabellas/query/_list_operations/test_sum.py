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
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 6, id="positive integers"),
        pytest.param([10], 10, id="single element"),
        pytest.param([], 0, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_sum_list_elements(value: list | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.sum(),
        expected,
        type_=DataTypes.List(DataTypes.Int64()),
    )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.List(DataTypes.Int8()), lambda cell: cell.list.sum(), DataTypes.Int64(), id="int8_list"),
        pytest.param(
            DataTypes.List(DataTypes.UInt8()), lambda cell: cell.list.sum(), DataTypes.Int64(), id="uint8_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Int64()), lambda cell: cell.list.sum(), DataTypes.Int64(), id="int64_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Boolean()), lambda cell: cell.list.sum(), DataTypes.UInt32(), id="bool_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Float32()), lambda cell: cell.list.sum(), DataTypes.Float32(), id="float32_list"
        ),
        pytest.param(
            DataTypes.List(DataTypes.Float64()), lambda cell: cell.list.sum(), DataTypes.Float64(), id="float64_list"
        ),
        pytest.param(DataTypes.Unknown(), lambda cell: cell.list.sum(), DataTypes.Unknown(), id="unknown"),
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


@pytest.mark.parametrize(
    "given_type",
    [
        pytest.param(DataTypes.List(DataTypes.String()), id="string inner"),
        pytest.param(DataTypes.List(DataTypes.Date()), id="date inner"),
    ],
)
def test_should_raise_type_error_for_non_numeric_inner(given_type: DataType) -> None:
    cell = cell_of_type(given_type)
    with pytest.raises(ColumnTypeError):
        cell.list.sum()


def test_should_skip_validation_for_unknown_type() -> None:
    cell = cell_of_type(DataTypes.Unknown())
    cell.list.sum()
