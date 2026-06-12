import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataTypes


def test_should_store_the_name() -> None:
    column = Column.int_range("id", 0, 5)
    assert column.name == "id"


@pytest.mark.parametrize(
    ("start", "end", "step", "expected"),
    [
        pytest.param(0, 0, 1, [], id="empty range"),
        pytest.param(0, 5, 1, [0, 1, 2, 3, 4], id="step 1"),
        pytest.param(0, 10, 2, [0, 2, 4, 6, 8], id="larger positive step"),
        pytest.param(5, 0, -1, [5, 4, 3, 2, 1], id="step -1"),
        pytest.param(10, 0, -3, [10, 7, 4, 1], id="larger negative step"),
    ],
)
def test_should_store_the_data(start: int, end: int, step: int, expected: list[int]) -> None:
    column = Column.int_range("col", start, end, step=step)
    assert list(column) == expected


def test_should_have_int64_type() -> None:
    column = Column.int_range("col", 0, 5)
    assert column.type == DataTypes.Int64()


def test_should_raise_for_zero_step() -> None:
    with pytest.raises(OutOfBoundsError):
        Column.int_range("col", 0, 5, step=0)
