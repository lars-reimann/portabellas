from collections.abc import Callable

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_type_matches_polars, assert_tables_are_equal, cell_of_type


@pytest.mark.parametrize(
    ("value", "old_name", "new_name", "expected", "type_if_none", "expected_type"),
    [
        pytest.param(
            {"name": "Alice", "age": 25},
            "name",
            "first_name",
            {"first_name": "Alice", "age": 25},
            None,
            None,
            id="rename string field",
        ),
        pytest.param(
            {"name": "Alice", "age": 25},
            "age",
            "years",
            {"name": "Alice", "years": 25},
            None,
            None,
            id="rename int field",
        ),
        pytest.param(
            None,
            "name",
            "first_name",
            None,
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            DataTypes.Struct(fields={"first_name": DataTypes.String(), "age": DataTypes.Int64()}),
            id="None",
        ),
    ],
)
def test_should_rename_struct_field(
    value: dict | None,
    old_name: str,
    new_name: str,
    expected: dict | None,
    type_if_none: DataType | None,
    expected_type: DataType | None,
) -> None:
    column = Column("a", [value], type=type_if_none)
    result = column.map(lambda cell: cell.struct.rename(old_name, new_name))
    expected_column = Column("a", [expected], type=expected_type)
    assert_tables_are_equal(result.to_table(), expected_column.to_table())


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            lambda cell: cell.struct.rename("name", "first_name"),
            DataTypes.Struct(fields={"first_name": DataTypes.String(), "age": DataTypes.Int64()}),
            id="rename",
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
