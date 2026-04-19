from datetime import date

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.containers._cell._cell import ConvertibleToIntCell
from portabellas.exceptions import LazyComputationError
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("year", "month", "day", "expected"),
    [
        pytest.param(1, 2, 3, date(1, 2, 3), id="int components"),
        pytest.param(Cell.constant(1), Cell.constant(2), Cell.constant(3), date(1, 2, 3), id="cell components"),
        pytest.param(None, 2, 3, None, id="year is None"),
        pytest.param(1, None, 3, None, id="month is None"),
        pytest.param(1, 2, None, None, id="day is None"),
    ],
)
def test_should_return_date(
    year: ConvertibleToIntCell,
    month: ConvertibleToIntCell,
    day: ConvertibleToIntCell,
    expected: date | None,
) -> None:
    assert_cell_operation_works(None, lambda _: Cell.date(year, month, day), expected)


@pytest.mark.parametrize(
    ("year", "month", "day"),
    [
        pytest.param(1, 0, 3, id="month is too low"),
        pytest.param(1, 13, 3, id="month is too high"),
        pytest.param(1, 2, 0, id="day is too low"),
        pytest.param(1, 2, 32, id="day is too high"),
    ],
)
def test_should_raise_for_invalid_components(
    year: ConvertibleToIntCell,
    month: ConvertibleToIntCell,
    day: ConvertibleToIntCell,
) -> None:
    column = Column("col1", [None])
    with pytest.raises(LazyComputationError):
        column.map(lambda _: Cell.date(year, month, day)).get_value(0)
