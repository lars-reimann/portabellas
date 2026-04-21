from datetime import date, datetime

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "replace_kwargs", "expected"),
    [
        pytest.param(
            datetime(2000, 1, 1),  # noqa: DTZ001
            {"month": 2, "day": 2, "hour": 2},
            datetime(2000, 2, 2, 2, 0, 0),  # noqa: DTZ001
            id="datetime replace month day hour",
        ),
        pytest.param(
            datetime(2000, 1, 1),  # noqa: DTZ001
            {"year": 2025},
            datetime(2025, 1, 1),  # noqa: DTZ001
            id="datetime replace year",
        ),
        pytest.param(
            None,
            {"month": 2},
            None,
            id="None datetime",
        ),
        pytest.param(
            date(2000, 1, 1),
            {"month": 2, "day": 2, "hour": 2},
            date(2000, 2, 2),
            id="date replace month day (hour ignored)",
        ),
    ],
)
def test_should_replace_components(
    value: datetime | date | None,
    replace_kwargs: dict,
    expected: datetime | date | None,
) -> None:
    type_if_none = DataType.Datetime()
    assert_cell_operation_works(
        value,
        lambda cell: cell.dt.replace(**replace_kwargs),
        expected,
        type_if_none=type_if_none if value is None else None,
    )
