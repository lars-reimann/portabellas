from collections.abc import Callable
from typing import Any

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
        pytest.param(0, -1, id="0"),
        pytest.param(1, -2, id="1"),
        pytest.param(-1, 0, id="-1"),
        pytest.param(None, None, id="None"),
    ],
)
class TestShouldInvertBitsOfCell:
    def test_dunder_method(self, value: Any, expected: int | None) -> None:
        assert_cell_operation_works(value, lambda cell: ~cell, expected, type_if_none=DataTypes.Int64())

    def test_named_method(self, value: Any, expected: int | None) -> None:
        assert_cell_operation_works(value, lambda cell: cell.bitwise_invert(), expected, type_if_none=DataTypes.Int64())


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Boolean(), id="boolean"),
        pytest.param(DataTypes.Float64(), id="float"),
    ],
)
class TestShouldRaiseForNonIntegerTypeOnBitwiseInvert:
    def test_self(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected integer type"):
            _ = cell_of_type(cell_type).bitwise_invert()


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Float64(), id="float"),
    ],
)
def test_should_raise_for_non_integer_type_on_operator(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected integer type"):
        _ = ~cell_of_type(cell_type)


def test_should_skip_validation_for_unknown_type() -> None:
    _ = ~cell_of_unknown_type()


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda cell: ~cell, DataTypes.Int64(), id="__invert__"),
        pytest.param(DataTypes.Int64(), lambda cell: cell.bitwise_invert(), DataTypes.Int64(), id="bitwise_invert"),
        pytest.param(DataTypes.Int32(), lambda cell: ~cell, DataTypes.Int32(), id="__invert___int32"),
        pytest.param(DataTypes.UInt32(), lambda cell: ~cell, DataTypes.UInt32(), id="__invert___uint32"),
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
