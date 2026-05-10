from collections.abc import Callable

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
        pytest.param(3, 3, 0, id="int - int"),
        pytest.param(3, 1.5, 0.0, id="int - float"),
        pytest.param(1.5, 3, 1.5, id="float - int"),
        pytest.param(1.5, 1.5, 0.0, id="float - float"),
        pytest.param(None, 3, None, id="left is None"),
        pytest.param(3, None, None, id="right is None"),
    ],
)
class TestShouldComputeModulus:
    def test_dunder_method(self, value1: float | None, value2: float | None, expected: float | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell % value2, expected)

    def test_dunder_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell % ExprCell(pl.lit(value2), type=DataTypes.Unknown()),
            expected,
        )

    def test_dunder_method_inverted_order(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 % cell, expected)

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(
            value2,
            lambda cell: ExprCell(pl.lit(value1), type=DataTypes.Unknown()) % cell,
            expected,
        )

    def test_named_method(self, value1: float | None, value2: float | None, expected: float | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.mod(value2), expected)

    def test_named_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell.mod(ExprCell(pl.lit(value2), type=DataTypes.Unknown())),
            expected,
        )


@pytest.mark.parametrize(
    ("left_type", "right_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int32(), DataTypes.Int32(), lambda a, b: a % b, DataTypes.Int32(), id="int_same"),
        pytest.param(DataTypes.Int8(), DataTypes.Int16(), lambda a, b: a % b, DataTypes.Int16(), id="int_promotion"),
        pytest.param(DataTypes.UInt64(), DataTypes.Int64(), lambda a, b: a % b, DataTypes.Float64(), id="uint64_int64"),
        pytest.param(DataTypes.Int32(), DataTypes.Float64(), lambda a, b: a % b, DataTypes.Float64(), id="int_float"),
        pytest.param(
            DataTypes.Unknown(), DataTypes.Int32(), lambda a, b: a % b, DataTypes.Unknown(), id="unknown_left"
        ),
        pytest.param(
            DataTypes.Int32(), DataTypes.Unknown(), lambda a, b: a % b, DataTypes.Unknown(), id="unknown_right"
        ),
        pytest.param(DataTypes.Null(), DataTypes.Int32(), lambda a, b: a % b, DataTypes.Int32(), id="null_left"),
        pytest.param(DataTypes.Int32(), DataTypes.Null(), lambda a, b: a % b, DataTypes.Int32(), id="null_right"),
    ],
)
class TestShouldInferType:
    def test_should_match_ground_truth(
        self,
        left_type: DataType,
        right_type: DataType,
        operation: Callable[[Cell, Cell], Cell],
        expected_type: DataType,
    ) -> None:
        result = operation(cell_of_type(left_type), cell_of_type(right_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self,
        left_type: DataType,
        right_type: DataType,
        operation: Callable[[Cell, Cell], Cell],
        expected_type: DataType,
    ) -> None:
        assert_cell_type_matches_polars((left_type, right_type), operation, expected_type)


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int8(), lambda cell: cell % 3, DataTypes.Int8(), id="int8_mod_int"),
        pytest.param(DataTypes.Int32(), lambda cell: cell % 3, DataTypes.Int32(), id="int32_mod_int"),
        pytest.param(DataTypes.Int64(), lambda cell: cell % 3, DataTypes.Int64(), id="int64_mod_int"),
        pytest.param(DataTypes.Int32(), lambda cell: cell % 3.14, DataTypes.Float64(), id="int32_mod_float"),
    ],
)
class TestShouldInferTypeWithLiteral:
    def test_should_match_ground_truth(
        self,
        given_type: DataType,
        operation: Callable[[Cell], Cell],
        expected_type: DataType,
    ) -> None:
        result = operation(cell_of_type(given_type))
        assert_cell_has_type(result, expected_type)

    def test_should_match_polars_type(
        self,
        given_type: DataType,
        operation: Callable[[Cell], Cell],
        expected_type: DataType,
    ) -> None:
        assert_cell_type_matches_polars(given_type, operation, expected_type)


@pytest.mark.parametrize(
    ("left_type", "right_type"),
    [
        pytest.param(DataTypes.String(), DataTypes.Int32(), id="string_int"),
        pytest.param(DataTypes.Int32(), DataTypes.String(), id="int_string"),
        pytest.param(DataTypes.Date(), DataTypes.Int32(), id="date_int"),
        pytest.param(DataTypes.Int32(), DataTypes.Date(), id="int_date"),
    ],
)
class TestShouldRaiseForInvalidOperandTypes:
    def test_dunder_method(self, left_type: DataType, right_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Invalid operand types"):
            _ = cell_of_type(left_type) % cell_of_type(right_type)

    def test_dunder_method_inverted_order(self, left_type: DataType, right_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Invalid operand types"):
            _ = cell_of_type(right_type) % cell_of_type(left_type)


class TestShouldRaiseForInvalidLiteralType:
    def test_dunder_method(self) -> None:
        with pytest.raises(ColumnTypeError, match="Invalid operand types"):
            _ = cell_of_type(DataTypes.String()) % 1

    def test_dunder_method_inverted_order(self) -> None:
        with pytest.raises(ColumnTypeError, match="Invalid operand types"):
            _ = 1 % cell_of_type(DataTypes.String())


class TestShouldSkipValidationForUnknownType:
    def test_self_unknown(self) -> None:
        _ = cell_of_unknown_type() % cell_of_type(DataTypes.Int32())

    def test_other_unknown(self) -> None:
        _ = cell_of_type(DataTypes.Int32()) % cell_of_unknown_type()

    def test_self_unknown_literal(self) -> None:
        _ = cell_of_unknown_type() % 1

    def test_literal_self_unknown_other(self) -> None:
        _ = 1 % cell_of_unknown_type()
