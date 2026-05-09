from collections.abc import Callable
from datetime import timedelta

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
    ("value", "expected"),
    [
        pytest.param(timedelta(microseconds=1), 1000, id="positive, exact"),
        pytest.param(timedelta(microseconds=-1), -1000, id="negative, exact"),
        pytest.param(timedelta(milliseconds=1, microseconds=-500), 500000, id="mixed"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_full_nanoseconds(value: timedelta | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.dur.full_nanoseconds(),
        expected,
        type_if_none=DataTypes.Duration("us"),
    )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(
            DataTypes.Duration("us"), lambda cell: cell.dur.full_nanoseconds(), DataTypes.Int64(), id="duration"
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
