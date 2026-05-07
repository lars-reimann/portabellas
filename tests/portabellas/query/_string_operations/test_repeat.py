import pytest

from portabellas import Column
from portabellas.containers import Cell
from portabellas.exceptions import OutOfBoundsError
from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "count", "expected"),
    [
        pytest.param("", 1, "", id="empty"),
        pytest.param("a", 0, "", id="zero count"),
        pytest.param("a", 1, "a", id="non-empty (count 1)"),
        pytest.param("a", 2, "aa", id="non-empty (count 2)"),
        pytest.param(None, 0, "", id="None as string (count 0)"),
        pytest.param(None, 1, None, id="None as string (count 1)"),
        pytest.param("", None, None, id="None as count"),
        pytest.param(None, None, None, id="None for both"),
    ],
)
class TestShouldRepeatString:
    def test_plain_arguments(self, value: str | None, count: int | None, expected: str | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.repeat(count),
            expected,
            type_if_none=DataTypes.String(),
        )

    def test_arguments_wrapped_in_cell(self, value: str | None, count: int | None, expected: str | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.str.repeat(
                Cell.constant(count),
            ),
            expected,
            type_if_none=DataTypes.String(),
        )


def test_should_raise_if_count_is_out_of_bounds() -> None:
    column = Column("a", ["a"])
    with pytest.raises(OutOfBoundsError):
        column.map(lambda cell: cell.str.repeat(-1))


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.String()).str.repeat(1)
    assert_cell_has_type(result, DataTypes.String())
