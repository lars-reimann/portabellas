import pytest

from portabellas import Column
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 1, id="non-empty list"),
        pytest.param([], None, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_get_first_element(value: list | None, expected: int | None) -> None:
    column = Column("a", [value], type=DataType.List(DataType.Int64()))
    result = column.map(lambda cell: cell.list.first())
    assert result[0] == expected
