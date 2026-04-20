import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="0"),
        pytest.param(-1, -0.5 * (math.e - 1 / math.e), id="-1"),
        pytest.param(1, 0.5 * (math.e - 1 / math.e), id="1"),
        pytest.param(math.log((1 + math.sqrt(5)) / 2), 0.5, id="ln of golden ratio"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_hyperbolic_sine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.sinh(), expected, type_if_none=DataType.Float64())
