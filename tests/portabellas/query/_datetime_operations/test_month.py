from datetime import date, datetime

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), 12, id="datetime December"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1), 1, id="datetime January"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1999, 12, 31), 12, id="date December"),
        pytest.param(date(2000, 1, 1), 1, id="date January"),
    ],
)
def test_should_extract_month(value: datetime | date | None, expected: int | None) -> None:
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.month(), expected, type_if_none=type_if_none if value is None else None
    )
