import math

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="zero int"),
        pytest.param(0.0, 0, id="zero float"),
        pytest.param(10, 10, id="positive int"),
        pytest.param(10.5, 11, id="positive float"),
        pytest.param(-10, -10, id="negative int"),
        pytest.param(-10.5, -10, id="negative float"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_ceiling(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: math.ceil(cell), expected, type_if_none=DataType.Float64())
