import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 3, id="three elements"),
        pytest.param([1], 1, id="one element"),
        pytest.param([], 0, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_get_list_length(value: list | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.length(),
        expected,
        type_=DataTypes.List(DataTypes.Int64()),
    )
