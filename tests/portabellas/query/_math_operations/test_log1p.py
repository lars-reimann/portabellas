import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(0, 0.0, id="0"),
        pytest.param(1e-15, 1e-15, id="near-zero"),
        pytest.param(1, 0.6931471805599453, id="1"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_log1p(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.log1p(), expected, type_if_none=DataTypes.Float64())
