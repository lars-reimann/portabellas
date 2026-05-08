import math
from collections.abc import Callable

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, -math.inf, id="0"),
        pytest.param(1, 0, id="1"),
        pytest.param(math.e, 1, id="e"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_natural_logarithm_by_default(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.log(), expected, type_if_none=DataTypes.Float64())


@pytest.mark.parametrize(
    ("value", "base", "expected"),
    [
        pytest.param(0, math.e, -math.inf, id="base e - 0"),
        pytest.param(1, math.e, 0, id="base e - 1"),
        pytest.param(math.e, math.e, 1, id="base e - e"),
        pytest.param(0, 10, -math.inf, id="base 10 - 0"),
        pytest.param(1, 10, 0, id="base 10 - 1"),
        pytest.param(10, 10, 1, id="base 10 - 10"),
        pytest.param(100, 10, 2, id="base 10 - 100"),
        pytest.param(None, 10, None, id="None"),
    ],
)
def test_should_return_logarithm_to_given_base(value: float | None, base: int, expected: float | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.math.log(base=base),
        expected,
        type_if_none=DataTypes.Float64(),
    )


@pytest.mark.parametrize(
    "base",
    [
        pytest.param(-1, id="negative"),
        pytest.param(0, id="zero"),
        pytest.param(1, id="one"),
    ],
)
def test_should_raise_if_base_is_out_of_bounds(base: int) -> None:
    column = Column("a", [1])
    with pytest.raises((OutOfBoundsError, ValueError), match="base"):
        column.map(lambda cell: cell.math.log(base=base))


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda cell: cell.math.log(), DataTypes.Float64(), id="float64"),
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
