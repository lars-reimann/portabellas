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
        pytest.param(3, 3, 6, id="int - int"),
        pytest.param(3, 1.5, 4.5, id="int - float"),
        pytest.param(1.5, 3, 4.5, id="float - int"),
        pytest.param(1.5, 1.5, 3.0, id="float - float"),
        pytest.param(None, 3, None, id="left is None"),
        pytest.param(3, None, None, id="right is None"),
    ],
)
class TestShouldComputeAddition:
    def test_dunder_method(self, value1: float | None, value2: float | None, expected: float | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell + value2, expected)

    def test_dunder_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell + ExprCell(pl.lit(value2)), expected)

    def test_dunder_method_inverted_order(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 + cell, expected)

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value2, lambda cell: ExprCell(pl.lit(value1)) + cell, expected)

    def test_named_method(self, value1: float | None, value2: float | None, expected: float | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.add(value2), expected)

    def test_named_method_wrapped_in_cell(
        self,
        value1: float | None,
        value2: float | None,
        expected: float | None,
    ) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.add(ExprCell(pl.lit(value2))), expected)


@pytest.mark.parametrize(
    ("left_type", "right_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Int32(), DataTypes.Int32(), lambda a, b: a + b, DataTypes.Int32(), id="int_same"),
        pytest.param(DataTypes.Int8(), DataTypes.Int16(), lambda a, b: a + b, DataTypes.Int16(), id="int_promotion"),
        pytest.param(DataTypes.UInt64(), DataTypes.Int64(), lambda a, b: a + b, DataTypes.Float64(), id="uint64_int64"),
        pytest.param(DataTypes.Int32(), DataTypes.Float64(), lambda a, b: a + b, DataTypes.Float64(), id="int_float"),
        pytest.param(
            DataTypes.String(), DataTypes.String(), lambda a, b: a + b, DataTypes.String(), id="string_string"
        ),
        pytest.param(
            DataTypes.Date(),
            DataTypes.Duration(time_unit="us"),
            lambda a, b: a + b,
            DataTypes.Date(),
            id="date_duration",
        ),
        pytest.param(
            DataTypes.Duration(time_unit="us"),
            DataTypes.Date(),
            lambda a, b: a + b,
            DataTypes.Date(),
            id="duration_date",
        ),
        pytest.param(
            DataTypes.Datetime(time_unit="us"),
            DataTypes.Duration(time_unit="us"),
            lambda a, b: a + b,
            DataTypes.Datetime(time_unit="us"),
            id="datetime_duration",
        ),
        pytest.param(
            DataTypes.Datetime(time_unit="us", time_zone="UTC"),
            DataTypes.Duration(time_unit="us"),
            lambda a, b: a + b,
            DataTypes.Datetime(time_unit="us", time_zone="UTC"),
            id="datetime_utc_duration",
        ),
        pytest.param(
            DataTypes.Duration(time_unit="us"),
            DataTypes.Duration(time_unit="ms"),
            lambda a, b: a + b,
            DataTypes.Duration(time_unit="ms"),
            id="duration_duration_coarser",
        ),
        pytest.param(
            DataTypes.Unknown(), DataTypes.Int32(), lambda a, b: a + b, DataTypes.Unknown(), id="unknown_left"
        ),
        pytest.param(
            DataTypes.Int32(), DataTypes.Unknown(), lambda a, b: a + b, DataTypes.Unknown(), id="unknown_right"
        ),
        pytest.param(DataTypes.Null(), DataTypes.Int32(), lambda a, b: a + b, DataTypes.Int32(), id="null_left"),
        pytest.param(DataTypes.Int32(), DataTypes.Null(), lambda a, b: a + b, DataTypes.Int32(), id="null_right"),
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
        pytest.param(DataTypes.Int8(), lambda cell: cell + 3, DataTypes.Int8(), id="int8_plus_int"),
        pytest.param(DataTypes.Int16(), lambda cell: cell + 3, DataTypes.Int16(), id="int16_plus_int"),
        pytest.param(DataTypes.Int32(), lambda cell: cell + 3, DataTypes.Int32(), id="int32_plus_int"),
        pytest.param(DataTypes.Int64(), lambda cell: cell + 3, DataTypes.Int64(), id="int64_plus_int"),
        pytest.param(DataTypes.UInt8(), lambda cell: cell + 3, DataTypes.UInt8(), id="uint8_plus_int"),
        pytest.param(DataTypes.UInt16(), lambda cell: cell + 3, DataTypes.UInt16(), id="uint16_plus_int"),
        pytest.param(DataTypes.UInt32(), lambda cell: cell + 3, DataTypes.UInt32(), id="uint32_plus_int"),
        pytest.param(DataTypes.UInt64(), lambda cell: cell + 3, DataTypes.UInt64(), id="uint64_plus_int"),
        pytest.param(DataTypes.Int32(), lambda cell: cell + 3.14, DataTypes.Float64(), id="int32_plus_float"),
        pytest.param(DataTypes.Float32(), lambda cell: cell + 3.14, DataTypes.Float32(), id="float32_plus_float"),
        pytest.param(DataTypes.String(), lambda cell: cell + "hello", DataTypes.String(), id="string_plus_str"),
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
