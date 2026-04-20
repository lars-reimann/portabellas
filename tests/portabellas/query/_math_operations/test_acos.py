import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(-1.0, math.pi, id="-1"),
        pytest.param(0, math.pi / 2, id="0"),
        pytest.param(1, 0, id="1"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_inverse_cosine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.acos(), expected, type_if_none=DataType.Float64())
