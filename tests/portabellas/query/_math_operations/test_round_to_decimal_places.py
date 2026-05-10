from collections.abc import Callable

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.exceptions import OutOfBoundsError
from portabellas.query._math_operations import RoundingMode
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
)


@pytest.mark.parametrize(
    ("value", "decimal_places", "expected"),
    [
        pytest.param(0.0, 1, 0, id="0.0"),
        pytest.param(0.1, 0, 0, id="0.1 (0 decimal places)"),
        pytest.param(1.0, 0, 1, id="1.0 (0 decimal places)"),
        pytest.param(1.1, 0, 1, id="1.1 (0 decimal places)"),
        pytest.param(0.14, 1, 0.1, id="0.14 (1 decimal places)"),
        pytest.param(0.104, 2, 0.1, id="0.104 (2 decimal places)"),
        pytest.param(0.15, 1, 0.2, id="0.15 (1 decimal places)"),
        pytest.param(0.105, 2, 0.11, id="0.105 (2 decimal places)"),
        pytest.param(9.99, 1, 10, id="9.99 (1 decimal places)"),
        pytest.param(9.99, 2, 9.99, id="9.99 (2 decimal places)"),
        pytest.param(None, 1, None, id="None"),
    ],
)
def test_should_round_to_decimal_places(
    value: float | None,
    decimal_places: int,
    expected: float | None,
) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.math.round_to_decimal_places(decimal_places),
        expected,
        type_if_none=DataTypes.Float64(),
    )


def test_should_raise_if_decimal_places_is_out_of_bounds() -> None:
    column = Column("a", [1])
    with pytest.raises(OutOfBoundsError):
        column.map(lambda cell: cell.math.round_to_decimal_places(-1))


@pytest.mark.parametrize(
    ("value", "mode", "expected"),
    [
        pytest.param(0.5, "half_to_even", 0, id="0.5 half_to_even"),
        pytest.param(1.5, "half_to_even", 2, id="1.5 half_to_even"),
        pytest.param(2.5, "half_to_even", 2, id="2.5 half_to_even"),
        pytest.param(0.5, "half_away_from_zero", 1, id="0.5 half_away_from_zero"),
        pytest.param(-0.5, "half_away_from_zero", -1, id="-0.5 half_away_from_zero"),
        pytest.param(2.5, "half_away_from_zero", 3, id="2.5 half_away_from_zero"),
        pytest.param(0.9, "truncate", 0, id="0.9 truncate"),
        pytest.param(-0.9, "truncate", 0, id="-0.9 truncate"),
        pytest.param(1.29, "truncate", 1, id="1.29 truncate (0 decimal places)"),
        pytest.param(None, "truncate", None, id="None truncate"),
    ],
)
def test_should_round_with_mode(value: float | None, mode: RoundingMode, expected: float | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.math.round_to_decimal_places(0, mode=mode),
        expected,
        type_if_none=DataTypes.Float64(),
    )


def test_should_raise_if_mode_is_invalid() -> None:
    column = Column("a", [1])
    with pytest.raises(ValueError, match="Invalid rounding mode"):
        column.map(lambda cell: cell.math.round_to_decimal_places(0, mode="invalid"))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Int32(),
            lambda cell: cell.math.round_to_decimal_places(2),
            DataTypes.Int32(),
            id="int",
        ),
        pytest.param(
            DataTypes.Float64(),
            lambda cell: cell.math.round_to_decimal_places(2),
            DataTypes.Float64(),
            id="float",
        ),
        pytest.param(
            DataTypes.Int32(),
            lambda cell: cell.math.round_to_decimal_places(2, mode="half_to_even"),
            DataTypes.Int32(),
            id="int_half_to_even",
        ),
        pytest.param(
            DataTypes.Float64(),
            lambda cell: cell.math.round_to_decimal_places(2, mode="half_to_even"),
            DataTypes.Float64(),
            id="float_half_to_even",
        ),
        pytest.param(
            DataTypes.Int32(),
            lambda cell: cell.math.round_to_decimal_places(2, mode="truncate"),
            DataTypes.Int32(),
            id="int_truncate",
        ),
        pytest.param(
            DataTypes.Float64(),
            lambda cell: cell.math.round_to_decimal_places(2, mode="truncate"),
            DataTypes.Float64(),
            id="float_truncate",
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
