import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 1, id="positive integers"),
        pytest.param([3, 1, 2], 1, id="unsorted integers"),
        pytest.param([-5, -1, -3], -5, id="negative integers"),
        pytest.param([], None, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_get_min_value(value: list | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.min(),
        expected,
        type_=DataType.List(DataType.Int64()),
    )
