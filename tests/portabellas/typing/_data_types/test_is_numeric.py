import pytest

from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(DataTypes.ExperimentalFloat16(), True, id="Float16"),
        pytest.param(DataTypes.Float32(), True, id="Float32"),
        pytest.param(DataTypes.Float64(), True, id="Float64"),
        pytest.param(DataTypes.Int8(), True, id="Int8"),
        pytest.param(DataTypes.Int16(), True, id="Int16"),
        pytest.param(DataTypes.Int32(), True, id="Int32"),
        pytest.param(DataTypes.Int64(), True, id="Int64"),
        pytest.param(DataTypes.ExperimentalInt128(), True, id="Int128"),
        pytest.param(DataTypes.UInt8(), True, id="UInt8"),
        pytest.param(DataTypes.UInt16(), True, id="UInt16"),
        pytest.param(DataTypes.UInt32(), True, id="UInt32"),
        pytest.param(DataTypes.UInt64(), True, id="UInt64"),
        pytest.param(DataTypes.Date(), False, id="Date"),
        pytest.param(DataTypes.Datetime(), False, id="Datetime"),
        pytest.param(DataTypes.Duration("us"), False, id="Duration"),
        pytest.param(DataTypes.Time(), False, id="Time"),
        pytest.param(DataTypes.String(), False, id="String"),
        pytest.param(DataTypes.Binary(), False, id="Binary"),
        pytest.param(DataTypes.Boolean(), False, id="Boolean"),
        pytest.param(DataTypes.Null(), False, id="Null"),
        pytest.param(DataTypes.Unknown(), False, id="Unknown"),
        pytest.param(DataTypes.List(DataTypes.Int64()), False, id="List"),
        pytest.param(DataTypes.Struct(fields={"name": DataTypes.String()}), False, id="Struct"),
    ],
)
def test_should_return_whether_type_represents_numbers(type_: DataType, expected: bool) -> None:
    assert type_.is_numeric == expected
