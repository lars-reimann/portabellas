import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(DataType.Float32(), False, id="Float32"),
        pytest.param(DataType.Float64(), False, id="Float64"),
        pytest.param(DataType.Int8(), True, id="Int8"),
        pytest.param(DataType.Int16(), True, id="Int16"),
        pytest.param(DataType.Int32(), True, id="Int32"),
        pytest.param(DataType.Int64(), True, id="Int64"),
        pytest.param(DataType.experimental_Int128(), True, id="Int128"),
        pytest.param(DataType.UInt8(), False, id="UInt8"),
        pytest.param(DataType.UInt16(), False, id="UInt16"),
        pytest.param(DataType.UInt32(), False, id="UInt32"),
        pytest.param(DataType.UInt64(), False, id="UInt64"),
        pytest.param(DataType.Date(), False, id="Date"),
        pytest.param(DataType.Datetime(), False, id="Datetime"),
        pytest.param(DataType.Duration("us"), False, id="Duration"),
        pytest.param(DataType.Time(), False, id="Time"),
        pytest.param(DataType.String(), False, id="String"),
        pytest.param(DataType.Binary(), False, id="Binary"),
        pytest.param(DataType.Boolean(), False, id="Boolean"),
        pytest.param(DataType.Null(), False, id="Null"),
    ],
)
def test_should_return_whether_type_represents_signed_ints(type_: DataType, expected: bool) -> None:
    assert type_.is_signed_int == expected
