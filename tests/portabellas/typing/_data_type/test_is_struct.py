import pytest

from portabellas.typing import DataType


@pytest.mark.parametrize(
    ("type_", "expected"),
    [
        pytest.param(DataType.Struct(fields={"name": DataType.String(), "age": DataType.Int64()}), True, id="Struct"),
        pytest.param(DataType.Float32(), False, id="Float32"),
        pytest.param(DataType.Int64(), False, id="Int64"),
        pytest.param(DataType.String(), False, id="String"),
        pytest.param(DataType.Boolean(), False, id="Boolean"),
    ],
)
def test_should_return_whether_type_is_struct(type_: DataType, expected: bool) -> None:
    assert type_.is_struct == expected
