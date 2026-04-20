import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="0 deg"),
        pytest.param(22.5, math.pi / 8, id="22.5 deg"),
        pytest.param(90, math.pi / 2, id="90 deg"),
        pytest.param(180, math.pi, id="180 deg"),
        pytest.param(270, 3 * math.pi / 2, id="270 deg"),
        pytest.param(360, 2 * math.pi, id="360 deg"),
        pytest.param(720, 4 * math.pi, id="720 deg"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_convert_degrees_to_radians(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(
        value, lambda cell: cell.math.degrees_to_radians(), expected, type_if_none=DataType.Float64()
    )
