from datetime import date, datetime

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), 2, id="datetime 1999"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1), 2, id="datetime 2000"),  # noqa: DTZ001
        pytest.param(datetime(2001, 1, 1), 3, id="datetime 2001"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1999, 12, 31), 2, id="date 1999"),
        pytest.param(date(2000, 1, 1), 2, id="date 2000"),
        pytest.param(date(2001, 1, 1), 3, id="date 2001"),
    ],
)
def test_should_extract_millennium(value: datetime | date | None, expected: int | None) -> None:
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.millennium(), expected, type_if_none=type_if_none if value is None else None
    )
