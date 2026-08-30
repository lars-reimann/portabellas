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
        pytest.param(False, True, id="False"),
        pytest.param(True, False, id="True"),
        pytest.param(None, None, id="None"),
    ],
)
class TestShouldInvertValueOfCell:
    def test_dunder_method(self, value: Any, expected: bool | None) -> None:
        assert_cell_operation_works(value, lambda cell: ~cell, expected, type_if_none=DataTypes.Boolean())

    def test_named_method(self, value: Any, expected: bool | None) -> None:
        assert_cell_operation_works(value, lambda cell: cell.not_(), expected, type_if_none=DataTypes.Boolean())


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Float64(), id="float"),
    ],
)
def test_should_raise_for_non_boolean_non_integer_type_on_operator(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected integer type"):
        _ = ~cell_of_type(cell_type)


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Int64(), id="int"),
    ],
)
def test_should_raise_for_non_boolean_type_on_named_method(cell_type: DataType) -> None:
    with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
        _ = cell_of_type(cell_type).not_()


def test_should_skip_validation_for_unknown_type() -> None:
    _ = ~cell_of_unknown_type()


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Boolean(), lambda cell: ~cell, DataTypes.Boolean(), id="__invert__"),
        pytest.param(DataTypes.Boolean(), lambda cell: cell.not_(), DataTypes.Boolean(), id="not_"),
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
