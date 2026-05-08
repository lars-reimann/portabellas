from collections.abc import Callable
from typing import Any

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_type_matches_polars, cell_of_type, cell_of_unknown_type


@pytest.mark.parametrize(
    ("cells", "expected"),
    [
        pytest.param([], None, id="empty"),
        pytest.param([Cell.constant(None)], None, id="all None"),
        pytest.param([Cell.constant(None), Cell.constant(1)], 1, id="one not null"),
        pytest.param([Cell.constant(1), Cell.constant(None), Cell.constant(2)], 1, id="multiple not null"),
    ],
)
def test_should_return_first_non_null_value(cells: list[Cell], expected: Any) -> None:
    column = Column("a", [None])
    transformed = column.map(lambda _: Cell.first_not_null(cells))
    assert transformed.get_value(0) == expected


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Int32(),
            lambda cell: Cell.first_not_null([cell]),
            DataTypes.Int32(),
            id="single_cell_with_known_type",
        ),
        pytest.param(
            DataTypes.Int32(),
            lambda cell: Cell.first_not_null([cell, cell_of_type(DataTypes.Int32())]),
            DataTypes.Int32(),
            id="multiple_cells_with_same_type",
        ),
        pytest.param(
            DataTypes.Int32(),
            lambda cell: Cell.first_not_null([cell, cell_of_type(DataTypes.String())]),
            DataTypes.Unknown(),
            id="mixed_types",
        ),
        pytest.param(
            DataTypes.Int32(),
            lambda _cell: Cell.first_not_null([cell_of_unknown_type()]),
            DataTypes.Unknown(),
            id="unknown_type",
        ),
        pytest.param(
            DataTypes.Int32(),
            lambda cell: Cell.first_not_null([cell, cell_of_unknown_type()]),
            DataTypes.Unknown(),
            id="known_and_unknown_types",
        ),
        pytest.param(
            DataTypes.Int32(),
            lambda _cell: Cell.first_not_null([Cell.constant(None)]),
            DataTypes.Null(),
            id="constant_none",
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
