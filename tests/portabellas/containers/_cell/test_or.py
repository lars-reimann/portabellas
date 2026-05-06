from typing import Any

import polars as pl
import pytest

from portabellas.containers._cell import ExprCell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes
from tests.helpers import assert_cell_operation_works, cell_of_type, cell_of_unknown_type


@pytest.mark.parametrize(
    ("value1", "value2", "expected"),
    [
        pytest.param(False, False, False, id="False - False"),
        pytest.param(False, True, True, id="False - True"),
        pytest.param(False, None, None, id="False - None"),
        pytest.param(True, False, True, id="True - False"),
        pytest.param(True, True, True, id="True - True"),
        pytest.param(True, None, True, id="True - None"),
        pytest.param(None, False, None, id="None - False"),
        pytest.param(None, True, True, id="None - True"),
        pytest.param(None, None, None, id="None - None"),
    ],
)
class TestShouldComputeDisjunction:
    def test_dunder_method(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell | value2, expected, type_if_none=DataTypes.Boolean())

    def test_dunder_method_wrapped_in_cell(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell | ExprCell(pl.lit(value2)),
            expected,
            type_if_none=DataTypes.Boolean(),
        )

    def test_dunder_method_inverted_order(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 | cell, expected, type_if_none=DataTypes.Boolean())

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: Any,
        value2: bool | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(
            value2,
            lambda cell: ExprCell(pl.lit(value1)) | cell,
            expected,
            type_if_none=DataTypes.Boolean(),
        )

    def test_named_method(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.or_(value2), expected, type_if_none=DataTypes.Boolean())

    def test_named_method_wrapped_in_cell(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell.or_(ExprCell(pl.lit(value2))),
            expected,
            type_if_none=DataTypes.Boolean(),
        )


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Int64(), id="int"),
    ],
)
class TestShouldRaiseForNonBooleanType:
    def test_self(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell_of_type(cell_type) | True

    def test_other_cell(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell_of_type(DataTypes.Boolean()) | cell_of_type(cell_type)

    def test_self_inverted_order(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = True | cell_of_type(cell_type)


class TestShouldRaiseForNonBooleanLiteral:
    def test_other_literal(self) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell_of_type(DataTypes.Boolean()) | 1  # type: ignore[operator]

    def test_other_literal_inverted_order(self) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = 1 | cell_of_type(DataTypes.Boolean())  # type: ignore[operator]


class TestShouldSkipValidationForUnknownType:
    def test_self(self) -> None:
        _ = cell_of_unknown_type() | True

    def test_other_cell(self) -> None:
        _ = cell_of_type(DataTypes.Boolean()) | cell_of_unknown_type()

    def test_other_literal_none(self) -> None:
        _ = cell_of_type(DataTypes.Boolean()) | None
