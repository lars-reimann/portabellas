import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "descending", "expected"),
    [
        pytest.param([3, 1, 2], False, [1, 2, 3], id="ascending"),
        pytest.param([3, 1, 2], True, [3, 2, 1], id="descending"),
        pytest.param([], False, [], id="empty list ascending"),
        pytest.param([], True, [], id="empty list descending"),
        pytest.param(None, False, None, id="None list"),
    ],
)
def test_should_sort_list(value: list | None, descending: bool, expected: list | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.sort(descending=descending),
        expected,
        type_=DataType.List(DataType.Int64()),
    )
