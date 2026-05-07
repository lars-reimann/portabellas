import pytest

from portabellas.containers import Cell
from portabellas.typing import DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value", "item", "expected"),
    [
        pytest.param([1, 2, 3], 2, True, id="item in list"),
        pytest.param([1, 2, 3], 4, False, id="item not in list"),
        pytest.param([], 1, False, id="empty list"),
        pytest.param(None, 1, None, id="None list"),
    ],
)
class TestShouldCheckIfListContainsItem:
    def test_plain_arguments(self, value: list | None, item: int, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.contains(item),
            expected,
            type_=DataTypes.List(DataTypes.Int64()),
        )

    def test_arguments_wrapped_in_cell(self, value: list | None, item: int, expected: bool | None) -> None:
        assert_cell_operation_works(
            value,
            lambda cell: cell.list.contains(Cell.constant(item)),
            expected,
            type_=DataTypes.List(DataTypes.Int64()),
        )


def test_should_infer_type() -> None:
    result = cell_of_type(DataTypes.List(DataTypes.Int64())).list.contains(1)
    assert_cell_has_type(result, DataTypes.Boolean())
