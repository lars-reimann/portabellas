from collections.abc import Callable
from datetime import datetime, time

import pytest

from portabellas.containers import Cell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
    cell_of_unknown_type,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(2000, 1, 1, hour=0), 0, id="datetime midnight"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1, hour=12), 12, id="datetime noon"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(time(hour=0), 0, id="time midnight"),
        pytest.param(time(hour=12), 12, id="time noon"),
    ],
)
def test_should_extract_hour(value: datetime | time | None, expected: int | None) -> None:
    type_if_none = DataTypes.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.hour(), expected, type_if_none=type_if_none if value is None else None
    )


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Datetime(), lambda cell: cell.dt.hour(), DataTypes.Int8(), id="datetime"),
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
    "cell_type",
    [
        pytest.param(DataTypes.Date(), id="date"),
    ],
)
class TestShouldRaiseForDateType:
    def test_should_raise(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Datetime or Time type"):
            _ = cell_of_type(cell_type).dt.hour()


def test_should_skip_validation_for_unknown_type() -> None:
    _ = cell_of_unknown_type().dt.hour()
