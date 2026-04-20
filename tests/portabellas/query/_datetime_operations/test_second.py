from datetime import datetime, time

import pytest

from portabellas.typing import DataType


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
    from tests.helpers import assert_cell_operation_works

    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.second(), expected, type_if_none=type_if_none if value is None else None
    )
