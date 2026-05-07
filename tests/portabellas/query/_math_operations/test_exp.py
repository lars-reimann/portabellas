import math

import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 1, id="0"),
        pytest.param(1.0, math.e, id="1"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_exponential(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.exp(), expected, type_if_none=DataTypes.Float64())


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Int64()).math.exp()
    assert_cell_has_type(result, DataTypes.Float64())
