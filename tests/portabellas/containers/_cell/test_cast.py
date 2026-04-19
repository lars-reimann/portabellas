from typing import Any

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "type_", "expected"),
    [
        pytest.param(1, DataType.String(), "1", id="int64 to string"),
        pytest.param("1", DataType.Int64(), 1, id="string to int64"),
        pytest.param(None, DataType.Int64(), None, id="None to int64"),
    ],
)
def test_should_cast_values_to_requested_type(value: Any, type_: DataType, expected: Any) -> None:
    assert_cell_operation_works(value, lambda cell: cell.cast(type_), expected)
