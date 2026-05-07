from datetime import date, datetime

import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(datetime(1999, 12, 31), 20, id="datetime 1999"),  # noqa: DTZ001
        pytest.param(datetime(2000, 1, 1), 20, id="datetime 2000"),  # noqa: DTZ001
        pytest.param(datetime(2001, 1, 1), 21, id="datetime 2001"),  # noqa: DTZ001
        pytest.param(None, None, id="None datetime"),
        pytest.param(date(1999, 12, 31), 20, id="date 1999"),
        pytest.param(date(2000, 1, 1), 20, id="date 2000"),
        pytest.param(date(2001, 1, 1), 21, id="date 2001"),
    ],
)
def test_should_extract_century(value: datetime | date | None, expected: int | None) -> None:
    type_if_none = DataTypes.Datetime()
    assert_cell_operation_works(
        value, lambda cell: cell.dt.century(), expected, type_if_none=type_if_none if value is None else None
    )


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Datetime()).dt.century()
    assert_cell_has_type(result, DataTypes.Int32())
