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
    ("value", "field_name", "expected", "type_if_none"),
    [
        pytest.param({"name": "Alice", "age": 25}, "name", "Alice", None, id="string field"),
        pytest.param({"name": "Alice", "age": 25}, "age", 25, None, id="int field"),
        pytest.param(
            None,
            "name",
            None,
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            id="None",
        ),
    ],
)
def test_should_get_struct_field(
    value: dict | None,
    field_name: str,
    expected: object,
    type_if_none: DataType | None,
) -> None:
    assert_cell_operation_works(value, lambda cell: cell.struct.get(field_name), expected, type_if_none=type_if_none)


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            lambda cell: cell.struct.get("name"),
            DataTypes.String(),
            id="get_string_field",
        ),
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            lambda cell: cell.struct.get("age"),
            DataTypes.Int64(),
            id="get_int_field",
        ),
        pytest.param(
            DataTypes.Struct(
                fields={"name": DataTypes.String(), "nested": DataTypes.Struct(fields={"x": DataTypes.Float64()})},
            ),
            lambda cell: cell.struct.get("nested"),
            DataTypes.Struct(fields={"x": DataTypes.Float64()}),
            id="get_nested_struct_field",
        ),
        pytest.param(
            DataTypes.Struct(fields={"items": DataTypes.List(DataTypes.Int32())}),
            lambda cell: cell.struct.get("items"),
            DataTypes.List(DataTypes.Int32()),
            id="get_list_field",
        ),
        pytest.param(
            DataTypes.Unknown(),
            lambda cell: cell.struct.get("name"),
            DataTypes.Unknown(),
            id="unknown_type",
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
