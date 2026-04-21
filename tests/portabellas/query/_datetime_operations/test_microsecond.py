from datetime import datetime, time

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(2000, 1, 1, microsecond=0), 0, id="datetime zero"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1, microsecond=500), 500, id="datetime 500"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(time(microsecond=0), 0, id="time zero"),
        pytest.param(time(microsecond=500), 500, id="time 500"),
    ],
)
def test_should_extract_microsecond(value: datetime | time | None, expected: int | None) -> None:
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.microsecond(), expected, type_if_none=type_if_none if value is None else None
    )
