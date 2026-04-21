import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 3, id="positive integers"),
        pytest.param([3, 1, 2], 3, id="unsorted integers"),
        pytest.param([-5, -1, -3], -1, id="negative integers"),
        pytest.param([], None, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_get_max_value(value: list | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.max(),
        expected,
        type_=DataType.List(DataType.Int64()),
    )
