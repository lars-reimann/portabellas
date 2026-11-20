from collections.abc import Callable
from typing import Any

import polars as pl
import pytest

from portabellas.containers import Cell
from portabellas.containers._cell import ExprCell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import (
    assert_cell_has_type,
    assert_cell_operation_works,
    assert_cell_type_matches_polars,
    cell_of_type,
    cell_of_unknown_type,
)


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(0b1100, 0b1010, 0b0110, id="1100 - 1010"),
        pytest.param(0b1100, 0, 0b1100, id="1100 - 0"),
        pytest.param(0, 0b1010, 0b1010, id="0 - 1010"),
        pytest.param(0b1111, 0b1111, 0, id="1111 - 1111"),
        pytest.param(0b1100, None, None, id="1100 - None"),
        pytest.param(None, 0b1010, None, id="None - 1010"),
        pytest.param(None, None, None, id="None - None"),
    ],
)
class TestShouldComputeBitwiseXor:
    def test_dunder_method(self, value1: Any, value2: int | None, expected: int | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell ^ value2, expected, type_if_none=DataTypes.Int64())

    def test_dunder_method_wrapped_in_cell(self, value1: Any, value2: int | None, expected: int | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell ^ ExprCell(pl.lit(value2), type=DataTypes.Unknown()),
            expected,
            type_if_none=DataTypes.Int64(),
        )

    def test_dunder_method_inverted_order(self, value1: Any, value2: int | None, expected: int | None) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 ^ cell, expected, type_if_none=DataTypes.Int64())

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: Any,
        value2: int | None,
        expected: int | None,
    ) -> None:
        assert_cell_operation_works(
            value2,
            lambda cell: ExprCell(pl.lit(value1), type=DataTypes.Unknown()) ^ cell,
            expected,
            type_if_none=DataTypes.Int64(),
        )

    def test_named_method(self, value1: Any, value2: int | None, expected: int | None) -> None:
        assert_cell_operation_works(
            value1, lambda cell: cell.bitwise_xor(value2), expected, type_if_none=DataTypes.Int64()
        )

    def test_named_method_wrapped_in_cell(self, value1: Any, value2: int | None, expected: int | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell.bitwise_xor(ExprCell(pl.lit(value2), type=DataTypes.Unknown())),
            expected,
            type_if_none=DataTypes.Int64(),
        )


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Boolean(), id="boolean"),
        pytest.param(DataTypes.Float64(), id="float"),
    ],
)
class TestShouldRaiseForNonIntegerTypeOnBitwiseXor:
    def test_self(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected integer type"):
            _ = cell_of_type(cell_type).bitwise_xor(1)

    def test_other_cell(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected integer type"):
            _ = cell_of_type(DataTypes.Int64()).bitwise_xor(cell_of_type(cell_type))


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Float64(), id="float"),
    ],
)
class TestShouldRaiseForNonIntegerTypeOnOperator:
    def test_self(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected integer type"):
            _ = cell_of_type(cell_type) ^ 1

    def test_other_cell(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected integer type"):
            _ = cell_of_type(DataTypes.Int64()) ^ cell_of_type(cell_type)


class TestShouldSkipValidationForUnknownType:
    def test_self(self) -> None:
        _ = cell_of_unknown_type() ^ 1

    def test_other_cell(self) -> None:
        _ = cell_of_type(DataTypes.Int64()) ^ cell_of_unknown_type()

    def test_other_literal_none(self) -> None:
        _ = cell_of_type(DataTypes.Int64()) ^ None

    def test_self_reflected(self) -> None:
        _ = 1 ^ cell_of_unknown_type()


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int64(), lambda cell: cell ^ 1, DataTypes.Int64(), id="__xor__"),
        pytest.param(DataTypes.Int64(), lambda cell: 1 ^ cell, DataTypes.Int64(), id="__rxor__"),
        pytest.param(DataTypes.Int64(), lambda cell: cell.bitwise_xor(1), DataTypes.Int64(), id="bitwise_xor"),
        pytest.param(DataTypes.Int32(), lambda cell: cell ^ 1, DataTypes.Int32(), id="__xor___int32"),
        pytest.param(DataTypes.UInt32(), lambda cell: cell ^ 1, DataTypes.UInt32(), id="__xor___uint32"),
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
