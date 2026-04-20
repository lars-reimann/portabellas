import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="0 deg"),
        pytest.param(math.pi / 8, 22.5, id="22.5 deg"),
        pytest.param(math.pi / 2, 90, id="90 deg"),
        pytest.param(math.pi, 180, id="180 deg"),
        pytest.param(3 * math.pi / 2, 270, id="270 deg"),
        pytest.param(2 * math.pi, 360, id="360 deg"),
        pytest.param(4 * math.pi, 720, id="720 deg"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_convert_radians_to_degrees(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(
        value, lambda cell: cell.math.radians_to_degrees(), expected, type_if_none=DataType.Float64()
    )
