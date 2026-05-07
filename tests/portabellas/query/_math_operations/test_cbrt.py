import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(-1, -1, id="-1"),
        pytest.param(0, 0, id="0"),
        pytest.param(1, 1, id="1"),
        pytest.param(3.375, 1.5, id="cube of float"),
        pytest.param(8, 2, id="cube of int"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_cube_root(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.cbrt(), expected, type_if_none=DataTypes.Float64())


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.Int64()).math.cbrt()
    assert_cell_has_type(result, DataTypes.Float64())
