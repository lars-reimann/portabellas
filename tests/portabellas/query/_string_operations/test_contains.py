import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "substring", "expected"),
    [
        pytest.param("", "", True, id="empty string, empty substring"),
        pytest.param("", "c", False, id="empty string, non-empty substring"),
        pytest.param("abc", "", True, id="non-empty string, empty substring"),
        pytest.param("abc", "c", True, id="correct substring"),
        pytest.param("abc", "abc", True, id="substring equal to string"),
        pytest.param("abc", "d", False, id="incorrect substring"),
        pytest.param(None, "", None, id="None as string"),
        pytest.param("abc", None, None, id="None as substring"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldCheckIfStringContainsSubstring:
    def test_plain_arguments(self, value: str | None, substring: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.contains(substring),
            expected,
            type_if_none=DataType.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, substring: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.contains(
                Cell.constant(substring),
            ),
            expected,
            type_if_none=DataType.String(),
        )
