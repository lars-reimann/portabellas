from datetime import time

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.containers._cell._cell import ConvertibleToIntCell
from portabellas.exceptions import LazyComputationError
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("hour", "minute", "second", "microsecond", "expected"),
    [
        pytest.param(1, 2, 3, 4, time(1, 2, 3, 4), id="int components"),
        pytest.param(
            Cell.constant(1),
            Cell.constant(2),
            Cell.constant(3),
            Cell.constant(4),
            time(1, 2, 3, 4),
            id="cell components",
        ),
        pytest.param(None, 2, 3, 4, None, id="hour is None"),
        pytest.param(1, None, 3, 4, None, id="minute is None"),
        pytest.param(1, 2, None, 4, None, id="second is None"),
        pytest.param(1, 2, 3, None, None, id="microsecond is None"),
    ],
)
def test_should_return_time(
    hour: ConvertibleToIntCell,
    minute: ConvertibleToIntCell,
    second: ConvertibleToIntCell,
    microsecond: ConvertibleToIntCell,
    expected: time | None,
) -> None:
    assert_cell_operation_works(
        None,
        lambda _: Cell.time(hour, minute, second, microsecond=microsecond),
        expected,
    )


@pytest.mark.parametrize(
    ("hour", "minute", "second", "microsecond"),
    [
        pytest.param(-1, 2, 3, 4, id="hour is too low"),
        pytest.param(24, 2, 3, 4, id="hour is too high"),
        pytest.param(1, -1, 3, 4, id="minute is too low"),
        pytest.param(1, 60, 3, 4, id="minute is too high"),
        pytest.param(1, 2, -1, 4, id="second is too low"),
        pytest.param(1, 2, 60, 4, id="second is too high"),
        pytest.param(1, 2, 3, -1, id="microsecond is too low"),
        pytest.param(
            1,
            2,
            3,
            1_000_000,
            marks=pytest.mark.xfail(reason="https://github.com/pola-rs/polars/issues/21664"),
            id="microsecond is too high",
        ),
    ],
)
def test_should_raise_for_invalid_components(
    hour: ConvertibleToIntCell,
    minute: ConvertibleToIntCell,
    second: ConvertibleToIntCell,
    microsecond: ConvertibleToIntCell,
) -> None:
    column = Column("col1", [None])
    with pytest.raises(LazyComputationError):
        column.map(
            lambda _: Cell.time(hour, minute, second, microsecond=microsecond),
        ).get_value(0)
