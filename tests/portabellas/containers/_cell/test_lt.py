from collections.abc import Callable

import polars as pl
import pytest

from portabellas.containers import Cell
from portabellas.containers._cell import ExprCell
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
)


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(3, 3, False, id="int - int"),
        pytest.param(3, 1.5, False, id="int - float"),
        pytest.param(1.5, 3, True, id="float - int"),
        pytest.param(1.5, 1.5, False, id="float - float"),
        pytest.param(None, 3, None, id="left is None"),
        pytest.param(3, None, None, id="right is None"),
    ],
)
class TestShouldComputeLessThan:
    def test_dunder_method(self, value1: float | None, value2: float | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell < value2, expected)

    def test_dunder_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell < ExprCell(pl.lit(value2)), expected)

    def test_dunder_method_inverted_order(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 < cell, expected)

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: ExprCell(pl.lit(value1)) < cell, expected)

    def test_named_method(self, value1: float | None, value2: float | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.lt(value2), expected)

    def test_named_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.lt(ExprCell(pl.lit(value2))), expected)


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int32(), lambda cell: cell < 1, DataTypes.Boolean(), id="__lt__"),
        pytest.param(DataTypes.Int32(), lambda cell: cell.lt(1), DataTypes.Boolean(), id="lt"),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self, given_type: DataType, operation: Callable[[Cell], Cell], expected_type: DataType
    ) -> None:
        assert_cell_type_matches_polars(given_type, operation, expected_type)
