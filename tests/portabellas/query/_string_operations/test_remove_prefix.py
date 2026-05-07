import pytest

from portabellas.containers import Cell
from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "prefix", "expected"),
    [
        pytest.param("", " ", "", id="empty"),
        pytest.param("~ a ~", "", "~ a ~", id="empty prefix"),
        pytest.param("~ a ~", "~ ", "a ~", id="non-empty (has prefix)"),
        pytest.param("~ a ~", " ~", "~ a ~", id="non-empty (does not have prefix)"),
        pytest.param(None, " ", None, id="None as string"),
        pytest.param("~ a ~", None, None, id="None as prefix"),
        pytest.param(None, None, None, id="None as both"),
    ],
)
class TestShouldRemovePrefix:
    def test_plain_arguments(self, value: str | None, prefix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.remove_prefix(prefix),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, prefix: str | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.remove_prefix(
                Cell.constant(prefix, type=DataTypes.String()),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.String()).str.remove_prefix("a")
    assert_cell_has_type(result, DataTypes.String())
