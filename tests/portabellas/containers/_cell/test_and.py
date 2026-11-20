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
        pytest.param(False, False, False, id="False - False"),
        pytest.param(False, True, False, id="False - True"),
        pytest.param(False, None, False, id="False - None"),
        pytest.param(True, False, False, id="True - False"),
        pytest.param(True, True, True, id="True - True"),
        pytest.param(True, None, None, id="True - None"),
        pytest.param(None, False, False, id="None - False"),
        pytest.param(None, True, None, id="None - True"),
        pytest.param(None, None, None, id="None - None"),
    ],
)
class TestShouldComputeConjunction:
    def test_dunder_method(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell & value2, expected, type_if_none=DataTypes.Boolean())

    def test_dunder_method_wrapped_in_cell(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell & ExprCell(pl.lit(value2), type=DataTypes.Unknown()),
            expected,
            type_if_none=DataTypes.Boolean(),
        )

    def test_dunder_method_inverted_order(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value2, lambda cell: value1 & cell, expected, type_if_none=DataTypes.Boolean())

    def test_dunder_method_inverted_order_wrapped_in_cell(
        self,
        value1: Any,
        value2: bool | None,
        expected: bool | None,
    ) -> None:
        assert_cell_operation_works(
            value2,
            lambda cell: ExprCell(pl.lit(value1), type=DataTypes.Unknown()) & cell,
            expected,
            type_if_none=DataTypes.Boolean(),
        )

    def test_named_method(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(value1, lambda cell: cell.and_(value2), expected, type_if_none=DataTypes.Boolean())

    def test_named_method_wrapped_in_cell(self, value1: Any, value2: bool | None, expected: bool | None) -> None:
        assert_cell_operation_works(
            value1,
            lambda cell: cell.and_(ExprCell(pl.lit(value2), type=DataTypes.Unknown())),
            expected,
            type_if_none=DataTypes.Boolean(),
        )


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.String(), id="string"),
        pytest.param(DataTypes.Float64(), id="float"),
    ],
)
class TestShouldRaiseForNonBooleanNonIntegerTypeOnOperator:
    def test_self(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected integer type"):
            _ = cell_of_type(cell_type) & True

    def test_other_cell(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected integer type"):
            _ = cell_of_type(DataTypes.Int64()) & cell_of_type(cell_type)

    def test_self_inverted_order(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected integer type"):
            _ = True & cell_of_type(cell_type)


@pytest.mark.parametrize(
    "cell_type",
    [
        pytest.param(DataTypes.Int64(), id="int"),
    ],
)
class TestShouldRaiseForNonBooleanTypeOnNamedMethod:
    def test_self(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell_of_type(cell_type).and_(True)  # noqa: FBT003

    def test_other_cell(self, cell_type: DataType) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            _ = cell_of_type(DataTypes.Boolean()).and_(cell_of_type(cell_type))


class TestShouldSkipValidationForUnknownType:
    def test_self(self) -> None:
        _ = cell_of_unknown_type() & True

    def test_other_cell(self) -> None:
        _ = cell_of_type(DataTypes.Boolean()) & cell_of_unknown_type()

    def test_other_literal_none(self) -> None:
        _ = cell_of_type(DataTypes.Boolean()) & None


@pytest.mark.parametrize(
    ("given_type", "operation", "expected_type"),
    [
        pytest.param(DataTypes.Boolean(), lambda cell: cell & True, DataTypes.Boolean(), id="__and__"),
        pytest.param(DataTypes.Boolean(), lambda cell: True & cell, DataTypes.Boolean(), id="__rand__"),
        pytest.param(DataTypes.Boolean(), lambda cell: cell.and_(True), DataTypes.Boolean(), id="and_"),  # noqa: FBT003
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
