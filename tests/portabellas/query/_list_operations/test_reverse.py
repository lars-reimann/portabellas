import pytest

from portabellas import Column
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], [3, 2, 1], id="non-empty list"),
        pytest.param([], [], id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_reverse_list(value: list | None, expected: list | None) -> None:
    column = Column("a", [value], type=DataType.List(DataType.Int64()))
    result = column.map(lambda cell: cell.list.reverse())
    actual = result[0]
    if expected is None:
        assert actual is None
    else:
        assert actual.to_list() == expected
