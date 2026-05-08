import polars as pl
import pytest

from portabellas._validation import CellTypeRequirement, InstanceOf, check_type
from portabellas.containers._cell import ExprCell
from portabellas.exceptions import ColumnTypeError
from portabellas.typing import DataType, DataTypes


class TestInstanceOf:
    @pytest.mark.parametrize(
        ("requirement", "cell_type", "expected"),
        [
            pytest.param(InstanceOf(DataTypes.String), DataTypes.String(), True, id="String matches String"),
            pytest.param(InstanceOf(DataTypes.String), DataTypes.Int64(), False, id="Int64 does not match String"),
            pytest.param(
                InstanceOf(DataTypes.Date, DataTypes.Datetime),
                DataTypes.Date(),
                True,
                id="Date matches Date or Datetime",
            ),
            pytest.param(
                InstanceOf(DataTypes.Date, DataTypes.Datetime),
                DataTypes.Datetime(),
                True,
                id="Datetime matches Date or Datetime",
            ),
            pytest.param(
                InstanceOf(DataTypes.Date, DataTypes.Datetime),
                DataTypes.Time(),
                False,
                id="Time does not match Date or Datetime",
            ),
        ],
    )
    def test_should_check_instance(self, requirement: InstanceOf, cell_type: DataType, expected: bool) -> None:
        assert requirement(cell_type) == expected

    @pytest.mark.parametrize(
        ("requirement", "expected_description"),
        [
            pytest.param(InstanceOf(DataTypes.String), "String", id="single type"),
            pytest.param(InstanceOf(DataTypes.Date, DataTypes.Datetime), "Date or Datetime", id="two types"),
            pytest.param(
                InstanceOf(DataTypes.Date, DataTypes.Datetime, DataTypes.Time),
                "Date, Datetime, or Time",
                id="three types",
            ),
        ],
    )
    def test_should_derive_description(self, requirement: InstanceOf, expected_description: str) -> None:
        assert requirement.description == expected_description


class TestCellTypeRequirement:
    @pytest.mark.parametrize(
        ("requirement", "cell_type", "expected"),
        [
            pytest.param(
                CellTypeRequirement("numeric", lambda t: t.is_numeric),
                DataTypes.Int64(),
                True,
                id="numeric matches Int64",
            ),
            pytest.param(
                CellTypeRequirement("numeric", lambda t: t.is_numeric),
                DataTypes.String(),
                False,
                id="numeric does not match String",
            ),
        ],
    )
    def test_should_use_custom_check(
        self,
        requirement: CellTypeRequirement,
        cell_type: DataType,
        expected: bool,
    ) -> None:
        assert requirement(cell_type) == expected

    def test_should_use_custom_description(self) -> None:
        requirement = CellTypeRequirement("numeric", lambda t: t.is_numeric)
        assert requirement.description == "numeric"


class TestCheckType:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            pytest.param(DataTypes.Int64(), True, id="DataType input"),
            pytest.param(ExprCell(pl.col("a"), type=DataTypes.Int64()), True, id="ExprCell input"),
            pytest.param(1, True, id="int literal"),
            pytest.param(3.14, True, id="float literal"),
            pytest.param("hello", False, id="str literal does not match numeric"),
        ],
    )
    def test_should_not_raise_for_valid_type(self, value: object, expected: bool) -> None:
        if expected:
            check_type(value, required=CellTypeRequirement("numeric", lambda t: t.is_numeric))
        else:
            with pytest.raises(ColumnTypeError):
                check_type(value, required=CellTypeRequirement("numeric", lambda t: t.is_numeric))

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(DataTypes.String(), id="DataType input"),
            pytest.param(ExprCell(pl.col("a"), type=DataTypes.String()), id="ExprCell input"),
            pytest.param("hello", id="str literal"),
        ],
    )
    def test_should_raise_for_invalid_type(self, value: object) -> None:
        with pytest.raises(ColumnTypeError):
            check_type(value, required=CellTypeRequirement("numeric", lambda t: t.is_numeric))

    @pytest.mark.parametrize(
        "value",
        [
            pytest.param(DataTypes.Unknown(), id="DataType Unknown"),
            pytest.param(DataTypes.Null(), id="DataType Null"),
            pytest.param(ExprCell(pl.col("a"), type=DataTypes.Unknown()), id="ExprCell with Unknown type"),
            pytest.param(ExprCell(pl.col("a"), type=DataTypes.Null()), id="ExprCell with Null type"),
            pytest.param(None, id="None literal"),
            pytest.param(object(), id="arbitrary object"),
        ],
    )
    def test_should_skip_validation_for_unknown_or_null_type(self, value: object) -> None:
        check_type(value, required=CellTypeRequirement("numeric", lambda t: t.is_numeric))

    def test_should_include_description_in_error_message(self) -> None:
        with pytest.raises(ColumnTypeError, match="Expected numeric type, got str"):
            check_type(DataTypes.String(), required=CellTypeRequirement("numeric", lambda t: t.is_numeric))

    def test_should_include_actual_type_in_error_message(self) -> None:
        with pytest.raises(ColumnTypeError, match="got i64"):
            check_type(DataTypes.Int64(), required=InstanceOf(DataTypes.String))

    def test_should_raise_for_int_literal_with_boolean_requirement(self) -> None:
        with pytest.raises(ColumnTypeError, match="Expected Boolean type"):
            check_type(1, required=InstanceOf(DataTypes.Boolean))

    def test_should_not_raise_for_bool_literal_with_boolean_requirement(self) -> None:
        check_type(value=True, required=InstanceOf(DataTypes.Boolean))
