import polars as pl
import pytest

from portabellas.containers._cell._expr_cell import ExprCell
from portabellas.typing import DataType
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(3, 2, 9, id="int - int"),
        pytest.param(4, 0.5, 2.0, id="int - float"),
        pytest.param(1.5, 2, 2.25, id="float - int"),
        pytest.param(2.25, 0.5, 1.5, id="float - float"),
        pytest.param(None, 3, None, id="left is None"),
        pytest.param(3, None, None, id="right is None"),
    ],
)
class TestShouldComputePower:
    def test_dunder_method(self, value1: float | None, value2: float | None, expected: float | None) -> None:
        if value2 is None:
            pytest.skip("polars does not support null exponents.")

        assert_cell_operation_works(value1, lambda cell: cell**value2, expected, type_if_none=DataType.Float64())

    def test_dunder_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell ** ExprCell(pl.lit(value2, dtype=pl.Float64())),
            expected,
            type_if_none=DataType.Float64(),
        )

    def test_dunder_method_inverted_order(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        if value1 is None:
            pytest.skip("polars does not support null base.")

        assert_cell_operation_works(value2, lambda cell: value1**cell, expected, type_if_none=DataType.Float64())

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(
            value2,
            lambda cell: ExprCell(pl.lit(value1, dtype=pl.Float64())) ** cell,
            expected,
            type_if_none=DataType.Float64(),
        )

    def test_named_method(self, value1: float | None, value2: float | None, expected: float | None) -> None:
        if value2 is None:
            pytest.skip("polars does not support null exponents.")

        assert_cell_operation_works(value1, lambda cell: cell.pow(value2), expected, type_if_none=DataType.Float64())

    def test_named_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell.pow(ExprCell(pl.lit(value2, dtype=pl.Float64()))),
            expected,
            type_if_none=DataType.Float64(),
        )
