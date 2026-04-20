import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 1, id="0 deg"),
        pytest.param(math.pi / 2, 0, id="90 deg"),
        pytest.param(math.pi, -1, id="180 deg"),
        pytest.param(3 * math.pi / 2, 0, id="270 deg"),
        pytest.param(2 * math.pi, 1, id="360 deg"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_cosine(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.cos(), expected, type_if_none=DataType.Float64())
