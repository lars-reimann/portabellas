import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "index", "expected"),
    [
        pytest.param([1, 2, 3], 0, 1, id="first element"),
        pytest.param([1, 2, 3], 2, 3, id="last element"),
        pytest.param([1, 2, 3], 5, None, id="positive out of bounds"),
        pytest.param([], 0, None, id="empty list"),
        pytest.param(None, 0, None, id="None list"),
        pytest.param([1, 2, 3], -1, 3, id="negative index last element"),
        pytest.param([1, 2, 3], -2, 2, id="negative index second to last element"),
        pytest.param([1, 2, 3], -4, None, id="negative out of bounds"),
    ],
)
class TestShouldGetElementAtIndex:
    def test_plain_arguments(self, value: list | None, index: int, expected: int | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.get(index),
            expected,
            type_=DataType.List(DataType.Int64()),
        )

    def test_arguments_wrapped_in_cell(self, value: list | None, index: int, expected: int | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.get(Cell.constant(index)),
            expected,
            type_=DataType.List(DataType.Int64()),
        )
