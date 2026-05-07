from datetime import date, datetime

import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), 365, id="datetime end of non-leap year"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1), 1, id="datetime start of year"),  # noqa: DTZ001
        pytest.param(datetime(2000, 12, 31), 366, id="datetime end of leap year"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1999, 12, 31), 365, id="date end of non-leap year"),
        pytest.param(date(2000, 1, 1), 1, id="date start of year"),
        pytest.param(date(2000, 12, 31), 366, id="date end of leap year"),
    ],
)
def test_should_extract_day_of_year(value: datetime | date | None, expected: int | None) -> None:
    type_if_none = DataTypes.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.day_of_year(), expected, type_if_none=type_if_none if value is None else None
    )


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Datetime()).dt.day_of_year()
    assert_cell_has_type(result, DataTypes.Int16())
