import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "suffix", "expected"),
    [
        pytest.param("", "", True, id="empty string, empty suffix"),
        pytest.param("", "c", False, id="empty string, non-empty suffix"),
        pytest.param("abc", "", True, id="non-empty string, empty suffix"),
        pytest.param("abc", "c", True, id="correct suffix"),
        pytest.param("abc", "abc", True, id="suffix equal to string"),
        pytest.param("abc", "d", False, id="incorrect suffix"),
        pytest.param(None, "", None, id="None as string"),
        pytest.param("abc", None, None, id="None as suffix"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldCheckIfStringEndsWithSuffix:
    def test_plain_arguments(self, value: str | None, suffix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.ends_with(suffix),
            expected,
            type_if_none=DataType.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, suffix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.ends_with(
                Cell.constant(suffix),
            ),
            expected,
            type_if_none=DataType.String(),
        )
