import math

import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


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
    assert_cell_operation_works(value, lambda cell: cell.math.asin(), expected, type_if_none=DataTypes.Float64())


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Int64()).math.asin()
    assert_cell_has_type(result, DataTypes.Float64())
