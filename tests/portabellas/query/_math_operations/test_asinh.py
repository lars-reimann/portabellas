import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="0"),
        pytest.param(-1, -0.881373587019543, id="-1"),
        pytest.param(1, 0.881373587019543, id="1"),
        pytest.param(0.5, math.asinh(0.5), id="0.5"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_inverse_hyperbolic_sine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.asinh(), expected, type_if_none=DataType.Float64())
