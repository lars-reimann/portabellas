import pytest

from portabellas.typing import DataTypes
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 3, id="non-empty list"),
        pytest.param([], None, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_get_last_element(value: list | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.last(),
        expected,
        type_=DataTypes.List(DataTypes.Int64()),
    )
