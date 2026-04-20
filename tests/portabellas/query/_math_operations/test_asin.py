import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(-1.0, -math.pi / 2, id="-90 deg"),
        pytest.param(0, 0, id="0 deg"),
        pytest.param(1, math.pi / 2, id="90 deg"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_inverse_sine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.asin(), expected, type_if_none=DataType.Float64())
