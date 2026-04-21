from datetime import date, datetime

import pytest

from portabellas import Column
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "format_", "expected"),
    [
        pytest.param(
            datetime(1999, 12, 31),  # noqa: DTZ001
            "iso",
            "1999-12-31T00:00:00.000000",
            id="datetime iso",
        ),
        pytest.param(
            datetime(2000, 1, 1, 12, 30, 0),  # noqa: DTZ001
            "iso",
            "2000-01-01T12:30:00.000000",
            id="datetime iso noon-thirty",
        ),
        pytest.param(
            None,
            "iso",
            None,
            id="None datetime iso",
        ),
        pytest.param(
            datetime(1999, 12, 31),  # noqa: DTZ001
            "{DOW-short} {D}-{M-short}-{Y} {h12}:{m}:{s} {AM/PM}",
            "Fri 31-Dec-1999 12:00:00 AM",
            id="datetime custom format",
        ),
        pytest.param(
            date(1999, 12, 31),
            "iso",
            "1999-12-31",
            id="date iso",
        ),
        pytest.param(
            date(2000, 1, 1),
            "iso",
            "2000-01-01",
            id="date iso 2",
        ),
        pytest.param(
            date(1999, 12, 31),
            "{M}/{D}/{Y}",
            "12/31/1999",
            id="date custom format",
        ),
    ],
)
def test_should_convert_to_string(
    value: datetime | date | None,
    format_: str,
    expected: str | None,
) -> None:
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value,
        lambda cell: cell.dt.to_string(format=format_),
        expected,
        type_if_none=type_if_none if value is None else None,
    )


def test_should_raise_for_invalid_format() -> None:
    column = Column("a", [datetime(2000, 1, 1)])  # noqa: DTZ001
    with pytest.raises(ValueError, match="Invalid specifier"):
        column.map(lambda cell: cell.dt.to_string(format="{invalid}"))
