import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works

E = math.e


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(1, 0, id="0"),
        pytest.param(0.5 * (E + 1 / E), 1, id="1"),
        pytest.param(0.5 * math.sqrt(5), math.log((1 + math.sqrt(5)) / 2), id="ln of golden ratio"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_inverse_hyperbolic_cosine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.acosh(), expected, type_if_none=DataType.Float64())
