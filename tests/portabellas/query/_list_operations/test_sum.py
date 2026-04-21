import pytest

from portabellas import Column
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 6, id="positive integers"),
        pytest.param([10], 10, id="single element"),
        pytest.param([], 0, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_sum_list_elements(value: list | None, expected: int | None) -> None:
    column = Column("a", [value], type=DataType.List(DataType.Int64()))
    result = column.map(lambda cell: cell.list.sum())
    assert result[0] == expected
