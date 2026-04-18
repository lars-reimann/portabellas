from typing import Any

import pytest

from portabellas.containers import Cell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "type_", "expected"),
    [
        pytest.param(None, None, None, id="None"),
        pytest.param(1, None, 1, id="int"),
        pytest.param(1, DataType.String(), "1", id="with explicit type"),
    ],
)
def test_should_return_constant_value(value: Any, type_: DataType | None, expected: Any) -> None:
    assert_cell_operation_works(None, lambda _: Cell.constant(value, type=type_), expected)
