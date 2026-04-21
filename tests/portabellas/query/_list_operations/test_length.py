import pytest

from portabellas import Column
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 3, id="three elements"),
        pytest.param([1], 1, id="one element"),
        pytest.param([], 0, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_get_list_length(value: list | None, expected: int | None) -> None:
    column = Column("a", [value], type=DataType.List(DataType.Int64()))
    result = column.map(lambda cell: cell.list.length())
    assert result[0] == expected
