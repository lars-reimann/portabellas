from collections.abc import Callable

import polars as pl
import pytest

from portabellas.containers import Cell
from portabellas.containers._cell import ExprCell
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_has_type, assert_cell_operation_works, cell_of_type


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(3, 3, False, id="int - int"),
        pytest.param(3, 1.5, True, id="int - float"),
        pytest.param(1.5, 3, True, id="float - int"),
        pytest.param(1.5, 1.5, False, id="float - float"),
        pytest.param(None, 3, True, id="left is None"),
        pytest.param(3, None, True, id="right is None"),
        pytest.param(None, None, False, id="both are None"),
    ],
)
class TestShouldComputeInequality:
    def test_dunder_method(self, value1: float | None, value2: float | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell != value2, expected)

    def test_dunder_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell != ExprCell(pl.lit(value2)), expected)

    def test_dunder_method_inverted_order(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 != cell, expected)  # type: ignore[arg-type,return-value]

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: ExprCell(pl.lit(value1)) != cell, expected)

    def test_named_method(self, value1: float | None, value2: float | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.neq(value2), expected)

    def test_named_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.neq(ExprCell(pl.lit(value2))), expected)


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(3, 3, False, id="equal"),
        pytest.param(1, 3, True, id="unequal"),
        pytest.param(None, 3, None, id="left is None"),
        pytest.param(3, None, None, id="right is None"),
        pytest.param(None, None, None, id="both are None"),
    ],
)
class TestShouldComputeInequalityWithPropagatingNulls:
    def test_named_method(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.neq(value2, propagate_nulls=True), expected)

    def test_named_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell.neq(ExprCell(pl.lit(value2)), propagate_nulls=True),
            expected,
        )


@pytest.mark.parametrize(
    ("operation", "expected_type"),
    [
        pytest.param(lambda cell: cell != 1, DataTypes.Boolean(), id="__ne__"),
        pytest.param(lambda cell: cell.neq(1), DataTypes.Boolean(), id="neq"),
        pytest.param(lambda cell: cell.neq(1, propagate_nulls=True), DataTypes.Boolean(), id="neq-propagate-nulls"),
    ],
)
def test_should_infer_type(operation: Callable[[Cell], Cell], expected_type: DataType) -> None:
    result = operation(cell_of_type(DataTypes.Int32()))
    assert_cell_has_type(result, expected_type)
