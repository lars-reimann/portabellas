import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("type_", "expected_class"),
    [
        pytest.param(DataType.Null(), DataType.Null, id="Null"),
        pytest.param(DataType.Boolean(), DataType.Boolean, id="Boolean"),
        pytest.param(DataType.Int8(), DataType.Int8, id="Int8"),
        pytest.param(DataType.Int16(), DataType.Int16, id="Int16"),
        pytest.param(DataType.Int32(), DataType.Int32, id="Int32"),
        pytest.param(DataType.Int64(), DataType.Int64, id="Int64"),
        pytest.param(DataType.experimental_Int128(), DataType.experimental_Int128, id="Int128"),
        pytest.param(DataType.UInt8(), DataType.UInt8, id="UInt8"),
        pytest.param(DataType.UInt16(), DataType.UInt16, id="UInt16"),
        pytest.param(DataType.UInt32(), DataType.UInt32, id="UInt32"),
        pytest.param(DataType.UInt64(), DataType.UInt64, id="UInt64"),
        pytest.param(DataType.Float32(), DataType.Float32, id="Float32"),
        pytest.param(DataType.Float64(), DataType.Float64, id="Float64"),
        pytest.param(DataType.String(), DataType.String, id="String"),
        pytest.param(DataType.Binary(), DataType.Binary, id="Binary"),
        pytest.param(DataType.Date(), DataType.Date, id="Date"),
        pytest.param(DataType.Datetime(), DataType.Datetime, id="Datetime"),
        pytest.param(DataType.Datetime(time_zone="UTC"), DataType.Datetime, id="Datetime with time zone"),
        pytest.param(DataType.Duration("us"), DataType.Duration, id="Duration"),
        pytest.param(DataType.Time(), DataType.Time, id="Time"),
        pytest.param(DataType.List(DataType.Int64()), DataType.List, id="List"),
        pytest.param(DataType.Struct(fields={"a": DataType.Int64()}), DataType.Struct, id="Struct"),
    ],
)
def test_should_return_true_for_matching_class(type_: DataType, expected_class: type) -> None:
    assert isinstance(type_, expected_class)


@pytest.mark.parametrize(
    ("type_", "non_matching_class"),
    [
        pytest.param(DataType.Int64(), DataType.List, id="Int64 is not List"),
        pytest.param(DataType.Int64(), DataType.String, id="Int64 is not String"),
        pytest.param(DataType.List(DataType.Int64()), DataType.Int64, id="List is not Int64"),
        pytest.param(DataType.Struct(fields={"a": DataType.Int64()}), DataType.List, id="Struct is not List"),
        pytest.param(DataType.Datetime(), DataType.Date, id="Datetime is not Date"),
        pytest.param(DataType.Duration("us"), DataType.Datetime, id="Duration is not Datetime"),
    ],
)
def test_should_return_false_for_non_matching_class(type_: DataType, non_matching_class: type) -> None:
    assert not isinstance(type_, non_matching_class)


def test_should_return_true_for_datatype_base_class() -> None:
    assert isinstance(DataType.Int64(), DataType)
