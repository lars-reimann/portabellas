import math

import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "base", "expected"),
    [
        pytest.param(0, math.e, -math.inf, id="base e - 0"),
        pytest.param(1, math.e, 0, id="base e - 1"),
        pytest.param(math.e, math.e, 1, id="base e - e"),
        pytest.param(0, 10, -math.inf, id="base 10 - 0"),
        pytest.param(1, 10, 0, id="base 10 - 1"),
        pytest.param(10, 10, 1, id="base 10 - 10"),
        pytest.param(100, 10, 2, id="base 10 - 100"),
        pytest.param(None, 10, None, id="None"),
    ],
)
def test_should_return_logarithm_to_given_base(value: float | None, base: int, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.log(base), expected, type_if_none=DataType.Float64())


@pytest.mark.parametrize(
    "base",
    [
        pytest.param(-1, id="negative"),
        pytest.param(0, id="zero"),
        pytest.param(1, id="one"),
    ],
)
def test_should_raise_if_base_is_out_of_bounds(base: int) -> None:
    column = Column("a", [1])
    with pytest.raises((OutOfBoundsError, ValueError), match="base"):
        column.map(lambda cell: cell.math.log(base))
