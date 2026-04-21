import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "separator", "expected"),
    [
        pytest.param(["a", "b", "c"], "-", "a-b-c", id="hyphen separator"),
        pytest.param(["a", "b", "c"], "", "abc", id="empty separator"),
        pytest.param(["x"], ",", "x", id="single element"),
        pytest.param(None, ",", None, id="None list"),
    ],
)
class TestShouldJoinListElements:
    def test_plain_arguments(self, value: list | None, separator: str, expected: str | None) -> None:
        column = Column("a", [value], type=DataType.List(DataType.String()))
        result = column.map(lambda cell: cell.list.join(separator))
        assert result[0] == expected

    def test_arguments_wrapped_in_cell(self, value: list | None, separator: str, expected: str | None) -> None:
        column = Column("a", [value], type=DataType.List(DataType.String()))
        result = column.map(lambda cell: cell.list.join(Cell.constant(separator)))
        assert result[0] == expected
