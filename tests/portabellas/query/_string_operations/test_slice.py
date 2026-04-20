import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("value", "start", "length", "expected"),
    [
        pytest.param("", 0, None, "", id="empty"),
        pytest.param("abc", 0, None, "abc", id="non-negative start in bounds"),
        pytest.param("abc", 10, None, "", id="non-negative start out of bounds"),
        pytest.param("abc", -1, None, "c", id="negative start in bounds"),
        pytest.param("abc", -10, None, "abc", id="negative start out of bounds"),
        pytest.param("abc", 0, 1, "a", id="non-negative length in bounds"),
        pytest.param("abc", 0, 10, "abc", id="non-negative length out of bounds"),
        pytest.param(None, 0, 1, None, id="None as string"),
        pytest.param("abc", None, 1, None, id="None as start"),
        pytest.param(None, None, None, None, id="None for all"),
    ],
)
class TestShouldSliceCharacters:
    def test_plain_arguments(
        self,
        value: str | None,
        start: int | None,
        length: int | None,
        expected: bool | None,
    ) -> None:
        from tests.helpers import assert_cell_operation_works

        assert_cell_operation_works(
            value,
            lambda cell: cell.str.slice(start=start, length=length),
            expected,
            type_if_none=DataType.String(),
        )

    def test_arguments_wrapped_in_cell(
        self,
        value: str | None,
        start: int | None,
        length: int | None,
        expected: bool | None,
    ) -> None:
        from tests.helpers import assert_cell_operation_works

        assert_cell_operation_works(
            value,
            lambda cell: cell.str.slice(
                start=Cell.constant(start),
                length=Cell.constant(length),
            ),
            expected,
            type_if_none=DataType.String(),
        )


def test_should_raise_for_negative_length() -> None:
    column = Column("a", [1])
    with pytest.raises(OutOfBoundsError):
        column.map(lambda cell: cell.str.slice(length=-1))
