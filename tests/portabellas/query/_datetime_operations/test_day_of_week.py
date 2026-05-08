from collections.abc import Callable
from datetime import date, datetime

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
        pytest.param(datetime(2000, 1, 1), 6, id="datetime Saturday"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 2), 7, id="datetime Sunday"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(2000, 1, 1), 6, id="date Saturday"),
        pytest.param(date(2000, 1, 2), 7, id="date Sunday"),
    ],
)
def test_should_extract_day_of_week(value: datetime | date | None, expected: int | None) -> None:
    type_if_none = DataTypes.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.day_of_week(), expected, type_if_none=type_if_none if value is None else None
    )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Datetime(), lambda cell: cell.dt.day_of_week(), DataTypes.Int8(), id="datetime"),
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
