from typing import Any

import polars as pl
import pytest

from portabellas.containers._cell import ExprCell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_operation_works


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(False, False, False, id="False - False"),
        pytest.param(False, True, True, id="False - True"),
        pytest.param(False, None, None, id="False - None"),
        pytest.param(True, False, True, id="True - False"),
        pytest.param(True, True, False, id="True - True"),
        pytest.param(True, None, None, id="True - None"),
        pytest.param(None, False, None, id="None - False"),
        pytest.param(None, True, None, id="None - True"),
        pytest.param(None, None, None, id="None - None"),
    ],
)
class TestShouldComputeExclusiveOr:
    def test_dunder_method(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell ^ value2, expected, type_if_none=DataTypes.Boolean())

    def test_dunder_method_wrapped_in_cell(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell ^ ExprCell(pl.lit(value2)),
            expected,
            type_if_none=DataTypes.Boolean(),
        )

    def test_dunder_method_inverted_order(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 ^ cell, expected, type_if_none=DataTypes.Boolean())

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: Any,
        value2: bool | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(
            value2,
            lambda cell: ExprCell(pl.lit(value1)) ^ cell,
            expected,
            type_if_none=DataTypes.Boolean(),
        )

    def test_named_method(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.xor(value2), expected, type_if_none=DataTypes.Boolean())

    def test_named_method_wrapped_in_cell(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell.xor(ExprCell(pl.lit(value2))),
            expected,
            type_if_none=DataTypes.Boolean(),
        )


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Boolean(), id="boolean"),
    ],
)
class TestShouldNotRaiseForBooleanType:
    def test_self(self, cell_type: DataType) -> None:
        cell: ExprCell = ExprCell(pl.col("a"), type=cell_type)
        _ = cell ^ True

    def test_other_cell(self, cell_type: DataType) -> None:
        cell: ExprCell = ExprCell(pl.col("a"), type=DataTypes.Boolean())
        other: ExprCell = ExprCell(pl.col("b"), type=cell_type)
        _ = cell ^ other


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Int64(), id="int"),
    ],
)
class TestShouldRaiseForNonBooleanType:
    def test_self(self, cell_type: DataType) -> None:
        cell: ExprCell = ExprCell(pl.col("a"), type=cell_type)
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell ^ True

    def test_other_cell(self, cell_type: DataType) -> None:
        cell: ExprCell = ExprCell(pl.col("a"), type=DataTypes.Boolean())
        other: ExprCell = ExprCell(pl.col("b"), type=cell_type)
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell ^ other

    def test_self_inverted_order(self, cell_type: DataType) -> None:
        cell: ExprCell = ExprCell(pl.col("a"), type=cell_type)
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = True ^ cell


class TestShouldRaiseForNonBooleanLiteral:
    def test_other_literal(self) -> None:
        cell: ExprCell = ExprCell(pl.col("a"), type=DataTypes.Boolean())
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell ^ 1  # type: ignore[operator]


class TestShouldSkipValidationForUnknownType:
    def test_self(self) -> None:
        cell: ExprCell = ExprCell(pl.col("a"))
        _ = cell ^ True

    def test_other_cell(self) -> None:
        cell: ExprCell = ExprCell(pl.col("a"), type=DataTypes.Boolean())
        other: ExprCell = ExprCell(pl.col("b"))
        _ = cell ^ other

    def test_other_literal_none(self) -> None:
        cell: ExprCell = ExprCell(pl.col("a"), type=DataTypes.Boolean())
        _ = cell ^ None
