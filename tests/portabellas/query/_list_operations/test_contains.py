import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "item", "expected"),
    [
        pytest.param([1, 2, 3], 2, True, id="item in list"),
        pytest.param([1, 2, 3], 4, False, id="item not in list"),
        pytest.param([], 1, False, id="empty list"),
        pytest.param(None, 1, None, id="None list"),
    ],
)
class TestShouldCheckIfListContainsItem:
    def test_plain_arguments(self, value: list | None, item: int, expected: bool | None) -> None:
        column = Column("a", [value], type=DataType.List(DataType.Int64()))
        result = column.map(lambda cell: cell.list.contains(item))
        assert result[0] == expected

    def test_arguments_wrapped_in_cell(self, value: list | None, item: int, expected: bool | None) -> None:
        column = Column("a", [value], type=DataType.List(DataType.Int64()))
        result = column.map(lambda cell: cell.list.contains(Cell.constant(item)))
        assert result[0] == expected
