from typing import Any

import polars as pl
import pytest

from portabellas.containers._cell import ExprCell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(False, False, False, id="False - False"),
        pytest.param(False, True, False, id="False - True"),
        pytest.param(False, None, False, id="False - None"),
        pytest.param(True, False, False, id="True - False"),
        pytest.param(True, True, True, id="True - True"),
        pytest.param(True, None, None, id="True - None"),
        pytest.param(None, False, False, id="None - False"),
        pytest.param(None, True, None, id="None - True"),
        pytest.param(None, None, None, id="None - None"),
        pytest.param(0, False, False, id="falsy int - False"),
        pytest.param(0, True, False, id="falsy int - True"),
        pytest.param(1, False, False, id="truthy int - False"),
        pytest.param(1, True, True, id="truthy int - True"),
    ],
)
class TestShouldComputeConjunction:
    def test_dunder_method(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell & value2, expected, type_if_none=DataType.Boolean())

    def test_dunder_method_wrapped_in_cell(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell & ExprCell(pl.lit(value2)),
            expected,
            type_if_none=DataType.Boolean(),
        )

    def test_dunder_method_inverted_order(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 & cell, expected, type_if_none=DataType.Boolean())

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: Any,
        value2: bool | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(
            value2,
            lambda cell: ExprCell(pl.lit(value1)) & cell,
            expected,
            type_if_none=DataType.Boolean(),
        )

    def test_named_method(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.and_(value2), expected, type_if_none=DataType.Boolean())

    def test_named_method_wrapped_in_cell(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell.and_(ExprCell(pl.lit(value2))),
            expected,
            type_if_none=DataType.Boolean(),
        )
