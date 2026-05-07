import math

import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type

E = math.e


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0, id="0"),
        pytest.param(-(E - 1 / E) / (E + 1 / E), -1, id="-1"),
        pytest.param((E - 1 / E) / (E + 1 / E), 1, id="1"),
        pytest.param(1 / math.sqrt(5), math.log((1 + math.sqrt(5)) / 2), id="ln of golden ratio"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_inverse_hyperbolic_tangent(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.atanh(), expected, type_if_none=DataTypes.Float64())


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Int64()).math.atanh()
    assert_cell_has_type(result, DataTypes.Float64())
