import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(DataType.Float32(), "f32", id="Float32"),
        pytest.param(DataType.Float64(), "f64", id="Float64"),
        pytest.param(DataType.Int8(), "i8", id="Int8"),
        pytest.param(DataType.Int16(), "i16", id="Int16"),
        pytest.param(DataType.Int32(), "i32", id="Int32"),
        pytest.param(DataType.Int64(), "i64", id="Int64"),
        pytest.param(DataType.experimental_Int128(), "i128", id="Int128"),
        pytest.param(DataType.UInt8(), "u8", id="UInt8"),
        pytest.param(DataType.UInt16(), "u16", id="UInt16"),
        pytest.param(DataType.UInt32(), "u32", id="UInt32"),
        pytest.param(DataType.UInt64(), "u64", id="UInt64"),
        pytest.param(DataType.Date(), "date", id="Date"),
        pytest.param(DataType.Datetime(), "datetime[μs]", id="Datetime (local)"),
        pytest.param(DataType.Datetime(time_zone="UTC"), "datetime[μs, UTC]", id="Datetime (UTC)"),
        pytest.param(DataType.Duration("ms"), "duration[ms]", id="Duration (ms)"),
        pytest.param(DataType.Duration("us"), "duration[μs]", id="Duration (us)"),
        pytest.param(DataType.Duration("ns"), "duration[ns]", id="Duration (ns)"),
        pytest.param(DataType.Time(), "time", id="Time"),
        pytest.param(DataType.String(), "str", id="String"),
        pytest.param(DataType.Binary(), "binary", id="Binary"),
        pytest.param(DataType.Boolean(), "bool", id="Boolean"),
        pytest.param(DataType.Null(), "null", id="Null"),
    ],
)
def test_should_return_a_string_representation(type_: DataType, expected: str) -> None:
    assert repr(type_) == expected
