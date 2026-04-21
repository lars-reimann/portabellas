import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "index", "expected"),
    [
        pytest.param([1, 2, 3], 0, 1, id="first element"),
        pytest.param([1, 2, 3], 2, 3, id="last element"),
        pytest.param([1, 2, 3], 5, None, id="out of bounds"),
        pytest.param([], 0, None, id="empty list"),
        pytest.param(None, 0, None, id="None list"),
    ],
)
class TestShouldGetElementAtIndex:
    def test_plain_arguments(self, value: list | None, index: int, expected: int | None) -> None:
        column = Column("a", [value], type=DataType.List(DataType.Int64()))
        result = column.map(lambda cell: cell.list.get(index))
        assert result[0] == expected

    def test_arguments_wrapped_in_cell(self, value: list | None, index: int, expected: int | None) -> None:
        column = Column("a", [value], type=DataType.List(DataType.Int64()))
        result = column.map(lambda cell: cell.list.get(Cell.constant(index)))
        assert result[0] == expected
