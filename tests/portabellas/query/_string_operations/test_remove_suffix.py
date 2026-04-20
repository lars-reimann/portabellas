import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "suffix", "expected"),
    [
        pytest.param("", " ", "", id="empty"),
        pytest.param("~ a ~", "", "~ a ~", id="empty suffix"),
        pytest.param("~ a ~", " ~", "~ a", id="non-empty (has suffix)"),
        pytest.param("~ a ~", "~ ", "~ a ~", id="non-empty (does not have suffix)"),
        pytest.param(None, " ", None, id="None as string"),
        pytest.param("~ a ~", None, None, id="None as suffix"),
        pytest.param(None, None, None, id="None as both"),
    ],
)
class TestShouldRemoveSuffix:
    def test_plain_arguments(self, value: str | None, suffix: str | None, expected: bool | None) -> None:
        from tests.helpers import assert_cell_operation_works

        assert_cell_operation_works(
            value,
            lambda cell: cell.str.remove_suffix(suffix),
            expected,
            type_if_none=DataType.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, suffix: str | None, expected: bool | None) -> None:
        from tests.helpers import assert_cell_operation_works

        assert_cell_operation_works(
            value,
            lambda cell: cell.str.remove_suffix(
                Cell.constant(suffix, type=DataType.String()),
            ),
            expected,
            type_if_none=DataType.String(),
        )
