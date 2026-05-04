import pytest

from portabellas.typing import DataType
from portabellas.typing._data_type import List


@pytest.mark.parametrize(
    ("type_", "expected_inner"),
    [
        pytest.param(DataType.List(DataType.Int64()), DataType.Int64(), id="List of Int64"),
        pytest.param(DataType.List(DataType.String()), DataType.String(), id="List of String"),
        pytest.param(DataType.List(DataType.Float32()), DataType.Float32(), id="List of Float32"),
        pytest.param(
            DataType.List(DataType.List(DataType.Int64())),
            DataType.List(DataType.Int64()),
            id="Nested List",
        ),
    ],
)
def test_should_return_inner_type(type_: List, expected_inner: DataType) -> None:
    assert type_.inner == expected_inner
