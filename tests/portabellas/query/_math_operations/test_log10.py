import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, -math.inf, id="0"),
        pytest.param(1, 0, id="1"),
        pytest.param(10, 1, id="10"),
        pytest.param(100, 2, id="100"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_common_logarithm(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.log10(), expected, type_if_none=DataType.Float64())
