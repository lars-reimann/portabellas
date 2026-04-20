import math

import pytest

from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(-1, math.nan, id="-1"),
        pytest.param(0, 0, id="0"),
        pytest.param(1, 1, id="1"),
        pytest.param(2.25, 1.5, id="square of 1.5"),
        pytest.param(4, 2, id="square of 2"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_return_square_root(value: float | None, expected: float | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.math.sqrt(), expected)
