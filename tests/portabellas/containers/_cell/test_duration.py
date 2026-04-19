from datetime import timedelta

import pytest

from portabellas.containers import Cell
from portabellas.containers._cell._cell import ConvertibleToIntCell
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("weeks", "days", "hours", "minutes", "seconds", "milliseconds", "microseconds", "expected"),
    [
        pytest.param(
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            timedelta(weeks=1, days=2, hours=3, minutes=4, seconds=5, milliseconds=6, microseconds=7),
            id="positive int components",
        ),
        pytest.param(
            -1,
            -2,
            -3,
            -4,
            -5,
            -6,
            -7,
            timedelta(weeks=-1, days=-2, hours=-3, minutes=-4, seconds=-5, milliseconds=-6, microseconds=-7),
            id="negative int components",
        ),
        pytest.param(
            Cell.constant(1),
            Cell.constant(2),
            Cell.constant(3),
            Cell.constant(4),
            Cell.constant(5),
            Cell.constant(6),
            Cell.constant(7),
            timedelta(weeks=1, days=2, hours=3, minutes=4, seconds=5, milliseconds=6, microseconds=7),
            id="cell components",
        ),
        pytest.param(None, 2, 3, 4, 5, 6, 7, None, id="weeks is None"),
        pytest.param(1, None, 3, 4, 5, 6, 7, None, id="days is None"),
        pytest.param(1, 2, None, 4, 5, 6, 7, None, id="hours is None"),
        pytest.param(1, 2, 3, None, 5, 6, 7, None, id="minutes is None"),
        pytest.param(1, 2, 3, 4, None, 6, 7, None, id="seconds is None"),
        pytest.param(1, 2, 3, 4, 5, None, 7, None, id="milliseconds is None"),
        pytest.param(1, 2, 3, 4, 5, 6, None, None, id="microseconds is None"),
    ],
)
def test_should_return_duration(
    weeks: ConvertibleToIntCell,
    days: ConvertibleToIntCell,
    hours: ConvertibleToIntCell,
    minutes: ConvertibleToIntCell,
    seconds: ConvertibleToIntCell,
    milliseconds: ConvertibleToIntCell,
    microseconds: ConvertibleToIntCell,
    expected: timedelta | None,
) -> None:
    assert_cell_operation_works(
        None,
        lambda _: Cell.duration(
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            milliseconds=milliseconds,
            microseconds=microseconds,
        ),
        expected,
    )
