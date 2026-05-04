import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 6, id="positive integers"),
        pytest.param([10], 10, id="single element"),
        pytest.param([], 0, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_sum_list_elements(value: list | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.sum(),
        expected,
        type_=DataTypes.List(DataTypes.Int64()),
    )
