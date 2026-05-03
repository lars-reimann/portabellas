import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param([1, 2, 3], 1, id="non-empty list"),
        pytest.param([], None, id="empty list"),
        pytest.param(None, None, id="None list"),
    ],
)
def test_should_get_first_element(value: list | None, expected: int | None) -> None:
    assert_cell_operation_works(
        value,
        lambda cell: cell.list.first(),
        expected,
        type_=DataType.List(DataType.Int64()),
    )
