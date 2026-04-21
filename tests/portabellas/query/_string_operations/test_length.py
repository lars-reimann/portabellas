import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "optimize_for_ascii", "expected"),
    [
        pytest.param("", False, 0, id="empty (not optimized)"),
        pytest.param("", True, 0, id="empty (optimized)"),
        pytest.param("abc", False, 3, id="ASCII only (not optimized)"),
        pytest.param("abc", True, 3, id="ASCII only (optimized)"),
        pytest.param("a 🪲", False, 3, id="unicode (not optimized)"),
        pytest.param("a 🪲", True, 6, id="unicode (optimized)"),
        pytest.param(None, False, None, id="None"),
    ],
)
def test_should_get_number_of_characters(value: str | None, optimize_for_ascii: bool, expected: str | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.str.length(optimize_for_ascii=optimize_for_ascii),
        expected,
        type_if_none=DataType.String(),
    )
