from datetime import datetime, time

import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), time(0, 0, 0), id="datetime midnight"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1, 12, 30, 0), time(12, 30, 0), id="datetime noon-thirty"),  # noqa: DTZ001
        pytest.param(None, None, id="None"),
    ],
)
def test_should_extract_time(value: datetime | None, expected: time | None) -> None:
    from tests.helpers import assert_cell_operation_works

    assert_cell_operation_works(value, lambda cell: cell.dt.time(), expected, type_if_none=DataType.Datetime())
