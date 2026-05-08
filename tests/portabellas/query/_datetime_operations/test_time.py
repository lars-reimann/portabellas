from collections.abc import Callable
from datetime import datetime, time

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
        pytest.param(datetime(1999, 12, 31), time(0, 0, 0), id="datetime midnight"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1, 12, 30, 0), time(12, 30, 0), id="datetime noon-thirty"),  # noqa: DTZ001
        pytest.param(None, None, id="None"),
    ],
)
def test_should_extract_time(value: datetime | None, expected: time | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.dt.time(), expected, type_if_none=DataTypes.Datetime())


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Datetime(), lambda cell: cell.dt.time(), DataTypes.Time(), id="datetime"),
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
