import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param("", "", id="empty"),
        pytest.param("abc", "cba", id="non-empty"),
        pytest.param(None, None, id="None"),
    ],
)
def test_should_reverse_string(value: str | None, expected: str | None) -> None:
    assert_cell_operation_works(value, lambda cell: cell.str.reverse(), expected, type_if_none=DataTypes.String())


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.String()).str.reverse()
    assert_cell_has_type(result, DataTypes.String())
