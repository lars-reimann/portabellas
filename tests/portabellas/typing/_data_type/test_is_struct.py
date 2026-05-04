import pytest

from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(
            DataTypes.Struct(fields={"name": DataTypes.String(), "age": DataTypes.Int64()}), True, id="Struct"
        ),
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
        pytest.param(DataTypes.Date(), False, id="Date"),
        pytest.param(DataTypes.Datetime(), False, id="Datetime"),
        pytest.param(DataTypes.Duration("us"), False, id="Duration"),
        pytest.param(DataTypes.Time(), False, id="Time"),
        pytest.param(DataTypes.String(), False, id="String"),
        pytest.param(DataTypes.Binary(), False, id="Binary"),
        pytest.param(DataTypes.Boolean(), False, id="Boolean"),
        pytest.param(DataTypes.Null(), False, id="Null"),
        pytest.param(DataTypes.List(DataTypes.Int64()), False, id="List"),
    ],
)
def test_should_return_whether_type_represents_structs(type_: DataType, expected: bool) -> None:
    assert type_.is_struct == expected
