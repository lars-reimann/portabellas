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
        pytest.param(datetime(2000, 1, 1, second=0), 0, id="datetime zero"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1, second=30), 30, id="datetime 30"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(time(second=0), 0, id="time zero"),
        pytest.param(time(second=30), 30, id="time 30"),
    ],
)
def test_should_extract_second(value: datetime | time | None, expected: int | None) -> None:
    type_if_none = DataTypes.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.second(), expected, type_if_none=type_if_none if value is None else None
    )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Datetime(), lambda cell: cell.dt.second(), DataTypes.Int8(), id="datetime"),
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
