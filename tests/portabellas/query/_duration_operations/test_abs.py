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
        pytest.param(timedelta(days=1), timedelta(days=1), id="positive days"),
        pytest.param(timedelta(days=1, hours=12), timedelta(days=1, hours=12), id="positive days and hours"),
        pytest.param(timedelta(days=-1), timedelta(days=1), id="negative days"),
        pytest.param(timedelta(days=-1, hours=-12), timedelta(days=1, hours=12), id="negative days and hours"),
        pytest.param(timedelta(days=1, hours=-12), timedelta(hours=12), id="positive days, negative hours"),
        pytest.param(timedelta(days=-1, hours=12), timedelta(hours=12), id="negative days, positive hours"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_absolute_duration(value: timedelta | None, expected: timedelta | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.dur.abs(), expected, type_if_none=DataTypes.Duration("us"))


_DURATION_MS = DataTypes.Duration("ms")
_DURATION_US = DataTypes.Duration("us")


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(_DURATION_MS, lambda cell: cell.dur.abs(), _DURATION_MS, id="ms"),
        pytest.param(_DURATION_US, lambda cell: cell.dur.abs(), _DURATION_US, id="us"),
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
