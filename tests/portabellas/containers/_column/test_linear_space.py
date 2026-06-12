import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataTypes


def test_should_store_the_name() -> None:
    column = Column.linear_space("bin", 0.0, 1.0, 11)
    assert column.name == "bin"


@pytest.mark.parametrize(
    ("start", "end", "count", "expected"),
    [
        pytest.param(0.0, 10.0, 2, [0.0, 10.0], id="two values"),
        pytest.param(0.0, 1.0, 11, [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], id="evenly spaced"),
        pytest.param(0.0, 10.0, 3, [0.0, 5.0, 10.0], id="three values"),
    ],
)
def test_should_store_the_data(start: float, end: float, count: int, expected: list[float]) -> None:
    column = Column.linear_space("col", start, end, count)
    assert list(column) == pytest.approx(expected)


def test_should_have_float64_type() -> None:
    column = Column.linear_space("col", 0.0, 1.0, 11)
    assert column.type == DataTypes.Float64()


def test_should_raise_for_count_below_2() -> None:
    with pytest.raises(OutOfBoundsError):
        Column.linear_space("col", 0.0, 1.0, 1)
