from collections.abc import Callable

import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
)


@pytest.mark.parametrize(
    ("value", "length", "character", "expected"),
    [
        pytest.param("", 0, "a", "", id="empty (length 0)"),
        pytest.param("", 1, "a", "a", id="empty (length 1)"),
        pytest.param("b", 2, "a", "ab", id="non-empty (shorter length)"),
        pytest.param("bc", 2, "a", "bc", id="non-empty (same length)"),
        pytest.param("abc", 2, "a", "abc", id="non-empty (longer length)"),
        pytest.param(None, 1, " ", None, id="None"),
    ],
)
def test_should_pad_start(value: str | None, length: int, character: str, expected: bool | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.str.pad_start(length, character=character),
        expected,
        type_if_none=DataTypes.String(),
    )


def test_should_raise_if_length_is_out_of_bounds() -> None:
    column = Column("col1", ["a"])
    with pytest.raises(OutOfBoundsError):
        column.map(lambda cell: cell.str.pad_start(-1))


@pytest.mark.parametrize(
    "character",
    [
        pytest.param("", id="empty string"),
        pytest.param("ab", id="multiple characters"),
    ],
)
def test_should_raise_if_char_is_not_single_character(character: str) -> None:
    column = Column("col1", ["a"])
    with pytest.raises(ValueError, match=r"Can only pad with a single character\."):
        column.map(lambda cell: cell.str.pad_start(1, character=character))


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.String(), lambda cell: cell.str.pad_start(1), DataTypes.String(), id="string"),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        assert_cell_type_matches_polars(given_type, operation, expected_type)
