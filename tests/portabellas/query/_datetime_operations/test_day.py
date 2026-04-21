from datetime import date, datetime

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), 31, id="datetime end of month"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1), 1, id="datetime start of month"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1999, 12, 31), 31, id="date end of month"),
        pytest.param(date(2000, 1, 1), 1, id="date start of month"),
    ],
)
def test_should_extract_day(value: datetime | date | None, expected: int | None) -> None:
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.day(), expected, type_if_none=type_if_none if value is None else None
    )
