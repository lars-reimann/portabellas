import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works

E = math.e


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 1, id="0"),
        pytest.param(-1, 0.5 * (E + 1 / E), id="-1"),
        pytest.param(1, 0.5 * (E + 1 / E), id="1"),
        pytest.param(math.log((1 + math.sqrt(5)) / 2), 0.5 * math.sqrt(5), id="ln of golden ratio"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_hyperbolic_cosine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.cosh(), expected, type_if_none=DataType.Float64())
