from datetime import date, datetime

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1900, 1, 1), False, id="datetime 1900 not leap"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1), True, id="datetime 2000 leap"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1900, 1, 1), False, id="date 1900 not leap"),
        pytest.param(date(2000, 1, 1), True, id="date 2000 leap"),
    ],
)
def test_should_check_leap_year(value: datetime | date | None, expected: bool | None) -> None:
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.is_in_leap_year(), expected, type_if_none=type_if_none if value is None else None
    )
