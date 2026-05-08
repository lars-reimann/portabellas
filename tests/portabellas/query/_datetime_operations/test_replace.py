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
    ("value", "replace_kwargs", "expected"),
    [
        pytest.param(
            datetime(2000, 1, 1),  # noqa: DTZ001
            {"month": 2, "day": 2, "hour": 2},
            datetime(2000, 2, 2, 2, 0, 0),  # noqa: DTZ001
            id="datetime replace month day hour",
        ),
        pytest.param(
            datetime(2000, 1, 1),  # noqa: DTZ001
            {"year": 2025},
            datetime(2025, 1, 1),  # noqa: DTZ001
            id="datetime replace year",
        ),
        pytest.param(
            None,
            {"month": 2},
            None,
            id="None datetime",
        ),
        pytest.param(
            date(2000, 1, 1),
            {"month": 2, "day": 2, "hour": 2},
            date(2000, 2, 2),
            id="date replace month day (hour ignored)",
        ),
    ],
)
def test_should_replace_components(
    value: datetime | date | None,
    replace_kwargs: dict,
    expected: datetime | date | None,
) -> None:
    type_if_none = DataTypes.Datetime()
    assert_cell_operation_works(
        value,
        lambda cell: cell.dt.replace(**replace_kwargs),
        expected,
        type_if_none=type_if_none if value is None else None,
    )


_DATETIME = DataTypes.Datetime()
_DATE = DataTypes.Date()


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(_DATETIME, lambda cell: cell.dt.replace(year=2025), _DATETIME, id="datetime"),
        pytest.param(_DATE, lambda cell: cell.dt.replace(year=2025), _DATE, id="date"),
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
