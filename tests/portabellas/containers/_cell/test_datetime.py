from datetime import UTC, datetime

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.containers._cell._cell import ConvertibleToIntCell
from portabellas.exceptions import LazyComputationError
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("year", "month", "day", "hour", "minute", "second", "microsecond", "time_zone", "expected"),
    [
        pytest.param(
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            None,
            datetime(1, 2, 3, 4, 5, 6, 7),  # noqa: DTZ001
            id="int components",
        ),
        pytest.param(
            Cell.constant(1),
            Cell.constant(2),
            Cell.constant(3),
            Cell.constant(4),
            Cell.constant(5),
            Cell.constant(6),
            Cell.constant(7),
            None,
            datetime(1, 2, 3, 4, 5, 6, 7),  # noqa: DTZ001
            id="cell components",
        ),
        pytest.param(None, 2, 3, 4, 5, 6, 7, None, None, id="year is None"),
        pytest.param(1, None, 3, 4, 5, 6, 7, None, None, id="month is None"),
        pytest.param(1, 2, None, 4, 5, 6, 7, None, None, id="day is None"),
        pytest.param(1, 2, 3, None, 5, 6, 7, None, None, id="hour is None"),
        pytest.param(1, 2, 3, 4, None, 6, 7, None, None, id="minute is None"),
        pytest.param(1, 2, 3, 4, 5, None, 7, None, None, id="second is None"),
        pytest.param(1, 2, 3, 4, 5, 6, None, None, None, id="microsecond is None"),
        pytest.param(
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            "UTC",
            datetime(1, 2, 3, 4, 5, 6, 7, tzinfo=UTC),
            id="with time zone",
        ),
    ],
)
def test_should_return_datetime(
    year: ConvertibleToIntCell,
    month: ConvertibleToIntCell,
    day: ConvertibleToIntCell,
    hour: ConvertibleToIntCell,
    minute: ConvertibleToIntCell,
    second: ConvertibleToIntCell,
    microsecond: ConvertibleToIntCell,
    time_zone: str | None,
    expected: datetime | None,
) -> None:
    assert_cell_operation_works(
        None,
        lambda _: Cell.datetime(
            year,
            month,
            day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            time_zone=time_zone,
        ),
        expected,
    )


@pytest.mark.parametrize(
    ("year", "month", "day", "hour", "minute", "second", "microsecond"),
    [
        pytest.param(1, 0, 3, 4, 5, 6, 7, id="month is too low"),
        pytest.param(1, 13, 3, 4, 5, 6, 7, id="month is too high"),
        pytest.param(1, 2, 0, 4, 5, 6, 7, id="day is too low"),
        pytest.param(1, 2, 32, 4, 5, 6, 7, id="day is too high"),
        pytest.param(1, 2, 3, -1, 5, 6, 7, id="hour is too low"),
        pytest.param(1, 2, 3, 24, 5, 6, 7, id="hour is too high"),
        pytest.param(1, 2, 3, 4, -1, 6, 7, id="minute is too low"),
        pytest.param(1, 2, 3, 4, 60, 6, 7, id="minute is too high"),
        pytest.param(1, 2, 3, 4, 5, -1, 7, id="second is too low"),
        pytest.param(1, 2, 3, 4, 5, 60, 7, id="second is too high"),
        pytest.param(1, 2, 3, 4, 5, 6, -1, id="microsecond is too low"),
        pytest.param(
            1,
            2,
            3,
            4,
            5,
            6,
            1_000_000,
            marks=pytest.mark.xfail(reason="https://github.com/pola-rs/polars/issues/21664"),
            id="microsecond is too high",
        ),
    ],
)
def test_should_raise_for_invalid_components(
    year: ConvertibleToIntCell,
    month: ConvertibleToIntCell,
    day: ConvertibleToIntCell,
    hour: ConvertibleToIntCell,
    minute: ConvertibleToIntCell,
    second: ConvertibleToIntCell,
    microsecond: ConvertibleToIntCell,
) -> None:
    column = Column("col1", [None])
    with pytest.raises(LazyComputationError):
        column.transform(
            lambda _: Cell.datetime(year, month, day, hour, minute, second, microsecond=microsecond),
        ).get_value(0)


def test_should_raise_if_time_zone_is_invalid() -> None:
    column = Column("col1", [None])
    with pytest.raises(ValueError, match="Invalid time zone"):
        column.transform(lambda _: Cell.datetime(1, 2, 3, 0, 0, 0, time_zone="invalid"))
