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
        pytest.param(None, None, None, id="None"),
        pytest.param(1, None, 1, id="int"),
        pytest.param(1, DataTypes.String(), "1", id="with explicit type"),
    ],
)
def test_should_return_constant_value(value: Any, type_: DataType | None, expected: Any) -> None:
    assert_cell_operation_works(None, lambda _: Cell.constant(value, type=type_), expected)


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda _: Cell.constant(42), DataTypes.Int32(), id="int"),
        pytest.param(DataTypes.Int64(), lambda _: Cell.constant(3.14), DataTypes.Float64(), id="float"),
        pytest.param(DataTypes.Int64(), lambda _: Cell.constant("hello"), DataTypes.String(), id="str"),
        pytest.param(DataTypes.Int64(), lambda _: Cell.constant(True), DataTypes.Boolean(), id="bool"),  # noqa: FBT003
        pytest.param(DataTypes.Int64(), lambda _: Cell.constant(None), DataTypes.Unknown(), id="none"),
    ],
)
class TestShouldInferTypeFromValue:
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
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Int64(),
            lambda _: Cell.constant(42, type=DataTypes.Int64()),
            DataTypes.Int64(),
            id="explicit_type",
        ),
    ],
)
class TestShouldUseExplicitTypeOverInferred:
    def test_should_match_ground_truth(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        assert_cell_type_matches_polars(given_type, operation, expected_type)
