from datetime import date, datetime

import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), 52, id="datetime 1999-12-31"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 2), 52, id="datetime 2000-01-02"),  # noqa: DTZ001
        pytest.param(datetime(2001, 12, 31), 1, id="datetime 2001-12-31"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1999, 12, 31), 52, id="date 1999-12-31"),
        pytest.param(date(2000, 1, 2), 52, id="date 2000-01-02"),
        pytest.param(date(2001, 12, 31), 1, id="date 2001-12-31"),
    ],
)
def test_should_extract_week(value: datetime | date | None, expected: int | None) -> None:
    from tests.helpers import assert_cell_operation_works

    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.week(), expected, type_if_none=type_if_none if value is None else None
    )
