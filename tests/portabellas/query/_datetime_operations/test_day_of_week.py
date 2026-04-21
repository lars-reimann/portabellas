from datetime import date, datetime

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


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
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.day_of_week(), expected, type_if_none=type_if_none if value is None else None
    )
