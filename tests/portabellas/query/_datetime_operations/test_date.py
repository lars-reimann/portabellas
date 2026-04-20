from datetime import date, datetime

import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), date(1999, 12, 31), id="datetime midnight"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1, 12, 30, 0), date(2000, 1, 1), id="datetime noon"),  # noqa: DTZ001
        pytest.param(None, None, id="None"),
    ],
)
def test_should_extract_date(value: datetime | None, expected: date | None) -> None:
    from tests.helpers import assert_cell_operation_works

    assert_cell_operation_works(value, lambda cell: cell.dt.date(), expected, type_if_none=DataType.Datetime())
