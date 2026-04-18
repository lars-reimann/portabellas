from typing import Any

import pytest

from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        pytest.param(False, True, id="False"),
        pytest.param(True, False, id="True"),
        pytest.param(None, None, id="None"),
        pytest.param(0, True, id="falsy int"),
        pytest.param(1, False, id="truthy int"),
    ],
)
class TestShouldInvertValueOfCell:
    def test_dunder_method(self, value: Any, expected: bool | None) -> None:
        assert_cell_operation_works(value, lambda cell: ~cell, expected, type_if_none=DataType.Boolean())

    def test_named_method(self, value: Any, expected: bool | None) -> None:
        assert_cell_operation_works(value, lambda cell: cell.not_(), expected, type_if_none=DataType.Boolean())
