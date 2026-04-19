import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(DataType.Float32(), True, id="Float32"),
        pytest.param(DataType.Float64(), True, id="Float64"),
        pytest.param(DataType.Int8(), True, id="Int8"),
        pytest.param(DataType.Int16(), True, id="Int16"),
        pytest.param(DataType.Int32(), True, id="Int32"),
        pytest.param(DataType.Int64(), True, id="Int64"),
        pytest.param(DataType.experimental_Int128(), True, id="Int128"),
        pytest.param(DataType.UInt8(), True, id="UInt8"),
        pytest.param(DataType.UInt16(), True, id="UInt16"),
        pytest.param(DataType.UInt32(), True, id="UInt32"),
        pytest.param(DataType.UInt64(), True, id="UInt64"),
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
def test_should_return_whether_type_represents_numbers(type_: DataType, expected: bool) -> None:
    assert type_.is_numeric == expected
