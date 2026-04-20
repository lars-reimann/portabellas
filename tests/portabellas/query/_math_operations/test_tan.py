import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="0 deg"),
        pytest.param(math.pi / 4, 1, id="45 deg"),
        pytest.param(math.pi, 0, id="180 deg"),
        pytest.param(3 * math.pi / 4, -1, id="135 deg"),
        pytest.param(2 * math.pi, 0, id="360 deg"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_tangent(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.tan(), expected, type_if_none=DataType.Float64())
