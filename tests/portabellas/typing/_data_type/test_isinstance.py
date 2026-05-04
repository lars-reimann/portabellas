import pytest

from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("type_", "expected_class"),
    [
        pytest.param(DataTypes.Null(), DataTypes.Null, id="Null"),
        pytest.param(DataTypes.Boolean(), DataTypes.Boolean, id="Boolean"),
        pytest.param(DataTypes.Int8(), DataTypes.Int8, id="Int8"),
        pytest.param(DataTypes.Int16(), DataTypes.Int16, id="Int16"),
        pytest.param(DataTypes.Int32(), DataTypes.Int32, id="Int32"),
        pytest.param(DataTypes.Int64(), DataTypes.Int64, id="Int64"),
        pytest.param(DataTypes.ExperimentalInt128(), DataTypes.ExperimentalInt128, id="Int128"),
        pytest.param(DataTypes.UInt8(), DataTypes.UInt8, id="UInt8"),
        pytest.param(DataTypes.UInt16(), DataTypes.UInt16, id="UInt16"),
        pytest.param(DataTypes.UInt32(), DataTypes.UInt32, id="UInt32"),
        pytest.param(DataTypes.UInt64(), DataTypes.UInt64, id="UInt64"),
        pytest.param(DataTypes.Float32(), DataTypes.Float32, id="Float32"),
        pytest.param(DataTypes.Float64(), DataTypes.Float64, id="Float64"),
        pytest.param(DataTypes.String(), DataTypes.String, id="String"),
        pytest.param(DataTypes.Binary(), DataTypes.Binary, id="Binary"),
        pytest.param(DataTypes.Date(), DataTypes.Date, id="Date"),
        pytest.param(DataTypes.Datetime(), DataTypes.Datetime, id="Datetime"),
        pytest.param(DataTypes.Datetime(time_zone="UTC"), DataTypes.Datetime, id="Datetime with time zone"),
        pytest.param(DataTypes.Duration("us"), DataTypes.Duration, id="Duration"),
        pytest.param(DataTypes.Time(), DataTypes.Time, id="Time"),
        pytest.param(DataTypes.List(DataTypes.Int64()), DataTypes.List, id="List"),
        pytest.param(DataTypes.Struct(fields={"a": DataTypes.Int64()}), DataTypes.Struct, id="Struct"),
    ],
)
def test_should_return_true_for_matching_class(type_: DataType, expected_class: type) -> None:
    assert isinstance(type_, expected_class)


@pytest.mark.parametrize(
    ("type_", "non_matching_class"),
    [
        pytest.param(DataTypes.Int64(), DataTypes.List, id="Int64 is not List"),
        pytest.param(DataTypes.Int64(), DataTypes.String, id="Int64 is not String"),
        pytest.param(DataTypes.List(DataTypes.Int64()), DataTypes.Int64, id="List is not Int64"),
        pytest.param(DataTypes.Struct(fields={"a": DataTypes.Int64()}), DataTypes.List, id="Struct is not List"),
        pytest.param(DataTypes.Datetime(), DataTypes.Date, id="Datetime is not Date"),
        pytest.param(DataTypes.Duration("us"), DataTypes.Datetime, id="Duration is not Datetime"),
    ],
)
def test_should_return_false_for_non_matching_class(type_: DataType, non_matching_class: type) -> None:
    assert not isinstance(type_, non_matching_class)


def test_should_return_true_for_datatype_base_class() -> None:
    assert isinstance(DataTypes.Int64(), DataType)
