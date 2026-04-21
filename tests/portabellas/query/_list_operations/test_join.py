import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "separator", "expected"),
    [
        pytest.param(["a", "b", "c"], "-", "a-b-c", id="hyphen separator"),
        pytest.param(["a", "b", "c"], "", "abc", id="empty separator"),
        pytest.param(["x"], ",", "x", id="single element"),
        pytest.param(None, ",", None, id="None list"),
        pytest.param(["a", "b", "c"], None, None, id="None separator"),
    ],
)
class TestShouldJoinListElements:
    def test_plain_arguments(self, value: list | None, separator: str | None, expected: str | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.join(separator),
            expected,
            type_=DataType.List(DataType.String()),
        )

    def test_arguments_wrapped_in_cell(self, value: list | None, separator: str | None, expected: str | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.join(Cell.constant(separator, type=DataType.String())),
            expected,
            type_=DataType.List(DataType.String()),
        )
