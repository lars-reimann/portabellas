import polars as pl
import pytest

from portabellas.containers._cell._expr_cell import ExprCell
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(3, 3, 1, id="int - int"),
        pytest.param(3, 1.5, 2.0, id="int - float"),
        pytest.param(1.5, 3, 0.5, id="float - int"),
        pytest.param(1.5, 1.5, 1.0, id="float - float"),
        pytest.param(None, 3, None, id="left is None"),
        pytest.param(3, None, None, id="right is None"),
    ],
)
class TestShouldComputeDivision:
    def test_dunder_method(self, value1: float | None, value2: float | None, expected: float | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell / value2, expected)

    def test_dunder_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell / ExprCell(pl.lit(value2)), expected)

    def test_dunder_method_inverted_order(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 / cell, expected)

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: ExprCell(pl.lit(value1)) / cell, expected)

    def test_named_method(self, value1: float | None, value2: float | None, expected: float | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.div(value2), expected)

    def test_named_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.div(ExprCell(pl.lit(value2))), expected)
