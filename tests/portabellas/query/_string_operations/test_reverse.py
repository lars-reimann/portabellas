import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("", "", id="empty"),
        pytest.param("abc", "cba", id="non-empty"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_reverse_string(value: str | None, expected: str | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.str.reverse(), expected, type_if_none=DataType.String())
