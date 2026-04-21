import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "substring", "expected"),
    [
        pytest.param("", "", 0, id="empty string, empty substring"),
        pytest.param("", "c", None, id="empty string, non-empty substring"),
        pytest.param("abc", "", 0, id="non-empty string, empty substring"),
        pytest.param("abc", "c", 2, id="correct substring"),
        pytest.param("abc", "abc", 0, id="substring equal to string"),
        pytest.param("abc", "d", None, id="incorrect substring"),
        pytest.param(None, "", None, id="None as string"),
        pytest.param("abc", None, None, id="None as substring"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldGetIndexOfSubstring:
    def test_plain_arguments(self, value: str | None, substring: str | None, expected: int | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.index_of(substring),
            expected,
            type_if_none=DataType.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, substring: str | None, expected: int | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.index_of(
                Cell.constant(substring),
            ),
            expected,
            type_if_none=DataType.String(),
        )
