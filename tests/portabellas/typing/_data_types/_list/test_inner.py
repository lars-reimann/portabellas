import pytest

from portabellas.typing import DataType, DataTypes


@pytest.mark.parametrize(
    ("type_", "expected_inner"),
    [
        pytest.param(DataTypes.List(DataTypes.Int64()), DataTypes.Int64(), id="List of Int64"),
        pytest.param(DataTypes.List(DataTypes.String()), DataTypes.String(), id="List of String"),
        pytest.param(DataTypes.List(DataTypes.Float32()), DataTypes.Float32(), id="List of Float32"),
        pytest.param(
            DataTypes.List(DataTypes.List(DataTypes.Int64())),
            DataTypes.List(DataTypes.Int64()),
            id="Nested List",
        ),
    ],
)
def test_should_return_inner_type(type_: DataTypes.List, expected_inner: DataType) -> None:
    assert type_.inner == expected_inner
