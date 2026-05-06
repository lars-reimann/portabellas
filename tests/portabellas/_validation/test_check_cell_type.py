import pytest

from portabellas._validation import CellTypeRequirement, InstanceOf, check_cell_type
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


class TestCheckCellType:
    def test_should_not_raise_for_valid_type(self) -> None:
        check_cell_type(DataTypes.Int64(), required=CellTypeRequirement("numeric", lambda t: t.is_numeric))

    def test_should_raise_for_invalid_type(self) -> None:
        with pytest.raises(ColumnTypeError):
            check_cell_type(DataTypes.String(), required=CellTypeRequirement("numeric", lambda t: t.is_numeric))

    def test_should_skip_validation_for_unknown_type(self) -> None:
        check_cell_type(DataTypes.Unknown(), required=CellTypeRequirement("numeric", lambda t: t.is_numeric))

    def test_should_include_description_in_error_message(self) -> None:
        with pytest.raises(ColumnTypeError, match="Expected numeric type, got str"):
            check_cell_type(DataTypes.String(), required=CellTypeRequirement("numeric", lambda t: t.is_numeric))

    def test_should_include_actual_type_in_error_message(self) -> None:
        with pytest.raises(ColumnTypeError, match="got i64"):
            check_cell_type(DataTypes.Int64(), required=InstanceOf(DataTypes.String))
