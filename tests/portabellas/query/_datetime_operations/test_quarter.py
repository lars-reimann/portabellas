from datetime import date, datetime

import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), 4, id="datetime Q4"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1), 1, id="datetime Q1"),  # noqa: DTZ001
        pytest.param(datetime(2000, 4, 1), 2, id="datetime Q2"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1999, 12, 31), 4, id="date Q4"),
        pytest.param(date(2000, 1, 1), 1, id="date Q1"),
        pytest.param(date(2000, 4, 1), 2, id="date Q2"),
    ],
)
def test_should_extract_quarter(value: datetime | date | None, expected: int | None) -> None:
    from tests.helpers import assert_cell_operation_works

    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.quarter(), expected, type_if_none=type_if_none if value is None else None
    )
