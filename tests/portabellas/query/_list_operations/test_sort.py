import pytest

from portabellas import Column
from portabellas.typing import DataType


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
    column = Column("a", [value], type=DataType.List(DataType.Int64()))
    result = column.map(lambda cell: cell.list.sort(descending=descending))
    actual = result[0]
    if expected is None:
        assert actual is None
    else:
        assert actual.to_list() == expected
