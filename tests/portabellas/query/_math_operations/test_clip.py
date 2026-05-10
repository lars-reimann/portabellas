from collections.abc import Callable

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
)


@pytest.mark.parametrize(
    ("value", "lower_bound", "upper_bound", "expected"),
    [
        pytest.param(-50, 1, 10, 1, id="below both bounds"),
        pytest.param(5, 1, 10, 5, id="within bounds"),
        pytest.param(50, 1, 10, 10, id="above both bounds"),
        pytest.param(-50, None, 10, -50, id="upper bound only - below"),
        pytest.param(5, None, 10, 5, id="upper bound only - within"),
        pytest.param(50, None, 10, 10, id="upper bound only - above"),
        pytest.param(-50, 1, None, 1, id="lower bound only - below"),
        pytest.param(5, 1, None, 5, id="lower bound only - within"),
        pytest.param(50, 1, None, 50, id="lower bound only - above"),
        pytest.param(None, 1, 10, None, id="None"),
    ],
)
def test_should_clip_with_literal_bounds(
    value: int | None,
    lower_bound: int | None,
    upper_bound: int | None,
    expected: int | None,
) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.math.clip(lower_bound=lower_bound, upper_bound=upper_bound),
        expected,
        type_if_none=DataTypes.Int64(),
    )


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(-50, 1, id="cell bounds - below"),
        pytest.param(5, 5, id="cell bounds - within"),
        pytest.param(50, 10, id="cell bounds - above"),
    ],
)
def test_should_clip_with_cell_bounds(value: int, expected: int) -> None:
    column = Column("a", [value])
    lower = Cell.constant(1)
    upper = Cell.constant(10)
    transformed_column = column.map(lambda cell: cell.math.clip(lower_bound=lower, upper_bound=upper))
    assert transformed_column[0] == expected


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Int32(),
            lambda cell: cell.math.clip(lower_bound=1, upper_bound=10),
            DataTypes.Int32(),
            id="int",
        ),
        pytest.param(
            DataTypes.Float64(),
            lambda cell: cell.math.clip(lower_bound=1.0, upper_bound=10.0),
            DataTypes.Float64(),
            id="float",
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


@pytest.mark.parametrize(
    ("value_type", "lower_type", "upper_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Int32(),
            DataTypes.Int64(),
            DataTypes.Int64(),
            lambda cell, lo, up: cell.math.clip(lower_bound=lo, upper_bound=up),
            DataTypes.Int32(),
            id="int_cell_bounds",
        ),
    ],
)
class TestShouldInferTypeWithCellBounds:
    def test_should_match_ground_truth(
        self,
        value_type: DataType,
        lower_type: DataType,
        upper_type: DataType,
        operation: Callable[[Cell, Cell, Cell], Cell],
        expected_type: DataType,
    ) -> None:
        result = operation(cell_of_type(value_type), cell_of_type(lower_type), cell_of_type(upper_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self,
        value_type: DataType,
        lower_type: DataType,
        upper_type: DataType,
        operation: Callable[[Cell, Cell, Cell], Cell],
        expected_type: DataType,
    ) -> None:
        assert_cell_type_matches_polars(
            (value_type, lower_type, upper_type),
            lambda a, b, c: operation(a, b, c),
            expected_type,
        )
