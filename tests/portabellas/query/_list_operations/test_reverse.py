import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], [3, 2, 1], id="non-empty list"),
        pytest.param([], [], id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_reverse_list(value: list | None, expected: list | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.reverse(),
        expected,
        type_=DataType.List(DataType.Int64()),
    )
