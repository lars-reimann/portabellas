from datetime import datetime, time

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


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
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.hour(), expected, type_if_none=type_if_none if value is None else None
    )
