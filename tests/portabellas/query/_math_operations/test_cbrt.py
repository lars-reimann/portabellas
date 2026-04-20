import pytest

from tests.helpers import assert_cell_operation_works


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
    assert_cell_operation_works(value, lambda cell: cell.math.cbrt(), expected)
