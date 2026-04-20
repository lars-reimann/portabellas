import pytest

from portabellas import Column
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType


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
    from tests.helpers import assert_cell_operation_works

    assert_cell_operation_works(
        value,
        lambda cell: cell.str.pad_start(length, character=character),
        expected,
        type_if_none=DataType.String(),
    )


def test_should_raise_if_length_is_out_of_bounds() -> None:
    column = Column("col1", [1])
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
    column = Column("col1", [1])
    with pytest.raises(ValueError, match=r"Can only pad with a single character\."):
        column.map(lambda cell: cell.str.pad_start(1, character=character))
