import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "prefix", "expected"),
    [
        pytest.param("", "", True, id="empty string, empty prefix"),
        pytest.param("", "a", False, id="empty string, non-empty prefix"),
        pytest.param("abc", "", True, id="non-empty string, empty prefix"),
        pytest.param("abc", "a", True, id="correct prefix"),
        pytest.param("abc", "abc", True, id="prefix equal to string"),
        pytest.param("abc", "d", False, id="incorrect prefix"),
        pytest.param(None, "", None, id="None as string"),
        pytest.param("abc", None, None, id="None as prefix"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldCheckIfStringStartsWithPrefix:
    def test_plain_arguments(self, value: str | None, prefix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.starts_with(prefix),
            expected,
            type_if_none=DataType.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, prefix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.starts_with(
                Cell.constant(prefix),
            ),
            expected,
            type_if_none=DataType.String(),
        )
