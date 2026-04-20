from datetime import date, datetime

import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), 1999, id="datetime 1999"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1), 2000, id="datetime 2000"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1999, 12, 31), 1999, id="date 1999"),
        pytest.param(date(2000, 1, 1), 2000, id="date 2000"),
    ],
)
def test_should_extract_year(value: datetime | date | None, expected: int | None) -> None:
    from tests.helpers import assert_cell_operation_works

    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.year(), expected, type_if_none=type_if_none if value is None else None
    )
