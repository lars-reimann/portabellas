from collections.abc import Callable

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_type_matches_polars, assert_tables_are_equal, cell_of_type


@pytest.mark.parametrize(
    ("value", "prefix", "expected", "type_if_none", "expected_type"),
    [
        pytest.param(
            {"name": "Alice", "age": 25},
            "pre_",
            {"pre_name": "Alice", "pre_age": 25},
            None,
            None,
            id="prefix all fields",
        ),
        pytest.param(
            None,
            "pre_",
            None,
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            DataTypes.Struct(fields={"pre_name": DataTypes.String(), "pre_age": DataTypes.Int64()}),
            id="None",
        ),
    ],
)
def test_should_prefix_field_names(
    value: dict | None,
    prefix: str,
    expected: dict | None,
    type_if_none: DataType | None,
    expected_type: DataType | None,
) -> None:
    column = Column("a", [value], type=type_if_none)
    result = column.map(lambda cell: cell.struct.prefix_names(prefix))
    expected_column = Column("a", [expected], type=expected_type)
    assert_tables_are_equal(result.to_table(), expected_column.to_table())


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            lambda cell: cell.struct.prefix_names("pre_"),
            DataTypes.Struct(fields={"pre_name": DataTypes.String(), "pre_age": DataTypes.Int64()}),
            id="prefix",
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
