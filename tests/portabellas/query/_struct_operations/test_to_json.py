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
    ("value", "expected", "type_if_none"),
    [
        pytest.param(
            {"name": "Alice", "age": 25},
            '{"name":"Alice","age":25}',
            None,
            id="struct with string and int",
        ),
        pytest.param(
            None,
            "null",
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            id="None",
        ),
    ],
)
def test_should_convert_struct_to_json(value: dict | None, expected: str | None, type_if_none: DataType | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.struct.to_json(), expected, type_if_none=type_if_none)


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Struct(fields={"a": DataTypes.Int64()}),
            lambda cell: cell.struct.to_json(),
            DataTypes.String(),
            id="int_struct",
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
