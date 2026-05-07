import pytest

from portabellas.containers import Cell
from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "characters", "expected"),
    [
        pytest.param("", " ", "", id="empty"),
        pytest.param("~ a ~", "", "~ a ~", id="non-empty (empty characters)"),
        pytest.param("~ a ~", "~", "~ a ", id="non-empty (one character)"),
        pytest.param("~ a ~", "~ ", "~ a", id="non-empty (multiple characters)"),
        pytest.param(None, " ", None, id="None as string"),
        pytest.param(" \na\n ", None, " \na", id="None as characters"),
        pytest.param(None, None, None, id="None as both"),
    ],
)
class TestShouldStripEnd:
    def test_plain_arguments(self, value: str | None, characters: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.strip_end(characters=characters),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, characters: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.strip_end(
                characters=Cell.constant(characters),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.String()).str.strip_end()
    assert_cell_has_type(result, DataTypes.String())
