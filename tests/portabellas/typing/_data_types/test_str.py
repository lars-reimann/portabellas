import pytest

from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(DataTypes.ExperimentalFloat16(), "f16", id="Float16"),
        pytest.param(DataTypes.Float32(), "f32", id="Float32"),
        pytest.param(DataTypes.Float64(), "f64", id="Float64"),
        pytest.param(DataTypes.Int8(), "i8", id="Int8"),
        pytest.param(DataTypes.Int16(), "i16", id="Int16"),
        pytest.param(DataTypes.Int32(), "i32", id="Int32"),
        pytest.param(DataTypes.Int64(), "i64", id="Int64"),
        pytest.param(DataTypes.ExperimentalInt128(), "i128", id="Int128"),
        pytest.param(DataTypes.UInt8(), "u8", id="UInt8"),
        pytest.param(DataTypes.UInt16(), "u16", id="UInt16"),
        pytest.param(DataTypes.UInt32(), "u32", id="UInt32"),
        pytest.param(DataTypes.UInt64(), "u64", id="UInt64"),
        pytest.param(DataTypes.Date(), "date", id="Date"),
        pytest.param(DataTypes.Datetime(), "datetime[μs]", id="Datetime (local)"),
        pytest.param(DataTypes.Datetime(time_zone="UTC"), "datetime[μs, UTC]", id="Datetime (UTC)"),
        pytest.param(DataTypes.Duration("ms"), "duration[ms]", id="Duration (ms)"),
        pytest.param(DataTypes.Duration("us"), "duration[μs]", id="Duration (us)"),
        pytest.param(DataTypes.Duration("ns"), "duration[ns]", id="Duration (ns)"),
        pytest.param(DataTypes.Time(), "time", id="Time"),
        pytest.param(DataTypes.String(), "str", id="String"),
        pytest.param(DataTypes.Binary(), "binary", id="Binary"),
        pytest.param(DataTypes.Boolean(), "bool", id="Boolean"),
        pytest.param(DataTypes.Null(), "null", id="Null"),
        pytest.param(DataTypes.Unknown(), "unknown", id="Unknown"),
        pytest.param(DataTypes.List(DataTypes.Int64()), "list[i64]", id="List of Int64"),
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}),
            "struct[2]",
            id="Struct",
        ),
    ],
)
def test_should_return_a_string_representation(type_: DataType, expected: str) -> None:
    assert str(type_) == expected
