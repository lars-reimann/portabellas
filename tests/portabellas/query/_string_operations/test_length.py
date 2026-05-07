from collections.abc import Callable

import pytest

from portabellas.containers import Cell
from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


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
        type_if_none=DataTypes.String(),
    )


@pytest.mark.parametrize(
    ("operation", "expected_type"),
    [
        pytest.param(lambda cell: cell.str.length(), DataTypes.UInt32(), id="length"),
        pytest.param(lambda cell: cell.str.length(optimize_for_ascii=True), DataTypes.UInt32(), id="length-ascii"),
    ],
)
def test_should_infer_type(operation: Callable[[Cell], Cell], expected_type: DataTypes.UInt32) -> None:
    result = operation(cell_of_type(DataTypes.String()))
    assert_cell_has_type(result, expected_type)
