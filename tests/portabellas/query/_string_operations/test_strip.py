import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "characters", "expected"),
    [
        pytest.param("", " ", "", id="empty"),
        pytest.param("~ a ~", "", "~ a ~", id="non-empty (empty characters)"),
        pytest.param("~ a ~", "~", " a ", id="non-empty (one character)"),
        pytest.param("~ a ~", "~ ", "a", id="non-empty (multiple characters)"),
        pytest.param(None, " ", None, id="None as string"),
        pytest.param(" \na\n ", None, "a", id="None as characters"),
        pytest.param(None, None, None, id="None as both"),
    ],
)
class TestShouldStrip:
    def test_plain_arguments(self, value: str | None, characters: str | None, expected: bool | None) -> None:
        from tests.helpers import assert_cell_operation_works

        assert_cell_operation_works(
            value,
            lambda cell: cell.str.strip(characters=characters),
            expected,
            type_if_none=DataType.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, characters: str | None, expected: bool | None) -> None:
        from tests.helpers import assert_cell_operation_works

        assert_cell_operation_works(
            value,
            lambda cell: cell.str.strip(
                characters=Cell.constant(characters),
            ),
            expected,
            type_if_none=DataType.String(),
        )
