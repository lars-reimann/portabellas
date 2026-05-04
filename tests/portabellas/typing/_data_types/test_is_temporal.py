import pytest

from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(DataTypes.Float32(), False, id="Float32"),
        pytest.param(DataTypes.Float64(), False, id="Float64"),
        pytest.param(DataTypes.Int8(), False, id="Int8"),
        pytest.param(DataTypes.Int16(), False, id="Int16"),
        pytest.param(DataTypes.Int32(), False, id="Int32"),
        pytest.param(DataTypes.Int64(), False, id="Int64"),
        pytest.param(DataTypes.ExperimentalInt128(), False, id="Int128"),
        pytest.param(DataTypes.UInt8(), False, id="UInt8"),
        pytest.param(DataTypes.UInt16(), False, id="UInt16"),
        pytest.param(DataTypes.UInt32(), False, id="UInt32"),
        pytest.param(DataTypes.UInt64(), False, id="UInt64"),
        pytest.param(DataTypes.Date(), True, id="Date"),
        pytest.param(DataTypes.Datetime(), True, id="Datetime"),
        pytest.param(DataTypes.Duration("us"), True, id="Duration"),
        pytest.param(DataTypes.Time(), True, id="Time"),
        pytest.param(DataTypes.String(), False, id="String"),
        pytest.param(DataTypes.Binary(), False, id="Binary"),
        pytest.param(DataTypes.Boolean(), False, id="Boolean"),
        pytest.param(DataTypes.Null(), False, id="Null"),
        pytest.param(DataTypes.List(DataTypes.Datetime()), False, id="List"),
        pytest.param(DataTypes.Struct(fields={"name": DataTypes.String()}), False, id="Struct"),
    ],
)
def test_should_return_whether_type_represents_temporal_data(type_: DataType, expected: bool) -> None:
    assert type_.is_temporal == expected
