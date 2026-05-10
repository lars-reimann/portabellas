import math
from collections.abc import Callable

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.containers._cell import ConvertibleToNumericCell
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
)


@pytest.mark.parametrize(
    ("y", "x", "expected"),
    [
        pytest.param(1, 1, math.pi / 4, id="1,1"),
        pytest.param(-1, 1, -math.pi / 4, id="-1,1"),
        pytest.param(1, -1, 3 * math.pi / 4, id="1,-1"),
        pytest.param(0, 1, 0, id="0,1"),
        pytest.param(1, 0, math.pi / 2, id="1,0"),
        pytest.param(None, 1, None, id="y is None"),
        pytest.param(1, None, None, id="x is None"),
    ],
)
def test_should_return_atan2(y: ConvertibleToNumericCell, x: ConvertibleToNumericCell, expected: float | None) -> None:
    assert_cell_operation_works(None, lambda _: Cell.atan2(y, x), expected, type_if_none=DataTypes.Float64())


@pytest.mark.parametrize(
    ("y", "x", "expected"),
    [
        pytest.param(Cell.constant(1), Cell.constant(1), math.pi / 4, id="cell components"),
    ],
)
def test_should_return_atan2_with_cell_args(
    y: ConvertibleToNumericCell, x: ConvertibleToNumericCell, expected: float | None
) -> None:
    assert_cell_operation_works(None, lambda _: Cell.atan2(y, x), expected, type_if_none=DataTypes.Float64())


def test_should_raise_if_no_args_are_provided() -> None:
    column = Column("a", [1])
    with pytest.raises(TypeError):
        column.map(lambda _: Cell.atan2(1)).get_value(0)  # type: ignore[call-arg]


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda _: Cell.atan2(1, 1), DataTypes.Float64(), id="literal args"),
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
    ("y_type", "x_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Int64(), DataTypes.Int64(), lambda y, x: Cell.atan2(y, x), DataTypes.Float64(), id="int_int"
        ),
        pytest.param(
            DataTypes.Float64(),
            DataTypes.Float64(),
            lambda y, x: Cell.atan2(y, x),
            DataTypes.Float64(),
            id="float_float",
        ),
    ],
)
class TestShouldInferTypeWithCellArgs:
    def test_should_match_ground_truth(
        self, y_type: DataType, x_type: DataType, operation: Callable[[Cell, Cell], Cell], expected_type: DataType
    ) -> None:
        result = operation(cell_of_type(y_type), cell_of_type(x_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self, y_type: DataType, x_type: DataType, operation: Callable[[Cell, Cell], Cell], expected_type: DataType
    ) -> None:
        assert_cell_type_matches_polars((y_type, x_type), lambda y, x: operation(y, x), expected_type)
